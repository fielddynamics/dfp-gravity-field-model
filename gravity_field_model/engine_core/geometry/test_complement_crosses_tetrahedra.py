# FILENAME: test_complement_crosses_tetrahedra.py

"""
Complement Crosses Tetrahedra
=============================

The stellated octahedron consists of two interpenetrating tetrahedra (Tet A
and Tet B) whose vertices are the 8 corners of a cube. Each vertex has a
complement defined by XOR with 7 (equivalently, 7 minus the vertex number),
which maps to the diagonally opposite cube corner. Standard geometry tells
us that the two tetrahedra inscribed in a cube are related by spatial
inversion through the center. Since inversion flips all three coordinates,
it must swap the parity class, sending odd parity vertices to even and
vice versa. The question is whether this parity swap perfectly coincides
with tetrahedron membership in the GFM dual chamber assignment.

GFM OBSERVATION: The XOR complement operation always crosses the bimetric
boundary, guaranteeing that the implicit channel (7 minus V) always lies
in the opposite tetrahedron from the explicit channel (V).

This is an OBSERVATION grounded in combinatorial geometry, not a derivation
from dynamical principles.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B,
    get_tetrahedron,
)


def count_ones(vertex: int) -> int:
    """Count the number of 1 bits in the binary representation."""
    return bin(vertex).count('1')


def get_parity(vertex: int) -> str:
    """Return 'odd' or 'even' based on popcount of vertex number."""
    return "odd" if count_ones(vertex) % 2 == 1 else "even"


class ComplementCrossesTetrahedra(Test):
    """
    PHYSICAL CONTEXT:
    A cube has four body diagonals connecting opposite corners. When two
    regular tetrahedra are inscribed in a cube (one per parity class of
    vertex coordinates), spatial inversion through the center maps one
    tetrahedron onto the other. This is a classical result in polyhedral
    geometry (Coxeter, Regular Polytopes, 1973). The XOR complement with
    7 implements exactly this inversion in binary coordinates: it flips
    all three bits, reversing every coordinate from +1 to  1 or vice
    versa. Because the tetrahedra are distinguished by bit parity (odd
    popcount vs even popcount), flipping all three bits necessarily
    changes the popcount parity and therefore the tetrahedron membership.

    GFM OBSERVATION:
    In the GFM dual channel architecture, at every traversal step the
    explicit channel visits vertex V while the implicit channel
    simultaneously registers vertex 7 minus V. This test confirms that
    these two vertices always belong to opposite tetrahedra, validating
    the claim that the implicit channel is guaranteed to sample the
    opposite Field Chamber. The number of crossing pairs is 8 (all
    vertices), and this connects to 2k = 2 times 4 = 8 total vertices
    with k = 4 being the closure constant.

    EPISTEMIC STATUS:
    This is a mathematical observation following from the parity partition
    of cube vertices. It is not a dynamical derivation but a combinatorial
    fact that underpins the dual channel mechanism.
    """

    name = "Complement Crosses Tetrahedra"

    question = (
        "Does the XOR complement operation (flipping all bits via XOR with 7) "
        "always send a vertex from one tetrahedron to the other? The dual channel "
        "architecture of GFM requires that the implicit channel (7 minus V) is "
        "guaranteed to lie in the opposite Field Chamber from the explicit channel "
        "(V). If even one vertex failed to cross, the bimetric balance would break. "
        "We test all 8 vertices to confirm universal crossing."
    )

    reference = "Coxeter, Regular Polytopes (1973); GFM Core Theory Section 3.1"

    tolerance = 0.001

    level = Level.STANDARD

    commentary = (
        "Every vertex crosses to the opposite tetrahedron under complementation. "
        "This is not surprising from a mathematical standpoint: XOR with 111 flips "
        "all three bits, which necessarily changes the popcount parity from odd to "
        "even or from even to odd. Since parity determines tetrahedron membership, "
        "crossing is guaranteed. What makes this physically significant is that it "
        "validates the dual channel architecture. At every step of the pi driven "
        "traversal, the field simultaneously samples both Field Chambers. This is "
        "an observation rooted in combinatorial geometry, not a derivation from "
        "dynamics. It explains why field closure operates at the full Compton "
        "frequency rather than half: both chambers are always engaged."
    )

    # Audit scoring
    audit_score = 91
    audit_notes = (
        "Question: 14/15 (strong stakes framing with the 'if even one vertex failed' tension, but opens with a yes/no rather than a deeper why mystery). Derivation: 14/15 (excellent intuition first approach with the parity argument building naturally to the equation, minor note: the physical setup could paint the picture slightly more before jumping to Tet A/B labels). Commentary: 14/15 (strong insight connecting crossing to full Compton frequency operation, clearly labels as observation not derivation, could benefit from a concrete analogy for non specialists). Model: 9/10 (clean single summary statistic, easy to interpret, appropriate for a combinatorial verification). Observations: 8/10 (value is mathematically exact and traceable to cube geometry, but the Coxeter reference in the reference field could be more specific with chapter/page). Constants: 9/10 (imports K, VERTICES, TET_A, TET_B, get_tetrahedron from common correctly, the helper functions count_ones and get_parity duplicate helpers from the sibling file test_binary_triad.py rather than importing from a shared utility). Accessibility: 14/15 (undergrads can follow the bit flipping logic, PhDs gain the dual channel connection, jargon like popcount is explained contextually, could define XOR explicitly for the broadest audience). Header: 9/10 (comprehensive module docstring covering phenomenon, GFM observation, and epistemic status, missing only an explicit target audience statement and could note relationship to sibling tests in the geometry domain)."
    )

    academic_paper = """\
