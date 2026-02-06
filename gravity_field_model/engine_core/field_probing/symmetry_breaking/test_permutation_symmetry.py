"""
Permutation Symmetry Probing
============================

PROBING QUESTION: Are all vertices treated equally, or are some preferred?

The 8 vertices of the Merkaba should ideally be equivalent.
This probe tests whether the dynamics shows preference for certain vertices.

MATHEMATICAL FOUNDATION:
- Symmetry group: S_8 (permutations of 8 vertices) or subgroup
- Equiprobability: P(v) = 1/8 for all vertices
- Preference: P(v_i) != P(v_j) for some i, j

NULL HYPOTHESIS: Uniform vertex distribution
DISCOVERY: Non-uniform distribution indicates symmetry reduction

Reference: Permutation symmetry, degeneracy lifting
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter
from scipy import stats

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def compute_vertex_distribution(history: List[int]) -> np.ndarray:
    """
    Compute probability distribution over 8 vertices.
    """
    counts = Counter(history)
    n = len(history)
    
    distribution = np.zeros(8)
    for v in range(8):
        distribution[v] = counts.get(v, 0) / n
    
    return distribution


def chi_squared_test(observed: np.ndarray, expected: np.ndarray) -> Dict:
    """
    Chi-squared test for goodness of fit.
    
    H0: observed comes from expected distribution
    """
    # Scale to counts
    n = 10000  # Effective sample size for chi-squared
    obs_counts = observed * n
    exp_counts = expected * n
    
    chi2 = np.sum((obs_counts - exp_counts) ** 2 / exp_counts)
    dof = len(observed) - 1
    p_value = 1 - stats.chi2.cdf(chi2, dof)
    
    return {
        'chi_squared': chi2,
        'dof': dof,
        'p_value': p_value,
        'is_uniform': p_value > 0.05,
    }


def test_vertex_pair_symmetry(history: List[int]) -> Dict:
    """
    Test symmetry between complementary vertex pairs.
    
    In the Merkaba, vertices may come in complementary pairs.
    """
    counts = Counter(history)
    n = len(history)
    
    # TetA vertices
    teta_counts = [counts.get(v, 0) for v in TET_A]
    # TetB vertices
    tetb_counts = [counts.get(v, 0) for v in TET_B]
    
    # Within-chamber symmetry
    teta_max_ratio = max(teta_counts) / min(teta_counts) if min(teta_counts) > 0 else float('inf')
    tetb_max_ratio = max(tetb_counts) / min(tetb_counts) if min(tetb_counts) > 0 else float('inf')
    
    return {
        'teta_counts': teta_counts,
        'tetb_counts': tetb_counts,
        'teta_max_min_ratio': teta_max_ratio,
        'tetb_max_min_ratio': tetb_max_ratio,
        'within_teta_symmetric': teta_max_ratio < 1.2,
        'within_tetb_symmetric': tetb_max_ratio < 1.2,
    }


def compute_vertex_entropy(distribution: np.ndarray) -> float:
    """
    Compute entropy of vertex distribution.
    
    Maximum entropy = log(8) for uniform distribution.
    """
    entropy = 0.0
    for p in distribution:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def analyze_transition_symmetry(history: List[int]) -> Dict:
    """
    Test if transition probabilities respect vertex symmetry.
    
    P(i -> j) should depend only on the relationship between i and j,
    not on the specific values of i and j.
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
    
    # Test: are all rows similar? (permutation symmetry would mean identical rows)
    row_stds = np.std(trans_matrix, axis=0)
    mean_row_std = np.mean(row_stds)
    
    # Test: is the matrix approximately bistochastic (row and column sums equal)?
    col_sums = trans_matrix.sum(axis=0)
    col_sum_std = np.std(col_sums)
    
    return {
        'transition_matrix': trans_matrix,
        'mean_row_variability': mean_row_std,
        'column_sum_variability': col_sum_std,
        'is_symmetric': mean_row_std < 0.1 and col_sum_std < 0.1,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class VertexEquiprobabilityProbe(Test):
    """
    PROBING: Are all 8 vertices visited with equal probability?
    """
    name = "Vertex Equiprobability Test"
    question = (
        "Does the traversal visit all 8 vertices with equal frequency? "
        "Deviation from uniform distribution indicates that some vertices "
        "are 'preferred' by the dynamics."
    )
    reference = "Equiprobability, chi-squared test"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We use chi-squared test to compare observed vertex counts "
        "against uniform expectation. Significant deviation would indicate "
        "the permutation symmetry is broken."
    )

    def derivation(self):
        return (
            Derivation()
            .step("EQUIPROBABILITY:")
            .step("For 8 vertices, uniform distribution:")
            .equation("P(v) = 1/8 = 0.125 for all v")
            .step("CHI-SQUARED TEST:")
            .equation("chi^2 = sum_v (O_v - E_v)^2 / E_v")
            .step("O_v = observed count, E_v = expected count")
            .step("Under H0, chi^2 follows chi^2(7) distribution.")
            .step("p < 0.05: reject uniformity")
            .conclude("Chi-squared tests permutation symmetry.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute distribution
        dist = compute_vertex_distribution(history)
        
        # Chi-squared test against uniform
        uniform = np.ones(8) / 8
        chi2_result = chi_squared_test(dist, uniform)
        
        # Distribution entropy
        entropy = compute_vertex_entropy(dist)
        max_entropy = math.log2(8)
        
        # Min and max probabilities
        min_p = np.min(dist)
        max_p = np.max(dist)
        
        return (
            Model()
            .add("Min vertex probability", min_p)
            .add("Max vertex probability", max_p)
            .add("Max/min ratio", max_p / min_p if min_p > 0 else float('inf'))
            .add("Distribution entropy", entropy)
            .add("Max entropy", max_entropy)
            .add("Chi-squared statistic", chi2_result['chi_squared'])
            .add("p-value", chi2_result['p_value'])
            .add("Is uniform", 1.0 if chi2_result['is_uniform'] else 0.0)
        )

    def observations(self):
        # NULL: Uniform distribution
        return (
            Observed()
            .add("Min vertex probability", 0.125)
            .add("Max vertex probability", 0.125)
            .add("Max/min ratio", 1.0)
            .add("Distribution entropy", 3.0)
            .add("Max entropy", 3.0)
            .add("Chi-squared statistic", 0.0)
            .add("p-value", 1.0)
            .add("Is uniform", 1.0)
        )


class TransitionSymmetryProbe(Test):
    """
    PROBING: Do transition probabilities respect vertex symmetry?
    """
    name = "Transition Symmetry Test"
    question = (
        "Are the transition probabilities symmetric? If all vertices are "
        "equivalent, the probability of going from i to j should depend "
        "only on the 'type' of transition (same chamber, cross chamber, etc.), "
        "not on the specific vertices."
    )
    reference = "Markov chain symmetry, permutation invariance"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We analyze the transition matrix for symmetry. In a "
        "permutation-symmetric system, all rows should be similar (just "
        "permuted versions of each other). Large row variability indicates "
        "vertices are not equivalent."
    )

    def derivation(self):
        return (
            Derivation()
            .step("TRANSITION SYMMETRY:")
            .step("Transition matrix: P[i,j] = P(next=j | current=i)")
            .step("PERMUTATION INVARIANCE:")
            .step("For symmetric dynamics, P[i,j] depends only on")
            .step("the relationship between i and j, not specific values.")
            .step("TEST: Row variability")
            .step("If rows are similar, row_std is small.")
            .step("Large row variability means vertices behave differently.")
            .conclude("Row variability measures transition symmetry.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Analyze transition symmetry
        trans_analysis = analyze_transition_symmetry(history)
        
        # Also test within-chamber symmetry
        pair_symmetry = test_vertex_pair_symmetry(history)
        
        return (
            Model()
            .add("Mean row variability", trans_analysis['mean_row_variability'])
            .add("Column sum variability", trans_analysis['column_sum_variability'])
            .add("TetA vertex ratio", pair_symmetry['teta_max_min_ratio'])
            .add("TetB vertex ratio", pair_symmetry['tetb_max_min_ratio'])
            .add("Is transition symmetric", 1.0 if trans_analysis['is_symmetric'] else 0.0)
        )

    def observations(self):
        # NULL: Symmetric transitions
        return (
            Observed()
            .add("Mean row variability", 0.0)
            .add("Column sum variability", 0.0)
            .add("TetA vertex ratio", 1.0)
            .add("TetB vertex ratio", 1.0)
            .add("Is transition symmetric", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    VertexEquiprobabilityProbe,
    TransitionSymmetryProbe,
]


def run_all():
    """Run all permutation symmetry probing tests."""
    summary = (
        "PERMUTATION SYMMETRY PROBING\n\n"
        "These probes test if all vertices are treated equally.\n"
        "Equiprobability: P(v) = 1/8 for all v\n"
        "Transition symmetry: P[i,j] depends only on relationship\n\n"
        "We are DISCOVERING vertex-level symmetry."
    )
    return run_tests("Permutation Symmetry Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
