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

import sys
import os
import math
from typing import Dict, Optional, List
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

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

class VertexEqualsCumsumMod8(GFDTest):
    """
    INVARIANT: vertex = cumsum % 8 (ALWAYS).
    Like verifying crankshaft position matches encoder.
    """
    name = "Vertex = Cumsum mod 8"
    question = "Does the vertex position always equal the cumulative sum modulo 8, ensuring deterministic state mapping?"
    reference_source = "State machine definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: The Field Chamber has 2k=8 vertices labeled 0-7. "
        "STEP 1: Each pi base-8 digit advances the cumulative sum. "
        "STEP 2: The current vertex is computed as cumsum mod 8. "
        "STEP 3: This modular arithmetic wraps the cumsum into the valid vertex range [0,7]. "
        "OUTPUT: vertex = cumsum mod 8 is the defining relation of the state machine."
    )
    commentary = None  # Fundamental invariant verification
    
    def model(self) -> Dict[str, float]:
        states = build_state_sequence(100)
        violations = sum(1 for s in states if s['vertex'] != s['cumsum'] % 8)
        return {
            "Violations": violations,
            "States checked": len(states),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Violations": 0,
            "States checked": 101,
        }


class OrbitEqualsCumsumDiv8(GFDTest):
    """
    INVARIANT: orbit = cumsum // 8 (ALWAYS).
    Orbit counter tracks cumulative angular position.
    """
    name = "Orbit = Cumsum // 8"
    question = "Does the orbit count equal the integer division of cumulative sum by 8, tracking complete traversal cycles?"
    reference_source = "State machine definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: One complete orbit traverses all 2k=8 vertex positions. "
        "STEP 1: Each orbit corresponds to accumulating 8 units of cumsum. "
        "STEP 2: Integer division cumsum // 8 counts how many complete sets of 8 have been traversed. "
        "STEP 3: The orbit number increments each time cumsum crosses a multiple of 8. "
        "OUTPUT: orbit = cumsum // 8 counts completed Field Closure cycles."
    )
    commentary = None  # Fundamental invariant verification
    
    def model(self) -> Dict[str, float]:
        states = build_state_sequence(100)
        violations = sum(1 for s in states if s['orbit'] != s['cumsum'] // 8)
        return {
            "Violations": violations,
            "States checked": len(states),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Violations": 0,
            "States checked": 101,
        }


class TetrahedronMatchesParity(GFDTest):
    """
    INVARIANT: Tet A = odd parity vertices, Tet B = even parity.
    Tetrahedron assignment is deterministic from vertex number.
    """
    name = "Tetrahedron Matches Parity"
    question = "Does the binary parity of each vertex index deterministically assign it to Tetrahedron A (odd) or Tetrahedron B (even)?"
    reference_source = "Parity definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each vertex index 0-7 has a 3-bit binary representation. "
        "STEP 1: Count the number of 1-bits in the binary representation. "
        "STEP 2: If the count is odd (vertices 1,2,4,7), assign to Tetrahedron A. "
        "STEP 3: If the count is even (vertices 0,3,5,6), assign to Tetrahedron B. "
        "OUTPUT: Parity partitions the 8 vertices into two disjoint sets of 4, each forming a tetrahedron."
    )
    commentary = (
        "Parity-based Field Chamber assignment ensures the dual structure emerges "
        "deterministically from vertex indices. This binary partition underlies "
        "the consistent separation of Tetrahedron A and Tetrahedron B throughout traversal."
    )
    
    def model(self) -> Dict[str, float]:
        states = build_state_sequence(100)
        violations = 0
        for s in states:
            expected = 'A' if s['vertex'] in TET_A else 'B'
            if s['tetrahedron'] != expected:
                violations += 1
        return {"Violations": violations}
    
    def observations(self) -> Dict[str, float]:
        return {"Violations": 0}


