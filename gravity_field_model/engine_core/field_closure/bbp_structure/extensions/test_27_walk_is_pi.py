"""
27. The walk is pi: lossless, locally checkable, statistically ordinary
=======================================================================

Role:     Makes exact what "the walk is pi" means (PROOF.md, section 10): the walk identifies pi, its statistics do not.
Expected: Passes. A failure means the walk loses information, fails a ladder check, or a statistic separates pi.

Let d_0 = 3 and d_1, d_2, ... be the base-8 digits of pi, and let the walk be
v_n = (d_0 + ... + d_n) mod 8. The test checks three statements.

1. **Lossless (Proposition 7).** The digits are recovered from the walk by
   d_n = (v_n - v_{n-1}) mod 8. The walk of pi contains all of pi.
2. **Locally checkable (Proposition 8).** Each step of the walk can be checked
   on its own, without the steps before it: v_n - v_{n-1} must equal the
   digit that the BBP ladder computes at position n. pi's walk passes every
   check. The walk of another constant (e) passes about one check in eight,
   so k checks reject it except with probability about 8^-k.
3. **Statistically ordinary (Proposition 9, empirical).** The 64 hexagram
   frequencies of pi's walk and of e's walk are both close to 1/64, and
   neither is closer than random digits usually are. Frequencies do not
   identify the constant.
"""

import random

from mpmath import mp, e as E

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_ladder import octal_digit_at

N = 10_000
CHECKS = 200
SEED = 8


def walk(digits):
    v, s = [], 0
    for d in digits:
        s = (s + d) % 8
        v.append(s)
    return v


def octal_fraction_digits(x_builder, n=N):
    with mp.workdps(int(n * 0.904) + 30):
        x = x_builder()
        f = x - mp.floor(x)
        out = []
        for _ in range(n):
            f *= 8
            d = int(f)
            out.append(d)
            f -= d
        return out


def max_freq_deviation(v):
    counts = [0] * 64
    for a, b in zip(v, v[1:]):
        counts[8 * a + b] += 1
    total = len(v) - 1
    return max(abs(c / total - 1 / 64) for c in counts)


class WalkIsPi(Test):
    name = "27. The Walk Is Pi: Lossless, Locally Checkable, Statistically Ordinary"
    question = (
        "Does the walk carry pi exactly, can each of its steps be checked against pi on its own, "
        "and do its frequencies single out pi?"
    )
    reference = "PROOF.md section 10 (Propositions 7-9); bbp_ladder.py"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Build pi's walk from d_0 = 3 and 10,000 base-8 digits; recover the digits from it.")
            .step("At 200 random positions n, compare v_n - v_{n-1} with the BBP ladder's digit n.")
            .step("Repeat the ladder checks on e's walk.")
            .step("Compare the largest deviation of the 64 hexagram frequencies from 1/64, pi vs e vs random.")
            .conclude("The walk identifies pi exactly; its frequencies do not.")
        )

    commentary = (
        "The walk of pi is pi: the digits come back from it without loss, and every step agrees "
        "with the digit the BBP ladder computes at that position, independently of all earlier "
        "steps. The walk of e passes about one check in eight, as two unrelated digit sequences "
        "should, so even a few checks tell the two apart. What does not tell them apart is "
        "frequency: both walks spread over the 64 hexagrams as evenly as random digits do. So "
        "'the sequence is pi' is exact, and it is decided by the digits themselves (or, before "
        "any walk, by the octahedron's rules, Theorems 2-6), not by the walk's statistics."
    )

    def model(self):
        pi_digits = [3] + list(PI_BASE8_FRACTIONAL[:N])
        v = walk(pi_digits)
        recovered = [v[0]] + [(v[n] - v[n - 1]) % 8 for n in range(1, len(v))]
        rng = random.Random(SEED)
        positions = rng.sample(range(1, N + 1), CHECKS)
        ladder = {n: octal_digit_at(n) for n in positions}
        pi_pass = sum((v[n] - v[n - 1]) % 8 == ladder[n] for n in positions)
        e_digits = [2] + octal_fraction_digits(lambda: +E)
        ve = walk(e_digits)
        e_pass = sum((ve[n] - ve[n - 1]) % 8 == ladder[n] for n in positions)
        rand_dev = sorted(
            max_freq_deviation(walk([3] + [rng.randrange(8) for _ in range(N)])) for _ in range(200)
        )
        lo, hi = rand_dev[2], rand_dev[-3]
        dev_pi, dev_e = max_freq_deviation(v), max_freq_deviation(ve)
        return (
            Model()
            .add("Digits recovered from pi's walk without error (1=yes)", int(recovered == pi_digits))
            .add("Ladder checks passed by pi's walk", pi_pass)
            .add("Ladder checks passed by e's walk (info)", e_pass)
            .add("Share of checks e's walk passes", round(e_pass / CHECKS, 3))
            .add("Largest hexagram-frequency deviation, pi (info)", round(dev_pi, 5))
            .add("Largest hexagram-frequency deviation, e (info)", round(dev_e, 5))
            .add("Pi inside the random 98% range (1=yes)", int(lo <= dev_pi <= hi))
            .add("e inside the random 98% range (1=yes)", int(lo <= dev_e <= hi))
        )

    def observations(self):
        return (
            Observed()
            .add("Digits recovered from pi's walk without error (1=yes)", 1)
            .add("Ladder checks passed by pi's walk", CHECKS)
            # Unrelated digits agree one time in eight.
            .add("Share of checks e's walk passes", 0.125, abs_tol=0.06)
            .add("Pi inside the random 98% range (1=yes)", 1)
            .add("e inside the random 98% range (1=yes)", 1)
        )


ALL_TESTS = [WalkIsPi]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("27", "The walk is pi.", ALL_TESTS) else 1)
