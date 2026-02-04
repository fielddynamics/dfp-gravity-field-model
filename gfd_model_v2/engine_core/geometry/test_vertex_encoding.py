"""
Binary Vertex Encoding
======================

The stellated octahedron (dual Field Chamber) has 8 vertices, each uniquely
addressable with a 3-bit binary index (0-7). The parity of each vertex's
binary representation naturally partitions the vertices into two disjoint
sets of 4, corresponding exactly to the vertices of each tetrahedron.

This mathematical property arises from binary arithmetic, not physical
assumption. That parity alone determines tetrahedron membership suggests
the dual tetrahedron structure may have information-theoretic significance.
"""

from typing import Dict

from gfd_model_v2.framework import *
from gfd_model_v2.common import VERTICES, TET_A, TET_B, get_vertex_binary, get_vertex_parity, get_tetrahedron


# =============================================================================
# TESTS
# =============================================================================

class VerticesAre0To7(Test):
    """
    Vertices must be indexed 0-7, matching the 8 possible 3-bit
    binary values. This is the foundation of the triad encoding.
    """
    name = "Vertices 0-7"
    question = (
        "Eight corners need 8 labels. The simplest choice: 0, 1, 2, 3, 4, 5, 6, 7. "
        "This is exactly all 3-bit binary numbers (000 to 111). Does every corner "
        "get a unique label, and does every 3-bit code get used exactly once?"
    )
    reference = "3-bit encoding (2^3 = 8)"
    tolerance = 0.001
    level = Critical
    commentary = (
        "There is something perfect here. We have 8 corners and need to label them. "
        "3 bits give 2^3 = 8 possibilities: 0, 1, 2, ..., 7. A bijection. Each corner "
        "gets one label, each label gets one corner. The labeling is not arbitrary "
        "decoration; it IS the geometry. The corner labeled 5 (binary 101) is at position "
        "(+1, -1, +1). The bits ARE the coordinates. Information and space merge."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: With d=k-1=3 spatial dimensions, each vertex requires d=3 bits for unique addressing.")
            .step("Number of unique 3-bit patterns: 2^3 = 8.")
            .step("Patterns range from 000 (=0) to 111 (=7).")
            .step("Vertex count = 2k = 2*4 = 8, matching pattern count.")
            .step("Bijective mapping: vertex index i <-> binary pattern format(i, '03b').")
            .conclude("Indices {0,1,2,3,4,5,6,7} exhaust all d=3 bit patterns.")
        )
    
    def model(self) -> Model:
        indices = set(VERTICES.keys())
        correct = 1 if indices == {0, 1, 2, 3, 4, 5, 6, 7} else 0
        return (
            Model()
            .add("Vertex count", len(indices))
            .add("Indices correct", correct)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Vertex count", 8)
            .add("Indices correct", 1)
        )


class BinaryRepresentation3Bits(Test):
    """
    Each vertex must have a valid 3-bit binary representation
    (e.g., V5 = "101"). This ensures the encoding is well-formed.
    """
    name = "Binary Representation"
    question = (
        "Each vertex should have a 3-character binary string: exactly 3 bits, each "
        "either '0' or '1'. V5 should be '101', not '5' or '0101'. Is every vertex's "
        "stored binary representation a valid 3-bit string?"
    )
    reference = "Binary encoding"
    tolerance = 0.001
    level = Standard
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Valid triad encoding requires exactly d=3 binary digits per vertex.")
            .step("For each vertex v in {0,1,...,7}, retrieve stored binary string.")
            .step("Verify string length = 3 (d bits).")
            .step("Verify each character is '0' or '1' (valid binary).")
            .step("Count vertices passing both checks.")
            .conclude("All 8 vertices have valid 3-bit triads.")
        )
    
    commentary = (
        "This is a basic sanity check. We expect V0 = '000', V1 = '001', up to V7 = '111'. "
        "Each string should be exactly 3 characters long, using only '0' and '1'. "
        "If this fails, something is badly wrong with the data. We are checking that "
        "the encoding is well-formed before using it for anything else."
    )
    
    def model(self) -> Model:
        valid = 0
        for v in range(8):
            binary = VERTICES[v]['binary']
            if len(binary) == 3 and all(b in '01' for b in binary):
                valid += 1
        return Model().add("Valid binary strings", valid)
    
    def observations(self) -> Observed:
        return Observed().add("Valid binary strings", 8)


