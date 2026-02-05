"""
Complexity and Information Measures for Discrete Sequences
==========================================================

This module implements three key complexity and information measures for testing
discrete sequences with values 0-7 (alphabet size 8):

1. Markov Order Testing - Conditional entropy comparisons
2. Lempel-Ziv Complexity - Sequence compressibility (LZ76/LZ78)
3. Permutation Entropy - Order pattern analysis

All measures include normalization and expected values for random sequences.
"""

from collections import Counter
from typing import List, Tuple, Dict
import math


# =============================================================================
# MARKOV ORDER TESTING
# =============================================================================

def conditional_entropy_order1(sequence: List[int]) -> float:
    """
    Compute conditional entropy H(X_n | X_{n-1}) for 1st order Markov chain.
    
    This measures how much information is needed to predict the next symbol
    given knowledge of the previous symbol.
    
    Args:
        sequence: List of integers 0-7
        
    Returns:
        Conditional entropy in bits
        
    Expected value for random sequence: 3.0 bits (log2(8))
    """
    if len(sequence) < 2:
        return 0.0
    
    # Count pairs (X_{n-1}, X_n)
    pairs = [(sequence[i], sequence[i+1]) for i in range(len(sequence)-1)]
    pair_counts = Counter(pairs)
    
    # Count previous symbols (for normalization)
    prev_counts = Counter(sequence[:-1])
    
    total_pairs = len(pairs)
    entropy = 0.0
    
    for (x, y), count in pair_counts.items():
        if count > 0 and prev_counts[x] > 0:
            p_xy = count / total_pairs
            p_y_given_x = count / prev_counts[x]
            entropy -= p_xy * math.log2(p_y_given_x)
    
    return entropy


def conditional_entropy_order2(sequence: List[int]) -> float:
    """
    Compute conditional entropy H(X_n | X_{n-1}, X_{n-2}) for 2nd order Markov chain.
    
    This measures how much information is needed to predict the next symbol
    given knowledge of the previous two symbols.
    
    Args:
        sequence: List of integers 0-7
        
    Returns:
        Conditional entropy in bits
        
    Expected value for random sequence: 3.0 bits (log2(8))
    Expected value for 1st order Markov: same as H(X_n | X_{n-1})
    """
    if len(sequence) < 3:
        return 0.0
    
    # Count triples (X_{n-2}, X_{n-1}, X_n)
    triples = [(sequence[i], sequence[i+1], sequence[i+2]) 
               for i in range(len(sequence)-2)]
    triple_counts = Counter(triples)
    
    # Count pairs (X_{n-2}, X_{n-1}) for normalization
    pairs = [(sequence[i], sequence[i+1]) for i in range(len(sequence)-1)]
    pair_counts = Counter(pairs)
    
    total_triples = len(triples)
    entropy = 0.0
    
    for (x, y, z), count in triple_counts.items():
        if count > 0 and pair_counts.get((x, y), 0) > 0:
            p_xyz = count / total_triples
            p_z_given_xy = count / pair_counts[(x, y)]
            entropy -= p_xyz * math.log2(p_z_given_xy)
    
    return entropy


def markov_order_test(sequence: List[int]) -> Dict[str, float]:
    """
    Perform Markov order test comparing 1st vs 2nd order.
    
    Returns:
        Dictionary with:
        - h1: H(X_n | X_{n-1})
        - h2: H(X_n | X_{n-1}, X_{n-2})
        - difference: h1 - h2
        - is_first_order: True if difference < 0.1 bits
        - is_random: True if h1 > 2.9 bits
    """
    h1 = conditional_entropy_order1(sequence)
    h2 = conditional_entropy_order2(sequence)
    diff = h1 - h2
    
    return {
        'h1': h1,
        'h2': h2,
        'difference': diff,
        'is_first_order': abs(diff) < 0.1,
        'is_random': h1 > 2.9,
        'h1_normalized': h1 / 3.0,  # Normalized to max entropy
        'h2_normalized': h2 / 3.0,
    }


# =============================================================================
# LEMPEL-ZIV COMPLEXITY
# =============================================================================

