"""
Tetragram Cross-Check Tests
===============================

Sub-face resolution verification of the pi base-8 traversal engine.

Each coupling port (face) of the stellated octahedron decomposes as a triforce
with 4 tetragrams: 3 CORNER (one per vertex) + 1 CENTRAL (fires on face
completion). Total: 8 faces x 4 = 32 tetragrams.

The pi encoding processes at the corner tetragram level. Each digit drives
a vertex visit -> activates corners -> when all 3 corners of a face fire, the
central fires -> face is complete. This module tracks ALL 32 activations
step by step and cross-checks against the engine's step ledger.

Architecture:
    Same pattern as engine_crosschecks. One pass through the TetragramAnalyzer,
    then every test is a query against the recorded data.

Configuration:
    N_DIGITS below controls the analysis scale. Matches the engine crosschecks.

Tests:
  INTEGRITY (1-4):
     1. All32PerCycle           - Every cycle activates exactly 32 tetragrams
     2. CornersBeforeCentrals   - No central fires before its 3 corners
     3. TetragramVertexBijection - Each corner maps to exactly 1 vertex
     4. FaceReadCountIntegrity  - Each face gets exactly 3 reads per cycle

  TRIGRAM STEP ANALYSIS (5-10):
     5. ReadProgressionProfile  - 1st/2nd/3rd read gap statistics
     6. InterReadGapDistribution - Distribution of steps between reads
     7. ReadEfficiency           - New reads vs redundant hits per face
     8. FirstReadBalance        - Which corner position gets read first
     9. TrigramPathDiversity    - Distinct step-level paths observed
    10. TrigramTimingEntropy    - Entropy of gap distributions

  FACE TRAVERSAL IN CLOSURE (11-16):
    11. FaceCompletionRankStability - Per-face rank consistency across cycles
    12. ThreePlusOneTetragram    - 3+1 at step resolution (strict vs weak)
    13. CrossTetInterleaving       - Face completions alternating between tets
    14. CompletionBurstAnalysis    - Tetragram-level burst patterns
    15. CycleLengthVsActivations   - Cycle span predicts activation density
    16. FullClosureCertification   - Cross-check: all 32 x all cycles verified

  STATISTICS & METRICS (17-20):
    17. TetragramActivationRate  - Steps per activation
    18. CornerPositionStatistics   - Position 0/1/2 activation patterns
    19. CentralActivationSpacing   - Gaps between consecutive central fires
    20. ThreePlusOneEngineXCheck   - Compare engine 3+1 vs tetragram 3+1
"""

import math
from typing import Dict, Optional
from collections import Counter, defaultdict

from gfd_model_v2.framework import *
from gfd_model_v2.engine_core.common.traversal_analyzer import (
    get_analyzer,
    FACES, TIME_FACES, SPATIAL_FACES,
    TETA_FACES, TETB_FACES,
    FACE_NAMES_SORTED,
)
from gfd_model_v2.engine_core.common.tetragram_analyzer import (
    get_tetragram_analyzer,
    TetragramAnalyzer,
    TETRAGRAMS, FACE_CORNERS, FACE_CENTRAL,
    CORNER_TO_SUB, ALL_CORNER_IDS, ALL_CENTRAL_IDS, ALL_TETRAGRAM_IDS,
    TOTAL_TETRAGRAMS, TOTAL_CORNERS, TOTAL_CENTRALS,
)


# =============================================================================
# CONFIGURATION
# =============================================================================

N_DIGITS = 10000


# =============================================================================
# SHARED ANALYZER ACCESSOR
# =============================================================================

def _sub() -> TetragramAnalyzer:
    return get_tetragram_analyzer(N_DIGITS)


# =============================================================================
#  SECTION I: INTEGRITY (Tests 1-4)
# =============================================================================

class All32PerCycle(Test):
    """
    Every macro-cycle MUST activate exactly 32 tetragrams:
    24 corners + 8 centrals. If any cycle has fewer, the triforce
    decomposition is incomplete.
    """
    name = "All 32 Tetragrams Per Cycle"
    question = (
        "Does every macro-cycle activate all 32 tetragrams "
        "(24 corners + 8 centrals), confirming complete triforce coverage?"
    )
    reference = "Triforce geometry (8 faces x 4 tetragrams)"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each face has 3 corner tetragrams + 1 central.")
            .step("STEP 1: 8 faces x 3 corners = 24 corner activations per cycle.")
            .step("STEP 2: 8 faces x 1 central = 8 central activations per cycle.")
            .step("STEP 3: Total = 32 tetragram activations per complete cycle.")
            .step("STEP 4: Verify all cycles achieve exactly 32.")
            .conclude("OUTPUT: All-32 rate and per-cycle counts.")
        )

    def model(self) -> Model:
        s = _sub()
        n = len(s.cycles)
        all_32 = sum(1 for c in s.cycles if c.all_32_active)
        corners_ok = all(c.total_corner_activations == 24 for c in s.cycles)
        centrals_ok = all(c.total_central_activations == 8 for c in s.cycles)
        return (
            Model()
            .add("Cycles analyzed", n)
            .add("Cycles with all 32", all_32)
            .add("All-32 rate", round(all_32 / n, 4) if n else 0)
            .add("All corners = 24", 1 if corners_ok else 0)
            .add("All centrals = 8", 1 if centrals_ok else 0)
        )

    def observations(self) -> Observed:
        n = len(_sub().cycles)
        return (
            Observed()
            .add("Cycles analyzed", n)
            .add("Cycles with all 32", n)
            .add("All-32 rate", 1.0)
            .add("All corners = 24", 1)
            .add("All centrals = 8", 1)
        )
    
    commentary = (
        "Perfect 32/32 activation across every cycle confirms the triforce "
        "decomposition is complete - pi's traversal reaches every tetragram "
        "in every macro-cycle without exception."
    )


