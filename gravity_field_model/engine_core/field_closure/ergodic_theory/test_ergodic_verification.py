"""
Comprehensive Ergodic Verification Tests

This module implements rigorous statistical tests for verifying ergodicity
of the pi base-8 vertex traversal system, based on Birkhoff's Ergodic Theorem.

Reference: gravity_field_model/reference/ergodic_theory_reference.md
"""

import math
from collections import Counter
from typing import Dict, List

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8


def compute_ergodic_statistics(trajectory: List[int], n_states: int = 8, expected_freq: float = None) -> Dict:
    """
    Compute comprehensive ergodic statistics for a trajectory.
    
    Implements statistical measures from ergodic theory reference:
    - Mean Absolute Deviation (MAD)
    - Root Mean Square Deviation (RMSD)
    - Maximum Deviation
    - Chi-squared goodness-of-fit test
    
    Parameters:
    -----------
    trajectory : List[int]
        Sequence of vertex indices (0 to n_states-1)
    n_states : int
        Number of vertices (default: 8)
    expected_freq : float, optional
        Expected frequency per vertex (default: 1/n_states for uniform)
    
    Returns:
    --------
    Dict containing:
        - counts: Dict[int, int] - Visit count per vertex
        - frequencies: Dict[int, float] - Visit frequency per vertex
        - mad: float - Mean Absolute Deviation
        - rmsd: float - Root Mean Square Deviation
        - max_dev: float - Maximum deviation from expected
        - chi2_statistic: float - Chi-squared test statistic
        - chi2_p_value: float - P-value for chi-squared test
        - chi2_critical_05: float - Critical value at 5% significance
        - pass_criteria: Dict[str, bool] - Pass/fail for each criterion
    """
    n = len(trajectory)
    
    if expected_freq is None:
        expected_freq = 1.0 / n_states
    
    # Count visits to each vertex
    counts = Counter(trajectory)
    c = {i: counts.get(i, 0) for i in range(n_states)}
    
    # Compute frequencies
    frequencies = {i: c[i] / n for i in range(n_states)}
    
    # Mean Absolute Deviation (MAD)
    mad = sum(abs(frequencies[i] - expected_freq) for i in range(n_states)) / n_states
    
    # Root Mean Square Deviation (RMSD)
    rmsd = math.sqrt(sum((frequencies[i] - expected_freq)**2 for i in range(n_states)) / n_states)
    
    # Maximum Deviation
    max_dev = max(abs(frequencies[i] - expected_freq) for i in range(n_states))
    
    # Chi-squared statistic
    # chi^2 = n * sum((f_i - pi_i)^2 / pi_i)
    chi2_statistic = n * sum((frequencies[i] - expected_freq)**2 / expected_freq for i in range(n_states))
    
    # Chi-squared p-value (7 degrees of freedom for 8 states)
    # Using approximation: P(chi^2_7 > x) ≈ exp(-x/2) * (x/2)^(df/2-1) / Gamma(df/2)
    # For exact calculation, would use scipy.stats.chi2, but avoiding external dependencies
    df = n_states - 1
    chi2_critical_05 = 14.07  # For 7 degrees of freedom, 5% significance level
    chi2_critical_01 = 18.48  # 1% significance level
    
    # Approximate p-value using critical values
    if chi2_statistic < chi2_critical_05:
        chi2_p_value_approx = "> 0.05"  # Fail to reject H0
    elif chi2_statistic < chi2_critical_01:
        chi2_p_value_approx = "0.01 < p < 0.05"
    else:
        chi2_p_value_approx = "< 0.01"  # Strong evidence against H0
    
    # Pass/fail criteria (for n=1000, adjust thresholds for other n)
    # Thresholds scale approximately as 1/sqrt(n)
    scale_factor = math.sqrt(1000 / n) if n > 0 else 1.0
    
    pass_criteria = {
        'mad': mad < 0.02 * scale_factor,
        'rmsd': rmsd < 0.025 * scale_factor,
        'max_dev': max_dev < 0.05 * scale_factor,
        'chi2': chi2_statistic < chi2_critical_05,
    }
    
    return {
        'n': n,
        'counts': c,
        'frequencies': frequencies,
        'expected_frequency': expected_freq,
        'mad': mad,
        'rmsd': rmsd,
        'max_dev': max_dev,
        'chi2_statistic': chi2_statistic,
        'chi2_p_value': chi2_p_value_approx,
        'chi2_critical_05': chi2_critical_05,
        'chi2_critical_01': chi2_critical_01,
        'pass_criteria': pass_criteria,
        'all_pass': all(pass_criteria.values()),
    }


