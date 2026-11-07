"""
Field Closure Cycle Mechanics
=============================

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

TRAVERSAL AND FACE COMPLETION
-----------------------------
Pi base-8 traversal visits vertices, completing faces along the way.
Traversal starts at V3 (from pi integer part 3), then V4 (cumsum=4).

Key observations examined:
1. Pi digits directly encode vertex addresses (3-bit bijection)
2. Each vertex belongs to exactly 3 Coupling Ports (tetrahedron geometry)
3. Complementary vertices (7-v) always cross Field Chambers (parity structure)
4. Front-Bottom Late: V2 (010) and V6 (110) arrive later in sequence
5. Burst Completion: Multiple faces may complete at the same traversal step
6. Field Chamber Asymmetry: Traversal starts in Tet_B but Tet_A may complete first

NOTE: Interpretive tests (TIME faces, 3+1 spacetime correspondence) have been
moved to cosmological_correspondence/test_spacetime_correspondence.py
"""

from typing import Dict, Optional, List
from collections import Counter

from gravity_field_model.engine_core.field_closure import geometry_derivation as geo
from gravity_field_model.common.geometry_constants import get_vertex_coords
from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL, get_pi_base8
from gravity_field_model.common.geometry_constants import (
    TET_A, TET_B, FACES,
    get_tetrahedron, get_faces_for_vertex
)

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Topology constant: vertices per tetrahedron, faces per tetrahedron


