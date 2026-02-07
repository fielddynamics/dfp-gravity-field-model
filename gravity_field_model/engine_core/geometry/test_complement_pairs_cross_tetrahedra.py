# FILENAME: test_complement_pairs_cross_tetrahedra.py

"""
Complement Pairs Cross Tetrahedra
==================================

The stellated octahedron has four complementary pairs of vertices: (0,7),
(1,6), (2,5), and (3,4). Each pair sums to 7 and connects diagonally
opposite corners of the embedding cube. A fundamental question is whether
these pairs always span both tetrahedra, meaning one member in Tet A and
one in Tet B. Standard combinatorics shows that XOR with 111 necessarily
flips bit parity, so the complement must live in the opposite parity class.
This property is what makes the dual channel architecture work: reading
vertex V on the explicit channel guarantees that vertex 7 minus V on the
implicit channel belongs to the other Field Chamber.

GFM OBSERVATION: All 4 complement pairs span both tetrahedra, enabling
simultaneous dual chamber readout at every traversal step.

This is a DERIVATION from the parity partition and XOR complement properties.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B,
    get_tetrahedron,
)


def count_ones(vertex: int) -> int:
    """Count 1 bits in the binary representation of a vertex label."""
    return bin(vertex).count('1')


def get_parity(vertex: int) -> int:
    """Return 0 for even bit count, 1 for odd bit count."""
    return count_ones(vertex) % 2


class ComplementPairsCrossTetrahedra(Test):
    """
    PHYSICAL CONTEXT:
    The stellated octahedron consists of two interpenetrating tetrahedra
    inscribed in a cube. The cube has four body diagonals, each connecting
    a vertex V to its complement 7 minus V. These diagonals all pass through
    the origin (0,0,0), the Field Origin. The parity partition assigns
    odd bit count vertices to Tet A and even bit count vertices to Tet B.

    GFM OBSERVATION:
    XOR with 111 flips all three bits, which necessarily changes the bit
    count parity. Therefore every complement pair has one member in Tet A
    and one in Tet B. This means all 4 pairs cross tetrahedra, yielding
    a crossing count of 4 out of 4. The dual channel architecture depends
    on this: at each traversal step, the explicit vertex and its implicit
    complement always belong to opposite Field Chambers.

    EPISTEMIC STATUS:
    This is a mathematical derivation. XOR with 111 flips parity as a
    theorem of binary arithmetic. No empirical input is needed.
    """

    name = "Complement Pairs Cross Tetrahedra"

    question = (
        "Do all four complementary pairs in the stellated octahedron span "
        "both tetrahedra? The pairs are (0,7), (1,6), (2,5), and (3,4), "
        "each summing to 7. If XOR with 111 always flips bit parity, then "
        "one member must have odd parity (Tet A) and the other even parity "
        "(Tet B). This would guarantee that the implicit channel always "
        "reads the opposite Field Chamber from the explicit channel."
    )

    reference = "Mathematical (parity flip under XOR 111); Coxeter 1973 (stellated octahedron geometry)"

    tolerance = 0.001

    level = Level.STANDARD

    commentary = (
        "This result bridges two properties already established in the binary "
        "triad tests: the parity partition (odd bits to Tet A, even to Tet B) "
        "and the XOR complement (flipping all bits via XOR 7). Their combination "
        "yields the physically crucial fact that complements always cross chambers. "
        "This is a derivation, not an observation: flipping all three bits in a "
        "binary string necessarily changes whether the total count of ones is odd "
        "or even. The consequence for field closure is profound. At every single "
        "step of the pi driven traversal, the system simultaneously accesses both "
        "tetrahedra through the explicit and implicit channels. No step is ever "
        "confined to one chamber. This is why closure operates at the full Compton "
        "frequency rather than half of it."
    )

    # Audit scoring
    audit_score = 91
    audit_notes = (
        "Question: 13/15 (asks a clear yes/no question with specific pairs listed and connects to dual channel consequence, but framing leans toward confirmation rather than mystery; could sharpen the stakes by leading with the physical consequence before the mechanism). Derivation: 14/15 (excellent structure with premise, theorem, proof, enumeration, and conclusion; the parity flip proof is intuitive before formal; minor note: the equation step packs three equalities tightly which could be split for readability). Commentary: 14/15 (strong insight connecting two prior tests into a new result, clearly states derivation not observation, explains the Compton frequency consequence; could benefit from a brief analogy to make the dual channel idea vivid for undergrads). Model: 9/10 (clean single summary statistic, easy to interpret; the loop over range(K) is elegant since K=4 gives exactly the 4 lower vertices of each pair, though a brief inline comment would help readers see why range(4) covers all pairs). Observations: 9/10 (value is exact by mathematical theorem, well justified; reference to Coxeter is appropriate but the observed value is purely mathematical so citing an experimental source is not applicable, which is correctly handled). Constants: 10/10 (K, VERTICES, TET_A, TET_B, get_tetrahedron all imported from common; no hardcoded physics constants; the number 7 appears as the XOR mask which is 2^d minus 1 and is correctly used as a structural constant). Accessibility: 14/15 (undergrads can follow the bit flipping logic, PhD readers gain the dual channel insight; jargon like Field Chamber and Compton frequency is used but explained in context; the parity argument is clean). Header: 8/10 (module docstring covers the physical domain, states what is being verified, identifies epistemic status as derivation, and notes the GFM observation; could add target audience level and a brief note on how this test relates to the existing binary triad suite)."
    )

    academic_paper = """\
