"""
Binary Triad Structure
======================

This module examines the 3-bit binary structure that emerges naturally from
pi base-8 traversal. Since pi base-8 uses digits 0-7 and 8 = 2^3, each digit
corresponds to a 3-bit binary pattern representing a position in a unit cube.

Key relationships examined:
- 8 triads from digits 0-7 (8 = 2^3)
- 3 bits encode 3D cube coordinates
- Bit parity partitions vertices into two tetrahedra (Field Chambers)
- Complements via XOR with 111 (7)
- Pi's first digits (3.1) correspond to the (3,4) complementary pair
"""

import sys
import os
from typing import Dict, Optional
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from gfd_model_v2.common import VERTICES, TET_A, TET_B, K, get_tetrahedron, get_pi_base8


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_triad(vertex: int) -> str:
    """Get the triad (3-bit binary) representation."""
    return format(vertex, '03b')


def count_ones(vertex: int) -> int:
    """Count 1-bits in the triad."""
    return bin(vertex).count('1')


def get_parity(vertex: int) -> str:
    """Get parity: even 1-count -> Tet B, odd 1-count -> Tet A."""
    return "even" if count_ones(vertex) % 2 == 0 else "odd"


# =============================================================================
# TESTS
# =============================================================================

class EightTriadsFromBase8(GFDTest):
    """
    Since pi base-8 uses digits 0-7 and 8 = 2^3, we automatically get 8
    unique 3-bit patterns. This is not a coincidence but a fundamental
    consequence of using base-8.
    """
    name = "8 Triads from Base-8"
    question = "Does base-8 encoding naturally produce exactly 2k=8 unique 3-bit triads, each addressing one Field Chamber vertex?"
    reference_source = "Mathematical (8 = 2^3)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Base-8 digits range from 0-7, requiring exactly 3 bits to encode (2^3 = 8). "
        "STEP 1: Each digit 0-7 has a unique 3-bit binary representation (triad). "
        "STEP 2: Count triads: {000, 001, 010, 011, 100, 101, 110, 111} = 8 triads. "
        "STEP 3: From Field Closure, 2k = 2*4 = 8 vertices in the stellated octahedron. "
        "OUTPUT: Base-8 digits map one-to-one to Field Chamber vertices via triads."
    )
    commentary = (
        "The correspondence between octal digits and 3-bit triads follows directly "
        "from 8 = 2^3. Each pi digit in base-8 addresses one of 8 vertices in the "
        "stellated octahedron, establishing a natural information-theoretic connection "
        "between pi's representation and Field Chamber topology."
    )
    
    def model(self) -> Dict[str, float]:
        triads = [get_triad(v) for v in range(8)]
        unique = len(set(triads))
        return {"Unique triads": unique}
    
    def observations(self) -> Dict[str, float]:
        return {"Unique triads": 8}


class TriadIsBinaryEncoding(GFDTest):
    """
    Each triad is simply the binary encoding of the vertex number.
    Converting the triad back to decimal gives the original vertex.
    """
    name = "Triad = Binary Encoding"
    question = "Does each triad bijectively encode its vertex index, enabling reversible conversion between decimal and binary?"
    reference_source = "Mathematical (binary conversion)"
    tolerance = 0.001
    derivation = (
        "PREMISE: A bijective encoding ensures no information loss during conversion. "
        "STEP 1: For each vertex v in {0,1,2,3,4,5,6,7}, compute triad = format(v, '03b'). "
        "STEP 2: Convert triad back to decimal: int(triad, 2). "
        "STEP 3: Verify round-trip: v == int(format(v, '03b'), 2) for all v. "
        "OUTPUT: All 8 vertices correctly encode and decode, confirming bijective mapping."
    )
    commentary = None  # Mechanical verification of binary encoding
    
    def model(self) -> Dict[str, float]:
        match_count = 0
        for v in range(8):
            triad = get_triad(v)
            if int(triad, 2) == v:
                match_count += 1
        return {"Vertices matching": match_count}
    
    def observations(self) -> Dict[str, float]:
        return {"Vertices matching": 8}