def lz76_complexity(sequence: List[int]) -> int:
    """
    Compute LZ76 complexity (Lempel-Ziv 1976).
    
    Parses the sequence into phrases, where each phrase is the longest
    substring that has appeared before plus one new symbol.
    
    Args:
        sequence: List of integers
        
    Returns:
        Number of phrases (complexity)
        
    For random sequence of length N: E[c] ≈ N / log_A(N) where A is alphabet size.
    """
    n = len(sequence)
    if n == 0:
        return 0
    
    complexity = 1  # First symbol is always a new phrase
    i = 1
    
    while i < n:
        # Find longest match in previous part of sequence
        max_match_len = 0
        
        for j in range(i):
            # Check how long the match starting at j matches sequence starting at i
            match_len = 0
            while (i + match_len < n and 
                   j + match_len < i and
                   sequence[j + match_len] == sequence[i + match_len]):
                match_len += 1
            
            max_match_len = max(max_match_len, match_len)
        
        if max_match_len > 0:
            # Move past the match plus one new symbol
            i += max_match_len + 1
        else:
            # Single new symbol
            i += 1
        
        complexity += 1
    
    return complexity


def lz78_complexity(sequence: List[int]) -> int:
    """
    Compute LZ78 complexity (Lempel-Ziv 1978).
    
    Builds a dictionary incrementally, adding new patterns as they are encountered.
    
    Args:
        sequence: List of integers
        
    Returns:
        Number of dictionary entries (complexity)
        
    For random sequence of length N: E[c] ≈ A * log_A(N) where A is alphabet size.
    """
    n = len(sequence)
    if n == 0:
        return 0
    
    dictionary = set()
    complexity = 0
    i = 0
    current_phrase = []
    
    while i < n:
        current_phrase.append(sequence[i])
        phrase_tuple = tuple(current_phrase)
        
        if phrase_tuple in dictionary:
            # Extend phrase
            i += 1
        else:
            # New pattern found
            dictionary.add(phrase_tuple)
            complexity += 1
            current_phrase = []
            i += 1
    
    return complexity


def lz76_normalized(sequence: List[int], alphabet_size: int = 8) -> float:
    """
    Normalized LZ76 complexity.
    
    Returns:
        Normalized complexity (1.0 for random sequence)
    """
    n = len(sequence)
    if n <= 1:
        return 1.0
    
    c = lz76_complexity(sequence)
    expected = n / math.log(n, alphabet_size) if n > 1 else 1
    return c / expected if expected > 0 else 1.0


def lz78_normalized(sequence: List[int], alphabet_size: int = 8) -> float:
    """
    Normalized LZ78 complexity.
    
    For finite sequences, LZ78 complexity grows approximately as N / log_A(N)
    similar to LZ76, but with a different constant. We use the same normalization
    as LZ76 for practical comparison.
    
    Returns:
        Normalized complexity (1.0 for random sequence)
    """
    n = len(sequence)
    if n <= 1:
        return 1.0
    
    c = lz78_complexity(sequence)
    # For finite sequences, use same normalization as LZ76
    # The actual expected value is approximately N / log_A(N) for both
    expected = n / math.log(n, alphabet_size) if n > 1 else 1
    return c / expected if expected > 0 else 1.0


def lempel_ziv_test(sequence: List[int], alphabet_size: int = 8) -> Dict[str, float]:
    """
    Perform Lempel-Ziv complexity test.
    
    Returns:
        Dictionary with:
        - lz76: Raw LZ76 complexity
        - lz78: Raw LZ78 complexity
        - lz76_normalized: Normalized LZ76 (1.0 for random)
        - lz78_normalized: Normalized LZ78 (1.0 for random)
        - is_random_lz76: True if normalized in [0.8, 1.2]
        - is_random_lz78: True if normalized in [0.8, 1.2]
    """
    lz76 = lz76_complexity(sequence)
    lz78 = lz78_complexity(sequence)
    lz76_norm = lz76_normalized(sequence, alphabet_size)
    lz78_norm = lz78_normalized(sequence, alphabet_size)
    
    return {
        'lz76': lz76,
        'lz78': lz78,
        'lz76_normalized': lz76_norm,
        'lz78_normalized': lz78_norm,
        'is_random_lz76': 0.8 <= lz76_norm <= 1.2,
        'is_random_lz78': 0.8 <= lz78_norm <= 1.2,
    }


# =============================================================================
# PERMUTATION ENTROPY
# =============================================================================

