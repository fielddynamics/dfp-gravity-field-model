"""
Theorems: the I Ching and the BBP formula as the stellated octahedron
=====================================================================

Machine check of the theorems in PROOF.md (this directory). Everything here
is exact: integer and rational arithmetic, and symbolic integration with
sympy. Nothing is fitted and nothing is read from the model.

Theorem 1  The trigram system is the stellated octahedron, and the Shuo Gua
           ranks fix the encoding.
Theorem 2  BBP is the member of pi's base-16 family selected by the
           octahedron's TIME axis and chamber balance.
Theorem 3  Under the reading R, the rank-ordered octahedron gives exactly
           the BBP coefficients, in both tetrahedra; so it realizes pi.
Theorem 4  The rank order is necessary: the other five orders of the
           children give numbers other than pi, while closure holds in all.

What is proved, and what is assumed (the reading R), is set out in PROOF.md.
"""

from fractions import Fraction
from itertools import combinations, permutations

import sympy as sp

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure import geometry_derivation as geo

# --------------------------------------------------------------------------
# Data from the text (Wilhelm/Baynes 1950, Shuo Kua): lines bottom, middle,
# top; 1 = yang (unbroken).
# --------------------------------------------------------------------------
LINES = {
    "Qian": (1, 1, 1), "Kun": (0, 0, 0),
    "Zhen": (1, 0, 0), "Kan": (0, 1, 0), "Gen": (0, 0, 1),     # sons: eldest, middle, youngest
    "Xun": (0, 1, 1), "Li": (1, 0, 1), "Dui": (1, 1, 0),       # daughters: eldest, middle, youngest
}
SONS = ["Zhen", "Kan", "Gen"]
DAUGHTERS = ["Xun", "Li", "Dui"]
OPPOSITES = [("Qian", "Kun"), ("Gen", "Dui"), ("Zhen", "Xun"), ("Kan", "Li")]   # ch. 3
SHAO_YONG = ["Qian", "Dui", "Li", "Zhen", "Xun", "Kan", "Gen", "Kun"]          # Fu Xi numbering 1..8

BBP = {1: 4, 4: -2, 5: -1, 6: -1}
KERNEL = {1: 8, 2: -8, 3: -4, 4: -8, 5: -2, 6: -2, 7: 1}
y = sp.symbols("y", positive=True)


def label(lines, bits=(2, 1, 0)):
    return sum(l << b for l, b in zip(lines, bits))


def coords(lines):
    return tuple(2 * l - 1 for l in lines)


def slot_combination(weights):
    """
    sum_j w_j S_j with S_j = sum_k 1/(16^k (8k+j)) = 16 int_0^1 y^(j-1)/(16 - y^8) dy
    (expand 1/(16 - y^8) = sum_k y^(8k)/16^(k+1) and integrate term by term).
    """
    num = sp.Add(*[sp.Rational(w) * y ** (j - 1) for j, w in weights.items()])
    return sp.simplify(16 * sp.integrate(num / (16 - y ** 8), (y, 0, 1)))


def reading_R(apex, children, complement=False):
    """
    The reading R (PROOF.md, Definition 4). Rows: apex, then the children in the
    given order. With l = (bottom, middle, top) lines of the row's trigram (or
    their complements, for the yin chamber):
      position: p_0 = 1, p_(j+1) = p_j + 2 t_j + 1
      magnitude: 2 b + m + t
      sign: + for the apex, - for the children.
    Returns the weights by slot 1..8 (residue 0 is slot 8).
    """
    rows = [apex] + list(children)
    lines = [LINES[r] for r in rows]
    if complement:
        lines = [tuple(1 - x for x in l) for l in lines]
    w, p = {}, 1
    for j, (b, m, t) in enumerate(lines):
        slot = ((p - 1) % 8) + 1
        w[slot] = w.get(slot, 0) + (1 if j == 0 else -1) * (2 * b + m + t)
        p += 2 * t + 1
    return {k: v for k, v in w.items() if v != 0}, p - 1


