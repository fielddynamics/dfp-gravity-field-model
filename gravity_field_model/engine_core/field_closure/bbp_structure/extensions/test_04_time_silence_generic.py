"""
04. TIME silence makes every formula unique; the shape is what is special
=========================================================================

Role:     Qualifies PROOF.md Theorem 3: which part of the selection is generic and which is specific to pi.
Expected: Passes. A failure means some constant has two TIME-silent formulas, or a second has the octahedral shape.

Theorem 3 says exactly one formula for pi leaves the TIME axis silent. Is that
uniqueness special to pi? The only rational relation among the slot series
(Theorem 2) involves S_7. So for any constant, its formulas differ by multiples
of that relation, and fixing w_7 = 0 leaves at most one. Uniqueness is
therefore generic. What distinguishes pi is the shape of its unique
TIME-silent formula.

For each named constant the test finds its TIME-silent formula (if any) and
checks the octahedral shape: four slots, two per tetrahedron, weights summing
to zero.
"""

import sympy as sp

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions.named_basis import (
    NAMES, slot_in_named,
)

TETA = {1, 2, 4, 7}


def time_silent_formulas(target):
    """All rational q on slots 1..6 with sum q_j S_j = named constant `target`; returns (count, q)."""
    M = slot_in_named()
    A = M[:6, :].T
    e = sp.Matrix([1 if k == target else 0 for k in range(7)])
    try:
        sol, params = A.gauss_jordan_solve(e)
    except ValueError:
        return 0, None
    return (1 if params.shape[0] == 0 else float("inf")), [sp.nsimplify(x) for x in sol]


class TimeSilenceGeneric(Test):
    name = "04. TIME Silence Is Generic; the Octahedral Shape Is Not"
    question = (
        "Is it special that pi has exactly one TIME-silent formula, or does every constant? "
        "If every constant does, what is special about pi's?"
    )
    reference = "PROOF.md Theorems 2 and 3; test 01"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Formulas for one constant differ by multiples of the Adamchik-Wagon relation, whose slot-7 weight is 1.")
            .step("So fixing w_7 = 0 (and w_8 = 0) leaves at most one formula, for any constant.")
            .step("For each named constant, solve for its TIME-silent formula exactly.")
            .step("Check each for the octahedral shape: four slots, 2 + 2, zero sum.")
            .conclude("Uniqueness is generic; the octahedral shape belongs to pi alone.")
        )

    commentary = (
        "Every named constant except ln 2 has exactly one TIME-silent formula, so the "
        "uniqueness in Theorem 3 is a property of the formula space, not of pi. What is "
        "particular to pi is what its unique formula looks like: four corners, two in each "
        "tetrahedron, weights summing to zero. ln 3 uses two slots, ln 5 three, arctan(1/2) "
        "two, and the sqrt2 constants five or more; none closes. The honest statement of the "
        "main result is therefore: silence fixes one formula for each constant, and only pi's "
        "has the stellated octahedron's shape."
    )

    def model(self):
        m = Model()
        n_unique, n_shape = 0, 0
        for k, name in enumerate(NAMES):
            count, q = time_silent_formulas(k)
            if count == 1:
                n_unique += 1
                act = {j + 1 for j, x in enumerate(q) if x != 0}
                shape = len(act) == 4 and len(act & TETA) == 2 and sum(q) == 0
                n_shape += int(shape)
                m.add(f"{name}: slots of its TIME-silent formula (info)", " ".join(map(str, sorted(act))))
                if shape:
                    m.add("Constant with the octahedral shape", name)
        m.add("Named constants with exactly one TIME-silent formula", n_unique)
        m.add("Of those, with the octahedral shape", n_shape)
        return m

    def observations(self):
        return (
            Observed()
            # Six of seven (ln 2 has none, test 02); uniqueness from the single relation.
            .add("Named constants with exactly one TIME-silent formula", 6)
            .add("Of those, with the octahedral shape", 1)
            .add("Constant with the octahedral shape", "pi")
        )


ALL_TESTS = [TimeSilenceGeneric]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("04", "TIME silence generic; shape special.", ALL_TESTS) else 1)
