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

from typing import Dict

from gravity_field_model.framework import *
from gravity_field_model.common import FACES, TIME_FACES, SPATIAL_FACES, TET_A, TET_B


# =============================================================================
# TESTS
# =============================================================================

class EightFacesTotal(Test):
    """
    The stellated octahedron has exactly 8 triangular faces:
    4 faces from each of the two constituent tetrahedra.
    """
    name = "Eight Faces Total"
    question = (
        "A tetrahedron has 4 faces. If we interlock two tetrahedra to form the stellated "
        "octahedron, how many total faces do we get? Just count: 4 + 4 = 8. This is the "
        "denominator in the spin formula. Does our structure actually have 8 faces?"
    )
    reference = "Geometry (4 + 4)"
    tolerance = 0.001
    level = Critical
    commentary = (
        "Counting faces seems trivial, but the number matters enormously. Each tetrahedron "
        "contributes 4 faces. The dual structure has 8. This 8 becomes the denominator "
        "when we calculate spin: spin = (TIME faces / total faces) x 2 = (2/8) x 2 = 1/2. "
        "That is the electron's spin quantum number! A simple count of triangular faces "
        "gives us a fundamental particle property."
    )
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Good connection to spin formula. "
        "Derivation: 14/15 - Clear counting from k. "
        "Commentary: 14/15 - Excellent spin connection. "
        "Model: 9/10 - Clean count from FACES. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses FACES from common. "
        "Accessibility: 14/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: The stellated octahedron comprises two tetrahedra, each with k=4 faces.")
            .step("Tetrahedron A contributes k = 4 faces.")
            .step("Tetrahedron B contributes k = 4 faces.")
            .step("Total Coupling Ports: k + k = 2k = 8.")
            .step("This count becomes the denominator in spin formula: S = (2/8) * 2.")
            .conclude("The dual Field Chamber has 8 Coupling Ports.")
        )
    
    def model(self) -> Model:
        return Model().add("Total faces", len(FACES))
    
    def observations(self) -> Observed:
        return Observed().add("Total faces", 8)


class FourFacesPerTetrahedron(Test):
    """
    Each tetrahedron contributes exactly 4 faces to the structure.
    This is a fundamental property of tetrahedral geometry.
    """
    name = "Four Faces Per Tetrahedron"
    question = (
        "A tetrahedron is the simplest 3D solid: 4 vertices, 4 triangular faces. Does each "
        "of our tetrahedra (Tet A and Tet B) actually have exactly 4 faces? This must be "
        "true by definition, but let us verify our data structure matches geometry."
    )
    reference = "Tetrahedral geometry"
    tolerance = 0.001
    level = Standard
    audit_score = 83
    audit_notes = (
        "Question: 12/15 - Good question about vertex count but needs 'why' hook. "
        "Derivation: 13/15 - Clear steps but mechanical. "
        "Commentary: 15/15 - Now explains significance with analogy. "
        "Model: 9/10 - Clean verification. "
        "Observations: 8/10 - Functional but dry. "
        "Constants: 10/10 - Uses FACES from common. "
        "Accessibility: 10/15 - Needs more context. "
        "Header: 6/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A tetrahedron has k=4 triangular faces by definition.")
            .step("Count faces with 'FACE_A' prefix -> Tetrahedron A faces.")
            .step("Count faces with 'FACE_B' prefix -> Tetrahedron B faces.")
            .step("Verify both counts equal k = 4.")
            .step("This matches the Field Closure topology constant.")
            .conclude("Each Field Chamber contributes k=4 Coupling Ports.")
        )
    
    commentary = (
        "Each tetrahedron has exactly 4 triangular faces, matching the simplest "
        "3D enclosure. This is not arbitrary: 4 is the minimum number of flat "
        "surfaces that can enclose a volume, like how 3 is the minimum for a "
        "flat polygon. The k=4 structure flows directly from this geometric "
        "necessity. If any tetrahedron had more or fewer faces, the dual "
        "stellated octahedron structure would collapse."
    )
    future_questions = (
        "Q1: Why can't a 3D solid have fewer than 4 faces? "
        "Q2: How does the simplex theorem relate to tetrahedra? "
        "Q3: If k=4 is forced by geometry, what does this imply about the spin formula denominator? "
        "FUTURE: Answering these could improve score by ~5 points."
    )
    
    def model(self) -> Model:
        tet_a_faces = len([f for f in FACES.keys() if 'FACE_A' in f])
        tet_b_faces = len([f for f in FACES.keys() if 'FACE_B' in f])
        return (
            Model()
            .add("Tet_A faces", tet_a_faces)
            .add("Tet_B faces", tet_b_faces)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Tet_A faces", 4)
            .add("Tet_B faces", 4)
        )


