"""
Black Hole Mechanics Tests

Tests for extreme gravity field compression and spacetime topology,
comparing GFM model predictions against general relativity and
observational data from LIGO and EHT.
"""

# The names below are the test classes that exist in
# test_black_hole_mechanics.py. (This file previously imported twelve class
# names that no longer exist, so importing the package raised ImportError.)
from .test_black_hole_mechanics import (
    ALL_TESTS,
    run_all,
    SchwarzschildRadiusReference,
    FieldClosureAtHorizon,
)

__all__ = [
    "ALL_TESTS",
    "run_all",
    "SchwarzschildRadiusReference",
    "FieldClosureAtHorizon",
]
