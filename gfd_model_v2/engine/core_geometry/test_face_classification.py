"""
Face Classification
====================

The stellated octahedron has 8 triangular faces (4 per tetrahedron). The model
classifies these into two types based on their geometric orientation:

- TIME faces (2): FACE_A7 and FACE_B0, opposite the apexes V7 and V0
- SPATIAL faces (6): The remaining faces that include an apex vertex

This 2:6 ratio produces f_time = 2/8 = 1/4. When combined with the spin
quantum number 2, this yields (2/8) x 2 = 1/2, corresponding to spin-1/2.
The classification is purely geometric, based on face orientation.
"""

import sys
import os
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from common import FACES, TIME_FACES, SPATIAL_FACES, TET_A, TET_B


# =============================================================================
# TESTS
# =============================================================================

class EightFacesTotal(GFDTest):
    """
    The stellated octahedron has exactly 8 triangular faces:
    4 faces from each of the two constituent tetrahedra.
    """
    name = "Eight Faces Total"
    question = "Does the stellated octahedron have exactly 2k=8 Coupling Ports (faces), establishing the spin derivation denominator?"
    reference_source = "Geometry (4 + 4)"
    tolerance = 0.001
    derivation = (
        "PREMISE: The stellated octahedron comprises two tetrahedra, each with k=4 faces. "
        "STEP 1: Tetrahedron A contributes k = 4 faces. "
        "STEP 2: Tetrahedron B contributes k = 4 faces. "
        "STEP 3: Total Coupling Ports: k + k = 2k = 8. "
        "STEP 4: This count becomes the denominator in spin formula: S = (2/8) * 2. "
        "OUTPUT: The dual Field Chamber has 8 Coupling Ports."
    )
    commentary = (
        "Eight Coupling Ports arise from two tetrahedra contributing four faces each. "
        "This count corresponds to the 8 gluon types in SU(3) color theory, suggesting "
        "a possible topological connection between Field Chamber faces and gauge bosons."
    )
    
    def model(self) -> Dict[str, float]:
        return {"Total faces": len(FACES)}
    
    def observations(self) -> Dict[str, float]:
        return {"Total faces": 8}


class FourFacesPerTetrahedron(GFDTest):
    """
    Each tetrahedron contributes exactly 4 faces to the structure.
    This is a fundamental property of tetrahedral geometry.
    """
    name = "Four Faces Per Tetrahedron"
    question = "Does each tetrahedron contribute exactly k=4 Coupling Ports, matching the topology constant?"
    reference_source = "Tetrahedral geometry"
    tolerance = 0.001
    derivation = (
        "PREMISE: A tetrahedron has k=4 triangular faces by definition. "
        "STEP 1: Count faces with 'FACE_A' prefix -> Tetrahedron A faces. "
        "STEP 2: Count faces with 'FACE_B' prefix -> Tetrahedron B faces. "
        "STEP 3: Verify both counts equal k = 4. "
        "STEP 4: This matches the Field Closure topology constant. "
        "OUTPUT: Each Field Chamber contributes k=4 Coupling Ports."
    )
    commentary = None  # Fundamental geometric property
    
    def model(self) -> Dict[str, float]:
        tet_a_faces = len([f for f in FACES.keys() if 'FACE_A' in f])
        tet_b_faces = len([f for f in FACES.keys() if 'FACE_B' in f])
        return {
            "Tet_A faces": tet_a_faces,
            "Tet_B faces": tet_b_faces,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Tet_A faces": 4,
            "Tet_B faces": 4,
        }


class EachFaceIsTriangle(GFDTest):
    """
    Each face must be a triangle (3 vertices). This is verified by
    checking that every face definition contains exactly 3 vertices.
    """
    name = "Each Face Is Triangle"
    question = "Does each Coupling Port have exactly k-1=3 vertices, defining triangular faces?"
    reference_source = "Definition of face"
    tolerance = 0.001
    derivation = (
        "PREMISE: A tetrahedral face is a triangle with k-1 = 3 vertices. "
        "STEP 1: For each face in the FACES dictionary, count vertices. "
        "STEP 2: Verify all 8 faces have exactly 3 vertices. "
        "STEP 3: Each Coupling Port is thus a triangular channel. "
        "STEP 4: The k-1 = 3 vertices per face relates to d=3 spatial dimensions. "
        "OUTPUT: All 8 Coupling Ports are triangular (3 vertices each)."
    )
    commentary = None  # Fundamental geometric property
    
    def model(self) -> Dict[str, float]:
        triangles = sum(1 for verts in FACES.values() if len(verts) == 3)
        return {"Faces with 3 vertices": triangles}
    
    def observations(self) -> Dict[str, float]:
        return {"Faces with 3 vertices": 8}


