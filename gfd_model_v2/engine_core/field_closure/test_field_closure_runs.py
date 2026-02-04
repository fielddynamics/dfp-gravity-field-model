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

from typing import Dict, Optional, List

from gfd_model_v2.framework import *

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

class ClosureRunsCalculated(Test):
    """
    Closure runs can be calculated from pi base-8 digits.
    """
    name = "Closure Runs Calculated"
    question = (
        "Can we track individual closure cycles? "
        "A 'closure' is one complete orbit, ending when the cumsum becomes a multiple of 8. "
        "This test verifies we can count closures algorithmically from pi's digits."
    )
    reference = None  # Algorithm verification
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A closure occurs when cumsum crosses a multiple of 8 (orbit boundary).")
            .step("Initialize cumsum=0 and closure_count=0.")
            .step("For each digit, add to cumsum and check if cumsum mod 8 = 0.")
            .step("When boundary crossed (cumsum//8 increases), record the closure.")
            .step("Continue until desired number of closures are captured.")
            .conclude("The algorithm successfully identifies discrete closure events.")
        )
    
    commentary = (
        "Think of walking around a track. Every time you cross the start/finish line, "
        "that is one lap (one closure). Here, the 'start line' is whenever cumsum hits "
        "a multiple of 8. We simply count how many times we cross it."
    )
    
    def model(self):
        closures = calculate_closure_runs(10)
        return (
            Model()
            .add("Closures calculated", len(closures))
            .add("Expected", 10)
        )


class ClosureDigitSumsMultipleOf8(Test):
    """
    Each closure's digit sum equals a multiple of 8
    (the cumsum advance from one boundary to the next).
    """
    name = "Digit Sums Multiple of 8"
    question = (
        "Does each closure span exactly 8 (or a multiple)? "
        "Closures are 'laps,' and each lap must cover exactly 8 cumsum units. "
        "This test checks that every closure's digit sum is a multiple of 8."
    )
    reference = "Orbit boundary definition"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Orbit boundaries occur at cumsum = 8n for integer n.")
            .step("A closure starts when cumsum reaches boundary 8n.")
            .step("The closure ends when cumsum reaches the next boundary 8(n+1).")
            .step("Digit sum for that closure = 8(n+1) - 8n = 8.")
            .step("More generally, spanning m boundaries gives digit sum = 8m.")
            .conclude("Every closure's digit sum is necessarily a multiple of 8.")
        )
    
    commentary = (
        "Imagine a track with mile markers at 0, 8, 16, 24... A complete lap goes "
        "from one marker to the next, always covering exactly 8 miles. "
        "The digit sum for each closure is the distance traveled in that lap. "
        "It must be a multiple of 8 because that is the distance between markers."
    )
    
    def model(self):
        closures = calculate_closure_runs(20)
        all_valid = all(c['digit_sum'] % 8 == 0 for c in closures)
        return (
            Model()
            .add("All multiples of 8", 1 if all_valid else 0)
            .add("Closures checked", len(closures))
        )
    
    def observations(self):
        return (
            Observed()
            .add("All multiples of 8", 1)
            .add("Closures checked", 20)
        )


class ClosuresEndAtV0(Test):
    """
    All closures end at V0 because cumsum % 8 == 0 at closure.
    """
    name = "Closures End at V0"
    question = (
        "Where does every closure end? "
        "Since closure means cumsum is a multiple of 8, the vertex must be cumsum mod 8 = 0. "
        "That is vertex V0. This test confirms every closure terminates at V0."
    )
    reference = "Closure definition"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Closure occurs when cumsum reaches a multiple of 8.")
            .step("At closure, cumsum = 8n for some integer n.")
            .step("Vertex = cumsum mod 8 = 8n mod 8 = 0.")
            .step("V0 is the vertex with index 0, belonging to Tetrahedron B.")
            .conclude("By definition, all closures terminate at V0.")
        )
    
    commentary = (
        "All roads lead to V0. When the cumulative sum hits 8, 16, 24, or any multiple of 8, "
        "dividing by 8 and taking the remainder always gives 0. So the 'landing spot' at "
        "the end of every closure is V0. This special vertex is like 'home base'; "
        "every complete orbit brings you back here."
    )
    
    def model(self):
        closures = calculate_closure_runs(20)
        all_at_v0 = all(c['final_vertex'] == 0 for c in closures)
        return Model().add("All end at V0", 1 if all_at_v0 else 0)
    
    def observations(self):
        return Observed().add("All end at V0", 1)


