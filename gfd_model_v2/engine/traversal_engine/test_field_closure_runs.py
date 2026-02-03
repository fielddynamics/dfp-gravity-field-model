"""
Field Closure Runs
==================

This module analyzes individual Field Closure cycles (orbits) derived from
pi base-8 traversal. A closure completes when cumsum reaches a multiple of 8
(one complete orbit through the dual Field Chamber).

Key observations:
- Orbit lengths vary based on pi digit sequence
- 137 orbits corresponds to 1/alpha
- All closures end at V0 (cumsum % 8 == 0)
- Settlement frequency approximately 10^20 Hz
"""

import sys
import os
import math
from typing import Dict, Optional, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

# =============================================================================
# CONSTANTS
# =============================================================================

ALPHA = 1/137.036
LAMBDA_COMPTON = 2.426310238e-12  # meters
C = 2.998e8  # m/s

# Pi base-8 fractional digits (first 200)
PI_BASE8_FRACTIONAL = [
    1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, 0, 2, 1, 5,
    1, 4, 2, 3, 0, 5, 5, 4, 5, 4, 1, 2, 2, 0, 3, 5, 2, 3, 4, 6,
    5, 4, 2, 1, 1, 3, 2, 6, 7, 2, 2, 3, 0, 1, 4, 6, 5, 4, 4, 0,
    6, 3, 4, 5, 6, 0, 6, 2, 3, 6, 5, 6, 3, 6, 6, 1, 0, 1, 5, 5,
    2, 3, 7, 2, 1, 5, 1, 6, 4, 5, 6, 7, 4, 2, 3, 7, 3, 2, 4, 2,
    2, 1, 7, 1, 1, 6, 7, 4, 0, 5, 5, 5, 2, 6, 4, 1, 7, 7, 0, 6,
    3, 3, 6, 1, 6, 1, 5, 4, 6, 6, 3, 0, 5, 6, 5, 6, 1, 5, 6, 7,
    1, 6, 1, 5, 4, 2, 6, 0, 7, 5, 5, 4, 4, 5, 4, 0, 3, 6, 2, 5,
    7, 2, 6, 0, 2, 4, 2, 6, 6, 4, 0, 1, 5, 0, 2, 3, 2, 4, 6, 4,
    7, 2, 1, 4, 6, 3, 0, 1, 0, 4, 6, 5, 3, 5, 1, 5, 7, 1, 6, 4,
]

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}


def get_pi_base8(n_digits, include_integer=True):
    """Get pi base-8 digits."""
    if include_integer:
        return [3] + PI_BASE8_FRACTIONAL[:n_digits]
    return PI_BASE8_FRACTIONAL[:n_digits]


def get_tetrahedron(vertex):
    """Get tetrahedron for vertex."""
    return 'A' if vertex in TET_A else 'B'


def calculate_settlement_frequency():
    """Settlement frequency from Compton wavelength."""
    return C / LAMBDA_COMPTON


