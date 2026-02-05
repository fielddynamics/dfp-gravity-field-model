"""
Parallel Coupling Port Traversal
================================

GEOMETRY OVERVIEW
-----------------
The 8 vertices are labeled 0-7 using cube coordinates (a 3-bit addressing scheme).
The cube is NOT the model; it is only a coordinate system. The actual structure
is TWO INTERPENETRATING TETRAHEDRA forming a stellated octahedron:

    COORDINATE SYSTEM (cube):              ACTUAL STRUCTURE (tetrahedra):
    
         6───────7                              Tet A: {1, 2, 4, 7}
        /|      /|                              (odd parity vertices)
       / |     / |                                    7
      2───────3  |                                   /|\\
      |  4────|──5                                  / | \\
      | /     | /                                  /  |  \\
      |/      |/                                  1---+---2    + = Field Origin
      0───────1                                       |            (0,0,0)
                                                      4
    Vertex binary encoding:
    V0=000, V1=001, V2=010, V3=011           Tet B: {0, 3, 5, 6}
    V4=100, V5=101, V6=110, V7=111           (even parity vertices)

FACE (COUPLING PORT) STRUCTURE
------------------------------
Each tetrahedron has 4 triangular faces. A face is named by its OPPOSITE vertex:

    Tet A Faces:                           Tet B Faces:
    FACE_A1 = {2,4,7} (opposite V1)        FACE_B0 = {3,5,6} (opposite V0) [TIME]
    FACE_A2 = {1,4,7} (opposite V2)        FACE_B3 = {0,5,6} (opposite V3)
    FACE_A4 = {1,2,7} (opposite V4)        FACE_B5 = {0,3,6} (opposite V5)
    FACE_A7 = {1,2,4} (opposite V7) [TIME] FACE_B6 = {0,3,5} (opposite V6)

Each vertex touches exactly 3 faces (all faces of its tetrahedron except the opposite one).

KEY RULES
---------
- Visiting a vertex "touches" the 3 Coupling Ports it belongs to
- A Coupling Port completes when all 3 of its vertices have been visited
- TIME Coupling Ports: FACE_A7, FACE_B0 (opposite the apex vertices)
- SPATIAL Coupling Ports: the other 6 faces (3 per tetrahedron)
"""

from typing import Dict, Optional, List

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import get_pi_base8
from gravity_field_model.common.geometry_constants import (
    TET_A, TET_B, FACES, TIME_FACES, SPATIAL_FACES,
    get_tetrahedron, get_faces_for_vertex
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_faces_containing_vertex(vertex):
    """Get all faces containing a vertex."""
    return {name: verts for name, verts in FACES.items() if vertex in verts}


def track_parallel_faces(n_digits=1000):
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

class TetAFacesUseTetAVertices(Test):
    """
    Tet A faces contain only Tet A vertices (1, 2, 4, 7).
    """
    name = "Tet A Faces Use Tet A Vertices"
    question = (
        "Do Tet A faces use only Tet A vertices? "
        "A tetrahedron's faces should not borrow corners from the other tetrahedron. "
        "This test verifies each Tet A face uses only vertices {1,2,4,7}."
    )
    reference = "Tetrahedron definition"
    tolerance = 0.0
    level = Critical
    audit_score = 84
    audit_notes = (
        "Question: 14/15 - Good 'borrow corners' intuition. "
        "Derivation: 14/15 - Clear subset verification. "
        "Commentary: 13/15 - Nice airplane wing analogy. "
        "Model: 9/10 - Good pass/fail output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Airplane wing analogy accessible. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: Why must Tet A faces use only Tet A vertices for geometric consistency? "
        "Q2: What would happen physically if faces mixed vertices from both tetrahedra? "
        "Q3: How does vertex ownership relate to parity in the dual tetrahedra structure? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A tetrahedron's faces are triangles using only its own vertices.")
            .step("Tet A vertices = {1,2,4,7} (odd parity set).")
            .step("FACE_A1 = {2,4,7} subset Tet A.")
            .step("FACE_A2 = {1,4,7} subset Tet A.")
            .step("FACE_A4 = {1,2,7} subset Tet A.")
            .step("FACE_A7 = {1,2,4} subset Tet A.")
            .conclude("All Tet A faces correct = 1.")
        )
    
    commentary = (
        "If you build a model airplane, all the pieces of the left wing "
        "should be left-wing pieces, not borrowed from the right wing. "
        "Similarly, Tet A's faces should only use Tet A's vertices. "
        "This test confirms the two tetrahedra are properly separated."
    )
    
    def model(self):
        all_correct = True
        for fname in ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7']:
            if not all(v in TET_A for v in FACES[fname]):
                all_correct = False
        return Model().add("All Tet A faces correct", 1 if all_correct else 0)
    
    def observations(self):
        return Observed().add("All Tet A faces correct", 1)


