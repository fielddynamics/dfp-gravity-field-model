"""
03. All formulas with the octahedral shape and BBP's magnitudes
===============================================================

Role:     Extends PROOF.md Theorem 3: searches every formula with the full octahedral shape for named constants.
Expected: Passes. A failure means a formula of this shape equals a single named constant other than pi.

Take every formula with the shape BBP has:
- TIME silent (slots 7 and 8 empty);
- four active slots, two in each tetrahedron (two of slots 1, 2, 4 and two of 3, 5, 6);
- weights a permutation of (4, -2, -1, -1) or of (-4, 2, 1, 1), so they sum to zero.

That is 9 slot sets x 24 weightings = 216 formulas. Each has an exact value
in the seven named constants (test 01). The test counts those whose value is a
rational multiple of a single named constant.
"""

from itertools import combinations, permutations

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.extensions.named_basis import (
    NAMES, value_vector,
)

TETA_SLOTS, TETB_SLOTS = (1, 2, 4), (3, 5, 6)


class OctahedralMagnitudeFormulas(Test):
    name = "03. Every Octahedral-Shape Formula with BBP's Magnitudes"
    question = (
        "Among all 216 formulas with BBP's octahedral shape and magnitudes, which equal a "
        "single named constant?"
    )
    reference = "PROOF.md Theorem 3; test 01; research check 25 (bbp_field_closure_complete.py)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Choose two slots from 1, 2, 4 (father's family) and two from 3, 5, 6 (mother's).")
            .step("Assign each permutation of (4,-2,-1,-1) and of (-4,2,1,1).")
            .step("Write each formula's value exactly in the seven named constants.")
            .conclude("Count the values that are a multiple of one named constant.")
        )

    commentary = (
        "Of 216 formulas with the octahedral shape and BBP's magnitudes, exactly two equal a "
        "single named constant: BBP and its negative, both pi. Every other arrangement gives "
        "a mixture of three or more constants. This strengthens research check 25, which fixed "
        "the slots in advance: here the slots range over every TIME-silent, chamber-balanced "
        "choice."
    )

    def model(self):
        total, singles = 0, []
        for a in combinations(TETA_SLOTS, 2):
            for b in combinations(TETB_SLOTS, 2):
                slots = a + b
                for ws in set(permutations((4, -2, -1, -1))) | set(permutations((-4, 2, 1, 1))):
                    total += 1
                    v = value_vector(dict(zip(slots, ws)))
                    nz = [k for k in range(7) if v[k] != 0]
                    if len(nz) == 1:
                        singles.append((tuple(sorted(slots)), NAMES[nz[0]], v[nz[0]]))
        return (
            Model()
            .add("Formulas with the octahedral shape", total)
            .add("Formulas equal to a single named constant", len(singles))
            .add("Those constants", ", ".join(sorted({f"{c} x {m}" for _, c, m in singles})))
            .add("Their slots", ", ".join(sorted({str(s) for s, _, _ in singles})))
        )

    def observations(self):
        return (
            Observed()
            # 3 x 3 slot sets; 12 distinct permutations of each signed multiset.
            .add("Formulas with the octahedral shape", 216)
            .add("Formulas equal to a single named constant", 2)
            .add("Those constants", "pi x -1, pi x 1")
            .add("Their slots", "(1, 4, 5, 6)")
        )


ALL_TESTS = [OctahedralMagnitudeFormulas]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("03", "Octahedral-shape formulas.", ALL_TESTS) else 1)
