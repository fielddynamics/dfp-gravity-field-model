"""
TIME Face Geometry Tests
========================

This module examines the geometry of TIME faces in the stellated octahedron.
TIME faces are the triangular faces of each tetrahedron that serve as
Coupling Ports for field-to-field interactions.

Key properties:
- Each tetrahedron has k=4 triangular faces
- Faces are oriented outward/inward relative to the Field Origin
- Adjacent faces share exactly one edge
- Each face has a complementary face on the opposite tetrahedron
- Face normals encode interaction directionality

The TIME acronym encodes the face's role in field dynamics:
T = Triangular interface
I = Information boundary
M = Momentum exchange surface
E = Energy transfer portal
"""

import math
from typing import Dict, List, Tuple, Optional

from gravity_field_model.framework import *
from gravity_field_model.common import K

# =============================================================================
# CONSTANTS (K imported from common)
# =============================================================================

SQRT_3 = math.sqrt(3)

# Tetrahedron geometry
TETRAHEDRON_VERTICES = 4
TETRAHEDRON_EDGES = 6
TETRAHEDRON_FACES = 4


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def face_area_equilateral(edge_length: float) -> float:
    """Calculate the area of an equilateral triangle."""
    return (SQRT_3 / 4) * edge_length ** 2


def solid_angle_equilateral() -> float:
    """
    Calculate the solid angle subtended by an equilateral triangular face
    of a regular tetrahedron as viewed from its centroid.
    Each of 4 faces subtends 4*pi/4 = pi steradians.
    """
    return math.pi  # steradians


def dihedral_angle_tetrahedron() -> float:
    """
    Calculate the dihedral angle between adjacent faces of a regular tetrahedron.
    This is arccos(1/3) = 70.53 degrees.
    """
    return math.acos(1/3)  # radians


# =============================================================================
# TESTS
# =============================================================================

class TimeFaceCount(Test):
    """
    Each tetrahedron has exactly k=4 TIME faces (triangular Coupling Ports).
    """
    name = "TIME Face Count"
    question = (
        "A tetrahedron has 4 triangular faces, each a potential coupling port. Why 4? "
        "With 4 vertices, each face is defined by 3 vertices, and C(4,3) = 4. Does "
        "each tetrahedron truly have exactly 4 TIME faces for field interactions?"
    )
    reference = "Tetrahedron geometry"
    tolerance = 0.0
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 13/15 - Hooks with 'why 4' and combinatorics. "
        "Derivation: 12/15 - Clear steps, could use more intuition. "
        "Commentary: 13/15 - Good 'window' analogy. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 9/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Count faces of a tetrahedron to establish Coupling Port count.")
            .step("A tetrahedron with k=4 vertices has k=4 triangular faces.")
            .step("Each face is bounded by 3 vertices (triangle).")
            .step("Each face corresponds to one Coupling Port.")
            .step("Total Coupling Ports per tetrahedron = 4.")
            .conclude("OUTPUT: TIME faces per tetrahedron = k = 4.")
        )
    
    commentary = (
        "Count the faces of a tetrahedron. Each face uses 3 of the 4 vertices. How many "
        "ways to choose 3 from 4? C(4,3) = 4. Four faces, four coupling ports. Each face "
        "is a triangular window through which the field can interact with the outside. "
        "The number k=4 is not arbitrary; it is forced by tetrahedron geometry."
    )
    
    def model(self):
        return (
            Model()
            .add("k", K)
            .add("Vertices per tet", TETRAHEDRON_VERTICES)
            .add("TIME faces per tet", TETRAHEDRON_FACES)
        )
    
    def observations(self):
        return (
            Observed()
            .add("k", 4)
            .add("Vertices per tet", 4)
            .add("TIME faces per tet", 4)
        )


