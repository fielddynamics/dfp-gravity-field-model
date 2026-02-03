"""
Parallel Coupling Port Traversal
================================

This module tracks Coupling Port (face) completion in both Field Chambers
during closure cycles. It monitors step-by-step activation for Tet_A and
Tet_B in parallel.

Key rules:
- Each vertex belongs to exactly 3 Coupling Ports in its Field Chamber
- Visiting a vertex "touches" those 3 Coupling Ports
- A Coupling Port is complete when all 3 vertices have been visited
- TIME Coupling Ports: FACE_A7, FACE_B0; SPATIAL: the other 6
"""

import sys
import os
import math
from typing import Dict, Optional, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

# =============================================================================
# CONSTANTS
# =============================================================================

PI_BASE8_FRACTIONAL = [
    1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, 0, 2, 1, 5,
    1, 4, 2, 3, 0, 5, 5, 4, 5, 4, 1, 2, 2, 0, 3, 5, 2, 3, 4, 6,
    5, 4, 2, 1, 1, 3, 2, 6, 7, 2, 2, 3, 0, 1, 4, 6, 5, 4, 4, 0,
]

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}

FACES = {
    'FACE_A1': frozenset({2, 4, 7}),
    'FACE_A2': frozenset({1, 4, 7}),
    'FACE_A4': frozenset({1, 2, 7}),
    'FACE_A7': frozenset({1, 2, 4}),  # TIME
    'FACE_B0': frozenset({3, 5, 6}),  # TIME
    'FACE_B3': frozenset({0, 5, 6}),
    'FACE_B5': frozenset({0, 3, 6}),
    'FACE_B6': frozenset({0, 3, 5}),
}

TIME_FACES = {'FACE_A7', 'FACE_B0'}
SPATIAL_FACES = set(FACES.keys()) - TIME_FACES


def get_pi_base8(n_digits, include_integer=True):
    if include_integer:
        return [3] + PI_BASE8_FRACTIONAL[:n_digits]
    return PI_BASE8_FRACTIONAL[:n_digits]


def get_tetrahedron(v):
    return 'A' if v in TET_A else 'B'


def get_faces_containing_vertex(vertex):
    return {name: verts for name, verts in FACES.items() if vertex in verts}


def track_parallel_faces(n_digits=50):
    """Track face completion for both tetrahedra."""
    digits = get_pi_base8(n_digits, include_integer=True)
    
    face_state = {name: set() for name in FACES}
    face_completed_at = {name: None for name in FACES}
    
    cumsum = 0
    for step, digit in enumerate(digits):
        cumsum += digit
        vertex = cumsum % 8
        
        faces_touched = get_faces_containing_vertex(vertex)
        for fname in faces_touched:
            face_state[fname].add(vertex)
            if face_completed_at[fname] is None and face_state[fname] == FACES[fname]:
                face_completed_at[fname] = step
    
    return face_state, face_completed_at


# =============================================================================
# TESTS
# =============================================================================

class TetAFacesUseTetAVertices(GFDTest):
    """
    Tet A faces contain only Tet A vertices (1, 2, 4, 7).
    """
    name = "Tet A Faces Use Tet A Vertices"
    question = "Do all k=4 Coupling Ports of Tetrahedron A contain only Tet A vertices {1,2,4,7}?"
    reference_source = "Tetrahedron definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: A tetrahedron's faces are triangles using only its own vertices. "
        "STEP 1: Tet A vertices = {1,2,4,7} (odd parity set). "
        "STEP 2: FACE_A1 = {2,4,7} ⊂ Tet A. "
        "STEP 3: FACE_A2 = {1,4,7} ⊂ Tet A. "
        "STEP 4: FACE_A4 = {1,2,7} ⊂ Tet A. "
        "STEP 5: FACE_A7 = {1,2,4} ⊂ Tet A. "
        "OUTPUT: All Tet A faces correct = 1."
    )
    commentary = None  # Structural verification of face membership
    
    def model(self) -> Dict[str, float]:
        all_correct = True
        for fname in ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7']:
            if not all(v in TET_A for v in FACES[fname]):
                all_correct = False
        return {"All Tet A faces correct": 1 if all_correct else 0}
    
    def observations(self) -> Dict[str, float]:
        return {"All Tet A faces correct": 1}


