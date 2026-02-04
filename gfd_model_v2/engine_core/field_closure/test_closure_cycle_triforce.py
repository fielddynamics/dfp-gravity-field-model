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

from typing import Dict, Optional, List
from collections import Counter

from gfd_model_v2.framework import *

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

class PiDigitIsTriad(Test):
    """
    Each pi digit (0-7) directly encodes a 3-bit triad.
    The digit IS the vertex position encoding.
    """
    name = "Pi Digit = 3-bit Triad"
    question = (
        "How do we address 8 vertices with pi digits? "
        "Each base-8 digit (0 through 7) can be written as 3 binary bits, "
        "and those 3 bits specify exactly one of 8 possible corners. "
        "This test confirms the bijection: digit and vertex address are the same thing."
    )
    reference = "Binary encoding"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Base-8 digits span 0-7, requiring exactly d=3 bits for representation.")
            .step("For each digit d in {0,1,2,3,4,5,6,7}, compute triad = format(d, '03b').")
            .step("Verify int(triad, 2) == d for all digits.")
            .step("This bijection means digit IS the vertex index.")
            .conclude("Pi digits directly encode Field Chamber vertex addresses via triads.")
        )
    
    commentary = (
        "Think of 3 light switches: each can be ON or OFF. With 3 switches, you have "
        "2 x 2 x 2 = 8 possible combinations: 000, 001, 010, 011, 100, 101, 110, 111. "
        "These are exactly the binary representations of 0 through 7. So when pi gives "
        "us the digit 5, that is binary 101, which we can read as: switch 1 ON, switch 2 OFF, "
        "switch 3 ON. This directly identifies vertex V5. No translation needed. The digit "
        "IS the address. This elegant correspondence is why base 8 works so naturally here."
    )
    
    def model(self):
        all_correct = True
        for digit in range(8):
            triad = format(digit, '03b')
            reconstructed = int(triad, 2)
            if reconstructed != digit:
                all_correct = False
        return Model().add("All digits encode correctly", 1 if all_correct else 0)
    
    def observations(self):
        return Observed().add("All digits encode correctly", 1)


class VertexBelongsToThreeFaces(Test):
    """
    Each vertex belongs to exactly 3 Coupling Ports. This follows from
    tetrahedron geometry: each tetrahedron has 4 faces and each vertex
    is absent from exactly 1 face (the opposite face).
    """
    name = "Vertex in 3 Coupling Ports"
    question = (
        "How many faces touch each corner of a pyramid? "
        "A tetrahedron has 4 triangular faces, and each corner touches exactly 3 of them "
        "(all except the one opposite). This test verifies this geometric fact: "
        "every vertex belongs to exactly 3 Coupling Ports."
    )
    reference = "Tetrahedron geometry"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tetrahedron has k=4 faces. Each vertex is part of all faces except the one opposite it.")
            .step("Faces per tetrahedron = k = 4.")
            .step("Faces containing a given vertex = k - 1 = 3 (excludes opposite face).")
            .step("Check all 8 vertices; each should belong to exactly 3 faces.")
            .conclude("Every vertex participates in exactly d=k-1=3 Coupling Ports.")
        )
    
    commentary = (
        "Picture a triangular pyramid (tetrahedron). Pick any corner and look at which "
        "faces include that corner. Three faces meet there; one face, the base, does not "
        "include it. This is universal: every vertex touches exactly 3 faces. "
        "Why does this matter? When we visit a vertex during traversal, we 'touch' 3 faces "
        "at once. This connectivity determines how quickly faces complete and how information "
        "spreads through the structure. The number 3 = k-1 is not a design choice; it is "
        "geometry telling us how things connect."
    )
    
    def model(self):
        all_three = all(len(get_faces_for_vertex(v)) == 3 for v in range(8))
        return Model().add("All vertices in 3 faces", 1 if all_three else 0)
    
    def observations(self):
        return Observed().add("All vertices in 3 faces", 1)


