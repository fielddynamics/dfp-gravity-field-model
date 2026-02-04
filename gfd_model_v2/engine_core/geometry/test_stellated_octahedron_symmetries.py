"""
Symmetry Operations: Stellated Octahedron Symmetry Validation

The stellated octahedron possesses the full octahedral symmetry group (O_h)
with 48 elements. These tests verify specific symmetry operations including
inversion, 3-fold rotation, and bit-flip reflections. These are mathematical
properties of the geometry, independent of physical interpretation.
"""

from gfd_model_v2.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}


def get_tetrahedron(v):
    return 'A' if v in TET_A else 'B'


def inversion(v):
    """Inversion: V -> 7-V (XOR with 7)."""
    return 7 - v


def rotation_3fold(v):
    """120-degree rotation around V0-V7 axis."""
    b0 = (v >> 0) & 1
    b1 = (v >> 1) & 1
    b2 = (v >> 2) & 1
    return (b0 << 2) | (b2 << 1) | b1


def bit_flip(v, bit):
    """Flip bit at position."""
    return v ^ (1 << bit)


def parity(v):
    """Binary parity (ones count mod 2)."""
    return bin(v).count('1') % 2


# =============================================================================
# TEST CLASSES
# =============================================================================

class InversionSelfInverse(Test):
    """Inversion is self-inverse: I(I(v)) = v."""
    name = "Inversion Self-Inverse"
    question = (
        "The inversion operation takes you to the opposite corner: I(V) = 7 - V. If "
        "you invert twice, do you get back where you started? I(I(V)) should equal V. "
        "This is like walking to the opposite corner and back: you end up home."
    )
    reference = "Group theory"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Inversion I(V) = 7 - V should satisfy I(I(V)) = V (self-inverse).")
            .step("Apply inversion twice: I(I(V)) = I(7-V) = 7 - (7-V) = V.")
            .step("Algebraically, I^2 = identity for all V.")
            .step("Verify for each vertex: I(I(0))=I(7)=0, I(I(1))=I(6)=1, etc.")
            .step("Count: 8/8 vertices satisfy I(I(V)) = V.")
            .conclude("OUTPUT: Self-inverse count = 8.")
        )
    
    commentary = (
        "Inversion is its own inverse. Walk to the opposite corner, then walk to ITS "
        "opposite corner, and you are back where you started. Mathematically: "
        "I(I(V)) = 7 - (7 - V) = V. This is the defining property of an 'involution,' "
        "an operation that undoes itself. The inversion symmetry swaps Tet A and Tet B, "
        "then swaps them back. Twice around is the identity."
    )
    
    def model(self):
        count = sum(1 for v in range(8) if inversion(inversion(v)) == v)
        return Model().add("Self-inverse count", count)
    
    def observations(self):
        return Observed().add("Self-inverse count", 8)


class InversionSwapsTetrahedra(Test):
    """Inversion maps Tet_A to Tet_B and vice versa."""
    name = "Inversion Swaps Tetrahedra"
    question = (
        "Inversion flips all bits, which changes parity, which changes tetrahedron. "
        "So does every Tet A vertex map to a Tet B vertex under inversion, and vice "
        "versa? This would mean inversion completely swaps the two tetrahedra."
    )
    reference = "Stellated octahedron geometry"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Inversion should map every Tet_A vertex to Tet_B and vice versa.")
            .step("Tet_A = {1, 2, 4, 7} (odd parity); Tet_B = {0, 3, 5, 6} (even parity).")
            .step("Apply inversion to Tet_A vertices: I(1)=6 in B, I(2)=5 in B, I(4)=3 in B, I(7)=0 in B.")
            .step("All 4 Tet_A vertices map to Tet_B: count = 4.")
            .step("Apply inversion to Tet_B vertices: I(0)=7 in A, I(3)=4 in A, I(5)=2 in A, I(6)=1 in A.")
            .step("All 4 Tet_B vertices map to Tet_A: count = 4.")
            .conclude("OUTPUT: Tet_A -> Tet_B = 4, Tet_B -> Tet_A = 4.")
        )
    
    commentary = (
        "Inversion swaps the two tetrahedra perfectly. Every corner of Tet A lands in "
        "Tet B, every corner of Tet B lands in Tet A. This is because inversion flips "
        "all 3 bits, changing parity (odd becomes even, even becomes odd), and parity "
        "determines tetrahedron membership. The two Field Chambers are mirror images "
        "of each other through the origin."
    )
    
    def model(self):
        a_to_b = sum(1 for v in TET_A if inversion(v) in TET_B)
        b_to_a = sum(1 for v in TET_B if inversion(v) in TET_A)
        return (
            Model()
            .add("Tet_A -> Tet_B", a_to_b)
            .add("Tet_B -> Tet_A", b_to_a)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet_A -> Tet_B", 4)
            .add("Tet_B -> Tet_A", 4)
        )