class OctahedronPiTheorems(Test):
    name = "Theorems: I Ching and BBP as the Stellated Octahedron Realizing Pi"
    question = (
        "Can it be proved, exactly, that the I Ching trigram system is the stellated "
        "octahedron, that the BBP formula is the octahedron's member of pi's base-16 "
        "family, and that the rank-ordered octahedron, read by one fixed rule, gives the "
        "BBP series and so pi?"
    )
    reference = (
        "PROOF.md in this directory; Wilhelm/Baynes (1950) Shuo Kua chs. 3, 10; "
        "Bailey, Borwein, Plouffe (1997); Adamchik and Wagon (1997)"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Theorem 1: trigrams -> {-1,+1}^3; families -> parity classes -> the two regular tetrahedra; opposites -> body diagonals; ranks -> bit order.")
            .step("Theorem 2: S_j = 16 int_0^1 y^(j-1)/(16-y^8) dy; BBP integrates to pi and the r-term to 0 exactly; TIME silence and chamber balance force r = 0.")
            .step("Theorem 3: reading R on (Qian; Zhen, Kan, Gen) and on (Kun; Xun, Li, Dui) by complement gives slots 1,4,5,6 with 4,-2,-1,-1.")
            .step("Theorem 4: the other five orders of the children give other numbers; zero sum holds for all six.")
            .conclude("Under R, the I Ching's rank-ordered stellated octahedron realizes pi through the BBP series.")
        )

    commentary = (
        "Every statement checked here holds exactly. The trigram system is the stellated "
        "octahedron: the two Shuo Gua families are the two inscribed regular tetrahedra, the "
        "opposites are the body diagonals, and the hexagrams are the 64 ordered vertex pairs; "
        "the ranks of the children fix the encoding uniquely. The BBP formula is exactly pi, "
        "the r-term of its family is exactly zero, and the octahedron's TIME silence (or "
        "four slots in a 2+2 chamber split) selects BBP alone from that family. Read by R "
        "in rank order, each tetrahedron produces the BBP coefficients and so pi, and no "
        "other order of the children does. The theorem is conditional on R: two of its "
        "clauses (positions from the top line, magnitude 2b + m + t) are stated rules, not "
        "derived from the text or the geometry, as PROOF.md explains."
    )

    def model(self):
        m = Model()
        # ---------------- Theorem 1 ----------------
        labs = {n: label(l) for n, l in LINES.items()}
        m.add("T1a trigrams -> 8 distinct vertices (1=yes)", int(sorted(labs.values()) == list(range(8))))
        yang = [n for n in LINES if sum(LINES[n]) % 2 == 1]
        yin = [n for n in LINES if sum(LINES[n]) % 2 == 0]
        d2 = lambda a, b: sum((p - q) ** 2 for p, q in zip(coords(LINES[a]), coords(LINES[b])))
        reg = all(d2(a, b) == 8 for fam in (yang, yin) for a, b in combinations(fam, 2))
        tets = {frozenset(t) for t in geo.regular_tetrahedra()}
        same = {frozenset(labs[n] for n in yang), frozenset(labs[n] for n in yin)} == tets
        m.add("T1b yang family = father + sons (1=yes)", int(set(yang) == {"Qian", *SONS}))
        m.add("T1b families are regular tetrahedra (edge^2 = 8) (1=yes)", int(reg))
        m.add("T1b families = the cube's two inscribed tetrahedra (1=yes)", int(same))
        opp = all(coords(LINES[b]) == tuple(-c for c in coords(LINES[a])) for a, b in OPPOSITES)
        cross = all((a in yang) != (b in yang) for a, b in OPPOSITES)
        m.add("T1c opposites are antipodes c -> -c (1=yes)", int(opp))
        m.add("T1c every opposite pair joins the two families (1=yes)", int(cross))
        split = [sum(1 for a in A for b in B) for A in (yang, yin) for B in (yang, yin)]
        m.add("T1d hexagrams (ordered pairs)", len(LINES) ** 2)
        m.add("T1d chamber split of hexagrams 16/16/16/16 (1=yes)", int(split == [16, 16, 16, 16]))
        encs = list(permutations((2, 1, 0)))
        rank_ok = [e for e in encs if [label(LINES[s], e) for s in SONS] == [4, 2, 1]]
        shao_ok = [e for e in encs if [label(LINES[n], e) for n in SHAO_YONG] == list(range(7, -1, -1))]
        inv = all(
            {frozenset(label(LINES[n], e) for n in yang), frozenset(label(LINES[n], e) for n in yin)} == tets
            for e in encs
        )
        m.add("T1e families/tetrahedra hold under all 6 encodings (1=yes)", int(inv))
        m.add("T1e encodings making the rank order 4,2,1", len(rank_ok))
        m.add("T1e that encoding is bottom = MSB and matches Shao Yong (1=yes)",
              int(rank_ok == shao_ok == [(2, 1, 0)]))
        # ---------------- Theorem 2 ----------------
        m.add("T2a BBP combination equals pi exactly (1=yes)", int(sp.simplify(slot_combination(BBP) - sp.pi) == 0))
        m.add("T2b r-term combination equals 0 exactly (1=yes)", int(slot_combination(KERNEL) == 0))
        r = sp.symbols("r")
        fam = {j: BBP.get(j, 0) + r * KERNEL.get(j, 0) for j in range(1, 9)}
        # Slot 8 (vertex 0) is empty in every member, so TIME silence reduces to w_7 = 0.
        time_silent = sp.solve(fam[7], r) if fam[8] == 0 else []
        zero_sum = sp.solve(sp.Add(*fam.values()), r)
        zeros = sorted({sp.Rational(z) for j in range(1, 9) for z in sp.solve(fam[j], r)})
        four = [z for z in zeros if sum(1 for j in range(1, 9) if fam[j].subs(r, z) != 0) == 4]
        t1, t2 = [set(t) for t in geo.regular_tetrahedra()]
        balanced = [z for z in four
                    if len({j % 8 for j in range(1, 9) if fam[j].subs(r, z) != 0} & t1) == 2]
        m.add("T2c TIME-silent members: r", str(time_silent))
        m.add("T2c zero-sum members: r", str(zero_sum))
        m.add("T2c four-slot members with a 2+2 chamber split: r", str(balanced))
        m.add("T2c each condition selects r = 0 only (1=yes)",
              int(time_silent == [0] and zero_sum == [0] and balanced == [0]))
        # ---------------- Theorem 3 ----------------
        wa, orbit_a = reading_R("Qian", SONS)
        wb, orbit_b = reading_R("Kun", DAUGHTERS, complement=True)
        m.add("T3 TetA (Qian; Zhen, Kan, Gen) gives the BBP coefficients (1=yes)", int(wa == BBP))
        m.add("T3 TetB (Kun; Xun, Li, Dui) by complement gives them (1=yes)", int(wb == BBP))
        m.add("T3 position increments close one orbit of 8 (1=yes)", int(orbit_a == orbit_b == 8))
        # ---------------- Theorem 4 ----------------
        n_pi, n_zero, values = 0, 0, []
        for order in permutations(SONS):
            w, _ = reading_R("Qian", order)
            v = slot_combination(w)
            values.append(v)
            n_pi += int(sp.simplify(v - sp.pi) == 0)
            n_zero += int(sum(w.values()) == 0)
        min_gap = min(abs(float(sp.re(sp.N(v - sp.pi, 30)))) for v in values if sp.simplify(v - sp.pi) != 0)
        m.add("T4 orders of the children giving pi (of 6)", n_pi)
        m.add("T4 orders with zero coefficient sum (of 6)", n_zero)
        m.add("T4 smallest |value - pi| among the other five", round(min_gap, 6))
        return m

    def observations(self):
        return (
            Observed()
            .add("T1a trigrams -> 8 distinct vertices (1=yes)", 1)
            .add("T1b yang family = father + sons (1=yes)", 1)
            .add("T1b families are regular tetrahedra (edge^2 = 8) (1=yes)", 1)
            .add("T1b families = the cube's two inscribed tetrahedra (1=yes)", 1)
            .add("T1c opposites are antipodes c -> -c (1=yes)", 1)
            .add("T1c every opposite pair joins the two families (1=yes)", 1)
            .add("T1d hexagrams (ordered pairs)", 64)
            .add("T1d chamber split of hexagrams 16/16/16/16 (1=yes)", 1)
            .add("T1e families/tetrahedra hold under all 6 encodings (1=yes)", 1)
            .add("T1e encodings making the rank order 4,2,1", 1)
            .add("T1e that encoding is bottom = MSB and matches Shao Yong (1=yes)", 1)
            .add("T2a BBP combination equals pi exactly (1=yes)", 1)
            .add("T2b r-term combination equals 0 exactly (1=yes)", 1)
            .add("T2c each condition selects r = 0 only (1=yes)", 1)
            .add("T3 TetA (Qian; Zhen, Kan, Gen) gives the BBP coefficients (1=yes)", 1)
            .add("T3 TetB (Kun; Xun, Li, Dui) by complement gives them (1=yes)", 1)
            .add("T3 position increments close one orbit of 8 (1=yes)", 1)
            .add("T4 orders of the children giving pi (of 6)", 1)
            .add("T4 orders with zero coefficient sum (of 6)", 6)
        )


ALL_TESTS = [OctahedronPiTheorems]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Octahedron pi theorems", "Exact check of PROOF.md.", ALL_TESTS) else 1)
