"""
Lyapunov Sensitivity Probing
============================

PROBING QUESTION: Is the dynamics chaotic or regular? How sensitive to initial conditions?

This probe estimates Lyapunov exponents to characterize the nature
of the dynamics (chaotic vs. regular).

MATHEMATICAL FOUNDATION:
- Lyapunov exponent: lambda = lim_{t->inf} (1/t) * log(|delta(t)|/|delta(0)|)
- lambda > 0: chaotic (exponential divergence)
- lambda = 0: marginal (power-law divergence)
- lambda < 0: stable (convergence)

NULL HYPOTHESIS: Regular dynamics (non-chaotic)
DISCOVERY: Positive Lyapunov would indicate chaos

Reference: Chaos theory, dynamical systems
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


def get_vertex_history(n_steps: int, offset: int = 0) -> List[int]:
    """
    Extract vertex sequence from traversal, with optional offset.
    
    Different offsets give "different initial conditions" in the pi sequence.
    """
    traversal = traverse_pi_base8(n_steps + offset, include_integer=True)
    return [step['vertex'] for step in traversal[offset:]]


def get_vertex_coordinates(vertex: int) -> np.ndarray:
    """Get 3D coordinates of a vertex."""
    coords = VERTICES[vertex]['coords']
    return np.array(coords, dtype=float)


def compute_trajectory_distance(traj1: List[int], traj2: List[int]) -> np.ndarray:
    """
    Compute distance between two trajectories at each time step.
    
    Distance = Euclidean distance in vertex coordinate space.
    """
    n = min(len(traj1), len(traj2))
    distances = np.zeros(n)
    
    for t in range(n):
        r1 = get_vertex_coordinates(traj1[t])
        r2 = get_vertex_coordinates(traj2[t])
        distances[t] = np.linalg.norm(r1 - r2)
    
    return distances


def compute_hamming_distance(traj1: List[int], traj2: List[int]) -> np.ndarray:
    """
    Compute Hamming distance (fraction of different vertices) in windows.
    """
    n = min(len(traj1), len(traj2))
    window = 10
    distances = []
    
    for i in range(n - window + 1):
        w1 = traj1[i:i+window]
        w2 = traj2[i:i+window]
        diff = sum(1 for a, b in zip(w1, w2) if a != b)
        distances.append(diff / window)
    
    return np.array(distances)


def estimate_lyapunov_exponent(distances: np.ndarray) -> float:
    """
    Estimate Lyapunov exponent from trajectory divergence.
    
    lambda = lim (1/t) * log(d(t)/d(0))
    
    Fit log(d(t)) = lambda * t + const
    """
    # Filter out zeros and initial transient
    start_idx = 5
    valid = distances[start_idx:] > 0.01
    
    if np.sum(valid) < 10:
        return 0.0
    
    t = np.arange(start_idx, len(distances))[valid[:len(distances)-start_idx]]
    log_d = np.log(distances[start_idx:][valid[:len(distances)-start_idx]])
    
    # Linear fit
    if len(t) >= 5:
        slope, _ = np.polyfit(t, log_d, 1)
        return slope
    
    return 0.0


def compute_divergence_rate(history: List[int], num_pairs: int = 20) -> Dict:
    """
    Compute divergence rate by comparing trajectories with different offsets.
    """
    base_length = len(history)
    offsets = list(range(1, num_pairs + 1))
    
    lyapunov_estimates = []
    
    for offset in offsets:
        # Get trajectory with different "initial condition" (offset in pi)
        traj2 = get_vertex_history(base_length, offset=offset * 100)
        
        # Compute distances
        distances = compute_trajectory_distance(history, traj2)
        
        # Estimate Lyapunov
        lam = estimate_lyapunov_exponent(distances)
        lyapunov_estimates.append(lam)
    
    mean_lyapunov = np.mean(lyapunov_estimates)
    std_lyapunov = np.std(lyapunov_estimates)
    
    return {
        'mean_lyapunov': mean_lyapunov,
        'std_lyapunov': std_lyapunov,
        'estimates': lyapunov_estimates,
        'is_chaotic': mean_lyapunov > 0.1,
        'is_stable': mean_lyapunov < -0.1,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class LyapunovExponentProbe(Test):
    """
    PROBING: Estimate the Lyapunov exponent of the dynamics.
    """
    name = "Lyapunov Exponent Estimation"
    question = (
        "Is the field dynamics chaotic? The Lyapunov exponent measures how fast "
        "nearby trajectories diverge. Positive lambda means chaos: small changes "
        "in initial conditions lead to exponentially different outcomes."
    )
    reference = "Chaos theory, Lyapunov exponents"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We compare trajectories starting from different points in "
        "the pi sequence and measure their divergence. Exponential growth of "
        "distance indicates chaos. Note: the pi-base-8 traversal is deterministic, "
        "so we're probing EFFECTIVE chaos in the digit structure."
    )

    def derivation(self):
        return (
            Derivation()
            .step("LYAPUNOV EXPONENT:")
            .equation("lambda = lim_{t->inf} (1/t) * log(|delta(t)|/|delta(0)|)")
            .step("where delta(t) = distance between nearby trajectories at time t")
            .step("INTERPRETATION:")
            .step("  lambda > 0: chaotic (exponential divergence)")
            .step("  lambda = 0: marginal (power-law)")
            .step("  lambda < 0: stable (convergence)")
            .step("ESTIMATION:")
            .step("Fit log(d(t)) = lambda * t + const")
            .step("Slope gives lambda")
            .conclude("Lyapunov exponent characterizes chaos/stability.")
        )

    def model(self):
        n_steps = 2000
        history = get_vertex_history(n_steps)
        
        # Compute divergence statistics
        divergence = compute_divergence_rate(history, num_pairs=15)
        
        # Characterize dynamics
        if divergence['mean_lyapunov'] > 0.1:
            dynamics_type = "chaotic"
        elif divergence['mean_lyapunov'] < -0.1:
            dynamics_type = "stable"
        else:
            dynamics_type = "marginal"
        
        return (
            Model()
            .add("Mean Lyapunov exponent", divergence['mean_lyapunov'])
            .add("Std of Lyapunov", divergence['std_lyapunov'])
            .add("Is chaotic", 1.0 if divergence['is_chaotic'] else 0.0)
            .add("Is stable", 1.0 if divergence['is_stable'] else 0.0)
        )

    def observations(self) -> Observed:
        # Random-digit baseline. Each expected value is the mean of the metric
        # over 150 uniformly random base-8 digit sequences of the same length
        # as the pi digits (seeds 5000-5149), and the absolute tolerance is
        # 1.15 times the largest distance from that mean to the most extreme
        # of the 150 values. A pass means pi is indistinguishable from random
        # digits on this metric; a fail would be a property of pi itself.
        # Metrics marked 'same for all random sequences' are fixed by the
        # traversal rule for any generic sequence (degenerate sequences such
        # as all zeros change them). The previous expected values were
        # unsourced guesses.
        return (
            Observed()
            .add("Mean Lyapunov exponent", -4.07316e-08, abs_tol=5.9e-06)  # random range [-5.14698e-06, 4.61748e-06]
            .add("Std of Lyapunov", 8.1841e-06, abs_tol=5.9e-06)  # random range [3.05954e-06, 1.17072e-05]
            .add("Is chaotic", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Is stable", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class PredictabilityHorizonProbe(Test):
    """
    PROBING: How far into the future can we predict?
    """
    name = "Predictability Horizon"
    question = (
        "Given the current state, how many steps into the future can we "
        "reliably predict? The predictability horizon is where forecast skill "
        "drops to random chance level."
    )
    reference = "Predictability, forecast skill"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We measure how prediction accuracy decays with forecast "
        "lead time. The horizon where accuracy hits 50% (random for 2 chambers) "
        "is the predictability limit. Long horizon = ordered dynamics. "
        "Short horizon = unpredictable dynamics."
    )

    def derivation(self):
        return (
            Derivation()
            .step("PREDICTABILITY HORIZON:")
            .step("Given state at time t, predict state at t+k")
            .step("Accuracy(k) = P(correct prediction at lead time k)")
            .step("For random: Accuracy = 0.5 (two chambers)")
            .step("HORIZON:")
            .step("k* = smallest k where Accuracy(k) <= 0.55")
            .step("Beyond k*, predictions are essentially random.")
            .step("CHAOS SIGNATURE:")
            .step("Accuracy decays exponentially: Acc(k) ~ exp(-k/tau)")
            .step("tau related to Lyapunov exponent")
            .conclude("Predictability horizon measures forecast limit.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute chamber sequence
        chambers = [0 if v in TET_A else 1 for v in history]
        
        # Compute accuracy at different lead times
        max_lead = 50
        accuracies = []
        
        for lead in range(1, max_lead + 1):
            correct = 0
            total = 0
            
            for t in range(len(chambers) - lead):
                # Simple predictor: same as current
                prediction = chambers[t]
                actual = chambers[t + lead]
                if prediction == actual:
                    correct += 1
                total += 1
            
            accuracies.append(correct / total if total > 0 else 0.5)
        
        accuracies = np.array(accuracies)
        
        # Find horizon (where accuracy drops to ~0.55)
        horizon = max_lead
        for k, acc in enumerate(accuracies):
            if acc < 0.55:
                horizon = k + 1
                break
        
        # Fit exponential decay
        leads = np.arange(1, len(accuracies) + 1)
        valid = accuracies > 0.51
        if np.sum(valid) >= 5:
            log_acc_excess = np.log(accuracies[valid] - 0.5 + 0.001)
            slope, _ = np.polyfit(leads[valid], log_acc_excess, 1)
            decay_rate = -slope
        else:
            decay_rate = 0.0
        
        return (
            Model()
            .add("Accuracy at lead 1", accuracies[0])
            .add("Accuracy at lead 5", accuracies[4])
            .add("Accuracy at lead 10", accuracies[9])
            .add("Predictability horizon", horizon)
            .add("Decay rate", decay_rate)
        )

    def observations(self) -> Observed:
        # Random-digit baseline. Each expected value is the mean of the metric
        # over 150 uniformly random base-8 digit sequences of the same length
        # as the pi digits (seeds 5000-5149), and the absolute tolerance is
        # 1.15 times the largest distance from that mean to the most extreme
        # of the 150 values. A pass means pi is indistinguishable from random
        # digits on this metric; a fail would be a property of pi itself.
        # Metrics marked 'same for all random sequences' are fixed by the
        # traversal rule for any generic sequence (degenerate sequences such
        # as all zeros change them). The previous expected values were
        # unsourced guesses.
        return (
            Observed()
            .add("Accuracy at lead 1", 0.499521, abs_tol=0.022)  # random range [0.4804, 0.5166]
            .add("Accuracy at lead 5", 0.499362, abs_tol=0.023)  # random range [0.479984, 0.517614]
            .add("Accuracy at lead 10", 0.49848, abs_tol=0.025)  # random range [0.476858, 0.518133]
            .add("Predictability horizon", 1, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Decay rate", 0.000421686, abs_tol=0.021)  # random range [-0.017204, 0.0156436]
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    LyapunovExponentProbe,
    PredictabilityHorizonProbe,
]


def run_all():
    """Run all Lyapunov sensitivity probing tests."""
    summary = (
        "LYAPUNOV SENSITIVITY PROBING\n\n"
        "These probes test for chaos and predictability.\n"
        "Lyapunov exponent: divergence rate of nearby trajectories\n"
        "Predictability horizon: how far can we forecast?\n\n"
        "We are DISCOVERING the nature of the dynamics."
    )
    return run_tests("Lyapunov Sensitivity Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