class TetBFacesUseTetBVertices(GFDTest):
    """
    Tet B faces contain only Tet B vertices (0, 3, 5, 6).
    """
    name = "Tet B Faces Use Tet B Vertices"
    question = "Do all k=4 Coupling Ports of Tetrahedron B contain only Tet B vertices {0,3,5,6}?"
    reference_source = "Tetrahedron definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: A tetrahedron's faces are triangles using only its own vertices. "
        "STEP 1: Tet B vertices = {0,3,5,6} (even parity set). "
        "STEP 2: FACE_B0 = {3,5,6} ⊂ Tet B. "
        "STEP 3: FACE_B3 = {0,5,6} ⊂ Tet B. "
        "STEP 4: FACE_B5 = {0,3,6} ⊂ Tet B. "
        "STEP 5: FACE_B6 = {0,3,5} ⊂ Tet B. "
        "OUTPUT: All Tet B faces correct = 1."
    )
    commentary = None  # Structural verification of face membership
    
    def model(self) -> Dict[str, float]:
        all_correct = True
        for fname in ['FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6']:
            if not all(v in TET_B for v in FACES[fname]):
                all_correct = False
        return {"All Tet B faces correct": 1 if all_correct else 0}
    
    def observations(self) -> Dict[str, float]:
        return {"All Tet B faces correct": 1}


class TimeFacesIdentified(GFDTest):
    """
    TIME faces are FACE_A7 and FACE_B0 (exactly 2).
    """
    name = "TIME Faces Identified"
    question = "Are exactly 2 TIME Coupling Ports identified (FACE_A7 and FACE_B0), perpendicular to the apex axis?"
    reference_source = "Face classification"
    tolerance = 0.0
    derivation = (
        "PREMISE: TIME faces are those perpendicular to the V0-V7 apex axis. "
        "STEP 1: FACE_A7 = {1,2,4} is opposite V7 in Tet A → TIME face. "
        "STEP 2: FACE_B0 = {3,5,6} is opposite V0 in Tet B → TIME face. "
        "STEP 3: Count TIME faces = 2 (one per tetrahedron). "
        "STEP 4: Remaining 6 faces are SPATIAL faces. "
        "OUTPUT: TIME face count = 2."
    )
    commentary = None  # Structural verification of TIME face identification
    
    def model(self) -> Dict[str, float]:
        return {
            "FACE_A7 is TIME": 1 if 'FACE_A7' in TIME_FACES else 0,
            "FACE_B0 is TIME": 1 if 'FACE_B0' in TIME_FACES else 0,
            "TIME face count": len(TIME_FACES),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "FACE_A7 is TIME": 1,
            "FACE_B0 is TIME": 1,
            "TIME face count": 2,
        }


class ParallelTrackingWorks(GFDTest):
    """
    Parallel face tracking captures all steps.
    """
    name = "Parallel Tracking Works"
    question = "Does the parallel face tracking algorithm correctly process all traversal steps and record progress for all 8 faces?"
    reference_source = None  # Algorithm verification
    derivation = (
        "PREMISE: The algorithm should track vertex visits for all 8 Coupling Ports simultaneously. "
        "STEP 1: Initialize empty vertex sets for all 8 faces. "
        "STEP 2: For each traversal step, add current vertex to all faces containing it. "
        "STEP 3: Count faces that have made progress (non-empty vertex sets). "
        "STEP 4: After sufficient steps, verify all 8 faces have some progress. "
        "OUTPUT: Faces with progress = 8."
    )
    commentary = None  # Algorithm verification
    
    def model(self) -> Dict[str, float]:
        face_state, face_completed = track_parallel_faces(50)
        faces_with_progress = sum(1 for s in face_state.values() if len(s) > 0)
        return {
            "Faces with progress": faces_with_progress,
            "Total faces": 8,
        }