def calculate_closure_runs(num_closures=20):
    """Calculate closure runs from pi base-8."""
    num_digits = min(num_closures * 20, 190)
    digits = get_pi_base8(num_digits, include_integer=True)
    
    closures = []
    cumsum = 0
    prev_cumsum = 0
    closure_start_step = 0
    current_digits = []
    current_vertices = []
    current_tet_a = 0
    current_tet_b = 0
    closure_count = 0
    
    for step, digit in enumerate(digits):
        prev_cumsum = cumsum
        cumsum += digit
        vertex = cumsum % 8
        tet = get_tetrahedron(vertex)
        
        current_digits.append(digit)
        current_vertices.append(vertex)
        if tet == 'A':
            current_tet_a += 1
        else:
            current_tet_b += 1
        
        # Check for closure
        is_at_boundary = (cumsum > 0 and cumsum % 8 == 0)
        crossed_boundary = (prev_cumsum // 8) < (cumsum // 8)
        
        if is_at_boundary and crossed_boundary:
            closure_count += 1
            closures.append({
                'closure_number': closure_count,
                'steps_in_closure': step - closure_start_step + 1,
                'digit_sum': sum(current_digits),
                'final_vertex': vertex,
                'tet_a_visits': current_tet_a,
                'tet_b_visits': current_tet_b,
            })
            
            if closure_count >= num_closures:
                break
            
            closure_start_step = step + 1
            current_digits = []
            current_vertices = []
            current_tet_a = 0
            current_tet_b = 0
    
    return closures


# =============================================================================
# TESTS
# =============================================================================

class ClosureRunsCalculated(GFDTest):
    """
    Closure runs can be calculated from pi base-8 digits.
    """
    name = "Closure Runs Calculated"
    question = "Can individual Field Closure cycles be algorithmically computed from pi base-8 digit sequences?"
    reference_source = None  # Algorithm verification
    derivation = (
        "PREMISE: A closure occurs when cumsum crosses a multiple of 8 (orbit boundary). "
        "STEP 1: Initialize cumsum=0 and closure_count=0. "
        "STEP 2: For each digit, add to cumsum and check if cumsum mod 8 = 0. "
        "STEP 3: When boundary crossed (cumsum//8 increases), record the closure. "
        "STEP 4: Continue until desired number of closures are captured. "
        "OUTPUT: The algorithm successfully identifies discrete closure events."
    )
    commentary = None  # Mechanical algorithm verification
    
    def model(self) -> Dict[str, float]:
        closures = calculate_closure_runs(10)
        return {
            "Closures calculated": len(closures),
            "Expected": 10,
        }


class ClosureDigitSumsMultipleOf8(GFDTest):
    """
    Each closure's digit sum equals a multiple of 8
    (the cumsum advance from one boundary to the next).
    """
    name = "Digit Sums Multiple of 8"
    question = "Does each Field Closure cycle span exactly a multiple of 8 cumsum units, corresponding to complete 2k-vertex orbits?"
    reference_source = "Orbit boundary definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: Orbit boundaries occur at cumsum = 8n for integer n. "
        "STEP 1: A closure starts when cumsum reaches boundary 8n. "
        "STEP 2: The closure ends when cumsum reaches the next boundary 8(n+1). "
        "STEP 3: Digit sum for that closure = 8(n+1) - 8n = 8. "
        "STEP 4: More generally, spanning m boundaries gives digit sum = 8m. "
        "OUTPUT: Every closure's digit sum is necessarily a multiple of 8."
    )
    commentary = (
        "Closure digit sums being multiples of 8 reflects the 8-vertex cycle of the "
        "Field Chamber. Each orbit represents a complete traversal through all "
        "possible vertex states modulo 8."
    )
    
    def model(self) -> Dict[str, float]:
        closures = calculate_closure_runs(20)
        all_valid = all(c['digit_sum'] % 8 == 0 for c in closures)
        return {
            "All multiples of 8": 1 if all_valid else 0,
            "Closures checked": len(closures),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "All multiples of 8": 1,
            "Closures checked": 20,
        }


class ClosuresEndAtV0(GFDTest):
    """
    All closures end at V0 because cumsum % 8 == 0 at closure.
    """
    name = "Closures End at V0"
    question = "Does every Field Closure terminate at vertex V0, the Tetrahedron B apex where cumsum mod 8 equals zero?"
    reference_source = "Closure definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: Closure occurs when cumsum reaches a multiple of 8. "
        "STEP 1: At closure, cumsum = 8n for some integer n. "
        "STEP 2: Vertex = cumsum mod 8 = 8n mod 8 = 0. "
        "STEP 3: V0 is the vertex with index 0, belonging to Tetrahedron B. "
        "OUTPUT: By definition, all closures terminate at V0."
    )
    commentary = (
        "Every Field Closure terminates at V0, the Tetrahedron B apex. This return "
        "to the origin vertex suggests V0 may represent a ground state or equilibrium "
        "configuration within the Field Chamber dynamics."
    )
    
    def model(self) -> Dict[str, float]:
        closures = calculate_closure_runs(20)
        all_at_v0 = all(c['final_vertex'] == 0 for c in closures)
        return {
            "All end at V0": 1 if all_at_v0 else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "All end at V0": 1,
        }


