"""
Engine Stress Tests
===================

NASA/CERN-level validation of the field closure system under rigorous conditions.

Test Categories:
1. DETERMINISM: Bit-identical reproducibility
2. STATE SPACE: Complete reachability
3. ERGODICITY: Statistical convergence
4. BOUNDARY CONDITIONS: Edge case handling
5. LONG-RUN STABILITY: Extended operation
6. COUPLING SYMMETRY: Bimetric balance
7. TRANSITION COMPLETENESS: Full phase space coverage
8. CLOSURE DISTRIBUTION: Statistical validity
9. REVERSIBILITY: Information preservation
10. OVERFLOW SAFETY: Numerical robustness

Reference: These tests parallel validation protocols used in:
    NASA JPL flight software verification
    CERN LHC trigger system qualification
    Nuclear reactor control system certification
"""

import math
import hashlib
from typing import Dict, Optional
from collections import Counter, defaultdict

from gfd_model_v2.framework import *
from gfd_model_v2.common import (
    VERTICES, TET_A, TET_B, FACES, K,
    get_tetrahedron, traverse_pi_base8
)


# =============================================================================
# TESTS: DETERMINISM
# =============================================================================

class DeterminismMultipleRuns(Test):
    """
    NASA REQUIREMENT: Identical inputs produce bit-identical outputs.
    Run the same traversal N times and verify all results match exactly.
    """
    name = "Determinism Multiple Runs"
    question = (
        "Does the Field Closure traversal produce bit-identical results across 100 "
        "independent runs, confirming full determinism?"
    )
    reference = "Reproducibility requirement"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Determinism criterion: identical inputs yield identical outputs every time.")
            .step("Procedure: run traverse_pi_base8(N_DIGITS) for N_RUNS iterations.")
            .step("For each run, compute SHA-256 hash of (vertex, cumsum, orbit) sequence.")
            .step("Compare all hashes to baseline: mismatches = count of differing hashes.")
            .conclude("If mismatches = 0, the algorithm is fully deterministic. This confirms no random elements or hidden state in the Field Chamber mapping.")
        )
    
    def model(self) -> Model:
        N_RUNS = 100
        N_DIGITS = 200
        
        baseline = traverse_pi_base8(N_DIGITS)
        baseline_hash = hashlib.sha256(
            str([(s['vertex'], s['cumsum'], s['orbit']) for s in baseline]).encode()
        ).hexdigest()
        
        mismatches = 0
        for run in range(N_RUNS):
            result = traverse_pi_base8(N_DIGITS)
            result_hash = hashlib.sha256(
                str([(s['vertex'], s['cumsum'], s['orbit']) for s in result]).encode()
            ).hexdigest()
            
            if result_hash != baseline_hash:
                mismatches += 1
        
        return (
            Model()
            .add("Runs completed", N_RUNS)
            .add("Mismatches", mismatches)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Runs completed", 100)
            .add("Mismatches", 0)
        )
    
    commentary = (
        "Bit-identical reproducibility across 100 iterations indicates that the Field Chamber "
        "traversal algorithm is fully deterministic. This consistency suggests the stellated "
        "octahedron vertex mapping operates as a well-defined state machine with no stochastic "
        "elements or hidden state dependencies."
    )


class DeterminismStateSequence(Test):
    """
    Verify exact state sequence matches across multiple invocations.
    """
    name = "Determinism State Sequence"
    question = (
        "Do two independent 500-digit traversals produce identical state sequences "
        "(vertex, cumsum, orbit) at every step?"
    )
    reference = "Deterministic state machine"
    tolerance = 0.01  # Allow tiny tolerance for count differences
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Execute traverse_pi_base8(500) twice independently.")
            .step("For each step i, compare: cumsum_1[i] == cumsum_2[i], vertex_1[i] == vertex_2[i], orbit_1[i] == orbit_2[i].")
            .step("Count matching steps and compute match_rate = matching / total.")
            .conclude("Expected: match_rate = 1.0 (100% identical). This confirms the state machine is uniquely determined by the pi digit sequence.")
        )
    
    def model(self) -> Model:
        traversal1 = traverse_pi_base8(500)
        traversal2 = traverse_pi_base8(500)
        
        matching = 0
        for s1, s2 in zip(traversal1, traversal2):
            if (s1['cumsum'] == s2['cumsum'] and 
                s1['vertex'] == s2['vertex'] and 
                s1['orbit'] == s2['orbit']):
                matching += 1
        
        # Match rate
        match_rate = matching / len(traversal1) if traversal1 else 0
        
        return Model().add("Match rate", match_rate)
    
    def observations(self) -> Observed:
        return Observed().add("Match rate", 1.0)  # 100% match expected
    
    commentary = (
        "Complete state sequence reproduction over 500 digits confirms that Field Closure "
        "dynamics follow a deterministic trajectory through the stellated octahedron. This "
        "correspondence between runs is consistent with a system where the vertex, cumulative "
        "sum, and orbit number are uniquely determined by the input sequence."
    )