class BothTetrahedraMakeProgress(GFDTest):
    """
    Both Tet_A and Tet_B make progress during traversal.
    """
    name = "Both Tetrahedra Progress"
    question = "Do both Tetrahedron A and Tetrahedron B make Coupling Port progress during traversal, confirming bidirectional bimetric coupling?"
    reference_source = "Bimetric coupling"
    tolerance = 0.0
    derivation = (
        "PREMISE: Bimetric coupling requires simultaneous engagement of both Field Chambers. "
        "STEP 1: Track face completion progress for Tet A faces {A1,A2,A4,A7}. "
        "STEP 2: Track face completion progress for Tet B faces {B0,B3,B5,B6}. "
        "STEP 3: Check if any Tet A face has vertices visited. "
        "STEP 4: Check if any Tet B face has vertices visited. "
        "OUTPUT: Tet A progress = 1, Tet B progress = 1."
    )
    commentary = (
        "Parallel progress in both Field Chambers confirms the bimetric coupling "
        "operates bidirectionally. The traversal advances Coupling Port completion "
        "in Tetrahedron A and B simultaneously rather than sequentially."
    )
    
    def model(self) -> Dict[str, float]:
        face_state, _ = track_parallel_faces(50)
        
        tet_a_progress = any(len(face_state[f]) > 0 
                           for f in ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7'])
        tet_b_progress = any(len(face_state[f]) > 0 
                           for f in ['FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6'])
        
        return {
            "Tet A progress": 1 if tet_a_progress else 0,
            "Tet B progress": 1 if tet_b_progress else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Tet A progress": 1,
            "Tet B progress": 1,
        }


class AllFacesCompleteEventually(GFDTest):
    """
    All 8 faces complete within reasonable number of digits.
    """
    name = "All Faces Complete"
    question = "Do all 8 Coupling Ports complete (all 3 vertices visited) within 60 traversal digits?"
    reference_source = "Complete coverage"
    tolerance = 0.0
    derivation = (
        "PREMISE: Complete coverage requires visiting all 3 vertices of each of 8 faces. "
        "STEP 1: Track which vertices have been visited for each face. "
        "STEP 2: A face is complete when its vertex set equals its defining vertex set. "
        "STEP 3: Count completed faces after 60 digits of traversal. "
        "STEP 4: With ergodic sampling, all 8 vertices are visited within ~20-30 steps. "
        "OUTPUT: Faces completed = 8."
    )
    commentary = (
        "Complete Coupling Port coverage within dozens of digits demonstrates "
        "efficient traversal. Pi's digit sequence provides sufficient variation "
        "to reach all vertices of all Coupling Ports in both Field Chambers."
    )
    
    def model(self) -> Dict[str, float]:
        _, face_completed = track_parallel_faces(60)
        completed_count = sum(1 for step in face_completed.values() if step is not None)
        return {
            "Faces completed": completed_count,
            "Total faces": 8,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Faces completed": 8,
            "Total faces": 8,
        }


class CumulativeFaceCoverage(GFDTest):
    """
    Cumulatively, all 8 faces are touched within first 50 digits.
    """
    name = "Cumulative Face Coverage"
    question = "Are all 8 Coupling Ports 'touched' (at least one vertex visited) within 50 traversal digits?"
    reference_source = "Complete sampling"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each face should receive at least partial coverage within early traversal. "
        "STEP 1: Each vertex belongs to exactly 3 faces (vertices opposite it in its tetrahedron). "
        "STEP 2: Visiting any vertex touches 3 faces simultaneously. "
        "STEP 3: With 8 vertices total, visiting all 8 touches all faces. "
        "STEP 4: Count faces with at least 1 vertex visited after 50 digits. "
        "OUTPUT: Faces touched = 8."
    )
    commentary = None  # Coverage verification
    
    def model(self) -> Dict[str, float]:
        face_state, _ = track_parallel_faces(50)
        faces_touched = sum(1 for s in face_state.values() if len(s) > 0)
        return {"Faces touched": faces_touched}
    
    def observations(self) -> Dict[str, float]:
        return {"Faces touched": 8}


