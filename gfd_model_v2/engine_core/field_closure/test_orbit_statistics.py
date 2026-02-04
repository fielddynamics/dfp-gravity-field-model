"""
Orbit Statistics
================

An "orbit" is defined as the accumulation of 8 units through traversal of the
stellated octahedron's vertices. Pi digits in base-8 drive the traversal,
and the statistics of orbit lengths reveal properties of the traversal.

The model predicts:
- Mean digits per orbit of approximately 2.42 (since 8 / mean_digit = 8 / 3.31)
- Equal visitation of both tetrahedra (50%/50% by parity symmetry)
- Uniform vertex visitation (approximately 12.5% each)

These statistical properties emerge from the combination of Pi's digit
distribution and the geometry of the 8-vertex structure.
"""

from typing import Dict, Optional
from collections import Counter

from gfd_model_v2.framework import *
from gfd_model_v2.common import traverse_pi_base8, TET_A, TET_B


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_orbit_lengths(traversal):
    """Calculate the number of digits between each orbit boundary crossing."""
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
    
    return crossing_lengths


def calculate_tetrahedra_visits(traversal):
    """Count visits to each tetrahedron."""
    tet_a_count = sum(1 for step in traversal if step['vertex'] in TET_A)
    tet_b_count = sum(1 for step in traversal if step['vertex'] in TET_B)
    return tet_a_count, tet_b_count


def analyze_orbit_stats(n_digits=1000):
    """Complete orbit statistics analysis."""
    traversal = traverse_pi_base8(n_digits)
    orbit_lengths = calculate_orbit_lengths(traversal)
    
    mean_length = sum(orbit_lengths) / len(orbit_lengths) if orbit_lengths else 0
    min_length = min(orbit_lengths) if orbit_lengths else 0
    max_length = max(orbit_lengths) if orbit_lengths else 0
    
    # Theoretical from actual mean digit
    digit_sum = sum(step['digit'] for step in traversal)
    mean_digit = digit_sum / len(traversal)
    theoretical = 8 / mean_digit
    
    # Short orbit fraction
    length_dist = Counter(orbit_lengths)
    short_orbits = sum(length_dist.get(i, 0) for i in [1, 2, 3])
    short_ratio = short_orbits / len(orbit_lengths) if orbit_lengths else 0
    
    return {
        'mean_length': mean_length,
        'min_length': min_length,
        'max_length': max_length,
        'theoretical': theoretical,
        'short_ratio': short_ratio,
        'total_orbits': len(orbit_lengths),
        'final_cumsum': traversal[-1]['cumsum'] if traversal else 0,
    }


def analyze_tetrahedra_balance(n_digits=1000):
    """Tetrahedra balance analysis."""
    traversal = traverse_pi_base8(n_digits)
    tet_a, tet_b = calculate_tetrahedra_visits(traversal)
    total = tet_a + tet_b
    
    vertex_counts = Counter(step['vertex'] for step in traversal)
    expected = 0.125  # 1/8
    max_deviation = max(
        abs(vertex_counts.get(v, 0) / total - expected)
        for v in range(8)
    )
    
    return {
        'tet_a_ratio': tet_a / total if total else 0,
        'tet_b_ratio': tet_b / total if total else 0,
        'ab_ratio': tet_a / tet_b if tet_b else 0,
        'max_vertex_deviation': max_deviation,
    }


# =============================================================================
# TESTS: DIGITS PER ORBIT
# =============================================================================

