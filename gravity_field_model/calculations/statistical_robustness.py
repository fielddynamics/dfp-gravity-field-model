"""
Statistical Robustness Methods for Discrete Sequence Validation

This module provides expert-level statistical methods for validating properties
of discrete sequences visiting 8 states. Includes concentration inequalities,
subsample stability testing, bootstrap confidence intervals, and long-range
correlation analysis.

References:
- Hoeffding (1963): Concentration inequalities
- Efron & Tibshirani (1993): Bootstrap methods
- Peng et al. (1994): Detrended Fluctuation Analysis
"""

import math
from typing import Dict, List, Tuple, Callable, Optional
from collections import Counter
import numpy as np

try:
    from scipy.stats import chi2
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not available. Chi-square tests will use manual implementation.")


# =============================================================================
# CONCENTRATION INEQUALITIES
# =============================================================================

def hoeffding_deviation(n: int, confidence: float = 0.95) -> float:
    """
    Compute maximum deviation at given confidence level using Hoeffding bound.
    
    For vertex counts in an 8-state uniform sequence:
    P(|count_v - n/8| > t) <= 2 * exp(-2t^2 / n)
    
    Args:
        n: Sequence length
        confidence: Confidence level (default 0.95 for 95%)
    
    Returns:
        Maximum deviation t such that P(|S_n - n/8| > t) <= (1 - confidence)
    
    Example:
        >>> hoeffding_deviation(1000, 0.95)
        42.95...  # At 95% confidence, counts should be within n/8 ± 43
    """
    alpha = 1 - confidence
    t = math.sqrt(-n * math.log(alpha / 2) / 2)
    return t


def check_vertex_counts(counts: Dict[int, int], n: int, confidence: float = 0.95) -> Dict:
    """
    Check if vertex counts are within Hoeffding bounds.
    
    Args:
        counts: Dictionary mapping vertex -> count
        n: Total sequence length
        confidence: Confidence level
    
    Returns:
        Dictionary with pass/fail status for each vertex
    
    Example:
        >>> counts = {0: 125, 1: 130, 2: 120, ...}
        >>> results = check_vertex_counts(counts, 1000)
        >>> results[0]['pass']  # True if within bounds
    """
    expected = n / 8
    threshold = hoeffding_deviation(n, confidence)
    
    results = {}
    for vertex in range(8):
        count = counts.get(vertex, 0)
        deviation = abs(count - expected)
        results[vertex] = {
            'count': count,
            'expected': expected,
            'deviation': deviation,
            'threshold': threshold,
            'pass': deviation <= threshold,
            'relative_deviation': deviation / expected if expected > 0 else 0
        }
    
    results['overall_pass'] = all(r['pass'] for r in results.values())
    return results


# =============================================================================
# SUBSAMPLE STABILITY TESTING
# =============================================================================

def chi_square_test(counts1: Dict[int, int], counts2: Dict[int, int], 
                    n1: int, n2: int) -> Dict:
    """
    Perform chi-square test comparing two vertex count distributions.
    
    Null hypothesis: Both subsets follow the same uniform distribution.
    
    Args:
        counts1: Vertex counts for subset 1
        counts2: Vertex counts for subset 2
        n1: Size of subset 1
        n2: Size of subset 2
    
    Returns:
        Dictionary with test statistic, p-value, and pass/fail status
    
    Example:
        >>> counts1 = Counter(sequence[:500])
        >>> counts2 = Counter(sequence[500:])
        >>> result = chi_square_test(counts1, counts2, 500, 500)
        >>> result['pass']  # True if subsets are similar
    """
    chi2_stat = 0.0
    expected1 = n1 / 8
    expected2 = n2 / 8
    
    for vertex in range(8):
        obs1 = counts1.get(vertex, 0)
        obs2 = counts2.get(vertex, 0)
        
        chi2_stat += (obs1 - expected1)**2 / expected1
        chi2_stat += (obs2 - expected2)**2 / expected2
    
    df = 7  # 8 vertices - 1
    critical_value = 14.07  # χ²₀.₀₅,₇
    
    if SCIPY_AVAILABLE:
        p_value = 1 - chi2.cdf(chi2_stat, df)
    else:
        # Manual approximation for p-value (less accurate)
        p_value = 0.05 if chi2_stat >= critical_value else 0.5
    
    return {
        'chi2_statistic': chi2_stat,
        'p_value': p_value,
        'critical_value': critical_value,
        'degrees_of_freedom': df,
        'pass': chi2_stat < critical_value,
        'interpretation': 'Subsets are similar' if chi2_stat < critical_value else 'Subsets differ significantly'
    }


