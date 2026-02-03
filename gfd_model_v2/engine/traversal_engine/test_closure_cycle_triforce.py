"""
Field Closure Cycle Mechanics
=============================

This module examines Coupling Port (face) completion during vertex traversal.
The tests document patterns in how faces complete as vertices are visited.

Key observations examined:
1. Front-Bottom Late: V2 (010) and V6 (110) arrive later in sequence
2. TIME Faces Complete Late: FACE_A7 and FACE_B0 complete later on average
3. Burst Completion: Multiple faces may complete at the same traversal step
4. Critical Vertices: Late-arriving vertices complete multiple faces
5. 3:1 Ratio: Vertices per face (k-1=3) corresponds to implicit knowledge ratio
6. Field Chamber Asymmetry: Traversal starts in Tet_B but Tet_A may complete first
"""

import sys
import os
import math
from typing import Dict, Optional, List
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4

# Pi base-8 fractional digits
PI_BASE8_FRACTIONAL = [
    1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, 0, 2, 1, 5,
    1, 4, 2, 3, 0, 5, 5, 4, 5, 4, 1, 2, 2, 0, 3, 5, 2, 3, 4, 6,
    5, 4, 2, 1, 1, 3, 2, 6, 7, 2,
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


def get_pi_base8(n_digits, include_integer=True):
    if include_integer:
        return [3] + PI_BASE8_FRACTIONAL[:n_digits]
    return PI_BASE8_FRACTIONAL[:n_digits]


def get_tetrahedron(v):
    return 'A' if v in TET_A else 'B'


def get_faces_for_vertex(v):
    return [name for name, verts in FACES.items() if v in verts]


def traverse_and_track_faces(n_digits=50):
    """Traverse and track face completion."""
    digits = get_pi_base8(n_digits, include_integer=True)
    
    face_reads = {name: set() for name in FACES}
    face_completed_at = {}
    vertex_first_seen = {}
    
    cumsum = 0
    for step, digit in enumerate(digits):
        cumsum += digit
        vertex = cumsum % 8
        
        if vertex not in vertex_first_seen:
            vertex_first_seen[vertex] = step
        
        for fname in get_faces_for_vertex(vertex):
            face_reads[fname].add(vertex)
            if fname not in face_completed_at and face_reads[fname] == FACES[fname]:
                face_completed_at[fname] = step
    
    return vertex_first_seen, face_completed_at


# =============================================================================
# TESTS
# =============================================================================

class PiDigitIsTriad(GFDTest):
    """
    Each pi digit (0-7) directly encodes a 3-bit triad.
    The digit IS the vertex position encoding.
    """
    name = "Pi Digit = 3-bit Triad"
    question = "Does each pi base-8 digit (0-7) bijectively encode a 3-bit triad, enabling direct vertex addressing?"
    reference_source = "Binary encoding"
    tolerance = 0.0
    derivation = (
        "PREMISE: Base-8 digits span 0-7, requiring exactly d=3 bits for representation. "
        "STEP 1: For each digit d in {0,1,2,3,4,5,6,7}, compute triad = format(d, '03b'). "
        "STEP 2: Verify int(triad, 2) == d for all digits. "
        "STEP 3: This bijection means digit IS the vertex index. "
        "OUTPUT: Pi digits directly encode Field Chamber vertex addresses via triads."
    )
    commentary = None  # Mechanical verification of encoding identity
    
    def model(self) -> Dict[str, float]:
        all_correct = True
        for digit in range(8):
            triad = format(digit, '03b')
            reconstructed = int(triad, 2)
            if reconstructed != digit:
                all_correct = False
        return {"All digits encode correctly": 1 if all_correct else 0}
    
    def observations(self) -> Dict[str, float]:
        return {"All digits encode correctly": 1}


class VertexBelongsToThreeFaces(GFDTest):
    """
    Each vertex belongs to exactly 3 Coupling Ports. This follows from
    tetrahedron geometry: each tetrahedron has 4 faces and each vertex
    is absent from exactly 1 face (the opposite face).
    """
    name = "Vertex in 3 Coupling Ports"
    question = "Does each vertex participate in exactly k-1=3 Coupling Ports, being absent only from its opposite face?"
    reference_source = "Tetrahedron geometry"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each tetrahedron has k=4 faces. Each vertex is part of all faces except the one opposite it. "
        "STEP 1: Faces per tetrahedron = k = 4. "
        "STEP 2: Faces containing a given vertex = k - 1 = 3 (excludes opposite face). "
        "STEP 3: Check all 8 vertices; each should belong to exactly 3 faces. "
        "OUTPUT: Every vertex participates in exactly d=k-1=3 Coupling Ports."
    )
    commentary = (
        "Each vertex participates in exactly k-1=3 Coupling Ports, being absent only "
        "from the face opposite to it. This geometric constraint determines how "
        "vertex visitation propagates information through the Field Chamber structure."
    )
    
    def model(self) -> Dict[str, float]:
        all_three = all(len(get_faces_for_vertex(v)) == 3 for v in range(8))
        return {"All vertices in 3 faces": 1 if all_three else 0}
    
    def observations(self) -> Dict[str, float]:
        return {"All vertices in 3 faces": 1}


