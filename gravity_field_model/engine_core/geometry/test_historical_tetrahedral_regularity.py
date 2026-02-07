# FILENAME: test_historical_tetrahedral_regularity.py

"""
Metric Regularity of Parity Partitioned Tetrahedra
===================================================

The binary vertex encoding of the cube partitions 8 vertices into two groups
of 4 based on bit count parity. The existing test suite validates this
combinatorial partition but never checks whether the resulting vertex groups
form regular tetrahedra in Euclidean space. A regular tetrahedron requires
all C(4,2) = 6 edges to have identical length. This test computes the
pairwise distances within each parity class using the coordinates
(+/- 1, +/- 1, +/- 1) and verifies that all 6 edges per tetrahedron
are equal, confirming genuine geometric regularity.

GFM OBSERVATION: The closure constant k=4 equals the vertex count of a regular tetrahedron.

This is a DERIVATION from Euclidean geometry applied to the cube vertex coordinates.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, TET_A, TET_B, VERTICES
)


class TetrahedralEdgeRegularity(Test):
    """
    Verify that the parity partition of cube vertices yields two regular tetrahedra.

    PHYSICAL CONTEXT:
    A cube with vertices at all sign combinations of (+/- 1, +/- 1, +/- 1)
    has 8 corners. Partitioning by bit count parity yields two sets of 4
    vertices each. For these sets to constitute genuine tetrahedra (not
    arbitrary 4 vertex subsets), every pairwise distance within each set
    must be identical. The expected edge length is 2*sqrt(2), since two
    vertices in the same parity class always differ in exactly 2 coordinates,
    giving distance sqrt(4+4) = 2*sqrt(2) approximately 2.8284.

    GFM OBSERVATION:
    Each tetrahedron has exactly k=4 vertices and C(k,2)=6 edges, all of
    length 2*sqrt(2). The edge length 2*sqrt(2) equals 2^(3/2) = 2^(d/2),
    connecting spatial dimension d=3 directly to the metric structure. Both
    tetrahedra are congruent, ensuring the bimetric balance required by GFM.

    EPISTEMIC STATUS:
    This is a pure geometric derivation. No empirical input is needed. The
    result follows necessarily from the coordinate definitions and Euclidean
    distance. It establishes that the combinatorial partition proven in
    sibling tests actually produces the geometric objects (regular tetrahedra)
    that the entire GFM framework depends upon.
    """

    name = "Tetrahedral Edge Regularity"

    question = (
        "Does the parity partition of cube vertices produce geometrically "
        "regular tetrahedra? The existing binary encoding tests confirm "
        "combinatorial properties (vertex counts, parity classification, "
        "XOR complementation) but never verify that the 6 edges within "
        "each group all have identical length. Without this check, the "
        "claim that the Field Chamber consists of two regular tetrahedra "
        "rests on assertion rather than geometric proof."
    )

    reference = (
        "Coxeter, Regular Polytopes (1973), Ch.2: vertex coordinates of "
        "the two tetrahedra inscribed in a cube; GFM Textbook Ch.9 Sec.9.2"
    )

    tolerance = 0.0001

    level = Level.STANDARD

    commentary = (
        "Every pair of vertices within the same parity class differs in "
        "exactly 2 out of 3 coordinates. This is a combinatorial fact: two "
        "3 bit strings with the same parity (both odd or both even popcount) "
        "must differ in an even number of positions, and since they are "
        "distinct, that number is exactly 2. Each differing coordinate "
        "contributes (1 minus negative 1)^2 = 4 to the squared distance, "
        "giving d^2 = 8 and d = 2*sqrt(2) for all 6 edges. This uniformity "
        "is what makes the tetrahedra regular. The result is a derivation "
        "from Euclidean geometry, not an observation or fit. It closes the "
        "foundational gap between the combinatorial partition and the "
        "geometric structure that all downstream GFM results require."
    )

    # Audit scoring
    audit_score = 88
    audit_notes = (
        "Question: 13/15 (clearly frames the gap and stakes, asks a genuine foundational question, but reads slightly more like a problem statement than a mystery hook; could sharpen the tension by leading with the surprise that nobody checked this). Derivation: 14/15 (excellent intuition first structure, the Hamming distance lemma is the key insight and it is well placed before the math, the only minor issue is that the physical setup could spend one more sentence on why regularity matters physically before diving into bit strings). Commentary: 12/15 (solid explanation of why all edges are equal, correctly labels epistemic status, but lacks an analogy for accessibility and does not state broader implications beyond closing the gap; no aha moment beyond confirming what was expected). Model: 9/10 (clean summary with 5 well chosen values, edge counts plus means plus max deviation is exactly the right level of abstraction, the only minor note is that max deviation comparing 0.0 to 0.0 is trivially satisfied by construction). Observations: 7/10 (values are mathematically exact and correct, Coxeter citation is appropriate, but the observed values are geometric truths not empirical measurements, and the test does not explicitly acknowledge that both model and observation are analytic; this weakens the notion of independent verification). Constants: 10/10 (K, TET_A, TET_B, VERTICES all imported from common, no hardcoded physics constants, derived quantities like 2*sqrt(2) are computed inline with clear documentation). Accessibility: 14/15 (builds from cube coordinates to binary parity to Hamming distance to Euclidean metric in a natural progression, an undergraduate in linear algebra could follow, the Hamming distance lemma proof is particularly well scaffolded, only minor gap is that the connection between Hamming distance and Euclidean distance could be stated more explicitly as a bridge sentence). Header: 9/10 (module docstring clearly states what is being tested and why, identifies the gap in the existing suite, labels epistemic status as derivation, cites the GFM observation, only missing element is an explicit target audience statement)."
    )

    academic_paper = """\
