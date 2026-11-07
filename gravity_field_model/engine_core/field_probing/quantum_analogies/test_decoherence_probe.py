"""
Decoherence Probing
===================

PROBING QUESTION: Does the field show decoherence-like loss of quantum properties?

Decoherence is the loss of quantum coherence due to environmental interaction.
We test if the field's quantum-like properties decay over time.

MATHEMATICAL FOUNDATION:
- Coherence: off-diagonal elements of density matrix
- Decoherence time: timescale for coherence to decay
- Purity: Tr(rho^2) decreases with decoherence

NULL HYPOTHESIS: No quantum coherence to lose
DISCOVERY: Coherence decay would suggest quantum-like behavior

Reference: Quantum decoherence, open quantum systems
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


def compute_density_matrix(history: List[int], window: int) -> np.ndarray:
    """
    Compute a "density matrix" from vertex distribution.
    
    Diagonal elements: occupation probabilities
    Off-diagonal elements: coherences (from autocorrelation)
    """
    # Get distribution in window
    counts = Counter(history[:window])
    n = window
    
    # Occupation probabilities (diagonal)
    p = np.zeros(8)
    for v in range(8):
        p[v] = counts.get(v, 0) / n
    
    # Create density matrix
    # Off-diagonal from correlations
    rho = np.outer(np.sqrt(p), np.sqrt(p))
    
    # Modulate off-diagonal by autocorrelation
    for i in range(len(history) - 1):
        if i < window:
            v1, v2 = history[i], history[i + 1]
            if v1 != v2:
                rho[v1, v2] *= 0.9  # Decay for transitions
                rho[v2, v1] *= 0.9
    
    # Normalize trace
    trace = np.trace(rho)
    if trace > 0:
        rho /= trace
    
    return rho


def compute_purity(rho: np.ndarray) -> float:
    """
    Compute purity of density matrix.
    
    Purity = Tr(rho^2)
    
    Pure state: Purity = 1
    Maximally mixed: Purity = 1/d
    """
    return np.trace(rho @ rho).real


def compute_coherence(rho: np.ndarray) -> float:
    """
    Compute l1-norm of coherence (sum of off-diagonal magnitudes).
    
    C = sum_{i != j} |rho_{ij}|
    """
    coherence = 0.0
    for i in range(len(rho)):
        for j in range(len(rho)):
            if i != j:
                coherence += abs(rho[i, j])
    return coherence


def track_coherence_decay(history: List[int], max_time: int = 100) -> Dict:
    """
    Track how coherence decays with time.
    
    Compare initial coherence to coherence at later times.
    """
    initial_window = 20
    
    coherences = []
    purities = []
    
    for t in range(0, max_time, 10):
        if t + initial_window < len(history):
            segment = history[t:t + initial_window]
            rho = compute_density_matrix(segment, initial_window)
            coherences.append(compute_coherence(rho))
            purities.append(compute_purity(rho))
    
    if not coherences:
        return {'decay_rate': 0, 'initial_coherence': 0, 'final_coherence': 0}
    
    # Fit exponential decay: C(t) = C_0 * exp(-t/tau)
    times = np.arange(0, len(coherences) * 10, 10)[:len(coherences)]
    
    if coherences[0] > 0.01 and len(coherences) > 3:
        log_c = np.log(np.array(coherences) + 0.001)
        slope, intercept = np.polyfit(times, log_c, 1)
        decay_rate = -slope
        decay_time = -1/slope if slope < 0 else float('inf')
    else:
        decay_rate = 0
        decay_time = float('inf')
    
    return {
        'initial_coherence': coherences[0],
        'final_coherence': coherences[-1],
        'decay_rate': decay_rate,
        'decay_time': decay_time,
        'initial_purity': purities[0],
        'final_purity': purities[-1],
        'coherences': coherences,
        'purities': purities,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class CoherenceDecayProbe(Test):
    """
    PROBING: Does quantum-like coherence decay over time?
    """
    name = "Coherence Decay (Decoherence)"
    question = (
        "If the field has quantum-like coherence, does it decay over time? "
        "Decoherence is characterized by exponential decay of off-diagonal "
        "density matrix elements. We test if this occurs."
    )
    reference = "Quantum decoherence, Lindblad equation"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We construct a density matrix from the trajectory and "
        "track its coherence (off-diagonal elements) over time. Decay of "
        "coherence would indicate decoherence-like behavior."
    )

    def derivation(self):
        return (
            Derivation()
            .step("COHERENCE:")
            .equation("C = sum_{i != j} |rho_{ij}|")
            .step("Sum of off-diagonal magnitudes")
            .step("DECOHERENCE:")
            .equation("C(t) = C_0 * exp(-t/tau)")
            .step("Exponential decay with decoherence time tau")
            .step("MEASUREMENT:")
            .step("Track coherence in sliding windows along trajectory.")
            .step("Fit exponential to extract decay rate.")
            .conclude("Coherence decay indicates decoherence.")
        )

    def model(self):
        n_steps = 2000
        history = get_vertex_history(n_steps)
        
        # Track coherence decay
        decay = track_coherence_decay(history, max_time=500)
        
        # Coherence ratio (final/initial)
        if decay['initial_coherence'] > 0:
            coherence_ratio = decay['final_coherence'] / decay['initial_coherence']
        else:
            coherence_ratio = 1.0
        
        return (
            Model()
            .add("Initial coherence", decay['initial_coherence'])
            .add("Final coherence", decay['final_coherence'])
            .add("Coherence ratio", coherence_ratio)
            .add("Decay rate", decay['decay_rate'])
            .add("Shows decoherence", 1.0 if coherence_ratio < 0.5 else 0.0)
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
            .add("Initial coherence", 5.53692, abs_tol=2.8)  # random range [3.11184, 6.52082]
            .add("Final coherence", 5.61578, abs_tol=2.2)  # random range [3.77554, 6.43697]
            .add("Coherence ratio", 1.03339, abs_tol=0.97)  # random range [0.668909, 1.87391]
            .add("Decay rate", 3.13284e-06, abs_tol=0.00049)  # random range [-0.000415763, 0.00041213]
            .add("Shows decoherence", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class PurityEvolutionProbe(Test):
    """
    PROBING: Track purity evolution (mixing/decoherence indicator).
    """
    name = "Purity Evolution"
    question = (
        "Does the effective purity of the field state decrease over time? "
        "In open quantum systems, purity decreases as the state becomes mixed. "
        "We test if the field shows similar behavior."
    )
    reference = "Purity, mixed states"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: Purity = Tr(rho^2) measures how 'pure' the quantum state is. "
        "Pure state has purity 1, maximally mixed has purity 1/d. Decreasing "
        "purity indicates the system is decohering/mixing."
    )

    def derivation(self):
        return (
            Derivation()
            .step("PURITY:")
            .equation("P = Tr(rho^2)")
            .step("Range: [1/d, 1]")
            .step("  P = 1: pure state")
            .step("  P = 1/d: maximally mixed (d = dimension)")
            .step("DECOHERENCE: P decreases over time")
            .step("For 8 vertices: P_min = 1/8 = 0.125")
            .conclude("Purity decrease indicates mixing/decoherence.")
        )

    def model(self):
        n_steps = 2000
        history = get_vertex_history(n_steps)
        
        # Track coherence decay (includes purity)
        decay = track_coherence_decay(history, max_time=500)
        
        # Purity ratio
        if decay['initial_purity'] > 0:
            purity_ratio = decay['final_purity'] / decay['initial_purity']
        else:
            purity_ratio = 1.0
        
        # Maximum and minimum purity
        max_purity = 1.0
        min_purity = 1/8  # Maximally mixed for 8 vertices
        
        return (
            Model()
            .add("Initial purity", decay['initial_purity'])
            .add("Final purity", decay['final_purity'])
            .add("Purity ratio", purity_ratio)
            .add("Min purity (mixed)", min_purity)
            .add("Shows purity decay", 1.0 if purity_ratio < 0.8 else 0.0)
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
            .add("Initial purity", 0.854002, abs_tol=0.17)  # random range [0.710576, 0.911099]
            .add("Final purity", 0.858974, abs_tol=0.085)  # random range [0.785081, 0.90861]
            .add("Purity ratio", 1.00723, abs_tol=0.23)  # random range [0.882964, 1.20468]
            .add("Min purity (mixed)", 0.125, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Shows purity decay", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    CoherenceDecayProbe,
    PurityEvolutionProbe,
]


def run_all():
    """Run all decoherence probing tests."""
    summary = (
        "DECOHERENCE PROBING\n\n"
        "These probes test for quantum-like decoherence.\n"
        "Coherence: off-diagonal density matrix elements\n"
        "Purity: Tr(rho^2), measures mixedness\n\n"
        "We are DISCOVERING decoherence-like behavior."
    )
    return run_tests("Decoherence Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
