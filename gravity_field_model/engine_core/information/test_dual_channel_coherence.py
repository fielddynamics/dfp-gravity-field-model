# FILENAME: test_dual_channel_coherence.py

"""
Dual Channel Coherence in Pi Driven Traversal
==============================================

The GFM traversal visits vertex V at each step, but simultaneously determines
the complement vertex 7-V via the implicit channel. This dual channel architecture
is central to the claim that field closure operates at full Compton frequency
rather than half. Standard information theory tells us that a deterministic
function of a random variable carries identical Shannon entropy to the original.
The open question is whether temporal correlations between successive explicit
and implicit channel states reveal structure beyond trivial deterministic coupling.

GFM OBSERVATION: The implicit channel (7-V) guarantees bimetric coverage at every step.

This is an OBSERVATION, not a derivation.
"""

import math
from typing import List, Dict
from collections import Counter, defaultdict

from gravity_field_model.framework import Test, Level, Derivation, Model, Observed, run_tests
from gravity_field_model.common import (
    traverse_pi_base8, TET_A, TET_B, K, VERTICES,
)


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def shannon_entropy(counts: Dict, total: int) -> float:
    """Compute Shannon entropy in bits from a counts dictionary."""
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def joint_entropy_pair(seq_a: List[int], seq_b: List[int]) -> float:
    """Compute joint Shannon entropy H(A,B) for two aligned sequences."""
    n = len(seq_a)
    joint_counts = Counter(zip(seq_a, seq_b))
    return shannon_entropy(joint_counts, n)


def marginal_entropy(seq: List[int]) -> float:
    """Compute marginal Shannon entropy H(X) for a single sequence."""
    n = len(seq)
    counts = Counter(seq)
    return shannon_entropy(counts, n)


def mutual_information(seq_a: List[int], seq_b: List[int]) -> float:
    """Compute I(A;B) = H(A) + H(B) - H(A,B)."""
    ha = marginal_entropy(seq_a)
    hb = marginal_entropy(seq_b)
    hab = joint_entropy_pair(seq_a, seq_b)
    return ha + hb - hab


def cross_channel_temporal_mi(explicit: List[int], implicit: List[int], lag: int) -> float:
    """
    Compute I(E_t; I_{t+lag}) where E is explicit channel and I is implicit.
    This measures how much the current explicit vertex tells us about
    the future implicit vertex (and vice versa for negative interpretation).
    """
    if lag < 0:
        raise ValueError("Lag must be non negative")
    n = len(explicit) - lag
    if n <= 0:
        return 0.0
    e_seq = explicit[:n]
    i_seq = implicit[lag:lag + n]
    return mutual_information(e_seq, i_seq)


def simultaneous_chamber_balance(explicit: List[int], implicit: List[int]) -> float:
    """
    At each step, check whether explicit and implicit land in different chambers.
    Returns the fraction of steps where both chambers are simultaneously active.
    """
    both_count = 0
    for e, i in zip(explicit, implicit):
        e_chamber = 0 if e in TET_A else 1
        i_chamber = 0 if i in TET_A else 1
        if e_chamber != i_chamber:
            both_count += 1
    return both_count / len(explicit)


def conditional_entropy_next_given_both(explicit: List[int], implicit: List[int]) -> float:
    """
    Compute H(E_{t+1} | E_t, I_t).
    This measures the residual uncertainty in the next explicit vertex
    given the current state of BOTH channels.
    Compare to H(E_{t+1} | E_t) to see if the implicit channel adds information.
    """
    n = len(explicit) - 1

    # H(E_{t+1} | E_t, I_t)
    joint_context_counts = defaultdict(lambda: defaultdict(int))
    for i in range(n):
        context = (explicit[i], implicit[i])
        target = explicit[i + 1]
        joint_context_counts[context][target] += 1

    h_joint = 0.0
    for context, targets in joint_context_counts.items():
        context_total = sum(targets.values())
        p_context = context_total / n
        h_ctx = 0.0
        for c in targets.values():
            if c > 0:
                p = c / context_total
                h_ctx -= p * math.log2(p)
        h_joint += p_context * h_ctx

    # H(E_{t+1} | E_t)
    single_context_counts = defaultdict(lambda: defaultdict(int))
    for i in range(n):
        context = explicit[i]
        target = explicit[i + 1]
        single_context_counts[context][target] += 1

    h_single = 0.0
    for context, targets in single_context_counts.items():
        context_total = sum(targets.values())
        p_context = context_total / n
        h_ctx = 0.0
        for c in targets.values():
            if c > 0:
                p = c / context_total
                h_ctx -= p * math.log2(p)
        h_single += p_context * h_ctx

    return h_joint, h_single


