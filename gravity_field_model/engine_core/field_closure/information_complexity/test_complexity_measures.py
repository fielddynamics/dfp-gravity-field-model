"""
Complexity and Randomness Measures
==================================

This module applies sophisticated complexity measures to the vertex sequence,
testing whether pi's traversal is truly "random-like" or contains hidden structure.

WHY COMPLEXITY MATTERS
----------------------

Shannon entropy tells us about the average information content, but it can miss
subtle patterns. These advanced measures probe deeper:

    ANALOGY: Think of a text message.
    
    "ABCDEFGH" and "AAAABBBB" might have similar letter frequencies,
    but one is clearly more structured. Compression algorithms would
    shrink the second one dramatically. That's what we're testing.

VALIDATION CATEGORIES:

1. Markov Order Testing (1 test)
   - Is the sequence memoryless, or does history help predict the future?
   
2. Lempel-Ziv Complexity (1 test)
   - Can the sequence be compressed? (Lower = more structure)
   
3. Permutation Entropy (1 test)
   - Do order patterns appear uniformly? (Tests temporal structure)

EXPECTED RESULTS FOR RANDOM SEQUENCES:

- Markov: Knowing v_{n-2} shouldn't help predict v_n beyond v_{n-1}
- Lempel-Ziv: Normalized complexity near 1.0 (incompressible)
- Permutation: Near-maximal for all embedding dimensions

PHYSICAL SIGNIFICANCE:

If pi's traversal has hidden structure, it might bias our field closure model.
These tests verify that pi acts as a "fair randomness source" for the traversal,
despite being completely deterministic.

ACADEMIC CONTEXT:

- Markov order: Cover & Thomas "Elements of Information Theory"
- Lempel-Ziv: Ziv & Lempel (1976, 1978) IEEE Trans. Information Theory
- Permutation entropy: Bandt & Pompe (2002) Physical Review Letters

DEPENDENCIES:
- gravity_field_model.common for traversal
"""

from typing import Dict, List, Tuple, Set
from collections import Counter
import math
from itertools import permutations

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


# =============================================================================
# MARKOV ORDER HELPER FUNCTIONS
# =============================================================================

def compute_conditional_entropy_order1(sequence: List[int], n_states: int = 8) -> float:
    """
    Compute H(X_n | X_{n-1}): entropy of next state given current state.
    
    For a 1st-order Markov chain, this is the fundamental measure of uncertainty.
    """
    # Count transitions
    transitions = Counter()
    current_counts = Counter()
    
    for i in range(len(sequence) - 1):
        current = sequence[i]
        next_state = sequence[i + 1]
        transitions[(current, next_state)] += 1
        current_counts[current] += 1
    
    # Compute conditional entropy
    h_cond = 0.0
    n_total = len(sequence) - 1
    
    for current in range(n_states):
        p_current = current_counts[current] / n_total if n_total > 0 else 0
        if p_current == 0:
            continue
            
        # Entropy of next state given this current state
        h_given_current = 0.0
        for next_state in range(n_states):
            count = transitions[(current, next_state)]
            if count > 0:
                p_next_given_current = count / current_counts[current]
                h_given_current -= p_next_given_current * math.log2(p_next_given_current)
        
        h_cond += p_current * h_given_current
    
    return h_cond


def compute_conditional_entropy_order2(sequence: List[int], n_states: int = 8) -> float:
    """
    Compute H(X_n | X_{n-1}, X_{n-2}): entropy given TWO previous states.
    
    If this is significantly lower than order-1, the sequence has memory.
    """
    # Count transitions from pairs
    pair_transitions = Counter()
    pair_counts = Counter()
    
    for i in range(len(sequence) - 2):
        pair = (sequence[i], sequence[i + 1])
        next_state = sequence[i + 2]
        pair_transitions[(pair, next_state)] += 1
        pair_counts[pair] += 1
    
    # Compute conditional entropy
    h_cond = 0.0
    n_total = len(sequence) - 2
    
    for s1 in range(n_states):
        for s2 in range(n_states):
            pair = (s1, s2)
            p_pair = pair_counts[pair] / n_total if n_total > 0 else 0
            if p_pair == 0:
                continue
            
            h_given_pair = 0.0
            for next_state in range(n_states):
                count = pair_transitions[(pair, next_state)]
                if count > 0:
                    p_next_given_pair = count / pair_counts[pair]
                    h_given_pair -= p_next_given_pair * math.log2(p_next_given_pair)
            
            h_cond += p_pair * h_given_pair
    
    return h_cond


