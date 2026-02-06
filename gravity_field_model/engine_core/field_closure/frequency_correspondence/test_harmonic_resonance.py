"""
Harmonic Resonance
==================

This module tests for harmonic structure in orbit periods.

THE QUESTION:
Do orbit lengths show harmonic structure, or are they purely random?

HARMONIC HYPOTHESIS:
If the Field Origin is a resonance node, orbit lengths might cluster
at harmonic ratios (1:2:3:4...) rather than being uniformly distributed.

WHAT WE'RE LOOKING FOR:
- Preferred orbit lengths (not just mean)
- Integer ratios between common orbit lengths
- Resonance peaks in the orbit length distribution

Reference: THE_ORIGIN_TIME_AND_ONE.md (Field Origin as resonance node)
"""

import math
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_orbit_length_distribution(n_digits=10000):
    """
    Compute the distribution of orbit lengths.
    """
    traversal = traverse_pi_base8(n_digits)
    
    orbit_lengths = []
    current_length = 0
    prev_orbit = 0
    
    for step in traversal:
        current_length += 1
        curr_orbit = step['cumsum'] // 8
        
        if curr_orbit > prev_orbit:
            orbit_lengths.append(current_length)
            current_length = 0
            prev_orbit = curr_orbit
    
    return orbit_lengths


