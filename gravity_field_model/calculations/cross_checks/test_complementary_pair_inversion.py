# FILENAME: test_complementary_pair_inversion.py

"""
Complementary Pair Inversion Across Field Chambers
===================================================

The GFD model claims that the two interlocking tetrahedra (TET_A and TET_B)
of the stellated octahedron are connected through complementary pairs: for
every vertex v in one tetrahedron, its bitwise complement (v XOR 7) resides
in the opposite tetrahedron. This is the dynamical bridge between the two
Field Chambers. Standard combinatorics tells us that XOR with 111 in binary
flips all three bits, which necessarily flips the popcount parity. Since
parity determines tetrahedron membership, inversion must cross chambers.

The question is whether this property holds for ALL 8 vertices, confirming
that every Coupling Port has exactly one complementary partner in the
opposite chamber. This is the coupling topology that the bimetric structure
requires for information exchange between the two independent metrics.

GFD OBSERVATION: All 8 complementary pairs (v, v XOR 7) cross between TET_A and TET_B.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, TET_A, TET_B,
)


class ComplementaryPairInversionCrossesChambers(Test):
    """
    PHYSICAL CONTEXT:
    In bimetric gravity, two independent metric sectors must exchange
    information through a well defined coupling topology. The GFD model
    realizes this through the stellated octahedron (Merkaba), where
    each vertex v is paired with its bitwise complement v XOR 7. This
    complement operation flips all d=3 bits of the binary label,
    geometrically mapping a cube vertex to its body diagonal opposite.
    The partition tests confirm TET_A and TET_B are disjoint and
    exhaustive. The parity test confirms membership is determined by
    popcount mod 2. This test verifies the consequence that binds
    those results together: inversion always crosses chambers.

    GFD OBSERVATION:
    For all 8 vertices of the stellated octahedron, the complementary
    pair operation (v XOR 7, equivalently v XOR (2^d minus 1)) maps
    TET_A vertices to TET_B and TET_B vertices to TET_A. The number
    of correctly crossing pairs equals 2*K = 8, with zero violations.
    This is the coupling topology that enables dual metric exchange.

    EPISTEMIC STATUS:
    This is a structural validation of the model's geometric definitions.
    Given that parity determines membership and XOR 7 flips parity,
    the result follows by elementary logic. The value of the test is
    confirming that TET_A and TET_B as concretely defined in the
    codebase are consistent with this algebraic requirement. It is a
    cross check between two independent properties (set membership
    and bitwise algebra) rather than a derivation from first principles.
    """

    name = "Complementary Pair Inversion Crosses Chambers"

    question = (
        "Does every vertex's complementary partner live in the opposite "
        "Field Chamber? The bimetric coupling mechanism requires that "
        "v XOR 7 maps TET_A vertices to TET_B and vice versa for all 8 "
        "vertices. If any pair failed to cross, that Coupling Port would "
        "lack a communication channel to the other metric sector, breaking "
        "the dual field exchange. How many of the 8 pairs cross correctly?"
    )

    reference = (
        "GFD Textbook Ch. 9: Complementary pair structure of the stellated "
        "octahedron; Ch. 3: Field closure requires bidirectional information "
        "exchange between chambers"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "This test bridges the static partition property and the dynamic "
        "coupling topology. The partition tests showed TET_A and TET_B are "
        "disjoint and exhaustive. The parity test showed membership follows "
        "popcount mod 2. This test verifies the physical consequence: the "
        "XOR 7 operation (body diagonal inversion on the cube) always sends "
        "a vertex from one chamber to the other. This is an observation about "
        "the consistency of the model's definitions, not a derivation of new "
        "physics. Its value lies in confirming that the algebraic structure "
        "(bitwise complement) and the geometric structure (tetrahedron "
        "membership) are fully aligned, which is necessary for the pi base 8 "
        "traversal algorithm to correctly alternate between Field Chambers."
    )

    # Audit scoring (self-assessed)
    audit_score = 85
    audit_notes = (
        "Question: 13/15 (good physical stakes, explains WHY crossing matters for bimetric coupling, asks a concrete quantitative question, but the mystery hook could be sharper by leading with the tension rather than the mechanism). Derivation: 12/15 (clear logical progression from combinatorics through parity to the crossing check, the key equation is well placed, but intuition building is somewhat thin: jumps into bit flipping without a physical analogy first, and the PHYSICAL SETUP and TENSION phases from the ideal structure are implicit rather than explicit). Commentary: 13/15 (strong connection back to partition and parity tests, honest epistemic labeling as observation not derivation, explains significance for the traversal algorithm, but could benefit from a concrete analogy to make the insight more visceral for undergrads). Model: 9/10 (clean binary summary with exactly two values, crossing count and violation count, easy to interpret at a glance, good use of float conversion). Observations: 7/10 (expected values are mathematically justified and internally consistent, but reference is to GFD Textbook chapters without external authoritative source since this is a purely internal structural check, which limits traceability to independent verification). Constants: 9/10 (K, TET_A, TET_B all imported from common, complement_mask derived from d=3 with inline comment, minor note that d=3 is hardcoded as a literal rather than imported, though it is used only to compute the mask). Accessibility: 12/15 (graduate level accessible, explains XOR and popcount, builds logically from prior tests, but assumes familiarity with bimetric gravity and bitwise operations without grounding analogies, an undergrad without CS background might struggle with the XOR notation). Header: 10/10 (comprehensive module docstring covering physical domain, the specific question being answered, explicit GFD OBSERVATION label, honest epistemic status, clear scope connecting to the partition and parity tests already validated)."
    )

    academic_paper = """\
