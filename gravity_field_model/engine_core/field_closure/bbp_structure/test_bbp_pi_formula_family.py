"""
All base-16, period-8 formulas for pi
=====================================

The BBP formula is not the only way to write pi with base 16 and
denominators 8n + j. Adamchik and Wagon (1997) found a one-parameter family:
for every r,

    pi = sum_n 16^-n [ (4+8r)/(8n+1) - 8r/(8n+2) - 4r/(8n+3) - (2+8r)/(8n+4)
                       - (1+2r)/(8n+5) - (1+2r)/(8n+6) + r/(8n+7) ].

The published BBP formula is r = 0. This test checks whether the family is
complete, i.e. whether the eight slot series satisfy exactly one rational
relation (the r-term), using the PSLQ integer relation algorithm at 100
digits. It also checks that the base -4, period-4 formula for pi,

    pi = sum_k (-1/4)^k [ 2/(4k+1) + 2/(4k+2) + 1/(4k+3) ],

is the member r = -1/4 regrouped in pairs of terms.

Any claim that the octahedron explains the BBP formula has to explain why it
picks r = 0 out of this family; the selection test in this package asks that.
"""

from fractions import Fraction

from mpmath import mp, mpf, pi

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import (
    PRECISION, MAX_COEFF, SLOTS, AW_PER_R, aw_weights, slot_values, formula_value, integer_relation,
)

SAMPLE_R = [Fraction(-1), Fraction(-1, 2), Fraction(-1, 4), Fraction(0), Fraction(1, 7), Fraction(3)]


def base_minus4_as_base16() -> dict:
    """
    Regroup sum_k (-1/4)^k [2/(4k+1) + 2/(4k+2) + 1/(4k+3)] into base 16:
    even k = 2n gives denominators 8n+1, 8n+2, 8n+3 with weights 2, 2, 1;
    odd k = 2n+1 gives 8n+5, 8n+6, 8n+7 with weights (-1/4)(2, 2, 1).
    """
    w = {j: Fraction(0) for j in SLOTS}
    w[1], w[2], w[3] = Fraction(2), Fraction(2), Fraction(1)
    w[5], w[6], w[7] = Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 4)
    return w


class PiFormulaFamily(Test):
    name = "Complete Family of Base-16 Period-8 Formulas for Pi"
    question = (
        "Is the BBP formula the only way to write pi with base 16 and denominators 8n+j, "
        "or one member of a larger family; and is the family complete?"
    )
    reference = (
        "Adamchik and Wagon (1997), Amer. Math. Monthly 104, 852-855; "
        "PSLQ: Ferguson, Bailey, Arno (1999), Math. Comp. 68, 351-369"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Compute the eight slot series S_j = sum_n 1/(16^n (8n+j)) to 100 digits.")
            .step("Run PSLQ on (S_1..S_8): it returns one integer relation.")
            .step("Remove S_7 (the relation's coefficient there is +-1) and run PSLQ again: no further relation.")
            .step("So the formulas for pi form a line: one particular solution plus r times the relation.")
            .step("Compare the relation with the Adamchik-Wagon r-term and evaluate members at several r.")
            .conclude("The BBP formula is the member r = 0 of a complete one-parameter family.")
        )

    commentary = (
        "Pi has infinitely many base-16, period-8 formulas: one for every rational r. They "
        "differ by a combination of slot series that sums to exactly zero, "
        "8S_1 - 8S_2 - 4S_3 - 8S_4 - 2S_5 - 2S_6 + S_7 = 0, and PSLQ finds no other "
        "relation, so the family is complete (up to coefficients of 10^8 at 100 digits). "
        "The weights of a member sum to -15r, so only r = 0 has zero weight sum and only "
        "r = 0 leaves slot 7 empty. The base -4, period-4 formula is the member r = -1/4, "
        "so pi also has a compact formula at base -4 and period 4. The four-slot, zero-sum "
        "BBP formula is therefore a choice within the family, and that choice is what an "
        "octahedral explanation has to account for."
    )

    def model(self):
        vals = slot_values()
        rel = integer_relation(vals)
        # Normalise the sign so the slot-7 coefficient is +1.
        if rel is not None and rel[6] < 0:
            rel = [-x for x in rel]
        reduced = integer_relation([vals[j - 1] for j in SLOTS if j != 7])
        n_relations = (1 if rel is not None else 0) + (1 if reduced is not None else 0)
        matches_aw = rel is not None and all(rel[j - 1] == AW_PER_R[j] for j in SLOTS)
        with mp.workdps(PRECISION):
            worst = max(abs(formula_value(aw_weights(r)) - pi) for r in SAMPLE_R)
        b4 = base_minus4_as_base16()
        return (
            Model()
            .add("Independent relations among the 8 slot series", n_relations)
            .add("Relation equals Adamchik-Wagon r-term (1=yes)", 1 if matches_aw else 0)
            .add("Max |member - pi| over sampled r", float(worst))
            .add("Weight sum per unit r", sum(rel) if rel is not None else 0)
            .add("Base -4 formula equals member r=-1/4 (1=yes)", 1 if b4 == aw_weights(Fraction(-1, 4)) else 0)
            .add("BBP formula equals member r=0 (1=yes)",
                 1 if {j: w for j, w in aw_weights(0).items() if w != 0} == {j: Fraction(w) for j, w in {1: 4, 4: -2, 5: -1, 6: -1}.items()} else 0)
        )

    def observations(self):
        return (
            Observed()
            # Adamchik and Wagon (1997) give exactly one free parameter.
            .add("Independent relations among the 8 slot series", 1)
            .add("Relation equals Adamchik-Wagon r-term (1=yes)", 1)
            .add("Max |member - pi| over sampled r", 0.0, abs_tol=1e-60)
            # 8 - 8 - 4 - 8 - 2 - 2 + 1 from the published family.
            .add("Weight sum per unit r", -15)
            .add("Base -4 formula equals member r=-1/4 (1=yes)", 1)
            .add("BBP formula equals member r=0 (1=yes)", 1)
        )


ALL_TESTS = [PiFormulaFamily]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Pi formula family", "All base-16 period-8 formulas for pi.", ALL_TESTS) else 1)
