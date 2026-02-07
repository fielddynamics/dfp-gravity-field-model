# FILENAME: test_complementary_pairs.py

"""
Complementary Pair Structure of the Stellated Octahedron
========================================================

The stellated octahedron consists of two interpenetrating tetrahedra whose
eight vertices sit at the corners of a cube with coordinates (+/- 1, +/- 1, +/- 1).
Each vertex is labeled by a 3 bit binary index (0 through 7). Standard group
theory identifies the bitwise complement operation (XOR with 111 in binary,
equivalently 7 minus V in decimal) as a Z2 involution that exchanges the two
tetrahedra. This operation produces four complementary pairs: (0,7), (1,6),
(2,5), (3,4). Each pair connects vertices of opposite parity, meaning one
vertex belongs to Tet A (odd bit sum) and the other to Tet B (even bit sum).
The midpoint of every pair is the geometric center (0,0,0), the Field Origin.

GFM OBSERVATION: The four complementary pairs are the geometric basis of the
dual channel architecture, where reading vertex V simultaneously determines 7 minus V.

This is a DERIVATION from the vertex coordinate geometry of the stellated octahedron.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K,
    VERTICES,
    TET_A,
    TET_B,
)


COMPLEMENT_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]

VERTEX_COORDS = {
    0: (-1, -1, -1),
    1: (-1, -1, +1),
    2: (-1, +1, -1),
    3: (-1, +1, +1),
    4: (+1, -1, -1),
    5: (+1, -1, +1),
    6: (+1, +1, -1),
    7: (+1, +1, +1),
}


def bit_sum(v):
    """Count the number of 1 bits in the 3 bit representation of v."""
    return bin(v).count("1")


def parity(v):
    """Return 0 for even bit sum, 1 for odd bit sum."""
    return bit_sum(v) % 2


def midpoint(v_a, v_b):
    """Compute the midpoint of two vertices in 3D coordinate space."""
    ca = VERTEX_COORDS[v_a]
    cb = VERTEX_COORDS[v_b]
    return ((ca[0] + cb[0]) / 2.0, (ca[1] + cb[1]) / 2.0, (ca[2] + cb[2]) / 2.0)


def distance_from_origin(coords):
    """Euclidean distance from (0,0,0)."""
    return math.sqrt(coords[0]**2 + coords[1]**2 + coords[2]**2)


def count_cross_tetrahedral_pairs():
    """Count how many complementary pairs span both tetrahedra."""
    count = 0
    for v_a, v_b in COMPLEMENT_PAIRS:
        a_in_tet_a = v_a in TET_A
        b_in_tet_a = v_b in TET_A
        if a_in_tet_a != b_in_tet_a:
            count += 1
    return count


def count_pairs_through_origin():
    """Count how many complementary pairs have midpoint at (0,0,0)."""
    count = 0
    for v_a, v_b in COMPLEMENT_PAIRS:
        mid = midpoint(v_a, v_b)
        dist = distance_from_origin(mid)
        if dist < 1e-12:
            count += 1
    return count


class ComplementaryPairStructure(Test):
    """
    PHYSICAL CONTEXT:
    In the geometry of the cube, each vertex has a unique antipodal partner
    obtained by negating all three coordinates. For vertices labeled 0 through
    7 by their 3 bit binary representation, this antipodal map is the XOR
    with 7 (binary 111), equivalently the map V -> 7 minus V. This Z2
    involution partitions the 8 vertices into 4 complementary pairs. The
    operation is well established in combinatorial geometry (Coxeter 1973)
    and appears in coding theory as the bitwise complement in the Hamming
    cube H(3,2). Each pair consists of vertices at maximum Hamming distance
    (3 bit flips), meaning they share no coordinate sign.

    GFM OBSERVATION:
    The four complementary pairs (0,7), (1,6), (2,5), (3,4) each cross the
    tetrahedral boundary: one member belongs to Tet A (odd parity vertices
    1,2,4,7) and the other to Tet B (even parity vertices 0,3,5,6). Every
    pair has its midpoint at (0,0,0), the Field Origin. This structure is
    the geometric foundation for the dual channel architecture: reading any
    vertex V on the explicit channel simultaneously determines 7 minus V on
    the implicit channel, always in the opposite tetrahedron. The number of
    pairs (4) equals the closure constant K, and each pair connects vertices
    separated by distance 2*sqrt(3), the body diagonal of the embedding cube.

    EPISTEMIC STATUS:
    This is a DERIVATION from the coordinate geometry of the stellated
    octahedron. All properties follow from the vertex positions and the
    bitwise complement operation. No approximations or fits are involved.
    """

    name = "Complementary Pair Structure"

    question = (
        "Do the four complementary pairs of the stellated octahedron each "
        "cross the tetrahedral boundary, and does every pair pass through "
        "the Field Origin at (0,0,0)? The dual channel architecture requires "
        "that reading vertex V always determines a vertex 7 minus V in the "
        "opposite tetrahedron. Is this guaranteed by the geometry, and do "
        "exactly K = 4 such pairs exist?"
    )

    reference = (
        "Coxeter (1973) Regular Polytopes; "
        "GFM Paper VII Section 2.2 (vertex labeling and complementary pairs); "
        "GFM Paper VII Section 3.1 (dual channel architecture)"
    )

    tolerance = 0.001

    level = Level.CRITICAL

    commentary = (
        "All four complementary pairs cross the tetrahedral boundary and "
        "pass through the Field Origin, confirming the geometric basis of "
        "the dual channel architecture. The complement operation V -> 7 "
        "minus V flips all three coordinate signs, which necessarily flips "
        "the bit sum parity, guaranteeing a crossing from Tet A to Tet B "
        "or vice versa. This is a derivation from coordinate geometry, not "
        "an empirical observation. The number of pairs equals K = 4, "
        "matching the closure constant, and the body diagonal length "
        "2*sqrt(3) is exactly twice the distance from any vertex to the "
        "Field Origin. These properties underpin the traversal mechanism: "
        "every explicit read on one tetrahedron produces an implicit read "
        "on the other, enabling closure at full Compton frequency."
    )

    # Audit scoring
    audit_score = 85
    audit_notes = (
        "Question: 12/15 (asks the right structural questions and includes specific numbers like K=4, but leads with a yes/no framing rather than a mystery hook; could open with WHY the dual channel works before asking whether it does). Derivation: 14/15 (excellent scaffolding from standard cube geometry through parity partition to the cross tetrahedral property and midpoint proof; the parity flip argument is the key insight and is well placed; minor gap: no everyday analogy to ground the abstract bit flipping for non specialists). Commentary: 12/15 (solid interpretation connecting results to the dual channel architecture and Compton frequency; correctly labels as derivation; missing an analogy or aha moment beyond restating the geometric facts; implications for downstream GFM results like spin and E=mc^2 are hinted but not developed). Model: 9/10 (clean set of 9 values mixing continuous quantities with binary pass/fail verdicts; easy to interpret; well within the 3 to 10 range; the body diagonal and vertex distance give geometric grounding beyond just boolean checks). Observations: 8/10 (all values are mathematically exact and traceable to GFM geometry definitions and Coxeter; K imported from common for the pair count; VERTEX_COORDS hardcoded as a module level dict rather than derived from imports, but this is justified since common does not export coordinates; sqrt(3) and 2*sqrt(3) are standard geometry). Constants: 9/10 (K, VERTICES, TET_A, TET_B all imported from common; VERTEX_COORDS necessarily hardcoded since coordinates are not available in common; COMPLEMENT_PAIRS defined at module level with clear documentation; VERTICES imported but not directly used in model/observations, minor unused import). Accessibility: 13/15 (an undergraduate with linear algebra and basic combinatorics can follow the parity argument and midpoint calculation; the Hamming cube reference in the docstring adds depth for specialists; the bit flipping argument could benefit from a concrete walkthrough of one example pair to anchor intuition; no everyday analogy provided). Header: 8/10 (comprehensive module docstring covering the physical structure, the GFM observation, and epistemic status as derivation; clearly states what is being tested and why; missing target audience line and explicit note about which downstream GFM results depend on this property)."
    )

    academic_paper = """\
