"""
16. The closure walk driven by other constants
==============================================

Role:     Control for the walk: does the I Ching walk distinguish pi from other constants with the same ladder property?
Expected: Passes. A failure means a constant's walk falls outside the random-digit range, i.e. the walk distinguishes it.

ln 2 also has a base-2 ladder (Bailey, Borwein, Plouffe 1997); sqrt 2 and e
have no known one. If the walk's statistics carried the BBP structure, pi's walk
should stand apart from these. The test runs the walk (start 3, add each base-8
digit, vertex = sum mod 8) for pi, ln 2, sqrt 2 and e, using each constant's
first 4,000 base-8 fractional digits, and measures:

- the step at which all 64 hexagrams have occurred;
- the TetA share of visited vertices.

Each is compared with the 99% range of 500 random digit sequences.
"""

import random

from mpmath import mp

from gravity_field_model.framework import *

N = 4000
TETA = {1, 2, 4, 7}


def octal_digits(make, n=N):
    """`make` builds the constant inside the working precision (a value made outside it is too short)."""
    with mp.workdps(int(n * 0.904) + 30):
        x = make()
        v = x - mp.floor(x)
        out = []
        for _ in range(n):
            v *= 8
            d = int(v)
            out.append(d)
            v -= d
        return out


def walk_stats(digits):
    s, prev, seen, close, teta = 3, None, set(), None, 0
    for i, d in enumerate([0] + digits):
        s += d
        v = s % 8
        teta += v in TETA
        if prev is not None:
            seen.add((prev, v))
            if len(seen) == 64 and close is None:
                close = i
        prev = v
    return close, teta / (len(digits) + 1)


class WalkOtherConstants(Test):
    name = "16. The Walk for Pi, ln 2, sqrt 2 and e"
    question = (
        "Does the I Ching closure walk tell pi apart from ln 2 (which also has a ladder), "
        "sqrt 2 or e?"
    )
    reference = "Bailey, Borwein, Plouffe (1997); walk: closure_walk_proof_iching.py"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Compute 4,000 base-8 digits of pi, ln 2, sqrt 2 and e.")
            .step("Run the walk for each; record the 64-hexagram closure step and the TetA share.")
            .step("Build the 99% range of both statistics from 500 random digit sequences.")
            .conclude("Count the constants inside both ranges.")
        )

    commentary = (
        "All four constants fall inside the random range on both statistics. The walk's "
        "behaviour does not single out pi, nor ln 2, which shares the ladder property. This is "
        "the control the main results need: the case for pi rests on the formula space "
        "(Theorems 2 and 3, tests 02-04), where pi is unique, and not on the walk, where every "
        "well-mixed constant behaves alike."
    )

    def model(self):
        rng = random.Random(64)
        closes, shares = [], []
        for _ in range(500):
            c, t = walk_stats([rng.randrange(8) for _ in range(N)])
            closes.append(c)
            shares.append(t)
        closes.sort()
        shares.sort()
        lo_c, hi_c = closes[2], closes[-3]
        lo_t, hi_t = shares[2], shares[-3]
        m = Model()
        inside = 0
        for name, x in (("pi", lambda: +mp.pi), ("ln 2", lambda: mp.log(2)),
                        ("sqrt 2", lambda: mp.sqrt(2)), ("e", lambda: +mp.e)):
            c, t = walk_stats(octal_digits(x))
            ok = lo_c <= c <= hi_c and lo_t <= t <= hi_t
            inside += ok
            m.add(f"{name}: closure step, TetA share (info)", f"{c}, {t:.3f}")
        m.add("Random 99% range of the closure step (info)", f"{lo_c}-{hi_c}")
        m.add("Constants inside the random range on both", inside)
        return m

    def observations(self):
        return (
            Observed()
            # Expected if the walk does not distinguish these constants from well-mixed digits.
            .add("Constants inside the random range on both", 4)
        )


ALL_TESTS = [WalkOtherConstants]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("16", "Walk for other constants.", ALL_TESTS) else 1)
