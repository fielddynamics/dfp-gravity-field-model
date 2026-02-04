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

from typing import Dict
import numpy as np

from gfd_model_v2.framework import *
from gfd_model_v2.common import (
    COMPLEMENTARY_PAIRS, TET_A, TET_B, VERTICES,
    get_tetrahedron, traverse_pi_base8
)


# =============================================================================
# TESTS
# =============================================================================

class PairsSumTo7(Test):
    """
    The complementary pairs (0,7), (1,6), (2,5), (3,4) all sum to 7. This is
    not coincidence but reflects the binary structure: n + (7-n) = 7 always.
    In binary, 7 = 111, representing complete traversal of all 3 bits.
    """
    name = "Pairs Sum to 7"
    question = (
        "Every cube corner has a partner at the diagonally opposite position. If we add "
        "their vertex numbers, do we always get 7? This is like asking: if I am at corner "
        "n, is my partner always at corner (7 minus n)? We check all 4 pairs."
    )
    reference = "Theoretical (n + (7-n) = 7)"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Seven is the magic number here. It is 2^3 minus 1, the largest 3-bit number. In "
        "binary, 7 is 111, all bits on. When you add a vertex to its complement, you must "
        "get 7, because wherever one vertex has a 0, the other has a 1. Together they "
        "cover all three bit positions. The pairs (0,7), (1,6), (2,5), (3,4) all sum to 7 "
        "because complementary means 'together we fill all the gaps.'"
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Complementary pairs are (n, 7-n) for n in {0,1,2,3}.")
            .step("List pairs: (0,7), (1,6), (2,5), (3,4).")
            .step("Compute sums: 0+7=7, 1+6=7, 2+5=7, 3+4=7.")
            .step("All sums equal 7 = 2^d - 1 = 2^3 - 1 (maximum d-bit value).")
            .step("In binary: 7 = 111, representing all d=3 bits set to 1.")
            .conclude("Each pair together covers all d=3 spatial dimensions.")
        )
    
    def model(self) -> Model:
        sums = [a + b for a, b in COMPLEMENTARY_PAIRS]
        all_7 = 1 if all(s == 7 for s in sums) else 0
        return (
            Model()
            .add("Number of pairs", len(COMPLEMENTARY_PAIRS))
            .add("All sums equal 7", all_7)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Number of pairs", 4)
            .add("All sums equal 7", 1)
        )


class PairsBinaryComplement(Test):
    """
    Each pair XORs to 7 (binary 111). This means each pair covers all 3 bits
    when combined: if one vertex has a 0 in a bit position, its complement
    has a 1 there.
    """
    name = "Pairs XOR to 111"
    question = (
        "XOR tells us which bits differ between two numbers. If complementary pairs differ "
        "in ALL bits, then XOR should give 111 (all three bits on). Does every pair pass "
        "this test? This is the bit-level proof that partners are truly opposite."
    )
    reference = "Theoretical (XOR complement)"
    tolerance = 0.001
    level = Standard
    commentary = (
        "XOR is like a 'difference detector.' Wherever two bits are the same, XOR gives 0. "
        "Wherever they differ, XOR gives 1. If two vertices are true complements, they "
        "differ in EVERY bit position, so XOR gives 111. This is beautiful: the algebraic "
        "operation XOR tells us the same thing as the geometric fact 'diagonally opposite.' "
        "Mathematics and geometry speak with one voice."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: XOR operation flips bits that differ, leaving bits that match as 0.")
            .step("For pair (n, 7-n), compute XOR: n XOR (7-n).")
            .step("Examples: 0 XOR 7 = 000 XOR 111 = 111 = 7; 3 XOR 4 = 011 XOR 100 = 111 = 7.")
            .step("For all 4 pairs, XOR result is 7 (111).")
            .step("This means every bit position differs between pair members.")
            .conclude("Perfect bit complementation; each pair covers all d=3 bit positions.")
        )
    
    def model(self) -> Model:
        xors = [a ^ b for a, b in COMPLEMENTARY_PAIRS]
        all_7 = 1 if all(x == 7 for x in xors) else 0
        return (
            Model()
            .add("All XORs equal 7", all_7)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("All XORs equal 7", 1)
        )