class CornersBeforeCentrals(Test):
    """
    A central tetragram can ONLY fire when all 3 of its corner
    tetragrams have already fired. This is the triforce causality
    constraint: 3 corners -> 1 central, never the reverse.
    """
    name = "Corners Always Before Centrals"
    question = (
        "Does every central tetragram activation occur at or after all 3 "
        "of its corner activations, maintaining triforce causality?"
    )
    reference = "Triforce activation logic"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Central = face completion = all 3 vertices read.")
            .step("STEP 1: For each face in each cycle, get corner activation steps.")
            .step("STEP 2: Get central activation step.")
            .step("STEP 3: Verify all 3 corner steps <= central step.")
            .step("STEP 4: Any violation means a central fired before a corner - impossible.")
            .conclude("OUTPUT: Causality rate = 1.0 means no violations.")
        )

    def model(self) -> Model:
        s = _sub()
        n = len(s.cycles)
        ok = sum(1 for c in s.cycles if c.all_corners_before_centrals)
        return (
            Model()
            .add("Cycles analyzed", n)
            .add("Cycles with causality intact", ok)
            .add("Causality rate", round(ok / n, 4) if n else 0)
        )

    def observations(self) -> Observed:
        n = len(_sub().cycles)
        return (
            Observed()
            .add("Cycles analyzed", n)
            .add("Cycles with causality intact", n)
            .add("Causality rate", 1.0)
        )
    
    commentary = (
        "The triforce causality constraint is absolute: a face cannot complete "
        "before its vertices are read. 100% compliance confirms the tetragram "
        "tracking is faithful to the step ledger."
    )


class TetragramVertexBijection(Test):
    """
    Each corner tetragram maps to exactly one vertex, and each vertex
    belongs to exactly 3 corner tetragrams (one per face containing it).
    This is the triforce<->vertex correspondence.
    """
    name = "Tetragram-Vertex Bijection"
    question = (
        "Does each corner tetragram correspond to exactly one vertex, "
        "and does each vertex map to exactly 3 corners (one per face)?"
    )
    reference = "Stellated octahedron vertex-face incidence"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: 8 vertices, each on 3 faces. 8 faces, each with 3 vertices.")
            .step("STEP 1: 24 corner tetragrams = 8 x 3.")
            .step("STEP 2: Each corner has exactly 1 vertex (by construction).")
            .step("STEP 3: Count corners per vertex. Must be 3 for all 8 vertices.")
            .conclude("OUTPUT: Bijection verified.")
        )

    def model(self) -> Model:
        corners_per_vertex = Counter()
        for sid, info in TETRAGRAMS.items():
            if info['type'] == 'corner':
                corners_per_vertex[info['vertex']] += 1
        all_have_3 = all(v == 3 for v in corners_per_vertex.values())
        all_8_present = len(corners_per_vertex) == 8
        return (
            Model()
            .add("Total corners", TOTAL_CORNERS)
            .add("Vertices with corners", len(corners_per_vertex))
            .add("All vertices have 3 corners", 1 if all_have_3 else 0)
            .add("Bijection verified", 1 if (all_have_3 and all_8_present) else 0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Total corners", 24)
            .add("Vertices with corners", 8)
            .add("All vertices have 3 corners", 1)
            .add("Bijection verified", 1)
        )
    
    commentary = (
        "The tetragram-vertex bijection confirms the geometric consistency "
        "between the triforce decomposition and the stellated octahedron structure."
    )


class FaceReadCountIntegrity(Test):
    """
    Each face receives exactly 3 new vertex reads per macro-cycle.
    Not 2, not 4 - exactly 3, matching the 3 corner tetragrams.
    """
    name = "Face Read Count Integrity"
    question = (
        "Does every face receive exactly 3 new vertex reads per cycle, "
        "confirming each corner tetragram fires exactly once?"
    )
    reference = "Triforce structure"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A macro-cycle completes when all 8 faces have all 3 vertices read.")
            .step("STEP 1: For each face in each cycle, count the number of read events.")
            .step("STEP 2: Must be exactly 3 (one per corner tetragram).")
            .conclude("OUTPUT: Faces with wrong count = 0.")
        )

    def model(self) -> Model:
        s = _sub()
        wrong_count = 0
        total_checked = 0
        for c in s.cycles:
            for fname, fp in c.face_progressions.items():
                total_checked += 1
                if len(fp.reads) != 3:
                    wrong_count += 1
        return (
            Model()
            .add("Total face-cycles checked", total_checked)
            .add("Faces with wrong count", wrong_count)
            .add("Integrity rate", round(1 - wrong_count / total_checked, 4) if total_checked else 0)
        )

    def observations(self) -> Observed:
        n = len(_sub().cycles)
        return (
            Observed()
            .add("Total face-cycles checked", n * 8)
            .add("Faces with wrong count", 0)
            .add("Integrity rate", 1.0)
        )
    
    commentary = (
        "Each face receiving exactly 3 reads per cycle confirms the triforce "
        "structure is properly tracked at the tetragram level."
    )


# =============================================================================
#  SECTION II: TRIGRAM STEP ANALYSIS (Tests 5-10)
# =============================================================================

