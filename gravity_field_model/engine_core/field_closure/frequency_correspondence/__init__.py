"""
Frequency Correspondence Tests
==============================

Tests that map field closure dynamics to physical frequencies.

The Field Origin is described as a "resonance node, not a spatial point."
These tests validate the frequency relationships:

1. OrbitToComptonFrequency: Map orbit frequency to electron Compton frequency
2. SpinorPhaseProperty: Verify 720 degree (2 orbit) phase return
3. HarmonicResonance: Test for harmonic structure in orbit periods

Key relationships:
- Electron Compton frequency: f_e = m_e c^2 / h ~ 1.24e20 Hz
- Mean digits per orbit: ~2.42
- Merkaba spin rate: f_e / (2 x digits_per_orbit) for spinor period

Reference: THE_ORIGIN_TIME_AND_ONE.md
"""

from .test_orbit_to_compton import *
from .test_spinor_phase_property import *
from .test_harmonic_resonance import *