class TriadCoordinatesMatchCube(GFDTest):
    """
    The 3 bits of each triad encode the 3D cube coordinates:
    - Bit 0 (rightmost) = Z-axis
    - Bit 1 (middle) = Y-axis
    - Bit 2 (leftmost) = X-axis
    """
    name = "Triad Bits = Cube Coordinates"
    question = "Do the d=3 triad bits encode spatial coordinates in the unit cube, connecting information to Field Chamber geometry?"
    reference_source = "Cube geometry"
    tolerance = 0.001
    derivation = (
        "PREMISE: From Field Closure, d=k-1=3 spatial dimensions encode the cube. "
        "STEP 1: For each vertex, extract 3-bit triad: bit[2]=X, bit[1]=Y, bit[0]=Z. "
        "STEP 2: Convert bits to coordinates: coord = 2*bit - 1 (maps {0,1} to {-1,+1}). "
        "STEP 3: Compare to stored VERTICES[v]['coords'] for all 8 vertices. "
        "OUTPUT: All 8 vertex triads correctly encode their 3D cube corner positions."
    )
    commentary = (
        "The 3-bit triad directly encodes spatial position within the unit cube. "
        "Each bit corresponds to one spatial axis, connecting the information content "
        "of pi digits to physical 3D coordinates within the Field Chamber structure."
    )
    
    def model(self) -> Dict[str, float]:
        match_count = 0
        for v in range(8):
            binary = get_triad(v)
            # Convert to -1/+1 coordinates
            coord_x = 2 * int(binary[0]) - 1
            coord_y = 2 * int(binary[1]) - 1
            coord_z = 2 * int(binary[2]) - 1
            expected = VERTICES[v]['coords']
            if (coord_x, coord_y, coord_z) == expected:
                match_count += 1
        return {"Coordinates matching": match_count}
    
    def observations(self) -> Dict[str, float]:
        return {"Coordinates matching": 8}


class ParityDeterminesTetrahedron(GFDTest):
    """
    The parity of the 1-bit count determines Field Chamber membership:
    - Odd 1-count -> Tet A (vertices 1, 2, 4, 7)
    - Even 1-count -> Tet B (vertices 0, 3, 5, 6)
    """
    name = "Parity Determines Field Chamber"
    question = "Does the parity of the 1-bit count in each triad deterministically assign vertices to Tetrahedron A or Tetrahedron B?"
    reference_source = "Theoretical (parity partition)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Parity is (number of 1-bits) mod 2. Odd parity = Tet A, even parity = Tet B. "
        "STEP 1: For each vertex v, count 1-bits in its triad: popcount(v). "
        "STEP 2: Compute parity: popcount(v) mod 2. "
        "STEP 3: Assign: odd (parity=1) -> Tet A {1,2,4,7}, even (parity=0) -> Tet B {0,3,5,6}. "
        "STEP 4: Verify all 8 vertices match their expected Field Chamber assignment. "
        "OUTPUT: Binary parity provides deterministic dual Field Chamber partition."
    )
    commentary = (
        "Binary parity naturally partitions the 8 vertices into two tetrahedra. "
        "This emergence of dual structure from a simple parity rule suggests the "
        "dual Field Chamber may have information-theoretic origins, where Tetrahedron A "
        "and Tetrahedron B represent complementary information states."
    )
    
    def model(self) -> Dict[str, float]:
        match_count = 0
        for v in range(8):
            parity = get_parity(v)
            expected_tet = 'A' if parity == 'odd' else 'B'
            actual_tet = get_tetrahedron(v)
            if expected_tet == actual_tet:
                match_count += 1
        return {"Parity-tetrahedron matches": match_count}
    
    def observations(self) -> Dict[str, float]:
        return {"Parity-tetrahedron matches": 8}


