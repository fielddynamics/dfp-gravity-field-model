# FILENAME: test_face_structure_3plus1.py

"""
Face Structure and 3+1 Decomposition of the Stellated Octahedron
================================================================

The stellated octahedron (two interpenetrating regular tetrahedra) has 8
triangular faces: 4 from each tetrahedron. In standard geometry, each face
of a tetrahedron is the triangle opposite one vertex. The GFM framework
classifies these faces by their physical role: faces opposite the extreme
vertices V7 (all bits 1) and V0 (all bits 0) are designated TIME faces,
while the remaining 6 are SPATIAL faces. This yields a 3+1 decomposition
per tetrahedron (3 spatial faces + 1 time face) and a 6+2 decomposition
globally (6 spatial + 2 temporal).

Standard physics treats the 3+1 signature of spacetime as an empirical
input. General relativity assumes a Lorentzian metric with signature
(+, -, -, -) or (-, +, +, +) but does not derive why one time dimension
accompanies three spatial ones. The GFM stellated octahedron produces
this signature geometrically: each tetrahedron contributes exactly 3
spatial coupling ports and 1 temporal coupling port.

The TIME face fraction 2/8 = 1/4 is the geometric ratio that enters
the electron spin derivation (S = hbar/2) and the uncertainty principle
(Delta_x Delta_p >= hbar/2). This test verifies the face structure
from first principles using vertex coordinates and parity assignments.

GFM OBSERVATION: The stellated octahedron has 8 faces decomposing as
6 spatial + 2 temporal, giving a TIME face fraction of exactly 1/4.

This is a DERIVATION from the combinatorial geometry of two tetrahedra
embedded in a cube with vertices at (+-1, +-1, +-1).
"""

import math
from itertools import combinations
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K,
    VERTICES,
    TET_A,
    TET_B,
)


# ======================================================================
# Geometry helpers
# ======================================================================

# Vertex coordinates: 3 bit binary labeling
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


def bit_parity(v):
    """Return sum of bits mod 2 for vertex label v (0 through 7)."""
    return bin(v).count("1") % 2


def get_faces(tet_vertices):
    """
    Return the 4 triangular faces of a tetrahedron.
    Each face is the set of 3 vertices remaining when one vertex is removed.
    Returns list of (opposite_vertex, frozenset_of_3_vertices).
    """
    faces = []
    for v in tet_vertices:
        face = frozenset(w for w in tet_vertices if w != v)
        faces.append((v, face))
    return faces


def is_time_face(opposite_vertex):
    """
    A TIME face is defined as the face opposite the apex vertex of its
    tetrahedron. V7 (111) is the apex of Tet A, V0 (000) is the apex
    of Tet B. The TIME face is opposite the apex, meaning:
      TIME face A7 = face opposite V7 in Tet A = {1, 2, 4}
      TIME face B0 = face opposite V0 in Tet B = {3, 5, 6}
    """
    return opposite_vertex in (7, 0)


def edge_length(v1, v2):
    """Euclidean distance between two vertices."""
    c1 = VERTEX_COORDS[v1]
    c2 = VERTEX_COORDS[v2]
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def is_regular_tetrahedron(tet_vertices):
    """Check that all 6 edges of a tetrahedron have equal length."""
    edges = list(combinations(tet_vertices, 2))
    lengths = [edge_length(v1, v2) for v1, v2 in edges]
    mean_len = sum(lengths) / len(lengths)
    return all(abs(l - mean_len) / mean_len < 1e-10 for l in lengths)


def complementary_pair(v):
    """Return the complement vertex: XOR with 7 flips all bits."""
    return v ^ 7


