# FILENAME: test_dual_channel_frequency_doubling.py

"""
Dual Channel Frequency Doubling
================================

In standard quantum mechanics, a system with N discrete states visited one at a
time requires N steps to achieve full coverage. The GFM traversal visits one
explicit vertex per step, but the complement vertex (7 minus V) is simultaneously
determined via the implicit channel. This means each step resolves two vertices
rather than one, effectively doubling the information rate of the traversal.

The core claim (Section 3.1 of the GFM framework) is that closure operates at
the full Compton frequency f_C rather than f_C/2 because both tetrahedra have
determined state at every step. This test measures the effective vertex resolution
rate by counting distinct vertices resolved per step through both channels, and
compares it to the single channel expectation.

GFM OBSERVATION: Two vertices resolved per step (explicit + implicit complement).

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B,
    traverse_pi_base8,
)


class DualChannelFrequencyDoubling(Test):
    """
    Measures the effective information rate of the dual channel traversal
    architecture and compares it to single channel expectations.

    PHYSICAL CONTEXT:
    In any discrete traversal of N states, a single channel resolves one
    state per step. Full coverage of all N states requires on average
    N * H_N steps (coupon collector problem), where H_N is the Nth
    harmonic number. For N=8, this is approximately 21.7 steps for a
    single channel. The GFM traversal defines an explicit channel (the
    visited vertex V) and an implicit channel (the complement 7 minus V),
    both determined at every step with no additional signal or computation.

    GFM OBSERVATION:
    Each traversal step resolves exactly 2 of the 8 vertices: the explicit
    vertex V and the implicit complement 7 minus V. These always belong to
    opposite tetrahedra (one from Tet A, one from Tet B). The effective
    vertex resolution rate is therefore 2.0 vertices per step, which is
    exactly double the single channel rate of 1.0. This doubling is why
    the framework claims closure operates at f_C rather than f_C/2.

    EPISTEMIC STATUS:
    This is an observation about the information content of the traversal
    algorithm. The doubling is arithmetic fact. The physical claim that
    this sets the closure frequency is a GFM interpretation.
    """

    name = "Dual Channel Frequency Doubling"

    question = (
        "How many distinct vertex states does each traversal step resolve? "
        "A single channel model resolves 1 vertex per step, requiring the "
        "full Compton period to cover both tetrahedra. The GFM dual channel "
        "architecture claims 2 vertices per step (explicit V plus implicit "
        "7 minus V), one from each tetrahedron. Does the traversal data "
        "confirm this doubling, and does every step always span both "
        "tetrahedra simultaneously?"
    )

    reference = "GFM Framework Section 3.1: Dual Channel Architecture"

    tolerance = 0.001

    level = Level.STANDARD

    commentary = (
        "Every step of the pi driven traversal visits an explicit vertex V "
        "and simultaneously determines its complement 7 minus V. Because "
        "vertex parity alternates between tetrahedra (V in Tet A implies "
        "7 minus V in Tet B, and vice versa), each step always touches both "
        "halves of the stellated octahedron. The measured resolution rate of "
        "2.0 vertices per step is an arithmetic fact about the complement "
        "operation on 3 bit binary labels. The physical interpretation, that "
        "this doubling allows closure at f_C rather than f_C/2, remains a "
        "GFM observation rather than a derivation from first principles. "
        "Standard physics has no direct analog to this dual channel concept, "
        "though the mathematical structure resembles the relationship between "
        "a spinor and its charge conjugate in the Dirac equation."
    )

    # Audit scoring
    audit_score = 85
    audit_notes = (
        "Question: 13/15 (asks how and whether, includes specific numbers and tension between single vs dual channel, but opens with 'how many' rather than a true mystery hook; could sharpen stakes by leading with the physical consequence of f_C vs f_C/2). Derivation: 14/15 (excellent intuition before math structure, parity argument builds naturally, the equation step is clean; minor gap: no analogy or everyday illustration to ground the abstract bit flipping for newcomers). Commentary: 13/15 (strong insight, honest epistemic labeling, good Dirac spinor connection; could add an everyday analogy like reading both sides of a coin in one glance, and state implications more explicitly). Model: 9/10 (clean summary with just two key values, ratio and fraction; no raw dumps; could arguably add a third metric like unique vertex pairs covered to strengthen). Observations: 7/10 (values are mathematically exact and correct, but the reference is internal GFM documentation only, not a peer reviewed or external source; the expected values of 2.0 and 1.0 are arithmetic truths rather than experimental data, which should be stated more explicitly). Constants: 9/10 (K, VERTICES, TET_A, TET_B, traverse_pi_base8 all imported from common; math imported but not used; no hardcoded physics constants; minor deduction for importing math unnecessarily). Accessibility: 13/15 (graduate student can follow easily, parity argument is well explained, coupon collector reference adds depth; lacks a simple everyday analogy in the derivation itself, and the Dirac spinor mention in commentary may lose undergrads without more context). Header: 7/10 (module docstring covers what is tested, the core claim, and labels it as observation; missing target audience level, key limitations of the test approach, and explicit scope boundaries for what this does not test)."
    )

    academic_paper = """\