TITLE Complementary Pair Structure of the Stellated Octahedron: Cross Tetrahedral Symmetry and the Field Origin ABSTRACT We investigate whether the four complementary vertex pairs of the stellated octahedron each cross the tetrahedral boundary and pass through the geometric center. Exhaustive computation confirms all four pairs satisfy both properties exactly. This is a DERIVATION from coordinate geometry, establishing the foundation for the dual channel architecture. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The stellated octahedron consists of two interpenetrating tetrahedra (Tet A, Tet B) whose eight vertices occupy the corners of a cube at coordinates (+/- 1, +/- 1, +/- 1). Each vertex carries a 3 bit binary label from 0 to 7. The bitwise complement operation, XOR with 7, maps each vertex V to its antipodal partner 7 minus V. This Z2 involution is well established in combinatorial geometry (Coxeter 1973) and produces four pairs: (0,7), (1,6), (2,5), (3,4). The GFM dual channel architecture requires that every explicit vertex read on one tetrahedron simultaneously determines an implicit vertex on the opposite tetrahedron. For this to be geometrically guaranteed, complementary pairs must always cross the tetrahedral boundary. Furthermore, the Field Origin at (0,0,0), the coupling interface between the two tetrahedra, should lie on every body diagonal connecting a pair. This test investigates whether both properties hold for all four pairs, and whether the pair count matches the closure constant K = 4. 2. METHODOLOGY We assign each vertex to Tet A (odd bit sum parity: vertices 1, 2, 4, 7) or Tet B (even bit sum parity: vertices 0, 3, 5, 6), using the framework imports TET_A and TET_B. For each of the four complementary pairs, we check three properties: (a) the two members sum to 7, (b) the members belong to opposite tetrahedra, and (c) the midpoint of the pair in 3D coordinate space equals (0,0,0). We also compute the body diagonal length between complementary partners and verify that all eight vertices are equidistant from the origin. Agreement criterion: exact match (0.00% error) for all nine quantities. 3. RESULTS All nine model outputs match their expected values exactly. The model calculates 4 complementary pairs, matching K = 4 (0.00% error). All 4 pairs cross the tetrahedral boundary (0.00% error). All 4 pairs have their midpoint at the origin (0.00% error). The complement sum check V + V_bar = 7 passes for every pair (binary verdict: 1). The body diagonal length is 3.464102, matching 2*sqrt(3) exactly (0.00% error). The vertex distance to the Field Origin is 1.732051, matching sqrt(3) exactly (0.00% error). All 8 vertices are confirmed equidistant from the origin (binary verdict: 1). Tet A contains exclusively odd parity vertices (binary verdict: 1). Tet B contains exclusively even parity vertices (binary verdict: 1). The parity partition is the key mechanism. XOR with 7 (binary 111) flips all three bits. Since flipping three bits changes the bit sum by an odd number, the operation necessarily flips parity. A vertex in Tet A (odd parity) is always mapped to Tet B (even parity) and vice versa. 4. DISCUSSION The cross tetrahedral property is not approximate or statistical. It is a theorem: flipping all bits in a 3 bit string always changes the parity. This guarantees that the complement of any Tet A vertex lies in Tet B, with no exceptions possible. The midpoint property follows from the coordinate structure: if vertex V has coordinates (a, b, c), then vertex 7 minus V has coordinates (minus a, minus b, minus c), and their average is exactly (0, 0, 0). EPISTEMIC STATUS: DERIVATION. Every result follows from the vertex coordinate assignments and the bitwise complement operation. No fits, approximations, or free parameters are involved. The number of pairs equaling K = 4 is consistent with the closure constant appearing as the natural partition size of the 8 vertex structure. This test establishes the geometric prerequisite for the dual channel architecture used in the pi base 8 traversal, the spin derivation (which relies on the time face identification via parity), and the E = mc^2 derivation (which requires two tetrahedra contributing independently). 5. LIMITATIONS AND HONESTY STATEMENT This test verifies geometric properties of an idealized mathematical structure. It does not prove that physical spacetime possesses this geometry.
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD PHYSICS: The 8 vertices of a cube at coordinates "
                "(+/- 1, +/- 1, +/- 1) are labeled V0 through V7 by their "
                "3 bit binary index. The antipodal map negates all coordinates, "
                "equivalent to XOR with 7 (binary 111). This produces 4 pairs: "
                "(0,7), (1,6), (2,5), (3,4)."
            )
            .step(
                "PARITY PARTITION: Tet A contains odd parity vertices (odd "
                "number of 1 bits): {1,2,4,7}. Tet B contains even parity "
                "vertices: {0,3,5,6}. The XOR with 7 flips all 3 bits, which "
                "always changes the bit sum by an odd number (either +3, +1, "
                " minus 1, or minus 3), necessarily flipping the parity."
            )
            .equation("parity(V XOR 7) = 1 minus parity(V)")
            .step(
                "CROSS TETRAHEDRAL PROPERTY: Since the complement flips parity, "
                "every complementary pair has one member in Tet A and one in "
                "Tet B. All 4 of 4 pairs cross the tetrahedral boundary."
            )
            .step(
                "MIDPOINT CALCULATION: For any pair (V, 7 minus V), the "
                "coordinates are (a,b,c) and ( minus a, minus b, minus c). "
                "The midpoint is (0,0,0), the Field Origin."
            )
            .equation("midpoint = ((a minus a)/2, (b minus b)/2, (c minus c)/2) = (0,0,0)")
            .step(
                "DISTANCE: Each vertex is at distance sqrt(1^2+1^2+1^2) = "
                "sqrt(3) from the origin. The body diagonal connecting "
                "complementary partners has length 2*sqrt(3)."
            )
            .step(
                "DUAL CHANNEL: Reading vertex V determines complement 7 minus V "
                "in the opposite tetrahedron without additional signal "
                "propagation. This is the implicit channel."
            )
            .conclude(
                "The 4 complementary pairs of the stellated octahedron each "
                "cross the tetrahedral boundary and intersect at the Field "
                "Origin. This is a geometric derivation guaranteeing the dual "
                "channel architecture: every explicit vertex read on one "
                "tetrahedron produces a simultaneous implicit read on the other."
            )
        )

    def model(self) -> Model:
        num_pairs = len(COMPLEMENT_PAIRS)
        cross_count = count_cross_tetrahedral_pairs()
        origin_count = count_pairs_through_origin()

        # Verify complement sum property: V + (7-V) = 7 for all pairs
        sum_check_passed = all(
            (v_a + v_b) == 7 for v_a, v_b in COMPLEMENT_PAIRS
        )
        sum_check = 1.0 if sum_check_passed else 0.0

        # Body diagonal length
        v_a_coords = VERTEX_COORDS[0]
        v_b_coords = VERTEX_COORDS[7]
        diag_length = math.sqrt(
            (v_b_coords[0] - v_a_coords[0])**2
            + (v_b_coords[1] - v_a_coords[1])**2
            + (v_b_coords[2] - v_a_coords[2])**2
        )

        # Distance from any vertex to origin
        vertex_to_origin = distance_from_origin(VERTEX_COORDS[0])

        # Verify all 8 vertices equidistant from origin
        distances = [distance_from_origin(VERTEX_COORDS[v]) for v in range(8)]
        all_equidistant = 1.0 if all(
            abs(d - distances[0]) < 1e-12 for d in distances
        ) else 0.0

        # Tet A has exactly the odd parity vertices
        tet_a_all_odd = 1.0 if all(parity(v) == 1 for v in TET_A) else 0.0

        # Tet B has exactly the even parity vertices
        tet_b_all_even = 1.0 if all(parity(v) == 0 for v in TET_B) else 0.0

        return (
            Model()
            .add("Number of complementary pairs", float(num_pairs))
            .add("Pairs crossing tetrahedral boundary", float(cross_count))
            .add("Pairs with midpoint at origin", float(origin_count))
            .add("Complement sum V+V_bar=7 (1=pass)", sum_check)
            .add("Body diagonal length", diag_length)
            .add("Vertex distance to Field Origin", vertex_to_origin)
            .add("All vertices equidistant from origin (1=pass)", all_equidistant)
            .add("Tet A all odd parity (1=pass)", tet_a_all_odd)
            .add("Tet B all even parity (1=pass)", tet_b_all_even)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Number of complementary pairs", float(K))
            .add("Pairs crossing tetrahedral boundary", float(K))
            .add("Pairs with midpoint at origin", float(K))
            .add("Complement sum V+V_bar=7 (1=pass)", 1.0)
            .add("Body diagonal length", 2.0 * math.sqrt(3.0))
            .add("Vertex distance to Field Origin", math.sqrt(3.0))
            .add("All vertices equidistant from origin (1=pass)", 1.0)
            .add("Tet A all odd parity (1=pass)", 1.0)
            .add("Tet B all even parity (1=pass)", 1.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Complementary Pair Structure of the Stellated Octahedron",
        summary="Verifies that all 4 complementary pairs cross tetrahedra and pass through the Field Origin",
        test_classes=[ComplementaryPairStructure],
    )
