"""
Memory Length Probing
=====================

PROBING QUESTION: How many steps back does the current vertex depend on?

This probe measures the autocorrelation function and determines
whether the field dynamics is Markovian (memoryless) or has long memory.

MATHEMATICAL FOUNDATION:
- Autocorrelation: R(k) = E[(X_t - mu)(X_{t+k} - mu)] / Var(X)
- Memory length: smallest k where R(k) becomes negligible
- Markov test: P(X_t | X_{t-1}, ...) = P(X_t | X_{t-1})

NULL HYPOTHESIS: First-order Markov (memory = 1 step)
DISCOVERY: Longer memory indicates hidden structure

Reference: Time series analysis, Markov chain theory
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


def compute_autocorrelation(history: List[int], max_lag: int = 50) -> np.ndarray:
    """
    Compute autocorrelation function R(k) for lags 0 to max_lag.
    
    R(k) = Cov(X_t, X_{t+k}) / Var(X)
    """
    x = np.array(history, dtype=float)
    n = len(x)
    mean = np.mean(x)
    var = np.var(x)
    
    if var == 0:
        return np.zeros(max_lag + 1)
    
    autocorr = np.zeros(max_lag + 1)
    for k in range(max_lag + 1):
        if k < n:
            cov = np.mean((x[:n-k] - mean) * (x[k:] - mean))
            autocorr[k] = cov / var
    
    return autocorr


def compute_partial_autocorrelation(autocorr: np.ndarray) -> np.ndarray:
    """
    Compute partial autocorrelation using Durbin-Levinson recursion.
    
    PACF(k) measures correlation at lag k after removing contributions
    from shorter lags. For AR(p) process, PACF cuts off after lag p.
    """
    n = len(autocorr) - 1
    pacf = np.zeros(n + 1)
    pacf[0] = 1.0
    
    if n < 1:
        return pacf
    
    # Durbin-Levinson recursion
    phi = np.zeros((n + 1, n + 1))
    phi[1, 1] = autocorr[1]
    pacf[1] = autocorr[1]
    
    for k in range(2, n + 1):
        # Compute phi[k,k]
        num = autocorr[k] - sum(phi[k-1, j] * autocorr[k-j] for j in range(1, k))
        den = 1 - sum(phi[k-1, j] * autocorr[j] for j in range(1, k))
        
        if abs(den) < 1e-10:
            break
            
        phi[k, k] = num / den
        pacf[k] = phi[k, k]
        
        # Update phi[k, j] for j < k
        for j in range(1, k):
            phi[k, j] = phi[k-1, j] - phi[k, k] * phi[k-1, k-j]
    
    return pacf


def find_memory_length(autocorr: np.ndarray, threshold: float = 0.05) -> int:
    """
    Find the lag where autocorrelation becomes negligible.
    
    Memory length = smallest k where |R(k)| < threshold for all k' > k.
    """
    n = len(autocorr)
    for k in range(1, n):
        if all(abs(autocorr[j]) < threshold for j in range(k, n)):
            return k
    return n


def test_markov_property(history: List[int], order: int = 1) -> Dict:
    """
    Test if the sequence is order-k Markov.
    
    Method: Compare P(X_t | X_{t-1},...,X_{t-order}) vs P(X_t | X_{t-1},...,X_{t-order-1})
    Using chi-squared test for independence.
    """
    from collections import defaultdict
    
    # Count transitions with different context lengths
    trans_short = defaultdict(lambda: defaultdict(int))  # Order-k context
    trans_long = defaultdict(lambda: defaultdict(int))   # Order-(k+1) context
    
    for i in range(order + 1, len(history)):
        short_context = tuple(history[i-order:i])
        long_context = tuple(history[i-order-1:i])
        symbol = history[i]
        
        trans_short[short_context][symbol] += 1
        trans_long[long_context][symbol] += 1
    
    # Compute entropy of transitions
    def context_entropy(trans_dict):
        total = sum(sum(d.values()) for d in trans_dict.values())
        h = 0.0
        for context, symbols in trans_dict.items():
            context_total = sum(symbols.values())
            p_context = context_total / total
            h_context = 0.0
            for count in symbols.values():
                if count > 0:
                    p = count / context_total
                    h_context -= p * math.log2(p)
            h += p_context * h_context
        return h
    
    h_short = context_entropy(trans_short)
    h_long = context_entropy(trans_long)
    
    # If Markov of order k, h_long should equal h_short
    entropy_gap = h_short - h_long
    
    return {
        'entropy_short_context': h_short,
        'entropy_long_context': h_long,
        'entropy_gap': entropy_gap,
        'is_markov': entropy_gap < 0.05,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class AutocorrelationProbe(Test):
    """
    PROBING: Measure the autocorrelation function of the traversal.
    """
    name = "Autocorrelation Function Probe"
    question = (
        "How correlated is the current vertex with past vertices? "
        "Does the correlation decay exponentially (short memory) or "
        "polynomially (long memory)? What is the characteristic "
        "memory timescale?"
    )
    reference = "Time series analysis, autocorrelation"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: The autocorrelation function reveals temporal structure. "
        "For a random walk, R(k) decays to zero quickly. Long-range "
        "correlations would indicate persistent patterns or memory. "
        "This is discovery about the temporal structure of the field."
    )

    def derivation(self):
        return (
            Derivation()
            .step("AUTOCORRELATION FUNCTION:")
            .equation("R(k) = E[(X_t - mu)(X_{t+k} - mu)] / Var(X)")
            .step("Properties:")
            .step("  R(0) = 1 (perfect self-correlation)")
            .step("  |R(k)| <= 1 for all k")
            .step("  R(k) -> 0 as k -> infinity (for stationary processes)")
            .step("MEMORY LENGTH:")
            .step("Defined as smallest k where R(k) becomes negligible.")
            .step("Short memory: R(k) ~ exp(-k/tau)")
            .step("Long memory: R(k) ~ k^(-alpha)")
            .conclude("Autocorrelation decay characterizes memory.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute autocorrelation
        autocorr = compute_autocorrelation(history, max_lag=50)
        
        # Find memory length
        memory_length = find_memory_length(autocorr, threshold=0.05)
        
        # Fit exponential decay: R(k) ~ exp(-k/tau)
        # Using log(|R(k)|) = -k/tau for k > 0
        valid_idx = [k for k in range(1, min(20, len(autocorr))) if abs(autocorr[k]) > 0.01]
        if len(valid_idx) >= 3:
            x = np.array(valid_idx)
            y = np.log(np.abs(autocorr[valid_idx]))
            slope, intercept = np.polyfit(x, y, 1)
            decay_time = -1 / slope if slope < 0 else float('inf')
        else:
            decay_time = 1.0
        
        return (
            Model()
            .add("R(1) autocorrelation", autocorr[1])
            .add("R(2) autocorrelation", autocorr[2])
            .add("R(5) autocorrelation", autocorr[5])
            .add("R(10) autocorrelation", autocorr[10])
            .add("Memory length (steps)", memory_length)
            .add("Exponential decay time", decay_time)
        )

    def observations(self):
        # NULL: White noise (zero autocorrelation for k > 0)
        return (
            Observed()
            .add("R(1) autocorrelation", 0.0)
            .add("R(2) autocorrelation", 0.0)
            .add("R(5) autocorrelation", 0.0)
            .add("R(10) autocorrelation", 0.0)
            .add("Memory length (steps)", 1)
            .add("Exponential decay time", 0.0)
        )


class MarkovOrderProbe(Test):
    """
    PROBING: What is the Markov order of the dynamics?
    """
    name = "Markov Order Determination"
    question = (
        "Is the traversal a first-order Markov chain (next vertex depends only "
        "on current), or does it have higher-order dependencies? What is the "
        "minimum history needed to predict the next vertex optimally?"
    )
    reference = "Markov chain theory, model order selection"
    level = Exploratory
    tolerance = 0.2

    commentary = (
        "PROBING: Determining the Markov order tells us how much history "
        "is relevant. First-order Markov means memoryless transitions. "
        "Higher orders indicate longer-range dependencies in the dynamics."
    )

    def derivation(self):
        return (
            Derivation()
            .step("MARKOV ORDER:")
            .step("A process is order-k Markov if:")
            .equation("P(X_t | X_{t-1},...,X_0) = P(X_t | X_{t-1},...,X_{t-k})")
            .step("TEST: Compare conditional entropies")
            .step("H(X | context_k) vs H(X | context_{k+1})")
            .step("If equal, order <= k is sufficient.")
            .step("The smallest k where they're equal is the Markov order.")
            .conclude("Markov order = minimum relevant history length.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Test Markov orders 1, 2, 3
        markov_1 = test_markov_property(history, order=1)
        markov_2 = test_markov_property(history, order=2)
        markov_3 = test_markov_property(history, order=3)
        
        # Determine effective Markov order
        if markov_1['is_markov']:
            effective_order = 1
        elif markov_2['is_markov']:
            effective_order = 2
        elif markov_3['is_markov']:
            effective_order = 3
        else:
            effective_order = 4  # Or higher
        
        return (
            Model()
            .add("Entropy gap (order 1 vs 2)", markov_1['entropy_gap'])
            .add("Entropy gap (order 2 vs 3)", markov_2['entropy_gap'])
            .add("Entropy gap (order 3 vs 4)", markov_3['entropy_gap'])
            .add("Is first-order Markov", 1.0 if markov_1['is_markov'] else 0.0)
            .add("Effective Markov order", effective_order)
        )

    def observations(self):
        # NULL: First-order Markov
        return (
            Observed()
            .add("Entropy gap (order 1 vs 2)", 0.0)
            .add("Entropy gap (order 2 vs 3)", 0.0)
            .add("Entropy gap (order 3 vs 4)", 0.0)
            .add("Is first-order Markov", 1.0)
            .add("Effective Markov order", 1)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    AutocorrelationProbe,
    MarkovOrderProbe,
]


def run_all():
    """Run all memory length probing tests."""
    summary = (
        "MEMORY LENGTH PROBING\n\n"
        "These probes measure how far back in time the dynamics depends.\n"
        "Autocorrelation: correlation between X_t and X_{t+k}\n"
        "Markov order: minimum history for optimal prediction\n\n"
        "We are DISCOVERING the temporal structure."
    )
    return run_tests("Memory Length Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