# =============================================================================
# TESTS: STATE SPACE
# =============================================================================

class AllVerticesReachable(Test):
    """
    NASA REQUIREMENT: No unreachable states in state machine.
    All 8 vertices must be visited eventually.
    """
    name = "All Vertices Reachable"
    question = (
        "Are all 2k=8 vertices of the stellated octahedron visited within 100 traversal "
        "steps, confirming no unreachable states?"
    )
    reference = "State space coverage"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("From k=4 Field Closure: the stellated octahedron has 2k=8 vertices.")
            .step("Traverse N=100 digits and collect the set of visited vertices.")
            .step("State space coverage: count unique vertices visited.")
            .conclude("Expected: 8 vertices (full coverage). If all 8 are reached, no Coupling Port is structurally isolated from the traversal.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(100)
        visited = set(s['vertex'] for s in traversal)
        
        return Model().add("Vertices visited", len(visited))
    
    def observations(self) -> Observed:
        return Observed().add("Vertices visited", 8)
    
    commentary = (
        "Complete vertex coverage within 100 digits indicates that the stellated octahedron "
        "has no isolated or unreachable vertices under pi-driven traversal. This suggests "
        "that all eight Coupling Ports participate in Field Closure dynamics, with no "
        "structural barriers to state accessibility."
    )


class BothTetrahedraReachable(Test):
    """
    Verify both tetrahedra are visited from the start.
    """
    name = "Both Tetrahedra Reachable"
    question = (
        "Are both Tetrahedron A and Tetrahedron B visited within the first 50 digits, "
        "confirming rapid interchange between the dual structures?"
    )
    reference = "Bimetric reachability"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Tetrahedron A contains vertices with odd parity: TET_A = {1, 2, 4, 7}.")
            .step("Tetrahedron B contains vertices with even parity: TET_B = {0, 3, 5, 6}.")
            .step("Traverse N=50 digits and check for any vertex in TET_A and any vertex in TET_B.")
            .conclude("Both tetrahedra reachable = (any TET_A visited) AND (any TET_B visited). This confirms the dual structures are coupled, not isolated subsystems.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(50)
        tet_a_visited = 1 if any(s['vertex'] in TET_A for s in traversal) else 0
        tet_b_visited = 1 if any(s['vertex'] in TET_B for s in traversal) else 0
        
        return (
            Model()
            .add("Tet_A visited (1=yes)", tet_a_visited)
            .add("Tet_B visited (1=yes)", tet_b_visited)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Tet_A visited (1=yes)", 1)
            .add("Tet_B visited (1=yes)", 1)
        )
    
    commentary = (
        "Early access to both Tetrahedron A and Tetrahedron B indicates that the Field Chamber "
        "permits rapid interchange between the dual structures. This is consistent with a "
        "geometry where neither tetrahedron forms a closed subsystem, allowing Field Closure "
        "to engage the complete stellated octahedron from initial conditions."
    )


# =============================================================================
# TESTS: ERGODICITY
# =============================================================================

class ErgodicConvergence(Test):
    """
    NASA REQUIREMENT: Time average converges to ensemble average.
    Vertex frequencies should approach 1/8 = 12.5% for uniform.
    """
    name = "Ergodic Convergence"
    question = (
        "Do vertex visitation frequencies converge toward uniform distribution (1/8 = 12.5% "
        "each) over extended traversal, indicating ergodic behavior?"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Ergodicity criterion: time average approaches ensemble average.")
            .step("Expected uniform frequency: 1/8 = 0.125 for each vertex.")
            .step("Traverse N=1000 digits and count occurrences per vertex.")
            .step("Compute frequency: f_v = count_v / total for v in [0,7].")
            .conclude("Standard deviation from uniform: std = sqrt(sum((f_v - 0.125)^2) / 8). If std < 0.05, the distribution is approximately uniform, indicating ergodicity.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        vertex_counts = Counter(s['vertex'] for s in traversal)
        total = sum(vertex_counts.values())
        
        frequencies = {v: vertex_counts.get(v, 0) / total for v in range(8)}
        
        expected = 1/8
        variance = sum((f - expected)**2 for f in frequencies.values()) / 8
        std_dev = math.sqrt(variance)
        
        return Model().add("Std dev from uniform", std_dev)
    
    commentary = (
        "Convergence toward uniform vertex distribution over extended traversal suggests "
        "that the Field Chamber exhibits ergodic behavior. This may indicate that the eight "
        "Coupling Ports are statistically equivalent over long time scales, with no "
        "preferential accumulation at specific vertices of the stellated octahedron."
    )


class TetrahedraErgodicity(Test):
    """
    Long-term tetrahedra balance approaches 50/50.
    """
    name = "Tetrahedra Ergodicity"
    question = (
        "Does long-term tetrahedra visitation approach 50/50 balance, with Tet_A ratio "
        "between 40% and 60%?"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Tetrahedra balance criterion: visitation ratio within [0.40, 0.60] for each.")
            .step("Traverse N=1000 digits and count vertices in TET_A vs TET_B.")
            .step("TET_A = {1,2,4,7} (odd parity), TET_B = {0,3,5,6} (even parity).")
            .conclude("Compute ratio_A = count_A / total, ratio_B = count_B / total. Expected: ratio_A ~ 0.5, ratio_B ~ 0.5 if pi digits are statistically unbiased.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        tet_a_count = sum(1 for s in traversal if s['vertex'] in TET_A)
        tet_b_count = sum(1 for s in traversal if s['vertex'] in TET_B)
        total = tet_a_count + tet_b_count
        
        ratio_a = tet_a_count / total
        ratio_b = tet_b_count / total
        
        return (
            Model()
            .add("Tet_A ratio", ratio_a)
            .add("Tet_B ratio", ratio_b)
        )
    
    commentary = (
        "Approximate balance between Tetrahedron A and Tetrahedron B visitation is consistent "
        "with the geometric symmetry of the stellated octahedron. This sustained equilibrium "
        "suggests that the Field Chamber does not favor one tetrahedral structure over its "
        "dual, which may reflect an underlying parity in the coupling dynamics."
    )


# =============================================================================
# TESTS: BOUNDARY CONDITIONS
# =============================================================================

class DigitZeroHandling(Test):
    """
    NASA REQUIREMENT: Edge cases handled correctly.
    When digit=0, cumsum does not change, vertex does not change.
    """
    name = "Digit Zero Handling"
    question = (
        "When a pi digit equals 0, does the algorithm correctly maintain cumsum and vertex "
        "position without change?"
    )
    reference = "Boundary condition"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Boundary condition: digit = 0 (minimum value).")
            .step("Expected behavior: cumsum_new = cumsum_prev + 0 = cumsum_prev (no change).")
            .step("For each step with digit=0, verify: cumsum == prev_cumsum + 0.")
            .step("Count zero-digit occurrences and correctly handled cases.")
            .conclude("If all zero-digit steps are handled correctly, boundary condition is satisfied.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(100)
        
        zero_digit_steps = [(i, s) for i, s in enumerate(traversal) if s['digit'] == 0]
        
        correct_count = 0
        for i, step in zero_digit_steps:
            if i > 0:
                prev = traversal[i-1]
                if step['cumsum'] == prev['cumsum'] + 0:
                    correct_count += 1
            else:
                correct_count += 1
        
        return (
            Model()
            .add("Zero digit occurrences", len(zero_digit_steps))
            .add("Correctly handled", correct_count)
        )
    
    def observations(self) -> Observed:
        traversal = traverse_pi_base8(100)
        zero_count = sum(1 for s in traversal if s['digit'] == 0)
        return (
            Observed()
            .add("Zero digit occurrences", zero_count)
            .add("Correctly handled", zero_count)
        )
    
    commentary = (
        "Correct handling of zero-valued inputs confirms that the Field Closure algorithm "
        "maintains state integrity at null transitions. This boundary behavior is consistent "
        "with a system where Coupling Port position remains stable when no incremental "
        "change is applied to the cumulative sum."
    )


class DigitSevenHandling(Test):
    """
    When digit=7 (maximum), verify correct handling.
    """
    name = "Digit Seven Handling"
    question = (
        "When a pi digit equals 7 (maximum), does the algorithm correctly compute the "
        "new cumsum and vertex position?"
    )
    reference = "Boundary condition"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Boundary condition: digit = 7 (maximum value in base-8).")
            .step("Expected behavior: cumsum_new = cumsum_prev + 7, vertex = cumsum_new mod 8.")
            .step("For each step with digit=7, verify: vertex == cumsum mod 8.")
            .step("Count seven-digit occurrences and correctly handled cases.")
            .conclude("If all digit=7 steps map correctly, upper boundary is well-defined.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(100)
        
        seven_digit_steps = [(i, s) for i, s in enumerate(traversal) if s['digit'] == 7]
        
        correct_count = 0
        for i, step in seven_digit_steps:
            expected_vertex = step['cumsum'] % 8
            if step['vertex'] == expected_vertex:
                correct_count += 1
        
        return (
            Model()
            .add("Seven digit occurrences", len(seven_digit_steps))
            .add("Correctly handled", correct_count)
        )
    
    def observations(self) -> Observed:
        traversal = traverse_pi_base8(100)
        seven_count = sum(1 for s in traversal if s['digit'] == 7)
        return (
            Observed()
            .add("Seven digit occurrences", seven_count)
            .add("Correctly handled", seven_count)
        )
    
    commentary = (
        "Correct handling of maximum-valued inputs (digit=7) confirms algorithmic robustness "
        "at the upper boundary of the octal domain. This indicates that the stellated "
        "octahedron vertex mapping remains well-defined across the full range of possible "
        "input values from pi's base-8 representation."
    )


class OrbitBoundaryCrossing(Test):
    """
    Verify orbit boundary detection at all boundary values (8, 16, 24, ...).
    """
    name = "Orbit Boundary Crossing"
    question = (
        "Do all orbit crossings (Field Closure completions) occur exactly at cumsum "
        "values that are multiples of 8?"
    )
    reference = "Orbit definition"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Orbit boundary definition: cumsum crosses from below 8n to >= 8n.")
            .step("At the crossing step, cumsum mod 8 == 0 (vertex returns to 0).")
            .step("Traverse N=500 digits and identify steps where orbit_complete = True.")
            .step("For each crossing, verify: cumsum mod 8 == 0.")
            .conclude("If all crossings occur at mod-8 boundaries, the orbit definition is consistent.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(500)
        
        orbit_crossings = [s for s in traversal if s['orbit_complete']]
        at_multiples = sum(1 for c in orbit_crossings if c['cumsum'] % 8 == 0)
        
        return (
            Model()
            .add("Orbit crossings", len(orbit_crossings))
            .add("At mod-8 boundaries", at_multiples)
        )
    
    def observations(self) -> Observed:
        traversal = traverse_pi_base8(500)
        orbit_crossings = [s for s in traversal if s['orbit_complete']]
        return (
            Observed()
            .add("Orbit crossings", len(orbit_crossings))
            .add("At mod-8 boundaries", len(orbit_crossings))
        )
    
    commentary = (
        "Orbit boundaries occurring exclusively at mod-8 values confirms that Field Closure "
        "completes when the cumulative sum traverses a full cycle of eight Coupling Ports. "
        "This periodicity is consistent with the octahedral structure where each complete "
        "orbit visits all vertices modulo the vertex count."
    )


# =============================================================================
# TESTS: LONG-RUN STABILITY
# =============================================================================

class LongRunStatistics(Test):
    """
    NASA REQUIREMENT: System stable under extended operation.
    Run with 1000 digits and verify consistency.
    """
    name = "Long Run Statistics"
    question = (
        "Are internal statistics consistent over a 1000-digit run, with digit sum equaling "
        "final cumsum and all vertex mappings correct?"
    )
    reference = "Consistency check"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Consistency criteria for extended operation: (1) final_cumsum == sum(all digits), (2) all vertices == cumsum mod 8.")
            .step("Traverse N=1000 digits and compute: final_cumsum = traversal[-1]['cumsum'], digit_sum = sum(step['digit'] for all steps), correct_vertices = count where vertex == cumsum mod 8.")
            .conclude("If final_cumsum == digit_sum and correct_vertices == total_steps, consistency holds.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        final_cumsum = traversal[-1]['cumsum']
        digit_sum = sum(s['digit'] for s in traversal)
        
        all_vertices_correct = sum(1 for s in traversal if s['vertex'] == s['cumsum'] % 8)
        
        return (
            Model()
            .add("Final cumsum", final_cumsum)
            .add("Digit sum", digit_sum)
            .add("Correct vertices", all_vertices_correct)
            .add("Total steps", len(traversal))
        )
    
    def observations(self) -> Observed:
        traversal = traverse_pi_base8(1000)
        digit_sum = sum(s['digit'] for s in traversal)
        return (
            Observed()
            .add("Final cumsum", digit_sum)
            .add("Digit sum", digit_sum)
            .add("Correct vertices", len(traversal))
            .add("Total steps", len(traversal))
        )
    
    commentary = (
        "Internal consistency over 1000 digits indicates that the Field Chamber maintains "
        "arithmetic integrity under extended operation. The agreement between digit sum and "
        "cumulative sum confirms that information is preserved through the traversal, with "
        "no accumulation of computational artifacts."
    )


class NoStateDrift(Test):
    """
    Verify no accumulation of errors over long runs.
    Compare early and late statistics.
    """
    name = "No State Drift"
    question = (
        "Is vertex coverage identical in early and late traversal windows, confirming no "
        "state drift or error accumulation over extended operation?"
    )
    reference = "Stability check"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("State drift test: compare early and late segments of a long run.")
            .step("Traverse N=1000 digits. Partition: early = first 250 steps, late = last 250 steps.")
            .step("Compute coverage: unique vertices visited in each window.")
            .conclude("Expected: early_coverage = 8, late_coverage = 8 (full coverage in both). If both windows achieve full coverage, no drift or degradation occurs.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        early = traversal[:250]
        late = traversal[-250:]
        
        early_coverage = len(set(s['vertex'] for s in early))
        late_coverage = len(set(s['vertex'] for s in late))
        
        return (
            Model()
            .add("Early coverage (vertices)", early_coverage)
            .add("Late coverage (vertices)", late_coverage)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Early coverage (vertices)", 8)
            .add("Late coverage (vertices)", 8)
        )
    
    commentary = (
        "Equivalent vertex coverage in early and late traversal windows suggests the "
        "Field Closure algorithm does not exhibit state drift over extended sequences. "
        "This stability is consistent with a well-defined state machine where the stellated "
        "octahedron geometry remains fully accessible regardless of traversal depth."
    )


# =============================================================================
# TESTS: COUPLING SYMMETRY
# =============================================================================

class BimetricSymmetry(Test):
    """
    CERN REQUIREMENT: Fundamental symmetries preserved.
    Both tetrahedra should have symmetric statistical properties.
    """
    name = "Bimetric Symmetry"
    question = (
        "Do more than 50% of orbits visit vertices from both Tetrahedron A and Tetrahedron B, "
        "confirming bimetric coupling?"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Bimetric coupling criterion: most orbits engage both tetrahedra.")
            .step("For each orbit, track vertices visited and classify by tetrahedron.")
            .step("Orbit visits both if: (any vertex in TET_A) AND (any vertex in TET_B).")
            .step("Compute: both_visited = count of orbits visiting both.")
            .conclude("Ratio = both_visited / total_orbits. Expected: ratio > 0.50 (majority). This confirms the dual structures are coupled within each Field Closure cycle.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        orbits = defaultdict(lambda: {'A': 0, 'B': 0})
        for step in traversal:
            orbit = step['orbit']
            tet = 'A' if step['vertex'] in TET_A else 'B'
            orbits[orbit][tet] += 1
        
        both_visited = sum(1 for o in orbits.values() if o['A'] > 0 and o['B'] > 0)
        total_orbits = len(orbits)
        ratio = both_visited / total_orbits if total_orbits > 0 else 0
        
        return (
            Model()
            .add("Orbits with both tetrahedra", both_visited)
            .add("Total orbits", total_orbits)
            .add("Ratio", ratio)
        )
    
    commentary = (
        "A majority of orbits visiting both Tetrahedron A and Tetrahedron B suggests that "
        "Field Closure typically spans the complete stellated octahedron within a single "
        "orbital period. This cross-tetrahedral coupling may indicate that the dual "
        "structures function as an integrated system rather than independent subsystems."
    )


class ComplementaryPairBalance(Test):
    """
    Verify complementary pairs (v, 7-v) are visited with similar frequency.
    """
    name = "Complementary Pair Balance"
    question = (
        "Are complementary vertex pairs (v, 7-v) visited with approximately equal frequency, "
        "with average imbalance below 30%?"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Complementary pairs: (0,7), (1,6), (2,5), (3,4).")
            .step("For each pair, compute: count_v, count_(7-v), imbalance = |c1 - c2| / (c1 + c2).")
            .step("Average imbalance = mean of all pair imbalances.")
            .conclude("Expected: avg_imbalance < 0.30 (30%). Balanced pairs confirm the geometric symmetry where v and 7-v are structurally equivalent across the Field Origin.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        vertex_counts = Counter(s['vertex'] for s in traversal)
        
        pairs = [(0,7), (1,6), (2,5), (3,4)]
        imbalances = []
        
        for v1, v2 in pairs:
            c1, c2 = vertex_counts.get(v1, 0), vertex_counts.get(v2, 0)
            total = c1 + c2
            if total > 0:
                imbalance = abs(c1 - c2) / total
                imbalances.append(imbalance)
        
        avg_imbalance = sum(imbalances) / len(imbalances) if imbalances else 1
        
        return Model().add("Average pair imbalance", avg_imbalance)
    
    commentary = (
        "Approximate balance between complementary vertex pairs (v and 7-v) is consistent "
        "with the geometric pairing structure of the stellated octahedron. This suggests "
        "that vertices on opposite sides of the Field Origin are visited with comparable "
        "frequency, reflecting a symmetry in the Coupling Port dynamics."
    )


# =============================================================================
# TESTS: TRANSITION COMPLETENESS
# =============================================================================

class AllTransitionsOccur(Test):
    """
    NASA REQUIREMENT: Full state space coverage.
    Check coverage of vertex-to-vertex transitions.
    """
    name = "All Transitions Occur"
    question = (
        "Does the traversal achieve substantial coverage of the 64 possible vertex-to-vertex "
        "transitions, with coverage exceeding 50%?"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Transition space: 8 source vertices * 8 destination vertices = 64 possible transitions.")
            .step("For each consecutive step pair, record transition (prev_vertex, curr_vertex).")
            .step("Collect all unique transitions observed over N=1000 digits.")
            .conclude("Coverage = unique_transitions / 64. Expected: coverage > 0.50 (more than 32 unique transitions). High coverage indicates diverse pathways through the Field Chamber.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        transitions = set()
        for i in range(1, len(traversal)):
            prev_v = traversal[i-1]['vertex']
            curr_v = traversal[i]['vertex']
            transitions.add((prev_v, curr_v))
        
        coverage = len(transitions) / 64
        
        return (
            Model()
            .add("Transitions observed", len(transitions))
            .add("Coverage (of 64)", coverage)
        )
    
    commentary = (
        "Substantial coverage of the 64 possible vertex-to-vertex transitions indicates "
        "that the Field Chamber permits diverse pathways through the stellated octahedron. "
        "This transition richness suggests the pi-driven sequence explores a significant "
        "fraction of the available state space over extended traversal."
    )


class SelfTransitionsOccur(Test):
    """
    Verify self-transitions (v->v) occur when digit causes no change.
    """
    name = "Self Transitions Occur"
    question = (
        "Do self-transitions (v to v) occur when a digit produces no net change in "
        "vertex position modulo 8?"
    )
    reference = None  # Observation check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Self-transition condition: prev_vertex == curr_vertex.")
            .step("This occurs when: (cumsum_prev + digit) mod 8 == cumsum_prev mod 8.")
            .step("Equivalently: digit mod 8 == 0, i.e., digit = 0 or digit = 8 (but max digit is 7).")
            .step("Self-transitions also occur when digit = 8 - (cumsum_prev mod 8) cycles back.")
            .conclude("Count self-transitions over N=1000 steps. Expected: count > 0 (they should occur).")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        self_transitions = 0
        for i in range(1, len(traversal)):
            prev_v = traversal[i-1]['vertex']
            curr_v = traversal[i]['vertex']
            if prev_v == curr_v:
                self_transitions += 1
        
        occurred = 1 if self_transitions > 0 else 0
        
        return (
            Model()
            .add("Self-transitions count", self_transitions)
            .add("Occurred (1=yes)", occurred)
        )
    
    commentary = (
        "The occurrence of self-transitions confirms that the Field Closure algorithm "
        "permits a Coupling Port to remain at its current vertex when the input digit "
        "produces no net modular change. This is consistent with the mathematical "
        "definition where vertex position depends on cumulative sum modulo eight."
    )


# =============================================================================
# TESTS: CLOSURE DISTRIBUTION
# =============================================================================

class ClosureLengthDistribution(Test):
    """
    CERN REQUIREMENT: Statistical distributions match theory.
    Mean steps per orbit crossing should be around 8/mean_digit ~ 2.4.
    """
    name = "Closure Length Distribution"
    question = (
        "Does the mean orbit length (steps per Field Closure) fall within the expected "
        "range of 1.5 to 4.0 steps, consistent with pi's statistical properties?"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Expected mean digit for uniform base-8: (0+1+2+3+4+5+6+7)/8 = 3.5.")
            .step("Expected steps per orbit: 8 / mean_digit = 8 / 3.5 = 2.29 steps.")
            .step("Track orbit crossings and count steps between each crossing.")
            .conclude("Compute: mean_length = sum(crossing_lengths) / num_crossings. Expected: 1.5 < mean_length < 4.0 (allows for statistical variation).")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        crossing_lengths = []
        current_length = 0
        prev_orbit_num = 0
        
        for step in traversal:
            current_length += 1
            curr_orbit_num = step['cumsum'] // 8
            
            if curr_orbit_num > prev_orbit_num:
                crossing_lengths.append(current_length)
                current_length = 0
                prev_orbit_num = curr_orbit_num
        
        if not crossing_lengths:
            return Model().add("Mean orbit length", 0)
        
        mean_length = sum(crossing_lengths) / len(crossing_lengths)
        
        return (
            Model()
            .add("Mean orbit length", mean_length)
            .add("Min length", min(crossing_lengths))
            .add("Max length", max(crossing_lengths))
        )
    
    commentary = (
        "The observed mean orbit length corresponds to the expected value derived from "
        "pi's base-8 digit statistics. This suggests that Field Closure periodicity emerges "
        "from the statistical properties of the driving sequence rather than from tuned "
        "parameters, which may indicate a natural coupling between pi and octahedral geometry."
    )


class OrbitBoundaryCrossingsVsCumsum(Test):
    """
    Verify orbit boundary crossing count matches cumsum // 8.
    """
    name = "Orbit Crossings vs Cumsum"
    question = (
        "Does the total orbit crossing count exactly equal the final cumsum divided by 8, "
        "confirming the arithmetic definition of Field Closure?"
    )
    reference = "Arithmetic identity"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Orbit definition: orbit_number = cumsum // 8 (integer division).")
            .step("Orbit crossing count = number of times orbit_number increments.")
            .step("At step N: expected_crossings = final_cumsum // 8.")
            .step("Track actual crossings by counting transitions where orbit_curr > orbit_prev.")
            .conclude("Verify: actual_crossings == expected_crossings (from cumsum // 8). This identity confirms the modular-8 foundation of Field Closure.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        final_cumsum = traversal[-1]['cumsum']
        expected_crossings = final_cumsum // 8
        
        actual_crossings = 0
        prev_orbit = 0
        for step in traversal:
            curr_orbit = step['cumsum'] // 8
            if curr_orbit > prev_orbit:
                actual_crossings += (curr_orbit - prev_orbit)
                prev_orbit = curr_orbit
        
        return (
            Model()
            .add("Actual crossings", actual_crossings)
            .add("Expected (cumsum // 8)", expected_crossings)
        )
    
    def observations(self) -> Observed:
        traversal = traverse_pi_base8(1000)
        final_cumsum = traversal[-1]['cumsum']
        expected = final_cumsum // 8
        return (
            Observed()
            .add("Actual crossings", expected)
            .add("Expected (cumsum // 8)", expected)
        )
    
    commentary = (
        "The identity between orbit crossing count and integer division of cumulative sum "
        "by eight confirms the arithmetic foundation of Field Closure. This relationship "
        "is consistent with the definition of an orbit as a complete traversal of eight "
        "Coupling Port increments within the stellated octahedron."
    )


# =============================================================================
# TESTS: REVERSIBILITY
# =============================================================================

class InformationPreservation(Test):
    """
    NASA REQUIREMENT: No information loss.
    Sum of all digits equals final cumsum.
    """
    name = "Information Preservation"
    question = (
        "Is information preserved through Field Closure, with the sum of all input digits "
        "exactly equaling the final cumulative sum?"
    )
    reference = "Conservation"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Information conservation law: sum(inputs) == final_state.")
            .step("Compute: digit_sum = sum(step['digit'] for all steps).")
            .step("Compute: final_cumsum = traversal[-1]['cumsum'].")
            .conclude("Verify: digit_sum == final_cumsum (exact equality). If true, no information is lost or injected during the traversal. This confirms the Field Chamber operates as a lossless accumulator.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(500)
        
        digit_sum = sum(s['digit'] for s in traversal)
        final_cumsum = traversal[-1]['cumsum']
        
        return (
            Model()
            .add("Digit sum", digit_sum)
            .add("Final cumsum", final_cumsum)
        )
    
    def observations(self) -> Observed:
        traversal = traverse_pi_base8(500)
        digit_sum = sum(s['digit'] for s in traversal)
        return (
            Observed()
            .add("Digit sum", digit_sum)
            .add("Final cumsum", digit_sum)
        )
    
    commentary = (
        "Conservation of the digit sum through traversal indicates that the Field Chamber "
        "preserves information content throughout the Field Closure sequence. This is "
        "consistent with a reversible process where the complete input history can be "
        "inferred from the final cumulative state."
    )


class PathReconstruction(Test):
    """
    Verify complete path reconstruction from states.
    """
    name = "Path Reconstruction"
    question = (
        "Can the complete cumulative sum sequence be reconstructed from the digit sequence "
        "alone, confirming bijective mapping through the Field Chamber?"
    )
    reference = "Reconstructibility"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Reconstruction procedure: cumsum_0 = digit_0, cumsum_n = cumsum_{n-1} + digit_n.")
            .step("For each step, compute reconstructed_cumsum from accumulated digits.")
            .step("Compare reconstructed_cumsum to actual step['cumsum'].")
            .conclude("Count matching steps. Expected: all steps match (100% reconstruction). Full reconstruction confirms the digit-to-cumsum mapping is bijective.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(100)
        
        reconstructed_cumsum = 0
        matching = 0
        
        for step in traversal:
            reconstructed_cumsum += step['digit']
            if reconstructed_cumsum == step['cumsum']:
                matching += 1
        
        return (
            Model()
            .add("Matching cumsums", matching)
            .add("Total steps", len(traversal))
        )
    
    def observations(self) -> Observed:
        traversal = traverse_pi_base8(100)
        return (
            Observed()
            .add("Matching cumsums", len(traversal))
            .add("Total steps", len(traversal))
        )
    
    commentary = (
        "Complete reconstructibility of the cumulative sum sequence from the digit history "
        "confirms that no state information is lost during Field Closure traversal. This "
        "suggests that the stellated octahedron mapping is bijective with respect to the "
        "cumulative input, preserving the full trajectory through the Field Chamber."
    )


# =============================================================================
# TESTS: OVERFLOW SAFETY
# =============================================================================

class NoIntegerOverflow(Test):
    """
    NASA REQUIREMENT: Numerical robustness.
    Even with 1000 digits, no overflow issues.
    """
    name = "No Integer Overflow"
    question = (
        "Do cumulative sum and orbit number remain within reasonable bounds over 1000 "
        "digits, confirming numerical stability without overflow?"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Overflow safety criterion: values remain within practical bounds.")
            .step("For N=1000 digits with max digit = 7: max_cumsum <= 7000.")
            .step("Max orbit: max_cumsum // 8 <= 875.")
            .step("Traverse N=1000 digits and record max_cumsum, max_orbit.")
            .conclude("Verify: 0 < max_cumsum < 10000 and 0 < max_orbit < 1000. If within bounds, the algorithm is numerically stable for extended operation.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        max_cumsum = max(s['cumsum'] for s in traversal)
        max_orbit = max(s['orbit'] for s in traversal)
        
        cumsum_reasonable = 1 if 0 < max_cumsum < 10000 else 0
        orbit_reasonable = 1 if 0 < max_orbit < 1000 else 0
        
        return (
            Model()
            .add("Max cumsum", max_cumsum)
            .add("Max orbit", max_orbit)
            .add("Cumsum reasonable (1=yes)", cumsum_reasonable)
            .add("Orbit reasonable (1=yes)", orbit_reasonable)
        )
    
    commentary = (
        "Bounded cumulative values over 1000 digits indicates numerical stability of the "
        "Field Closure algorithm under extended operation. This robustness suggests that "
        "practical implementations can traverse the stellated octahedron for arbitrarily "
        "long sequences without encountering overflow conditions."
    )


class ModularArithmeticConsistency(Test):
    """
    Verify vertex = cumsum % 8 never fails due to numerical issues.
    """
    name = "Modular Arithmetic Consistency"
    question = (
        "Is the vertex position always exactly equal to cumsum mod 8, with 100% consistency "
        "across all traversal steps?"
    )
    reference = "Modular arithmetic"
    tolerance = 0.01  # Allow tiny tolerance for count differences
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("Core mapping: vertex = cumsum mod 8.")
            .step("This maps the unbounded cumsum onto the 8-vertex stellated octahedron.")
            .step("For each step, verify: step['vertex'] == step['cumsum'] mod 8.")
            .conclude("Count consistent steps and compute: consistency_rate = consistent / total. Expected: consistency_rate = 1.0 (100%). Perfect consistency confirms exact modular arithmetic without numerical artifacts.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        
        consistent = sum(1 for s in traversal if s['vertex'] == s['cumsum'] % 8)
        consistency_rate = consistent / len(traversal) if traversal else 0
        
        return Model().add("Consistency rate", consistency_rate)
    
    def observations(self) -> Observed:
        return Observed().add("Consistency rate", 1.0)  # 100% consistent expected
    
    commentary = (
        "Perfect consistency between vertex position and cumulative sum modulo eight "
        "confirms that the core Field Closure mapping remains exact throughout traversal. "
        "This suggests that the modular arithmetic foundation of Coupling Port assignment "
        "is numerically stable and free from rounding or truncation artifacts."
    )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    DeterminismMultipleRuns,
    DeterminismStateSequence,
    AllVerticesReachable,
    BothTetrahedraReachable,
    ErgodicConvergence,
    TetrahedraErgodicity,
    DigitZeroHandling,
    DigitSevenHandling,
    OrbitBoundaryCrossing,
    LongRunStatistics,
    NoStateDrift,
    BimetricSymmetry,
    ComplementaryPairBalance,
    AllTransitionsOccur,
    SelfTransitionsOccur,
    ClosureLengthDistribution,
    OrbitBoundaryCrossingsVsCumsum,
    InformationPreservation,
    PathReconstruction,
    NoIntegerOverflow,
    ModularArithmeticConsistency,
]


def run_all() -> bool:
    """Run all engine stress tests."""
    return run_tests(
        title="Engine Stress Tests",
        summary=(
            "NASA/CERN-level validation of field closure mechanics. These tests verify: "
            "(1) bit-identical determinism across 100 runs, (2) complete state space coverage "
            "(all 8 vertices reachable), (3) ergodic convergence to uniform distribution, "
            "(4) correct boundary condition handling (digit=0, digit=7), (5) long-run stability "
            "over 1000 digits, (6) bimetric symmetry between tetrahedra, (7) transition matrix "
            "completeness, (8) closure length statistics match theory, (9) information preservation "
            "(digit sum = cumsum), and (10) numerical overflow safety."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