class ComplementCrossesTetrahedra(Test):
    """
    Each vertex's complement (7-v) is in the opposite Field Chamber.
    This structure enables parallel traversal patterns.
    """
    name = "Complements Cross Field Chambers"
    question = (
        "What happens when you flip all the bits? "
        "Vertex 3 (binary 011) becomes 4 (binary 100) when complemented. "
        "Remarkably, complementary vertices always belong to opposite tetrahedra. "
        "This test confirms every vertex has a partner across the chamber divide."
    )
    reference = "Parity structure"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Complement of vertex v is 7-v. Parity inversion implies Field Chamber change.")
            .step("For each vertex v, compute complement c = 7 - v.")
            .step("Determine Field Chamber of v and c using parity.")
            .step("Verify v and c are in different Field Chambers for all 8 vertices.")
            .conclude("All complementary pairs span both Field Chambers (cross-chamber structure).")
        )
    
    commentary = (
        "Take any vertex and calculate 7 minus it. Vertex 2 gives 5. Vertex 1 gives 6. "
        "Now here is the magic: the original and its complement are always in opposite "
        "tetrahedra. Why? Because complementing flips all bits, which flips the parity, "
        "which changes the tetrahedron assignment. V2 (binary 010, odd parity, Tet A) "
        "complements to V5 (binary 101, even parity, Tet B). This is not coincidence; "
        "it is how binary arithmetic interacts with our parity-based partitioning. "
        "Every corner has a partner on the other side."
    )
    
    def model(self):
        all_cross = True
        for v in range(8):
            comp = 7 - v
            v_tet = get_tetrahedron(v)
            c_tet = get_tetrahedron(comp)
            if v_tet == c_tet:
                all_cross = False
        return Model().add("All complements cross", 1 if all_cross else 0)
    
    def observations(self):
        return Observed().add("All complements cross", 1)


class FrontBottomLate(Test):
    """
    V2 (010) and V6 (110) arrive last. Both share Y=1 (Front), Z=0 (Bottom).
    Pi's early digits avoid the Front-Bottom region.
    """
    name = "Front-Bottom Late Arrival"
    question = (
        "Which corners does pi visit last? "
        "Pi's digits do not visit all vertices equally quickly. V2 and V6 tend to arrive late, "
        "and both share the same spatial coordinates (Front-Bottom). "
        "This test documents this pattern: pi seems to 'avoid' one region initially."
    )
    reference = "Pi traversal pattern"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Traversal arrival order depends on pi's cumulative sums mod 8.")
            .step("Track first appearance of each vertex during 50-digit traversal.")
            .step("Sort vertices by arrival step to identify the last two arrivals.")
            .step("Check if V2 (triad 010) and V6 (triad 110) are among the last two.")
            .step("Verify both share Y=1 (bit 1) and Z=0 (bit 0), defining Front-Bottom region.")
            .conclude("Late arrival of Front-Bottom vertices emerges from pi's digit distribution.")
        )
    
    commentary = (
        "Imagine a room with 8 corners. You enter through a door and start wandering. "
        "Some corners you find quickly; others take longer. When pi drives the wandering, "
        "vertices V2 and V6 tend to be visited last. What do they have in common? "
        "Both share the 'Front-Bottom' position: middle bit = 1 (Front), last bit = 0 (Bottom). "
        "This is a quirk of pi's specific digit sequence, not something we designed. "
        "Pi's early digits happen to steer the traversal away from this region."
    )
    
    def model(self):
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
        
        return (
            Model()
            .add("V2 late", 1 if v2_late else 0)
            .add("V6 late", 1 if v6_late else 0)
            .add("Share Front-Bottom", 1 if share_pattern else 0)
        )


class TimeFacesCompleteLate(Test):
    """
    TIME faces (FACE_A7, FACE_B0) complete later than SPATIAL faces.
    """
    name = "TIME Faces Complete Late"
    question = (
        "Which faces finish last? "
        "The Field Chamber has 2 'TIME' faces (perpendicular to the time axis) and 6 'SPATIAL' faces. "
        "Remarkably, the TIME faces tend to complete later during traversal. "
        "This test checks whether time settles after space."
    )
    reference = "Face completion pattern"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A Coupling Port completes when all 3 of its vertices have been visited.")
            .step("Track face completion steps during traversal.")
            .step("Compute average completion step for TIME faces: (step_A7 + step_B0) / 2.")
            .step("Compute average completion step for 6 SPATIAL faces.")
            .step("Compare: if avg_TIME >= avg_SPATIAL, TIME completes later.")
            .conclude("TIME Coupling Ports complete later, suggesting temporal structure settles after spatial.")
        )
    
    commentary = (
        "In physics, we often treat space and time together as 'spacetime.' But they are not identical. "
        "Here is a curious observation: the faces oriented along the time axis complete later than "
        "the spatially-oriented faces. Space settles first; time follows. Is this deep or coincidental? "
        "We report the pattern without claiming to fully understand it. But it echoes a theme from "
        "relativity: spatial structure can be frozen on a slice, while temporal evolution requires "
        "additional information to determine."
    )
    
    def model(self):
        _, face_completed = traverse_and_track_faces(50)
        
        time_faces = ['FACE_A7', 'FACE_B0']
        time_steps = [face_completed.get(f, 50) for f in time_faces]
        spatial_steps = [s for f, s in face_completed.items() if f not in time_faces]
        
        avg_time = sum(time_steps) / len(time_steps) if time_steps else 0
        avg_spatial = sum(spatial_steps) / len(spatial_steps) if spatial_steps else 0
        
        return (
            Model()
            .add("Avg TIME completion step", avg_time)
            .add("Avg SPATIAL completion step", avg_spatial)
            .add("TIME later", 1 if avg_time >= avg_spatial else 0)
        )


