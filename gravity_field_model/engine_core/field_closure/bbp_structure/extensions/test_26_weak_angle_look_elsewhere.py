"""
26. Look-elsewhere audit of the weak mixing angle formula
=========================================================

Role:     Tests GFD's closed form for sin^2(theta_W) against the current measurement, and how many formulas of its form fit.
Expected: Passes, recording the outcome. Of the two pre-registered predictions (PREDICTIONS.md, test 26), one was met and one was not.

Research note 33 gives

    sin^2(theta_W) = (3/13) (1 + a/4 + 13 a^2/8) = 0.231210        (a = alpha)

with 3 = D, 13 = Phi_6, 4 = K and 8 = SO_v, and compares it with the MS-bar
value 0.23121(4), reporting agreement to 0.9 ppm.

Two checks a collider physicist would make:

1. **Is the comparison value current?** The 2024 Review of Particle
   Physics (PDG, Table 10.2) gives sin^2 theta-hat_W(M_Z) = 0.23129(4) in the
   MS-bar scheme. Against that the formula is 2 sigma low.
2. **How many formulas of the same form fit?** The grammar (p/q)(1 + c1 a +
   c2 a^2), with p and q from the framework numbers {1, 2, 3, 4, 8, 13, 17, 21}
   and c1, c2 from the framework numbers divided by 1, 2, 4 or 8, is searched for formulas within
   1 sigma of the old and of the current value.

A note on procedure: the first run used test 25's menu (denominators 1, 2,
4), which does not contain the formula's own coefficient 13/8. That was a
construction error, so denominator 8 was added and the test rerun. The
first run's counts were 16 formulas within 1 sigma of 0.23121 and 5 within 1
sigma of 0.23129.

If many formulas fit either value, the formula's match to the old one was
not evidence, and a formula of this kind can be found for whatever value is
measured next.

**Outcome against the pre-registration.**
- More than 1.5 sigma from the current value: **met** (2.0 sigma low).
- More than ten menu formulas within 1 sigma of the current value: **not
  met**. There are nine (and 28 near the old value).

The nine include (3/13)(1 + a/4 + 8a^2) = 0.231289, which differs from the
published formula only in the a^2 coefficient (8, i.e. SO_v, in place of
13/8) and is 0.04 sigma from the current value. A one-symbol change refits
the new measurement.
"""

from fractions import Fraction

import numpy as np

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions.test_25_mass_ratio_look_elsewhere import (
    ALPHA_2018, FRAMEWORK,
)

# Test 25's menu has denominators 1, 2, 4; the coefficient 13/8 needs 8 (= SO_v, a framework
# number). The first run omitted it, so the formula was outside its own grammar; denominator 8
# was added to make the menu contain it. See the docstring.
_v = sorted({Fraction(a, b) for a in FRAMEWORK for b in (1, 2, 4, 8)})
COEFFS = [Fraction(0)] + _v + [-x for x in _v]

OLD, NEW, SIGMA = 0.23121, 0.23129, 0.00004      # research note 33; PDG 2024 Table 10.2
N_FAKE = 2000
SEED = 13


def gfd_formula(a=ALPHA_2018):
    return 3 / 13 * (1 + a / 4 + 13 * a * a / 8)


def values(a=ALPHA_2018):
    lead = sorted({Fraction(p, q) for p in FRAMEWORK for q in FRAMEWORK})
    signed = COEFFS
    L = np.array([float(x) for x in lead])
    C = np.array([float(c) for c in signed])
    return (L[:, None, None] * (1 + C[None, :, None] * a + C[None, None, :] * a * a)).ravel(), len(lead), len(signed)


