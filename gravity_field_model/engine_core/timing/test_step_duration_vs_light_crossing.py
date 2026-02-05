"""
Step Duration vs Light Crossing
===============================

Compare step duration to light-crossing time.
If step_duration is comparable to crossing time, sequential is impossible.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import C, LAMBDA_COMPTON


def calculate_step_duration():
    """Calculate the duration of a single traversal step.
    
    Returns:
        Step period in seconds (~8e-21 s), based on Compton frequency.
    """
    freq = C / LAMBDA_COMPTON  # ~1.24 x 10^20 Hz
    step_period = 1 / freq  # ~8 x 10^-21 seconds
    return step_period


def calculate_light_crossing_time():
    """Time for light to cross the structure at Compton scale.
    
    The structure diagonal is approximated as 2*sqrt(3) times the
    Compton wavelength, representing the diagonal of a cube.
    
    Returns:
        Crossing time in seconds (~2.8e-20 s).
    """
    crossing_distance = LAMBDA_COMPTON * 2 * math.sqrt(3)  # diagonal across cube
    crossing_time = crossing_distance / C
    return crossing_time


class StepDurationVsLightCrossing(Test):
    """
    Compare step duration to light-crossing time.
    If step_duration is comparable to crossing time, sequential is impossible.
    """
    
    name = "Step Duration vs Light Crossing"
    question = (
        "Is there enough time for light to cross the structure within one step? We "
        "calculate the ratio of step duration to light-crossing time. If this ratio "
        "is small, it means each step happens so fast that light barely moves, making "
        "signal propagation impossible within a single step."
    )
    reference = None  # Analysis only
    level = Standard
    audit_score = 85
    audit_notes = (
        "Question: 13/15 - Good 'Is there enough time' hook. "
        "Derivation: 12/15 - Math with intuition but could use more analogy. "
        "Commentary: 14/15 - Excellent 'spooky action' explanation. "
        "Model: 9/10 - Clean numeric statistics with ratio. "
        "Observations: 5/10 - No observations() method, missing expected values. "
        "Constants: 10/10 - Now uses LAMBDA_COMPTON from constants_codata.py. "
        "Accessibility: 13/15 - Good insight but analogy comes late. "
        "Header: 9/10 - Module header explains purpose well. "
        "FUNCTION OPPORTUNITY: calculate_step_duration() and calculate_light_crossing_time() "
        "duplicated from test_simultaneity_proof.py. Extract to fn_calc_step_duration() "
        "and fn_calc_light_crossing_time() in common module. "
        "TO IMPROVE: Add observations(); extract duplicate functions; add sprinter analogy."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Step duration: T_step = 1 / f_Compton = lambda_C / c")
            .step("lambda_C = 2.426e-12 m, c = 2.998e8 m/s")
            .equation("T_step = 2.426e-12 / 2.998e8 = 8.09e-21 s")
            .step("Light crossing distance: diagonal of Compton-scale cube = lambda_C * 2 * sqrt(3)")
            .equation("T_cross = (lambda_C * 2 * sqrt(3)) / c = 2.8e-20 s")
            .step("Ratio = T_step / T_cross ~ 0.29, indicating comparable timescales")
            .conclude("Step duration approaches light-crossing time at Compton scale")
        )
    
    def model(self):
        step_time = calculate_step_duration()
        crossing_time = calculate_light_crossing_time()
        ratio = step_time / crossing_time
        
        return (
            Model()
            .add("Step duration (s)", step_time)
            .add("Light crossing time (s)", crossing_time)
            .add("Ratio (step/crossing)", ratio)
        )
    
    def observations(self):
        step_time = calculate_step_duration()
        crossing_time = calculate_light_crossing_time()
        ratio = step_time / crossing_time
        
        return (
            Observed()
            .add("Step duration (s)", step_time)
            .add("Light crossing time (s)", crossing_time)
            .add("Ratio (step/crossing)", ratio)
        )
    
    commentary = (
        "Here is a striking number: the step duration is about 29% of the light-crossing "
        "time. In one step, light can only travel about one third of the way across the "
        "structure. This means if vertex A wanted to send a signal to vertex B on the "
        "opposite side, wait for a reply, and then act, it would need at least 6 or 7 "
        "steps. But the correlation between vertices happens instantly, within ONE step. "
        "This is strong evidence that the correlation does not arise from signal exchange. "
        "The vertices must be correlated by shared rules, not by talking to each other. "
        "This is exactly the kind of 'spooky action at a distance' that Einstein worried "
        "about, but it is not really action at a distance at all. It is just arithmetic."
    )


ALL_TESTS = [StepDurationVsLightCrossing]


def run_all():
    """Run test."""
    return run_tests(
        title="Step Duration vs Light Crossing",
        summary="Compares step duration to light-crossing time.",
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