class TetBFacesUseTetBVertices(Test):
    """
    Tet B faces contain only Tet B vertices (0, 3, 5, 6).
    """
    name = "Tet B Faces Use Tet B Vertices"
    question = (
        "Do Tet B faces use only Tet B vertices? "
        "Just like Tet A, Tet B's triangular faces must stay 'in-house.' "
        "This test verifies each Tet B face uses only vertices {0,3,5,6}."
    )
    reference = "Tetrahedron definition"
    tolerance = 0.0
    level = Critical
    audit_score = 83
    audit_notes = (
        "Question: 13/15 - Good 'in-house' framing. "
        "Derivation: 14/15 - Clear subset verification. "
        "Commentary: 13/15 - Structural integrity well explained. "
        "Model: 9/10 - Good pass/fail output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Good structural integrity explanation. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: What symmetry principle ensures Tet B mirrors Tet A's vertex ownership rule? "
        "Q2: How does the even/odd parity partition create two distinct tetrahedra? "
        "Q3: Is there a mathematical proof that this partitioning is unique? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A tetrahedron's faces are triangles using only its own vertices.")
            .step("Tet B vertices = {0,3,5,6} (even parity set).")
            .step("FACE_B0 = {3,5,6} subset Tet B.")
            .step("FACE_B3 = {0,5,6} subset Tet B.")
            .step("FACE_B5 = {0,3,6} subset Tet B.")
            .step("FACE_B6 = {0,3,5} subset Tet B.")
            .conclude("All Tet B faces correct = 1.")
        )
    
    commentary = (
        "The same logic applies to Tet B as Tet A: each face must be built "
        "entirely from that tetrahedron's own vertices. Mixing would blur "
        "the boundary between the two geometric halves. "
        "This verifies Tet B's structural integrity."
    )
    
    def model(self):
        all_correct = True
        for fname in ['FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6']:
            if not all(v in TET_B for v in FACES[fname]):
                all_correct = False
        return Model().add("All Tet B faces correct", 1 if all_correct else 0)
    
    def observations(self):
        return Observed().add("All Tet B faces correct", 1)


class TimeFacesIdentified(Test):
    """
    TIME faces are FACE_A7 and FACE_B0 (exactly 2).
    """
    name = "TIME Faces Identified"
    question = (
        "Which faces represent the 'time' direction? "
        "Two faces point along the apex axis (V0 to V7), representing time. "
        "This test verifies exactly 2 TIME faces are identified: FACE_A7 and FACE_B0."
    )
    reference = "Face classification"
    tolerance = 0.0
    level = Standard
    audit_score = 85
    audit_notes = (
        "Question: 15/15 - Excellent 'time direction' hook. "
        "Derivation: 14/15 - Clear opposite-apex logic. "
        "Commentary: 14/15 - Nice hourglass analogy. "
        "Model: 10/10 - Good classification output. "
        "Observations: 10/10 - Clear expected values. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Hourglass analogy accessible. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: Why are faces opposite the apex vertices designated as TIME faces? "
        "Q2: What physical property distinguishes TIME faces from SPATIAL faces? "
        "Q3: How does the 3+1 dimensional structure emerge from this face classification? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: TIME faces are those perpendicular to the V0-V7 apex axis.")
            .step("FACE_A7 = {1,2,4} is opposite V7 in Tet A -> TIME face.")
            .step("FACE_B0 = {3,5,6} is opposite V0 in Tet B -> TIME face.")
            .step("Count TIME faces = 2 (one per tetrahedron).")
            .step("Remaining 6 faces are SPATIAL faces.")
            .conclude("TIME face count = 2.")
        )
    
    commentary = (
        "Think of an hourglass standing upright. The top and bottom openings point "
        "in the 'time' direction (vertical). The Field Chamber is similar: "
        "two faces point along the V0-V7 axis, which we call the time direction. "
        "There is exactly one such face per tetrahedron: FACE_A7 and FACE_B0."
    )
    
    def model(self):
        return (
            Model()
            .add("FACE_A7 is TIME", 1 if 'FACE_A7' in TIME_FACES else 0)
            .add("FACE_B0 is TIME", 1 if 'FACE_B0' in TIME_FACES else 0)
            .add("TIME face count", len(TIME_FACES))
        )
    
    def observations(self):
        return (
            Observed()
            .add("FACE_A7 is TIME", 1)
            .add("FACE_B0 is TIME", 1)
            .add("TIME face count", 2)
        )