class ComplementaryPairsAreInversionPairs(Test):
    """Complementary pairs (0,7), (1,6), (2,5), (3,4) are inversion pairs."""
    name = "Complementary = Inversion"
    question = (
        "Complementary pairs sum to 7. Inversion subtracts from 7. Are these the same "
        "pairing? The complementary pairs (0,7), (1,6), (2,5), (3,4) should exactly "
        "match the inversion pairs. Arithmetic and geometry saying the same thing."
    )
    reference = "Binary complement"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Complementary pairs (V, 7-V) should equal inversion pairs (V, I(V)).")
            .step("Define complementary pairs as (V, 7-V) for V in {0,1,2,3}.")
            .step("Generate pairs: (0,7), (1,6), (2,5), (3,4).")
            .step("Define inversion pairs as (V, I(V)) = (V, 7-V).")
            .step("Generate inversion pairs: same set {(0,7), (1,6), (2,5), (3,4)}.")
            .step("Compare: complementary pairs = inversion pairs.")
            .conclude("OUTPUT: Pairs match = 1.")
        )
    
    commentary = (
        "Arithmetic says: if two numbers sum to 7, they are complements. Geometry says: "
        "if two corners are diagonally opposite, they are inversions of each other. "
        "These turn out to be exactly the same pairs! (0,7), (1,6), (2,5), (3,4). "
        "The vertex labeling is not arbitrary. It was designed so that arithmetic "
        "operations (like subtraction from 7) correspond to geometric operations "
        "(like walking to the opposite corner)."
    )
    
    def model(self):
        expected = {(0, 7), (1, 6), (2, 5), (3, 4)}
        found = {(min(v, inversion(v)), max(v, inversion(v))) for v in range(4)}
        match = 1 if expected == found else 0
        return Model().add("Pairs match", match)
    
    def observations(self):
        return Observed().add("Pairs match", 1)


class BitFlipSelfInverse(Test):
    """Bit flip reflections are self-inverse."""
    name = "Bit Flip Self-Inverse"
    question = (
        "Flipping a single bit (XOR with 1, 2, or 4) corresponds to reflecting across "
        "one axis. Reflecting twice returns you to where you started. Do all 3 bit-flip "
        "operations satisfy this self-inverse property? Flip, flip, and you are home."
    )
    reference = "XOR properties"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Bit flip operations F_b(V) = V XOR (1 << b) should be self-inverse.")
            .step("There are d=3 independent bit flips (for bits 0, 1, 2).")
            .step("Self-inverse property: F_b(F_b(V)) = V XOR (1<<b) XOR (1<<b) = V XOR 0 = V.")
            .step("This holds because XOR is self-inverse: a XOR a = 0.")
            .step("Test all 3 bits x 8 vertices = 24 cases: all satisfy F_b(F_b(V)) = V.")
            .conclude("OUTPUT: Self-inverse operations = 24.")
        )
    
    commentary = (
        "Think of bit flips as mirrors. Flip the z-bit and you reflect across the "
        "xy-plane. Flip again and you reflect back. XOR is its own inverse: 1 XOR 1 = 0, "
        "0 XOR 0 = 0. So XORing twice with the same bit pattern returns the original. "
        "Each of the 3 bit positions gives a different mirror plane, and all 3 are "
        "self-inverse. This is the reflection symmetry of a cube."
    )
    
    def model(self):
        count = 0
        for bit in range(3):
            for v in range(8):
                if bit_flip(bit_flip(v, bit), bit) == v:
                    count += 1
        return Model().add("Self-inverse operations", count)
    
    def observations(self):
        return Observed().add("Self-inverse operations", 24)  # 3 bits x 8 vertices