class FaceStructure3Plus1(Test):
    """
    PHYSICAL CONTEXT:
    The 3+1 dimensional structure of spacetime is one of the deepest
    features of our universe. General relativity encodes it via a metric
    with Lorentzian signature, but the theory accepts this signature as
    an axiom rather than deriving it. Kaluza Klein theories and string
    theory introduce additional dimensions, then must explain why only
    3+1 are macroscopically visible. The question of why spacetime has
    one time dimension and three spatial dimensions remains open.

    In combinatorial geometry, a tetrahedron has exactly 4 triangular
    faces, each defined as the triangle opposite one vertex (Coxeter
    1973). The stellated octahedron, formed by two interpenetrating
    regular tetrahedra inscribed in a cube, therefore has 8 faces total.

    GFM OBSERVATION:
    Labeling vertices by 3 bit binary indices, Tet A occupies odd parity
    vertices {1, 2, 4, 7} and Tet B occupies even parity vertices
    {0, 3, 5, 6}. The apex vertices V7 = (1,1,1) and V0 = (-1,-1,-1)
    sit at opposite ends of the main body diagonal. The faces opposite
    these apexes (FACE_A7 and FACE_B0) are designated TIME faces. The
    remaining 6 faces are SPATIAL. This gives 3 spatial + 1 time face
    per tetrahedron, matching the 3+1 signature of spacetime. The TIME
    face fraction 2/8 = 1/4 enters the spin and uncertainty derivations.

    EPISTEMIC STATUS:
    The face counting and classification are geometric derivations from
    the vertex coordinates and parity assignments. The identification of
    the apex opposite faces as TIME faces is a GFM framework definition,
    not a theorem of standard physics.
    """

    name = "Face Structure and 3+1 Decomposition"

    question = (
        "Does the stellated octahedron produce exactly 8 triangular faces "
        "decomposing into 6 spatial and 2 temporal faces? Is the resulting "
        "3+1 pattern per tetrahedron (3 spatial faces + 1 time face) a "
        "necessary consequence of the geometry, and does the TIME face "
        "fraction equal exactly 1/4?"
    )

    reference = (
        "Coxeter (1973) Regular Polytopes; "
        "GFM Paper VII Section 2.2 (face classification); "
        "GFM Paper VI Section 7 (spin from face ratio); "
        "GFM Paper VII Section 5.2 (uncertainty from face ratio)"
    )

    tolerance = 0.001

    level = Level.CRITICAL

    commentary = (
        "The stellated octahedron has 8 faces by elementary geometry: each "
        "of 2 tetrahedra contributes 4 faces, and no faces are shared. The "
        "classification into TIME and SPATIAL faces follows from identifying "
        "the apex vertices V0 and V7 as the endpoints of the principal body "
        "diagonal connecting (-1,-1,-1) to (+1,+1,+1). Each tetrahedron "
        "contributes exactly 1 TIME face (opposite its apex) and 3 SPATIAL "
        "faces, giving the 3+1 pattern. The global ratio of TIME faces to "
        "total faces is 2/8 = 1/4. This fraction is a geometric fact, not "
        "a tunable parameter. It directly enters two GFM results: the "
        "electron spin magnitude S = (2/8) * 2 * hbar = hbar/2, and the "
        "minimum uncertainty product Delta_x * Delta_p >= hbar/2. Both "
        "tetrahedra are verified to be regular (all edges equal at length "
        "2*sqrt(2)), and the parity assignment is confirmed: odd bit sum "
        "vertices form Tet A, even bit sum vertices form Tet B."
    )

    # Audit scoring
    audit_score = 86
    audit_notes = (
        "Question: 12/15 (asks the right geometric questions with specific numbers like 6+2 and 1/4, but reads as a checklist of sub questions rather than opening with a single compelling mystery hook; starting with 'Why does spacetime have a 3+1 signature?' and building from there would be sharper). Derivation: 14/15 (excellent scaffolding from standard geometry through vertex assignment, disjointness proof, face enumeration, classification, per tetrahedron breakdown, regularity check, and complementary structure; intuition is strong throughout; the only minor gap is no everyday analogy to ground the spatial vs temporal distinction for a newcomer). Commentary: 12/15 (solid interpretation connecting the 1/4 fraction to spin and uncertainty, confirms regularity and parity, but reads more like a derivation recap than an insight delivery; missing an aha moment about what it means physically that geometry forces exactly one time face per tetrahedron; no analogy to anchor the abstract result). Model: 9/10 (12 clean summary values covering total counts, per tetrahedron breakdowns, fraction, regularity booleans, edge length, and complementary check; well organized and easy to interpret; could arguably consolidate the per tetrahedron counts but this is minor). Observations: 8/10 (all values are exact geometric expectations traceable to Coxeter and the GFM vertex definitions; edge length uses math.sqrt rather than hardcoding; however VERTICES, TET_A, TET_B are imported but not directly used in the observations method, and the Coxeter reference is in the derivation but not explicitly tied to each observed value). Constants: 8/10 (K, VERTICES, TET_A, TET_B properly imported from common; however VERTICES, TET_A, TET_B are imported but the model method recomputes tet_a and tet_b from scratch via bit_parity rather than using the imported constants, which is a missed opportunity and mild inconsistency; VERTEX_COORDS is hardcoded at module level rather than imported, though this may not be available in common). Accessibility: 14/15 (an undergraduate with basic geometry can follow the face counting and parity logic; the binary labeling is explained clearly; the derivation builds from simple to complex; the only gap is the lack of a physical analogy for why apex opposite faces would correspond to time). Header: 9/10 (comprehensive module docstring covering physical context, standard physics position, GFM classification, the key ratio and its downstream uses, epistemic status clearly stated as derivation; minor gap: no explicit target audience statement)."
    )

    academic_paper = """\
TITLE Face Structure and 3+1 Decomposition of the Stellated Octahedron ABSTRACT We investigate the face structure of the stellated octahedron, formed by two interpenetrating regular tetrahedra inscribed in a cube. Combinatorial enumeration yields exactly 8 triangular faces decomposing as 6 spatial and 2 temporal, giving a TIME face fraction of exactly 1/4. This is a geometric DERIVATION, not a fit. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The 3+1 dimensional signature of spacetime is among the most fundamental features of our universe. General relativity encodes this signature through a Lorentzian metric, but accepts it as an axiom. Kaluza Klein theories and string theory introduce additional dimensions and must compactify the extras by hand. No standard framework derives why one time dimension accompanies exactly three spatial dimensions. The stellated octahedron consists of two interpenetrating regular tetrahedra with 8 vertices at cube corners (+-1, +-1, +-1). Each tetrahedron has 4 triangular faces. In the GFM framework, faces are classified by the role of their opposite vertex: the face opposite the apex vertex V7 = (1,1,1) in Tet A and the face opposite V0 = (-1,-1,-1) in Tet B are designated TIME faces. The remaining 6 are SPATIAL faces. This test verifies whether this classification is a necessary geometric consequence of the vertex structure, producing 3 spatial + 1 temporal face per tetrahedron and a TIME face fraction of 1/4. This fraction enters the GFM derivations of electron spin (S = hbar/2) and the uncertainty principle (Delta_x Delta_p >= hbar/2). 2. METHODOLOGY The model assigns 8 vertices to cube corners using 3 bit binary labels (0 through 7). Vertices with odd bit sum {1, 2, 4, 7} form Tet A; even bit sum {0, 3, 5, 6} form Tet B. For each tetrahedron, all 4 faces are enumerated as the triangle opposite each vertex. Faces are classified as TIME (opposite V7 or V0) or SPATIAL (all others). Regularity is verified by computing all 6 edge lengths per tetrahedron and confirming equality. The complementary relationship between TIME faces is checked via XOR with 7 (bitwise complement). Agreement criterion: exact match (0.00% error) on all 12 quantities. 3. RESULTS All 12 model outputs match their expected values exactly (0.00% error on every quantity). Face counts: Total faces = 8, TIME faces = 2, SPATIAL faces = 6. Per tetrahedron: Tet A has 1 TIME face and 3 SPATIAL faces. Tet B has 1 TIME face and 3 SPATIAL faces. The TIME face fraction = 0.250000, matching 2/8 = 1/4 exactly. Geometric verification: Both Tet A and Tet B pass the regularity check (1.0, meaning yes). All edges measure 2.828427 (= 2*sqrt(2)), confirming both are regular tetrahedra inscribed in the unit cube scaled by factor 2. Structural verification: The TIME faces are confirmed complementary (1.0, meaning yes). FACE_A7 = {1, 2, 4} maps to {6, 5, 3} = FACE_B0 under bitwise complement, confirming the bimetric mirror symmetry between temporal coupling ports. 4. DISCUSSION The 3+1 decomposition per tetrahedron is not imposed but follows necessarily from the geometry. Each tetrahedron has exactly 4 faces. Exactly one face is opposite the apex vertex (V7 for Tet A, V0 for Tet B), so exactly one face per tetrahedron is temporal. The remaining 3 are spatial. The global count of 6 spatial + 2 temporal faces, and the fraction 2/8 = 1/4, are combinatorial facts about two tetrahedra embedded in a cube with opposite parity vertex assignments. EPISTEMIC STATUS: DERIVATION. The face counts and regularity are theorems of Euclidean geometry. The identification of apex opposite faces as TIME faces is a GFM framework definition. The downstream physical consequences (spin = hbar/2, uncertainty = hbar/2) rely on this definition. This test connects to the dimensionality uniqueness test (which derives d = 3 and K = 4) and provides the geometric substrate for the spin and uncertainty derivations. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove that the 3+1 signature of physical spacetime originates from tetrahedral face counting. The TIME face designation is a GFM definition, not a result of standard physics. The physical interpretation gains weight only if the downstream predictions (spin, uncertainty) are independently confirmed. 6. CONCLUSION The stellated octahedron produces exactly 8 faces with a 6+2 spatial/temporal decomposition, yielding
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: A tetrahedron has exactly 4 triangular "
                "faces. Each face consists of the 3 vertices not including "
                "one specific vertex. Two tetrahedra therefore have 8 faces "
                "total, provided no faces are shared (Coxeter 1973)."
            )
            .step(
                "VERTEX ASSIGNMENT: Place 8 vertices at cube corners "
                "(+-1, +-1, +-1) with 3 bit binary labels 0 through 7. "
                "Vertices with odd bit sum {1, 2, 4, 7} form Tet A. "
                "Vertices with even bit sum {0, 3, 5, 6} form Tet B. "
                "Each set of 4 vertices forms a regular tetrahedron with "
                "edge length 2*sqrt(2)."
            )
            .step(
                "NO SHARED FACES: Tet A and Tet B share no vertices "
                "(odd and even parity are disjoint), so no triangular face "
                "can belong to both tetrahedra. The 8 faces are distinct."
            )
            .step(
                "FACE ENUMERATION: Tet A faces are opposite V1, V2, V4, V7 "
                "respectively: {2,4,7}, {1,4,7}, {1,2,7}, {1,2,4}. "
                "Tet B faces are opposite V0, V3, V5, V6 respectively: "
                "{3,5,6}, {0,5,6}, {0,3,6}, {0,3,5}."
            )
            .step(
                "GFM CLASSIFICATION: The apex of Tet A is V7 = (1,1,1), "
                "the vertex where all coordinates are maximal. The apex of "
                "Tet B is V0 = (-1,-1,-1), all coordinates minimal. These "
                "are connected by the main body diagonal. Faces opposite "
                "these apexes are TIME faces: FACE_A7 = {1,2,4} and "
                "FACE_B0 = {3,5,6}. All other faces are SPATIAL."
            )
            .equation("N_time = 2, N_spatial = 6, N_total = 8")
            .step(
                "PER TETRAHEDRON: Each tetrahedron has 1 TIME face and "
                "3 SPATIAL faces, giving 3+1 per tetrahedron."
            )
            .equation("TIME face fraction = N_time / N_total = 2/8 = 1/4")
            .step(
                "REGULARITY CHECK: All 6 edges of Tet A have length "
                "2*sqrt(2) (distance between any two odd parity cube "
                "corners). Same for Tet B. Both are regular tetrahedra."
            )
            .step(
                "COMPLEMENTARY STRUCTURE: Each TIME face vertex in one "
                "tetrahedron has its complement in the other tetrahedron. "
                "FACE_A7 = {1,2,4} complements to {6,5,3} = FACE_B0. "
                "The TIME faces are complementary pairs."
            )
            .conclude(
                "The stellated octahedron necessarily has 8 faces with a "
                "6+2 spatial/temporal decomposition. The 3+1 pattern per "
                "tetrahedron and the TIME face fraction 1/4 are geometric "
                "consequences of embedding two regular tetrahedra of "
                "opposite parity in a cube."
            )
        )

    def model(self) -> Model:
        # Verify parity assignments
        tet_a = sorted([v for v in range(8) if bit_parity(v) == 1])
        tet_b = sorted([v for v in range(8) if bit_parity(v) == 0])

        # Get all faces
        faces_a = get_faces(tet_a)
        faces_b = get_faces(tet_b)
        all_faces = faces_a + faces_b
        total_faces = float(len(all_faces))

        # Classify faces
        time_faces = [(opp, f) for opp, f in all_faces if is_time_face(opp)]
        spatial_faces = [(opp, f) for opp, f in all_faces if not is_time_face(opp)]
        n_time = float(len(time_faces))
        n_spatial = float(len(spatial_faces))

        # Per tetrahedron counts
        time_per_tet_a = float(sum(1 for opp, f in faces_a if is_time_face(opp)))
        spatial_per_tet_a = float(sum(1 for opp, f in faces_a if not is_time_face(opp)))
        time_per_tet_b = float(sum(1 for opp, f in faces_b if is_time_face(opp)))
        spatial_per_tet_b = float(sum(1 for opp, f in faces_b if not is_time_face(opp)))

        # TIME face fraction
        time_fraction = n_time / total_faces

        # Regularity check: both tetrahedra regular
        reg_a = 1.0 if is_regular_tetrahedron(tet_a) else 0.0
        reg_b = 1.0 if is_regular_tetrahedron(tet_b) else 0.0

        # Edge length (all equal for regular tet in cube)
        tet_a_edge = edge_length(tet_a[0], tet_a[1])

        # Complementary check: TIME face vertices complement each other
        face_a7_verts = set()
        face_b0_verts = set()
        for opp, f in faces_a:
            if opp == 7:
                face_a7_verts = set(f)
        for opp, f in faces_b:
            if opp == 0:
                face_b0_verts = set(f)
        complements_match = 1.0 if face_a7_verts == {complementary_pair(v) for v in face_b0_verts} else 0.0

        return (
            Model()
            .add("Total faces", total_faces)
            .add("TIME faces", n_time)
            .add("SPATIAL faces", n_spatial)
            .add("TIME faces per Tet A", time_per_tet_a)
            .add("SPATIAL faces per Tet A", spatial_per_tet_a)
            .add("TIME faces per Tet B", time_per_tet_b)
            .add("SPATIAL faces per Tet B", spatial_per_tet_b)
            .add("TIME face fraction", time_fraction)
            .add("Tet A is regular (1=yes)", reg_a)
            .add("Tet B is regular (1=yes)", reg_b)
            .add("Edge length", tet_a_edge)
            .add("TIME faces are complementary (1=yes)", complements_match)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Total faces", 8.0)
            .add("TIME faces", 2.0)
            .add("SPATIAL faces", 6.0)
            .add("TIME faces per Tet A", 1.0)
            .add("SPATIAL faces per Tet A", 3.0)
            .add("TIME faces per Tet B", 1.0)
            .add("SPATIAL faces per Tet B", 3.0)
            .add("TIME face fraction", 0.25)
            .add("Tet A is regular (1=yes)", 1.0)
            .add("Tet B is regular (1=yes)", 1.0)
            .add("Edge length", 2.0 * math.sqrt(2.0))
            .add("TIME faces are complementary (1=yes)", 1.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Face Structure and 3+1 Decomposition",
        summary="Verify the stellated octahedron has 8 faces with 6 spatial and 2 temporal, giving TIME fraction 1/4",
        test_classes=[FaceStructure3Plus1],
    )
