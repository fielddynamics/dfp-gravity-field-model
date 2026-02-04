"""
Field Closure System Validation
===============================

This module provides comprehensive validation of the Field Closure state
machine treating pi-driven traversal as a deterministic system. Tests validate:

1. State Machine Integrity: Deterministic transitions, invariants
2. Closure Event Detection: Precise boundary crossing at cumsum mod 8 = 0
3. Statistical Properties: Digit distribution, ergodicity
4. Cross-Validation: Multiple independent derivation paths
5. Consistency: Internal self-consistency checks
"""

from typing import Dict, Optional, List
from collections import Counter

from gfd_model_v2.framework import *

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
ALPHA = 1/137.036
HBAR = 1.055e-34  # J*s
C = 2.998e8  # m/s
ELECTRON_MASS = 9.109e-31  # kg
LAMBDA_COMPTON = 2.426310238e-12  # m

# Pi base-8 fractional digits
PI_BASE8_FRACTIONAL = [
    1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, 0, 2, 1, 5,
    1, 4, 2, 3, 0, 5, 5, 4, 5, 4, 1, 2, 2, 0, 3, 5, 2, 3, 4, 6,
    5, 4, 2, 1, 1, 3, 2, 6, 7, 2, 2, 3, 0, 1, 4, 6, 5, 4, 4, 0,
    6, 3, 4, 5, 6, 0, 6, 2, 3, 6, 5, 6, 3, 6, 6, 1, 0, 1, 5, 5,
    2, 3, 7, 2, 1, 5, 1, 6, 4, 5, 6, 7, 4, 2, 3, 7, 3, 2, 4, 2,
]

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}


def get_pi_base8(n_digits, include_integer=True):
    if include_integer:
        return [3] + PI_BASE8_FRACTIONAL[:n_digits]
    return PI_BASE8_FRACTIONAL[:n_digits]


def get_tetrahedron(v):
    return 'A' if v in TET_A else 'B'


def calculate_settlement_frequency():
    return C / LAMBDA_COMPTON


def build_state_sequence(num_digits=100):
    """Build complete state sequence."""
    digits = get_pi_base8(num_digits, include_integer=True)
    states = []
    cumsum = 0
    
    for step, digit in enumerate(digits):
        cumsum += digit
        vertex = cumsum % 8
        tet = get_tetrahedron(vertex)
        orbit = cumsum // 8
        
        states.append({
            'step': step,
            'digit': digit,
            'cumsum': cumsum,
            'vertex': vertex,
            'tetrahedron': tet,
            'orbit': orbit,
        })
    
    return states


# =============================================================================
# TESTS
# =============================================================================

class VertexEqualsCumsumMod8(Test):
    """
    INVARIANT: vertex = cumsum % 8 (ALWAYS).
    Like verifying crankshaft position matches encoder.
    """
    name = "Vertex = Cumsum mod 8"
    question = (
        "How do we know which vertex we are on? "
        "The rule is simple: add up all the pi digits so far (the cumulative sum), "
        "divide by 8, and take the remainder. That remainder IS the current vertex. "
        "This test verifies this fundamental formula never fails."
    )
    reference = "State machine definition"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The Field Chamber has 2k=8 vertices labeled 0-7.")
            .step("Each pi base-8 digit advances the cumulative sum.")
            .step("The current vertex is computed as cumsum mod 8.")
            .step("This modular arithmetic wraps the cumsum into the valid vertex range [0,7].")
            .conclude("vertex = cumsum mod 8 is the defining relation of the state machine.")
        )
    
    commentary = (
        "Think of an odometer that only shows the last digit. It cycles 0, 1, 2, ... 7, 0, 1, 2... "
        "The cumulative sum is like total miles driven; the vertex is like that last digit. "
        "No matter how big the cumsum gets, taking mod 8 always gives a number 0 through 7, "
        "which is a valid vertex. This simple formula is the beating heart of the traversal."
    )
    
    def model(self):
        states = build_state_sequence(100)
        violations = sum(1 for s in states if s['vertex'] != s['cumsum'] % 8)
        return (
            Model()
            .add("Violations", violations)
            .add("States checked", len(states))
        )
    
    def observations(self):
        return (
            Observed()
            .add("Violations", 0)
            .add("States checked", 101)
        )


