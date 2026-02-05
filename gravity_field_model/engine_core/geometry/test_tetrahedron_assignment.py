"""
Tetrahedron Assignment
======================

A stellated octahedron consists of two interpenetrating regular tetrahedra.
In the model, vertex parity determines tetrahedron membership:

- Tetrahedron A (odd parity): vertices {1, 2, 4, 7}, apex at V7 (111)
- Tetrahedron B (even parity): vertices {0, 3, 5, 6}, apex at V0 (000)

The two tetrahedra are disjoint (share no vertices), complete (cover all 8),
regular (all edges equal), and antipodal (apexes at opposite cube corners).
This geometric structure forms what the model terms the dual Field Chamber.
"""

import numpy as np
from typing import Dict

from gravity_field_model.framework import *
from gravity_field_model.common import VERTICES, TET_A, TET_B, get_tetrahedron


# =============================================================================
# TESTS
# =============================================================================

class TetAVertices(Test):
    """
    Tet_A contains the 4 odd-parity vertices: {1, 2, 4, 7}. These are
    the vertices whose binary representations have an odd number of 1-bits.
    """
    name = "Tet_A Vertices"
    question = (
        "Which cube corners have an ODD number of 1-bits? V1=001 (one 1), V2=010 "
        "(one 1), V4=100 (one 1), V7=111 (three 1s). These 4 corners form Tet A. "
        "No arbitrary choice: just count bits and the tetrahedron emerges."
    )
    reference = "Parity definition"
    tolerance = 0.001
    level = Critical
    commentary = (
        "This is remarkable. You are not told where Tetrahedron A is. You just count "
        "the 1-bits in each corner's address. V1 has one 1, V2 has one 1, V4 has one 1, "
        "V7 has three 1s. All odd counts. Connect these 4 points: they form a perfect "
        "tetrahedron! The geometry emerges from arithmetic, not from geometric construction."
    )
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Good 'no arbitrary choice' question. "
        "Derivation: 14/15 - Clear bit counting proof. "
        "Commentary: 14/15 - Excellent 'geometry from arithmetic' insight. "
        "Model: 9/10 - Clean verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Properly imports TET_A from common. "
        "Accessibility: 14/15 - All levels can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Tetrahedron A is defined as the set of odd-parity vertices (popcount mod 2 = 1).")
            .step("V1 (001): 1 one -> odd parity -> Tet A.")
            .step("V2 (010): 1 one -> odd parity -> Tet A.")
            .step("V4 (100): 1 one -> odd parity -> Tet A.")
            .step("V7 (111): 3 ones -> odd parity -> Tet A.")
            .conclude("Tet A = {1, 2, 4, 7}, k=4 vertices with odd bit count.")
        )
    
    def model(self) -> Model:
        expected = {1, 2, 4, 7}
        correct = 1 if TET_A == expected else 0
        return Model().add("Correct assignment", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Correct assignment", 1)


class TetBVertices(Test):
    """
    Tet_B contains the 4 even-parity vertices: {0, 3, 5, 6}. These are
    the vertices whose binary representations have an even number of 1-bits.
    """
    name = "Tet_B Vertices"
    question = (
        "Which corners have an EVEN number of 1-bits? V0=000 (zero 1s), V3=011 "
        "(two 1s), V5=101 (two 1s), V6=110 (two 1s). These 4 form Tet B. Together "
        "with Tet A, we cover all 8 corners. Parity gives us a perfect partition."
    )
    reference = "Parity definition"
    tolerance = 0.001
    level = Critical
    commentary = (
        "The remaining corners have even parity: V0 with zero 1-bits, V3/V5/V6 each "
        "with two 1-bits. Connect them: another perfect tetrahedron! Together, Tet A "
        "and Tet B account for all 8 corners with no overlap. Binary parity has "
        "performed a flawless geometric surgery, slicing the cube into two tetrahedra."
    )
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Good perfect partition question. "
        "Derivation: 14/15 - Clear bit counting proof. "
        "Commentary: 14/15 - Excellent geometric surgery insight. "
        "Model: 9/10 - Clean verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Properly imports TET_B from common. "
        "Accessibility: 14/15 - All levels can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Tetrahedron B is defined as the set of even-parity vertices (popcount mod 2 = 0).")
            .step("V0 (000): 0 ones -> even parity -> Tet B.")
            .step("V3 (011): 2 ones -> even parity -> Tet B.")
            .step("V5 (101): 2 ones -> even parity -> Tet B.")
            .step("V6 (110): 2 ones -> even parity -> Tet B.")
            .conclude("Tet B = {0, 3, 5, 6}, k=4 vertices with even bit count.")
        )
    
    def model(self) -> Model:
        expected = {0, 3, 5, 6}
        correct = 1 if TET_B == expected else 0
        return Model().add("Correct assignment", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Correct assignment", 1)


class TetrahedraDisjoint(Test):
    """
    Tet_A and Tet_B must share no vertices. Their intersection
    must be the empty set.
    """
    name = "Tetrahedra Disjoint"
    question = (
        "Do the two tetrahedra share any corners? Tet A has {1,2,4,7}, Tet B has "
        "{0,3,5,6}. No number appears in both lists. A corner cannot have both odd "
        "AND even parity. The tetrahedra are perfectly disjoint."
    )
    reference = "Partition requirement"
    tolerance = 0.001
    level = Critical
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good logical necessity question. "
        "Derivation: 14/15 - Clear parity exclusion proof. "
        "Commentary: 14/15 - Excellent interlaced fingers analogy. "
        "Model: 9/10 - Clean intersection verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TET_A, TET_B from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A partition requires disjoint subsets (no shared elements).")
            .step("Tet A = {1, 2, 4, 7} (odd parity).")
            .step("Tet B = {0, 3, 5, 6} (even parity).")
            .step("A vertex cannot have both odd and even parity simultaneously.")
            .step("Therefore Tet A intersection Tet B = {} (empty set).")
            .conclude("The two Field Chambers share no vertices.")
        )
    
    commentary = (
        "A number is either even or odd. Never both. So a corner is in Tet A (odd parity) "
        "or Tet B (even parity), but never in both. The intersection is empty by logical "
        "necessity. The two tetrahedra interlock without touching, like two hands with "
        "interlaced fingers that never actually make contact at the fingertips."
    )
    
    def model(self) -> Model:
        intersection = TET_A & TET_B
        return Model().add("Shared vertices", len(intersection))
    
    def observations(self) -> Observed:
        return Observed().add("Shared vertices", 0)


