"""
Vortex Dynamics Tests
=====================

Tests that validate the vortex interpretation of field closure.

The vortex cosmology model states that gravity is a vortex field around the Field Origin,
with the pi-base-8 traversal creating a spiral structure. These tests validate:

1. MerkabaSpinRate: Compute and validate the Merkaba rotation frequency
2. VortexAngularMomentum: Verify angular momentum in the traversal
3. BiDirectionalFlow: Test that vortex flow can be reversed

Reference: VORTEX_COSMOLOGY_AND_INFORMATION_DOMAINS.md
"""

from .test_merkaba_spin_rate import *
from .test_vortex_angular_momentum import *
from .test_bidirectional_flow import *
