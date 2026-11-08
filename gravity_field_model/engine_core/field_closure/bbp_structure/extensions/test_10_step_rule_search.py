"""
10. How sharply the step rule is determined
===========================================

Role:     Extends PROOF.md Theorem 5 and test_reading_rules_exact.py (which searched the weight rule) to the step rule.
Expected: Passes. A failure means a second step rule or starting point also gives pi.

Theorem 5 places the rows at positions p_0 = 1, p_(i+1) = p_i + 2t + 1, where
t is the row's top line. With the weight rule 2b + m + t fixed, this test
tries every step rule a t + c (a in 0..4, c in 0..3) and every starting
position 0..7: 160 combinations. It counts those whose series equals pi.
"""

from itertools import product

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions._reading import read_rows, is_pi

FATHER_RANK = (7, 4, 2, 1)


class StepRuleSearch(Test):
    name = "10. Step Rules and Starting Points"
    question = (
        "With the weight rule fixed, how many simple step rules a*t + c, from any starting "
        "position, produce pi?"
    )
    reference = "PROOF.md Theorem 5"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Enumerate step = a*t + c for a in 0..4, c in 0..3, and start in 0..7.")
            .step("Read Qian, Zhen, Kan, Gen with weight 2b + m + t and that step.")
            .conclude("Count the combinations whose series is pi (to 60 digits).")
        )

    commentary = (
        "Only one combination of the 160 works: step 2t + 1 from position 1. Like the weight "
        "rule, the step rule is sharply determined once its linear form is chosen; like the "
        "weight rule, it was identified by matching BBP, so the count shows specificity, not "
        "a derivation. Note that 2t + 1 is D = 3 for a yang top line and 1 for a yin one, the "
        "same D-or-1 reading as the axis vectors of why_pi_formal_derivation.md."
    )

    def model(self):
        hits = []
        for a, c, start in product(range(5), range(4), range(8)):
            w = read_rows(FATHER_RANK, step=lambda b, m, t, a=a, c=c: a * t + c, start=start)
            if w and is_pi(w):
                hits.append((a, c, start))
        return (
            Model()
            .add("Step rules tried", 5 * 4 * 8)
            .add("Step rules giving pi", len(hits))
            .add("That rule (a, c, start)", " ".join(map(str, hits[0])) if hits else "none")
        )

    def observations(self):
        return (
            Observed()
            .add("Step rules giving pi", 1)
            # step 2t + 1 from position 1 (Theorem 5).
            .add("That rule (a, c, start)", "2 1 1")
        )


ALL_TESTS = [StepRuleSearch]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("10", "Step rule search.", ALL_TESTS) else 1)