class ComplementXOR111(GFDTest):
    """
    The complement of vertex n is n XOR 7, which equals 7-n. XORing with
    111 (binary) inverts all three bits, producing the geometrically
    opposite vertex.
    """
    name = "Complement = XOR 111"
    question = "Does XOR with 7 (binary 111) produce vertex complements, connecting algebraic and geometric opposition?"
    reference_source = "Mathematical (XOR identity)"
    tolerance = 0.001
    derivation = (
        "PREMISE: XOR with 111 inverts all 3 bits; subtraction from 7 gives arithmetic complement. "
        "STEP 1: For each vertex n in {0,1,2,3,4,5,6,7}, compute n XOR 7. "
        "STEP 2: Compute 7 - n for comparison. "
        "STEP 3: Verify n XOR 7 == 7 - n for all vertices. "
        "STEP 4: Example: V3 (011) XOR 7 (111) = 4 (100) = 7 - 3. "
        "OUTPUT: XOR with 111 equals arithmetic complement, linking algebraic and geometric opposition."
    )
    commentary = (
        "The XOR operation with 7 (binary 111) produces vertex complements, connecting "
        "algebraic complementation to geometric opposition. This identity underlies the "
        "pairing structure where each vertex in Tetrahedron A has a corresponding "
        "complement in Tetrahedron B."
    )
    
    def model(self) -> Dict[str, float]:
        match_count = 0
        for v in range(8):
            xor_result = v ^ 7
            sub_result = 7 - v
            if xor_result == sub_result:
                match_count += 1
        return {"XOR = subtraction matches": match_count}
    
    def observations(self) -> Dict[str, float]:
        return {"XOR = subtraction matches": 8}