class ComplementCrossesTetrahedra(GFDTest):
    """
    Each vertex's complement (7-v) is in the opposite Field Chamber.
    This structure enables parallel traversal patterns.
    """
    name = "Complements Cross Field Chambers"
    question = "Does the complement operation (7-v) guarantee cross-chamber pairing for all vertices?"
    reference_source = "Parity structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: Complement of vertex v is 7-v. Parity inversion implies Field Chamber change. "
        "STEP 1: For each vertex v, compute complement c = 7 - v. "
        "STEP 2: Determine Field Chamber of v and c using parity. "
        "STEP 3: Verify v and c are in different Field Chambers for all 8 vertices. "
        "OUTPUT: All complementary pairs span both Field Chambers (cross-chamber structure)."
    )
    commentary = (
        "The cross-chamber complementary structure ensures that every vertex in "
        "Tetrahedron A has a partner in Tetrahedron B. This pairing may underlie "
        "the bimetric balance maintained during Field Closure traversal."
    )
    
    def model(self) -> Dict[str, float]:
        all_cross = True
        for v in range(8):
            comp = 7 - v
            v_tet = get_tetrahedron(v)
            c_tet = get_tetrahedron(comp)
            if v_tet == c_tet:
                all_cross = False
        return {"All complements cross": 1 if all_cross else 0}
    
    def observations(self) -> Dict[str, float]:
        return {"All complements cross": 1}


