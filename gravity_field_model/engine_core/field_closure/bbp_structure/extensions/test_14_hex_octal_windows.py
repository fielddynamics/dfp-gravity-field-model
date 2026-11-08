"""
14. Three hexadecimal digits are four trigrams, window by window
================================================================

Role:     Checks the 12-bit alignment (research §5 of bbp_field_closure_synthesis.md) on the actual digits of pi.
Expected: Passes. A failure means a window's hex and octal digits disagree bit for bit.

Base 16 and base 8 cut the same binary stream into 4-bit and 3-bit groups,
which realign every 12 bits. So for every window w = 0, 1, 2, ... the three
hexadecimal digits 3w+1..3w+3 and the four base-8 digits 4w+1..4w+4 must spell
the same 12 bits. This test checks the first 2,000 windows (8,000 trigrams),
with the hex digits taken from the BBP ladder and the base-8 digits from the
stored mpmath table: two independent computations.
"""

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_ladder import hex_digits_at

N_WINDOWS = 2000


class HexOctalWindows(Test):
    name = "14. Three Hex Digits Are Four Trigrams"
    question = (
        "Do the BBP ladder's hexadecimal digits and the stored base-8 digits of pi spell the "
        "same bits in every 12-bit window?"
    )
    reference = "bbp_field_closure_synthesis.md section 5; stored digits: common/pi_data.py (mpmath)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("For each window w, take hex digits 3w+1..3w+3 from rung 3w of the ladder.")
            .step("Take base-8 digits 4w+1..4w+4 from the stored table.")
            .step("Write both as 12-bit strings and compare.")
            .conclude("Every window should agree.")
        )

    commentary = (
        "All 2,000 windows agree: twelve bits, three hexadecimal digits, four trigrams. The "
        "ladder works natively in base 16; the I Ching walk reads base 8; this check shows "
        "concretely that they read one stream, and that every group of four trigrams is "
        "fixed by three rungs of the ladder."
    )

    def model(self):
        ok = 0
        for w in range(N_WINDOWS):
            hx = hex_digits_at(3 * w, 3)
            hbits = "".join(format(d, "04b") for d in hx)
            obits = "".join(format(d, "03b") for d in PI_BASE8_FRACTIONAL[4 * w:4 * w + 4])
            ok += hbits == obits
        return (
            Model()
            .add("Windows checked", N_WINDOWS)
            .add("Windows where 3 hex digits = 4 trigrams", ok)
        )

    def observations(self):
        return (
            Observed()
            .add("Windows checked", 2000)
            .add("Windows where 3 hex digits = 4 trigrams", 2000)
        )


ALL_TESTS = [HexOctalWindows]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("14", "Hex-octal windows.", ALL_TESTS) else 1)
