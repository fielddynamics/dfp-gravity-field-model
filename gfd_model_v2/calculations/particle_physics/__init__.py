"""
Particle Physics: Standard Model Correspondences

This module examines correspondences between the stellated octahedron geometry
and Standard Model parameters including particle properties, quark charges,
shell structure, and advanced quantum numbers.
"""

from .test_particle_properties import ALL_TESTS as PARTICLE_TESTS, run_all as run_particle_properties
from .test_particle_advanced import ALL_TESTS as ADVANCED_TESTS, run_all as run_particle_advanced
from .test_quark_derivations import ALL_TESTS as QUARK_TESTS, run_all as run_quark_derivations
from .test_shell_structure import ALL_TESTS as SHELL_TESTS, run_all as run_shell_structure

__all__ = [
    'PARTICLE_TESTS',
    'ADVANCED_TESTS',
    'QUARK_TESTS',
    'SHELL_TESTS',
    'run_particle_properties',
    'run_particle_advanced',
    'run_quark_derivations',
    'run_shell_structure',
]
