"""
Statistical Dynamics Tests
==========================

This module contains tests analyzing the traversal as a Markov-like process,
including transition matrices, dwell times, convergence, and robustness.

Key Questions Answered:
- What are the transition probabilities between vertices?
- How long does traversal stay in each chamber?
- How quickly do statistics converge?
- Are results robust across subsamples?

Tests:
- test_transition_matrix.py: 8x8 transition matrix analysis
- test_chamber_dynamics.py: Dwell times and crossings
- test_statistical_convergence.py: Sample size validation
- test_statistical_robustness.py: Hoeffding bounds, bootstrap

See README.md in this directory for detailed findings.
"""