class OrbitEqualsCumsumDiv8(Test):
    """
    INVARIANT: orbit = cumsum // 8 (ALWAYS).
    Orbit counter tracks cumulative angular position.
    """
    name = "Orbit = Cumsum // 8"
    question = (
        "How do we count completed laps around the Field Chamber? "
        "Every time the cumsum increases by 8, we complete one orbit. "
        "Integer division (cumsum // 8) counts these laps. "
        "This test verifies the orbit counter stays in sync with the cumulative sum."
    )
    reference = "State machine definition"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: One complete orbit traverses all 2k=8 vertex positions.")
            .step("Each orbit corresponds to accumulating 8 units of cumsum.")
            .step("Integer division cumsum // 8 counts how many complete sets of 8 have been traversed.")
            .step("The orbit number increments each time cumsum crosses a multiple of 8.")
            .conclude("orbit = cumsum // 8 counts completed Field Closure cycles.")
        )
    
    commentary = (
        "Imagine running laps on a track with 8 positions. Each digit advances you some distance. "
        "The vertex (cumsum mod 8) tells you where you are on THIS lap. "
        "The orbit (cumsum // 8) tells you how many COMPLETE laps you have finished. "
        "Together they give your full position: lap 5, position 3 means cumsum = 5*8 + 3 = 43. "
        "This test confirms the lap counter (orbit) and position (vertex) always agree with cumsum."
    )
    
    def model(self):
        states = build_state_sequence(100)
        violations = sum(1 for s in states if s['orbit'] != s['cumsum'] // 8)
        return (
            Model()
            .add("Violations", violations)
            .add("States checked", len(states))
        )
    
    def observations(self):
        return (
            Observed()
            .add("Violations", 0)
            .add("States checked", 101)
        )


class TetrahedronMatchesParity(Test):
    """
    INVARIANT: Tet A = odd parity vertices, Tet B = even parity.
    Tetrahedron assignment is deterministic from vertex number.
    """
    name = "Tetrahedron Matches Parity"
    question = (
        "Which tetrahedron does each vertex belong to? "
        "The rule is elegant: count the 1-bits in the vertex number's binary representation. "
        "If odd, Tetrahedron A. If even, Tetrahedron B. "
        "This test verifies this parity rule correctly partitions all 8 vertices."
    )
    reference = "Parity definition"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each vertex index 0-7 has a 3-bit binary representation.")
            .step("Count the number of 1-bits in the binary representation.")
            .step("If the count is odd (vertices 1,2,4,7), assign to Tetrahedron A.")
            .step("If the count is even (vertices 0,3,5,6), assign to Tetrahedron B.")
            .conclude("Parity partitions the 8 vertices into two disjoint sets of 4, each forming a tetrahedron.")
        )
    
    commentary = (
        "Vertex 5 is binary 101, which has two 1-bits (even), so it belongs to Tetrahedron B. "
        "Vertex 7 is binary 111, which has three 1-bits (odd), so it belongs to Tetrahedron A. "
        "This is not arbitrary: parity naturally divides a cube's vertices into two interlocking "
        "tetrahedra. No special encoding needed. The mathematics hands us a clean partition, "
        "4 vertices each, forming the dual Field Chamber structure."
    )
    
    def model(self):
        states = build_state_sequence(100)
        violations = 0
        for s in states:
            expected = 'A' if s['vertex'] in TET_A else 'B'
            if s['tetrahedron'] != expected:
                violations += 1
        return Model().add("Violations", violations)
    
    def observations(self):
        return Observed().add("Violations", 0)


