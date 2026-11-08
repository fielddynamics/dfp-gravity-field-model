"""
20. Auditing the numerical coincidences
=======================================

Role:     Weighs the numerical readings in the research notes against their comparison classes.
Expected: Passes. A failure means a recorded chance differs from the exact count stated.

Several research notes read numbers in BBP as octahedral quantities. Some are
now theorems (base, period, the TIME selection). Others are numerical
coincidences, and their weight depends on how many alternatives could have
matched. This test computes, exactly:

1. The BBP slots sum to 1 + 4 + 5 + 6 = 16 = K^2. Among the 9 TIME-silent,
   2 + 2 slot sets (the octahedral shape), how many sum to 16? Among all 70
   four-slot subsets of 0..7?
2. The silent slots sum to 0 + 2 + 3 + 7 = 12 = K D. Among the 70 subsets,
   how many have complement summing to 12? (Equivalent to the first sum being
   28 - 12 = 16.)
3. The weight magnitudes {4, 2, 1} are the bit place values. Given magnitudes
   {4, 2, 1, 1}, this is automatic; recorded for completeness.
4. The research claim that K^3 = 2^(2D) has an integer solution only at D = 3
   (bbp_field_closure_synthesis.md, constraint B): count the D <= 30 that solve it.
"""

from itertools import combinations

from gravity_field_model.framework import *

K, D = 4, 3


class NumerologyAudit(Test):
    name = "20. Auditing the Numerical Coincidences"
    question = (
        "How surprising are the numerical readings of BBP in the research notes, once each is "
        "set against the alternatives that could also have matched?"
    )
    reference = "bbp_field_closure_synthesis.md; Paper 6 plan (positions sum to K^2)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("List the 9 octahedral slot sets (two of 1, 2, 4 and two of 3, 5, 6) and their sums.")
            .step("List all 70 four-element subsets of 0..7 and count those summing to 16.")
            .step("Count D in 1..30 for which K^3 = 2^(2D) has an integer solution K.")
            .conclude("Report each coincidence with its comparison class.")
        )

    commentary = (
        "Among the nine octahedral slot sets, only BBP's sums to 16, so within its own shape "
        "the sum K^2 is distinctive (1 in 9). Among all 70 four-slot subsets, 7 sum to 16 "
        "(1 in 10), so as a bare number it is not rare, and 'silent slots sum to K D = 12' is "
        "the same fact restated. The place-value reading of {4, 2, 1} is automatic once the "
        "magnitudes are fixed. Constraint B of the synthesis, K^3 = 2^(2D) only at D = 3, is "
        "false: it has integer solutions at every multiple of 3. These numbers are worth "
        "noting, but the weight of the case rests on the theorems, not on them."
    )

    def model(self):
        octa = [a + b for a in combinations((1, 2, 4), 2) for b in combinations((3, 5, 6), 2)]
        octa16 = [s for s in octa if sum(s) == 16]
        all16 = [s for s in combinations(range(8), 4) if sum(s) == 16]
        silent12 = [s for s in combinations(range(8), 4) if 28 - sum(s) == 12]
        d_solutions = [d for d in range(1, 31) if round(2 ** (2 * d / 3)) ** 3 == 2 ** (2 * d)]
        return (
            Model()
            .add("Octahedral slot sets", len(octa))
            .add("Octahedral sets summing to 16", len(octa16))
            .add("That set", " ".join(map(str, sorted(octa16[0]))) if octa16 else "none")
            .add("All 4-subsets of 0..7 summing to 16", len(all16))
            .add("4-subsets whose complement sums to 12", len(silent12))
            .add("D <= 30 with an integer K, K^3 = 2^(2D)", len(d_solutions))
        )

    def observations(self):
        return (
            Observed()
            .add("Octahedral slot sets", 9)
            # Sums: {1,2}+{3,5},{3,6},{5,6} = 11,12,14; {1,4}+... = 13,14,16; {2,4}+... = 14,15,17.
            .add("Octahedral sets summing to 16", 1)
            .add("That set", "1 4 5 6")
            # Four-element subsets of {0..7} with sum 16, by hand: {0,3,6,7}, {0,4,5,7},
            # {1,2,6,7}, {1,3,5,7}, {1,4,5,6}, {2,3,4,7}, {2,3,5,6}.
            .add("All 4-subsets of 0..7 summing to 16", 7)
            # 0 + ... + 7 = 28, so complement sum 12 <=> subset sum 16.
            .add("4-subsets whose complement sums to 12", 7)
            # 2^(2D) is a cube exactly when 3 divides D: D = 3, 6, ..., 30.
            .add("D <= 30 with an integer K, K^3 = 2^(2D)", 10)
        )


ALL_TESTS = [NumerologyAudit]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("20", "Numerology audit.", ALL_TESTS) else 1)
