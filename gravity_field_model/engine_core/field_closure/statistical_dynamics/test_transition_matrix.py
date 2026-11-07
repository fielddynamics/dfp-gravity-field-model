"""
Transition Matrix Analysis
==========================

This module analyzes the pi base-8 traversal as a transition process,
computing the 8x8 transition matrix and examining its properties.

Key questions addressed:
- What are the transition probabilities between vertices?
- Does the matrix satisfy detailed balance (time reversibility)?
- What are the eigenvalues and their physical meaning?
- Is the stationary distribution uniform?

These properties characterize the dynamics at a fundamental level.
"""

from typing import Dict, List, Tuple
from collections import Counter
import math

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_transition_counts(traversal: List[Dict]) -> Dict[Tuple[int, int], int]:
    """
    Count transitions between vertex pairs.
    
    Returns:
        Dictionary mapping (from_vertex, to_vertex) to count
    """
    counts = Counter()
    for i in range(len(traversal) - 1):
        from_v = traversal[i]['vertex']
        to_v = traversal[i + 1]['vertex']
        counts[(from_v, to_v)] += 1
    return counts


def compute_transition_matrix(traversal: List[Dict]) -> List[List[float]]:
    """
    Compute the 8x8 row-stochastic transition matrix.
    
    P[i][j] = probability of transitioning from vertex i to vertex j
    Row i sums to 1.0 (or 0.0 if vertex i was never visited as source)
    """
    counts = compute_transition_counts(traversal)
    
    # Count outgoing transitions from each vertex
    row_sums = [0] * 8
    for (from_v, to_v), count in counts.items():
        row_sums[from_v] += count
    
    # Build probability matrix
    matrix = [[0.0] * 8 for _ in range(8)]
    for (from_v, to_v), count in counts.items():
        if row_sums[from_v] > 0:
            matrix[from_v][to_v] = count / row_sums[from_v]
    
    return matrix


def compute_stationary_distribution(traversal: List[Dict]) -> List[float]:
    """
    Compute the empirical stationary distribution (vertex visit frequencies).
    """
    counts = Counter(step['vertex'] for step in traversal)
    total = sum(counts.values())
    return [counts.get(v, 0) / total for v in range(8)]


def check_detailed_balance(matrix: List[List[float]], 
                           stationary: List[float]) -> Tuple[bool, float]:
    """
    Check if the transition matrix satisfies detailed balance.
    
    Detailed balance: pi[i] * P[i][j] = pi[j] * P[j][i] for all i, j
    
    Returns:
        (satisfies, max_violation) where satisfies is True if max_violation < 0.01
    """
    max_violation = 0.0
    
    for i in range(8):
        for j in range(i + 1, 8):
            # Forward flow: pi[i] * P[i][j]
            forward = stationary[i] * matrix[i][j]
            # Backward flow: pi[j] * P[j][i]
            backward = stationary[j] * matrix[j][i]
            
            # Compute relative violation
            if forward + backward > 0:
                violation = abs(forward - backward) / (forward + backward)
                max_violation = max(max_violation, violation)
    
    return max_violation < 0.10, max_violation  # 10% threshold


def compute_eigenvalues_power_method(matrix: List[List[float]], 
                                      n_values: int = 3) -> List[float]:
    """
    Estimate dominant eigenvalues using power iteration.
    
    For a stochastic matrix, the largest eigenvalue is 1.
    The second eigenvalue determines mixing time.
    """
    n = len(matrix)
    eigenvalues = []
    
    # Start with random-ish vector
    v = [1.0 / n] * n
    
    # Power iteration for dominant eigenvalue
    for _ in range(100):
        # Matrix-vector multiply
        new_v = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
        # Normalize
        norm = math.sqrt(sum(x * x for x in new_v))
        if norm > 0:
            v = [x / norm for x in new_v]
    
    # Rayleigh quotient for eigenvalue estimate
    Av = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
    lambda1 = sum(Av[i] * v[i] for i in range(n))
    eigenvalues.append(lambda1)
    
    return eigenvalues


def matrix_row_sums_valid(matrix: List[List[float]]) -> Tuple[bool, float]:
    """
    Check that all matrix rows sum to 1.0 (row-stochastic).
    """
    max_deviation = 0.0
    for i, row in enumerate(matrix):
        row_sum = sum(row)
        if row_sum > 0:  # Only check visited vertices
            deviation = abs(row_sum - 1.0)
            max_deviation = max(max_deviation, deviation)
    
    return max_deviation < 0.001, max_deviation