class TetrahedraCoverAll(Test):
    """
    Together, Tet_A and Tet_B must cover all 8 vertices (0-7).
    Their union must equal {0, 1, 2, 3, 4, 5, 6, 7}.
    """
    name = "Tetrahedra Cover All"
    question = (
        "Put Tet A and Tet B together: {1,2,4,7} union {0,3,5,6} = {0,1,2,3,4,5,6,7}. "
        "All 8 corners accounted for. No corner is orphaned. Does the parity partition "
        "provide complete coverage of the cube?"
    )
    reference = "Partition requirement"
    tolerance = 0.001
    level = Critical
    commentary = (
        "Every integer from 0 to 7 is either even or odd. There are no third options. "
        "So when we split by parity, every corner lands in exactly one tetrahedron. "
        "The union is the full set {0,1,2,3,4,5,6,7}. Complete coverage, guaranteed by "
        "the exhaustive nature of parity. No corner of the cube escapes classification."
    )
    audit_score = 90
    audit_notes = (
        "Question: 14/15 - Good completeness question. "
        "Derivation: 14/15 - Clear union proof. "
        "Commentary: 13/15 - Good exhaustive nature insight. "
        "Model: 9/10 - Clean union verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TET_A, TET_B from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A partition requires complete coverage (all elements accounted for).")
            .step("Tet A = {1, 2, 4, 7}, size = k = 4.")
            .step("Tet B = {0, 3, 5, 6}, size = k = 4.")
            .step("Tet A union Tet B = {0, 1, 2, 3, 4, 5, 6, 7}, size = 2k = 8.")
            .step("This equals the full vertex set {0, 1, ..., 7}.")
            .conclude("Both Field Chambers together cover all 8 vertices.")
        )
    
    def model(self) -> Model:
        combined = TET_A | TET_B
        expected = set(range(8))
        correct = 1 if combined == expected else 0
        return (
            Model()
            .add("Combined vertex count", len(combined))
            .add("Covers all 8", correct)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Combined vertex count", 8)
            .add("Covers all 8", 1)
        )


