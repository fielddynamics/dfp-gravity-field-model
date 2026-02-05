"""
Coupling Dynamics Module
========================

Tests for tetrahedra coupling validation in the stellated octahedron geometry.

These tests verify the geometric constraints that make the dual tetrahedra
structure unique: parity partition, complementary pairing, and central symmetry.
"""

from .test_tetrahedra_coupling import (
    ALL_TESTS,
    run_all,
    ParityPartitionIsUnique,
    ComplementsAlwaysCrossTetrahedra,
    OriginEquidistantFromAllVertices,
)

__all__ = [
    "ALL_TESTS",
    "run_all",
    "ParityPartitionIsUnique",
    "ComplementsAlwaysCrossTetrahedra",
    "OriginEquidistantFromAllVertices",
]
