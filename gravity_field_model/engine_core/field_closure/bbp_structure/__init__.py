"""
BBP Structure: the I Ching and the BBP formula as the stellated octahedron.

Start with README.md (what was found and how the tests map to it) and
PROOF.md (the theorems and their proofs).

Main result (PROOF.md, Theorems 1-3, checked by test_bbp_completeness_proof.py):
in the I Ching's encoding of the cube's vertices, exactly one base-16,
period-8 formula for pi leaves the two TIME apices (father Qian, mother Kun)
silent, and it is the BBP formula; its four slots, 2+2 chamber split and
zero weight sum then follow.

Helpers:
- bbp_slots.py: the slot series S_j, the Adamchik-Wagon family, the octahedral conditions
- bbp_ladder.py: BBP digit extraction (base 16 and base 8 at any position)
- closure_reading.py: the six-constraint face reading of why_pi_formal_derivation.md
- iching_orders.py: the documented trigram orders, with sources

Every test module begins with a Role line (which theorem or finding it
supports) and an Expected line (what a pass means). All tests are expected to
pass.

Requires mpmath (PSLQ, high precision) and sympy (exact algebra and integration).
"""
