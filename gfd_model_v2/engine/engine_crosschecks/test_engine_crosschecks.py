"""
Engine Cross-Check Tests
========================

NASA-level verification of the pi base-8 traversal engine.

Architecture:
    One pass. One ledger. Many tests.
    The TraversalAnalyzer processes N_DIGITS ONCE, producing a complete
    step-by-step ledger. Every test below is a QUERY against that ledger.
    No test re-runs the traversal. No test re-computes state.

Configuration:
    Change N_DIGITS below to scale the analysis. Supported: 1–10,000.
    The pi_data module provides 10,000 verified base-8 fractional digits
    computed at mp.dps=12000 via mpmath with triple verification.

All 26 tests are CRITICAL. This is the crankshaft.

Tests:
  INTEGRITY (1–3):
     1. StepLedgerIntegrity         — Every invariant at every step
     2. ComplementIntegrity         — 7-v maps to opposite tet, every step
     3. LinearGuaranteesNonLinear   — Tet_A verification guarantees Tet_B

  DISTRIBUTIONS (4–7):
     4. DigitDistribution           — Input digit frequency, entropy, uniformity
     5. VertexDistribution          — Output vertex frequency, entropy, balance
     6. TetrahedronBalance          — Tet_A / Tet_B step counts and per-vertex
     7. ComplementPairActivity      — Per complementary pair (v, 7-v) step counts

  FACE MECHANICS (8–11):
     8. OrbitFaceTargeting          — Per-orbit new vs redundant face hits
     9. PerOrbitFaceCoverage        — Face progress within each orbit
    10. RedundantReadDistribution   — Which faces absorb redundant hits
    11. FaceFirstCompletion         — Step at which each face first completes

  MACRO-CYCLE ANALYSIS (12–17):
    12. TrigamCompletionOrder       — Face completion sequence per macro-cycle
    13. ThreePlusOnePattern         — 3 SPATIAL then 1 TIME, per tet, per cycle
    14. MacroCycleConsistency       — Structural pattern stability across cycles
    15. MacroCycleLengthDistribution — Quartiles, IQR, CoV, full histogram
    16. FaceCompletionRank          — Which face completes first/last most often
    17. CycleToOrbitRatio           — Orbits per macro-cycle, scaling relationships

  TRIGRAM ANALYSIS (18–19):
    18. TrigamReadIntegrity         — Per-face vertex read sequence analysis
    19. TrigamEntropyPerFace        — Shannon entropy of trigram orderings

  CROSSING FORENSICS (20–22):
    20. FieldOriginCrossingPattern  — Crossing frequency and handoff integrity
    21. CrossingDirectionSymmetry   — A→B vs B→A balance
    22. SameTetGapDistribution      — Gap length histogram and long-gap frequency

  STALL & VERTEX DYNAMICS (23–25):
    23. ZeroDigitStallAnalysis      — Impact of digit=0 on face machinery
    24. StallClusterDepth           — Max consecutive zeros, run distribution
    25. VertexAutocorrelation       — Consecutive same-vertex rate, repeat analysis

  SUMMARY (26):
    26. FullAnomalyReport           — Comprehensive anomaly summary
"""

import math
import sys
import os
from typing import Dict, Optional
from collections import Counter, defaultdict

# Path setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group
from traversal_analyzer import (
    get_analyzer, TraversalAnalyzer,
    FACES, TET_A, TET_B, TIME_FACES, SPATIAL_FACES,
    TET_A_FACES, TET_B_FACES, FACE_NAMES_SORTED,
    get_tet, get_faces_for_vertex,
)


# =============================================================================
# CONFIGURATION
# =============================================================================
# Change this to scale. Supported: 1 – 10,000.
# The traversal runs ONCE at this digit count; all 26 tests query the result.

N_DIGITS = 10000

# =============================================================================


def _analyzer() -> TraversalAnalyzer:
    return get_analyzer(N_DIGITS)


# ---------------------------------------------------------------------------
#  SECTION I: INTEGRITY (Tests 1-3)
# ---------------------------------------------------------------------------