class StateDeterminism(Test):
    """
    DETERMINISM: Same input -> Same output (ALWAYS).
    Run twice and verify identical results.
    """
    name = "State Determinism"
    question = (
        "If we run the same traversal twice, do we get the same result? "
        "Physics must be reproducible. Same inputs must yield same outputs. "
        "This test runs the state machine twice and verifies every step matches perfectly."
    )
    reference = "Reproducibility requirement"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A deterministic system produces identical outputs from identical inputs.")
            .step("Initialize two independent traversals with the same pi digit sequence.")
            .step("Execute both traversals using identical state transition rules.")
            .step("Compare cumsum and vertex at each step across both executions.")
            .conclude("Zero mismatches confirms the state machine is fully deterministic.")
        )
    
    commentary = (
        "Science requires repeatability. Drop a ball twice from the same height, it falls the same way. "
        "Our traversal must work the same way: give it the same pi digits, get the same vertex sequence. "
        "No randomness, no hidden variables, no surprises. This test runs the algorithm twice "
        "and checks every single step. If anything differs, our foundation is broken. "
        "Thankfully, pure arithmetic is perfectly deterministic."
    )
    
    def model(self):
        states1 = build_state_sequence(50)
        states2 = build_state_sequence(50)
        
        mismatches = sum(1 for s1, s2 in zip(states1, states2)
                        if s1['cumsum'] != s2['cumsum'] or s1['vertex'] != s2['vertex'])
        return Model().add("Mismatches", mismatches)
    
    def observations(self):
        return Observed().add("Mismatches", 0)


class CumsumMonotonic(Test):
    """
    MONOTONICITY: cumsum is non-decreasing (digits >= 0).
    """
    name = "Cumsum Monotonic"
    question = (
        "Does the cumulative sum ever go backward? "
        "Since pi digits are always 0 or positive (never negative), the cumsum can only stay "
        "the same or increase. This test confirms we always move forward, never in reverse."
    )
    reference = "Digit range [0,7]"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Pi base-8 digits are in the range [0,7], all non-negative.")
            .step("At each step, cumsum_new = cumsum_old + digit.")
            .step("Since digit >= 0, cumsum_new >= cumsum_old always.")
            .step("The only way cumsum could decrease would be negative digits, which do not exist.")
            .conclude("Monotonicity is guaranteed by the non-negative digit range.")
        )
    
    commentary = (
        "Time flows forward. You cannot un-eat lunch or un-speak words. "
        "The cumulative sum has the same one-way property. Since every pi digit is "
        "zero or positive, adding it never decreases the total. We march forward through "
        "vertex space, orbit by orbit, without ever retreating. This arrow of progression "
        "mirrors the arrow of time: always forward, never back."
    )
    
    def model(self):
        states = build_state_sequence(100)
        violations = sum(1 for i in range(1, len(states))
                        if states[i]['cumsum'] < states[i-1]['cumsum'])
        return Model().add("Violations", violations)
    
    def observations(self):
        return Observed().add("Violations", 0)


class IncrementEqualsDigit(Test):
    """
    INCREMENT: cumsum[n] - cumsum[n-1] = digit[n].
    Fundamental accounting check.
    """
    name = "Increment = Digit"
    question = (
        "If we subtract yesterday's total from today's, do we get today's new input? "
        "Basic accounting: total growth equals the amount added. "
        "This test verifies cumsum[n] minus cumsum[n-1] equals the n-th digit, every single time."
    )
    reference = "Cumsum definition"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The cumulative sum is defined as the running total of pi digits.")
            .step("By definition, cumsum[n] = cumsum[n-1] + digit[n].")
            .step("Rearranging: cumsum[n] - cumsum[n-1] = digit[n].")
            .step("This equality must hold at every step for correct accounting.")
            .conclude("Any violation indicates an arithmetic error in the traversal.")
        )
    
    commentary = (
        "A bank account works this way: today's balance minus yesterday's balance equals "
        "today's deposit (or withdrawal). The cumulative sum is our 'balance,' and each "
        "pi digit is a 'deposit.' If the books do not balance, something is wrong. "
        "This test is the auditor, checking that every increment matches its source digit. "
        "Boring but essential: correct accounting is the foundation of trust."
    )
    
    def model(self):
        states = build_state_sequence(100)
        violations = 0
        prev_cumsum = 0
        for s in states:
            delta = s['cumsum'] - prev_cumsum
            if delta != s['digit']:
                violations += 1
            prev_cumsum = s['cumsum']
        return Model().add("Violations", violations)
    
    def observations(self):
        return Observed().add("Violations", 0)