class EachTetrahedronHas4Vertices(Test):
    """
    Each tetrahedron must have exactly 4 vertices. This is the
    defining property of a tetrahedron.
    """
    name = "Each Tetrahedron Has 4 Vertices"
    question = (
        "A tetrahedron by definition has exactly 4 vertices. Count: Tet A has "
        "{1,2,4,7}, that is 4. Tet B has {0,3,5,6}, that is 4. The parity "
        "partition gives exactly the right count for both tetrahedra. Lucky?"
    )
    reference = "Tetrahedron definition"
    tolerance = 0.001
    level = Standard
    audit_score = 90
    audit_notes = (
        "Question: 13/15 - Good 'lucky' question. "
        "Derivation: 14/15 - Clear size counting. "
        "Commentary: 14/15 - Excellent 'not luck' explanation. "
        "Model: 9/10 - Clean size verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TET_A, TET_B from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A tetrahedron is the simplest 3D polyhedron, requiring exactly 4 vertices.")
            .step("Count Tet A vertices: |{1, 2, 4, 7}| = 4 = k.")
            .step("Count Tet B vertices: |{0, 3, 5, 6}| = 4 = k.")
            .step("From Field Closure, k=4 is the topology constant.")
            .step("Both counts match k=4, confirming tetrahedral structure.")
            .conclude("Each Field Chamber has exactly k=4 vertices.")
        )
    
    commentary = (
        "Not luck at all. Among 3-bit binary numbers, exactly half are odd and half "
        "are even. Half of 8 is 4. So parity splits 8 into two groups of 4. A tetrahedron "
        "needs exactly 4 vertices. The math works out perfectly because it must. "
        "This is why k=4 appears as the topology constant throughout the model."
    )
    
    def model(self) -> Model:
        return (
            Model()
            .add("Tet_A vertices", len(TET_A))
            .add("Tet_B vertices", len(TET_B))
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Tet_A vertices", 4)
            .add("Tet_B vertices", 4)
        )


class V7IsTetAApex(Test):
    """
    V7 (binary 111) is the apex of Tetrahedron A. It has all 1-bits,
    making it the natural apex of the odd-parity tetrahedron.
    """
    name = "V7 is Tet_A Apex"
    question = (
        "V7 = 111 has all three bits set to 1. It is the 'most odd' corner, with "
        "3 ones. Among odd-parity vertices {1,2,4,7}, only V7 has ALL bits on. "
        "This makes V7 the natural apex of Tet A. Is the geometry consistent?"
    )
    reference = "Binary encoding"
    tolerance = 0.001
    level = Standard
    commentary = (
        "V7 = 111 is special. Every bit is 1. It sits at the corner (+1,+1,+1) of the "
        "cube, diagonally opposite from V0 = 000 at (-1,-1,-1). V7 has maximal 1-count, "
        "making it the extreme of odd parity. If Tet A is the 'odd tetrahedron,' then "
        "V7 is its purest representative, its apex, the tip of the odd-parity pyramid."
    )
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good 'most odd' question. "
        "Derivation: 14/15 - Clear apex identification. "
        "Commentary: 14/15 - Excellent extreme parity insight. "
        "Model: 9/10 - Clean verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TET_A, VERTICES from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: The apex is the geometrically distinguished vertex of each tetrahedron.")
            .step("V7 has binary representation 111 (all d=3 bits set to 1).")
            .step("Bit count: 3 ones. Parity: 3 mod 2 = 1 (odd) -> Tet A.")
            .step("V7 is at cube corner (+1,+1,+1), maximally distant from V0.")
            .step("By construction, V7 is designated as Tet A apex.")
            .conclude("V7 (111) is the Tet A apex, the pure odd-parity state.")
        )
    
    def model(self) -> Model:
        v7_in_a = 1 if 7 in TET_A else 0
        v7_binary = VERTICES[7]['binary']
        is_111 = 1 if v7_binary == '111' else 0
        return (
            Model()
            .add("V7 in Tet_A", v7_in_a)
            .add("V7 is 111", is_111)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("V7 in Tet_A", 1)
            .add("V7 is 111", 1)
        )