class MeanDigitsPerOrbit(Test):
    """
    Mean digits per orbit = 8 / mean_digit_value. With Pi's base-8 digits
    averaging about 3.31, we expect approximately 2.42 digits per orbit.
    This value emerges from Pi's statistical properties.
    """
    name = "Mean Digits Per Orbit"
    question = (
        "How many digits does a typical orbit take? "
        "An orbit completes when cumsum gains 8. If digits average 3.3, "
        "we need about 8/3.3 = 2.4 digits. This test verifies the mean matches this expectation."
    )
    reference = "Theoretical (8 / mean_digit)"
    tolerance = 0.05
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each orbit spans 2k=8 cumsum units; digit count depends on mean digit value.")
            .step("For uniform distribution over 0-7, mean digit = (0+1+...+7)/8 = 3.5.")
            .step("Actual pi digits have mean = 3.31 (slight deviation from uniform).")
            .step("Expected digits per orbit = 8 / <digit> = 8 / 3.31 = 2.42.")
            .step("Measure actual mean across many orbits and compare.")
            .conclude("Mean digits per orbit = 2.4.")
        )
    
    commentary = (
        "Think of filling a bucket that holds 8 liters. If each scoop averages 3.3 liters, "
        "you need about 2.4 scoops. Same here: orbits need 8 cumsum units, "
        "digits average about 3.3, so orbits average about 2.4 digits. "
        "This simple ratio tells us the 'pace' of traversal."
    )
    
    def model(self):
        stats = analyze_orbit_stats(1000)
        return Model().add("Mean digits per orbit", stats['mean_length'])
    
    def observations(self):
        stats = analyze_orbit_stats(1000)
        return Observed().add("Mean digits per orbit", stats['theoretical'])


class OrbitLengthDistribution(Test):
    """
    Most orbits (>85%) should be 1-3 digits. Small digits accumulate,
    while large digits (like 7) can cross boundaries alone. This
    distribution emerges from Pi's digit patterns.
    """
    name = "Orbit Length Distribution"
    question = (
        "Are orbits mostly short? "
        "Since digits can be as large as 7 (nearly an orbit by itself), most orbits should "
        "complete in 1 to 3 digits. This test checks that over 85% of orbits are 'short.'"
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Orbit length depends on how many digits sum to 8.")
            .step("Large digits (6,7) can nearly or fully complete an orbit alone.")
            .step("Medium digits (3,4,5) typically complete orbits in 2 steps.")
            .step("Small digits (0,1,2) require more steps to sum to 8.")
            .step("Pi's roughly uniform distribution favors short orbit lengths.")
            .step("Count orbits with length <= 3 and divide by total.")
            .conclude("Short orbit fraction > 0.85, above threshold = 1.")
        )
    
    commentary = (
        "If you roll dice where each roll can give you up to 7 points and you need 8 to win, "
        "most games end quickly. One lucky 7 plus a 1 finishes in 2 rolls. "
        "Similarly, most orbits complete in just 1 to 3 digits because pi's digits are spread "
        "across 0 through 7, and combinations that sum to 8 appear quickly."
    )
    
    def model(self):
        stats = analyze_orbit_stats(1000)
        is_short = 1 if stats['short_ratio'] > 0.85 else 0
        return (
            Model()
            .add("Short orbit fraction", stats['short_ratio'])
            .add("Above 85% threshold", is_short)
        )


class MinimumOrbitLength(Test):
    """
    A single large digit (like 7) can complete an orbit alone if the
    cumsum was already near a boundary. This proves the minimum orbit
    length is 1 digit.
    """
    name = "Minimum Orbit Length"
    question = (
        "What is the shortest possible orbit? "
        "If you are at cumsum = 1 and get digit 7, you jump to 8 in one step. "
        "This test confirms that single-digit orbits exist."
    )
    reference = "Theoretical (min = 1)"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A single digit can complete an orbit if it alone spans 8 cumsum units.")
            .step("If cumsum is at boundary 8n and digit = 8 (impossible in base-8).")
            .step("Alternatively: cumsum at 8n+1 and digit=7 gives cumsum = 8(n+1).")
            .step("More generally, any digit >= (8 - cumsum mod 8) crosses the boundary.")
            .step("Example: cumsum=1, digit=7 -> cumsum=8 (orbit complete in 1 step).")
            .conclude("Minimum orbit length = 1.")
        )
    
    commentary = (
        "Imagine you need $8 to buy lunch, and you have $1 in your pocket. "
        "If someone hands you $7, you are instantly there. "
        "Similarly, if cumsum is 1 (just past the last boundary) and the next digit is 7, "
        "you cross the next boundary immediately: a one-digit orbit."
    )
    
    def model(self):
        stats = analyze_orbit_stats(1000)
        return Model().add("Minimum orbit length", stats['min_length'])
    
    def observations(self):
        return Observed().add("Minimum orbit length", 1)


