"""
25. Look-elsewhere audit of the proton-electron mass ratio formulas
===================================================================

Role:     Tests whether GFD's closed forms for m_p/m_e carry evidential weight, by fitting fake targets with the same grammar.
Expected: Passes, recording the outcome. The pre-registered prediction (PREDICTIONS.md, test 25) was NOT met; see below.

Research note 32 (great-pyramid/pyramid_portal_research/active_work) gives

    m_p/m_e = 1836 + 21 a/(1 + a/2) - a^2/4 - 3 a^3/2        (Form IV, a = alpha)

with 1836 = K D^3 Phi_4 = 4 * 27 * 17 and 21 = Phi_3, and reports agreement
with CODATA 2018 to about 15 parts per trillion. The terms were added one at
a time, each after the previous residual was known.

A collider physicist's question is: **how often would a formula of the same
form match a number that is not the real one?** If fake targets are matched
as well as the real one, the agreement shows how flexible the grammar is,
not that the formula is right. The test:

- fixes the grammar: bulk 1836, then c1 a/(1 + a/2) + c2 a^2 + c3 a^3;
- fixes a menu for the coefficients, built from the framework's own numbers
  {1, 2, 3, 4, 8, 13, 17, 21} divided by 1, 2 or 4 (c2 and c3 may also be 0
  or negative). Form IV is in this menu;
- places 2,000 fake targets uniformly within 1 ppm of the true value, and
  for each finds the best menu formula;
- counts the fake targets fitted at least as closely as Form IV fits the
  real one.

The menu is narrower than the one the research note drew on (it also used
the denominator 1 + a/2 as a choice), which favours the formula.

**Outcome against the pre-registration.** The prediction was that more than
20% of fakes would be fitted as closely. The outcome is about 2%. The
prediction was wrong: the grammar is less flexible than expected, and the
fit is better than chance at roughly the 2% level.

**Where the agreement comes from (exploratory, added after the outcome).**
Splitting the fit into its stages shows which step carries it:

- Form I, 1836 + 21a (0.31 ppm): about 30% of fakes are fitted as well. Chance.
- Form II, 1836 + 21a/(1 + a/2) (7.6 ppb): about 0.7% of fakes. This is the
  one step that is unlikely by chance.
- Forms III and IV, given Form II's residual: the a^2 and a^3 terms from the
  menu fit a random residual of that size as closely about 16% of the time.
  They add no evidence.

So the evidential content is one coincidence of about 1 in 150, at the
choice of the denominator 1 + a/2. Six such denominators (1, 1 +- a/2,
1 +- a, 1 + a/4) give similar chances, and the research tried several
ratios (m_mu/m_e at -42 ppm did not fit), so the trials factor is at least
several. The global significance is then about 2 sigma at most.
"""

from fractions import Fraction

import numpy as np

from gravity_field_model.framework import *

# CODATA 2018 (used by research note 32) and CODATA 2022 (PDG 2025, "Physical constants").
ALPHA_2018, MPME_2018, U_2018 = 1 / 137.035999084, 1836.15267343, 0.00000011
ALPHA_2022, MPME_2022, U_2022 = 1 / 137.035999177, 1836.152673426, 0.000000032
FRAMEWORK = (1, 2, 3, 4, 8, 13, 17, 21)
N_FAKE = 2000
SEED = 1836


def menu():
    vals = sorted({Fraction(a, b) for a in FRAMEWORK for b in (1, 2, 4)})
    return vals, [Fraction(0)] + vals + [-v for v in vals]


def form_iv(a):
    return 1836 + 21 * a / (1 + a / 2) - a * a / 4 - 3 * a ** 3 / 2


def grid(a):
    pos, signed = menu()
    A = np.array([float(c) for c in pos]) * a / (1 + a / 2)
    B = np.array([float(c) for c in signed]) * a * a
    C = np.array([float(c) for c in signed]) * a ** 3
    return np.sort((A[:, None, None] + B[None, :, None] + C[None, None, :]).ravel())


def best_dev(g, delta):
    i = np.clip(np.searchsorted(g, delta), 1, len(g) - 1)
    return np.minimum(np.abs(g[i] - delta), np.abs(g[i - 1] - delta))


