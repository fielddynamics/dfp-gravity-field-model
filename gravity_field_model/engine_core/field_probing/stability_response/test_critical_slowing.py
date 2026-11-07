"""
Critical Slowing Down Probing
=============================

PROBING QUESTION: Are there signatures of critical behavior (phase transitions)?

This probe looks for critical slowing down: diverging relaxation times
that occur near phase transitions.

MATHEMATICAL FOUNDATION:
- Near critical point: tau ~ |T - Tc|^(-nu)
- Relaxation time diverges as criticality is approached
- Fluctuations also diverge (critical opalescence)

NULL HYPOTHESIS: No critical behavior (bounded relaxation time)
DISCOVERY: Diverging tau would indicate phase transition

Reference: Critical phenomena, phase transitions
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


def compute_order_parameter(history: List[int], window: int = 50) -> np.ndarray:
    """
    Compute order parameter: magnetization-like quantity.
    
    m = (N_A - N_B) / (N_A + N_B)
    
    m = +1: all TetA
    m = -1: all TetB
    m = 0: balanced
    """
    n = len(history)
    order_param = []
    
    for i in range(n - window + 1):
        w = history[i:i+window]
        n_a = sum(1 for v in w if v in TET_A)
        n_b = window - n_a
        m = (n_a - n_b) / window
        order_param.append(m)
    
    return np.array(order_param)


def compute_susceptibility(order_param: np.ndarray) -> float:
    """
    Compute susceptibility: variance of order parameter.
    
    chi = Var(m) * N
    
    Susceptibility diverges at critical point.
    """
    return np.var(order_param) * len(order_param)


def compute_correlation_length(history: List[int]) -> float:
    """
    Estimate spatial correlation length.
    
    For discrete system: number of correlated neighbors.
    """
    n = len(history)
    
    # Compute vertex-vertex correlation
    chamber = np.array([1 if v in TET_A else -1 for v in history])
    
    # Correlation at different lags
    max_lag = 50
    correlations = []
    
    for lag in range(1, max_lag + 1):
        corr = np.mean(chamber[:-lag] * chamber[lag:])
        correlations.append(abs(corr))
    
    # Find correlation length (where correlation drops to 1/e)
    correlations = np.array(correlations)
    threshold = correlations[0] / math.e if correlations[0] > 0 else 0.1
    
    for i, c in enumerate(correlations):
        if c < threshold:
            return i + 1
    
    return max_lag


def compute_binder_cumulant(order_param: np.ndarray) -> float:
    """
    Compute Binder cumulant: U = 1 - <m^4> / (3 * <m^2>^2)
    
    U = 0 for Gaussian distribution
    U = 2/3 for ordered phase
    Universal value at critical point
    """
    m2 = np.mean(order_param ** 2)
    m4 = np.mean(order_param ** 4)
    
    if m2 == 0:
        return 0.0
    
    return 1 - m4 / (3 * m2 ** 2)


def analyze_scaling(history: List[int], windows: List[int]) -> Dict:
    """
    Analyze finite-size scaling behavior.
    
    At criticality, susceptibility scales as chi ~ L^(gamma/nu)
    """
    susceptibilities = []
    binders = []
    
    for w in windows:
        order = compute_order_parameter(history, window=w)
        chi = compute_susceptibility(order)
        u = compute_binder_cumulant(order)
        susceptibilities.append(chi)
        binders.append(u)
    
    # Fit power law: chi ~ w^alpha
    log_w = np.log(windows)
    log_chi = np.log(np.array(susceptibilities) + 0.01)
    
    if len(log_w) >= 3:
        alpha, _ = np.polyfit(log_w, log_chi, 1)
    else:
        alpha = 0.0
    
    return {
        'susceptibilities': susceptibilities,
        'binders': binders,
        'scaling_exponent': alpha,
        'windows': windows,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class CriticalFluctuationsProbe(Test):
    """
    PROBING: Look for enhanced fluctuations indicating criticality.
    """
    name = "Critical Fluctuation Analysis"
    question = (
        "Are the fluctuations in the TetA/TetB balance anomalously large? "
        "Near a critical point, fluctuations diverge. We measure susceptibility "
        "(variance of order parameter) and look for signs of criticality."
    )
    reference = "Critical phenomena, susceptibility"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: Susceptibility chi = Var(m) * N measures how strongly the "
        "system responds to perturbations. Large chi suggests the system is "
        "near criticality (phase transition). We also compute the Binder "
        "cumulant which has universal value at critical point."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ORDER PARAMETER (magnetization):")
            .equation("m = (N_A - N_B) / N")
            .step("SUSCEPTIBILITY:")
            .equation("chi = Var(m) * N")
            .step("At criticality, chi diverges: chi ~ |T-Tc|^(-gamma)")
            .step("BINDER CUMULANT:")
            .equation("U = 1 - <m^4> / (3 * <m^2>^2)")
            .step("U = 0 (Gaussian), U = 2/3 (ordered)")
            .step("Universal value at critical point")
            .conclude("Susceptibility and Binder cumulant probe criticality.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute order parameter
        window = 100
        order = compute_order_parameter(history, window)
        
        # Susceptibility
        chi = compute_susceptibility(order)
        
        # Binder cumulant
        u = compute_binder_cumulant(order)
        
        # Correlation length
        xi = compute_correlation_length(history)
        
        # Mean and variance of order parameter
        mean_m = np.mean(order)
        var_m = np.var(order)
        
        return (
            Model()
            .add("Mean order parameter", mean_m)
            .add("Variance of order parameter", var_m)
            .add("Susceptibility chi", chi)
            .add("Binder cumulant U", u)
            .add("Correlation length xi", xi)
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
            .add("Mean order parameter", 0.00075547, abs_tol=0.033)  # random range [-0.0278732, 0.0254575]
            .add("Variance of order parameter", 0.00981775, abs_tol=0.0046)  # random range [0.00742515, 0.0138071]
            .add("Susceptibility chi", 97.2154, abs_tol=46)  # random range [73.5239, 136.718]
            .add("Binder cumulant U", 0.0150028, abs_tol=0.52)  # random range [-0.430829, 0.225979]
            .add("Correlation length xi", 9.62, abs_tol=47)  # random range [1, 50]
        )

class FiniteSizeScalingProbe(Test):
    """
    PROBING: Test for finite-size scaling (critical behavior).
    """
    name = "Finite-Size Scaling Analysis"
    question = (
        "Does the susceptibility scale with system size in a power-law way? "
        "At criticality, chi ~ L^(gamma/nu). We vary the window size and "
        "look for power-law scaling."
    )
    reference = "Finite-size scaling, critical exponents"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: Finite-size scaling is a hallmark of critical systems. "
        "By varying the 'system size' (window length), we can detect if the "
        "field is at or near a critical point. Power-law scaling of "
        "susceptibility with window size would be significant."
    )

    def derivation(self):
        return (
            Derivation()
            .step("FINITE-SIZE SCALING:")
            .step("At criticality, thermodynamic quantities scale with system size L:")
            .equation("chi ~ L^(gamma/nu)")
            .equation("xi ~ L (correlation length)")
            .step("TEST: Vary window size w and fit")
            .equation("log(chi) = alpha * log(w) + const")
            .step("If alpha != 0, there is non-trivial scaling.")
            .step("alpha > 0 suggests approach to criticality.")
            .conclude("Finite-size scaling reveals critical behavior.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Analyze scaling for different window sizes
        windows = [20, 40, 80, 160, 320]
        scaling = analyze_scaling(history, windows)
        
        # Check if Binder cumulants converge (criticality signature)
        binder_var = np.var(scaling['binders'])
        
        # Scaling exponent
        alpha = scaling['scaling_exponent']
        
        # Is scaling non-trivial?
        is_critical = abs(alpha - 1.0) < 0.3  # Near alpha=1 suggests mean-field
        
        return (
            Model()
            .add("Scaling exponent alpha", alpha)
            .add("Chi at w=20", scaling['susceptibilities'][0])
            .add("Chi at w=320", scaling['susceptibilities'][-1])
            .add("Binder variance", binder_var)
            .add("Is near criticality", 1.0 if is_critical else 0.0)
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
            .add("Scaling exponent alpha", -1.03466, abs_tol=0.24)  # random range [-1.23892, -0.856515]
            .add("Chi at w=20", 495.538, abs_tol=77)  # random range [443.02, 562.012]
            .add("Chi at w=320", 28.6311, abs_tol=22)  # random range [15.7018, 47.2111]
            .add("Binder variance", 0.00629324, abs_tol=0.098)  # random range [0.000107431, 0.0910153]
            .add("Is near criticality", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    CriticalFluctuationsProbe,
    FiniteSizeScalingProbe,
]


def run_all():
    """Run all critical slowing probing tests."""
    summary = (
        "CRITICAL SLOWING DOWN PROBING\n\n"
        "These probes look for phase transition signatures.\n"
        "Susceptibility: response to perturbations\n"
        "Finite-size scaling: power-law dependence on size\n\n"
        "We are DISCOVERING if the field is near criticality."
    )
    return run_tests("Critical Slowing Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
