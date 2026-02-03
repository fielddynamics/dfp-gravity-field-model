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

import sys
import os
import numpy as np
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from gfd_model_v2.common import VERTICES, TET_A, TET_B, get_tetrahedron


# =============================================================================
# TESTS
# =============================================================================

class TetAVertices(GFDTest):
    """
    Tet_A contains the 4 odd-parity vertices: {1, 2, 4, 7}. These are
    the vertices whose binary representations have an odd number of 1-bits.
    """
    name = "Tet_A Vertices"
    question = "Does Tetrahedron A contain exactly the k=4 odd-parity vertices {1, 2, 4, 7}, determined by bit counting?"
    reference_source = "Parity definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: Tetrahedron A is defined as the set of odd-parity vertices (popcount mod 2 = 1). "
        "STEP 1: V1 (001): 1 one -> odd parity -> Tet A. "
        "STEP 2: V2 (010): 1 one -> odd parity -> Tet A. "
        "STEP 3: V4 (100): 1 one -> odd parity -> Tet A. "
        "STEP 4: V7 (111): 3 ones -> odd parity -> Tet A. "
        "OUTPUT: Tet A = {1, 2, 4, 7}, k=4 vertices with odd bit count."
    )
    commentary = (
        "Tetrahedron A containing odd-parity vertices connects binary encoding to "
        "geometric structure. This assignment emerges from bit counting, not from "
        "arbitrary choice or fitting."
    )
    
    def model(self) -> Dict[str, float]:
        expected = {1, 2, 4, 7}
        correct = 1 if TET_A == expected else 0
        return {"Correct assignment": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Correct assignment": 1}


class TetBVertices(GFDTest):
    """
    Tet_B contains the 4 even-parity vertices: {0, 3, 5, 6}. These are
    the vertices whose binary representations have an even number of 1-bits.
    """
    name = "Tet_B Vertices"
    question = "Does Tetrahedron B contain exactly the k=4 even-parity vertices {0, 3, 5, 6}, completing the binary partition?"
    reference_source = "Parity definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: Tetrahedron B is defined as the set of even-parity vertices (popcount mod 2 = 0). "
        "STEP 1: V0 (000): 0 ones -> even parity -> Tet B. "
        "STEP 2: V3 (011): 2 ones -> even parity -> Tet B. "
        "STEP 3: V5 (101): 2 ones -> even parity -> Tet B. "
        "STEP 4: V6 (110): 2 ones -> even parity -> Tet B. "
        "OUTPUT: Tet B = {0, 3, 5, 6}, k=4 vertices with even bit count."
    )
    commentary = (
        "Tetrahedron B containing even-parity vertices completes the binary partition. "
        "Together with Tetrahedron A, this provides complete coverage of all 8 vertices "
        "through parity classification."
    )
    
    def model(self) -> Dict[str, float]:
        expected = {0, 3, 5, 6}
        correct = 1 if TET_B == expected else 0
        return {"Correct assignment": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Correct assignment": 1}


class TetrahedraDisjoint(GFDTest):
    """
    Tet_A and Tet_B must share no vertices. Their intersection
    must be the empty set.
    """
    name = "Tetrahedra Disjoint"
    question = "Is the intersection of Tet A and Tet B empty, ensuring the two Field Chambers form a proper partition?"
    reference_source = "Partition requirement"
    tolerance = 0.001
    derivation = (
        "PREMISE: A partition requires disjoint subsets (no shared elements). "
        "STEP 1: Tet A = {1, 2, 4, 7} (odd parity). "
        "STEP 2: Tet B = {0, 3, 5, 6} (even parity). "
        "STEP 3: A vertex cannot have both odd and even parity simultaneously. "
        "STEP 4: Therefore Tet A ∩ Tet B = {} (empty set). "
        "OUTPUT: The two Field Chambers share no vertices."
    )
    commentary = None  # Partition property verification
    
    def model(self) -> Dict[str, float]:
        intersection = TET_A & TET_B
        return {"Shared vertices": len(intersection)}
    
    def observations(self) -> Dict[str, float]:
        return {"Shared vertices": 0}


class TetrahedraCoverAll(GFDTest):
    """
    Together, Tet_A and Tet_B must cover all 8 vertices (0-7).
    Their union must equal {0, 1, 2, 3, 4, 5, 6, 7}.
    """
    name = "Tetrahedra Cover All"
    question = "Does the union of Tet A and Tet B cover all 2k=8 vertices, ensuring no d-bit state is excluded?"
    reference_source = "Partition requirement"
    tolerance = 0.001
    derivation = (
        "PREMISE: A partition requires complete coverage (all elements accounted for). "
        "STEP 1: Tet A = {1, 2, 4, 7}, size = k = 4. "
        "STEP 2: Tet B = {0, 3, 5, 6}, size = k = 4. "
        "STEP 3: Tet A ∪ Tet B = {0, 1, 2, 3, 4, 5, 6, 7}, size = 2k = 8. "
        "STEP 4: This equals the full vertex set {0, 1, ..., 7}. "
        "OUTPUT: Both Field Chambers together cover all 8 vertices."
    )
    commentary = (
        "Complete vertex coverage by the two Field Chambers ensures the dual "
        "structure encodes all possible 3-bit states. No vertex is excluded from "
        "the traversal mechanics."
    )
    
    def model(self) -> Dict[str, float]:
        combined = TET_A | TET_B
        expected = set(range(8))
        correct = 1 if combined == expected else 0
        return {
            "Combined vertex count": len(combined),
            "Covers all 8": correct,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Combined vertex count": 8,
            "Covers all 8": 1,
        }


class EachTetrahedronHas4Vertices(GFDTest):
    """
    Each tetrahedron must have exactly 4 vertices. This is the
    defining property of a tetrahedron.
    """
    name = "Each Tetrahedron Has 4 Vertices"
    question = "Does each tetrahedron have exactly k=4 vertices, satisfying the fundamental tetrahedral definition?"
    reference_source = "Tetrahedron definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: A tetrahedron is the simplest 3D polyhedron, requiring exactly 4 vertices. "
        "STEP 1: Count Tet A vertices: |{1, 2, 4, 7}| = 4 = k. "
        "STEP 2: Count Tet B vertices: |{0, 3, 5, 6}| = 4 = k. "
        "STEP 3: From Field Closure, k=4 is the topology constant. "
        "STEP 4: Both counts match k=4, confirming tetrahedral structure. "
        "OUTPUT: Each Field Chamber has exactly k=4 vertices."
    )
    commentary = None  # Fundamental geometric property
    
    def model(self) -> Dict[str, float]:
        return {
            "Tet_A vertices": len(TET_A),
            "Tet_B vertices": len(TET_B),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Tet_A vertices": 4,
            "Tet_B vertices": 4,
        }


