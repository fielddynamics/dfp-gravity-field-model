"""
Entropy Rate Probing
====================

PROBING QUESTION: How many bits of information does each traversal step produce?

This probe measures the Shannon entropy rate of the vertex visitation sequence.
The entropy rate quantifies the "surprise" or unpredictability per step.

MATHEMATICAL FOUNDATION:
- Shannon entropy: H(X) = -sum_x P(x) log2 P(x)
- Entropy rate: h = lim_{n->inf} H(X_1,...,X_n) / n
- For i.i.d.: h = H(X)
- For Markov: h = H(X_t | X_{t-1})

NULL HYPOTHESIS: Maximum entropy (uniform random) = log2(8) = 3 bits/step
DISCOVERY: Any deviation indicates structure in the dynamics

Reference: Cover & Thomas "Elements of Information Theory"
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


def compute_single_symbol_entropy(history: List[int]) -> float:
    """
    Compute H(X) - entropy of single vertex distribution.
    
    Maximum is log2(8) = 3 bits for uniform distribution.
    """
    counts = Counter(history)
    n = len(history)
    
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / n
            entropy -= p * math.log2(p)
    
    return entropy


def compute_conditional_entropy(history: List[int], order: int = 1) -> float:
    """
    Compute H(X_t | X_{t-1}, ..., X_{t-order}) - conditional entropy.
    
    For a Markov chain, this equals the entropy rate.
    """
    if len(history) <= order:
        return 0.0
    
    # Count (context, symbol) pairs
    context_counts = Counter()
    joint_counts = Counter()
    
    for i in range(order, len(history)):
        context = tuple(history[i-order:i])
        symbol = history[i]
        context_counts[context] += 1
        joint_counts[(context, symbol)] += 1
    
    # H(X_t | context) = sum_context P(context) * H(X_t | context=c)
    n = len(history) - order
    conditional_entropy = 0.0
    
    for context, context_count in context_counts.items():
        p_context = context_count / n
        # H(X_t | context = c)
        h_given_context = 0.0
        for symbol in range(8):
            joint_count = joint_counts.get((context, symbol), 0)
            if joint_count > 0:
                p_symbol_given_context = joint_count / context_count
                h_given_context -= p_symbol_given_context * math.log2(p_symbol_given_context)
        conditional_entropy += p_context * h_given_context
    
    return conditional_entropy


def compute_block_entropy(history: List[int], block_size: int) -> float:
    """
    Compute H(X_1, ..., X_k) / k for blocks of size k.
    
    As k -> infinity, this converges to the entropy rate.
    """
    if len(history) < block_size:
        return 0.0
    
    # Count blocks
    blocks = []
    for i in range(len(history) - block_size + 1):
        blocks.append(tuple(history[i:i+block_size]))
    
    counts = Counter(blocks)
    n = len(blocks)
    
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / n
            entropy -= p * math.log2(p)
    
    return entropy / block_size


def estimate_entropy_rate(history: List[int], max_order: int = 5) -> Dict:
    """
    Estimate entropy rate using multiple methods.
    
    Methods:
    1. Single symbol entropy (upper bound)
    2. Conditional entropy (Markov estimate)
    3. Block entropy extrapolation
    """
    results = {}
    
    # Method 1: Single symbol
    h1 = compute_single_symbol_entropy(history)
    results['single_symbol_entropy'] = h1
    
    # Method 2: Conditional entropies for different orders
    conditional = []
    for order in range(1, max_order + 1):
        h_cond = compute_conditional_entropy(history, order)
        conditional.append(h_cond)
        results[f'conditional_order_{order}'] = h_cond
    
    # Entropy rate estimate: last conditional (highest order)
    results['entropy_rate_markov'] = conditional[-1] if conditional else h1
    
    # Method 3: Block entropy
    block_entropies = []
    for k in range(1, min(8, len(history) // 100)):
        h_block = compute_block_entropy(history, k)
        block_entropies.append(h_block)
        results[f'block_entropy_k{k}'] = h_block
    
    # Extrapolate to k -> infinity (linear fit of H(k)/k vs 1/k)
    if len(block_entropies) >= 3:
        x = np.array([1/k for k in range(1, len(block_entropies) + 1)])
        y = np.array(block_entropies)
        # Linear fit: y = h + c/k, so intercept is entropy rate
        coeffs = np.polyfit(x, y, 1)
        results['entropy_rate_extrapolated'] = coeffs[1]  # Intercept
    
    # Maximum possible entropy
    results['max_entropy'] = math.log2(8)
    
    # Redundancy: how much below maximum
    best_estimate = results.get('entropy_rate_markov', h1)
    results['redundancy'] = results['max_entropy'] - best_estimate
    results['efficiency'] = best_estimate / results['max_entropy']
    
    return results


# =============================================================================
# TEST CLASS
# =============================================================================

class EntropyRateProbe(Test):
    """
    PROBING: Measure the information entropy rate of the traversal.
    """
    name = "Information Entropy Rate Probe"
    question = (
        "How many bits of information does each traversal step produce? "
        "Is the field maximally random (3 bits/step), or is there structure "
        "that reduces the entropy? What does the entropy rate tell us about "
        "the field's information-carrying capacity?"
    )
    reference = "Shannon entropy, Cover & Thomas"
    level = Exploratory
    tolerance = 0.5  # Wide tolerance for probing

    commentary = (
        "PROBING: We measure the entropy rate to discover whether the field "
        "has hidden structure. Maximum entropy (3 bits) would mean the "
        "traversal is unpredictable. Lower entropy indicates patterns or "
        "correlations that constrain the dynamics. This is discovery, not "
        "verification: we do not know what to expect."
    )

    def derivation(self):
        return (
            Derivation()
            .step("INFORMATION ENTROPY RATE:")
            .step("For a sequence X_1, X_2, ..., X_n of symbols from alphabet A:")
            .equation("H(X) = -sum_x P(x) log2 P(x)")
            .step("Entropy rate (bits per symbol):")
            .equation("h = lim_{n->inf} H(X_1,...,X_n) / n")
            .step("For Markov chains: h = H(X_t | X_{t-1})")
            .step("BOUNDS:")
            .step("  Maximum: log2(|A|) = log2(8) = 3 bits (uniform random)")
            .step("  Minimum: 0 bits (deterministic sequence)")
            .step("PROBING: Measure h and compare to maximum.")
            .conclude("Entropy rate quantifies the field's unpredictability.")
        )

    def model(self):
        # Generate long traversal
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute entropy estimates
        results = estimate_entropy_rate(history, max_order=5)
        
        return (
            Model()
            .add("Single symbol entropy (bits)", results['single_symbol_entropy'])
            .add("Markov entropy rate (bits)", results['entropy_rate_markov'])
            .add("Maximum entropy (bits)", results['max_entropy'])
            .add("Redundancy (bits)", results['redundancy'])
            .add("Efficiency", results['efficiency'])
            .add("Conditional H(X|X-1)", results.get('conditional_order_1', 0))
            .add("Conditional H(X|X-1,X-2)", results.get('conditional_order_2', 0))
        )

    def observations(self):
        # NULL HYPOTHESIS: Maximum entropy (uniform random)
        # Any deviation is a DISCOVERY
        return (
            Observed()
            .add("Single symbol entropy (bits)", 3.0)  # Maximum
            .add("Markov entropy rate (bits)", 3.0)    # Maximum
            .add("Maximum entropy (bits)", 3.0)
            .add("Redundancy (bits)", 0.0)             # No redundancy = max random
            .add("Efficiency", 1.0)                    # 100% of max
            .add("Conditional H(X|X-1)", 3.0)
            .add("Conditional H(X|X-2)", 3.0)
        )


class EntropyConvergenceProbe(Test):
    """
    PROBING: How does entropy rate converge with increasing context?
    """
    name = "Entropy Convergence Analysis"
    question = (
        "As we condition on more history (longer context), does the conditional "
        "entropy converge quickly or slowly? Fast convergence suggests short "
        "memory; slow convergence suggests long-range correlations."
    )
    reference = "Markov chain theory, entropy rate convergence"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: The rate at which conditional entropy converges reveals "
        "the memory structure of the dynamics. If H(X|X-1) equals H(X|X-1,X-2,...), "
        "the process is first-order Markov. Slower convergence indicates "
        "longer memory. This is discovery about the temporal structure."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ENTROPY CONVERGENCE:")
            .step("For increasing context length k:")
            .equation("H(X_t | X_{t-1},...,X_{t-k})")
            .step("This sequence is non-increasing and converges to h.")
            .step("MEMORY INDICATOR:")
            .step("Define convergence rate:")
            .equation("Delta_k = H(X|context_k) - H(X|context_{k+1})")
            .step("Fast decay of Delta_k means short memory.")
            .step("Slow decay means long-range correlations.")
            .conclude("Convergence rate reveals memory structure.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute conditional entropies for orders 1-5
        conditionals = []
        for order in range(1, 6):
            h = compute_conditional_entropy(history, order)
            conditionals.append(h)
        
        # Compute deltas (drops)
        deltas = [conditionals[0] - conditionals[i] for i in range(1, len(conditionals))]
        
        # Total drop from order 1 to order 5
        total_drop = conditionals[0] - conditionals[-1]
        
        # First-order Markov test: is order-2 similar to order-1?
        markov_gap = conditionals[0] - conditionals[1]
        
        return (
            Model()
            .add("H(X|X-1)", conditionals[0])
            .add("H(X|X-1,X-2)", conditionals[1])
            .add("H(X|context_5)", conditionals[4])
            .add("Total entropy drop (order 1 to 5)", total_drop)
            .add("First-order Markov gap", markov_gap)
        )

    def observations(self):
        # NULL: First-order Markov (no drop after order 1)
        return (
            Observed()
            .add("H(X|X-1)", 2.8)          # Slightly below max
            .add("H(X|X-1,X-2)", 2.8)      # Same as order 1 if Markov
            .add("H(X|context_5)", 2.8)    # Same if Markov
            .add("Total entropy drop (order 1 to 5)", 0.0)  # No additional drop
            .add("First-order Markov gap", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    EntropyRateProbe,
    EntropyConvergenceProbe,
]


def run_all():
    """Run all entropy rate probing tests."""
    summary = (
        "ENTROPY RATE PROBING\n\n"
        "These probes measure the information content of the traversal.\n"
        "Entropy rate = bits per step.\n"
        "Maximum = 3 bits (uniform random over 8 vertices).\n"
        "Lower values indicate structure/predictability.\n\n"
        "We are DISCOVERING, not verifying."
    )
    return run_tests("Entropy Rate Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
