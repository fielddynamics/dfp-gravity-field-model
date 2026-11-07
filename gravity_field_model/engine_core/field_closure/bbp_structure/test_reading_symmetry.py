"""
Is the face reading that yields pi a property of the geometry?
==============================================================

Role:     PROOF.md Theorem 5: only the I Ching rank order of the children gives pi; refutes 'no freedom' in why_pi_formal_derivation.md.
Expected: Passes when 1 of the 6 TIME-preserving relabellings gives pi.

Claim under test (``why_pi_formal_derivation.md``): six constraints, each
forced by the stellated octahedron, turn the TetA face normals into the BBP
series, so pi is "the geometry's only possible output".

If the output is fixed by the geometry, it cannot change under a symmetry of
the geometry. The stellated octahedron is unchanged by any permutation of the
three coordinate axes: such a permutation maps TetA to TetA and fixes the
TIME apices 0 and 7, so the temporal face stays first and only the three
spatial faces (or, equivalently, the roles of x, y and z) are relabelled.
There are six such symmetries. The test runs the mechanism exactly as the
derivation specifies under each of them.

Finding: only one of the six gives pi, so the claim that the geometry alone
forces every coefficient does not hold. The closure condition (signed
numerators summing to zero), which the derivation calls automatic, holds in
all six and so does not select pi.

The I Ching itself breaks this symmetry: a trigram's lines are ordered,
bottom to top. The test also records which line order the pi-giving
labelling corresponds to, reading the axis-to-line assignment off the three
sons of the Shuo Gua family (Zhen, Kan, Gen: one yang line at the bottom,
middle and top respectively).
"""

from mpmath import mp, pi

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import PRECISION, formula_value
from gravity_field_model.engine_core.field_closure.bbp_structure.closure_reading import (
    ALL_AXIS_PERMUTATIONS, axis_permutation_is_symmetry, read, line_of_axis,
)

TOL = mp.mpf(10) ** (-(PRECISION - 20))


class ReadingSymmetry(Test):
    name = "Face Reading of Pi under the Octahedron's Symmetries"
    question = (
        "The derivation says the stellated octahedron forces the BBP series for pi. The "
        "octahedron is unchanged when the three spatial axes are relabelled. Does the "
        "reading still give pi after each such relabelling?"
    )
    reference = (
        "Mechanism: research/exploratory/i-ching/why_pi_formal_derivation.md and "
        "why_pi_verification.py; series values to 100 digits with mpmath"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("List the six permutations of (x, y, z); check each maps TetA to TetA and fixes vertices 0 and 7.")
            .step("For each, run the six-constraint reading: axis vectors, z running sum for positions, (x, y) rule for magnitudes, temporal + / spatial - signs.")
            .step("Sum the resulting series to 100 digits and compare with pi.")
            .step("Check the signed numerator sum (closure) for each.")
            .conclude("A geometric derivation must give pi under all six; the count shows whether it does.")
        )

    commentary = (
        "Only one of the six relabellings gives pi. The other five give five different numbers "
        "(3.1838, 3.1920, 3.3102, 3.3498, 3.3680), although the stellated octahedron, its TIME "
        "axis and its temporal face are identical in all six. Closure holds in every case: the "
        "signed numerators always sum to zero, so closure does not select pi. The geometry "
        "alone therefore does not force the BBP series, contrary to why_pi_formal_derivation.md. "
        "What does select it is the I Ching's own ordering of the lines. The labelling that gives pi "
        "reads the bottom and middle lines, in that order, for the magnitudes and the top line "
        "for the sector positions; the axis-to-line assignment is read off the three sons "
        "(Zhen, Kan, Gen). So pi follows from the octahedron together with the trigram line "
        "order, bottom to top, plus two reading conventions: the top line supplies positions, "
        "and the magnitude rule is ordered (see the weight-rule test). A uniformly chosen line "
        "order would give pi one time in six."
    )

    def model(self):
        symmetries = [p for p in ALL_AXIS_PERMUTATIONS if axis_permutation_is_symmetry(p)]
        values, zero_sums = [], 0
        with mp.workdps(PRECISION):
            for p in symmetries:
                w, *_ = read(axes=p)
                values.append(formula_value(w))
                zero_sums += sum(w.values()) == 0
            gives_pi = sum(1 for v in values if abs(v - pi) < TOL)
            distinct = len({mp.nstr(v, 30) for v in values})
            paper_w, *_ = read()
            paper_is_pi = abs(formula_value(paper_w) - pi) < TOL
            pi_perms = [p for p, v in zip(symmetries, values) if abs(v - pi) < TOL]
        lines = line_of_axis()
        pi_line_order = (
            tuple(lines[i] for i in pi_perms[0]) if len(pi_perms) == 1 else ()
        )
        m = (
            Model()
            .add("Axis permutations that are symmetries (of 6)", len(symmetries))
            .add("Paper's labelling gives pi (1=yes)", 1 if paper_is_pi else 0)
            .add("Symmetry images giving pi (of 6)", gives_pi)
            .add("Symmetry images with zero numerator sum (of 6)", zero_sums)
            .add("Distinct series values among the 6 (info)", distinct)
            .add("Pi labelling reads lines bottom, middle (magnitudes), top (positions) (1=yes)",
                 1 if pi_line_order == ("bottom", "middle", "top") else 0)
        )
        for p, v in zip(symmetries, values):
            m.add(f"Value with axes {''.join('xyz'[i] for i in p)} (info)", float(v))
        return m

    def observations(self):
        return (
            Observed()
            # Every permutation of the axes preserves the cube, TetA and the TIME axis.
            .add("Axis permutations that are symmetries (of 6)", 6)
            .add("Paper's labelling gives pi (1=yes)", 1)
            # Exact integration of all six series (PROOF.md, Theorem 5): only the
            # rank order is pi; the nearest other value is ln(675/256) + 2 arctan 2.
            .add("Symmetry images giving pi (of 6)", 1)
            # The derivation calls closure automatic.
            .add("Symmetry images with zero numerator sum (of 6)", 6)
            # The I Ching reads a trigram from the bottom line up.
            .add("Pi labelling reads lines bottom, middle (magnitudes), top (positions) (1=yes)", 1)
        )


ALL_TESTS = [ReadingSymmetry]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Reading symmetry", "Is the pi reading invariant under the octahedron's symmetries?", ALL_TESTS) else 1)