def subsample_stability_test(sequence: List[int], method: str = 'half') -> Dict:
    """
    Test stability by comparing subsets.
    
    Args:
        sequence: List of vertex indices
        method: 'half' for first/second half, 'odd_even' for odd/even positions
    
    Returns:
        Test results dictionary
    
    Example:
        >>> sequence = [0, 1, 2, ...]  # 1000 elements
        >>> result = subsample_stability_test(sequence, method='half')
        >>> result['pass']  # True if subsets are statistically similar
    """
    n = len(sequence)
    
    if method == 'half':
        subset1 = sequence[:n//2]
        subset2 = sequence[n//2:]
    elif method == 'odd_even':
        subset1 = sequence[::2]  # Even indices
        subset2 = sequence[1::2]  # Odd indices
    else:
        raise ValueError("method must be 'half' or 'odd_even'")
    
    counts1 = Counter(subset1)
    counts2 = Counter(subset2)
    
    return chi_square_test(counts1, counts2, len(subset1), len(subset2))


# =============================================================================
# BOOTSTRAP CONFIDENCE INTERVALS
# =============================================================================

def bootstrap_ci(sequence: List[int], statistic_func: Callable[[List[int]], float],
                 B: int = 10000, confidence: float = 0.95) -> Dict:
    """
    Compute bootstrap confidence interval for a statistic.
    
    Args:
        sequence: Original sequence
        statistic_func: Function that computes statistic from a sequence
        B: Number of bootstrap samples (default 10000)
        confidence: Confidence level (default 0.95)
    
    Returns:
        Dictionary with CI bounds and bootstrap distribution
    
    Example:
        >>> def entropy_stat(seq):
        ...     counts = Counter(seq)
        ...     n = len(seq)
        ...     return -sum((c/n)*math.log2(c/n) for c in counts.values() if c > 0)
        >>> ci = bootstrap_ci(sequence, entropy_stat, B=10000)
        >>> ci['ci_lower'], ci['ci_upper']  # 95% CI bounds
    """
    n = len(sequence)
    bootstrap_stats = []
    
    # Use numpy for efficient random sampling
    seq_array = np.array(sequence)
    
    for _ in range(B):
        # Sample with replacement
        bootstrap_sample = np.random.choice(seq_array, size=n, replace=True)
        stat = statistic_func(bootstrap_sample.tolist())
        bootstrap_stats.append(stat)
    
    bootstrap_stats = np.sort(bootstrap_stats)
    
    alpha = 1 - confidence
    lower_idx = int(alpha/2 * B)
    upper_idx = int((1 - alpha/2) * B)
    
    ci_lower = bootstrap_stats[lower_idx]
    ci_upper = bootstrap_stats[upper_idx]
    
    return {
        'statistic': statistic_func(sequence),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'ci_width': float(ci_upper - ci_lower),
        'bootstrap_mean': float(np.mean(bootstrap_stats)),
        'bootstrap_std': float(np.std(bootstrap_stats)),
        'bootstrap_median': float(np.median(bootstrap_stats))
    }


def entropy_statistic(sequence: List[int]) -> float:
    """
    Compute Shannon entropy of a sequence.
    
    Args:
        sequence: List of vertex indices
    
    Returns:
        Shannon entropy in bits
    """
    counts = Counter(sequence)
    total = len(sequence)
    if total == 0:
        return 0.0
    
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    
    return entropy


def balance_statistic(sequence: List[int], category_func: Callable[[int], int]) -> float:
    """
    Compute balance metric for binary categorization.
    
    Args:
        sequence: List of vertex indices
        category_func: Function mapping vertex -> category (0 or 1)
    
    Returns:
        Balance metric: min(p_A, p_B) / max(p_A, p_B)
    """
    counts = Counter(category_func(v) for v in sequence)
    total = len(sequence)
    
    if total == 0:
        return 0.0
    
    p_A = counts.get(0, 0) / total
    p_B = counts.get(1, 0) / total
    
    if p_A == 0 or p_B == 0:
        return 0.0
    
    return min(p_A, p_B) / max(p_A, p_B)


# =============================================================================
# LONG-RANGE CORRELATION ANALYSIS
# =============================================================================

def autocorrelation_large_lags(sequence: List[int], max_lag: int = 100) -> Dict:
    """
    Compute autocorrelation at large lags and detect periodic patterns.
    
    Args:
        sequence: Sequence of vertex indices
        max_lag: Maximum lag to compute
    
    Returns:
        Dictionary with autocorrelation values and detected periods
    
    Example:
        >>> result = autocorrelation_large_lags(sequence, max_lag=100)
        >>> result['autocorr'][10]  # Autocorrelation at lag 10
        >>> result['periods']  # List of detected periodic patterns
    """
    n = len(sequence)
    max_lag = min(max_lag, n // 4)
    
    # Convert to numeric array
    seq_array = np.array(sequence, dtype=float)
    mean = np.mean(seq_array)
    variance = np.var(seq_array)
    
    if variance == 0:
        return {
            'autocorr': [1.0] + [0.0] * max_lag,
            'threshold': 2 / math.sqrt(n),
            'peaks': [],
            'periods': []
        }
    
    autocorr = [1.0]  # R(0) = 1
    for k in range(1, max_lag + 1):
        if k >= n:
            break
        covariance = np.mean((seq_array[:-k] - mean) * (seq_array[k:] - mean))
        autocorr.append(covariance / variance)
    
    # Statistical threshold (95% confidence for random sequence)
    threshold = 2 / math.sqrt(n)
    
    # Find significant peaks (potential periods)
    peaks = []
    for k in range(1, len(autocorr)):
        if abs(autocorr[k]) > threshold:
            peaks.append((k, autocorr[k]))
    
    # Detect periodic patterns
    periods = []
    if peaks:
        peak_lags = [p[0] for p in peaks]
        # Check if peaks occur at multiples
        for base_period in range(2, min(20, max_lag // 2)):
            multiples = [base_period * m for m in range(1, max_lag // base_period + 1)]
            matches = [lag for lag in peak_lags if lag in multiples]
            if len(matches) >= 2:  # At least 2 multiples
                periods.append({
                    'period': base_period,
                    'multiples': matches,
                    'strength': float(np.mean([abs(autocorr[lag]) for lag in matches]))
                })
    
    return {
        'autocorr': [float(r) for r in autocorr],
        'threshold': float(threshold),
        'peaks': [(int(k), float(r)) for k, r in peaks],
        'periods': periods,
        'max_autocorr': float(max(abs(r) for r in autocorr[1:]) if len(autocorr) > 1 else 0.0)
    }


def dfa_exponent(sequence: List[int], window_sizes: Optional[List[int]] = None) -> Dict:
    """
    Compute DFA (Detrended Fluctuation Analysis) scaling exponent.
    
    DFA measures long-range correlations:
    - α ≈ 0.5: Random (no long-range correlation)
    - α > 0.5: Persistent (positive correlation)
    - α < 0.5: Anti-persistent (negative correlation)
    
    Args:
        sequence: Sequence of vertex indices
        window_sizes: List of window sizes (default: powers of 2)
    
    Returns:
        Dictionary with DFA exponent and fluctuations
    
    Example:
        >>> result = dfa_exponent(sequence)
        >>> result['alpha']  # Scaling exponent (should be ~0.5 for random)
        >>> result['interpretation']  # 'random', 'persistent', or 'anti-persistent'
    """
    if window_sizes is None:
        n = len(sequence)
        max_power = int(math.log2(n)) - 1
        window_sizes = [2**i for i in range(2, max_power)]
    
    seq_array = np.array(sequence, dtype=float)
    mean = np.mean(seq_array)
    
    # Integrate: Y(i) = Σⱼ (X(j) - mean)
    integrated = np.cumsum(seq_array - mean)
    
    fluctuations = []
    valid_window_sizes = []
    
    for s in window_sizes:
        if s >= len(integrated) or s < 4:
            continue
        
        # Divide into windows
        n_windows = len(integrated) // s
        if n_windows < 2:
            continue
        
        F_s = []
        for i in range(n_windows):
            window = integrated[i*s:(i+1)*s]
            indices = np.arange(len(window))
            
            # Fit linear trend
            coeffs = np.polyfit(indices, window, 1)
            trend = np.polyval(coeffs, indices)
            
            # Fluctuation
            F_s.append(math.sqrt(np.mean((window - trend)**2)))
        
        if F_s:
            fluctuations.append(np.mean(F_s))
            valid_window_sizes.append(s)
    
    # Fit power law: F(s) ~ s^α
    if len(fluctuations) < 2:
        return {
            'alpha': 0.5,
            'fluctuations': [],
            'interpretation': 'insufficient_data'
        }
    
    log_s = np.log(valid_window_sizes)
    log_F = np.log(fluctuations)
    
    # Linear regression: log(F) = α * log(s) + c
    alpha = np.polyfit(log_s, log_F, 1)[0]
    
    interpretation = 'random'
    if alpha > 0.55:
        interpretation = 'persistent'
    elif alpha < 0.45:
        interpretation = 'anti-persistent'
    
    return {
        'alpha': float(alpha),
        'fluctuations': [(int(s), float(f)) for s, f in zip(valid_window_sizes, fluctuations)],
        'interpretation': interpretation
    }


# =============================================================================
# COMPREHENSIVE VALIDATION
# =============================================================================

def comprehensive_validation(sequence: List[int], 
                            category_func: Optional[Callable[[int], int]] = None) -> Dict:
    """
    Perform comprehensive statistical validation of 8-state sequence.
    
    Args:
        sequence: Sequence of vertex indices (0-7)
        category_func: Optional function for binary categorization (e.g., tetrahedron)
    
    Returns:
        Dictionary with all test results and overall pass/fail status
    
    Example:
        >>> sequence = [0, 1, 2, 3, 4, 5, 6, 7] * 125  # n=1000, uniform
        >>> results = comprehensive_validation(sequence)
        >>> results['overall_pass']  # True if all tests pass
        >>> results['tests']['entropy']['entropy']  # Shannon entropy value
    """
    n = len(sequence)
    results = {
        'sequence_length': n,
        'tests': {},
        'overall_pass': True,
        'warnings': []
    }
    
    # Check minimum sample size
    if n < 1000:
        results['warnings'].append(f"Sample size {n} < 1000. Some tests may be unreliable.")
    
    # 1. Vertex count uniformity
    counts = Counter(sequence)
    vertex_results = check_vertex_counts(counts, n)
    results['tests']['vertex_uniformity'] = {
        'pass': vertex_results['overall_pass'],
        'details': {k: v for k, v in vertex_results.items() if k != 'overall_pass'}
    }
    if not vertex_results['overall_pass']:
        results['overall_pass'] = False
    
    # 2. Entropy
    entropy = entropy_statistic(sequence)
    entropy_test = {
        'entropy': entropy,
        'max_entropy': 3.0,
        'efficiency': entropy / 3.0,
        'pass': entropy > 2.9,
        'warning': 2.7 < entropy <= 2.9
    }
    results['tests']['entropy'] = entropy_test
    if not entropy_test['pass']:
        results['overall_pass'] = False
    if entropy_test['warning']:
        results['warnings'].append("Entropy efficiency between 0.9 and 0.97")
    
    # 3. Bootstrap CI for entropy
    try:
        entropy_ci = bootstrap_ci(sequence, entropy_statistic, B=10000)
        bootstrap_test = {
            'entropy': entropy_ci['statistic'],
            'ci_lower': entropy_ci['ci_lower'],
            'ci_upper': entropy_ci['ci_upper'],
            'ci_width': entropy_ci['ci_width'],
            'expected_in_ci': 3.0 >= entropy_ci['ci_lower'] and 3.0 <= entropy_ci['ci_upper'],
            'pass': 3.0 >= entropy_ci['ci_lower'] and 3.0 <= entropy_ci['ci_upper']
        }
        results['tests']['bootstrap_ci'] = bootstrap_test
        if not bootstrap_test['pass']:
            results['overall_pass'] = False
    except Exception as e:
        results['warnings'].append(f"Bootstrap CI failed: {e}")
        results['tests']['bootstrap_ci'] = {'pass': False, 'error': str(e)}
    
    # 4. Subsample stability (first/second half)
    try:
        stability_test = subsample_stability_test(sequence, method='half')
        results['tests']['subsample_stability'] = stability_test
        if not stability_test['pass']:
            results['overall_pass'] = False
    except Exception as e:
        results['warnings'].append(f"Subsample stability test failed: {e}")
        results['tests']['subsample_stability'] = {'pass': False, 'error': str(e)}
    
    # 5. Autocorrelation
    try:
        autocorr_result = autocorrelation_large_lags(sequence, max_lag=min(100, n//4))
        threshold_ac = 2 / math.sqrt(n)
        autocorr_test = {
            'max_autocorr': autocorr_result['max_autocorr'],
            'threshold': threshold_ac,
            'pass': autocorr_result['max_autocorr'] < threshold_ac,
            'periods_detected': len(autocorr_result['periods']) > 0,
            'periods': autocorr_result['periods']
        }
        results['tests']['autocorrelation'] = autocorr_test
        if not autocorr_test['pass']:
            results['overall_pass'] = False
        if autocorr_test['periods_detected']:
            results['warnings'].append(f"Periodic patterns detected: {autocorr_test['periods']}")
    except Exception as e:
        results['warnings'].append(f"Autocorrelation test failed: {e}")
        results['tests']['autocorrelation'] = {'pass': False, 'error': str(e)}
    
    # 6. DFA
    try:
        dfa_result = dfa_exponent(sequence)
        dfa_test = {
            'alpha': dfa_result['alpha'],
            'pass': 0.45 < dfa_result['alpha'] < 0.55,
            'interpretation': dfa_result['interpretation']
        }
        results['tests']['dfa'] = dfa_test
        if not dfa_test['pass']:
            results['overall_pass'] = False
    except Exception as e:
        results['warnings'].append(f"DFA test failed: {e}")
        results['tests']['dfa'] = {'pass': False, 'error': str(e)}
    
    # 7. Balance (if category function provided)
    if category_func is not None:
        try:
            balance = balance_statistic(sequence, category_func)
            balance_test = {
                'balance': balance,
                'pass': balance > 0.95,
                'warning': 0.90 < balance <= 0.95
            }
            results['tests']['balance'] = balance_test
            if not balance_test['pass']:
                results['overall_pass'] = False
            if balance_test['warning']:
                results['warnings'].append("Balance between 0.90 and 0.95")
        except Exception as e:
            results['warnings'].append(f"Balance test failed: {e}")
            results['tests']['balance'] = {'pass': False, 'error': str(e)}
    
    return results


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_validation_report(results: Dict) -> None:
    """
    Print a human-readable validation report.
    
    Args:
        results: Output from comprehensive_validation()
    """
    print("=" * 70)
    print("STATISTICAL VALIDATION REPORT")
    print("=" * 70)
    print(f"Sequence length: {results['sequence_length']}")
    print(f"Overall status: {'PASS' if results['overall_pass'] else 'FAIL'}")
    print()
    
    for test_name, test_result in results['tests'].items():
        status = "PASS" if test_result.get('pass', False) else "FAIL"
        print(f"{test_name.upper().replace('_', ' ')}: {status}")
        
        if 'entropy' in test_result:
            print(f"  Entropy: {test_result['entropy']:.4f} bits (max: 3.0)")
            print(f"  Efficiency: {test_result.get('efficiency', 0):.4f}")
        
        if 'ci_lower' in test_result:
            print(f"  95% CI: [{test_result['ci_lower']:.4f}, {test_result['ci_upper']:.4f}]")
        
        if 'max_autocorr' in test_result:
            print(f"  Max autocorr: {test_result['max_autocorr']:.4f} (threshold: {test_result['threshold']:.4f})")
        
        if 'alpha' in test_result:
            print(f"  DFA exponent: {test_result['alpha']:.4f} ({test_result.get('interpretation', 'unknown')})")
        
        if 'balance' in test_result:
            print(f"  Balance: {test_result['balance']:.4f}")
        
        print()
    
    if results['warnings']:
        print("WARNINGS:")
        for warning in results['warnings']:
            print(f"  - {warning}")
    
    print("=" * 70)