class TimeFacesCount(GFDTest):
    """
    There are exactly 2 TIME faces: FACE_A7 (opposite apex V7) and
    FACE_B0 (opposite apex V0). These faces are opposite the apexes
    and point inward toward the center of the structure.
    """
    name = "TIME Faces Count"
    question = "Are there exactly 2 TIME Coupling Ports (one per tetrahedron), providing the spin formula numerator?"
    reference_source = "Topology (2 apexes)"
    tolerance = 0.001
    derivation = (
        "PREMISE: TIME faces are defined as those opposite the apex vertices. "
        "STEP 1: Each tetrahedron has exactly 1 apex (V7 for Tet A, V0 for Tet B). "
        "STEP 2: Each tetrahedron has exactly 1 face opposite its apex. "
        "STEP 3: TIME faces = {FACE_A7, FACE_B0}, count = 2. "
        "STEP 4: This provides numerator in spin: S = (2/8) * 2 = 1/2. "
        "OUTPUT: Exactly 2 TIME Coupling Ports exist."
    )
    commentary = (
        "Two TIME Coupling Ports correspond to one per tetrahedron, positioned "
        "opposite the apex vertices. The 2:6 ratio of TIME to SPATIAL faces "
        "produces the fraction 1/4 that underlies the spin-1/2 calculation."
    )
    
    def model(self) -> Dict[str, float]:
        return {"TIME faces": len(TIME_FACES)}
    
    def observations(self) -> Dict[str, float]:
        return {"TIME faces": 2}


class SpatialFacesCount(GFDTest):
    """
    The remaining 6 faces are classified as SPATIAL. These faces
    include an apex vertex and point outward from the structure.
    """
    name = "SPATIAL Faces Count"
    question = "Are there exactly 2(k-1)=6 SPATIAL Coupling Ports, each containing an apex vertex?"
    reference_source = "Topology (8 - 2)"
    tolerance = 0.001
    derivation = (
        "PREMISE: SPATIAL faces are those containing the apex vertex (not opposite it). "
        "STEP 1: Each tetrahedron has k=4 faces. One is TIME (opposite apex). "
        "STEP 2: Remaining faces per tetrahedron: k - 1 = 3 SPATIAL faces. "
        "STEP 3: Total SPATIAL: 2 * (k-1) = 2 * 3 = 6. "
        "STEP 4: Verify: 2k - 2 = 8 - 2 = 6. "
        "OUTPUT: Exactly 6 SPATIAL Coupling Ports exist (3 per Field Chamber)."
    )
    commentary = (
        "Six SPATIAL Coupling Ports (3 per tetrahedron) correspond to the "
        "number of quark flavors and edges per tetrahedron. This multiplicity "
        "may reflect the three spatial dimensions with dual representation "
        "across both Field Chambers."
    )
    
    def model(self) -> Dict[str, float]:
        return {"SPATIAL faces": len(SPATIAL_FACES)}
    
    def observations(self) -> Dict[str, float]:
        return {"SPATIAL faces": 6}


