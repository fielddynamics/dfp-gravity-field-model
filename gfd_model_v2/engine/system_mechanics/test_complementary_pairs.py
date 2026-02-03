"""
Complementary Pairs
===================

This module examines the complementary vertex pair structure in the dual
Field Chamber geometry. Each vertex V_n pairs with V_(7-n), with the
following properties:

- Each pair sums to 7 (binary: 111)
- Each pair contains one vertex from each Field Chamber (Tet A and Tet B)
- Pairs are geometrically opposed (at opposite cube corners)
- The (3,4) pair completes first in pi traversal

The complementary pairs are: (0,7), (1,6), (2,5), (3,4)
"""

import sys
import os
from typing import Dict, Optional
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from common import (
    COMPLEMENTARY_PAIRS, TET_A, TET_B, VERTICES,
    get_tetrahedron, traverse_pi_base8
)


# =============================================================================
# TESTS
# =============================================================================

class PairsSumTo7(GFDTest):
    """
    The complementary pairs (0,7), (1,6), (2,5), (3,4) all sum to 7. This is
    not coincidence but reflects the binary structure: n + (7-n) = 7 always.
    In binary, 7 = 111, representing complete traversal of all 3 bits.
    """
    name = "Pairs Sum to 7"
    question = "Do all complementary pairs sum to 7 (binary 111), representing complete coverage of d=3 spatial dimensions?"
    reference_source = "Theoretical (n + (7-n) = 7)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Complementary pairs are (n, 7-n) for n in {0,1,2,3}. "
        "STEP 1: List pairs: (0,7), (1,6), (2,5), (3,4). "
        "STEP 2: Compute sums: 0+7=7, 1+6=7, 2+5=7, 3+4=7. "
        "STEP 3: All sums equal 7 = 2^d - 1 = 2^3 - 1 (maximum d-bit value). "
        "STEP 4: In binary: 7 = 111, representing all d=3 bits set to 1. "
        "OUTPUT: Each pair together covers all d=3 spatial dimensions."
    )
    commentary = (
        "Complementary pairs summing to 7 (binary 111) represents complete bit coverage. "
        "Each pair together addresses all three spatial dimensions, suggesting the pairing "
        "structure encodes complete information about Field Chamber geometry."
    )
    
    def model(self) -> Dict[str, float]:
        sums = [a + b for a, b in COMPLEMENTARY_PAIRS]
        all_7 = 1 if all(s == 7 for s in sums) else 0
        return {
            "Number of pairs": len(COMPLEMENTARY_PAIRS),
            "All sums equal 7": all_7,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Number of pairs": 4,
            "All sums equal 7": 1,
        }


