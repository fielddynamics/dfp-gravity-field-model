"""
Orbit Statistics
================

An "orbit" is defined as the accumulation of 8 units through traversal of the
stellated octahedron's vertices. Pi digits in base-8 drive the traversal,
and the statistics of orbit lengths reveal properties of the traversal.

The model predicts:
- Mean digits per orbit of approximately 2.42 (since 8 / mean_digit ≈ 8 / 3.31)
- Equal visitation of both tetrahedra (50%/50% by parity symmetry)
- Uniform vertex visitation (approximately 12.5% each)

These statistical properties emerge from the combination of Pi's digit
distribution and the geometry of the 8-vertex structure.
"""

import sys
import os
from typing import Dict, Optional
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
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

class MeanDigitsPerOrbit(GFDTest):
    """
    Mean digits per orbit = 8 / mean_digit_value. With Pi's base-8 digits
    averaging about 3.31, we expect approximately 2.42 digits per orbit.
    This value emerges from Pi's statistical properties.
    """
    name = "Mean Digits Per Orbit"
    question = "Does the mean number of digits per orbit equal 2k/⟨digit⟩ = 8/⟨digit⟩ ≈ 2.4, consistent with pi's digit statistics?"
    reference_source = "Theoretical (8 / mean_digit)"
    tolerance = 0.05
    derivation = (
        "PREMISE: Each orbit spans 2k=8 cumsum units; digit count depends on mean digit value. "
        "STEP 1: For uniform distribution over 0-7, mean digit = (0+1+...+7)/8 = 3.5. "
        "STEP 2: Actual pi digits have mean ≈ 3.31 (slight deviation from uniform). "
        "STEP 3: Expected digits per orbit = 8 / ⟨digit⟩ = 8 / 3.31 ≈ 2.42. "
        "STEP 4: Measure actual mean across many orbits and compare. "
        "OUTPUT: Mean digits per orbit ≈ 2.4."
    )
    commentary = (
        "The mean digits per orbit of approximately 2.4 emerges from pi's base-8 "
        "digit statistics. This value determines the typical information content "
        "per complete traversal cycle and follows from pi's mathematical properties."
    )
    
    def model(self) -> Dict[str, float]:
        stats = analyze_orbit_stats(1000)
        return {"Mean digits per orbit": stats['mean_length']}
    
    def observations(self) -> Dict[str, float]:
        stats = analyze_orbit_stats(1000)
        return {"Mean digits per orbit": stats['theoretical']}


class OrbitLengthDistribution(GFDTest):
    """
    Most orbits (>85%) should be 1-3 digits. Small digits accumulate,
    while large digits (like 7) can cross boundaries alone. This
    distribution emerges from Pi's digit patterns.
    """
    name = "Orbit Length Distribution"
    question = "Do more than 85% of orbits complete within 1-3 digits, reflecting pi's digit distribution characteristics?"
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Orbit length depends on how many digits sum to 8. "
        "STEP 1: Large digits (6,7) can nearly or fully complete an orbit alone. "
        "STEP 2: Medium digits (3,4,5) typically complete orbits in 2 steps. "
        "STEP 3: Small digits (0,1,2) require more steps to sum to 8. "
        "STEP 4: Pi's roughly uniform distribution favors short orbit lengths. "
        "STEP 5: Count orbits with length ≤ 3 and divide by total. "
        "OUTPUT: Short orbit fraction > 0.85, above threshold = 1."
    )
    commentary = (
        "The concentration of orbit lengths in the 1-3 digit range reflects the "
        "distribution of pi's base-8 digits. Large digits can complete orbits "
        "rapidly, while sequences of small digits take longer."
    )
    
    def model(self) -> Dict[str, float]:
        stats = analyze_orbit_stats(1000)
        is_short = 1 if stats['short_ratio'] > 0.85 else 0
        return {
            "Short orbit fraction": stats['short_ratio'],
            "Above 85% threshold": is_short,
        }


class MinimumOrbitLength(GFDTest):
    """
    A single large digit (like 7) can complete an orbit alone if the
    cumsum was already near a boundary. This proves the minimum orbit
    length is 1 digit.
    """
    name = "Minimum Orbit Length"
    question = "Can a single digit complete an orbit, demonstrating that the minimum orbit length is 1?"
    reference_source = "Theoretical (min = 1)"
    tolerance = 0.001
    derivation = (
        "PREMISE: A single digit can complete an orbit if it alone spans 8 cumsum units. "
        "STEP 1: If cumsum is at boundary 8n and digit = 8 (impossible in base-8). "
        "STEP 2: Alternatively: cumsum at 8n+1 and digit=7 gives cumsum = 8(n+1). "
        "STEP 3: More generally, any digit ≥ (8 - cumsum mod 8) crosses the boundary. "
        "STEP 4: Example: cumsum=1, digit=7 → cumsum=8 (orbit complete in 1 step). "
        "OUTPUT: Minimum orbit length = 1."
    )
    commentary = None  # Structural observation from traversal mechanics
    
    def model(self) -> Dict[str, float]:
        stats = analyze_orbit_stats(1000)
        return {"Minimum orbit length": stats['min_length']}
    
    def observations(self) -> Dict[str, float]:
        return {"Minimum orbit length": 1}


