"""
08. The TIME axis is the one diagonal every encoding agrees on
==============================================================

Role:     Supports PROOF.md Definition of the TIME axis: it is fixed by the labels, not chosen.
Expected: Passes. A failure means another body diagonal is invariant under all encodings.

The cube has four body diagonals. The TIME axis is the one through 000 and 111:
Kun and Qian, the parents. This test checks that it is singled out by the
labels themselves: of the four diagonals, it is the only one whose two labels
are unchanged by every permutation of the three bits, i.e. by every possible
assignment of trigram lines to coordinates. It also checks that it is the only
diagonal joining two trigrams of equal lines (all yang, all yin).
"""

from itertools import permutations

from gravity_field_model.framework import *


def permute_bits(v, perm):
    bits = [(v >> 2) & 1, (v >> 1) & 1, v & 1]
    b = [bits[perm[i]] for i in range(3)]
    return (b[0] << 2) | (b[1] << 1) | b[2]


class TimeAxisCanonical(Test):
    name = "08. The TIME Axis Is Fixed by Every Encoding"
    question = (
        "Is the TIME axis (Qian-Kun) a choice, or is it the only body diagonal that every "
        "line-to-bit encoding leaves in place?"
    )
    reference = "PROOF.md section 1 and Theorem 1(e)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("List the four body diagonals {v, 7-v}.")
            .step("Apply all 6 permutations of the bit positions to both ends.")
            .step("Count the diagonals mapped to themselves vertex by vertex under all six.")
            .conclude("Only {0, 7} is fixed: the parents' axis needs no convention.")
        )

    commentary = (
        "Only the diagonal through 000 and 111 is fixed by every permutation of the bits; the "
        "other three are shuffled among themselves. So once the trigrams are vertices of the "
        "cube, the parents' axis is singled out whatever line is called which coordinate, and "
        "it is the only diagonal whose ends have all lines alike. The TIME axis is not a "
        "convention of the encoding; the encoding only names the other six corners."
    )

    def model(self):
        diagonals = [(v, 7 - v) for v in range(4)]
        fixed = [d for d in diagonals
                 if all(permute_bits(d[0], p) == d[0] and permute_bits(d[1], p) == d[1]
                        for p in permutations(range(3)))]
        uniform = [d for d in diagonals if all(bin(v).count("1") in (0, 3) for v in d)]
        return (
            Model()
            .add("Body diagonals", len(diagonals))
            .add("Diagonals fixed by all six encodings", len(fixed))
            .add("That diagonal", " ".join(map(str, fixed[0])) if fixed else "none")
            .add("Diagonals joining all-yang and all-yin", len(uniform))
        )

    def observations(self):
        return (
            Observed()
            .add("Body diagonals", 4)
            # A bit permutation fixes v only if v's bits are all equal: 000 and 111.
            .add("Diagonals fixed by all six encodings", 1)
            .add("That diagonal", "0 7")
            .add("Diagonals joining all-yang and all-yin", 1)
        )


ALL_TESTS = [TimeAxisCanonical]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("08", "TIME axis canonical.", ALL_TESTS) else 1)