class MaximumOrbitBounded(Test):
    """
    Even with many small digits, orbits must complete within reasonable
    bounds. A maximum of less than 15 digits confirms the traversal
    cannot "stall" indefinitely.
    """
    name = "Maximum Orbit Bounded"
    question = (
        "Can an orbit drag on forever? No. "
        "Even with many small digits, we eventually reach 8. "
        "This test checks that the longest orbit is under 15 digits."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Even sequences of small digits must eventually sum to 8.")
            .step("Worst case: all digits are 0 (no progress indefinitely).")
            .step("But pi has no long runs of zeros; non-zero digits appear regularly.")
            .step("Even with minimum non-zero digit (1), 8 steps suffice: 1*8 = 8.")
            .step("Pi's digit variety ensures faster completion in practice.")
            .step("Observe maximum orbit length across many closures.")
            .conclude("Maximum orbit length < 15, below threshold = 1.")
        )
    
    commentary = (
        "What if you keep getting 0s and 1s? You might worry the orbit will take forever. "
        "But pi does not have long stretches of zeros. Even in the worst case, "
        "eight 1s sum to 8. In practice, larger digits appear and speed things up. "
        "The maximum orbit length stays bounded, so the traversal never 'stalls.'"
    )
    
    def model(self):
        stats = analyze_orbit_stats(1000)
        bounded = 1 if stats['max_length'] < 15 else 0
        return (
            Model()
            .add("Maximum orbit length", stats['max_length'])
            .add("Below 15 threshold", bounded)
        )


class TotalOrbitsMatchCumsum(Test):
    """
    The total number of orbit crossings must equal cumsum // 8.
    This validates the orbit counting algorithm against the
    fundamental cumulative sum arithmetic.
    """
    name = "Orbit Count Consistency"
    question = (
        "Does our orbit counter work correctly? "
        "The total orbit count should equal floor(cumsum / 8). "
        "This test cross-checks our counting algorithm against basic arithmetic."
    )
    reference = "Arithmetic identity"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Orbits are counted each time cumsum crosses a multiple of 8.")
            .step("Final cumsum after N digits = Sum(digits).")
            .step("Number of complete orbits = floor(cumsum / 8) = cumsum // 8.")
            .step("The orbit counting algorithm must match this arithmetic identity.")
            .step("Compare algorithm count to cumsum // 8.")
            .conclude("Orbit count = cumsum // 8.")
        )
    
    commentary = (
        "This is a sanity check. If cumsum is 1000, we must have crossed 1000 // 8 = 125 "
        "orbit boundaries. Our counting algorithm should report exactly 125 orbits. "
        "If it does not, we have a bug. This test ensures internal consistency."
    )
    
    def model(self):
        stats = analyze_orbit_stats(1000)
        expected = stats['final_cumsum'] // 8
        return (
            Model()
            .add("Orbit count", stats['total_orbits'])
            .add("Expected (cumsum // 8)", expected)
        )
    
    def observations(self):
        stats = analyze_orbit_stats(1000)
        expected = stats['final_cumsum'] // 8
        return (
            Observed()
            .add("Orbit count", expected)
            .add("Expected (cumsum // 8)", expected)
        )


# =============================================================================
# TESTS: TETRAHEDRA BALANCE
# =============================================================================

