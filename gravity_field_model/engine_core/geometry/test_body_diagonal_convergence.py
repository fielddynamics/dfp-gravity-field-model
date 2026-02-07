# FILENAME: test_body_diagonal_convergence.py

"""
Body Diagonal Convergence at the Field Origin
==============================================

The stellated octahedron has four body diagonals, each connecting a
complementary pair of vertices (V0,V7), (V1,V6), (V2,V5), (V3,V4).
Standard Euclidean geometry tells us that the body diagonals of a cube
all pass through its geometric center. The question is whether this
center point, computed purely from the binary vertex encoding, coincides
with the GFM Field Origin at coordinates (0,0,0).

This test verifies that all four midpoints are identical and located at
the origin, establishing that the Field Origin is not an additional
postulate but a geometric consequence of the binary coordinate system.
It also confirms that all vertices are equidistant from this center,
with distance sqrt(3), as required by the dual Field Chamber geometry.

GFM OBSERVATION: The Field Origin (0,0,0) emerges as the unique intersection of all body diagonals.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    VERTICES, TET_A, TET_B, COMPLEMENTARY_PAIRS
)


# Vertex coordinate map: 3-bit binary index -> (+/-1, +/-1, +/-1)
COORDS = {
    0: (-1, -1, -1),
    1: (-1, -1, +1),
    2: (-1, +1, -1),
    3: (-1, +1, +1),
    4: (+1, -1, -1),
    5: (+1, -1, +1),
    6: (+1, +1, -1),
    7: (+1, +1, +1),
}


class BodyDiagonalConvergence(Test):
    """
    Validates that the four body diagonals of the stellated octahedron
    all intersect at a single point: the Field Origin at (0,0,0).

    PHYSICAL CONTEXT:
    In Euclidean geometry, a rectangular parallelepiped (including the cube)
    has body diagonals that bisect each other at the geometric center. For
    the unit cube with vertices at (+/- 1, +/- 1, +/- 1), this center is
    the origin. Each complementary pair (v, 7 minus v) connects vertices
    whose coordinates are sign reflections of each other, so their midpoint
    is necessarily (0,0,0). Furthermore every vertex sits at Euclidean
    distance sqrt(1^2 + 1^2 + 1^2) = sqrt(3) from the center.

    GFM OBSERVATION:
    The Field Origin, defined as the coupling interface where Tetrahedra A
    and B meet (GFM Textbook Ch.9 Sec.9.5), coincides exactly with the
    geometric center determined by the binary encoding. The number sqrt(3)
    equals sqrt(d) for d = 3 spatial dimensions. All 8 vertices are
    equidistant from this point, confirming its role as the unique center
    of the dual Field Chamber.

    EPISTEMIC STATUS:
    This is a geometric observation. The Field Origin location is a theorem
    of Euclidean geometry applied to the cube, not a GFM derivation.
    """

    name = "Body Diagonal Convergence at Field Origin"

    question = (
        "Do all four body diagonals of the stellated octahedron converge "
        "at a single point, and is that point the Field Origin (0,0,0)? "
        "The binary vertex encoding assigns coordinates (+/- 1, +/- 1, +/- 1) "
        "to each vertex. Each complementary pair sums to (0,0,0) by construction. "
        "This test verifies the convergence numerically and confirms that all "
        "8 vertices are equidistant from the intersection at distance sqrt(d) "
        "where d = 3."
    )

    reference = (
        "GFM Textbook Ch.9 Sec.9.5: Field Origin and body diagonals; "
        "Coxeter (1973) Regular Polytopes, Ch.4: cube diagonal properties"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "Standard Euclidean geometry guarantees that cube body diagonals "
        "bisect each other at the center. GFM identifies this center as "
        "the Field Origin: the coupling interface between the two tetrahedra. "
        "The observation that all four complementary pairs share the same "
        "midpoint is not a derivation from GFM principles but a geometric "
        "fact that GFM elevates to physical significance. The equidistance "
        "sqrt(3) = sqrt(d) connects the vertex distance to the spatial "
        "dimension count, reinforcing that d = 3 is encoded in the structure."
    )

    # Audit scoring
    audit_score = 83
    audit_notes = (
        "Question: 11/15 (asks a clear geometric question with specific numbers, but the answer is obvious from the setup, reducing mystery tension; saying 'sums to zero by construction' in the question itself deflates the hook). Derivation: 13/15 (good intuition first structure, clear progression from physical setup through midpoint calculation to GFM observation; minor issue: the tension step is weak because the result is self evident from signed coordinates, so there is no real puzzle to resolve). Commentary: 12/15 (delivers the key insight that the Field Origin is a consequence not a postulate, connects sqrt(3) to d=3, and is honest about epistemic status; lacks an analogy for non experts and does not state broader implications for other GFM results that depend on the Field Origin). Model: 9/10 (clean summary with 3 key values, good mix of count, deviation, and binary verdict style outputs; minor redundancy in computing midpoints twice in the code, though output itself is crisp). Observations: 8/10 (values are exact geometric facts, Coxeter reference is authoritative; the observed value 0.0 for deviation sum is a boundary case that could cause tolerance issues in some frameworks, but is mathematically correct). Constants: 8/10 (imports VERTICES, TET_A, TET_B, COMPLEMENTARY_PAIRS from common correctly; COORDS dictionary is hardcoded locally, which is justified since coordinates are not available in common, but this should be noted; no physics constants needed so no CODATA issue). Accessibility: 13/15 (undergrads can follow the midpoint and distance arguments easily; the connection between binary encoding and sign reflection is clearly explained; could benefit from a simple analogy such as comparing body diagonals to threads through a bead at the center). Header: 9/10 (comprehensive module docstring covering what is tested, why it matters, the GFM observation, and epistemic status; missing explicit target audience level and could mention relationship to the existing binary encoding tests in the suite)."
    )

    academic_paper = """\
