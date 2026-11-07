"""
Information Theory Analysis
===========================

This module applies information-theoretic measures to the pi base-8 traversal,
quantifying the randomness and structure of the vertex sequence.

VALIDATION CATEGORIES:

1. Entropy Measures (2 tests)
   - Shannon entropy of vertex sequence
   - Block entropy scaling

2. Temporal Structure (2 tests)
   - Autocorrelation function decay
   - Mutual information between consecutive vertices

PHYSICAL SIGNIFICANCE:

Information theory provides rigorous tools to answer: "How random is this
traversal?" A maximally random sequence on 8 vertices has Shannon entropy
H = log2(8) = 3 bits. Deviations indicate structure, patterns, or bias.

Autocorrelation measures "memory" in the sequence: does knowing the current
vertex help predict the next? For independent samples, autocorrelation decays
immediately to zero. Persistent autocorrelation suggests hidden structure.

ACADEMIC CONTEXT:

These measures derive from Claude Shannon's foundational work (1948) on
information theory. The entropy measures follow Cover & Thomas "Elements of
Information Theory" (2006). NIST SP 800-22 uses similar spectral and entropy
tests to validate random number generators.

EXPECTED RESULTS:

For a "normal" sequence (pi is conjectured normal):
- Shannon entropy near 3 bits (maximum for 8 symbols)
- Autocorrelation decaying rapidly to near zero
- Low mutual information between consecutive vertices

DEPENDENCIES:
- gravity_field_model.common.pi_data for verified pi digits
- gravity_field_model.common for traversal functions and geometry constants
"""

from typing import Dict, List, Tuple
from collections import Counter
import math

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


# =============================================================================
# INFORMATION THEORY HELPER FUNCTIONS
# =============================================================================

def compute_shannon_entropy(sequence: List[int], base: int = 2) -> float:
    """
    Compute Shannon entropy H = -sum(p_i * log(p_i)) of a sequence.
    
    For a sequence of symbols, this measures the average information
    content per symbol. Maximum entropy for 8 symbols is log2(8) = 3 bits.
    
    Args:
        sequence: List of symbol values (e.g., vertex indices 0-7)
        base: Logarithm base (2 for bits, e for nats)
        
    Returns:
        Entropy in specified base units
    """
    if not sequence:
        return 0.0
    
    counts = Counter(sequence)
    total = len(sequence)
    
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log(p, base)
    
    return entropy


def compute_block_entropy(sequence: List[int], block_size: int) -> float:
    """
    Compute entropy of n-grams (blocks of consecutive symbols).
    
    For independent symbols, H(n) = n * H(1).
    Sublinear scaling indicates dependencies between symbols.
    
    Args:
        sequence: List of symbol values
        block_size: Size of blocks (n-grams)
        
    Returns:
        Entropy of block distribution
    """
    if len(sequence) < block_size:
        return 0.0
    
    # Extract all blocks of given size
    blocks = []
    for i in range(len(sequence) - block_size + 1):
        block = tuple(sequence[i:i + block_size])
        blocks.append(block)
    
    return compute_shannon_entropy(blocks)


def compute_autocorrelation(sequence: List[int], max_lag: int = 20) -> List[float]:
    """
    Compute normalized autocorrelation function R(k) for lags 0 to max_lag.
    
    R(k) = Cov(X_t, X_{t+k}) / Var(X)
    
    For independent samples, R(k) = 0 for k > 0.
    R(0) = 1 by definition.
    
    Args:
        sequence: List of symbol values
        max_lag: Maximum lag to compute
        
    Returns:
        List of autocorrelation values for lags 0, 1, ..., max_lag
    """
    n = len(sequence)
    if n < max_lag + 1:
        max_lag = n - 1
    
    # Compute mean and variance
    mean = sum(sequence) / n
    variance = sum((x - mean) ** 2 for x in sequence) / n
    
    if variance == 0:
        return [1.0] + [0.0] * max_lag
    
    autocorr = []
    for k in range(max_lag + 1):
        if k == 0:
            autocorr.append(1.0)
        else:
            covariance = sum(
                (sequence[t] - mean) * (sequence[t + k] - mean)
                for t in range(n - k)
            ) / (n - k)
            autocorr.append(covariance / variance)
    
    return autocorr


