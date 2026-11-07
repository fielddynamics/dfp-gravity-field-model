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

Requires mpmath (PSLQ and 100-digit arithmetic).
"""
