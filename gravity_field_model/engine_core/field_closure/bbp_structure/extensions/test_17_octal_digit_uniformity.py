"""
17. Pi's trigrams and digit pairs are evenly spread
===================================================

Role:     Control: the statistical face of pi's base-8 digits, to set beside its formula structure.
Expected: Passes. A failure means pi's first 10,000 trigrams or their consecutive pairs are unevenly spread at the 0.1% level.

Pi is not random: every digit is fixed by a four-term formula. Its digits
nevertheless look random, which is the content of the conjecture that pi is
normal (in base 8 among others). This test applies the chi-square test to
pi's first 10,000 base-8 digits:

- the 8 trigram frequencies (7 degrees of freedom);
- the 64 frequencies of consecutive digit pairs, the hexagram-like pairs of
  trigrams (63 degrees of freedom).

The p-values should lie between 0.001 and 0.999.
"""

from collections import Counter

from mpmath import gammainc, inf

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL


def chisquare_p(counts):
    """Pearson chi-square p-value against equal frequencies (upper regularised gamma)."""
    n, k = sum(counts), len(counts)
    e = n / k
    x = sum((c - e) ** 2 / e for c in counts)
    return float(gammainc((k - 1) / 2, x / 2, inf, regularized=True))


class OctalDigitUniformity(Test):
    name = "17. Pi's Trigrams Are Evenly Spread"
    question = (
        "Pi's digits are fixed by a formula. Do its base-8 digits, singly and in consecutive "
        "pairs, nevertheless pass a uniformity test?"
    )
    reference = "Pearson chi-square test; normality of pi (conjecture)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Count each of the 8 trigrams in the first 10,000 base-8 digits.")
            .step("Count each of the 64 ordered pairs of consecutive digits.")
            .step("Apply the chi-square test against equal frequencies.")
            .conclude("Both p-values should be unremarkable.")
        )

    commentary = (
        "Both tests pass with unremarkable p-values. Pi's trigrams, one at a time and in "
        "consecutive pairs, are spread as evenly as random digits would be. Together with "
        "test 16 this marks the boundary of the findings: pi's place in the stellated "
        "octahedron is a property of its formula, while its digits, read statistically, look "
        "like any well-mixed sequence."
    )

    def model(self):
        d = list(PI_BASE8_FRACTIONAL)
        singles = Counter(d)
        pairs = Counter(zip(d, d[1:]))
        p1 = chisquare_p([singles[k] for k in range(8)])
        p2 = chisquare_p([pairs[(a, b)] for a in range(8) for b in range(8)])
        return (
            Model()
            .add("Trigram chi-square p-value (info)", round(float(p1), 4))
            .add("Pair chi-square p-value (info)", round(float(p2), 4))
            .add("Both p-values in (0.001, 0.999) (1=yes)", int(0.001 < p1 < 0.999 and 0.001 < p2 < 0.999))
        )

    def observations(self):
        return Observed().add("Both p-values in (0.001, 0.999) (1=yes)", 1)


ALL_TESTS = [OctalDigitUniformity]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("17", "Octal digit uniformity.", ALL_TESTS) else 1)
