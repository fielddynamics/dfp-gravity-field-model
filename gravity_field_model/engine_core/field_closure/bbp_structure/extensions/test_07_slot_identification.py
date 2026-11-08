"""
07. How the slots are laid on the cube
======================================

Role:     Probes the one input of PROOF.md Theorem 3 that is a choice: which vertex each slot belongs to.
Expected: Passes. A failure means a different natural identification selects a different formula than recorded.

The theorems read slot j (denominator 8k + j) as the vertex labelled j mod 8.
Other identifications are possible. This test tries four natural ones and
records which formula for pi each one's TIME silence selects:

    j mod 8          slot 8 -> 0, slots 1..7 -> 1..7    (the theorems' choice)
    7 - (j mod 8)    the same with every label complemented
    -j mod 8         slots counted the other way round the cube
    j - 1            slots shifted by one (slot 1 -> vertex 0)

Each slot weight of the family is linear in r (PROOF.md, Theorem 3), so each
answer is an exact solve.
"""

import sympy as sp

from gravity_field_model.framework import *

BBP = {1: 4, 4: -2, 5: -1, 6: -1}
AW = {1: 8, 2: -8, 3: -4, 4: -8, 5: -2, 6: -2, 7: 1, 8: 0}
MAPS = {
    "j mod 8": lambda j: j % 8,
    "7 - (j mod 8)": lambda j: 7 - (j % 8),
    "-j mod 8": lambda j: (-j) % 8,
    "j - 1": lambda j: j - 1,
}


class SlotIdentification(Test):
    name = "07. How the Slots Are Laid on the Cube"
    question = (
        "The selection reads slot j as vertex j mod 8. Under other natural ways of laying the "
        "eight slots on the cube, which formula does TIME silence select?"
    )
    reference = "PROOF.md Theorems 2 and 3"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("For each map, find the slots that land on vertices 0 and 7.")
            .step("Solve for the r at which the family's weights vanish there.")
            .conclude("Record which member of the family each identification selects.")
        )

    commentary = (
        "Reading slot j as vertex j mod 8, or as its complement 7 - j (which swaps the two "
        "tetrahedra and the two ends of the TIME axis), selects BBP. Counting the slots the "
        "other way round, or shifting them by one, puts slots 1 and 8 on the TIME axis and "
        "selects the member r = -1/2 instead, the formula that splits 3 + 1. So the result "
        "depends on the identification of slot with vertex. The natural one, the denominator's "
        "residue as the vertex's binary label, and its complement both give BBP."
    )

    def model(self):
        r = sp.symbols("r")
        m = Model()
        for name, f in MAPS.items():
            time_slots = [j for j in range(1, 9) if f(j) in (0, 7)]
            conds = [BBP.get(j, 0) + r * AW[j] for j in time_slots]
            conds = [c for c in conds if c != 0]
            sol = sp.solve(conds, r, dict=True)
            m.add(f"{name}: TIME slots", " ".join(map(str, time_slots)))
            m.add(f"{name}: selected r", " ".join(str(d[r]) for d in sol) if sol else "none")
        return m

    def observations(self):
        return (
            Observed()
            .add("j mod 8: TIME slots", "7 8")
            .add("j mod 8: selected r", "0")
            .add("7 - (j mod 8): TIME slots", "7 8")
            .add("7 - (j mod 8): selected r", "0")
            # Slots 1 and 8: weight 4 + 8r vanishes at r = -1/2; slot 8 is always 0.
            .add("-j mod 8: TIME slots", "1 8")
            .add("-j mod 8: selected r", "-1/2")
            .add("j - 1: TIME slots", "1 8")
            .add("j - 1: selected r", "-1/2")
        )


ALL_TESTS = [SlotIdentification]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("07", "Slot identifications.", ALL_TESTS) else 1)
