"""
12. Every formula in pi's family is a ladder
============================================

Role:     Qualifies the ladder finding: digit extraction is a property of the whole family, not of BBP alone.
Expected: Passes. A failure means a family member does not reproduce pi's digits by extraction.

BBP's ladder (bbp_ladder.py) computes frac(16^n pi) from the four slots at
rung n. Every member w(r) of the family has the same base and period, so the
same modular method works with its own weights. This test extracts hex digits
of pi at random rungs from three members: BBP (r = 0), the base -4 formula
(r = -1/4) and r = 1, and compares them with the mpmath digits.
"""

import random

from mpmath import mp

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_ladder import _frac_16n_slot
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import aw_weights

RUNGS = random.Random(16).sample(range(10, 3000), 25)


def scale(r):
    """Smallest positive integer D making every weight of w(r) an integer."""
    from math import lcm
    return lcm(*[c.denominator for c in aw_weights(r).values()])


def hex_from_member(r, n, count=6):
    """Hex digits of frac(16^n * D * pi) from the integer formula D * w(r).

    The fractional part of a sum is only the sum of fractional parts when the
    weights are integers, so a member with fractional weights is first scaled
    by D; it then reaches the digits of D * pi, which for D a power of two are
    pi's own bits, shifted.
    """
    D = scale(r)
    w = aw_weights(r)
    x = sum(int(c * D) * _frac_16n_slot(n, j) for j, c in w.items() if c != 0) % 1.0
    out = []
    for _ in range(count):
        x *= 16
        d = int(x)
        out.append(d)
        x -= d
    return out


def reference_hex(n, D=1, count=6):
    with mp.workdps(4000):
        x = D * mp.pi * mp.mpf(16) ** n
        x -= mp.floor(x)
        out = []
        for _ in range(count):
            x *= 16
            d = int(x)
            out.append(d)
            x -= d
        return out


class FamilyLadders(Test):
    name = "12. Every Member of Pi's Family Is a Ladder"
    question = (
        "Is BBP's ability to reach any digit special to BBP, or shared by every base-16 "
        "formula for pi?"
    )
    reference = "Bailey, Borwein, Plouffe (1997); Adamchik and Wagon (1997)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("For r = 0, -1/4 and 1, take the family member w(r).")
            .step("At 25 random rungs n < 3000, compute frac(16^n pi) from w(r) by modular powers.")
            .step("Members with fractional weights are scaled by D (4 for r = -1/4) and reach D*pi.")
            .step("Compare 6 hex digits per rung with mpmath.")
            .conclude("Digit extraction works for every member.")
        )

    commentary = (
        "All three members reach pi's digits at every rung tested. The ladder belongs to the "
        "whole family: any base-16 formula with integer-friendly denominators allows digit "
        "extraction (a member with fractional weights, such as r = -1/4, is scaled by 4 and "
        "reaches 4 pi, whose bits are pi's shifted by two places). So the ladder is a property of base 16, and of pi having formulas in it, "
        "not a property that singles out BBP. What singles out BBP is TIME silence and its "
        "shape (Theorem 3, tests 02-04); what BBP adds to the ladder is economy, four slots "
        "instead of six or seven."
    )

    def model(self):
        ok = {}
        for r, name in ((0, "r = 0 (BBP)"), (-0.25, "r = -1/4"), (1, "r = 1")):
            from fractions import Fraction
            rr = Fraction(r).limit_denominator(8)
            ok[name] = sum(hex_from_member(rr, n) == reference_hex(n, scale(rr)) for n in RUNGS)
        m = Model()
        for name, k in ok.items():
            m.add(f"{name}: rungs matching (of 25)", k)
        return m

    def observations(self):
        return (
            Observed()
            .add("r = 0 (BBP): rungs matching (of 25)", 25)
            .add("r = -1/4: rungs matching (of 25)", 25)
            .add("r = 1: rungs matching (of 25)", 25)
        )


ALL_TESTS = [FamilyLadders]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("12", "Family ladders.", ALL_TESTS) else 1)
