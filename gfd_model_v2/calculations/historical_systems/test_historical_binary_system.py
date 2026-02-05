"""
Binary Vertex Encoding: Coordinate Structure of the Dual Field Chamber

This module validates the mathematical properties of the binary vertex encoding
in the dual Field Chamber. The key insight is simple: a cube has 8 vertices,
and 8 = 2^3, so we can label each vertex with a 3-bit binary number.

THE PHYSICAL CLAIM:
The two tetrahedra (A and B) that form the stellated octahedron are distinguished
by the parity of their vertex labels. Tet A contains vertices with an odd number
of 1-bits, Tet B contains vertices with an even number of 1-bits. This is not
mystical, it is just how the geometry works.

WHY THIS MATTERS:
This binary structure connects the Field Chamber geometry to information theory.
Each vertex can be thought of as a state in a 3-bit register, and the two
tetrahedra correspond to the two parity classes. This is the same structure
used in error-correcting codes.
"""

from gfd_model_v2.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

# The two tetrahedra are distinguished by bit-count parity
TET_A = {1, 2, 4, 7}  # Odd parity: 001, 010, 100, 111
TET_B = {0, 3, 5, 6}  # Even parity: 000, 011, 101, 110

# Complementary pairs are connected by body diagonals of the cube
COMPLEMENTARY_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]


# =============================================================================
# TEST CLASSES
# =============================================================================

class BinaryVertexCount(Test):
    """8 vertices = 2^3 binary encodings."""
    name = "Binary Vertex Count"
    level = Level.STANDARD
    question = (
        "The cube has 8 vertices, and 8 = 2^3. Does each vertex correspond "
        "to a unique 3-bit binary number from 000 to 111?"
    )
    reference = "Basic combinatorics: 2^d states in d dimensions"
    tolerance = 0.01
    commentary = (
        "This is straightforward counting. A cube vertex can be at +1 or -1 "
        "along each of 3 axes, giving 2 x 2 x 2 = 8 possibilities. We encode "
        "+1 as bit 1, and -1 as bit 0."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("A cube exists in d=3 dimensions.")
            .step("Each coordinate can be +1 or -1 (2 choices per axis).")
            .step("Total vertices = 2^d = 2^3 = 8.")
            .step("These map to binary codes 000, 001, 010, ..., 111.")
            .conclude("Binary vertex count = 8.")
        )
    
    def model(self):
        d = 3
        vertex_count = 2 ** d
        return Model().add("Binary vertex count", vertex_count)
    
    def observations(self):
        return Observed().add("Binary vertex count", 8)


class ParityDeterminesTetrahedron(Test):
    """Bit-count parity determines tetrahedron membership."""
    name = "Parity Classification"
    level = Level.STANDARD
    question = (
        "Does the parity of the bit count (number of 1s mod 2) correctly "
        "classify vertices into Tetrahedron A (odd) and Tetrahedron B (even)?"
    )
    reference = "Parity check codes in information theory"
    tolerance = 0.01
    commentary = (
        "This is the key structural result. The two tetrahedra that interlock "
        "to form the stellated octahedron are exactly the two parity classes "
        "of the 3-bit binary encoding. No coincidence: alternate vertices of "
        "a cube always form a tetrahedron."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Count 1-bits for each vertex index:")
            .step("  0 (000): 0 ones -> even -> Tet B")
            .step("  1 (001): 1 one  -> odd  -> Tet A")
            .step("  2 (010): 1 one  -> odd  -> Tet A")
            .step("  3 (011): 2 ones -> even -> Tet B")
            .step("  4 (100): 1 one  -> odd  -> Tet A")
            .step("  5 (101): 2 ones -> even -> Tet B")
            .step("  6 (110): 2 ones -> even -> Tet B")
            .step("  7 (111): 3 ones -> odd  -> Tet A")
            .conclude("Parity matches = 8 (all vertices correctly classified).")
        )
    
    def model(self):
        matches = 0
        for v in range(8):
            bit_parity = bin(v).count('1') % 2  # 1 = odd, 0 = even
            expected_tet_a = (bit_parity == 1)
            actual_tet_a = (v in TET_A)
            if expected_tet_a == actual_tet_a:
                matches += 1
        return Model().add("Parity matches", matches)
    
    def observations(self):
        return Observed().add("Parity matches", 8)


class ComplementaryPairsXOR(Test):
    """Complementary vertices differ by XOR with 7 (all bits flipped)."""
    name = "Complementary Pairs XOR"
    level = Level.STANDARD
    question = (
        "The 4 body diagonals of the cube connect complementary vertices. "
        "Are these pairs exactly the vertices related by v XOR 7 (bit complement)?"
    )
    reference = "Cube body diagonals pass through center"
    tolerance = 0.01
    commentary = (
        "The XOR operation with 7 (binary 111) flips all bits. Geometrically, "
        "this maps each vertex to the opposite corner of the cube. These "
        "antipodal pairs form the body diagonals, and each pair contains "
        "one vertex from Tet A and one from Tet B."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Compute v XOR 7 for v = 0, 1, 2, 3:")
            .step("  0 XOR 7 = 7  -> pair (0, 7)")
            .step("  1 XOR 7 = 6  -> pair (1, 6)")
            .step("  2 XOR 7 = 5  -> pair (2, 5)")
            .step("  3 XOR 7 = 4  -> pair (3, 4)")
            .step("These are exactly the 4 body diagonals of the cube.")
            .conclude("All 4 complementary pairs follow XOR pattern.")
        )
    
    def model(self):
        computed_pairs = [(i, i ^ 7) for i in range(4)]
        our_pairs = set(tuple(sorted(p)) for p in COMPLEMENTARY_PAIRS)
        computed_set = set(tuple(sorted(p)) for p in computed_pairs)
        match = (our_pairs == computed_set)
        return Model().add("Pairs match XOR pattern", 1 if match else 0)
    
    def observations(self):
        return Observed().add("Pairs match XOR pattern", 1)


