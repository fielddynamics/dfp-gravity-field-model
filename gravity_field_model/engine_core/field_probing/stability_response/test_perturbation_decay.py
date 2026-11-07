"""
Perturbation Decay Probing
==========================

PROBING QUESTION: How fast does the field return to equilibrium after perturbation?

This probe measures relaxation time by tracking how long it takes
for deviations from equilibrium to decay.

MATHEMATICAL FOUNDATION:
- Relaxation: deviation(t) ~ exp(-t/tau)
- Relaxation time tau: characteristic decay timescale
- Fast relaxation: strong restoring force
- Slow relaxation: weak restoring force or near critical point

NULL HYPOTHESIS: Fast relaxation (tau ~ few steps)
DISCOVERY: Long relaxation times indicate interesting dynamics

Reference: Relaxation dynamics, approach to equilibrium
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


def compute_chamber_imbalance(history: List[int], window: int = 10) -> np.ndarray:
    """
    Compute TetA - TetB imbalance in sliding windows.
    
    Returns: array of imbalance values (positive = TetA heavy)
    """
    n = len(history)
    imbalance = []
    
    for i in range(n - window + 1):
        w = history[i:i+window]
        teta_count = sum(1 for v in w if v in TET_A)
        tetb_count = window - teta_count
        imbalance.append(teta_count - tetb_count)
    
    return np.array(imbalance)


def find_extreme_events(imbalance: np.ndarray, threshold: float = 0.8) -> List[int]:
    """
    Find indices where imbalance exceeds threshold (in either direction).
    
    These are "perturbation" events where the system is far from equilibrium.
    """
    max_imbalance = np.max(np.abs(imbalance))
    if max_imbalance == 0:
        return []
    
    normalized = np.abs(imbalance) / max_imbalance
    events = np.where(normalized > threshold)[0]
    
    return list(events)


def measure_relaxation_from_event(imbalance: np.ndarray, event_idx: int, 
                                  max_steps: int = 100) -> Dict:
    """
    Measure how the imbalance decays after an extreme event.
    """
    initial = abs(imbalance[event_idx])
    if initial == 0:
        return {'tau': 0, 'decay_curve': []}
    
    decay_curve = []
    for k in range(max_steps):
        idx = event_idx + k
        if idx >= len(imbalance):
            break
        decay_curve.append(abs(imbalance[idx]) / initial)
    
    # Fit exponential decay: y = exp(-t/tau)
    # log(y) = -t/tau
    if len(decay_curve) >= 5:
        t = np.arange(len(decay_curve))
        y = np.array(decay_curve)
        valid = y > 0.1  # Only fit where signal is above noise
        
        if np.sum(valid) >= 3:
            log_y = np.log(y[valid])
            t_valid = t[valid]
            slope, _ = np.polyfit(t_valid, log_y, 1)
            tau = -1 / slope if slope < 0 else float('inf')
        else:
            tau = float('inf')
    else:
        tau = float('inf')
    
    return {
        'tau': tau,
        'decay_curve': decay_curve,
        'initial_imbalance': initial,
    }


def compute_autocorrelation_time(signal: np.ndarray) -> float:
    """
    Compute integrated autocorrelation time.
    
    tau_int = 1 + 2 * sum_{k=1}^{inf} R(k)
    
    This is another measure of relaxation time.
    """
    n = len(signal)
    mean = np.mean(signal)
    var = np.var(signal)
    
    if var == 0:
        return 0.0
    
    # Compute autocorrelation
    max_lag = min(100, n // 2)
    tau_int = 0.5  # Start with 0.5 (from R(0) = 1, but we count 1 + 2*sum)
    
    for k in range(1, max_lag):
        corr = np.mean((signal[:n-k] - mean) * (signal[k:] - mean)) / var
        if corr < 0.05:  # Cutoff when correlation becomes negligible
            break
        tau_int += corr
    
    return tau_int


# =============================================================================
# TEST CLASSES
# =============================================================================

class RelaxationTimeProbe(Test):
    """
    PROBING: Measure the relaxation time after extreme events.
    """
    name = "Relaxation Time from Perturbations"
    question = (
        "When the system is far from equilibrium (strong TetA or TetB bias), "
        "how quickly does it return to balance? Short relaxation time indicates "
        "strong restoring force. Long time indicates weak coupling or critical behavior."
    )
    reference = "Relaxation dynamics, exponential decay"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We find moments of extreme imbalance and track how the "
        "system relaxes back to equilibrium. Exponential decay with time "
        "constant tau characterizes the relaxation. This reveals the field's "
        "self-correcting dynamics."
    )

    def derivation(self):
        return (
            Derivation()
            .step("RELAXATION DYNAMICS:")
            .step("After perturbation from equilibrium:")
            .equation("deviation(t) ~ exp(-t/tau)")
            .step("tau = relaxation time")
            .step("FITTING:")
            .step("log(deviation) = -t/tau + const")
            .step("Slope gives -1/tau")
            .step("INTERPRETATION:")
            .step("  Short tau: fast self-correction, robust equilibrium")
            .step("  Long tau: slow relaxation, near criticality?")
            .conclude("Relaxation time reveals restoring dynamics.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute imbalance
        window = 20
        imbalance = compute_chamber_imbalance(history, window)
        
        # Find extreme events
        events = find_extreme_events(imbalance, threshold=0.7)
        
        # Measure relaxation from each event
        taus = []
        for event_idx in events[:50]:  # Limit to first 50 events
            result = measure_relaxation_from_event(imbalance, event_idx, max_steps=50)
            if 0 < result['tau'] < 100:
                taus.append(result['tau'])
        
        mean_tau = np.mean(taus) if taus else float('inf')
        std_tau = np.std(taus) if len(taus) > 1 else 0
        
        # Also compute integrated autocorrelation time
        tau_int = compute_autocorrelation_time(imbalance.astype(float))
        
        return (
            Model()
            .add("Number of extreme events", len(events))
            .add("Mean relaxation time tau", mean_tau)
            .add("Std of tau", std_tau)
            .add("Integrated autocorrelation time", tau_int)
            .add("Relaxation events measured", len(taus))
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
            .add("Number of extreme events", 170.267, abs_tol=430)  # random range [14, 539]
            .add("Mean relaxation time tau", 43.2947, abs_tol=26)  # random range [30.256, 65.3168]
            .add("Std of tau", 16.8388, abs_tol=12)  # random range [6.98394, 24.9147]
            .add("Integrated autocorrelation time", 10.0137, abs_tol=4.9)  # random range [9.19738, 14.2417]
            .add("Relaxation events measured", 38.42, abs_tol=29)  # random range [14, 50]
        )

class EquilibriumFluctuationsProbe(Test):
    """
    PROBING: Characterize fluctuations around equilibrium.
    """
    name = "Equilibrium Fluctuation Analysis"
    question = (
        "How large are the fluctuations around the 50/50 equilibrium? "
        "Are they Gaussian (normal) or do they have fat tails (extreme events)? "
        "The fluctuation statistics reveal the nature of equilibrium."
    )
    reference = "Fluctuation theory, central limit theorem"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We analyze the distribution of chamber imbalance. Gaussian "
        "fluctuations suggest normal equilibrium. Fat tails suggest large "
        "deviations are more common than expected. Skewness would indicate "
        "asymmetry between TetA and TetB."
    )

    def derivation(self):
        return (
            Derivation()
            .step("FLUCTUATION STATISTICS:")
            .step("For system in equilibrium with N particles:")
            .equation("Var(imbalance) ~ N (for random)")
            .step("Fluctuation-dissipation: Var related to response")
            .step("DISTRIBUTION SHAPE:")
            .step("  Gaussian: normal fluctuations")
            .step("  Fat tails: large deviations common")
            .step("  Skewed: asymmetric equilibrium")
            .step("KURTOSIS:")
            .equation("kappa = E[(X-mu)^4] / sigma^4 - 3")
            .step("  kappa = 0: Gaussian")
            .step("  kappa > 0: fat tails")
            .conclude("Fluctuation statistics characterize equilibrium.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute imbalance
        window = 20
        imbalance = compute_chamber_imbalance(history, window)
        
        # Basic statistics
        mean_imb = np.mean(imbalance)
        std_imb = np.std(imbalance)
        
        # Skewness: E[(X-mu)^3] / sigma^3
        if std_imb > 0:
            skewness = np.mean(((imbalance - mean_imb) / std_imb) ** 3)
        else:
            skewness = 0
        
        # Kurtosis: E[(X-mu)^4] / sigma^4 - 3
        if std_imb > 0:
            kurtosis = np.mean(((imbalance - mean_imb) / std_imb) ** 4) - 3
        else:
            kurtosis = 0
        
        # Test for Gaussian: Jarque-Bera statistic
        jb_stat = (n_steps / 6) * (skewness**2 + kurtosis**2 / 4)
        is_gaussian = jb_stat < 10  # Rough threshold
        
        return (
            Model()
            .add("Mean imbalance", mean_imb)
            .add("Std of imbalance", std_imb)
            .add("Skewness", skewness)
            .add("Excess kurtosis", kurtosis)
            .add("Is Gaussian", 1.0 if is_gaussian else 0.0)
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
            .add("Mean imbalance", 0.0151526, abs_tol=0.68)  # random range [-0.575636, 0.526949]
            .add("Std of imbalance", 4.45506, abs_tol=0.34)  # random range [4.2134, 4.74563]
            .add("Skewness", 0.00512324, abs_tol=0.25)  # random range [-0.204539, 0.158807]
            .add("Excess kurtosis", -0.0902217, abs_tol=0.45)  # random range [-0.421409, 0.293543]
            .add("Is Gaussian", 0.333333, abs_tol=0.77)  # random range [0, 1]
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    RelaxationTimeProbe,
    EquilibriumFluctuationsProbe,
]


def run_all():
    """Run all perturbation decay probing tests."""
    summary = (
        "PERTURBATION DECAY PROBING\n\n"
        "These probes measure relaxation and fluctuation dynamics.\n"
        "Relaxation time: how fast equilibrium is restored\n"
        "Fluctuations: character of deviations from equilibrium\n\n"
        "We are DISCOVERING the field's stability properties."
    )
    return run_tests("Perturbation Decay Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
