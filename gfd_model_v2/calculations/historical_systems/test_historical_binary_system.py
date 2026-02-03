"""
Reference Systems: Binary Classification Validation

This module validates the mathematical properties of the binary vertex encoding
used in the dual Field Chamber. Tests verify complementary pair relationships,
parity classification, and the isomorphism between vertex indices and 3-bit
binary representations.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group


# =============================================================================
# CONSTANTS
# =============================================================================

TET_A = {1, 2, 4, 7}  # Odd parity vertices
TET_B = {0, 3, 5, 6}  # Even parity vertices

COMPLEMENTARY_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]

# Binary vertex encodings (3-bit representation)
BINARY_VERTICES = {
    0: {'binary': '000'},
    1: {'binary': '001'},
    2: {'binary': '010'},
    3: {'binary': '011'},
    4: {'binary': '100'},
    5: {'binary': '101'},
    6: {'binary': '110'},
    7: {'binary': '111'},
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_tetrahedron(v):
    return 'A' if v in TET_A else 'B'

def get_parity(v):
    return bin(v).count('1') % 2


# =============================================================================
# TEST CLASSES
# =============================================================================

class EightBinaryVertices(GFDTest):
    """8 binary encodings correspond to 8 vertices."""
    name = "Binary Vertex Count"
    question = (
        "Does the number of unique d-bit binary encodings (where d=k-1=3) equal the number of "
        "Coupling Port vertices (2k=8) in the dual Field Chamber?"
    )
    reference_source = "Binary counting (2^3 = 8)"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Chamber exists in d=k-1=3 spatial dimensions, with 2k=8 vertices. "
        "STEP 1: A d-bit binary number can encode 2^d distinct values. "
        "STEP 2: With d=3 bits: 2^3 = 8 unique encodings (000 through 111). "
        "STEP 3: The dual Field Chamber has 2k = 2×4 = 8 vertices. "
        "OUTPUT: Binary vertex count = 8."
    )
    commentary = (
        "The correspondence between 8 vertices and 3-bit binary encodings reflects the 2^3 structure of the Field "
        "Chamber coordinate system. This isomorphism suggests that the Coupling Port positions may be naturally "
        "represented in a binary framework."
    )
    
    def model(self):
        return {"Binary vertex count": len(BINARY_VERTICES)}
    
    def observations(self):
        return {"Binary vertex count": 8}


class BinaryEncodingIsomorphism(GFDTest):
    """Vertex binary encoding covers all 3-bit values."""
    name = "Binary Isomorphism"
    question = (
        "Is the mapping from vertex indices {0,1,2,3,4,5,6,7} to d=3-bit binary codes {000,...,111} "
        "a complete isomorphism with no gaps or duplicates?"
    )
    reference_source = "Binary representation theorem"
    tolerance = 0.01
    derivation = (
        "PREMISE: Each vertex index i ∈ {0,1,...,7} is assigned a binary code. "
        "STEP 1: The standard encoding assigns vertex i the binary representation of i itself. "
        "STEP 2: Enumerate: 0→000, 1→001, 2→010, 3→011, 4→100, 5→101, 6→110, 7→111. "
        "STEP 3: This covers all 2^d = 8 possible d-bit codes exactly once. "
        "OUTPUT: Binary sets match = 1."
    )
    commentary = (
        "The complete coverage of 3-bit values (000-111) establishes a bijection between binary coordinates and "
        "vertex positions. This correspondence is consistent with treating each spatial axis as a binary degree "
        "of freedom."
    )
    
    def model(self):
        vertex_binaries = {t['binary'] for t in BINARY_VERTICES.values()}
        expected_binaries = {format(v, '03b') for v in range(8)}
        match = vertex_binaries == expected_binaries
        return {"Binary sets match": 1 if match else 0}
    
    def observations(self):
        return {"Binary sets match": 1}


class ComplementaryPairsCorrespond(GFDTest):
    """Complementary pairs follow XOR with 7 pattern."""
    name = "Complementary Pairs"
    question = (
        "Do the k=4 complementary vertex pairs in the Field Chamber correspond to the binary complement "
        "operation (XOR with 2^d - 1 = 7), which geometrically represents body diagonals of the containing cube?"
    )
    reference_source = "Binary complement structure"
    tolerance = 0.01
    derivation = (
        "PREMISE: Two vertices are complementary if they lie on opposite corners of the cube (body diagonal). "
        "STEP 1: The binary complement of code B is NOT(B) = (2^d - 1) XOR B = 7 XOR B. "
        "STEP 2: Compute pairs: 0 XOR 7 = 7, 1 XOR 7 = 6, 2 XOR 7 = 5, 3 XOR 7 = 4. "
        "STEP 3: This yields pairs: (0,7), (1,6), (2,5), (3,4). "
        "STEP 4: Total pairs = 8/2 = k = 4, each connecting antipodal vertices. "
        "OUTPUT: Pairs match = 1."
    )
    commentary = (
        "The XOR-with-7 pattern for complementary pairs corresponds to the body diagonals of the containing cube. "
        "This relationship suggests that complementary vertices occupy positions of maximum spatial separation "
        "within the Field Chamber."
    )
    
    def model(self):
        # Complementary pairs have all bits inverted (XOR 7)
        computed_pairs = [(i, 7-i) for i in range(4)]
        our_pairs = set(tuple(sorted(p)) for p in COMPLEMENTARY_PAIRS)
        computed_set = set(tuple(sorted(p)) for p in computed_pairs)
        match = our_pairs == computed_set
        return {"Pairs match": 1 if match else 0}
    
    def observations(self):
        return {"Pairs match": 1}


class ParityClassificationMatch(GFDTest):
    """Bit-count parity matches tetrahedron assignment."""
    name = "Parity Classification"
    question = (
        "For all 2k=8 vertices, does the bit-count parity (number of 1s mod 2) of each binary code "
        "correctly determine assignment to Tetrahedron A (odd parity) or Tetrahedron B (even parity)?"
    )
    reference_source = "Parity classification"
    tolerance = 0.01
    derivation = (
        "PREMISE: Tetrahedron A = {vertices with odd number of 1-bits}; Tetrahedron B = {even number}. "
        "STEP 1: Count 1-bits for each vertex: 0(0), 1(1), 2(1), 3(2), 4(1), 5(2), 6(2), 7(3). "
        "STEP 2: Odd parity vertices: {1, 2, 4, 7} → Tetrahedron A. "
        "STEP 3: Even parity vertices: {0, 3, 5, 6} → Tetrahedron B. "
        "STEP 4: Each tetrahedron has exactly k=4 vertices. "
        "OUTPUT: Parity matches = 8."
    )
    commentary = (
        "The alignment between bit-count parity and tetrahedron assignment is consistent with the geometric "
        "definition of Tetrahedron A and Tetrahedron B. This correspondence may indicate that the binary "
        "coordinate system naturally encodes the dual structure."
    )
    
    def model(self):
        matches = 0
        for v in range(8):
            our_parity = 1 if get_tetrahedron(v) == 'A' else 0
            bit_count = BINARY_VERTICES[v]['binary'].count('1')
            binary_parity = bit_count % 2
            if our_parity == binary_parity:
                matches += 1
        return {"Parity matches": matches}
    
    def observations(self):
        return {"Parity matches": 8}


class ApexCorrespondence(GFDTest):
    """Pure forms (000, 111) correspond to apex vertices."""
    name = "Apex Correspondence"
    question = (
        "Do the binary extrema—vertex 0 (code 000) and vertex 7 (code 111)—belong to opposite tetrahedra, "
        "confirming that the 'pure states' of the binary encoding are assigned to complementary structures?"
    )
    reference_source = "Binary extrema"
    tolerance = 0.01
    derivation = (
        "PREMISE: Vertex 0 has code 000 (all zeros); Vertex 7 has code 111 (all ones). "
        "STEP 1: Bit-count of 000 is 0 (even parity) → Vertex 0 ∈ Tetrahedron B. "
        "STEP 2: Bit-count of 111 is 3 (odd parity) → Vertex 7 ∈ Tetrahedron A. "
        "STEP 3: These vertices are complementary: 0 XOR 7 = 7 (full complement). "
        "STEP 4: They occupy opposite corners of the cube (body diagonal). "
        "OUTPUT: All apex correspondences correct = 1."
    )
    commentary = (
        "The correspondence of vertices 0 (000) and 7 (111) to opposite tetrahedra reflects their positions as "
        "binary extrema. These vertices correspond to the pure-state endpoints of the 3-bit coordinate space."
    )
    
    def model(self):
        v0_is_000 = BINARY_VERTICES[0]['binary'] == '000'
        v7_is_111 = BINARY_VERTICES[7]['binary'] == '111'
        v0_is_tet_b = 0 in TET_B
        v7_is_tet_a = 7 in TET_A
        all_correct = v0_is_000 and v7_is_111 and v0_is_tet_b and v7_is_tet_a
        return {"All apex correspondences correct": 1 if all_correct else 0}
    
    def observations(self):
        return {"All apex correspondences correct": 1}


class ComplementaryPairXOR(GFDTest):
    """The (3,4) pair demonstrates XOR complement relationship."""
    name = "(3,4) Pair XOR"
    question = (
        "Does the complementary pair (3, 4) satisfy the defining XOR relationship: 3 XOR 4 = 2^d - 1 = 7, "
        "confirming that their binary codes are bitwise complements?"
    )
    reference_source = "Binary arithmetic"
    tolerance = 0.01
    derivation = (
        "PREMISE: Two vertices form a complementary pair if their XOR equals 2^d - 1 = 7. "
        "STEP 1: Vertex 3 has binary code 011; Vertex 4 has binary code 100. "
        "STEP 2: Compute XOR bit-by-bit: 0⊕1=1, 1⊕0=1, 1⊕0=1 → result = 111 = 7. "
        "STEP 3: Verify: 3 + 4 = 7 (sum equals 2^d - 1, confirming complementarity). "
        "OUTPUT: 3 XOR 4 = 7."
    )
    commentary = (
        "The (3, 4) pair XOR yielding 7 demonstrates the full complement relationship between binary codes 011 "
        "and 100. This arithmetic property is consistent with the spatial opposition of these vertices across "
        "the Field Origin."
    )
    
    def model(self):
        xor_result = 3 ^ 4
        return {"3 XOR 4": xor_result}
    
    def observations(self):
        return {"3 XOR 4": 7}


class AllPairsCrossTetrahedra(GFDTest):
    """All complementary pairs cross tetrahedra boundaries."""
    name = "Cross-Tetrahedra Pairs"
    question = (
        "For each of the k=4 complementary vertex pairs, does one member belong to Tetrahedron A and "
        "the other to Tetrahedron B, confirming that body diagonals always connect the dual structures?"
    )
    reference_source = "Dual Field Chamber geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Complementary pairs are: (0,7), (1,6), (2,5), (3,4). "
        "STEP 1: The XOR operation flips all bits, which changes the parity of the bit-count. "
        "STEP 2: If vertex v has even parity, then v XOR 7 has odd parity (and vice versa). "
        "STEP 3: Therefore, complementary vertices always have opposite parities. "
        "STEP 4: Since parity determines tetrahedron membership, each pair spans both tetrahedra. "
        "OUTPUT: Pairs crossing tetrahedra = 4."
    )
    commentary = (
        "The universal crossing of complementary pairs between Tetrahedron A and Tetrahedron B reflects the "
        "interlocking nature of the dual structure. This property is consistent with the definition of "
        "complementary vertices as occupying opposite tetrahedra."
    )
    
    def model(self):
        cross_count = 0
        for v1, v2 in COMPLEMENTARY_PAIRS:
            if get_tetrahedron(v1) != get_tetrahedron(v2):
                cross_count += 1
        return {"Pairs crossing tetrahedra": cross_count}
    
    def observations(self):
        return {"Pairs crossing tetrahedra": 4}


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    EightBinaryVertices,
    BinaryEncodingIsomorphism,
    ComplementaryPairsCorrespond,
    ParityClassificationMatch,
    ApexCorrespondence,
    ComplementaryPairXOR,
    AllPairsCrossTetrahedra,
]


def run_all_tests():
    """Run all binary classification tests."""
    return run_test_group(
        title="Binary Classification Validation",
        summary=(
            "These tests validate the mathematical properties of the binary vertex "
            "encoding in the dual Field Chamber. The 3-bit binary representation "
            "produces consistent complementary pairs, parity classification, and "
            "tetrahedra assignment."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