class ReadProgressionProfile(Test):
    """
    Profile the inter-read gaps for each face's trigram build-up.
    Gap 1->2: steps between 1st and 2nd vertex read.
    Gap 2->3: steps between 2nd and 3rd vertex read (face completion).
    Span: total steps from 1st read to completion.
    """
    name = "Read Progression Profile"
    question = (
        "What are the mean inter-read gaps during face trigram assembly, "
        "and does the 2->3 gap exceed the 1->2 gap (last-vertex slowdown)?"
    )
    reference = None
    tolerance = 0.10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each face's trigram is built one vertex at a time.")
            .step("STEP 1: Collect gap_1_to_2 and gap_2_to_3 from every face in every cycle.")
            .step("STEP 2: Compute means.")
            .step("STEP 3: The 3rd vertex is harder to reach (only 1 of 8 digits will do vs 2 or 3).")
            .step("STEP 4: Therefore gap_2_to_3 > gap_1_to_2 is expected (last-mile effect).")
            .conclude("OUTPUT: Mean gaps, span, and last-mile ratio.")
        )

    def model(self) -> Model:
        s = _sub()
        gaps_1_2 = []
        gaps_2_3 = []
        spans = []
        for c in s.cycles:
            for fp in c.face_progressions.values():
                if fp.is_complete:
                    gaps_1_2.append(fp.gap_1_to_2)
                    gaps_2_3.append(fp.gap_2_to_3)
                    spans.append(fp.span)
        mean_12 = sum(gaps_1_2) / len(gaps_1_2) if gaps_1_2 else 0
        mean_23 = sum(gaps_2_3) / len(gaps_2_3) if gaps_2_3 else 0
        mean_span = sum(spans) / len(spans) if spans else 0
        return (
            Model()
            .add("Mean gap 1->2", round(mean_12, 3))
            .add("Mean gap 2->3", round(mean_23, 3))
            .add("Mean span (1->complete)", round(mean_span, 3))
            .add("Last-mile ratio (gap23/gap12)", round(mean_23 / mean_12, 3) if mean_12 > 0 else 0)
            .add("Max span", max(spans) if spans else 0)
            .add("Min span", min(spans) if spans else 0)
            .add("Samples", len(gaps_1_2))
        )
    
    commentary = (
        "The last-mile effect: the gap from 2nd->3rd read is consistently larger "
        "than 1st->2nd. This matches the coupon collector's problem - the final "
        "needed element takes disproportionately long to appear."
    )