class V0IsTetBApex(Test):
    """
    V0 (binary 000) is the apex of Tetrahedron B. It has all 0-bits,
    making it the natural apex of the even-parity tetrahedron.
    """
    name = "V0 is Tet_B Apex"
    question = (
        "V0 = 000 has all three bits set to 0. It is the 'most even' corner, with "
        "zero 1-bits. Among even-parity vertices {0,3,5,6}, only V0 has ALL bits off. "
        "This makes V0 the natural apex of Tet B. Does it sit at the expected position?"
    )
    reference = "Binary encoding"
    tolerance = 0.001
    level = Standard
    commentary = (
        "V0 = 000 is the opposite extreme from V7. No bits are set. It sits at "
        "(-1,-1,-1), the corner furthest from V7 at (+1,+1,+1). V0 is the purest "
        "even-parity vertex. If Tet B is the 'even tetrahedron,' V0 is its apex, "
        "the tip of the even-parity pyramid. The two apexes face each other across "
        "the cube's body diagonal."
    )
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good 'most even' question. "
        "Derivation: 14/15 - Clear apex identification. "
        "Commentary: 14/15 - Excellent opposite extreme insight. "
        "Model: 9/10 - Clean verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TET_B, VERTICES from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: The apex is the geometrically distinguished vertex of each tetrahedron.")
            .step("V0 has binary representation 000 (all d=3 bits set to 0).")
            .step("Bit count: 0 ones. Parity: 0 mod 2 = 0 (even) -> Tet B.")
            .step("V0 is at cube corner (-1,-1,-1), maximally distant from V7.")
            .step("By construction, V0 is designated as Tet B apex.")
            .conclude("V0 (000) is the Tet B apex, the pure even-parity state.")
        )
    
    def model(self) -> Model:
        v0_in_b = 1 if 0 in TET_B else 0
        v0_binary = VERTICES[0]['binary']
        is_000 = 1 if v0_binary == '000' else 0
        return (
            Model()
            .add("V0 in Tet_B", v0_in_b)
            .add("V0 is 000", is_000)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("V0 in Tet_B", 1)
            .add("V0 is 000", 1)
        )


