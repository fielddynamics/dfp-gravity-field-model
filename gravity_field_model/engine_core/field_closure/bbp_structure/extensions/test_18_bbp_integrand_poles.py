"""
18. Which poles the BBP numerator keeps
=======================================

Role:     Extends PROOF.md Theorem 4: how the BBP weights act on the eight poles of the slot integrand.
Expected: Passes. A failure means the factorisations or the surviving poles differ from those stated.

Every slot combination is 16 * integral_0^1 P(y) / (16 - y^8) dy (Lemma 1), and
16 - y^8 has eight simple poles at y = sqrt2 * w, w^8 = 1: a regular octagon of
radius sqrt 2, which is two squares. Over the rationals,

    16 - y^8 = -(y^2 - 2)(y^2 + 2)(y^2 - 2y + 2)(y^2 + 2y + 2).

For BBP, P(y) = 4 - 2y^3 - y^4 - y^5. The test checks that this numerator
cancels exactly two of the four quadratic factors, (y^2 + 2) and
(y^2 + 2y + 2), leaving the poles +-sqrt2 and 1 +- i: the real pair and the
pair at +-45 degrees. The cancelled poles are +-i sqrt2 and -1 +- i.
"""

import sympy as sp

from gravity_field_model.framework import *

y = sp.symbols("y")
QUADRATICS = {"y^2 - 2": y**2 - 2, "y^2 + 2": y**2 + 2, "y^2 - 2y + 2": y**2 - 2*y + 2, "y^2 + 2y + 2": y**2 + 2*y + 2}


class BBPIntegrandPoles(Test):
    name = "18. The Poles the BBP Numerator Keeps"
    question = (
        "The slot integrand has eight poles on an octagon. Which of them does the BBP formula's "
        "numerator cancel, and which survive to produce pi?"
    )
    reference = "PROOF.md Lemma 1 and Theorem 4"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Factor 16 - y^8 over the rationals into four quadratics.")
            .step("Divide the BBP numerator 4 - 2y^3 - y^4 - y^5 by each quadratic.")
            .step("List the roots of the quadratics that do not divide it.")
            .conclude("Those are the poles of the reduced integrand.")
        )

    commentary = (
        "The BBP numerator is exactly -(y - 1)(y^2 + 2)(y^2 + 2y + 2): it cancels the "
        "imaginary pair +-i sqrt2 and the left-hand pair -1 +- i, and keeps the real pair "
        "+-sqrt2 and the pair 1 +- i at 45 degrees. Of the octagon's two squares (axis-aligned "
        "+-sqrt2, +-i sqrt2 and diagonal +-1 +- i), BBP keeps one half of each: the half that "
        "faces the positive real direction. The kept 1 +- i give pi; the kept +-sqrt2 cancel "
        "the logarithm (Theorem 4)."
    )

    def model(self):
        full = sp.expand(-sp.Mul(*QUADRATICS.values()))
        P = 4 - 2 * y**3 - y**4 - y**5
        divides = [k for k, q in QUADRATICS.items() if sp.rem(P, q, y) == 0]
        kept = [k for k in QUADRATICS if k not in divides]
        poles = sorted({str(sp.nsimplify(r)) for k in kept for r in sp.solve(QUADRATICS[k], y)})
        return (
            Model()
            .add("16 - y^8 = -(product of the four quadratics) (1=yes)", int(sp.expand(full - (16 - y**8)) == 0))
            .add("BBP numerator = -(y-1)(y^2+2)(y^2+2y+2) (1=yes)",
                 int(sp.expand(P + (y - 1) * (y**2 + 2) * (y**2 + 2*y + 2)) == 0))
            .add("Quadratics cancelled by the numerator", ", ".join(divides))
            .add("Poles kept", ", ".join(poles))
        )

    def observations(self):
        return (
            Observed()
            .add("16 - y^8 = -(product of the four quadratics) (1=yes)", 1)
            .add("BBP numerator = -(y-1)(y^2+2)(y^2+2y+2) (1=yes)", 1)
            .add("Quadratics cancelled by the numerator", "y^2 + 2, y^2 + 2y + 2")
            # Roots of y^2 - 2 and y^2 - 2y + 2.
            .add("Poles kept", "-sqrt(2), 1 + I, 1 - I, sqrt(2)")
        )


ALL_TESTS = [BBPIntegrandPoles]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("18", "BBP integrand poles.", ALL_TESTS) else 1)