class PairsBinaryComplement(GFDTest):
    """
    Each pair XORs to 7 (binary 111). This means each pair covers all 3 bits
    when combined: if one vertex has a 0 in a bit position, its complement
    has a 1 there.
    """
    name = "Pairs XOR to 111"
    question = "Does XOR of each complementary pair equal 7 (binary 111), confirming perfect bit complementation?"
    reference_source = "Theoretical (XOR complement)"
    tolerance = 0.001
    derivation = (
        "PREMISE: XOR operation flips bits that differ, leaving bits that match as 0. "
        "STEP 1: For pair (n, 7-n), compute XOR: n XOR (7-n). "
        "STEP 2: Examples: 0 XOR 7 = 000 XOR 111 = 111 = 7; 3 XOR 4 = 011 XOR 100 = 111 = 7. "
        "STEP 3: For all 4 pairs, XOR result is 7 (111). "
        "STEP 4: This means every bit position differs between pair members. "
        "OUTPUT: Perfect bit complementation; each pair covers all d=3 bit positions."
    )
    commentary = (
        "The XOR operation producing 111 for all pairs indicates perfect bit "
        "complementation. This algebraic property connects to geometric opposition, "
        "where each vertex pair occupies antipodal positions in the Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        xors = [a ^ b for a, b in COMPLEMENTARY_PAIRS]
        all_7 = 1 if all(x == 7 for x in xors) else 0
        return {
            "All XORs equal 7": all_7,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "All XORs equal 7": 1,
        }


class PairsCrossTetrahedra(GFDTest):
    """
    Each complementary pair has one vertex from Tet A and one from Tet B.
    This ensures that complementary vertices reside in opposite Field Chambers.
    """
    name = "Pairs Cross Field Chambers"
    question = "Does each complementary pair span both Field Chambers, with one vertex in Tet A and one in Tet B?"
    reference_source = "Theoretical (dual structure)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Bit complementation flips all d=3 bits, changing parity (odd <-> even). "
        "STEP 1: Tet A = odd parity vertices {1,2,4,7}. Tet B = even parity vertices {0,3,5,6}. "
        "STEP 2: Check pair (0,7): 0 in Tet B, 7 in Tet A. Cross-chamber: yes. "
        "STEP 3: Check pair (1,6): 1 in Tet A, 6 in Tet B. Cross-chamber: yes. "
        "STEP 4: Similarly (2,5) and (3,4) cross chambers. "
        "OUTPUT: All 4 pairs span both Field Chambers due to parity inversion."
    )
    commentary = (
        "Cross-chamber pairing links every Tetrahedron A vertex to a Tetrahedron B "
        "partner. This structure may enable information exchange between Field Chambers "
        "and underlie the bimetric coupling observed during traversal."
    )
    
    def model(self) -> Dict[str, float]:
        cross_count = 0
        for a, b in COMPLEMENTARY_PAIRS:
            tet_a = get_tetrahedron(a)
            tet_b = get_tetrahedron(b)
            if tet_a != tet_b:
                cross_count += 1
        return {
            "Pairs crossing tetrahedra": cross_count,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Pairs crossing tetrahedra": 4,
        }


class Pair34CompletesFirst(GFDTest):
    """
    When traversing with pi base-8, the (3,4) pair completes first. The digit
    3 goes to V3, and the next digit 1 takes cumsum to 4, completing the pair.
    This (3,4) encoding reflects 3+1 spacetime structure.
    """
    name = "(3,4) Pair Completes First"
    question = "Does pi's leading digit sequence (3.1) complete the (3,4) complementary pair first, encoding the k=4 topology constant?"
    reference_source = "Pi = 3.14159..."
    tolerance = 0.001
    derivation = (
        "PREMISE: Pi = 3.14159... in base-8 begins 3.1..., immediately visiting V3 then V4. "
        "STEP 1: First digit 3: cumsum=3, vertex=V3 (Tet B). "
        "STEP 2: Second digit 1: cumsum=4, vertex=V4 (Tet A). "
        "STEP 3: Both V3 and V4 are now visited. Check: is (3,4) a complementary pair? 3+4=7. Yes. "
        "STEP 4: First complete pair is (3,4), encoding 3+1=k=4. "
        "OUTPUT: Pi naturally completes the (3,4) pair first, linking to 3+1 spacetime structure."
    )
    commentary = (
        "The (3,4) pair completing first is determined by pi's initial digits. "
        "This specific pairing encodes 3+1=4, corresponding to both the topology "
        "constant k and the spacetime dimensional structure. The correspondence "
        "emerges from pi's mathematical value without parameter adjustment."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(20)
        
        visited = set()
        first_pair = None
        first_step = None
        
        for r in results:
            v = r['vertex']
            visited.add(v)
            
            for a, b in COMPLEMENTARY_PAIRS:
                if a in visited and b in visited:
                    first_pair = (min(a, b), max(a, b))
                    first_step = r['step']
                    break
            
            if first_pair:
                break
        
        is_34 = 1 if first_pair == (3, 4) else 0
        return {
            "First pair is (3,4)": is_34,
            "Completion step": first_step if first_step else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "First pair is (3,4)": 1,
            "Completion step": 1,
        }


class Pair34Correspondence(GFDTest):
    """
    The (3,4) pair corresponds to the 3+1 structure: V3 is from Tet B
    and V4 is from Tet A. This is the first complementary pair completed
    when pi drives the traversal.
    """
    name = "(3,4) Pair Correspondence"
    question = "Does the (3,4) pair establish immediate bimetric coupling with V3 in Tet B and V4 in Tet A?"
    reference_source = "Theoretical (dual structure)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Bimetric coupling requires interaction between both Field Chambers. "
        "STEP 1: Determine V3's Field Chamber: parity of 3 (011) = 2 ones = even -> Tet B. "
        "STEP 2: Determine V4's Field Chamber: parity of 4 (100) = 1 one = odd -> Tet A. "
        "STEP 3: First two vertices: V3 (Tet B) -> V4 (Tet A). "
        "STEP 4: This transition crosses Field Chambers at the very first step. "
        "OUTPUT: Immediate bimetric coupling is established by the (3,4) pair structure."
    )
    commentary = (
        "The (3,4) pair spans both Field Chambers, with V3 in Tetrahedron B and "
        "V4 in Tetrahedron A. This cross-chamber pairing at the first step "
        "establishes immediate bimetric coupling in the traversal sequence."
    )
    
    def model(self) -> Dict[str, float]:
        v3_is_tet_b = 1 if get_tetrahedron(3) == 'B' else 0
        v4_is_tet_a = 1 if get_tetrahedron(4) == 'A' else 0
        correct_encoding = 1 if v3_is_tet_b and v4_is_tet_a else 0
        return {
            "V3 in Tet B (spatial)": v3_is_tet_b,
            "V4 in Tet A (temporal)": v4_is_tet_a,
            "Correct 3+1 encoding": correct_encoding,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "V3 in Tet B (spatial)": 1,
            "V4 in Tet A (temporal)": 1,
            "Correct 3+1 encoding": 1,
        }