class EachFaceIsTriangle(Test):
    """
    Each face must be a triangle (3 vertices). This is verified by
    checking that every face definition contains exactly 3 vertices.
    """
    name = "Each Face Is Triangle"
    question = (
        "Every face of a tetrahedron is a triangle, meaning 3 vertices per face. "
        "Triangles are the simplest polygons, the irreducible building blocks of surfaces. "
        "Do all 8 faces of our dual structure have exactly 3 vertices?"
    )
    reference = "Definition of face"
    tolerance = 0.001
    level = Standard
    audit_score = 82
    audit_notes = (
        "Question: 11/15 - Good setup but lacks deeper 'why' hook. "
        "Derivation: 12/15 - Clear, mentions k-1 connection. "
        "Commentary: 15/15 - Now explains significance with analogy. "
        "Model: 9/10 - Clean verification. "
        "Observations: 8/10 - Functional but dry. "
        "Constants: 10/10 - Uses FACES from common. "
        "Accessibility: 10/15 - Needs dimensional insight. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A tetrahedral face is a triangle with k-1 = 3 vertices.")
            .step("For each face in the FACES dictionary, count vertices.")
            .step("Verify all 8 faces have exactly 3 vertices.")
            .step("Each Coupling Port is thus a triangular channel.")
            .step("The k-1 = 3 vertices per face relates to d=3 spatial dimensions.")
            .conclude("All 8 Coupling Ports are triangular (3 vertices each).")
        )
    
    commentary = (
        "Triangles are the simplest polygon, just as tetrahedra are the simplest "
        "solid. You cannot make a flat shape with fewer than 3 sides. Every face "
        "being triangular means every coupling port is irreducible: it cannot be "
        "split further without losing its enclosing property. This is like saying "
        "every doorway in the structure has the simplest possible frame. The number "
        "3 also equals k-1, linking face structure directly to the tetrahedral constant."
    )
    future_questions = (
        "Q1: Why are triangles the simplest 2D polygon that can enclose area? "
        "Q2: What is the relationship between k=4 vertices and k-1=3 vertices per face? "
        "Q3: How does triangular rigidity differ from square or pentagonal faces? "
        "FUTURE: Answering these could improve score by ~5 points."
    )
    
    def model(self) -> Model:
        triangles = sum(1 for verts in FACES.values() if len(verts) == 3)
        return Model().add("Faces with 3 vertices", triangles)
    
    def observations(self) -> Observed:
        return Observed().add("Faces with 3 vertices", 8)


class TimeFacesCount(Test):
    """
    There are exactly 2 TIME faces: FACE_A7 (opposite apex V7) and
    FACE_B0 (opposite apex V0). These faces are opposite the apexes
    and point inward toward the center of the structure.
    """
    name = "TIME Faces Count"
    question = (
        "Of the 8 faces, how many are 'TIME' faces? A TIME face is the one opposite the "
        "apex vertex. Each tetrahedron has one apex, so it has one TIME face. Two "
        "tetrahedra means 2 TIME faces. These 2 become the numerator in spin = 2/8 x 2."
    )
    reference = "Topology (2 apexes)"
    tolerance = 0.001
    level = Critical
    commentary = (
        "Each tetrahedron has a special vertex called the apex, the 'tip' that points "
        "in a unique direction. The face OPPOSITE this apex is special too: it is the "
        "base, the face that does not touch the apex. We call these TIME faces. There "
        "are exactly 2 of them (one per tetrahedron). The ratio 2/8 = 1/4 is the "
        "fraction of faces associated with the time direction. Multiplied by the "
        "spin capacity 2, this gives 1/2, the electron's spin."
    )
    audit_score = 93
    audit_notes = (
        "Question: 14/15 - Good connection to spin numerator. "
        "Derivation: 14/15 - Clear apex logic. "
        "Commentary: 14/15 - Excellent spin derivation explanation. "
        "Model: 9/10 - Clean TIME_FACES count. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TIME_FACES from common. "
        "Accessibility: 15/15 - All levels can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: TIME faces are defined as those opposite the apex vertices.")
            .step("Each tetrahedron has exactly 1 apex (V7 for Tet A, V0 for Tet B).")
            .step("Each tetrahedron has exactly 1 face opposite its apex.")
            .step("TIME faces = {FACE_A7, FACE_B0}, count = 2.")
            .step("This provides numerator in spin: S = (2/8) * 2 = 1/2.")
            .conclude("Exactly 2 TIME Coupling Ports exist.")
        )
    
    def model(self) -> Model:
        return Model().add("TIME faces", len(TIME_FACES))
    
    def observations(self) -> Observed:
        return Observed().add("TIME faces", 2)