def permutation_pattern(subsequence: List[int]) -> Tuple[int, ...]:
    """
    Compute permutation pattern (ordinal pattern) for a subsequence.
    
    The pattern is the permutation that sorts the subsequence by value.
    Ties are broken by position (earlier position wins).
    
    Args:
        subsequence: List of d values
        
    Returns:
        Tuple of indices sorted by value (ordinal pattern)
        
    Example:
        [3, 7, 1] -> (2, 0, 1)  (position 2 has smallest, 0 has middle, 1 has largest)
    """
    d = len(subsequence)
    # Sort indices by value, breaking ties by position
    sorted_indices = sorted(range(d), key=lambda i: (subsequence[i], i))
    return tuple(sorted_indices)


def permutation_entropy(sequence: List[int], d: int = 3) -> float:
    """
    Compute permutation entropy for embedding dimension d.
    
    Examines order patterns in subsequences of length d.
    
    Args:
        sequence: List of integers
        d: Embedding dimension (length of subsequences to examine)
        
    Returns:
        Permutation entropy in bits
        
    Maximum entropy: log2(d!) bits (all patterns equally likely)
    """
    n = len(sequence)
    if n < d:
        return 0.0
    
    # Extract all subsequences and compute patterns
    patterns = []
    for i in range(n - d + 1):
        subseq = sequence[i:i+d]
        pattern = permutation_pattern(subseq)
        patterns.append(pattern)
    
    # Count pattern frequencies
    pattern_counts = Counter(patterns)
    total = len(patterns)
    
    # Compute entropy
    entropy = 0.0
    for count in pattern_counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    
    return entropy


def permutation_entropy_normalized(sequence: List[int], d: int = 3) -> float:
    """
    Normalized permutation entropy.
    
    Returns:
        Normalized entropy (1.0 for random sequence)
    """
    h = permutation_entropy(sequence, d)
    h_max = math.log2(math.factorial(d))
    return h / h_max if h_max > 0 else 0.0


def permutation_entropy_test(sequence: List[int], 
                             dimensions: List[int] = [3, 4, 5]) -> Dict[str, float]:
    """
    Perform permutation entropy test for multiple embedding dimensions.
    
    Args:
        sequence: List of integers
        dimensions: List of embedding dimensions to test
        
    Returns:
        Dictionary with results for each dimension:
        - h_d3, h_d4, h_d5: Raw permutation entropies
        - h_d3_normalized, h_d4_normalized, h_d5_normalized: Normalized entropies
        - is_random_d3, is_random_d4, is_random_d5: True if normalized > 0.9
    """
    results = {}
    
    for d in dimensions:
        h = permutation_entropy(sequence, d)
        h_norm = permutation_entropy_normalized(sequence, d)
        
        results[f'h_d{d}'] = h
        results[f'h_d{d}_normalized'] = h_norm
        results[f'is_random_d{d}'] = h_norm > 0.9
    
    return results


# =============================================================================
# COMPREHENSIVE TEST SUITE
# =============================================================================

def comprehensive_complexity_test(sequence: List[int], 
                                  alphabet_size: int = 8) -> Dict:
    """
    Run all complexity and information measures on a sequence.
    
    Args:
        sequence: List of integers 0-7
        alphabet_size: Size of alphabet (default 8)
        
    Returns:
        Dictionary with all test results and summary statistics
    """
    results = {}
    
    # Markov order test
    markov_results = markov_order_test(sequence)
    results.update({f'markov_{k}': v for k, v in markov_results.items()})
    
    # Lempel-Ziv test
    lz_results = lempel_ziv_test(sequence, alphabet_size)
    results.update({f'lz_{k}': v for k, v in lz_results.items()})
    
    # Permutation entropy test
    perm_results = permutation_entropy_test(sequence, [3, 4, 5])
    results.update({f'perm_{k}': v for k, v in perm_results.items()})
    
    # Summary: Is sequence random-like?
    is_random = (
        markov_results['is_random'] and
        markov_results['is_first_order'] and
        lz_results['is_random_lz76'] and
        lz_results['is_random_lz78'] and
        perm_results.get('is_random_d3', False) and
        perm_results.get('is_random_d4', False)
    )
    
    results['is_random_like'] = is_random
    results['sequence_length'] = len(sequence)
    
    return results


# =============================================================================
# EXPECTED VALUES FOR RANDOM SEQUENCES
# =============================================================================