class WeakAngleLookElsewhere(Test):
    name = "26. Look-Elsewhere Audit of the sin^2(theta_W) Formula"
    question = (
        "GFD's (3/13)(1 + a/4 + 13a^2/8) matched sin^2(theta_W) = 0.23121. Does it match the "
        "current value, and how many formulas of the same form would have matched either?"
    )
    reference = "Research note 33; PDG 2024, Review 10 (Electroweak model), Table 10.2; PREDICTIONS.md (test 26)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Evaluate the formula; compare with 0.23121(4) and with PDG 2024's 0.23129(4).")
            .step("Build every (p/q)(1 + c1 a + c2 a^2) from the framework menu.")
            .step("Count menu formulas within 1 sigma of each value, and of 2,000 fake values.")
            .conclude("A grammar that fits any value near 0.231 cannot be confirmed by fitting one of them.")
        )

    commentary = (
        "The formula gives 0.231210. It matched the value it was built against, 0.23121(4), "
        "but the current PDG value is 0.23129(4), and the formula is now 2 sigma low. That is "
        "not yet a refutation, but it is the direction a falsifiable prediction can fail. The "
        "grammar does not care: it holds 28 formulas within 1 sigma of the old value, 9 within "
        "1 sigma of the new one (fewer than the ten pre-registered), and at least one within "
        "1 sigma of every fake value tried between 0.2305 and 0.2320. The simplest fit to the "
        "new value, (3/13)(1 + a/4 + 8a^2), changes one coefficient of the published formula. "
        "So agreement with either value carries little weight. A prediction would have to fix the coefficients by a rule stated "
        "before the comparison, and specify the renormalisation scheme and scale, since the "
        "MS-bar and effective angles differ by 0.00032, eight times the uncertainty."
    )

    def model(self):
        a = ALPHA_2018
        v, n_lead, n_c = values()
        f = gfd_formula()
        rng = np.random.default_rng(SEED)
        fakes = rng.uniform(0.2305, 0.2320, N_FAKE)
        srt = np.sort(v)
        lo = np.searchsorted(srt, fakes - SIGMA)
        hi = np.searchsorted(srt, fakes + SIGMA)
        covered = float((hi > lo).mean())
        n_old = int((np.abs(v - OLD) <= SIGMA).sum())
        n_new = int((np.abs(v - NEW) <= SIGMA).sum())
        return (
            Model()
            .add("Formula value", round(f, 6))
            .add("Formula minus old value 0.23121, in sigma (info)", round((f - OLD) / SIGMA, 2))
            .add("Formula minus PDG 2024 value 0.23129, in sigma", round((f - NEW) / SIGMA, 1))
            .add("Formula in the menu (1=yes)",
                 int(Fraction(3, 13) in {Fraction(p, q) for p in FRAMEWORK for q in FRAMEWORK}
                     and Fraction(1, 4) in COEFFS and Fraction(13, 8) in COEFFS))
            .add("Menu formulas (info)", len(v))
            .add("Menu formulas within 1 sigma of 0.23121", n_old)
            .add("Menu formulas within 1 sigma of 0.23129", n_new)
            .add("Pre-registered: more than ten within 1 sigma of 0.23129 (1=yes)", int(n_new > 10))
            .add("(3/13)(1 + a/4 + 8a^2) minus PDG 2024, in sigma", round((3 / 13 * (1 + a / 4 + 8 * a * a) - NEW) / SIGMA, 2))
            .add("Fake values in 0.2305-0.2320 with a menu formula within 1 sigma (fraction)", round(covered, 3))
        )

    def observations(self):
        return (
            Observed()
            .add("Formula value", 0.23121, abs_tol=0.000001)
            # Pre-registered: more than 1.5 sigma from the current value.
            .add("Formula minus PDG 2024 value 0.23129, in sigma", -2.0, abs_tol=0.1)
            .add("Formula in the menu (1=yes)", 1)
            # Outcome recorded after the run (exact enumeration).
            .add("Menu formulas within 1 sigma of 0.23121", 28)
            .add("Menu formulas within 1 sigma of 0.23129", 9)
            # Pre-registered prediction (> 10) not met.
            .add("Pre-registered: more than ten within 1 sigma of 0.23129 (1=yes)", 0)
            .add("(3/13)(1 + a/4 + 8a^2) minus PDG 2024, in sigma", -0.04, abs_tol=0.01)
            .add("Fake values in 0.2305-0.2320 with a menu formula within 1 sigma (fraction)", 1.0, abs_tol=0.02)
        )


ALL_TESTS = [WeakAngleLookElsewhere]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("26", "Weak mixing angle look-elsewhere audit.", ALL_TESTS) else 1)
