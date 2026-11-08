"""
28. Does pi balance itself faster than random digits?
=====================================================

Role:     Tests the hypothesis that pi "self-balances with every new digit", using balance statistics fixed in advance.
Expected: Passes, recording the outcome against the prediction in PREDICTIONS.md (test 28).

For random digits, any count drifts from its balanced value by about sqrt(n)
after n digits. If pi balances itself, its drift should be systematically
smaller. Five balance measures over the first 100,000 base-8 digits of pi, each
scaled by sqrt(n) and maximised over checkpoints n = 1000, 2000, ..., 100,000:

1. digit balance: max_k |c_k(n) - n/8|;
2. chamber balance: walk visits to TetA minus visits to TetB;
3. TIME-axis balance: walk visits to Qian or Kun, minus n/4;
4. digit-sum balance: sum_{i<=n} (d_i - 3.5);
5. hexagram balance: chi-squared of the 64 hexagram counts at n = 100,000.

Each is compared with 1,000 random sequences (lower-tail p: the share of random
sequences at least as balanced as pi), and a global p corrects for five
looks. ln 2, sqrt 2 and e are measured the same way for comparison.
"""

import numpy as np
from mpmath import mp, log, sqrt, e as E, pi as PI

from gravity_field_model.framework import *

N = 100_000
N_RANDOM = 1000
SEED = 28
STEP = 1000
TETA = np.array([v in (1, 2, 4, 7) for v in range(8)])
TIME = np.array([v in (0, 7) for v in range(8)])
NAMES = ("digit balance", "chamber balance", "TIME-axis balance", "digit-sum balance", "hexagram chi-squared")


def octal_digits(builder, n=N):
    with mp.workdps(int(n * 0.904) + 40):
        x = builder()
        integer = int(mp.floor(x))
        frac = int(mp.floor((x - integer) * mp.mpf(8) ** n))
    s = format(frac, "o").rjust(n, "0")
    return integer, np.frombuffer(s.encode(), dtype=np.uint8) - 48


def balance(rows, start):
    """rows: (m, N) digits; start: integer parts (walk starts there). Returns (m, 5)."""
    m, n = rows.shape
    checkpoints = np.arange(STEP, n + 1, STEP)
    scale = np.sqrt(checkpoints)
    out = np.zeros((m, 5))
    onehot_max = np.zeros((m, len(checkpoints)))
    for k in range(8):
        c = np.cumsum(rows == k, axis=1)[:, checkpoints - 1]
        onehot_max = np.maximum(onehot_max, np.abs(c - checkpoints / 8))
    out[:, 0] = (onehot_max / scale).max(axis=1)
    v = (start[:, None] + np.cumsum(rows, axis=1)) % 8
    tet = np.cumsum(np.where(TETA[v], 1, -1), axis=1)[:, checkpoints - 1]
    out[:, 1] = (np.abs(tet) / scale).max(axis=1)
    time = np.cumsum(TIME[v], axis=1)[:, checkpoints - 1]
    out[:, 2] = (np.abs(time - checkpoints / 4) / scale).max(axis=1)
    ds = np.cumsum(rows - 3.5, axis=1)[:, checkpoints - 1]
    out[:, 3] = (np.abs(ds) / scale).max(axis=1)
    hexes = v[:, :-1] * 8 + v[:, 1:]
    for i in range(m):
        counts = np.bincount(hexes[i], minlength=64)
        exp = (n - 1) / 64
        out[i, 4] = ((counts - exp) ** 2 / exp).sum()
    return out


class SelfBalancing(Test):
    name = "28. Does Pi Balance Itself Faster Than Random Digits?"
    question = (
        "Does pi stay closer to balance, digit by digit, than random digits do, on balance "
        "measures built from the stellated octahedron?"
    )
    reference = "extensions/PREDICTIONS.md (test 28)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Compute 100,000 base-8 digits of pi, ln 2, sqrt 2 and e; draw 1,000 random sequences.")
            .step("For each, five balance measures, scaled by sqrt(n), maximised over checkpoints.")
            .step("Lower-tail p for pi on each; global p from the random sequences' own smallest p.")
            .conclude("Self-balancing would show as pi well below the random range on these measures.")
        )

    commentary = (
        "Pi's balance is that of random digits. Its counts drift from balance by about sqrt(n), "
        "as random counts do, on all five measures, including the octahedral ones (the two "
        "chambers, the TIME axis, the 64 hexagrams). ln 2, sqrt 2 and e behave the same way. "
        "So pi does not balance itself faster than chance, at least not in any of these senses. "
        "Its balance is what is expected of a normal number, which pi is conjectured to be."
    )

    def model(self):
        rng = np.random.default_rng(SEED)
        rand = rng.integers(0, 8, (N_RANDOM, N), dtype=np.uint8).astype(np.int64)
        null = balance(rand, np.full(N_RANDOM, 3))
        srt = np.sort(null, axis=0)

        def lower_p(x):
            return np.array([np.searchsorted(srt[:, k], x[k], side="right") / N_RANDOM for k in range(5)])

        null_min = np.array([lower_p(r).min() for r in null])
        results = {}
        for name, b in (("pi", lambda: +PI), ("ln 2", lambda: log(2)), ("sqrt 2", lambda: sqrt(2)), ("e", lambda: +E)):
            ip, d = octal_digits(b)
            stats = balance(d[None, :].astype(np.int64), np.array([ip % 8]))[0]
            p = lower_p(stats)
            results[name] = (stats, p, float((null_min <= p.min()).mean()))
        stats, p, g = results["pi"]
        m = Model()
        for k in range(5):
            m.add(f"pi {NAMES[k]} (info)", round(float(stats[k]), 3))
            m.add(f"pi lower-tail p, {NAMES[k]} (info)", round(float(p[k]), 3))
        for name in ("ln 2", "sqrt 2", "e"):
            m.add(f"{name}: smallest lower-tail p (info)", round(float(results[name][1].min()), 3))
        return (
            m.add("Pi smallest lower-tail p (info)", round(float(p.min()), 3))
            .add("Pi global p (info)", round(g, 3))
            .add("Pi measures below the 5th percentile", int((p < 0.05).sum()))
            .add("Prediction met: smallest p > 0.01 and global p > 0.05 (1=yes)", int(p.min() > 0.01 and g > 0.05))
        )

    def observations(self):
        return (
            Observed()
            .add("Pi measures below the 5th percentile", 0)
            .add("Prediction met: smallest p > 0.01 and global p > 0.05 (1=yes)", 1)
        )


ALL_TESTS = [SelfBalancing]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("28", "Self-balancing.", ALL_TESTS) else 1)
