"""
29. The Clifford reading: the TIME axis carries BBP's base, period and pole
===========================================================================

Role:     Makes exact the link between the trigrams as Cl(3,0), the TIME axis, and the BBP formula (PROOF.md, section 11).
Expected: Passes. A failure means one of the algebraic identities below is wrong.

Read each yang line as a basis vector: bottom e1, middle e2, top e3. Each
trigram becomes a basis blade of Cl(3,0), the geometric algebra of space:
Kun = 1, the sons e1, e2, e3, the daughters e2e3, e1e3, e1e2, Qian = I = e1e2e3.
The test checks, exactly:

1. The grades are 1, 3, 3, 1: the layers mother | sons | daughters | father
   along the TIME axis.
2. The centre of the algebra (elements commuting with everything) is spanned by
   Kun and Qian, and I^2 = -1: the TIME axis is a copy of the complex numbers.
3. The mother's family is closed under multiplication and each daughter squares
   to -1 (the quaternions); the father's family is the odd part.
4. Multiplication by I sends every trigram to its Fu Xi opposite (up to sign).
5. The TIME-axis element 1 + I (Kun + Qian) satisfies (1 + I)^8 = 16, BBP's
   base; z = (1 + I)/sqrt 2 has order exactly 8, BBP's period; and the
   roots of y^8 = 16 on the TIME axis are (1 + I) z^m. The root 1 + I is the
   pole that produces pi (Theorem 4).
6. Every TIME-silent element (grades 1 and 2 only) squares onto the TIME axis;
   for BBP's weighting W, W^2 = 18 - 8I.
7. Multiplication by 1 + I does not produce BBP's weights from a simpler
   element: the link runs through the denominator (base, period, pole), not
   the numerator.
8. Two group structures on the eight trigrams: XOR (line changes, Clifford
   products, Hamming distance, opposites) and addition mod 8 (the walk, BBP's
   slots, the eighth roots). Place value identifies them. They agree on 36 of
   the 64 pairs, and for every trigram only for the steps 0 and 4.
"""

from fractions import Fraction
from itertools import product

from gravity_field_model.framework import *

KUN, QIAN = 0, 7
SONS, DAUGHTERS = (4, 2, 1), (3, 5, 6)
TETA, TETB = {1, 2, 4, 7}, {0, 3, 5, 6}
W_BBP = {1: 4, 4: -2, 5: -1, 6: -1}    # Gen +4, Zhen -2, Li -1, Dui -1


# --- Cl(3,0) on 3-bit blade masks (bit 2 = e1, bit 1 = e2, bit 0 = e3) --------------------------
def _vectors(m):
    return [i for i in range(3) if m >> (2 - i) & 1]


def blade_sign(a, b):
    A, B = _vectors(a), _vectors(b)
    return -1 if sum(1 for x in A for y in B if x > y) % 2 else 1


def mul(X, Y):
    Z = {}
    for a, x in X.items():
        for b, y in Y.items():
            Z[a ^ b] = Z.get(a ^ b, 0) + blade_sign(a, b) * x * y
    return {k: v for k, v in Z.items() if v != 0}


def add(*Xs):
    Z = {}
    for X in Xs:
        for k, v in X.items():
            Z[k] = Z.get(k, 0) + v
    return {k: v for k, v in Z.items() if v != 0}


def power(X, n):
    R = {0: 1}
    for _ in range(n):
        R = mul(R, X)
    return R


def grade(m):
    return bin(m).count("1")


ONE, I = {0: 1}, {7: 1}


