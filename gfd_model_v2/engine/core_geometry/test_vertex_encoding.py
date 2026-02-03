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

import sys
import os
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from gfd_model_v2.common import VERTICES, TET_A, TET_B, get_vertex_binary, get_vertex_parity, get_tetrahedron


# =============================================================================
# TESTS
# =============================================================================

class VerticesAre0To7(GFDTest):
    """
    Vertices must be indexed 0-7, matching the 8 possible 3-bit
    binary values. This is the foundation of the triad encoding.
    """
    name = "Vertices 0-7"
    question = "Do the 2k=8 Field Chamber vertices map to indices 0-7, corresponding to all 2^d = 2^3 = 8 possible d-bit binary states?"
    reference_source = "3-bit encoding (2^3 = 8)"
    tolerance = 0.001
    derivation = (
        "PREMISE: With d=k-1=3 spatial dimensions, each vertex requires d=3 bits for unique addressing. "
        "STEP 1: Number of unique 3-bit patterns: 2^3 = 8. "
        "STEP 2: Patterns range from 000 (=0) to 111 (=7). "
        "STEP 3: Vertex count = 2k = 2*4 = 8, matching pattern count. "
        "STEP 4: Bijective mapping: vertex index i <-> binary pattern format(i, '03b'). "
        "OUTPUT: Indices {0,1,2,3,4,5,6,7} exhaust all d=3 bit patterns."
    )
    commentary = (
        "The 0-7 vertex indexing maps directly to 3-bit binary states, enabling "
        "information-theoretic interpretation of Field Chamber traversal. Each "
        "vertex represents a unique 3-bit spatial address."
    )
    
    def model(self) -> Dict[str, float]:
        indices = set(VERTICES.keys())
        correct = 1 if indices == {0, 1, 2, 3, 4, 5, 6, 7} else 0
        return {
            "Vertex count": len(indices),
            "Indices correct": correct,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Vertex count": 8,
            "Indices correct": 1,
        }


class BinaryRepresentation3Bits(GFDTest):
    """
    Each vertex must have a valid 3-bit binary representation
    (e.g., V5 = "101"). This ensures the encoding is well-formed.
    """
    name = "Binary Representation"
    question = "Does each vertex have a valid d=3 bit binary string (triad), ensuring well-formed spatial addressing?"
    reference_source = "Binary encoding"
    tolerance = 0.001
    derivation = (
        "PREMISE: Valid triad encoding requires exactly d=3 binary digits per vertex. "
        "STEP 1: For each vertex v in {0,1,...,7}, retrieve stored binary string. "
        "STEP 2: Verify string length = 3 (d bits). "
        "STEP 3: Verify each character is '0' or '1' (valid binary). "
        "STEP 4: Count vertices passing both checks. "
        "OUTPUT: All 8 vertices have valid 3-bit triads."
    )
    commentary = None  # Data integrity verification
    
    def model(self) -> Dict[str, float]:
        valid = 0
        for v in range(8):
            binary = VERTICES[v]['binary']
            if len(binary) == 3 and all(b in '01' for b in binary):
                valid += 1
        return {"Valid binary strings": valid}
    
    def observations(self) -> Dict[str, float]:
        return {"Valid binary strings": 8}


class BinaryMatchesIndex(GFDTest):
    """
    The binary representation must equal the vertex index in binary
    (e.g., V5 = "101" = 5 in decimal). This is the consistency check.
    """
    name = "Binary Matches Index"
    question = "Does each stored binary string equal the calculated binary representation of its vertex index?"
    reference_source = "Decimal-binary identity"
    tolerance = 0.001
    derivation = (
        "PREMISE: Bijective encoding requires stored triad to match calculated triad. "
        "STEP 1: For each vertex v, retrieve stored binary: VERTICES[v]['binary']. "
        "STEP 2: Calculate expected binary: format(v, '03b'). "
        "STEP 3: Compare: stored == calculated. "
        "STEP 4: Example: V5 stored='101', calculated=format(5,'03b')='101'. Match. "
        "OUTPUT: All 8 vertices have consistent triad encoding."
    )
    commentary = None  # Encoding consistency verification
    
    def model(self) -> Dict[str, float]:
        matching = 0
        for v in range(8):
            stored = VERTICES[v]['binary']
            calculated = format(v, '03b')
            if stored == calculated:
                matching += 1
        return {"Matching encodings": matching}
    
    def observations(self) -> Dict[str, float]:
        return {"Matching encodings": 8}