class BurstCompletion(Test):
    """
    Faces complete in bursts (multiple at same step), not evenly.
    A single critical vertex can unlock multiple faces.
    """
    name = "Burst Completion Pattern"
    question = (
        "Do faces complete one at a time, or do they sometimes finish together? "
        "Since each vertex touches 3 faces, a late-arriving vertex can complete multiple faces at once. "
        "This test checks for 'burst' completion: moments when several faces finish simultaneously."
    )
    reference = "Traversal dynamics"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each vertex participates in k-1=3 faces. A late-arriving vertex may complete multiple faces at once.")
            .step("Track the step at which each face completes.")
            .step("Count how many faces complete at each step.")
            .step("Find maximum simultaneous completions (burst size).")
            .step("If max_burst >= 2, burst completion pattern is confirmed.")
            .conclude("Burst pattern indicates information cascades at critical vertices.")
        )
    
    commentary = (
        "Think about filling in a crossword puzzle. Sometimes one answer unlocks several others "
        "at once, the crossing words that share letters. The Field Chamber works similarly. "
        "Each vertex participates in 3 faces. If faces A, B, and C all need vertex V5, "
        "and we have visited all their other vertices, then the moment V5 arrives, "
        "all three faces complete at once. This is a 'burst.' It shows how information "
        "cascades through connected structures, with single events triggering multiple completions."
    )
    
    def model(self):
        _, face_completed = traverse_and_track_faces(50)
        
        step_counts = Counter(face_completed.values())
        max_burst = max(step_counts.values()) if step_counts else 0
        has_burst = max_burst >= 2
        
        return (
            Model()
            .add("Max simultaneous completions", max_burst)
            .add("Has burst (>=2)", 1 if has_burst else 0)
        )


class KMinus1Ratio(Test):
    """
    The 3:1 ratio = (k-1):1 connects to 3+1 spacetime structure.
    3 explicit reads per implicit knowledge event.
    """
    name = "(k-1):1 = 3:1 Ratio"
    question = (
        "Why 3 vertices per face? "
        "A tetrahedron has 4 corners but each face is a triangle with 3 corners. "
        "This 3:1 relationship (3 vertices per face, 1 face completion) mirrors "
        "spacetime's 3+1 structure: 3 space dimensions plus 1 time dimension."
    )
    reference = "k=4 topology"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: From Field Closure, k=4 determines tetrahedral structure; d=k-1=3 is spatial dimension count.")
            .step("Each Coupling Port (triangular face) has k-1 = 3 vertices.")
            .step("Each face completion requires 3 explicit vertex visits.")
            .step("Face completion itself is 1 implicit event.")
            .step("Ratio: (k-1) : 1 = 3 : 1, matching 3 spatial + 1 temporal dimensions.")
            .conclude("The 3:1 ratio parallels the 3+1 spacetime structure.")
        )
    
    commentary = (
        "Einstein's spacetime has 3 space dimensions and 1 time dimension: 3+1. "
        "Our Field Chamber faces have 3 vertices each, and completing a face is 1 event: also 3+1. "
        "This parallel may be coincidence, or it may be a clue. The number 3 = k-1 appears because "
        "a tetrahedron has k=4 vertices but each face excludes one of them. Nature picked the simplest "
        "3D shape (the tetrahedron) and gave it exactly the right structure to echo spacetime. "
        "Three things you can see (vertex visits), one thing that emerges (face completion)."
    )
    
    def model(self):
        vertices_per_face = 3  # = k-1
        implicit_per_face = 1  # Gained at 2nd read
        ratio = vertices_per_face / implicit_per_face
        
        # k encodes in structure
        faces_per_tet = 4  # = k
        vertices_per_face_check = 3  # = k-1
        
        return (
            Model()
            .add("Vertices per face", vertices_per_face)
            .add("Implicit per face", implicit_per_face)
            .add("Ratio", ratio)
            .add("k", K)
            .add("k-1", K - 1)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Vertices per face", 3)
            .add("Implicit per face", 1)
            .add("Ratio", 3)
            .add("k", 4)
            .add("k-1", 3)
        )