Body Diagonal Convergence and the Geometric Origin of the Field Origin in the Stellated Octahedron A numerical verification that all four body diagonals intersect at (0,0,0) with zero deviation AUTHOR GFM Research Agent ABSTRACT The Gravity Field Model assigns physical significance to the Field Origin, the point where two interpenetrating tetrahedra couple. A natural question arises: is this point an independent postulate, or does it follow from the coordinate structure? We compute the midpoints of all four complementary vertex pairs in the stellated octahedron and verify that each midpoint coincides exactly with (0,0,0), yielding a total squared deviation of 0.00. We further confirm that all eight vertices are equidistant from this point at distance sqrt(3), which equals sqrt(d) for d = 3 spatial dimensions. The Field Origin is a geometric consequence of the binary vertex encoding, not an additional axiom. 1. INTRODUCTION 1.1 The Field Origin as a Central Concept The Gravity Field Model (GFM) describes gravity as the internal dynamics of a stellated octahedron: two interpenetrating tetrahedra sharing a common center called the Field Origin. This center, located at coordinates (0,0,0), serves as the coupling interface between the two chambers. The gravitational constant G, electron spin, and the constitutive law mu(x) = x/(1+x) all depend on properties defined at this point (Paper VI, Section 8; Paper VII, Sections 3.3 and 4.1). Given its foundational role, establishing the geometric necessity of the Field Origin is essential. 1.2 The Geometric Question The stellated octahedron has eight vertices, labeled 0 through 7 using a 3 bit binary encoding. Each vertex maps to a corner of the cube at coordinates (+/- 1, +/- 1, +/- 1). Four complementary pairs, (0,7), (1,6), (2,5), and (3,4), connect vertices related by the XOR operation with 7. Each pair spans both tetrahedra. The question is whether these four body diagonals share a common intersection, and whether that intersection coincides with the origin. 1.3 Structure of This Paper Section 2 presents the coordinate geometry underlying the binary vertex encoding. Section 3 computes the midpoints and vertex distances. Section 4 reports the numerical results. Section 5 discusses the physical interpretation and scope. 2. THE GEOMETRY 2.1 Binary Coordinates and Complementary Pairs Each vertex index v in {0, 1, ..., 7} encodes a position in three dimensional space. The coordinate along each axis is determined by the corresponding bit: 0 maps to -1 and 1 maps to +1. Vertex 0 = (000) sits at (-1, -1, -1), while vertex 7 = (111) sits at (+1, +1, +1). The complement of vertex v is 7 minus v, equivalently v XOR 7, which flips all three coordinate signs. This operation always changes the bit parity, ensuring complementary vertices belong to opposite tetrahedra (Coxeter 1973, Ch. 4). 2.2 Why Midpoints Reveal the Center A body diagonal connects two vertices whose coordinates are exact negatives of each other. Consider a vertex at position (x, y, z). Its complement sits at (-x, -y, -z). The midpoint is ((x + (-x))/2, (y + (-y))/2, (z + (-z))/2) = (0, 0, 0). This cancellation is exact for every pair, because the binary encoding guarantees that complementation is equivalent to coordinate sign inversion. If all four midpoints coincide, the diagonals share a unique intersection. 3. FROM STRUCTURE TO CALCULATION 3.1 Midpoint Computation For each of the four complementary pairs, we compute the midpoint and its squared distance from the origin. Denoting the coordinates of vertex v1 as c1 and of vertex v2 as c2, the midpoint is m = (c1 + c2) / 2. The total squared deviation is the sum of |m|^2 across all four pairs. If this sum vanishes, every midpoint lies exactly at the origin. 3.2 Equidistance Verification The Euclidean distance from the origin to any vertex (+/- 1, +/- 1, +/- 1) is sqrt(1^2 + 1^2 + 1^2) = sqrt(3). This value equals sqrt(d) where d = 3 is the spatial dimension. We count how many of the eight vertices satisfy this condition to within numerical precision (tolerance 10^-12). 4. RESULTS 4.1 Numerical Outcomes The test produces three quantities. Midpoints at origin: model value 4, observed value 4, deviation 0.00%. Midpoint deviation sum: model value 0.0, observed value 0.0, deviation 0.00%. Vertices equidistant from origin: model value 8, observed value 8, deviation 0.00%. All three comparisons match exactly. The test passes with zero error on every metric. 4.2 Robustness The result is not approximate. The cancellation of coordinates in each complementary pair is algebraically exact, not dependent on numerical precision or parameter tuning. Any coordinate system that assigns (+/- 1, +/- 1, +/- 1) to cube vertices and defines complementation as full sign inversion will produce the same outcome. The only requirement is that the cube be centered at the origin, which the binary encoding guarantees by construction. 5. DISCUSSION 5.1 Physical Interpretation The Field Origin in GFM serves multiple roles: it is the coupling interface between the two tetrahedra, the point where angular momentum transfers between chambers (yielding spin 1/2 via the time face fraction 2/8), and the location where the gravitational coupling hierarchy of depth 21 originates. This test establishes that the Field Origin does not require independent specification. It emerges as the unique point equidistant from all eight vertices and common to all four body diagonals. Analogously, just as the center of mass of a symmetric body follows from the mass distribution rather than from external definition, the Field Origin follows from the vertex coordinates. 5.2 Scope and Limitations This result is a theorem of Euclidean geometry, not a GFM derivation. The physical claim that this geometric center functions as a coupling interface between dual tetrahedra is a separate assertion that depends on the broader GFM framework. The present test validates the geometric prerequisite: the center exists, is unique, and is equidistant from all vertices at distance sqrt(3) = sqrt(d). The connection between sqrt(d) and the spatial dimension count d = 3 is noted as an observation. 6. CONCLUSION All four body diagonals of the stellated octahedron converge at a single
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD PHYSICS: In a cube with vertices at "
                "(+/- 1, +/- 1, +/- 1), each body diagonal connects a "
                "vertex (x, y, z) to its antipode (-x, -y, -z)."
            )
            .step(
                "The midpoint of any such pair is "
                "((x + (-x))/2, (y + (-y))/2, (z + (-z))/2) = (0, 0, 0)."
            )
            .equation("midpoint = (v_i + v_complement) / 2 = (0, 0, 0) for all i")
            .step(
                "Since all four midpoints are (0,0,0), the diagonals "
                "intersect at exactly one point: the geometric center."
            )
            .step(
                "The Euclidean distance from (0,0,0) to any vertex "
                "(+/- 1, +/- 1, +/- 1) is sqrt(1^2 + 1^2 + 1^2) = sqrt(3)."
            )
            .step(
                "GFM OBSERVATION: This unique intersection point is the "
                "Field Origin, the coupling interface where Tet A and Tet B "
                "meet. The distance sqrt(3) = sqrt(d) ties the geometry to "
                "the spatial dimension count d = 3."
            )
            .conclude(
                "All 4 body diagonals converge at (0,0,0). All 8 vertices "
                "are equidistant from this point at distance sqrt(3). The "
                "Field Origin is a geometric consequence of the binary "
                "vertex encoding, not an independent postulate."
            )
        )

    def model(self) -> Model:
        # Compute midpoints of all 4 complementary pairs
        # and check they all equal (0,0,0).
        # Sum of squared deviations from origin across all midpoints.
        midpoint_deviation_sum = 0.0
        for v1, v2 in COMPLEMENTARY_PAIRS:
            c1 = COORDS[v1]
            c2 = COORDS[v2]
            mx = (c1[0] + c2[0]) / 2.0
            my = (c1[1] + c2[1]) / 2.0
            mz = (c1[2] + c2[2]) / 2.0
            midpoint_deviation_sum += mx**2 + my**2 + mz**2

        # Count how many of the 4 midpoints are exactly (0,0,0)
        midpoints_at_origin = 0
        for v1, v2 in COMPLEMENTARY_PAIRS:
            c1 = COORDS[v1]
            c2 = COORDS[v2]
            mx = (c1[0] + c2[0]) / 2.0
            my = (c1[1] + c2[1]) / 2.0
            mz = (c1[2] + c2[2]) / 2.0
            if mx == 0.0 and my == 0.0 and mz == 0.0:
                midpoints_at_origin += 1

        # Compute distances from origin to all 8 vertices
        # and check they all equal sqrt(3)
        d = 3
        expected_distance = math.sqrt(d)
        distances_match = 0
        for v in range(8):
            c = COORDS[v]
            dist = math.sqrt(c[0]**2 + c[1]**2 + c[2]**2)
            if abs(dist - expected_distance) < 1e-12:
                distances_match += 1

        return (
            Model()
            .add("Midpoints at origin", float(midpoints_at_origin))
            .add("Midpoint deviation sum", midpoint_deviation_sum)
            .add("Vertices equidistant from origin", float(distances_match))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Midpoints at origin", 4.0)
            .add("Midpoint deviation sum", 0.0)
            .add("Vertices equidistant from origin", 8.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Body Diagonal Convergence at the Field Origin",
        summary="Verifies all 4 body diagonals intersect at (0,0,0) and all 8 vertices are equidistant at sqrt(3)",
        test_classes=[BodyDiagonalConvergence],
    )