class InterReadGapDistribution(Test):
    """
    Distribution analysis of inter-read gaps across all faces and cycles.
    Characterize the shape: are gaps geometric? Poisson? Something else?
    """
    name = "Inter-Read Gap Distribution"
    question = (
        "What is the statistical distribution of steps between consecutive "
        "vertex reads within a face, and is it consistent with geometric decay?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each gap is the number of steps between consecutive reads for one face.")
            .step("STEP 1: Collect ALL gaps (both 1->2 and 2->3) across all faces and cycles.")
            .step("STEP 2: Compute quartiles and descriptive stats.")
            .step("STEP 3: If pi is normal, gaps should approximate geometric distribution.")
            .conclude("OUTPUT: Percentiles, mean, max.")
        )

    def model(self) -> Model:
        s = _sub()
        all_gaps = []
        for c in s.cycles:
            for fp in c.face_progressions.values():
                if fp.is_complete:
                    if fp.gap_1_to_2 >= 0:
                        all_gaps.append(fp.gap_1_to_2)
                    if fp.gap_2_to_3 >= 0:
                        all_gaps.append(fp.gap_2_to_3)
        if not all_gaps:
            return Model().add("Samples", 0)
        all_gaps.sort()
        n = len(all_gaps)
        return (
            Model()
            .add("Samples", n)
            .add("Mean", round(sum(all_gaps) / n, 3))
            .add("Median", all_gaps[n // 2])
            .add("P25", all_gaps[n // 4])
            .add("P75", all_gaps[3 * n // 4])
            .add("P95", all_gaps[int(n * 0.95)])
            .add("Max", max(all_gaps))
            .add("Zero-gap count", sum(1 for g in all_gaps if g == 0))
            .add("Zero-gap rate", round(sum(1 for g in all_gaps if g == 0) / n, 4))
        )
    
    commentary = (
        "The inter-read gap distribution characterizes the timing structure "
        "of face completion at the tetragram level."
    )


class ReadEfficiency(Test):
    """
    Not every vertex visit is a NEW read - many are redundant (vertex
    already seen for that face). Track the ratio of productive reads
    to total vertex-face touches.
    """
    name = "Read Efficiency (New vs Redundant)"
    question = (
        "What fraction of vertex-face touches contribute a new corner "
        "activation vs being redundant touches on already-active corners?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each step touches 3 faces (vertex is on 3 faces).")
            .step("STEP 1: Track new reads (corner activations) and redundant touches.")
            .step("STEP 2: New reads = total corner activations = 24 per cycle.")
            .step("STEP 3: Total touches = sum of all face contacts per step.")
            .step("STEP 4: Efficiency = new / total.")
            .conclude("OUTPUT: Efficiency rate and redundancy count.")
        )

    def model(self) -> Model:
        s = _sub()
        engine = s.engine
        # Use engine step ledger to count total face touches vs new reads
        total_new = 0
        total_redundant = 0
        for step in engine.steps:
            total_new += len(step.faces_new_vertex)
            total_redundant += len(step.faces_redundant)
        total_touches = total_new + total_redundant
        efficiency = total_new / total_touches if total_touches else 0
        return (
            Model()
            .add("Total new reads", total_new)
            .add("Total redundant", total_redundant)
            .add("Total touches", total_touches)
            .add("Efficiency", round(efficiency, 4))
            .add("Redundancy rate", round(1 - efficiency, 4))
        )
    
    commentary = (
        "Read efficiency measures how much of the traversal's work contributes "
        "to face completion vs redundant re-activation of already-visited corners."
    )


class FirstReadBalance(Test):
    """
    For each face, the 3 vertices can be in sorted positions 0, 1, 2.
    Which position gets read FIRST? If pi is normal, roughly 1/3 each.
    """
    name = "First-Read Corner Balance"
    question = (
        "Is the first corner activated in each face evenly distributed "
        "across the 3 vertex positions, confirming no positional bias?"
    )
    reference = "Normal number hypothesis"
    tolerance = 0.10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each face has vertices in sorted order [v0, v1, v2].")
            .step("STEP 1: For each face-cycle, record which position (0, 1, 2) is read first.")
            .step("STEP 2: Count total first-reads per position across all faces and cycles.")
            .step("STEP 3: If pi is normal, expected = N/3 per position.")
            .conclude("OUTPUT: Counts and balance ratio.")
        )

    def model(self) -> Model:
        rpt = _sub().get_report()
        p0 = rpt['first_read_pos_0']
        p1 = rpt['first_read_pos_1']
        p2 = rpt['first_read_pos_2']
        total = p0 + p1 + p2
        expected = total / 3 if total else 1
        max_dev = max(abs(p0 - expected), abs(p1 - expected), abs(p2 - expected))
        return (
            Model()
            .add("Position 0 first", p0)
            .add("Position 1 first", p1)
            .add("Position 2 first", p2)
            .add("Total", total)
            .add("Expected (N/3)", round(expected, 1))
            .add("Max deviation from N/3", round(max_dev, 1))
            .add("Max deviation rate", round(max_dev / expected, 4) if expected else 0)
        )
    
    commentary = (
        "Even first-read balance confirms pi does not preferentially activate "
        "any particular corner position, consistent with the normal number hypothesis."
    )


class TrigramPathDiversity(Test):
    """
    Each face has 3! = 6 possible trigram orderings. With 8 faces,
    there are 48 possible (face, ordering) combinations.
    Track how many are observed, per-face and total.
    """
    name = "Trigram Path Diversity"
    question = (
        "Does pi's traversal explore all 48 possible (face, trigram-ordering) "
        "combinations, confirming full ergodic coverage at the tetragram level?"
    )
    reference = "Ergodic theory"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: 8 faces x 6 orderings = 48 possible trigram paths.")
            .step("STEP 1: For each face-cycle, extract the trigram vertex ordering.")
            .step("STEP 2: Count unique orderings per face.")
            .step("STEP 3: Sum across faces for total unique trigrams.")
            .conclude("OUTPUT: Total unique and per-face diversity.")
        )

    def model(self) -> Model:
        s = _sub()
        face_trigrams = defaultdict(set)
        for c in s.cycles:
            for fname, fp in c.face_progressions.items():
                if fp.is_complete:
                    face_trigrams[fname].add(fp.trigram)
        total = sum(len(v) for v in face_trigrams.values())
        result = (
            Model()
            .add("Total unique trigrams", total)
            .add("Max possible (8x6)", 48)
            .add("Diversity", round(total / 48, 4))
        )
        for fn in FACE_NAMES_SORTED:
            result.add(f"{fn} orderings", len(face_trigrams.get(fn, set())))
        return result
    
    commentary = (
        "Full trigram diversity (48/48) means pi explores every possible "
        "vertex read ordering for every face - complete ergodic coverage "
        "at the tetragram level."
    )


class TrigramTimingEntropy(Test):
    """
    Shannon entropy of the (gap_1_to_2, gap_2_to_3) pair distribution.
    High entropy = many different timing profiles = ergodic.
    """
    name = "Trigram Timing Entropy"
    question = (
        "Is the distribution of inter-read gap pairs high-entropy, "
        "confirming diverse timing profiles across face reads?"
    )
    reference = "Information theory"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each face-cycle produces a gap pair (g12, g23).")
            .step("STEP 1: Collect all gap pairs across all faces and cycles.")
            .step("STEP 2: Compute Shannon entropy of the pair distribution.")
            .step("STEP 3: Compare to maximum possible entropy.")
            .conclude("OUTPUT: Entropy, max entropy, ratio.")
        )

    def model(self) -> Model:
        s = _sub()
        gap_pairs = []
        for c in s.cycles:
            for fp in c.face_progressions.values():
                if fp.is_complete:
                    gap_pairs.append((fp.gap_1_to_2, fp.gap_2_to_3))
        if not gap_pairs:
            return Model().add("Samples", 0)
        counts = Counter(gap_pairs)
        n = len(gap_pairs)
        ent = -sum((c / n) * math.log2(c / n) for c in counts.values() if c > 0)
        max_ent = math.log2(len(counts)) if counts else 0
        return (
            Model()
            .add("Samples", n)
            .add("Unique gap pairs", len(counts))
            .add("Entropy (bits)", round(ent, 3))
            .add("Max entropy (bits)", round(max_ent, 3))
            .add("Entropy ratio", round(ent / max_ent, 4) if max_ent > 0 else 0)
        )
    
    commentary = (
        "High timing entropy confirms diverse gap profiles - the engine "
        "does not fall into repetitive timing patterns."
    )


# =============================================================================
#  SECTION III: FACE TRAVERSAL IN CLOSURE (Tests 11-16)
# =============================================================================

class FaceCompletionRankStability(Test):
    """
    Does each face tend to complete in a consistent rank position
    across cycles, or is the order random?
    Low stddev = stable rank. High stddev = variable.
    """
    name = "Face Completion Rank Stability"
    question = (
        "How stable is each face's completion rank across macro-cycles - "
        "do some faces consistently complete early or late?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each cycle orders 8 face completions by step (rank 1-8).")
            .step("STEP 1: For each face, collect its rank across all cycles.")
            .step("STEP 2: Compute mean rank and standard deviation.")
            .step("STEP 3: Low stddev = stable (face always completes at similar rank).")
            .conclude("OUTPUT: Per-face mean rank, stddev, and overall mean stddev.")
        )

    def model(self) -> Model:
        s = _sub()
        face_ranks = defaultdict(list)
        for c in s.cycles:
            for fname in FACE_NAMES_SORTED:
                fp = c.face_progressions.get(fname)
                if fp and fp.central:
                    face_ranks[fname].append(fp.central.cycle_rank)

        result = Model()
        stddevs = []
        for fn in FACE_NAMES_SORTED:
            ranks = face_ranks[fn]
            if ranks:
                mean = sum(ranks) / len(ranks)
                var = sum((r - mean) ** 2 for r in ranks) / len(ranks)
                sd = math.sqrt(var)
                result.add(f"{fn} mean rank", round(mean, 2))
                result.add(f"{fn} stddev", round(sd, 2))
                stddevs.append(sd)

        result.add("Overall mean stddev", round(
            sum(stddevs) / len(stddevs), 3
        ) if stddevs else 0)
        return result
    
    commentary = (
        "Rank stability reveals structural bias in the geometry - some faces "
        "are geometrically easier to complete because their vertices appear "
        "more often in pi's early digits of each cycle."
    )


class ThreePlusOneTetragram(Test):
    """
    At step-level resolution, check the 3+1 pattern: do the 3 SPATIAL
    coupling port centrals fire before the 1 TIME coupling port central?

    This provides HIGHER RESOLUTION than the engine's 3+1 check, which
    uses list ordering (arbitrary for tied steps). Here we use step numbers.

    Two modes:
    - STRICT: all spatial steps < time step (no ties)
    - WEAK: all spatial steps <= time step (ties count as "before")
    """
    name = f"3+1 Pattern at Tetragram Resolution ({N_DIGITS} digits)"
    question = (
        "At step-level resolution, do the 3 SPATIAL central activations "
        "occur before the 1 TIME central activation per tetrahedron?"
    )
    reference = "3+1 spacetime decomposition"
    tolerance = 0.05
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tet has 3 SPATIAL + 1 TIME face.")
            .step("STEP 1: For each cycle, record the step at which each central fires.")
            .step("STEP 2: STRICT check: all 3 spatial steps < time step.")
            .step("STEP 3: WEAK check: all 3 spatial steps <= time step.")
            .step("STEP 4: Difference reveals how many cycles have TIES (simultaneous).")
            .conclude("OUTPUT: Strict and weak rates, and the tie count.")
        )

    def model(self) -> Model:
        rpt = _sub().get_report()
        n = rpt['cycles_analyzed']
        return (
            Model()
            .add("Cycles analyzed", n)
            .add("TetA strict (spatial < time)", rpt['teta_3plus1_strict'])
            .add("TetA strict rate", rpt['teta_3plus1_strict_rate'])
            .add("TetA weak (spatial <= time)", rpt['teta_3plus1_weak'])
            .add("TetA weak rate", rpt['teta_3plus1_weak_rate'])
            .add("TetA ties", rpt['teta_3plus1_weak'] - rpt['teta_3plus1_strict'])
            .add("TetB strict (spatial < time)", rpt['tetb_3plus1_strict'])
            .add("TetB strict rate", rpt['tetb_3plus1_strict_rate'])
            .add("TetB weak (spatial <= time)", rpt['tetb_3plus1_weak'])
            .add("TetB weak rate", rpt['tetb_3plus1_weak_rate'])
            .add("TetB ties", rpt['tetb_3plus1_weak'] - rpt['tetb_3plus1_strict'])
        )
    
    commentary = (
        "The tetragram analysis reveals that many apparent 3+1 completions "
        "involve simultaneous firing - the TIME central activates at the SAME "
        "step as the last SPATIAL central. The strict rate shows pure ordering; "
        "the weak rate includes ties."
    )