class PairsCrossTetrahedra(Test):
    """
    Each complementary pair has one vertex from Tet A and one from Tet B.
    This ensures that complementary vertices reside in opposite Field Chambers.
    """
    name = "Pairs Cross Field Chambers"
    question = (
        "Parity determines which tetrahedron you belong to. Complements flip all bits, "
        "which changes the parity. So does every complementary pair have one member in "
        "Tet A and one in Tet B? This would mean the two tetrahedra are perfectly woven "
        "together by their opposite corners."
    )
    reference = "Theoretical (dual structure)"
    tolerance = 0.001
    level = Standard
    commentary = (
        "This is how the dual structure locks together. Tet A holds odd-parity corners, "
        "Tet B holds even-parity corners. Complements always switch parity (flip 3 bits, "
        "change the 1-count by an odd amount). So if you are in Tet A, your complement "
        "is in Tet B. Every corner of each tetrahedron has a dance partner in the other. "
        "The two Field Chambers are not just overlapping shapes. They are interleaved "
        "like clasped hands."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Bit complementation flips all d=3 bits, changing parity (odd <-> even).")
            .step("Tet A = odd parity vertices {1,2,4,7}. Tet B = even parity vertices {0,3,5,6}.")
            .step("Check pair (0,7): 0 in Tet B, 7 in Tet A. Cross-chamber: yes.")
            .step("Check pair (1,6): 1 in Tet A, 6 in Tet B. Cross-chamber: yes.")
            .step("Similarly (2,5) and (3,4) cross chambers.")
            .conclude("All 4 pairs span both Field Chambers due to parity inversion.")
        )
    
    def model(self) -> Model:
        cross_count = 0
        for a, b in COMPLEMENTARY_PAIRS:
            tet_a = get_tetrahedron(a)
            tet_b = get_tetrahedron(b)
            if tet_a != tet_b:
                cross_count += 1
        return (
            Model()
            .add("Pairs crossing tetrahedra", cross_count)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Pairs crossing tetrahedra", 4)
        )


class Pair34CompletesFirst(Test):
    """
    When traversing with pi base-8, the (3,4) pair completes first. The digit
    3 goes to V3, and the next digit 1 takes cumsum to 4, completing the pair.
    This (3,4) encoding reflects 3+1 spacetime structure.
    """
    name = "(3,4) Pair Completes First"
    question = (
        "When we walk through the Field Chamber using pi's digits, which complementary "
        "pair do we complete first? Pi starts 3.1, so we visit V3, then V4. Since 3+4=7, "
        "they are complements. Does pi really complete this specific pair on its very "
        "first step?"
    )
    reference = "Pi = 3.14159..."
    tolerance = 0.001
    level = Standard
    commentary = (
        "Pi could have started any way, but it starts 3.1 in base 8. First stop: V3. "
        "Add 1: next stop is V4. These two are complements (3+4=7). So pi completes a "
        "cross-chamber pairing on its FIRST move. It links Tet A and Tet B immediately. "
        "And notice: 3+1=4=k, the tetrahedral number. Pi's opening move encodes the "
        "fundamental topology constant. We did not design this. Pi is a mathematical "
        "constant that predates our theory. It just happens to do this."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Pi = 3.14159... in base-8 begins 3.1..., immediately visiting V3 then V4.")
            .step("First digit 3: cumsum=3, vertex=V3 (Tet B).")
            .step("Second digit 1: cumsum=4, vertex=V4 (Tet A).")
            .step("Both V3 and V4 are now visited. Check: is (3,4) a complementary pair? 3+4=7. Yes.")
            .step("First complete pair is (3,4), encoding 3+1=k=4.")
            .conclude("Pi naturally completes the (3,4) pair first, linking to 3+1 spacetime structure.")
        )
    
    def model(self) -> Model:
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
        return (
            Model()
            .add("First pair is (3,4)", is_34)
            .add("Completion step", first_step if first_step else 0)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("First pair is (3,4)", 1)
            .add("Completion step", 1)
        )


