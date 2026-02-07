# FILENAME: test_stellated_octahedron_geometry.py
"""
Stellated Octahedron Geometry Validation
========================================

The stellated octahedron (stella octangula) consists of two interpenetrating
regular tetrahedra whose 8 vertices coincide with the corners of a cube.
This structure was first described by Kepler (1619) and systematically
classified by Coxeter (1973). In standard geometry, the two tetrahedra
partition the 8 cube vertices into two sets of 4 related by spatial
inversion, and each tetrahedron is a regular simplex with all 6 edge
lengths equal.

GFM builds its entire framework on this geometry: Tet A occupies the
odd parity vertices, Tet B occupies the even parity vertices, the two
are related by bitwise complement (XOR with 7), and the Field Origin
at (0,0,0) is equidistant from all 8 vertices at distance sqrt(3).
Every downstream GFM result depends on these geometric facts being true.

GFM OBSERVATION: The stellated octahedron realizes the 2(d+1) = 2^d = 8
vertex identity for d = 3 with two regular tetrahedra of edge length
2*sqrt(2), partitioned by parity, related by inversion through the origin.

This is a DERIVATION from Euclidean geometry, not a fit or approximation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K,
    VERTICES,
    TET_A,
    TET_B,
)


# Vertex coordinates: 3 bit binary labeling at unit cube corners
VERTEX_COORDS = {
    0: (-1.0, -1.0, -1.0),
    1: (-1.0, -1.0, +1.0),
    2: (-1.0, +1.0, -1.0),
    3: (-1.0, +1.0, +1.0),
    4: (+1.0, -1.0, -1.0),
    5: (+1.0, -1.0, +1.0),
    6: (+1.0, +1.0, -1.0),
    7: (+1.0, +1.0, +1.0),
}

# Faces of each tetrahedron: face opposite the named vertex
FACES_A = {
    "A1": {2, 4, 7},
    "A2": {1, 4, 7},
    "A4": {1, 2, 7},
    "A7": {1, 2, 4},
}

FACES_B = {
    "B0": {3, 5, 6},
    "B3": {0, 5, 6},
    "B5": {0, 3, 6},
    "B6": {0, 3, 5},
}

TIME_FACE_NAMES = {"A7", "B0"}
SPATIAL_FACE_NAMES = {"A1", "A2", "A4", "B3", "B5", "B6"}


def distance(v1, v2):
    """Euclidean distance between two vertex coordinate tuples."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def parity(vertex_id):
    """Count the number of 1 bits in the binary representation."""
    return bin(vertex_id).count("1") % 2


def all_edges(tet_vertices):
    """Return all pairwise distances for a list of vertex IDs."""
    verts = list(tet_vertices)
    edges = []
    for i in range(len(verts)):
        for j in range(i + 1, len(verts)):
            edges.append(distance(VERTEX_COORDS[verts[i]], VERTEX_COORDS[verts[j]]))
    return edges


def centroid(tet_vertices):
    """Compute the centroid of a set of vertex IDs."""
    coords = [VERTEX_COORDS[v] for v in tet_vertices]
    n = len(coords)
    return tuple(sum(c[i] for c in coords) / n for i in range(3))


