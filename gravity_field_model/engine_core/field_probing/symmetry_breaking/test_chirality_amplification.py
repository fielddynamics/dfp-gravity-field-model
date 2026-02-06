"""
Chirality Amplification Probing
===============================

PROBING QUESTION: Does the ~1% TetB bias grow, shrink, or stay constant over time?

We found a slight bias toward TetB. This probe tests whether this
asymmetry amplifies (grows) or is a fixed statistical fluctuation.

MATHEMATICAL FOUNDATION:
- Chirality: C = (N_B - N_A) / N
- Amplification: C(t) ~ t^alpha or C(t) ~ C_0 * exp(gamma * t)
- alpha > 0: growing asymmetry
- alpha = 0: constant asymmetry
- alpha < 0: shrinking asymmetry

NULL HYPOTHESIS: Constant chirality (alpha = 0)
DISCOVERY: Growing chirality would indicate instability

Reference: Symmetry breaking, chirality in physics
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


def compute_cumulative_chirality(history: List[int]) -> np.ndarray:
    """
    Compute cumulative chirality as function of trajectory length.
    
    C(t) = (N_B(t) - N_A(t)) / t
    """
    n = len(history)
    n_a = 0
    n_b = 0
    chirality = []
    
    for i, v in enumerate(history):
        if v in TET_A:
            n_a += 1
        else:
            n_b += 1
        chirality.append((n_b - n_a) / (i + 1))
    
    return np.array(chirality)


def compute_windowed_chirality(history: List[int], windows: List[int]) -> Dict:
    """
    Compute chirality for different window sizes.
    
    If chirality amplifies, it should be larger for longer windows.
    """
    results = {}
    
    for w in windows:
        n_windows = len(history) // w
        chiralities = []
        
        for i in range(n_windows):
            segment = history[i*w:(i+1)*w]
            n_a = sum(1 for v in segment if v in TET_A)
            n_b = w - n_a
            chiralities.append((n_b - n_a) / w)
        
        results[w] = {
            'mean': np.mean(chiralities),
            'std': np.std(chiralities),
            'max': np.max(np.abs(chiralities)),
        }
    
    return results


def fit_amplification_model(chirality: np.ndarray) -> Dict:
    """
    Fit models for chirality amplification.
    
    Model 1: C(t) = C_inf + a/sqrt(t) (statistical settling)
    Model 2: C(t) = C_0 * t^alpha (power law growth)
    Model 3: C(t) = C_0 * exp(gamma * t) (exponential growth)
    """
    n = len(chirality)
    t = np.arange(1, n + 1)
    
    # Model 1: 1/sqrt(t) settling to constant
    # C = C_inf + a/sqrt(t)
    # Linear fit: C * sqrt(t) = C_inf * sqrt(t) + a
    sqrt_t = np.sqrt(t[100:])  # Skip transient
    C_sqrt_t = chirality[100:] * sqrt_t
    if len(sqrt_t) > 10:
        slope1, intercept1 = np.polyfit(sqrt_t, C_sqrt_t, 1)
        C_inf = slope1
        settling_coeff = intercept1
    else:
        C_inf = np.mean(chirality[100:])
        settling_coeff = 0
    
    # Model 2: Power law
    # log|C| = alpha * log(t) + const
    valid = np.abs(chirality[100:]) > 0.001
    if np.sum(valid) > 10:
        log_t = np.log(t[100:][valid])
        log_C = np.log(np.abs(chirality[100:][valid]))
        alpha, _ = np.polyfit(log_t, log_C, 1)
    else:
        alpha = 0.0
    
    return {
        'C_infinity': C_inf,
        'settling_coefficient': settling_coeff,
        'power_law_alpha': alpha,
        'is_constant': abs(alpha) < 0.1,
        'is_growing': alpha > 0.1,
        'is_shrinking': alpha < -0.1,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class ChiralityEvolutionProbe(Test):
    """
    PROBING: Track chirality evolution over time.
    """
    name = "Chirality Evolution Analysis"
    question = (
        "We found ~1% TetB bias. Is this bias constant, or does it grow/shrink "
        "as the trajectory gets longer? Growing chirality would indicate the "
        "symmetry is unstable and naturally breaks further."
    )
    reference = "Symmetry breaking, chiral amplification"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We track the cumulative chirality C(t) = (N_B - N_A) / t "
        "over the trajectory. If C converges to a constant, the bias is "
        "fixed. If C grows with t, the symmetry is actively breaking. "
        "If C shrinks, the system self-corrects toward symmetry."
    )

    def derivation(self):
        return (
            Derivation()
            .step("CHIRALITY:")
            .equation("C(t) = (N_B(t) - N_A(t)) / t")
            .step("EVOLUTION MODELS:")
            .step("1. Statistical settling: C(t) = C_inf + a/sqrt(t)")
            .step("   (Central limit theorem: fluctuations ~ 1/sqrt(N))")
            .step("2. Power law growth: C(t) ~ t^alpha")
            .step("3. Exponential amplification: C(t) ~ exp(gamma*t)")
            .step("FIT: Determine which model best describes the data.")
            .conclude("Chirality evolution reveals symmetry stability.")
        )

    def model(self):
        n_steps = 8000
        history = get_vertex_history(n_steps)
        
        # Compute cumulative chirality
        chirality = compute_cumulative_chirality(history)
        
        # Fit amplification model
        fit = fit_amplification_model(chirality)
        
        # Chirality at different points
        c_1000 = chirality[999]
        c_5000 = chirality[4999]
        c_8000 = chirality[-1]
        
        return (
            Model()
            .add("C at 1000 steps", c_1000)
            .add("C at 5000 steps", c_5000)
            .add("C at 8000 steps", c_8000)
            .add("Asymptotic C_infinity", fit['C_infinity'])
            .add("Power law alpha", fit['power_law_alpha'])
            .add("Is constant", 1.0 if fit['is_constant'] else 0.0)
        )

    def observations(self):
        # NULL: Constant chirality (statistical fluctuation only)
        return (
            Observed()
            .add("C at 1000 steps", 0.01)
            .add("C at 5000 steps", 0.01)
            .add("C at 8000 steps", 0.01)
            .add("Asymptotic C_infinity", 0.01)
            .add("Power law alpha", 0.0)
            .add("Is constant", 1.0)
        )


class WindowedChiralityProbe(Test):
    """
    PROBING: Check if chirality depends on measurement window.
    """
    name = "Window-Dependent Chirality"
    question = (
        "Is the chirality bias independent of how we measure it? If the bias "
        "is larger for longer windows, it indicates amplification. If smaller, "
        "it indicates averaging/cancellation."
    )
    reference = "Scale-dependent asymmetry, averaging"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We measure chirality in windows of different sizes. "
        "If chirality is a fixed bias, mean chirality should be constant. "
        "If it depends on window size, there may be scale-dependent dynamics."
    )

    def derivation(self):
        return (
            Derivation()
            .step("WINDOWED CHIRALITY:")
            .step("For window size w, compute C in non-overlapping windows.")
            .step("mean(C_w) = average chirality at scale w")
            .step("std(C_w) = fluctuation at scale w")
            .step("SCALING:")
            .step("For random: std(C_w) ~ 1/sqrt(w) (CLT)")
            .step("For amplifying: mean(C_w) increases with w")
            .step("For constant: mean(C_w) independent of w")
            .conclude("Window dependence reveals scale structure.")
        )

    def model(self):
        n_steps = 8000
        history = get_vertex_history(n_steps)
        
        # Compute chirality for different windows
        windows = [100, 500, 1000, 4000]
        results = compute_windowed_chirality(history, windows)
        
        # Check if mean increases with window size
        means = [results[w]['mean'] for w in windows]
        stds = [results[w]['std'] for w in windows]
        
        # Test for window dependence
        # Fit mean vs log(w)
        log_w = np.log(windows)
        slope, intercept = np.polyfit(log_w, means, 1)
        
        # Check if stds follow 1/sqrt(w)
        expected_std_ratio = math.sqrt(windows[0] / windows[-1])
        actual_std_ratio = stds[0] / stds[-1] if stds[-1] > 0 else 1.0
        
        return (
            Model()
            .add("Mean C (w=100)", results[100]['mean'])
            .add("Mean C (w=1000)", results[1000]['mean'])
            .add("Mean C (w=4000)", results[4000]['mean'])
            .add("Window dependence slope", slope)
            .add("Std ratio (actual)", actual_std_ratio)
            .add("Std ratio (expected CLT)", expected_std_ratio)
        )

    def observations(self):
        # NULL: Window-independent (constant bias)
        return (
            Observed()
            .add("Mean C (w=100)", 0.01)
            .add("Mean C (w=1000)", 0.01)
            .add("Mean C (w=4000)", 0.01)
            .add("Window dependence slope", 0.0)
            .add("Std ratio (actual)", 7.0)  # sqrt(5000/100)
            .add("Std ratio (expected CLT)", 7.07)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ChiralityEvolutionProbe,
    WindowedChiralityProbe,
]


def run_all():
    """Run all chirality amplification probing tests."""
    summary = (
        "CHIRALITY AMPLIFICATION PROBING\n\n"
        "These probes test if the ~1% TetB bias grows or stays constant.\n"
        "Evolution: how does C(t) change with trajectory length?\n"
        "Windows: does bias depend on measurement scale?\n\n"
        "We are DISCOVERING the stability of the asymmetry."
    )
    return run_tests("Chirality Amplification Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
