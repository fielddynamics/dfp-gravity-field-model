"""
BBP Structure: tests of the hypothesis that the BBP formula is the
stellated-octahedron structure.

PROOF.md states the theorems (I Ching and BBP as the stellated octahedron realizing pi);
test_octahedron_pi_theorems.py checks them exactly.

Each test states a consequence of the hypothesis that could fail, and checks
it against mathematics independent of the model.

- test_bbp_integral_mechanism.py: which factor of the BBP integrand produces pi
- test_bbp_face_diagonal_reading.py: the integrand's roots as cube / tetrahedron ratios, with a square as control
- test_bbp_pi_formula_family.py: the complete Adamchik-Wagon family of base-16 formulas for pi
- test_bbp_octahedral_selection.py: do the octahedral conditions select the BBP member (r = 0)?
- test_bbp_octahedral_prediction.py: does the octahedral shape single out pi among other BBP constants?
- test_reading_symmetry.py: is the six-constraint face reading (why_pi_formal_derivation.md)
  invariant under the octahedron's symmetries, and which trigram line order gives pi?
  (fails: 1 of 6 symmetric relabellings gives pi; the I Ching line order selects it)
- test_reading_weight_rule.py: can an agreement rule give the BBP numerators?
  (fails: no; the coded rule is ordered)
- test_hexagram_closure_null.py: does the I Ching closure walk need pi? (no: random digits close it alike)
- test_iching_visit_order.py: is the Shuo Gua family sequence the BBP reading order? (yes, in both
  tetrahedra; the only documented arrangement that is)
- test_iching_encoding_selection.py: which I Ching facts fix the trigram encoding? (the Fu Xi numbering
  and the birth order do; parity, opposites and the TIME-face step hold under all six)
- test_bbp_ladder_base8.py: the BBP ladder gives base-8 digits of pi at any position (up to 10,000)
- test_walk_from_bbp_ladder.py: the closure walk driven by the BBP formula alone (closes at step 332)
- test_pi_walk_visit_order.py: does the pi walk visit the vertices in the Shuo Gua order? (fails: no)

The three failing tests are EXPLORATORY and fail on purpose: their expected
values are predictions of the claims under test (the geometry alone forces pi;
the pi walk follows the I Ching's order).

Requires mpmath (PSLQ and 100-digit arithmetic) and sympy (exact integration).
"""