class CliffordReading(Test):
    name = "29. The Clifford Reading: the TIME Axis Carries BBP's Base, Period and Pole"
    question = (
        "Read as Cl(3,0), what is the TIME axis, and how exactly does it connect to the "
        "BBP formula's base 16, period 8 and the pole 1 + i that produces pi?"
    )
    reference = "PROOF.md section 11; research notes 13 and 15 (great-pyramid/active_work)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Map trigrams to Cl(3,0) blades (yang line = basis vector).")
            .step("Check grades, centre, even subalgebra and multiplication by I exactly.")
            .step("Compute powers of 1 + I and the order of (1 + I)/sqrt 2 in the centre.")
            .step("Square BBP's weighting; test whether (1 + I) generates it.")
            .step("Compare XOR and addition mod 8 on the eight labels.")
            .conclude("The TIME axis is the algebra's complex line, and it carries BBP's denominator.")
        )

    commentary = (
        "Read as the geometric algebra of space, the stellated octahedron is graded 1, 3, 3, 1 "
        "along its TIME axis, and that axis, Kun to Qian, is the algebra's centre: a copy of "
        "the complex numbers, with Qian as the unit I, I^2 = -1. Multiplying by I is the Fu Xi "
        "opposition; the mother's family is the quaternions. On this axis, Kun + Qian = 1 + I "
        "is exactly the number BBP is built on: its eighth power is 16, the base; (1 + I)/sqrt 2 "
        "has order 8, the period; and 1 + I is the pole that produces pi. So the octahedron's "
        "TIME axis carries the complex structure in which BBP's pi arises, while BBP's weights "
        "live on the ring of six children around it and square back onto the axis. The link "
        "runs through BBP's denominator: multiplication by 1 + I does not generate its "
        "weights. The identification of the TIME axis with C is canonical up to orientation "
        "(I or -I), and BBP, being real, does not depend on that choice, which agrees with the "
        "reading's achirality (test 22). Finally, the eight trigrams carry two group "
        "structures, line changes (XOR) and the walk's addition mod 8; place value identifies "
        "them, and they agree only for staying put or changing the bottom line."
    )

    def model(self):
        grades = tuple(sum(1 for v in range(8) if grade(v) == g) for g in range(4))
        layers_ok = (
            {v for v in range(8) if grade(v) == 0} == {KUN}
            and {v for v in range(8) if grade(v) == 1} == set(SONS)
            and {v for v in range(8) if grade(v) == 2} == set(DAUGHTERS)
            and {v for v in range(8) if grade(v) == 3} == {QIAN}
        )
        centre = sorted(v for v in range(8) if all(mul({v: 1}, {u: 1}) == mul({u: 1}, {v: 1}) for u in range(8)))
        i_squared = mul(I, I)
        even_closed = all((a ^ b) in TETB for a in TETB for b in TETB)
        daughters_sq = all(mul({d: 1}, {d: 1}) == {0: -1} for d in DAUGHTERS)
        odd_times_odd_even = all((a ^ b) in TETB for a in TETA for b in TETA)
        opposites = all(set(mul(I, {v: 1})) == {7 - v} for v in range(8))
        one_plus_i = add(ONE, I)
        p8 = power(one_plus_i, 8)
        p2 = power(one_plus_i, 2)
        # z = (1+I)/sqrt2: z^n = (1+I)^n / 2^(n/2); its order is the least n with (1+I)^n = 2^(n/2)
        order = next(n for n in range(1, 17) if n % 2 == 0 and power(one_plus_i, n) == {0: 2 ** (n // 2)})
        # roots of y^8 = 16 of the form (1+I) z^m, m = 0..7: check (1+I)^(m+1)^8 / 2^(4m) == 16
        roots_ok = all(
            {k: Fraction(v, 2 ** (4 * m)) for k, v in power(power(one_plus_i, m + 1), 8).items()} == {0: 16}
            for m in range(8)
        )
        W2 = mul(W_BBP, W_BBP)
        # every element with grades 1 and 2 only squares into span{1, I} (generic check on a grid)
        silent_to_axis = True
        for coeffs in product((-1, 0, 2), repeat=6):
            X = {v: c for v, c in zip((4, 2, 1, 3, 5, 6), coeffs) if c}
            if not set(mul(X, X)) <= {0, 7}:
                silent_to_axis = False
                break
        # (1+I)^-1 = (1 - I)/2; is (1+I)^-1 W a "simpler" element (integer, at most 4 terms)?
        pre = {k: Fraction(v, 2) for k, v in mul(add(ONE, {7: -1}), W_BBP).items()}
        pre_simple = int(all(x.denominator == 1 for x in pre.values()) and len(pre) <= 4)
        agree = sum(1 for a in range(8) for d in range(8) if (a + d) % 8 == (a ^ d))
        always = [d for d in range(8) if all((a + d) % 8 == (a ^ d) for a in range(8))]
        return (
            Model()
            .add("Grade counts", str(grades))
            .add("Grades are mother | sons | daughters | father (1=yes)", int(layers_ok))
            .add("Centre of the algebra (labels)", str(centre))
            .add("I^2", str(i_squared))
            .add("Mother's family closed, daughters square to -1 (1=yes)", int(even_closed and daughters_sq))
            .add("Father's family times father's family lands in mother's (1=yes)", int(odd_times_odd_even))
            .add("Multiplication by I gives the Fu Xi opposite (1=yes)", int(opposites))
            .add("(1 + I)^2", str(p2))
            .add("(1 + I)^8", str(p8))
            .add("Order of (1 + I)/sqrt 2", order)
            .add("(1 + I) z^m solve y^8 = 16 for m = 0..7 (1=yes)", int(roots_ok))
            .add("W^2 for BBP's weighting", str(W2))
            .add("TIME-silent elements square onto the TIME axis (1=yes)", int(silent_to_axis))
            .add("BBP's W is (1 + I) times a simpler element (1=yes)", pre_simple)
            .add("Pairs where addition mod 8 equals XOR", agree)
            .add("Steps where they agree for every trigram", str(always))
        )

    def observations(self):
        return (
            Observed()
            .add("Grade counts", "(1, 3, 3, 1)")
            .add("Grades are mother | sons | daughters | father (1=yes)", 1)
            .add("Centre of the algebra (labels)", "[0, 7]")
            .add("I^2", "{0: -1}")
            .add("Mother's family closed, daughters square to -1 (1=yes)", 1)
            .add("Father's family times father's family lands in mother's (1=yes)", 1)
            .add("Multiplication by I gives the Fu Xi opposite (1=yes)", 1)
            .add("(1 + I)^2", "{7: 2}")
            .add("(1 + I)^8", "{0: 16}")
            .add("Order of (1 + I)/sqrt 2", 8)
            .add("(1 + I) z^m solve y^8 = 16 for m = 0..7 (1=yes)", 1)
            # |v|^2 - |B|^2 + 2 v^B with v = 4e3 - 2e1, B = -e13 - e12: 20 - 2 = 18, and -8 I.
            .add("W^2 for BBP's weighting", "{0: 18, 7: -8}")
            .add("TIME-silent elements square onto the TIME axis (1=yes)", 1)
            .add("BBP's W is (1 + I) times a simpler element (1=yes)", 0)
            .add("Pairs where addition mod 8 equals XOR", 36)
            .add("Steps where they agree for every trigram", "[0, 4]")
        )


ALL_TESTS = [CliffordReading]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("29", "The Clifford reading.", ALL_TESTS) else 1)
