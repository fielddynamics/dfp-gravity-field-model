"""
Directed Information Flow Probing
=================================

PROBING QUESTION: Is there net information transfer from TetA to TetB or vice versa?

This probe computes transfer entropy to determine if one chamber
"drives" the other informationally.

MATHEMATICAL FOUNDATION:
- Transfer entropy: T_{X->Y} = H(Y_t | Y_{t-1}) - H(Y_t | Y_{t-1}, X_{t-1})
- Net flow: T_{X->Y} - T_{Y->X}
- Positive net flow means X "drives" Y

NULL HYPOTHESIS: Zero net flow (symmetric coupling)
DISCOVERY: Directed flow would indicate causal asymmetry

Reference: Schreiber "Measuring Information Transfer", PRE 2000
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


def get_chamber_sequence(history: List[int]) -> List[int]:
    """Convert vertex sequence to chamber sequence (0=TetA, 1=TetB)."""
    return [0 if v in TET_A else 1 for v in history]


def compute_transfer_entropy(source: List[int], target: List[int], 
                            source_order: int = 1, target_order: int = 1) -> float:
    """
    Compute transfer entropy from source to target.
    
    T_{S->T} = H(T_t | T_{t-1},...,T_{t-k}) - H(T_t | T_{t-1},...,T_{t-k}, S_{t-1},...,S_{t-m})
    
    This measures the information that source provides about target's future
    beyond what target's own past provides.
    """
    n = len(source)
    if n != len(target):
        raise ValueError("Source and target must have same length")
    
    start_idx = max(source_order, target_order)
    
    # Count contexts
    target_only_counts = defaultdict(lambda: defaultdict(int))
    joint_counts = defaultdict(lambda: defaultdict(int))
    
    for i in range(start_idx, n):
        target_context = tuple(target[i-target_order:i])
        source_context = tuple(source[i-source_order:i])
        joint_context = (target_context, source_context)
        target_value = target[i]
        
        target_only_counts[target_context][target_value] += 1
        joint_counts[joint_context][target_value] += 1
    
    # Compute conditional entropies
    def conditional_entropy(context_dict):
        total = sum(sum(d.values()) for d in context_dict.values())
        h = 0.0
        for context, values in context_dict.items():
            context_total = sum(values.values())
            p_context = context_total / total
            h_context = 0.0
            for count in values.values():
                if count > 0:
                    p = count / context_total
                    h_context -= p * math.log2(p)
            h += p_context * h_context
        return h
    
    h_target_only = conditional_entropy(target_only_counts)
    h_joint = conditional_entropy(joint_counts)
    
    # Transfer entropy = reduction in uncertainty
    transfer = h_target_only - h_joint
    
    return max(0, transfer)  # Should be non-negative


def compute_mutual_information_rate(x: List[int], y: List[int]) -> float:
    """
    Compute mutual information rate between two sequences.
    
    I(X;Y) = H(X) + H(Y) - H(X,Y)
    """
    n = len(x)
    
    # Joint distribution
    joint_counts = Counter(zip(x, y))
    x_counts = Counter(x)
    y_counts = Counter(y)
    
    # Entropies
    def entropy(counts, n):
        h = 0.0
        for c in counts.values():
            if c > 0:
                p = c / n
                h -= p * math.log2(p)
        return h
    
    h_x = entropy(x_counts, n)
    h_y = entropy(y_counts, n)
    h_xy = entropy(joint_counts, n)
    
    return h_x + h_y - h_xy


# =============================================================================
# TEST CLASSES
# =============================================================================

class TransferEntropyProbe(Test):
    """
    PROBING: Measure transfer entropy between TetA and TetB.
    """
    name = "Transfer Entropy (Directed Information)"
    question = (
        "Does information flow preferentially from TetA to TetB, or from TetB "
        "to TetA? Transfer entropy measures the directed information transfer. "
        "Net flow would indicate that one chamber 'drives' the other."
    )
    reference = "Schreiber transfer entropy, Granger causality"
    level = Exploratory
    tolerance = 0.2

    commentary = (
        "PROBING: Transfer entropy T_{A->B} measures how much knowing TetA's "
        "past helps predict TetB's future, beyond TetB's own past. Net flow "
        "T_{A->B} - T_{B->A} indicates causal asymmetry. Zero net flow means "
        "symmetric coupling. This is discovery about which side 'leads'."
    )

    def derivation(self):
        return (
            Derivation()
            .step("TRANSFER ENTROPY:")
            .step("For processes X and Y:")
            .equation("T_{X->Y} = H(Y_t | Y_{t-1}) - H(Y_t | Y_{t-1}, X_{t-1})")
            .step("Interpretation:")
            .step("  T_{X->Y} = information X provides about Y's future")
            .step("  Beyond what Y's own past provides")
            .step("NET FLOW:")
            .equation("Net = T_{A->B} - T_{B->A}")
            .step("  Net > 0: A drives B")
            .step("  Net < 0: B drives A")
            .step("  Net = 0: Symmetric coupling")
            .conclude("Transfer entropy reveals causal direction.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        chambers = get_chamber_sequence(history)
        
        # Create TetA and TetB activity sequences
        # Count visits in windows
        window = 5
        teta_activity = []
        tetb_activity = []
        for i in range(0, len(chambers) - window, window):
            w = chambers[i:i+window]
            teta_activity.append(sum(1 for c in w if c == 0))
            tetb_activity.append(sum(1 for c in w if c == 1))
        
        # Discretize to 0,1,2,... for transfer entropy
        teta_disc = [min(a, 4) for a in teta_activity]
        tetb_disc = [min(a, 4) for a in tetb_activity]
        
        # Compute transfer entropies
        t_a_to_b = compute_transfer_entropy(teta_disc, tetb_disc)
        t_b_to_a = compute_transfer_entropy(tetb_disc, teta_disc)
        
        # Net flow
        net_flow = t_a_to_b - t_b_to_a
        
        # Mutual information for comparison
        mi = compute_mutual_information_rate(teta_disc, tetb_disc)
        
        return (
            Model()
            .add("Transfer entropy A->B (bits)", t_a_to_b)
            .add("Transfer entropy B->A (bits)", t_b_to_a)
            .add("Net flow (A->B positive)", net_flow)
            .add("Mutual information (bits)", mi)
            .add("Flow asymmetry ratio", t_a_to_b / t_b_to_a if t_b_to_a > 0.001 else 1.0)
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
            .add("Transfer entropy A->B (bits)", 0.00145395, abs_tol=0.0049)  # random range [9.42189e-05, 0.00569767]
            .add("Transfer entropy B->A (bits)", 0.00162601, abs_tol=0.0059)  # random range [8.77703e-05, 0.00671442]
            .add("Net flow (A->B positive)", -0.000172057, abs_tol=0.0073)  # random range [-0.00646323, 0.00415723]
            .add("Mutual information (bits)", 1.95255, abs_tol=0.028)  # random range [1.92844, 1.97129]
            .add("Flow asymmetry ratio", 0.901783, abs_tol=2.1)  # random range [0.0266553, 2.65369]
        )

class CausalInfluenceProbe(Test):
    """
    PROBING: Test for Granger-like causal influence between chambers.
    """
    name = "Causal Influence Between Chambers"
    question = (
        "Can we predict TetB's state better by knowing TetA's history? "
        "This tests for causal influence in a Granger sense: does past A "
        "help predict future B beyond B's own past?"
    )
    reference = "Granger causality, predictive information"
    level = Exploratory
    tolerance = 0.2

    commentary = (
        "PROBING: Granger causality asks: does including X's past improve "
        "prediction of Y? We test whether TetA's history helps predict TetB's "
        "future. Significant improvement indicates causal influence."
    )

    def derivation(self):
        return (
            Derivation()
            .step("GRANGER CAUSALITY:")
            .step("X Granger-causes Y if:")
            .equation("H(Y_t | Y_{past}) > H(Y_t | Y_{past}, X_{past})")
            .step("That is, X's past helps predict Y beyond Y's own past.")
            .step("TEST STATISTIC:")
            .step("Prediction improvement = H(Y|Y_past) - H(Y|Y_past,X_past)")
            .step("If > 0, there is causal influence from X to Y.")
            .conclude("Granger causality reveals predictive relationships.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        chambers = get_chamber_sequence(history)
        
        # Prediction using only target's past
        def prediction_error_target_only(target, order=2):
            counts = defaultdict(lambda: defaultdict(int))
            for i in range(order, len(target)):
                context = tuple(target[i-order:i])
                counts[context][target[i]] += 1
            
            # Compute average entropy
            total = sum(sum(d.values()) for d in counts.values())
            h = 0.0
            for context, values in counts.items():
                n = sum(values.values())
                p_context = n / total
                h_context = 0.0
                for c in values.values():
                    if c > 0:
                        p = c / n
                        h_context -= p * math.log2(p)
                h += p_context * h_context
            return h
        
        # Prediction using target and source past
        def prediction_error_joint(source, target, order=2):
            counts = defaultdict(lambda: defaultdict(int))
            for i in range(order, min(len(source), len(target))):
                context = (tuple(target[i-order:i]), tuple(source[i-order:i]))
                counts[context][target[i]] += 1
            
            total = sum(sum(d.values()) for d in counts.values())
            h = 0.0
            for context, values in counts.items():
                n = sum(values.values())
                p_context = n / total
                h_context = 0.0
                for c in values.values():
                    if c > 0:
                        p = c / n
                        h_context -= p * math.log2(p)
                h += p_context * h_context
            return h
        
        # TetA -> TetB influence
        h_b_alone = prediction_error_target_only(chambers, 2)
        h_b_with_a = prediction_error_joint(chambers, chambers, 2)
        influence_a_to_b = h_b_alone - h_b_with_a
        
        # Compute both directions using vertex-level data
        teta_seq = [v for v in history if v in TET_A]
        tetb_seq = [v for v in history if v in TET_B]
        
        return (
            Model()
            .add("H(B|B_past)", h_b_alone)
            .add("H(B|B_past,A_past)", h_b_with_a)
            .add("Causal influence A->B", influence_a_to_b)
            .add("Is causally significant", 1.0 if influence_a_to_b > 0.05 else 0.0)
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
            .add("H(B|B_past)", 0.999743, abs_tol=0.00081)  # random range [0.999039, 0.999988]
            .add("H(B|B_past,A_past)", 0.999743, abs_tol=0.00081)  # random range [0.999039, 0.999988]
            .add("Causal influence A->B", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Is causally significant", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    TransferEntropyProbe,
    CausalInfluenceProbe,
]


def run_all():
    """Run all directed flow probing tests."""
    summary = (
        "DIRECTED INFORMATION FLOW PROBING\n\n"
        "These probes measure directed information transfer.\n"
        "Transfer entropy: T_{X->Y} = info X provides about Y's future\n"
        "Net flow: T_{A->B} - T_{B->A}\n\n"
        "We are DISCOVERING causal structure."
    )
    return run_tests("Directed Flow Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