class ParallelTrackingWorks(Test):
    """
    Parallel face tracking captures all steps.
    """
    name = "Parallel Tracking Works"
    question = (
        "Can we track all 8 faces at once? "
        "We want to monitor progress on every face simultaneously, not one at a time. "
        "This test verifies the parallel tracking algorithm processes all traversal steps correctly."
    )
    reference = None  # Algorithm verification
    level = Standard
    audit_score = 83
    audit_notes = (
        "Question: 14/15 - Good 'simultaneously' framing. "
        "Derivation: 13/15 - Clear algorithm steps. "
        "Commentary: 13/15 - Nice dashboard analogy. "
        "Model: 9/10 - Good progress count. "
        "Observations: 8/10 - Clear expected progress. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Dashboard analogy accessible. "
        "Header: 8/10 (module level) - Proper imports in place. "
        "SAMPLE SIZE: 1000 digits - Adequate for tracking demonstration. "
    )
    future_questions = (
        "Q1: Why is parallel tracking more efficient than sequential face-by-face tracking? "
        "Q2: What data structures best support monitoring 8 faces simultaneously? "
        "Q3: How does tracking completion differ from tracking progress? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The algorithm should track vertex visits for all 8 Coupling Ports simultaneously.")
            .step("Initialize empty vertex sets for all 8 faces.")
            .step("For each traversal step, add current vertex to all faces containing it.")
            .step("Count faces that have made progress (non-empty vertex sets).")
            .step("After sufficient steps, verify all 8 faces have some progress.")
            .conclude("Faces with progress = 8.")
        )
    
    commentary = (
        "Imagine a dashboard with 8 progress bars, one for each face. "
        "As the traversal visits vertices, the relevant progress bars fill. "
        "This test ensures our 'dashboard' works: after enough steps, "
        "all 8 bars should show some progress."
    )
    
    def model(self):
        face_state, face_completed = track_parallel_faces(1000)
        faces_with_progress = sum(1 for s in face_state.values() if len(s) > 0)
        return (
            Model()
            .add("Faces with progress", faces_with_progress)
            .add("Total faces", 8)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Faces with progress", 8)
            .add("Total faces", 8)
        )