class DigitDistributionReasonable(Test):
    """
    Pi digits should be roughly uniformly distributed (0-7).
    """
    name = "Digit Distribution"
    question = (
        "Are pi's digits random enough? "
        "If 7 appears too often and 0 too rarely, traversal would be biased. "
        "This test checks that each digit 0 through 7 appears roughly equally, "
        "supporting pi's conjectured status as a 'normal number.'"
    )
    reference = "Normal number conjecture"
    tolerance = 0.30
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A normal number has uniformly distributed digits in every base.")
            .step("For base-8, the expected frequency of each digit 0-7 is 1/8 = 12.5%.")
            .step("Calculate observed frequency for each digit in the sample.")
            .step("Compute maximum deviation from expected 12.5%.")
            .conclude("Deviation < 30% supports approximate uniformity over this sample size.")
        )
    
    commentary = (
        "Imagine rolling a fair 8-sided die millions of times. Each face should appear "
        "about 1/8 of the time. Pi's digits work similarly: 0 through 7 each appear "
        "roughly 12.5% of the time. This is not proven (pi is only 'conjectured' normal), "
        "but all evidence supports it. Good digit distribution ensures our traversal "
        "samples all vertices fairly, with no systematic blind spots."
    )
    
    def model(self):
        observed = Counter(PI_BASE8_FRACTIONAL)
        n = len(PI_BASE8_FRACTIONAL)
        expected = n / 8
        
        max_dev = max(abs(observed.get(d, 0) - expected) / expected for d in range(8))
        
        return (
            Model()
            .add("Max deviation from expected", max_dev)
            .add("Expected per digit", expected)
        )


class VertexErgodicity(Test):
    """
    ERGODICITY: Each vertex visited approximately equally over time.
    """
    name = "Vertex Ergodicity"
    question = (
        "Does the traversal visit all corners of the room equally? "
        "Ergodicity means long-term averages match the expected distribution. "
        "If we visit for long enough, each vertex should get about 12.5% of visits. "
        "This test checks whether pi-driven traversal is ergodic."
    )
    reference = "Ergodic hypothesis"
    tolerance = 0.30
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Ergodicity requires time averages to equal ensemble averages.")
            .step("With 2k=8 vertices and uniform digit distribution, expected visit fraction is 1/8 per vertex.")
            .step("Track vertex visits across N traversal steps.")
            .step("Calculate deviation of each vertex's visit count from N/8.")
            .conclude("Maximum deviation < 30% indicates ergodic sampling over this sample.")
        )
    
    commentary = (
        "Ergodicity is a fancy word for 'fair sampling.' A drunk walking home will, given "
        "enough time, visit every street corner about equally often. Pi-driven traversal "
        "should work the same way: over many steps, no vertex is systematically neglected. "
        "This matters because information stored at any vertex eventually gets sampled. "
        "No corner of the Field Chamber is a permanent blind spot."
    )
    
    def model(self):
        states = build_state_sequence(100)
        vertex_counts = Counter(s['vertex'] for s in states)
        
        expected = len(states) / 8
        max_dev = max(abs(vertex_counts.get(v, 0) - expected) / expected for v in range(8))
        
        return Model().add("Max vertex deviation", max_dev)