class MassRatioLookElsewhere(Test):
    name = "25. Look-Elsewhere Audit of the m_p/m_e Formulas"
    question = (
        "GFD's Form IV matches m_p/m_e to about 15 parts per trillion. Would a formula of the "
        "same form, from the same framework numbers, match a fake value just as well?"
    )
    reference = (
        "Research note 32; CODATA 2018 and 2022 (PDG 2025, Physical constants); "
        "extensions/PREDICTIONS.md (test 25)"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Evaluate Form IV at CODATA alpha; compare with CODATA m_p/m_e (2018 and 2022).")
            .step("Build every formula 1836 + c1 a/(1+a/2) + c2 a^2 + c3 a^3 from the framework menu.")
            .step("For 2,000 fake targets within 1 ppm, find the closest menu formula.")
            .conclude("The share of fakes fitted as well as the real value measures the grammar's flexibility.")
        )

    commentary = (
        "Form IV agrees with CODATA 2018 and 2022 within their uncertainties. The "
        "pre-registered prediction, that more than 20% of fake targets would be fitted as "
        "closely, was wrong: only about 2% are, so the fit is better than this grammar gives "
        "by chance. Splitting it by stage locates the coincidence. Form I (31% of fakes) is "
        "chance. Form II, the denominator 1 + a/2, is the one unlikely step (about 0.7%). The "
        "a^2 and a^3 terms of Forms III and IV fit Form II's residual as well as they fit a "
        "random residual of that size about 16% of the time, so their parts-per-trillion "
        "precision adds no evidence. With the denominator and the ratios tried counted as "
        "trials, the global significance is about 2 sigma at most. This is an interesting "
        "coincidence, not a detection. What would turn it into evidence is a derivation of "
        "the denominator 1 + a/2 and of the a^2 and a^3 coefficients fixed before comparing, "
        "or a correct prediction of a ratio not yet used, such as m_mu/m_e at ppb level."
    )

    def model(self):
        g18 = grid(ALPHA_2018)
        real_dev = abs(form_iv(ALPHA_2018) - MPME_2018)
        rng = np.random.default_rng(SEED)
        fakes = MPME_2018 * (1 + rng.uniform(-1e-6, 1e-6, N_FAKE))
        fake_best = best_dev(g18, fakes - 1836)
        frac = float((fake_best <= real_dev).mean())
        # Exploratory (post hoc): stage II alone, and stages III-IV given stage II's residual.
        pos, signed = menu()
        P = np.array([float(c) for c in pos])
        S = np.array([float(c) for c in signed])
        a = ALPHA_2018
        f1, f2 = 1836 + 21 * a, 1836 + 21 * a / (1 + a / 2)
        frac_1 = float((best_dev(np.sort(P * a), fakes - 1836) <= abs(f1 - MPME_2018)).mean())
        frac_2 = float((best_dev(np.sort(P * a / (1 + a / 2)), fakes - 1836) <= abs(f2 - MPME_2018)).mean())
        resid = MPME_2018 - f2
        fake_resid = rng.uniform(-1.5 * abs(resid), 1.5 * abs(resid), 20_000)
        g34 = np.sort((S[:, None] * a * a + S[None, :] * a ** 3).ravel())
        frac_34 = float((best_dev(g34, fake_resid) <= real_dev).mean())
        within_real = int((np.abs(g18 - (MPME_2018 - 1836)) <= U_2018).sum())
        within_fake = float(np.mean([(np.abs(g18 - (f - 1836)) <= U_2018).sum() for f in fakes[:200]]))
        in_menu = Fraction(21) in pos and Fraction(-1, 4) in signed and Fraction(-3, 2) in signed
        return (
            Model()
            .add("Formulas in the menu (info)", len(g18))
            .add("Form IV in the menu (1=yes)", int(in_menu))
            .add("Form IV minus CODATA 2018, parts per trillion (info)",
                 round((form_iv(ALPHA_2018) - MPME_2018) / MPME_2018 * 1e12, 1))
            .add("Form IV within CODATA 2018 uncertainty (1=yes)", int(real_dev <= U_2018))
            .add("Form IV minus CODATA 2022, in sigma (info)",
                 round((form_iv(ALPHA_2022) - MPME_2022) / U_2022, 2))
            .add("Menu formulas within 1 sigma of the real value (info)", within_real)
            .add("Mean menu formulas within 1 sigma of a fake value (info)", round(within_fake, 1))
            .add("Fakes fitted as closely as Form IV (pre-registered fraction)", round(frac, 3))
            .add("Pre-registered prediction (fraction > 0.2) met (1=yes)", int(frac > 0.2))
            .add("Exploratory: fakes fitted as closely as Form I", round(frac_1, 3))
            .add("Exploratory: fakes fitted as closely as Form II", round(frac_2, 4))
            .add("Exploratory: a^2, a^3 terms fit a random stage-II residual as well", round(frac_34, 3))
        )

    def observations(self):
        return (
            Observed()
            .add("Form IV in the menu (1=yes)", 1)
            # Research note 32 reports -15.4 ppt against CODATA 2018 (uncertainty 60 ppt).
            .add("Form IV within CODATA 2018 uncertainty (1=yes)", 1)
            # Outcome recorded after the pre-registered run (prediction was > 0.2).
            .add("Fakes fitted as closely as Form IV (pre-registered fraction)", 0.02, abs_tol=0.01)
            .add("Pre-registered prediction (fraction > 0.2) met (1=yes)", 0)
            .add("Exploratory: fakes fitted as closely as Form I", 0.31, abs_tol=0.04)
            .add("Exploratory: fakes fitted as closely as Form II", 0.007, abs_tol=0.004)
            .add("Exploratory: a^2, a^3 terms fit a random stage-II residual as well", 0.16, abs_tol=0.04)
        )


ALL_TESTS = [MassRatioLookElsewhere]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("25", "Mass-ratio look-elsewhere audit.", ALL_TESTS) else 1)
