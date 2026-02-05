"""
Example Usage of Statistical Robustness Methods

This script demonstrates how to use the statistical robustness methods
for validating discrete sequences visiting 8 states.
"""

import math
import random
from collections import Counter

from gravity_field_model.calculations.statistical_robustness import (
    hoeffding_deviation,
    check_vertex_counts,
    subsample_stability_test,
    bootstrap_ci,
    entropy_statistic,
    autocorrelation_large_lags,
    dfa_exponent,
    comprehensive_validation,
    print_validation_report
)


# =============================================================================
# EXAMPLE 1: Random Uniform Sequence (Should Pass All Tests)
# =============================================================================

def example_random_sequence():
    """Generate a random uniform sequence - should pass all tests."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Random Uniform Sequence (n=1000)")
    print("="*70)
    
    # Generate random uniform sequence
    n = 1000
    sequence = [random.randint(0, 7) for _ in range(n)]
    
    # Comprehensive validation
    results = comprehensive_validation(sequence)
    print_validation_report(results)
    
    return results


# =============================================================================
# EXAMPLE 2: Biased Sequence (Should Fail Some Tests)
# =============================================================================

def example_biased_sequence():
    """Generate a biased sequence - should fail uniformity tests."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Biased Sequence (n=1000, vertex 0 appears 50% of time)")
    print("="*70)
    
    n = 1000
    # Vertex 0 appears 50% of the time, others share remaining 50%
    sequence = []
    for _ in range(n):
        if random.random() < 0.5:
            sequence.append(0)
        else:
            sequence.append(random.randint(1, 7))
    
    results = comprehensive_validation(sequence)
    print_validation_report(results)
    
    return results


# =============================================================================
# EXAMPLE 3: Periodic Sequence (Should Fail Correlation Tests)
# =============================================================================