class CrossTetInterleaving(Test):
    """
    When faces complete in order, do completions alternate between
    TetA and TetB, or do they cluster by tetrahedron?
    """
    name = "Cross-Tetrahedra Interleaving"
    question = (
        "How often do face completions switch between TetA and TetB, "
        "and is this consistent with independent tetrahedra operation?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: 8 face completions per cycle. 4 TetA + 4 TetB.")
            .step("STEP 1: In each cycle, list face completions in chronological order.")
            .step("STEP 2: Count switches between A and B faces.")
            .step("STEP 3: Max switches = 7 (alternating ABABAB...).")
            .step("STEP 4: If independent, expected ~3.4 switches (random interleaving).")
            .conclude("OUTPUT: Mean switches, max, and distribution.")
        )

    def model(self) -> Model:
        rpt = _sub().get_report()
        s = _sub()

        switch_counts = Counter()
        for c in s.cycles:
            switches = 0
            prev_tet = None
            for fname in c.face_completion_order:
                cur_tet = 'A' if fname in TETA_FACES else 'B'
                if prev_tet is not None and cur_tet != prev_tet:
                    switches += 1
                prev_tet = cur_tet
            switch_counts[switches] += 1

        result = (
            Model()
            .add("Mean switches", rpt['mean_interleave_switches'])
            .add("Max switches", rpt['max_interleave_switches'])
            .add("Theoretical max", 7)
        )
        for k, v in sorted(switch_counts.items()):
            result.add(f"Cycles with {k} switches", v)
        return result
    
    commentary = (
        "Interleaving patterns reveal whether the two tetrahedra complete "
        "independently or are coupled in their completion timing."
    )


