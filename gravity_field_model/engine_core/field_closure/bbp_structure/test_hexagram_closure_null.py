"""
Does the I Ching closure walk require pi?
=========================================

The closure walk (``research/exploratory/i-ching/closure_walk_proof_iching.py``):
start with pi's integer part 3, add each base-8 digit of pi, and take the
running sum mod 8 as the current trigram. Each consecutive pair of trigrams is
a hexagram. The walk closes when all 64 hexagrams have occurred; for pi this
happens at step 332.

If closure needed pi, other digit sequences should close later, rarely, or
not at all. This test runs the same walk on 2000 uniformly random digit
sequences (each also starting with 3) and compares. The independent
reference for the random walk is the coupon-collector expectation: each step
draws one of 64 equally likely hexagrams, so the mean time to see all 64 is
64 * H_64 = 303.6 steps (H_n the harmonic number). Successive hexagrams share
a trigram, so this is an approximation, checked here to 5%.
"""

import random
import statistics

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL

N_RANDOM = 2000
SEED = 64


def closure_step(digits):
    """Index (in `digits`) at which all 64 hexagrams have occurred, or None."""
    cum, prev, seen = 0, None, set()
    for i, d in enumerate(digits):
        cum += d
        v = cum % 8
        if prev is not None:
            seen.add((prev, v))
            if len(seen) == 64:
                return i
        prev = v
    return None


def coupon_collector_mean(n=64):
    return n * sum(1.0 / k for k in range(1, n + 1))


class HexagramClosureNull(Test):
    name = "I Ching Closure Walk: Pi vs Random Digits"
    question = (
        "Does the walk need pi to complete all 64 hexagrams, or does any well-mixed digit "
        "sequence close it in the same way?"
    )
    reference = (
        "Walk: research/exploratory/i-ching/closure_walk_proof_iching.py; "
        "coupon-collector mean n H_n (Feller, An Introduction to Probability Theory, Vol. 1)"
    )
    tolerance = 0.05
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Run the walk on 3 followed by the base-8 digits of pi; record the closure step.")
            .step("Run it on 2000 random sequences, each starting with 3.")
            .step("Compare the random mean with the coupon-collector value 64 H_64.")
            .step("Place pi's closure step in the random distribution.")
            .conclude("If pi sits inside the random range, closure is a property of the walk, not of pi.")
        )

    commentary = (
        "Every random sequence closes the walk, on average at about step 304, the "
        "coupon-collector value for 64 equally likely hexagrams. Pi closes at step 332, "
        "inside the random range (roughly the 70th percentile). The hexagram walk therefore "
        "does not need pi: any sequence whose digits are well mixed completes the 64 "
        "hexagrams in about this time, as the research note on the walk also observes. What "
        "the I Ching supplies is the space the walk explores (8 trigrams, 64 hexagrams, the "
        "parity families, the body-diagonal opposites), and that space is fixed by the "
        "cube's geometry with no reference to pi. The claim that pi itself is forced rests on "
        "the six-constraint reading; the two reading tests in this package examine it."
    )

    def model(self):
        pi_step = closure_step([3] + list(PI_BASE8_FRACTIONAL))
        rng = random.Random(SEED)
        steps = []
        for _ in range(N_RANDOM):
            s = closure_step([3] + [rng.randrange(8) for _ in range(5000)])
            if s is not None:
                steps.append(s)
        steps.sort()
        lo, hi = steps[int(0.005 * len(steps))], steps[int(0.995 * len(steps)) - 1]
        pct = sum(1 for s in steps if s < pi_step) / len(steps)
        return (
            Model()
            .add("Pi closure step", pi_step)
            .add("Random sequences that close (fraction)", len(steps) / N_RANDOM)
            .add("Mean random closure step", statistics.mean(steps))
            .add("Std of random closure step (info)", statistics.stdev(steps))
            .add("Pi percentile among random walks (info)", round(pct, 3))
            .add("Pi inside the random 99% range (1=yes)", 1 if lo <= pi_step <= hi else 0)
        )

    def observations(self):
        return (
            Observed()
            # Reported by closure_walk_proof_iching.py (mpmath digits).
            .add("Pi closure step", 332, abs_tol=0)
            .add("Random sequences that close (fraction)", 1.0, abs_tol=0.0)
            # 64 * H_64; the shared trigram between successive hexagrams makes it approximate.
            .add("Mean random closure step", round(coupon_collector_mean(), 1), tol=0.05)
            .add("Pi inside the random 99% range (1=yes)", 1)
        )


ALL_TESTS = [HexagramClosureNull]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Hexagram closure", "Does the closure walk require pi?", ALL_TESTS) else 1)
