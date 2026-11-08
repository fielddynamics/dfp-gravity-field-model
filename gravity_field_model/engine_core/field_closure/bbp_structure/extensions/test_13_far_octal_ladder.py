"""
13. The trigram ladder far beyond the stored digits
===================================================

Role:     Extends test_bbp_ladder_base8.py from position 10,000 to positions near 100,000.
Expected: Passes. A failure means a far trigram from the ladder disagrees with an independent computation.

The stored digits stop at 10,000. The ladder does not. This test reads 40
base-8 digits of pi (trigrams) at random positions between 90,000 and 100,000,
each from its own BBP rung, and compares them with pi computed independently by
mpmath to 100,000 octal places (about 90,400 decimal digits).
"""

import random

from mpmath import mp

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_ladder import octal_digit_at

POSITIONS = sorted(random.Random(90).sample(range(90_000, 100_001), 40))


def reference_octal(positions):
    top = max(positions)
    with mp.workdps(int(top * 0.904) + 50):          # log10(8) = 0.903
        n = int(mp.floor((mp.pi - 3) * mp.mpf(8) ** top))
    s = oct(n)[2:].zfill(top)
    return [int(s[m - 1]) for m in positions]


class FarOctalLadder(Test):
    name = "13. Trigrams of Pi Near the 100,000th Place"
    question = (
        "Does the ladder keep giving the right trigrams far beyond any stored table, near "
        "the 100,000th base-8 place?"
    )
    reference = "Bailey, Borwein, Plouffe (1997); mpmath arbitrary-precision pi"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Pick 40 random base-8 positions between 90,000 and 100,000.")
            .step("Read each from its hexadecimal rung with the BBP ladder.")
            .step("Compute pi to 100,000 octal places with mpmath and read the same positions.")
            .conclude("Every ladder trigram should match.")
        )

    commentary = (
        "All forty far trigrams match. The ladder reaches the 100,000th trigram of pi in a "
        "fraction of a second each, without the 99,999 before it, and agrees with a full "
        "arbitrary-precision computation. Every rung of the walk's digit supply is reachable "
        "directly."
    )

    def model(self):
        ladder = [octal_digit_at(m) for m in POSITIONS]
        ref = reference_octal(POSITIONS)
        return (
            Model()
            .add("Far positions checked", len(POSITIONS))
            .add("Ladder trigrams matching mpmath", sum(a == b for a, b in zip(ladder, ref)))
        )

    def observations(self):
        return (
            Observed()
            .add("Far positions checked", 40)
            .add("Ladder trigrams matching mpmath", 40)
        )


ALL_TESTS = [FarOctalLadder]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("13", "Far octal ladder.", ALL_TESTS) else 1)