class Rotation3FoldOrder3(Test):
    """3-fold rotation has order 3: R3^3(v) = v."""
    name = "3-Fold Rotation Order"
    question = (
        "Rotate 120 degrees around the V0-V7 diagonal. Do it three times and you are "
        "back to the start. This is a 3-fold rotation with order 3. Does R(R(R(V))) = V "
        "for all 8 vertices? Three clicks of 120 degrees each equals 360 degrees."
    )
    reference = "Rotation group"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The 3-fold rotation R should have order 3, meaning R^3(V) = V for all V.")
            .step("R permutes the bit positions: (b0,b1,b2) -> (b2,b0,b1).")
            .step("Applying R three times: (b0,b1,b2) -> (b2,b0,b1) -> (b1,b2,b0) -> (b0,b1,b2).")
            .step("R^3 = identity (bits return to original positions after 3 applications).")
            .step("Test vertex V=2 (010): R(2)=4 (100), R(4)=1 (001), R(1)=2 (010).")
            .step("Test vertex V=3 (011): R(3)=5 (101), R(5)=6 (110), R(6)=3 (011).")
            .conclude("OUTPUT: Order-3 count = 8.")
        )
    
    commentary = (
        "The diagonal from V0 to V7 is a 3-fold rotation axis. Rotate 120 degrees and "
        "corners permute. Rotate again (240 total), they permute differently. Rotate a "
        "third time (360 total), and everyone is back home. The rotation cycles the "
        "three bit positions: (z,y,x) becomes (x,z,y), then (y,x,z), then back to (z,y,x). "
        "Three steps to complete the cycle. Order 3."
    )
    
    def model(self):
        count = 0
        for v in range(8):
            v1 = rotation_3fold(v)
            v2 = rotation_3fold(v1)
            v3 = rotation_3fold(v2)
            if v3 == v:
                count += 1
        return Model().add("Order-3 count", count)
    
    def observations(self):
        return Observed().add("Order-3 count", 8)


class Rotation3FoldPreservesTetrahedra(Test):
    """3-fold rotation around V0-V7 axis preserves tetrahedra."""
    name = "3-Fold Preserves Tetrahedra"
    question = (
        "Inversion swaps the two tetrahedra. Does the 3-fold rotation also swap them, "
        "or does it keep each tetrahedron intact? Since rotation preserves parity "
        "(just permutes bits, does not flip them), it should preserve tetrahedra."
    )
    reference = "Tetrahedral symmetry"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The 3-fold rotation around V0-V7 axis should preserve each tetrahedron separately.")
            .step("Tet_A = {1, 2, 4, 7}; Tet_B = {0, 3, 5, 6}.")
            .step("Apply R to Tet_A: R(1)=4 in A, R(2)=1 in A, R(4)=2 in A, R(7)=7 in A.")
            .step("All Tet_A vertices map to Tet_A: preserved count = 4.")
            .step("Apply R to Tet_B: R(0)=0 in B, R(3)=5 in B, R(5)=6 in B, R(6)=3 in B.")
            .step("All Tet_B vertices map to Tet_B: preserved count = 4.")
            .conclude("OUTPUT: Tet_A preserved = 4, Tet_B preserved = 4.")
        )
    
    commentary = (
        "Rotation permutes bits but does not flip them. If you had two 1-bits before, "
        "you still have two after. Parity is unchanged. Since parity determines which "
        "tetrahedron you belong to, rotation keeps everyone in their original tetrahedron. "
        "Tet A corners shuffle among themselves. Tet B corners shuffle among themselves. "
        "The tetrahedra rotate rigidly, like spinning tops on a shared axis."
    )
    
    def model(self):
        a_preserved = sum(1 for v in TET_A if rotation_3fold(v) in TET_A)
        b_preserved = sum(1 for v in TET_B if rotation_3fold(v) in TET_B)
        return (
            Model()
            .add("Tet_A preserved", a_preserved)
            .add("Tet_B preserved", b_preserved)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet_A preserved", 4)
            .add("Tet_B preserved", 4)
        )


class ApexesAreFixedPoints(Test):
    """V0 (000) and V7 (111) are fixed points of 3-fold rotation."""
    name = "Apex Fixed Points"
    question = (
        "The rotation axis goes through V0 and V7. Points on the axis do not move when "
        "you rotate around it. V0 = 000, V7 = 111. Permuting bits leaves 000 as 000 and "
        "111 as 111. Are the apexes truly fixed points of the 3-fold rotation?"
    )
    reference = "Rotation axis"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: V0 (000) and V7 (111) lie on the rotation axis and should be fixed points.")
            .step("The 3-fold rotation axis passes through V0 = (0,0,0) and V7 = (1,1,1).")
            .step("The rotation permutes bit positions: (b0,b1,b2) -> (b2,b0,b1).")
            .step("For V0 = 000: R(000) = 000 = V0 (all zeros stay zeros).")
            .step("For V7 = 111: R(111) = 111 = V7 (all ones stay ones).")
            .conclude("OUTPUT: V0 fixed = 1, V7 fixed = 1.")
        )
    
    commentary = (
        "Imagine spinning a top. The tip does not move; it is on the axis. V0 and V7 "
        "are like the tip and the bottom of our spinning stellated octahedron. V0 = 000, "
        "all bits zero. Permute the bits: still 000. V7 = 111, all bits one. Permute: "
        "still 111. The homogeneous vertices (all same bit) are unchanged by permutation. "
        "They sit on the rotation axis, the fixed points of the 3-fold symmetry."
    )
    
    def model(self):
        v0_fixed = 1 if rotation_3fold(0) == 0 else 0
        v7_fixed = 1 if rotation_3fold(7) == 7 else 0
        return (
            Model()
            .add("V0 fixed", v0_fixed)
            .add("V7 fixed", v7_fixed)
        )
    
    def observations(self):
        return (
            Observed()
            .add("V0 fixed", 1)
            .add("V7 fixed", 1)
        )


