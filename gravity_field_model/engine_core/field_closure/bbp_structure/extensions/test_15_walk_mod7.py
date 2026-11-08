"""
15. What a ladder can and cannot say about the walk's position
==============================================================

Role:     Sharpens the ladder/walk distinction (test_walk_from_bbp_ladder.py) with an exact identity.
Expected: Passes. A failure means the mod-7 identity fails, or the walk position is predictable from the prefix mod 8.

The walk's position after n trigrams is (3 + d_1 + ... + d_n) mod 8. The
ladder gives each d_i directly, but the position needs their sum. There is an
exact identity for the sum modulo 7: since 8 = 1 (mod 7),

    d_1 + ... + d_n  =  N_n  (mod 7),   N_n = floor(8^n (pi - 3)),

the integer formed by the first n trigrams. Modulo 8 there is no such
identity: N_n mod 8 is just the last trigram d_n. This test checks the mod-7
identity for n = 1..1500 exactly, and counts how often the digit sum agrees
with N_n modulo 8 (expected about 1 in 8, by chance).
"""

from mpmath import mp

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL

N = 1500


class WalkMod7(Test):
    name = "15. The Walk's Digit Sum: Exact Mod 7, Not Mod 8"
    question = (
        "The walk adds the trigrams. Is the running sum determined by pi's prefix as a "
        "number, modulo 7 and modulo 8?"
    )
    reference = "Casting out (b - 1): for base b, a number is congruent to its digit sum mod b - 1"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Compute N_n = floor(8^n (pi - 3)) exactly for n = 1500, and its prefixes by shifting.")
            .step("Compare the digit sum with N_n modulo 7 for every n.")
            .step("Count agreements modulo 8.")
            .conclude("The digit sum is fixed mod 7 by pi's prefix; mod 8 it is not.")
        )

    commentary = (
        "The identity holds for every n: the walk's digit sum modulo 7 equals pi's first n "
        "trigrams read as an integer, modulo 7 (casting out sevens, as one casts out nines in "
        "base 10). Modulo 8, the cube's own modulus, agreement happens about one time in "
        "eight, i.e. by chance. So the walk's position on the cube is a genuinely cumulative "
        "quantity: the ladder supplies each step, but no known identity turns the position "
        "into a single rung."
    )

    def model(self):
        with mp.workdps(int(N * 0.904) + 50):
            big = int(mp.floor((mp.pi - 3) * mp.mpf(8) ** N))
        ok7 = agree8 = 0
        s = 0
        for n in range(1, N + 1):
            s += PI_BASE8_FRACTIONAL[n - 1]
            Nn = big >> (3 * (N - n))
            ok7 += (s - Nn) % 7 == 0
            agree8 += (s - Nn) % 8 == 0
        return (
            Model()
            .add("Prefixes checked", N)
            .add("Mod-7 identity holds", ok7)
            .add("Mod-8 agreement rate", agree8 / N)
        )

    def observations(self):
        return (
            Observed()
            .add("Prefixes checked", 1500)
            .add("Mod-7 identity holds", 1500)
            # Chance agreement for a residue mod 8: 1/8, sampling sd ~ 0.0085 for 1500 trials.
            .add("Mod-8 agreement rate", 0.125, abs_tol=0.03)
        )


ALL_TESTS = [WalkMod7]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("15", "Walk digit sum mod 7.", ALL_TESTS) else 1)
