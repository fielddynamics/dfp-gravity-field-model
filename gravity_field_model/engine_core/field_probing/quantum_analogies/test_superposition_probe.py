"""
Superposition Probing
=====================

PROBING QUESTION: Can the field occupy multiple states simultaneously?

This probe tests for superposition-like behavior where the field's
"wave function" is spread across multiple vertices.

IMPORTANT CAVEAT: The GFD model is DETERMINISTIC, not quantum.
We're probing whether quantum-like statistics emerge from deterministic chaos.

MATHEMATICAL FOUNDATION:
- State vector |psi> with amplitudes at each vertex
- Superposition: |psi> = sum_v c_v |v>
- Delocalization measure: participation ratio PR = 1 / sum(p_v^2)

NULL HYPOTHESIS: Localized dynamics (one vertex at a time)
DISCOVERY: Delocalized statistics would suggest quantum-like behavior

Reference: Quantum mechanics, participation ratio
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def compute_windowed_distribution(history: List[int], window: int) -> np.ndarray:
    """
    Compute probability distribution over vertices in windows.
    
    Returns matrix of shape (n_windows, 8) where each row is a distribution.
    """
    n_windows = len(history) - window + 1
    distributions = np.zeros((n_windows, 8))
    
    for i in range(n_windows):
        segment = history[i:i+window]
        counts = Counter(segment)
        for v in range(8):
            distributions[i, v] = counts.get(v, 0) / window
    
    return distributions


def compute_participation_ratio(distribution: np.ndarray) -> float:
    """
    Compute participation ratio: measure of delocalization.
    
    PR = 1 / sum(p_v^2)
    
    PR = 1: completely localized (one vertex)
    PR = N: completely delocalized (uniform over N vertices)
    """
    p_squared = distribution ** 2
    ipr = np.sum(p_squared)
    
    if ipr > 0:
        return 1 / ipr
    return 1.0


def compute_effective_dimension(distributions: np.ndarray) -> float:
    """
    Compute effective dimension via principal component analysis.
    
    High effective dimension means the distribution explores many states.
    """
    if len(distributions) < 2:
        return 1.0
    
    # Subtract mean
    mean_dist = np.mean(distributions, axis=0)
    centered = distributions - mean_dist
    
    # Covariance matrix
    cov = np.cov(centered.T)
    
    # Eigenvalues
    eigenvalues = np.linalg.eigvalsh(cov)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    
    if len(eigenvalues) == 0:
        return 1.0
    
    # Effective dimension: exponential of entropy of normalized eigenvalues
    eigenvalues_norm = eigenvalues / np.sum(eigenvalues)
    entropy = -np.sum(eigenvalues_norm * np.log(eigenvalues_norm + 1e-10))
    
    return np.exp(entropy)


def compute_spreading_time(history: List[int]) -> float:
    """
    Compute time for the trajectory to spread across all vertices.
    
    This is analogous to quantum spreading of a wave packet.
    """
    visited = set()
    
    for t, v in enumerate(history):
        visited.add(v)
        if len(visited) == 8:  # All vertices visited
            return t + 1
    
    return len(history)  # Never fully spread


# =============================================================================
# TEST CLASSES
# =============================================================================

class ParticipationRatioProbe(Test):
    """
    PROBING: Measure delocalization via participation ratio.
    """
    name = "Participation Ratio (Delocalization)"
    question = (
        "How delocalized is the trajectory in vertex space? The participation "
        "ratio measures effective number of vertices occupied. High PR means "
        "superposition-like spread across many vertices."
    )
    reference = "Participation ratio, localization"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: While the trajectory is at one vertex at a time, its "
        "statistical distribution may be spread. We compute PR from the "
        "time-averaged distribution. High PR indicates quantum-like "
        "delocalization in a classical deterministic system."
    )

    def derivation(self):
        return (
            Derivation()
            .step("PARTICIPATION RATIO:")
            .equation("PR = 1 / sum(p_v^2)")
            .step("where p_v = probability of vertex v")
            .step("INTERPRETATION:")
            .step("  PR = 1: localized on one vertex")
            .step("  PR = 8: uniform over all 8 vertices")
            .step("  4 < PR < 8: delocalized across many")
            .step("QUANTUM ANALOGY:")
            .step("PR measures effective number of states in superposition.")
            .conclude("PR quantifies delocalization.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute distributions in windows
        window = 50
        distributions = compute_windowed_distribution(history, window)
        
        # Participation ratio for each window
        prs = [compute_participation_ratio(d) for d in distributions]
        
        mean_pr = np.mean(prs)
        std_pr = np.std(prs)
        min_pr = np.min(prs)
        max_pr = np.max(prs)
        
        # Overall distribution
        overall_dist = np.mean(distributions, axis=0)
        overall_pr = compute_participation_ratio(overall_dist)
        
        return (
            Model()
            .add("Mean PR (windows)", mean_pr)
            .add("Std of PR", std_pr)
            .add("Min PR", min_pr)
            .add("Max PR", max_pr)
            .add("Overall PR", overall_pr)
            .add("Is delocalized (PR > 4)", 1.0 if overall_pr > 4 else 0.0)
        )

    def observations(self):
        # NULL: Uniform distribution (PR = 8)
        return (
            Observed()
            .add("Mean PR (windows)", 6.0)
            .add("Std of PR", 1.0)
            .add("Min PR", 3.0)
            .add("Max PR", 8.0)
            .add("Overall PR", 7.0)
            .add("Is delocalized (PR > 4)", 1.0)
        )


class WavePacketSpreadingProbe(Test):
    """
    PROBING: How fast does the trajectory spread to cover all vertices?
    """
    name = "Wave Packet Spreading"
    question = (
        "How quickly does the trajectory 'spread' to visit all vertices? "
        "This is analogous to quantum wave packet spreading. Fast spreading "
        "indicates efficient exploration (diffusive). Slow indicates localization."
    )
    reference = "Wave packet dynamics, diffusion"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We measure the time to first visit all 8 vertices, and "
        "the ongoing spreading rate. This is analogous to how a quantum "
        "wave packet disperses from an initial localized state."
    )

    def derivation(self):
        return (
            Derivation()
            .step("SPREADING TIME:")
            .step("T_spread = steps until all 8 vertices visited")
            .step("EXPECTED FOR RANDOM WALK:")
            .step("Coupon collector problem: E[T] ~ N * ln(N) ~ 17 steps")
            .step("BALLISTIC: T ~ N")
            .step("DIFFUSIVE: T ~ N * ln(N)")
            .step("LOCALIZED: T >> N * ln(N)")
            .conclude("Spreading time reveals exploration efficiency.")
        )

    def model(self):
        n_steps = 500
        history = get_vertex_history(n_steps)
        
        # Compute spreading time
        spreading_time = compute_spreading_time(history)
        
        # Expected for random walk (coupon collector)
        expected_time = 8 * math.log(8)  # ~ 16.6
        
        # Ratio to expected
        ratio = spreading_time / expected_time
        
        # Compute multiple spreading trials
        spreading_times = []
        for offset in range(0, 400, 50):
            if offset + 100 < len(history):
                segment = history[offset:offset+100]
                t = compute_spreading_time(segment)
                if t < 100:  # Only count if spread within window
                    spreading_times.append(t)
        
        mean_spread_time = np.mean(spreading_times) if spreading_times else spreading_time
        
        return (
            Model()
            .add("First spreading time", spreading_time)
            .add("Expected (coupon collector)", expected_time)
            .add("Ratio to expected", ratio)
            .add("Mean spreading time", mean_spread_time)
            .add("Is efficient (ratio < 1.5)", 1.0 if ratio < 1.5 else 0.0)
        )

    def observations(self):
        # NULL: Near-optimal spreading (coupon collector)
        return (
            Observed()
            .add("First spreading time", 17)
            .add("Expected (coupon collector)", 16.6)
            .add("Ratio to expected", 1.0)
            .add("Mean spreading time", 15)
            .add("Is efficient (ratio < 1.5)", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ParticipationRatioProbe,
    WavePacketSpreadingProbe,
]


def run_all():
    """Run all superposition probing tests."""
    summary = (
        "SUPERPOSITION PROBING\n\n"
        "These probes test for quantum-like delocalization.\n"
        "Participation ratio: effective number of states\n"
        "Spreading time: how fast trajectory covers vertices\n\n"
        "We are DISCOVERING superposition-like behavior."
    )
    return run_tests("Superposition Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
