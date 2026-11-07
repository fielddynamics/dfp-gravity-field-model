"""
Which I Ching facts fix the line-to-bit encoding?
=================================================

A trigram becomes a cube vertex once each of its three lines is assigned to a
bit. The model uses bottom line = most significant bit (Kun 0 ... Qian 7).
The synthesis ``papers/09-complete-field-closure/IChing_Solve_Synthesis.md``
(section 3) states that three facts validate this encoding and hold only
under it: the parity partition gives regular tetrahedra, the traditional
opposites are complements, and the pi traversal gives the correct TIME-face
completion order.

There are 3! = 6 encodings. This test evaluates each fact under all six, and
adds two facts that do depend on the encoding: Shao Yong's Fu Xi numbering
(Qian 1 ... Kun 8) as descending binary, and the Shuo Gua birth order of the
sons as descending vertex labels, which is the order the BBP face reading
needs.
"""

import math
from itertools import combinations, permutations

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL
from gravity_field_model.engine_core.field_closure import geometry_derivation as geo
from gravity_field_model.engine_core.field_closure.bbp_structure.iching_orders import LINES, ARRANGEMENTS

# Shuo Kua ch. 3: heaven and earth, mountain and lake, thunder and wind, water and fire.
OPPOSITES = [("Qian", "Kun"), ("Gen", "Dui"), ("Zhen", "Xun"), ("Kan", "Li")]
FUXI_NUMBERING = ARRANGEMENTS["Fu Xi numbering 1-8 (Shao Yong)"]
SONS_BY_RANK = ["Zhen", "Kan", "Gen"]  # Shuo Kua ch. 10: eldest, middle, youngest


def label(name, bits):
    """Vertex label of a trigram when line i (bottom, middle, top) is bit bits[i]."""
    return sum(line << b for line, b in zip(LINES[name], bits))


def regular(vertices):
    c = geo.cube_vertices()
    d = {round(math.dist(c[a], c[b]), 9) for a, b in combinations(vertices, 2)}
    return len(d) == 1


def first_time_face_step(apex_labels):
    """Step at which the first TIME face (opposite an apex) completes in the pi walk."""
    tets = [set(t) for t in geo.regular_tetrahedra()]
    faces = []
    for a in apex_labels:
        tet = next(t for t in tets if a in t)
        faces.append(tet - {a})
    seen, cum = set(), 0
    for i, d in enumerate([3] + list(PI_BASE8_FRACTIONAL)):
        cum += d
        seen.add(cum % 8)
        if any(f <= seen for f in faces):
            return i
    return None


class EncodingSelection(Test):
    name = "I Ching Facts That Fix the Trigram Encoding"
    question = (
        "Which properties of the I Ching single out the encoding bottom line = most "
        "significant bit, and which hold under every encoding?"
    )
    reference = (
        "IChing_Solve_Synthesis.md section 3; Wilhelm/Baynes (1950), Shuo Kua chs. 3 and 10; "
        "Shao Yong's Fu Xi numbering"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Enumerate the 6 assignments of (bottom, middle, top) lines to bits (2, 1, 0).")
            .step("For each: are the odd- and even-yang trigrams regular tetrahedra? Are the Shuo Kua opposites complements?")
            .step("For each: at which step does the first TIME face complete in the pi walk?")
            .step("For each: is the Fu Xi numbering descending binary, and is the sons' birth order descending?")
            .conclude("Facts that hold under all 6 cannot validate the encoding; the others can.")
        )

    commentary = (
        "Three of the facts cited as validating the encoding hold under all six encodings: "
        "parity and complement do not depend on which line is which bit, and Qian and Kun are "
        "always 7 and 0, so the TIME faces and the pi walk's TIME-face completion step are "
        "unchanged. They confirm the trigram geometry but not the encoding. Two facts do fix "
        "it, and they fix the same one: Shao Yong's numbering of the Fu Xi arrangement is "
        "descending binary only when the bottom line is the most significant bit, and only "
        "then does the Shuo Gua birth order of the sons (Zhen, Kan, Gen) run 4, 2, 1, the "
        "order the BBP face reading needs. The encoding is therefore documented by the I "
        "Ching's own orderings, not by its geometry."
    )

    def model(self):
        encs = list(permutations((2, 1, 0)))
        n_regular = n_opp = n_time = n_shao = n_birth = 0
        time_steps = set()
        shao_encs, birth_encs = [], []
        for bits in encs:
            lab = {n: label(n, bits) for n in LINES}
            odd = [lab[n] for n in LINES if sum(LINES[n]) % 2 == 1]
            even = [lab[n] for n in LINES if sum(LINES[n]) % 2 == 0]
            n_regular += regular(odd) and regular(even)
            n_opp += all(lab[a] + lab[b] == 7 for a, b in OPPOSITES)
            time_steps.add(first_time_face_step([lab["Qian"], lab["Kun"]]))
            if [lab[n] for n in FUXI_NUMBERING] == list(range(7, -1, -1)):
                n_shao += 1
                shao_encs.append(bits)
            if [lab[n] for n in SONS_BY_RANK] == [4, 2, 1]:
                n_birth += 1
                birth_encs.append(bits)
        n_time = len(encs) if len(time_steps) == 1 else 0
        return (
            Model()
            .add("Encodings giving regular tetrahedra (of 6)", n_regular)
            .add("Encodings making the opposites complements (of 6)", n_opp)
            .add("Encodings with the same TIME-face completion step (of 6)", n_time)
            .add("Encodings making Fu Xi numbering descending binary", n_shao)
            .add("Encodings making the sons' birth order 4, 2, 1", n_birth)
            .add("Both select bottom line = most significant bit (1=yes)",
                 1 if shao_encs == birth_encs == [(2, 1, 0)] else 0)
        )

    def observations(self):
        return (
            Observed()
            # Parity and bitwise complement are unchanged by permuting bit positions.
            .add("Encodings giving regular tetrahedra (of 6)", 6)
            .add("Encodings making the opposites complements (of 6)", 6)
            # Qian -> 7 and Kun -> 0 under every encoding; the walk itself does not change.
            .add("Encodings with the same TIME-face completion step (of 6)", 6)
            # Descending binary needs the line ranks to be the bit ranks.
            .add("Encodings making Fu Xi numbering descending binary", 1)
            .add("Encodings making the sons' birth order 4, 2, 1", 1)
            .add("Both select bottom line = most significant bit (1=yes)", 1)
        )


ALL_TESTS = [EncodingSelection]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Encoding selection", "Which I Ching facts fix the encoding?", ALL_TESTS) else 1)