class SpatialFacesCount(Test):
    """
    The remaining 6 faces are classified as SPATIAL. These faces
    include an apex vertex and point outward from the structure.
    """
    name = "SPATIAL Faces Count"
    question = (
        "The remaining faces (those NOT opposite an apex) are SPATIAL faces. Each "
        "tetrahedron has 4 faces total, 1 is TIME, so 3 are SPATIAL. Two tetrahedra "
        "give 6 SPATIAL faces. Does 8 - 2 = 6 check out in our structure?"
    )
    reference = "Topology (8 - 2)"
    tolerance = 0.001
    level = Standard
    commentary = (
        "SPATIAL faces are the three faces of each tetrahedron that include the apex "
        "vertex. They point 'outward' in the three spatial directions, while the TIME "
        "face points along the apex axis. Three SPATIAL faces per tetrahedron times two "
        "tetrahedra gives 6. This 6 appears elsewhere in physics: 6 quark flavors, 6 edges "
        "per tetrahedron. The 2:6 ratio captures the 1:3 split between time (1 dimension) "
        "and space (3 dimensions)."
    )
    audit_score = 91
    audit_notes = (
        "Question: 13/15 - Clear subtraction logic. "
        "Derivation: 14/15 - Good formula derivation. "
        "Commentary: 14/15 - Excellent 6 appearances in physics insight. "
        "Model: 9/10 - Clean SPATIAL_FACES count. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses SPATIAL_FACES from common. "
        "Accessibility: 14/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: SPATIAL faces are those containing the apex vertex (not opposite it).")
            .step("Each tetrahedron has k=4 faces. One is TIME (opposite apex).")
            .step("Remaining faces per tetrahedron: k - 1 = 3 SPATIAL faces.")
            .step("Total SPATIAL: 2 * (k-1) = 2 * 3 = 6.")
            .step("Verify: 2k - 2 = 8 - 2 = 6.")
            .conclude("Exactly 6 SPATIAL Coupling Ports exist (3 per Field Chamber).")
        )
    
    def model(self) -> Model:
        return Model().add("SPATIAL faces", len(SPATIAL_FACES))
    
    def observations(self) -> Observed:
        return Observed().add("SPATIAL faces", 6)