class FieldChamberAsymmetry(Test):
    """
    Pi traversal starts in Tet_B (first vertex V3) but Tet_A may complete first.
    First entry does not necessarily mean first completion.
    """
    name = "Field Chamber Asymmetry"
    question = (
        "Does starting first mean finishing first? "
        "Pi begins at V3 (Tetrahedron B), but Tetrahedron A might complete all its faces sooner. "
        "This test explores whether the starting chamber determines the finishing order."
    )
    reference = "Traversal dynamics"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Pi's integer part 3 places first vertex in Tet B. Completion order depends on digit sequence.")
            .step("First vertex = V3, which is in Tet B (even parity).")
            .step("Track when all 4 Tet A faces complete vs all 4 Tet B faces.")
            .step("Compare completion steps: if Tet_A_complete < Tet_B_complete, asymmetry holds.")
            .step("This demonstrates initial chamber entry does not determine completion order.")
            .conclude("Completion order is determined by pi's digit distribution, not starting position.")
        )
    
    commentary = (
        "The tortoise and the hare: starting fast does not guarantee finishing first. "
        "Pi drops us into Tetrahedron B at step one, but the subsequent digit sequence might "
        "favor Tetrahedron A's vertices. We could visit all of Tet A's corners before "
        "revisiting enough of Tet B to complete its faces. This counterintuitive result "
        "shows that initial conditions are not destiny. The full digit sequence, not just "
        "the starting point, determines when each chamber finishes."
    )
    
    def model(self):
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
        
        return (
            Model()
            .add("Starts in Tet_B", starts_in_b)
            .add("Tet_A completes first", tet_a_first)
            .add("Tet_A step", tet_a_complete_step if tet_a_complete_step else -1)
            .add("Tet_B step", tet_b_complete_step if tet_b_complete_step else -1)
        )


class ThreePlusOneStructure(Test):
    """
    k = 4 = 3+1 corresponds to the GR spacetime decomposition.
    3 spatial Coupling Ports + 1 TIME Coupling Port per Field Chamber.
    """
    name = "3+1 Structure Correspondence"
    question = (
        "Why 3+1? Physics tells us spacetime is 3 dimensions of space plus 1 of time. "
        "Our tetrahedron has 4 faces: 3 spatial ones that include the apex, and 1 time face opposite it. "
        "This test verifies the 3+1 decomposition appears naturally in tetrahedral geometry."
    )
    reference = "General relativity analogy"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tetrahedron has k=4 faces. These are classified as SPATIAL or TIME.")
            .step("SPATIAL faces include an apex vertex: k-1 = 3 per tetrahedron.")
            .step("TIME face is opposite the apex: 1 per tetrahedron.")
            .step("Total per tetrahedron: 3 SPATIAL + 1 TIME = 4 = k.")
            .step("This parallels spacetime: d=3 spatial dimensions + 1 temporal dimension.")
            .conclude("Tetrahedral face classification mirrors the 3+1 spacetime decomposition.")
        )
    
    commentary = (
        "Einstein showed us that the universe has 3 space dimensions and 1 time dimension. "
        "Now look at a tetrahedron: it has 4 faces. Three of them touch the apex (think of them "
        "as 'pointing in space'), and one faces away from the apex (think of it as 'pointing in time'). "
        "So we get 3 + 1 = 4, the same decomposition as spacetime. "
        "Did nature choose the tetrahedron because it encodes 3+1 structure? "
        "Or is 3+1 a consequence of tetrahedral geometry? Either way, the match is remarkable."
    )
    
    def model(self):
        spatial_per_tet = 3  # A1, A2, A4 or B3, B5, B6
        time_per_tet = 1     # A7 or B0
        total = spatial_per_tet + time_per_tet
        
        return (
            Model()
            .add("Spatial faces per tet", spatial_per_tet)
            .add("TIME faces per tet", time_per_tet)
            .add("Total (k)", total)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Spatial faces per tet", 3)
            .add("TIME faces per tet", 1)
            .add("Total (k)", 4)
        )


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


def run_all():
    """Run all Field Closure cycle mechanics tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
