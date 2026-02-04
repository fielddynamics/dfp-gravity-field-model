"""
No Intermediate States
======================

Between steps, there are NO intermediate states.
The system is always in a definite vertex state (0-7).
"""

from gfd_model_v2.framework import *
from gfd_model_v2.common import traverse_pi_base8


class NoIntermediateStates(Test):
    """
    Between steps, there are NO intermediate states.
    The system is always in a definite vertex state (0-7).
    """
    
    name = "No Intermediate States"
    question = (
        "Why can't the system be 'between' vertices, like vertex 2.5? Because the "
        "vertex is computed as cumsum mod 8, and both operations only produce integers. "
        "We test whether every single step lands on a definite vertex from 0 to 7, "
        "proving that the Field Chamber has no fuzzy or in-between states."
    )
    reference = "State machine definition"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("For each traversal step, the vertex is computed as: vertex = cumsum mod 8")
            .step("Since cumsum is an integer and mod 8 yields integers in [0,7]")
            .step("The vertex is always a definite integer value")
            .step("Traverse N steps and confirm each step['vertex'] is in {0,1,...,7}")
            .conclude("No fractional or intermediate states exist in the discrete lattice model")
        )
    
    def model(self):
        traversal = traverse_pi_base8(50)
        
        definite_count = 0
        for step in traversal:
            vertex = step['vertex']
            if isinstance(vertex, int) and 0 <= vertex <= 7:
                definite_count += 1
        
        return (
            Model()
            .add("Steps with definite vertex", definite_count)
            .add("Total steps", len(traversal))
        )
    
    def observations(self):
        traversal = traverse_pi_base8(50)
        return (
            Observed()
            .add("Steps with definite vertex", len(traversal))
            .add("Total steps", len(traversal))
        )
    
    commentary = (
        "Imagine a clock with only hour marks, no minute hand. You cannot ask 'what time "
        "is it between 3 and 4?' The clock only shows whole hours. The Field Chamber is "
        "like this clock. The vertex is determined by integer arithmetic: add integers, "
        "take remainder when dividing by 8. Both operations can only give you integers. "
        "There is no mathematical pathway to a fractional vertex. This is profound! In "
        "classical physics, things can be anywhere along a continuum. But here, nature "
        "is counting, not measuring. The system clicks from one vertex to another with "
        "nothing in between, just like an electron jumping between energy levels in an "
        "atom. The discreteness is not approximate; it is exact and fundamental."
    )


ALL_TESTS = [NoIntermediateStates]


def run_all():
    """Run test."""
    return run_tests(
        title="No Intermediate States",
        summary="Verifies that the system is always in a definite vertex state.",
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