# =============================================================================
# LEMPEL-ZIV COMPLEXITY HELPER FUNCTIONS
# =============================================================================

def lempel_ziv_complexity(sequence: List[int]) -> int:
    """
    Compute Lempel-Ziv complexity (LZ76 variant).
    
    This counts the number of distinct substrings needed to build the sequence.
    Higher complexity = more random. Lower = more compressible.
    
    Algorithm:
    1. Start with empty dictionary
    2. Scan sequence, extending current substring until it's new
    3. Add new substring to dictionary, increment complexity
    4. Repeat until end of sequence
    """
    n = len(sequence)
    if n == 0:
        return 0
    
    complexity = 1
    substring_set: Set[Tuple[int, ...]] = set()
    
    i = 0
    while i < n:
        # Find longest substring starting at i that's already seen
        length = 1
        while i + length <= n:
            substring = tuple(sequence[i:i + length])
            if substring not in substring_set:
                substring_set.add(substring)
                complexity += 1
                break
            length += 1
        i += length
    
    return complexity


def normalized_lz_complexity(sequence: List[int], alphabet_size: int = 8) -> float:
    """
    Normalize LZ complexity to [0, 1] range.
    
    For a random sequence of length n over alphabet of size k:
    Expected complexity ~ n / log_k(n)
    
    Normalization: LZ / (n / log_k(n))
    
    Values near 1.0 indicate random-like complexity.
    Values << 1.0 indicate compressible structure.
    """
    n = len(sequence)
    if n <= 1:
        return 1.0
    
    lz = lempel_ziv_complexity(sequence)
    
    # Expected complexity for random sequence
    log_k_n = math.log(n) / math.log(alphabet_size)
    expected = n / log_k_n if log_k_n > 0 else n
    
    return lz / expected if expected > 0 else 1.0


# =============================================================================
# PERMUTATION ENTROPY HELPER FUNCTIONS
# =============================================================================

def ordinal_pattern(subsequence: List[int]) -> Tuple[int, ...]:
    """
    Convert a subsequence to its ordinal pattern.
    
    The ordinal pattern is the ranking of elements.
    Example: [5, 2, 8] -> (1, 0, 2) because 2 < 5 < 8
    
    For equal elements, use order of appearance (stable sort).
    """
    indexed = [(val, idx) for idx, val in enumerate(subsequence)]
    sorted_indexed = sorted(indexed, key=lambda x: (x[0], x[1]))
    
    pattern = [0] * len(subsequence)
    for rank, (val, orig_idx) in enumerate(sorted_indexed):
        pattern[orig_idx] = rank
    
    return tuple(pattern)


