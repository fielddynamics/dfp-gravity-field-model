"""
The I Ching's order of the trigrams as the BBP reading order
============================================================

Role:     PROOF.md Theorem 5: the Shuo Gua family sequence is the order that gives BBP in both tetrahedra.
Expected: Passes. A failure means another documented arrangement also does, or the Shuo Gua sequence does not.

Claim under test: the I Ching documents field closure; it records the order
in which the vertices of the stellated octahedron are visited, and that order
is the BBP structure.

The Shuo Gua (ch. 10) lists the trigrams as a family in a fixed sequence:
father Qian, mother Kun, then the eldest son Zhen and eldest daughter Xun,
the middle son Kan and middle daughter Li, the youngest son Gen and youngest
daughter Dui. As vertices this is 7, 0, 4, 3, 2, 5, 1, 6.

The test checks, from the trigram figures and the cube alone:
- whether the sequence moves between complementary vertices, crossing the
  Field Origin between the two tetrahedra;
- whether reading each tetrahedron's faces in the order the sequence visits
  them, with the six-constraint mechanism of why_pi_formal_derivation.md,
  gives pi (TetB through the complement map, as the derivation prescribes);
- the same for the other documented arrangements (Fu Xi and King Wen), as
  comparisons.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import permutations

from mpmath import mp, pi

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure import geometry_derivation as geo
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import PRECISION, formula_value
from gravity_field_model.engine_core.field_closure.bbp_structure.closure_reading import read
from gravity_field_model.engine_core.field_closure.bbp_structure.iching_orders import (
    ARRANGEMENTS, SHUO_GUA_SEQUENCE, VERTEX, LINES, chamber_order,
)

TOL = mp.mpf(10) ** (-(PRECISION - 20))
SHUO_GUA = "Shuo Gua ch. 10 sequence"


@lru_cache(maxsize=None)
def _reads_pi(order, complement):
    with mp.workdps(PRECISION):
        w, *_ = read(order=order, complement=complement)
        return bool(abs(formula_value(w) - pi) < TOL)


def reads_pi(order, complement):
    return _reads_pi(tuple(order), complement)


def chance_both_chambers():
    """
    Exact fraction of all 8! orderings of the trigrams that give pi in both
    chambers, and of the orderings built from complementary pairs (each
    TetA vertex followed by its complement) that do.
    """
    names = list(VERTEX)
    hits = 0
    total = 0
    for perm in permutations(names):
        total += 1
        hits += reads_pi(chamber_order(perm, "Qian"), False) and reads_pi(chamber_order(perm, "Kun"), True)
    sons = [n for n in names if sum(LINES[n]) % 2 == 1]
    comp = {n: next(m for m in names if all(a + b == 1 for a, b in zip(LINES[n], LINES[m]))) for n in sons}
    p_hits = p_total = 0
    for perm in permutations(sons):
        seq = [x for n in perm for x in (n, comp[n])]
        p_total += 1
        p_hits += reads_pi(chamber_order(seq, "Qian"), False) and reads_pi(chamber_order(seq, "Kun"), True)
    return Fraction(hits, total), Fraction(p_hits, p_total)


class IChingVisitOrder(Test):
    name = "Shuo Gua Family Sequence as the BBP Reading Order"
    question = (
        "Is the order in which the I Ching lists the trigrams (the Shuo Gua family: father, "
        "mother, then sons and daughters by rank) the order of reading that yields the BBP "
        "series for pi in both tetrahedra of the stellated octahedron?"
    )
    reference = (
        "Wilhelm, The I Ching or Book of Changes, trans. Baynes (1950), Shuo Kua chs. 3, 5, 10; "
        "reading mechanism: research/exploratory/i-ching/notes/why_pi_formal_derivation.md"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Map the Shuo Gua sequence to vertices: Qian 7, Kun 0, Zhen 4, Xun 3, Kan 2, Li 5, Gen 1, Dui 6.")
            .step("Check each consecutive pair (father-mother, son-daughter of equal rank) is a complementary pair v, 7-v.")
            .step("Take each tetrahedron's vertices in the order visited and run the face reading (TetB by complement).")
            .step("Repeat for the Fu Xi and King Wen arrangements as comparisons.")
            .conclude("If the I Ching records the reading order, its family sequence should give pi in both chambers.")
        )

    commentary = (
        "The Shuo Gua sequence gives pi in both tetrahedra: father then sons (7, 4, 2, 1) "
        "reads TetA as the BBP series, and mother then daughters (0, 3, 5, 6) reads TetB as "
        "the same series through the complement map. Each pair in the sequence is a vertex "
        "and its complement, so the sequence crosses the Field Origin at every step of a "
        "pair. None of the other documented arrangements does this: the Fu Xi numbering "
        "gives pi for TetA only, and neither circle (Fu Xi or King Wen) gives pi in either "
        "chamber. So the I Ching's family order is the visiting order the BBP reading needs, "
        "as claimed. Two qualifications. The rank of each child is defined in the text by the "
        "position of its single distinctive line (bottom, middle, top), so this is the same "
        "fact as the bottom-to-top line order found in the symmetry test, now located in the "
        "text's own sequence; under a uniformly random ordering of the three sons, one order "
        "in six would give pi (the test computes this exactly, and 1 in 36 for an unrestricted "
        "ordering of all eight). And the reading still uses two conventions not yet derived: "
        "the top line supplies the sector positions, and the magnitude rule is ordered."
    )

    def model(self):
        seq = [VERTEX[n] for n in SHUO_GUA_SEQUENCE]
        pairs = list(zip(seq[0::2], seq[1::2]))
        complementary = sum(1 for a, b in pairs if a + b == 7)
        t1, t2 = [set(t) for t in geo.regular_tetrahedra()]
        crossing = sum(1 for a, b in pairs if (a in t1) != (b in t1))
        m = (
            Model()
            .add("Shuo Gua pairs that are complements v, 7-v (of 4)", complementary)
            .add("Shuo Gua pairs crossing between tetrahedra (of 4)", crossing)
        )
        both = []
        with mp.workdps(PRECISION):
            for name, arr in ARRANGEMENTS.items():
                a = reads_pi(chamber_order(arr, "Qian"), complement=False)
                b = reads_pi(chamber_order(arr, "Kun"), complement=True)
                if name == SHUO_GUA:
                    m.add("Shuo Gua: TetA read in visit order gives pi (1=yes)", int(a))
                    m.add("Shuo Gua: TetB read in visit order gives pi (1=yes)", int(b))
                else:
                    m.add(f"{name}: pi in TetA, TetB (info)", f"{int(a)}, {int(b)}")
                if a and b:
                    both.append(name)
        m.add("Arrangements giving pi in both chambers", len(both))
        m.add("That arrangement is the Shuo Gua sequence (1=yes)", 1 if both == [SHUO_GUA] else 0)
        p_any, p_pairs = chance_both_chambers()
        m.add("Chance: random ordering of all 8 gives pi in both (info)", float(p_any))
        m.add("Chance: random complementary-pair ordering gives pi in both (info)", float(p_pairs))
        return m

    def observations(self):
        return (
            Observed()
            # From the trigram figures: each son and daughter of equal rank are line-for-line opposites.
            .add("Shuo Gua pairs that are complements v, 7-v (of 4)", 4)
            .add("Shuo Gua pairs crossing between tetrahedra (of 4)", 4)
            # Prediction of the claim that the I Ching records the BBP reading order.
            .add("Shuo Gua: TetA read in visit order gives pi (1=yes)", 1)
            .add("Shuo Gua: TetB read in visit order gives pi (1=yes)", 1)
            .add("Arrangements giving pi in both chambers", 1)
            .add("That arrangement is the Shuo Gua sequence (1=yes)", 1)
        )


ALL_TESTS = [IChingVisitOrder]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("I Ching visit order", "The Shuo Gua sequence as the BBP reading order.", ALL_TESTS) else 1)