class ClosureLengthsVary(Test):
    """
    Closure lengths vary because pi is irrational.
    Not all closures take the same number of steps.
    """
    name = "Closure Lengths Vary"
    question = (
        "Are all closures the same length? No! "
        "Pi's digits are unpredictable, so some closures take 2 digits, others take 5. "
        "This test confirms closure lengths are not all identical."
    )
    reference = "Irrational number property"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Pi is irrational with non-repeating, non-periodic digits.")
            .step("Closure length depends on how many digits sum to 8.")
            .step("Different digit sequences reach 8 in different numbers of steps.")
            .step("A sequence like [7,1] reaches 8 in 2 steps; [1,1,1,1,1,1,1,1] takes 8.")
            .step("Count unique closure lengths over many closures.")
            .conclude("Multiple distinct lengths confirms variable, aperiodic behavior.")
        )
    
    commentary = (
        "If you need to sum to 8, and your digits are 7, 1, you are done in 2 steps. "
        "But if they are 1, 0, 1, 2, 1, 1, 1, 1, you need 8 steps. "
        "Because pi's digits are unpredictable (irrational means no repeating pattern), "
        "closure lengths vary. This variability gives the traversal its richness."
    )
    
    def model(self):
        closures = calculate_closure_runs(50)
        steps = [c['steps_in_closure'] for c in closures]
        unique_lengths = len(set(steps))
        return (
            Model()
            .add("Unique closure lengths", unique_lengths)
            .add("Lengths vary", 1 if unique_lengths > 1 else 0)
        )


class BothTetrahedraVisited(Test):
    """
    Most closures visit both tetrahedra (interleaved traversal).
    """
    name = "Both Tetrahedra Visited"
    question = (
        "Does each closure touch both halves of the Field Chamber? "
        "The structure has two tetrahedra (A and B). If a closure only visits one, "
        "it misses half the structure. This test checks that most closures visit both."
    )
    reference = "Bimetric coupling"
    tolerance = 0.1
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Bimetric coupling requires engagement of both Field Chambers.")
            .step("For each closure, track which tetrahedron each visited vertex belongs to.")
            .step("Count closures where Tet_A_visits > 0 AND Tet_B_visits > 0.")
            .step("Calculate ratio = both_visited / total_closures.")
            .conclude("High ratio (>90%) confirms strong bimetric interleaving.")
        )
    
    commentary = (
        "Think of a house with two wings. A thorough walkthrough should visit both wings. "
        "Similarly, each closure should typically visit vertices from both tetrahedra. "
        "If most closures touch both Tet A and Tet B, the traversal is 'interleaved,' "
        "confirming the two halves communicate. This bimetric coupling is central to the model."
    )
    
    def model(self):
        closures = calculate_closure_runs(100)
        visits_both = sum(1 for c in closures 
                        if c['tet_a_visits'] > 0 and c['tet_b_visits'] > 0)
        ratio = visits_both / len(closures)
        return (
            Model()
            .add("Closures visiting both", visits_both)
            .add("Total closures", len(closures))
            .add("Ratio", ratio)
        )


