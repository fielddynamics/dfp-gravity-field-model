"""
Traversal Analyzer
==================

Single-pass analysis engine for pi base-8 traversal through the stellated
octahedron. Processes N digits ONCE, producing a complete step-by-step ledger
that all cross-check tests query against.

Design principle:
    One pass. One ledger. Many tests.
    The traversal is deterministic — pi doesn't change. Process once, record
    everything, then every test is a query against the recorded data.

The analyzer captures:
    1. Step ledger     — every step with full state and flags
    2. Face state      — per-face vertex accumulation and completion tracking
    3. Orbit records   — per-orbit face coverage analysis
    4. Macro-cycles    — face completion order across full coverage cycles
    5. Crossing log    — every TetA ↔ TetB transition
    6. Anomaly report  — anything unexpected, with step-level detail

Usage:
    analyzer = TraversalAnalyzer(n_digits=1000)
    analyzer.run()

    # Query the ledger
    ledger = analyzer.steps          # List of StepRecord
    orbits = analyzer.orbits         # List of OrbitRecord
    cycles = analyzer.macro_cycles   # List of MacroCycleRecord
    report = analyzer.get_report()   # Summary dict
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from collections import Counter

from gravity_field_model.common.pi_data import get_pi_base8


# =============================================================================
# GEOMETRY CONSTANTS (authoritative definitions)
# =============================================================================

TETA = frozenset({1, 2, 4, 7})
TETB = frozenset({0, 3, 5, 6})

FACES = {
    'FACE_A1': frozenset({2, 4, 7}),
    'FACE_A2': frozenset({1, 4, 7}),
    'FACE_A4': frozenset({1, 2, 7}),
    'FACE_A7': frozenset({1, 2, 4}),   # TIME
    'FACE_B0': frozenset({3, 5, 6}),   # TIME
    'FACE_B3': frozenset({0, 5, 6}),
    'FACE_B5': frozenset({0, 3, 6}),
    'FACE_B6': frozenset({0, 3, 5}),
}

TIME_FACES = frozenset({'FACE_A7', 'FACE_B0'})
SPATIAL_FACES = frozenset(FACES.keys()) - TIME_FACES

TETA_FACES = frozenset({'FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7'})
TETB_FACES = frozenset({'FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6'})

FACE_NAMES_SORTED = sorted(FACES.keys())


def get_tet(vertex: int) -> str:
    """Return 'A' or 'B' for a vertex."""
    return 'A' if vertex in TETA else 'B'


def get_faces_for_vertex(vertex: int) -> List[str]:
    """Return list of face names containing this vertex."""
    return [name for name, verts in FACES.items() if vertex in verts]


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class StepRecord:
    """Complete state at a single traversal step."""
    step: int
    digit: int
    cumsum: int
    vertex: int
    tet: str
    orbit: int
    complement: int
    comp_tet: str
    faces_touched: List[str]

    # Flags
    is_orbit_complete: bool
    is_tet_crossing: bool
    is_zero_digit: bool
    is_vertex_repeat: bool

    # Face events at this step
    faces_new_vertex: List[str]       # Faces that got a NEW vertex from this step
    faces_redundant: List[str]        # Faces that got a REDUNDANT hit
    faces_completed: List[str]        # Faces that completed on this step


@dataclass
class FaceTracker:
    """Tracks vertex accumulation for a single face across the traversal."""
    name: str
    required_vertices: frozenset
    vertices_seen: set = field(default_factory=set)
    vertex_read_order: list = field(default_factory=list)
    completion_step: int = -1
    redundant_hits: int = 0
    is_complete: bool = False

    def touch(self, vertex: int, step: int) -> Tuple[bool, bool]:
        """
        Record a vertex hit.
        Returns: (is_new, just_completed)
        """
        if vertex not in self.required_vertices:
            return False, False  # Vertex doesn't belong to this face

        if vertex in self.vertices_seen:
            self.redundant_hits += 1
            return False, False  # Redundant — vertex already counted

        self.vertices_seen.add(vertex)
        self.vertex_read_order.append((vertex, step))

        if self.vertices_seen == self.required_vertices:
            self.is_complete = True
            self.completion_step = step
            return True, True  # New vertex AND face just completed

        return True, False  # New vertex, face not yet complete

    def reset(self):
        """Reset for next macro-cycle."""
        self.vertices_seen = set()
        self.vertex_read_order = []
        self.completion_step = -1
        self.redundant_hits = 0
        self.is_complete = False


@dataclass
class OrbitRecord:
    """Analysis of a single orbit (cumsum traversal of 8 units)."""
    orbit_number: int
    start_step: int
    end_step: int
    steps_in_orbit: int
    digits_in_orbit: List[int]
    vertices_in_orbit: List[int]

    # Face analysis within this orbit
    face_new_hits: Dict[str, int] = field(default_factory=dict)
    face_redundant_hits: Dict[str, int] = field(default_factory=dict)
    face_completions: List[str] = field(default_factory=list)

    # Crossing analysis
    tet_crossings: int = 0
    teta_steps: int = 0
    tetb_steps: int = 0
    zero_digit_steps: int = 0

    # Anomalies detected in this orbit
    anomalies: List[str] = field(default_factory=list)


@dataclass
class MacroCycleRecord:
    """
    One complete coverage of all 8 faces.
    A macro-cycle starts when face tracking resets and ends when all 8 faces
    have completed at least once.
    """
    cycle_number: int
    start_step: int
    end_step: int
    completion_order: List[Tuple[str, int]]   # (face_name, step) in order of completion

    # 3+1 analysis per tetrahedron
    teta_order: List[str] = field(default_factory=list)
    tetb_order: List[str] = field(default_factory=list)
    teta_3plus1: bool = False    # Did 3 SPATIAL complete before TIME in TetA?
    tetb_3plus1: bool = False    # Did 3 SPATIAL complete before TIME in TetB?

    # Per-face trigram read order
    trigram_orders: Dict[str, List[Tuple[int, int]]] = field(default_factory=dict)


@dataclass
class CrossingRecord:
    """A single TetA ↔ TetB transition."""
    step: int
    from_tet: str
    to_tet: str
    from_vertex: int
    to_vertex: int
    complement_of_to: int
    complement_tet: str
    complement_valid: bool   # Does 7-v map to opposite tet?


@dataclass
class Anomaly:
    """A detected anomaly with full context."""
    code: str
    severity: str          # CRITICAL, ERROR, WARNING, INFO
    step: int
    orbit: int
    description: str
    details: Dict = field(default_factory=dict)


# =============================================================================
# TRAVERSAL ANALYZER
# =============================================================================

class TraversalAnalyzer:
    """
    Runs the full traversal for N digits and produces the golden ledger.

    Usage:
        analyzer = TraversalAnalyzer(n_digits=1000)
        analyzer.run()
        report = analyzer.get_report()
    """

    def __init__(self, n_digits: int = 1000):
        self.n_digits = n_digits
        self.digits = get_pi_base8(n_digits, include_integer=True)

        # Primary outputs
        self.steps: List[StepRecord] = []
        self.orbits: List[OrbitRecord] = []
        self.macro_cycles: List[MacroCycleRecord] = []
        self.crossings: List[CrossingRecord] = []
        self.anomalies: List[Anomaly] = []

        # Internal state
        self._face_trackers: Dict[str, FaceTracker] = {}
        self._cycle_face_trackers: Dict[str, FaceTracker] = {}
        self._has_run = False

    def run(self):
        """Execute the full analysis. Idempotent — only runs once."""
        if self._has_run:
            return
        self._has_run = True

        self._run_traversal()
        self._analyze_orbits()
        self._analyze_macro_cycles()
        self._detect_anomalies()

    # -----------------------------------------------------------------
    # PASS 1: Step-by-step traversal with full state recording
    # -----------------------------------------------------------------

    def _run_traversal(self):
        """Walk every digit, record every step."""
        # Initialize face trackers (cumulative — track total progress)
        self._face_trackers = {
            name: FaceTracker(name=name, required_vertices=verts)
            for name, verts in FACES.items()
        }

        cumsum = 0
        prev_vertex = None
        prev_tet = None

        for step_idx, digit in enumerate(self.digits):
            cumsum += digit
            vertex = cumsum % 8
            tet = get_tet(vertex)
            orbit = cumsum // 8
            complement = 7 - vertex
            comp_tet = get_tet(complement)

            # Flags
            is_orbit_complete = cumsum > 0 and cumsum % 8 == 0
            is_tet_crossing = prev_tet is not None and tet != prev_tet
            is_zero_digit = digit == 0
            is_vertex_repeat = prev_vertex is not None and vertex == prev_vertex

            # Face analysis for this step
            faces_touched = get_faces_for_vertex(vertex)
            faces_new = []
            faces_redundant = []
            faces_completed = []

            for fname in faces_touched:
                tracker = self._face_trackers[fname]
                is_new, just_completed = tracker.touch(vertex, step_idx)
                if is_new:
                    faces_new.append(fname)
                    if just_completed:
                        faces_completed.append(fname)
                else:
                    if vertex in tracker.required_vertices:
                        faces_redundant.append(fname)

            # Record crossing
            if is_tet_crossing:
                crossing = CrossingRecord(
                    step=step_idx,
                    from_tet=prev_tet,
                    to_tet=tet,
                    from_vertex=prev_vertex,
                    to_vertex=vertex,
                    complement_of_to=complement,
                    complement_tet=comp_tet,
                    complement_valid=(comp_tet != tet),
                )
                self.crossings.append(crossing)

            # Build step record
            record = StepRecord(
                step=step_idx,
                digit=digit,
                cumsum=cumsum,
                vertex=vertex,
                tet=tet,
                orbit=orbit,
                complement=complement,
                comp_tet=comp_tet,
                faces_touched=faces_touched,
                is_orbit_complete=is_orbit_complete,
                is_tet_crossing=is_tet_crossing,
                is_zero_digit=is_zero_digit,
                is_vertex_repeat=is_vertex_repeat,
                faces_new_vertex=faces_new,
                faces_redundant=faces_redundant,
                faces_completed=faces_completed,
            )
            self.steps.append(record)

            prev_vertex = vertex
            prev_tet = tet

    # -----------------------------------------------------------------
    # PASS 2: Orbit-level analysis (derived from step ledger)
    # -----------------------------------------------------------------

    def _analyze_orbits(self):
        """Group steps into orbits and analyze face coverage per orbit."""
        if not self.steps:
            return

        current_orbit = 0
        orbit_start = 0
        orbit_digits = []
        orbit_vertices = []
        orbit_face_new = Counter()
        orbit_face_redundant = Counter()
        orbit_face_completions = []
        orbit_tet_crossings = 0
        orbit_teta = 0
        orbit_tetb = 0
        orbit_zero_digits = 0

        for s in self.steps:
            step_orbit = s.cumsum // 8 if s.cumsum > 0 else 0

            # Check if we've crossed into a new orbit
            if s.is_orbit_complete or (step_orbit > current_orbit and s.step > 0):
                # Save current orbit (but not before the first step)
                if s.step > 0 and (orbit_digits or current_orbit == 0):
                    self._save_orbit(
                        current_orbit, orbit_start, s.step - 1,
                        orbit_digits, orbit_vertices,
                        orbit_face_new, orbit_face_redundant,
                        orbit_face_completions,
                        orbit_tet_crossings, orbit_teta, orbit_tetb,
                        orbit_zero_digits,
                    )

                # Reset for new orbit
                current_orbit = step_orbit
                orbit_start = s.step
                orbit_digits = []
                orbit_vertices = []
                orbit_face_new = Counter()
                orbit_face_redundant = Counter()
                orbit_face_completions = []
                orbit_tet_crossings = 0
                orbit_teta = 0
                orbit_tetb = 0
                orbit_zero_digits = 0

            # Accumulate
            orbit_digits.append(s.digit)
            orbit_vertices.append(s.vertex)
            for f in s.faces_new_vertex:
                orbit_face_new[f] += 1
            for f in s.faces_redundant:
                orbit_face_redundant[f] += 1
            orbit_face_completions.extend(s.faces_completed)
            if s.is_tet_crossing:
                orbit_tet_crossings += 1
            if s.tet == 'A':
                orbit_teta += 1
            else:
                orbit_tetb += 1
            if s.is_zero_digit:
                orbit_zero_digits += 1

        # Save final orbit
        if orbit_digits:
            self._save_orbit(
                current_orbit, orbit_start, len(self.steps) - 1,
                orbit_digits, orbit_vertices,
                orbit_face_new, orbit_face_redundant,
                orbit_face_completions,
                orbit_tet_crossings, orbit_teta, orbit_tetb,
                orbit_zero_digits,
            )

    def _save_orbit(self, orbit_num, start, end, digits, vertices,
                    face_new, face_redundant, face_completions,
                    tet_crossings, teta, tetb, zero_digits):
        """Package orbit data into an OrbitRecord."""
        record = OrbitRecord(
            orbit_number=orbit_num,
            start_step=start,
            end_step=end,
            steps_in_orbit=end - start + 1,
            digits_in_orbit=list(digits),
            vertices_in_orbit=list(vertices),
            face_new_hits=dict(face_new),
            face_redundant_hits=dict(face_redundant),
            face_completions=list(face_completions),
            tet_crossings=tet_crossings,
            teta_steps=teta,
            tetb_steps=tetb,
            zero_digit_steps=zero_digits,
        )
        self.orbits.append(record)

    # -----------------------------------------------------------------
    # PASS 3: Macro-cycle analysis (face completion order)
    # -----------------------------------------------------------------

    def _analyze_macro_cycles(self):
        """
        Track macro-cycles: periods where all 8 faces complete.
        After all 8 complete, reset and start a new cycle.
        """
        cycle_trackers = {
            name: FaceTracker(name=name, required_vertices=verts)
            for name, verts in FACES.items()
        }
        cycle_num = 0
        cycle_start = 0
        completion_order = []

        for s in self.steps:
            vertex = s.vertex

            for fname in get_faces_for_vertex(vertex):
                tracker = cycle_trackers[fname]
                if tracker.is_complete:
                    continue
                is_new, just_completed = tracker.touch(vertex, s.step)
                if just_completed:
                    completion_order.append((fname, s.step))

            # Check if all 8 faces are complete
            if all(t.is_complete for t in cycle_trackers.values()):
                # Build macro-cycle record
                cycle = self._build_macro_cycle(
                    cycle_num, cycle_start, s.step,
                    completion_order, cycle_trackers,
                )
                self.macro_cycles.append(cycle)

                # Reset for next cycle
                cycle_num += 1
                cycle_start = s.step + 1
                completion_order = []
                for t in cycle_trackers.values():
                    t.reset()

    def _build_macro_cycle(self, cycle_num, start, end,
                           completion_order, trackers) -> MacroCycleRecord:
        """Build a MacroCycleRecord with 3+1 analysis."""
        # Separate by tetrahedron
        teta_order = [f for f, _ in completion_order if f in TETA_FACES]
        tetb_order = [f for f, _ in completion_order if f in TETB_FACES]

        # 3+1 check using completion STEPS, not list position.
        # A tet has 3+1 if all 3 SPATIAL faces complete at or before
        # the 1 TIME face (weak ordering: ties count as "before").
        #
        # Pi's encoding visits both tets explicitly — the step numbers
        # are the ground truth for completion order.
        teta_steps = {f: s for f, s in completion_order if f in TETA_FACES}
        tetb_steps = {f: s for f, s in completion_order if f in TETB_FACES}

        teta_3plus1 = False
        if len(teta_steps) == 4 and 'FACE_A7' in teta_steps:
            time_step = teta_steps['FACE_A7']
            spatial_steps = [s for f, s in teta_steps.items() if f != 'FACE_A7']
            teta_3plus1 = all(s <= time_step for s in spatial_steps)

        tetb_3plus1 = False
        if len(tetb_steps) == 4 and 'FACE_B0' in tetb_steps:
            time_step = tetb_steps['FACE_B0']
            spatial_steps = [s for f, s in tetb_steps.items() if f != 'FACE_B0']
            tetb_3plus1 = all(s <= time_step for s in spatial_steps)

        # Collect trigram read orders
        trigram_orders = {}
        for name, tracker in trackers.items():
            trigram_orders[name] = list(tracker.vertex_read_order)

        return MacroCycleRecord(
            cycle_number=cycle_num,
            start_step=start,
            end_step=end,
            completion_order=list(completion_order),
            teta_order=teta_order,
            tetb_order=tetb_order,
            teta_3plus1=teta_3plus1,
            tetb_3plus1=tetb_3plus1,
            trigram_orders=trigram_orders,
        )

    # -----------------------------------------------------------------
    # PASS 4: Anomaly detection
    # -----------------------------------------------------------------

    def _detect_anomalies(self):
        """Scan the ledger for anomalies."""
        self._check_complement_integrity()
        self._check_cumsum_integrity()
        self._check_zero_digit_clusters()
        self._check_crossing_gaps()

    def _check_complement_integrity(self):
        """CRITICAL: verify 7-v maps to opposite tet at every step."""
        for s in self.steps:
            if s.comp_tet == s.tet:
                self.anomalies.append(Anomaly(
                    code='COMPLEMENT_VIOLATION',
                    severity='CRITICAL',
                    step=s.step,
                    orbit=s.orbit,
                    description=(
                        f"Step {s.step}: vertex {s.vertex} (Tet{s.tet}) has "
                        f"complement {s.complement} also in Tet{s.comp_tet}. "
                        f"Field Origin coupling is BROKEN."
                    ),
                    details={'vertex': s.vertex, 'complement': s.complement},
                ))

    def _check_cumsum_integrity(self):
        """Verify cumsum == running sum of all digits."""
        running_sum = 0
        for s in self.steps:
            running_sum += s.digit
            if s.cumsum != running_sum:
                self.anomalies.append(Anomaly(
                    code='CUMSUM_MISMATCH',
                    severity='CRITICAL',
                    step=s.step,
                    orbit=s.orbit,
                    description=(
                        f"Step {s.step}: cumsum={s.cumsum} but running sum "
                        f"of digits = {running_sum}."
                    ),
                ))
            if s.vertex != s.cumsum % 8:
                self.anomalies.append(Anomaly(
                    code='VERTEX_MISMATCH',
                    severity='CRITICAL',
                    step=s.step,
                    orbit=s.orbit,
                    description=(
                        f"Step {s.step}: vertex={s.vertex} but cumsum%8 = "
                        f"{s.cumsum % 8}."
                    ),
                ))

    def _check_zero_digit_clusters(self):
        """Flag clusters of 3+ consecutive zero digits."""
        run_length = 0
        run_start = -1
        for s in self.steps:
            if s.is_zero_digit:
                if run_length == 0:
                    run_start = s.step
                run_length += 1
            else:
                if run_length >= 3:
                    self.anomalies.append(Anomaly(
                        code='STALL_CLUSTER',
                        severity='INFO',
                        step=run_start,
                        orbit=self.steps[run_start].orbit,
                        description=(
                            f"Steps {run_start}-{run_start + run_length - 1}: "
                            f"{run_length} consecutive zero digits (stall cluster)."
                        ),
                        details={'length': run_length, 'start': run_start},
                    ))
                run_length = 0

    def _check_crossing_gaps(self):
        """Flag 8+ consecutive steps in same tetrahedron."""
        if not self.steps:
            return
        run_tet = self.steps[0].tet
        run_length = 1
        run_start = 0
        for s in self.steps[1:]:
            if s.tet == run_tet:
                run_length += 1
            else:
                if run_length >= 8:
                    self.anomalies.append(Anomaly(
                        code='CROSSING_GAP',
                        severity='INFO',
                        step=run_start,
                        orbit=self.steps[run_start].orbit,
                        description=(
                            f"Steps {run_start}-{run_start + run_length - 1}: "
                            f"{run_length} consecutive steps in Tet{run_tet}."
                        ),
                        details={'length': run_length, 'tet': run_tet},
                    ))
                run_tet = s.tet
                run_length = 1
                run_start = s.step

    # -----------------------------------------------------------------
    # REPORT
    # -----------------------------------------------------------------

    def get_report(self) -> Dict:
        """Return comprehensive analysis summary."""
        if not self._has_run:
            self.run()

        critical_anomalies = [a for a in self.anomalies if a.severity == 'CRITICAL']
        error_anomalies = [a for a in self.anomalies if a.severity == 'ERROR']
        warning_anomalies = [a for a in self.anomalies if a.severity == 'WARNING']
        info_anomalies = [a for a in self.anomalies if a.severity == 'INFO']

        # 3+1 statistics
        cycles_a_3plus1 = sum(1 for c in self.macro_cycles if c.teta_3plus1)
        cycles_b_3plus1 = sum(1 for c in self.macro_cycles if c.tetb_3plus1)
        cycles_both_3plus1 = sum(
            1 for c in self.macro_cycles
            if c.teta_3plus1 and c.tetb_3plus1
        )

        # Complement integrity
        complement_violations = sum(
            1 for a in self.anomalies if a.code == 'COMPLEMENT_VIOLATION'
        )

        # Crossing stats
        total_crossings = len(self.crossings)
        crossing_rate = total_crossings / len(self.steps) if self.steps else 0

        return {
            'total_steps': len(self.steps),
            'total_digits': self.n_digits,
            'total_orbits': len(self.orbits),
            'total_macro_cycles': len(self.macro_cycles),
            'total_crossings': total_crossings,
            'crossing_rate': crossing_rate,

            # Integrity
            'complement_violations': complement_violations,
            'cumsum_errors': sum(1 for a in self.anomalies if a.code == 'CUMSUM_MISMATCH'),
            'vertex_errors': sum(1 for a in self.anomalies if a.code == 'VERTEX_MISMATCH'),

            # 3+1 pattern
            'cycles_teta_3plus1': cycles_a_3plus1,
            'cycles_tetb_3plus1': cycles_b_3plus1,
            'cycles_both_3plus1': cycles_both_3plus1,
            'cycles_teta_3plus1_rate': cycles_a_3plus1 / len(self.macro_cycles) if self.macro_cycles else 0,
            'cycles_tetb_3plus1_rate': cycles_b_3plus1 / len(self.macro_cycles) if self.macro_cycles else 0,

            # Anomaly counts by severity
            'anomalies_critical': len(critical_anomalies),
            'anomalies_error': len(error_anomalies),
            'anomalies_warning': len(warning_anomalies),
            'anomalies_info': len(info_anomalies),
            'anomalies_total': len(self.anomalies),
        }


# =============================================================================
# MODULE-LEVEL SINGLETON
# =============================================================================
# All tests in test_engine_crosschecks.py share this single instance.
# Created on first import, run on first access.

_analyzer_instance: Optional[TraversalAnalyzer] = None


def get_analyzer(n_digits: int = 1000) -> TraversalAnalyzer:
    """
    Get the shared TraversalAnalyzer instance.
    Created once, shared across all tests.
    """
    global _analyzer_instance
    if _analyzer_instance is None or _analyzer_instance.n_digits != n_digits:
        _analyzer_instance = TraversalAnalyzer(n_digits=n_digits)
        _analyzer_instance.run()
    return _analyzer_instance
