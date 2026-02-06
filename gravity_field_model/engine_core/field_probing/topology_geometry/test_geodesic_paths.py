"""
Geodesic Paths Probing
======================

PROBING QUESTION: Does the traversal follow shortest paths through the Merkaba?

Geodesics are the "straight lines" in a curved space. If the field
dynamics respects geometry, trajectories should tend toward geodesics.

MATHEMATICAL FOUNDATION:
- Geodesic: path that locally minimizes distance
- In discrete space: shortest path on graph
- Deviation from geodesic indicates "force" or "curvature"

NULL HYPOTHESIS: Random walk (no geodesic preference)
DISCOVERY: Geodesic following would indicate geometric structure

Reference: Geodesics, discrete geometry, graph shortest paths
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def get_vertex_coordinates(vertex: int) -> np.ndarray:
    """Get 3D coordinates of a vertex."""
    coords = VERTICES[vertex]['coords']
    return np.array(coords, dtype=float)


def compute_euclidean_distance(v1: int, v2: int) -> float:
    """Compute Euclidean distance between two vertices."""
    r1 = get_vertex_coordinates(v1)
    r2 = get_vertex_coordinates(v2)
    return np.linalg.norm(r1 - r2)


def compute_all_distances() -> np.ndarray:
    """Compute all pairwise distances between vertices."""
    distances = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            distances[i, j] = compute_euclidean_distance(i, j)
    return distances


def compute_path_length(path: List[int]) -> float:
    """Compute total Euclidean length of a path."""
    length = 0.0
    for i in range(len(path) - 1):
        length += compute_euclidean_distance(path[i], path[i+1])
    return length


def compute_geodesic_efficiency(history: List[int], window: int = 10) -> List[float]:
    """
    Compute geodesic efficiency for trajectory segments.
    
    Efficiency = direct_distance / path_length
    
    Efficiency = 1: straight line (geodesic)
    Efficiency < 1: curved path (longer than geodesic)
    """
    efficiencies = []
    
    for i in range(len(history) - window + 1):
        segment = history[i:i+window]
        
        # Direct distance from start to end
        direct = compute_euclidean_distance(segment[0], segment[-1])
        
        # Actual path length
        path_len = compute_path_length(segment)
        
        if path_len > 0:
            efficiency = direct / path_len
        else:
            efficiency = 1.0
        
        efficiencies.append(efficiency)
    
    return efficiencies


def compute_step_optimality(history: List[int]) -> List[float]:
    """
    For each step, compute how optimal it is toward eventual destination.
    
    Optimality = (d_before - d_after) / step_length
    
    Where d = distance to the vertex that will be reached k steps later.
    """
    k = 5  # Look ahead
    optimalities = []
    distances = compute_all_distances()
    
    for i in range(len(history) - k - 1):
        current = history[i]
        next_v = history[i + 1]
        target = history[i + k]
        
        d_before = distances[current, target]
        d_after = distances[next_v, target]
        step_len = distances[current, next_v]
        
        if step_len > 0:
            # Optimality: how much closer did we get relative to step size?
            optimality = (d_before - d_after) / step_len
        else:
            optimality = 0.0
        
        optimalities.append(optimality)
    
    return optimalities


# =============================================================================
# TEST CLASSES
# =============================================================================

class GeodesicEfficiencyProbe(Test):
    """
    PROBING: Does the trajectory follow geodesics (shortest paths)?
    """
    name = "Geodesic Efficiency Analysis"
    question = (
        "How efficient is the trajectory in terms of distance traveled? "
        "Efficiency = direct_distance / path_length. High efficiency means "
        "the path is close to a geodesic. Low efficiency means meandering."
    )
    reference = "Geodesics, path efficiency"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We measure how 'straight' the trajectory is by comparing "
        "direct distance to actual path length. Random walks have low "
        "efficiency. Geodesic-following dynamics would show high efficiency."
    )

    def derivation(self):
        return (
            Derivation()
            .step("GEODESIC EFFICIENCY:")
            .equation("E = |r(end) - r(start)| / path_length")
            .step("Range: (0, 1]")
            .step("  E = 1: straight line (perfect geodesic)")
            .step("  E << 1: wandering path")
            .step("FOR RANDOM WALK:")
            .step("Expected efficiency scales as 1/sqrt(n) for n steps")
            .step("(due to diffusive spreading)")
            .conclude("Efficiency measures geodesic following.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute efficiencies for different window sizes
        eff_5 = compute_geodesic_efficiency(history, window=5)
        eff_10 = compute_geodesic_efficiency(history, window=10)
        eff_20 = compute_geodesic_efficiency(history, window=20)
        
        mean_eff_5 = np.mean(eff_5)
        mean_eff_10 = np.mean(eff_10)
        mean_eff_20 = np.mean(eff_20)
        
        # Expected for random walk: ~1/sqrt(n)
        expected_eff_5 = 1 / math.sqrt(5)
        expected_eff_10 = 1 / math.sqrt(10)
        expected_eff_20 = 1 / math.sqrt(20)
        
        # Ratio to expected
        ratio_5 = mean_eff_5 / expected_eff_5
        ratio_10 = mean_eff_10 / expected_eff_10
        
        return (
            Model()
            .add("Mean efficiency (5 steps)", mean_eff_5)
            .add("Mean efficiency (10 steps)", mean_eff_10)
            .add("Mean efficiency (20 steps)", mean_eff_20)
            .add("Ratio to random (5 steps)", ratio_5)
            .add("Ratio to random (10 steps)", ratio_10)
            .add("Is geodesic-like", 1.0 if ratio_10 > 1.5 else 0.0)
        )

    def observations(self):
        # NULL: Random walk efficiency
        return (
            Observed()
            .add("Mean efficiency (5 steps)", 0.45)  # ~1/sqrt(5)
            .add("Mean efficiency (10 steps)", 0.32)  # ~1/sqrt(10)
            .add("Mean efficiency (20 steps)", 0.22)  # ~1/sqrt(20)
            .add("Ratio to random (5 steps)", 1.0)
            .add("Ratio to random (10 steps)", 1.0)
            .add("Is geodesic-like", 0.0)
        )


class StepOptimalityProbe(Test):
    """
    PROBING: Are individual steps locally optimal toward eventual destination?
    """
    name = "Step Optimality Analysis"
    question = (
        "When the trajectory takes a step, does it tend to move closer to "
        "where it will eventually go? Positive optimality means steps are "
        "directionally coherent. Zero/negative means no directional intent."
    )
    reference = "Local optimization, gradient descent"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We measure whether each step reduces the distance to the "
        "eventual destination. This would indicate the dynamics has a sense "
        "of 'direction' or 'goal'. Random dynamics would show zero net optimality."
    )

    def derivation(self):
        return (
            Derivation()
            .step("STEP OPTIMALITY:")
            .step("For step from v_t to v_{t+1}, targeting v_{t+k}:")
            .equation("O = (d(v_t, v_{t+k}) - d(v_{t+1}, v_{t+k})) / d(v_t, v_{t+1})")
            .step("  O > 0: step moves toward target")
            .step("  O = 0: step is tangent to target")
            .step("  O < 0: step moves away from target")
            .step("FOR RANDOM WALK:")
            .step("Expected optimality = 0 (no directional bias)")
            .conclude("Optimality measures directional coherence.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute step optimality
        optimalities = compute_step_optimality(history)
        
        mean_opt = np.mean(optimalities)
        std_opt = np.std(optimalities)
        
        # Fraction of positive (toward target) steps
        frac_positive = np.mean(np.array(optimalities) > 0)
        
        # t-test for mean != 0
        n = len(optimalities)
        t_stat = mean_opt / (std_opt / math.sqrt(n)) if std_opt > 0 else 0
        
        return (
            Model()
            .add("Mean step optimality", mean_opt)
            .add("Std of optimality", std_opt)
            .add("Fraction positive", frac_positive)
            .add("t-statistic", t_stat)
            .add("Has directional intent", 1.0 if t_stat > 2 else 0.0)
        )

    def observations(self):
        # NULL: Random (zero optimality)
        return (
            Observed()
            .add("Mean step optimality", 0.0)
            .add("Std of optimality", 0.5)
            .add("Fraction positive", 0.5)
            .add("t-statistic", 0.0)
            .add("Has directional intent", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    GeodesicEfficiencyProbe,
    StepOptimalityProbe,
]


def run_all():
    """Run all geodesic paths probing tests."""
    summary = (
        "GEODESIC PATHS PROBING\n\n"
        "These probes test if the trajectory follows shortest paths.\n"
        "Efficiency: direct distance / path length\n"
        "Optimality: do steps reduce distance to destination?\n\n"
        "We are DISCOVERING geodesic structure."
    )
    return run_tests("Geodesic Paths Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