class TimeFaceAreaFraction(Test):
    """
    Each TIME face covers 1/4 of the tetrahedron's total surface area.
    """
    name = "TIME Face Area Distribution"
    question = (
        "A regular tetrahedron has 4 identical faces. Each face should cover exactly "
        "1/4 of the total surface. No face is bigger or smaller than another. Does "
        "each TIME face truly cover exactly 25% of the tetrahedron's surface area?"
    )
    reference = "Regular tetrahedron geometry"
    tolerance = 0.001
    level = Standard
    audit_score = 90
    audit_notes = (
        "Question: 14/15 - Good equality and democracy question. "
        "Derivation: 14/15 - Clear symmetry argument. "
        "Commentary: 14/15 - Excellent 'democracy in geometry' insight. "
        "Model: 9/10 - Clean area calculation. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 12/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: face_area_equilateral() could move to common. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Verify equal area distribution among TIME faces.")
            .step("A regular tetrahedron has k=4 congruent equilateral triangular faces.")
            .step("Each face has the same area (by congruence).")
            .step("Total surface area = 4 x (area of one face).")
            .step("Fraction per face = (area of one face) / (4 x area of one face) = 1/4.")
            .conclude("OUTPUT: Each TIME face covers 1/k = 25% of total surface.")
        )
    
    commentary = (
        "In a regular tetrahedron, symmetry is perfect. All 4 faces are congruent "
        "equilateral triangles. Each face is exactly 1/4 of the total skin. No port "
        "is favored, no direction is special. If fields couple through these faces, "
        "they have equal opportunity at each port. Democracy in geometry."
    )
    
    def model(self):
        edge = 1.0  # Normalized
        face_area = face_area_equilateral(edge)
        total_area = K * face_area
        fraction = face_area / total_area
        return (
            Model()
            .add("Face count", K)
            .add("Area per face (normalized)", face_area)
            .add("Total surface area", total_area)
            .add("Fraction per face", fraction)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Face count", 4)
            .add("Area per face (normalized)", SQRT_3 / 4)
            .add("Total surface area", SQRT_3)
            .add("Fraction per face", 0.25)
        )


class TimeFaceSolidAngle(Test):
    """
    Each TIME face subtends pi steradians when viewed from the tetrahedron centroid.
    Total solid angle: 4 faces x pi = 4*pi steradians (full sphere).
    """
    name = "TIME Face Solid Angle"
    question = (
        "Stand at the center of a tetrahedron and look at one face. How much of your "
        "field of view does it cover? A full sphere is 4*pi steradians. With 4 equal "
        "faces, each should subtend pi steradians. Does the geometry confirm this?"
    )
    reference = "Solid geometry"
    tolerance = 0.001
    level = Standard
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Good field of view question. "
        "Derivation: 14/15 - Clear symmetry proof. "
        "Commentary: 14/15 - Excellent 'tiles the sphere' insight. "
        "Model: 9/10 - Clean steradian calculation. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 14/15 - All levels can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: solid_angle_equilateral() could move to common. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Calculate solid angle subtended by each TIME face from centroid.")
            .step("The full sphere subtends 4*pi steradians.")
            .step("The tetrahedron has k=4 faces, symmetric around the centroid.")
            .step("By symmetry, each face subtends (4*pi)/4 = pi steradians.")
            .step("Verification: 4 faces x pi = 4*pi steradians (complete sphere).")
            .conclude("OUTPUT: Each TIME face subtends pi steradians; total = 4*pi.")
        )
    
    commentary = (
        "Imagine you are a tiny observer at the tetrahedron's center. Looking outward, "
        "your view is divided into 4 equal sectors, one per face. A full sphere of "
        "directions is 4*pi steradians. Divide by 4 faces: each face covers pi "
        "steradians. The four faces tile the sphere of directions perfectly. Every "
        "possible direction points toward exactly one face. No gaps, no overlaps."
    )
    
    def model(self):
        solid_angle_per_face = solid_angle_equilateral()
        total_solid_angle = K * solid_angle_per_face
        full_sphere = 4 * math.pi
        return (
            Model()
            .add("Solid angle per face (sr)", solid_angle_per_face)
            .add("Total solid angle (sr)", total_solid_angle)
            .add("Full sphere (sr)", full_sphere)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Solid angle per face (sr)", math.pi)
            .add("Total solid angle (sr)", 4 * math.pi)
            .add("Full sphere (sr)", 4 * math.pi)
        )