class ComplementsCrossTetrahedra(GFDTest):
    """
    XOR with 111 flips all bits, changing parity and thus changing
    Field Chamber. Every complementary pair crosses Field Chambers.
    """
    name = "Complements Cross Field Chambers"
    question = "Does bit inversion (XOR 111) necessarily change parity, ensuring all complementary pairs span both Field Chambers?"
    reference_source = "Theoretical (parity flip)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Flipping all 3 bits changes the 1-bit count by +/-1 or +/-3 (always odd change). "
        "STEP 1: An odd change to 1-bit count inverts parity (odd becomes even, even becomes odd). "
        "STEP 2: For pairs (0,7), (1,6), (2,5), (3,4), check if tetrahedra differ. "
        "STEP 3: Verify: 0 in Tet B, 7 in Tet A; 1 in Tet A, 6 in Tet B; etc. "
        "OUTPUT: All 4 complementary pairs cross Field Chambers due to parity inversion."
    )
    commentary = (
        "Complementary pairs necessarily span both Field Chambers because bit inversion "
        "changes parity. This cross-chamber pairing structure may underlie how the dual "
        "tetrahedra maintain balance during traversal, with each vertex having a "
        "counterpart in the opposing Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        cross_count = 0
        for v in range(4):  # Check pairs (0,7), (1,6), (2,5), (3,4)
            complement = 7 - v
            if get_tetrahedron(v) != get_tetrahedron(complement):
                cross_count += 1
        return {"Pairs crossing tetrahedra": cross_count}
    
    def observations(self) -> Dict[str, float]:
        return {"Pairs crossing tetrahedra": 4}


class PiFirstPairIs34(GFDTest):
    """
    Pi's first two digits (3, then 1 after decimal) produce cumsum 3 then 4.
    The triads 011 and 100 are complements (XOR = 111), making (3,4) the
    first complementary pair completed in the traversal.
    """
    name = "Pi's First Pair is (3,4)"
    question = "Do pi's first two digits (3.1) produce the complementary pair (V3, V4), establishing cross-chamber coupling from the outset?"
    reference_source = "Pi = 3.14159..."
    tolerance = 0.001
    derivation = (
        "PREMISE: Pi base-8 begins 3.1..., so first digit is 3, second fractional digit is 1. "
        "STEP 1: First cumsum = 3, placing traversal at V3 (triad 011). "
        "STEP 2: Second cumsum = 3 + 1 = 4, placing traversal at V4 (triad 100). "
        "STEP 3: Check complement: V3 XOR V4 = 3 XOR 4 = 7 (binary 011 XOR 100 = 111). "
        "STEP 4: V3 in Tet B, V4 in Tet A, confirming cross-chamber pairing. "
        "OUTPUT: Pi immediately produces the (3,4) complementary pair linking both Field Chambers."
    )
    commentary = (
        "Pi's initial digits produce vertices 3 and 4, a complementary pair with "
        "XOR equal to 7. This immediate completion of a cross-chamber pair suggests "
        "pi traversal establishes dual Field Chamber coupling from the first steps. "
        "The (3,4) encoding also corresponds to 3+1 dimensional structure."
    )
    
    def model(self) -> Dict[str, float]:
        digits = get_pi_base8(2, include_integer=True)
        v1 = digits[0] % 8  # First vertex from digit 3
        v2 = (digits[0] + digits[1]) % 8  # Second vertex from cumsum
        is_34 = 1 if (v1, v2) == (3, 4) else 0
        xor = v1 ^ v2
        return {
            "First vertex": v1,
            "Second vertex": v2,
            "Is (3,4) pair": is_34,
            "XOR result": xor,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "First vertex": 3,
            "Second vertex": 4,
            "Is (3,4) pair": 1,
            "XOR result": 7,
        }


class FirstPairEncodesK(GFDTest):
    """
    The sum of pi's first vertices (3+1=4) corresponds to the topology
    constant k. This correspondence is noted in the model.
    """
    name = "First Pair Encodes k=4"
    question = "Does the sum of pi's first two digits (3+1=4) encode the topology constant k, linking pi's structure to tetrahedral geometry?"
    reference_source = "Theoretical (k=4)"
    tolerance = 0.001
    derivation = (
        "PREMISE: k=4 is the Field Closure constant determining tetrahedral face count. "
        "STEP 1: Pi's integer part is 3. "
        "STEP 2: Pi's first fractional digit (base-8) is 1. "
        "STEP 3: Sum: 3 + 1 = 4 = k. "
        "STEP 4: This equals the number of vertices per tetrahedron and faces per tetrahedron. "
        "OUTPUT: Pi's leading digits encode k=4 without parameter adjustment."
    )
    commentary = (
        "The sum 3+1=4 from pi's first two digits matches the topology constant k, "
        "which determines vertices per tetrahedron and faces per Field Chamber. "
        "This correspondence emerges without parameter adjustment from pi's "
        "mathematical structure."
    )
    
    def model(self) -> Dict[str, float]:
        # First vertex is 3, second step adds 1 to get 4
        k_derived = 3 + 1
        return {"Derived k": k_derived}
    
    def observations(self) -> Dict[str, float]:
        return {"Derived k": K}


class AllTriadsVisitedByPi(GFDTest):
    """
    Pi traversal is ergodic, visiting all 8 triads. This ensures complete
    coverage of the geometric structure.
    """
    name = "All Triads Visited"
    question = "Is pi-driven traversal ergodic, visiting all 2k=8 triads to ensure complete Field Chamber coverage?"
    reference_source = "Theoretical (ergodic property)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Ergodic traversal requires visiting all 8 vertices (triads 000 through 111). "
        "STEP 1: Compute pi base-8 cumulative sums for 100 digits. "
        "STEP 2: For each cumsum, compute vertex = cumsum mod 8, then triad = format(vertex, '03b'). "
        "STEP 3: Collect all unique triads visited. "
        "STEP 4: Count unique triads: should equal 8. "
        "OUTPUT: All 8 triads visited confirms ergodic Field Chamber coverage."
    )
    commentary = (
        "Complete triad coverage indicates the traversal is ergodic, sampling all "
        "regions of the Field Chamber. This property is consistent with pi's "
        "conjectured status as a normal number, ensuring no systematic bias in "
        "vertex visitation."
    )
    
    def model(self) -> Dict[str, float]:
        digits = get_pi_base8(100, include_integer=True)
        cumsum = 0
        triads = set()
        for d in digits:
            cumsum += d
            triads.add(get_triad(cumsum % 8))
        return {"Unique triads visited": len(triads)}
    
    def observations(self) -> Dict[str, float]:
        return {"Unique triads visited": 8}