class BinaryMatchesIndex(Test):
    """
    The binary representation must equal the vertex index in binary
    (e.g., V5 = "101" = 5 in decimal). This is the consistency check.
    """
    name = "Binary Matches Index"
    question = (
        "V5 is stored with binary string '101'. But 101 in binary IS 5 in decimal. "
        "This should be true for all vertices: the stored binary should equal the "
        "calculated binary of the index. Is there perfect consistency?"
    )
    reference = "Decimal-binary identity"
    tolerance = 0.001
    level = Standard
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Bijective encoding requires stored triad to match calculated triad.")
            .step("For each vertex v, retrieve stored binary: VERTICES[v]['binary'].")
            .step("Calculate expected binary: format(v, '03b').")
            .step("Compare: stored == calculated.")
            .step("Example: V5 stored='101', calculated=format(5,'03b')='101'. Match.")
            .conclude("All 8 vertices have consistent triad encoding.")
        )
    
    commentary = (
        "This test checks that we have not made a typo anywhere. V3 should store '011' "
        "because 3 in decimal = 011 in 3-bit binary. If someone accidentally stored '110', "
        "this test catches it. The index IS the number, and the binary IS that number "
        "in base 2. They must match by definition."
    )
    
    def model(self) -> Model:
        matching = 0
        for v in range(8):
            stored = VERTICES[v]['binary']
            calculated = format(v, '03b')
            if stored == calculated:
                matching += 1
        return Model().add("Matching encodings", matching)
    
    def observations(self) -> Observed:
        return Observed().add("Matching encodings", 8)