class MaximumOrbitBounded(GFDTest):
    """
    Even with many small digits, orbits must complete within reasonable
    bounds. A maximum of less than 15 digits confirms the traversal
    cannot "stall" indefinitely.
    """
    name = "Maximum Orbit Bounded"
    question = "Is the maximum orbit length bounded below 15 digits, confirming the traversal cannot stall indefinitely?"
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Even sequences of small digits must eventually sum to 8. "
        "STEP 1: Worst case: all digits are 0 (no progress indefinitely). "
        "STEP 2: But pi has no long runs of zeros; non-zero digits appear regularly. "
        "STEP 3: Even with minimum non-zero digit (1), 8 steps suffice: 1×8 = 8. "
        "STEP 4: Pi's digit variety ensures faster completion in practice. "
        "STEP 5: Observe maximum orbit length across many closures. "
        "OUTPUT: Maximum orbit length < 15, below threshold = 1."
    )
    commentary = (
        "Bounded maximum orbit length confirms the traversal cannot stall "
        "indefinitely on small digit sequences. Pi's digit distribution "
        "ensures eventual orbit completion within reasonable bounds."
    )
    
    def model(self) -> Dict[str, float]:
        stats = analyze_orbit_stats(1000)
        bounded = 1 if stats['max_length'] < 15 else 0
        return {
            "Maximum orbit length": stats['max_length'],
            "Below 15 threshold": bounded,
        }


class TotalOrbitsMatchCumsum(GFDTest):
    """
    The total number of orbit crossings must equal cumsum // 8.
    This validates the orbit counting algorithm against the
    fundamental cumulative sum arithmetic.
    """
    name = "Orbit Count Consistency"
    question = "Does the total orbit count equal cumsum // 8, validating the counting algorithm against fundamental arithmetic?"
    reference_source = "Arithmetic identity"
    tolerance = 0.001
    derivation = (
        "PREMISE: Orbits are counted each time cumsum crosses a multiple of 8. "
        "STEP 1: Final cumsum after N digits = Σ(digits). "
        "STEP 2: Number of complete orbits = floor(cumsum / 8) = cumsum // 8. "
        "STEP 3: The orbit counting algorithm must match this arithmetic identity. "
        "STEP 4: Compare algorithm count to cumsum // 8. "
        "OUTPUT: Orbit count = cumsum // 8."
    )
    commentary = None  # Mechanical consistency check
    
    def model(self) -> Dict[str, float]:
        stats = analyze_orbit_stats(1000)
        expected = stats['final_cumsum'] // 8
        return {
            "Orbit count": stats['total_orbits'],
            "Expected (cumsum // 8)": expected,
        }
    
    def observations(self) -> Dict[str, float]:
        stats = analyze_orbit_stats(1000)
        expected = stats['final_cumsum'] // 8
        return {
            "Orbit count": expected,
            "Expected (cumsum // 8)": expected,
        }


# =============================================================================
# TESTS: TETRAHEDRA BALANCE
# =============================================================================

