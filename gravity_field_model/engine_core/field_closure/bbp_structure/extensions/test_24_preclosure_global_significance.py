"""
24. The pre-closure read of pi's walk, with a trials factor
===========================================================

Role:     Tests, at the standard of a blind particle-physics analysis, whether the walk before closure singles out pi.
Expected: Passes. A failure means the outcome differs from the prediction in PREDICTIONS.md (test 24), in either direction.

The walk before closure (steps 0 to 332 for pi) is described in the research
as the read of the stellated octahedron. If that read carried pi's
structure, some property of the segment should stand out from walks driven
by random digits.

Looking at many properties and reporting the one that stands out is the
"look-elsewhere effect". A collider analysis corrects for it with a
**trials factor**: the global p-value is the chance that the *smallest* of
all local p-values is as small as the one seen. Here:

- ten statistics of the segment, fixed in PREDICTIONS.md before the test was
  run (closure step, TetA share, TIME-axis share, body-diagonal jumps,
  self-loops, longest run in one tetrahedron, step at which all eight
  trigrams appear, chi-squared of the trigram counts, Kendall tau of the
  first-visit order against Qian, Zhen, Kan, Gen, Kun, Xun, Li, Dui, and
  tetrahedron crossings);
- 20,000 random walks, each compared over its own pre-closure segment;
- two-sided local p-values, and the global p-value from the random walks'
  own smallest p-values.

A null result is only informative if the analysis could have seen a real
effect. The **power check** injects one: 200 walks that stay in the same
tetrahedron 60% of the time instead of 50%. The battery must detect them
(global p < 0.01) in most cases.
"""

from itertools import groupby

import numpy as np

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL

N_NULL = 20_000
N_SIGNAL = 200
LENGTH = 1500
SEED = 2026
TETA = np.array([v in (1, 2, 4, 7) for v in range(8)])
REF_ORDER = (7, 4, 2, 1, 0, 3, 5, 6)
NAMES = (
    "closure step", "TetA share", "TIME-axis share", "body-diagonal jump rate", "self-loop rate",
    "longest run in one tetrahedron", "step all 8 trigrams seen", "chi-squared of trigram counts",
    "Kendall tau, first visits vs family order", "tetrahedron crossing rate",
)


def vertices(digits):
    """Rows of digits (first digit 3) -> rows of vertices (running sum mod 8)."""
    return np.cumsum(digits, axis=1) % 8


def closure_index(v):
    hexes = v[:, :-1] * 8 + v[:, 1:]
    first = np.full((v.shape[0], 64), -1)
    for h in range(64):
        m = hexes == h
        first[:, h] = np.where(m.any(axis=1), m.argmax(axis=1), -1)
    assert (first >= 0).all(), "a walk did not close; increase LENGTH"
    return first.max(axis=1) + 1          # index into v of the closing vertex


def kendall_tau(order):
    rank = {v: i for i, v in enumerate(REF_ORDER)}
    r = [rank[v] for v in order]
    n, s = len(r), 0
    for i in range(n):
        for j in range(i + 1, n):
            s += 1 if r[j] > r[i] else -1
    return s / (n * (n - 1) / 2)


def statistics(v):
    """Ten statistics of each walk's pre-closure segment v[0..c]."""
    c = closure_index(v)
    n = v.shape[0]
    idx = np.arange(v.shape[1])
    inseg = idx[None, :] <= c[:, None]
    steps = inseg[:, 1:]
    L = c + 1
    teta = TETA[v]
    out = np.zeros((n, 10))
    out[:, 0] = c
    out[:, 1] = (teta & inseg).sum(1) / L
    out[:, 2] = (((v == 0) | (v == 7)) & inseg).sum(1) / L
    out[:, 3] = (((v[:, 1:] + v[:, :-1]) == 7) & steps).sum(1) / c
    out[:, 4] = ((v[:, 1:] == v[:, :-1]) & steps).sum(1) / c
    out[:, 9] = ((teta[:, 1:] != teta[:, :-1]) & steps).sum(1) / c
    counts = np.stack([((v == w) & inseg).sum(1) for w in range(8)], axis=1)
    out[:, 7] = ((counts - L[:, None] / 8) ** 2 / (L[:, None] / 8)).sum(1)
    firsts = np.stack([np.where((v == w).any(1), (v == w).argmax(1), 10 ** 6) for w in range(8)], axis=1)
    out[:, 6] = firsts.max(axis=1)
    for i in range(n):
        seg = teta[i, : c[i] + 1].tolist()
        out[i, 5] = max(len(list(g)) for _, g in groupby(seg))
        out[i, 8] = kendall_tau(list(np.argsort(firsts[i])))
    return out