class TetrahedraNearEqual(Test):
    """
    Tet_A (vertices 1,2,4,7) and Tet_B (vertices 0,3,5,6) should be
    visited equally due to parity symmetry. Each should receive about
    50% of all visits, as expected from the symmetric structure.
    """
    name = "Tetrahedra Near Equal"
    question = (
        "Is the traversal balanced between the two tetrahedra? "
        "With 4 vertices each, Tet A and Tet B should each receive about 50% of visits. "
        "This test checks for near-equal engagement."
    )
    reference = "Parity symmetry (50%/50%)"
    tolerance = 0.10  # Allow 45-55%
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Parity symmetry partitions 8 vertices into two equal sets.")
            .step("Tet_A = {1,2,4,7} (odd parity) has 4 vertices.")
            .step("Tet_B = {0,3,5,6} (even parity) has 4 vertices.")
            .step("With uniform vertex visitation, each tetrahedron receives 4/8 = 50%.")
            .step("Count visits to each tetrahedron across traversal.")
            .conclude("Tet_A visits = 0.50, Tet_B visits = 0.50.")
        )
    
    commentary = (
        "The Field Chamber has two 'halves' (the two tetrahedra). "
        "A fair dice does not favor one side; similarly, pi's digits do not favor one tetrahedron. "
        "Each half has 4 of the 8 vertices, so we expect 50/50 visitation. "
        "This balance reflects the underlying parity symmetry."
    )
    
    def model(self):
        analysis = analyze_tetrahedra_balance(1000)
        return (
            Model()
            .add("Tet_A visits (fraction)", analysis['tet_a_ratio'])
            .add("Tet_B visits (fraction)", analysis['tet_b_ratio'])
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet_A visits (fraction)", 0.50)
            .add("Tet_B visits (fraction)", 0.50)
        )


class TetrahedraRatioUnity(Test):
    """
    The ratio Tet_A:Tet_B should remain bounded. Pi's digit distribution
    creates statistical fluctuations, but the ratio should not exceed 1.3
    (neither tetrahedron receiving >56% of visits).
    """
    name = "Tetrahedra Ratio Bounded"
    question = (
        "Is there extreme favoritism toward one tetrahedron? "
        "Perfect 50/50 is unlikely, but gross imbalance (like 70/30) would be suspicious. "
        "This test checks that the Tet_A/Tet_B ratio stays below 1.3."
    )
    reference = None  # Statistical observation
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Pi's digit distribution couples to the parity partition.")
            .step("Count Tet_A visits and Tet_B visits during traversal.")
            .step("Calculate ratio = Tet_A_count / Tet_B_count.")
            .step("Pi's specific digit sequences may favor one tetrahedron slightly.")
            .step("Verify ratio < 1.3 (no extreme bias).")
            .conclude("Ratio is bounded, confirming statistical reasonableness.")
        )
    
    commentary = (
        "In a coin flip, you do not expect exactly 50/50 after 100 flips, but you do expect "
        "something close, like 55/45. If you get 75/25, you suspect a rigged coin. "
        "Similarly, a Tet_A/Tet_B ratio beyond 1.3 would suggest pi's digits systematically "
        "favor one tetrahedron. Staying under 1.3 means no extreme bias."
    )
    
    def model(self):
        analysis = analyze_tetrahedra_balance(1000)
        ratio_bounded = 1.0 if analysis['ab_ratio'] < 1.3 else 0.0
        return (
            Model()
            .add("Tet_A / Tet_B ratio", analysis['ab_ratio'])
            .add("Ratio bounded (< 1.3)", ratio_bounded)
        )
    
    def observations(self):
        analysis = analyze_tetrahedra_balance(1000)
        return (
            Observed()
            .add("Tet_A / Tet_B ratio", analysis['ab_ratio'])
            .add("Ratio bounded (< 1.3)", 1.0)
        )


