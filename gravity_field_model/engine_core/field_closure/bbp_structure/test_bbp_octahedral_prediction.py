"""
Does the octahedral shape single out pi among BBP constants?
============================================================

Role:     Supporting finding: among named BBP constants only pi has an octahedral-shape formula.
Expected: Passes. Exploratory: the result depends on the chosen list of constants.

Prediction of the hypothesis "the BBP formula is the stellated-octahedron
structure": among the constants that have base-16, period-8 formulas, pi
should be the one whose formula has the octahedral shape (TIME apices
silent, weights summing to zero, four active slots, 2+2 chamber split).

The eight slot series span a 7-dimensional space over the rationals (one
relation, see the family test). Constants known to lie in it include
ln 2, ln 3, ln 5, arctan(1/2), arctan(1/3) and sqrt(2) ln(1 + sqrt 2) besides
pi. Every constant in the span has exactly one formula with slot 7 empty,
which is the only member that can be TIME-silent. The test finds it with PSLQ
and checks its shape.

Constants outside the span (Catalan's constant, ln 7, pi^2, e) have no such
formula at all; they are reported for completeness.

The prediction concerns named constants only. For any admissible choice of
four slots, the zero-sum weights form a 3-parameter set, so infinitely many
unnamed constants in the span also have octahedral-shape formulas.
"""

from fractions import Fraction

from mpmath import mp, mpf, pi, log, atan, sqrt, catalan, e, pslq

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import (
    PRECISION, slot7_free_formula, is_octahedral, octahedral_conditions, formula_value,
)

# Control: a formula with the octahedral shape that is not pi. Slots 1, 4
# (one tetrahedron) and 5, 6 (the other), TIME apices silent, weights
# +1, -1, +1, -1 summing to zero.
CONTROL_WEIGHTS = {1: Fraction(1), 4: Fraction(-1), 5: Fraction(1), 6: Fraction(-1)}


def _constants():
    with mp.workdps(PRECISION + 10):
        inside = {
            "pi": +pi,
            "ln 2": log(2),
            "ln 3": log(3),
            "ln 5": log(5),
            "arctan(1/2)": atan(mpf(1) / 2),
            "arctan(1/3)": atan(mpf(1) / 3),
            "sqrt2 ln(1+sqrt2)": sqrt(2) * log(1 + sqrt(2)),
        }
        outside = {"Catalan": +catalan, "ln 7": log(7), "pi^2": pi ** 2, "e": +e}
    return inside, outside


class OctahedralPrediction(Test):
    name = "Octahedral Formula Shape Singles Out Pi"
    question = (
        "If the BBP formula is the stellated-octahedron structure, pi should be the constant "
        "whose base-16 formula has the octahedral shape. Among ln 2, ln 3, ln 5, arctan(1/2), "
        "arctan(1/3) and sqrt(2) ln(1+sqrt 2), which others also have it?"
    )
    reference = (
        "Bailey, Borwein, Plouffe (1997); Bailey's compendium of BBP-type formulas; "
        "PSLQ (Ferguson, Bailey, Arno 1999)"
    )
    tolerance = 0.0
    level = Level.EXPLORATORY

    def derivation(self):
        return (
            Derivation()
            .step("For each constant, run PSLQ on (S_1..S_6, S_8, constant) to get its slot-7-free formula.")
            .step("This formula is unique, and it is the only one that can leave the TIME apex 7 silent.")
            .step("Check the octahedral conditions on it: TIME silent, zero sum, four slots, 2+2 split.")
            .conclude("The prediction holds if pi is the only constant whose formula passes all four.")
        )

    commentary = (
        "Pi is the only one of the named constants whose base-16 formula has the octahedral "
        "shape. The others fail in different ways: ln 2 needs slot 0, a TIME apex; ln 3 and "
        "arctan(1/2) use two slots; ln 5 uses three; arctan(1/3) uses four slots but splits "
        "3+1 and does not sum to zero; sqrt(2) ln(1+sqrt 2) uses five. That is the outcome the "
        "hypothesis predicts. Its weight is limited by two facts stated in the module header: "
        "the conditions were read off pi's own formula, and infinitely many unnamed constants "
        "in the same span also have octahedral-shape formulas. The control shows one: "
        "S_1 - S_4 + S_5 - S_6 has the octahedral shape and equals a mixture of six constants "
        "(pi, ln 3, ln 5, arctan(1/2), sqrt(2) ln(1+sqrt 2), sqrt(2) arctan(1/sqrt 2)). So the shape "
        "singles out pi among the named constants, not among all formulas. A stronger test would derive "
        "the conditions from the octahedron first and then find pi; this test cannot do that."
    )

    def model(self):
        inside, outside = _constants()
        m = Model()
        for name, c in inside.items():
            w = slot7_free_formula(c)
            if w is None:
                m.add(f"{name}: octahedral formula (1=yes)", -1)
                continue
            m.add(f"{name}: octahedral formula (1=yes)", 1 if is_octahedral(w) else 0)
            failed = [k for k, ok in octahedral_conditions(w).items() if not ok]
            m.add(f"{name}: conditions failed", ", ".join(failed) if failed else "none")
        n_out = sum(1 for c in outside.values() if slot7_free_formula(c) is None)
        m.add("Constants tested outside the span (no formula)", n_out)

        # The control: which constants does the octahedral-shape formula
        # S_1 - S_4 + S_5 - S_6 equal? Express it in the named constants plus
        # sqrt(2) arctan(1/sqrt 2), which completes a basis of the span.
        m.add("Control S1-S4+S5-S6: octahedral shape (1=yes)", 1 if is_octahedral(CONTROL_WEIGHTS) else 0)
        with mp.workdps(PRECISION):
            v = formula_value(CONTROL_WEIGHTS)
            basis = [inside[k] for k in ["pi", "ln 2", "ln 3", "ln 5", "arctan(1/2)", "sqrt2 ln(1+sqrt2)"]]
            basis.append(sqrt(2) * atan(1 / sqrt(2)))
            rel = pslq([v] + basis, maxcoeff=10 ** 6, maxsteps=10 ** 6)
        m.add("Control: constants needed to express it (info)",
              sum(1 for x in rel[1:] if x != 0) if rel else -1)
        return m

    def observations(self):
        # Prediction of the hypothesis: pi alone has the octahedral shape.
        obs = Observed().add("pi: octahedral formula (1=yes)", 1)
        for name in ["ln 2", "ln 3", "ln 5", "arctan(1/2)", "arctan(1/3)", "sqrt2 ln(1+sqrt2)"]:
            obs.add(f"{name}: octahedral formula (1=yes)", 0)
        # Catalan, ln 7, pi^2 and e have no first-power base-16 period-8 formula.
        obs.add("Constants tested outside the span (no formula)", 4)
        # By construction: TIME silent, zero sum, four slots, 2+2.
        obs.add("Control S1-S4+S5-S6: octahedral shape (1=yes)", 1)
        return obs


ALL_TESTS = [OctahedralPrediction]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Octahedral prediction", "Does the octahedral shape single out pi?", ALL_TESTS) else 1)
