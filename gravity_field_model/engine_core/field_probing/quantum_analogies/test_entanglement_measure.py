"""
Entanglement Measure Probing
============================

PROBING QUESTION: Are TetA and TetB "entangled" in a quantum sense?

Entanglement is quantum correlation that cannot be explained classically.
We test for classical analogs: correlations that mimic entanglement.

IMPORTANT CAVEAT: Classical systems cannot have true entanglement.
We're testing for strong correlations that LOOK entangled.

MATHEMATICAL FOUNDATION:
- Entanglement entropy: S = -Tr(rho_A * log(rho_A))
- Mutual information: I(A;B) = S(A) + S(B) - S(A,B)
- Bell inequality violation (classical limit)

NULL HYPOTHESIS: Classical correlations (no entanglement-like behavior)
DISCOVERY: Strong correlations would suggest entanglement-like coupling

Reference: Quantum entanglement, mutual information
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


def compute_joint_distribution(history: List[int], window: int = 10) -> np.ndarray:
    """
    Compute joint distribution P(TetA vertex, TetB vertex) from consecutive windows.
    
    This creates a "density matrix" like structure from classical data.
    """
    # Discretize TetA and TetB states
    half_window = window // 2
    n_windows = (len(history) - window) // half_window
    
    # Use (TetA activity, TetB activity) as joint state
    joint_counts = np.zeros((5, 5))  # 0-4 visits in each chamber
    
    for i in range(n_windows):
        start = i * half_window
        segment = history[start:start+window]
        
        # Count TetA and TetB visits
        n_a = sum(1 for v in segment if v in TET_A)
        n_b = window - n_a
        
        # Bin to 0-4
        a_bin = min(n_a, 4)
        b_bin = min(n_b, 4)
        
        joint_counts[a_bin, b_bin] += 1
    
    # Normalize
    total = joint_counts.sum()
    if total > 0:
        joint_dist = joint_counts / total
    else:
        joint_dist = np.ones((5, 5)) / 25
    
    return joint_dist


def compute_entanglement_entropy(joint_dist: np.ndarray) -> float:
    """
    Compute entanglement entropy from joint distribution.
    
    S_A = -Tr(rho_A * log(rho_A)) where rho_A is reduced density matrix
    """
    # Marginal for A (sum over B)
    p_a = joint_dist.sum(axis=1)
    
    # Entropy
    entropy = 0.0
    for p in p_a:
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy


def compute_quantum_discord_analog(joint_dist: np.ndarray) -> float:
    """
    Compute classical analog of quantum discord.
    
    Discord = I(A;B) - J(A|B)
    where J is one-way classical correlation
    """
    # Marginals
    p_a = joint_dist.sum(axis=1)
    p_b = joint_dist.sum(axis=0)
    
    # Entropies
    def entropy(p):
        return -sum(x * math.log2(x) if x > 0 else 0 for x in p)
    
    h_a = entropy(p_a)
    h_b = entropy(p_b)
    
    # Joint entropy
    h_ab = 0.0
    for row in joint_dist:
        for p in row:
            if p > 0:
                h_ab -= p * math.log2(p)
    
    # Mutual information
    mi = h_a + h_b - h_ab
    
    # Conditional entropy H(A|B)
    h_a_given_b = h_ab - h_b
    
    # Classical correlation J = H(A) - H(A|B)
    j = h_a - h_a_given_b
    
    # Discord analog (should be 0 for classical)
    discord = mi - j
    
    return discord


def compute_concurrence_analog(joint_dist: np.ndarray) -> float:
    """
    Compute analog of concurrence from correlation structure.
    
    Uses the correlation matrix eigenvalues.
    """
    # Normalize and center
    mean_a = np.sum(joint_dist * np.arange(5)[:, None])
    mean_b = np.sum(joint_dist * np.arange(5)[None, :])
    
    # Correlation
    corr = 0.0
    for i in range(5):
        for j in range(5):
            corr += joint_dist[i, j] * (i - mean_a) * (j - mean_b)
    
    std_a = math.sqrt(np.sum(joint_dist * (np.arange(5)[:, None] - mean_a)**2))
    std_b = math.sqrt(np.sum(joint_dist * (np.arange(5)[None, :] - mean_b)**2))
    
    if std_a > 0 and std_b > 0:
        correlation = corr / (std_a * std_b)
    else:
        correlation = 0.0
    
    # Concurrence-like: 0 for uncorrelated, 1 for maximally correlated
    return abs(correlation)


# =============================================================================
# TEST CLASSES
# =============================================================================

class EntanglementEntropyProbe(Test):
    """
    PROBING: Compute entanglement-like entropy between TetA and TetB.
    """
    name = "Entanglement Entropy Analog"
    question = (
        "What is the entanglement entropy between TetA and TetB? "
        "This measures how much information about one chamber is encoded "
        "in the other. High entropy suggests strong (entanglement-like) coupling."
    )
    reference = "Entanglement entropy, quantum information"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We treat the joint TetA-TetB state distribution as a "
        "density matrix and compute its entanglement entropy. While this "
        "is classical, high values indicate the chambers are strongly "
        "coupled in a way that mimics quantum entanglement."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ENTANGLEMENT ENTROPY:")
            .equation("S_A = -Tr(rho_A * log(rho_A))")
            .step("where rho_A is the reduced density matrix for subsystem A")
            .step("FOR PRODUCT STATE: S = 0 (no entanglement)")
            .step("FOR MAXIMALLY ENTANGLED: S = log(d) (d = dimension)")
            .step("CLASSICAL ANALOG:")
            .step("Treat joint distribution as density matrix.")
            .step("Compute entropy of marginal distribution.")
            .conclude("Entanglement entropy measures TetA-TetB coupling.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute joint distribution
        joint = compute_joint_distribution(history, window=20)
        
        # Entanglement entropy
        s_entangle = compute_entanglement_entropy(joint)
        
        # Maximum entropy for 5 states
        max_entropy = math.log2(5)
        
        # Entropy ratio
        entropy_ratio = s_entangle / max_entropy
        
        # Mutual information
        p_a = joint.sum(axis=1)
        p_b = joint.sum(axis=0)
        h_a = -sum(p * math.log2(p) if p > 0 else 0 for p in p_a)
        h_b = -sum(p * math.log2(p) if p > 0 else 0 for p in p_b)
        h_ab = -sum(p * math.log2(p) if p > 0 else 0 for p in joint.flatten())
        mi = h_a + h_b - h_ab
        
        return (
            Model()
            .add("Entanglement entropy", s_entangle)
            .add("Max entropy (log2(5))", max_entropy)
            .add("Entropy ratio", entropy_ratio)
            .add("Mutual information", mi)
            .add("Is highly entangled (ratio > 0.5)", 1.0 if entropy_ratio > 0.5 else 0.0)
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
            .add("Entanglement entropy", 0.0108038, abs_tol=0.055)  # random range [0, 0.0586246]
            .add("Max entropy (log2(5))", 2.321928094887, abs_tol=2e-09)  # same for all 150 random sequences
            .add("Entropy ratio", 0.00465293, abs_tol=0.024)  # random range [0, 0.0252482]
            .add("Mutual information", 2.06301e-06, abs_tol=5.2e-05)  # random range [0, 4.68202e-05]
            .add("Is highly entangled (ratio > 0.5)", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class ConcurrenceProbe(Test):
    """
    PROBING: Compute concurrence-like correlation measure.
    """
    name = "Concurrence Analog (Correlation Strength)"
    question = (
        "How strongly correlated are TetA and TetB activities? "
        "Concurrence measures the strength of quantum correlations. "
        "We compute a classical analog from the correlation coefficient."
    )
    reference = "Concurrence, correlation measures"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: Concurrence in quantum mechanics ranges from 0 "
        "(product state) to 1 (maximally entangled). Our classical analog "
        "uses the correlation coefficient, measuring how strongly "
        "TetA activity predicts TetB activity."
    )

    def derivation(self):
        return (
            Derivation()
            .step("CONCURRENCE (quantum):")
            .step("Measures strength of entanglement in 2-qubit system.")
            .step("Range [0, 1]: 0 = separable, 1 = maximally entangled")
            .step("CLASSICAL ANALOG:")
            .equation("C = |Corr(A, B)|")
            .step("where Corr is the Pearson correlation coefficient")
            .step("C = 0: independent")
            .step("C = 1: perfectly correlated (or anti-correlated)")
            .conclude("Concurrence analog measures correlation strength.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute joint distribution
        joint = compute_joint_distribution(history, window=20)
        
        # Concurrence analog
        concurrence = compute_concurrence_analog(joint)
        
        # Discord analog
        discord = compute_quantum_discord_analog(joint)
        
        # Is strongly correlated?
        is_strong = concurrence > 0.5
        
        return (
            Model()
            .add("Concurrence analog", concurrence)
            .add("Discord analog", discord)
            .add("Is strongly correlated", 1.0 if is_strong else 0.0)
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
            .add("Concurrence analog", 0.000466305, abs_tol=0.0061)  # random range [0, 0.00571401]
            .add("Discord analog", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Is strongly correlated", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    EntanglementEntropyProbe,
    ConcurrenceProbe,
]


def run_all():
    """Run all entanglement measure probing tests."""
    summary = (
        "ENTANGLEMENT MEASURE PROBING\n\n"
        "These probes test for entanglement-like correlations.\n"
        "Entanglement entropy: information shared between chambers\n"
        "Concurrence: strength of correlation\n\n"
        "We are DISCOVERING quantum-like coupling."
    )
    return run_tests("Entanglement Measure Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