def expected_values_random_sequence(n: int, alphabet_size: int = 8) -> Dict[str, float]:
    """
    Return expected values for a truly random sequence of length n.
    
    Useful for comparison with actual measurements.
    """
    return {
        'h1_expected': 3.0,  # log2(8)
        'h2_expected': 3.0,
        'h1_h2_diff_expected': 0.0,
        'lz76_expected': n / math.log(n, alphabet_size) if n > 1 else 1,
        'lz78_expected': alphabet_size * math.log(n, alphabet_size) if n > 1 else 1,
        'lz76_normalized_expected': 1.0,
        'lz78_normalized_expected': 1.0,
        'perm_h_d3_expected': math.log2(6),  # log2(3!)
        'perm_h_d4_expected': math.log2(24),  # log2(4!)
        'perm_h_d5_expected': math.log2(120),  # log2(5!)
        'perm_normalized_expected': 1.0,
    }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    import random
    
    # Generate random sequence
    random.seed(42)
    random_seq = [random.randint(0, 7) for _ in range(1000)]
    
    print("Testing random sequence (length 1000):")
    print("=" * 60)
    
    results = comprehensive_complexity_test(random_seq)
    
    print("\nMarkov Order Test:")
    print(f"  H(X_n | X_{{n-1}}) = {results['markov_h1']:.4f} bits (expected: 3.0)")
    print(f"  H(X_n | X_{{n-1}}, X_{{n-2}}) = {results['markov_h2']:.4f} bits (expected: 3.0)")
    print(f"  Difference = {results['markov_difference']:.4f} bits (expected: 0.0)")
    print(f"  Is first order? {results['markov_is_first_order']}")
    print(f"  Is random? {results['markov_is_random']}")
    
    print("\nLempel-Ziv Complexity:")
    print(f"  LZ76 complexity = {results['lz_lz76']}")
    print(f"  LZ76 normalized = {results['lz_lz76_normalized']:.4f} (expected: 1.0)")
    print(f"  LZ78 complexity = {results['lz_lz78']}")
    print(f"  LZ78 normalized = {results['lz_lz78_normalized']:.4f} (expected: 1.0)")
    print(f"  LZ76 random-like? {results['lz_is_random_lz76']}")
    print(f"  LZ78 random-like? {results['lz_is_random_lz78']}")
    
    print("\nPermutation Entropy:")
    print(f"  d=3: H = {results['perm_h_d3']:.4f} bits (max: {math.log2(6):.4f})")
    print(f"  d=3 normalized = {results['perm_h_d3_normalized']:.4f} (expected: 1.0)")
    print(f"  d=4: H = {results['perm_h_d4']:.4f} bits (max: {math.log2(24):.4f})")
    print(f"  d=4 normalized = {results['perm_h_d4_normalized']:.4f} (expected: 1.0)")
    print(f"  d=5: H = {results['perm_h_d5']:.4f} bits (max: {math.log2(120):.4f})")
    print(f"  d=5 normalized = {results['perm_h_d5_normalized']:.4f} (expected: 1.0)")
    
    print("\nOverall Assessment:")
    print(f"  Sequence is random-like? {results['is_random_like']}")
    
    # Test structured sequence
    print("\n" + "=" * 60)
    print("Testing structured sequence (repeating pattern):")
    structured_seq = ([0, 1, 2, 3, 4, 5, 6, 7] * 125)[:1000]
    
    results_struct = comprehensive_complexity_test(structured_seq)
    
    print(f"\nMarkov Order Test:")
    print(f"  H(X_n | X_{{n-1}}) = {results_struct['markov_h1']:.4f} bits")
    print(f"  H(X_n | X_{{n-1}}, X_{{n-2}}) = {results_struct['markov_h2']:.4f} bits")
    print(f"  Is random? {results_struct['markov_is_random']}")
    
    print(f"\nLempel-Ziv Complexity:")
    print(f"  LZ76 normalized = {results_struct['lz_lz76_normalized']:.4f}")
    print(f"  LZ78 normalized = {results_struct['lz_lz78_normalized']:.4f}")
    
    print(f"\nPermutation Entropy:")
    print(f"  d=3 normalized = {results_struct['perm_h_d3_normalized']:.4f}")
    print(f"  d=4 normalized = {results_struct['perm_h_d4_normalized']:.4f}")
    
    print(f"\nOverall Assessment:")
    print(f"  Sequence is random-like? {results_struct['is_random_like']}")
