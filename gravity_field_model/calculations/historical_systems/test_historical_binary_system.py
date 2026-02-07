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

TEXTBOOK REFERENCE:
Gravity Field Dynamics Textbook, Chapter 9 (The Dual Field Chamber), Section 9.2:
"The 8 vertices can be divided into two groups of 4 based on parity of the
binary representation. This partition defines the two interlocking tetrahedra."

AUDIT NOTES:
- audit_score: 95
- audit_notes: None (cleared after audit)
"""

from gravity_field_model.framework import *
from gravity_field_model.common.geometry_constants import (
    TET_A, TET_B, COMPLEMENTARY_PAIRS, VERTICES
)


# =============================================================================
# TEST CLASSES
# =============================================================================

class BinaryVertexCount(Test):
    """8 vertices = 2^3 binary encodings."""
    name = "Binary Vertex Count"
    level = Level.STANDARD
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Why specifically 3 dimensions for the Field Chamber, and could d=4 "
        "create a 16-vertex hypercube structure? "
        "(Answering would improve Question by +2 points: connects 3D choice to physics) "
        "Q2: How does the binary encoding relate to error-correcting codes like Hamming codes? "
        "(Answering would improve Commentary by +2 points: deepens information theory link) "
        "Q3: What physical process selects the cube over other 8-vertex polyhedra? "
        "(Answering would improve Derivation by +2 points: grounds geometry in physics)"
    )
    question = (
        "Why does the cube's geometry naturally encode a 3-bit binary system? "
        "The answer reveals how spatial dimension d directly determines the "
        "information capacity (2^d states) of the Field Chamber structure."
    )
    reference = "GFM Textbook Ch.9 Sec.9.2: Binary encoding of cube vertices"
    tolerance = 0.01
    commentary = (
        "The cube in d=3 dimensions offers exactly 2^d = 8 corner positions, "
        "each describable by three binary choices (left/right, up/down, front/back). "
        "This is not coincidence: spatial closure requires 2^d vertices to span "
        "all possible sign combinations of d orthogonal axes."
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
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Does parity partition generalize to higher dimensions (d=4 hypercube)? "
        "(Answering would improve Question by +2 points: tests universality of pattern) "
        "Q2: How does parity relate to the bimetric ghost-freedom condition in Hassan-Rosen theory? "
        "(Answering would improve Commentary by +2 points: connects math to physics) "
        "Q3: Why does nature prefer parity-based structure over other vertex partitions? "
        "(Answering would improve Derivation by +2 points: addresses necessity vs sufficiency)"
    )
    question = (
        "Why does bit-count parity (odd vs even number of 1s) perfectly partition "
        "the cube vertices into two interlocking tetrahedra? Understanding this "
        "reveals why the bimetric structure emerges from pure combinatorics."
    )
    reference = "GFM Textbook Ch.9 Sec.9.2: Parity partition into dual tetrahedra"
    tolerance = 0.01
    commentary = (
        "The two tetrahedra are the two eigenspaces of the parity operator. "
        "Vertices with odd popcount (1,2,4,7) span one tetrahedron; vertices with "
        "even popcount (0,3,5,6) span the other. This is the same structure used "
        "in error-correcting codes, where parity bits detect single-bit errors."
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
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Is XOR with 2^d - 1 the universal complementation operator for d-cubes? "
        "(Answering would improve Derivation by +2 points: generalizes the pattern) "
        "Q2: How does bitwise complementation relate to CPT symmetry in physics? "
        "(Answering would improve Commentary by +2 points: connects to fundamental symmetries) "
        "Q3: What information-theoretic meaning does the XOR operation carry for field closure? "
        "(Answering would improve Question by +2 points: deepens conceptual understanding)"
    )
    question = (
        "Why does the XOR operation with 7 (binary 111) map each vertex to "
        "its geometric opposite? This reveals how bitwise complementation "
        "encodes the cube's spatial inversion symmetry."
    )
    reference = "GFM Textbook Ch.9 Sec.9.5: Field Origin and body diagonals"
    tolerance = 0.01
    commentary = (
        "XOR with 111 flips all three bits, geometrically reflecting the vertex "
        "through the origin. This operation connects Chamber A to Chamber B, "
        "since flipping all bits always changes the parity. The four body "
        "diagonals thus link the two tetrahedra through the Field Origin."
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
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: What happens to bimetric coupling if we swap tetrahedra assignments? "
        "(Answering would improve Question by +2 points: probes symmetry breaking) "
        "Q2: How do cross-tetrahedral paths relate to graviton propagation in bimetric theory? "
        "(Answering would improve Commentary by +2 points: connects geometry to dynamics) "
        "Q3: Is there a physical quantity conserved along body diagonal paths? "
        "(Answering would improve Derivation by +2 points: identifies conservation laws)"
    )
    question = (
        "Why must every body diagonal connect opposite tetrahedra? The answer "
        "shows how parity conservation under inversion enforces the bimetric "
        "coupling between Chamber A and Chamber B."
    )
    reference = "GFM Textbook Ch.9 Sec.9.3: Bimetric balance through antipodal pairs"
    tolerance = 0.01
    commentary = (
        "Flipping all d=3 bits changes the popcount by an odd amount (from k "
        "to 3-k ones). Since 3 is odd, k and 3-k have opposite parity. Therefore, "
        "complementary vertices always belong to opposite chambers, ensuring "
        "every body diagonal crosses between the dual Field Chambers."
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
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Why is k=4 the minimal closure constant, not k=3 or k=5? "
        "(Answering would improve Question by +2 points: addresses uniqueness of tetrahedron) "
        "Q2: How does the k=4 count connect to the 4 forces of the Standard Model? "
        "(Answering would improve Commentary by +2 points: explores physics correspondence) "
        "Q3: What geometric theorem proves the tetrahedron is the minimal 3D enclosure? "
        "(Answering would improve Derivation by +2 points: grounds claim rigorously)"
    )
    question = (
        "Why does the parity partition yield exactly 4 vertices per tetrahedron? "
        "This connects the closure constant k=4 to the binary structure, showing "
        "that field closure naturally produces tetrahedral geometry."
    )
    reference = "GFM Textbook Ch.7 Sec.7.2: The simplex theorem and k=4"
    tolerance = 0.01
    commentary = (
        "Of 2^d = 8 binary numbers, exactly half have odd popcount and half have "
        "even popcount. This combinatorial fact ensures the two tetrahedra have "
        "equal size (4 vertices each), which is required for the bimetric balance "
        "of the stellated octahedron."
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
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Do the extrema (000, 111) have special physical meaning as vacuum states? "
        "(Answering would improve Question by +2 points: probes quantum vacuum structure) "
        "Q2: How does the principal diagonal relate to time evolution in the Field Chamber? "
        "(Answering would improve Commentary by +2 points: connects space to time) "
        "Q3: Is the GHZ state |000> + |111> the natural quantum state of the extrema pair? "
        "(Answering would improve Derivation by +2 points: links geometry to entanglement)"
    )
    question = (
        "Why must the binary extrema (000 and 111) belong to opposite chambers? "
        "These vertices represent the pure states of the Field Chamber, and their "
        "separation ensures maximum information contrast across the structure."
    )
    reference = "GFM Textbook Ch.9 Sec.9.3: Apex vertices and TIME faces"
    tolerance = 0.01
    commentary = (
        "Vertex 0 (popcount 0) and Vertex 7 (popcount 3) have maximally different "
        "parities. They sit at opposite corners of the cube, connected by the "
        "principal body diagonal through the Field Origin. In the face classification, "
        "these are the apex vertices whose opposite faces become the TIME faces."
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
            "These tests validate why the cube's 8 vertices naturally form a "
            "3-bit binary system. Key insight: the two tetrahedra of the stellated "
            "octahedron correspond exactly to the two parity classes (odd/even "
            "popcount). Complementary pairs (body diagonals) link Chamber A to "
            "Chamber B through the Field Origin, ensuring bimetric coupling. "
            "This structure underlies the GFM field closure mechanism."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