class PairsGeometricallyOpposed(GFDTest):
    """
    Each complementary pair sits at opposite corners of the cube. Geometrically,
    if vertex A is at coordinates (x, y, z), its complement is at (-x, -y, -z).
    """
    name = "Pairs Geometrically Opposed"
    question = "Do complementary vertices occupy diagonally opposite cube corners, with coordinates (x,y,z) and (-x,-y,-z)?"
    reference_source = "Cube geometry"
    tolerance = 0.001
    derivation = (
        "PREMISE: Cube corners have coordinates (+/-1, +/-1, +/-1). Opposite corners sum to (0,0,0). "
        "STEP 1: For each pair (n, 7-n), get coordinates of both vertices. "
        "STEP 2: Check if coords[n] = -coords[7-n] for all d=3 axes. "
        "STEP 3: Example: V0=(-1,-1,-1), V7=(+1,+1,+1). Sum: (0,0,0). Opposite: yes. "
        "STEP 4: Verify for all 4 pairs: each pair occupies antipodal cube corners. "
        "OUTPUT: All complementary pairs are at maximum geometric separation (cube diagonal)."
    )
    commentary = (
        "Geometric opposition places complementary vertices at maximum separation "
        "within the Field Chamber structure. This spatial arrangement suggests "
        "complementary pairs represent maximally distinct information states."
    )
    
    def model(self) -> Dict[str, float]:
        opposed_count = 0
        for a, b in COMPLEMENTARY_PAIRS:
            a_coords = VERTICES[a]['coords']
            b_coords = VERTICES[b]['coords']
            is_opposite = all(a_coords[i] == -b_coords[i] for i in range(3))
            if is_opposite:
                opposed_count += 1
        return {
            "Geometrically opposed pairs": opposed_count,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Geometrically opposed pairs": 4,
        }


