"""
Tetragram Analyzer
====================

Sub-face resolution analysis of the pi base-8 traversal.

Each coupling port (face) of the stellated octahedron is a triangle with
3 vertices. Decomposed as a triforce, each face has 4 tetragrams:

    3 CORNER tetragrams — one per vertex, activated when that vertex is read
    1 CENTRAL tetragram — activated when all 3 corners are active (face complete)

Total: 8 faces × 4 tetragrams = 32 tetragrams.

The pi encoding processes at this level. Each digit drives a vertex visit,
which activates corner tetragrams in every face containing that vertex.
This analyzer tracks the activation of all 32 tetragrams step by step,
producing metrics at a resolution BELOW the face level.

Architecture:
    Wraps the existing TraversalAnalyzer. Does NOT re-run the traversal.
    Instead, it performs a second pass over the step ledger and the
    macro-cycle trigram_orders to derive tetragram-level records.

Data Structures:
    TetragramID       — Unique identifier for each of the 32 tetragrams
    CornerActivation    — Record of a single corner tetragram firing
    CentralActivation   — Record of a central tetragram firing
    FaceProgression     — Step-by-step build-up of a face's trigram within a cycle
    TetragramCycle    — Complete tetragram analysis for one macro-cycle
    TetragramReport   — Aggregate statistics across all cycles

Usage:
    from traversal_analyzer import get_analyzer
    from tetragram_analyzer import TetragramAnalyzer

    engine = get_analyzer(10000)
    sub = TetragramAnalyzer(engine)
    sub.run()

    cycles = sub.cycles          # List of TetragramCycle
    report = sub.get_report()    # Aggregate statistics dict
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from collections import Counter, defaultdict
import math

from .traversal_analyzer import (
    TraversalAnalyzer, get_analyzer,
    FACES, TIME_FACES, SPATIAL_FACES,
    TETA_FACES, TETB_FACES,
    FACE_NAMES_SORTED,
    get_tet, get_faces_for_vertex,
)


# =============================================================================
# TETRAGRAM GEOMETRY
# =============================================================================

# Build the 32 tetragram IDs.
# Each face has 3 corners (keyed by vertex) and 1 central.
# Format: "FACE_A1.C2", "FACE_A1.C4", "FACE_A1.C7", "FACE_A1.X"
# where C<v> = corner for vertex v, X = central.

TETRAGRAMS = {}   # id -> {face, type, vertex (or None)}
FACE_CORNERS = {}   # face -> sorted list of corner tetragram IDs
FACE_CENTRAL = {}   # face -> central tetragram ID
CORNER_TO_SUB = {}  # (face, vertex) -> tetragram ID
ALL_CORNER_IDS = []
ALL_CENTRAL_IDS = []
ALL_TETRAGRAM_IDS = []

for face_name in FACE_NAMES_SORTED:
    verts = sorted(FACES[face_name])
    corners = []
    for v in verts:
        sid = f"{face_name}.C{v}"
        TETRAGRAMS[sid] = {
            'face': face_name,
            'type': 'corner',
            'vertex': v,
        }
        CORNER_TO_SUB[(face_name, v)] = sid
        corners.append(sid)
        ALL_CORNER_IDS.append(sid)
    central_id = f"{face_name}.X"
    TETRAGRAMS[central_id] = {
        'face': face_name,
        'type': 'central',
        'vertex': None,
    }
    FACE_CORNERS[face_name] = corners
    FACE_CENTRAL[face_name] = central_id
    ALL_CENTRAL_IDS.append(central_id)

ALL_TETRAGRAM_IDS = ALL_CORNER_IDS + ALL_CENTRAL_IDS

TOTAL_TETRAGRAMS = len(ALL_TETRAGRAM_IDS)   # 32
TOTAL_CORNERS = len(ALL_CORNER_IDS)     # 24
TOTAL_CENTRALS = len(ALL_CENTRAL_IDS)   # 8


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CornerActivation:
    """A single corner tetragram activation event."""
    tetragram_id: str
    face: str
    vertex: int
    step: int
    read_position: int          # 1st, 2nd, or 3rd read for this face (1-indexed)
    gap_from_previous: int      # Steps since previous read for this face (-1 if first)


@dataclass
class CentralActivation:
    """A central tetragram activation (= face completion)."""
    tetragram_id: str
    face: str
    step: int                   # Same step as the 3rd corner activation
    triggering_corner: str      # Which corner's activation triggered this
    cycle_rank: int             # 1st, 2nd, ..., 8th face to complete in this cycle


@dataclass
class FaceProgression:
    """
    Step-by-step build-up of one face's trigram within a single macro-cycle.

    Tracks the 3 corner activations and the central activation, including
    inter-read gaps and the total span from first read to completion.
    """
    face: str
    cycle: int

    # The 3 reads in order
    reads: List[CornerActivation] = field(default_factory=list)

    # Central activation
    central: Optional[CentralActivation] = None

    # Derived
    span: int = 0               # Steps from 1st read to completion
    gap_1_to_2: int = -1        # Steps between 1st and 2nd read
    gap_2_to_3: int = -1        # Steps between 2nd and 3rd read
    trigram: Tuple = ()          # Vertex ordering tuple, e.g. (2, 7, 4)

    @property
    def is_complete(self) -> bool:
        return len(self.reads) == 3 and self.central is not None


@dataclass
class TetragramCycle:
    """
    Complete tetragram analysis for one macro-cycle.

    Contains the full activation sequence of all 32 tetragrams,
    per-face progressions, and integrity cross-checks.
    """
    cycle_number: int
    start_step: int
    end_step: int

    # Full activation sequence in chronological order
    activation_sequence: List[Tuple[str, int]] = field(default_factory=list)

    # Per-face progressions
    face_progressions: Dict[str, FaceProgression] = field(default_factory=dict)

    # Counts
    total_corner_activations: int = 0
    total_central_activations: int = 0
    total_activations: int = 0

    # Integrity flags
    all_32_active: bool = False
    all_corners_before_centrals: bool = True   # No central fired before its 3 corners
    face_completion_order: List[str] = field(default_factory=list)

    # 3+1 at tetragram level
    teta_spatial_centrals_first: bool = False       # strict: all spatial < time
    tetb_spatial_centrals_first: bool = False
    teta_spatial_centrals_first_weak: bool = False   # weak: all spatial <= time (ties OK)
    tetb_spatial_centrals_first_weak: bool = False


# =============================================================================
# TETRAGRAM ANALYZER
# =============================================================================

class TetragramAnalyzer:
    """
    Wraps a TraversalAnalyzer and derives tetragram-level metrics.

    Does NOT re-run the traversal. Processes existing macro-cycle data
    to produce tetragram-level resolution analysis.
    """

    def __init__(self, engine: TraversalAnalyzer):
        self.engine = engine
        if not engine._has_run:
            engine.run()

        self.cycles: List[TetragramCycle] = []
        self._has_run = False

    def run(self):
        """Execute tetragram analysis. Idempotent."""
        if self._has_run:
            return
        self._has_run = True
        self._analyze_cycles()

    # -----------------------------------------------------------------
    # CYCLE ANALYSIS
    # -----------------------------------------------------------------

    def _analyze_cycles(self):
        """Process each macro-cycle's trigram data at tetragram resolution."""
        for mc in self.engine.macro_cycles:
            cycle = self._analyze_one_cycle(mc)
            self.cycles.append(cycle)

    def _analyze_one_cycle(self, mc) -> TetragramCycle:
        """
        For a single macro-cycle, reconstruct the tetragram activation
        sequence from the trigram_orders data.
        """
        cycle = TetragramCycle(
            cycle_number=mc.cycle_number,
            start_step=mc.start_step,
            end_step=mc.end_step,
        )

        # Collect ALL activation events across faces, then sort by step
        all_events = []  # (step, tetragram_id, type, face, vertex_or_none)

        for face_name in FACE_NAMES_SORTED:
            reads_raw = mc.trigram_orders.get(face_name, [])
            if not reads_raw:
                continue

            prog = FaceProgression(face=face_name, cycle=mc.cycle_number)
            prev_step = -1

            for read_idx, (vertex, step) in enumerate(reads_raw):
                # Corner activation
                corner_id = CORNER_TO_SUB.get((face_name, vertex))
                if corner_id is None:
                    continue  # Safety check

                gap = (step - prev_step) if prev_step >= 0 else -1
                activation = CornerActivation(
                    tetragram_id=corner_id,
                    face=face_name,
                    vertex=vertex,
                    step=step,
                    read_position=read_idx + 1,
                    gap_from_previous=gap,
                )
                prog.reads.append(activation)
                all_events.append((step, corner_id, 'corner', face_name, vertex))
                prev_step = step

            # If face completed (3 reads), the central activates at the same step
            # as the 3rd corner
            if len(prog.reads) == 3:
                last_read = prog.reads[-1]
                central_id = FACE_CENTRAL[face_name]
                central = CentralActivation(
                    tetragram_id=central_id,
                    face=face_name,
                    step=last_read.step,
                    triggering_corner=last_read.tetragram_id,
                    cycle_rank=-1,  # Will be set below
                )
                prog.central = central
                all_events.append(
                    (last_read.step, central_id, 'central', face_name, None)
                )

                # Derived metrics
                prog.span = last_read.step - prog.reads[0].step
                prog.trigram = tuple(r.vertex for r in prog.reads)
                if len(prog.reads) >= 2:
                    prog.gap_1_to_2 = prog.reads[1].step - prog.reads[0].step
                if len(prog.reads) >= 3:
                    prog.gap_2_to_3 = prog.reads[2].step - prog.reads[1].step

            cycle.face_progressions[face_name] = prog

        # Sort all events by step (stable: corners before centrals at same step)
        all_events.sort(key=lambda e: (e[0], 0 if e[2] == 'corner' else 1))
        cycle.activation_sequence = [(sid, step) for step, sid, _, _, _ in all_events]

        # Assign central completion ranks
        central_rank = 0
        for step, sid, etype, fname, _ in all_events:
            if etype == 'central':
                central_rank += 1
                prog = cycle.face_progressions[fname]
                if prog.central:
                    prog.central.cycle_rank = central_rank
                cycle.face_completion_order.append(fname)

        # Counts
        cycle.total_corner_activations = sum(
            1 for _, _, t, _, _ in all_events if t == 'corner'
        )
        cycle.total_central_activations = sum(
            1 for _, _, t, _, _ in all_events if t == 'central'
        )
        cycle.total_activations = len(all_events)
        cycle.all_32_active = (
            cycle.total_corner_activations == 24 and
            cycle.total_central_activations == 8
        )

        # Integrity: verify no central fires before its 3 corners
        corner_steps = {}  # tetragram_id -> step
        for step, sid, etype, _, _ in all_events:
            if etype == 'corner':
                corner_steps[sid] = step

        for fname in FACE_NAMES_SORTED:
            central_id = FACE_CENTRAL[fname]
            corner_ids = FACE_CORNERS[fname]
            prog = cycle.face_progressions.get(fname)
            if prog and prog.central:
                central_step = prog.central.step
                for cid in corner_ids:
                    if cid not in corner_steps or corner_steps[cid] > central_step:
                        cycle.all_corners_before_centrals = False

        # 3+1 at tetragram level: spatial centrals complete before time central?
        teta_central_steps = []
        teta_time_step = None
        tetb_central_steps = []
        tetb_time_step = None

        for fname in cycle.face_completion_order:
            prog = cycle.face_progressions[fname]
            if not prog.central:
                continue
            cstep = prog.central.step
            if fname in TETA_FACES:
                if fname in TIME_FACES:
                    teta_time_step = cstep
                else:
                    teta_central_steps.append(cstep)
            elif fname in TETB_FACES:
                if fname in TIME_FACES:
                    tetb_time_step = cstep
                else:
                    tetb_central_steps.append(cstep)

        if teta_time_step is not None and len(teta_central_steps) == 3:
            cycle.teta_spatial_centrals_first = all(
                s < teta_time_step for s in teta_central_steps
            )
            cycle.teta_spatial_centrals_first_weak = all(
                s <= teta_time_step for s in teta_central_steps
            )
        if tetb_time_step is not None and len(tetb_central_steps) == 3:
            cycle.tetb_spatial_centrals_first = all(
                s < tetb_time_step for s in tetb_central_steps
            )
            cycle.tetb_spatial_centrals_first_weak = all(
                s <= tetb_time_step for s in tetb_central_steps
            )

        return cycle

    # -----------------------------------------------------------------
    # REPORT
    # -----------------------------------------------------------------

    def get_report(self) -> Dict:
        """Return comprehensive tetragram statistics."""
        if not self._has_run:
            self.run()

        n_cycles = len(self.cycles)
        if n_cycles == 0:
            return {'cycles_analyzed': 0}

        # --- Integrity ---
        all_32_count = sum(1 for c in self.cycles if c.all_32_active)
        all_corners_first_count = sum(
            1 for c in self.cycles if c.all_corners_before_centrals
        )

        # --- Gap statistics ---
        gaps_1_to_2 = []
        gaps_2_to_3 = []
        spans = []
        for c in self.cycles:
            for fp in c.face_progressions.values():
                if fp.is_complete:
                    if fp.gap_1_to_2 >= 0:
                        gaps_1_to_2.append(fp.gap_1_to_2)
                    if fp.gap_2_to_3 >= 0:
                        gaps_2_to_3.append(fp.gap_2_to_3)
                    spans.append(fp.span)

        # --- Trigram diversity ---
        face_trigrams = defaultdict(list)
        for c in self.cycles:
            for fname, fp in c.face_progressions.items():
                if fp.is_complete:
                    face_trigrams[fname].append(fp.trigram)

        total_unique_trigrams = sum(
            len(set(tgs)) for tgs in face_trigrams.values()
        )

        # --- Completion rank stability ---
        face_ranks = defaultdict(list)
        for c in self.cycles:
            for fname in FACE_NAMES_SORTED:
                fp = c.face_progressions.get(fname)
                if fp and fp.central:
                    face_ranks[fname].append(fp.central.cycle_rank)

        rank_stddevs = {}
        for fname, ranks in face_ranks.items():
            if len(ranks) > 1:
                mean = sum(ranks) / len(ranks)
                var = sum((r - mean) ** 2 for r in ranks) / len(ranks)
                rank_stddevs[fname] = math.sqrt(var)

        # --- 3+1 rates ---
        a_3plus1_strict = sum(1 for c in self.cycles if c.teta_spatial_centrals_first)
        b_3plus1_strict = sum(1 for c in self.cycles if c.tetb_spatial_centrals_first)
        a_3plus1_weak = sum(1 for c in self.cycles if c.teta_spatial_centrals_first_weak)
        b_3plus1_weak = sum(1 for c in self.cycles if c.tetb_spatial_centrals_first_weak)

        # --- First-read corner position ---
        first_read_positions = Counter()  # which corner position (1st/2nd/3rd sorted vertex) gets read first
        for c in self.cycles:
            for fp in c.face_progressions.values():
                if fp.reads:
                    first_v = fp.reads[0].vertex
                    face_verts = sorted(FACES[fp.face])
                    pos = face_verts.index(first_v) if first_v in face_verts else -1
                    first_read_positions[pos] += 1

        # --- Cross-tet interleaving ---
        interleave_counts = []
        for c in self.cycles:
            switches = 0
            prev_tet = None
            for fname in c.face_completion_order:
                cur_tet = 'A' if fname in TETA_FACES else 'B'
                if prev_tet is not None and cur_tet != prev_tet:
                    switches += 1
                prev_tet = cur_tet
            interleave_counts.append(switches)

        # --- Central activation spacing ---
        central_gaps = []
        for c in self.cycles:
            central_steps_sorted = []
            for sid, step in c.activation_sequence:
                if TETRAGRAMS[sid]['type'] == 'central':
                    central_steps_sorted.append(step)
            for i in range(1, len(central_steps_sorted)):
                central_gaps.append(central_steps_sorted[i] - central_steps_sorted[i - 1])

        return {
            'cycles_analyzed': n_cycles,

            # Integrity
            'cycles_all_32_active': all_32_count,
            'cycles_all_32_rate': round(all_32_count / n_cycles, 4),
            'cycles_corners_before_centrals': all_corners_first_count,
            'corners_before_centrals_rate': round(all_corners_first_count / n_cycles, 4),

            # Gap statistics
            'mean_gap_1_to_2': round(sum(gaps_1_to_2) / len(gaps_1_to_2), 3) if gaps_1_to_2 else 0,
            'mean_gap_2_to_3': round(sum(gaps_2_to_3) / len(gaps_2_to_3), 3) if gaps_2_to_3 else 0,
            'mean_span': round(sum(spans) / len(spans), 3) if spans else 0,
            'max_span': max(spans) if spans else 0,
            'min_span': min(spans) if spans else 0,
            'gap_1_to_2_samples': len(gaps_1_to_2),
            'gap_2_to_3_samples': len(gaps_2_to_3),

            # Trigram diversity
            'total_unique_trigrams': total_unique_trigrams,
            'max_possible_trigrams': 48,
            'trigram_diversity': round(total_unique_trigrams / 48, 4) if total_unique_trigrams else 0,

            # Completion rank stability
            'mean_rank_stddev': round(
                sum(rank_stddevs.values()) / len(rank_stddevs), 3
            ) if rank_stddevs else 0,

            # 3+1 (strict: spatial < time; weak: spatial <= time, matches engine)
            'teta_3plus1_strict': a_3plus1_strict,
            'teta_3plus1_strict_rate': round(a_3plus1_strict / n_cycles, 4),
            'tetb_3plus1_strict': b_3plus1_strict,
            'tetb_3plus1_strict_rate': round(b_3plus1_strict / n_cycles, 4),
            'teta_3plus1_weak': a_3plus1_weak,
            'teta_3plus1_weak_rate': round(a_3plus1_weak / n_cycles, 4),
            'tetb_3plus1_weak': b_3plus1_weak,
            'tetb_3plus1_weak_rate': round(b_3plus1_weak / n_cycles, 4),

            # First-read corner position
            'first_read_pos_0': first_read_positions.get(0, 0),
            'first_read_pos_1': first_read_positions.get(1, 0),
            'first_read_pos_2': first_read_positions.get(2, 0),

            # Cross-tet interleaving
            'mean_interleave_switches': round(
                sum(interleave_counts) / len(interleave_counts), 3
            ) if interleave_counts else 0,
            'max_interleave_switches': max(interleave_counts) if interleave_counts else 0,

            # Central spacing
            'mean_central_gap': round(
                sum(central_gaps) / len(central_gaps), 3
            ) if central_gaps else 0,
            'max_central_gap': max(central_gaps) if central_gaps else 0,
            'min_central_gap': min(central_gaps) if central_gaps else 0,
        }


# =============================================================================
# MODULE-LEVEL ACCESSOR
# =============================================================================

_sub_instance: Optional[TetragramAnalyzer] = None


def get_tetragram_analyzer(n_digits: int = 1000) -> TetragramAnalyzer:
    """
    Get the shared TetragramAnalyzer instance.
    Created once, shared across all tests.
    """
    global _sub_instance
    engine = get_analyzer(n_digits)
    if _sub_instance is None or _sub_instance.engine.n_digits != n_digits:
        _sub_instance = TetragramAnalyzer(engine)
        _sub_instance.run()
    return _sub_instance