TITLE Complementary Vertex Pairs and Bimetric Chamber Crossing in the Stellated Octahedron ABSTRACT We investigate whether all four complementary pairs in the stellated octahedron necessarily span both tetrahedra. Using the parity flip theorem for XOR with 111, we derive that crossing is guaranteed. All 4 of 4 pairs confirmed. This is a mathematical DERIVATION. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The stellated octahedron, formed by two interpenetrating tetrahedra inscribed in a cube, is the central geometric object in the Gravity Field Model. Its eight vertices split into two groups of four by bit parity: Tet A receives vertices with an odd number of 1 bits (1, 2, 4, 7), and Tet B receives vertices with an even number (0, 3, 5, 6). Separately, each vertex V has a complement defined as 7 minus V, equivalently V XOR 7, which lies at the diagonally opposite cube corner. A critical structural question arises: does every complementary pair always have one member in each tetrahedron? If so, the dual channel architecture of field closure is guaranteed. At every traversal step, reading vertex V on the explicit channel means the implicit channel (vertex 7 minus V) automatically accesses the opposite Field Chamber. Without this crossing property, simultaneous dual chamber readout would not be assured. Standard combinatorics provides the answer through parity analysis of binary strings under bit inversion. GFM identifies this property as the foundation of bimetric balance during the pi driven traversal. This test verifies the crossing property for all four pairs. 2. METHODOLOGY We enumerate all four complementary pairs: (0,7), (1,6), (2,5), and (3,4). For each pair, we determine the tetrahedron membership of both members using the get_tetrahedron function imported from the common module. A pair is counted as crossing if its two members belong to different tetrahedra. The model output is the total count of crossing pairs. The expected value is 4 out of 4, established by the parity flip theorem: XOR with 111 flips all three bits, transforming a bit count of p into 3 minus p, which necessarily changes the parity. Agreement criterion is an exact match with zero tolerance. 3. RESULTS Model output: Pairs crossing tetrahedra equals 4. Observed expectation: 4. Pair by pair enumeration confirms the result. Vertex 0 (bit count 0, even, Tet B) pairs with vertex 7 (bit count 3, odd, Tet A). Vertex 1 (bit count 1, odd, Tet A) pairs with vertex 6 (bit count 2, even, Tet B). Vertex 2 (bit count 1, odd, Tet A) pairs with vertex 5 (bit count 2, even, Tet B). Vertex 3 (bit count 2, even, Tet B) pairs with vertex 4 (bit count 1, odd, Tet A). Every pair spans both chambers. The match is exact with zero residual. 4. DISCUSSION The crossing property is not empirical. It is a theorem of binary arithmetic. Flipping all d bits in a d bit string changes the bit count from p to d minus p. For d equals 3 (an odd number), d minus p has opposite parity to p. This means the XOR complement of any vertex is always in the opposite parity class and therefore the opposite tetrahedron. EPISTEMIC STATUS: DERIVATION. This follows necessarily from the parity partition and the definition of bitwise complement. No physical measurement or fitting is involved. The result is significant because it bridges two previously established properties (parity partition and XOR complement identity) into a single structural guarantee. It underpins the dual channel architecture described in the core theory: the implicit channel always reads the opposite Field Chamber. This is why field closure operates at the full Compton frequency rather than half. This test connects to the broader binary triad suite and provides the logical prerequisite for traversal tests that assume simultaneous access to both tetrahedra. 5. LIMITATIONS AND HONESTY STATEMENT This test verifies a mathematical identity, not a physical prediction. It does not prove that nature uses the stellated octahedron. The parity argument requires exactly d equals 3 bits (odd dimensionality). Extension to other dimensions would require separate analysis. The physical interpretation of dual channel readout remains a GFM framework assumption. 6. CONCLUSION All four complementary pairs in the stellated octahedron are proven to cross tetrahedra by the parity flip
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "PREMISE: Vertices are labeled 0 through 7 with 3 bit binary codes. "
                "Tet A contains vertices with odd bit count: {1, 2, 4, 7}. "
                "Tet B contains vertices with even bit count: {0, 3, 5, 6}."
            )
            .step(
                "The complement of vertex V is defined as V XOR 7, which equals "
                "7 minus V. XOR with 111 flips all three bits."
            )
            .step(
                "THEOREM: If V has bit count p, then V XOR 7 has bit count 3 minus p. "
                "Proof: each of the 3 bits is flipped, so every 1 becomes 0 and every "
                "0 becomes 1. The new count of ones is (3 minus original count)."
            )
            .equation("parity(V XOR 7) = (3 - count_ones(V)) mod 2 = (1 - count_ones(V) mod 2) = 1 - parity(V)")
            .step(
                "Since parity is flipped, if V is in Tet A (odd parity), then "
                "V XOR 7 is in Tet B (even parity), and vice versa."
            )
            .step(
                "Enumerate all 4 pairs: (0,7) has parities (0,1), (1,6) has (1,0), "
                "(2,5) has (1,0), (3,4) has (0,1). Each pair spans both chambers."
            )
            .conclude(
                "All 4 complementary pairs cross tetrahedra. The dual channel "
                "architecture is guaranteed by binary arithmetic: the implicit "
                "channel always reads the opposite Field Chamber."
            )
        )

    def model(self) -> Model:
        crossing_count = 0
        for v in range(K):
            complement = 7 - v
            tet_v = get_tetrahedron(v)
            tet_c = get_tetrahedron(complement)
            if tet_v != tet_c:
                crossing_count += 1
        return Model().add("Pairs crossing tetrahedra", float(crossing_count))

    def observations(self) -> Observed:
        return Observed().add("Pairs crossing tetrahedra", 4.0)


if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Complement Pairs Cross Tetrahedra",
        summary="Verifies that all 4 complementary pairs span both Field Chambers via parity flip under XOR",
        test_classes=[ComplementPairsCrossTetrahedra],
    )
