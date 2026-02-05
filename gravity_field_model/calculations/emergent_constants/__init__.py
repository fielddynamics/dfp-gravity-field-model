"""
Emergent Constants: Fundamental Parameters from GFD Geometry
============================================================

This module demonstrates that fundamental physical constants are NOT
arbitrary parameters requiring fine-tuning, but EMERGE naturally from
the tetrahedral field closure geometry with k=4 vertices in d=3 spatial
dimensions.

Key Results:
- Fine structure constant: alpha = 1/137 from 861/(2*pi)
- Proton-electron mass ratio: m_p/m_e = 6*pi^5 = 1836
- Gravitational constant: G from Merkaba geometry
- Bekenstein-Hawking factor: 4 = k (exact)
- MOND acceleration scale from hexagonal geometry
- Spin-1/2 from TIME face topology
"""

from .test_emergent_constants import ALL_TESTS as EMERGENT_TESTS
from .test_emergent_constants import run_all as run_emergent_constants

from .test_emergent_constants_extended import ALL_TESTS as EXTENDED_TESTS
from .test_emergent_constants_extended import run_all as run_extended

from .test_field_energy import ALL_TESTS as FIELD_ENERGY_TESTS
from .test_field_energy import run_all as run_field_energy

from .test_hubble_electron_mond import ALL_TESTS as HUBBLE_TESTS
from .test_hubble_electron_mond import run_all as run_hubble_mond

from .test_mond_hexagonal import ALL_TESTS as MOND_TESTS
from .test_mond_hexagonal import run_all as run_mond_hexagonal

from .test_sixfold_symmetry import ALL_TESTS as SIXFOLD_TESTS
from .test_sixfold_symmetry import run_all as run_sixfold

from .test_spin_derivation import ALL_TESTS as SPIN_TESTS
from .test_spin_derivation import run_all as run_spin

__all__ = [
    "EMERGENT_TESTS",
    "EXTENDED_TESTS",
    "FIELD_ENERGY_TESTS",
    "HUBBLE_TESTS",
    "MOND_TESTS",
    "SIXFOLD_TESTS",
    "SPIN_TESTS",
    "run_emergent_constants",
    "run_extended",
    "run_field_energy",
    "run_hubble_mond",
    "run_mond_hexagonal",
    "run_sixfold",
    "run_spin",
]
