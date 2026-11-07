"""
The BBP ladder reaches the base-8 digits of pi directly
=======================================================

Claim under test: the BBP formula lets one move through pi like a ladder,
going to any rung (digit position) without climbing the ones below; and the
I Ching walk needs pi in base 8, one trigram per digit.

The test computes base-8 digits of pi at random positions up to 10,000 using
only the BBP formula at that position (bbp_ladder.py), and compares them with
the stored digits, which were computed independently with mpmath. It also
checks the ladder in the other power-of-two bases and the 12-bit alignment of
the hexadecimal and octal groupings.

Background (not computed here): Borwein, Borwein and Galway (2004) proved
that pi has no Machin-type BBP formula in any base b that is not a power of
2, so base 10, for example, has no such ladder of this type.
"""

import random
from math import gcd

from mpmath import mp

from gravity_field_model.framework import *
from gravity_field_model.common import PI_BASE16_DIGITS
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_ladder import (
    hex_digits_at, octal_digit_at, base_2k_digit_at,
)

N_POSITIONS = 300
SEED = 8
D = 3


def _mp_digits(base, count):
    with mp.workdps(count * 2 + 50):
        f = mp.pi - 3
        out = []
        for _ in range(count):
            f *= base
            d = int(f)
            out.append(d)
            f -= d
        return out


class BBPLadderBase8(Test):
    name = "BBP Ladder: Base-8 Digits of Pi at Any Position"
    question = (
        "Can the base-8 digits of pi, the trigrams that drive the walk, be reached at any "
        "position directly from the BBP formula, without computing the digits before them?"
    )
    reference = (
        "Bailey, Borwein, Plouffe (1997), Math. Comp. 66, 903-913; Borwein, Borwein, Galway "
        "(2004), Canad. J. Math. 56, 897-925; stored digits: mpmath, common/pi_data.py"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("At rung n, the BBP slots give frac(16^n pi) with modular powers: no digit before n is used.")
            .step("Octal digit m is bits 3m-2..3m of pi's binary expansion; read them from the rung holding those bits.")
            .step("Compare with the mpmath digits at 300 random positions up to 10,000, and the first 64 hex digits.")
            .step("Repeat in bases 2, 4, 16, 32 and 64.")
            .conclude("Hex and octal regroup the same bits; they realign every lcm(4, 3) = 12 bits.")
        )

    commentary = (
        "Every digit checked is right: the BBP formula reaches any base-8 digit of pi on its "
        "own, without the digits below it, at positions up to 10,000. So the trigram stream "
        "of pi is addressable, rung by rung, from the formula's four slots. That is a "
        "property random digits do not have: a random sequence has no formula that produces "
        "its millionth digit. It works because 8 = 2^3 and 16 = 2^4 are powers of two, so the "
        "octal and hexadecimal expansions are one binary stream in 3-bit and 4-bit groups; "
        "the ladder works in every power-of-two base tested. For bases that are not powers "
        "of 2, such as 10, pi has no BBP formula of the Machin type (Borwein, Borwein and "
        "Galway 2004). Among the ladder bases, base 8 is the one whose digit is exactly one "
        "trigram (3 bits). The 12-bit realignment of hex and octal is fixed by the bit widths "
        "4 and 3."
    )

    def model(self):
        rng = random.Random(SEED)
        positions = rng.sample(range(1, len(PI_BASE8_FRACTIONAL) + 1), N_POSITIONS)
        oct_ok = sum(octal_digit_at(m) == PI_BASE8_FRACTIONAL[m - 1] for m in positions)
        stored_hex = [int(c, 16) for c in PI_BASE16_DIGITS[1:]]
        ladder_hex = []
        n = 0
        while len(ladder_hex) < len(stored_hex):
            ladder_hex += hex_digits_at(n, 4)
            n += 4
        hex_ok = sum(a == b for a, b in zip(ladder_hex, stored_hex))
        bases_ok = 0
        for k in (1, 2, 4, 5, 6):
            ref = _mp_digits(2 ** k, 100)
            bases_ok += all(base_2k_digit_at(m, k) == ref[m - 1] for m in range(1, 101))
        bases_ok += oct_ok == N_POSITIONS
        window = 4 * D // gcd(4, D)
        return (
            Model()
            .add("Octal digits from the ladder that match (fraction)", oct_ok / N_POSITIONS)
            .add("Hex digits 1-64 from the ladder that match (fraction)", hex_ok / len(stored_hex))
            .add("Power-of-two bases 2^1..2^6 where the ladder works", bases_ok)
            .add("Bits per hex/octal realignment", window)
            .add("Octal digits per window", window // D)
            .add("Hex digits per window", window // 4)
            .add("Bits per base-8 digit = lines per trigram", D)
        )

    def observations(self):
        return (
            Observed()
            # mpmath digits, computed independently of the BBP formula.
            .add("Octal digits from the ladder that match (fraction)", 1.0, abs_tol=0.0)
            .add("Hex digits 1-64 from the ladder that match (fraction)", 1.0, abs_tol=0.0)
            .add("Power-of-two bases 2^1..2^6 where the ladder works", 6)
            # lcm(4, 3) = 12.
            .add("Bits per hex/octal realignment", 12)
            .add("Octal digits per window", 4)
            .add("Hex digits per window", 3)
            # A trigram has three lines.
            .add("Bits per base-8 digit = lines per trigram", 3)
        )


ALL_TESTS = [BBPLadderBase8]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("BBP ladder", "Base-8 digits of pi from the BBP formula at any position.", ALL_TESTS) else 1)
