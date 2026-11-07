"""
Causal Horizon Probing
======================

PROBING QUESTION: Is the Field Origin a true information bottleneck?

This probe tests whether the Field Origin "screens off" TetA from TetB,
meaning all information between them must pass through the origin.

MATHEMATICAL FOUNDATION:
- Conditional independence: A _||_ B | O means A and B are independent given O
- Screening: I(A;B|O) = 0 if O screens A from B
- Transfer via origin: I(A;B) = I(A;O) + I(O;B) - I(O)

NULL HYPOTHESIS: Origin is just geometric center (no special causal role)
DISCOVERY: If origin screens, it's a true causal bottleneck

Reference: Causal inference, d-separation, information bottleneck
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


def detect_origin_crossings(history: List[int]) -> List[int]:
    """
    Detect when trajectory crosses through the origin (chamber changes).
    
    Returns: sequence of 0 (no crossing) or 1 (crossing at this step)
    """
    chambers = get_chamber_sequence(history)
    crossings = [0]  # First step has no prior
    for i in range(1, len(chambers)):
        if chambers[i] != chambers[i-1]:
            crossings.append(1)
        else:
            crossings.append(0)
    return crossings


def compute_conditional_mutual_information(x: List[int], y: List[int], z: List[int]) -> float:
    """
    Compute I(X;Y|Z) = H(X|Z) + H(Y|Z) - H(X,Y|Z)
    
    This measures the information X and Y share that isn't explained by Z.
    If Z screens X from Y, then I(X;Y|Z) = 0.
    """
    n = len(x)
    
    # Count joint occurrences
    xyz_counts = Counter(zip(x, y, z))
    xz_counts = Counter(zip(x, z))
    yz_counts = Counter(zip(y, z))
    z_counts = Counter(z)
    
    # Compute conditional entropies
    def entropy(counts, n):
        h = 0.0
        for c in counts.values():
            if c > 0:
                p = c / n
                h -= p * math.log2(p)
        return h
    
    h_xyz = entropy(xyz_counts, n)
    h_xz = entropy(xz_counts, n)
    h_yz = entropy(yz_counts, n)
    h_z = entropy(z_counts, n)
    
    # I(X;Y|Z) = H(X,Z) + H(Y,Z) - H(X,Y,Z) - H(Z)
    cmi = h_xz + h_yz - h_xyz - h_z
    
    return max(0, cmi)  # Should be non-negative


def compute_information_decomposition(a: List[int], b: List[int], o: List[int]) -> Dict:
    """
    Decompose mutual information I(A;B) into parts via O.
    
    I(A;B) = I(A;B;O) + I(A;B|O)
    
    Where I(A;B;O) is the co-information (can be negative).
    """
    n = len(a)
    
    # Joint counts
    ab_counts = Counter(zip(a, b))
    ao_counts = Counter(zip(a, o))
    bo_counts = Counter(zip(b, o))
    abo_counts = Counter(zip(a, b, o))
    a_counts = Counter(a)
    b_counts = Counter(b)
    o_counts = Counter(o)
    
    def entropy(counts, n):
        h = 0.0
        for c in counts.values():
            if c > 0:
                p = c / n
                h -= p * math.log2(p)
        return h
    
    h_a = entropy(a_counts, n)
    h_b = entropy(b_counts, n)
    h_o = entropy(o_counts, n)
    h_ab = entropy(ab_counts, n)
    h_ao = entropy(ao_counts, n)
    h_bo = entropy(bo_counts, n)
    h_abo = entropy(abo_counts, n)
    
    # Mutual informations
    i_ab = h_a + h_b - h_ab
    i_ao = h_a + h_o - h_ao
    i_bo = h_b + h_o - h_bo
    
    # Co-information (can be negative)
    i_abo = h_a + h_b + h_o - h_ab - h_ao - h_bo + h_abo
    
    # Conditional MI
    i_ab_given_o = h_ao + h_bo - h_abo - h_o
    
    return {
        'I(A;B)': i_ab,
        'I(A;O)': i_ao,
        'I(B;O)': i_bo,
        'I(A;B;O)': i_abo,
        'I(A;B|O)': max(0, i_ab_given_o),
        'screening_ratio': i_ab_given_o / i_ab if i_ab > 0.01 else 0,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class OriginScreeningProbe(Test):
    """
    PROBING: Does the Field Origin screen TetA from TetB?
    """
    name = "Origin Screening (Causal Bottleneck)"
    question = (
        "Is the Field Origin a true information bottleneck? If conditioning on "
        "whether we just crossed the origin makes TetA and TetB independent, "
        "then the origin 'screens' them: all information flows THROUGH it."
    )
    reference = "Causal inference, conditional independence, d-separation"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We test if I(TetA;TetB|Origin) = 0. If so, the origin "
        "is a true causal bottleneck: knowing whether we crossed tells us "
        "everything about the TetA-TetB relationship. Non-zero conditional MI "
        "means there's direct TetA-TetB information not mediated by origin."
    )

    def derivation(self):
        return (
            Derivation()
            .step("SCREENING (CONDITIONAL INDEPENDENCE):")
            .step("O screens A from B if:")
            .equation("I(A;B|O) = 0")
            .step("Meaning: given O, A provides no additional info about B.")
            .step("INFORMATION DECOMPOSITION:")
            .equation("I(A;B) = I(A;B;O) + I(A;B|O)")
            .step("If I(A;B|O) = 0, all A-B information flows via O.")
            .step("SCREENING RATIO:")
            .equation("r = I(A;B|O) / I(A;B)")
            .step("  r = 0: perfect screening (origin is bottleneck)")
            .step("  r = 1: no screening (direct A-B connection)")
            .conclude("Screening ratio reveals causal structure.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Define A = TetA activity, B = TetB activity, O = crossing indicator
        chambers = get_chamber_sequence(history)
        crossings = detect_origin_crossings(history)
        
        # Use windowed activity
        window = 3
        a_activity = []
        b_activity = []
        o_activity = []
        
        for i in range(window, len(history)):
            # Activity in window before
            w = chambers[i-window:i]
            a_activity.append(sum(1 for c in w if c == 0))
            b_activity.append(sum(1 for c in w if c == 1))
            # Did we cross in this window?
            o_activity.append(1 if any(crossings[i-window:i]) else 0)
        
        # Discretize
        a_disc = [min(a, 3) for a in a_activity]
        b_disc = [min(b, 3) for b in b_activity]
        
        # Compute information decomposition
        decomp = compute_information_decomposition(a_disc, b_disc, o_activity)
        
        # Conditional MI test
        cmi = compute_conditional_mutual_information(a_disc, b_disc, o_activity)
        
        return (
            Model()
            .add("I(TetA;TetB)", decomp['I(A;B)'])
            .add("I(TetA;Origin)", decomp['I(A;O)'])
            .add("I(TetB;Origin)", decomp['I(B;O)'])
            .add("I(TetA;TetB|Origin)", decomp['I(A;B|O)'])
            .add("Screening ratio", decomp['screening_ratio'])
            .add("Is origin a bottleneck", 1.0 if decomp['screening_ratio'] < 0.2 else 0.0)
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
            .add("I(TetA;TetB)", 1.80989, abs_tol=0.031)  # random range [1.78326, 1.83051]
            .add("I(TetA;Origin)", 0.292805, abs_tol=0.025)  # random range [0.271471, 0.313676]
            .add("I(TetB;Origin)", 0.292805, abs_tol=0.025)  # random range [0.271471, 0.313676]
            .add("I(TetA;TetB|Origin)", 1.51709, abs_tol=0.019)  # random range [1.50064, 1.52861]
            .add("Screening ratio", 0.838234, abs_tol=0.012)  # random range [0.828527, 0.847973]
            .add("Is origin a bottleneck", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class InformationFlowPathProbe(Test):
    """
    PROBING: What fraction of TetA-TetB information flows through the origin?
    """
    name = "Information Flow Path Analysis"
    question = (
        "How much of the TetA-TetB mutual information is mediated by the origin? "
        "We decompose I(A;B) into the part that flows through O and the direct part."
    )
    reference = "Information decomposition, partial information"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: Information can flow directly (A->B) or via mediator (A->O->B). "
        "We measure how much goes each way. High mediation fraction means "
        "the origin is central to TetA-TetB coupling."
    )

    def derivation(self):
        return (
            Derivation()
            .step("INFORMATION FLOW PATHS:")
            .step("Total information: I(A;B)")
            .step("Mediated by O: min(I(A;O), I(O;B))")
            .step("Direct (residual): I(A;B|O)")
            .step("MEDIATION FRACTION:")
            .equation("f_mediated = 1 - I(A;B|O)/I(A;B)")
            .step("f = 1: all info flows through O")
            .step("f = 0: no info flows through O")
            .conclude("Mediation fraction quantifies origin's role.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        chambers = get_chamber_sequence(history)
        crossings = detect_origin_crossings(history)
        
        # Compute various information quantities
        # Use single-step data for cleaner analysis
        a_state = [1 if c == 0 else 0 for c in chambers[:-1]]  # TetA at t
        b_state = [1 if c == 1 else 0 for c in chambers[1:]]   # TetB at t+1
        o_state = crossings[1:]  # Crossing at t+1
        
        decomp = compute_information_decomposition(a_state, b_state, o_state)
        
        # Mediation fraction
        mediation = 1 - decomp['screening_ratio'] if decomp['I(A;B)'] > 0.01 else 0
        
        # Information bottleneck: how much info about B does O capture?
        info_captured = decomp['I(B;O)'] / decomp['I(A;B)'] if decomp['I(A;B)'] > 0.01 else 0
        
        return (
            Model()
            .add("Total I(A;B)", decomp['I(A;B)'])
            .add("Direct I(A;B|O)", decomp['I(A;B|O)'])
            .add("Mediation fraction", mediation)
            .add("Info captured by origin", info_captured)
            .add("Co-information I(A;B;O)", decomp['I(A;B;O)'])
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
            .add("Total I(A;B)", 6.821e-05, abs_tol=0.00069)  # random range [5.2745e-10, 0.00066715]
            .add("Direct I(A;B|O)", 0.999875, abs_tol=0.0013)  # random range [0.99883, 1]
            .add("Mediation fraction", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Info captured by origin", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Co-information I(A;B;O)", -0.999806, abs_tol=0.0014)  # random range [-0.999999, -0.998651]
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    OriginScreeningProbe,
    InformationFlowPathProbe,
]


def run_all():
    """Run all causal horizon probing tests."""
    summary = (
        "CAUSAL HORIZON PROBING\n\n"
        "These probes test if the Field Origin is a causal bottleneck.\n"
        "Screening: I(A;B|O) = 0 means O blocks all A-B information\n"
        "Mediation: fraction of info that flows through O\n\n"
        "We are DISCOVERING the causal structure."
    )
    return run_tests("Causal Horizon Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