class ParityCalculation(GFDTest):
    """
    Parity is computed as (number of 1-bits) mod 2. This must match
    the expected values: even for {0,3,5,6}, odd for {1,2,4,7}.
    """
    name = "Parity Calculation"
    question = "Is parity (popcount mod 2) calculated correctly, partitioning vertices into even {0,3,5,6} and odd {1,2,4,7}?"
    reference_source = "Parity definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: Parity of vertex v = (number of 1-bits in binary(v)) mod 2. "
        "STEP 1: Count 1-bits for each vertex: 0->0, 1->1, 2->1, 3->2, 4->1, 5->2, 6->2, 7->3. "
        "STEP 2: Apply mod 2: 0->0, 1->1, 2->1, 3->0, 4->1, 5->0, 6->0, 7->1. "
        "STEP 3: Even parity (0): {0,3,5,6}. Odd parity (1): {1,2,4,7}. "
        "STEP 4: Each set has exactly k=4 vertices. "
        "OUTPUT: Parity partitions 8 vertices into two disjoint sets of 4."
    )
    commentary = (
        "Parity computation from 1-bit count provides a single-bit classification "
        "of each vertex. This information-theoretic property naturally partitions "
        "the 8 vertices into two groups of 4."
    )
    
    def model(self) -> Dict[str, float]:
        expected = {0: 0, 1: 1, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1}
        correct = sum(1 for v in range(8) if get_vertex_parity(v) == expected[v])
        return {"Correct parities": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Correct parities": 8}


class EvenParityIsTetB(GFDTest):
    """
    Even parity vertices {0,3,5,6} must belong to Tetrahedron B.
    This tetrahedron has its apex at V0 (binary 000, all zeros).
    """
    name = "Even Parity = Tet B"
    question = "Do the even parity vertices {0,3,5,6} form Tetrahedron B, with apex V0 (000) at zero 1-bit count?"
    reference_source = "Parity-tetrahedron rule"
    tolerance = 0.001
    derivation = (
        "PREMISE: Tetrahedron B is defined as the set of even-parity vertices. "
        "STEP 1: Collect vertices with parity = 0: {v | popcount(v) mod 2 = 0}. "
        "STEP 2: Result: {0, 3, 5, 6} (vertices with 0 or 2 ones). "
        "STEP 3: V0 (000) has 0 ones (minimum), making it the pure-state apex. "
        "STEP 4: These 4 vertices form a valid tetrahedron in the cube geometry. "
        "OUTPUT: Even parity vertices {0,3,5,6} = Tet B, with apex V0."
    )
    commentary = (
        "Even parity determining Tetrahedron B membership connects information "
        "theory to geometry. The apex V0 (000) with zero 1-bits anchors the "
        "even-parity Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        even = {v for v in range(8) if get_vertex_parity(v) == 0}
        expected = {0, 3, 5, 6}
        correct = 1 if even == expected == TET_B else 0
        return {"Tet_B assignment correct": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Tet_B assignment correct": 1}


class OddParityIsTetA(GFDTest):
    """
    Odd parity vertices {1,2,4,7} must belong to Tetrahedron A.
    This tetrahedron has its apex at V7 (binary 111, all ones).
    """
    name = "Odd Parity = Tet A"
    question = "Do the odd parity vertices {1,2,4,7} form Tetrahedron A, with apex V7 (111) at maximum 1-bit count?"
    reference_source = "Parity-tetrahedron rule"
    tolerance = 0.001
    derivation = (
        "PREMISE: Tetrahedron A is defined as the set of odd-parity vertices. "
        "STEP 1: Collect vertices with parity = 1: {v | popcount(v) mod 2 = 1}. "
        "STEP 2: Result: {1, 2, 4, 7} (vertices with 1 or 3 ones). "
        "STEP 3: V7 (111) has 3 ones (maximum = d), making it the pure-state apex. "
        "STEP 4: These 4 vertices form a valid tetrahedron in the cube geometry. "
        "OUTPUT: Odd parity vertices {1,2,4,7} = Tet A, with apex V7."
    )
    commentary = (
        "Odd parity determining Tetrahedron A membership mirrors the even-parity "
        "rule. The apex V7 (111) with maximal 1-bits anchors the odd-parity "
        "Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        odd = {v for v in range(8) if get_vertex_parity(v) == 1}
        expected = {1, 2, 4, 7}
        correct = 1 if odd == expected == TET_A else 0
        return {"Tet_A assignment correct": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Tet_A assignment correct": 1}


class TetrahedronFunction(GFDTest):
    """
    The get_tetrahedron() function must return 'A' or 'B' correctly
    for all 8 vertices based on their parity.
    """
    name = "Tetrahedron Function"
    question = "Does get_tetrahedron(v) correctly return 'A' for odd parity and 'B' for even parity for all 8 vertices?"
    reference_source = "Function definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: get_tetrahedron() must implement the parity-based Field Chamber assignment. "
        "STEP 1: For each vertex in Tet A {1,2,4,7}, verify get_tetrahedron(v) == 'A'. "
        "STEP 2: For each vertex in Tet B {0,3,5,6}, verify get_tetrahedron(v) == 'B'. "
        "STEP 3: Count correct assignments. "
        "STEP 4: All 8 assignments must be correct. "
        "OUTPUT: Function correctly implements parity-based tetrahedron assignment."
    )
    commentary = None  # Function correctness verification
    
    def model(self) -> Dict[str, float]:
        correct = 0
        for v in TET_A:
            if get_tetrahedron(v) == 'A':
                correct += 1
        for v in TET_B:
            if get_tetrahedron(v) == 'B':
                correct += 1
        return {"Correct assignments": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Correct assignments": 8}


class TetrahedronPartition(GFDTest):
    """
    Parity must create a valid partition: two disjoint sets of
    exactly 4 vertices each that together cover all 8 vertices.
    """
    name = "Tetrahedron Partition"
    question = "Does parity create a valid partition: two disjoint sets of exactly k=4 vertices each, covering all 2k=8?"
    reference_source = "Partition requirement"
    tolerance = 0.001
    derivation = (
        "PREMISE: A valid partition requires disjoint sets with complete coverage. "
        "STEP 1: Even parity set: {0,3,5,6}, size = 4. "
        "STEP 2: Odd parity set: {1,2,4,7}, size = 4. "
        "STEP 3: Check disjoint: {0,3,5,6} ∩ {1,2,4,7} = {} (empty). "
        "STEP 4: Check complete: {0,3,5,6} ∪ {1,2,4,7} = {0,1,2,3,4,5,6,7} (all 8). "
        "OUTPUT: Parity creates a valid 4+4 partition of the 8 vertices."
    )
    commentary = (
        "The parity partition yielding exactly two disjoint sets of 4 is a "
        "mathematical necessity from binary arithmetic. This property enables "
        "the dual tetrahedron structure without arbitrary assignment."
    )
    
    def model(self) -> Dict[str, float]:
        even = {v for v in range(8) if get_vertex_parity(v) == 0}
        odd = {v for v in range(8) if get_vertex_parity(v) == 1}
        
        disjoint = 1 if len(even & odd) == 0 else 0
        complete = 1 if (even | odd) == set(range(8)) else 0
        correct_size = 1 if len(even) == 4 and len(odd) == 4 else 0
        
        return {
            "Sets disjoint": disjoint,
            "Sets complete": complete,
            "Each set has 4": correct_size,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Sets disjoint": 1,
            "Sets complete": 1,
            "Each set has 4": 1,
        }


class ApexesCorrect(GFDTest):
    """
    V7 (111, all 1s, odd parity) must be the Tet_A apex.
    V0 (000, all 0s, even parity) must be the Tet_B apex.
    These are the "pure" vertices of each tetrahedron.
    """
    name = "Apexes Correct"
    question = "Are V7 (111, all 1s) and V0 (000, all 0s) the apexes of Tet A and Tet B respectively, as pure binary states?"
    reference_source = "Apex definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: Apex vertices are pure binary states at extremes of the 1-bit count spectrum. "
        "STEP 1: V7 (111) has d=3 ones (maximum). Parity: 3 mod 2 = 1 (odd) -> Tet A. "
        "STEP 2: V0 (000) has 0 ones (minimum). Parity: 0 mod 2 = 0 (even) -> Tet B. "
        "STEP 3: V7 and V0 are maximally separated: all bits differ. "
        "STEP 4: These pure states anchor their respective tetrahedra as apexes. "
        "OUTPUT: V7 is Tet A apex (all 1s), V0 is Tet B apex (all 0s)."
    )
    commentary = (
        "V7 (111) and V0 (000) as pure binary states naturally serve as apexes "
        "for their respective Field Chambers. Their maximal difference in 1-bit "
        "count positions them as endpoints of the parity spectrum."
    )
    
    def model(self) -> Dict[str, float]:
        v7_correct = 1 if 7 in TET_A else 0
        v0_correct = 1 if 0 in TET_B else 0
        return {
            "V7 in Tet_A": v7_correct,
            "V0 in Tet_B": v0_correct,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "V7 in Tet_A": 1,
            "V0 in Tet_B": 1,
        }


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


def run_all_tests() -> bool:
    """Run all vertex encoding tests."""
    return run_test_group(
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
    success = run_all_tests()
    sys.exit(0 if success else 1)