def example_periodic_sequence():
    """Generate a periodic sequence - should fail autocorrelation tests."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Periodic Sequence (n=1000, period=8)")
    print("="*70)
    
    n = 1000
    # Simple cycle: 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, ...
    sequence = [i % 8 for i in range(n)]
    
    results = comprehensive_validation(sequence)
    print_validation_report(results)
    
    return results


# =============================================================================
# EXAMPLE 4: Individual Test Demonstrations
# =============================================================================

def example_individual_tests():
    """Demonstrate individual statistical tests."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Individual Test Demonstrations")
    print("="*70)
    
    n = 1000
    sequence = [random.randint(0, 7) for _ in range(n)]
    
    # 1. Hoeffding deviation
    print("\n1. HOEFFDING DEVIATION")
    print("-" * 70)
    threshold = hoeffding_deviation(n, confidence=0.95)
    print(f"Sequence length: {n}")
    print(f"Expected count per vertex: {n/8:.1f}")
    print(f"95% confidence deviation threshold: ±{threshold:.2f}")
    print(f"Acceptable range: [{n/8 - threshold:.1f}, {n/8 + threshold:.1f}]")
    
    # 2. Vertex count check
    print("\n2. VERTEX COUNT UNIFORMITY")
    print("-" * 70)
    counts = Counter(sequence)
    vertex_results = check_vertex_counts(counts, n)
    print(f"Overall pass: {vertex_results['overall_pass']}")
    for v in range(8):
        r = vertex_results[v]
        status = "PASS" if r['pass'] else "FAIL"
        print(f"  Vertex {v}: count={r['count']:4d}, expected={r['expected']:6.1f}, "
              f"deviation={r['deviation']:6.1f}, {status}")
    
    # 3. Entropy
    print("\n3. SHANNON ENTROPY")
    print("-" * 70)
    entropy = entropy_statistic(sequence)
    max_entropy = 3.0
    efficiency = entropy / max_entropy
    print(f"Entropy: {entropy:.4f} bits")
    print(f"Maximum entropy: {max_entropy:.4f} bits")
    print(f"Efficiency: {efficiency:.4f} ({efficiency*100:.2f}%)")
    print(f"Status: {'PASS' if entropy > 2.9 else 'FAIL'}")
    
    # 4. Bootstrap CI for entropy
    print("\n4. BOOTSTRAP CONFIDENCE INTERVAL (Entropy)")
    print("-" * 70)
    print("Computing bootstrap CI (this may take a moment)...")
    entropy_ci = bootstrap_ci(sequence, entropy_statistic, B=5000)  # Reduced for speed
    print(f"Observed entropy: {entropy_ci['statistic']:.4f} bits")
    print(f"95% CI: [{entropy_ci['ci_lower']:.4f}, {entropy_ci['ci_upper']:.4f}]")
    print(f"CI width: {entropy_ci['ci_width']:.4f} bits")
    print(f"Expected (3.0) in CI: {3.0 >= entropy_ci['ci_lower'] and 3.0 <= entropy_ci['ci_upper']}")
    
    # 5. Subsample stability
    print("\n5. SUBSAMPLE STABILITY (First/Second Half)")
    print("-" * 70)
    stability = subsample_stability_test(sequence, method='half')
    print(f"Chi-square statistic: {stability['chi2_statistic']:.4f}")
    print(f"Critical value (95%): {stability['critical_value']:.4f}")
    print(f"P-value: {stability['p_value']:.4f}")
    print(f"Status: {'PASS' if stability['pass'] else 'FAIL'}")
    print(f"Interpretation: {stability['interpretation']}")
    
    # 6. Autocorrelation
    print("\n6. AUTOCORRELATION ANALYSIS")
    print("-" * 70)
    autocorr_result = autocorrelation_large_lags(sequence, max_lag=50)
    print(f"Statistical threshold: ±{autocorr_result['threshold']:.4f}")
    print(f"Max autocorrelation (k>0): {autocorr_result['max_autocorr']:.4f}")
    print(f"Status: {'PASS' if autocorr_result['max_autocorr'] < autocorr_result['threshold'] else 'FAIL'}")
    
    if autocorr_result['peaks']:
        print(f"Significant peaks found: {autocorr_result['peaks'][:5]}")  # Show first 5
    else:
        print("No significant peaks detected")
    
    if autocorr_result['periods']:
        print(f"Periodic patterns detected: {autocorr_result['periods']}")
    else:
        print("No periodic patterns detected")
    
    # 7. DFA
    print("\n7. DETRENDED FLUCTUATION ANALYSIS (DFA)")
    print("-" * 70)
    dfa_result = dfa_exponent(sequence)
    print(f"DFA exponent (α): {dfa_result['alpha']:.4f}")
    print(f"Interpretation: {dfa_result['interpretation']}")
    print(f"Status: {'PASS' if 0.45 < dfa_result['alpha'] < 0.55 else 'FAIL'}")
    if dfa_result['fluctuations']:
        print(f"Sample fluctuations: {dfa_result['fluctuations'][:3]}")  # Show first 3


# =============================================================================
# EXAMPLE 5: Using with Real Traversal Data
# =============================================================================

def example_with_traversal():
    """Example using actual traversal data from the codebase."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Using with Real Traversal Data")
    print("="*70)
    
    try:
        from gravity_field_model.common import traverse_pi_base8
        
        # Get traversal sequence
        traversal = traverse_pi_base8(1000)
        sequence = [step['vertex'] for step in traversal]
        
        print(f"Traversal length: {len(sequence)}")
        print("Running comprehensive validation...")
        
        # Category function for tetrahedron balance
        from gravity_field_model.common import TET_A, TET_B
        def tetrahedron_category(vertex):
            return 0 if vertex in TET_A else 1
        
        results = comprehensive_validation(sequence, category_func=tetrahedron_category)
        print_validation_report(results)
        
        return results
        
    except ImportError:
        print("Could not import traversal functions. Skipping this example.")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("STATISTICAL ROBUSTNESS METHODS - EXAMPLES")
    print("="*70)
    
    # Run examples
    example_random_sequence()
    example_biased_sequence()
    example_periodic_sequence()
    example_individual_tests()
    
    # Try real traversal if available
    try:
        example_with_traversal()
    except Exception as e:
        print(f"\nSkipping real traversal example: {e}")
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETE")
    print("="*70)