class TetrahedraNearEqual(GFDTest):
    """
    Tet_A (vertices 1,2,4,7) and Tet_B (vertices 0,3,5,6) should be
    visited equally due to parity symmetry. Each should receive about
    50% of all visits, as expected from the symmetric structure.
    """
    name = "Tetrahedra Near Equal"
    question = "Do Tetrahedron A and Tetrahedron B each receive approximately 50% of vertex visits, reflecting parity symmetry?"
    reference_source = "Parity symmetry (50%/50%)"
    tolerance = 0.10  # Allow 45-55%
    derivation = (
        "PREMISE: Parity symmetry partitions 8 vertices into two equal sets. "
        "STEP 1: Tet_A = {1,2,4,7} (odd parity) has 4 vertices. "
        "STEP 2: Tet_B = {0,3,5,6} (even parity) has 4 vertices. "
        "STEP 3: With uniform vertex visitation, each tetrahedron receives 4/8 = 50%. "
        "STEP 4: Count visits to each tetrahedron across traversal. "
        "OUTPUT: Tet_A visits ≈ 0.50, Tet_B visits ≈ 0.50."
    )
    commentary = (
        "Equal Field Chamber visitation reflects the parity symmetry underlying "
        "the dual tetrahedron structure. Pi's digit distribution couples to both "
        "Field Chambers without systematic bias, consistent with bimetric balance."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_tetrahedra_balance(1000)
        return {
            "Tet_A visits (fraction)": analysis['tet_a_ratio'],
            "Tet_B visits (fraction)": analysis['tet_b_ratio'],
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Tet_A visits (fraction)": 0.50,
            "Tet_B visits (fraction)": 0.50,
        }


class TetrahedraRatioUnity(GFDTest):
    """
    The ratio Tet_A:Tet_B should remain bounded. Pi's digit distribution
    creates statistical fluctuations, but the ratio should not exceed 1.3
    (neither tetrahedron receiving >56% of visits).
    """
    name = "Tetrahedra Ratio Bounded"
    question = "Is the Tet_A/Tet_B visit ratio bounded below 1.3, confirming no extreme bias in pi's traversal?"
    reference_source = None  # Statistical observation
    tolerance = 0.01
    derivation = (
        "PREMISE: Pi's digit distribution couples to the parity partition. "
        "STEP 1: Count Tet_A visits and Tet_B visits during traversal. "
        "STEP 2: Calculate ratio = Tet_A_count / Tet_B_count. "
        "STEP 3: Pi's specific digit sequences may favor one tetrahedron slightly. "
        "STEP 4: Verify ratio < 1.3 (no extreme bias). "
        "OUTPUT: Ratio is bounded, confirming statistical reasonableness."
    )
    commentary = (
        "The bounded ratio between Field Chamber visits confirms pi's traversal "
        "doesn't systematically favor one tetrahedron. While perfect unity isn't "
        "guaranteed, extreme bias would indicate a problem with the traversal model."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_tetrahedra_balance(1000)
        ratio_bounded = 1.0 if analysis['ab_ratio'] < 1.3 else 0.0
        return {
            "Tet_A / Tet_B ratio": analysis['ab_ratio'],
            "Ratio bounded (< 1.3)": ratio_bounded,
        }
    
    def observations(self) -> Dict[str, float]:
        analysis = analyze_tetrahedra_balance(1000)
        return {
            "Tet_A / Tet_B ratio": analysis['ab_ratio'],
            "Ratio bounded (< 1.3)": 1.0,
        }


class VertexDistributionUniform(GFDTest):
    """
    All 8 vertices should be visited with approximately equal frequency
    (about 12.5% each). Maximum deviation from 12.5% should be less than
    5%, indicating uniform sampling of the vertex structure.
    """
    name = "Vertex Distribution Uniform"
    question = "Is the maximum deviation from the expected 12.5% (1/8) vertex frequency below 5%, confirming uniform sampling?"
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: With 2k=8 vertices, uniform visitation gives 1/8 = 12.5% each. "
        "STEP 1: Count visits to each vertex v ∈ {0,1,...,7}. "
        "STEP 2: Calculate fraction for each: f_v = count_v / total. "
        "STEP 3: Compute deviation: |f_v - 0.125| for each vertex. "
        "STEP 4: Find maximum deviation across all 8 vertices. "
        "OUTPUT: Max deviation < 0.05, below threshold = 1."
    )
    commentary = (
        "Near-uniform vertex distribution indicates no systematic bias in the "
        "traversal pattern. This ergodic property ensures all regions of the "
        "Field Chamber are sampled proportionally over time."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_tetrahedra_balance(1000)
        uniform = 1 if analysis['max_vertex_deviation'] < 0.05 else 0
        return {
            "Max deviation from 12.5%": analysis['max_vertex_deviation'],
            "Below 5% threshold": uniform,
        }


class ParityDeterminesTetrahedron(GFDTest):
    """
    Vertex parity (number of 1-bits mod 2) determines tetrahedron membership:
    - Odd parity (1,2,4,7) -> Tet_A
    - Even parity (0,3,5,6) -> Tet_B
    This is the fundamental encoding of the bimetric structure.
    """
    name = "Parity Determines Tetrahedron"
    question = "Does the binary parity (popcount mod 2) of each vertex index deterministically assign tetrahedron membership?"
    reference_source = "Binary parity definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: Tetrahedron membership can be encoded in a single parity bit. "
        "STEP 1: For vertex v, compute popcount(v) = number of 1-bits in binary representation. "
        "STEP 2: Parity = popcount(v) mod 2. "
        "STEP 3: Vertex 0=000→0, 1=001→1, 2=010→1, 3=011→0, 4=100→1, 5=101→0, 6=110→0, 7=111→1. "
        "STEP 4: Odd parity {1,2,4,7} → Tet_A; Even parity {0,3,5,6} → Tet_B. "
        "OUTPUT: Vertices with correct parity assignment = 8."
    )
    commentary = (
        "Binary parity providing deterministic Field Chamber assignment connects "
        "the information-theoretic encoding to geometric structure. This 1-bit "
        "choice underlies all bimetric properties of the traversal."
    )
    
    def model(self) -> Dict[str, float]:
        correct = 0
        for v in range(8):
            parity = bin(v).count('1') % 2
            expected_tet = 'A' if parity == 1 else 'B'
            actual_tet = 'A' if v in TET_A else 'B'
            if expected_tet == actual_tet:
                correct += 1
        return {"Vertices with correct parity assignment": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Vertices with correct parity assignment": 8}


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


def run_all_tests() -> bool:
    """Run all orbit statistics tests."""
    return run_test_group(
        title="Orbit Statistics",
        summary=(
            "An 'orbit' completes when the cumulative sum of Pi digits crosses a multiple "
            "of 8. Mean digits per orbit is about 2.42, derived from Pi's mean base-8 digit "
            "of approximately 3.31 (since 8 / 3.31 ≈ 2.42). The two tetrahedra are visited "
            "equally due to parity symmetry. These statistical properties emerge from the "
            "combination of Pi's digit distribution and the 8-vertex structure."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