class TimeFacesIdentified(GFDTest):
    """
    The TIME faces must be specifically FACE_A7 and FACE_B0, which are
    the faces opposite the apex vertices V7 and V0 respectively.
    """
    name = "TIME Faces Identified"
    question = "Are the TIME faces specifically {FACE_A7, FACE_B0}, opposite the apex vertices V7 and V0?"
    reference_source = "Apex definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: TIME faces are defined as opposite the apex vertices. "
        "STEP 1: Tet A apex is V7 (111). Face opposite V7 is FACE_A7. "
        "STEP 2: Tet B apex is V0 (000). Face opposite V0 is FACE_B0. "
        "STEP 3: TIME_FACES set should equal {'FACE_A7', 'FACE_B0'}. "
        "STEP 4: Verify set equality. "
        "OUTPUT: TIME faces are correctly identified as {FACE_A7, FACE_B0}."
    )
    commentary = None  # Structural verification of face classification
    
    def model(self) -> Dict[str, float]:
        expected = {'FACE_A7', 'FACE_B0'}
        correct = 1 if TIME_FACES == expected else 0
        return {"Correct identification": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Correct identification": 1}


class TimeFaceA7Vertices(GFDTest):
    """
    FACE_A7 is the face of Tet_A opposite the apex V7. It must contain
    the other 3 vertices of Tet_A: {1, 2, 4}.
    """
    name = "FACE_A7 Vertices"
    question = "Does FACE_A7 contain exactly vertices {1, 2, 4}, the k-1=3 non-apex vertices of Tet A?"
    reference_source = "Tet_A definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: FACE_A7 is opposite apex V7, so it contains the other Tet A vertices. "
        "STEP 1: Tet A vertices: {1, 2, 4, 7}. "
        "STEP 2: Remove apex V7: {1, 2, 4}. "
        "STEP 3: FACE_A7 should contain exactly these k-1 = 3 vertices. "
        "STEP 4: Verify FACES['FACE_A7'] == {1, 2, 4}. "
        "OUTPUT: FACE_A7 correctly contains {1, 2, 4}."
    )
    commentary = None  # Structural verification
    
    def model(self) -> Dict[str, float]:
        expected = frozenset({1, 2, 4})
        actual = FACES.get('FACE_A7', frozenset())
        correct = 1 if actual == expected else 0
        return {"Vertices correct": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Vertices correct": 1}


class TimeFaceB0Vertices(GFDTest):
    """
    FACE_B0 is the face of Tet_B opposite the apex V0. It must contain
    the other 3 vertices of Tet_B: {3, 5, 6}.
    """
    name = "FACE_B0 Vertices"
    question = "Does FACE_B0 contain exactly vertices {3, 5, 6}, the k-1=3 non-apex vertices of Tet B?"
    reference_source = "Tet_B definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: FACE_B0 is opposite apex V0, so it contains the other Tet B vertices. "
        "STEP 1: Tet B vertices: {0, 3, 5, 6}. "
        "STEP 2: Remove apex V0: {3, 5, 6}. "
        "STEP 3: FACE_B0 should contain exactly these k-1 = 3 vertices. "
        "STEP 4: Verify FACES['FACE_B0'] == {3, 5, 6}. "
        "OUTPUT: FACE_B0 correctly contains {3, 5, 6}."
    )
    commentary = None  # Structural verification
    
    def model(self) -> Dict[str, float]:
        expected = frozenset({3, 5, 6})
        actual = FACES.get('FACE_B0', frozenset())
        correct = 1 if actual == expected else 0
        return {"Vertices correct": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Vertices correct": 1}


class TimePlusSpatialEqualsTotal(GFDTest):
    """
    TIME and SPATIAL faces must form a complete, disjoint partition
    of all 8 faces. Their union equals all faces, and their
    intersection is empty.
    """
    name = "TIME + SPATIAL = Total"
    question = "Do TIME and SPATIAL faces form a complete, disjoint partition of all 2k=8 Coupling Ports?"
    reference_source = "Set partition"
    tolerance = 0.001
    derivation = (
        "PREMISE: A partition requires disjoint sets with complete coverage. "
        "STEP 1: TIME_FACES = {FACE_A7, FACE_B0}, size = 2. "
        "STEP 2: SPATIAL_FACES = remaining 6 faces. "
        "STEP 3: Check disjoint: TIME ∩ SPATIAL = {} (empty). "
        "STEP 4: Check complete: TIME ∪ SPATIAL = all 8 faces. "
        "OUTPUT: Face classification creates valid 2 + 6 = 8 partition."
    )
    commentary = (
        "The clean partition of Coupling Ports into TIME and SPATIAL categories "
        "reflects a fundamental dimensional decomposition within the Field Chamber "
        "structure, paralleling the 3+1 spacetime separation."
    )
    
    def model(self) -> Dict[str, float]:
        union = TIME_FACES | SPATIAL_FACES
        intersection = TIME_FACES & SPATIAL_FACES
        all_faces = set(FACES.keys())
        
        complete = 1 if union == all_faces else 0
        disjoint = 1 if len(intersection) == 0 else 0
        
        return {
            "Union equals all": complete,
            "Sets disjoint": disjoint,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Union equals all": 1,
            "Sets disjoint": 1,
        }


class TimeFacesOppositeApexes(GFDTest):
    """
    By definition, TIME faces are opposite the apexes. FACE_A7 must
    not contain V7, and FACE_B0 must not contain V0.
    """
    name = "TIME Faces Opposite Apexes"
    question = "Do TIME faces exclude their respective apex vertices, positioning them perpendicular to the V0-V7 axis?"
    reference_source = "Face-apex relationship"
    tolerance = 0.001
    derivation = (
        "PREMISE: A face opposite vertex V excludes V from its vertex set. "
        "STEP 1: FACE_A7 is opposite V7, so it should not contain V7. "
        "STEP 2: FACE_B0 is opposite V0, so it should not contain V0. "
        "STEP 3: Verify: 7 not in FACES['FACE_A7'] and 0 not in FACES['FACE_B0']. "
        "STEP 4: Both conditions satisfied. "
        "OUTPUT: TIME faces correctly exclude their corresponding apexes."
    )
    commentary = (
        "TIME Coupling Ports exclude their respective apex vertices, positioning "
        "them perpendicular to the V0-V7 axis. This geometric arrangement creates "
        "a distinguished temporal direction within the Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        face_a7 = FACES.get('FACE_A7', frozenset())
        face_b0 = FACES.get('FACE_B0', frozenset())
        
        a7_excludes = 1 if 7 not in face_a7 else 0
        b0_excludes = 1 if 0 not in face_b0 else 0
        
        return {
            "FACE_A7 excludes V7": a7_excludes,
            "FACE_B0 excludes V0": b0_excludes,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "FACE_A7 excludes V7": 1,
            "FACE_B0 excludes V0": 1,
        }


class FaceVerticesInCorrectTetrahedron(GFDTest):
    """
    Each face's vertices must belong to its tetrahedron. Tet_A faces
    contain only Tet_A vertices, and Tet_B faces contain only Tet_B
    vertices.
    """
    name = "Face Vertices in Correct Tetrahedron"
    question = "Do all Tet A faces contain only Tet A vertices, and all Tet B faces contain only Tet B vertices?"
    reference_source = "Tetrahedron definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: Each face belongs to one tetrahedron and should contain only that tetrahedron's vertices. "
        "STEP 1: Tet A vertices: {1, 2, 4, 7}. Tet B vertices: {0, 3, 5, 6}. "
        "STEP 2: For each FACE_A*, verify all vertices are in Tet A. "
        "STEP 3: For each FACE_B*, verify all vertices are in Tet B. "
        "STEP 4: Count faces with correct vertex membership. "
        "OUTPUT: All 8 faces have vertices belonging to their correct tetrahedron."
    )
    commentary = None  # Structural verification of face-tetrahedron membership
    
    def model(self) -> Dict[str, float]:
        correct = 0
        for face_name in ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7']:
            verts = FACES.get(face_name, frozenset())
            if all(v in TET_A for v in verts):
                correct += 1
        for face_name in ['FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6']:
            verts = FACES.get(face_name, frozenset())
            if all(v in TET_B for v in verts):
                correct += 1
        return {"Faces with correct vertices": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Faces with correct vertices": 8}


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    EightFacesTotal,
    FourFacesPerTetrahedron,
    EachFaceIsTriangle,
    TimeFacesCount,
    SpatialFacesCount,
    TimeFacesIdentified,
    TimeFaceA7Vertices,
    TimeFaceB0Vertices,
    TimePlusSpatialEqualsTotal,
    TimeFacesOppositeApexes,
    FaceVerticesInCorrectTetrahedron,
]


def run_all_tests() -> bool:
    """Run all face classification tests."""
    return run_test_group(
        title="Face Classification",
        summary=(
            "The stellated octahedron has 8 triangular faces, 4 per tetrahedron. The model "
            "classifies these geometrically: 2 TIME faces (opposite the apexes, pointing "
            "inward) and 6 SPATIAL faces (including apexes, pointing outward). This produces "
            "f_time = 2/8 = 1/4. The model associates this ratio with spin: (2/8) x 2 = 1/2, "
            "consistent with spin-1/2 particles. This correspondence is geometric, not derived "
            "from quantum mechanics."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
