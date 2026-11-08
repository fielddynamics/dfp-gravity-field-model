"""
21. The reading rules, confirmed without assuming pi
====================================================

Role:     PROOF.md Theorem 6: characterises the reading rules of Theorem 5 by structural conditions alone.
Expected: Passes. A failure means a second admissible reading computes a multiple of pi or of another basis constant.

Theorem 5's rules (weight 2b + m + t, step 2t + 1, start 1, sons in rank
order) were found by matching BBP. Here they are recovered without using pi.

Search space (_structural.py): the three sons in any of 6 orders; weight
a*b + c*m + d*t + e (a, c, d in 0..4, e in -2..2); step al*b + be*m + ga*t + de
(each 0..3); start 0..7. Conditions, all structural: positive weights and
steps, closure (weights sum to zero), one orbit (steps sum to 8), four distinct
slots, TIME silent, two slots in each tetrahedron.

Every admissible reading yields a formula sum_j w_j S_j, whose exact value in
the seven named constants is known (test 01). The test asks which admissible
readings compute a rational multiple of pi, and whether any computes a multiple
of another basis constant. Then it reads off the rule that realises the answer
in each order of the sons.
"""

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions._structural import (
    admissible_table, LINES,
)
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions.named_basis import (
    NAMES, value_vector,
)


def order_relative_rule(order, w, s):
    """Is the weight 'line sum + first son's line' and the step '1 + 2 x last son's line' (up to scale)?"""
    first = LINES[order[0]].index(1)
    last = LINES[order[-1]].index(1)
    a, c, d, e = w
    coeffs = [a, c, d]
    k = min(coeffs)
    want_w = [k * (2 if i == first else 1) for i in range(3)]
    al, be, ga, de = s
    want_s = [2 if i == last else 0 for i in range(3)]
    return e == 0 and coeffs == want_w and [al, be, ga] == want_s and de == 1


class ReadingRulesConfirmed(Test):
    name = "21. The Reading Rules Confirmed by Structure Alone"
    question = (
        "Without using pi: among all readings of the father's tetrahedron that satisfy only "
        "the octahedral conditions (closure, one orbit, TIME silence, chamber balance), which "
        "compute pi, and by what rule?"
    )
    reference = "PROOF.md Theorems 2, 5 and 6; test 01"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Enumerate 6 orders x affine weights x affine steps x starts (30,720 rule sets).")
            .step("Keep the readings meeting the structural conditions; collect their distinct formulas.")
            .step("Write each formula's value exactly in the seven named constants.")
            .step("Find the formulas equal to a multiple of a single basis constant.")
            .conclude("Read off the rule that produces them in each order of the sons.")
        )

    commentary = (
        "The structural conditions alone leave 704 distinct formulas. Exactly two of them "
        "compute a multiple of any single basis constant, and both compute pi: BBP itself and "
        "twice BBP (the same rule with weights doubled). No admissible reading computes a "
        "multiple of ln 2, ln 3, ln 5 or the other constants. In every order of the sons the "
        "rule that produces pi is the same once stated relative to the reading order: the line "
        "of the first son read counts double in the weight, and the line of the last son read "
        "sets the step, 3 if yang and 1 if yin, starting from position 1. With the I Ching's "
        "rank order (eldest first, bottom line) this is exactly 2b + m + t and 2t + 1. So the "
        "rules are not fitted parameters: they are the unique admissible reading whose output "
        "is a named constant, and that constant is pi."
    )

    def model(self):
        table = admissible_table()
        pi_formulas, other = [], []
        for formula, readings in table.items():
            v = value_vector(dict(formula))
            nz = [k for k in range(7) if v[k] != 0]
            if len(nz) == 1:
                (pi_formulas if NAMES[nz[0]] == "pi" else other).append((formula, v[nz[0]], readings))
        multiples = sorted(str(m) for _, m, _ in pi_formulas)
        realising = [r for _, _, rs in pi_formulas for r in rs]
        relative_ok = sum(order_relative_rule(od, w, s) and st == 1 for od, w, s, st in realising)
        rank = [r for r in realising if r[0] == ("Zhen", "Kan", "Gen") and r[1] == (2, 1, 1, 0)]
        return (
            Model()
            .add("Admissible formulas (structural conditions only)", len(table))
            .add("Admissible formulas equal to a multiple of pi", len(pi_formulas))
            .add("Multiples of pi obtained", ", ".join(multiples))
            .add("Admissible formulas equal to a multiple of another basis constant", len(other))
            .add("Readings realising pi (all orders)", len(realising))
            .add("Of those, following 'first son doubles, last son steps, start 1'", relative_ok)
            .add("Rank order rule is weight 2b+m+t, step 2t+1, start 1 (1=yes)",
                 int(len(rank) == 1 and rank[0][2] == (0, 0, 2, 1) and rank[0][3] == 1))
        )

    def observations(self):
        return (
            Observed()
            # Theorem 6 (exact enumeration).
            .add("Admissible formulas equal to a multiple of pi", 2)
            .add("Multiples of pi obtained", "1, 2")
            .add("Admissible formulas equal to a multiple of another basis constant", 0)
            # 6 orders x 2 scales, each realised by the order-relative rule.
            .add("Readings realising pi (all orders)", 12)
            .add("Of those, following 'first son doubles, last son steps, start 1'", 12)
            .add("Rank order rule is weight 2b+m+t, step 2t+1, start 1 (1=yes)", 1)
        )


ALL_TESTS = [ReadingRulesConfirmed]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("21", "Reading rules confirmed.", ALL_TESTS) else 1)