TITLE Complementary Pair Inversion Across Field Chambers: Verifying the Coupling Topology of the Stellated Octahedron ABSTRACT This investigation verifies whether the bitwise complement operation (v XOR 7) consistently maps vertices from one tetrahedron of the stellated octahedron to the other. The model checks all 8 vertices and finds 8 crossing pairs with zero violations. This is documented as a structural OBSERVATION confirming internal consistency. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The GFD model proposes that gravitational field closure requires a specific geometric structure: two interlocking tetrahedra forming a stellated octahedron, with K=4 coupling channels and d=3 spatial dimensions producing 2K=8 vertices. Prior structural validations have confirmed that the two tetrahedra (TET_A and TET_B) partition these 8 vertices into disjoint, exhaustive sets, and that binary popcount parity determines membership. However, a partition alone is not sufficient for bimetric gravity. The two Field Chambers must also communicate. The GFD model claims this communication occurs through complementary pairs: each vertex v is paired with v XOR 7 (its bitwise complement, equivalently its body diagonal opposite on the cube). For the coupling topology to function, every such pair must cross between chambers. A vertex in TET_A must have its partner in TET_B, and vice versa. Standard combinatorics predicts this must hold because XOR with 7 flips all three bits, reversing popcount parity. But the prediction assumes TET_A and TET_B are defined purely by parity. This test checks whether the concrete set definitions in the codebase satisfy the algebraic requirement. This test specifically investigates whether all 8 complementary pairs cross between chambers, with zero violations. 2. METHODOLOGY The model iterates over all 8 vertices in the set {0, 1, 2, 3, 4, 5, 6, 7}. For each vertex v, it computes the complement partner as v XOR 7, where 7 equals 2^d minus 1 for d=3. It then checks whether v and its partner belong to opposite tetrahedra by testing set membership in TET_A and TET_B as defined in the GFD common constants module. Two summary statistics are recorded: the count of vertices whose partners correctly cross chambers, and the count of violations. Agreement is defined as 8 crossings and 0 violations, with a tolerance of 1 percent. 3. RESULTS Model output: Crossing pair count: 8.0 Violation count: 0.0 Expected values: Crossing pair count: 8.0 Violation count: 0.0 The explicit vertex pairs are: 0 paired with 7 (TET_B to TET_A), 1 paired with 6 (TET_A to TET_B), 2 paired with 5 (TET_A to TET_B), 3 paired with 4 (TET_B to TET_A), and symmetrically in reverse. Every pair crosses chambers. The pattern is complete: no vertex lacks a partner in the opposite tetrahedron. The result holds exactly, not approximately, because it is a property of finite sets under a deterministic operation. 4. DISCUSSION The result confirms that the XOR 7 operation serves as a valid coupling bridge between the two Field Chambers. Geometrically, this means every Coupling Port on one tetrahedron has exactly one communication partner on the other tetrahedron, located at the opposite end of the cube's body diagonal. EPISTEMIC STATUS: OBSERVATION. This is a structural validation of the model's internal definitions. The result follows from elementary combinatorics once parity based membership is assumed. We observe that the concrete TET_A and TET_B sets in the codebase are consistent with this algebraic requirement. This is not a derivation of new physics. This test connects to and extends the partition tests (disjointness and exhaustiveness) and the parity correspondence test. Together, these four validations establish that the stellated octahedron's vertex structure supports partition, parity assignment, and complementary pair coupling as a coherent system. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove that bimetric gravity is correct or that the stellated octahedron is physically realized. It assumes that parity based tetrahedron assignment is the correct scheme, which is itself a GFD postulate. The test validates internal consistency of definitions, not correspondence with experiment. Further work should investigate whether the complementary pair structure produces measurable physical predictions that could distinguish GFD from alternative frameworks. 6. CONCLUSION All 8 complementary pairs under XOR 7 inversion cross between TET_A and TET_B with zero violations. This confirms the coupling topology required for dual metric information exchange in the GFD stellated octahedron. The
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD COMBINATORICS: For a 3 bit binary label v in {0..7},")
            .step("the complement v XOR 7 flips all three bits.")
            .step("If v has popcount p, then v XOR 7 has popcount 3 minus p.")
            .step("Therefore parity(v XOR 7) = parity(3 minus p) = 1 minus parity(p),")
            .step("since 3 minus p and p always have opposite parity.")
            .equation("parity(v XOR 7) = 1 minus parity(v) for all v in {0..7}")
            .step("GFD DEFINITION: TET_A = odd parity vertices = {1, 2, 4, 7}")
            .step("GFD DEFINITION: TET_B = even parity vertices = {0, 3, 5, 6}")
            .step("CHECK: For each vertex v, compute v XOR 7 and verify it")
            .step("belongs to the opposite tetrahedron from v.")
            .step("Count crossing pairs (should be 8) and violations (should be 0).")
            .conclude(
                "If all 8 pairs cross correctly with 0 violations, the "
                "complementary pair topology is confirmed: every Coupling Port "
                "has exactly one partner in the opposite Field Chamber."
            )
        )

    def model(self) -> Model:
        all_vertices = set(range(2 * K))
        complement_mask = 2 ** 3 - 1  # 7 for d=3

        crossing_count = 0
        violation_count = 0

        for v in all_vertices:
            partner = v ^ complement_mask
            v_in_a = v in TET_A
            partner_in_b = partner in TET_B
            v_in_b = v in TET_B
            partner_in_a = partner in TET_A

            if (v_in_a and partner_in_b) or (v_in_b and partner_in_a):
                crossing_count += 1
            else:
                violation_count += 1

        return (
            Model()
            .add("Crossing pair count", float(crossing_count))
            .add("Violation count", float(violation_count))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Crossing pair count", 8.0)
            .add("Violation count", 0.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Complementary Pair Inversion Across Field Chambers",
        summary="Verifies that XOR 7 inversion maps every vertex to the opposite tetrahedron",
        test_classes=[ComplementaryPairInversionCrossesChambers],
    )
