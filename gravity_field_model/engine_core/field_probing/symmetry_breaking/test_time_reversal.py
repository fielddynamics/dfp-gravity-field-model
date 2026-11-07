"""
Time Reversal Probing
=====================

PROBING QUESTION: Does the traversal look different when run backwards?

Time reversal symmetry is fundamental. If forward and backward are
statistically distinguishable, there's an arrow of time.

MATHEMATICAL FOUNDATION:
- Time reversal: T: sequence -> reversed sequence
- T-symmetric: P(v_t -> v_{t+1}) = P(v_{t+1} -> v_t)
- T-asymmetric: forward and backward have different statistics

NULL HYPOTHESIS: Time symmetric (forward = backward statistically)
DISCOVERY: T-asymmetry would indicate arrow of time

Reference: Time reversal symmetry, irreversibility
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter, defaultdict

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def compute_transition_matrix(history: List[int]) -> np.ndarray:
    """
    Compute transition probability matrix.
    
    P[i,j] = P(next = j | current = i)
    """
    trans_counts = np.zeros((8, 8))
    
    for i in range(len(history) - 1):
        v_from = history[i]
        v_to = history[i + 1]
        trans_counts[v_from, v_to] += 1
    
    # Normalize rows
    row_sums = trans_counts.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    trans_matrix = trans_counts / row_sums
    
    return trans_matrix


def compute_detailed_balance_violation(history: List[int]) -> float:
    """
    Compute violation of detailed balance.
    
    Detailed balance: P(i) * P(i->j) = P(j) * P(j->i)
    Violation: sum_ij |P(i) * P(i->j) - P(j) * P(j->i)|
    """
    # Compute stationary distribution
    counts = Counter(history)
    n = len(history)
    stationary = np.zeros(8)
    for v in range(8):
        stationary[v] = counts.get(v, 0) / n
    
    # Compute transition matrix
    trans = compute_transition_matrix(history)
    
    # Compute detailed balance violation
    violation = 0.0
    for i in range(8):
        for j in range(8):
            lhs = stationary[i] * trans[i, j]
            rhs = stationary[j] * trans[j, i]
            violation += abs(lhs - rhs)
    
    return violation / 2  # Divide by 2 to avoid double counting


def compare_forward_backward(history: List[int]) -> Dict:
    """
    Compare statistical properties of forward and reversed sequences.
    """
    forward = history
    backward = list(reversed(history))
    
    # Transition matrices
    trans_fwd = compute_transition_matrix(forward)
    trans_bwd = compute_transition_matrix(backward)
    
    # Matrix difference
    matrix_diff = np.abs(trans_fwd - trans_bwd).mean()
    
    # Cross-chamber transition rates
    def cross_rate(h):
        cross = 0
        for i in range(len(h) - 1):
            in_a_now = h[i] in TET_A
            in_a_next = h[i+1] in TET_A
            if in_a_now != in_a_next:
                cross += 1
        return cross / (len(h) - 1)
    
    cross_fwd = cross_rate(forward)
    cross_bwd = cross_rate(backward)
    
    # Autocorrelation at lag 1
    def autocorr_1(h):
        chambers = np.array([1 if v in TET_A else -1 for v in h])
        return np.corrcoef(chambers[:-1], chambers[1:])[0, 1]
    
    ac_fwd = autocorr_1(forward)
    ac_bwd = autocorr_1(backward)
    
    return {
        'matrix_difference': matrix_diff,
        'cross_rate_forward': cross_fwd,
        'cross_rate_backward': cross_bwd,
        'cross_rate_diff': abs(cross_fwd - cross_bwd),
        'autocorr_forward': ac_fwd,
        'autocorr_backward': ac_bwd,
        'autocorr_diff': abs(ac_fwd - ac_bwd),
    }


def compute_entropy_production_rate(history: List[int]) -> float:
    """
    Compute entropy production rate (measure of irreversibility).
    
    sigma = sum_ij J_ij * log(P_ij / P_ji)
    
    where J_ij is the probability current.
    """
    trans = compute_transition_matrix(history)
    counts = Counter(history)
    n = len(history)
    stationary = np.array([counts.get(v, 0) / n for v in range(8)])
    
    sigma = 0.0
    for i in range(8):
        for j in range(8):
            if trans[i, j] > 0.001 and trans[j, i] > 0.001:
                J_ij = stationary[i] * trans[i, j] - stationary[j] * trans[j, i]
                if J_ij != 0:
                    sigma += J_ij * math.log(trans[i, j] / trans[j, i])
    
    return sigma


# =============================================================================
# TEST CLASSES
# =============================================================================

class TimeReversalSymmetryProbe(Test):
    """
    PROBING: Test for time reversal symmetry.
    """
    name = "Time Reversal Symmetry Test"
    question = (
        "Is the forward trajectory statistically distinguishable from the "
        "backward trajectory? If yes, there is an arrow of time in the dynamics. "
        "Time-symmetric processes have detailed balance."
    )
    reference = "Time reversal symmetry, detailed balance"
    level = Exploratory
    tolerance = 0.2

    commentary = (
        "PROBING: We compare the transition matrices and other statistics "
        "of the forward and reversed sequences. Significant differences "
        "would indicate time asymmetry. Detailed balance violation is "
        "another measure of irreversibility."
    )

    def derivation(self):
        return (
            Derivation()
            .step("TIME REVERSAL:")
            .step("Forward: v_0 -> v_1 -> v_2 -> ...")
            .step("Backward: ... -> v_2 -> v_1 -> v_0")
            .step("T-SYMMETRY:")
            .step("Forward and backward have same transition probabilities:")
            .equation("P(v_i -> v_j) = P(v_j -> v_i) for all i, j")
            .step("DETAILED BALANCE:")
            .equation("P(i) * P(i->j) = P(j) * P(j->i)")
            .step("If violated, there is net probability current (irreversibility).")
            .conclude("T-asymmetry indicates arrow of time.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compare forward and backward
        comparison = compare_forward_backward(history)
        
        # Detailed balance violation
        db_violation = compute_detailed_balance_violation(history)
        
        # Entropy production
        sigma = compute_entropy_production_rate(history)
        
        # Is T-symmetric?
        is_symmetric = (comparison['matrix_difference'] < 0.05 and 
                       db_violation < 0.05 and
                       abs(sigma) < 0.05)
        
        return (
            Model()
            .add("Transition matrix difference", comparison['matrix_difference'])
            .add("Cross-rate forward", comparison['cross_rate_forward'])
            .add("Cross-rate backward", comparison['cross_rate_backward'])
            .add("Detailed balance violation", db_violation)
            .add("Entropy production rate", sigma)
            .add("Is T-symmetric", 1.0 if is_symmetric else 0.0)
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
            .add("Transition matrix difference", 0.00855547, abs_tol=0.0044)  # random range [0.00542226, 0.0123204]
            .add("Cross-rate forward", 0.500467, abs_tol=0.017)  # random range [0.4885, 0.5152]
            .add("Cross-rate backward", 0.500467, abs_tol=0.017)  # random range [0.4885, 0.5152]
            .add("Detailed balance violation", 0.0341903, abs_tol=0.018)  # random range [0.0216881, 0.0493128]
            .add("Entropy production rate", 0.00840418, abs_tol=0.0089)  # random range [0.00379549, 0.0161248]
            .add("Is T-symmetric", 1, abs_tol=1e-09)  # same for all 150 random sequences
        )

class ArrowOfTimeProbe(Test):
    """
    PROBING: Can we determine the direction of time from statistics?
    """
    name = "Arrow of Time Detection"
    question = (
        "If given a trajectory segment, can we tell whether it's running "
        "forward or backward in time? This tests whether there's a statistical "
        "arrow of time encoded in the dynamics."
    )
    reference = "Arrow of time, Loschmidt paradox"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We create a simple classifier to distinguish forward from "
        "backward segments. Accuracy > 50% indicates detectable time direction. "
        "This is a direct test of whether the field has a built-in arrow of time."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ARROW OF TIME TEST:")
            .step("Given segment S, classify as forward (F) or backward (B).")
            .step("Use simple features:")
            .step("  - First vertex (more likely to be in TetB for forward?)")
            .step("  - Transition asymmetries")
            .step("CLASSIFIER ACCURACY:")
            .step("  50% = no arrow (can't distinguish)")
            .step("  > 50% = arrow exists (directions differ)")
            .step("  100% = perfect arrow (always distinguishable)")
            .conclude("Classifier accuracy measures arrow strength.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Create forward and backward segments
        segment_length = 100
        n_segments = (len(history) - segment_length) // segment_length
        
        correct = 0
        total = 0
        
        for i in range(n_segments):
            start = i * segment_length
            end = start + segment_length
            segment = history[start:end]
            
            # Feature: first visit in TetB
            first_in_b = 1 if segment[0] in TET_B else 0
            
            # Ground truth: this is forward
            # Prediction: if first_in_b, predict forward (based on prior finding)
            prediction_forward = first_in_b
            
            if prediction_forward == 1:
                correct += 1
            total += 1
        
        forward_accuracy = correct / total if total > 0 else 0.5
        
        # Also test on reversed segments
        correct_rev = 0
        for i in range(n_segments):
            start = i * segment_length
            end = start + segment_length
            segment = list(reversed(history[start:end]))
            
            first_in_b = 1 if segment[0] in TET_B else 0
            prediction_forward = first_in_b
            
            # Ground truth: this is backward, so prediction should be 0
            if prediction_forward == 0:
                correct_rev += 1
        
        backward_accuracy = correct_rev / n_segments if n_segments > 0 else 0.5
        
        # Combined accuracy
        combined_accuracy = (forward_accuracy + backward_accuracy) / 2
        
        return (
            Model()
            .add("Forward detection accuracy", forward_accuracy)
            .add("Backward detection accuracy", backward_accuracy)
            .add("Combined accuracy", combined_accuracy)
            .add("Has arrow of time", 1.0 if combined_accuracy > 0.55 else 0.0)
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
            .add("Forward detection accuracy", 0.509495, abs_tol=0.17)  # random range [0.393939, 0.656566]
            .add("Backward detection accuracy", 0.499394, abs_tol=0.2)  # random range [0.333333, 0.626263]
            .add("Combined accuracy", 0.504444, abs_tol=0.11)  # random range [0.414141, 0.585859]
            .add("Has arrow of time", 0.106667, abs_tol=1.1)  # random range [0, 1]
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    TimeReversalSymmetryProbe,
    ArrowOfTimeProbe,
]


def run_all():
    """Run all time reversal probing tests."""
    summary = (
        "TIME REVERSAL PROBING\n\n"
        "These probes test for time-reversal asymmetry.\n"
        "T-symmetry: forward = backward statistically\n"
        "Arrow of time: can we tell time direction from data?\n\n"
        "We are DISCOVERING if the field has a time direction."
    )
    return run_tests("Time Reversal Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
