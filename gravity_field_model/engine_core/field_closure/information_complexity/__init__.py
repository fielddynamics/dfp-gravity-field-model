"""
Information and Complexity Tests
================================

This module contains tests applying information theory and complexity measures
to the traversal sequence, quantifying randomness and structure.

Key Questions Answered:
- How much entropy does the traversal have?
- Are there hidden periodicities?
- Is the sequence compressible?
- Does the algorithm work with other normal numbers?

Tests:
- test_information_theory.py: Shannon entropy, autocorrelation
- test_spectral_analysis.py: Fourier analysis, periodicity detection
- test_complexity_measures.py: Lempel-Ziv, permutation entropy
- test_constant_comparison.py: Algorithm validation with e, sqrt(2)

See README.md in this directory for detailed findings.
"""
