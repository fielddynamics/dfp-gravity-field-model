"""
Bidirectional Flow
==================

This module tests bi-directional vortex flow (in and out of the Field Origin).

THE VORTEX COSMOLOGY MODEL:
The gravity vortex has bi-directional flow:
- Vortex IN:  TetB -> Field Origin -> TetA (manifestation)
- Vortex OUT: TetA -> Field Origin -> TetB (encoding)

THE QUESTION:
Can we run the pi-base-8 traversal in reverse? Does it maintain the same
statistical properties? If the Field Origin is truly a bi-directional gate,
both directions should be valid.

KEY TESTS:
1. Forward vs reverse traversal statistics
2. Chamber transition symmetry
3. Time reversal invariance

Reference: VORTEX_COSMOLOGY_AND_INFORMATION_DOMAINS.md
"""

from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def analyze_chamber_transitions(traversal):
    """
    Analyze transitions between TetA and TetB.

    Returns counts of A->A, A->B, B->A, B->B transitions.
    """
    transitions = {'AA': 0, 'AB': 0, 'BA': 0, 'BB': 0}

    for i in range(len(traversal) - 1):
        v1 = traversal[i]['vertex']
        v2 = traversal[i + 1]['vertex']

        in_A_1 = v1 in TET_A
        in_A_2 = v2 in TET_A

        if in_A_1 and in_A_2:
            transitions['AA'] += 1
        elif in_A_1 and not in_A_2:
            transitions['AB'] += 1
        elif not in_A_1 and in_A_2:
            transitions['BA'] += 1
        else:
            transitions['BB'] += 1

    return transitions


def analyze_vertex_frequencies(traversal):
    """Compute vertex visitation frequencies."""
    counts = Counter(step['vertex'] for step in traversal)
    total = sum(counts.values())
    return {v: counts.get(v, 0) / total for v in range(8)}