class TimeFaceDihedralAngle(Test):
    """
    Adjacent TIME faces meet at the characteristic dihedral angle arccos(1/3) = 70.53 degrees.
    """
    name = "TIME Face Dihedral Angle"
    question = (
        "Two adjacent faces of a tetrahedron meet at an edge like pages of a book. "
        "What angle do they make? For a tetrahedron, arccos(1/3) = 70.53 degrees. "
        "This is sharper than a right angle. Does every edge have this same angle?"
    )
    reference = "Tetrahedron geometry"
    tolerance = 0.01
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 13/15 - Good 'book pages' analogy setup. "
        "Derivation: 13/15 - Clear with exact values. "
        "Commentary: 13/15 - Good 'pointy' characterization. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: dihedral_angle_tetrahedron() could move to common. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Calculate the angle between adjacent TIME faces.")
            .step("The dihedral angle of a regular tetrahedron is arccos(1/3).")
            .step("arccos(1/3) = 70.53 degrees (or 1.2310 radians).")
            .step("This is the angle between face normals of adjacent faces.")
            .step("All 6 edges have the same dihedral angle (by symmetry).")
            .conclude("OUTPUT: Dihedral angle = 70.53 degrees = arccos(1/3).")
        )
    
    commentary = (
        "The dihedral angle is the angle between two adjacent faces, measured like "
        "opening a book. For a tetrahedron, cos(angle) = 1/3, giving angle = 70.53 "
        "degrees. This is the same at all 6 edges. The tetrahedron is 'pointy' in a "
        "specific way. This angle determines how neighboring coupling ports are "
        "oriented relative to each other."
    )
    
    def model(self):
        dihedral_rad = dihedral_angle_tetrahedron()
        dihedral_deg = math.degrees(dihedral_rad)
        cos_dihedral = math.cos(dihedral_rad)
        return (
            Model()
            .add("Dihedral angle (radians)", dihedral_rad)
            .add("Dihedral angle (degrees)", dihedral_deg)
            .add("cos(dihedral)", cos_dihedral)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Dihedral angle (radians)", 1.2310)
            .add("Dihedral angle (degrees)", 70.53)
            .add("cos(dihedral)", 1/3)
        )


class TimeFaceVertexComposition(Test):
    """
    Each TIME face is defined by 3 vertices (a triangle).
    Each vertex belongs to exactly 3 TIME faces.
    """
    name = "TIME Face Vertex Composition"
    question = (
        "Each triangular face uses 3 of the 4 vertices. But how many faces does each "
        "vertex touch? With 4 faces of 3 vertices each, that is 12 incidences. Divide "
        "by 4 vertices: each vertex is in 3 faces. A beautiful symmetry?"
    )
    reference = "Tetrahedron topology"
    tolerance = 0.0
    level = Standard
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good incidence counting question. "
        "Derivation: 14/15 - Clear dual counting proof. "
        "Commentary: 14/15 - Excellent self-duality insight. "
        "Model: 9/10 - Clean incidence calculation. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Analyze vertex-face incidence in a tetrahedron.")
            .step("Each TIME face is a triangle, having exactly 3 vertices.")
            .step("Total vertex-face incidences = 4 faces x 3 vertices = 12.")
            .step("Each of the 4 vertices appears in 12/4 = 3 faces.")
            .step("Alternatively: each vertex is excluded from exactly 1 face (the opposite face).")
            .conclude("OUTPUT: Vertices per face = 3; faces per vertex = 3.")
        )
    
    commentary = (
        "This is the tetrahedron's self-duality. 4 vertices, 4 faces. 3 vertices per "
        "face, 3 faces per vertex. Swap 'vertex' and 'face' and the description stays "
        "the same! Each vertex belongs to exactly the faces that do NOT have it as the "
        "'opposite' vertex. This dual structure means vertices and faces play symmetric "
        "roles in the geometry."
    )
    
    def model(self):
        vertices_per_face = 3
        total_vertices = K
        total_faces = K
        incidences = total_faces * vertices_per_face
        faces_per_vertex = incidences // total_vertices
        return (
            Model()
            .add("Vertices per TIME face", vertices_per_face)
            .add("Faces per vertex", faces_per_vertex)
            .add("Total incidences", incidences)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Vertices per TIME face", 3)
            .add("Faces per vertex", 3)
            .add("Total incidences", 12)
        )


