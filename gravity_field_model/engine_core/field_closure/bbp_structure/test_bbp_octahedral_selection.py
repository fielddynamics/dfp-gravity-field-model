"""
Does the octahedron select the BBP member of the family?
========================================================

Role:     PROOF.md Theorem 3 remark: each octahedral condition selects BBP within the family.
Expected: Passes. A failure means a condition admits a second member of the family.

Hypothesis: the BBP formula is the stellated-octahedron structure. If so, the
octahedral conditions read into it (TIME apices silent, weights summing to
zero, K = 4 active slots, two active slots per tetrahedron) should pick out
the BBP formula, r = 0, from the complete Adamchik-Wagon family of base-16,
period-8 formulas for pi, and should do so better than a criterion with no
geometry in it.

Each slot weight is linear in r, w_j(r) = a_j + r b_j, so the members where
any slot falls silent are the finitely many roots r = -a_j / b_j. The test
enumerates them exactly with rational arithmetic.

The geometric comparison criterion is sparsity: fewest active slots.
"""

from fractions import Fraction

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import (
    SLOTS, AW_CONSTANT, AW_PER_R, aw_weights, active_vertices, octahedral_conditions,
    is_octahedral, tetrahedra,
)


def special_members():
    """Every r at which some slot weight vanishes, plus one generic value."""
    rs = {Fraction(-AW_CONSTANT[j], AW_PER_R[j]) for j in SLOTS if AW_PER_R[j] != 0}
    generic = max(rs) + 1          # no slot weight vanishes here
    return sorted(rs) + [generic]


class OctahedralSelection(Test):
    name = "Octahedral Conditions Select the BBP Member"
    question = (
        "Pi has a whole family of base-16 formulas. Do the stellated-octahedron conditions "
        "(TIME silent, zero sum, four slots, 2+2 chamber split) pick out the BBP formula, "
        "and do they select more sharply than plain sparsity?"
    )
    reference = "Adamchik and Wagon (1997); conditions from the BBP field-closure synthesis note"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Members of the family have weights a_j + r b_j; a slot falls silent only at r = -a_j/b_j.")
            .step("Evaluate every condition at each such r and at one generic r.")
            .step("Count the members satisfying each condition alone, and all of them together.")
            .step("Compare with sparsity: how many members have the fewest active slots?")
            .conclude("If the octahedron explains BBP, its conditions should select r = 0 and only r = 0.")
        )

    commentary = (
        "The octahedral conditions select r = 0, the published BBP formula, and nothing else. "
        "Sparsity alone does not: two members have four active slots, r = 0 (slots 1,4,5,6) and "
        "r = -1/2 (slots 2,3,4,7). The second puts three active slots in one tetrahedron, one in "
        "the other, and uses the TIME apex 7, so the chamber and TIME conditions reject it. This "
        "is a real, checkable selection, in favour of the hypothesis. Two cautions. In a "
        "one-parameter family any single linear condition already picks one member; TIME "
        "silence alone (w_7 = 0) and zero sum alone (-15r = 0) both give r = 0, because they are "
        "the same member's properties. Since the family is complete "
        "(test_bbp_completeness_proof.py), these selections hold among all base-16, "
        "period-8 formulas for pi, not only within the family."
    )

    def model(self):
        members = special_members()
        conds = {r: octahedral_conditions(aw_weights(r)) for r in members}
        actives = {r: active_vertices(aw_weights(r)) for r in members}
        fewest = min(len(a) for a in actives.values())
        sparsest = [r for r in members if len(actives[r]) == fewest]
        octa = [r for r in members if is_octahedral(aw_weights(r))]
        t1, t2 = tetrahedra()
        other4 = [r for r in sparsest if r != 0]
        split_other = (
            f"{len(actives[other4[0]] & t1)}+{len(actives[other4[0]] & t2)}" if other4 else "none"
        )
        return (
            Model()
            .add("Members with TIME apices silent", sum(c["time_silent"] for c in conds.values()))
            .add("Members with zero weight sum", sum(c["zero_sum"] for c in conds.values()))
            .add("Members with four active slots", sum(c["four_active"] for c in conds.values()))
            .add("Members satisfying all octahedral conditions", len(octa))
            .add("Octahedral member is the BBP formula r=0 (1=yes)", 1 if octa == [0] else 0)
            .add("Fewest active slots in the family", fewest)
            .add("Members with the fewest active slots", len(sparsest))
            .add("Chamber split of the other four-slot member", split_other)
        )

    def observations(self):
        return (
            Observed()
            # Hypothesis predictions: each octahedral condition is met by the
            # BBP member alone, and together they select exactly r = 0.
            .add("Members with TIME apices silent", 1)
            .add("Members with zero weight sum", 1)
            .add("Members satisfying all octahedral conditions", 1)
            .add("Octahedral member is the BBP formula r=0 (1=yes)", 1)
        )


ALL_TESTS = [OctahedralSelection]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Octahedral selection", "Do octahedral conditions pick the BBP member?", ALL_TESTS) else 1)
