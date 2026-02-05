"""
Biological Mechanics Tests

Reduced to honest assessments of the Fe-56 numerical coincidence.
Original tests were numerology (noting patterns without derivation).

The remaining tests document observations and include one genuine
statistical test that could be falsified.
"""

from .test_iron_hemoglobin import (
    Fe56CoincidenceNote,
    TetrahedralStabilityStatistic,
    ALL_TESTS,
    run_all,
)

__all__ = [
    'Fe56CoincidenceNote',
    'TetrahedralStabilityStatistic',
    'ALL_TESTS',
    'run_all',
]