class ParityCalculation(Test):
    """
    Parity is computed as (number of 1-bits) mod 2. This must match
    the expected values: even for {0,3,5,6}, odd for {1,2,4,7}.
    """
    name = "Parity Calculation"
    question = (
        "Count the 1-bits: V0=000 has 0 ones (even), V7=111 has 3 ones (odd). "
        "Parity = count mod 2. This single bit classifies each vertex. Does our "
        "parity function give the correct answer for all 8 vertices?"
    )
    reference = "Parity definition"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Parity is the simplest classifier of a binary number: just count the 1s and "
        "report whether the count is even or odd. V0 = 000 has 0 ones, which is even. "
        "V3 = 011 has 2 ones, also even. V7 = 111 has 3 ones, which is odd. This one-bit "
        "answer (even=0, odd=1) will determine which tetrahedron each vertex belongs to."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Parity of vertex v = (number of 1-bits in binary(v)) mod 2.")
            .step("Count 1-bits for each vertex: 0->0, 1->1, 2->1, 3->2, 4->1, 5->2, 6->2, 7->3.")
            .step("Apply mod 2: 0->0, 1->1, 2->1, 3->0, 4->1, 5->0, 6->0, 7->1.")
            .step("Even parity (0): {0,3,5,6}. Odd parity (1): {1,2,4,7}.")
            .step("Each set has exactly k=4 vertices.")
            .conclude("Parity partitions 8 vertices into two disjoint sets of 4.")
        )
    
    def model(self) -> Model:
        expected = {0: 0, 1: 1, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1}
        correct = sum(1 for v in range(8) if get_vertex_parity(v) == expected[v])
        return Model().add("Correct parities", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Correct parities", 8)


class EvenParityIsTetB(Test):
    """
    Even parity vertices {0,3,5,6} must belong to Tetrahedron B.
    This tetrahedron has its apex at V0 (binary 000, all zeros).
    """
    name = "Even Parity = Tet B"
    question = (
        "Gather all vertices with an even number of 1-bits: V0 (zero 1s), V3 (two 1s), "
        "V5 (two 1s), V6 (two 1s). These form Tet B. Connect them and you get a "
        "tetrahedron. Is parity really a geometric property in disguise?"
    )
    reference = "Parity-tetrahedron rule"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Even parity means 0 or 2 ones in the binary code. The vertices 0, 3, 5, 6 "
        "satisfy this. Look at them in 3D space: they form a perfect tetrahedron! "
        "V0 = 000 is the apex with minimal 1-count. The others have exactly 2 ones each. "
        "Pure number theory (counting bits) has produced a geometric object (a tetrahedron)."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Tetrahedron B is defined as the set of even-parity vertices.")
            .step("Collect vertices with parity = 0: {v | popcount(v) mod 2 = 0}.")
            .step("Result: {0, 3, 5, 6} (vertices with 0 or 2 ones).")
            .step("V0 (000) has 0 ones (minimum), making it the pure-state apex.")
            .step("These 4 vertices form a valid tetrahedron in the cube geometry.")
            .conclude("Even parity vertices {0,3,5,6} = Tet B, with apex V0.")
        )
    
    def model(self) -> Model:
        even = {v for v in range(8) if get_vertex_parity(v) == 0}
        expected = {0, 3, 5, 6}
        correct = 1 if even == expected == TET_B else 0
        return Model().add("Tet_B assignment correct", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Tet_B assignment correct", 1)


class OddParityIsTetA(Test):
    """
    Odd parity vertices {1,2,4,7} must belong to Tetrahedron A.
    This tetrahedron has its apex at V7 (binary 111, all ones).
    """
    name = "Odd Parity = Tet A"
    question = (
        "Gather all vertices with an odd number of 1-bits: V1 (one 1), V2 (one 1), "
        "V4 (one 1), V7 (three 1s). These form Tet A. Connect them and you get the "
        "other tetrahedron. Parity splits the cube into two perfect tetrahedra?"
    )
    reference = "Parity-tetrahedron rule"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Odd parity means 1 or 3 ones. Vertices 1, 2, 4, 7 qualify. In 3D, these four "
        "points form another perfect tetrahedron! V7 = 111 with all bits on is the apex, "
        "the most extreme odd-parity vertex. The others (1, 2, 4) each have exactly one "
        "bit on. Arithmetic parity has carved two geometric shapes from a cube."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Tetrahedron A is defined as the set of odd-parity vertices.")
            .step("Collect vertices with parity = 1: {v | popcount(v) mod 2 = 1}.")
            .step("Result: {1, 2, 4, 7} (vertices with 1 or 3 ones).")
            .step("V7 (111) has 3 ones (maximum = d), making it the pure-state apex.")
            .step("These 4 vertices form a valid tetrahedron in the cube geometry.")
            .conclude("Odd parity vertices {1,2,4,7} = Tet A, with apex V7.")
        )
    
    def model(self) -> Model:
        odd = {v for v in range(8) if get_vertex_parity(v) == 1}
        expected = {1, 2, 4, 7}
        correct = 1 if odd == expected == TET_A else 0
        return Model().add("Tet_A assignment correct", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Tet_A assignment correct", 1)


class TetrahedronFunction(Test):
    """
    The get_tetrahedron() function must return 'A' or 'B' correctly
    for all 8 vertices based on their parity.
    """
    name = "Tetrahedron Function"
    question = (
        "We have a function get_tetrahedron(v) that should return 'A' or 'B'. "
        "It should say 'A' for odd-parity vertices (1,2,4,7) and 'B' for even-parity "
        "(0,3,5,6). Does the function agree with the parity rule for all 8 vertices?"
    )
    reference = "Function definition"
    tolerance = 0.001
    level = Standard
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: get_tetrahedron() must implement the parity-based Field Chamber assignment.")
            .step("For each vertex in Tet A {1,2,4,7}, verify get_tetrahedron(v) == 'A'.")
            .step("For each vertex in Tet B {0,3,5,6}, verify get_tetrahedron(v) == 'B'.")
            .step("Count correct assignments.")
            .step("All 8 assignments must be correct.")
            .conclude("Function correctly implements parity-based tetrahedron assignment.")
        )
    
    commentary = (
        "This tests the code, not the math. The math says parity determines tetrahedron. "
        "The code should implement this. Call get_tetrahedron(5): it should return 'B' "
        "because V5 = 101 has 2 ones (even parity). All 8 calls must return the "
        "correct letter. If not, there is a bug."
    )
    
    def model(self) -> Model:
        correct = 0
        for v in TET_A:
            if get_tetrahedron(v) == 'A':
                correct += 1
        for v in TET_B:
            if get_tetrahedron(v) == 'B':
                correct += 1
        return Model().add("Correct assignments", correct)
    
    def observations(self) -> Observed:
        return Observed().add("Correct assignments", 8)


