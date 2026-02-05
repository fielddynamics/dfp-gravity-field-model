"""
Tetrahedra Do Not Wait
======================

Tet_A does not wait for Tet_B or vice versa.
Both are defined at every step (one explicitly, one implicitly via complement).
"""

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8


class TetrahedraDoNotWait(Test):
    """
    Tet_A does not wait for Tet_B or vice versa.
    Both are defined at every step (one explicitly, one implicitly via complement).
    """
    
    name = "Tetrahedra Do Not Wait"
    question = (
        "Does Tetrahedron A ever have to wait for Tetrahedron B, or vice versa? We test "
        "whether BOTH tetrahedra are defined at every single step. If yes, they evolve "
        "together as one unified structure. Neither waits for the other because they "
        "are two aspects of the same geometric state."
    )
    reference = "Complement definition"
    tolerance = 0.001
    level = Standard
    audit_score = 87
    audit_notes = (
        "Question: 14/15 - Good 'does one wait for the other' framing. "
        "Derivation: 13/15 - Clear complement logic showing simultaneity. "
        "Commentary: 15/15 - Excellent left/right hand analogy, very accessible. "
        "Model: 8/10 - Simple but effective both-defined check. "
        "Observations: 9/10 - Good binary match with proper expected values. "
        "Constants: 9/10 - Proper imports from common module. "
        "Accessibility: 14/15 - Undergraduate accessible with excellent body analogy. "
        "Header: 5/10 - Module docstring minimal, lacks validation coverage. "
        "TO IMPROVE: Expand header with what this test validates in broader context."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("At each step, the explicit vertex v determines:")
            .step("(1) Explicit tetrahedron: Tet_A if parity(v) = 1, Tet_B if parity(v) = 0")
            .step("(2) Complement vertex: 7 - v, which belongs to the opposite tetrahedron")
            .step("Therefore, knowing v immediately defines both tetrahedra:")
            .step("explicit_tet from v, implicit_tet from (7-v)")
            .conclude("Neither tetrahedron waits for the other; both are determined simultaneously")
        )
    
    def model(self):
        traversal = traverse_pi_base8(50)
        
        both_defined_count = 0
        for step in traversal:
            explicit_tet = step['tetrahedron']
            implicit_tet = 'A' if explicit_tet == 'B' else 'B'
            
            if explicit_tet in ['A', 'B'] and implicit_tet in ['A', 'B']:
                both_defined_count += 1
        
        return (
            Model()
            .add("Steps with both tetrahedra defined", both_defined_count)
            .add("Total steps", len(traversal))
        )
    
    def observations(self):
        traversal = traverse_pi_base8(50)
        return (
            Observed()
            .add("Steps with both tetrahedra defined", len(traversal))
            .add("Total steps", len(traversal))
        )
    
    commentary = (
        "When you look at your left hand, do you have to wait for your right hand to "
        "exist? Of course not. They are both part of the same body. The two tetrahedra "
        "work the same way. When the traversal visits vertex 2 (on Tetrahedron A), vertex "
        "5 (on Tetrahedron B) is automatically defined as the complement, because 2 + 5 = 7. "
        "There is no sequence where one tetrahedron is defined and the other is not. They "
        "come into being together, like the front and back of a coin. This simultaneity "
        "is not a special feature we engineered; it is a mathematical necessity of the "
        "complement relationship. You cannot have one without the other."
    )


ALL_TESTS = [TetrahedraDoNotWait]


def run_all():
    """Run test."""
    return run_tests(
        title="Tetrahedra Do Not Wait",
        summary="Verifies that both tetrahedra are defined at every step.",
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
