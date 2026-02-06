"""
Spontaneous Symmetry Breaking Probing
=====================================

PROBING QUESTION: Does the TetA/TetB symmetry break spontaneously?

Spontaneous symmetry breaking occurs when the dynamics picks
a preferred state even though the underlying equations are symmetric.

MATHEMATICAL FOUNDATION:
- Symmetry group: Z_2 (TetA <-> TetB exchange)
- Order parameter: m = (N_B - N_A) / N
- SSB: <m> != 0 even though Hamiltonian has m <-> -m symmetry

NULL HYPOTHESIS: Symmetric dynamics (no spontaneous breaking)
DISCOVERY: Non-zero order parameter indicates SSB

Reference: Spontaneous symmetry breaking, Goldstone theorem
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B


def get_vertex_history(n_steps: int, offset: int = 0) -> List[int]:
    """Extract vertex sequence from traversal with optional offset."""
    traversal = traverse_pi_base8(n_steps + offset, include_integer=True)
    return [step['vertex'] for step in traversal[offset:]]


def compute_order_parameter_distribution(history: List[int], window: int = 100) -> np.ndarray:
    """
    Compute distribution of order parameter over windows.
    
    m = (N_B - N_A) / window
    """
    n_windows = len(history) // window
    order_params = []
    
    for i in range(n_windows):
        segment = history[i*window:(i+1)*window]
        n_a = sum(1 for v in segment if v in TET_A)
        n_b = window - n_a
        m = (n_b - n_a) / window
        order_params.append(m)
    
    return np.array(order_params)


def analyze_distribution_shape(order_params: np.ndarray) -> Dict:
    """
    Analyze the shape of the order parameter distribution.
    
    Symmetric: peaked at m=0
    SSB: peaked away from m=0 (one or two peaks)
    """
    mean = np.mean(order_params)
    std = np.std(order_params)
    
    # Test for bimodality (sign of SSB in finite system)
    positive = order_params[order_params > 0]
    negative = order_params[order_params < 0]
    
    frac_positive = len(positive) / len(order_params) if len(order_params) > 0 else 0.5
    
    # Skewness
    if std > 0:
        skewness = np.mean(((order_params - mean) / std) ** 3)
    else:
        skewness = 0
    
    # Test for deviation from zero mean
    # t-test statistic
    n = len(order_params)
    t_stat = mean / (std / math.sqrt(n)) if std > 0 else 0
    
    return {
        'mean': mean,
        'std': std,
        'skewness': skewness,
        'frac_positive': frac_positive,
        't_statistic': t_stat,
        'is_symmetric': abs(t_stat) < 2.0,  # |t| < 2 means consistent with zero
        'is_broken': abs(t_stat) > 3.0,     # |t| > 3 means significantly non-zero
    }


def test_ssb_persistence(n_steps: int, n_trials: int = 5) -> Dict:
    """
    Test if symmetry breaking persists across different starting points.
    
    True SSB should show consistent bias regardless of where we start.
    """
    biases = []
    
    for trial in range(n_trials):
        offset = trial * 500  # Reduced from 1000 to stay within data limits
        history = get_vertex_history(n_steps, offset)
        n_a = sum(1 for v in history if v in TET_A)
        n_b = n_steps - n_a
        bias = (n_b - n_a) / n_steps
        biases.append(bias)
    
    mean_bias = np.mean(biases)
    std_bias = np.std(biases)
    
    # Consistent if all biases have same sign and similar magnitude
    all_same_sign = all(b > 0 for b in biases) or all(b < 0 for b in biases)
    
    return {
        'mean_bias': mean_bias,
        'std_bias': std_bias,
        'all_same_sign': all_same_sign,
        'biases': biases,
        'is_persistent': all_same_sign and std_bias < abs(mean_bias),
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class SpontaneousBreakingProbe(Test):
    """
    PROBING: Test for spontaneous symmetry breaking between TetA and TetB.
    """
    name = "Spontaneous Symmetry Breaking Test"
    question = (
        "Does the TetA/TetB symmetry break spontaneously? The underlying "
        "structure is symmetric (both tetrahedra are geometrically equivalent), "
        "but the dynamics might pick a preferred side."
    )
    reference = "Spontaneous symmetry breaking, Landau theory"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We test whether the order parameter m = (N_B - N_A)/N is "
        "statistically different from zero. Prior probes found ~1% TetB bias. "
        "Here we formally test if this is genuine SSB or just fluctuation."
    )

    def derivation(self):
        return (
            Derivation()
            .step("SPONTANEOUS SYMMETRY BREAKING (SSB):")
            .step("Symmetry group: Z_2 (TetA <-> TetB exchange)")
            .step("Order parameter: m = (N_B - N_A) / N")
            .step("SSB CONDITION:")
            .equation("<m> != 0 even with symmetric dynamics")
            .step("TEST: t-statistic for mean != 0")
            .equation("t = mean(m) / (std(m) / sqrt(n))")
            .step("If |t| > 3, SSB is statistically significant.")
            .conclude("Non-zero mean order parameter indicates SSB.")
        )

    def model(self):
        n_steps = 8000
        history = get_vertex_history(n_steps)
        
        # Compute order parameter distribution
        window = 100
        order_params = compute_order_parameter_distribution(history, window)
        
        # Analyze distribution
        analysis = analyze_distribution_shape(order_params)
        
        return (
            Model()
            .add("Mean order parameter", analysis['mean'])
            .add("Std of order parameter", analysis['std'])
            .add("Skewness", analysis['skewness'])
            .add("t-statistic", analysis['t_statistic'])
            .add("Fraction positive", analysis['frac_positive'])
            .add("Is SSB present", 1.0 if analysis['is_broken'] else 0.0)
        )

    def observations(self):
        # NULL: Symmetric (no SSB)
        return (
            Observed()
            .add("Mean order parameter", 0.0)
            .add("Std of order parameter", 0.1)
            .add("Skewness", 0.0)
            .add("t-statistic", 0.0)
            .add("Fraction positive", 0.5)
            .add("Is SSB present", 0.0)
        )


class SSBPersistenceProbe(Test):
    """
    PROBING: Is the symmetry breaking persistent or transient?
    """
    name = "SSB Persistence Test"
    question = (
        "Does the TetB bias persist across different trajectory segments? "
        "True SSB should show consistent bias everywhere. Transient breaking "
        "would show varying signs."
    )
    reference = "Ergodicity breaking, persistent symmetry breaking"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We check if the bias has the same sign and magnitude "
        "when starting from different points in the pi sequence. Persistent "
        "bias suggests true SSB built into the dynamics structure."
    )

    def derivation(self):
        return (
            Derivation()
            .step("PERSISTENCE TEST:")
            .step("Measure bias starting from different initial conditions.")
            .step("If bias is always toward TetB:")
            .step("  True SSB = built into dynamics structure")
            .step("If bias varies in sign:")
            .step("  Transient = fluctuation around symmetric point")
            .step("CRITERION:")
            .step("  Persistent: all biases same sign AND std(bias) < |mean(bias)|")
            .conclude("Persistence distinguishes true SSB from fluctuations.")
        )

    def model(self):
        n_steps = 2000
        
        # Test SSB persistence (reduced to stay within data limits)
        persistence = test_ssb_persistence(n_steps, n_trials=5)
        
        # Additional: check different trajectory lengths
        biases_by_length = []
        for length in [1000, 2000, 4000, 8000]:
            history = get_vertex_history(length)
            n_a = sum(1 for v in history if v in TET_A)
            bias = (length - 2*n_a) / length
            biases_by_length.append(bias)
        
        return (
            Model()
            .add("Mean bias across trials", persistence['mean_bias'])
            .add("Std of bias", persistence['std_bias'])
            .add("All same sign", 1.0 if persistence['all_same_sign'] else 0.0)
            .add("Is persistent SSB", 1.0 if persistence['is_persistent'] else 0.0)
            .add("Bias variance across lengths", np.var(biases_by_length))
        )

    def observations(self):
        # NULL: No persistent bias
        return (
            Observed()
            .add("Mean bias across trials", 0.0)
            .add("Std of bias", 0.05)
            .add("All same sign", 0.0)
            .add("Is persistent SSB", 0.0)
            .add("Bias variance across lengths", 0.001)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    SpontaneousBreakingProbe,
    SSBPersistenceProbe,
]


def run_all():
    """Run all spontaneous breaking probing tests."""
    summary = (
        "SPONTANEOUS SYMMETRY BREAKING PROBING\n\n"
        "These probes test for SSB between TetA and TetB.\n"
        "Order parameter: m = (N_B - N_A) / N\n"
        "SSB present if <m> significantly != 0\n\n"
        "We are DISCOVERING if symmetry breaks spontaneously."
    )
    return run_tests("Spontaneous Breaking Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
