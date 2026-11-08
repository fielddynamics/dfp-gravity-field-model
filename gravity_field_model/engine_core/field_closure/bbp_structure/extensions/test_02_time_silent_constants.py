"""
02. Which constants can be written with the TIME axis silent, and with closure
==============================================================================

Role:     Extends PROOF.md Theorem 3: TIME silence and closure as conditions on the constant, not only on pi.
Expected: Passes. A failure means a second named constant admits a TIME-silent, zero-sum formula.

A formula is TIME-silent if it gives no weight to slots 7 (Qian) and 8 (Kun),
and closed if its weights sum to zero. This test asks, for each of the seven
named constants of test 01: does it have a TIME-silent formula, and does it
have one that is also closed?

TIME-silent formulas use slots 1..6 only, so their values form the rational
span of S_1..S_6 (rank 6). Adding closure is one more linear condition. Both
questions are exact linear algebra over the named-constant coordinates.
"""

import sympy as sp

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions.named_basis import (
    NAMES, slot_in_named,
)


def reachable(target, closed):
    """Is the named constant `target` = sum_{j<=6} q_j S_j for rational q (with sum q = 0 if closed)?"""
    M = slot_in_named()
    A = M[:6, :].T                       # 7 x 6: column j = S_(j+1)
    e = sp.Matrix([1 if k == target else 0 for k in range(7)])
    if closed:
        A = A.col_join(sp.ones(1, 6))
        e = e.col_join(sp.Matrix([0]))
    return A.rank() == A.row_join(e).rank()


class TimeSilentConstants(Test):
    name = "02. Constants with a TIME-Silent Formula, and with a Closed One"
    question = (
        "If the father and mother must stay silent, which constants can still be written? "
        "And if, in addition, the weights must sum to zero (closure), which remain?"
    )
    reference = "PROOF.md Theorems 2 and 3; test 01"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("TIME-silent formulas span the values of S_1..S_6; check their rank.")
            .step("For each named constant, test membership in that span (exact rank comparison).")
            .step("Add the closure condition sum q_j = 0 and test membership again.")
            .conclude("Count the constants that survive each condition.")
        )

    commentary = (
        "Six of the seven named constants can be written with the TIME axis silent; ln 2 "
        "cannot, because it lives only in Kun's slot (test 01). Add closure, the weights "
        "summing to zero, and only pi remains. So the two octahedral conditions together, "
        "silent parents and a closed reading, single out pi among the basis constants. This "
        "is a statement about the constant, not just about one formula: no TIME-silent, closed "
        "formula of this kind exists for ln 3, ln 5, arctan(1/2) or the two sqrt2 constants. "
        "(Combinations of constants are a different matter: the closed, TIME-silent values form "
        "a 5-dimensional space, and pi is the only basis direction inside it.)"
    )

    def model(self):
        M = slot_in_named()
        silent = [n for k, n in enumerate(NAMES) if reachable(k, closed=False)]
        closed = [n for k, n in enumerate(NAMES) if reachable(k, closed=True)]
        # Values of closed TIME-silent formulas: A applied to {q in Q^6 : sum q = 0}.
        zero_sum_basis = sp.Matrix.hstack(*sp.ones(1, 6).nullspace())
        closed_dim = (M[:6, :].T * zero_sum_basis).rank()
        return (
            Model()
            .add("Rank of S_1..S_6", M[:6, :].rank())
            .add("Named constants with a TIME-silent formula", len(silent))
            .add("Named constant without one", ", ".join(n for n in NAMES if n not in silent))
            .add("Named constants with a TIME-silent closed formula", len(closed))
            .add("That constant", ", ".join(closed))
            .add("Dimension of TIME-silent closed values", closed_dim)
        )

    def observations(self):
        return (
            Observed()
            # S_1..S_6 are independent: the only relation (Theorem 2) involves S_7.
            .add("Rank of S_1..S_6", 6)
            .add("Named constants with a TIME-silent formula", 6)
            # ln 2 appears only in S_8 (test 01).
            .add("Named constant without one", "ln 2")
            # Prediction of the octahedral reading: pi alone.
            .add("Named constants with a TIME-silent closed formula", 1)
            .add("That constant", "pi")
            # Six independent slots, one closure condition.
            .add("Dimension of TIME-silent closed values", 5)
        )


ALL_TESTS = [TimeSilentConstants]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("02", "TIME-silent and closed formulas.", ALL_TESTS) else 1)