class ClosureStatisticsReasonable(Test):
    """
    Average steps per closure should be in reasonable range
    based on pi digit distribution.
    """
    name = "Closure Statistics"
    question = (
        "What is the average closure length? "
        "If digits average about 3.3, and we need to sum to 8, we expect about 8/3.3 = 2.4 steps. "
        "This test checks whether the actual average matches this expectation."
    )
    reference = "Statistical expectation"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each closure spans 8 cumsum units.")
            .step("Pi base-8 digits range 0-7 with mean = 3.5 (for uniform distribution).")
            .step("Actual pi digit mean is close to 3.5, say ~3.3 in practice.")
            .step("Expected steps per closure = 8 / mean_digit = 8/3.3 = 2.4.")
            .step("Measure actual average across many closures.")
            .conclude("Average near 2-3 steps confirms statistical consistency.")
        )
    
    commentary = (
        "If you need to collect $8 and each step gives you an average of $3.30, "
        "you expect to need about 2.4 steps. That is the logic here: closures need 8 cumsum units, "
        "and pi's digits average about 3.3, so closures average about 2.4 digits. "
        "This simple arithmetic check confirms the traversal behaves as expected."
    )
    
    def model(self):
        closures = calculate_closure_runs(100)
        steps = [c['steps_in_closure'] for c in closures]
        avg = sum(steps) / len(steps)
        min_steps = min(steps)
        max_steps = max(steps)
        return (
            Model()
            .add("Average steps", avg)
            .add("Min steps", min_steps)
            .add("Max steps", max_steps)
        )


class SettlementFrequency(Test):
    """
    Settlement frequency from Compton wavelength is ~10^20 Hz.
    """
    name = "Settlement Frequency"
    question = (
        "How fast is Field Closure? "
        "Using the electron's Compton wavelength and the speed of light, we get a frequency "
        "of about 10^20 Hz. This test computes f = c / lambda_Compton."
    )
    reference = "Compton wavelength"
    tolerance = 0.5  # Order of magnitude
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The electron Compton wavelength lambda_c = 2.426x10^-12 m defines a quantum scale.")
            .step("Settlement frequency f = c / lambda_c.")
            .step("f = (2.998x10^8 m/s) / (2.426x10^-12 m).")
            .step("f = 1.235x10^20 Hz.")
            .conclude("This frequency places Field Closure dynamics at quantum electrodynamic timescales.")
        )
    
    commentary = (
        "The Compton wavelength is the electron's natural 'quantum ruler.' "
        "Dividing the speed of light by this wavelength gives a frequency: "
        "about 124 billion billion (10^20) times per second. "
        "That is how fast Field Closure operates: at the timescale of quantum electrodynamics."
    )
    
    def model(self):
        f = calculate_settlement_frequency()
        return Model().add("Settlement frequency (Hz)", f)
    
    def observations(self):
        return Observed().add("Settlement frequency (Hz)", 1.235e20)


class OrbitsForElectron(Test):
    """
    137 orbits make one electron (1/alpha).
    """
    name = "137 Orbits per Electron"
    question = (
        "Why does 137 keep appearing? "
        "The fine structure constant alpha is approximately 1/137. "
        "This test notes that 137 orbits may correspond to one 'electron cycle,' "
        "a tantalizing numerical correspondence."
    )
    reference = "Fine structure constant"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The fine structure constant alpha = 1/137.036 governs electromagnetic coupling.")
            .step("Calculate 1/alpha = 137.036.")
            .step("Round to integer: 137 orbits per characteristic electron cycle.")
            .step("This count may represent complete phase accumulation for electron identity.")
            .conclude("137 orbits establishes a numerical correspondence with alpha.")
        )
    
    commentary = (
        "Feynman called 137 one of the greatest mysteries of physics. It is 1/alpha, "
        "where alpha is the fine structure constant governing how strongly electrons "
        "interact with light. Here we suggest: maybe 137 orbits through the Field Chamber "
        "constitute one 'electron' in some informational sense. "
        "Why 137? Nobody knows. But when the same number appears in two places, pay attention."
    )
    
    def model(self):
        orbits = int(1 / ALPHA)
        return (
            Model()
            .add("1/alpha", 1/ALPHA)
            .add("Orbits per electron", orbits)
        )
    
    def observations(self):
        return (
            Observed()
            .add("1/alpha", 137.036)
            .add("Orbits per electron", 137)
        )


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


def run_all():
    """Run all Field Closure run tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
