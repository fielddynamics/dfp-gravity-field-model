"""
Causality Preserved
===================

Causality is preserved even though there is no communication.
Each step depends only on the PREVIOUS cumsum, not on signals from
other parts of the structure.
"""

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8


class CausalityPreserved(Test):
    """
    Causality is preserved even though there is no communication.
    Each step depends only on the PREVIOUS cumsum, not on signals from
    other parts of the structure.
    """
    
    name = "Causality Preserved Without Communication"
    question = (
        "Why can two tetrahedra stay perfectly correlated without sending signals to "
        "each other? Because each step depends ONLY on the previous cumulative sum "
        "and the current digit. We test whether every step follows this local rule, "
        "proving that causality is preserved through shared arithmetic, not communication."
    )
    reference = "Cumulative sum definition"
    tolerance = 0.001
    level = Critical  # Foundational to the model
    audit_score = 85
    audit_notes = (
        "Question: 14/15 - Excellent 'Why can two tetrahedra stay correlated' hook. "
        "Derivation: 13/15 - Clear steps but could build more intuition before math. "
        "Commentary: 15/15 - Outstanding dancer analogy connecting to entanglement. "
        "Model: 8/10 - Simple counts but effective for invariant check. "
        "Observations: 8/10 - Binary check appropriate but dynamic computation less traceable. "
        "Constants: 8/10 - Imports from common, but uses only 50 pi digits (marginal for claims). "
        "Accessibility: 14/15 - Undergraduate can follow, excellent analogies. "
        "Header: 5/10 - Module docstring minimal, lacks coverage/limitations. "
        "SAMPLE SIZE: Uses 50 digits, marginal for statistical claims but OK for invariant. "
        "TO IMPROVE: Expand module header with validation goals and coverage assessment."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("State update rule: cumsum_n = cumsum_{n-1} + digit_n")
            .step("Current state depends only on: (1) previous cumsum, (2) current digit")
            .step("No information from other vertices is required or transmitted")
            .equation("expected_cumsum = prev_cumsum + digit")
            .step("If this holds for all steps, the system is causally consistent")
            .conclude("Correlation between vertices arises from shared arithmetic, not communication")
        )
    
    def model(self):
        traversal = traverse_pi_base8(50)
        
        causal_count = 0
        prev_cumsum = 0
        
        for step in traversal:
            digit = step['digit']
            cumsum = step['cumsum']
            expected_cumsum = prev_cumsum + digit
            
            if cumsum == expected_cumsum:
                causal_count += 1
            
            prev_cumsum = cumsum
        
        return (
            Model()
            .add("Causally consistent steps", causal_count)
            .add("Total steps", len(traversal))
        )
    
    def observations(self):
        traversal = traverse_pi_base8(50)
        return (
            Observed()
            .add("Causally consistent steps", len(traversal))
            .add("Total steps", len(traversal))
        )
    
    commentary = (
        "Here is the beautiful thing: imagine two dancers on opposite sides of a stage, "
        "moving in perfect synchrony. You might think they must be watching each other "
        "or receiving signals. But no! They are both following the same choreography "
        "written in the digits of pi. Each dancer only needs to know their previous "
        "position and the next instruction. The correlation emerges from shared rules, "
        "not from any communication between them. This is exactly how quantum entanglement "
        "works too. When you measure one entangled particle, you instantly know about "
        "its partner, not because a signal traveled between them, but because they share "
        "the same underlying arithmetic. Causality is preserved because nothing needs "
        "to travel faster than light. The correlations were baked in from the start."
    )


ALL_TESTS = [CausalityPreserved]


def run_all():
    """Run all tests in this module."""
    return run_tests(
        title="Causality Preserved",
        summary="Verifies that causality is preserved without inter-vertex communication.",
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