class PairMidpointsAtOrigin(GFDTest):
    """
    The midpoint of each complementary pair is the origin (0,0,0). This means
    the line connecting any pair passes through the center of the dual
    Field Chamber structure.
    """
    name = "Pair Midpoints at Origin"
    question = "Do the midpoints of all complementary pairs converge at the Field Origin (0,0,0)?"
    reference_source = "Cube geometry"
    tolerance = 0.001
    derivation = (
        "PREMISE: Midpoint of (A, B) is (A + B) / 2. For antipodal points, midpoint is origin. "
        "STEP 1: For pair (0,7): midpoint = (V0_coords + V7_coords) / 2 = ((-1,-1,-1) + (+1,+1,+1)) / 2 = (0,0,0). "
        "STEP 2: For pair (1,6): midpoint = (V1_coords + V6_coords) / 2 = ((-1,-1,+1) + (+1,+1,-1)) / 2 = (0,0,0). "
        "STEP 3: Similarly verify for pairs (2,5) and (3,4): all midpoints are (0,0,0). "
        "STEP 4: The origin is the Field Origin, geometric center of the stellated octahedron. "
        "OUTPUT: All 4 complementary pair midpoints coincide at the Field Origin."
    )
    commentary = (
        "All complementary pair midpoints converge at the Field Origin, the "
        "geometric center of the stellated octahedron. This property positions "
        "the Field Origin as the balance point for all cross-chamber interactions."
    )
    
    def model(self) -> Dict[str, float]:
        at_origin_count = 0
        for a, b in COMPLEMENTARY_PAIRS:
            a_coords = np.array(VERTICES[a]['coords'])
            b_coords = np.array(VERTICES[b]['coords'])
            midpoint = (a_coords + b_coords) / 2
            if np.allclose(midpoint, [0, 0, 0]):
                at_origin_count += 1
        return {
            "Midpoints at origin": at_origin_count,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Midpoints at origin": 4,
        }


class PiIntegerProduces34(GFDTest):
    """
    Pi's first digit (3) goes directly to V3. The second digit (1) advances
    the cumsum to 4, landing on V4. Thus pi's integer part naturally produces
    the (3,4) pair that encodes spacetime structure.
    """
    name = "Pi Integer Produces (3,4)"
    question = "Do pi's first two digits (3.1...) deterministically produce the (V3, V4) vertex pair without parameter adjustment?"
    reference_source = "Pi = 3.14159..."
    tolerance = 0.001
    derivation = (
        "PREMISE: Pi base-8 = 3.1103755... The integer part is 3, first fractional digit is 1. "
        "STEP 1: First digit is 3. Initial cumsum = 3. Vertex = 3 mod 8 = V3. "
        "STEP 2: Second digit is 1. Cumsum = 3 + 1 = 4. Vertex = 4 mod 8 = V4. "
        "STEP 3: First vertex: V3 (digit 3). Second vertex: V4 (digit 1). "
        "STEP 4: Sum: 3 + 1 = 4 = k. This is the topology constant. "
        "OUTPUT: Pi's mathematical structure produces (V3, V4), encoding 3+1 = k."
    )
    commentary = (
        "Pi's leading digits 3.1 deterministically produce the (3,4) vertex pair, "
        "encoding the 3+1 dimensional structure from the outset. This correspondence "
        "between a fundamental mathematical constant and spacetime dimensionality "
        "emerges without any fitted parameters."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(5)
        v1 = results[0]['vertex']  # Should be 3
        v2 = results[1]['vertex']  # Should be 4
        d1 = results[0]['digit']   # Should be 3
        d2 = results[1]['digit']   # Should be 1
        
        correct = 1 if v1 == 3 and v2 == 4 and d1 == 3 and d2 == 1 else 0
        return {
            "First vertex": v1,
            "Second vertex": v2,
            "Produces (3,4)": correct,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "First vertex": 3,
            "Second vertex": 4,
            "Produces (3,4)": 1,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    PairsSumTo7,
    PairsBinaryComplement,
    PairsCrossTetrahedra,
    Pair34CompletesFirst,
    Pair34Correspondence,
    PairsGeometricallyOpposed,
    PairMidpointsAtOrigin,
    PiIntegerProduces34,
]


def run_all_tests() -> bool:
    """Run all complementary pairs tests."""
    return run_test_group(
        title="Complementary Pairs",
        summary=(
            "These tests examine the complementary vertex pair structure in the dual "
            "Field Chamber geometry. Each vertex V_n pairs with V_(7-n), forming pairs "
            "that are geometrically opposed and cross Field Chambers. The pairs are "
            "(0,7), (1,6), (2,5), and (3,4). When pi drives the traversal, the (3,4) "
            "pair completes first because 3.1... produces vertices 3 then 4. V3 resides "
            "in Tet B and V4 resides in Tet A."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