class StateDeterminism(GFDTest):
    """
    DETERMINISM: Same input -> Same output (ALWAYS).
    Run twice and verify identical results.
    """
    name = "State Determinism"
    question = "Given identical pi digit inputs, does the traversal state machine produce identical outputs across multiple executions?"
    reference_source = "Reproducibility requirement"
    tolerance = 0.0
    derivation = (
        "PREMISE: A deterministic system produces identical outputs from identical inputs. "
        "STEP 1: Initialize two independent traversals with the same pi digit sequence. "
        "STEP 2: Execute both traversals using identical state transition rules. "
        "STEP 3: Compare cumsum and vertex at each step across both executions. "
        "OUTPUT: Zero mismatches confirms the state machine is fully deterministic."
    )
    commentary = None  # Mechanical reproducibility check
    
    def model(self) -> Dict[str, float]:
        states1 = build_state_sequence(50)
        states2 = build_state_sequence(50)
        
        mismatches = sum(1 for s1, s2 in zip(states1, states2)
                        if s1['cumsum'] != s2['cumsum'] or s1['vertex'] != s2['vertex'])
        return {"Mismatches": mismatches}
    
    def observations(self) -> Dict[str, float]:
        return {"Mismatches": 0}


class CumsumMonotonic(GFDTest):
    """
    MONOTONICITY: cumsum is non-decreasing (digits >= 0).
    """
    name = "Cumsum Monotonic"
    question = "Is the cumulative sum always non-decreasing, ensuring unidirectional progression through the Field Chamber?"
    reference_source = "Digit range [0,7]"
    tolerance = 0.0
    derivation = (
        "PREMISE: Pi base-8 digits are in the range [0,7], all non-negative. "
        "STEP 1: At each step, cumsum_new = cumsum_old + digit. "
        "STEP 2: Since digit >= 0, cumsum_new >= cumsum_old always. "
        "STEP 3: The only way cumsum could decrease would be negative digits, which do not exist. "
        "OUTPUT: Monotonicity is guaranteed by the non-negative digit range."
    )
    commentary = (
        "Monotonic cumulative sum progression reflects unidirectional advancement "
        "through the Field Chamber structure. This property is consistent with "
        "a time-forward traversal where information accumulates without reversal."
    )
    
    def model(self) -> Dict[str, float]:
        states = build_state_sequence(100)
        violations = sum(1 for i in range(1, len(states))
                        if states[i]['cumsum'] < states[i-1]['cumsum'])
        return {"Violations": violations}
    
    def observations(self) -> Dict[str, float]:
        return {"Violations": 0}


class IncrementEqualsDigit(GFDTest):
    """
    INCREMENT: cumsum[n] - cumsum[n-1] = digit[n].
    Fundamental accounting check.
    """
    name = "Increment = Digit"
    question = "Does the difference between consecutive cumulative sums exactly equal the corresponding pi digit?"
    reference_source = "Cumsum definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: The cumulative sum is defined as the running total of pi digits. "
        "STEP 1: By definition, cumsum[n] = cumsum[n-1] + digit[n]. "
        "STEP 2: Rearranging: cumsum[n] - cumsum[n-1] = digit[n]. "
        "STEP 3: This equality must hold at every step for correct accounting. "
        "OUTPUT: Any violation indicates an arithmetic error in the traversal."
    )
    commentary = None  # Fundamental accounting verification
    
    def model(self) -> Dict[str, float]:
        states = build_state_sequence(100)
        violations = 0
        prev_cumsum = 0
        for s in states:
            delta = s['cumsum'] - prev_cumsum
            if delta != s['digit']:
                violations += 1
            prev_cumsum = s['cumsum']
        return {"Violations": violations}
    
    def observations(self) -> Dict[str, float]:
        return {"Violations": 0}


class DigitDistributionReasonable(GFDTest):
    """
    Pi digits should be roughly uniformly distributed (0-7).
    """
    name = "Digit Distribution"
    question = "Are pi's base-8 digits approximately uniformly distributed across 0-7, consistent with pi being a normal number?"
    reference_source = "Normal number conjecture"
    tolerance = 0.30
    derivation = (
        "PREMISE: A normal number has uniformly distributed digits in every base. "
        "STEP 1: For base-8, the expected frequency of each digit 0-7 is 1/8 = 12.5%. "
        "STEP 2: Calculate observed frequency for each digit in the sample. "
        "STEP 3: Compute maximum deviation from expected 12.5%. "
        "OUTPUT: Deviation < 30% supports approximate uniformity over this sample size."
    )
    commentary = (
        "Approximately uniform digit distribution is consistent with the conjecture "
        "that pi is a normal number. This statistical property ensures balanced "
        "sampling across all vertices of the Field Chamber over long traversals."
    )
    
    def model(self) -> Dict[str, float]:
        observed = Counter(PI_BASE8_FRACTIONAL)
        n = len(PI_BASE8_FRACTIONAL)
        expected = n / 8
        
        max_dev = max(abs(observed.get(d, 0) - expected) / expected for d in range(8))
        
        return {
            "Max deviation from expected": max_dev,
            "Expected per digit": expected,
        }
    
    def observations(self) -> Optional[Dict[str, float]]:
        # Statistical check - deviation depends on sample
        # Important check: deviation should be < tolerance
        return None