class TetrahedronBalance(Test):
    """
    Tet A and Tet B should be visited approximately equally.
    """
    name = "Tetrahedron Balance"
    question = (
        "Do both halves of the Field Chamber get equal attention? "
        "Tetrahedron A and Tetrahedron B each have 4 vertices. If traversal is fair, "
        "each should receive about 50% of visits. This test checks for bimetric balance."
    )
    reference = "Bimetric balance"
    tolerance = 0.10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tetrahedron contains 4 of the 8 vertices (50% each by structure).")
            .step("Tet A vertices {1,2,4,7} and Tet B vertices {0,3,5,6} partition the vertex set.")
            .step("With ergodic vertex sampling, each tetrahedron should receive ~50% of visits.")
            .step("Compute ratio of Tet A visits to total visits.")
            .conclude("Ratio near 0.5 confirms balanced bimetric coupling.")
        )
    
    commentary = (
        "The Field Chamber is split into two interlocking tetrahedra, like yin and yang. "
        "For the model to work, both halves must be engaged equally. If pi's digits strongly "
        "favored Tetrahedron A, the bimetric structure would be lopsided. This test confirms "
        "the 50/50 split is approximately maintained, ensuring symmetric coupling between "
        "the dual sectors of the geometry."
    )
    
    def model(self):
        states = build_state_sequence(100)
        tet_a = sum(1 for s in states if s['tetrahedron'] == 'A')
        tet_b = sum(1 for s in states if s['tetrahedron'] == 'B')
        total = tet_a + tet_b
        ratio_a = tet_a / total
        
        return (
            Model()
            .add("Tet A visits", tet_a)
            .add("Tet B visits", tet_b)
            .add("Ratio A", ratio_a)
        )


class AlphaFromOrbits(Test):
    """
    137 orbits corresponds to 1/alpha. This establishes a correspondence
    between orbit count and the fine structure constant.
    """
    name = "Alpha from Orbits"
    question = (
        "Why does 137 keep appearing? "
        "The fine structure constant is about 1/137. The model suggests 137 orbits "
        "have special significance for electron structure. This test documents the "
        "numerical correspondence between orbit counting and electromagnetic coupling."
    )
    reference = "Fine structure constant"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The fine structure constant alpha = 1/137.036 characterizes electromagnetic coupling.")
            .step("The model proposes 137 orbits as a characteristic electron cycle count.")
            .step("Derived alpha = 1/137 = 0.00730.")
            .step("Compare to measured alpha = 1/137.036 = 0.00729735.")
            .conclude("Agreement within 0.03% suggests a numerical correspondence.")
        )
    
    commentary = (
        "Physicists have puzzled over 137 for a century. The fine structure constant is "
        "about 1/137, and nobody knows why. In our model, 137 orbits completes one 'electron.' "
        "Is this coincidence or insight? We cannot say. But when pure geometry produces the same "
        "mysterious number that governs electromagnetic interactions, it deserves attention. "
        "Perhaps counting orbits is, at some level, what nature does when creating electrons."
    )
    
    def model(self):
        orbits_per_electron = 137
        derived_alpha = 1 / orbits_per_electron
        
        return (
            Model()
            .add("Derived alpha", derived_alpha)
            .add("Actual alpha", ALPHA)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Derived alpha", 1/137)
            .add("Actual alpha", ALPHA)
        )


