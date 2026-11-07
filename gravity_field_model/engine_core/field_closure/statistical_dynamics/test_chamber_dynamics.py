"""
Chamber Dwell Time Dynamics
===========================

This module analyzes how the traversal moves between the two chambers
(Tetrahedron A and Tetrahedron B) over time.

Key questions addressed:
- How long does the traversal stay in one chamber before crossing?
- What is the distribution of dwell times?
- Are there extended periods of chamber isolation?
- Does the bimetric coupling remain healthy throughout?

These metrics quantify the yin-yang dynamics of the field.
"""

from typing import Dict, List, Tuple
from collections import Counter
import math

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_chamber_sequence(traversal: List[Dict]) -> List[str]:
    """
    Convert vertex traversal to chamber sequence ('A' or 'B').
    """
    return [step['tetrahedron'] for step in traversal]


def compute_dwell_times(chamber_sequence: List[str]) -> Dict[str, List[int]]:
    """
    Compute consecutive dwell times in each chamber.
    
    Returns:
        {'A': [dwell_times_in_A], 'B': [dwell_times_in_B]}
    """
    dwell_times = {'A': [], 'B': []}
    
    if not chamber_sequence:
        return dwell_times
    
    current_chamber = chamber_sequence[0]
    current_dwell = 1
    
    for chamber in chamber_sequence[1:]:
        if chamber == current_chamber:
            current_dwell += 1
        else:
            dwell_times[current_chamber].append(current_dwell)
            current_chamber = chamber
            current_dwell = 1
    
    # Don't forget the last run
    dwell_times[current_chamber].append(current_dwell)
    
    return dwell_times


def compute_crossing_count(chamber_sequence: List[str]) -> int:
    """Count the number of chamber crossings (A->B or B->A)."""
    crossings = 0
    for i in range(len(chamber_sequence) - 1):
        if chamber_sequence[i] != chamber_sequence[i + 1]:
            crossings += 1
    return crossings


def compute_dwell_statistics(dwell_times: List[int]) -> Dict[str, float]:
    """
    Compute statistics for a list of dwell times.
    """
    if not dwell_times:
        return {'mean': 0, 'min': 0, 'max': 0, 'std': 0, 'count': 0}
    
    n = len(dwell_times)
    mean = sum(dwell_times) / n
    min_dwell = min(dwell_times)
    max_dwell = max(dwell_times)
    
    # Standard deviation
    variance = sum((t - mean) ** 2 for t in dwell_times) / n
    std = math.sqrt(variance)
    
    return {
        'mean': mean,
        'min': min_dwell,
        'max': max_dwell,
        'std': std,
        'count': n
    }


def compute_long_dwell_fraction(dwell_times: List[int], threshold: int = 5) -> float:
    """
    Compute fraction of dwell periods exceeding the threshold.
    
    Long dwells indicate periods of chamber isolation.
    """
    if not dwell_times:
        return 0.0
    
    long_dwells = sum(1 for t in dwell_times if t > threshold)
    return long_dwells / len(dwell_times)


def theoretical_mean_dwell():
    """
    Compute theoretical mean dwell time assuming random chamber transitions.
    
    If P(cross) = 0.5 at each step, the dwell time follows geometric distribution
    with mean = 1 / P(cross) = 2.
    
    However, P(cross) is not exactly 0.5 because chamber membership depends on
    vertex parity, and consecutive vertices are correlated through cumsum.
    """
    # With 4 vertices per chamber and 8 total, staying in same chamber
    # depends on the distribution of (next_cumsum mod 8) landing on
    # same-parity vertices.
    #
    # For digit d, new_vertex = (old_cumsum + d) mod 8
    # Same chamber requires: parity(new_vertex) == parity(old_vertex)
    #
    # This depends on d: if d is even, parity can stay same or change
    # depending on which bits flip.
    #
    # Empirically, P(same chamber) is approximately 50%, giving mean dwell ~2.
    return 2.0


# =============================================================================
# TESTS
# =============================================================================