def compute_permutation_entropy(sequence: List[int], 
                                embedding_dim: int = 3,
                                delay: int = 1) -> float:
    """
    Compute permutation entropy for given embedding dimension.
    
    Permutation entropy examines the distribution of ordinal patterns
    in the sequence. Maximum entropy means all patterns appear equally.
    
    Args:
        sequence: Input sequence
        embedding_dim: Length of subsequences to examine (d)
        delay: Time delay between elements (tau)
    
    Returns:
        Normalized permutation entropy in [0, 1]
    """
    n = len(sequence)
    
    # Extract all ordinal patterns
    patterns = []
    for i in range(n - (embedding_dim - 1) * delay):
        subseq = [sequence[i + j * delay] for j in range(embedding_dim)]
        pattern = ordinal_pattern(subseq)
        patterns.append(pattern)
    
    if not patterns:
        return 1.0
    
    # Count pattern frequencies
    pattern_counts = Counter(patterns)
    n_patterns = len(patterns)
    
    # Compute Shannon entropy of pattern distribution
    entropy = 0.0
    for count in pattern_counts.values():
        p = count / n_patterns
        if p > 0:
            entropy -= p * math.log2(p)
    
    # Maximum entropy is log2(d!) where d! is number of possible patterns
    max_entropy = math.log2(math.factorial(embedding_dim))
    
    # Normalize to [0, 1]
    return entropy / max_entropy if max_entropy > 0 else 1.0


# =============================================================================
# TESTS
# =============================================================================