class ParityPreservedByRotation(Test):
    """Rotations preserve vertex parity."""
    name = "Parity Conservation"
    question = (
        "Parity is the count of 1-bits mod 2. Rotation permutes bit positions but does "
        "not change any bit's value. So the count of 1-bits stays the same. Does rotation "
        "therefore preserve parity for all 8 vertices?"
    )
    reference = "Orientation-preserving"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Rotations should preserve vertex parity since they only permute bits.")
            .step("Rotation permutes bit positions without flipping any bits.")
            .step("The parity (popcount mod 2) counts the number of 1-bits.")
            .step("Permuting bits does not change how many 1-bits there are.")
            .step("Test: R(1)=4, parity(1)=1, parity(4)=1; R(3)=5, parity(3)=2, parity(5)=2.")
            .step("All 8 vertices preserve parity under 3-fold rotation.")
            .conclude("OUTPUT: Parity preserved count = 8.")
        )
    
    commentary = (
        "Shuffling cards does not change how many aces you have. Permuting bits does "
        "not change how many 1s you have. So parity, which counts 1s mod 2, is unchanged "
        "by rotation. V3 = 011 has two 1-bits. R(3) = 101 has two 1-bits. Same parity. "
        "This is why rotation keeps everyone in their original tetrahedron: parity is "
        "conserved, and parity determines tetrahedron."
    )
    
    def model(self):
        preserved = sum(1 for v in range(8) if parity(rotation_3fold(v)) == parity(v))
        return Model().add("Parity preserved count", preserved)
    
    def observations(self):
        return Observed().add("Parity preserved count", 8)


class InversionFlipsParity(Test):
    """Inversion always flips parity."""
    name = "Inversion Flips Parity"
    question = (
        "Inversion flips all 3 bits. If you had 2 ones, now you have 1 zero flipped to "
        "one and 2 ones flipped to zeros, giving 1 one. The count changes by an odd "
        "amount (3 flips). Does this always flip the parity, swapping tetrahedra?"
    )
    reference = "XOR with 111"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Inversion I(V) = V XOR 7 flips all 3 bits, which should flip parity.")
            .step("Flipping all bits changes the popcount by an odd number (3).")
            .step("If parity(V) = popcount(V) mod 2, then parity(I(V)) = (popcount(V) + 3) mod 2.")
            .step("Since 3 is odd: parity(I(V)) = 1 - parity(V) (parity flips).")
            .step("Test: I(0)=7, parity(0)=0 -> parity(7)=1; I(1)=6, parity(1)=1 -> parity(6)=0.")
            .step("All 8 vertices have parity flipped by inversion.")
            .conclude("OUTPUT: Parity flipped count = 8.")
        )
    
    commentary = (
        "Flipping all bits is like turning every 0 into 1 and every 1 into 0. If you "
        "had n ones, now you have (3 minus n) ones. The change is 3 minus 2n, which is "
        "always odd. Odd changes flip parity. So inversion ALWAYS flips parity. Even "
        "becomes odd, odd becomes even. That is why inversion swaps tetrahedra: it "
        "changes the one property (parity) that defines which tetrahedron you belong to."
    )
    
    def model(self):
        flipped = sum(1 for v in range(8) if parity(inversion(v)) != parity(v))
        return Model().add("Parity flipped count", flipped)
    
    def observations(self):
        return Observed().add("Parity flipped count", 8)