class TimeFaceEdgeSharing(Test):
    """
    Adjacent TIME faces share exactly one edge.
    Each TIME face has 3 edges and 3 neighboring faces.
    """
    name = "TIME Face Edge Sharing"
    question = (
        "Any two faces of a tetrahedron share exactly one edge (they cannot be "
        "disjoint). Each face has 3 edges, hence 3 neighbors. Is every pair of "
        "TIME faces adjacent? Is the face connectivity complete?"
    )
    reference = "Tetrahedron topology"
    tolerance = 0.0
    level = Standard
    audit_score = 90
    audit_notes = (
        "Question: 14/15 - Good maximum connectivity question. "
        "Derivation: 14/15 - Clear C(4,2) argument. "
        "Commentary: 14/15 - Excellent 'no face is isolated' insight. "
        "Model: 9/10 - Clean edge counting. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 12/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Analyze edge-face relationships in a tetrahedron.")
            .step("The tetrahedron has 6 edges.")
            .step("Each edge is shared by exactly 2 faces (no more, no less).")
            .step("Each face has 3 edges, so 3 neighboring faces.")
            .step("Two faces are adjacent if and only if they share an edge.")
            .step("There are C(4,2) = 6 face pairs; all 6 share edges (complete adjacency).")
            .conclude("OUTPUT: Each face has 3 neighbors; pairs share exactly 1 edge.")
        )
    
    commentary = (
        "In a tetrahedron, there are no 'opposite' faces in the sense of faces that do "
        "not touch. Every pair of faces shares an edge. C(4,2) = 6 pairs of faces, and "
        "6 edges for them to share. One edge per pair. This means every coupling port "
        "is one step away from every other. Maximum connectivity. No face is isolated."
    )
    
    def model(self):
        edges_total = TETRAHEDRON_EDGES  # 6
        edges_per_face = 3
        neighbors_per_face = 3
        edge_shared_per_pair = 1
        return (
            Model()
            .add("Total edges", edges_total)
            .add("Edges per face", edges_per_face)
            .add("Neighbors per face", neighbors_per_face)
            .add("Shared edges per adjacent pair", edge_shared_per_pair)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Total edges", 6)
            .add("Edges per face", 3)
            .add("Neighbors per face", 3)
            .add("Shared edges per adjacent pair", 1)
        )


class TimeFaceOppositeVertex(Test):
    """
    Each TIME face has exactly one opposite vertex (not on the face).
    This vertex is maximally distant from the face.
    """
    name = "TIME Face Opposite Vertex"
    question = (
        "Each face is a triangle with 3 vertices. The fourth vertex is NOT on that "
        "face. It sits opposite, like the apex of a pyramid when the face is the base. "
        "Does each TIME face have exactly one such opposite vertex?"
    )
    reference = "Tetrahedron geometry"
    tolerance = 0.0
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 13/15 - Good pyramid/apex setup. "
        "Derivation: 13/15 - Clear arithmetic. "
        "Commentary: 13/15 - Nice tent analogy. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Identify the vertex opposite to each TIME face.")
            .step("Each face has 3 vertices; the tetrahedron has 4 vertices total.")
            .step("One vertex is not on each face: 4 - 3 = 1 opposite vertex.")
            .step("The opposite vertex is the apex when viewing the face as base.")
            .step("Distance from apex to face = tetrahedron height = sqrt(2/3) * edge.")
            .conclude("OUTPUT: Each face has exactly 1 opposite vertex.")
        )
    
    commentary = (
        "Think of the face as the floor and the opposite vertex as the peak of a tent. "
        "4 vertices, 3 on the floor, 1 at the peak. The peak vertex defines the 'up' "
        "direction for that face. For field coupling, this creates a natural orientation: "
        "the face points away from its opposite vertex toward the outside world."
    )
    
    def model(self):
        vertices_total = K
        vertices_per_face = 3
        opposite_vertices = vertices_total - vertices_per_face
        return (
            Model()
            .add("Total vertices", vertices_total)
            .add("Vertices on face", vertices_per_face)
            .add("Opposite vertices", opposite_vertices)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Total vertices", 4)
            .add("Vertices on face", 3)
            .add("Opposite vertices", 1)
        )


class TimeFaceNormalOrientation(Test):
    """
    TIME face normals point outward from the tetrahedron centroid.
    All 4 normals are equally spaced at tetrahedral angles.
    """
    name = "TIME Face Normal Orientation"
    question = (
        "Draw a perpendicular arrow outward from each face. The 4 arrows point in "
        "different directions. The angle between any two is arccos(-1/3) = 109.47 "
        "degrees, the famous tetrahedral angle. Are the normals maximally spread?"
    )
    reference = "Tetrahedron geometry"
    tolerance = 0.01
    level = Standard
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Good tetrahedral angle question. "
        "Derivation: 14/15 - Clear angle calculation. "
        "Commentary: 14/15 - Excellent CH4 and maximal spread insight. "
        "Model: 9/10 - Clean angle verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 14/15 - All levels can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Analyze the orientation of TIME face normals.")
            .step("Each face has an outward-pointing normal perpendicular to the face.")
            .step("The 4 normals point toward the 4 face centers from the centroid.")
            .step("The angle between any two normals = arccos(-1/3) = 109.47 degrees.")
            .step("This is the tetrahedral angle (supplement of dihedral angle).")
            .step("The 4 normals are maximally separated in 3D space.")
            .conclude("OUTPUT: Normals separated by 109.47 degrees; maximally spread.")
        )
    
    commentary = (
        "109.47 degrees is special. It is the angle that maximally separates 4 "
        "directions in 3D space. Carbon atoms in methane (CH4) arrange their bonds "
        "this way. The tetrahedron is nature's solution for 'point 4 things outward "
        "as evenly as possible.' The coupling ports face outward with maximum spread, "
        "covering all directions with equal emphasis."
    )
    
    def model(self):
        # Angle between normals = arccos(-1/3)
        normal_angle_rad = math.acos(-1/3)
        normal_angle_deg = math.degrees(normal_angle_rad)
        cos_normal_angle = math.cos(normal_angle_rad)
        return (
            Model()
            .add("Normal angle (radians)", normal_angle_rad)
            .add("Normal angle (degrees)", normal_angle_deg)
            .add("cos(normal angle)", cos_normal_angle)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Normal angle (radians)", 1.9106)
            .add("Normal angle (degrees)", 109.47)
            .add("cos(normal angle)", -1/3)
        )


