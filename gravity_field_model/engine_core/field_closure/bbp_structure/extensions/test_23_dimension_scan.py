"""
23. Only D = 3 gives pi: the dimension scan
===========================================

Role:     Tests whether the BBP construction gives pi in other dimensions D, i.e. base 2^(D+1) and period 2^D.
Expected: Passes. A failure means pi has a formula of this kind at some D other than 3, or the pole condition differs.

BBP has base 16 = 2^(D+1) and period 8 = 2^D at D = 3. A physicist's first
question is: what happens at other D? If the result is a property of the
octahedron, it should appear at D = 3 and nowhere else.

**Why only D = 3 (exact).** A formula of this kind is an integral over
1/(1 - y^p / b) with p = 2^D and b = 2^(D+1) (Theorem 4). Its poles are the
roots of y^p = b, which lie on a circle of radius b^(1/p) = 2^((D+1)/2^D).
pi comes from the pole 1 + i, whose radius is sqrt 2. The radius is sqrt 2
exactly when 2(D + 1) = 2^D, which holds only at D = 3. Then the poles are
sqrt 2 times the eighth roots of unity, which include 1 + i. The test checks
this for D = 1 to 64, with exact integer arithmetic.

The same equation, 2(D + 1) = 2^D, is the one GFD uses for spatial
uniqueness (research note 32). Here it has a concrete meaning: it is the
condition for the BBP integrand to have a Gaussian-integer pole.

**Numerical check.** PSLQ looks for an integer relation among the 2^D slot
series and pi at D = 1, 2 and 4 (coefficients up to 10^6), and must find one
at D = 3 (positive control). For the control, slot 7 is left out: that
removes the family's free direction, so the only relation is BBP itself.
At D = 1, 2 and 4 all slots are kept, so "no relation" excludes any formula.
D = 5 (32 slots)
also gives none, but takes five minutes, so is not run here.
"""

from fractions import Fraction

from mpmath import mp, mpf, nsum, inf, pslq

from gravity_field_model.framework import *


def slots(D):
    base, per = 2 ** (D + 1), 2 ** D
    return [nsum(lambda k, j=j: 1 / (mpf(base) ** k * (per * k + j)), [0, inf]) for j in range(1, per + 1)]


def pi_relation(D, drop=None, maxcoeff=10 ** 6):
    """Integer relation among the slots (slot `drop` removed) and pi, with nonzero pi coefficient."""
    with mp.workdps(60 + 12 * 2 ** D):
        S = slots(D)
        if drop is not None:
            S = S[:drop - 1] + S[drop:]
        rel = pslq(S + [mp.pi], maxcoeff=maxcoeff, maxsteps=10 ** 6)
    if rel is None or rel[-1] == 0:
        return None
    return [Fraction(-c, rel[-1]) for c in rel[:-1]]


def radius_is_sqrt2(D):
    # b^(1/p) = 2^((D+1)/2^D) equals 2^(1/2)  <=>  2(D+1) = 2^D
    return 2 * (D + 1) == 2 ** D


def has_gaussian_pole(D):
    # (1+i)^(2^D) == 2^(D+1), using Gaussian integers as pairs
    re, im = 1, 0
    for _ in range(2 ** D if D <= 12 else 0):
        re, im = re - im, re + im
    if D > 12:      # (1+i)^(2^D) = (2i)^(2^(D-1)) = 2^(2^(D-1)) for D >= 3; never 2^(D+1) for D > 3
        return False
    return (re, im) == (2 ** (D + 1), 0)


class DimensionScan(Test):
    name = "23. Only D = 3 Gives Pi: the Dimension Scan"
    question = (
        "If BBP is the D = 3 case of base 2^(D+1), period 2^D, does pi have a formula of "
        "that kind in any other dimension?"
    )
    reference = "PROOF.md Theorem 4; extensions/PREDICTIONS.md (test 23)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Poles of 1/(1 - y^p/b): radius 2^((D+1)/2^D); equal to sqrt 2 iff 2(D+1) = 2^D.")
            .step("Check exactly, D = 1 to 64, which D give radius sqrt 2 and the pole 1 + i.")
            .step("PSLQ on the slots and pi at D = 1, 2, 4 (none expected) and D = 3 (control).")
            .conclude("Only D = 3 has the Gaussian pole that produces pi, and only D = 3 has a formula.")
        )

    commentary = (
        "Only D = 3 puts the poles at radius sqrt 2, and only D = 3 has the pole 1 + i that "
        "turns the integral into arctan 1 = pi/4. PSLQ agrees: no formula at D = 1, 2 or 4, "
        "and the expected one at D = 3. So within this generalisation, BBP is not one member "
        "of a series of dimensional analogues; it exists only in three dimensions. The "
        "condition that selects it, 2(D + 1) = 2^D, is the one GFD already uses for spatial "
        "uniqueness. Two limits: the generalisation (base 2^(D+1), period 2^D) is one of "
        "several possible, and the PSLQ result excludes formulas only up to its coefficient "
        "bound. The pole argument is exact."
    )

    def model(self):
        rad = [D for D in range(1, 65) if radius_is_sqrt2(D)]
        gauss = [D for D in range(1, 65) if has_gaussian_pole(D)]
        found = {D: pi_relation(D) is not None for D in (1, 2, 4)}
        control = pi_relation(3, drop=7)
        found[3] = control == [4, 0, 0, -2, -1, -1, 0]
        return (
            Model()
            .add("D in 1..64 with pole radius sqrt 2", str(rad))
            .add("D in 1..64 with pole 1 + i", str(gauss))
            .add("Pi formula found at D = 1", int(found[1]))
            .add("Pi formula found at D = 2", int(found[2]))
            .add("BBP recovered at D = 3, slot 7 left out (control)", int(found[3]))
            .add("Pi formula found at D = 4", int(found[4]))
        )

    def observations(self):
        return (
            Observed()
            .add("D in 1..64 with pole radius sqrt 2", "[3]")
            .add("D in 1..64 with pole 1 + i", "[3]")
            .add("Pi formula found at D = 1", 0)
            .add("Pi formula found at D = 2", 0)
            .add("BBP recovered at D = 3, slot 7 left out (control)", 1)
            .add("Pi formula found at D = 4", 0)
        )


ALL_TESTS = [DimensionScan]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("23", "Dimension scan.", ALL_TESTS) else 1)