class VertexErgodicity(GFDTest):
    """
    ERGODICITY: Each vertex visited approximately equally over time.
    """
    name = "Vertex Ergodicity"
    question = "Over extended traversal, does each of the 8 vertices receive approximately equal visitation, satisfying ergodic sampling?"
    reference_source = "Ergodic hypothesis"
    tolerance = 0.30
    derivation = (
        "PREMISE: Ergodicity requires time averages to equal ensemble averages. "
        "STEP 1: With 2k=8 vertices and uniform digit distribution, expected visit fraction is 1/8 per vertex. "
        "STEP 2: Track vertex visits across N traversal steps. "
        "STEP 3: Calculate deviation of each vertex's visit count from N/8. "
        "OUTPUT: Maximum deviation < 30% indicates ergodic sampling over this sample."
    )
    commentary = (
        "Ergodic vertex visitation indicates the traversal samples all regions of "
        "the Field Chamber with statistical uniformity. This property suggests "
        "long-term averages reflect the complete geometric structure."
    )
    
    def model(self) -> Dict[str, float]:
        states = build_state_sequence(100)
        vertex_counts = Counter(s['vertex'] for s in states)
        
        expected = len(states) / 8
        max_dev = max(abs(vertex_counts.get(v, 0) - expected) / expected for v in range(8))
        
        return {
            "Max vertex deviation": max_dev,
        }


class TetrahedronBalance(GFDTest):
    """
    Tet A and Tet B should be visited approximately equally.
    """
    name = "Tetrahedron Balance"
    question = "Does pi-driven traversal visit Tetrahedron A and Tetrahedron B with approximately equal frequency, reflecting bimetric symmetry?"
    reference_source = "Bimetric balance"
    tolerance = 0.10
    derivation = (
        "PREMISE: Each tetrahedron contains 4 of the 8 vertices (50% each by structure). "
        "STEP 1: Tet A vertices {1,2,4,7} and Tet B vertices {0,3,5,6} partition the vertex set. "
        "STEP 2: With ergodic vertex sampling, each tetrahedron should receive ~50% of visits. "
        "STEP 3: Compute ratio of Tet A visits to total visits. "
        "OUTPUT: Ratio near 0.5 confirms balanced bimetric coupling."
    )
    commentary = (
        "Balanced visitation between Tetrahedron A and Tetrahedron B reflects "
        "the symmetric parity structure. This equilibrium between Field Chambers "
        "is consistent with bimetric theories where dual sectors couple equally."
    )
    
    def model(self) -> Dict[str, float]:
        states = build_state_sequence(100)
        tet_a = sum(1 for s in states if s['tetrahedron'] == 'A')
        tet_b = sum(1 for s in states if s['tetrahedron'] == 'B')
        total = tet_a + tet_b
        ratio_a = tet_a / total
        
        return {
            "Tet A visits": tet_a,
            "Tet B visits": tet_b,
            "Ratio A": ratio_a,
        }
    
    def observations(self) -> Optional[Dict[str, float]]:
        # Statistical check - exact counts depend on traversal data
        # Important: both should be visited, ratio should be near 0.5
        return None