TITLE Metric Regularity of the Parity Partitioned Cube: Proving the Dual Tetrahedra Are Geometrically Regular ABSTRACT We verify that partitioning the eight vertices of a cube by bit count parity produces two congruent regular tetrahedra. All six edges within each group have identical length 2*sqrt(2). This is a geometric derivation, closing a foundational gap in the binary encoding test suite. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The Gravity Field Model (GFM) rests on the stellated octahedron: two interpenetrating regular tetrahedra whose eight vertices coincide with the corners of a cube. The existing binary encoding test suite validates several combinatorial properties of this structure. It confirms that eight vertices equal 2^3, that bit count parity classifies vertices into two groups of four, that XOR with 7 generates complementary pairs, and that those pairs cross between tetrahedra. These are important results, but they share a critical omission: none of them verify that the two groups of four vertices actually form regular tetrahedra in Euclidean space. Standard geometry establishes that a cube admits exactly two inscribed regular tetrahedra (Coxeter, 1973), and that these correspond to the two parity classes. The edge length of each tetrahedron inscribed in a cube of half side length 1 is 2*sqrt(2). This is well known, but the GFM test suite had not confirmed it computationally. This test closes that gap. It computes all pairwise distances within each parity class and verifies that all six edges per tetrahedron are identical, establishing geometric regularity from coordinate arithmetic. 2. METHODOLOGY Each of the eight cube vertices receives coordinates (+/- 1, +/- 1, +/- 1) determined by its 3 bit binary index. Tet A consists of vertices {1, 2, 4, 7} (odd popcount) and Tet B consists of vertices {0, 3, 5, 6} (even popcount), imported from the GFM geometry constants module. For each tetrahedron, we compute all C(4,2) = 6 pairwise Euclidean distances. We report the edge count per tetrahedron, the mean edge length, and the maximum deviation of any individual edge from the expected length 2*sqrt(2). Agreement criterion: maximum deviation equals zero to within tolerance 0.0001. 3. RESULTS Model output: Tet A edge count: 6.0 Tet B edge count: 6.0 Tet A mean edge length: 2.82842712 (2*sqrt(2)) Tet B mean edge length: 2.82842712 (2*sqrt(2)) Max deviation from regularity: 0.0 All six edges within Tet A are exactly 2*sqrt(2). All six edges within Tet B are exactly 2*sqrt(2). The two tetrahedra are congruent. The maximum deviation from perfect regularity is identically zero. The key insight underlying this result is a Hamming distance lemma: two distinct 3 bit strings with the same parity must differ in exactly 2 bit positions. This forces every intra tetrahedral pair to have squared distance 4 + 4 = 8, yielding edge length sqrt(8) = 2*sqrt(2) uniformly. The edge count C(4,2) = 6 also equals 2*d where d = 3, connecting the combinatorial structure to spatial dimensionality. 4. DISCUSSION This result bridges the combinatorial and metric levels of the GFM geometry. The sibling tests prove that parity partitions vertices into two groups of four. This test proves those groups are regular tetrahedra, not merely arbitrary subsets. The distinction matters because every downstream GFM result (coupling ports as triangular faces, the stellated octahedron structure, bimetric balance, the k = 4 closure constant) presupposes regular tetrahedral geometry. EPISTEMIC STATUS: DERIVATION. The result follows from Euclidean distance applied to defined coordinates. No empirical data or fitting is involved. Both the model values and the expected values are analytic, making this a self consistency verification of the geometric foundation. The congruence of the two tetrahedra confirms the bimetric symmetry that GFM requires: Chamber A and Chamber B are geometrically identical, differing only in orientation. 5. LIMITATIONS AND HONESTY STATEMENT This test verifies geometry, not physics. It does not prove that nature employs this structure. The coordinates (+/- 1) are a convention; rescaling changes edge lengths but not regularity. Because both model and observation are analytic, the test cannot fail in the empirical sense. It serves as a consistency check rather than an experimental confrontation. 6. CONCLUSION We confirm that the parity partition of cube vertices produces two congruent regular tetrahedra with six edges each, all of length 2*sqrt(2). This closes the foundational
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: Assign coordinates to the 8 cube vertices. "
                "Vertex i has coordinates ((-1)^b0, (-1)^b1, (-1)^b2) where "
                "b0 b1 b2 is the binary representation of i."
            )
            .step(
                "Tet A = {1, 2, 4, 7} (odd popcount). "
                "Tet B = {0, 3, 5, 6} (even popcount)."
            )
            .step(
                "KEY LEMMA: Two distinct 3 bit strings with the same parity "
                "must differ in exactly 2 bit positions. Proof: the Hamming "
                "distance between same parity strings is always even (flipping "
                "one bit changes parity). Since the strings are distinct, "
                "Hamming distance >= 2. Since there are only 3 bits, the "
                "maximum even Hamming distance for distinct strings is 2 "
                "(distance 0 means identical, distance 3 would flip parity "
                "of a 3 bit string)."
            )
            .equation(
                "d_edge = sqrt(sum of (delta_i)^2) where delta_i = 0 or 2"
            )
            .step(
                "With exactly 2 differing coordinates, each contributing "
                "(+1 minus (minus 1))^2 = 4, the squared distance is 4+4 = 8."
            )
            .equation("d_edge = sqrt(8) = 2*sqrt(2) = 2.82842712...")
            .step(
                "This holds for ALL C(4,2) = 6 pairs within each tetrahedron. "
                "Equal edge lengths confirm regularity."
            )
            .step(
                "Both tetrahedra have identical edge lengths, confirming "
                "they are congruent regular tetrahedra."
            )
            .step(
                "Additionally, the number of edges per tetrahedron is "
                "C(k,2) = C(4,2) = 6 = 2*d, connecting the edge count "
                "to spatial dimension d=3."
            )
            .conclude(
                "The parity partition produces two congruent regular tetrahedra "
                "with 6 edges each, all of length 2*sqrt(2). The combinatorial "
                "partition is geometrically valid."
            )
        )

    def _vertex_coords(self, v):
        """Convert vertex index to (+/- 1, +/- 1, +/- 1) coordinates."""
        x = 1 if (v & 4) else -1
        y = 1 if (v & 2) else -1
        z = 1 if (v & 1) else -1
        return (x, y, z)

    def _edge_length(self, v1, v2):
        """Euclidean distance between two vertices."""
        c1 = self._vertex_coords(v1)
        c2 = self._vertex_coords(v2)
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    def _compute_tet_edges(self, tet_vertices):
        """Compute all pairwise distances within a tetrahedron."""
        verts = list(tet_vertices)
        edges = []
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                edges.append(self._edge_length(verts[i], verts[j]))
        return edges

    def model(self) -> Model:
        expected_length = 2.0 * math.sqrt(2.0)

        edges_a = self._compute_tet_edges(TET_A)
        edges_b = self._compute_tet_edges(TET_B)

        edges_per_tet_a = float(len(edges_a))
        edges_per_tet_b = float(len(edges_b))

        mean_length_a = sum(edges_a) / len(edges_a)
        mean_length_b = sum(edges_b) / len(edges_b)

        max_deviation_a = max(abs(e - expected_length) for e in edges_a)
        max_deviation_b = max(abs(e - expected_length) for e in edges_b)
        max_deviation = max(max_deviation_a, max_deviation_b)

        return (
            Model()
            .add("Tet A edge count", edges_per_tet_a)
            .add("Tet B edge count", edges_per_tet_b)
            .add("Tet A mean edge length", mean_length_a)
            .add("Tet B mean edge length", mean_length_b)
            .add("Max deviation from regularity", max_deviation)
        )

    def observations(self) -> Observed:
        expected_length = 2.0 * math.sqrt(2.0)
        return (
            Observed()
            .add("Tet A edge count", 6.0)
            .add("Tet B edge count", 6.0)
            .add("Tet A mean edge length", expected_length)
            .add("Tet B mean edge length", expected_length)
            .add("Max deviation from regularity", 0.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Tetrahedral Edge Regularity from Binary Parity Partition",
        summary="Verifies that parity partitioned cube vertices form two congruent regular tetrahedra",
        test_classes=[TetrahedralEdgeRegularity],
    )