TITLE XOR Complementation and Tetrahedron Crossing in the Stellated Octahedron: Verifying the Dual Channel Boundary Property ABSTRACT We test whether the XOR complement operation (V XOR 7) always maps a vertex of one inscribed tetrahedron to the other in a cube. The model checks all 8 vertices and finds 8 out of 8 cross the tetrahedron boundary, matching exactly. This combinatorial fact underpins the GFM dual channel architecture. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The stellated octahedron consists of two regular tetrahedra inscribed in a cube, with vertices at the eight corners labeled 0 through 7. Each vertex has a 3 bit binary address, and the two tetrahedra are distinguished by the parity of the popcount (number of 1 bits): odd parity vertices {1, 2, 4, 7} form Tet A, while even parity vertices {0, 3, 5, 6} form Tet B. This partition is a classical result in polyhedral geometry (Coxeter, Regular Polytopes, 1973). Standard geometry establishes that spatial inversion through the cube center maps one inscribed tetrahedron onto the other. In binary coordinates, this inversion is implemented by XOR with 7 (binary 111), which flips all three bits simultaneously. The Gravity Field Model proposes a dual channel architecture in which every traversal step reads vertex V explicitly while simultaneously registering the complement vertex 7 minus V implicitly. For this architecture to guarantee bimetric balance, complementation must always cross the tetrahedron boundary. If even one vertex mapped to the same tetrahedron under complementation, the implicit channel would sometimes duplicate the explicit channel rather than sampling the opposite Field Chamber. This test investigates whether all 8 vertices satisfy the crossing property without exception. 2. METHODOLOGY The model iterates over all 8 vertices (0 through 7). For each vertex V, it computes the complement V XOR 7 and determines the tetrahedron membership of both V and its complement using the parity partition imported from the GFM common library. A vertex counts as "crossing" if V and V XOR 7 belong to different tetrahedra. The model reports the total count of crossing vertices. The expected value is 8 (all vertices cross), derived from the mathematical argument that XOR with 7 flips all 3 bits, changing the popcount from p to 3 minus p, which always reverses parity since 3 is odd. Agreement is defined as 0.00% error between model and expectation. 3. RESULTS The model output reports: Vertices crossing tetrahedra: 8 The expected observation, from combinatorial geometry: Vertices crossing tetrahedra: 8 Comparison yields 0.00% error. The match is exact, not approximate. To illustrate: V3 (binary 011, popcount 2, even, Tet B) maps to V4 (binary 100, popcount 1, odd, Tet A). V7 (binary 111, popcount 3, odd, Tet A) maps to V0 (binary 000, popcount 0, even, Tet B). Every one of the four complementary pairs, (0,7), (1,6), (2,5), (3,4), spans both tetrahedra. No exceptions exist. 4. DISCUSSION The result is a mathematical certainty rather than an empirical finding. If V has popcount p, then V XOR 7 has popcount 3 minus p. Because 3 is odd, the parity of 3 minus p is always opposite to the parity of p. This guarantees universal crossing. EPISTEMIC STATUS: OBSERVATION. We observe that the XOR complement operation always crosses the tetrahedron boundary. This is a combinatorial fact about cube geometry, not a dynamical derivation from GFM principles. GFM does not derive this property; it inherits it from the choice of the stellated octahedron as its geometric substrate. The physical significance is that the dual channel architecture is structurally guaranteed to sample both Field Chambers at every traversal step. This is consistent with the claim that field closure operates at the full Compton frequency (approximately 10^20 Hz) rather than half that rate, because both tetrahedra are always engaged. This test complements the existing binary triad tests that verify parity partitioning and XOR identity independently, bridging those two results into a single combined property. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove the dual channel architecture is physically realized. It confirms only that the geometric prerequisite (complementation crosses tetrahedra) holds. The result follows from elementary combinatorics and does not constitute evidence for GFM beyond validating internal consistency. The crossing property would hold for any parity based
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: Two tetrahedra inscribed in a cube are "
                "distinguished by bit parity. Tet A contains vertices with odd "
                "popcount {1, 2, 4, 7} and Tet B contains vertices with even "
                "popcount {0, 3, 5, 6}."
            )
            .step(
                "XOR COMPLEMENT: For any vertex V, the complement is V XOR 7, "
                "which flips all three bits of the binary representation."
            )
            .step(
                "PARITY ARGUMENT: If V has popcount p, then V XOR 7 has "
                "popcount 3 minus p (each of 3 bits flips). Since 3 is odd, "
                "the parity of (3 minus p) is always opposite to the parity of p."
            )
            .equation("parity(V XOR 7) = parity(3 - popcount(V)) != parity(popcount(V))")
            .step(
                "Therefore the complement always belongs to the opposite tetrahedron. "
                "We verify this for all 8 vertices: count how many satisfy the "
                "crossing property."
            )
            .step(
                "GFM OBSERVATION: This crossing property is exactly what the dual "
                "channel architecture requires. The explicit channel reads V from "
                "one Field Chamber while the implicit channel simultaneously reads "
                "7 minus V from the other."
            )
            .conclude(
                "All 8 vertices cross tetrahedra under complementation, confirming "
                "that the implicit channel always samples the opposite Field Chamber "
                "from the explicit channel."
            )
        )

    def model(self) -> Model:
        crossing_count = 0
        for v in range(8):
            complement = v ^ 7
            tet_v = get_tetrahedron(v)
            tet_c = get_tetrahedron(complement)
            if tet_v != tet_c:
                crossing_count += 1
        return (
            Model()
            .add("Vertices crossing tetrahedra", float(crossing_count))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Vertices crossing tetrahedra", 8.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Complement Crosses Tetrahedra",
        summary="Verify that XOR complement always maps vertices to the opposite Field Chamber",
        test_classes=[ComplementCrossesTetrahedra],
    )