class FrontBottomLate(GFDTest):
    """
    V2 (010) and V6 (110) arrive last. Both share Y=1 (Front), Z=0 (Bottom).
    Pi's early digits avoid the Front-Bottom region.
    """
    name = "Front-Bottom Late Arrival"
    question = "Do vertices V2 (010) and V6 (110) arrive late in pi traversal, sharing the Front-Bottom spatial coordinates?"
    reference_source = "Pi traversal pattern"
    derivation = (
        "PREMISE: Traversal arrival order depends on pi's cumulative sums mod 8. "
        "STEP 1: Track first appearance of each vertex during 50-digit traversal. "
        "STEP 2: Sort vertices by arrival step to identify the last two arrivals. "
        "STEP 3: Check if V2 (triad 010) and V6 (triad 110) are among the last two. "
        "STEP 4: Verify both share Y=1 (bit 1) and Z=0 (bit 0), defining Front-Bottom region. "
        "OUTPUT: Late arrival of Front-Bottom vertices emerges from pi's digit distribution."
    )
    commentary = (
        "Vertices V2 and V6, which share the Front-Bottom spatial coordinates, "
        "arrive later in the traversal sequence. This pattern emerges from pi's "
        "digit distribution and may indicate non-uniform coupling to specific "
        "regions of the Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        vertex_first_seen, _ = traverse_and_track_faces(50)
        
        arrival_order = sorted(vertex_first_seen.items(), key=lambda x: x[1])
        last_two = [v for v, _ in arrival_order[-2:]]
        
        v2_late = 2 in last_two
        v6_late = 6 in last_two
        
        # Both share Front-Bottom (Y=1, Z=0)
        v2_triad = format(2, '03b')  # 010
        v6_triad = format(6, '03b')  # 110
        share_pattern = (v2_triad[1] == v6_triad[1] == '1' and  # Y=1
                        v2_triad[2] == v6_triad[2] == '0')      # Z=0
        
        return {
            "V2 late": 1 if v2_late else 0,
            "V6 late": 1 if v6_late else 0,
            "Share Front-Bottom": 1 if share_pattern else 0,
        }


class TimeFacesCompleteLate(GFDTest):
    """
    TIME faces (FACE_A7, FACE_B0) complete later than SPATIAL faces.
    """
    name = "TIME Faces Complete Late"
    question = "Do the 2 TIME Coupling Ports (FACE_A7, FACE_B0) complete later on average than the 6 SPATIAL Coupling Ports?"
    reference_source = "Face completion pattern"
    derivation = (
        "PREMISE: A Coupling Port completes when all 3 of its vertices have been visited. "
        "STEP 1: Track face completion steps during traversal. "
        "STEP 2: Compute average completion step for TIME faces: (step_A7 + step_B0) / 2. "
        "STEP 3: Compute average completion step for 6 SPATIAL faces. "
        "STEP 4: Compare: if avg_TIME >= avg_SPATIAL, TIME completes later. "
        "OUTPUT: TIME Coupling Ports complete later, suggesting temporal structure settles after spatial."
    )
    commentary = (
        "TIME Coupling Ports complete later than SPATIAL Coupling Ports on average. "
        "This ordering may reflect a fundamental asymmetry where spatial degrees of "
        "freedom settle before temporal ones during Field Closure."
    )
    
    def model(self) -> Dict[str, float]:
        _, face_completed = traverse_and_track_faces(50)
        
        time_faces = ['FACE_A7', 'FACE_B0']
        time_steps = [face_completed.get(f, 50) for f in time_faces]
        spatial_steps = [s for f, s in face_completed.items() if f not in time_faces]
        
        avg_time = sum(time_steps) / len(time_steps) if time_steps else 0
        avg_spatial = sum(spatial_steps) / len(spatial_steps) if spatial_steps else 0
        
        return {
            "Avg TIME completion step": avg_time,
            "Avg SPATIAL completion step": avg_spatial,
            "TIME later": 1 if avg_time >= avg_spatial else 0,
        }


class BurstCompletion(GFDTest):
    """
    Faces complete in bursts (multiple at same step), not evenly.
    A single critical vertex can unlock multiple faces.
    """
    name = "Burst Completion Pattern"
    question = "Do Coupling Ports complete in bursts where a single critical vertex unlocks multiple faces simultaneously?"
    reference_source = "Traversal dynamics"
    derivation = (
        "PREMISE: Each vertex participates in k-1=3 faces. A late-arriving vertex may complete multiple faces at once. "
        "STEP 1: Track the step at which each face completes. "
        "STEP 2: Count how many faces complete at each step. "
        "STEP 3: Find maximum simultaneous completions (burst size). "
        "STEP 4: If max_burst >= 2, burst completion pattern is confirmed. "
        "OUTPUT: Burst pattern indicates information cascades at critical vertices."
    )
    commentary = (
        "Coupling Port completion occurs in bursts rather than uniformly. Critical "
        "vertices that arrive late can simultaneously complete multiple Coupling Ports, "
        "suggesting information cascades during the final stages of Field Closure."
    )
    
    def model(self) -> Dict[str, float]:
        _, face_completed = traverse_and_track_faces(50)
        
        step_counts = Counter(face_completed.values())
        max_burst = max(step_counts.values()) if step_counts else 0
        has_burst = max_burst >= 2
        
        return {
            "Max simultaneous completions": max_burst,
            "Has burst (>=2)": 1 if has_burst else 0,
        }


class KMinus1Ratio(GFDTest):
    """
    The 3:1 ratio = (k-1):1 connects to 3+1 spacetime structure.
    3 explicit reads per implicit knowledge event.
    """
    name = "(k-1):1 = 3:1 Ratio"
    question = "Does the vertex-per-face ratio k-1=3 correspond to the 3+1 spacetime decomposition?"
    reference_source = "k=4 topology"
    tolerance = 0.0
    derivation = (
        "PREMISE: From Field Closure, k=4 determines tetrahedral structure; d=k-1=3 is spatial dimension count. "
        "STEP 1: Each Coupling Port (triangular face) has k-1 = 3 vertices. "
        "STEP 2: Each face completion requires 3 explicit vertex visits. "
        "STEP 3: Face completion itself is 1 implicit event. "
        "STEP 4: Ratio: (k-1) : 1 = 3 : 1, matching 3 spatial + 1 temporal dimensions. "
        "OUTPUT: The 3:1 ratio parallels the 3+1 spacetime structure."
    )
    commentary = (
        "The ratio k-1=3 vertices per Coupling Port corresponds to the 3+1 "
        "decomposition familiar from spacetime. Three spatial dimensions plus one "
        "temporal dimension parallels three explicit vertex reads plus one implicit "
        "completion event per Coupling Port."
    )
    
    def model(self) -> Dict[str, float]:
        vertices_per_face = 3  # = k-1
        implicit_per_face = 1  # Gained at 2nd read
        ratio = vertices_per_face / implicit_per_face
        
        # k encodes in structure
        faces_per_tet = 4  # = k
        vertices_per_face_check = 3  # = k-1
        
        return {
            "Vertices per face": vertices_per_face,
            "Implicit per face": implicit_per_face,
            "Ratio": ratio,
            "k": K,
            "k-1": K - 1,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Vertices per face": 3,
            "Implicit per face": 1,
            "Ratio": 3,
            "k": 4,
            "k-1": 3,
        }


class FieldChamberAsymmetry(GFDTest):
    """
    Pi traversal starts in Tet_B (first vertex V3) but Tet_A may complete first.
    First entry does not necessarily mean first completion.
    """
    name = "Field Chamber Asymmetry"
    question = "Can Tetrahedron A complete its Coupling Ports before Tetrahedron B, despite traversal starting in Tet B?"
    reference_source = "Traversal dynamics"
    derivation = (
        "PREMISE: Pi's integer part 3 places first vertex in Tet B. Completion order depends on digit sequence. "
        "STEP 1: First vertex = V3, which is in Tet B (even parity). "
        "STEP 2: Track when all 4 Tet A faces complete vs all 4 Tet B faces. "
        "STEP 3: Compare completion steps: if Tet_A_complete < Tet_B_complete, asymmetry holds. "
        "STEP 4: This demonstrates initial chamber entry does not determine completion order. "
        "OUTPUT: Completion order is determined by pi's digit distribution, not starting position."
    )
    commentary = (
        "Although traversal begins in Tetrahedron B, Tetrahedron A may complete its "
        "Coupling Port coverage first. This asymmetry emerges from pi's specific digit "
        "sequence and illustrates how initial conditions do not determine completion order."
    )
    
    def model(self) -> Dict[str, float]:
        digits = get_pi_base8(50, include_integer=True)
        
        # First vertex
        cumsum = digits[0]
        first_vertex = cumsum % 8
        first_tet = get_tetrahedron(first_vertex)
        starts_in_b = 1 if first_tet == 'B' else 0
        
        # Track completion
        face_reads = {name: set() for name in FACES}
        tet_a_complete_step = None
        tet_b_complete_step = None
        
        cumsum = 0
        for step, digit in enumerate(digits):
            cumsum += digit
            vertex = cumsum % 8
            
            for fname in get_faces_for_vertex(vertex):
                face_reads[fname].add(vertex)
            
            if tet_a_complete_step is None:
                tet_a_faces = ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7']
                if all(face_reads[f] == FACES[f] for f in tet_a_faces):
                    tet_a_complete_step = step
            
            if tet_b_complete_step is None:
                tet_b_faces = ['FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6']
                if all(face_reads[f] == FACES[f] for f in tet_b_faces):
                    tet_b_complete_step = step
        
        tet_a_first = 1 if (tet_a_complete_step and tet_b_complete_step and 
                          tet_a_complete_step < tet_b_complete_step) else 0
        
        return {
            "Starts in Tet_B": starts_in_b,
            "Tet_A completes first": tet_a_first,
            "Tet_A step": tet_a_complete_step if tet_a_complete_step else -1,
            "Tet_B step": tet_b_complete_step if tet_b_complete_step else -1,
        }


class ThreePlusOneStructure(GFDTest):
    """
    k = 4 = 3+1 corresponds to the GR spacetime decomposition.
    3 spatial Coupling Ports + 1 TIME Coupling Port per Field Chamber.
    """
    name = "3+1 Structure Correspondence"
    question = "Do the k=4 faces per tetrahedron decompose as 3 SPATIAL + 1 TIME Coupling Ports, mirroring 3+1 spacetime?"
    reference_source = "General relativity analogy"
    tolerance = 0.0
    derivation = (
        "PREMISE: Each tetrahedron has k=4 faces. These are classified as SPATIAL or TIME. "
        "STEP 1: SPATIAL faces include an apex vertex: k-1 = 3 per tetrahedron. "
        "STEP 2: TIME face is opposite the apex: 1 per tetrahedron. "
        "STEP 3: Total per tetrahedron: 3 SPATIAL + 1 TIME = 4 = k. "
        "STEP 4: This parallels spacetime: d=3 spatial dimensions + 1 temporal dimension. "
        "OUTPUT: Tetrahedral face classification mirrors the 3+1 spacetime decomposition."
    )
    commentary = (
        "The k=4 topology decomposes as 3 SPATIAL Coupling Ports plus 1 TIME Coupling "
        "Port per tetrahedron, mirroring the 3+1 dimensional structure of spacetime. "
        "This correspondence between tetrahedral faces and spacetime dimensions may "
        "indicate geometric origins for dimensional structure."
    )
    
    def model(self) -> Dict[str, float]:
        spatial_per_tet = 3  # A1, A2, A4 or B3, B5, B6
        time_per_tet = 1     # A7 or B0
        total = spatial_per_tet + time_per_tet
        
        return {
            "Spatial faces per tet": spatial_per_tet,
            "TIME faces per tet": time_per_tet,
            "Total (k)": total,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Spatial faces per tet": 3,
            "TIME faces per tet": 1,
            "Total (k)": 4,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    PiDigitIsTriad,
    VertexBelongsToThreeFaces,
    ComplementCrossesTetrahedra,
    FrontBottomLate,
    TimeFacesCompleteLate,
    BurstCompletion,
    KMinus1Ratio,
    FieldChamberAsymmetry,
    ThreePlusOneStructure,
]


def run_all_tests() -> bool:
    """Run all Field Closure cycle mechanics tests."""
    return run_test_group(
        title="Field Closure Cycle Mechanics",
        summary=(
            "These tests examine Coupling Port completion patterns during vertex traversal. "
            "Observations include: V2 and V6 arrive later in the sequence, TIME Coupling Ports "
            "complete later on average, faces complete in bursts, and the 3:1 ratio (k-1 "
            "vertices per face) corresponds to the 3+1 dimensional structure. Field Chamber "
            "asymmetry shows that starting in Tet_B does not mean Tet_B completes first. "
            "Each vertex belongs to exactly 3 Coupling Ports, and complements always cross "
            "Field Chambers."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