class SpatialFaceCount(GFDTest):
    """
    There are exactly 6 SPATIAL faces (3 per tetrahedron).
    """
    name = "Spatial Face Count"
    question = "Are there exactly 6 SPATIAL Coupling Ports (d=k-1=3 per tetrahedron), corresponding to 3 spatial dimensions?"
    reference_source = "Face classification"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each tetrahedron has k=4 faces; one is TIME, k-1=3 are SPATIAL. "
        "STEP 1: Total faces = 2k = 8. "
        "STEP 2: TIME faces = 2 (one per tetrahedron). "
        "STEP 3: SPATIAL faces = Total - TIME = 8 - 2 = 6. "
        "STEP 4: Per tetrahedron: 6/2 = 3 SPATIAL faces. "
        "OUTPUT: SPATIAL faces = 6."
    )
    commentary = None  # Structural count verification
    
    def model(self) -> Dict[str, float]:
        return {"SPATIAL faces": len(SPATIAL_FACES)}
    
    def observations(self) -> Dict[str, float]:
        return {"SPATIAL faces": 6}


class EachFaceHasThreeVertices(GFDTest):
    """
    Each face has exactly 3 vertices (triangular faces).
    """
    name = "Faces Have 3 Vertices"
    question = "Does each Coupling Port have exactly 3 vertices, forming triangular faces as required by tetrahedral geometry?"
    reference_source = "Tetrahedron face geometry"
    tolerance = 0.0
    derivation = (
        "PREMISE: A tetrahedron's faces are triangles formed by any 3 of its 4 vertices. "
        "STEP 1: Each face excludes exactly 1 vertex (the opposite apex). "
        "STEP 2: Therefore each face contains k-1 = 4-1 = 3 vertices. "
        "STEP 3: Verify: count |FACE| for each of the 8 defined faces. "
        "OUTPUT: All faces have 3 vertices = 1."
    )
    commentary = None  # Fundamental geometric property
    
    def model(self) -> Dict[str, float]:
        all_three = all(len(verts) == 3 for verts in FACES.values())
        return {"All faces have 3 vertices": 1 if all_three else 0}
    
    def observations(self) -> Dict[str, float]:
        return {"All faces have 3 vertices": 1}


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    TetAFacesUseTetAVertices,
    TetBFacesUseTetBVertices,
    TimeFacesIdentified,
    ParallelTrackingWorks,
    BothTetrahedraMakeProgress,
    AllFacesCompleteEventually,
    CumulativeFaceCoverage,
    SpatialFaceCount,
    EachFaceHasThreeVertices,
]


def run_all_tests() -> bool:
    """Run all parallel Coupling Port traversal tests."""
    return run_test_group(
        title="Parallel Coupling Port Traversal",
        summary=(
            "These tests track Coupling Port completion in both Field Chambers during "
            "traversal. Tet A Coupling Ports contain only Tet A vertices (1,2,4,7), and "
            "Tet B Coupling Ports contain only Tet B vertices (0,3,5,6). There are 2 TIME "
            "Coupling Ports (FACE_A7, FACE_B0) and 6 SPATIAL Coupling Ports. Both Field "
            "Chambers make progress during traversal, and all 8 Coupling Ports complete "
            "within a reasonable digit count. Each Coupling Port is triangular with 3 vertices."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