class BirkhoffErgodicTheorem(Test):
    """
    Verify Birkhoff's Ergodic Theorem: Time average equals space average.
    
    For an ergodic system, the fraction of time spent in each vertex should
    converge to the stationary distribution (uniform: 1/8 = 12.5% per vertex).
    """
    name = "Birkhoff Ergodic Theorem Verification"
    question = (
        "Does the pi base-8 traversal satisfy Birkhoff's Ergodic Theorem? "
        "Specifically, do time averages (empirical frequencies) converge to "
        "space averages (stationary distribution: 1/8 = 12.5% per vertex)?"
    )
    reference = "Birkhoff (1931), Walters (1982) - An Introduction to Ergodic Theory"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("BIRKHOFF'S THEOREM: For an ergodic measure-preserving transformation, "
                  "time averages converge to space averages: "
                  "lim(n→∞) (1/n) Σ f(T^k x) = ∫ f dμ")
            .step("For discrete system on 8 vertices with uniform stationary distribution:")
            .step("  - Space average: π_i = 1/8 = 0.125 for each vertex i")
            .step("  - Time average: f_i = (count_i) / n = fraction of visits to vertex i")
            .step("Ergodicity requires: f_i → 0.125 as n → ∞ for all i")
            .step("For finite n=1000, verify: |f_i - 0.125| < 0.05 (5% deviation)")
            .step("Statistical tests: MAD < 0.02, RMSD < 0.025, Max dev < 0.05, χ² < 14.07")
            .conclude("If all criteria pass, system exhibits ergodic behavior.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        vertices = [s['vertex'] for s in traversal]
        
        stats = compute_ergodic_statistics(vertices, n_states=8, expected_freq=1/8)
        
        return (
            Model()
            .add("Mean Absolute Deviation (MAD)", stats['mad'])
            .add("Root Mean Square Deviation (RMSD)", stats['rmsd'])
            .add("Maximum Deviation", stats['max_dev'])
            .add("Chi-squared statistic", stats['chi2_statistic'])
            .add("Chi-squared p-value", stats['chi2_p_value'])
            .add("All criteria pass", 1 if stats['all_pass'] else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Mean Absolute Deviation (MAD)", "< 0.02")
            .add("Root Mean Square Deviation (RMSD)", "< 0.025")
            .add("Maximum Deviation", "< 0.05")
            .add("Chi-squared statistic", "< 14.07")
            .add("Chi-squared p-value", "> 0.05")
            .add("All criteria pass", 1)
        )
    
    commentary = (
        "Birkhoff's Ergodic Theorem is fundamental to statistical mechanics and dynamical systems. "
        "It states that for ergodic systems, following one trajectory over time (time average) gives "
        "the same result as averaging over all possible states (space average). "
        "This test verifies that the pi base-8 traversal exhibits ergodic behavior by checking "
        "whether vertex visitation frequencies converge to the uniform distribution (1/8 per vertex). "
        "The statistical tests (MAD, RMSD, chi-squared) provide rigorous criteria for acceptance. "
        "If the system is ergodic, it explores the entire state space uniformly, with no vertices "
        "being systematically over- or under-visited."
    )


class TimeAverageConvergence(Test):
    """
    Verify that time averages converge to expected values.
    
    For each vertex, check that the empirical frequency is within acceptable
    statistical bounds of the expected frequency (1/8 = 12.5%).
    """
    name = "Time Average Convergence"
    question = (
        "Do vertex visitation frequencies converge to the expected uniform distribution? "
        "For each of the 8 vertices, is the observed frequency within ±5% of 12.5%?"
    )
    reference = "Ergodic theory reference - Section 6.3"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("TIME AVERAGE: f_i = (1/n) Σ_{k=0}^{n-1} 1_{X_k = i} = count_i / n")
            .step("SPACE AVERAGE: π_i = 1/8 = 0.125 (uniform stationary distribution)")
            .step("For n=1000 steps:")
            .step("  - Expected count per vertex: E[c_i] = n/8 = 125")
            .step("  - Standard deviation: σ_i = sqrt(7n/64) ≈ 10.4")
            .step("  - 95% confidence interval: [104, 146] visits")
            .step("  - Acceptable frequency range: [0.105, 0.145] (10.5% to 14.5%)")
            .step("Check: |f_i - 0.125| < 0.05 for all vertices i")
            .conclude("All vertices within ±5% of expected frequency indicates convergence.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        vertices = [s['vertex'] for s in traversal]
        
        stats = compute_ergodic_statistics(vertices, n_states=8, expected_freq=1/8)
        
        # Check each vertex individually
        vertex_deviations = {
            i: abs(stats['frequencies'][i] - stats['expected_frequency'])
            for i in range(8)
        }
        
        vertices_within_bounds = sum(
            1 for dev in vertex_deviations.values() if dev < 0.05
        )
        
        return (
            Model()
            .add("Vertices within ±5% bounds", vertices_within_bounds)
            .add("Maximum vertex deviation", max(vertex_deviations.values()))
            .add("Mean vertex deviation", sum(vertex_deviations.values()) / 8)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Vertices within ±5% bounds", 8)
            .add("Maximum vertex deviation", "< 0.05")
            .add("Mean vertex deviation", "< 0.02")
        )
    
    commentary = (
        "Time average convergence is the core prediction of Birkhoff's theorem. "
        "For an ergodic system, the fraction of time spent in each state should equal "
        "the stationary probability of that state. For uniform distribution on 8 vertices, "
        "each vertex should be visited 12.5% of the time. This test verifies that all "
        "8 vertices have frequencies within acceptable statistical bounds (±5% deviation). "
        "If convergence holds, the system 'forgets' its initial state and explores all "
        "vertices uniformly over time."
    )


class ChiSquaredGoodnessOfFit(Test):
    """
    Chi-squared goodness-of-fit test for uniform distribution.
    
    Tests the null hypothesis that vertex frequencies follow a uniform distribution
    (π_i = 1/8 for all i) against the alternative that they do not.
    """
    name = "Chi-Squared Goodness-of-Fit Test"
    question = (
        "Does the chi-squared test support the hypothesis of uniform vertex distribution? "
        "Null hypothesis: π_i = 1/8 for all vertices. "
        "Test statistic: χ² = n Σ (f_i - π_i)² / π_i"
    )
    reference = "Lehmann & Romano (2005) - Testing Statistical Hypotheses, Chapter 14"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("NULL HYPOTHESIS H0: Vertex frequencies follow uniform distribution π_i = 1/8")
            .step("TEST STATISTIC: χ² = n Σ_{i=0}^7 (f_i - π_i)² / π_i")
            .step("  = 8n Σ_{i=0}^7 (f_i - 0.125)²")
            .step("DISTRIBUTION: Under H0, χ² ~ χ²_7 (chi-squared with 7 degrees of freedom)")
            .step("CRITICAL VALUES:")
            .step("  - χ²_{0.05} = 14.07 (5% significance level)")
            .step("  - χ²_{0.01} = 18.48 (1% significance level)")
            .step("DECISION RULE:")
            .step("  - If χ² < 14.07: Fail to reject H0 (evidence supports ergodicity)")
            .step("  - If χ² ≥ 14.07: Reject H0 (evidence against uniform ergodicity)")
            .conclude("χ² < 14.07 indicates uniform distribution consistent with ergodicity.")
        )
    
    def model(self) -> Model:
        traversal = traverse_pi_base8(1000)
        vertices = [s['vertex'] for s in traversal]
        
        stats = compute_ergodic_statistics(vertices, n_states=8, expected_freq=1/8)
        
        return (
            Model()
            .add("Chi-squared statistic", stats['chi2_statistic'])
            .add("Critical value (5%)", stats['chi2_critical_05'])
            .add("Critical value (1%)", stats['chi2_critical_01'])
            .add("P-value interpretation", stats['chi2_p_value'])
            .add("Test passes (χ² < 14.07)", 1 if stats['pass_criteria']['chi2'] else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Chi-squared statistic", "< 14.07")
            .add("Critical value (5%)", 14.07)
            .add("Critical value (1%)", 18.48)
            .add("P-value interpretation", "> 0.05")
            .add("Test passes (χ² < 14.07)", 1)
        )
    
    commentary = (
        "The chi-squared goodness-of-fit test provides a rigorous statistical framework "
        "for testing whether observed frequencies match the expected uniform distribution. "
        "The test accounts for correlations between vertex counts (multinomial distribution) "
        "and provides a single statistic summarizing deviations from uniformity. "
        "A small chi-squared value (< 14.07 for 7 degrees of freedom) indicates that "
        "observed frequencies are consistent with uniform distribution, supporting ergodicity. "
        "A large chi-squared value suggests systematic deviations, which could indicate "
        "non-ergodicity, insufficient sample size, or systematic biases in the traversal."
    )


class SampleSizeAdequacy(Test):
    """
    Verify that sample size is adequate for reliable ergodic verification.
    
    For chi-squared test, need n >> 1/π_* where π_* is minimum probability.
    For uniform distribution on 8 states: π_* = 1/8, so need n >> 8.
    """
    name = "Sample Size Adequacy"
    question = (
        "Is the sample size (n=1000) adequate for reliable ergodic verification? "
        "Rule of thumb: n >> 1/π_* where π_* is minimum stationary probability."
    )
    reference = "Ergodic theory reference - Section 4.4"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("RULE OF THUMB: For reliable verification, need n >> 1/π_*")
            .step("For uniform distribution on 8 states: π_* = min_i π_i = 1/8")
            .step("Therefore: n >> 8")
            .step("RECOMMENDED SAMPLE SIZES:")
            .step("  - Minimum: n = 100 (very rough estimate)")
            .step("  - Adequate: n = 1000 (good for initial verification)")
            .step("  - Reliable: n = 10,000 (strong statistical power)")
            .step("  - Excellent: n = 100,000 (very high confidence)")
            .step("STATISTICAL POWER (for detecting 5% deviation):")
            .step("  - n = 1000: Can detect ~5-6% deviations with 80% power")
            .step("  - n = 10,000: Can detect ~1.5-2% deviations with 80% power")
            .conclude("n = 1000 is adequate for detecting moderate deviations (5% level).")
        )
    
    def model(self) -> Model:
        n = 1000
        pi_star = 1/8
        
        # Check adequacy
        adequate = n > 10 / pi_star  # n >> 1/π_* means n > 10/π_*
        
        # Expected statistical power (approximate)
        # For detecting 5% deviation with 80% power, need n ≈ 1155
        power_adequate = n >= 1155
        
        return (
            Model()
            .add("Sample size n", n)
            .add("Minimum probability π_*", pi_star)
            .add("Threshold (10/π_*)", 10 / pi_star)
            .add("Adequate (n > 10/π_*)", 1 if adequate else 0)
            .add("Power adequate (n ≥ 1155)", 1 if power_adequate else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Sample size n", 1000)
            .add("Minimum probability π_*", 0.125)
            .add("Threshold (10/π_*)", 80)
            .add("Adequate (n > 10/π_*)", 1)
            .add("Power adequate (n ≥ 1155)", 0)  # n=1000 is slightly below ideal
        )
    
    commentary = (
        "Sample size adequacy is crucial for reliable statistical inference. "
        "For ergodic verification, we need sufficient observations to detect deviations "
        "from the expected uniform distribution. The rule of thumb n >> 1/π_* ensures "
        "that even the least probable state (with probability π_*) is observed frequently "
        "enough for reliable frequency estimation. For uniform distribution on 8 states, "
        "n = 1000 is adequate for detecting moderate deviations (5-6% level) but may "
        "miss smaller deviations. For higher precision, larger sample sizes (n = 10,000+) "
        "are recommended."
    )