class StepLedgerIntegrity(GFDTest):
    """
    Verify every invariant at every step for N_DIGITS digits.
    - cumsum == running sum of all digits
    - vertex == cumsum % 8
    - tet matches vertex parity
    - orbit == cumsum // 8
    - complement == 7 - vertex
    If ANY step fails ANY check, the engine is broken.
    """
    name = f"Step Ledger Integrity ({N_DIGITS} digits)"
    question = (
        f"Does every single step across {N_DIGITS} pi base-8 digits satisfy all "
        "state invariants: cumsum, vertex, tetrahedron, orbit, and complement?"
    )
    reference_source = "Traversal definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: The traversal has 5 invariants that must hold at every step. "
        "STEP 1: cumsum_n = sum(digits[0..n]) — verified against running total. "
        "STEP 2: vertex_n = cumsum_n mod 8 — verified against stored vertex. "
        "STEP 3: tet_n = 'A' if vertex in {1,2,4,7} else 'B' — verified against parity. "
        "STEP 4: orbit_n = cumsum_n // 8 — verified against stored orbit. "
        "STEP 5: complement_n = 7 - vertex_n — verified against stored complement. "
        "OUTPUT: 5 checks x N steps. Zero failures required."
    )
    commentary = (
        "This is the foundation. If any step fails any invariant, nothing built "
        "on top of the ledger can be trusted."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total_steps = len(a.steps)
        cumsum_ok = vertex_ok = tet_ok = orbit_ok = complement_ok = 0

        running_sum = 0
        for s in a.steps:
            running_sum += s.digit
            if s.cumsum == running_sum:
                cumsum_ok += 1
            if s.vertex == s.cumsum % 8:
                vertex_ok += 1
            expected_tet = 'A' if s.vertex in TET_A else 'B'
            if s.tet == expected_tet:
                tet_ok += 1
            if s.orbit == s.cumsum // 8:
                orbit_ok += 1
            if s.complement == 7 - s.vertex:
                complement_ok += 1

        return {
            "Total steps": total_steps,
            "Cumsum verified": cumsum_ok,
            "Vertex verified": vertex_ok,
            "Tetrahedron verified": tet_ok,
            "Orbit verified": orbit_ok,
            "Complement verified": complement_ok,
        }

    def observations(self) -> Dict[str, float]:
        n = len(_analyzer().steps)
        return {
            "Total steps": n,
            "Cumsum verified": n,
            "Vertex verified": n,
            "Tetrahedron verified": n,
            "Orbit verified": n,
            "Complement verified": n,
        }


class ComplementIntegrity(GFDTest):
    """
    The complement 7-v MUST map to the opposite tetrahedron at EVERY step.
    This is the Field Origin coupling. A single violation breaks the
    linear/non-linear bridge.
    """
    name = "Field Origin Complement Integrity"
    question = (
        "Does the complement operation (7-v) map every vertex to the opposite "
        "tetrahedron at every step, guaranteeing Field Origin coupling?"
    )
    reference_source = "Parity structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: Field Origin couples Tet_A (linear) to Tet_B (non-linear). "
        "STEP 1: For each step, compute complement = 7 - vertex. "
        "STEP 2: Verify complement is in the OPPOSITE tetrahedron from vertex. "
        "STEP 3: If tet(v) == tet(7-v) for ANY step, the coupling is broken. "
        "OUTPUT: Violations = 0 means the non-linear side is guaranteed correct."
    )
    commentary = (
        "If complement integrity holds with zero violations, then Tet_B "
        "(subspace, non-linear) is deterministically bound to Tet_A through "
        "the complement operation."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        violations = 0
        total = len(a.steps)
        for s in a.steps:
            if s.comp_tet == s.tet:
                violations += 1
        return {
            "Steps checked": total,
            "Complement violations": violations,
            "Bridge intact": 1 if violations == 0 else 0,
        }

    def observations(self) -> Dict[str, float]:
        return {
            "Steps checked": len(_analyzer().steps),
            "Complement violations": 0,
            "Bridge intact": 1,
        }


class LinearGuaranteesNonLinear(GFDTest):
    """
    If the step function is verified on the Tet_A side AND the complement
    relationship holds at every step, then Tet_B is mathematically guaranteed.
    """
    name = "Linear Side Guarantees Non-Linear"
    question = (
        "If all 5 step invariants hold AND complement maps to the opposite "
        "tetrahedron at every step, is Tet_B (non-linear) mathematically "
        "guaranteed correct?"
    )
    reference_source = "Complement determinism"
    tolerance = 0.0
    derivation = (
        "PREMISE: Tet_B is deterministically bound to Tet_A through complement. "
        "STEP 1: Step ledger integrity verifies Tet_A step function. "
        "STEP 2: Complement integrity verifies 7-v maps to opposite tet. "
        "STEP 3: If BOTH hold, Tet_B states are guaranteed at every step. "
        "OUTPUT: Both conditions satisfied = non-linear side guaranteed."
    )
    commentary = (
        "This is the key argument. We cannot look inside Tet_B directly, "
        "but if the bridge (complement) holds and the linear side (Tet_A) "
        "is verified, then Tet_B must follow. Mathematical proof, not statistics."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        report = a.get_report()
        ledger_ok = (report['cumsum_errors'] == 0 and report['vertex_errors'] == 0)
        complement_ok = report['complement_violations'] == 0
        both_ok = ledger_ok and complement_ok
        return {
            "Ledger integrity": 1 if ledger_ok else 0,
            "Complement integrity": 1 if complement_ok else 0,
            "Non-linear guaranteed": 1 if both_ok else 0,
        }

    def observations(self) -> Dict[str, float]:
        return {
            "Ledger integrity": 1,
            "Complement integrity": 1,
            "Non-linear guaranteed": 1,
        }


# ---------------------------------------------------------------------------
#  SECTION II: DISTRIBUTIONS (Tests 4-7)
# ---------------------------------------------------------------------------

class DigitDistribution(GFDTest):
    """
    Analyze the input digit frequency distribution.
    Pi's base-8 digits should be approximately uniform over {0..7}.
    """
    name = "Input Digit Distribution"
    question = (
        "Are pi's base-8 fractional digits uniformly distributed across "
        "{0..7}, and what is the Shannon entropy of the distribution?"
    )
    reference_source = "Pi normality conjecture"
    tolerance = 0.05
    derivation = (
        "PREMISE: Pi is conjectured to be normal — digits uniform in every base. "
        "STEP 1: Count occurrences of each digit 0-7 across all steps. "
        "STEP 2: Compute Shannon entropy: H = -sum p_i log2(p_i). "
        "STEP 3: Maximum entropy for 8 symbols = log2(8) = 3.0 bits. "
        "STEP 4: Compute mean, std deviation, max deviation from expected. "
        "OUTPUT: Entropy ratio (should be ~1.0), digit counts, deviation."
    )
    commentary = (
        "The digit distribution drives everything downstream. If digits were "
        "non-uniform, vertex visits, face hits, and crossing rates would all "
        "be systematically biased."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total = len(a.steps)
        digit_counts = Counter(s.digit for s in a.steps)
        expected = total / 8
        entropy = -sum(
            (c / total) * math.log2(c / total)
            for c in digit_counts.values() if c > 0
        )
        max_entropy = math.log2(8)
        mean_digit = sum(s.digit for s in a.steps) / total
        var_digit = sum((s.digit - mean_digit) ** 2 for s in a.steps) / total
        max_dev = max(abs(digit_counts.get(d, 0) - expected) / expected for d in range(8))

        result = {
            "Total steps": total,
            "Shannon entropy (bits)": round(entropy, 6),
            "Max entropy (bits)": max_entropy,
            "Entropy ratio": round(entropy / max_entropy, 6),
            "Mean digit value": round(mean_digit, 4),
            "Expected mean (3.5)": 3.5,
            "Std deviation": round(var_digit ** 0.5, 4),
            "Max deviation from uniform": round(max_dev, 4),
        }
        for d in range(8):
            result[f"Digit {d} count"] = digit_counts.get(d, 0)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class VertexDistribution(GFDTest):
    """
    Analyze the output vertex visit frequencies.
    """
    name = "Output Vertex Distribution"
    question = (
        "Are vertex visits distributed evenly across all 8 vertices, "
        "and what is the vertex entropy?"
    )
    reference_source = "Traversal uniformity"
    tolerance = 0.05
    derivation = (
        "PREMISE: If input digits are uniform, output vertices should be ~uniform. "
        "STEP 1: Count visits to each vertex 0-7 across all steps. "
        "STEP 2: Compute Shannon entropy and compare to max (3 bits). "
        "OUTPUT: Vertex counts, entropy, imbalance metrics."
    )
    commentary = (
        "Vertex distribution reveals whether the cumsum-mod-8 mapping preserves "
        "the approximate uniformity of pi's digits."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total = len(a.steps)
        vcounts = Counter(s.vertex for s in a.steps)
        entropy = -sum(
            (c / total) * math.log2(c / total)
            for c in vcounts.values() if c > 0
        )
        result = {
            "Total steps": total,
            "Vertex entropy (bits)": round(entropy, 6),
            "Max entropy (3 bits)": 3.0,
            "Entropy ratio": round(entropy / 3.0, 6),
        }
        for v in range(8):
            tet = 'A' if v in TET_A else 'B'
            result[f"Vertex {v} (Tet_{tet})"] = vcounts.get(v, 0)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class TetrahedronBalance(GFDTest):
    """
    Measure the balance between Tet_A and Tet_B step counts,
    and per-vertex distribution within each tetrahedron.
    """
    name = "Tetrahedron Balance"
    question = (
        "Are steps evenly distributed between Tet_A and Tet_B, "
        "and are vertices balanced within each tetrahedron?"
    )
    reference_source = "Bimetric symmetry"
    tolerance = 0.10
    derivation = (
        "PREMISE: Balanced traversal should visit both tetrahedra ~equally. "
        "STEP 1: Count Tet_A and Tet_B steps. "
        "STEP 2: Compute balance ratio = min(A,B) / max(A,B). "
        "STEP 3: Within each tet, compute per-vertex fractions. "
        "OUTPUT: Tet counts, balance ratio, per-vertex breakdown."
    )
    commentary = (
        "The bimetric structure requires tight coupling between the two "
        "tetrahedra. Large imbalance would indicate one side dominates."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total = len(a.steps)
        tet_a = sum(1 for s in a.steps if s.tet == 'A')
        tet_b = total - tet_a
        balance = min(tet_a, tet_b) / max(tet_a, tet_b) if max(tet_a, tet_b) > 0 else 0
        vcounts = Counter(s.vertex for s in a.steps)
        result = {
            "Tet_A steps": tet_a,
            "Tet_B steps": tet_b,
            "Tet_A fraction": round(tet_a / total, 6),
            "Tet_B fraction": round(tet_b / total, 6),
            "Balance ratio (min/max)": round(balance, 6),
        }
        for tet_name, tet_set in [("A", TET_A), ("B", TET_B)]:
            tet_total = sum(vcounts.get(v, 0) for v in tet_set)
            for v in sorted(tet_set):
                cnt = vcounts.get(v, 0)
                pct = cnt / tet_total if tet_total else 0
                result[f"Tet_{tet_name}_V{v} pct"] = round(pct, 4)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class ComplementPairActivity(GFDTest):
    """
    Track how often each complementary pair (v, 7-v) is active.
    The four pairs are (0,7), (1,6), (2,5), (3,4).
    """
    name = "Complement Pair Activity"
    question = (
        "Are the four complementary vertex pairs equally active "
        "across the traversal?"
    )
    reference_source = "Field Origin balance"
    tolerance = 0.10
    derivation = (
        "PREMISE: Each step activates a vertex v and its complement 7-v. "
        "STEP 1: For each step, determine which pair is active. "
        "STEP 2: Count activations per pair. "
        "OUTPUT: Per-pair counts and balance metrics."
    )
    commentary = (
        "The complement pairs are the Field Origin coupling bridges. "
        "If one pair is underactive, that coupling channel is starved."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total = len(a.steps)
        pair_counts = Counter()
        PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]
        for s in a.steps:
            pair = tuple(sorted([s.vertex, s.complement]))
            pair_counts[pair] += 1
        result = {"Total steps": total}
        for p in PAIRS:
            cnt = pair_counts.get(p, 0)
            result[f"Pair ({p[0]},{p[1]}) count"] = cnt
            result[f"Pair ({p[0]},{p[1]}) pct"] = round(cnt / total, 4)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


# ---------------------------------------------------------------------------
#  SECTION III: FACE MECHANICS (Tests 8-11)
# ---------------------------------------------------------------------------

class OrbitFaceTargeting(GFDTest):
    """
    For each orbit, track which faces received new vs redundant vertex hits.
    """
    name = "Per-Orbit Face Targeting Analysis"
    question = (
        "Across all orbits, are vertex hits distributed across faces "
        "without systematic starvation or oversaturation?"
    )
    reference_source = "Engine balance"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each orbit spans ~2-3 steps. Face hits should spread across faces. "
        "STEP 1: For each orbit, count faces receiving new vertex hits. "
        "STEP 2: Count faces receiving ONLY redundant hits. "
        "STEP 3: Track total new and redundant hits across all orbits. "
        "OUTPUT: Distribution of face targeting across the full traversal."
    )
    commentary = (
        "Face targeting distribution reveals whether the engine distributes "
        "vertex hits evenly or concentrates them."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total_new = 0
        total_redundant = 0
        orbits_with_completions = 0
        for orb in a.orbits:
            total_new += sum(orb.face_new_hits.values())
            total_redundant += sum(orb.face_redundant_hits.values())
            if orb.face_completions:
                orbits_with_completions += 1
        return {
            "Total orbits": len(a.orbits),
            "Total new hits": total_new,
            "Total redundant hits": total_redundant,
            "Orbits with completions": orbits_with_completions,
            "Analysis complete": 1,
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class PerOrbitFaceCoverage(GFDTest):
    """
    For each orbit, count faces that received new vertex contributions.
    """
    name = "Per-Orbit Face Coverage"
    question = (
        "Within each orbit, how many faces make progress, "
        "and are there orbits with zero face progress?"
    )
    reference_source = "Engine efficiency"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each orbit spans ~2-3 steps. "
        "STEP 1: For each orbit, count unique faces with new vertex hits. "
        "STEP 2: Find min, max, mean coverage per orbit. "
        "OUTPUT: Coverage statistics across all orbits."
    )
    commentary = (
        "Per-orbit face coverage reveals whether the engine consistently "
        "makes progress or has dead orbits."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        faces_per_orbit = [len(orb.face_new_hits) for orb in a.orbits]
        zero_progress = sum(1 for f in faces_per_orbit if f == 0)
        return {
            "Total orbits": len(a.orbits),
            "Min faces per orbit": min(faces_per_orbit) if faces_per_orbit else 0,
            "Max faces per orbit": max(faces_per_orbit) if faces_per_orbit else 0,
            "Mean faces per orbit": round(sum(faces_per_orbit) / len(faces_per_orbit), 2) if faces_per_orbit else 0,
            "Zero-progress orbits": zero_progress,
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class RedundantReadDistribution(GFDTest):
    """
    Track which faces absorb the most redundant reads and why.
    """
    name = "Redundant Read Distribution"
    question = (
        "Are redundant vertex reads distributed evenly across faces, "
        "or do certain faces absorb disproportionately more?"
    )
    reference_source = "Face geometry"
    tolerance = 0.0
    derivation = (
        "PREMISE: Redundant reads occur when a vertex re-hits an already-counted face. "
        "STEP 1: Tally redundant hits per face from all steps. "
        "STEP 2: Compare distribution: TIME vs SPATIAL, Tet_A vs Tet_B. "
        "OUTPUT: Per-face redundant counts and distribution analysis."
    )
    commentary = (
        "Redundant read distribution reveals structural biases in which "
        "faces accumulate excess hits after initial completion."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        face_redundant = Counter()
        for s in a.steps:
            for f in s.faces_redundant:
                face_redundant[f] += 1
        total_redundant = sum(face_redundant.values())
        time_redundant = sum(face_redundant.get(f, 0) for f in TIME_FACES)
        spatial_redundant = sum(face_redundant.get(f, 0) for f in SPATIAL_FACES)

        result = {
            "Total redundant reads": total_redundant,
            "TIME face redundant": time_redundant,
            "SPATIAL face redundant": spatial_redundant,
        }
        for fn in FACE_NAMES_SORTED:
            result[f"{fn} redundant"] = face_redundant.get(fn, 0)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class FaceFirstCompletion(GFDTest):
    """
    Track the step at which each face first completes (ever).
    This is the boot-up sequence of the engine.
    """
    name = "Face First Completion (Engine Boot)"
    question = (
        "At what step does each face first achieve a complete trigram read, "
        "and what is the engine's boot-up sequence?"
    )
    reference_source = "Face geometry + pi sequence"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each face needs all 3 vertices visited to complete. "
        "STEP 1: Scan the step ledger for faces_completed events. "
        "STEP 2: Record the FIRST step at which each face completes. "
        "STEP 3: Order faces by first completion step. "
        "OUTPUT: Boot-up sequence — which faces come online first."
    )
    commentary = (
        "The boot-up sequence reveals how pi's initial digits interact with "
        "the geometry. Faces whose vertices appear early in pi complete first."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        first_complete = {}
        for s in a.steps:
            for fn in s.faces_completed:
                if fn not in first_complete:
                    first_complete[fn] = s.step
        result = {"Faces completed": len(first_complete)}
        for fn in sorted(first_complete, key=first_complete.get):
            ftype = 'TIME' if fn in TIME_FACES else 'SPATIAL'
            result[f"{fn} ({ftype})"] = first_complete[fn]
        result["Last face online at step"] = max(first_complete.values()) if first_complete else -1
        result["Engine fully booted"] = 1 if len(first_complete) == 8 else 0
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


# ---------------------------------------------------------------------------
#  SECTION IV: MACRO-CYCLE ANALYSIS (Tests 12-17)
# ---------------------------------------------------------------------------

class TrigamCompletionOrder(GFDTest):
    """
    Track the ORDER in which face trigrams complete across macro-cycles.
    Verify each cycle has exactly 8 unique face completions.
    """
    name = "Trigram Completion Order"
    question = (
        "In each macro-cycle, does every face complete exactly once before "
        "any face can complete again?"
    )
    reference_source = "Macro-cycle definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: A macro-cycle ends when all 8 faces have completed once. "
        "STEP 1: Within a cycle, no face CAN complete twice (tracking resets). "
        "STEP 2: Count total macro-cycles completed. "
        "STEP 3: Verify each cycle has exactly 8 completions, all unique faces. "
        "OUTPUT: Cycles found, all with exactly 8 unique face completions."
    )
    commentary = (
        "The macro-cycle structure guarantees that every face gets exactly one "
        "trigram read per cycle — the engine's duty cycle."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total_cycles = len(a.macro_cycles)
        all_have_8 = all(len(c.completion_order) == 8 for c in a.macro_cycles)
        all_unique = all(
            len(set(f for f, _ in c.completion_order)) == 8
            for c in a.macro_cycles
        )
        return {
            "Macro-cycles completed": total_cycles,
            "All have 8 completions": 1 if all_have_8 else 0,
            "All faces unique per cycle": 1 if all_unique else 0,
        }

    def observations(self) -> Dict[str, float]:
        return {
            "Macro-cycles completed": len(_analyzer().macro_cycles),
            "All have 8 completions": 1,
            "All faces unique per cycle": 1,
        }


class ThreePlusOnePattern(GFDTest):
    """
    For each macro-cycle, check the 3+1 pattern:
    Do 3 SPATIAL faces complete before the TIME face per tetrahedron?
    """
    name = f"3+1 Pattern at Scale ({N_DIGITS} digits)"
    question = (
        "In each macro-cycle, do the 3 SPATIAL coupling ports complete before "
        "the 1 TIME coupling port in each tetrahedron?"
    )
    reference_source = "3+1 spacetime structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: 3+1 pattern requires SPATIAL faces to complete before TIME. "
        "STEP 1: For each macro-cycle, extract Tet_A and Tet_B completion order. "
        "STEP 2: Tet_A 3+1 holds if FACE_A7 (TIME) is last of the 4 Tet_A faces. "
        "STEP 3: Tet_B 3+1 holds if FACE_B0 (TIME) is last of the 4 Tet_B faces. "
        "OUTPUT: Conformance rates for Tet_A and Tet_B across all cycles."
    )
    commentary = (
        "If 3+1 holds for EVERY cycle, it is structural. If for MOST, the "
        "violations need explanation."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        report = a.get_report()
        total = len(a.macro_cycles)
        a7_positions = Counter()
        b0_positions = Counter()
        for c in a.macro_cycles:
            if 'FACE_A7' in c.tet_a_order:
                a7_positions[c.tet_a_order.index('FACE_A7')] += 1
            if 'FACE_B0' in c.tet_b_order:
                b0_positions[c.tet_b_order.index('FACE_B0')] += 1

        result = {
            "Total macro-cycles": total,
            "Tet_A 3+1 conforming": report['cycles_tet_a_3plus1'],
            "Tet_A 3+1 rate": round(report['cycles_a_3plus1_rate'], 4),
            "Tet_B 3+1 conforming": report['cycles_tet_b_3plus1'],
            "Tet_B 3+1 rate": round(report['cycles_b_3plus1_rate'], 4),
            "Both 3+1 conforming": report['cycles_both_3plus1'],
        }
        for pos in range(4):
            result[f"FACE_A7 at pos {pos}"] = a7_positions.get(pos, 0)
        for pos in range(4):
            result[f"FACE_B0 at pos {pos}"] = b0_positions.get(pos, 0)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class MacroCycleConsistency(GFDTest):
    """
    Verify all macro-cycles produce consistent structural patterns.
    """
    name = "Macro-Cycle Structural Consistency"
    question = "Are macro-cycle lengths consistent across the full traversal?"
    reference_source = "Engine regularity"
    tolerance = 0.0
    derivation = (
        "PREMISE: If the engine is regular, cycle lengths should be bounded. "
        "STEP 1: Calculate cycle length for each macro-cycle. "
        "STEP 2: Compute min, max, mean, std deviation. "
        "OUTPUT: Cycle length statistics and regularity assessment."
    )
    commentary = (
        "Consistent macro-cycle lengths indicate the engine completes its "
        "duty cycle reliably."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        if not a.macro_cycles:
            return {"Macro-cycles found": 0}
        lengths = [c.end_step - c.start_step + 1 for c in a.macro_cycles]
        mean_len = sum(lengths) / len(lengths)
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        return {
            "Macro-cycles found": len(a.macro_cycles),
            "Min cycle length": min(lengths),
            "Max cycle length": max(lengths),
            "Mean cycle length": round(mean_len, 1),
            "Std deviation": round(variance ** 0.5, 1),
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class MacroCycleLengthDistribution(GFDTest):
    """
    Deep statistical analysis of macro-cycle lengths: quartiles, IQR,
    coefficient of variation, and outlier detection.
    """
    name = "Macro-Cycle Length Distribution"
    question = (
        "What is the full statistical distribution of macro-cycle lengths, "
        "including quartiles, IQR, and coefficient of variation?"
    )
    reference_source = "Engine regularity"
    tolerance = 0.0
    derivation = (
        "PREMISE: Cycle length distribution reveals engine regularity. "
        "STEP 1: Compute Q1, Q2 (median), Q3 from sorted cycle lengths. "
        "STEP 2: IQR = Q3 - Q1. "
        "STEP 3: CoV = std / mean (normalized variability). "
        "STEP 4: Identify outlier cycles (beyond 1.5x IQR). "
        "OUTPUT: Full distribution statistics."
    )
    commentary = (
        "CoV < 0.5 suggests a reasonably tight distribution. Outlier cycles "
        "reveal pi-driven irregularities."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        if not a.macro_cycles:
            return {"Macro-cycles found": 0}
        lengths = sorted(c.end_step - c.start_step + 1 for c in a.macro_cycles)
        n = len(lengths)
        mean_l = sum(lengths) / n
        var_l = sum((l - mean_l) ** 2 for l in lengths) / n
        std_l = var_l ** 0.5
        q1 = lengths[n // 4]
        q2 = lengths[n // 2]
        q3 = lengths[3 * n // 4]
        iqr = q3 - q1
        low_fence = q1 - 1.5 * iqr
        high_fence = q3 + 1.5 * iqr
        outliers = sum(1 for l in lengths if l < low_fence or l > high_fence)
        return {
            "Total cycles": n,
            "Q1 (25th pctile)": q1,
            "Q2 (median)": q2,
            "Q3 (75th pctile)": q3,
            "IQR": iqr,
            "Mean": round(mean_l, 2),
            "Std deviation": round(std_l, 2),
            "Coefficient of variation": round(std_l / mean_l, 4) if mean_l > 0 else 0,
            "Min length": lengths[0],
            "Max length": lengths[-1],
            "Outlier cycles (1.5x IQR)": outliers,
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class FaceCompletionRank(GFDTest):
    """
    Which face completes first and last most often across macro-cycles?
    """
    name = "Face Completion Rank Statistics"
    question = (
        "Which faces tend to complete first and which tend to complete last "
        "in each macro-cycle?"
    )
    reference_source = "Face geometry + pi sequence"
    tolerance = 0.0
    derivation = (
        "PREMISE: In each macro-cycle, 8 faces complete in some order (rank 0-7). "
        "STEP 1: For each cycle, record the rank of each face. "
        "STEP 2: Count how often each face is first (rank 0) and last (rank 7). "
        "STEP 3: Compute mean rank per face across all cycles. "
        "OUTPUT: Per-face first/last counts and mean ranks."
    )
    commentary = (
        "Faces that consistently complete last gate the macro-cycle. "
        "This reveals which face is the bottleneck."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        if not a.macro_cycles:
            return {"Macro-cycles found": 0}
        total = len(a.macro_cycles)
        first_counts = Counter()
        last_counts = Counter()
        rank_sums = defaultdict(list)
        for c in a.macro_cycles:
            for rank, (fn, _) in enumerate(c.completion_order):
                rank_sums[fn].append(rank)
                if rank == 0:
                    first_counts[fn] += 1
                if rank == 7:
                    last_counts[fn] += 1
        result = {"Total cycles": total}
        for fn in FACE_NAMES_SORTED:
            ranks = rank_sums.get(fn, [])
            mean_rank = sum(ranks) / len(ranks) if ranks else -1
            result[f"{fn} first"] = first_counts.get(fn, 0)
            result[f"{fn} last"] = last_counts.get(fn, 0)
            result[f"{fn} mean rank"] = round(mean_rank, 2)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class CycleToOrbitRatio(GFDTest):
    """
    How many orbits per macro-cycle? How does this relate to alpha?
    """
    name = "Cycle-to-Orbit Ratio"
    question = (
        "How many orbits does it take to complete one macro-cycle, "
        "and how many macro-cycles fit into 137 orbits?"
    )
    reference_source = "Engine scaling"
    tolerance = 0.0
    derivation = (
        "PREMISE: An orbit = 8 cumsum units. A macro-cycle = all 8 faces complete. "
        "STEP 1: Compute total orbits and total macro-cycles. "
        "STEP 2: Orbits per cycle = total_orbits / total_cycles. "
        "STEP 3: Cycles in 137 orbits = 137 / orbits_per_cycle. "
        "OUTPUT: Scaling ratios and alpha correspondence."
    )
    commentary = (
        "The orbits-per-cycle ratio is a key structural constant. "
        "Its relationship to 1/137 may reveal deep connections."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total_orbits = len(a.orbits)
        total_cycles = len(a.macro_cycles)
        orbits_per_cycle = total_orbits / total_cycles if total_cycles > 0 else 0
        cycles_in_137 = 137 / orbits_per_cycle if orbits_per_cycle > 0 else 0
        orbit_lengths = [orb.steps_in_orbit for orb in a.orbits]
        mean_orbit_len = sum(orbit_lengths) / len(orbit_lengths) if orbit_lengths else 0
        return {
            "Total orbits": total_orbits,
            "Total macro-cycles": total_cycles,
            "Orbits per cycle": round(orbits_per_cycle, 2),
            "Cycles in 137 orbits": round(cycles_in_137, 2),
            "Mean steps per orbit": round(mean_orbit_len, 2),
            "Steps per 137 orbits": round(137 * mean_orbit_len, 1),
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


# ---------------------------------------------------------------------------
#  SECTION V: TRIGRAM ANALYSIS (Tests 18-19)
# ---------------------------------------------------------------------------

class TrigamReadIntegrity(GFDTest):
    """
    For each face in each macro-cycle, record the vertex read order.
    """
    name = "Trigram Read Sequence Analysis"
    question = (
        "What vertex read sequences (trigrams) does each face exhibit, "
        "and are all 6 orderings observed?"
    )
    reference_source = "Face geometry"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each face has 3 vertices read in some order per cycle. "
        "STEP 1: Extract the trigram per face per cycle. "
        "STEP 2: Count unique orderings per face. Max = 3! = 6. "
        "STEP 3: Total max = 8 faces x 6 = 48 unique trigrams. "
        "OUTPUT: Total unique trigrams observed."
    )
    commentary = (
        "Full trigram diversity (48/48) means pi explores all possible vertex "
        "read orderings — full ergodic coverage."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        if not a.macro_cycles:
            return {"Macro-cycles analyzed": 0}
        face_trigrams = {fn: [] for fn in FACES}
        for c in a.macro_cycles:
            for fn, reads in c.trigram_orders.items():
                vertex_order = tuple(v for v, _ in reads)
                if len(vertex_order) == 3:
                    face_trigrams[fn].append(vertex_order)
        total_unique = sum(len(set(face_trigrams[fn])) for fn in FACES)
        result = {
            "Macro-cycles analyzed": len(a.macro_cycles),
            "Total unique trigrams": total_unique,
            "Max possible (8 x 6)": 48,
            "Trigram diversity": round(total_unique / 48, 4),
        }
        for fn in FACE_NAMES_SORTED:
            result[f"{fn} unique orderings"] = len(set(face_trigrams[fn]))
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class TrigamEntropyPerFace(GFDTest):
    """
    Shannon entropy of trigram orderings per face.
    Max entropy = log2(6) ~ 2.585 bits when all 6 orderings equally likely.
    """
    name = "Trigram Entropy per Face"
    question = (
        "Is pi's traversal ergodic at the trigram level — does each face "
        "explore all orderings with roughly equal probability?"
    )
    reference_source = "Ergodic theory"
    tolerance = 0.05
    derivation = (
        "PREMISE: If pi is normal, each ordering should be ~equally likely. "
        "STEP 1: For each face, collect all trigram orderings across cycles. "
        "STEP 2: Compute Shannon entropy per face. "
        "STEP 3: Compare to max entropy log2(6) ~ 2.585 bits. "
        "OUTPUT: Per-face entropy and entropy ratios."
    )
    commentary = (
        "High trigram entropy means no preferred vertex ordering — the engine "
        "explores the full phase space of face reads."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        if not a.macro_cycles:
            return {"Macro-cycles analyzed": 0}
        face_trigrams = {fn: [] for fn in FACES}
        for c in a.macro_cycles:
            for fn, reads in c.trigram_orders.items():
                vertex_order = tuple(v for v, _ in reads)
                if len(vertex_order) == 3:
                    face_trigrams[fn].append(vertex_order)
        max_ent = math.log2(6)
        result = {"Max entropy (log2_6)": round(max_ent, 4)}
        entropies = []
        for fn in FACE_NAMES_SORTED:
            trigrams = face_trigrams[fn]
            if not trigrams:
                result[f"{fn} entropy"] = 0
                continue
            tcounts = Counter(trigrams)
            total = len(trigrams)
            ent = -sum((c / total) * math.log2(c / total) for c in tcounts.values() if c > 0)
            entropies.append(ent)
            result[f"{fn} entropy"] = round(ent, 4)
            result[f"{fn} ratio"] = round(ent / max_ent, 4)
        if entropies:
            result["Mean entropy"] = round(sum(entropies) / len(entropies), 4)
            result["Min entropy"] = round(min(entropies), 4)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


# ---------------------------------------------------------------------------
#  SECTION VI: CROSSING FORENSICS (Tests 20-22)
# ---------------------------------------------------------------------------

class FieldOriginCrossingPattern(GFDTest):
    """
    Track every Tet_A <-> Tet_B crossing.
    """
    name = "Field Origin Crossing Pattern"
    question = (
        "How frequently does the traversal cross between tetrahedra?"
    )
    reference_source = "Bimetric balance"
    tolerance = 0.10
    derivation = (
        "PREMISE: Balanced traversal should cross between tetrahedra regularly. "
        "STEP 1: Count total crossings. "
        "STEP 2: Compute crossing rate = crossings / total_steps. "
        "STEP 3: Track max gap. Compute Tet_A vs Tet_B step balance. "
        "OUTPUT: Crossing rate, max gap, balance ratio."
    )
    commentary = (
        "The crossing pattern reveals how the Field Origin couples the two "
        "tetrahedra. Regular crossings indicate tight coupling."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total_crossings = len(a.crossings)
        total_steps = len(a.steps)
        crossing_rate = total_crossings / total_steps if total_steps else 0
        tet_a_count = sum(1 for s in a.steps if s.tet == 'A')
        tet_b_count = total_steps - tet_a_count
        balance = min(tet_a_count, tet_b_count) / max(tet_a_count, tet_b_count) if max(tet_a_count, tet_b_count) > 0 else 0
        max_gap = 0
        current_gap = 1
        for i in range(1, total_steps):
            if a.steps[i].tet == a.steps[i - 1].tet:
                current_gap += 1
                max_gap = max(max_gap, current_gap)
            else:
                current_gap = 1
        return {
            "Total crossings": total_crossings,
            "Crossing rate": round(crossing_rate, 4),
            "Tet_A steps": tet_a_count,
            "Tet_B steps": tet_b_count,
            "Balance ratio": round(balance, 4),
            "Max same-tet gap": max_gap,
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class CrossingDirectionSymmetry(GFDTest):
    """
    Are A->B and B->A crossings balanced?
    """
    name = "Crossing Direction Symmetry"
    question = (
        "Are A->B crossings balanced against B->A crossings, "
        "indicating symmetric Field Origin coupling?"
    )
    reference_source = "Bimetric symmetry"
    tolerance = 0.10
    derivation = (
        "PREMISE: Symmetric coupling should produce equal A->B and B->A crossings. "
        "STEP 1: For each crossing, record from_tet and to_tet. "
        "STEP 2: Count A->B and B->A separately. Compute ratio. "
        "OUTPUT: Direction counts and symmetry ratio."
    )
    commentary = (
        "Directional symmetry means neither tetrahedron is a source or sink."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        ab = sum(1 for c in a.crossings if c.from_tet == 'A')
        ba = sum(1 for c in a.crossings if c.from_tet == 'B')
        ratio = ab / ba if ba > 0 else 0
        return {
            "Total crossings": len(a.crossings),
            "A->B crossings": ab,
            "B->A crossings": ba,
            "A->B / B->A ratio": round(ratio, 4),
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class SameTetGapDistribution(GFDTest):
    """
    Histogram of consecutive same-tetrahedron gaps.
    """
    name = "Same-Tet Gap Distribution"
    question = (
        "What is the distribution of consecutive same-tetrahedron runs, "
        "and how frequent are long gaps (8+ steps)?"
    )
    reference_source = "Crossing regularity"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each gap = consecutive steps in the same tetrahedron. "
        "STEP 1: Scan the step ledger for gap lengths. "
        "STEP 2: Build histogram: gap length -> frequency. "
        "STEP 3: Count gaps >= 8 (crossing-gap anomalies). "
        "OUTPUT: Gap distribution, mean, median, max, long-gap count."
    )
    commentary = (
        "Short gaps (1-2 steps) indicate tight oscillation. "
        "Long gaps indicate dwelling in one tetrahedron."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        if not a.steps:
            return {"Total steps": 0}
        gaps = []
        current_gap = 1
        for i in range(1, len(a.steps)):
            if a.steps[i].tet == a.steps[i - 1].tet:
                current_gap += 1
            else:
                gaps.append(current_gap)
                current_gap = 1
        gaps.append(current_gap)
        gap_counts = Counter(gaps)
        sorted_gaps = sorted(gaps)
        n = len(gaps)
        result = {
            "Total gaps": n,
            "Min gap": min(gaps),
            "Max gap": max(gaps),
            "Mean gap": round(sum(gaps) / n, 4),
            "Median gap": sorted_gaps[n // 2],
            "Gaps >= 8": sum(1 for g in gaps if g >= 8),
        }
        for length in range(1, 8):
            cnt = gap_counts.get(length, 0)
            result[f"Gap={length} count"] = cnt
            result[f"Gap={length} pct"] = round(cnt / n * 100, 1)
        return result

    def observations(self) -> Optional[Dict[str, float]]:
        return None


# ---------------------------------------------------------------------------
#  SECTION VII: STALL & VERTEX DYNAMICS (Tests 23-25)
# ---------------------------------------------------------------------------

class ZeroDigitStallAnalysis(GFDTest):
    """
    When digit = 0, cumsum doesn't change, vertex repeats.
    """
    name = "Zero Digit Stall Analysis"
    question = (
        "How do zero-digit stalls distribute across the traversal?"
    )
    reference_source = "Pi digit distribution"
    tolerance = 0.15
    derivation = (
        "PREMISE: Digit 0 causes no cumsum change. Expected ~12.5% (1/8). "
        "STEP 1: Count total zero-digit steps. "
        "STEP 2: Count stall clusters (3+ consecutive zeros). "
        "OUTPUT: Stall count, rate, cluster information."
    )
    commentary = (
        "Zero digits create redundant face reads without advancing the traversal."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total_zeros = sum(1 for s in a.steps if s.is_zero_digit)
        total = len(a.steps)
        stall_clusters = [an for an in a.anomalies if an.code == 'STALL_CLUSTER']
        return {
            "Total zero digits": total_zeros,
            "Zero rate": round(total_zeros / total, 4),
            "Expected rate (1/8)": round(1 / 8, 4),
            "Stall clusters (3+)": len(stall_clusters),
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class StallClusterDepth(GFDTest):
    """
    Deep analysis of zero-digit runs: max consecutive zeros,
    run length distribution.
    """
    name = "Stall Cluster Depth Analysis"
    question = (
        "What is the maximum consecutive zero run, and how do zero-run "
        "lengths distribute?"
    )
    reference_source = "Pi digit sequence"
    tolerance = 0.0
    derivation = (
        "PREMISE: Consecutive zeros cause repeated vertex stalls. "
        "STEP 1: Scan for runs of consecutive zero digits. "
        "STEP 2: Build histogram of run lengths. "
        "STEP 3: For base-8, P(run >= k) ~ (1/8)^k. "
        "OUTPUT: Run length distribution and comparison to expected."
    )
    commentary = (
        "Long zero runs are rare but impactful — they freeze the engine. "
        "At 10k digits, we expect ~1-2 runs of length 4+."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        zero_runs = []
        run_len = 0
        for s in a.steps:
            if s.is_zero_digit:
                run_len += 1
            else:
                if run_len > 0:
                    zero_runs.append(run_len)
                run_len = 0
        if run_len > 0:
            zero_runs.append(run_len)
        run_counts = Counter(zero_runs)
        total_runs = len(zero_runs)
        max_run = max(zero_runs) if zero_runs else 0
        mean_run = sum(zero_runs) / total_runs if total_runs else 0
        total = len(a.steps)
        return {
            "Total zero-runs": total_runs,
            "Max consecutive zeros": max_run,
            "Mean run length": round(mean_run, 4),
            "Runs of length 1": run_counts.get(1, 0),
            "Runs of length 2": run_counts.get(2, 0),
            "Runs of length 3": run_counts.get(3, 0),
            "Runs of length 4+": sum(c for l, c in run_counts.items() if l >= 4),
            "Expected runs >= 3 (N/512)": round(total / 512, 1),
            "Actual runs >= 3": sum(c for l, c in run_counts.items() if l >= 3),
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


class VertexAutocorrelation(GFDTest):
    """
    Measure consecutive same-vertex rate and vertex repeat patterns.
    """
    name = "Vertex Autocorrelation"
    question = (
        "How often does the same vertex appear on consecutive steps, "
        "and does this match the digit=0 frequency?"
    )
    reference_source = "Traversal dynamics"
    tolerance = 0.05
    derivation = (
        "PREMISE: Same vertex on consecutive steps requires digit = 0. "
        "STEP 1: Count consecutive same-vertex pairs. "
        "STEP 2: Rate should ~ P(digit=0) ~ 1/8. "
        "STEP 3: Check: does same-vertex always correspond to digit=0? "
        "OUTPUT: Repeat rate, expected rate, digit=0 correspondence."
    )
    commentary = (
        "Vertex autocorrelation should be entirely explained by digit=0. "
        "If it exceeds the zero rate, something unexpected is happening."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        total = len(a.steps)
        same_vertex = 0
        same_vertex_and_zero = 0
        same_vertex_not_zero = 0
        for i in range(1, total):
            if a.steps[i].vertex == a.steps[i - 1].vertex:
                same_vertex += 1
                if a.steps[i].is_zero_digit:
                    same_vertex_and_zero += 1
                else:
                    same_vertex_not_zero += 1
        pairs = total - 1
        zero_count = sum(1 for s in a.steps if s.is_zero_digit)
        return {
            "Consecutive same-vertex": same_vertex,
            "Same-vertex rate": round(same_vertex / pairs, 6) if pairs else 0,
            "Expected (= zero rate)": round(zero_count / total, 6),
            "Same-vertex AND digit=0": same_vertex_and_zero,
            "Same-vertex NOT digit=0": same_vertex_not_zero,
            "All repeats from digit=0": 1 if same_vertex_not_zero == 0 else 0,
        }

    def observations(self) -> Optional[Dict[str, float]]:
        return None


# ---------------------------------------------------------------------------
#  SECTION VIII: SUMMARY (Test 26)
# ---------------------------------------------------------------------------

class FullAnomalyReport(GFDTest):
    """
    Comprehensive anomaly summary from the entire N-digit analysis.
    """
    name = f"Full Anomaly Report ({N_DIGITS} digits)"
    question = (
        f"What anomalies were detected across {N_DIGITS} digits, "
        "and are there any CRITICAL or ERROR-severity issues?"
    )
    reference_source = "Anomaly detection"
    tolerance = 0.0
    derivation = (
        "PREMISE: The analyzer detects anomalies during traversal. "
        "STEP 1: Count anomalies by severity: CRITICAL, ERROR, WARNING, INFO. "
        "STEP 2: Zero CRITICAL + zero ERROR = engine verified. "
        "OUTPUT: Anomaly counts by severity."
    )
    commentary = (
        "The anomaly report is the executive summary. Zero CRITICAL and "
        "zero ERROR = NASA-level verification passed."
    )

    def model(self) -> Dict[str, float]:
        a = _analyzer()
        report = a.get_report()
        table_rows = []
        for an in a.anomalies[:20]:
            table_rows.append([an.severity, an.code, an.step, an.description[:60]])
        if table_rows:
            self.table = {
                "title": "Anomaly Details",
                "headers": ["Severity", "Code", "Step", "Description"],
                "rows": table_rows,
                "footer": f"Showing first 20 of {len(a.anomalies)}" if len(a.anomalies) > 20 else None,
            }
        return {
            "CRITICAL anomalies": report['anomalies_critical'],
            "ERROR anomalies": report['anomalies_error'],
            "WARNING anomalies": report['anomalies_warning'],
            "INFO anomalies": report['anomalies_info'],
            "Total anomalies": report['anomalies_total'],
            "Engine verified": 1 if (report['anomalies_critical'] == 0 and report['anomalies_error'] == 0) else 0,
        }

    def observations(self) -> Dict[str, float]:
        return {
            "CRITICAL anomalies": 0,
            "ERROR anomalies": 0,
            "Engine verified": 1,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    # Section I: Integrity
    StepLedgerIntegrity,
    ComplementIntegrity,
    LinearGuaranteesNonLinear,
    # Section II: Distributions
    DigitDistribution,
    VertexDistribution,
    TetrahedronBalance,
    ComplementPairActivity,
    # Section III: Face Mechanics
    OrbitFaceTargeting,
    PerOrbitFaceCoverage,
    RedundantReadDistribution,
    FaceFirstCompletion,
    # Section IV: Macro-Cycle Analysis
    TrigamCompletionOrder,
    ThreePlusOnePattern,
    MacroCycleConsistency,
    MacroCycleLengthDistribution,
    FaceCompletionRank,
    CycleToOrbitRatio,
    # Section V: Trigram Analysis
    TrigamReadIntegrity,
    TrigamEntropyPerFace,
    # Section VI: Crossing Forensics
    FieldOriginCrossingPattern,
    CrossingDirectionSymmetry,
    SameTetGapDistribution,
    # Section VII: Stall & Vertex Dynamics
    ZeroDigitStallAnalysis,
    StallClusterDepth,
    VertexAutocorrelation,
    # Section VIII: Summary
    FullAnomalyReport,
]


def run_all_tests() -> bool:
    """Run all engine cross-check tests."""
    return run_test_group(
        title=f"Engine Cross-Checks ({N_DIGITS} Digits)",
        summary=(
            f"NASA-level verification of the pi base-8 traversal engine at {N_DIGITS} "
            "digit scale. The traversal runs ONCE into a complete step-by-step ledger. "
            "All 26 tests query this ledger. Tests are organized into 8 sections: "
            "Integrity (3), Distributions (4), Face Mechanics (4), Macro-Cycle Analysis "
            "(6), Trigram Analysis (2), Crossing Forensics (3), Stall & Vertex Dynamics "
            "(3), and Summary (1). Zero CRITICAL/ERROR anomalies = VERIFIED."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    success = run_all_tests()
    import sys as _sys
    _sys.exit(0 if success else 1)
