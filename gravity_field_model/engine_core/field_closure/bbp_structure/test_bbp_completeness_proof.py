"""
Proof that the octahedron's TIME axis selects BBP from all of pi's formulas
=========================================================================

Exact check of Theorems 2 and 3 of PROOF.md:

Theorem 2 (completeness). The only rational linear relation among the slot
series S_j = sum_k 16^-k/(8k+j), j = 1..8, is the Adamchik-Wagon relation
8S_1 - 8S_2 - 4S_3 - 8S_4 - 2S_5 - 2S_6 + S_7 = 0. Hence the base-16,
period-8 formulas for pi are exactly BBP + r (that relation).

Proof outline (each step checked here):
1. Partial fractions: S_j = -(1/8) sum_{w^8=1} (sqrt2 w)^j L_w, with
   L_w = int_0^1 dy/(y - sqrt2 w) = log(1 - conj(w)/sqrt2).
2. Each L_w is a rational combination of the seven logarithms
   Lambda = (i pi, log 2, log(1+sqrt2), log(2+i), log(2-i), log(sqrt2+i), log(sqrt2-i)),
   by exact factorisations in Q(zeta_8), branch fixed numerically.
3. Lambda is linearly independent over Q (unique factorisation of ideals in
   Z[zeta_8]: the primes above 2, 3 and 5 separate the exponents; 1+sqrt2 is
   not a root of unity). By Baker's theorem it is then linearly independent
   over the algebraic numbers.
4. So a rational relation sum q_j S_j = 0 holds iff the algebraic coefficient
   of every log vanishes: a rational linear system of 28 equations in 8
   unknowns. Its solution space is one-dimensional and is the
   Adamchik-Wagon relation.

Theorem 3 (selection). In the I Ching encoding, slot 7 is Qian (father) and
slot 8 is Kun (mother): the TIME apices. Exactly one formula for pi leaves
both silent: BBP. It then follows, without being assumed, that the formula
has four active slots, two in each tetrahedron, and weights summing to zero.
"""

import sympy as sp
from mpmath import mp, mpf, mpc, quad, nsum, inf, log as mlog, pi as mpi

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure import geometry_derivation as geo

I, S2 = sp.I, sp.sqrt(2)
ZETA = sp.exp(I * sp.pi / 4)
LAMBDA_ARGS = [-1, 2, 1 + S2, 2 + I, 2 - I, S2 + I, S2 - I]   # Lambda_k = Log(arg_k); Log(-1) = i pi
LAMBDA_NAMES = ["i pi", "log 2", "log(1+sqrt2)", "log(2+i)", "log(2-i)", "log(sqrt2+i)", "log(sqrt2-i)"]

h, q = sp.Rational(1, 2), sp.Rational(1, 4)
# beta_w = 1 - conj(w)/sqrt2 for w = zeta^k, its factorisation, and Log beta_w over Lambda.
L_TABLE = {
    0: ((S2 - 1) / S2, [0, -h, -1, 0, 0, 0, 0]),
    1: ((1 + I) / 2, [q, -h, 0, 0, 0, 0, 0]),
    2: ((S2 + I) / S2, [0, -h, 0, 0, 0, 1, 0]),
    3: ((1 + I) * (2 - I) / 2, [q, -h, 0, 0, 1, 0, 0]),
    4: ((S2 + 1) / S2, [0, -h, 1, 0, 0, 0, 0]),
    5: ((1 - I) * (2 + I) / 2, [-q, -h, 0, 1, 0, 0, 0]),
    6: ((S2 - I) / S2, [0, -h, 0, 0, 0, 0, 1]),
    7: ((1 - I) / 2, [-q, -h, 0, 0, 0, 0, 0]),
}
AW = [8, -8, -4, -8, -2, -2, 1, 0]
BBP = [4, 0, 0, -2, -1, -1, 0, 0]
DPS = 60


def _num(e):
    v = sp.N(e, DPS + 10)
    return mpc(mpf(str(sp.re(v))), mpf(str(sp.im(v))))


def slot_coefficients():
    """S_j as algebraic coefficient vectors over Lambda (step 1 + step 2)."""
    out = []
    for j in range(1, 9):
        vec = [0] * 7
        for k in range(8):
            f = sp.expand(-sp.Rational(1, 8) * sp.expand_complex((S2 * ZETA ** k) ** j))
            for t in range(7):
                vec[t] += f * L_TABLE[k][1][t]
        out.append([sp.nsimplify(sp.expand(x)) for x in vec])
    return out


def q_parts(e):
    """Coordinates of an element of Q(zeta_8) = Q(sqrt2, i) in the basis 1, sqrt2, i, i sqrt2."""
    e = sp.expand(e)
    re, im = e.as_real_imag()
    a = re.subs(S2, 0)
    b = sp.expand(re - a) / S2
    c = im.subs(S2, 0)
    d = sp.expand(im - c) / S2
    assert sp.simplify(a + b * S2 + I * (c + d * S2) - e) == 0
    return [sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c), sp.nsimplify(d)]