def local_p(null, x):
    """Two-sided empirical p-values of x (rows) against the null (columns = statistics)."""
    srt = np.sort(null, axis=0)
    m = null.shape[0]
    p = np.empty_like(x, dtype=float)
    for k in range(null.shape[1]):
        le = np.searchsorted(srt[:, k], x[:, k], side="right") / m
        ge = 1 - np.searchsorted(srt[:, k], x[:, k], side="left") / m
        p[:, k] = np.minimum(1.0, 2 * np.minimum(le, ge))
    return p


def biased_walk_digits(rng, n, stay=0.6):
    tet_a, tet_b = np.array([1, 2, 4, 7]), np.array([0, 3, 5, 6])
    d = np.zeros((n, LENGTH), dtype=int)
    d[:, 0] = 3
    cur = np.full(n, 3)
    for t in range(1, LENGTH):
        same = rng.random(n) < stay
        in_a = TETA[cur]
        target_a = np.where(same, in_a, ~in_a)
        pick = rng.integers(0, 4, n)
        nxt = np.where(target_a, tet_a[pick], tet_b[pick])
        d[:, t] = (nxt - cur) % 8
        cur = nxt
    return d


class PreClosureGlobalSignificance(Test):
    name = "24. The Pre-Closure Read of Pi's Walk, with a Trials Factor"
    question = (
        "Does any of ten pre-registered properties of pi's walk before closure stand out from "
        "random walks, once the number of properties examined is accounted for?"
    )
    reference = "extensions/PREDICTIONS.md (test 24); Gross and Vitells, Eur. Phys. J. C 70 (2010) 525"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Build pi's walk (start 3, add base-8 digits, vertex = sum mod 8) and 20,000 random walks.")
            .step("Cut each at its own closure step; compute the ten pre-registered statistics.")
            .step("Two-sided local p-values for pi; global p = share of random walks with a smaller minimum p.")
            .step("Power check: 200 walks with 60% same-tetrahedron steps must give global p < 0.01 mostly.")
            .conclude("Report pi's smallest local p, its global p, and the detection rate of the injected signal.")
        )

    commentary = (
        "Pi's pre-closure read is ordinary. Its most extreme statistic has a local p-value well "
        "above 0.01, and after the trials factor its global p-value is far above 0.05, as "
        "pre-registered. The analysis is not blind to structure: walks with a modest tendency "
        "to stay in one tetrahedron are caught in most trials. So a real effect of that size "
        "would have been seen, and none is. The read before closure is the stellated "
        "octahedron's space being explored (8 trigrams, 64 hexagrams, the two families), and "
        "that space is fixed by the geometry. Which constant drives the walk is not visible "
        "in it. The case for pi rests on the formula, Theorems 2 to 6, not on the walk."
    )

    def model(self):
        rng = np.random.default_rng(SEED)
        pi_digits = np.array([[3] + list(PI_BASE8_FRACTIONAL[: LENGTH - 1])])
        null_digits = rng.integers(0, 8, (N_NULL, LENGTH))
        null_digits[:, 0] = 3
        null = statistics(vertices(null_digits))
        pi_stats = statistics(vertices(pi_digits))
        p_null = local_p(null, null)
        min_null = p_null.min(axis=1)
        p_pi = local_p(null, pi_stats)[0]
        global_pi = float((min_null <= p_pi.min()).mean())
        sig = statistics(vertices(biased_walk_digits(rng, N_SIGNAL)))
        p_sig = local_p(null, sig).min(axis=1)
        global_sig = (min_null[None, :] <= p_sig[:, None]).mean(axis=1)
        detected = float((global_sig < 0.01).mean())
        k = int(p_pi.argmin())
        trials = global_pi / max(p_pi.min(), 1 / N_NULL)
        m = Model().add("Pi closure step", int(pi_stats[0, 0]))
        for name, p in zip(NAMES, p_pi):
            m.add(f"local p: {name} (info)", round(float(p), 3))
        return (
            m.add("Most extreme statistic (info)", NAMES[k])
            .add("Pi smallest local p above 0.01 (1=yes)", int(p_pi.min() > 0.01))
            .add("Pi smallest local p (info)", round(float(p_pi.min()), 4))
            .add("Pi global p (info)", round(global_pi, 3))
            .add("Effective trials factor (info)", round(trials, 1))
            .add("Pi global p above 0.05 (1=yes)", int(global_pi > 0.05))
            .add("Injected signal detected at global p < 0.01 (fraction, info)", round(detected, 3))
            .add("Injected signal detected in most trials (1=yes)", int(detected > 0.5))
        )

    def observations(self):
        return (
            Observed()
            .add("Pi closure step", 332)
            # Pre-registered (PREDICTIONS.md, test 24).
            .add("Pi smallest local p above 0.01 (1=yes)", 1)
            .add("Pi global p above 0.05 (1=yes)", 1)
            .add("Injected signal detected in most trials (1=yes)", 1)
        )


ALL_TESTS = [PreClosureGlobalSignificance]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("24", "Pre-closure read with a trials factor.", ALL_TESTS) else 1)