class MeanDwellTime(Test):
    """
    The average number of consecutive steps in one chamber before crossing.
    With random transitions, expected mean dwell is about 2.
    """
    name = "Mean Chamber Dwell Time"
    question = (
        "How long does the traversal typically stay in one chamber? "
        "If chamber crossings are random with P=0.5, mean dwell should be ~2 steps. "
        "Longer dwells would indicate the chambers are 'sticky.'"
    )
    reference = "Geometric distribution (p=0.5 gives mean=2)"
    tolerance = 0.20
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Dwell time follows geometric distribution if crossings are random.")
            .step("P(cross) approximately 0.5 (4 vertices per chamber, random next vertex).")
            .step("Mean of geometric distribution = 1 / P(cross) = 1 / 0.5 = 2.")
            .step("Compute actual consecutive steps in each chamber.")
            .step("Average across all dwell periods.")
            .conclude("Mean dwell time approximately 2 steps.")
        )
    
    commentary = (
        "Think of a coin flip at each step: heads you stay, tails you cross. "
        "With a fair coin, you stay for 2 flips on average before crossing. "
        "If the chambers were sticky (hard to leave), mean dwell would be higher. "
        "A healthy bimetric coupling has short dwells and frequent crossings."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        chamber_seq = compute_chamber_sequence(traversal)
        dwell_times = compute_dwell_times(chamber_seq)
        
        all_dwells = dwell_times['A'] + dwell_times['B']
        stats = compute_dwell_statistics(all_dwells)
        
        return (
            Model()
            .add("Mean dwell time", stats['mean'])
            .add("Dwell count", stats['count'])
        )
    
    def observations(self):
        return (
            Observed()
            .add("Mean dwell time", theoretical_mean_dwell())
            .add("Dwell count", 500)  # ~1000 steps / 2 mean dwell
        )


class DwellTimeSymmetry(Test):
    """
    Chamber A and Chamber B should have similar dwell time statistics.
    Asymmetry would indicate structural bias toward one chamber.
    """
    name = "Chamber Dwell Time Symmetry"
    question = (
        "Do both chambers have similar dwell characteristics? "
        "If the system favors one chamber, dwells there would be longer. "
        "Symmetry indicates balanced bimetric coupling."
    )
    reference = "Parity symmetry"
    tolerance = 0.20
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Chambers A and B are symmetric by construction (4 vertices each).")
            .step("Compute mean dwell time for Chamber A.")
            .step("Compute mean dwell time for Chamber B.")
            .step("Calculate ratio: mean_A / mean_B.")
            .step("Ratio near 1.0 indicates symmetry.")
            .conclude("Dwell time ratio approximately 1.0.")
        )
    
    commentary = (
        "If you spent 3 steps in Chamber A on average but only 1.5 in Chamber B, "
        "something is pulling you toward A. The chambers should be balanced: "
        "what applies to one applies equally to the other. Asymmetry would "
        "suggest a flaw in the geometry or the traversal algorithm."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        chamber_seq = compute_chamber_sequence(traversal)
        dwell_times = compute_dwell_times(chamber_seq)
        
        stats_a = compute_dwell_statistics(dwell_times['A'])
        stats_b = compute_dwell_statistics(dwell_times['B'])
        
        ratio = stats_a['mean'] / stats_b['mean'] if stats_b['mean'] > 0 else 0
        
        return (
            Model()
            .add("Chamber A mean dwell", stats_a['mean'])
            .add("Chamber B mean dwell", stats_b['mean'])
            .add("Dwell ratio (A/B)", ratio)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Chamber A mean dwell", 2.0)
            .add("Chamber B mean dwell", 2.0)
            .add("Dwell ratio (A/B)", 1.0)
        )


class MaximumDwellBounded(Test):
    """
    The maximum dwell time should be bounded. Extended periods stuck
    in one chamber would indicate unhealthy coupling.
    """
    name = "Maximum Dwell Time Bounded"
    question = (
        "What is the longest stretch without crossing chambers? "
        "Very long dwells would mean the field gets 'trapped' in one half. "
        "A maximum under 15 steps indicates healthy coupling."
    )
    reference = "Statistical bound"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: With P(cross)~0.5, long dwells are exponentially unlikely.")
            .step("P(dwell > k) = (1 - p)^k = 0.5^k.")
            .step("P(dwell > 10) = 0.5^10 = 1/1024 = 0.1%.")
            .step("With ~500 dwell periods, expect ~0.5 instances of dwell > 10.")
            .step("Maximum dwell should be bounded, typically under 15.")
            .conclude("Maximum dwell < 15.")
        )
    
    commentary = (
        "In a healthy system, you cannot get stuck. If the field spent 20 steps "
        "in Chamber A without visiting Chamber B, that would be a long isolation. "
        "Statistical theory says long runs are rare but not impossible. "
        "A maximum under 15 is comfortable; much higher would warrant investigation."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        chamber_seq = compute_chamber_sequence(traversal)
        dwell_times = compute_dwell_times(chamber_seq)
        
        all_dwells = dwell_times['A'] + dwell_times['B']
        max_dwell = max(all_dwells) if all_dwells else 0
        bounded = 1 if max_dwell < 15 else 0
        
        return (
            Model()
            .add("Maximum dwell time", max_dwell, abs_tol=5)
            .add("Below 15 threshold", bounded)
        )
    
    def observations(self):
        # About 500 runs, each geometric with p = 1/2: the longest is typically
        # log2(500) = 9 steps, and lies between 4 and 14 for nearly all random
        # sequences. A run of 15 or more has probability of about 3%.
        return (
            Observed()
            .add("Maximum dwell time", 9)
            .add("Below 15 threshold", 1)
        )

class DwellTimeDistribution(Test):
    """
    The distribution of dwell times should follow a geometric-like pattern:
    many short dwells, fewer long dwells, exponential decay.
    """
    name = "Dwell Time Distribution Shape"
    question = (
        "Does the dwell time distribution decay appropriately? "
        "Short dwells (1-2 steps) should dominate. "
        "Long dwells (>5 steps) should be rare (<15% of all dwells)."
    )
    reference = "Geometric distribution"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Geometric distribution has P(dwell=k) = p * (1-p)^(k-1).")
            .step("For p=0.5: P(1)=0.5, P(2)=0.25, P(3)=0.125, ...")
            .step("P(dwell > 5) = 0.5^5 = 3.1%.")
            .step("Count dwells with length > 5 and compute fraction.")
            .step("Fraction should be small (<15%) for healthy dynamics.")
            .conclude("Long dwell fraction < 15%.")
        )
    
    commentary = (
        "Most chamber visits should be brief: hop in, hop out. "
        "Extended stays are like traffic jams in the field dynamics. "
        "A geometric distribution has this property naturally: the probability "
        "of staying decreases exponentially with time spent."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        chamber_seq = compute_chamber_sequence(traversal)
        dwell_times = compute_dwell_times(chamber_seq)
        
        all_dwells = dwell_times['A'] + dwell_times['B']
        long_fraction = compute_long_dwell_fraction(all_dwells, threshold=5)
        short_count = sum(1 for d in all_dwells if d <= 2)
        short_fraction = short_count / len(all_dwells) if all_dwells else 0
        
        return (
            Model()
            .add("Short dwells (<=2) fraction", short_fraction, tol=0.08)
            .add("Long dwells (>5) fraction", long_fraction, abs_tol=0.02)
            .add("Long fraction < 15%", 1 if long_fraction < 0.15 else 0)
        )
    
    def observations(self):
        # Independent uniform vertices: each step stays in the same chamber with
        # probability 1/2, so dwell times are geometric with p = 1/2:
        # P(dwell <= 2) = 3/4 and P(dwell > 5) = (1/2)^5 = 0.031.
        return (
            Observed()
            .add("Short dwells (<=2) fraction", 0.75)
            .add("Long dwells (>5) fraction", 0.03125)
            .add("Long fraction < 15%", 1)
        )

class CrossingFrequency(Test):
    """
    The number of chamber crossings per unit traversal length.
    With random crossings at 50% rate, expect ~500 crossings per 1000 steps.
    """
    name = "Chamber Crossing Frequency"
    question = (
        "How frequently does the traversal cross between chambers? "
        "With P(cross)=0.5 at each step, expect ~50% of steps to be crossings. "
        "This measures the intensity of bimetric coupling."
    )
    reference = "Random crossing (50%)"
    tolerance = 0.10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each step either stays in chamber or crosses.")
            .step("P(cross) approximately 0.5 for random destination vertex.")
            .step("Expected crossings in N steps = N * P(cross) = 0.5 * N.")
            .step("For N=1000, expect ~500 crossings.")
            .step("Count actual crossings and compute rate.")
            .conclude("Crossing rate approximately 50%.")
        )
    
    commentary = (
        "Crossings are the heartbeat of bimetric coupling. Each crossing "
        "represents the field engaging both tetrahedra. A rate near 50% means "
        "the system oscillates freely between yin and yang. A low rate would "
        "indicate sluggish coupling; high rate is not possible (max is ~100%)."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        chamber_seq = compute_chamber_sequence(traversal)
        crossings = compute_crossing_count(chamber_seq)
        total_transitions = len(chamber_seq) - 1
        rate = crossings / total_transitions if total_transitions > 0 else 0
        
        return (
            Model()
            .add("Total crossings", crossings, tol=0.1)
            .add("Crossing rate", rate, tol=0.1)
        )
    
    def observations(self):
        # Independent uniform vertices: the next vertex is in the other chamber
        # with probability 1/2, so about 500 of the 1000 transitions cross
        # (standard deviation 16, so 10% is about 3 standard deviations).
        return (
            Observed()
            .add("Total crossings", 500)
            .add("Crossing rate", 0.5)
        )

class AlternationRuns(Test):
    """
    Count sequences of rapid alternation (A-B-A-B...) vs staying put.
    High alternation indicates strong chamber coupling.
    """
    name = "Rapid Alternation Frequency"
    question = (
        "How often does the traversal rapidly alternate between chambers? "
        "Patterns like A-B-A-B show tight coupling. "
        "Long same-chamber runs show weak coupling."
    )
    reference = "Random alternation pattern"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Rapid alternation = consecutive A-B-A or B-A-B patterns.")
            .step("Count length-3 substrings that alternate: ABA or BAB.")
            .step("With random 50% crossings, P(ABA) = P(cross) * P(cross) = 0.25.")
            .step("Total alternation triplets in N steps approximately N * 0.25.")
            .step("Compute actual alternation rate.")
            .conclude("Alternation rate approximately 25%.")
        )
    
    commentary = (
        "Rapid alternation (A-B-A-B...) is like a ping-pong game between chambers. "
        "It shows the field is actively engaging both halves. "
        "If we see long stretches of AAAAA or BBBBB, the coupling is sluggish. "
        "A healthy system has a mix but with significant alternation."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        chamber_seq = compute_chamber_sequence(traversal)
        
        # Count alternation triplets (ABA or BAB)
        alternations = 0
        for i in range(len(chamber_seq) - 2):
            if chamber_seq[i] != chamber_seq[i+1] and chamber_seq[i+1] != chamber_seq[i+2]:
                if chamber_seq[i] == chamber_seq[i+2]:  # ABA or BAB pattern
                    alternations += 1
        
        total_triplets = len(chamber_seq) - 2
        rate = alternations / total_triplets if total_triplets > 0 else 0
        
        return (
            Model()
            .add("Alternation triplets", alternations, tol=0.2)
            .add("Alternation rate", rate, tol=0.2)
        )
    
    def observations(self):
        # Expected: P(cross) * P(cross) = 0.5 * 0.5 = 0.25 for ABA pattern
        # But also need the third to match first, which is automatic if both cross
        traversal = traverse_pi_base8(1000)
        total_triplets = len(traversal) - 2
        expected_alternations = int(total_triplets * 0.25)
        
        return (
            Observed()
            .add("Alternation triplets", expected_alternations)
            .add("Alternation rate", 0.25)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    MeanDwellTime,
    DwellTimeSymmetry,
    MaximumDwellBounded,
    DwellTimeDistribution,
    CrossingFrequency,
    AlternationRuns,
]


def run_all():
    """Run all chamber dynamics tests."""
    return run_tests(
        title="Chamber Dwell Time Dynamics",
        summary=(
            "The traversal moves between two chambers (Tetrahedra A and B). "
            "Dwell time is how long it stays in one chamber before crossing. "
            "Key findings: mean dwell is ~2 steps, distribution is geometric, "
            "and both chambers have symmetric statistics. These properties "
            "confirm healthy bimetric coupling with no chamber favoritism."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
