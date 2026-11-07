"""
Where pi comes from inside the BBP formula
==========================================

Role:     PROOF.md Theorem 4: where pi arises inside BBP.
Expected: Passes. A failure means the partial-fraction account of BBP is wrong.

Summing the four BBP slot series term by term turns the formula into one
integral (Bailey, Borwein, Plouffe 1997):

    pi = integral_0^1 16 (y - 1) / (y^4 - 2y^3 + 4y - 4) dy.

The denominator factors as (y^2 - 2)(y^2 - 2y + 2), with roots +-sqrt(2) and
1 +- i. This test splits the integral into partial fractions and checks which
piece produces pi and which pieces cancel. Every expected value is a closed
form; nothing is taken from the model.
"""

from mpmath import mp, mpf, quad, pi, log, sqrt, polyroots, mpc

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import PRECISION

TOL = mpf(10) ** (-(PRECISION - 20))


class BBPIntegralMechanism(Test):
    name = "BBP Integral: Which Factor Produces Pi"
    question = (
        "The BBP formula is an integral of a rational function whose denominator has "
        "two quadratic factors. Which factor produces pi, and what does the other one do?"
    )
    reference = "Bailey, Borwein, Plouffe (1997), Math. Comp. 66, 903-913"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Write 1/(8n+j) = integral_0^1 t^(8n+j-1) dt and sum the geometric series in n.")
            .step("With t = y / sqrt(2) the four BBP slots combine to 16(y-1)/(y^4-2y^3+4y-4) on [0, 1].")
            .step("The denominator factors as (y^2 - 2)(y^2 - 2y + 2).")
            .step("Partial fractions: 4y/(y^2-2) - 4(y-1)/((y-1)^2+1) + 4/((y-1)^2+1).")
            .step("The first two terms are logarithms, -ln 4 and +ln 4; they cancel.")
            .conclude("The last term is 4 arctan(1) = 4 (pi/4) = pi: the factor with roots 1 +- i produces pi.")
        )

    commentary = (
        "Pi enters the BBP formula through one factor, y^2 - 2y + 2 = (y-1)^2 + 1, whose "
        "roots 1 +- i lie at 45 degrees; its arctangent term gives 4 x pi/4. The other factor, "
        "y^2 - 2 with roots +-sqrt(2), contributes only a logarithm, and that logarithm "
        "cancels the logarithm from the first factor. So any geometric account of why BBP "
        "computes pi has to account for these two roles: a 45-degree point that produces pi, "
        "and a sqrt(2) that removes the logarithm."
    )

    def model(self):
        with mp.workdps(PRECISION):
            f = lambda y: 16 * (y - 1) / (y ** 4 - 2 * y ** 3 + 4 * y - 4)
            full = quad(f, [0, 1])
            log_sqrt2_factor = quad(lambda y: 4 * y / (y ** 2 - 2), [0, 1])
            log_complex_factor = quad(lambda y: -4 * (y - 1) / ((y - 1) ** 2 + 1), [0, 1])
            arctan_part = quad(lambda y: 4 / ((y - 1) ** 2 + 1), [0, 1])
            roots = polyroots([1, -2, 0, 4, -4], maxsteps=200, extraprec=200)
            expected = [sqrt(2), -sqrt(2), mpc(1, 1), mpc(1, -1)]
            roots_match = all(min(abs(r - e) for r in roots) < TOL for e in expected)
            return (
                Model()
                .add("Integral minus pi", float(full - pi))
                .add("Roots are +-sqrt(2) and 1+-i (1=yes)", 1 if roots_match else 0)
                .add("Log term of (y^2-2) factor", float(log_sqrt2_factor))
                .add("Log term of (y^2-2y+2) factor", float(log_complex_factor))
                .add("Sum of log terms", float(log_sqrt2_factor + log_complex_factor))
                .add("Arctan term / pi", float(arctan_part / pi))
            )

    def observations(self):
        ln4 = float(log(4))
        return (
            Observed()
            .add("Integral minus pi", 0.0, abs_tol=1e-30)
            .add("Roots are +-sqrt(2) and 1+-i (1=yes)", 1)
            .add("Log term of (y^2-2) factor", -ln4, abs_tol=1e-14)   # 2 ln|y^2-2| from 0 to 1 = -2 ln 2
            .add("Log term of (y^2-2y+2) factor", ln4, abs_tol=1e-14)  # -2 ln((y-1)^2+1) from 0 to 1 = 2 ln 2
            .add("Sum of log terms", 0.0, abs_tol=1e-14)
            .add("Arctan term / pi", 1.0, abs_tol=1e-14)               # 4 (arctan 0 - arctan(-1)) = pi
        )


ALL_TESTS = [BBPIntegralMechanism]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("BBP integral mechanism", "Which factor of the BBP integrand produces pi.", ALL_TESTS) else 1)