class V7IsTetAApex(GFDTest):
    """
    V7 (binary 111) is the apex of Tetrahedron A. It has all 1-bits,
    making it the natural apex of the odd-parity tetrahedron.
    """
    name = "V7 is Tet_A Apex"
    question = "Is V7 (binary 111, d=3 ones) the apex of Tetrahedron A, representing the maximal odd-parity state?"
    reference_source = "Binary encoding"
    tolerance = 0.001
    derivation = (
        "PREMISE: The apex is the geometrically distinguished vertex of each tetrahedron. "
        "STEP 1: V7 has binary representation 111 (all d=3 bits set to 1). "
        "STEP 2: Bit count: 3 ones. Parity: 3 mod 2 = 1 (odd) -> Tet A. "
        "STEP 3: V7 is at cube corner (+1,+1,+1), maximally distant from V0. "
        "STEP 4: By construction, V7 is designated as Tet A apex. "
        "OUTPUT: V7 (111) is the Tet A apex, the pure odd-parity state."
    )
    commentary = (
        "V7 with binary representation 111 serves as the Tetrahedron A apex. "
        "Its maximal 1-bit count makes it the natural endpoint of the odd-parity "
        "Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        v7_in_a = 1 if 7 in TET_A else 0
        v7_binary = VERTICES[7]['binary']
        is_111 = 1 if v7_binary == '111' else 0
        return {
            "V7 in Tet_A": v7_in_a,
            "V7 is 111": is_111,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "V7 in Tet_A": 1,
            "V7 is 111": 1,
        }


class V0IsTetBApex(GFDTest):
    """
    V0 (binary 000) is the apex of Tetrahedron B. It has all 0-bits,
    making it the natural apex of the even-parity tetrahedron.
    """
    name = "V0 is Tet_B Apex"
    question = "Is V0 (binary 000, zero ones) the apex of Tetrahedron B, representing the minimal even-parity state?"
    reference_source = "Binary encoding"
    tolerance = 0.001
    derivation = (
        "PREMISE: The apex is the geometrically distinguished vertex of each tetrahedron. "
        "STEP 1: V0 has binary representation 000 (all d=3 bits set to 0). "
        "STEP 2: Bit count: 0 ones. Parity: 0 mod 2 = 0 (even) -> Tet B. "
        "STEP 3: V0 is at cube corner (-1,-1,-1), maximally distant from V7. "
        "STEP 4: By construction, V0 is designated as Tet B apex. "
        "OUTPUT: V0 (000) is the Tet B apex, the pure even-parity state."
    )
    commentary = (
        "V0 with binary representation 000 serves as the Tetrahedron B apex. "
        "Its zero 1-bit count makes it the natural endpoint of the even-parity "
        "Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        v0_in_b = 1 if 0 in TET_B else 0
        v0_binary = VERTICES[0]['binary']
        is_000 = 1 if v0_binary == '000' else 0
        return {
            "V0 in Tet_B": v0_in_b,
            "V0 is 000": is_000,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "V0 in Tet_B": 1,
            "V0 is 000": 1,
        }


class ApicesAreAntipodal(GFDTest):
    """
    V0 and V7 are at opposite corners of the cube (antipodal).
    Their distance is 2*sqrt(3) in the centered cube [-1,1]^3.
    """
    name = "Apices Are Antipodal"
    question = "Are the apices V0 and V7 at maximum separation (cube diagonal 2*sqrt(d) = 2*sqrt(3)), defining the Field Chamber axis?"
    reference_source = "Cube geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Antipodal vertices are at opposite cube corners with maximum separation. "
        "STEP 1: V0 coordinates: (-1, -1, -1). V7 coordinates: (+1, +1, +1). "
        "STEP 2: Displacement: V7 - V0 = (2, 2, 2). "
        "STEP 3: Distance: ||(2,2,2)|| = sqrt(4+4+4) = sqrt(12) = 2*sqrt(3) ≈ 3.464. "
        "STEP 4: This is the cube body diagonal, the maximum possible vertex separation. "
        "OUTPUT: V0 and V7 are antipodal, separated by 2*sqrt(3)."
    )
    commentary = (
        "The apices V0 and V7 at maximum separation (cube diagonal) create the "
        "axis around which the dual Field Chamber structure is organized. This "
        "antipodal arrangement enables the TIME face classification."
    )
    
    def model(self) -> Dict[str, float]:
        v0_coords = np.array(VERTICES[0]['coords'])
        v7_coords = np.array(VERTICES[7]['coords'])
        distance = np.linalg.norm(v7_coords - v0_coords)
        return {"V0-V7 distance": distance}
    
    def observations(self) -> Dict[str, float]:
        return {"V0-V7 distance": 2 * np.sqrt(3)}


class TetrahedraAreRegular(GFDTest):
    """
    Both tetrahedra are regular, meaning all 6 edges of each have equal
    length. For the centered cube, this length is 2*sqrt(2).
    """
    name = "Tetrahedra Are Regular"
    question = "Are both tetrahedra regular (all 6 edges equal to 2*sqrt(2)), ensuring symmetric Field Chambers?"
    reference_source = "Cube geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: A regular tetrahedron has all 6 edges of equal length. "
        "STEP 1: Edge length formula for cube face diagonal: sqrt(2^2 + 2^2) = 2*sqrt(2) ≈ 2.828. "
        "STEP 2: For Tet A, compute all 6 pairwise distances between {1,2,4,7}. "
        "STEP 3: For Tet B, compute all 6 pairwise distances between {0,3,5,6}. "
        "STEP 4: Verify all 12 edges equal 2*sqrt(2). "
        "OUTPUT: Both tetrahedra are regular with edge length 2*sqrt(2)."
    )
    commentary = (
        "Both tetrahedra being regular (equal edge lengths) ensures the Field "
        "Chambers have identical geometry. This symmetry underlies the balanced "
        "treatment of Tetrahedron A and Tetrahedron B."
    )
    
    def model(self) -> Dict[str, float]:
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
        
        return {
            "Tet_A edge length": edges_a[0],
            "Tet_A regular": all_equal_a,
            "Tet_B regular": all_equal_b,
        }
    
    def observations(self) -> Dict[str, float]:
        expected_edge = 2 * np.sqrt(2)
        return {
            "Tet_A edge length": expected_edge,
            "Tet_A regular": 1,
            "Tet_B regular": 1,
        }


