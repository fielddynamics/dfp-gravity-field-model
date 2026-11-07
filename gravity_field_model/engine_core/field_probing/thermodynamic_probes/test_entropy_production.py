"""
Entropy Production Probing
==========================

PROBING QUESTION: Does the field produce entropy (approach equilibrium)?

The second law requires entropy to increase in isolated systems.
Entropy production rate characterizes how far from equilibrium.

MATHEMATICAL FOUNDATION:
- Shannon entropy: S = -sum(p * log(p))
- Entropy production: dS/dt >= 0
- Near equilibrium: dS/dt ~ (distance from equilibrium)^2

NULL HYPOTHESIS: Already at equilibrium (zero production)
DISCOVERY: Positive production indicates non-equilibrium dynamics

Reference: Thermodynamics, entropy production, fluctuation theorems
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


def compute_shannon_entropy(distribution: np.ndarray) -> float:
    """
    Compute Shannon entropy.
    
    S = -sum(p * log(p))
    """
    entropy = 0.0
    for p in distribution:
        if p > 0:
            entropy -= p * math.log(p)
    return entropy


def compute_entropy_time_series(history: List[int], window: int = 50) -> np.ndarray:
    """
    Compute entropy in sliding windows along trajectory.
    """
    n_windows = len(history) - window + 1
    entropies = []
    
    for i in range(n_windows):
        segment = history[i:i+window]
        counts = Counter(segment)
        dist = np.zeros(8)
        for v in range(8):
            dist[v] = counts.get(v, 0) / window
        entropies.append(compute_shannon_entropy(dist))
    
    return np.array(entropies)


def compute_entropy_production_rate(entropies: np.ndarray) -> Dict:
    """
    Compute entropy production rate from time series.
    
    dS/dt = (S(t+dt) - S(t)) / dt
    """
    if len(entropies) < 2:
        return {'rate': 0, 'mean_entropy': 0}
    
    # Compute rate of change
    dS = np.diff(entropies)
    
    mean_rate = np.mean(dS)
    std_rate = np.std(dS)
    
    # Is rate significantly positive?
    n = len(dS)
    t_stat = mean_rate / (std_rate / math.sqrt(n)) if std_rate > 0 else 0
    is_positive = t_stat > 2  # Significantly > 0
    
    return {
        'mean_rate': mean_rate,
        'std_rate': std_rate,
        't_statistic': t_stat,
        'is_positive': is_positive,
        'mean_entropy': np.mean(entropies),
        'final_entropy': entropies[-1],
        'max_entropy': math.log(8),  # Maximum for 8 states
    }


def compute_relative_entropy(p: np.ndarray, q: np.ndarray) -> float:
    """
    Compute KL divergence D(p||q) = sum(p * log(p/q))
    
    Measures how far p is from reference q.
    """
    kl = 0.0
    for i in range(len(p)):
        if p[i] > 0 and q[i] > 0:
            kl += p[i] * math.log(p[i] / q[i])
    return kl


def track_equilibration(history: List[int], window: int = 100) -> Dict:
    """
    Track approach to equilibrium (uniform distribution).
    """
    uniform = np.ones(8) / 8
    n_windows = len(history) // window
    
    kl_divergences = []
    
    for i in range(n_windows):
        segment = history[i*window:(i+1)*window]
        counts = Counter(segment)
        dist = np.zeros(8)
        for v in range(8):
            dist[v] = counts.get(v, 0) / window
        
        kl = compute_relative_entropy(dist, uniform)
        kl_divergences.append(kl)
    
    if not kl_divergences:
        return {'converging': False, 'rate': 0}
    
    # Fit exponential decay: KL(t) ~ exp(-t/tau)
    times = np.arange(len(kl_divergences))
    log_kl = np.log(np.array(kl_divergences) + 0.001)
    
    if len(times) > 3:
        slope, _ = np.polyfit(times, log_kl, 1)
        is_converging = slope < -0.01
        relaxation_rate = -slope
    else:
        is_converging = False
        relaxation_rate = 0
    
    return {
        'initial_kl': kl_divergences[0],
        'final_kl': kl_divergences[-1],
        'is_converging': is_converging,
        'relaxation_rate': relaxation_rate,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class EntropyProductionProbe(Test):
    """
    PROBING: Measure entropy production rate.
    """
    name = "Entropy Production Rate"
    question = (
        "Does the field produce entropy over time? Positive entropy production "
        "indicates non-equilibrium dynamics approaching equilibrium. Zero "
        "production means already at equilibrium or in steady state."
    )
    reference = "Entropy production, second law"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We track Shannon entropy in sliding windows and compute "
        "its rate of change. Positive rate means entropy is increasing "
        "(approaching equilibrium). Negative or zero means steady state."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ENTROPY:")
            .equation("S = -sum(p * log(p))")
            .step("Maximum entropy: S_max = log(8) for uniform distribution")
            .step("ENTROPY PRODUCTION:")
            .equation("dS/dt = rate of entropy change")
            .step("SECOND LAW: dS/dt >= 0 for isolated system")
            .step("Near equilibrium: dS/dt -> 0")
            .conclude("Entropy production measures distance from equilibrium.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute entropy time series
        entropies = compute_entropy_time_series(history, window=50)
        
        # Entropy production
        production = compute_entropy_production_rate(entropies)
        
        # Distance from maximum entropy
        entropy_deficit = production['max_entropy'] - production['mean_entropy']
        
        return (
            Model()
            .add("Mean entropy", production['mean_entropy'])
            .add("Max entropy", production['max_entropy'])
            .add("Entropy deficit", entropy_deficit)
            .add("Production rate", production['mean_rate'])
            .add("Is producing entropy", 1.0 if production['is_positive'] else 0.0)
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
            .add("Mean entropy", 2.00685, abs_tol=0.011)  # random range [1.99744, 2.01528]
            .add("Max entropy", 2.07944154168, abs_tol=2e-09)  # same for all 150 random sequences
            .add("Entropy deficit", 0.0725883, abs_tol=0.011)  # random range [0.0641572, 0.0820031]
            .add("Production rate", -1.97993e-07, abs_tol=4.7e-05)  # random range [-2.89592e-05, 4.02425e-05]
            .add("Is producing entropy", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class EquilibrationProbe(Test):
    """
    PROBING: Is the field approaching equilibrium?
    """
    name = "Equilibration Dynamics"
    question = (
        "Is the distribution approaching uniform (maximum entropy)? "
        "We track the KL divergence from uniform distribution over time. "
        "Decreasing KL indicates equilibration."
    )
    reference = "Approach to equilibrium, relaxation"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: KL divergence D(p||uniform) measures how far the current "
        "distribution is from equilibrium. Exponential decay of KL indicates "
        "relaxation toward equilibrium."
    )

    def derivation(self):
        return (
            Derivation()
            .step("KL DIVERGENCE:")
            .equation("D(p||q) = sum(p * log(p/q))")
            .step("Measures 'distance' from reference distribution q")
            .step("EQUILIBRATION:")
            .step("q = uniform = (1/8, ..., 1/8)")
            .step("D(p||uniform) -> 0 as p -> uniform")
            .step("RELAXATION:")
            .equation("D(t) ~ D_0 * exp(-t/tau)")
            .step("tau = relaxation time")
            .conclude("Decreasing KL indicates equilibration.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Track equilibration
        equilibration = track_equilibration(history, window=100)
        
        # KL reduction ratio
        if equilibration['initial_kl'] > 0:
            kl_ratio = equilibration['final_kl'] / equilibration['initial_kl']
        else:
            kl_ratio = 1.0
        
        return (
            Model()
            .add("Initial KL divergence", equilibration['initial_kl'])
            .add("Final KL divergence", equilibration['final_kl'])
            .add("KL reduction ratio", kl_ratio)
            .add("Relaxation rate", equilibration['relaxation_rate'])
            .add("Is converging", 1.0 if equilibration['is_converging'] else 0.0)
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
            .add("Initial KL divergence", 0.0344074, abs_tol=0.073)  # random range [0.0040088, 0.0974698]
            .add("Final KL divergence", 0.0334087, abs_tol=0.093)  # random range [0.00465938, 0.114177]
            .add("KL reduction ratio", 1.39604, abs_tol=8.8)  # random range [0.0929224, 8.97349]
            .add("Relaxation rate", -0.000206201, abs_tol=0.016)  # random range [-0.0133801, 0.0132217]
            .add("Is converging", 0.0333333, abs_tol=1.2)  # random range [0, 1]
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    EntropyProductionProbe,
    EquilibrationProbe,
]


def run_all():
    """Run all entropy production probing tests."""
    summary = (
        "ENTROPY PRODUCTION PROBING\n\n"
        "These probes test for entropy production.\n"
        "Production rate: dS/dt > 0?\n"
        "Equilibration: KL divergence decreasing?\n\n"
        "We are DISCOVERING thermodynamic behavior."
    )
    return run_tests("Entropy Production Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
