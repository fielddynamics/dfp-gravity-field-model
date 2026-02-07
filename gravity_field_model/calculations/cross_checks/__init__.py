"""
Cross-Checks: Inter-Module Consistency Validation

This module verifies consistency across different calculation domains in the
GFM validation suite. Tests confirm that k=4, fundamental constants, and
geometric relationships maintain agreement between modules.
"""

from .test_cross_checks import ALL_TESTS, run_all

__all__ = ["ALL_TESTS", "run_all"]