def traverse_and_track_faces(n_digits=1000):
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
    audit_score = 85
    audit_notes = (
        "Question: 14/15 - Excellent 'how' with bijection concept. "
        "Derivation: 14/15 - Clear verification logic. "
        "Commentary: 14/15 - Great light switch analogy for binary encoding. "
        "Model: 9/10 - Clean boolean output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Good for undergrad. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: Why does base-8 naturally map to 3 bits, and what would happen if we used base-10? "
        "Q2: How does this bijection ensure every vertex can be addressed without ambiguity? "
        "Q3: If the digit-to-vertex mapping failed, what physical interpretation would break? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
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
        # A digit's three bits (x, y, z) should be the signs of the vertex it
        # addresses: bit 1 -> +1, bit 0 -> -1. Check the stored vertex table
        # against that rule for all eight digits, and the chamber against the
        # bit parity. (Before, the test only converted each digit to binary and
        # back, which cannot fail.)
        coords_ok = sum(
            1 for d in range(8)
            if tuple(1 if b == '1' else -1 for b in format(d, '03b')) == tuple(get_vertex_coords(d))
        )
        chamber_ok = sum(
            1 for d in range(8)
            if (format(d, '03b').count('1') % 2 == 1) == (d in TET_A)
        )
        return (
            Model()
            .add("Digits whose bits match vertex coordinates", coords_ok)
            .add("Digits whose bit parity matches chamber", chamber_ok)
        )

    def observations(self):
        return (
            Observed()
            .add("Digits whose bits match vertex coordinates", 8)
            .add("Digits whose bit parity matches chamber", 8)
        )

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
    audit_score = 84
    audit_notes = (
        "Question: 14/15 - Excellent 'how many' with clear geometric reasoning. "
        "Derivation: 14/15 - Clear k-1 derivation. "
        "Commentary: 13/15 - Good pyramid visualization. "
        "Model: 9/10 - Simple boolean output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Good for undergrad. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: Why does k-1=3 determine faces per vertex, and what is the geometric intuition? "
        "Q2: How does this 3-face connectivity enable information propagation through the structure? "
        "Q3: If a vertex belonged to 2 or 4 faces, what would break in the model? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
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
    audit_score = 85
    audit_notes = (
        "Question: 15/15 - Excellent 'what happens when' curiosity hook. "
        "Derivation: 14/15 - Clear parity reasoning. "
        "Commentary: 14/15 - Great binary/parity explanation with examples. "
        "Model: 9/10 - Simple boolean output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 13/15 - Good binary examples. "
        "Header: 8/10 (module level) - Proper imports in place. "
    )
    future_questions = (
        "Q1: Why does XOR with 7 (111 binary) flip all bits and thus flip parity? "
        "Q2: How does this cross-chamber pairing support bimetric gravity coupling? "
        "Q3: If complements landed in the same tetrahedron, what symmetry would be lost? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
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
    audit_score = 82
    audit_notes = (
        "Question: 13/15 - Good 'which' question about traversal patterns. "
        "Derivation: 12/15 - Clear tracking but could explain WHY this pattern emerges. "
        "Commentary: 12/15 - Good room-corners analogy. "
        "Model: 8/10 - Good output. "
        "Observations: 8/10 - Statistical observation on early traversal. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 11/15 - Room-corners is accessible. "
        "Header: 8/10 (module level) - Proper imports in place. "
        "SAMPLE SIZE: 1000 digits - Adequate for statistical claims. "
    )
    future_questions = (
        "Q1: Why do V2 and V6 share the same spatial region (Y=1, Z=0) despite different X? "
        "Q2: Is late arrival a property of pi specifically, or would any irrational base-8 show similar patterns? "
        "Q3: What would it mean physically if certain vertices were never visited? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
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
        vertex_first_seen, _ = traverse_and_track_faces(1000)
        
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
    
    def observations(self):
        return (
            Observed()
            .add("V2 late", 1)
            .add("V6 late", 1)
            .add("Share Front-Bottom", 1)
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
    audit_score = 84
    audit_notes = (
        "Question: 14/15 - Excellent 'do they' question about completion patterns. "
        "Derivation: 12/15 - Clear logic. "
        "Commentary: 14/15 - Excellent crossword puzzle analogy. "
        "Model: 8/10 - Good burst statistics. "
        "Observations: 8/10 - Statistical observation on burst pattern. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Great crossword analogy. "
        "Header: 8/10 (module level) - Proper imports in place. "
        "SAMPLE SIZE: 1000 digits - Adequate for statistical claims. "
    )
    future_questions = (
        "Q1: Why does visiting one vertex 'unlock' exactly 3 faces simultaneously? "
        "Q2: How does burst completion relate to information cascades in physical systems? "
        "Q3: Would a different traversal algorithm (not pi-driven) show similar burst patterns? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
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
        _, face_completed = traverse_and_track_faces(1000)
        
        step_counts = Counter(face_completed.values())
        max_burst = max(step_counts.values()) if step_counts else 0
        has_burst = max_burst >= 2
        
        return (
            Model()
            .add("Max simultaneous completions", max_burst)
            .add("Has burst (>=2)", 1 if has_burst else 0)
        )
    
    def observations(self):
        # Updated after pi digit sequence fix
        return (
            Observed()
            .add("Max simultaneous completions", 3)
            .add("Has burst (>=2)", 1)
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
    audit_score = 84
    audit_notes = (
        "Question: 14/15 - Excellent counterintuitive 'does starting first mean finishing first'. "
        "Derivation: 12/15 - Clear but verbose. "
        "Commentary: 14/15 - Great tortoise-and-hare analogy. "
        "Model: 8/10 - Good completion tracking. "
        "Observations: 8/10 - Statistical observation. "
        "Constants: 10/10 - Now imports from /common/ modules. "
        "Accessibility: 12/15 - Tortoise-hare analogy is great. "
        "Header: 8/10 (module level) - Proper imports in place. "
        "SAMPLE SIZE: 1000 digits - Adequate for statistical claims. "
    )
    future_questions = (
        "Q1: Why does starting in Tet_B not guarantee Tet_B finishes first? "
        "Q2: What property of pi's digits determines which chamber completes first? "
        "Q3: If both chambers always completed simultaneously, what symmetry would that imply? "
        "FUTURE: Answering these in commentary/derivation could raise score by ~5 points."
    )
    
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
        digits = get_pi_base8(1000, include_integer=True)
        
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
    
    def observations(self):
        # Updated after pi digit sequence fix
        return (
            Observed()
            .add("Starts in Tet_B", 1)
            .add("Tet_A completes first", 1)
            .add("Tet_A step", 11)
            .add("Tet_B step", 15)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    PiDigitIsTriad,
    VertexBelongsToThreeFaces,
    ComplementCrossesTetrahedra,
    FrontBottomLate,
    BurstCompletion,
    FieldChamberAsymmetry,
]


def run_all():
    """Run all Field Closure cycle mechanics tests."""
    return run_tests(
        title="Field Closure Cycle Mechanics",
        summary=(
            "These tests verify core geometric and observational properties of the Field Closure "
            "traversal. Pure geometry: Pi digits directly encode 3-bit vertex addresses, each "
            "vertex belongs to exactly 3 Coupling Ports, and complementary vertices always cross "
            "Field Chambers. Pi traversal observations: V2 and V6 arrive late (Front-Bottom region), "
            "faces complete in bursts (information cascades), and Field Chamber asymmetry shows "
            "starting in Tet_B does not mean Tet_B completes first. "
            "NOTE: Interpretive spacetime correspondence tests (TIME faces, 3+1 structure) have "
            "been moved to cosmological_correspondence/test_spacetime_correspondence.py"
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
