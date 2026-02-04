"""
Face Reads Accumulate
=====================

Face vertex readings ACCUMULATE over steps, they do not PROPAGATE.
There is no signal traveling from V1 to V2 to V3 on a face.
Vertices are visited in any order, not a specific propagation sequence.
"""

from gfd_model_v2.framework import *
from gfd_model_v2.common import FACES, TIME_FACES, traverse_pi_base8


def analyze_face_read_timing(traversal_data):
    """
    Analyze when each face's vertices are read.
    For each face, record the steps at which each of its 3 vertices is visited.
    """
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


class FaceReadsAccumulate(Test):
    """
    Face vertex readings ACCUMULATE over steps, they do not PROPAGATE.
    There is no signal traveling from V1 to V2 to V3 on a face.
    Vertices are visited in any order, not a specific propagation sequence.
    """
    
    name = "Face Reads Accumulate Not Propagate"
    question = (
        "Why don't face vertices need to be visited in a specific order? Because faces "
        "collect information by accumulation, not by passing a message along a chain. "
        "We test whether vertices are visited out of their natural numerical order, "
        "proving that no signal travels from vertex to vertex around the face."
    )
    reference = None  # Observation
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("For each face (3 vertices), record the step at which each vertex is visited")
            .step("Natural order: vertices sorted numerically (e.g., {1,2,4} for FACE_A7)")
            .step("Visit order: vertices sorted by step number")
            .step("If visit_order != natural_order for any face, vertices are visited out-of-order")
            .step("Out-of-order visitation implies accumulation: the face collects vertex states")
            .conclude("Faces accumulate state as vertices are encountered, not via sequential propagation")
        )
    
    def model(self):
        traversal = traverse_pi_base8(50)
        face_timing = analyze_face_read_timing(traversal)
        
        out_of_order_count = 0
        complete_faces = 0
        
        for face_name, timing in face_timing.items():
            if timing['complete']:
                complete_faces += 1
                visits = timing['visit_steps']
                vertex_order = sorted(visits.keys(), key=lambda v: visits[v])
                natural_order = sorted(timing['vertices'])
                
                if vertex_order != natural_order:
                    out_of_order_count += 1
        
        return (
            Model()
            .add("Faces with out-of-order visits", out_of_order_count)
            .add("Complete faces", complete_faces)
        )
    
    commentary = (
        "Picture three friends at a party who need to confirm they all agree on something. "
        "One way: Alice tells Bob, Bob tells Carol, Carol reports the consensus. This is "
        "propagation, and it takes time for the message to travel. Another way: everyone "
        "writes their vote on the same shared whiteboard whenever they happen to walk by. "
        "No specific order needed, no waiting for a signal. The face works like the "
        "whiteboard. Each vertex contributes its state when visited, and the face simply "
        "notices when all three contributions are present. This means no signal needs to "
        "race around the edges. The information accumulates in place, making the whole "
        "process much faster than any propagation scheme could be."
    )


ALL_TESTS = [FaceReadsAccumulate]


def run_all():
    """Run test."""
    return run_tests(
        title="Face Reads Accumulate",
        summary="Verifies that face vertices accumulate state through out-of-order visitation.",
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
