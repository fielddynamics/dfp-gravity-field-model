"""
22. Does the pi reading carry a sense of rotation?
==================================================

Role:     Tests whether the stellated-octahedron reading of pi singles out a direction of rotation, and what fixes it.
Expected: Passes. A failure means the reading's symmetry group or its rotation sense differs from that stated.

A preferred direction of spin is an axial vector: a rotation sense about an
axis. Two different properties matter:

- **Chirality** (handedness) is whether a figure differs from its mirror image.
  A figure with a centre of inversion is achiral.
- **A sense of rotation** is compatible with a centre of inversion, because
  axial vectors such as angular momentum do not change under inversion. A
  spinning ball is achiral and still spins one way.

The test takes the pi reading with its rules fixed to the lines (Qian, then
Zhen, Kan, Gen; weight 2b + m + t; step 2t + 1) and finds:

1. its symmetry group among the 12 symmetries that keep the TIME axis, and
   whether that group contains an improper element (then the reading is achiral);
2. whether it contains the 120-degree rotations about the TIME axis (if not,
   the reading distinguishes the cyclic order of the sons);
3. the rotation sense of the reading: going Zhen -> Kan -> Gen around the TIME
   axis, the sign of (Zhen x Kan) . (1, 1, 1) gives the sense (+1 =
   counterclockwise seen from Qian); the same sign must hold for Kan -> Gen and
   Gen -> Zhen;
4. whether every mirror image of the reading (an odd permutation of the axes)
   fails to give pi, so that the sense is not shared by its mirror.
"""

from fractions import Fraction
from itertools import permutations

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions._reading import read_rows, is_pi

FATHER_RANK = (7, 4, 2, 1)


def coords(v):
    return tuple(2 * ((v >> s) & 1) - 1 for s in (2, 1, 0))


def label(c):
    return sum(((x + 1) // 2) << s for x, s in zip(c, (2, 1, 0)))


def perm_sign(p):
    s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]:
                s = -s
    return s


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def turn_sense(a, b, axis=(1, 1, 1)):
    return sum(x * y for x, y in zip(cross(a, b), axis))


class ReadingRotationSense(Test):
    name = "22. Does the Pi Reading Carry a Sense of Rotation?"
    question = (
        "Could the stellated-octahedron reading of pi prefer one direction of rotation? Is it "
        "chiral, does it fix a sense of rotation about the TIME axis, and what fixes that sense?"
    )
    reference = "Test 09; PROOF.md Theorems 5 and 6"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Apply the 12 TIME-preserving symmetries to the rank-order reading; keep those that still give pi.")
            .step("Classify each kept symmetry as proper or improper; check the 120-degree turns.")
            .step("Compute the rotation sense of Zhen -> Kan -> Gen about the axis Kun -> Qian.")
            .step("Check that the reading's mirror images (odd permutations of the axes) do not give pi.")
            .conclude("The reading is achiral, yet fixes one sense of rotation about the TIME axis.")
        )

    commentary = (
        "The reading is kept by exactly two symmetries, the identity and the central inversion, "
        "so it has a centre of inversion and is achiral. It is not kept by the 120-degree turns "
        "about the TIME axis, so it distinguishes the order of the sons around that axis, and "
        "its mirror images give other numbers, not pi. Going eldest, middle, youngest around the "
        "axis is counterclockwise seen from Qian (sense +1). Because an axial vector is "
        "unchanged by inversion, this sense is compatible with the reading's symmetry: the "
        "structure does carry a preferred direction of rotation about the TIME axis. What fixes "
        "its sign is the assignment of bottom, middle and top lines to a right-handed x, y, z. "
        "That assignment is the encoding's convention (Theorem 1(e) fixes which line is which "
        "bit, not which way the axes turn), so within the mathematics the sense is conventional. "
        "It would become physical only if GFD tied the trigram lines to physical directions "
        "with a definite handedness."
    )

    def model(self):
        kept, kept_improper, kept_rot120 = [], 0, 0
        mirror_pi = 0
        for perm in permutations(range(3)):
            for sign in (1, -1):
                image = [label(tuple(sign * coords(v)[perm[i]] for i in range(3))) for v in FATHER_RANK]
                ok = is_pi(read_rows(image, complement=(image[0] == 0)))
                det = sign ** 3 * perm_sign(perm)
                if ok:
                    kept.append((perm, sign))
                    kept_improper += det == -1
                    kept_rot120 += perm in ((1, 2, 0), (2, 0, 1)) and sign == 1
                if sign == 1 and perm_sign(perm) == -1:
                    mirror_pi += ok
        z, k, g = (coords(v) for v in (4, 2, 1))     # Zhen, Kan, Gen
        senses = {turn_sense(z, k) > 0, turn_sense(k, g) > 0, turn_sense(g, z) > 0}
        sense = (1 if True in senses else -1) if len(senses) == 1 else 0
        return (
            Model()
            .add("Symmetries keeping the pi reading", len(kept))
            .add("Of those, improper (reading is achiral if > 0)", kept_improper)
            .add("120-degree turns keeping it", kept_rot120)
            .add("Rotation sense of Zhen -> Kan -> Gen about Kun -> Qian", 1 if sense > 0 else -1)
            .add("Mirror images (reflections) that still give pi", mirror_pi)
        )

    def observations(self):
        return (
            Observed()
            # Test 09: the identity and the central inversion.
            .add("Symmetries keeping the pi reading", 2)
            # The central inversion has determinant -1.
            .add("Of those, improper (reading is achiral if > 0)", 1)
            .add("120-degree turns keeping it", 0)
            # Zhen = (1,-1,-1), Kan = (-1,1,-1): Zhen x Kan = (2,2,0), dot (1,1,1) = 4 > 0.
            .add("Rotation sense of Zhen -> Kan -> Gen about Kun -> Qian", 1)
            # Theorem 5: only the rank order gives pi with these rules.
            .add("Mirror images (reflections) that still give pi", 0)
        )


ALL_TESTS = [ReadingRotationSense]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("22", "Reading rotation sense.", ALL_TESTS) else 1)