def compute_mutual_information(sequence: List[int], lag: int = 1) -> float:
    """
    Compute mutual information I(X_t; X_{t+lag}) between lagged symbols.
    
    I(X;Y) = H(X) + H(Y) - H(X,Y)
    
    For independent symbols, I = 0.
    High I indicates predictability (knowing X helps predict Y).
    
    Args:
        sequence: List of symbol values
        lag: Time lag between symbols
        
    Returns:
        Mutual information in bits
    """
    if len(sequence) < lag + 1:
        return 0.0
    
    # Extract lagged pairs
    x_seq = sequence[:-lag]
    y_seq = sequence[lag:]
    
    # H(X), H(Y)
    h_x = compute_shannon_entropy(x_seq)
    h_y = compute_shannon_entropy(y_seq)
    
    # H(X,Y) - joint entropy
    pairs = list(zip(x_seq, y_seq))
    h_xy = compute_shannon_entropy(pairs)
    
    return h_x + h_y - h_xy


def compute_entropy_rate(sequence: List[int], max_block: int = 5) -> float:
    """
    Estimate entropy rate h = lim_{n->inf} H(X_n | X_1, ..., X_{n-1}).
    
    Approximated as H(block_n) - H(block_{n-1}) for large n.
    For independent symbols, entropy rate = H(single symbol).
    
    Args:
        sequence: List of symbol values
        max_block: Maximum block size to use
        
    Returns:
        Estimated entropy rate in bits
    """
    if len(sequence) < max_block + 1:
        return compute_shannon_entropy(sequence)
    
    # Use difference of block entropies
    h_n = compute_block_entropy(sequence, max_block)
    h_n_minus_1 = compute_block_entropy(sequence, max_block - 1)
    
    return h_n - h_n_minus_1


def autocorr_decay_rate(autocorr: List[float]) -> float:
    """
    Estimate exponential decay rate of autocorrelation.
    
    Fit |R(k)| ~ exp(-k/tau), return 1/tau.
    Faster decay = less memory = more random-like.
    
    Args:
        autocorr: Autocorrelation values for lags 0, 1, 2, ...
        
    Returns:
        Decay rate (higher = faster decay)
    """
    # Find first k where |R(k)| < 0.1 (90% decay)
    for k in range(1, len(autocorr)):
        if abs(autocorr[k]) < 0.1:
            return 1.0 / k
    
    # If never decays to 0.1, use the full length
    return 1.0 / len(autocorr)


# =============================================================================
# TESTS: SHANNON ENTROPY
# =============================================================================