class ComplementaryPairsCrossTetrahedra(Test):
    """Each complementary pair has one vertex in Tet A, one in Tet B."""
    name = "Cross-Tetrahedra Pairs"
    level = Level.STANDARD
    question = (
        "Since XOR with 7 flips all bits, it changes the parity. Does this "
        "mean every complementary pair connects Tet A to Tet B?"
    )
    reference = "Parity flip under bit complement"
    tolerance = 0.01
    commentary = (
        "Flipping all 3 bits changes the bit count by +/- 3, 1, or some odd "
        "number. Since 3 is odd, the parity always flips. Therefore, if v is "
        "in Tet A (odd parity), then v XOR 7 is in Tet B (even parity)."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("XOR with 7 flips all bits.")
            .step("If v has k ones, then v XOR 7 has (3-k) ones.")
            .step("k and (3-k) have opposite parity (one odd, one even).")
            .step("Therefore complementary vertices are in opposite tetrahedra.")
            .conclude("Pairs crossing tetrahedra = 4 (all of them).")
        )
    
    def model(self):
        cross_count = 0
        for v1, v2 in COMPLEMENTARY_PAIRS:
            tet_v1 = 'A' if v1 in TET_A else 'B'
            tet_v2 = 'A' if v2 in TET_A else 'B'
            if tet_v1 != tet_v2:
                cross_count += 1
        return Model().add("Pairs crossing tetrahedra", cross_count)
    
    def observations(self):
        return Observed().add("Pairs crossing tetrahedra", 4)


class FourVerticesPerTetrahedron(Test):
    """Each tetrahedron has exactly k=4 vertices."""
    name = "Tetrahedron Vertex Count"
    level = Level.STANDARD
    question = (
        "A regular tetrahedron has 4 vertices. Do both Tet A and Tet B "
        "have exactly 4 vertices each?"
    )
    reference = "Tetrahedron definition"
    tolerance = 0.01
    commentary = (
        "The 8 cube vertices split evenly into two tetrahedra of 4 vertices "
        "each. This is because exactly half of all 3-bit numbers have odd "
        "parity (four: 001, 010, 100, 111) and half have even parity."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Tet A = {1, 2, 4, 7} = vertices with odd bit parity.")
            .step("Tet B = {0, 3, 5, 6} = vertices with even bit parity.")
            .step("|Tet A| = 4, |Tet B| = 4.")
            .step("Total: 4 + 4 = 8 = all cube vertices.")
            .conclude("Tet A count = 4; Tet B count = 4.")
        )
    
    def model(self):
        return (
            Model()
            .add("Tet A count", len(TET_A))
            .add("Tet B count", len(TET_B))
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet A count", 4)
            .add("Tet B count", 4)
        )


class BinaryExtremaAreAntipodal(Test):
    """Vertices 0 (000) and 7 (111) are antipodal and in opposite tetrahedra."""
    name = "Binary Extrema"
    level = Level.STANDARD
    question = (
        "The binary extrema 000 (all -1 coordinates) and 111 (all +1 coordinates) "
        "form an antipodal pair. Are they in opposite tetrahedra?"
    )
    reference = "Cube geometry"
    tolerance = 0.01
    commentary = (
        "Vertex 0 has 0 ones (even parity) so is in Tet B. Vertex 7 has 3 ones "
        "(odd parity) so is in Tet A. These pure states occupy opposite corners "
        "of the cube and belong to opposite tetrahedra."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Vertex 0 = binary 000, coordinates (-1, -1, -1).")
            .step("Vertex 7 = binary 111, coordinates (+1, +1, +1).")
            .step("0 has 0 ones (even) -> Tet B.")
            .step("7 has 3 ones (odd) -> Tet A.")
            .step("They form complementary pair (0, 7) across the body diagonal.")
            .conclude("Extrema in opposite tetrahedra = 1 (true).")
        )
    
    def model(self):
        v0_in_tet_b = 0 in TET_B
        v7_in_tet_a = 7 in TET_A
        opposite = v0_in_tet_b and v7_in_tet_a
        return Model().add("Extrema in opposite tetrahedra", 1 if opposite else 0)
    
    def observations(self):
        return Observed().add("Extrema in opposite tetrahedra", 1)


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BinaryVertexCount,
    ParityDeterminesTetrahedron,
    ComplementaryPairsXOR,
    ComplementaryPairsCrossTetrahedra,
    FourVerticesPerTetrahedron,
    BinaryExtremaAreAntipodal,
]


def run_all():
    """Run all binary vertex encoding tests."""
    return run_tests(
        title="Binary Vertex Encoding: Coordinate Structure",
        summary=(
            "These tests validate the binary encoding of cube vertices. The 8 "
            "vertices map to 3-bit codes 000 through 111. The two tetrahedra "
            "are exactly the two parity classes: Tet A has odd parity vertices, "
            "Tet B has even parity. Complementary pairs (body diagonals) are "
            "related by XOR with 7 and always cross between tetrahedra."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