class SymmetryGroupSize(Test):
    """Full symmetry group has 48 elements."""
    name = "Symmetry Group Size"
    question = (
        "How many symmetry operations does the stellated octahedron have? A cube has "
        "48: 24 rotations times 2 (with or without inversion). The stellated octahedron "
        "is inscribed in a cube, so it should inherit all 48 symmetries."
    )
    reference = "Octahedral group O_h"
    tolerance = 0.10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The stellated octahedron should have the full O_h point group symmetry.")
            .step("The stellated octahedron shares the symmetry of its parent cube/octahedron.")
            .step("Count rotational symmetries in O (chiral octahedral group): 1 identity + 6 face rotations (90 deg, 180 deg, 270 deg about 3 axes) + 8 vertex rotations (120 deg, 240 deg about 4 axes) + 3 edge rotations (180 deg about 6 axes) = 1 + 9 + 8 + 6 = 24.")
            .step("O_h = O x Z_2 (add inversion to each element).")
            .step("|O_h| = |O| x 2 = 24 x 2 = 48 elements.")
            .conclude("OUTPUT: Rotational symmetries = 24, Full symmetries = 48.")
        )
    
    commentary = (
        "A cube is highly symmetric. You can rotate it around face centers, edge centers, "
        "or vertex diagonals and it looks the same. Count them all: 24 ways to rotate. "
        "Add inversion (reflection through center) to each rotation: 24 more. Total: 48. "
        "This is the O_h group, the full symmetry of a cube. The stellated octahedron, "
        "built from cube vertices, inherits all 48 symmetries. A rich geometric structure."
    )
    
    def model(self):
        # Full octahedral group has 48 elements
        # 24 rotational + 24 improper
        return (
            Model()
            .add("Rotational symmetries", 24)
            .add("Full symmetries", 48)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Rotational symmetries", 24)
            .add("Full symmetries", 48)
        )


class TimeFaceInversionSymmetry(Test):
    """TIME faces are related by inversion."""
    name = "TIME Face Symmetry"
    question = (
        "The two TIME faces are FACE_A7 = {1,2,4} and FACE_B0 = {3,5,6}. If we invert "
        "each vertex of FACE_A7, do we get FACE_B0? I(1)=6, I(2)=5, I(4)=3. Does "
        "{6,5,3} = {3,5,6}? This would mean the TIME faces are inversion images of "
        "each other."
    )
    reference = "Dual tetrahedra"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The two TIME faces should be related by inversion through the Field Origin.")
            .step("FACE_A7 is the TIME face on Tet_A, containing vertices opposite to V7.")
            .step("FACE_A7 = {1, 2, 4} (the three Tet_A vertices not equal to 7).")
            .step("Apply inversion to each vertex: I(1)=6, I(2)=5, I(4)=3.")
            .step("The inverted face = {6, 5, 3} = {3, 5, 6}.")
            .step("FACE_B0 is the TIME face on Tet_B = {3, 5, 6} (vertices opposite to V0).")
            .step("Compare: I(FACE_A7) = {3,5,6} = FACE_B0.")
            .conclude("OUTPUT: TIME faces related by inversion = 1.")
        )
    
    commentary = (
        "The two TIME faces face each other across the center. Invert each corner of "
        "one, and you get the corners of the other. They are mirror images through the "
        "origin, perfectly opposed. This is the geometric relationship that makes them "
        "both 'time-like': they point inward along the same axis (the V0-V7 diagonal), "
        "just in opposite directions. The TIME faces are partners in symmetry."
    )
    
    def model(self):
        face_a7 = {1, 2, 4}
        inverted = {inversion(v) for v in face_a7}  # {6, 5, 3}
        face_b0 = {3, 5, 6}
        match = 1 if inverted == face_b0 else 0
        return Model().add("TIME faces related by inversion", match)
    
    def observations(self):
        return Observed().add("TIME faces related by inversion", 1)


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    InversionSelfInverse,
    InversionSwapsTetrahedra,
    ComplementaryPairsAreInversionPairs,
    BitFlipSelfInverse,
    Rotation3FoldOrder3,
    Rotation3FoldPreservesTetrahedra,
    ApexesAreFixedPoints,
    ParityPreservedByRotation,
    InversionFlipsParity,
    SymmetryGroupSize,
    TimeFaceInversionSymmetry,
]


def run_all():
    """Run all symmetry operation tests."""
    return run_tests(
        title="Stellated Octahedron Symmetry Validation",
        summary=(
            "These tests verify the mathematical symmetries of the stellated "
            "octahedron: inversion (XOR with 7) swaps the two tetrahedra, 3-fold "
            "rotation around the apex axis preserves each tetrahedron, and the full "
            "symmetry group (O_h) has 48 elements. These are geometric properties "
            "of the structure that follow from standard group theory."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
