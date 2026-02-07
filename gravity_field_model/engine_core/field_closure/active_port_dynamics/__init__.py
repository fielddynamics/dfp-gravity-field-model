"""
Active Port Face Dynamics Tests
===============================

Tests that model the fluid-like field dynamics on active coupling port faces.

THE PHYSICAL MODEL:
Each face of the stellated octahedron is a "Coupling Port" through which
gravitational flux flows. When the pi-base-8 traversal visits a vertex,
it activates the 3 faces containing that vertex. This activation creates
a flow pattern that we can analyze as fluid dynamics.

KEY CONCEPTS:
1. Face Activation: Which faces are "lit up" at each step
2. Triad Dynamics: Each face has 4 triads (sub-triangles) that phase-lock flux
3. Flux Direction: Is flow inward (to origin) or outward (to space)?
4. Face Angular Momentum: Projection of vortex L onto each face normal

THE QUESTION:
If the Merkaba is vortexing at ~5e19 Hz, what are the local field dynamics
on each active face? Can we calculate the spin and flux at the face level?

Reference:
- GFM_concepts.py: Coupling Port mechanics, Triad phase-locking
- test_face_sampling_subdivision.py: Medial construction of triads
- VORTEX_COSMOLOGY_AND_INFORMATION_DOMAINS.md: Vortex model
"""

from .test_face_activation_flow import *
from .test_triad_dynamics import *
from .test_face_flux_spin import *