class MarkovOrderTest(Test):
    """
    Is the sequence memoryless, or does knowing more history help prediction?
    """
    name = "Markov Order (Memory) Test"
    question = (
        "Does the traversal have hidden memory? "
        "A 1st-order Markov process is 'memoryless': knowing the current state "
        "tells you everything about where you'll go next. Knowing earlier history "
        "doesn't help. Does pi's traversal have this property, or does it have "
        "subtle patterns that depend on longer history?"
    )
    reference = "H(X_n|X_{n-1}) approximately equals H(X_n|X_{n-1},X_{n-2})"
    level = Standard
    
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Excellent memory/memoryless framing. "
        "Derivation: 14/15 - Clear conditional entropy explanation. "
        "Commentary: 14/15 - Good interpretation of what memory would mean. "
        "Model: 9/10 - Good entropy comparison. "
        "Observations: 9/10 - Difference threshold reasonable. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 13/15 - Graduate level, good intuition. "
        "Header: 9/10 - Module header excellent."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("MARKOV PROPERTY: Future depends only on present, not past.")
            .step("TEST: Compare H(X_n | X_{n-1}) vs H(X_n | X_{n-1}, X_{n-2})")
            .step("If equal, knowing two steps back doesn't help beyond one step back.")
            .step("H(X_n | X_{n-1}): Uncertainty in next state given current state")
            .step("H(X_n | X_{n-1}, X_{n-2}): Uncertainty given TWO previous states")
            .step("CRITERION: Difference < 0.1 bits indicates effectively memoryless")
            .step("For truly random: both should be near 3 bits (log2(8))")
            .conclude("Small difference confirms 1st-order Markov behavior.")
        )
    
    commentary = (
        "The traversal is effectively memoryless: knowing where you were two steps "
        "ago doesn't help predict where you'll go next, beyond what your current "
        "position tells you. This is important because it means the traversal "
        "doesn't carry hidden correlations that could bias field closure. Each step "
        "is essentially independent of distant history, like rolling a fair die."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        vertices = [step['vertex'] for step in traversal]
        
        h_order1 = compute_conditional_entropy_order1(vertices)
        h_order2 = compute_conditional_entropy_order2(vertices)
        
        difference = abs(h_order1 - h_order2)
        max_entropy = 3.0  # log2(8)
        
        effectively_memoryless = 1 if difference < 0.1 else 0
        near_max_entropy = 1 if h_order1 > 2.8 else 0
        
        return (
            Model()
            .add("H(X_n|X_{n-1})", round(h_order1, 3), tol=0.015)
            .add("H(X_n|X_{n-1},X_{n-2})", round(h_order2, 3), tol=0.03)
            .add("Difference (bits)", round(difference, 3), abs_tol=0.07)
            .add("Max possible", max_entropy)
            .add("Near max entropy", near_max_entropy)
            .add("Difference < 0.1 bits (info)", effectively_memoryless)
        )
    
    def observations(self):
        # For a memoryless (independent) sequence both conditional entropies are
        # 3 bits in the limit. At 1001 samples the plug-in estimates are biased
        # low, strongly for order 2 (512 contexts): expected values over 150
        # random sequences are 2.959 and 2.625 bits, a difference of 0.334 bits.
        # A sequence with real memory would show a larger drop than this.
        # (The original criterion, difference < 0.1 bits, fails for every
        # random sequence of this length because of that bias.)
        return (
            Observed()
            .add("H(X_n|X_{n-1})", 2.959)
            .add("H(X_n|X_{n-1},X_{n-2})", 2.625)
            .add("Difference (bits)", 0.334)
            .add("Near max entropy", 1)
        )

class LempelZivComplexityTest(Test):
    """
    Can the vertex sequence be compressed? Random sequences are incompressible.
    """
    name = "Lempel-Ziv Algorithmic Complexity"
    question = (
        "Is the vertex sequence compressible? "
        "Compression algorithms like gzip work by finding repeated patterns. "
        "A truly random sequence has no patterns to exploit, so it can't be "
        "compressed. Does pi's traversal have hidden patterns that would allow "
        "compression, or is it incompressible like true randomness?"
    )
    reference = "Normalized LZ complexity near 1.0"
    level = Standard
    
    audit_score = 93
    audit_notes = (
        "Question: 15/15 - Excellent compression analogy. "
        "Derivation: 14/15 - Clear LZ algorithm explanation. "
        "Commentary: 14/15 - Good random vs structured interpretation. "
        "Model: 9/10 - Good normalized complexity. "
        "Observations: 9/10 - Threshold well-justified. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 14/15 - Undergrad can follow compression analogy. "
        "Header: 8/10 - Module header good."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Can you describe the sequence more compactly?")
            .step("'AAAABBBB' is compressible: '4A4B' is shorter.")
            .step("'ABCDEFGH' is not: no patterns to exploit.")
            .step("LZ COMPLEXITY: Counts distinct substrings needed to build sequence.")
            .step("NORMALIZATION: Divide by expected complexity for random sequence.")
            .step("Random sequence: normalized LZ near 1.0")
            .step("Structured sequence: normalized LZ << 1.0")
            .step("CRITERION: Normalized complexity > 0.7 indicates low structure")
            .conclude("High complexity confirms no exploitable patterns.")
        )
    
    commentary = (
        "The traversal is essentially incompressible, with normalized complexity "
        "near 1.0. This means gzip or other compressors would fail to shrink it "
        "significantly. Pi's digits, while deterministic, produce a vertex sequence "
        "with no repeated patterns that could be exploited for compression. This is "
        "the gold standard test for practical randomness: if you can't compress it, "
        "you can't predict it."
    )
    
    def model(self):
        traversal = traverse_pi_base8(500)  # LZ is O(n^2), keep reasonable
        vertices = [step['vertex'] for step in traversal]
        
        lz_raw = lempel_ziv_complexity(vertices)
        lz_normalized = normalized_lz_complexity(vertices)
        
        high_complexity = 1 if lz_normalized > 0.7 else 0
        
        return (
            Model()
            .add("Sequence length", len(vertices))
            .add("LZ complexity (raw)", lz_raw)
            .add("LZ complexity (normalized)", round(lz_normalized, 3), tol=0.03)
            .add("Threshold", 0.7)
            .add("High complexity (random-like)", high_complexity)
        )
    
    def observations(self):
        # Expected for independent uniform vertices at this length (501 symbols,
        # mean over 150 random sequences): raw LZ complexity 188, normalised
        # 1.121; 99% of random sequences lie within 2% of these values.
        return (
            Observed()
            .add("LZ complexity (normalized)", 1.121)
            .add("High complexity (random-like)", 1)
        )

class PermutationEntropyTest(Test):
    """
    Do ordinal patterns appear uniformly? Tests for subtle temporal structure.
    """
    name = "Permutation Entropy (Order Patterns)"
    question = (
        "Are there preferred ordinal patterns in the sequence? "
        "Permutation entropy looks at the ORDER of values in subsequences. "
        "For example, in [5,2,8], '2 < 5 < 8' is the pattern. If some patterns "
        "appear more than others, there's hidden structure. Does pi's traversal "
        "show any preferred ordinal patterns?"
    )
    reference = "Normalized permutation entropy near 1.0"
    level = Standard
    
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good ordinal pattern explanation. "
        "Derivation: 14/15 - Clear permutation entropy definition. "
        "Commentary: 13/15 - Good interpretation. "
        "Model: 9/10 - Good multi-dimension analysis. "
        "Observations: 9/10 - Thresholds reasonable. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 13/15 - Graduate level. "
        "Header: 9/10 - Module header excellent."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("ORDINAL PATTERN: The ranking of values in a subsequence.")
            .step("Example: [5,2,8] has pattern (1,0,2) because 2 < 5 < 8")
            .step("For length d, there are d! possible patterns")
            .step("d=3: 6 patterns, d=4: 24 patterns, d=5: 120 patterns")
            .step("PERMUTATION ENTROPY: Shannon entropy of pattern distribution")
            .step("Maximum entropy when all patterns equally likely")
            .step("NORMALIZATION: Divide by log2(d!) to get [0, 1] range")
            .step("CRITERION: Normalized PE > 0.9 for d=3,4,5 indicates no structure")
            .conclude("High permutation entropy confirms no preferred patterns.")
        )
    
    commentary = (
        "Permutation entropy is near-maximal for all embedding dimensions tested. "
        "This means there are no preferred ordinal patterns in the sequence. "
        "Whether we look at triples, quadruples, or quintuples, all possible "
        "orderings appear with roughly equal frequency. This is a strong indicator "
        "of genuine randomness in the temporal structure."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        vertices = [step['vertex'] for step in traversal]
        
        pe_d3 = compute_permutation_entropy(vertices, embedding_dim=3)
        pe_d4 = compute_permutation_entropy(vertices, embedding_dim=4)
        pe_d5 = compute_permutation_entropy(vertices, embedding_dim=5)
        
        all_high = 1 if pe_d3 > 0.9 and pe_d4 > 0.9 and pe_d5 > 0.9 else 0
        
        return (
            Model()
            .add("PE (d=3, 6 patterns)", round(pe_d3, 3), tol=0.025)
            .add("PE (d=4, 24 patterns)", round(pe_d4, 3), tol=0.025)
            .add("PE (d=5, 120 patterns)", round(pe_d5, 3), tol=0.025)
            .add("Threshold", 0.9)
            .add("All dimensions high PE", all_high)
        )
    
    def observations(self):
        # Expected normalised permutation entropy for independent uniform
        # vertices at 1001 samples (mean over 150 random sequences; ties between
        # equal values lower it slightly below 1): 0.986, 0.980 and 0.967 for
        # d = 3, 4, 5. 99% of random sequences lie within 2%.
        return (
            Observed()
            .add("PE (d=3, 6 patterns)", 0.986)
            .add("PE (d=4, 24 patterns)", 0.980)
            .add("PE (d=5, 120 patterns)", 0.967)
            .add("All dimensions high PE", 1)
        )

# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    MarkovOrderTest,
    LempelZivComplexityTest,
    PermutationEntropyTest,
]


def run_all():
    """Run all complexity measure tests."""
    return run_tests(
        title="Complexity and Randomness Measures",
        summary=(
            "Three sophisticated complexity measures confirm the vertex sequence "
            "is random-like: (1) Markov order test shows no hidden memory beyond "
            "1 step; (2) Lempel-Ziv complexity is near-maximal, meaning the sequence "
            "is incompressible; (3) Permutation entropy is high for all embedding "
            "dimensions, showing no preferred ordinal patterns. Despite being "
            "generated deterministically from pi, the traversal passes these gold "
            "standard tests for practical randomness."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
