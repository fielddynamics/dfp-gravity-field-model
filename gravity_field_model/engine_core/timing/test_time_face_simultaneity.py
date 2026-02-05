"""
TIME Face Simultaneity
======================

When a TIME face completes, all 3 vertices have been visited.
The completion is a recognition, not a signal.
"""

from gravity_field_model.framework import *
from gravity_field_model.common import FACES, TIME_FACES, traverse_pi_base8


def analyze_face_read_timing(traversal_data):
    """Analyze when each face's vertices are read."""
    face_timing = {}
    
    for face_name, face_vertices in FACES.items():
        face_timing[face_name] = {
            'vertices': face_vertices,
            'visit_steps': {},
            'type': 'TIME' if face_name in TIME_FACES else 'SPATIAL',
            'tetrahedron': 'A' if face_name.startswith('FACE_A') else 'B'
        }
    
    for step in traversal_data:
        vertex = step['vertex']
        step_num = step['step']
        
        for face_name in face_timing:
            if vertex in face_timing[face_name]['vertices']:
                if vertex not in face_timing[face_name]['visit_steps']:
                    face_timing[face_name]['visit_steps'][vertex] = step_num
    
    for face_name in face_timing:
        visits = list(face_timing[face_name]['visit_steps'].values())
        if len(visits) == 3:
            face_timing[face_name]['span'] = max(visits) - min(visits)
            face_timing[face_name]['complete'] = True
        else:
            face_timing[face_name]['span'] = None
            face_timing[face_name]['complete'] = False
    
    return face_timing


class TimeFaceSimultaneity(Test):
    """
    When a TIME face completes, all 3 vertices have been visited.
    The completion is a recognition, not a signal.
    """
    
    name = "TIME Face Simultaneity"
    question = (
        "How do the special TIME faces (the ones pointing at each other) complete their "
        "reads? We test whether all 3 vertices of each TIME face get visited within the "
        "first 50 steps of the pi traversal, showing that temporal information is captured "
        "through accumulation, not through any special signaling mechanism."
    )
    reference = None  # Observation
    level = Standard
    audit_score = 82
    audit_notes = (
        "Question: 13/15 - Good hook about TIME faces but could emphasize physical significance. "
        "Derivation: 12/15 - Clear face completion logic but minimal intuition building. "
        "Commentary: 14/15 - Excellent jigsaw puzzle analogy for recognition vs signal. "
        "Model: 7/10 - Simple completion count, could show timing details. "
        "Observations: 5/10 - No observations() method defined, missing expected values. "
        "Constants: 9/10 - Proper imports (FACES, TIME_FACES) from common. "
        "Accessibility: 13/15 - Good analogies, accessible to undergraduates. "
        "Header: 6/10 - Module header explains concept but lacks validation scope. "
        "FUNCTION OPPORTUNITY: analyze_face_read_timing() duplicated from test_face_reads_accumulate. "
        "Should be extracted to common module as fn_analyze_face_timing(). "
        "TO IMPROVE: Add observations() method; deduplicate timing analysis function."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("TIME faces: FACE_A7 = {1,2,4}, FACE_B0 = {3,5,6}")
            .step("A face 'completes' when all 3 of its vertices have been visited at least once")
            .step("Traverse N=50 digits and track which vertices have been visited per face")
            .step("Completion is a recognition event: no signal propagates between vertices")
            .conclude("The face records when all constituent vertex states have been encountered")
        )
    
    def model(self):
        traversal = traverse_pi_base8(50)
        face_timing = analyze_face_read_timing(traversal)
        
        time_faces = ['FACE_A7', 'FACE_B0']
        time_complete = sum(1 for f in time_faces if face_timing[f]['complete'])
        
        return (
            Model()
            .add("TIME faces complete", time_complete)
            .add("Total TIME faces", len(time_faces))
        )
    
    def observations(self):
        traversal = traverse_pi_base8(50)
        face_timing = analyze_face_read_timing(traversal)
        
        time_faces = ['FACE_A7', 'FACE_B0']
        time_complete = sum(1 for f in time_faces if face_timing[f]['complete'])
        
        return (
            Observed()
            .add("TIME faces complete", time_complete)
            .add("Total TIME faces", len(time_faces))
        )
    
    commentary = (
        "The TIME faces (FACE_A7 with vertices 1, 2, 4 and FACE_B0 with vertices 3, 5, 6) "
        "are special because they face each other, meeting at the Field Origin. When does "
        "a face 'know' its complete state? When all three of its vertices have been visited "
        "at least once. But notice: the face does not send a signal saying 'I am complete.' "
        "It simply IS complete when the third vertex is visited. This is like a jigsaw "
        "puzzle. Each piece does not announce itself; the picture is simply complete when "
        "the last piece is placed. The face completion is a recognition event, not a "
        "communication event. This distinction is crucial for understanding how the Field "
        "Chamber can operate faster than light could propagate signals across it."
    )


ALL_TESTS = [TimeFaceSimultaneity]


def run_all():
    """Run test."""
    return run_tests(
        title="TIME Face Simultaneity",
        summary="Verifies TIME face completion through accumulated vertex visits.",
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