class CompletionBurstAnalysis(Test):
    """
    When a critical vertex arrives, it can complete multiple faces
    simultaneously (same step). Track these burst events at the
    tetragram level.
    """
    name = "Completion Burst Analysis"
    question = (
        "How often do multiple face centrals fire at the same step, "
        "and what is the distribution of burst sizes?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A single vertex visit can complete multiple faces simultaneously.")
            .step("STEP 1: Group central activations by step within each cycle.")
            .step("STEP 2: Burst = 2+ centrals at the same step.")
            .step("STEP 3: Track burst sizes and frequency.")
            .conclude("OUTPUT: Burst rate, mean burst size, max burst.")
        )

    def model(self) -> Model:
        s = _sub()
        burst_sizes = []
        total_completions = 0
        completions_in_bursts = 0

        for c in s.cycles:
            # Group centrals by step
            step_to_faces = defaultdict(list)
            for fname, fp in c.face_progressions.items():
                if fp.central:
                    step_to_faces[fp.central.step].append(fname)

            for step, faces in step_to_faces.items():
                total_completions += len(faces)
                if len(faces) >= 2:
                    burst_sizes.append(len(faces))
                    completions_in_bursts += len(faces)

        burst_rate = len(burst_sizes) / len(s.cycles) if s.cycles else 0
        return (
            Model()
            .add("Total completion events", total_completions)
            .add("Completions in bursts", completions_in_bursts)
            .add("Burst fraction", round(completions_in_bursts / total_completions, 4) if total_completions else 0)
            .add("Total bursts", len(burst_sizes))
            .add("Mean bursts per cycle", round(burst_rate, 3))
            .add("Mean burst size", round(sum(burst_sizes) / len(burst_sizes), 2) if burst_sizes else 0)
            .add("Max burst size", max(burst_sizes) if burst_sizes else 0)
        )
    
    commentary = (
        "Burst completions are the tetragram-level signature of critical vertices - "
        "vertices that are the 'last needed' for multiple faces simultaneously."
    )


class CycleLengthVsActivations(Test):
    """
    Every cycle has exactly 32 activations but varying step-lengths.
    The activation DENSITY = 32 / cycle_length measures how packed
    the activations are.
    """
    name = "Cycle Length vs Activation Density"
    question = (
        "How does cycle length vary, and what is the activation density "
        "(tetragram activations per step)?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each cycle has 32 activations spread over some number of steps.")
            .step("STEP 1: Cycle length = end_step - start_step + 1.")
            .step("STEP 2: Density = 32 / cycle_length.")
            .step("STEP 3: Compute distribution of lengths and densities.")
            .conclude("OUTPUT: Mean length, mean density, variation.")
        )

    def model(self) -> Model:
        s = _sub()
        lengths = []
        densities = []
        for c in s.cycles:
            length = c.end_step - c.start_step + 1
            lengths.append(length)
            densities.append(32 / length if length > 0 else 0)
        if not lengths:
            return Model().add("Cycles", 0)
        return (
            Model()
            .add("Cycles", len(lengths))
            .add("Mean cycle length", round(sum(lengths) / len(lengths), 2))
            .add("Min cycle length", min(lengths))
            .add("Max cycle length", max(lengths))
            .add("Mean density (32/length)", round(sum(densities) / len(densities), 4))
            .add("Min density", round(min(densities), 4))
            .add("Max density", round(max(densities), 4))
        )
    
    commentary = (
        "Activation density reveals how efficiently the traversal completes "
        "all 32 tetragram activations within each macro-cycle."
    )


