"""
Step Duration vs Light Crossing
===============================

Compare step duration to light-crossing time.
If step_duration is comparable to crossing time, sequential is impossible.
"""

import math
from gfd_model_v2.framework import *
from gfd_model_v2.common import C


def calculate_step_duration():
    """Calculate the duration of a single traversal step."""
    lambda_c = 2.426310238e-12  # Compton wavelength (meters)
    freq = C / lambda_c  # ~1.24 x 10^20 Hz
    step_period = 1 / freq  # ~8 x 10^-21 seconds
    return step_period


def calculate_light_crossing_time():
    """Time for light to cross the structure at Compton scale."""
    lambda_c = 2.426310238e-12  # Compton wavelength (meters)
    crossing_distance = lambda_c * 2 * math.sqrt(3)  # diagonal across cube
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
