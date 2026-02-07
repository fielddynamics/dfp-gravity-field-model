"""
Black Hole Mechanics Tests

Tests for extreme gravity field compression and spacetime topology,
comparing GFM model predictions against general relativity and
observational data from LIGO and EHT.
"""

from .test_black_hole_mechanics import (
    ALL_TESTS,
    run_all,
    SchwarzschildRadius,
    HawkingTemperature,
    BekensteinHawkingEntropy,
    PhotonSphere,
    ISCO,
    TimeDilationAtHorizon,
    EvaporationTime,
    BlackHoleShadow,
    MergerEnergy,
    PenroseProcess,
    MinimumBlackHoleMass,
    GravityFieldPropagationSpeed,
)

__all__ = [
    "ALL_TESTS",
    "run_all",
    "SchwarzschildRadius",
    "HawkingTemperature",
    "BekensteinHawkingEntropy",
    "PhotonSphere",
    "ISCO",
    "TimeDilationAtHorizon",
    "EvaporationTime",
    "BlackHoleShadow",
    "MergerEnergy",
    "PenroseProcess",
    "MinimumBlackHoleMass",
    "GravityFieldPropagationSpeed",
]