class ShannonEntropyMaximal(Test):
    """
    Is the vertex sequence maximally random? Shannon entropy quantifies
    the average information content. For 8 equiprobable symbols, the
    maximum possible entropy is log2(8) = 3 bits.
    """
    name = "Shannon Entropy Near Maximum"
    question = (
        "How random is the vertex sequence? "
        "If vertices were chosen uniformly at random, entropy would be 3 bits. "
        "Low entropy would reveal hidden structure or bias. Is pi's traversal "
        "information-theoretically close to random?"
    )
    reference = "Maximum entropy = log2(8) = 3 bits"
    tolerance = 0.05
    level = Standard
    
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Good 'how random' hook with clear stakes. "
        "Derivation: 14/15 - Excellent intuition with coin flip analogy. "
        "Commentary: 14/15 - Strong insight about pi's digit normality. "
        "Model: 10/10 - Good summary with efficiency metric. "
        "Observations: 9/10 - Maximum entropy well-defined. "
        "Constants: 10/10 - All from common modules. "
        "Accessibility: 13/15 - Undergrad can follow with coin analogy. "
        "Header: 8/10 - Good module header with academic context. "
        "SAMPLE SIZE: 1000 digits - ADEQUATE for entropy estimation."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("CONTEXT: Shannon entropy measures uncertainty in a random variable.")
            .step("DEFINITION: H = -sum(p_i * log2(p_i)) where p_i is probability of symbol i.")
            .step("For 8 equiprobable symbols: H_max = -8 * (1/8) * log2(1/8) = 3 bits.")
            .step("INTUITION: A fair 8-sided die has 3 bits of entropy per roll.")
            .step("If one face appears more often, entropy decreases (less surprise).")
            .step("MEASURE: Compute empirical entropy from vertex frequencies.")
            .step("CRITERION: H > 2.9 bits indicates near-maximal randomness.")
            .conclude("Entropy close to 3 bits confirms uniform-like visitation.")
        )
    
    commentary = (
        "Shannon entropy answers: 'How surprised am I, on average, by each vertex?' "
        "Maximum surprise (3 bits) means the sequence is as unpredictable as possible "
        "given 8 choices. The traversal achieves near-maximal entropy, confirming that "
        "pi's base-8 digits produce a sequence without obvious patterns or biases. "
        "This aligns with the conjecture that pi is a 'normal' number, meaning its "
        "digits are statistically indistinguishable from random in every base."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        vertices = [step['vertex'] for step in traversal]
        
        entropy = compute_shannon_entropy(vertices)
        max_entropy = math.log2(8)  # = 3.0
        efficiency = entropy / max_entropy  # How close to maximum?
        
        return (
            Model()
            .add("Shannon entropy (bits)", round(entropy, 4), tol=0.005)
            .add("Maximum possible (bits)", max_entropy)
            .add("Entropy efficiency", round(efficiency, 4), tol=0.005)
            .add("Near maximal (>97%)", 1 if efficiency > 0.97 else 0)
        )
    
    def observations(self):
        # Independent uniform vertices: H = log2(8) = 3 bits. The plug-in
        # estimator over N = 1001 samples is biased low by about
        # (8 - 1) / (2 N ln 2) = 0.005 bits, so the expected value is 2.995.
        return (
            Observed()
            .add("Shannon entropy (bits)", 2.995)
            .add("Entropy efficiency", round(2.995 / 3, 4))
            .add("Near maximal (>97%)", 1)
        )

class BlockEntropyScaling(Test):
    """
    Does entropy scale linearly with block size? For independent symbols,
    H(n-gram) = n * H(symbol). Sublinear scaling reveals dependencies.
    """
    name = "Block Entropy Scaling"
    question = (
        "Are consecutive vertices independent, or do patterns emerge? "
        "If each vertex is independent, the entropy of pairs should be twice "
        "the entropy of singles. Sublinear scaling would reveal hidden structure."
    )
    reference = "Linear scaling for independence"
    tolerance = 0.10
    level = Standard
    
    audit_score = 90
    audit_notes = (
        "Question: 13/15 - Good independence testing framing. "
        "Derivation: 14/15 - Clear explanation of scaling. "
        "Commentary: 13/15 - Good practical interpretation. "
        "Model: 9/10 - Good ratio comparison. "
        "Observations: 9/10 - Theoretical values well-justified. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 12/15 - Graduate level, could add more intuition. "
        "Header: 10/10 - Module header excellent."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: For n independent symbols, joint entropy H(X1,...,Xn) = n*H(X).")
            .step("Block entropy H(n) measures entropy of n-grams (consecutive n symbols).")
            .step("SCALING: H(1) = entropy of single symbols.")
            .step("         H(2) = entropy of pairs. If independent, H(2) = 2*H(1).")
            .step("         H(3) = entropy of triples. If independent, H(3) = 3*H(1).")
            .step("RATIO: H(2)/H(1) should be close to 2 for independent symbols.")
            .step("Sublinearity (ratio < 2) indicates predictability/patterns.")
            .conclude("Ratio near 2 confirms independence; lower reveals structure.")
        )
    
    commentary = (
        "Block entropy scaling reveals whether knowing one vertex helps predict the next. "
        "If pairs have only 1.8x the entropy of singles (instead of 2x), some information "
        "is 'shared' between consecutive vertices. The pi traversal shows near-linear "
        "scaling, confirming that each step is nearly independent of the previous one. "
        "This is expected because the next vertex depends on the digit, not the current vertex."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        vertices = [step['vertex'] for step in traversal]
        
        h1 = compute_shannon_entropy(vertices)
        h2 = compute_block_entropy(vertices, 2)
        h3 = compute_block_entropy(vertices, 3)
        
        # Ratios (should be near 2 and 3 for independence)
        ratio_2_1 = h2 / h1 if h1 > 0 else 0
        ratio_3_1 = h3 / h1 if h1 > 0 else 0
        
        # Check if scaling is approximately linear
        linear_scaling = 1 if ratio_2_1 > 1.9 and ratio_3_1 > 2.8 else 0
        
        return (
            Model()
            .add("H(1) single entropy", round(h1, 4))
            .add("H(2) pair entropy", round(h2, 4), tol=0.01)
            .add("H(3) triple entropy", round(h3, 4), tol=0.015)
            .add("Ratio H(2)/H(1)", round(ratio_2_1, 3), tol=0.01)
            .add("Ratio H(3)/H(1)", round(ratio_3_1, 3), tol=0.015)
            .add("Near linear scaling", linear_scaling)
        )
    
    def observations(self):
        # Independent uniform vertices: H(n) = 3n bits in the limit. With 1001
        # samples the plug-in estimates are biased low, most for triples (512
        # cells). Expected values at this sample size (mean over 200 random
        # sequences): H(2) = 5.954, H(3) = 8.580, ratios 1.988 and 2.865.
        return (
            Observed()
            .add("H(2) pair entropy", 5.954)
            .add("H(3) triple entropy", 8.580)
            .add("Ratio H(2)/H(1)", 1.988)
            .add("Ratio H(3)/H(1)", 2.865)
            .add("Near linear scaling", 1)
        )

# =============================================================================
# TESTS: AUTOCORRELATION
# =============================================================================

class AutocorrelationDecay(Test):
    """
    Does the autocorrelation function decay rapidly to zero?
    For independent samples, R(k) = 0 for all k > 0.
    Persistent autocorrelation indicates memory or periodicity.
    """
    name = "Autocorrelation Rapid Decay"
    question = (
        "Does knowing the current vertex help predict the next? "
        "Autocorrelation measures the 'memory' of a sequence. "
        "For a truly random sequence, autocorrelation is zero at all lags. "
        "Does pi's traversal exhibit memory?"
    )
    reference = "R(k) = 0 for k > 0 (independence)"
    tolerance = 0.15
    level = Standard
    
    audit_score = 93
    audit_notes = (
        "Question: 14/15 - Excellent 'memory' framing. "
        "Derivation: 14/15 - Clear explanation of autocorrelation. "
        "Commentary: 14/15 - Strong insight about determinism vs randomness. "
        "Model: 10/10 - Good summary with max autocorrelation. "
        "Observations: 9/10 - Independence criterion clear. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 14/15 - Good analogy to coin flips. "
        "Header: 8/10 - Module header good."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("DEFINITION: Autocorrelation R(k) = Cov(X_t, X_{t+k}) / Var(X).")
            .step("R(0) = 1 always (a value is perfectly correlated with itself).")
            .step("For independent samples: R(k) = 0 for k > 0.")
            .step("INTUITION: Think of coin flips. Knowing flip #5 does not help predict #10.")
            .step("If R(5) is large, there is a pattern relating values 5 steps apart.")
            .step("MEASURE: Compute R(k) for k = 1, 2, ..., 20.")
            .step("CRITERION: Max |R(k)| < 0.1 for k > 0 indicates near-independence.")
            .conclude("Rapid decay to zero confirms no significant memory.")
        )
    
    commentary = (
        "The autocorrelation function is the 'memory detector' of time series analysis. "
        "The traversal shows very low autocorrelation at all lags, meaning each vertex "
        "carries almost no information about future vertices. This seems paradoxical "
        "because the sequence is deterministic (driven by pi). But determinism does not "
        "imply predictability: the pattern of pi's digits is so complex that the sequence "
        "appears statistically random. This is the hallmark of a normal number."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        vertices = [step['vertex'] for step in traversal]
        
        autocorr = compute_autocorrelation(vertices, max_lag=20)
        
        # Exclude lag 0 (which is always 1)
        max_nonzero_lag = max(abs(r) for r in autocorr[1:])
        
        # Check key lags
        r1 = autocorr[1]  # Lag 1
        r5 = autocorr[5]  # Lag 5
        r10 = autocorr[10]  # Lag 10
        
        low_memory = 1 if max_nonzero_lag < 0.15 else 0
        
        return (
            Model()
            .add("R(1) lag-1 autocorr", round(r1, 4), abs_tol=0.11)
            .add("R(5) lag-5 autocorr", round(r5, 4), abs_tol=0.11)
            .add("R(10) lag-10 autocorr", round(r10, 4), abs_tol=0.11)
            .add("Max |R(k)| for k>0", round(max_nonzero_lag, 4))
            .add("Low memory (<0.15)", low_memory)
        )
    
    def observations(self):
        # For independent vertices R(k) = 0 for k > 0, with sampling error of
        # about 1/sqrt(N) = 0.032. Each lag is checked against 0 with an absolute
        # bound of 0.11 (about 3.5 standard errors).
        return (
            Observed()
            .add("R(1) lag-1 autocorr", 0.0)
            .add("R(5) lag-5 autocorr", 0.0)
            .add("R(10) lag-10 autocorr", 0.0)
            .add("Low memory (<0.15)", 1)
        )

class MutualInformationLow(Test):
    """
    Is mutual information between consecutive vertices close to zero?
    I(X;Y) = 0 for independent random variables.
    High mutual information indicates predictability.
    """
    name = "Mutual Information Near Zero"
    question = (
        "How much does the current vertex 'tell' us about the next? "
        "Mutual information measures shared information between variables. "
        "For independent vertices, I(X_t; X_{t+1}) = 0. "
        "Does knowing vertex t help predict vertex t+1?"
    )
    reference = "I = 0 for independence"
    tolerance = 0.10
    level = Standard
    
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good 'tell us' predictability framing. "
        "Derivation: 13/15 - Clear MI definition with examples. "
        "Commentary: 14/15 - Strong connection to predictability. "
        "Model: 9/10 - Good fraction of maximum MI. "
        "Observations: 9/10 - Independence criterion clear. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 13/15 - Graduate level, good examples. "
        "Header: 9/10 - Module header good."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("DEFINITION: Mutual information I(X;Y) = H(X) + H(Y) - H(X,Y).")
            .step("I measures how much knowing X reduces uncertainty about Y.")
            .step("I = 0 means X and Y are independent (no shared information).")
            .step("I = H(X) means X determines Y completely (maximum dependence).")
            .step("For consecutive vertices: I(X_t; X_{t+1}) measures predictability.")
            .step("UPPER BOUND: I <= min(H(X), H(Y)) = 3 bits for 8-symbol sequences.")
            .step("CRITERION: I < 0.3 bits indicates weak dependence.")
            .conclude("Low mutual information confirms near-independence.")
        )
    
    commentary = (
        "Mutual information captures both linear and nonlinear dependencies, unlike "
        "autocorrelation which only detects linear relationships. Low MI confirms that "
        "the vertex sequence has little predictability: even sophisticated pattern "
        "recognition would fail to forecast the next vertex better than random guessing. "
        "This validates that pi's digits, despite being deterministic, appear "
        "information-theoretically random in how they drive the traversal."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        vertices = [step['vertex'] for step in traversal]
        
        mi_1 = compute_mutual_information(vertices, lag=1)
        mi_2 = compute_mutual_information(vertices, lag=2)
        mi_5 = compute_mutual_information(vertices, lag=5)
        
        max_possible = 3.0  # log2(8) bits
        mi_fraction = mi_1 / max_possible
        
        low_predictability = 1 if mi_1 < 0.3 else 0
        
        return (
            Model()
            .add("I(t, t+1) lag-1 MI", round(mi_1, 4), abs_tol=0.035)
            .add("I(t, t+2) lag-2 MI", round(mi_2, 4), abs_tol=0.035)
            .add("I(t, t+5) lag-5 MI", round(mi_5, 4), abs_tol=0.035)
            .add("Fraction of max MI", round(mi_fraction, 4))
            .add("Low predictability (<0.3)", low_predictability)
        )
    
    def observations(self):
        # For independent vertices the true mutual information is 0. The plug-in
        # estimate over 1001 samples is biased up by about (8 - 1)^2 / (2 N ln 2)
        # = 0.035 bits; 99% of random sequences give less than 0.066 bits.
        return (
            Observed()
            .add("I(t, t+1) lag-1 MI", 0.035)
            .add("I(t, t+2) lag-2 MI", 0.035)
            .add("I(t, t+5) lag-5 MI", 0.035)
            .add("Low predictability (<0.3)", 1)
        )

# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    ShannonEntropyMaximal,
    BlockEntropyScaling,
    AutocorrelationDecay,
    MutualInformationLow,
]


def run_all():
    """Run all information theory tests."""
    return run_tests(
        title="Information Theory Analysis",
        summary=(
            "Information theory provides rigorous measures of randomness and "
            "structure. Shannon entropy quantifies unpredictability (max 3 bits "
            "for 8 symbols). Autocorrelation detects temporal memory. Mutual "
            "information measures predictability between consecutive vertices. "
            "The traversal achieves near-maximal entropy with low autocorrelation "
            "and mutual information, confirming that pi's digits produce a "
            "statistically random-like sequence despite being deterministic."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