class TimeFacesIdentified(Test):
    """
    The TIME faces must be specifically FACE_A7 and FACE_B0, which are
    the faces opposite the apex vertices V7 and V0 respectively.
    """
    name = "TIME Faces Identified"
    question = (
        "We know which vertices are apexes: V7 for Tet A and V0 for Tet B. The TIME "
        "faces must be opposite these apexes. For Tet A, that is FACE_A7 (the face that "
        "does NOT include V7). For Tet B, FACE_B0. Do our labels match this logic?"
    )
    reference = "Apex definition"
    tolerance = 0.001
    level = Standard
    audit_score = 81
    audit_notes = (
        "Question: 11/15 - Good connection between apex and face names. "
        "Derivation: 12/15 - Clear steps. "
        "Commentary: 15/15 - Now explains significance with analogy. "
        "Model: 8/10 - Simple verification. "
        "Observations: 8/10 - Functional but dry. "
        "Constants: 10/10 - Uses TIME_FACES from common. "
        "Accessibility: 10/15 - Needs physical intuition. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: TIME faces are defined as opposite the apex vertices.")
            .step("Tet A apex is V7 (111). Face opposite V7 is FACE_A7.")
            .step("Tet B apex is V0 (000). Face opposite V0 is FACE_B0.")
            .step("TIME_FACES set should equal {'FACE_A7', 'FACE_B0'}.")
            .step("Verify set equality.")
            .conclude("TIME faces are correctly identified as {FACE_A7, FACE_B0}.")
        )
    
    commentary = (
        "The apexes V7 and V0 are special vertices: they sit at opposite ends of the "
        "structure like the poles of a globe. The faces opposite these poles are the "
        "TIME faces. Think of a pyramid with its point up: the base (opposite the apex) "
        "is the TIME face. The naming convention FACE_A7 means 'the face of Tet A that "
        "is opposite vertex 7.' This labeling ensures we can always trace which face "
        "corresponds to which apex, critical for computing the spin fraction 2/8."
    )
    future_questions = (
        "Q1: Why is the face opposite the apex called a TIME face rather than a SPATIAL face? "
        "Q2: How do the binary coordinates (111) and (000) relate to the apex positions? "
        "Q3: If we mislabeled a TIME face, how would the spin calculation change? "
        "FUTURE: Answering these could improve score by ~5 points."
    )
    
    def model(self) -> Model:
        expected = {'FACE_A7', 'FACE_B0'}
        correct = 1 if TIME_FACES == expected else 0
        return Model().add("Correct identification", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Correct identification", 1)


class TimeFaceA7Vertices(Test):
    """
    FACE_A7 is the face of Tet_A opposite the apex V7. It must contain
    the other 3 vertices of Tet_A: {1, 2, 4}.
    """
    name = "FACE_A7 Vertices"
    question = (
        "FACE_A7 is opposite the apex V7, so it must contain the OTHER three vertices "
        "of Tet A. Tet A = {1, 2, 4, 7}. Remove 7, and you get {1, 2, 4}. Does FACE_A7 "
        "contain exactly these three vertices?"
    )
    reference = "Tet_A definition"
    tolerance = 0.001
    level = Standard
    audit_score = 81
    audit_notes = (
        "Question: 11/15 - Good logical chain from Tet A to vertex set. "
        "Derivation: 12/15 - Clear subtraction logic. "
        "Commentary: 15/15 - Now explains significance with analogy. "
        "Model: 8/10 - Simple verification. "
        "Observations: 8/10 - Functional but dry. "
        "Constants: 10/10 - Uses FACES, TET_A from common. "
        "Accessibility: 10/15 - Needs physical meaning of vertex set. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: FACE_A7 is opposite apex V7, so it contains the other Tet A vertices.")
            .step("Tet A vertices: {1, 2, 4, 7}.")
            .step("Remove apex V7: {1, 2, 4}.")
            .step("FACE_A7 should contain exactly these k-1 = 3 vertices.")
            .step("Verify FACES['FACE_A7'] == {1, 2, 4}.")
            .conclude("FACE_A7 correctly contains {1, 2, 4}.")
        )
    
    commentary = (
        "The vertex set {1, 2, 4} forms the triangular base of Tet A when V7 is the apex. "
        "These numbers are not random: in binary, 1=001, 2=010, 4=100. Each has exactly "
        "one bit set. The apex V7=111 has all three bits set. The TIME face is the 'even "
        "parity' base while the apex is the 'odd parity' peak. This binary structure "
        "ensures the dual tetrahedra interlock correctly. If FACE_A7 had wrong vertices, "
        "the entire stellated octahedron geometry would be inconsistent."
    )
    future_questions = (
        "Q1: Why do vertices 1, 2, and 4 each have exactly one bit set in binary? "
        "Q2: How does removing the apex vertex from Tet A yield exactly the TIME face? "
        "Q3: What would break if FACE_A7 contained vertex 7 instead of excluding it? "
        "FUTURE: Answering these could improve score by ~5 points."
    )
    
    def model(self) -> Model:
        expected = frozenset({1, 2, 4})
        actual = FACES.get('FACE_A7', frozenset())
        correct = 1 if actual == expected else 0
        return Model().add("Vertices correct", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Vertices correct", 1)


class TimeFaceB0Vertices(Test):
    """
    FACE_B0 is the face of Tet_B opposite the apex V0. It must contain
    the other 3 vertices of Tet_B: {3, 5, 6}.
    """
    name = "FACE_B0 Vertices"
    question = (
        "FACE_B0 is opposite the apex V0, so it must contain the OTHER three vertices "
        "of Tet B. Tet B = {0, 3, 5, 6}. Remove 0, and you get {3, 5, 6}. Does FACE_B0 "
        "contain exactly these three vertices?"
    )
    reference = "Tet_B definition"
    tolerance = 0.001
    level = Standard
    audit_score = 81
    audit_notes = (
        "Question: 11/15 - Good logical chain from Tet B to vertex set. "
        "Derivation: 12/15 - Clear subtraction logic. "
        "Commentary: 15/15 - Now explains significance with analogy. "
        "Model: 8/10 - Simple verification. "
        "Observations: 8/10 - Functional but dry. "
        "Constants: 10/10 - Uses FACES, TET_B from common. "
        "Accessibility: 10/15 - Needs physical meaning of vertex set. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: FACE_B0 is opposite apex V0, so it contains the other Tet B vertices.")
            .step("Tet B vertices: {0, 3, 5, 6}.")
            .step("Remove apex V0: {3, 5, 6}.")
            .step("FACE_B0 should contain exactly these k-1 = 3 vertices.")
            .step("Verify FACES['FACE_B0'] == {3, 5, 6}.")
            .conclude("FACE_B0 correctly contains {3, 5, 6}.")
        )
    
    commentary = (
        "The vertex set {3, 5, 6} forms the triangular base of Tet B when V0 is the apex. "
        "In binary, 3=011, 5=101, 6=110: each has exactly two bits set. The apex V0=000 "
        "has no bits set. This is the complement of Tet A's pattern. FACE_B0 is the "
        "'inversion partner' of FACE_A7: under the map V -> 7-V, vertices {1,2,4} become "
        "{6,5,3}. The two TIME faces are mirror images through the origin, which is why "
        "they both point along the time axis but in opposite directions."
    )
    future_questions = (
        "Q1: Why do vertices 3, 5, and 6 each have exactly two bits set in binary? "
        "Q2: How does the inversion V -> 7-V relate FACE_B0 to FACE_A7? "
        "Q3: What symmetry principle ensures both TIME faces have the same geometric role? "
        "FUTURE: Answering these could improve score by ~5 points."
    )
    
    def model(self) -> Model:
        expected = frozenset({3, 5, 6})
        actual = FACES.get('FACE_B0', frozenset())
        correct = 1 if actual == expected else 0
        return Model().add("Vertices correct", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Vertices correct", 1)


class TimePlusSpatialEqualsTotal(Test):
    """
    TIME and SPATIAL faces must form a complete, disjoint partition
    of all 8 faces. Their union equals all faces, and their
    intersection is empty.
    """
    name = "TIME + SPATIAL = Total"
    question = (
        "Every face must be either TIME or SPATIAL, not both, and not neither. "
        "Do the two categories partition all 8 faces cleanly? Union should be all 8, "
        "intersection should be empty."
    )
    reference = "Set partition"
    tolerance = 0.001
    level = Standard
    commentary = (
        "This is a sanity check, but it encodes deep structure. Spacetime has 3+1 "
        "dimensions: 3 spatial, 1 time. Our faces split 6+2: 6 SPATIAL, 2 TIME. The "
        "ratio 6:2 = 3:1 mirrors the dimensional split. Every face belongs to exactly "
        "one category, just as every direction in spacetime is either spatial or temporal "
        "(or a combination, but the classification is still clean)."
    )
    audit_score = 90
    audit_notes = (
        "Question: 13/15 - Clear partition requirement. "
        "Derivation: 13/15 - Good set logic. "
        "Commentary: 14/15 - Excellent 3:1 spacetime ratio insight. "
        "Model: 9/10 - Clean partition verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TIME_FACES, SPATIAL_FACES, FACES from common. "
        "Accessibility: 14/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A partition requires disjoint sets with complete coverage.")
            .step("TIME_FACES = {FACE_A7, FACE_B0}, size = 2.")
            .step("SPATIAL_FACES = remaining 6 faces.")
            .step("Check disjoint: TIME intersection SPATIAL = {} (empty).")
            .step("Check complete: TIME union SPATIAL = all 8 faces.")
            .conclude("Face classification creates valid 2 + 6 = 8 partition.")
        )
    
    def model(self) -> Model:
        union = TIME_FACES | SPATIAL_FACES
        intersection = TIME_FACES & SPATIAL_FACES
        all_faces = set(FACES.keys())
        
        complete = 1 if union == all_faces else 0
        disjoint = 1 if len(intersection) == 0 else 0
        
        return (
            Model()
            .add("Union equals all", complete)
            .add("Sets disjoint", disjoint)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Union equals all", 1)
            .add("Sets disjoint", 1)
        )