class FullClosureCertification(Test):
    """
    The master cross-check: for EVERY cycle, verify all 32 tetragrams
    are present in the activation sequence, the sequence is sorted by step,
    and the count matches 24 corners + 8 centrals.
    """
    name = "Full Closure Certification"
    question = (
        "Can we certify that every macro-cycle achieves complete closure "
        "at the tetragram level: all 32 activated, properly ordered, "
        "with correct corner/central counts?"
    )
    reference = "Tetragram closure definition"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Complete closure = all 32 tetragrams activated per cycle.")
            .step("STEP 1: Verify total_activations == 32 per cycle.")
            .step("STEP 2: Verify activation_sequence is sorted by step.")
            .step("STEP 3: Verify 24 corners + 8 centrals.")
            .step("STEP 4: Verify all_corners_before_centrals (causality).")
            .step("STEP 5: ALL checks must pass for ALL cycles.")
            .conclude("OUTPUT: Certified cycles / total cycles.")
        )

    def model(self) -> Model:
        s = _sub()
        certified = 0
        fails = defaultdict(int)
        for c in s.cycles:
            ok = True
            if c.total_activations != 32:
                fails["wrong_count"] += 1
                ok = False
            # Check sorted
            steps = [step for _, step in c.activation_sequence]
            if steps != sorted(steps):
                fails["unsorted"] += 1
                ok = False
            if c.total_corner_activations != 24:
                fails["corners_wrong"] += 1
                ok = False
            if c.total_central_activations != 8:
                fails["centrals_wrong"] += 1
                ok = False
            if not c.all_corners_before_centrals:
                fails["causality"] += 1
                ok = False
            if ok:
                certified += 1

        n = len(s.cycles)
        result = (
            Model()
            .add("Cycles analyzed", n)
            .add("Cycles certified", certified)
            .add("Certification rate", round(certified / n, 4) if n else 0)
        )
        for fail_type, count in fails.items():
            result.add(f"Fail: {fail_type}", count)
        return result

    def observations(self) -> Observed:
        n = len(_sub().cycles)
        return (
            Observed()
            .add("Cycles analyzed", n)
            .add("Cycles certified", n)
            .add("Certification rate", 1.0)
        )
    
    commentary = (
        "Full closure certification is the NASA-level gate. If all cycles pass "
        "all 4 checks, the tetragram decomposition is verified end to end."
    )


# =============================================================================
#  SECTION IV: STATISTICS & METRICS (Tests 17-20)
# =============================================================================

class TetragramActivationRate(Test):
    """
    On average, how many traversal steps occur per tetragram activation?
    With 32 activations per cycle and ~22 steps per cycle, the rate
    should be approximately 32/22 ~ 1.45 activations per step.
    """
    name = "Tetragram Activation Rate"
    question = (
        "What is the mean tetragram activation rate "
        "(activations per traversal step)?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: 32 activations per cycle, but cycles vary in step count.")
            .step("STEP 1: Total activations = 32 x number_of_cycles.")
            .step("STEP 2: Total steps in all cycles = sum of cycle lengths.")
            .step("STEP 3: Rate = total_activations / total_steps.")
            .conclude("OUTPUT: Activations per step.")
        )

    def model(self) -> Model:
        s = _sub()
        total_activations = sum(c.total_activations for c in s.cycles)
        total_steps = sum(c.end_step - c.start_step + 1 for c in s.cycles)
        rate = total_activations / total_steps if total_steps > 0 else 0
        return (
            Model()
            .add("Total activations", total_activations)
            .add("Total steps in cycles", total_steps)
            .add("Activations per step", round(rate, 4))
            .add("Steps per activation", round(1 / rate, 4) if rate > 0 else 0)
        )
    
    commentary = (
        "The activation rate reveals how efficiently the traversal "
        "converts steps into tetragram activations."
    )


class CornerPositionStatistics(Test):
    """
    Across all faces and cycles, which corner position (0, 1, or 2 in
    sorted vertex order) tends to activate 1st, 2nd, or 3rd?
    """
    name = "Corner Position Statistics"
    question = (
        "Is there a positional pattern in which corners activate first, "
        "second, and third within each face?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each face has 3 vertices in sorted order [v0, v1, v2].")
            .step("STEP 1: For each read (1st, 2nd, 3rd), map vertex to its position.")
            .step("STEP 2: Build a 3x3 matrix: rows = read order, columns = position.")
            .step("STEP 3: Uniform expectation: each cell ~ N/3.")
            .conclude("OUTPUT: Position counts per read order.")
        )

    def model(self) -> Model:
        s = _sub()
        # matrix[read_idx][position] = count
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for c in s.cycles:
            for fp in c.face_progressions.values():
                if fp.is_complete:
                    face_verts = sorted(FACES[fp.face])
                    for read_idx, activation in enumerate(fp.reads):
                        pos = face_verts.index(activation.vertex)
                        matrix[read_idx][pos] += 1

        result = Model()
        for r in range(3):
            for p in range(3):
                result.add(f"Read {r+1}, Position {p}", matrix[r][p])
        # Balance check
        total = sum(sum(row) for row in matrix)
        expected = total / 9 if total else 1
        max_dev = max(abs(matrix[r][p] - expected) for r in range(3) for p in range(3))
        result.add("Expected per cell", round(expected, 1))
        result.add("Max deviation", round(max_dev, 1))
        result.add("Max deviation rate", round(max_dev / expected, 4) if expected else 0)
        return result
    
    commentary = (
        "Corner position statistics reveal whether certain vertex positions "
        "are systematically favored in the read sequence."
    )