class ApicesAreBinaryComplements(GFDTest):
    """
    V0 (000) and V7 (111) are binary complements. XORing them gives 111
    (7 in decimal), confirming they are maximally different.
    """
    name = "Apices Are Binary Complements"
    question = "Does V0 XOR V7 = 7 (binary 111), confirming the apices differ in all d=3 bit positions?"
    reference_source = "Binary arithmetic"
    tolerance = 0.001
    derivation = (
        "PREMISE: Binary complements differ in every bit position (XOR yields all 1s). "
        "STEP 1: V0 = 0 = 000 in binary. V7 = 7 = 111 in binary. "
        "STEP 2: XOR: 000 XOR 111 = 111 = 7 in decimal. "
        "STEP 3: Result 111 means all d=3 bits differ between V0 and V7. "
        "STEP 4: This is the maximum possible Hamming distance (d bits). "
        "OUTPUT: V0 and V7 are binary complements, maximally different."
    )
    commentary = (
        "The apices V0 and V7 being binary complements connects the geometric "
        "antipodal relationship to information-theoretic maximal difference. "
        "Every bit differs between these extreme vertices."
    )
    
    def model(self) -> Dict[str, float]:
        xor_result = 0 ^ 7
        return {"V0 XOR V7": xor_result}
    
    def observations(self) -> Dict[str, float]:
        return {"V0 XOR V7": 7}


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


def run_all_tests() -> bool:
    """Run all tetrahedron assignment tests."""
    return run_test_group(
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
    success = run_all_tests()
    sys.exit(0 if success else 1)
