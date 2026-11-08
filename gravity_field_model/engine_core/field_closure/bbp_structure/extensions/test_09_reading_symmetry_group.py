"""
09. The reading under all twelve symmetries that keep the TIME axis
===================================================================

Role:     Extends PROOF.md Theorem 5 from the six relabellings to the full symmetry group of the TIME axis.
Expected: Passes. A failure means a symmetry other than the identity and the central inversion preserves the reading.

The cube has 48 symmetries (signed permutations of the coordinates). Twelve
keep the TIME axis as a set: the six permutations of the axes, each with or
without the central inversion c -> -c (which swaps Qian and Kun, and the two
families). Apply each to the rank-ordered father's family (Qian, Zhen, Kan,
Gen), keep the image order, and read it with Theorem 5's rule, through the
complement map when the image is the mother's family. Count the symmetries
whose reading is still pi.
"""

from itertools import permutations

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions._reading import read_rows, is_pi

FATHER_RANK = (7, 4, 2, 1)


def coords(v):
    return tuple(2 * ((v >> s) & 1) - 1 for s in (2, 1, 0))


def label(c):
    return sum(((x + 1) // 2) << s for x, s in zip(c, (2, 1, 0)))


class ReadingSymmetryGroup(Test):
    name = "09. The Reading Under the Twelve TIME-Preserving Symmetries"
    question = (
        "Which symmetries of the stellated octahedron that keep the TIME axis also keep the "
        "reading that produces pi?"
    )
    reference = "PROOF.md Theorem 5"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Enumerate the 12 signed permutations g with g(1,1,1) = +-(1,1,1).")
            .step("Map Qian, Zhen, Kan, Gen through g, keeping their order.")
            .step("Read the image with the line rules (complemented if it lies in the mother's family).")
            .conclude("Count the symmetries whose reading equals pi.")
        )

    commentary = (
        "Two of the twelve symmetries keep the reading: the identity, and the central "
        "inversion, which carries the father and sons onto the mother and daughters in the "
        "same rank order (Theorem 5's second family). The ten others reorder the children and "
        "give other numbers. The reading's symmetry is exactly the exchange of the two "
        "families through the Field Origin, and nothing more: a Z2, not the full S3 x Z2."
    )

    def model(self):
        n, keep = 0, []
        for perm in permutations(range(3)):
            for sign in (1, -1):
                n += 1
                image = []
                for v in FATHER_RANK:
                    c = coords(v)
                    image.append(label(tuple(sign * c[perm[i]] for i in range(3))))
                if is_pi(read_rows(image, complement=(image[0] == 0))):
                    keep.append(("identity" if sign == 1 else "inversion") if perm == (0, 1, 2) else f"{perm},{sign}")
        return (
            Model()
            .add("Symmetries keeping the TIME axis", n)
            .add("Of those, keeping the pi reading", len(keep))
            .add("Which", ", ".join(keep))
        )

    def observations(self):
        return (
            Observed()
            # 3! axis permutations x {identity, inversion}.
            .add("Symmetries keeping the TIME axis", 12)
            .add("Of those, keeping the pi reading", 2)
            .add("Which", "identity, inversion")
        )


ALL_TESTS = [ReadingSymmetryGroup]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("09", "Reading symmetry group.", ALL_TESTS) else 1)