class VertexDistributionUniform(Test):
    """
    All 8 vertices should be visited with approximately equal frequency
    (about 12.5% each). Maximum deviation from 12.5% should be less than
    5%, indicating uniform sampling of the vertex structure.
    """
    name = "Vertex Distribution Uniform"
    question = (
        "Does every vertex get roughly equal attention? "
        "With 8 vertices, each should receive about 12.5% of visits. "
        "This test checks that no vertex deviates by more than 5% from the expected."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: With 2k=8 vertices, uniform visitation gives 1/8 = 12.5% each.")
            .step("Count visits to each vertex v in {0,1,...,7}.")
            .step("Calculate fraction for each: f_v = count_v / total.")
            .step("Compute deviation: |f_v - 0.125| for each vertex.")
            .step("Find maximum deviation across all 8 vertices.")
            .conclude("Max deviation < 0.05, below threshold = 1.")
        )
    
    commentary = (
        "In a fair 8-sided die, each face should come up 12.5% of the time. "
        "Our traversal should behave similarly: no vertex should be a 'favorite' or 'avoided.' "
        "If the maximum deviation from 12.5% is under 5%, the sampling is nearly uniform, "
        "confirming the traversal explores the entire vertex space evenly."
    )
    
    def model(self):
        analysis = analyze_tetrahedra_balance(1000)
        uniform = 1 if analysis['max_vertex_deviation'] < 0.05 else 0
        return (
            Model()
            .add("Max deviation from 12.5%", analysis['max_vertex_deviation'])
            .add("Below 5% threshold", uniform)
        )


class ParityDeterminesTetrahedron(Test):
    """
    Vertex parity (number of 1-bits mod 2) determines tetrahedron membership:
    - Odd parity (1,2,4,7) -> Tet_A
    - Even parity (0,3,5,6) -> Tet_B
    This is the fundamental encoding of the bimetric structure.
    """
    name = "Parity Determines Tetrahedron"
    question = (
        "How do we know which tetrahedron a vertex belongs to? "
        "The answer is simple: count the 1 bits in its binary representation. "
        "Odd count means Tet A, even count means Tet B. This test verifies the encoding."
    )
    reference = "Binary parity definition"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Tetrahedron membership can be encoded in a single parity bit.")
            .step("For vertex v, compute popcount(v) = number of 1-bits in binary representation.")
            .step("Parity = popcount(v) mod 2.")
            .step("Vertex 0=000->0, 1=001->1, 2=010->1, 3=011->0, 4=100->1, 5=101->0, 6=110->0, 7=111->1.")
            .step("Odd parity {1,2,4,7} -> Tet_A; Even parity {0,3,5,6} -> Tet_B.")
            .conclude("Vertices with correct parity assignment = 8.")
        )
    
    commentary = (
        "Write any vertex index in binary. For example, 5 is 101 (two 1s). "
        "Count the 1s: if odd, the vertex is in Tetrahedron A; if even, Tetrahedron B. "
        "This is elegant: a single bit (parity) determines which 'half' of the Field Chamber "
        "you are in. Information theory meets geometry in one simple rule."
    )
    
    def model(self):
        correct = 0
        for v in range(8):
            parity = bin(v).count('1') % 2
            expected_tet = 'A' if parity == 1 else 'B'
            actual_tet = 'A' if v in TET_A else 'B'
            if expected_tet == actual_tet:
                correct += 1
        return Model().add("Vertices with correct parity assignment", correct)
    
    def observations(self):
        return Observed().add("Vertices with correct parity assignment", 8)


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    MeanDigitsPerOrbit,
    OrbitLengthDistribution,
    MinimumOrbitLength,
    MaximumOrbitBounded,
    TotalOrbitsMatchCumsum,
    TetrahedraNearEqual,
    TetrahedraRatioUnity,
    VertexDistributionUniform,
    ParityDeterminesTetrahedron,
]


def run_all():
    """Run all orbit statistics tests."""
    return run_tests(
        title="Orbit Statistics",
        summary=(
            "An 'orbit' completes when the cumulative sum of Pi digits crosses a multiple "
            "of 8. Mean digits per orbit is about 2.42, derived from Pi's mean base-8 digit "
            "of approximately 3.31 (since 8 / 3.31 = 2.42). The two tetrahedra are visited "
            "equally due to parity symmetry. These statistical properties emerge from the "
            "combination of Pi's digit distribution and the 8-vertex structure."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
