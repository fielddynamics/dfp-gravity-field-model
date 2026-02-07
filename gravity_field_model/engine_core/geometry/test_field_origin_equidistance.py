# FILENAME: test_field_origin_equidistance.py

"""
Field Origin Equidistance from Stellated Octahedron Vertices
============================================================

The stellated octahedron (two interpenetrating tetrahedra) has 8 vertices
placed at the corners of a cube with coordinates (+/- 1, +/- 1, +/- 1).
The geometric center of this structure sits at (0, 0, 0), the point GFM
identifies as the Field Origin: where the two tetrahedra couple, where
body diagonals intersect, and where mass energy is bound (t = 0).

Standard geometry guarantees that the center of a cube is equidistant from
all its vertices. The distance is sqrt(1^2 + 1^2 + 1^2) = sqrt(3) for a
unit cube with vertices at +/- 1. This metric property is what makes the
Field Origin physically meaningful: it is the unique point of maximal
symmetry, equally coupled to every vertex in both Chamber A and Chamber B.

The existing binary encoding tests validate the combinatorial properties
(parity, XOR, counting) but never confirm this metric foundation. This
test bridges that gap: verifying that all 8 vertices, across both
tetrahedra, lie at identical Euclidean distance sqrt(3) from the origin.

GFM OBSERVATION: The Field Origin at (0,0,0) is equidistant from all 2^d = 8
vertices at distance sqrt(d) = sqrt(3), a metric consequence of the cube
geometry that underlies the bimetric coupling symmetry.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B
)


class FieldOriginEquidistance(Test):
    """
    Validates that the Field Origin at (0,0,0) is equidistant from all 8
    vertices of the stellated octahedron, and that this distance equals
    sqrt(3).

    PHYSICAL CONTEXT:
    In Euclidean geometry, the center of a cube with vertices at coordinates
    (+/- 1, +/- 1, +/- 1) is equidistant from all 8 corners. The distance
    from the origin to any vertex (a, b, c) where a, b, c are each +1 or
    -1 is sqrt(a^2 + b^2 + c^2) = sqrt(3). This is a standard result from
    solid geometry (Coxeter, Regular Polytopes, 1973). The property holds
    regardless of which tetrahedron a vertex belongs to, establishing the
    center as a point of full octahedral symmetry.

    GFM OBSERVATION:
    GFM identifies this geometric center as the Field Origin, the coupling
    interface between Chamber A (Tet A) and Chamber B (Tet B). The equal
    distance sqrt(d) = sqrt(3) from all 2^d = 8 vertices means the Field
    Origin has no bias toward either tetrahedron. This metric symmetry is
    the geometric foundation for bimetric balance: the two tetrahedra
    contribute equally to field closure at the coupling point. The distance
    sqrt(3) also connects spatial dimension d = 3 directly to the metric
    structure, since sqrt(d) arises from summing d unit squared coordinates.

    EPISTEMIC STATUS:
    The equidistance property is a geometric theorem (standard Euclidean
    geometry). The identification of this center as the physically meaningful
    Field Origin is a GFM observation, not a derivation from first principles.
    """

    name = "Field Origin Equidistance"

    question = (
        "Why is the geometric center of the stellated octahedron equidistant "
        "from all 8 vertices, and why does this distance equal sqrt(3)? "
        "The equidistance follows from cube symmetry: each vertex has "
        "coordinates that are +1 or -1 along all three axes, so every "
        "vertex lies at the same distance sqrt(1^2 + 1^2 + 1^2) = sqrt(3) "
        "from the origin. Does this metric property underpin the bimetric "
        "balance required for field closure?"
    )

    reference = (
        "Coxeter, Regular Polytopes (1973); "
        "GFM Textbook Ch.9 Sec.9.5: Field Origin and body diagonals"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "Standard Euclidean geometry guarantees that the center of a cube "
        "is equidistant from all vertices. For unit coordinates +/- 1, the "
        "distance is sqrt(3) in d = 3 dimensions. GFM observes that this "
        "metric symmetry is the foundation of the Field Origin concept: "
        "the coupling interface must be unbiased toward either tetrahedron. "
        "This is an observation connecting standard geometry to GFM structure, "
        "not a derivation of new physics. The test also confirms that "
        "Tet A and Tet B vertices individually share this equidistance, "
        "verifying that bimetric balance holds at the metric level and not "
        "only at the combinatorial level established by parity tests."
    )

    # Audit scoring
    audit_score = 83
    audit_notes = (
        "Question: 11/15 (asks why but partially answers itself within the question text, reducing mystery; the final sentence about bimetric balance is the real hook but arrives late). Derivation: 12/15 (clear logical progression, good use of equation step, but the physical setup lacks a tension or puzzle stage; it proceeds directly to an obvious geometric fact without first establishing why equidistance matters or what would go wrong without it). Commentary: 12/15 (solid interpretation, correctly labels observation vs derivation, connects metric to combinatorial level nicely, but lacks an analogy for accessibility and does not state broader implications for other GFM results that depend on the Field Origin). Model: 9/10 (clean summary statistics with 5 well chosen values; variance as a zero check is smart; per tetrahedron breakdown adds meaningful structure). Observations: 7/10 (values are mathematically exact and correct, Coxeter citation is given, but the observed values are computed from math.sqrt(3.0) rather than referenced from an external authoritative table; the variance comparison at 0.0 may cause floating point issues with tolerance checking). Constants: 9/10 (K, VERTICES, TET_A, TET_B properly imported from common; d=3 used as literal consistent with project rules; minor note that K is imported but never used in computation). Accessibility: 13/15 (undergrad can follow the geometry, docstring explains coordinates clearly, epistemic status section is excellent, but assumes familiarity with terms like bimetric balance and coupling interface without defining them for newcomers). Header: 10/10 (comprehensive module docstring covers physical domain, what is verified, epistemic status clearly labeled as observation, references both standard geometry and GFM textbook, scope and limitations stated)."
    )

    academic_paper = """\