class TetrahedronPartition(Test):
    """
    Parity must create a valid partition: two disjoint sets of
    exactly 4 vertices each that together cover all 8 vertices.
    """
    name = "Tetrahedron Partition"
    question = (
        "A partition means: two sets with no overlap, and together they cover "
        "everything. Tet A and Tet B must be disjoint (no shared vertex) and "
        "complete (union = all 8). Does the parity rule create a valid partition?"
    )
    reference = "Partition requirement"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Every integer is either even or odd, never both, never neither. So when we "
        "split 0-7 by parity, we get a perfect partition: two disjoint sets that "
        "together account for everyone. {0,3,5,6} union {1,2,4,7} = {0,1,2,3,4,5,6,7}. "
        "Intersection is empty. This is guaranteed by the nature of parity."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: A valid partition requires disjoint sets with complete coverage.")
            .step("Even parity set: {0,3,5,6}, size = 4.")
            .step("Odd parity set: {1,2,4,7}, size = 4.")
            .step("Check disjoint: {0,3,5,6} intersection {1,2,4,7} = {} (empty).")
            .step("Check complete: {0,3,5,6} union {1,2,4,7} = {0,1,2,3,4,5,6,7} (all 8).")
            .conclude("Parity creates a valid 4+4 partition of the 8 vertices.")
        )
    
    def model(self) -> Model:
        even = {v for v in range(8) if get_vertex_parity(v) == 0}
        odd = {v for v in range(8) if get_vertex_parity(v) == 1}
        
        disjoint = 1 if len(even & odd) == 0 else 0
        complete = 1 if (even | odd) == set(range(8)) else 0
        correct_size = 1 if len(even) == 4 and len(odd) == 4 else 0
        
        return (
            Model()
            .add("Sets disjoint", disjoint)
            .add("Sets complete", complete)
            .add("Each set has 4", correct_size)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Sets disjoint", 1)
            .add("Sets complete", 1)
            .add("Each set has 4", 1)
        )


class ApexesCorrect(Test):
    """
    V7 (111, all 1s, odd parity) must be the Tet_A apex.
    V0 (000, all 0s, even parity) must be the Tet_B apex.
    These are the "pure" vertices of each tetrahedron.
    """
    name = "Apexes Correct"
    question = (
        "V7 = 111 (all bits on) should be Tet A's apex. V0 = 000 (all bits off) "
        "should be Tet B's apex. These are the 'purest' states of each parity class. "
        "Are the apexes assigned correctly to their respective tetrahedra?"
    )
    reference = "Apex definition"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Among odd-parity vertices, V7 is extreme: it has 3 ones, the maximum possible. "
        "Among even-parity vertices, V0 is extreme: it has 0 ones, the minimum. These "
        "'pure' states sit at opposite corners of the cube and serve as apexes for their "
        "tetrahedra. The two apexes are binary complements and geometric antipodes."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Apex vertices are pure binary states at extremes of the 1-bit count spectrum.")
            .step("V7 (111) has d=3 ones (maximum). Parity: 3 mod 2 = 1 (odd) -> Tet A.")
            .step("V0 (000) has 0 ones (minimum). Parity: 0 mod 2 = 0 (even) -> Tet B.")
            .step("V7 and V0 are maximally separated: all bits differ.")
            .step("These pure states anchor their respective tetrahedra as apexes.")
            .conclude("V7 is Tet A apex (all 1s), V0 is Tet B apex (all 0s).")
        )
    
    def model(self) -> Model:
        v7_correct = 1 if 7 in TET_A else 0
        v0_correct = 1 if 0 in TET_B else 0
        return (
            Model()
            .add("V7 in Tet_A", v7_correct)
            .add("V0 in Tet_B", v0_correct)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("V7 in Tet_A", 1)
            .add("V0 in Tet_B", 1)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    VerticesAre0To7,
    BinaryRepresentation3Bits,
    BinaryMatchesIndex,
    ParityCalculation,
    EvenParityIsTetB,
    OddParityIsTetA,
    TetrahedronFunction,
    TetrahedronPartition,
    ApexesCorrect,
]


def run_all() -> bool:
    """Run all vertex encoding tests."""
    return run_tests(
        title="Binary Vertex Encoding",
        summary=(
            "The 8 vertices of a stellated octahedron can be indexed 0-7, each with a "
            "unique 3-bit binary address. Binary parity (count of 1-bits mod 2) naturally "
            "partitions these vertices into two sets of 4: even parity {0,3,5,6} and odd "
            "parity {1,2,4,7}. These sets correspond exactly to the vertices of each "
            "constituent tetrahedron. This partition emerges from binary arithmetic alone, "
            "suggesting the dual tetrahedron structure encodes information at a fundamental level."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
