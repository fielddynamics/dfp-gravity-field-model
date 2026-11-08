"""
05. Period 8 is the smallest that writes pi in base 16
======================================================

Role:     Supports the formula type of PROOF.md: why period 8 = 2^D rather than a shorter one.
Expected: Passes. A failure means a base-16 formula for pi with period 1..7 exists within the search bound.

The theorems use base 16 = K^2 and period 8 = 2^D. Base 16 alone does not fix
the period: a formula could use denominators p k + j for any period p. This
test asks, for p = 1, ..., 8, whether pi is a rational combination of the p
slot series sum_k 16^-k/(p k + j), j = 1..p.

Method: PSLQ at 120 digits on (T_1, ..., T_p, pi) with coefficients up to
10^9. For p <= 7 no integer relation exists within that bound (not even one
among the T_j alone). For p = 8 PSLQ returns BBP. The negative results are
numerical bounds, not proofs.
"""

from mpmath import mp, mpf, nsum, inf, pi, pslq

from gravity_field_model.framework import *

DPS, BOUND = 120, 10 ** 9


def relation(period):
    with mp.workdps(DPS):
        T = [nsum(lambda k, j=j: 1 / (mpf(16) ** k * (period * k + j)), [0, inf]) for j in range(1, period + 1)]
        return pslq(T + [+pi], maxcoeff=BOUND, maxsteps=10 ** 7)


class MinimalPeriod(Test):
    name = "05. The Smallest Base-16 Period That Writes Pi"
    question = (
        "In base 16, could pi be written with a period shorter than 8? Which is the smallest "
        "period whose slot series reach pi?"
    )
    reference = "PSLQ: Ferguson, Bailey, Arno (1999), Math. Comp. 68, 351-369"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("For p = 1..8, compute T_j = sum_k 16^-k/(p k + j), j = 1..p, to 120 digits.")
            .step("Run PSLQ on (T_1..T_p, pi) with coefficients up to 10^9.")
            .conclude("Record the smallest p for which pi appears in a relation.")
        )

    commentary = (
        "No base-16 formula for pi exists with period 1 to 7 within coefficients of 10^9 (and "
        "at those periods the slot series satisfy no relation at all). Period 8 is the first, "
        "and PSLQ returns exactly BBP there. So in base 16 = K^2, the period 8 = 2^D, one slot "
        "per cube vertex, is the shortest that reaches pi. This is numerical evidence within a "
        "bound, not a proof of non-existence."
    )

    def model(self):
        first = None
        rels = {}
        for p in range(1, 9):
            rels[p] = relation(p)
            if first is None and rels[p] is not None and rels[p][-1] != 0:
                first = p
        r8 = rels[8]
        bbp = [-x * (1 if r8[-1] > 0 else -1) for x in r8[:-1]] if r8 else None
        return (
            Model()
            .add("Periods 1-7 with any relation", sum(1 for p in range(1, 8) if rels[p] is not None))
            .add("Smallest period writing pi", first)
            .add("Formula found at period 8", " ".join(map(str, bbp)) if bbp else "none")
        )

    def observations(self):
        return (
            Observed()
            .add("Periods 1-7 with any relation", 0)
            .add("Smallest period writing pi", 8)
            # BBP: 4 S_1 - 2 S_4 - S_5 - S_6 (Bailey, Borwein, Plouffe 1997).
            .add("Formula found at period 8", "4 0 0 -2 -1 -1 0 0")
        )


ALL_TESTS = [MinimalPeriod]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("05", "Minimal base-16 period for pi.", ALL_TESTS) else 1)