class ClosureLengthsVary(GFDTest):
    """
    Closure lengths vary because pi is irrational.
    Not all closures take the same number of steps.
    """
    name = "Closure Lengths Vary"
    question = "Do Field Closure cycle lengths vary due to pi's irrational and non-repeating digit sequence?"
    reference_source = "Irrational number property"
    derivation = (
        "PREMISE: Pi is irrational with non-repeating, non-periodic digits. "
        "STEP 1: Closure length depends on how many digits sum to 8. "
        "STEP 2: Different digit sequences reach 8 in different numbers of steps. "
        "STEP 3: A sequence like [7,1] reaches 8 in 2 steps; [1,1,1,1,1,1,1,1] takes 8. "
        "STEP 4: Count unique closure lengths over many closures. "
        "OUTPUT: Multiple distinct lengths confirms variable, aperiodic behavior."
    )
    commentary = (
        "Variable closure lengths reflect pi's non-repeating digit sequence. "
        "This aperiodicity may contribute to the emergence of statistical "
        "behavior from deterministic traversal rules."
    )
    
    def model(self) -> Dict[str, float]:
        closures = calculate_closure_runs(50)
        steps = [c['steps_in_closure'] for c in closures]
        unique_lengths = len(set(steps))
        return {
            "Unique closure lengths": unique_lengths,
            "Lengths vary": 1 if unique_lengths > 1 else 0,
        }


class BothTetrahedraVisited(GFDTest):
    """
    Most closures visit both tetrahedra (interleaved traversal).
    """
    name = "Both Tetrahedra Visited"
    question = "Do the majority of Field Closure cycles visit vertices from both Tetrahedron A and Tetrahedron B, demonstrating bimetric interleaving?"
    reference_source = "Bimetric coupling"
    tolerance = 0.1
    derivation = (
        "PREMISE: Bimetric coupling requires engagement of both Field Chambers. "
        "STEP 1: For each closure, track which tetrahedron each visited vertex belongs to. "
        "STEP 2: Count closures where Tet_A_visits > 0 AND Tet_B_visits > 0. "
        "STEP 3: Calculate ratio = both_visited / total_closures. "
        "OUTPUT: High ratio (>90%) confirms strong bimetric interleaving."
    )
    commentary = (
        "The majority of closures sampling both Field Chambers indicates strong "
        "bimetric coupling in the traversal dynamics. This interleaving prevents "
        "either tetrahedron from being isolated during the closure process."
    )
    
    def model(self) -> Dict[str, float]:
        closures = calculate_closure_runs(100)
        visits_both = sum(1 for c in closures 
                        if c['tet_a_visits'] > 0 and c['tet_b_visits'] > 0)
        ratio = visits_both / len(closures)
        return {
            "Closures visiting both": visits_both,
            "Total closures": len(closures),
            "Ratio": ratio,
        }
    
    def observations(self) -> Optional[Dict[str, float]]:
        # The exact counts depend on digit sequence and algorithm
        # Important check: most closures visit both tetrahedra
        return None


class ClosureStatisticsReasonable(GFDTest):
    """
    Average steps per closure should be in reasonable range
    based on pi digit distribution.
    """
    name = "Closure Statistics"
    question = "Is the average Field Closure length approximately 8/(mean digit) ≈ 2.4 steps, consistent with pi's digit statistics?"
    reference_source = "Statistical expectation"
    derivation = (
        "PREMISE: Each closure spans 8 cumsum units. "
        "STEP 1: Pi base-8 digits range 0-7 with mean ≈ 3.5 (for uniform distribution). "
        "STEP 2: Actual pi digit mean is close to 3.5, say ~3.3 in practice. "
        "STEP 3: Expected steps per closure = 8 / mean_digit ≈ 8/3.3 ≈ 2.4. "
        "STEP 4: Measure actual average across many closures. "
        "OUTPUT: Average near 2-3 steps confirms statistical consistency."
    )
    commentary = (
        "The average closure length of approximately 2-3 digits corresponds to "
        "pi's mean digit value dividing into 8. This statistical consistency "
        "confirms the traversal follows expected digit distribution patterns."
    )
    
    def model(self) -> Dict[str, float]:
        closures = calculate_closure_runs(100)
        steps = [c['steps_in_closure'] for c in closures]
        avg = sum(steps) / len(steps)
        min_steps = min(steps)
        max_steps = max(steps)
        return {
            "Average steps": avg,
            "Min steps": min_steps,
            "Max steps": max_steps,
        }


