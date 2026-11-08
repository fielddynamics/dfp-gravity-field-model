"""
01. The eight slot series in seven named constants
==================================================

Role:     Extends PROOF.md Theorem 2: names the 7-dimensional space that every base-16, period-8 formula lives in.
Expected: Passes. A failure means a slot series is not a rational combination of the seven constants, or they are dependent.

Theorem 2 shows the slot series S_1..S_8 span a 7-dimensional space over Q.
This test names a basis of that space,

    pi, ln 2, ln 3, ln 5, arctan(1/2), sqrt2 ln(1+sqrt2), sqrt2 arctan(1/sqrt2),

and writes every S_j as an exact rational combination of them (exact algebra
over the seven logarithms of the completeness proof). It then checks the
combinations numerically to 100 digits, and checks two of them against
independent closed forms:

    S_8 = sum 1/(16^k (8k+8)) = (1/8) sum 1/(16^k (k+1)) = 2 ln(16/15),
    S_4 = sum 1/(16^k (8k+4)) = (1/4) sum 1/(16^k (2k+1)) = (1/2) ln(5/3).

(Both from ln((1+x)/(1-x)) = 2 sum x^(2k+1)/(2k+1) and -ln(1-x) = sum x^(k+1)/(k+1).)
"""

import sympy as sp
from mpmath import mp, mpf, nsum, inf

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions.named_basis import (
    NAMES, SYMPY, named_matrix, slot_in_named,
)


class SlotSpanBasis(Test):
    name = "01. The Slot Series in Seven Named Constants"
    question = (
        "Every base-16, period-8 formula is a combination of the eight slot series. Which "
        "named constants do those series consist of?"
    )
    reference = "PROOF.md Theorem 2; series for ln((1+x)/(1-x)) and -ln(1-x)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Write the seven named constants in the seven logarithms Lambda of the completeness proof.")
            .step("Solve exactly for each S_j as a rational combination of the named constants.")
            .step("Check every combination against the series to 100 digits.")
            .step("Check S_8 and S_4 against their elementary closed forms.")
            .conclude("The space of base-16, period-8 formulas is the rational span of these seven constants.")
        )

    commentary = (
        "Every slot series is a rational combination of pi, ln 2, ln 3, ln 5, arctan(1/2), "
        "sqrt2 ln(1+sqrt2) and sqrt2 arctan(1/sqrt2), and these seven are independent. So any "
        "base-16, period-8 formula, for any constant, evaluates to a rational combination of "
        "these seven numbers and nothing else. Two slots are elementary: S_8 = 2 ln(16/15) and "
        "S_4 = (1/2) ln(5/3) are pure logarithms with no pi in them. Only S_8 contains ln 2, which "
        "is why ln 2 needs Kun's corner (see test 02)."
    )

    def model(self):
        M = slot_in_named()
        with mp.workdps(110):
            worst = max(
                abs(sum(mpf(sp.N(M[j, k], 120)) * mpf(sp.N(SYMPY[k], 120)) for k in range(7))
                    - nsum(lambda n: 1 / (mpf(16) ** n * (8 * n + j + 1)), [0, inf]))
                for j in range(8)
            )
        s8 = sp.nsimplify(sum(M[7, k] * SYMPY[k] for k in range(7)))
        s4 = sp.nsimplify(sum(M[3, k] * SYMPY[k] for k in range(7)))
        ln2_slots = [j + 1 for j in range(8) if M[j, 1] != 0]
        return (
            Model()
            .add("Rank of the seven named constants (over Lambda)", named_matrix().rank())
            .add("Slots written exactly in the named constants", M.shape[0])
            .add("Max |S_j - named combination| (100 digits)", float(worst))
            .add("S_8 = 2 ln(16/15) (1=yes)", int(sp.simplify(sp.expand_log(s8 - 2 * sp.log(sp.Rational(16, 15)), force=True)) == 0))
            .add("S_4 = (1/2) ln(5/3) (1=yes)", int(sp.simplify(sp.expand_log(s4 - sp.log(sp.Rational(5, 3)) / 2, force=True)) == 0))
            .add("Slots containing ln 2", ", ".join(map(str, ln2_slots)))
        )

    def observations(self):
        return (
            Observed()
            .add("Rank of the seven named constants (over Lambda)", 7)
            .add("Slots written exactly in the named constants", 8)
            .add("Max |S_j - named combination| (100 digits)", 0.0, abs_tol=1e-90)
            # Elementary series, see the module docstring.
            .add("S_8 = 2 ln(16/15) (1=yes)", 1)
            .add("S_4 = (1/2) ln(5/3) (1=yes)", 1)
            # S_8 = 2 ln(16/15) = 8 ln 2 - 2 ln 3 - 2 ln 5 carries ln 2. The other seven slots have
            # no ln 2 component in the exact solution (recorded here as the expected finding).
            .add("Slots containing ln 2", "8")
        )


ALL_TESTS = [SlotSpanBasis]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("01", "Slot series in named constants.", ALL_TESTS) else 1)