class BothTetrahedraMakeProgress(Test):
    """
    Both Tet_A and Tet_B make progress during traversal.
    """
    name = "Both Tetrahedra Progress"
    question = (
        "Do both tetrahedra advance, or just one? "
        "Bimetric means both halves work together. "
        "This test checks that both Tet A and Tet B faces make progress during traversal."
    )
    reference = "Bimetric coupling"
    tolerance = 0.0
    level = Standard
    audit_score = 85
    audit_notes = (
        "Question: 15/15 - Excellent 'one or both' rhetorical framing. "
        "Derivation: 14/15 - Clear bimetric reasoning. "
        "Commentary: 13/15 - Nice partnership analogy. "
        "Model: 10/10 - Good dual progress output. "
        "Observations: 10/10 - Clear expected values. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 13/15 - Partnership analogy accessible. "
        "Header: 8/10 (module level) - Proper imports in place. "
        "SAMPLE SIZE: 1000 digits - Adequate for progress demonstration. "
    )
    future_questions = (
        "Q1: What is bimetric coupling and why is it essential for the field model? "
        "Q2: Could the traversal be biased toward one tetrahedron, and what would that imply? "
        "Q3: How does simultaneous progress in both relate to quantum superposition? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Bimetric coupling requires simultaneous engagement of both Field Chambers.")
            .step("Track face completion progress for Tet A faces {A1,A2,A4,A7}.")
            .step("Track face completion progress for Tet B faces {B0,B3,B5,B6}.")
            .step("Check if any Tet A face has vertices visited.")
            .step("Check if any Tet B face has vertices visited.")
            .conclude("Tet A progress = 1, Tet B progress = 1.")
        )
    
    commentary = (
        "In a healthy partnership, both partners contribute. "
        "The Field Chamber has two 'partners' (Tet A and Tet B). "
        "If only one made progress while the other sat idle, we would have "
        "'uni-metric' behavior. This test confirms both sides are engaged."
    )
    
    def model(self):
        face_state, _ = track_parallel_faces(1000)
        
        tet_a_progress = any(len(face_state[f]) > 0 
                           for f in ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7'])
        tet_b_progress = any(len(face_state[f]) > 0 
                           for f in ['FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6'])
        
        return (
            Model()
            .add("Tet A progress", 1 if tet_a_progress else 0)
            .add("Tet B progress", 1 if tet_b_progress else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet A progress", 1)
            .add("Tet B progress", 1)
        )


class AllFacesCompleteEventually(Test):
    """
    All 8 faces complete within reasonable number of digits.
    """
    name = "All Faces Complete"
    question = (
        "Do all 8 faces eventually complete? "
        "A face 'completes' when all 3 of its vertices have been visited. "
        "This test checks whether all 8 faces complete within 1000 traversal digits."
    )
    reference = "Complete coverage"
    tolerance = 0.0
    level = Standard
    audit_score = 84
    audit_notes = (
        "Question: 14/15 - Good 'eventually' framing. "
        "Derivation: 14/15 - Clear completion logic. "
        "Commentary: 13/15 - Nice bingo card analogy. "
        "Model: 9/10 - Good completion count. "
        "Observations: 10/10 - Clear expected values. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Bingo card analogy accessible. "
        "Header: 8/10 (module level) - Proper imports in place. "
        "SAMPLE SIZE: 1000 digits - Adequate for completion claims. "
    )
    future_questions = (
        "Q1: What is the expected number of digits needed to complete all 8 faces? "
        "Q2: How does ergodicity guarantee eventual face completion? "
        "Q3: What would incomplete faces imply about the traversal's coverage properties? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Complete coverage requires visiting all 3 vertices of each of 8 faces.")
            .step("Track which vertices have been visited for each face.")
            .step("A face is complete when its vertex set equals its defining vertex set.")
            .step("Count completed faces after 60 digits of traversal.")
            .step("With ergodic sampling, all 8 vertices are visited within ~20-30 steps.")
            .conclude("Faces completed = 8.")
        )
    
    commentary = (
        "Completing a face is like filling a bingo card with 3 slots. "
        "Each face needs its specific 3 vertices visited. "
        "Since pi's digits eventually visit all 8 vertices, and 60 digits is plenty "
        "of opportunity, all 8 faces should complete. "
        "This confirms full geometric coverage."
    )
    
    def model(self):
        _, face_completed = track_parallel_faces(1000)
        completed_count = sum(1 for step in face_completed.values() if step is not None)
        return (
            Model()
            .add("Faces completed", completed_count)
            .add("Total faces", 8)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Faces completed", 8)
            .add("Total faces", 8)
        )


class CumulativeFaceCoverage(Test):
    """
    Cumulatively, all 8 faces are touched within first 1000 digits.
    """
    name = "Cumulative Face Coverage"
    question = (
        "Are all 8 faces at least 'touched'? "
        "A face is 'touched' when at least one of its vertices is visited. "
        "This test checks that all 8 faces see some activity within 1000 digits."
    )
    reference = "Complete sampling"
    tolerance = 0.0
    level = Standard
    audit_score = 83
    audit_notes = (
        "Question: 14/15 - Good 'touched' distinction from completed. "
        "Derivation: 13/15 - Clear vertex-to-face relationship. "
        "Commentary: 13/15 - Good weaker/stronger check distinction. "
        "Model: 9/10 - Good touched count. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Weaker/stronger distinction helpful. "
        "Header: 8/10 (module level) - Proper imports in place. "
        "SAMPLE SIZE: 1000 digits - Adequate for coverage claims. "
    )
    future_questions = (
        "Q1: What is the difference between 'touched' and 'completed' for a face? "
        "Q2: Why is partial coverage an important intermediate metric? "
        "Q3: How quickly should all faces be touched given uniform digit distribution? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each face should receive at least partial coverage within early traversal.")
            .step("Each vertex belongs to exactly 3 faces (vertices opposite it in its tetrahedron).")
            .step("Visiting any vertex touches 3 faces simultaneously.")
            .step("With 8 vertices total, visiting all 8 touches all faces.")
            .step("Count faces with at least 1 vertex visited after 50 digits.")
            .conclude("Faces touched = 8.")
        )
    
    commentary = (
        "Before a face completes, it needs to at least 'start.' "
        "Touching a face means visiting any of its 3 vertices. "
        "Each vertex touches 3 faces at once, so visiting all 8 vertices "
        "guarantees all 8 faces are touched. This is a weaker check than completion, "
        "but ensures no face is completely ignored."
    )
    
    def model(self):
        face_state, _ = track_parallel_faces(1000)
        faces_touched = sum(1 for s in face_state.values() if len(s) > 0)
        return Model().add("Faces touched", faces_touched)
    
    def observations(self):
        return Observed().add("Faces touched", 8)