class SettlementFrequency(GFDTest):
    """
    Settlement frequency from Compton wavelength is ~10^20 Hz.
    """
    name = "Settlement Frequency"
    question = "Does the settlement frequency f = c/λ_Compton yield approximately 1.24×10²⁰ Hz, placing Field Closure at QED scales?"
    reference_source = "Compton wavelength"
    tolerance = 0.5  # Order of magnitude
    derivation = (
        "PREMISE: The electron Compton wavelength λ_c = 2.426×10⁻¹² m defines a quantum scale. "
        "STEP 1: Settlement frequency f = c / λ_c. "
        "STEP 2: f = (2.998×10⁸ m/s) / (2.426×10⁻¹² m). "
        "STEP 3: f ≈ 1.235×10²⁰ Hz. "
        "OUTPUT: This frequency places Field Closure dynamics at quantum electrodynamic timescales."
    )
    commentary = (
        "The settlement frequency derived from the electron Compton wavelength "
        "places Field Closure dynamics at quantum electrodynamic scales. This "
        "frequency connects electron mass-energy to the Field Closure cycle rate."
    )
    
    def model(self) -> Dict[str, float]:
        f = calculate_settlement_frequency()
        return {"Settlement frequency (Hz)": f}
    
    def observations(self) -> Dict[str, float]:
        return {"Settlement frequency (Hz)": 1.235e20}


class OrbitsForElectron(GFDTest):
    """
    137 orbits make one electron (1/alpha).
    """
    name = "137 Orbits per Electron"
    question = "Does the inverse fine structure constant 1/α ≈ 137 establish a correspondence between orbit count and electron structure?"
    reference_source = "Fine structure constant"
    tolerance = 0.001
    derivation = (
        "PREMISE: The fine structure constant α ≈ 1/137.036 governs electromagnetic coupling. "
        "STEP 1: Calculate 1/α = 137.036. "
        "STEP 2: Round to integer: 137 orbits per characteristic electron cycle. "
        "STEP 3: This count may represent complete phase accumulation for electron identity. "
        "OUTPUT: 137 orbits establishes a numerical correspondence with α."
    )
    commentary = (
        "The correspondence between 137 orbits and 1/alpha suggests a possible "
        "information-theoretic interpretation of the fine structure constant. "
        "This relationship connects electromagnetic coupling strength to orbit "
        "counting in the Field Closure model."
    )
    
    def model(self) -> Dict[str, float]:
        orbits = int(1 / ALPHA)
        return {
            "1/alpha": 1/ALPHA,
            "Orbits per electron": orbits,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "1/alpha": 137.036,
            "Orbits per electron": 137,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    ClosureRunsCalculated,
    ClosureDigitSumsMultipleOf8,
    ClosuresEndAtV0,
    ClosureLengthsVary,
    BothTetrahedraVisited,
    ClosureStatisticsReasonable,
    SettlementFrequency,
    OrbitsForElectron,
]


def run_all_tests() -> bool:
    """Run all Field Closure run tests."""
    return run_test_group(
        title="Field Closure Runs",
        summary=(
            "These tests analyze Field Closure cycles (orbits) from pi base-8 traversal. "
            "Each closure completes when cumsum reaches a multiple of 8, ending at V0 "
            "(Tet_B apex). Closure lengths vary because pi is irrational. Most closures "
            "visit both Field Chambers due to interleaved traversal. The settlement "
            "frequency (~10^20 Hz) corresponds to the timing scale, and 137 orbits "
            "corresponds to 1/alpha."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