def norm_q_zeta8(x):
    """Norm from Q(zeta_8) to Q: product over the automorphisms zeta -> zeta^a, a = 1,3,5,7."""
    # sqrt2 = zeta + zeta^-1 and i = zeta^2 transform as: a=1: (s2, i); a=3: (-s2, -i); a=5: (-s2, i); a=7: (s2, -i)
    s, i_ = sp.symbols("s i_")
    expr = sp.sympify(x).subs({S2: s, I: i_})
    prod = 1
    for sv, iv in [(S2, I), (-S2, -I), (-S2, I), (S2, -I)]:
        prod *= expr.subs({s: sv, i_: iv})
    return sp.nsimplify(sp.expand(prod))


class BBPCompletenessProof(Test):
    name = "Proof: the TIME Axis Selects BBP from All of Pi's Base-16 Formulas"
    question = (
        "Can it be proved, not just found numerically, that the formulas for pi in base 16 "
        "with period 8 form exactly the Adamchik-Wagon family, so that leaving the I Ching's "
        "father and mother (the TIME apices) silent selects BBP and nothing else?"
    )
    reference = (
        "PROOF.md (Theorems 2, 3); A. Baker, Mathematika 13 (1966) 204-216 (linear forms in "
        "logarithms); Adamchik and Wagon (1997); Bailey, Borwein, Plouffe (1997)"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Partial fractions over the 8th roots of unity write each S_j through eight logarithms L_w.")
            .step("Exact factorisations in Q(zeta_8) write every L_w over seven logarithms Lambda.")
            .step("Lambda is Q-independent (primes above 2, 3, 5 and the unit 1+sqrt2), hence independent over the algebraic numbers (Baker).")
            .step("Rational relations among the S_j are the rational kernel of a 28 x 8 matrix: one-dimensional, the Adamchik-Wagon relation.")
            .step("So pi's formulas are BBP + r * AW; parents silent forces r = 0.")
            .conclude("BBP is the only formula of this type that leaves the TIME apices silent; chamber balance and closure follow.")
        )

    commentary = (
        "This closes the gap that was numerical before. The slot series span a space of "
        "dimension exactly 7, so pi has exactly a one-parameter family of base-16, period-8 "
        "formulas, and the octahedron's TIME axis, read through the I Ching encoding (father "
        "Qian = slot 7, mother Kun = slot 8), cuts it to the single BBP formula. Only that one "
        "condition is imposed. The rest of the octahedral structure then follows as theorems: "
        "the formula uses exactly K = 4 slots, two in each tetrahedron (Mountain and Thunder "
        "from the father's family, Fire and Lake from the mother's), and its weights sum to "
        "zero. The proof uses Baker's theorem on linear forms in logarithms, a standard "
        "result of transcendental number theory; every other step is exact algebra."
    )

    def model(self):
        m = Model()
        # Step 2: factorisations exact; branch of each Log fixed against the integral.
        fact_ok = all(sp.simplify(sp.expand_complex(beta - (1 - sp.conjugate(ZETA ** k) / S2))) == 0
                      for k, (beta, _) in L_TABLE.items())
        with mp.workdps(DPS):
            lam = [_num(sp.log(a)) if a != -1 else mpc(0, mpi) for a in LAMBDA_ARGS]
            worst_L = mpf(0)
            for k, (_, vec) in L_TABLE.items():
                a = _num(S2 * ZETA ** k)
                integral = quad(lambda yv: 1 / (yv - a), [0, 1])
                rhs = sum(_num(c) * l for c, l in zip(vec, lam))
                worst_L = max(worst_L, abs(integral - rhs))
        m.add("Step 2: factorisations of 1 - conj(w)/sqrt2 exact (1=yes)", int(fact_ok))
        m.add("Step 2: max |L_w - combination of Lambda|", float(worst_L))
        # Step 1: S_j over Lambda, checked against the series.
        coeffs = slot_coefficients()
        with mp.workdps(DPS):
            worst_S = max(
                abs(sum(_num(c) * l for c, l in zip(coeffs[j - 1], lam))
                    - nsum(lambda n: 1 / (mpf(16) ** n * (8 * n + j)), [0, inf]))
                for j in range(1, 9)
            )
        m.add("Step 1: max |S_j - combination of Lambda|", float(worst_S))
        # Step 3: Q-independence of Lambda via ideals of Z[zeta_8].
        norms = {n: norm_q_zeta8(x) for n, x in zip(LAMBDA_NAMES[3:], LAMBDA_ARGS[3:])}
        coprime_5 = sp.simplify((2 + I) * (2 - I) - ((2 + I) + (2 - I)) - 1) == 0      # 5 - 4 = 1
        coprime_3 = sp.simplify(3 * (S2 + I) * (S2 - I) - ((S2 + I) + (S2 - I)) ** 2 - 1) == 0  # 9 - 8 = 1
        res_deg = all(pow(p, 2, 8) == 1 and p % 8 != 1 for p in (3, 5))   # order 2 mod 8
        unit_infinite = abs(float(1 + S2)) > 1
        m.add("Step 3: norms of 2+i, 2-i (25) and sqrt2+i, sqrt2-i (9) (1=yes)",
              int([norms[k] for k in LAMBDA_NAMES[3:]] == [25, 25, 9, 9]))
        m.add("Step 3: 2+i, 2-i coprime and sqrt2+i, sqrt2-i coprime (1=yes)", int(coprime_5 and coprime_3))
        m.add("Step 3: 3 and 5 have residue degree 2 in Q(zeta_8) (1=yes)", int(res_deg))
        m.add("Step 3: 1+sqrt2 is not a root of unity (1=yes)", int(unit_infinite))
        # Step 4: the rational relation space.
        M = sp.Matrix([[q_parts(coeffs[j][t])[c] for j in range(8)] for t in range(7) for c in range(4)])
        ns = M.nullspace()
        kern = []
        if len(ns) == 1:
            v = ns[0] / ns[0][6]
            kern = [int(x) for x in v]
        m.add("Step 4: rank of the 28 x 8 rational system", M.rank())
        m.add("Step 4: dimension of the rational relation space", len(ns))
        m.add("Step 4: the relation is Adamchik-Wagon (1=yes)", int(kern == AW))
        target = sp.Matrix([(-1 if (t == 0 and c == 2) else 0) for t in range(7) for c in range(4)])  # pi = -i (i pi)
        sol, params = M.gauss_jordan_solve(target)
        tau = list(params)[0] if params.shape[0] else sp.Integer(0)
        particular = [sp.nsimplify(x.subs(tau, 0)) for x in sol]
        m.add("Step 4: pi lies in the span, particular solution = BBP (1=yes)", int(particular == BBP))
        # Theorem 3: parents silent -> r = 0, and the consequences.
        r = sp.symbols("r")
        fam = [sp.nsimplify(x.subs(tau, r)) for x in sol]
        sol_r = sp.solve([fam[6], fam[7]], r, dict=True)
        unique = len(sol_r) == 1 and sol_r[0][r] == 0
        w0 = [x.subs(r, 0) for x in fam]
        active = {(j + 1) % 8 for j, x in enumerate(w0) if x != 0}
        t1, t2 = [set(t) for t in geo.regular_tetrahedra()]
        m.add("Thm 3: formulas for pi with Qian and Kun silent", len(sol_r))
        m.add("Thm 3: that formula is BBP (1=yes)", int(unique and [int(x) for x in w0] == BBP))
        m.add("Thm 3 consequence: active slots", len(active))
        m.add("Thm 3 consequence: two active in each tetrahedron (1=yes)",
              int(len(active & t1) == 2 and len(active & t2) == 2))
        m.add("Thm 3 consequence: weights sum to zero (1=yes)", int(sum(w0) == 0))
        return m

    def observations(self):
        return (
            Observed()
            .add("Step 2: factorisations of 1 - conj(w)/sqrt2 exact (1=yes)", 1)
            .add("Step 2: max |L_w - combination of Lambda|", 0.0, abs_tol=1e-40)
            .add("Step 1: max |S_j - combination of Lambda|", 0.0, abs_tol=1e-40)
            .add("Step 3: norms of 2+i, 2-i (25) and sqrt2+i, sqrt2-i (9) (1=yes)", 1)
            .add("Step 3: 2+i, 2-i coprime and sqrt2+i, sqrt2-i coprime (1=yes)", 1)
            .add("Step 3: 3 and 5 have residue degree 2 in Q(zeta_8) (1=yes)", 1)
            .add("Step 3: 1+sqrt2 is not a root of unity (1=yes)", 1)
            .add("Step 4: rank of the 28 x 8 rational system", 7)
            .add("Step 4: dimension of the rational relation space", 1)
            .add("Step 4: the relation is Adamchik-Wagon (1=yes)", 1)
            .add("Step 4: pi lies in the span, particular solution = BBP (1=yes)", 1)
            .add("Thm 3: formulas for pi with Qian and Kun silent", 1)
            .add("Thm 3: that formula is BBP (1=yes)", 1)
            .add("Thm 3 consequence: active slots", 4)
            .add("Thm 3 consequence: two active in each tetrahedron (1=yes)", 1)
            .add("Thm 3 consequence: weights sum to zero (1=yes)", 1)
        )


ALL_TESTS = [BBPCompletenessProof]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("BBP completeness proof", "TIME axis selects BBP from all formulas.", ALL_TESTS) else 1)