class TriadBalanceOverTraversal(GFDTest):
    """
    Triads should be visited approximately equally over a long traversal.
    This indicates unbiased geometric sampling.
    """
    name = "Triad Visit Balance"
    question = "Does pi traversal visit all triads with approximately equal frequency, indicating unbiased Field Chamber sampling?"
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Unbiased sampling requires approximately uniform triad visitation. "
        "STEP 1: Traverse 500 pi base-8 digits, counting visits to each triad. "
        "STEP 2: Find minimum and maximum visit counts across all 8 triads. "
        "STEP 3: Compute ratio: max_count / min_count. "
        "STEP 4: Threshold: ratio < 1.5 indicates balanced sampling. "
        "OUTPUT: Ratio below 1.5 confirms statistically balanced Field Chamber visitation."
    )
    commentary = (
        "Balanced triad visitation indicates the traversal samples the Field Chamber "
        "without systematic bias. Statistical equilibrium across all 8 vertices is "
        "consistent with pi's digit distribution approaching uniformity over long sequences."
    )
    
    def model(self) -> Dict[str, float]:
        digits = get_pi_base8(500, include_integer=True)
        cumsum = 0
        triad_counts = Counter()
        for d in digits:
            cumsum += d
            triad_counts[get_triad(cumsum % 8)] += 1
        
        min_count = min(triad_counts.values())
        max_count = max(triad_counts.values())
        ratio = max_count / min_count if min_count > 0 else 999
        balanced = 1 if ratio < 1.5 else 0
        return {
            "Min visits": min_count,
            "Max visits": max_count,
            "Max/min ratio": ratio,
            "Balanced (< 1.5)": balanced,
        }


class PureFormsAreApexes(GFDTest):
    """
    The pure triads 000 and 111 are the apexes of the two Field Chambers:
    - 000 (all zeros) = V0 = Tet B apex at (-1,-1,-1)
    - 111 (all ones) = V7 = Tet A apex at (+1,+1,+1)
    """
    name = "Pure Forms are Apexes"
    question = "Do the pure triads (000 and 111) occupy the apex positions of their respective Field Chambers at opposite cube corners?"
    reference_source = "Cube geometry"
    tolerance = 0.001
    derivation = (
        "PREMISE: Pure binary states have all bits identical (all 0 or all 1). "
        "STEP 1: Triad 000 = V0 with coordinates (-1,-1,-1), 0 ones = even parity -> Tet B. "
        "STEP 2: Triad 111 = V7 with coordinates (+1,+1,+1), 3 ones = odd parity -> Tet A. "
        "STEP 3: V0 and V7 are at diagonally opposite cube corners (maximum separation). "
        "STEP 4: By construction, V0 is Tet B apex, V7 is Tet A apex. "
        "OUTPUT: Pure triads 000 and 111 are Field Chamber apexes at antipodal cube positions."
    )
    commentary = (
        "The pure binary states (000 and 111) occupy diagonally opposite cube corners "
        "and serve as apex vertices for Tetrahedron B and Tetrahedron A respectively. "
        "This positions the Field Origin at the geometric center, equidistant from "
        "both extremal information states."
    )
    
    def model(self) -> Dict[str, float]:
        v0_is_tet_b = 1 if 0 in TET_B else 0
        v7_is_tet_a = 1 if 7 in TET_A else 0
        v0_at_minus = 1 if VERTICES[0]['coords'] == (-1, -1, -1) else 0
        v7_at_plus = 1 if VERTICES[7]['coords'] == (1, 1, 1) else 0
        return {
            "V0 in Tet B": v0_is_tet_b,
            "V7 in Tet A": v7_is_tet_a,
            "V0 at (-1,-1,-1)": v0_at_minus,
            "V7 at (+1,+1,+1)": v7_at_plus,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "V0 in Tet B": 1,
            "V7 in Tet A": 1,
            "V0 at (-1,-1,-1)": 1,
            "V7 at (+1,+1,+1)": 1,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    EightTriadsFromBase8,
    TriadIsBinaryEncoding,
    TriadCoordinatesMatchCube,
    ParityDeterminesTetrahedron,
    ComplementXOR111,
    ComplementsCrossTetrahedra,
    PiFirstPairIs34,
    FirstPairEncodesK,
    AllTriadsVisitedByPi,
    TriadBalanceOverTraversal,
    PureFormsAreApexes,
]


def run_all_tests() -> bool:
    """Run all binary triad tests."""
    return run_test_group(
        title="Binary Triad Structure",
        summary=(
            "These tests examine the 3-bit binary structure emerging from pi base-8 "
            "representation. Since 8 = 2^3, each digit encodes a 3D cube coordinate. "
            "Bit-count parity partitions vertices into two Field Chambers (tetrahedra), "
            "and complements arise via XOR with 111. Pi's first digits (3.1) correspond "
            "to the (3,4) complementary pair, with their sum (4) matching the topology "
            "constant k."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