class Pair34Correspondence(Test):
    """
    The (3,4) pair corresponds to the 3+1 structure: V3 is from Tet B
    and V4 is from Tet A. This is the first complementary pair completed
    when pi drives the traversal.
    """
    name = "(3,4) Pair Correspondence"
    question = (
        "V3 has binary code 011 (two 1-bits, even parity, so Tet B). V4 has binary code "
        "100 (one 1-bit, odd parity, so Tet A). Does the (3,4) pair actually cross from "
        "one tetrahedron to the other, establishing a link between both Field Chambers "
        "on pi's first step?"
    )
    reference = "Theoretical (dual structure)"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Let us verify. V3 is 011 in binary. Count the 1s: two. Two is even, so V3 "
        "belongs to Tet B. V4 is 100 in binary. Count the 1s: one. One is odd, so V4 "
        "belongs to Tet A. When pi moves from V3 to V4, it crosses from Tet B to Tet A. "
        "The dual Field Chambers become coupled on the very first transition. Pi does "
        "not wander around in one tetrahedron before finding the other. It connects them "
        "instantly."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Bimetric coupling requires interaction between both Field Chambers.")
            .step("Determine V3's Field Chamber: parity of 3 (011) = 2 ones = even -> Tet B.")
            .step("Determine V4's Field Chamber: parity of 4 (100) = 1 one = odd -> Tet A.")
            .step("First two vertices: V3 (Tet B) -> V4 (Tet A).")
            .step("This transition crosses Field Chambers at the very first step.")
            .conclude("Immediate bimetric coupling is established by the (3,4) pair structure.")
        )
    
    def model(self) -> Model:
        v3_is_tet_b = 1 if get_tetrahedron(3) == 'B' else 0
        v4_is_tet_a = 1 if get_tetrahedron(4) == 'A' else 0
        correct_encoding = 1 if v3_is_tet_b and v4_is_tet_a else 0
        return (
            Model()
            .add("V3 in Tet B (spatial)", v3_is_tet_b)
            .add("V4 in Tet A (temporal)", v4_is_tet_a)
            .add("Correct 3+1 encoding", correct_encoding)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("V3 in Tet B (spatial)", 1)
            .add("V4 in Tet A (temporal)", 1)
            .add("Correct 3+1 encoding", 1)
        )


class PairsGeometricallyOpposed(Test):
    """
    Each complementary pair sits at opposite corners of the cube. Geometrically,
    if vertex A is at coordinates (x, y, z), its complement is at (-x, -y, -z).
    """
    name = "Pairs Geometrically Opposed"
    question = (
        "If complementary means 'flip all bits,' does it also mean 'flip all spatial "
        "coordinates'? A vertex at (x, y, z) should have its complement at (-x, -y, -z). "
        "This would put them at maximum distance apart. Do all 4 pairs satisfy this?"
    )
    reference = "Cube geometry"
    tolerance = 0.001
    level = Standard
    commentary = (
        "Bits and coordinates are secretly the same thing. Bit 2 controls the x-sign, "
        "bit 1 controls y, bit 0 controls z. Flipping all bits flips all signs. So the "
        "complement of (1, -1, 1) is (-1, 1, -1). They are at opposite ends of the cube's "
        "space diagonal. The distance between them is 2*sqrt(3), the longest distance "
        "possible inside the cube. Complementary pairs are not just 'different.' They "
        "are MAXIMALLY different. They sit as far apart as geometry allows."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Cube corners have coordinates (+/-1, +/-1, +/-1). Opposite corners sum to (0,0,0).")
            .step("For each pair (n, 7-n), get coordinates of both vertices.")
            .step("Check if coords[n] = -coords[7-n] for all d=3 axes.")
            .step("Example: V0=(-1,-1,-1), V7=(+1,+1,+1). Sum: (0,0,0). Opposite: yes.")
            .step("Verify for all 4 pairs: each pair occupies antipodal cube corners.")
            .conclude("All complementary pairs are at maximum geometric separation (cube diagonal).")
        )
    
    def model(self) -> Model:
        opposed_count = 0
        for a, b in COMPLEMENTARY_PAIRS:
            a_coords = VERTICES[a]['coords']
            b_coords = VERTICES[b]['coords']
            is_opposite = all(a_coords[i] == -b_coords[i] for i in range(3))
            if is_opposite:
                opposed_count += 1
        return (
            Model()
            .add("Geometrically opposed pairs", opposed_count)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Geometrically opposed pairs", 4)
        )