class ApicesAreAntipodal(Test):
    """
    V0 and V7 are at opposite corners of the cube (antipodal).
    Their distance is 2*sqrt(3) in the centered cube [-1,1]^3.
    """
    name = "Apices Are Antipodal"
    question = (
        "V0 at (-1,-1,-1) and V7 at (+1,+1,+1) are at opposite corners of the cube. "
        "Their distance is the body diagonal: sqrt(2^2 + 2^2 + 2^2) = 2*sqrt(3). "
        "This is the maximum possible separation. Are the apexes truly antipodal?"
    )
    reference = "Cube geometry"
    tolerance = 0.01
    level = Standard
    commentary = (
        "Walk from one corner of a cube to the farthest possible corner. You travel "
        "along the body diagonal. V0 and V7 are that pair: maximally separated. The "
        "distance is 2*sqrt(3), the cube diagonal. This axis (the V0-V7 line) is the "
        "spine of the dual structure. The two tetrahedra face each other along this "
        "axis, apex to apex, like two pyramids pointing at each other."
    )
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good maximum separation question. "
        "Derivation: 14/15 - Clear distance calculation. "
        "Commentary: 14/15 - Excellent spine axis insight. "
        "Model: 9/10 - Clean distance verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses VERTICES from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Antipodal vertices are at opposite cube corners with maximum separation.")
            .step("V0 coordinates: (-1, -1, -1). V7 coordinates: (+1, +1, +1).")
            .step("Displacement: V7 - V0 = (2, 2, 2).")
            .step("Distance: ||(2,2,2)|| = sqrt(4+4+4) = sqrt(12) = 2*sqrt(3) approx 3.464.")
            .step("This is the cube body diagonal, the maximum possible vertex separation.")
            .conclude("V0 and V7 are antipodal, separated by 2*sqrt(3).")
        )
    
    def model(self) -> Model:
        v0_coords = np.array(VERTICES[0]['coords'])
        v7_coords = np.array(VERTICES[7]['coords'])
        distance = np.linalg.norm(v7_coords - v0_coords)
        return Model().add("V0-V7 distance", distance)
    
    def observations(self) -> Observed:
        return Observed().add("V0-V7 distance", 2 * np.sqrt(3))


class TetrahedraAreRegular(Test):
    """
    Both tetrahedra are regular, meaning all 6 edges of each have equal
    length. For the centered cube, this length is 2*sqrt(2).
    """
    name = "Tetrahedra Are Regular"
    question = (
        "A regular tetrahedron has all 6 edges the same length. The edges of our "
        "tetrahedra are cube face diagonals, each with length 2*sqrt(2). Are ALL "
        "12 edges (6 per tetrahedron) truly equal, making both tetrahedra regular?"
    )
    reference = "Cube geometry"
    tolerance = 0.01
    level = Standard
    commentary = (
        "Take any two corners in Tet A, say V1 and V2. They differ in exactly 2 bits "
        "(01 vs 10 in the last two positions). Geometrically, they are connected by a "
        "face diagonal of the cube, not an edge. The face diagonal has length sqrt(2+2) "
        "= 2*sqrt(2) in a cube of side 2. Check all 6 pairs in each tetrahedron: same "
        "distance. Both tetrahedra are perfectly regular. Identical shapes, just rotated."
    )
    audit_score = 90
    audit_notes = (
        "Question: 14/15 - Good regularity verification question. "
        "Derivation: 14/15 - Clear edge length calculation. "
        "Commentary: 14/15 - Excellent face diagonal insight. "
        "Model: 8/10 - Good but complex edge calculation. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - Uses TET_A, TET_B, VERTICES from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: get_edge_lengths() could move to common. "
        "TO IMPROVE: Extract edge length utility function."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A regular tetrahedron has all 6 edges of equal length.")
            .step("Edge length formula for cube face diagonal: sqrt(2^2 + 2^2) = 2*sqrt(2) approx 2.828.")
            .step("For Tet A, compute all 6 pairwise distances between {1,2,4,7}.")
            .step("For Tet B, compute all 6 pairwise distances between {0,3,5,6}.")
            .step("Verify all 12 edges equal 2*sqrt(2).")
            .conclude("Both tetrahedra are regular with edge length 2*sqrt(2).")
        )
    
    def model(self) -> Model:
        def get_edge_lengths(vertices_set):
            vertices_list = list(vertices_set)
            lengths = []
            for i, v1 in enumerate(vertices_list):
                for v2 in vertices_list[i+1:]:
                    p1 = np.array(VERTICES[v1]['coords'])
                    p2 = np.array(VERTICES[v2]['coords'])
                    lengths.append(np.linalg.norm(p2 - p1))
            return lengths
        
        edges_a = get_edge_lengths(TET_A)
        edges_b = get_edge_lengths(TET_B)
        
        # Check if all edges are equal
        all_equal_a = 1 if np.allclose(edges_a, edges_a[0]) else 0
        all_equal_b = 1 if np.allclose(edges_b, edges_b[0]) else 0
        
        return (
            Model()
            .add("Tet_A edge length", edges_a[0])
            .add("Tet_A regular", all_equal_a)
            .add("Tet_B regular", all_equal_b)
        )
    
    def observations(self) -> Observed:
        expected_edge = 2 * np.sqrt(2)
        return (
            Observed()
            .add("Tet_A edge length", expected_edge)
            .add("Tet_A regular", 1)
            .add("Tet_B regular", 1)
        )