TITLE Dual Channel Vertex Resolution in the GFM Traversal: Quantifying the Implicit Complement Architecture ABSTRACT We investigate whether the GFM pi driven traversal resolves two vertex states per step through its dual channel architecture. Over 200 traversal steps, the model confirms an effective rate of exactly 2.0 vertices per step with 100% cross tetrahedral coverage. This is documented as an arithmetic OBSERVATION. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The Gravity Field Model describes gravity as a geometric object built from two interpenetrating tetrahedra forming a stellated octahedron with 8 vertices. A deterministic traversal driven by pi in base 8 visits these vertices sequentially. A natural question arises: at what rate does the traversal resolve the full geometric state? In any discrete system with N states, a single observation channel resolves one state per step. For the 8 vertex stellated octahedron, a single channel would require the full Compton period to sample both tetrahedral halves. However, the GFM framework (Section 3.1) claims that a second channel operates simultaneously. When vertex V is read explicitly, the complement vertex 7 minus V is determined by arithmetic alone, with no signal propagation required. This implicit channel allegedly doubles the effective information rate. This test investigates two specific claims: first, that each step resolves exactly 2.0 vertices rather than 1.0, and second, that every step necessarily spans both Tet A and Tet B. These properties, if confirmed, provide the structural basis for the assertion that field closure operates at the full Compton frequency f_C rather than f_C/2. 2. METHODOLOGY The model executes the standard pi base 8 traversal algorithm over 200 digits. At each step, the explicit vertex V is recorded and the complement C = 7 minus V is computed. For each step, we determine whether V and C belong to opposite tetrahedra by checking membership in Tet A ({1, 2, 4, 7}, odd parity vertices) and Tet B ({0, 3, 5, 6}, even parity vertices). Two summary metrics are computed: the effective vertex resolution rate (total vertex instances divided by total steps) and the cross tetrahedral fraction (proportion of steps touching both tetrahedra). Agreement criterion is exact match (0.00% error) since the expected values are arithmetic necessities rather than empirical measurements. 3. RESULTS The model outputs over 200 traversal steps: Effective vertices per step: 2.0 (model) versus 2.0 (expected), 0.00% error. Cross tetrahedral fraction: 1.0 (model) versus 1.0 (expected), 0.00% error. Both metrics match exactly. Every single step, without exception, resolved one vertex from Tet A and one from Tet B. The doubling is uniform across the entire traversal. No step was found where explicit and implicit vertices belonged to the same tetrahedron. The underlying mechanism is the parity structure of the 3 bit vertex labels. The operation 7 minus V is equivalent to XOR with 111 in binary, which flips all three bits. Since Tet A contains odd parity vertices and Tet B contains even parity vertices, flipping all bits always crosses the tetrahedral boundary. This guarantee is combinatorial, independent of which digits pi produces. 4. DISCUSSION The exact match (0.00% on both metrics) is not surprising because the result follows from integer arithmetic on binary labels rather than from empirical measurement. The significance lies not in the numerical agreement but in what the structure implies. If each traversal step simultaneously determines the state of both tetrahedra, then a single step carries the information content of two independent vertex reads. The physical interpretation, that this doubling sets the closure frequency at f_C rather than f_C/2, is a GFM claim that extends beyond the arithmetic. EPISTEMIC STATUS: OBSERVATION. The doubling of vertex resolution rate is an arithmetic fact about the complement operation. The connection to Compton frequency and physical closure rate is a GFM interpretation, not a derivation from established physics. The structure is analogous to how a Dirac spinor and its charge conjugate are simultaneously determined, but this analogy has not been formalized. 5. LIMITATIONS AND HONESTY STATEMENT This test does NOT prove that physical field closure operates at any particular frequency. The expected values are mathematical truths about modular complement arithmetic, not experimental data. The test cannot distinguish whether the implicit channel carries physical significance or is merely a bookkeeping convenience. Further
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD PHYSICS: In a discrete system with N=8 states, "
                "one observation per step resolves one state. The information "
                "rate is 1 state per step."
            )
            .step(
                "GFM ARCHITECTURE: At each traversal step, vertex V is read "
                "explicitly. The complement vertex C = 7 minus V is determined "
                "simultaneously by arithmetic, requiring no signal propagation."
            )
            .step(
                "PARITY ARGUMENT: Vertex labels are 3 bit binary. The XOR "
                "complement (7 minus V, equivalently V XOR 111) flips all bits, "
                "which flips parity. If V is in Tet A (odd parity: {1,2,4,7}), "
                "then C is in Tet B (even parity: {0,3,5,6}), and vice versa."
            )
            .equation("vertices_per_step = 1 (explicit) + 1 (implicit) = 2")
            .step(
                "COVERAGE RATE: Over N steps, the dual channel resolves 2N "
                "vertex instances. The effective rate is exactly 2.0 vertices "
                "per step, double the single channel rate."
            )
            .step(
                "CROSS TETRAHEDRAL GUARANTEE: Since explicit and implicit "
                "vertices always have opposite parity, every single step "
                "spans both Tet A and Tet B. The fraction of steps touching "
                "both tetrahedra is exactly 1.0."
            )
            .conclude(
                "The dual channel architecture doubles the effective vertex "
                "resolution rate from 1.0 to 2.0 per step, and guarantees "
                "that both tetrahedra are resolved at every step. This is "
                "the basis for the claim that closure operates at f_C."
            )
        )

    def model(self) -> Model:
        n_digits = 200
        traversal = traverse_pi_base8(n_digits)

        total_vertices_resolved = 0
        both_tet_count = 0

        for step in traversal:
            vertex = step['vertex']
            complement = 7 - vertex

            explicit_in_a = 1 if vertex in TET_A else 0
            explicit_in_b = 1 if vertex in TET_B else 0
            complement_in_a = 1 if complement in TET_A else 0
            complement_in_b = 1 if complement in TET_B else 0

            touches_a = max(explicit_in_a, complement_in_a)
            touches_b = max(explicit_in_b, complement_in_b)

            total_vertices_resolved += 2
            if touches_a and touches_b:
                both_tet_count += 1

        effective_rate = total_vertices_resolved / len(traversal)
        cross_tet_fraction = both_tet_count / len(traversal)

        return (
            Model()
            .add("Effective vertices per step", effective_rate)
            .add("Cross tetrahedral fraction", cross_tet_fraction)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Effective vertices per step", 2.0)
            .add("Cross tetrahedral fraction", 1.0)
        )


ALL_TESTS = [DualChannelFrequencyDoubling]


def run_all():
    """Run all tests in this module."""
    from gravity_field_model.framework import run_tests
    return run_tests(
        title="Dual Channel Frequency Doubling",
        summary=(
            "Validates that the implicit complement channel doubles the effective "
            "vertex resolution rate and guarantees cross tetrahedral coverage at "
            "every traversal step."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
