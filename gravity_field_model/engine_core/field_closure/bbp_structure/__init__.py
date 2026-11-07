"""
BBP Structure: tests of the hypothesis that the BBP formula is the
stellated-octahedron structure.

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

The two failing tests are EXPLORATORY and fail on purpose: their expected
values are the predictions of the claim that the geometry alone forces pi.

Requires mpmath (PSLQ and 100-digit arithmetic).
"""