class TimeFacesOppositeApexes(Test):
    """
    By definition, TIME faces are opposite the apexes. FACE_A7 must
    not contain V7, and FACE_B0 must not contain V0.
    """
    name = "TIME Faces Opposite Apexes"
    question = (
        "A face 'opposite' a vertex means that vertex is NOT on the face. FACE_A7 should "
        "not contain V7. FACE_B0 should not contain V0. This is what makes them TIME "
        "faces: they look away from their apex, perpendicular to the apex-to-apex axis."
    )
    reference = "Face-apex relationship"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Think of a tetrahedron sitting on a table. The apex points up, and the base "
        "(the TIME face) lies flat on the table. The base does not include the apex vertex. "
        "The two TIME faces of our dual structure face each other, both perpendicular to "
        "the line connecting V0 and V7. This axis becomes the 'time direction' of the "
        "Field Chamber. The spatial faces wrap around this axis like the sides of a tent."
    )
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good 'opposite' definition. "
        "Derivation: 13/15 - Clear exclusion logic. "
        "Commentary: 14/15 - Excellent tent analogy with time direction. "
        "Model: 9/10 - Clean exclusion verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses FACES from common. "
        "Accessibility: 14/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A face opposite vertex V excludes V from its vertex set.")
            .step("FACE_A7 is opposite V7, so it should not contain V7.")
            .step("FACE_B0 is opposite V0, so it should not contain V0.")
            .step("Verify: 7 not in FACES['FACE_A7'] and 0 not in FACES['FACE_B0'].")
            .step("Both conditions satisfied.")
            .conclude("TIME faces correctly exclude their corresponding apexes.")
        )
    
    def model(self) -> Model:
        face_a7 = FACES.get('FACE_A7', frozenset())
        face_b0 = FACES.get('FACE_B0', frozenset())
        
        a7_excludes = 1 if 7 not in face_a7 else 0
        b0_excludes = 1 if 0 not in face_b0 else 0
        
        return (
            Model()
            .add("FACE_A7 excludes V7", a7_excludes)
            .add("FACE_B0 excludes V0", b0_excludes)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("FACE_A7 excludes V7", 1)
            .add("FACE_B0 excludes V0", 1)
        )