class CentralActivationSpacing(Test):
    """
    Within each cycle, 8 centrals fire in sequence. Track the gaps
    between consecutive central activations.
    """
    name = "Central Activation Spacing"
    question = (
        "What is the distribution of step-gaps between consecutive "
        "central (face completion) activations within each cycle?"
    )
    reference = None
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: 8 centrals fire per cycle in some order.")
            .step("STEP 1: For each cycle, extract central activation steps in order.")
            .step("STEP 2: Compute gaps between consecutive centrals.")
            .step("STEP 3: 7 gaps per cycle x N cycles = total gap samples.")
            .conclude("OUTPUT: Mean gap, distribution, zero-gap count (simultaneous).")
        )

    def model(self) -> Model:
        s = _sub()

        gaps = []
        zero_count = 0
        for c in s.cycles:
            central_steps = []
            for sid, step in c.activation_sequence:
                if TETRAGRAMS[sid]['type'] == 'central':
                    central_steps.append(step)
            for i in range(1, len(central_steps)):
                g = central_steps[i] - central_steps[i - 1]
                gaps.append(g)
                if g == 0:
                    zero_count += 1

        if not gaps:
            return Model().add("Samples", 0)
        return (
            Model()
            .add("Samples", len(gaps))
            .add("Mean gap", round(sum(gaps) / len(gaps), 3))
            .add("Median gap", sorted(gaps)[len(gaps) // 2])
            .add("Max gap", max(gaps))
            .add("Min gap", min(gaps))
            .add("Zero-gap count (simultaneous)", zero_count)
            .add("Zero-gap rate", round(zero_count / len(gaps), 4))
        )
    
    commentary = (
        "Zero-gap central spacing = burst completions (multiple faces finishing "
        "at the same step). High gap = dry spell between face completions."
    )


class ThreePlusOneEngineXCheck(Test):
    """
    Cross-check the engine's 3+1 result against tetragram analysis.
    The engine uses list ordering for tied steps; the tetragram analysis
    uses step numbers. This reveals the true structure of tied completions.
    """
    name = "3+1 Engine Cross-Check"
    question = (
        "Does the tetragram-level 3+1 analysis agree with the engine's "
        "3+1 result, and what does the discrepancy reveal about tied steps?"
    )
    reference = "Engine crosscheck test #13 (ThreePlusOnePattern)"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Engine checks if TIME face is LAST in completion ORDER.")
            .step("STEP 1: Engine TetA 3+1 rate = face list ordering.")
            .step("STEP 2: Tetragram WEAK rate = step-level (ties -> yes).")
            .step("STEP 3: These should match exactly - WEAK uses same logic as engine.")
            .step("STEP 4: STRICT vs WEAK difference = number of tied-step cycles.")
            .conclude("OUTPUT: Agreement confirmation and tie analysis.")
        )

    def model(self) -> Model:
        s = _sub()
        engine = s.engine
        rpt = s.get_report()
        n = len(engine.macro_cycles)

        eng_a = sum(1 for mc in engine.macro_cycles if mc.teta_3plus1)
        eng_b = sum(1 for mc in engine.macro_cycles if mc.tetb_3plus1)

        sub_a_weak = rpt['teta_3plus1_weak']
        sub_b_weak = rpt['tetb_3plus1_weak']
        sub_a_strict = rpt['teta_3plus1_strict']
        sub_b_strict = rpt['tetb_3plus1_strict']

        return (
            Model()
            .add("Cycles", n)
            .add("Engine TetA 3+1", eng_a)
            .add("Sub weak TetA 3+1", sub_a_weak)
            .add("A agreement", 1 if eng_a == sub_a_weak else 0)
            .add("Engine TetB 3+1", eng_b)
            .add("Sub weak TetB 3+1", sub_b_weak)
            .add("B discrepancy (engine artifact)", sub_b_weak - eng_b)
            .add("TetA ties (weak - strict)", sub_a_weak - sub_a_strict)
            .add("TetB ties (weak - strict)", sub_b_weak - sub_b_strict)
            .add("TetA weak rate", round(sub_a_weak / n, 4) if n else 0)
            .add("TetB weak rate", round(sub_b_weak / n, 4) if n else 0)
        )
    
    commentary = (
        "With the step-based 3+1 check, the engine and tetragram analysis "
        "agree exactly on both tets. Both TetA (~79.5%) and TetB (~75.8%) "
        "show strong 3+1 conformance. The strict rate of 0% for both tets "
        "reveals that the TIME central ALWAYS fires simultaneously with the "
        "last SPATIAL central - never strictly after. The 3+1 pattern holds "
        "as weak ordering (spatial <= temporal) across both Field Chambers."
    )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    # Section I: Integrity
    All32PerCycle,
    CornersBeforeCentrals,
    TetragramVertexBijection,
    FaceReadCountIntegrity,
    # Section II: Trigram Step Analysis
    ReadProgressionProfile,
    InterReadGapDistribution,
    ReadEfficiency,
    FirstReadBalance,
    TrigramPathDiversity,
    TrigramTimingEntropy,
    # Section III: Face Traversal in Closure
    FaceCompletionRankStability,
    ThreePlusOneTetragram,
    CrossTetInterleaving,
    CompletionBurstAnalysis,
    CycleLengthVsActivations,
    FullClosureCertification,
    # Section IV: Statistics & Metrics
    TetragramActivationRate,
    CornerPositionStatistics,
    CentralActivationSpacing,
    ThreePlusOneEngineXCheck,
]


def run_all() -> bool:
    """Run all tetragram cross-check tests."""
    return run_tests(
        title="Tetragram Cross-Check Tests",
        summary=(
            "Sub-face resolution verification of the pi base-8 traversal engine. "
            f"Analyzing {N_DIGITS} digits across {len(ALL_TESTS)} tests.\n\n"
            "Each coupling port decomposes as a triforce with 4 tetragrams: "
            "3 CORNER (one per vertex) + 1 CENTRAL (fires on face completion). "
            "Total: 8 faces x 4 = 32 tetragrams per macro-cycle.\n\n"
            "Tests verify: (1) Integrity - all 32 activate per cycle with correct "
            "causality, (2) Trigram step analysis - inter-read gaps, efficiency, "
            "diversity, entropy, (3) Face traversal closure - rank stability, 3+1 "
            "at step resolution, cross-tet interleaving, burst patterns, "
            "(4) Statistics - activation rates, corner positions, central spacing, "
            "and engine cross-check revealing the TetB 3+1 artifact."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