TITLE Metric Equidistance of the Field Origin in the Stellated Octahedron ABSTRACT This investigation verifies that the geometric center of the stellated octahedron is equidistant from all 8 vertices at distance sqrt(3). The model computes distances, variance, and per tetrahedron means. GFM observes that this metric symmetry underlies bimetric coupling balance. This is an OBSERVATION, not a derivation. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The stellated octahedron, formed by two interpenetrating tetrahedra, places its 8 vertices at the corners of a cube with coordinates (+/- 1, +/- 1, +/- 1). The geometric center at (0, 0, 0) serves a distinguished role in the Gravity Field Model as the Field Origin: the coupling interface between Chamber A (Tet A, vertices 1, 2, 4, 7) and Chamber B (Tet B, vertices 0, 3, 5, 6). Multiple GFM results depend on this point, including the spin derivation (Section 4.3 of the core theory), the E = mc^2 interpretation (Section 4.4), and the coupling hierarchy (Section 4.2). Standard Euclidean geometry establishes that the center of a cube is equidistant from all its vertices. For a cube with unit coordinates, this distance is sqrt(1^2 + 1^2 + 1^2) = sqrt(3). This is a theorem from solid geometry documented by Coxeter (Regular Polytopes, 1973). Previous tests in the historical systems domain validated the combinatorial properties of the vertex encoding: parity classification, XOR complementation, cross tetrahedral pairing, and vertex counting. However, no test confirmed the metric foundation. This investigation bridges that gap by verifying equidistance numerically and checking that neither tetrahedron is metrically privileged relative to the center. 2. METHODOLOGY The model assigns coordinates to each vertex using the 3 bit binary encoding: bit 2 controls the x axis, bit 1 controls y, and bit 0 controls z. A set bit maps to +1, a clear bit maps to -1. The Euclidean distance from the origin (0, 0, 0) to each vertex is computed. Five quantities are reported: the mean distance across all 8 vertices, the variance in distances (testing perfect equidistance), the mean distance for Tet A vertices alone, the mean distance for Tet B vertices alone, and the theoretical expectation sqrt(d) where d = 3. Agreement requires all values to match within 1% tolerance. The variance must equal zero. 3. RESULTS Model output: Distance to vertex from origin: 1.7321 (sqrt(3)) Distance variance: 0.0000 Tet A mean distance: 1.7321 Tet B mean distance: 1.7321 Expected distance sqrt(d): 1.7321 All 8 individual vertex distances equal sqrt(3) exactly. The variance is identically zero, confirming perfect equidistance. The per tetrahedron means are identical to each other and to the global mean. No vertex deviates from sqrt(3) by any amount. The result sqrt(3) = sqrt(d) connects the metric structure directly to the spatial dimensionality d = 3. This relationship generalizes: in a d dimensional hypercube with +/- 1 coordinates, all 2^d vertices lie at distance sqrt(d) from the center. 4. DISCUSSION The equidistance property is geometrically guaranteed and the test confirms it computationally. The physical significance within GFM is that the Field Origin couples to both tetrahedra without metric bias. Neither Chamber A nor Chamber B is closer to or farther from the coupling interface. This metric symmetry complements the combinatorial symmetry (equal vertex counts, cross tetrahedral pairing) established by existing tests. EPISTEMIC STATUS: OBSERVATION. The equidistance is a standard geometric theorem. GFM observes that this property is consistent with the requirement for bimetric balance at the Field Origin. GFM does not derive the equidistance; it identifies the geometric center as physically meaningful and notes that the metric structure supports that identification. The distance sqrt(3) encoding d = 3 is consistent with the broader GFM theme that spatial dimensionality is not arbitrary but appears throughout the geometry. 5. LIMITATIONS AND HONESTY STATEMENT This test verifies a standard geometric property. It does not prove that the Field Origin has physical significance, only that its metric properties are consistent with the role GFM assigns to it. The coordinates +/- 1 are a convention; rescaling would change the absolute distance while preserving equidistance. The test assumes Euclidean metric, which is appropriate for the coordinate framework but does not address curved spacetime contexts. 6. CONCLUSION We confirm that all 8 vertices of the stellated octahedron
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: The stellated octahedron has 8 vertices "
                "at the corners of a cube with coordinates (s1, s2, s3) where "
                "each si is +1 or -1."
            )
            .step(
                "The geometric center is at (0, 0, 0), the arithmetic mean "
                "of all vertex positions."
            )
            .step(
                "The Euclidean distance from origin to any vertex (s1, s2, s3) is:"
            )
            .equation("dist = sqrt(s1^2 + s2^2 + s3^2) = sqrt(1 + 1 + 1) = sqrt(3)")
            .step(
                "Since s_i^2 = 1 for all i regardless of sign, every vertex "
                "is at identical distance sqrt(3) from the center."
            )
            .step(
                "The variance in distances across all 8 vertices is exactly 0, "
                "confirming perfect equidistance."
            )
            .step(
                "GFM OBSERVATION: This metric symmetry means the Field Origin "
                "couples equally to both tetrahedra. Neither Chamber A nor "
                "Chamber B is metrically privileged. The distance sqrt(d) = "
                "sqrt(3) encodes the spatial dimensionality directly into "
                "the coupling geometry."
            )
            .conclude(
                "All 8 vertices lie at distance sqrt(3) from the Field Origin "
                "with zero variance, confirming the metric foundation of "
                "bimetric balance in the stellated octahedron."
            )
        )

    def model(self) -> Model:
        # Vertex coordinates: 3-bit binary -> (+/-1, +/-1, +/-1)
        coords = {}
        for v in range(8):
            x = 1.0 if (v & 4) else -1.0
            y = 1.0 if (v & 2) else -1.0
            z = 1.0 if (v & 1) else -1.0
            coords[v] = (x, y, z)

        # Compute distance from origin to each vertex
        distances = []
        for v in range(8):
            x, y, z = coords[v]
            dist = math.sqrt(x**2 + y**2 + z**2)
            distances.append(dist)

        # Mean distance across all 8 vertices
        mean_dist = sum(distances) / len(distances)

        # Variance in distances (should be 0 for perfect equidistance)
        variance = sum((d - mean_dist)**2 for d in distances) / len(distances)

        # Separate checks: mean distance for Tet A and Tet B vertices
        tet_a_dists = [distances[v] for v in TET_A]
        tet_b_dists = [distances[v] for v in TET_B]
        mean_a = sum(tet_a_dists) / len(tet_a_dists)
        mean_b = sum(tet_b_dists) / len(tet_b_dists)

        # Expected distance from geometry: sqrt(d) where d = 3
        d = 3
        expected_dist = math.sqrt(float(d))

        return (
            Model()
            .add("Distance to vertex from origin", mean_dist)
            .add("Distance variance", variance)
            .add("Tet A mean distance", mean_a)
            .add("Tet B mean distance", mean_b)
            .add("Expected distance sqrt(d)", expected_dist)
        )

    def observations(self) -> Observed:
        expected = math.sqrt(3.0)
        return (
            Observed()
            .add("Distance to vertex from origin", expected)
            .add("Distance variance", 0.0)
            .add("Tet A mean distance", expected)
            .add("Tet B mean distance", expected)
            .add("Expected distance sqrt(d)", expected)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Field Origin Equidistance Test",
        summary="Validates that all 8 stellated octahedron vertices are equidistant from the Field Origin at sqrt(3)",
        test_classes=[FieldOriginEquidistance],
    )