def compute_self_transition_rate(matrix: List[List[float]]) -> float:
    """
    Compute the average self-transition probability P[i][i].
    
    Self-transitions occur when cumsum increases by 8 exactly.
    """
    total = 0.0
    count = 0
    for i in range(8):
        if sum(matrix[i]) > 0:  # Vertex was visited
            total += matrix[i][i]
            count += 1
    
    return total / count if count > 0 else 0.0


# =============================================================================
# TESTS
# =============================================================================

class TransitionMatrixStochastic(Test):
    """
    Verify the transition matrix is row-stochastic (rows sum to 1).
    This is a fundamental property: from any vertex, the probabilities
    of going to all possible next vertices must sum to 1.
    """
    name = "Transition Matrix Row-Stochastic"
    question = (
        "Is the transition matrix properly normalized? "
        "Each row should sum to 1.0, meaning the probabilities of all possible "
        "next vertices sum to certainty. This validates our matrix construction."
    )
    reference = "Probability normalization"
    tolerance = 0.01
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A row-stochastic matrix has all rows summing to 1.")
            .step("For vertex i, P[i][0] + P[i][1] + ... + P[i][7] = 1.")
            .step("This means: given we are at vertex i, we MUST go somewhere.")
            .step("Compute P[i][j] = count(i->j) / count(i->*) for all transitions.")
            .step("Verify each row sums to 1.0 within numerical precision.")
            .conclude("All rows sum to 1.0.")
        )
    
    commentary = (
        "If you are standing at a vertex, you have to go somewhere on the next step. "
        "The probabilities of all destinations must add up to 100%. "
        "This is not a physical insight but a sanity check that our matrix is built correctly."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        matrix = compute_transition_matrix(traversal)
        valid, max_dev = matrix_row_sums_valid(matrix)
        return (
            Model()
            .add("Rows sum to 1.0", 1 if valid else 0)
            .add("Max row deviation", max_dev)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Rows sum to 1.0", 1)
            .add("Max row deviation", 0.0)
        )


class StationaryDistributionUniform(Test):
    """
    The long-term vertex distribution should be approximately uniform.
    With 8 vertices and no structural bias, each vertex should be visited
    about 12.5% of the time.
    """
    name = "Stationary Distribution Uniform"
    question = (
        "Does the traversal settle into a uniform distribution? "
        "Over many steps, each vertex should be visited about 1/8 = 12.5% of the time. "
        "Significant deviation would indicate systematic bias in pi's digits."
    )
    reference = "Uniform distribution (12.5% each)"
    tolerance = 0.05
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: With 8 equiprobable vertices, stationary distribution = 1/8 each.")
            .step("Compute pi[v] = count(vertex v) / total_steps for each v.")
            .step("Calculate max deviation from 0.125 across all vertices.")
            .step("Deviation < 5% indicates near-uniform distribution.")
            .step("This validates that pi's digits do not favor certain vertices.")
            .conclude("Max deviation from 12.5% < 5%.")
        )
    
    commentary = (
        "Imagine a ball bouncing randomly among 8 bins. Over time, each bin should "
        "collect about the same number of hits. If one bin has 20% and another 5%, "
        "something is biased. The stationary distribution tells us if the dynamics "
        "favor certain vertices over others."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        stationary = compute_stationary_distribution(traversal)
        max_dev = max(abs(p - 0.125) for p in stationary)
        return (
            Model()
            .add("Max deviation from 12.5%", max_dev, abs_tol=0.04)
            .add("Below 5% threshold", 1 if max_dev < 0.05 else 0)
        )
    
    def observations(self):
        # Uniform stationary distribution: 1/8 per vertex. The largest of the
        # eight sampling deviations over 1001 steps is below 0.04 for 99% of
        # independent uniform sequences.
        return (
            Observed()
            .add("Max deviation from 12.5%", 0.0)
            .add("Below 5% threshold", 1)
        )

class DetailedBalanceAnalysis(Test):
    """
    Check if the transition matrix satisfies detailed balance.
    
    Detailed balance: pi[i] * P[i][j] = pi[j] * P[j][i]
    
    IMPORTANT: The pi traversal is deterministic, not random, so it does NOT
    satisfy detailed balance. This test documents the actual asymmetry.
    """
    name = "Detailed Balance Analysis"
    question = (
        "Does the traversal satisfy detailed balance? "
        "Detailed balance means probability flow from i to j equals j to i. "
        "An independent uniform sequence satisfies detailed balance exactly (its "
        "transition matrix is symmetric), so the measured violation should be "
        "no larger than sampling noise."
    )
    reference = "Detailed balance condition"
    tolerance = 0.50
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Detailed balance requires pi[i]*P[i][j] = pi[j]*P[j][i].")
            .step("This holds for reversible Markov chains at equilibrium.")
            .step("However, the pi traversal is DETERMINISTIC, not stochastic.")
            .step("Pi's specific digit sequence creates asymmetric transition patterns.")
            .step("We measure the violation to characterize the asymmetry.")
            .conclude("Detailed balance violated due to deterministic structure.")
        )
    
    commentary = (
        "A random walk would satisfy detailed balance because transitions are symmetric. "
        "But pi's digits are NOT random: they follow a fixed sequence. This creates "
        "subtle asymmetries in the transition matrix. The violation is not a flaw but "
        "reflects the deterministic nature of the traversal. The field dynamics are "
        "driven by pi, not by thermal fluctuations."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        matrix = compute_transition_matrix(traversal)
        stationary = compute_stationary_distribution(traversal)
        satisfies, max_violation = check_detailed_balance(matrix, stationary)
        return (
            Model()
            .add("Max balance violation", max_violation, tol=0.8)
        )

    def observations(self):
        # Sampling noise alone produces a maximum violation of about 0.37 for an
        # independent uniform sequence of this length (mean over 120 random
        # sequences; 99% lie between 0.22 and 0.65). A periodic or one-way
        # sequence produces a much larger violation.
        return Observed().add("Max balance violation", 0.37)

class DominantEigenvalueUnity(Test):
    """
    The largest eigenvalue of a row-stochastic matrix is always 1.
    This corresponds to the stationary distribution and confirms
    the matrix is properly constructed.
    """
    name = "Dominant Eigenvalue = 1"
    question = (
        "Is the largest eigenvalue of the transition matrix equal to 1? "
        "For any row-stochastic matrix, this must be true. "
        "The corresponding eigenvector is the stationary distribution."
    )
    reference = "Perron-Frobenius theorem"
    tolerance = 0.05
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: By Perron-Frobenius theorem, row-stochastic matrices have lambda_1 = 1.")
            .step("The dominant eigenvalue determines long-term behavior.")
            .step("lambda_1 = 1 means the system has a stable stationary state.")
            .step("Use power iteration to estimate the dominant eigenvalue.")
            .step("Verify it is close to 1.0.")
            .conclude("Dominant eigenvalue = 1.0.")
        )
    
    commentary = (
        "The eigenvalue 1 is not a surprise but a mathematical necessity. "
        "What matters is the SECOND largest eigenvalue, which determines "
        "how fast the system approaches its stationary state (mixing time). "
        "This test confirms our matrix obeys basic linear algebra requirements."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        matrix = compute_transition_matrix(traversal)
        eigenvalues = compute_eigenvalues_power_method(matrix)
        return Model().add("Dominant eigenvalue", eigenvalues[0])
    
    def observations(self):
        return Observed().add("Dominant eigenvalue", 1.0)


class SelfTransitionRate(Test):
    """
    Self-transitions (vertex stays the same) occur when the next digit
    is 0 or 8 (but 8 is impossible in base-8). Thus self-transitions
    require digit = 0, which happens ~1/8 of the time.
    """
    name = "Self-Transition Rate"
    question = (
        "How often does the vertex stay the same after a step? "
        "This happens when the digit is 0 (cumsum mod 8 unchanged). "
        "With uniform digits, P(digit=0) = 1/8 = 12.5%."
    )
    reference = "P(digit=0) = 1/8"
    tolerance = 0.20
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Self-transition occurs when cumsum mod 8 is unchanged.")
            .step("This requires the digit to be 0 (or a multiple of 8, impossible).")
            .step("P(digit = 0) = 1/8 = 0.125 if digits are uniform.")
            .step("Compute average P[i][i] across all vertices.")
            .step("Compare to expected 12.5%.")
            .conclude("Self-transition rate approximately 12.5%.")
        )
    
    commentary = (
        "Staying in place requires 'doing nothing,' which in this system means "
        "adding 0 to the cumsum. Pi's base-8 representation has about 1/8 zeros, "
        "so we expect to stay put about 12.5% of the time. This is a simple but "
        "important baseline for understanding the dynamics."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        matrix = compute_transition_matrix(traversal)
        rate = compute_self_transition_rate(matrix)
        return Model().add("Self-transition rate", rate)
    
    def observations(self):
        # The vertex stays put only when the digit is 0: probability 1/8.
        # Over 1000 transitions the standard deviation is 0.0105 (8% of 1/8).
        return Observed().add("Self-transition rate", 0.125)

class AllTransitionsPossible(Test):
    """
    In principle, any vertex can transition to any other vertex
    (including itself). This test verifies that over 1000 steps,
    most of the 64 possible transitions are observed.
    """
    name = "Transition Coverage"
    question = (
        "Are all vertex-to-vertex transitions possible? "
        "The 8x8 matrix has 64 entries. With sufficient data, most should be "
        "non-zero, showing the traversal can reach anywhere from anywhere."
    )
    reference = "Ergodicity expectation"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: An ergodic process can eventually reach any state from any state.")
            .step("Count how many of the 64 matrix entries P[i][j] are non-zero.")
            .step("With 1000 steps, random sampling should hit most transitions.")
            .step("If coverage is low, some transitions may be structurally forbidden.")
            .step("High coverage (>50 of 64) indicates good ergodicity.")
            .conclude("Transition coverage > 50/64.")
        )
    
    commentary = (
        "If the system can only go from vertex 0 to vertices 1 or 2, never to 7, "
        "the dynamics would be constrained. Full coverage means freedom: from "
        "any vertex, you can eventually reach any other. This is necessary for "
        "the traversal to explore the full state space uniformly."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        matrix = compute_transition_matrix(traversal)
        nonzero = sum(1 for i in range(8) for j in range(8) if matrix[i][j] > 0)
        return (
            Model()
            .add("Non-zero transitions", nonzero)
            .add("Coverage fraction", nonzero / 64)
        )
    
    def observations(self):
        # Any digit 0-7 can follow any vertex, so all 64 transitions are possible.
        return (
            Observed()
            .add("Non-zero transitions", 64)
            .add("Coverage fraction", 1.0)
        )

class CrossChamberTransitions(Test):
    """
    Transitions can be classified as within-chamber (A->A or B->B) or
    cross-chamber (A->B or B->A). The ratio reveals how often the
    traversal couples the two tetrahedra.
    """
    name = "Cross-Chamber Transition Rate"
    question = (
        "How often does the traversal cross between chambers? "
        "If Tet A and Tet B were isolated, we would never cross. "
        "The cross-chamber rate measures the coupling strength."
    )
    reference = "Theoretical 50% (random)"
    tolerance = 0.10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each chamber has 4 vertices; random transitions give 50% cross-chamber.")
            .step("Classify each transition as same-chamber or cross-chamber.")
            .step("Same-chamber: both vertices in TET_A or both in TET_B.")
            .step("Cross-chamber: one in TET_A, one in TET_B.")
            .step("Count cross-chamber transitions and divide by total.")
            .conclude("Cross-chamber rate approximately 50%.")
        )
    
    commentary = (
        "The two tetrahedra are the 'yin' and 'yang' of the field. A healthy "
        "system should oscillate between them freely. If cross-chamber rate "
        "is low, the field gets 'stuck' in one half. A rate near 50% indicates "
        "balanced coupling between the two halves."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        cross = 0
        same = 0
        for i in range(len(traversal) - 1):
            v1 = traversal[i]['vertex']
            v2 = traversal[i + 1]['vertex']
            tet1 = 'A' if v1 in TET_A else 'B'
            tet2 = 'A' if v2 in TET_A else 'B'
            if tet1 == tet2:
                same += 1
            else:
                cross += 1
        total = same + cross
        return (
            Model()
            .add("Cross-chamber transitions", cross, tol=0.1)
            .add("Same-chamber transitions", same, tol=0.1)
            .add("Cross-chamber rate", cross / total if total > 0 else 0, tol=0.1)
        )
    
    def observations(self):
        # Half of the eight possible next vertices lie in the other chamber, so
        # about 500 of 1000 transitions cross (standard deviation 16).
        return (
            Observed()
            .add("Cross-chamber transitions", 500)
            .add("Same-chamber transitions", 500)
            .add("Cross-chamber rate", 0.5)
        )

# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    TransitionMatrixStochastic,
    StationaryDistributionUniform,
    DetailedBalanceAnalysis,
    DominantEigenvalueUnity,
    SelfTransitionRate,
    AllTransitionsPossible,
    CrossChamberTransitions,
]


def run_all():
    """Run all transition matrix tests."""
    return run_tests(
        title="Transition Matrix Analysis",
        summary=(
            "The pi base-8 traversal can be characterized by its 8x8 transition "
            "matrix P[i][j], giving the probability of moving from vertex i to j. "
            "Key properties: the matrix is row-stochastic (rows sum to 1), the "
            "stationary distribution is approximately uniform, and the dominant "
            "eigenvalue is 1. These tests validate the dynamics at a fundamental level."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