def analyze_orbit_distribution(orbit_lengths):
    """
    Analyze the distribution for harmonic structure.
    """
    if not orbit_lengths:
        return {}
    
    # Basic statistics
    mean = sum(orbit_lengths) / len(orbit_lengths)
    variance = sum((L - mean)**2 for L in orbit_lengths) / len(orbit_lengths)
    std = math.sqrt(variance)
    
    # Distribution
    dist = Counter(orbit_lengths)
    total = len(orbit_lengths)
    
    # Find mode (most common)
    mode = dist.most_common(1)[0][0] if dist else 0
    
    # Check for peaks at integer values
    peak_values = [L for L, count in dist.most_common(5)]
    
    # Harmonic ratios: check if peak values are in simple ratios
    harmonic_ratios = []
    for i, L1 in enumerate(peak_values):
        for L2 in peak_values[i+1:]:
            if L2 > 0:
                ratio = L1 / L2
                # Check if close to simple ratio (1, 2, 3, 1/2, 2/3, etc.)
                for n in range(1, 5):
                    for m in range(1, 5):
                        target = n / m
                        if abs(ratio - target) < 0.1:
                            harmonic_ratios.append((L1, L2, f"{n}:{m}"))
    
    return {
        'mean': mean,
        'std': std,
        'mode': mode,
        'distribution': dict(dist.most_common(10)),
        'peak_values': peak_values,
        'harmonic_ratios': harmonic_ratios,
        'total_orbits': total,
        'min_length': min(orbit_lengths),
        'max_length': max(orbit_lengths),
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class OrbitLengthDistribution(Test):
    """
    What is the distribution of orbit lengths?
    
    If the Field Origin is a resonance node, we might see clustering
    at specific values rather than a smooth distribution.
    """
    name = "Orbit Length Distribution"
    question = (
        "What is the distribution of orbit lengths? "
        "Do certain lengths appear more often than expected? "
        "This could indicate resonance structure."
    )
    reference = "Resonance theory, Field Origin as resonance node"
    level = Standard
    tolerance = 0.20
    
    commentary = (
        "INTERPRETING THE DISTRIBUTION: "
        "A smooth distribution suggests no resonance. "
        "Peaks at specific values suggest resonance. "
        "Common orbit lengths: Length 1 = large digit (7) that completes immediately. "
        "Length 2-3 = typical orbits. Length 4+ = sequences of small digits. "
        "The mode being 2 or 3 is consistent with the mean ~2.4."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("ORBIT LENGTH DISTRIBUTION:")
            .step("Measure the length (in digits) of each orbit.")
            .step("For random pi digits:")
            .step("Expected geometric distribution")
            .step("Mean ~ 8 / mean_digit ~ 2.42")
            .step("Some orbits are short (1-2 digits)")
            .step("Some are long (10+ digits)")
            .step("For resonance structure:")
            .conclude("Certain lengths would be preferred. Distribution would have peaks.")
        )
    
    def model(self):
        orbit_lengths = compute_orbit_length_distribution(10000)
        analysis = analyze_orbit_distribution(orbit_lengths)
        
        return (
            Model()
            .add("Total orbits", analysis['total_orbits'])
            .add("Mean length", analysis['mean'])
            .add("Std deviation", analysis['std'])
            .add("Mode (most common)", analysis['mode'])
            .add("Min length", analysis['min_length'])
            .add("Max length", analysis['max_length'])
        )
    
    def observations(self):
        return (
            Observed()
            .add("Expected mean", 2.42)
            .add("Expected mode", 2)
        )


class HarmonicRatioSearch(Test):
    """
    Are common orbit lengths in simple harmonic ratios?
    
    Harmonic systems show resonance at 1:2:3:4... ratios.
    """
    name = "Harmonic Ratio Search"
    question = (
        "Are the most common orbit lengths in simple harmonic ratios (1:2, 2:3, etc.)? "
        "This would indicate the Field Origin is a true resonance node."
    )
    reference = "Harmonic oscillator theory"
    level = Standard
    tolerance = 0.20
    
    commentary = (
        "HARMONIC RATIOS AND RESONANCE: "
        "If common orbit lengths are in simple ratios, the system has harmonic structure. "
        "Physical meaning: The Field Origin as a 'resonance node' would "
        "amplify certain orbit lengths over others. "
        "Finding ratios like 1:2 or 2:3 would support the idea that traversal "
        "is not random, but resonantly structured."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("HARMONIC RATIO SEARCH:")
            .step("Find the 5 most common orbit lengths.")
            .step("Check if they form simple ratios:")
            .step("1:2 (octave)")
            .step("2:3 (perfect fifth)")
            .step("3:4 (perfect fourth)")
            .step("1:1 (unison)")
            .conclude("Harmonic ratios would suggest resonance structure.")
        )
    
    def model(self):
        orbit_lengths = compute_orbit_length_distribution(10000)
        analysis = analyze_orbit_distribution(orbit_lengths)
        
        return (
            Model()
            .add("Peak values (top 5)", len(analysis['peak_values']))
            .add("Harmonic ratios found", len(analysis['harmonic_ratios']))
        )
    
    def observations(self):
        return (
            Observed()
            .add("Expected for resonance (ratios)", 3)
            .add("Expected for random (ratios)", 1)
        )


class SequencePeriodicity(Test):
    """
    Is there periodicity in the sequence of orbit lengths?
    
    Not just the distribution, but the ORDER of orbit lengths.
    """
    name = "Orbit Sequence Periodicity"
    question = (
        "Is there periodicity in the sequence of orbit lengths? "
        "Do short and long orbits alternate in a pattern?"
    )
    reference = "Spectral analysis"
    level = Standard
    tolerance = 0.30
    
    commentary = (
        "SEQUENCE PERIODICITY: "
        "If the power spectrum is flat, the sequence is random. "
        "If there's a dominant frequency, there's periodic structure. "
        "What this would mean: Period 2 = short/long alternation (SLSL...). "
        "Period 3 = triplet pattern (SML SML...). Period 4 = 2-orbit phase pattern. "
        "The spinor property predicts period-2 structure (related to the 720-degree phase period)."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("SEQUENCE PERIODICITY:")
            .step("The sequence of orbit lengths is: L1, L2, L3, ...")
            .step("Does this sequence have periodic structure?")
            .step("Compute autocorrelation at different lags:")
            .step("Lag 1: correlation between consecutive orbits")
            .step("Lag 2: correlation between orbits 2 apart")
            .conclude("High correlation at lag 2 would match spinor property.")
        )
    
    def model(self):
        orbit_lengths = compute_orbit_length_distribution(10000)
        
        # Simple autocorrelation at lag 1 and lag 2
        n = len(orbit_lengths)
        mean = sum(orbit_lengths) / n
        variance = sum((L - mean)**2 for L in orbit_lengths) / n
        
        if variance > 0 and n > 2:
            # Lag 1
            cov1 = sum((orbit_lengths[i] - mean) * (orbit_lengths[i+1] - mean) for i in range(n-1)) / (n-1)
            corr1 = cov1 / variance
            
            # Lag 2
            cov2 = sum((orbit_lengths[i] - mean) * (orbit_lengths[i+2] - mean) for i in range(n-2)) / (n-2)
            corr2 = cov2 / variance
        else:
            corr1 = 0
            corr2 = 0
        
        return (
            Model()
            .add("Total orbits", n)
            .add("Autocorrelation lag 1", corr1)
            .add("Autocorrelation lag 2", corr2)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Expected for random (lag 1)", 0.0)
            .add("Expected for random (lag 2)", 0.0)
        )


# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all harmonic resonance tests."""
    return run_tests(
        "Harmonic Resonance",
        "Tests for harmonic structure in orbit periods",
        [
            OrbitLengthDistribution,
            HarmonicRatioSearch,
            SequencePeriodicity,
        ]
    )


if __name__ == "__main__":
    run_all()
