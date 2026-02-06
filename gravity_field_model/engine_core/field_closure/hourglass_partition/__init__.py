"""
Hourglass Partition Tests
=========================

Tests that validate the hourglass vortex model of electron spin.

The electron is modeled as an hourglass vortex spanning TetA and TetB, with the
Field Origin as the "neck". Spin-1/2 emerges from the fraction of angular momentum
that flows through the TIME faces (the neck).

Key ratio: 2/8 = 25% flows through the neck, giving S = (2/8) x 2hbar = hbar/2

These tests validate:
1. TimeFaceCompletionRate: TIME faces complete differently than SPATIAL
2. NeckFlowRatio: Validate the 2/8 = 25% transfer ratio
3. AngularMomentumPartition: Verify 3:2:3 split (TetA : neck : TetB)

Reference: ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md
"""

from .test_time_face_completion import *
from .test_neck_flow_ratio import *
from .test_angular_momentum_partition import *