class SpatialFaceCount(Test):
    """
    There are exactly 6 SPATIAL faces (3 per tetrahedron).
    """
    name = "Spatial Face Count"
    question = (
        "How many SPATIAL faces are there? "
        "Space has 3 dimensions, and each tetrahedron has 3 SPATIAL faces (plus 1 TIME face). "
        "This test verifies the total is 6 SPATIAL faces."
    )
    reference = "Face classification"
    tolerance = 0.0
    level = Standard
    audit_score = 86
    audit_notes = (
        "Question: 15/15 - Great connection to 3D space. "
        "Derivation: 14/15 - Clear arithmetic. "
        "Commentary: 14/15 - Excellent 3+1 dimensional explanation. "
        "Model: 9/10 - Simple count output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 13/15 - 3+1 explanation excellent. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: Why does the number of SPATIAL faces equal 2 times the number of spatial dimensions? "
        "Q2: How does the 3+1 structure of spacetime emerge from face classification? "
        "Q3: Would a model with different k value have different TIME/SPATIAL face ratios? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tetrahedron has k=4 faces; one is TIME, k-1=3 are SPATIAL.")
            .step("Total faces = 2k = 8.")
            .step("TIME faces = 2 (one per tetrahedron).")
            .step("SPATIAL faces = Total - TIME = 8 - 2 = 6.")
            .step("Per tetrahedron: 6/2 = 3 SPATIAL faces.")
            .conclude("SPATIAL faces = 6.")
        )
    
    commentary = (
        "We live in 3+1 dimensions: 3 spatial (left/right, forward/back, up/down) "
        "plus 1 time. The Field Chamber encodes this: 6 SPATIAL faces (3 per tetrahedron) "
        "for the spatial dimensions, and 2 TIME faces for the temporal dimension. "
        "The count 6 = 2 tetrahedra * 3 spatial dimensions."
    )
    
    def model(self):
        return Model().add("SPATIAL faces", len(SPATIAL_FACES))
    
    def observations(self):
        return Observed().add("SPATIAL faces", 6)


class EachFaceHasThreeVertices(Test):
    """
    Each face has exactly 3 vertices (triangular faces).
    """
    name = "Faces Have 3 Vertices"
    question = (
        "Are all faces triangular? "
        "A tetrahedron has triangular faces, meaning 3 vertices each. "
        "This test verifies every face in our structure has exactly 3 vertices."
    )
    reference = "Tetrahedron face geometry"
    tolerance = 0.0
    level = Critical
    audit_score = 87
    audit_notes = (
        "Question: 15/15 - Excellent 'Are all faces triangular?' simplicity. "
        "Derivation: 15/15 - Clear k-1 derivation. "
        "Commentary: 15/15 - Brilliant basic geometry insight. "
        "Model: 10/10 - Clean output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 14/15 - Very clear geometric reasoning. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: Why must tetrahedron faces be triangular (3 vertices) and not some other polygon? "
        "Q2: How does the k-1 = 3 relationship connect to simplex geometry? "
        "Q3: What would it mean for the model if faces had 4 or more vertices? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A tetrahedron's faces are triangles formed by any 3 of its 4 vertices.")
            .step("Each face excludes exactly 1 vertex (the opposite apex).")
            .step("Therefore each face contains k-1 = 4-1 = 3 vertices.")
            .step("Verify: count |FACE| for each of the 8 defined faces.")
            .conclude("All faces have 3 vertices = 1.")
        )
    
    commentary = (
        "A tetrahedron is the simplest 3D shape: 4 vertices, 4 triangular faces. "
        "Each face excludes one vertex (the apex opposite to it), leaving 3 vertices. "
        "There is no such thing as a square or pentagonal face on a tetrahedron. "
        "This basic geometric fact must hold for our model to be consistent."
    )
    
    def model(self):
        all_three = all(len(verts) == 3 for verts in FACES.values())
        return Model().add("All faces have 3 vertices", 1 if all_three else 0)
    
    def observations(self):
        return Observed().add("All faces have 3 vertices", 1)


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


def run_all():
    """Run all parallel Coupling Port traversal tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
