"""
Closure Simultaneity
====================

These tests examine the timing characteristics of the traversal algorithm.
The vertex index (0-7) is a 3-bit number that fully specifies the system
state at each step. The tests analyze step duration at the Compton frequency
scale versus light-crossing time for the structure.

This file imports tests from individual modules for combined execution.
Each test also exists in its own file for easier maintenance.
"""

from gfd_model_v2.framework import *

# Import individual tests from their modules
from gfd_model_v2.engine_core.timing_analysis.test_single_value_encodes_state import SingleValueEncodesState
from gfd_model_v2.engine_core.timing_analysis.test_no_intermediate_states import NoIntermediateStates
from gfd_model_v2.engine_core.timing_analysis.test_step_duration_vs_light_crossing import StepDurationVsLightCrossing
from gfd_model_v2.engine_core.timing_analysis.test_closure_instantaneous import ClosureIsInstantaneous
from gfd_model_v2.engine_core.timing_analysis.test_orbit_boundary_crossing import OrbitBoundaryCrossingDiscrete
from gfd_model_v2.engine_core.timing_analysis.test_causality_preserved import CausalityPreserved
from gfd_model_v2.engine_core.timing_analysis.test_face_reads_accumulate import FaceReadsAccumulate
from gfd_model_v2.engine_core.timing_analysis.test_tetrahedra_do_not_wait import TetrahedraDoNotWait
from gfd_model_v2.engine_core.timing_analysis.test_time_face_simultaneity import TimeFaceSimultaneity
from gfd_model_v2.engine_core.timing_analysis.test_quantum_nonlocality_analogy import QuantumNonlocalityAnalogy
from gfd_model_v2.engine_core.timing_analysis.test_simultaneity_proof import SimultaneityProof


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    SingleValueEncodesState,
    NoIntermediateStates,
    StepDurationVsLightCrossing,
    ClosureIsInstantaneous,
    OrbitBoundaryCrossingDiscrete,
    CausalityPreserved,
    FaceReadsAccumulate,
    TetrahedraDoNotWait,
    TimeFaceSimultaneity,
    QuantumNonlocalityAnalogy,
    SimultaneityProof,
]


def run_all():
    """Run all closure simultaneity tests."""
    return run_tests(
        title="Closure Timing Analysis",
        summary=(
            "These tests examine timing properties of the traversal algorithm. The vertex "
            "index (0-7) is a 3-bit value that fully encodes each state, with no intermediate "
            "values between steps. At Compton frequency (~10^20 Hz), light-crossing time "
            "approaches step duration. The tests document these timing relationships and "
            "the discrete nature of state transitions without asserting physical causation."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
