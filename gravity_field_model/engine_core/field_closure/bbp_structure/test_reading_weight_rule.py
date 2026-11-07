"""
Can an agreement rule produce the BBP numerators?
=================================================

Role:     PROOF.md Theorem 5 status: the magnitude rule is ordered, not an agreement rule.
Expected: Passes when no agreement rule gives pi (as the proof shows none can).

The derivation obtains the numerator magnitudes [4, 2, 1, 1] from the x and y
axis vectors with what it calls an agreement rule: full weight when both axes
read D, partial weight when they disagree, unit weight when both read 1. The
rule as coded assigns the two disagreement cases different values,
(D, 1) -> 2 and (1, D) -> 1.

A rule based on agreement treats (D, 1) and (1, D) alike. This test asks
whether any such rule gives pi, and shows why none can:

- The complete family of base-16 formulas for pi (Adamchik and Wagon 1997;
  see test_bbp_pi_formula_family.py) has exactly one member using only the
  slots 1, 4, 5, 6: the BBP formula, with weights 4, -2, -1, -1.
- The two disagreement readings land on slots 4 and 5, so an agreement rule
  gives them equal magnitude. BBP needs 2 and 1.
"""

from fractions import Fraction
from itertools import product

from mpmath import mp, pi

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import (
    PRECISION, SLOTS, AW_CONSTANT, AW_PER_R, aw_weights, formula_value,
)
from gravity_field_model.engine_core.field_closure.bbp_structure.closure_reading import (
    D, paper_rule, symmetric_rule, read,
)

TOL = mp.mpf(10) ** (-(PRECISION - 20))
RULE_VALUES = range(1, 5)  # each of the three agreement classes takes a weight 1..4


def pi_formulas_on_bbp_slots():
    """Members of the Adamchik-Wagon family whose weights vanish off slots 1, 4, 5, 6."""
    off = [j for j in SLOTS if j not in (1, 4, 5, 6)]
    candidates = {Fraction(-AW_CONSTANT[j], AW_PER_R[j]) for j in off if AW_PER_R[j] != 0}
    candidates.add(Fraction(0))
    return [r for r in sorted(candidates) if all(aw_weights(r)[j] == 0 for j in off)]


class WeightRuleSymmetry(Test):
    name = "Agreement Rule for the BBP Numerators"
    question = (
        "The derivation calls its magnitude rule an agreement rule. Does any rule that "
        "depends only on whether the x and y axes agree produce the BBP numerators and pi?"
    )
    reference = (
        "Rule: why_pi_verification.py (constraint 4); family: Adamchik and Wagon (1997), "
        "Amer. Math. Monthly 104, 852-855"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Check whether the coded rule weights (D,1) and (1,D) equally.")
            .step("Enumerate the 64 agreement rules with weights 1..4 for (both D, disagree, both 1).")
            .step("Run the reading with each and compare the series with pi to 100 digits.")
            .step("From the complete family, find every pi formula supported on slots 1, 4, 5, 6.")
            .conclude("If only BBP lives on those slots and it needs unequal weights at slots 4 and 5, no agreement rule can work.")
        )

    commentary = (
        "No agreement rule gives pi: none of the 64 does, and none can. The only base-16 "
        "formula for pi on the slots 1, 4, 5, 6 is BBP itself, and it needs magnitude 2 at "
        "slot 4 and 1 at slot 5, exactly the two readings where the x and y lines disagree. "
        "The coded rule produces these values by treating (D,1) and (1,D) differently, so it "
        "is an ordered rule, not an agreement rule. In I Ching terms x and y are the bottom "
        "and middle lines, so the rule gives weight 2 when only the bottom line is yang and "
        "weight 1 when only the middle line is yang. An ordered rule is consistent with the "
        "trigram's ordered lines, but the values 2 and 1 are not given by any stated "
        "principle, and the rule's four entries (4, 2, 1, 1) are the four BBP magnitudes one "
        "for one: the rule restates them rather than deriving them. So the description "
        "'agreement rule' in why_pi_formal_derivation.md is inaccurate; the rule is ordered."
    )

    def model(self):
        coded_symmetric = paper_rule(D, 1) == paper_rule(1, D)
        n_pi = 0
        with mp.workdps(PRECISION):
            for a, b, c in product(RULE_VALUES, repeat=3):
                w, *_ = read(rule=symmetric_rule(a, b, c))
                n_pi += abs(formula_value(w) - pi) < TOL
        on_slots = pi_formulas_on_bbp_slots()
        w0 = aw_weights(on_slots[0]) if on_slots else {}
        return (
            Model()
            .add("Coded rule weights (D,1) and (1,D) equally (1=yes)", 1 if coded_symmetric else 0)
            .add("Agreement rules giving pi (of 64)", n_pi)
            .add("Pi formulas using only slots 1,4,5,6", len(on_slots))
            .add("That formula has equal weights at slots 4 and 5 (1=yes)",
                 1 if on_slots and abs(w0[4]) == abs(w0[5]) else 0)
            .add("An agreement rule gives pi (1=yes)", 1 if n_pi > 0 else 0)
        )

    def observations(self):
        return (
            Observed()
            # The family has one member on these slots: BBP, r = 0.
            .add("Pi formulas using only slots 1,4,5,6", 1)
            # BBP: |-2| at slot 4, |-1| at slot 5.
            .add("That formula has equal weights at slots 4 and 5 (1=yes)", 0)
            # why_pi_verification.py, constraint 4: (D,1) -> D-1 = 2, (1,D) -> 1.
            .add("Coded rule weights (D,1) and (1,D) equally (1=yes)", 0)
            # Follows from the two lines above: an agreement rule would give equal
            # weights at slots 4 and 5, and the only pi formula there needs 2 and 1.
            .add("An agreement rule gives pi (1=yes)", 0)
        )


ALL_TESTS = [WeightRuleSymmetry]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Weight rule", "Can an agreement rule produce the BBP numerators?", ALL_TESTS) else 1)