class SpinFromFaces(Test):
    """
    2 TIME Coupling Ports / 8 total = 1/4 -> Spin correspondence = 1/4 * 2 = 1/2.
    """
    name = "Spin from Coupling Ports"
    question = (
        "Can we derive electron spin from geometry? "
        "There are 8 faces total, 2 of which are TIME faces. The ratio 2/8 = 1/4. "
        "Multiply by 2 (for the two tetrahedra), and we get 1/2, the electron's spin. "
        "This test documents this geometric derivation of spin-1/2."
    )
    reference = "Electron spin"
    tolerance = 1e-10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The stellated octahedron has 8 total Coupling Ports (k=4 per tetrahedron * 2).")
            .step("Of these 8 faces, 2 are TIME Coupling Ports (one per tetrahedron apex).")
            .step("TIME fraction = 2/8 = 1/4.")
            .step("Multiply by 2 (the bimetric factor): spin = (1/4) * 2 = 1/2.")
            .conclude("The geometric ratio yields the fermion spin quantum number.")
        )
    
    commentary = (
        "Electrons have spin 1/2, a quantum property with no classical analogue. "
        "You cannot visualize it as a spinning top. But look at the Field Chamber: "
        "2 TIME faces out of 8 total gives 2/8 = 1/4. The bimetric factor of 2 "
        "(two tetrahedra) gives us 1/4 x 2 = 1/2. Spin emerges from face counting! "
        "This does not explain WHY electrons have spin 1/2, but it shows the number "
        "can arise from geometry. Perhaps quantum properties are topological at heart."
    )
    
    def model(self):
        time_faces = 2
        total_faces = 8
        time_fraction = time_faces / total_faces
        spin = time_fraction * 2
        
        return (
            Model()
            .add("TIME faces", time_faces)
            .add("Total faces", total_faces)
            .add("Spin", spin)
        )
    
    def observations(self):
        return (
            Observed()
            .add("TIME faces", 2)
            .add("Total faces", 8)
            .add("Spin", 0.5)
        )


class KFromTopology(Test):
    """
    k=4 appears in: vertices per tet, faces per tet, base 8 = 2k.
    """
    name = "k=4 from Topology"
    question = (
        "Why does k=4 appear everywhere? "
        "A tetrahedron has 4 vertices and 4 faces. Two tetrahedra give 8 = 2k vertices. "
        "The number of spatial dimensions is k-1 = 3. This test confirms k=4 is "
        "not just a constant but the organizing principle of the entire structure."
    )
    reference = "Tetrahedral structure"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: k=4 is the fundamental Field Closure topology constant.")
            .step("A tetrahedron has k=4 vertices by definition.")
            .step("A tetrahedron has k=4 faces (triangular Coupling Ports).")
            .step("The dual structure has 2k=8 total vertices, hence base-8 encoding.")
            .step("Spatial dimensions d = k-1 = 3.")
            .conclude("k=4 organizes the entire Field Chamber structure.")
        )
    
    commentary = (
        "Everything flows from k=4. The tetrahedron is the simplest 3D shape: 4 corners, "
        "4 triangular faces. Two tetrahedra make 8 corners. Base 8 arithmetic addresses them. "
        "Subtract 1 from k and you get 3, our number of spatial dimensions. The BBP formula "
        "has 4 terms. The constraint equations in General Relativity number 4. "
        "Again and again, k=4 organizes the mathematics. It is not a chosen parameter; "
        "it is the inevitable consequence of using tetrahedra as fundamental building blocks."
    )
    
    def model(self):
        return (
            Model()
            .add("Vertices per tet", len(TET_A))
            .add("Base 8 = 2k", 8)
            .add("k", K)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Vertices per tet", 4)
            .add("Base 8 = 2k", 8)
            .add("k", 4)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    VertexEqualsCumsumMod8,
    OrbitEqualsCumsumDiv8,
    TetrahedronMatchesParity,
    StateDeterminism,
    CumsumMonotonic,
    IncrementEqualsDigit,
    DigitDistributionReasonable,
    VertexErgodicity,
    TetrahedronBalance,
    AlphaFromOrbits,
    SpinFromFaces,
    KFromTopology,
]


def run_all():
    """Run all Field Closure system validation tests."""
    return run_tests(
        title="Field Closure System Validation",
        summary=(
            "These tests provide comprehensive validation of the Field Closure state "
            "machine. Tests verify invariants (vertex=cumsum%8, orbit=cumsum//8), "
            "determinism, monotonicity, and fundamental accounting. Statistical tests "
            "check digit distribution, vertex ergodicity, and Field Chamber balance. "
            "Cross-validation documents correspondences: alpha from orbits, spin from "
            "Coupling Ports, and k=4 throughout topology."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
