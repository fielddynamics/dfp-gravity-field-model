"""
06. The selection under every line-to-bit encoding
===================================================

Role:     Extends PROOF.md Theorems 1(e) and 3: what the main result needs from the encoding.
Expected: Passes. A failure means the selection or the 2+2 split depends on the encoding.

The main theorem reads slot j as the vertex labelled j mod 8, with labels from
the Shuo Gua encoding (bottom line = most significant bit). There are six ways
to assign the three lines to the three bits. Under every one, Qian is 111 = 7
and Kun is 000 = 0, so the TIME slots are 7 and 8 and the selected formula is
BBP. What changes is which trigrams sit at slots 1, 4, 5, 6.

The test lists, for each encoding: the selected formula, its chamber split, and
the four trigrams it uses.
"""

from itertools import permutations

from gravity_field_model.framework import *

LINES = {"Qian": (1, 1, 1), "Kun": (0, 0, 0), "Zhen": (1, 0, 0), "Kan": (0, 1, 0), "Gen": (0, 0, 1),
         "Xun": (0, 1, 1), "Li": (1, 0, 1), "Dui": (1, 1, 0)}
BBP_SLOTS = (1, 4, 5, 6)
AW_SLOT7 = 1          # slot-7 weight per unit r; slot 8 is always 0


def label(lines, bits):
    return sum(l << b for l, b in zip(lines, bits))


class EncodingInvariance(Test):
    name = "06. The Selection Under Every Line-to-Bit Encoding"
    question = (
        "Does the main result depend on the Shuo Gua's choice of bottom line = most "
        "significant bit, and if not, what does that choice decide?"
    )
    reference = "PROOF.md Theorems 1(e) and 3"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("For each of the 6 assignments of (bottom, middle, top) to bits, label all trigrams.")
            .step("The TIME apices Qian and Kun are 7 and 0 under every assignment, so TIME silence still forces r = 0.")
            .step("Read off which trigrams occupy slots 1, 4, 5, 6 and the chamber split.")
            .conclude("The selection is encoding-free; the names of the four corners are not.")
        )

    commentary = (
        "Under all six encodings the TIME slots are Qian and Kun, so the selected formula is "
        "always BBP and always splits 2 + 2 between the families: parity does not depend on "
        "the encoding. The encoding decides only which four trigrams BBP uses. Under the Shuo "
        "Gua encoding they are Gen, Zhen, Li and Dui (Mountain, Thunder, Fire, Lake); the six "
        "encodings give six different quartets. So the main theorem rests on the cube and its "
        "TIME axis, and the I Ching's line order adds the names."
    )

    def model(self):
        quartets, splits, apices = [], [], []
        for bits in permutations((2, 1, 0)):
            lab = {n: label(l, bits) for n, l in LINES.items()}
            inv = {v: n for n, v in lab.items()}
            apices.append(lab["Qian"] == 7 and lab["Kun"] == 0)
            quartet = tuple(inv[s % 8] for s in BBP_SLOTS)
            quartets.append(quartet)
            fam = sum(1 for n in quartet if sum(LINES[n]) % 2 == 1)
            splits.append(fam)
        shuo = quartets[0]   # bits (2, 1, 0): bottom = MSB
        return (
            Model()
            .add("Encodings with Qian = 7 and Kun = 0", sum(apices))
            .add("Encodings where TIME silence selects BBP", sum(apices))
            .add("Encodings with a 2+2 split", sum(1 for f in splits if f == 2))
            .add("Distinct quartets of trigrams", len(set(frozenset(q) for q in quartets)))
            .add("Quartet under the Shuo Gua encoding", ", ".join(shuo))
        )

    def observations(self):
        return (
            Observed()
            # 111 and 000 are fixed by every permutation of bit positions.
            .add("Encodings with Qian = 7 and Kun = 0", 6)
            .add("Encodings where TIME silence selects BBP", 6)
            # Parity is invariant under bit permutations.
            .add("Encodings with a 2+2 split", 6)
            .add("Distinct quartets of trigrams", 6)
            # Slots 1, 4, 5, 6 = 001, 100, 101, 110 read bottom line first.
            .add("Quartet under the Shuo Gua encoding", "Gen, Zhen, Li, Dui")
        )


ALL_TESTS = [EncodingInvariance]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("06", "Selection under every encoding.", ALL_TESTS) else 1)
