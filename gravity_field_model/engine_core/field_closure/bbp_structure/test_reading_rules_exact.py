"""
How sharply the trigram-line reading is determined
==================================================

Role:     PROOF.md Theorem 5: the search over weight rules, and the exact values of the other orders.
Expected: Passes. A failure means a second simple rule also gives pi, or a quoted closed form is wrong.

Theorem 5 writes BBP in the trigram lines with the weight 2b + m + t and the
step 2t + 1 (b, m, t = bottom, middle, top line; 1 = yang). The text states
that the weight rule was found by search and is the only rule of its form
that works. This test makes that statement checkable:

1. Every rule of the form  a*b + c*m + d*t + e  with a, c, d in 0..4 and
   e in -2..2 (625 rules), positive on all four rows, combined with the step
   rule, sign + for the father and - for the sons, and the rank order. The
   test counts the rules whose series equals pi (screened at 60 digits,
   confirmed by exact symbolic integration).
2. The two closed forms quoted for other orders of the sons:
   (Zhen, Gen, Kan) gives ln(675/256) + 2 arctan 2, and
   (Kan, Gen, Zhen) gives ln(50625 sqrt(15)/65536) + 2 arctan 2.

The search shows the rule is sharply determined once its form is fixed. It
does not derive the rule; PROOF.md, section 7, says so.
"""

from itertools import product

import sympy as sp

from gravity_field_model.framework import *
from fractions import Fraction

from mpmath import mp, pi as mpi

from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import formula_value
from gravity_field_model.engine_core.field_closure.bbp_structure.test_octahedron_pi_theorems import (
    LINES, SONS, slot_combination,
)


def series_weights(order, weight):
    """Slot weights for Qian followed by `order`, with step 2t+1 and the given weight rule."""
    rows = ["Qian"] + list(order)
    w, p = {}, 1
    for j, r in enumerate(rows):
        b, m, t = LINES[r]
        slot = ((p - 1) % 8) + 1
        w[slot] = w.get(slot, 0) + (1 if j == 0 else -1) * weight(b, m, t)
        p += 2 * t + 1
    return {k: v for k, v in w.items() if v != 0}


class ReadingRulesExact(Test):
    name = "Trigram-Line Reading: Rule Search and Exact Values"
    question = (
        "Among simple linear weight rules on the three lines, how many give pi with the "
        "Shuo Gua order, and are the closed forms quoted for the other orders exact?"
    )
    reference = "PROOF.md Theorem 5; exact integration with sympy"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Enumerate a*b + c*m + d*t + e for a, c, d in 0..4 and e in -2..2.")
            .step("Keep rules positive on all four rows; build the series with step 2t+1 in rank order.")
            .step("Screen each series at 60 digits; confirm any match with pi by exact integration.")
            .step("Integrate the series for (Zhen, Gen, Kan) and (Kan, Gen, Zhen) and compare with the quoted closed forms.")
            .conclude("One rule of 625 gives pi: 2b + m + t. The quoted values are exact.")
        )

    commentary = (
        "Exactly one of the 625 rules gives pi, the rule 2b + m + t, so the reading is sharply "
        "determined once its linear form is chosen. Because the rule was identified by this "
        "search, the count measures how specific it is, not why it holds. The two closed forms "
        "for other orders of the sons are exact: ln(675/256) + 2 arctan 2 and "
        "ln(50625 sqrt(15)/65536) + 2 arctan 2. They are close to pi (3.18 and 3.31) but not "
        "equal to it."
    )

    def model(self):
        cache, hits = {}, []
        for a, c, d, e in product(range(5), range(5), range(5), range(-2, 3)):
            rule = lambda b, m, t, a=a, c=c, d=d, e=e: a * b + c * m + d * t + e
            if min(rule(*LINES[r]) for r in ["Qian"] + SONS) <= 0:
                continue
            w = series_weights(SONS, rule)
            key = tuple(sorted(w.items()))
            if key not in cache:
                # Screen at 60 digits; confirm any candidate by exact integration.
                with mp.workdps(60):
                    close = abs(formula_value({j: Fraction(v) for j, v in w.items()}) - mpi) < mp.mpf(10) ** -50
                cache[key] = bool(close) and bool(sp.simplify(slot_combination(w) - sp.pi) == 0)
            if cache[key]:
                hits.append((a, c, d, e))
        weight = lambda b, m, t: 2 * b + m + t
        v1 = slot_combination(series_weights(["Zhen", "Gen", "Kan"], weight))
        v2 = slot_combination(series_weights(["Kan", "Gen", "Zhen"], weight))
        f1 = sp.log(sp.Rational(675, 256)) + 2 * sp.atan(2)
        f2 = sp.log(sp.Rational(50625, 65536) * sp.sqrt(15)) + 2 * sp.atan(2)
        same1 = bool(abs(sp.N(v1 - f1, 60)) < sp.Float("1e-50"))
        same2 = bool(abs(sp.N(v2 - f2, 60)) < sp.Float("1e-50"))
        return (
            Model()
            .add("Weight rules tried", 625)
            .add("Weight rules giving pi", len(hits))
            .add("That rule is 2b + m + t (1=yes)", int(hits == [(2, 1, 1, 0)]))
            .add("(Zhen, Gen, Kan) = ln(675/256) + 2 arctan 2 (1=yes)", int(same1))
            .add("(Kan, Gen, Zhen) = ln(50625 sqrt15/65536) + 2 arctan 2 (1=yes)", int(same2))
        )

    def observations(self):
        return (
            Observed()
            .add("Weight rules giving pi", 1)
            .add("That rule is 2b + m + t (1=yes)", 1)
            # Closed forms from exact integration (PROOF.md, Theorem 5).
            .add("(Zhen, Gen, Kan) = ln(675/256) + 2 arctan 2 (1=yes)", 1)
            .add("(Kan, Gen, Zhen) = ln(50625 sqrt15/65536) + 2 arctan 2 (1=yes)", 1)
        )


ALL_TESTS = [ReadingRulesExact]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Reading rules", "Rule search and exact values for the trigram reading.", ALL_TESTS) else 1)