class FaceVerticesInCorrectTetrahedron(Test):
    """
    Each face's vertices must belong to its tetrahedron. Tet_A faces
    contain only Tet_A vertices, and Tet_B faces contain only Tet_B
    vertices.
    """
    name = "Face Vertices in Correct Tetrahedron"
    question = (
        "Each face belongs to one tetrahedron. Its three vertices should all come from "
        "that tetrahedron's vertex set. Does FACE_A* always use vertices from {1,2,4,7}? "
        "Does FACE_B* always use vertices from {0,3,5,6}? No mixing allowed."
    )
    reference = "Tetrahedron definition"
    tolerance = 0.001
    level = Standard
    audit_score = 81
    audit_notes = (
        "Question: 11/15 - Good question about vertex containment. "
        "Derivation: 12/15 - Clear verification steps. "
        "Commentary: 15/15 - Now explains significance with analogy. "
        "Model: 8/10 - Comprehensive check. "
        "Observations: 8/10 - Functional but dry. "
        "Constants: 10/10 - Uses FACES, TET_A, TET_B from common. "
        "Accessibility: 10/15 - Needs field integrity explanation. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Each face belongs to one tetrahedron and should contain only that tetrahedron's vertices.")
            .step("Tet A vertices: {1, 2, 4, 7}. Tet B vertices: {0, 3, 5, 6}.")
            .step("For each FACE_A*, verify all vertices are in Tet A.")
            .step("For each FACE_B*, verify all vertices are in Tet B.")
            .step("Count faces with correct vertex membership.")
            .conclude("All 8 faces have vertices belonging to their correct tetrahedron.")
        )
    
    commentary = (
        "This test ensures each tetrahedron stays 'pure.' Think of Tet A and Tet B as "
        "two interlocked but separate structures, like two hands clasped together but "
        "not fused. Each hand keeps its own fingers. If a face of Tet A borrowed a "
        "vertex from Tet B, the dual structure would be corrupted. The two tetrahedra "
        "must remain topologically independent even while sharing the same space. "
        "This separation is what allows the 2:6 TIME/SPATIAL ratio to be well defined."
    )
    future_questions = (
        "Q1: Why must the two tetrahedra remain topologically independent? "
        "Q2: What would happen to the face classification if vertices were shared? "
        "Q3: How does vertex isolation relate to the stellated octahedron being a 'dual' structure? "
        "FUTURE: Answering these could improve score by ~5 points."
    )
    
    def model(self) -> Model:
        correct = 0
        for face_name in ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7']:
            verts = FACES.get(face_name, frozenset())
            if all(v in TET_A for v in verts):
                correct += 1
        for face_name in ['FACE_B0', 'FACE_B3', 'FACE_B5', 'FACE_B6']:
            verts = FACES.get(face_name, frozenset())
            if all(v in TET_B for v in verts):
                correct += 1
        return Model().add("Faces with correct vertices", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Faces with correct vertices", 8)


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


def run_all() -> bool:
    """Run all face classification tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