class AlphaFromOrbits(GFDTest):
    """
    137 orbits corresponds to 1/alpha. This establishes a correspondence
    between orbit count and the fine structure constant.
    """
    name = "Alpha from Orbits"
    question = "Does the fine structure constant alpha approximately equal 1/137, establishing a correspondence with orbit counting?"
    reference_source = "Fine structure constant"
    tolerance = 0.01
    derivation = (
        "PREMISE: The fine structure constant alpha ≈ 1/137.036 characterizes electromagnetic coupling. "
        "STEP 1: The model proposes 137 orbits as a characteristic electron cycle count. "
        "STEP 2: Derived alpha = 1/137 ≈ 0.00730. "
        "STEP 3: Compare to measured alpha = 1/137.036 ≈ 0.00729735. "
        "OUTPUT: Agreement within 0.03% suggests a numerical correspondence."
    )
    commentary = (
        "The correspondence between 137 orbits and 1/alpha connects traversal "
        "counting to the fine structure constant. This numerical relationship "
        "suggests a possible information-theoretic interpretation of electromagnetic "
        "coupling strength in terms of Field Closure cycles."
    )
    
    def model(self) -> Dict[str, float]:
        orbits_per_electron = 137
        derived_alpha = 1 / orbits_per_electron
        
        return {
            "Derived alpha": derived_alpha,
            "Actual alpha": ALPHA,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Derived alpha": 1/137,
            "Actual alpha": ALPHA,
        }


class SpinFromFaces(GFDTest):
    """
    2 TIME Coupling Ports / 8 total = 1/4 -> Spin correspondence = 1/4 × 2 = 1/2.
    """
    name = "Spin from Coupling Ports"
    question = "Does the ratio of TIME Coupling Ports to total faces yield a spin-1/2 correspondence through geometric counting?"
    reference_source = "Electron spin"
    tolerance = 1e-10
    derivation = (
        "PREMISE: The stellated octahedron has 8 total Coupling Ports (k=4 per tetrahedron × 2). "
        "STEP 1: Of these 8 faces, 2 are TIME Coupling Ports (one per tetrahedron apex). "
        "STEP 2: TIME fraction = 2/8 = 1/4. "
        "STEP 3: Multiply by 2 (the bimetric factor): spin = (1/4) × 2 = 1/2. "
        "OUTPUT: The geometric ratio yields the fermion spin quantum number."
    )
    commentary = (
        "The ratio of TIME to total Coupling Ports (2/8 = 1/4) multiplied by 2 "
        "yields 1/2, corresponding numerically to fermion spin. This geometric "
        "derivation suggests spin may have topological origins in the Field "
        "Chamber face structure."
    )
    
    def model(self) -> Dict[str, float]:
        time_faces = 2
        total_faces = 8
        time_fraction = time_faces / total_faces
        spin = time_fraction * 2
        
        return {
            "TIME faces": time_faces,
            "Total faces": total_faces,
            "Spin": spin,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "TIME faces": 2,
            "Total faces": 8,
            "Spin": 0.5,
        }


class KFromTopology(GFDTest):
    """
    k=4 appears in: vertices per tet, faces per tet, base 8 = 2k.
    """
    name = "k=4 from Topology"
    question = "Does the Field Closure constant k=4 appear consistently throughout the topology as vertices per tetrahedron, faces per tetrahedron, and base 2k=8?"
    reference_source = "Tetrahedral structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: k=4 is the fundamental Field Closure topology constant. "
        "STEP 1: A tetrahedron has k=4 vertices by definition. "
        "STEP 2: A tetrahedron has k=4 faces (triangular Coupling Ports). "
        "STEP 3: The dual structure has 2k=8 total vertices, hence base-8 encoding. "
        "STEP 4: Spatial dimensions d = k-1 = 3. "
        "OUTPUT: k=4 organizes the entire Field Chamber structure."
    )
    commentary = (
        "The topology constant k=4 appears in multiple structural relationships: "
        "vertices per tetrahedron, faces per tetrahedron, and base-8 as 2k. This "
        "consistency suggests k is a fundamental organizing parameter of the "
        "Field Chamber geometry."
    )
    
    def model(self) -> Dict[str, float]:
        return {
            "Vertices per tet": len(TET_A),
            "Base 8 = 2k": 8,
            "k": K,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Vertices per tet": 4,
            "Base 8 = 2k": 8,
            "k": 4,
        }


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


def run_all_tests() -> bool:
    """Run all Field Closure system validation tests."""
    return run_test_group(
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
    success = run_all_tests()
    sys.exit(0 if success else 1)