class PairMidpointsAtOrigin(Test):
    """
    The midpoint of each complementary pair is the origin (0,0,0). This means
    the line connecting any pair passes through the center of the dual
    Field Chamber structure.
    """
    name = "Pair Midpoints at Origin"
    question = (
        "Take any complementary pair and find the point halfway between them. Is it "
        "always the origin (0,0,0)? If so, all four pairs are balanced around the center. "
        "The Field Origin would be the common midpoint of every diagonal."
    )
    reference = "Cube geometry"
    tolerance = 0.001
    level = Standard
    commentary = (
        "If V is at position P, its complement is at -P (flip all coordinates). The "
        "midpoint is (P + (-P)) / 2 = 0. Every complementary pair straddles the origin "
        "like a seesaw perfectly balanced at the fulcrum. All four diagonal lines through "
        "the cube cross at one point: the center. This is the Field Origin, the heart of "
        "the dual structure, equidistant from every extreme."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Midpoint of (A, B) is (A + B) / 2. For antipodal points, midpoint is origin.")
            .step("For pair (0,7): midpoint = (V0_coords + V7_coords) / 2 = ((-1,-1,-1) + (+1,+1,+1)) / 2 = (0,0,0).")
            .step("For pair (1,6): midpoint = (V1_coords + V6_coords) / 2 = ((-1,-1,+1) + (+1,+1,-1)) / 2 = (0,0,0).")
            .step("Similarly verify for pairs (2,5) and (3,4): all midpoints are (0,0,0).")
            .step("The origin is the Field Origin, geometric center of the stellated octahedron.")
            .conclude("All 4 complementary pair midpoints coincide at the Field Origin.")
        )
    
    def model(self) -> Model:
        at_origin_count = 0
        for a, b in COMPLEMENTARY_PAIRS:
            a_coords = np.array(VERTICES[a]['coords'])
            b_coords = np.array(VERTICES[b]['coords'])
            midpoint = (a_coords + b_coords) / 2
            if np.allclose(midpoint, [0, 0, 0]):
                at_origin_count += 1
        return (
            Model()
            .add("Midpoints at origin", at_origin_count)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Midpoints at origin", 4)
        )


class PiIntegerProduces34(Test):
    """
    Pi's first digit (3) goes directly to V3. The second digit (1) advances
    the cumsum to 4, landing on V4. Thus pi's integer part naturally produces
    the (3,4) pair that encodes spacetime structure.
    """
    name = "Pi Integer Produces (3,4)"
    question = (
        "Pi's value is fixed by mathematics. In base 8, it starts 3.1... When we use "
        "these digits to walk the cube, do we deterministically land on V3 then V4? "
        "No tuning, no choices. Just pi being pi."
    )
    reference = "Pi = 3.14159..."
    tolerance = 0.001
    level = Standard
    commentary = (
        "There is no parameter fitting here. Pi is what it is: the ratio of a circle's "
        "circumference to its diameter. In base 8, that ratio begins 3.110375... The "
        "integer part is 3, so start at V3. The first fractional digit is 1, so step to "
        "V4 (cumulative sum = 4). We did not choose these numbers. We did not adjust "
        "anything. Pi chooses them for us, and they happen to form a complementary pair "
        "that connects both tetrahedra. Either this is a coincidence, or pi encodes "
        "something about dual geometry."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PREMISE: Pi base-8 = 3.1103755... The integer part is 3, first fractional digit is 1.")
            .step("First digit is 3. Initial cumsum = 3. Vertex = 3 mod 8 = V3.")
            .step("Second digit is 1. Cumsum = 3 + 1 = 4. Vertex = 4 mod 8 = V4.")
            .step("First vertex: V3 (digit 3). Second vertex: V4 (digit 1).")
            .step("Sum: 3 + 1 = 4 = k. This is the topology constant.")
            .conclude("Pi's mathematical structure produces (V3, V4), encoding 3+1 = k.")
        )
    
    def model(self) -> Model:
        results = traverse_pi_base8(5)
        v1 = results[0]['vertex']  # Should be 3
        v2 = results[1]['vertex']  # Should be 4
        d1 = results[0]['digit']   # Should be 3
        d2 = results[1]['digit']   # Should be 1
        
        correct = 1 if v1 == 3 and v2 == 4 and d1 == 3 and d2 == 1 else 0
        return (
            Model()
            .add("First vertex", v1)
            .add("Second vertex", v2)
            .add("Produces (3,4)", correct)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("First vertex", 3)
            .add("Second vertex", 4)
            .add("Produces (3,4)", 1)
        )


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


def run_all() -> bool:
    """Run all complementary pairs tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