class DualChannelCoherenceProbe(Test):
    """
    PHYSICAL CONTEXT:
    In any deterministic dynamical system, applying a fixed invertible map
    to a sequence produces a new sequence with identical marginal entropy.
    The complement map V -> 7-V is such a map on the 8 vertex Merkaba.
    Standard information theory (Cover and Thomas, 2006) guarantees that
    H(implicit) = H(explicit) at every timescale. The nontrivial question
    is whether temporal cross channel correlations, I(E_t; I_{t+lag}),
    reveal structure, and whether conditioning on both channels reduces
    uncertainty about future states beyond what either channel alone provides.

    GFM OBSERVATION:
    The complement map 7-V deterministically maps TetA vertices to TetB
    and vice versa. This guarantees that at every traversal step, both
    chambers are simultaneously determined: the dual channel architecture
    gives 2^d = 8 = 2*K coverage at every tick. The bimetric balance
    fraction (both chambers active simultaneously) should be identically
    1.0 since vertices in TetA = {1,2,4,7} always complement to TetB
    = {0,3,5,6} and vice versa.

    EPISTEMIC STATUS:
    The marginal entropy equality is a mathematical theorem. The bimetric
    balance of 1.0 is a deterministic consequence of the complement map.
    The cross channel temporal mutual information profile is an empirical
    observation about the pi driven traversal that probes whether the
    dual channel carries exploitable temporal structure.
    """

    name = "Dual Channel Coherence (Explicit vs Implicit)"

    question = (
        "Does the implicit channel (complement vertex 7-V) carry temporal "
        "information beyond what the explicit channel alone provides? "
        "The marginal entropies must match by construction, but cross channel "
        "temporal correlations could reveal hidden structure in the pi driven "
        "traversal. Does conditioning on both channels at time t reduce "
        "uncertainty about the next explicit vertex at t+1?"
    )

    reference = (
        "Cover and Thomas, Elements of Information Theory (2006); "
        "Schreiber, Measuring Information Transfer, PRL 85 (2000); "
        "GFM Paper VII Section 3.1, Dual Channel Architecture"
    )

    tolerance = 0.05

    level = Level.EXPLORATORY

    commentary = (
        "Standard information theory guarantees that H(7-V) = H(V) for any "
        "sequence, since the complement is a bijection. The bimetric balance "
        "fraction must be exactly 1.0 because TetA and TetB are complementary "
        "sets under V -> 7-V. These are mathematical certainties, not empirical "
        "findings. The genuinely exploratory quantity is the cross channel "
        "temporal mutual information: does knowing the implicit state at time t "
        "help predict the explicit state at t+1 beyond what the explicit state "
        "at t already tells us? For a memoryless ergodic process, the implicit "
        "channel should add zero predictive power, since it is a deterministic "
        "function of the explicit channel at the same timestep. This test "
        "documents the observation that the pi traversal is consistent with "
        "memoryless behavior across channels, confirming that the dual channel "
        "architecture provides simultaneous bimetric coverage without introducing "
        "temporal asymmetry. This is an observation about the traversal, not a "
        "derivation from first principles."
    )

    # Audit scoring
    audit_score = 82
    audit_notes = (
        "Question: 13/15 (asks a clear 'does X carry information beyond Y' question with specific mechanism, but the stakes could be sharpened: the reader needs more upfront tension about WHY this matters for Compton frequency claims). Derivation: 13/15 (excellent logical progression from bijection theorem through bimetric balance to temporal structure, intuition precedes math throughout, but the predictive gain argument could use a one sentence analogy to make the deterministic function point more vivid for non experts). Commentary: 12/15 (clearly distinguishes mathematical certainties from empirical observations, honest about epistemic status, includes 'observation not a derivation' language, but lacks an everyday analogy and does not spell out implications for the broader GFM program or what a nonzero result would have meant). Model: 9/10 (clean 5 quantity summary, good mix of ratios and absolute values, binary style verdicts implicit in the 0.0/1.0 targets, descriptive names with units). Observations: 7/10 (the 1.0 and 0.0 values are mathematically justified and explained in derivation, but the cross channel MI and predictive gain targets of exactly 0.0 are theoretical limits for perfect memorylessness rather than empirically sourced values, and no tolerance discussion for finite sample bias near zero). Constants: 9/10 (all traversal functions and geometry constants imported from common, K and VERTICES imported even though K is only used conceptually in the docstring, no hardcoded physics constants, minor note: math.log2(8) could reference 2**d or 2*K for tighter traceability). Accessibility: 12/15 (graduate level accessible, explains bijection and conditional entropy concepts, but assumes familiarity with mutual information and conditional entropy notation without defining them in plain language first, the jump from 'bijection preserves entropy' to 'predictive gain is zero' needs one more bridging sentence for undergrads). Header: 7/10 (good scope statement, explains the physical phenomenon and GFM observation, includes epistemic status section, but missing explicit target audience level and could better summarize what questions are answered versus left open)."
    )

    academic_paper = """\
TITLE Dual Channel Coherence in the Pi Driven Merkaba Traversal: Information Theoretic Probing of the Implicit Complement Channel ABSTRACT We investigate whether the implicit complement channel (vertex 7-V) carries temporal information beyond the explicit channel in the GFM pi driven traversal. Using Shannon entropy, cross channel mutual information, and conditional entropy analysis over 10000 traversal steps, we find results consistent with memoryless ergodic behavior and perfect bimetric balance. The entropy equality and balance fraction are mathematical theorems; the temporal independence is an empirical observation. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The Gravity Field Model posits that at every traversal step visiting vertex V, the complement vertex 7-V is simultaneously determined. This dual channel architecture is central to the claim that field closure operates at full Compton frequency rather than half: both tetrahedra have a known state at every tick. The explicit channel reads V directly from the pi base 8 cumulative sum; the implicit channel obtains 7-V by the complement map. Standard information theory (Cover and Thomas, 2006) guarantees that any bijection preserves Shannon entropy. Since V maps to 7-V is an involution on {0,1,...,7}, the implicit channel must carry identical marginal entropy to the explicit channel. This is a theorem, not an empirical finding. Similarly, because TetA = {1,2,4,7} and TetB = {0,3,5,6} are complementary under the 7-V map, both chambers are necessarily active at every step. The genuinely open question is temporal: does knowing the implicit channel state at time t reduce uncertainty about the explicit channel at time t+1, beyond what the explicit channel at time t already provides? If the traversal is memoryless, the implicit channel at time t is a deterministic function of the explicit channel at t, and conditioning on it given the explicit state adds zero predictive power. Nonzero predictive gain would indicate exploitable temporal structure in the dual channel system. This test specifically investigates the cross channel temporal mutual information I(E_t; I_{t+1}) and the predictive gain from conditioning on both channels simultaneously. 2. METHODOLOGY We generate 10000 traversal steps from pi in base 8 using the standard cumulative sum algorithm with the integer part included. For each step, the explicit vertex V and implicit vertex 7-V are recorded. We compute five quantities: the entropy ratio H(implicit)/H(explicit), the bimetric balance fraction, the cross channel mutual information at lag 1, the predictive gain defined as H(E_{t+1}|E_t) minus H(E_{t+1}|E_t, I_t), and the explicit entropy efficiency relative to the 3 bit maximum. Expected values are 1.0, 1.0, 0.0, 0.0, and 1.0 respectively. Agreement is assessed at 5% tolerance, with the understanding that the first two quantities are mathematical certainties and the latter three are empirical measurements subject to finite sample fluctuation. 3. RESULTS The model calculates an entropy ratio of 1.0 (exact to numerical precision), confirming the bijection theorem. The bimetric balance fraction is 1.0: every step activates both chambers simultaneously, as guaranteed by the complement structure. The cross channel mutual information at lag 1 is consistent with zero, indicating no temporal correlation between the current explicit vertex and the next implicit vertex beyond what same channel autocorrelation provides. The predictive gain from adding the implicit channel is consistent with zero, confirming that I_t = 7 minus E_t adds no information given E_t. The explicit entropy efficiency approaches 1.0, consistent with prior ergodicity validations showing Shannon entropy near 2.99 out of 3.0 bits. 4. DISCUSSION The entropy equality and bimetric balance results are mathematical necessities, not discoveries. Their inclusion serves as internal consistency verification. The scientifically meaningful results are the temporal quantities. The near zero cross channel mutual information at lag 1 is consistent with the established observation that the pi traversal exhibits negligible autocorrelation. The zero predictive gain confirms that the implicit channel, while guaranteeing simultaneous bimetric coverage, carries no temporally exploitable structure beyond the explicit channel. EPISTEMIC STATUS: The entropy equality and bimetric balance are DERIVATIONS from the complement bijection. The temporal independence is an OBSERVATION about the pi driven traversal. We do not derive why pi in base 8 produces memoryless statistics. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove the dual channel architecture has physical significance. The zero predictive gain follows trivially from the deterministic relationship I_t = 7 minus E_t
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD INFORMATION THEORY:")
            .step("For any bijection f, H(f(X)) = H(X). The complement map "
                  "V -> 7-V is a bijection on {0,1,...,7}.")
            .equation("H(implicit) = H(explicit)")
            .step("Joint entropy of simultaneous (E_t, I_t) pair: since I_t = 7 - E_t "
                  "is deterministic, H(E_t, I_t) = H(E_t). No new information.")
            .equation("I(E_t; I_t) = H(E_t) + H(I_t) - H(E_t, I_t) = H(E_t)")
            .step("BIMETRIC BALANCE:")
            .step("TetA = {1,2,4,7}, TetB = {0,3,5,6}. Complement of any TetA "
                  "vertex is in TetB and vice versa. Therefore both chambers are "
                  "always simultaneously active.")
            .equation("bimetric_balance_fraction = 1.0")
            .step("CROSS CHANNEL TEMPORAL STRUCTURE:")
            .step("I(E_t; I_{t+1}) measures whether the current explicit vertex "
                  "predicts the next implicit vertex. Since I_{t+1} = 7 - E_{t+1}, "
                  "this equals I(E_t; E_{t+1}), the standard autocorrelation.")
            .equation("I(E_t; I_{t+1}) = I(E_t; 7 - E_{t+1}) = I(E_t; E_{t+1})")
            .step("For a memoryless process, I(E_t; E_{t+1}) approaches 0.")
            .step("PREDICTIVE GAIN from implicit channel:")
            .equation("gain = H(E_{t+1}|E_t) - H(E_{t+1}|E_t, I_t)")
            .step("Since I_t is a deterministic function of E_t, conditioning on "
                  "I_t given E_t adds nothing. Gain should be 0.")
            .conclude("The dual channel provides guaranteed bimetric coverage "
                      "(balance = 1.0) with zero redundant temporal information, "
                      "consistent with memoryless ergodic traversal.")
        )

    def model(self) -> Model:
        n_steps = 10000
        history = get_vertex_history(n_steps)

        # Build explicit and implicit sequences
        explicit = history
        implicit = [7 - v for v in history]

        # 1. Marginal entropies (should match)
        h_explicit = marginal_entropy(explicit)
        h_implicit = marginal_entropy(implicit)
        entropy_ratio = h_implicit / h_explicit if h_explicit > 0 else 0.0

        # 2. Bimetric balance (fraction where both chambers simultaneously active)
        balance = simultaneous_chamber_balance(explicit, implicit)

        # 3. Cross channel temporal MI at lag=1
        # I(E_t; I_{t+1}) which equals I(E_t; E_{t+1}) by determinism
        cross_mi_lag1 = cross_channel_temporal_mi(explicit, implicit, lag=1)

        # 4. Predictive gain from adding implicit channel
        h_next_given_both, h_next_given_explicit = conditional_entropy_next_given_both(
            explicit, implicit
        )
        predictive_gain = h_next_given_explicit - h_next_given_both

        # 5. Maximum possible entropy for 8 symbols = 3.0 bits
        max_entropy = math.log2(8)
        explicit_efficiency = h_explicit / max_entropy

        return (
            Model()
            .add("Entropy ratio H(implicit)/H(explicit)", entropy_ratio)
            .add("Bimetric balance fraction", balance)
            .add("Cross channel MI at lag 1 (bits)", cross_mi_lag1)
            .add("Predictive gain from implicit (bits)", predictive_gain)
            .add("Explicit entropy efficiency", explicit_efficiency)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Entropy ratio H(implicit)/H(explicit)", 1.0)
            .add("Bimetric balance fraction", 1.0)
            # The plug-in MI estimate of two independent 8-symbol variables
            # is not zero but has expectation (8-1)^2 / (2 N ln 2) bits
            # (Miller-Madow bias; 2 N ln2 * MI follows chi-squared with 49
            # degrees of freedom). For N = 9999 pairs that is 0.00354 bits,
            # standard deviation sqrt(98) / (2 N ln2) = 0.00071 bits. The
            # tolerance is 3.3 standard deviations. Comparing with exactly 0
            # by relative error failed for any finite sample.
            .add("Cross channel MI at lag 1 (bits)", 49.0 / (2 * 9999 * math.log(2)),
                 abs_tol=0.0024)
            .add("Predictive gain from implicit (bits)", 0.0, abs_tol=1e-12)
            .add("Explicit entropy efficiency", 1.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    run_tests(
        title="Dual Channel Coherence Probing",
        summary="Tests whether the implicit complement channel carries temporal structure beyond the explicit channel",
        test_classes=[DualChannelCoherenceProbe],
    )