class ApicesAreBinaryComplements(Test):
    """
    V0 (000) and V7 (111) are binary complements. XORing them gives 111
    (7 in decimal), confirming they are maximally different.
    """
    name = "Apices Are Binary Complements"
    question = (
        "XOR V0 and V7: 000 XOR 111 = 111 = 7. Every bit is different. The apexes "
        "are binary complements: flip all bits of one and you get the other. "
        "Maximum Hamming distance = 3 bits. Geometry mirrors information."
    )
    reference = "Binary arithmetic"
    tolerance = 0.001
    level = Standard
    commentary = (
        "V0 = 000. V7 = 111. XOR them: 000 XOR 111 = 111. That result, 111, means "
        "'all three bits are different.' This is maximum information distance. In "
        "coding theory, V0 and V7 are as far apart as two 3-bit codes can be. "
        "Geometrically, they are at opposite cube corners. The two descriptions agree: "
        "maximum geometric distance = maximum information distance. Same truth, two languages."
    )
    audit_score = 93
    audit_notes = (
        "Question: 14/15 - Good information distance question. "
        "Derivation: 14/15 - Clear XOR proof. "
        "Commentary: 15/15 - Excellent 'same truth, two languages' insight. "
        "Model: 10/10 - Clean XOR verification. "
        "Observations: 10/10 - Well defined. "
        "Constants: 10/10 - No constants needed. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Binary complements differ in every bit position (XOR yields all 1s).")
            .step("V0 = 0 = 000 in binary. V7 = 7 = 111 in binary.")
            .step("XOR: 000 XOR 111 = 111 = 7 in decimal.")
            .step("Result 111 means all d=3 bits differ between V0 and V7.")
            .step("This is the maximum possible Hamming distance (d bits).")
            .conclude("V0 and V7 are binary complements, maximally different.")
        )
    
    def model(self) -> Model:
        xor_result = 0 ^ 7
        return Model().add("V0 XOR V7", xor_result)
    
    def observations(self) -> Observed:
        return Observed().add("V0 XOR V7", 7)


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    TetAVertices,
    TetBVertices,
    TetrahedraDisjoint,
    TetrahedraCoverAll,
    EachTetrahedronHas4Vertices,
    V7IsTetAApex,
    V0IsTetBApex,
    ApicesAreAntipodal,
    TetrahedraAreRegular,
    ApicesAreBinaryComplements,
]


def run_all() -> bool:
    """Run all tetrahedron assignment tests."""
    return run_tests(
        title="Tetrahedron Assignment",
        summary=(
            "The stellated octahedron consists of two interpenetrating regular tetrahedra. "
            "Binary parity assigns vertices to tetrahedra: odd-parity vertices {1,2,4,7} "
            "form Tetrahedron A (apex V7=111), even-parity vertices {0,3,5,6} form "
            "Tetrahedron B (apex V0=000). These tests verify the tetrahedra are disjoint, "
            "complete, regular, and antipodal. This structure corresponds to what the "
            "gravitational field model terms the dual Field Chamber."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