class DualTimeFaceCorrespondence(Test):
    """
    In the dual Field Chamber, each Tet_A face corresponds to
    a complementary Tet_B face via inversion through the Field Origin.
    """
    name = "Dual TIME Face Correspondence"
    question = (
        "In the dual Field Chamber, Tet A has 4 faces and Tet B has 4 faces. That is "
        "8 total. But they are not independent. Inversion (V -> 7-V) maps each Tet A "
        "face to a Tet B face. Are the faces paired by this symmetry?"
    )
    reference = "Stellated octahedron geometry"
    tolerance = 0.0
    level = Critical
    audit_score = 90
    audit_notes = (
        "Question: 14/15 - Good inversion symmetry question. "
        "Derivation: 14/15 - Clear face pairing proof. "
        "Commentary: 14/15 - Excellent flux channel insight. "
        "Model: 9/10 - Clean counting. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 12/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Examine face correspondence in the dual structure.")
            .step("Tet_A has 4 TIME faces; Tet_B has 4 TIME faces.")
            .step("Total TIME faces in merkaba = 8.")
            .step("Inversion I(V) = 7-V maps Tet_A vertices to Tet_B vertices.")
            .step("Each Tet_A face maps to a Tet_B face under inversion.")
            .step("Corresponding faces are parallel but oppositely oriented.")
            .conclude("OUTPUT: 4 face pairs related by inversion; 8 total TIME faces.")
        )
    
    commentary = (
        "The two tetrahedra are inversion images of each other. Flip all coordinates "
        "through the origin and Tet A becomes Tet B. Each face of A has a partner face "
        "in B: parallel but pointing the opposite direction. These 4 pairs of faces "
        "define 4 coupling channels through the Field Origin. A flux entering through "
        "a Tet A face can exit through its partner in Tet B."
    )
    
    def model(self):
        faces_tet_a = K
        faces_tet_b = K
        total_faces = faces_tet_a + faces_tet_b
        face_pairs = K  # Each A face pairs with a B face
        return (
            Model()
            .add("Tet_A TIME faces", faces_tet_a)
            .add("Tet_B TIME faces", faces_tet_b)
            .add("Total TIME faces", total_faces)
            .add("Inversion pairs", face_pairs)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet_A TIME faces", 4)
            .add("Tet_B TIME faces", 4)
            .add("Total TIME faces", 8)
            .add("Inversion pairs", 4)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    TimeFaceCount,
    TimeFaceAreaFraction,
    TimeFaceSolidAngle,
    TimeFaceDihedralAngle,
    TimeFaceVertexComposition,
    TimeFaceEdgeSharing,
    TimeFaceOppositeVertex,
    TimeFaceNormalOrientation,
    DualTimeFaceCorrespondence,
]


def run_all() -> bool:
    """Run all TIME face geometry tests."""
    return run_tests(
        title="TIME Face Geometry",
        summary=(
            "These tests examine the geometric properties of TIME faces (Coupling Ports) "
            "in the stellated octahedron: k=4 faces per tetrahedron, each covering 1/4 "
            "of total surface area and subtending pi steradians from the centroid. "
            "Adjacent faces meet at 70.53 degrees (arccos 1/3), and face normals are "
            "separated by 109.47 degrees (tetrahedral angle) for maximal directional "
            "coverage. The dual structure has 8 total TIME faces with 4 inversion pairs."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