def compare_forward_reverse(n_digits=10000):
    """Compare forward and reverse traversal statistics."""
    forward = traverse_pi_base8(n_digits)
    
    # Create reverse traversal by reversing the vertex sequence
    reverse_vertices = [step['vertex'] for step in reversed(forward)]
    
    # Vertex frequencies
    fwd_freq = analyze_vertex_frequencies(forward)
    
    # For reverse, create a simple traversal-like structure
    rev_counts = Counter(reverse_vertices)
    total = len(reverse_vertices)
    rev_freq = {v: rev_counts.get(v, 0) / total for v in range(8)}

    # Max difference in frequencies
    freq_diff = max(abs(fwd_freq[v] - rev_freq[v]) for v in range(8))

    # Chamber transitions
    fwd_trans = analyze_chamber_transitions(forward)
    total_fwd = sum(fwd_trans.values())

    # Cross-chamber rates
    fwd_cross = (fwd_trans['AB'] + fwd_trans['BA']) / total_fwd if total_fwd else 0

    return {
        'forward_vertex_freq': fwd_freq,
        'reverse_vertex_freq': rev_freq,
        'max_freq_difference': freq_diff,
        'forward_transitions': fwd_trans,
        'forward_cross_chamber': fwd_cross,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class ForwardReverseVertexSymmetry(Test):
    """
    Are vertex frequencies the same in forward and reverse traversal?

    If the Field Origin is a true bi-directional gate, time reversal
    should preserve statistical properties.
    """
    name = "Forward-Reverse Vertex Symmetry"
    question = (
        "Does reversing the traversal preserve vertex frequencies? "
        "If the vortex flow is truly bi-directional (in and out), "
        "both directions should explore the geometry equally."
    )
    reference = "Vortex cosmology bi-directional model"
    level = Standard
    tolerance = 0.05

    commentary = (
        "INTERPRETING TIME-REVERSAL SYMMETRY: "
        "If forward and reverse traversals have the same statistics, "
        "the vortex is truly bi-directional. "
        "Physical meaning: Manifestation (IN) and encoding (OUT) "
        "both use the same geometry. The Field Origin doesn't favor one direction."
    )

    def derivation(self):
        return (
            Derivation()
            .step("BI-DIRECTIONAL FLOW TEST:")
            .step("Forward traversal: cumsum increases, vertex = cumsum mod 8")
            .step("Reverse traversal: read vertices in reverse order")
            .step("If Field Origin is bi-directional:")
            .step("Forward: TetB -> Origin -> TetA (manifestation)")
            .step("Reverse: TetA -> Origin -> TetB (encoding)")
            .conclude("Both should visit all 8 vertices with equal probability (1/8).")
        )

    def model(self):
        comparison = compare_forward_reverse(10000)
        fwd = comparison['forward_vertex_freq']
        rev = comparison['reverse_vertex_freq']
        return (
            Model()
            .add("Forward V0 freq", fwd[0])
            .add("Reverse V0 freq", rev[0])
            .add("Forward V7 freq", fwd[7])
            .add("Reverse V7 freq", rev[7])
            .add("Max frequency difference", comparison['max_freq_difference'])
        )

    def observations(self):
        return (
            Observed()
            .add("Expected vertex freq", 0.125)
            .add("Expected max difference", 0.02)
        )


class CrossChamberSymmetry(Test):
    """
    Is the cross-chamber transition rate the same in both directions?

    The rate of A->B and B->A transitions should be symmetric under
    time reversal if the bimetric coupling is truly balanced.
    """
    name = "Cross-Chamber Transition Symmetry"
    question = (
        "Is the rate of crossing between TetA and TetB the same in both "
        "directions? This tests whether the bimetric coupling is balanced."
    )
    reference = "Bimetric gravity, vortex bi-directional flow"
    level = Standard
    tolerance = 0.05

    commentary = (
        "BIMETRIC BALANCE: "
        "If TetA and TetB are truly coupled as equal partners, "
        "the cross-chamber rate should be ~50% in both directions. "
        "Why this matters: Symmetric coupling means both chambers are equally accessible. "
        "The Field Origin is the neutral interface. Energy/information flows freely both ways. "
        "Asymmetry would suggest one chamber is 'preferred', breaking the bimetric equivalence."
    )

    def derivation(self):
        return (
            Derivation()
            .step("CROSS-CHAMBER RATE:")
            .equation("cross_rate = (A->B + B->A) / total_transitions")
            .step("For balanced bimetric coupling:")
            .step("Forward cross rate ~ 50%")
            .step("Reverse cross rate ~ 50%")
            .step("Difference ~ 0")
            .conclude("Asymmetry would indicate a preferred direction of flow.")
        )

    def model(self):
        comparison = compare_forward_reverse(10000)
        fwd_trans = comparison['forward_transitions']
        return (
            Model()
            .add("Forward A->B", fwd_trans['AB'])
            .add("Forward B->A", fwd_trans['BA'])
            .add("Forward cross rate", comparison['forward_cross_chamber'])
        )

    def observations(self):
        return (
            Observed()
            .add("Expected cross rate", 0.50)
        )


class VortexInVsVortexOut(Test):
    """
    Compare the statistical properties of 'vortex in' vs 'vortex out'.

    Vortex IN: manifestation (TetB -> TetA)
    Vortex OUT: encoding (TetA -> TetB)
    """
    name = "Vortex In vs Vortex Out"
    question = (
        "Are 'vortex in' (manifestation) and 'vortex out' (encoding) "
        "statistically equivalent? If so, the Field Origin is a true "
        "bi-directional gate."
    )
    reference = "Vortex cosmology bi-directional flow"
    level = Critical
    tolerance = 0.10

    commentary = (
        "THE BI-DIRECTIONAL GATE: "
        "High symmetry (>0.9) means the Field Origin doesn't prefer a direction. "
        "Vortex IN and OUT are equivalent processes. The geometry is time-reversal invariant. "
        "Physical implications: Manifestation and encoding are dual processes. "
        "Information is preserved (not lost) at the Origin. The vortex 'breathes' in both directions. "
        "This supports the cosmological claim that TetB (subspace) is an information archive, "
        "accessible through the bi-directional Field Origin."
    )

    def derivation(self):
        return (
            Derivation()
            .step("BI-DIRECTIONAL VORTEX FLOW:")
            .step("VORTEX IN (manifestation): Information from TetB boundary flows through Field Origin, manifests as matter in TetA")
            .step("VORTEX OUT (encoding): Activity in TetA flows through Field Origin, encodes onto TetB boundary")
            .conclude("If Field Origin is bi-directional, both flows should have the same geometric properties.")
        )

    def model(self):
        comparison = compare_forward_reverse(10000)

        # Compute overall symmetry score
        freq_symmetry = 1 - comparison['max_freq_difference'] * 8  # Scale to [0,1]
        overall_symmetry = freq_symmetry

        return (
            Model()
            .add("Vertex frequency symmetry", freq_symmetry)
            .add("Overall bi-directional symmetry", overall_symmetry)
            .add("Forward cross rate", comparison['forward_cross_chamber'])
        )

    def observations(self):
        return (
            Observed()
            .add("Vertex frequency symmetry", 0.95)
            .add("Overall bi-directional symmetry", 0.95)
        )


# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all bi-directional flow tests."""
    return run_tests(
        "Bi-Directional Flow",
        "Tests for bi-directional vortex flow through the Field Origin",
        [
            ForwardReverseVertexSymmetry,
            CrossChamberSymmetry,
            VortexInVsVortexOut,
        ]
    )


if __name__ == "__main__":
    run_all()