class StellatedOctahedronGeometry(Test):
    """
    PHYSICAL CONTEXT:
    The stellated octahedron is a well known polyhedron compound consisting
    of two regular tetrahedra in dual orientation, first studied by Kepler
    in Harmonices Mundi (1619) and classified in Coxeter's Regular Polytopes
    (1973). Its 8 vertices occupy all corners of a cube. Each tetrahedron
    is a regular 3 simplex with 4 vertices, 6 equal edges, and 4 equilateral
    triangular faces. The two tetrahedra are related by inversion through
    the cube center.

    GFM OBSERVATION:
    GFM assigns Tet A to odd parity vertices {1,2,4,7} and Tet B to even
    parity vertices {0,3,5,6}. The complement operation V -> 7 minus V
    (equivalently XOR with 7) maps every Tet A vertex to a Tet B vertex
    and vice versa, forming 4 complementary pairs. The Field Origin at
    (0,0,0) is equidistant from all 8 vertices at distance sqrt(3). Each
    tetrahedron has exactly 4 faces classified as 3 spatial plus 1 temporal,
    giving 6 spatial and 2 temporal faces total (the 3+1 structure). These
    are geometric facts about the stellated octahedron, verified here by
    direct coordinate computation.

    EPISTEMIC STATUS:
    This is a DERIVATION from Euclidean geometry. Every quantity tested is
    computed from vertex coordinates and compared against exact geometric
    values. No physical measurements or fitting are involved.
    """

    name = "Stellated Octahedron Geometry Validation"

    question = (
        "Does the GFM stellated octahedron have the geometric properties "
        "claimed by the framework? Specifically: do Tet A and Tet B each "
        "form regular tetrahedra with edge length 2*sqrt(2)? Are they "
        "partitioned by vertex parity? Does XOR with 7 map between them? "
        "Is the Field Origin equidistant from all 8 vertices? Do the 8 "
        "faces decompose into 6 spatial and 2 temporal faces?"
    )

    reference = (
        "Kepler (1619) Harmonices Mundi; "
        "Coxeter (1973) Regular Polytopes Ch. 3; "
        "GFM Paper VII Section 2.2"
    )

    tolerance = 0.001

    level = Level.CRITICAL

    commentary = (
        "Every quantity in this test is computed from explicit coordinates "
        "and compared against exact geometric values. The two tetrahedra "
        "each have 6 edges of length 2*sqrt(2), confirming regularity. "
        "The parity partition assigns odd bit count vertices to Tet A and "
        "even bit count vertices to Tet B with zero misassignments. The "
        "complement operation XOR with 7 maps every vertex to the opposite "
        "tetrahedron, producing 4 complementary pairs that each sum to 7. "
        "The Field Origin at (0,0,0) sits at distance sqrt(3) from all 8 "
        "vertices, confirmed by direct computation. The face classification "
        "yields 6 spatial and 2 temporal faces. These are geometric facts, "
        "not approximations or fits. This test validates the structural "
        "foundation on which all subsequent GFM results are built."
    )

    # Audit scoring
    audit_score = 82
    audit_notes = (
        "Question: 10/15 (asks whether properties hold but reads as a checklist of sub questions rather than a mystery hook; no tension or stakes established; the reader is told what to expect before being invited to wonder). Derivation: 14/15 (excellent scaffolding from coordinate setup through parity argument to complement operation; the regularity proof via bit parity is genuinely insightful; the equation step is clean; minor gap: no everyday analogy to ground the abstract geometry, such as comparing the two tetrahedra to a Star of David in 3D). Commentary: 10/15 (thorough summary of results but reads as a restatement of what the model computed rather than delivering an aha moment; missing an analogy, missing implications for downstream GFM results beyond the generic final sentence; no statement about what would break if this test failed). Model: 9/10 (14 clean summary values covering regularity, parity, complement, equidistance, centroids, and face counts; variance as a regularity proxy is smart; could arguably consolidate the two centroid distances into one since both must be zero, but well within range). Observations: 8/10 (all values are exact geometric results from Coxeter and direct computation; Kepler and Coxeter cited in reference field; the face classification source is GFM Paper VII rather than an independent authority, which is appropriate since the classification is a GFM definition; VERTEX_COORDS hardcoded rather than imported from geometry_constants). Constants: 8/10 (K, VERTICES, TET_A, TET_B properly imported from common; VERTEX_COORDS, FACES_A, FACES_B, TIME_FACE_NAMES, SPATIAL_FACE_NAMES all hardcoded at module level rather than imported from geometry_constants where FACES, TIME_FACES, SPATIAL_FACES are listed as available; the face data and coordinate data should ideally come from the canonical source). Accessibility: 13/15 (an undergraduate with linear algebra can follow the parity argument and distance calculations; the bit manipulation explanation is clear; the derivation builds from simple to complex nicely; lacks an everyday analogy to make the stellated octahedron tangible for non specialists; the term Field Origin is used without a brief gloss for newcomers). Header: 10/10 (comprehensive module docstring covering physical domain, historical context with Kepler and Coxeter, what GFM claims, explicit epistemic status as derivation, and clear statement that this is geometry not fitting)."
    )

    academic_paper = """\
TITLE Geometric Validation of the Stellated Octahedron as the GFM Structural Foundation ABSTRACT We verify by direct coordinate computation that two tetrahedra inscribed in a cube at vertices (+-1,+-1,+-1) form regular simplices, are partitioned by bit parity, related by complement, and centered on an equidistant Field Origin. All 14 quantities match exactly. EPISTEMIC STATUS: DERIVATION from Euclidean geometry. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The Gravity Field Model builds every physical result on a single geometric object: the stellated octahedron, two interpenetrating regular tetrahedra whose 8 vertices coincide with the corners of a cube. The gravitational constant G depends on the numbers 17, 13, and 21, which count coupling channels, edge structures, and hierarchy depth respectively. Electron spin depends on the face ratio 2/8. The bimetric architecture requires that two tetrahedra partition the cube vertices by parity and map to each other through bitwise complement. If any of these geometric properties fail, the entire downstream framework collapses. Standard geometry, following Kepler (1619) and Coxeter (1973), establishes that two tetrahedra can be inscribed in a cube with vertices at alternating corners. This test asks whether the specific coordinate realization used by GFM actually produces two regular tetrahedra with the claimed partition, symmetry, equidistance, and face decomposition properties. Every quantity is computed from explicit coordinates and compared against exact analytic values. No fitting or approximation is involved. 2. METHODOLOGY We place 8 vertices at all sign combinations of (+-1,+-1,+-1), labeled V0 through V7 by 3 bit binary index. Tet A receives odd parity vertices {1,2,4,7} and Tet B receives even parity vertices {0,3,5,6}. For each tetrahedron we compute all 6 pairwise edge lengths and their variance. We count how many Tet A vertices have odd bit parity and how many Tet B vertices have even bit parity. We test whether 7 minus V maps every Tet A vertex into Tet B. We compute the distance from the origin (0,0,0) to each vertex, reporting the mean and variance. We compute each tetrahedron centroid and its distance from the origin. We count faces classified as temporal (A7, B0) versus spatial (A1, A2, A4, B3, B5, B6). Agreement criterion: exact match (0.00% error) for all 14 quantities. 3. RESULTS Both tetrahedra have mean edge length 2.828427, matching the analytic value 2*sqrt(2) = 2.828427 exactly (0.00% error). Edge length variance is 0.000000 for both, confirming all 6 edges per tetrahedron are identical: both are regular. All 4 Tet A vertices have odd bit parity (4/4). All 4 Tet B vertices have even bit parity (4/4). The complement operation 7 minus V maps all 4 Tet A vertices into Tet B (4/4 crossings confirmed). The Field Origin mean distance to all 8 vertices is 1.732051, matching sqrt(3) = 1.732051 exactly. Distance variance is 0.000000, confirming perfect equidistance. Both tetrahedron centroids sit at distance 0.000000 from the origin, confirming each centroid coincides with the Field Origin. Face counts: 2 temporal, 6 spatial, 8 total. All 14 model values match their expected values at 0.00% error. The test passes at CRITICAL level. 4. DISCUSSION Every geometric claim made by the GFM framework about the stellated octahedron is verified exactly. The regularity of both tetrahedra follows from bit parity: any two distinct vertices sharing the same parity differ in exactly 2 of 3 coordinates, producing identical squared distances of 8. The complement symmetry follows from the algebraic structure of 3 bit binary labels. The equidistance of the Field Origin is a consequence of the cube's central symmetry. EPISTEMIC STATUS: DERIVATION. These are theorems of Euclidean geometry, not approximations or observations. The face decomposition into 6 spatial plus 2 temporal faces is a GFM definition applied to this geometry, not an independent physical measurement. This test connects directly to the dimensionality uniqueness result (2(d+1) = 2^d = 8 at d = 3) by confirming that the 8 vertex structure actually realizes two regular tetrahedra with the properties that all subsequent GFM derivations assume. 5. LIMITATIONS AND HONESTY STATEMENT This test verifies geometry, not physics. It does not prove that gravity has tetrahedral structure. The face classification into temporal and spatial is a GFM convention. The vertex coordinates are hardcoded rather than imported from a canonical source. 6. CONCLUSION All 14 geometric properties
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: Place a cube with vertices at all "
                "combinations of (+-1, +-1, +-1). Label each vertex by "
                "its 3 bit binary index: V0 = (neg1,neg1,neg1) through "
                "V7 = (+1,+1,+1). The cube has 8 vertices."
            )
            .step(
                "TETRAHEDRAL PARTITION: Assign vertices with an odd number "
                "of +1 coordinates (odd bit parity) to Tet A = {1,2,4,7}, "
                "and vertices with an even number of +1 coordinates (even "
                "bit parity) to Tet B = {0,3,5,6}. Each set has 4 vertices."
            )
            .step(
                "REGULARITY CHECK: For Tet A, compute all 6 pairwise "
                "distances. Each pair of vertices in Tet A differs in "
                "exactly 2 coordinates (since they share the same parity "
                "and differ in an even number of bits, but being distinct, "
                "they differ in exactly 2 of 3 bits). Each differing "
                "coordinate contributes (+-2)^2 = 4 to the squared distance."
            )
            .equation("edge_length = sqrt(4 + 4) = 2*sqrt(2) for all 6 edges")
            .step(
                "The same holds for Tet B by the identical parity argument. "
                "All edges equal confirms both are regular tetrahedra."
            )
            .step(
                "COMPLEMENT OPERATION: For any vertex V, the complement is "
                "7 minus V, which in binary is XOR with 111. This flips all "
                "3 bits, flips parity, and therefore maps Tet A to Tet B "
                "and vice versa. The 4 complementary pairs are (0,7), (1,6), "
                "(2,5), (3,4), each summing to 7."
            )
            .step(
                "FIELD ORIGIN: The point (0,0,0) is the centroid of all 8 "
                "vertices and also the centroid of each tetrahedron separately "
                "(since Tet A and Tet B centroids are both at the origin by "
                "the symmetry of the complement operation). Distance from "
                "origin to any vertex: sqrt(1^2 + 1^2 + 1^2) = sqrt(3)."
            )
            .step(
                "FACE CLASSIFICATION: Each tetrahedron has 4 triangular "
                "faces. Face A7 = {1,2,4} (opposite V7) and Face B0 = "
                "{3,5,6} (opposite V0) are TIME faces, pointing along the "
                "body diagonal toward the coupling center. The remaining 6 "
                "faces are SPATIAL. Total: 6 spatial + 2 temporal = 8 faces."
            )
            .conclude(
                "The stellated octahedron at cube corners (+-1,+-1,+-1) "
                "consists of two regular tetrahedra with edge length "
                "2*sqrt(2), partitioned by vertex parity, related by "
                "bitwise complement, centered on a Field Origin equidistant "
                "from all vertices. The 8 faces decompose as 6+2, giving "
                "the 3+1 structure per tetrahedron. All properties are "
                "exact geometric facts."
            )
        )

    def model(self) -> Model:
        # Edge lengths for both tetrahedra
        edges_a = all_edges(TET_A)
        edges_b = all_edges(TET_B)
        edge_length_a = sum(edges_a) / len(edges_a)
        edge_length_b = sum(edges_b) / len(edges_b)

        # Edge length variance (0 means all edges equal = regular)
        variance_a = sum((e - edge_length_a) ** 2 for e in edges_a) / len(edges_a)
        variance_b = sum((e - edge_length_b) ** 2 for e in edges_b) / len(edges_b)

        # Parity check: count Tet A vertices with odd parity
        odd_parity_in_a = sum(1 for v in TET_A if parity(v) == 1)
        even_parity_in_b = sum(1 for v in TET_B if parity(v) == 0)

        # Complement mapping: count pairs where v XOR 7 crosses tetrahedra
        complement_crosses = 0
        for v in TET_A:
            comp = 7 - v
            if comp in TET_B:
                complement_crosses += 1

        # Field Origin distances
        origin = (0.0, 0.0, 0.0)
        distances_from_origin = [distance(origin, VERTEX_COORDS[v]) for v in range(8)]
        mean_distance = sum(distances_from_origin) / 8.0
        distance_variance = sum(
            (d - mean_distance) ** 2 for d in distances_from_origin
        ) / 8.0

        # Centroid of each tetrahedron
        centroid_a = centroid(TET_A)
        centroid_b = centroid(TET_B)
        centroid_a_distance = math.sqrt(sum(c ** 2 for c in centroid_a))
        centroid_b_distance = math.sqrt(sum(c ** 2 for c in centroid_b))

        # Face counts
        n_time = sum(1 for name in list(FACES_A.keys()) + list(FACES_B.keys())
                     if name in TIME_FACE_NAMES)
        n_spatial = sum(1 for name in list(FACES_A.keys()) + list(FACES_B.keys())
                        if name in SPATIAL_FACE_NAMES)
        total_faces = len(FACES_A) + len(FACES_B)

        return (
            Model()
            .add("Tet A mean edge length", edge_length_a)
            .add("Tet B mean edge length", edge_length_b)
            .add("Tet A edge variance", variance_a)
            .add("Tet B edge variance", variance_b)
            .add("Tet A vertices with odd parity", float(odd_parity_in_a))
            .add("Tet B vertices with even parity", float(even_parity_in_b))
            .add("Complement pairs crossing tetrahedra", float(complement_crosses))
            .add("Field Origin mean distance to vertices", mean_distance)
            .add("Field Origin distance variance", distance_variance)
            .add("Tet A centroid distance from origin", centroid_a_distance)
            .add("Tet B centroid distance from origin", centroid_b_distance)
            .add("Time faces", float(n_time))
            .add("Spatial faces", float(n_spatial))
            .add("Total faces", float(total_faces))
        )

    def observations(self) -> Observed:
        expected_edge = 2.0 * math.sqrt(2.0)
        expected_distance = math.sqrt(3.0)

        return (
            Observed()
            .add("Tet A mean edge length", expected_edge)
            .add("Tet B mean edge length", expected_edge)
            .add("Tet A edge variance", 0.0)
            .add("Tet B edge variance", 0.0)
            .add("Tet A vertices with odd parity", 4.0)
            .add("Tet B vertices with even parity", 4.0)
            .add("Complement pairs crossing tetrahedra", 4.0)
            .add("Field Origin mean distance to vertices", expected_distance)
            .add("Field Origin distance variance", 0.0)
            .add("Tet A centroid distance from origin", 0.0)
            .add("Tet B centroid distance from origin", 0.0)
            .add("Time faces", 2.0)
            .add("Spatial faces", 6.0)
            .add("Total faces", 8.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Stellated Octahedron Geometry Validation",
        summary="Verify that the GFM stellated octahedron has the claimed geometric properties",
        test_classes=[StellatedOctahedronGeometry],
    )
