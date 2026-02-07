"""
Lemniscate Topology Tests
=========================

PROBING TESTS: Not fitting expected results, but discovering structure.

The user's insight: The gravity field is in "mitosis" with a subspace
gravity field. The net field is only HALF in our (3+1) space. The
Field Origin is like an infinity sign (lemniscate) where the net
field exists at the crossing point.

These tests PROBE this hypothesis:

TEST 1: ZeroNetFieldAtOrigin
    If the origin is the crossing point of the lemniscate, all
    directional quantities should sum to zero there. DISCOVERY test.

TEST 2: ExactHalfPartition
    Is exactly 50% of something (energy, information, vertices) in
    each half? Or is there asymmetry? DISCOVERY test.

TEST 3: LemniscateCirculationPattern
    Does the traversal trace a figure-8 pattern, crossing at the
    origin repeatedly? DISCOVERY test.

TEST 4: HolographicMirror
    Is TetB's state a "mirror" encoding of TetA's state, like the
    two loops of infinity reflecting each other? DISCOVERY test.

TEST 5: MitosisSymmetryBreaking
    In biological mitosis, small asymmetries matter. Is TetA/TetB
    perfectly symmetric, or is there a detectable asymmetry? DISCOVERY test.

These tests may FAIL or reveal unexpected patterns. That's the point.
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict

from gravity_field_model.framework import *
from gravity_field_model.common import (
    TET_A, TET_B,
    FACES, VERTICES,
    COMPLEMENTARY_PAIRS,
    traverse_pi_base8,
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def get_vertex_coordinates(vertex: int) -> np.ndarray:
    """Get 3D coordinates of a vertex."""
    coords = VERTICES[vertex]['coords']
    return np.array(coords, dtype=float)


def compute_vector_sum_at_visits(history: List[int]) -> Dict:
    """
    Compute the cumulative vector sum as vertices are visited.
    
    Each visit "adds" the vertex's position vector to the sum.
    At the Field Origin, this sum should be near zero.
    """
    cumsum = np.zeros(3)
    history_sums = []
    
    for v in history:
        coords = get_vertex_coordinates(v)
        cumsum = cumsum + coords
        history_sums.append(cumsum.copy())
    
    return {
        'final_sum': cumsum,
        'magnitude': np.linalg.norm(cumsum),
        'history': history_sums,
    }


def compute_chamber_vector_sums(history: List[int]) -> Dict:
    """
    Compute separate vector sums for TetA and TetB visits.
    
    If they're symmetric, their sums should be equal and opposite.
    """
    teta_sum = np.zeros(3)
    tetb_sum = np.zeros(3)
    teta_count = 0
    tetb_count = 0
    
    for v in history:
        coords = get_vertex_coordinates(v)
        if v in TET_A:
            teta_sum += coords
            teta_count += 1
        else:
            tetb_sum += coords
            tetb_count += 1
    
    # Normalize by counts
    teta_mean = teta_sum / teta_count if teta_count > 0 else teta_sum
    tetb_mean = tetb_sum / tetb_count if tetb_count > 0 else tetb_sum
    
    # Check if they're opposite
    sum_of_means = teta_mean + tetb_mean
    
    return {
        'teta_sum': teta_sum,
        'tetb_sum': tetb_sum,
        'teta_mean': teta_mean,
        'tetb_mean': tetb_mean,
        'sum_of_means': sum_of_means,
        'are_opposite': np.linalg.norm(sum_of_means) < 0.01,
        'teta_count': teta_count,
        'tetb_count': tetb_count,
    }


def count_origin_crossings(history: List[int]) -> Dict:
    """
    Count how many times the traversal "crosses" the origin.
    
    A crossing is defined as a transition between TetA and TetB.
    In a lemniscate, you cross the center every time you switch loops.
    """
    crossings = 0
    teta_to_tetb = 0
    tetb_to_teta = 0
    
    for i in range(len(history) - 1):
        v_curr = history[i]
        v_next = history[i + 1]
        
        curr_in_teta = v_curr in TET_A
        next_in_teta = v_next in TET_A
        
        if curr_in_teta != next_in_teta:
            crossings += 1
            if curr_in_teta:
                teta_to_tetb += 1
            else:
                tetb_to_teta += 1
    
    total_transitions = len(history) - 1
    
    return {
        'total_crossings': crossings,
        'teta_to_tetb': teta_to_tetb,
        'tetb_to_teta': tetb_to_teta,
        'crossing_rate': crossings / total_transitions if total_transitions > 0 else 0,
        'flow_asymmetry': abs(teta_to_tetb - tetb_to_teta) / crossings if crossings > 0 else 0,
    }


def analyze_loop_lengths(history: List[int]) -> Dict:
    """
    Analyze the "loop lengths" - how long does the traversal stay in each chamber?
    
    In a lemniscate traversal, you trace one loop, cross, trace the other, cross, ...
    Loop lengths should be similar if the two halves are symmetric.
    """
    loop_lengths = {'TetA': [], 'TetB': []}
    current_chamber = 'TetA' if history[0] in TET_A else 'TetB'
    current_length = 1
    
    for i in range(1, len(history)):
        v = history[i]
        chamber = 'TetA' if v in TET_A else 'TetB'
        
        if chamber == current_chamber:
            current_length += 1
        else:
            loop_lengths[current_chamber].append(current_length)
            current_chamber = chamber
            current_length = 1
    
    # Don't forget the last loop
    loop_lengths[current_chamber].append(current_length)
    
    # Statistics
    teta_loops = loop_lengths['TetA']
    tetb_loops = loop_lengths['TetB']
    
    return {
        'teta_mean_loop': np.mean(teta_loops) if teta_loops else 0,
        'tetb_mean_loop': np.mean(tetb_loops) if tetb_loops else 0,
        'teta_std_loop': np.std(teta_loops) if teta_loops else 0,
        'tetb_std_loop': np.std(tetb_loops) if tetb_loops else 0,
        'loop_symmetry': 1 - abs(np.mean(teta_loops) - np.mean(tetb_loops)) / max(np.mean(teta_loops), np.mean(tetb_loops)) if teta_loops and tetb_loops else 0,
        'n_teta_loops': len(teta_loops),
        'n_tetb_loops': len(tetb_loops),
    }


def compute_mirror_correlation(history: List[int]) -> Dict:
    """
    Test if TetB's activation pattern "mirrors" TetA's.
    
    In a true lemniscate/mitosis structure, the two halves should
    be reflections of each other through the origin.
    """
    # Map TetA vertices to their complements in TetB
    # Complements: (0,7), (1,6), (2,5), (3,4)
    complement_map = {0: 7, 7: 0, 1: 6, 6: 1, 2: 5, 5: 2, 3: 4, 4: 3}
    
    # Track when each vertex and its complement are visited
    visit_times = {v: [] for v in range(8)}
    for t, v in enumerate(history):
        visit_times[v].append(t)
    
    # Compute correlation between complementary pairs
    correlations = []
    for v_a, v_b in COMPLEMENTARY_PAIRS:
        times_a = visit_times[v_a]
        times_b = visit_times[v_b]
        
        if len(times_a) > 1 and len(times_b) > 1:
            # Compute mean inter-visit interval
            intervals_a = np.diff(times_a)
            intervals_b = np.diff(times_b)
            
            # Compare distributions
            mean_a = np.mean(intervals_a)
            mean_b = np.mean(intervals_b)
            
            # Similarity measure
            similarity = 1 - abs(mean_a - mean_b) / max(mean_a, mean_b)
            correlations.append(similarity)
    
    return {
        'mean_mirror_correlation': np.mean(correlations) if correlations else 0,
        'min_mirror_correlation': min(correlations) if correlations else 0,
        'pair_correlations': correlations,
    }


def detect_asymmetry(history: List[int]) -> Dict:
    """
    Look for any asymmetry between TetA and TetB.
    
    In perfect mitosis, the daughters are identical.
    Any detectable asymmetry could be significant.
    """
    # Count visits
    teta_visits = sum(1 for v in history if v in TET_A)
    tetb_visits = sum(1 for v in history if v in TET_B)
    total = len(history)
    
    teta_fraction = teta_visits / total
    tetb_fraction = tetb_visits / total
    
    # Visit asymmetry
    visit_asymmetry = abs(teta_fraction - tetb_fraction)
    
    # First visit asymmetry
    first_teta = next((i for i, v in enumerate(history) if v in TET_A), None)
    first_tetb = next((i for i, v in enumerate(history) if v in TET_B), None)
    first_visit_diff = abs(first_teta - first_tetb) if first_teta is not None and first_tetb is not None else 0
    
    # Vertex uniformity within each chamber
    teta_vertex_counts = Counter(v for v in history if v in TET_A)
    tetb_vertex_counts = Counter(v for v in history if v in TET_B)
    
    teta_cv = np.std(list(teta_vertex_counts.values())) / np.mean(list(teta_vertex_counts.values())) if teta_vertex_counts else 0
    tetb_cv = np.std(list(tetb_vertex_counts.values())) / np.mean(list(tetb_vertex_counts.values())) if tetb_vertex_counts else 0
    
    return {
        'teta_fraction': teta_fraction,
        'tetb_fraction': tetb_fraction,
        'visit_asymmetry': visit_asymmetry,
        'first_visit_difference': first_visit_diff,
        'teta_internal_cv': teta_cv,
        'tetb_internal_cv': tetb_cv,
        'is_symmetric': visit_asymmetry < 0.02,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class ZeroNetFieldAtOrigin(Test):
    """
    PROBING: Does the net field sum to zero at the origin?
    """
    name = "Zero Net Field at Origin"
    question = (
        "If the Field Origin is the crossing point of a lemniscate, "
        "all directional quantities should sum to zero there. The two "
        "loops contribute equally but oppositely. Does the mean position "
        "vector from TetA visits equal and opposite the mean from TetB?"
    )
    reference = "Lemniscate topology, vector field theory"
    level = Critical
    tolerance = 0.15

    commentary = (
        "DISCOVERY: Testing whether the Field Origin is truly a 'zero point' "
        "where opposing contributions from TetA and TetB cancel. This would "
        "confirm the lemniscate/infinity sign topology where the crossing "
        "point has zero net field because both loops contribute equally "
        "but in opposite directions."
    )

    audit_score = 90
    audit_notes = (
        "PROBING TEST: This may reveal unexpected structure. "
        "We're not fitting; we're discovering."
    )

    def derivation(self):
        return (
            Derivation()
            .step("LEMNISCATE TOPOLOGY:")
            .step("The infinity sign (lemniscate) has a crossing point")
            .step("where the two loops meet.")
            .step("At this point, contributions from both loops should cancel:")
            .equation("mean(TetA vectors) + mean(TetB vectors) = 0")
            .step("TEST: Compute mean position vectors for each chamber.")
            .step("If they're equal and opposite, the origin has zero net field.")
            .conclude("Zero sum proves lemniscate crossing point topology.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        result = compute_chamber_vector_sums(history)
        
        # Magnitude of the sum of means (should be near zero)
        sum_magnitude = np.linalg.norm(result['sum_of_means'])
        
        # Individual magnitudes
        teta_magnitude = np.linalg.norm(result['teta_mean'])
        tetb_magnitude = np.linalg.norm(result['tetb_mean'])
        
        # Are they opposite?
        are_opposite = 1.0 if result['are_opposite'] else 0.0
        
        return (
            Model()
            .add("Sum of means magnitude", sum_magnitude)
            .add("TetA mean magnitude", teta_magnitude)
            .add("TetB mean magnitude", tetb_magnitude)
            .add("TetA visit fraction", result['teta_count'] / (result['teta_count'] + result['tetb_count']))
        )

    def observations(self):
        # PROBING: What do we expect?
        # If lemniscate topology, sum should be NEAR zero
        # Allow for statistical fluctuation
        return (
            Observed()
            .add("Sum of means magnitude", 0.03)  # Near zero (allow fluctuation)
            .add("TetA mean magnitude", 0.02)     # Small but nonzero
            .add("TetB mean magnitude", 0.02)     # Similar to TetA
            .add("TetA visit fraction", 0.5)      # Equal visits
        )


class ExactHalfPartition(Test):
    """
    PROBING: Is the partition exactly 50/50?
    """
    name = "Exact Half Partition (Mitosis Test)"
    question = (
        "In mitosis, a cell divides into two equal halves. If the gravity "
        "field is in 'mitosis' with subspace, is the partition exactly 50%? "
        "Or is there a detectable bias toward one half?"
    )
    reference = "Mitosis symmetry, partition theory"
    level = Critical
    tolerance = 0.02

    commentary = (
        "DISCOVERY: Testing the 'mitosis' metaphor. Perfect mitosis gives "
        "50/50, but biological mitosis often has small asymmetries that "
        "determine cell fate. Is GFM perfectly symmetric, or is there "
        "a detectable 'chirality' to the field?"
    )

    audit_score = 90
    audit_notes = "PROBING TEST: Looking for asymmetry."

    def derivation(self):
        return (
            Derivation()
            .step("MITOSIS SYMMETRY:")
            .step("In cell division, chromosomes are distributed equally.")
            .step("Perfect mitosis: 50% to each daughter cell.")
            .step("Asymmetric division: slight bias toward one side.")
            .step("TEST: Measure TetA vs TetB visit fractions.")
            .equation("Perfect mitosis: TetA fraction = TetB fraction = 0.5")
            .step("Any deviation from 0.5 indicates asymmetry.")
            .conclude("Testing if GFM has perfect or asymmetric 'division'.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        result = detect_asymmetry(history)
        
        return (
            Model()
            .add("TetA fraction", result['teta_fraction'])
            .add("TetB fraction", result['tetb_fraction'])
            .add("Visit asymmetry", result['visit_asymmetry'])
            .add("Is symmetric (< 2%)", 1.0 if result['is_symmetric'] else 0.0)
        )

    def observations(self):
        # PROBING: Is it NEAR 50/50?
        # Allow for statistical fluctuation (~1%)
        return (
            Observed()
            .add("TetA fraction", 0.495)          # Near 50%
            .add("TetB fraction", 0.505)          # Near 50%
            .add("Visit asymmetry", 0.01)         # ~1% asymmetry (statistical)
            .add("Is symmetric (< 2%)", 1.0)
        )


class LemniscateCirculationPattern(Test):
    """
    PROBING: Does the traversal trace a figure-8 pattern?
    """
    name = "Lemniscate Circulation Pattern"
    question = (
        "In a lemniscate (figure-8), you trace one loop, cross the center, "
        "trace the other loop, cross again. Does the pi-base-8 traversal "
        "exhibit this alternating pattern? How often does it cross the origin?"
    )
    reference = "Lemniscate curve, circulation topology"
    level = Critical
    tolerance = 0.1

    commentary = (
        "DISCOVERY: Testing if the vortex follows a figure-8 circulation. "
        "We already found 50% crossing rate, but here we test the PATTERN "
        "of crossings. Regular alternation would confirm lemniscate flow."
    )

    audit_score = 90
    audit_notes = "PROBING TEST: Analyzing circulation pattern."

    def derivation(self):
        return (
            Derivation()
            .step("LEMNISCATE CIRCULATION:")
            .step("A figure-8 traversal alternates between loops.")
            .step("Cross, trace loop A, cross, trace loop B, repeat")
            .step("This creates a specific pattern:")
            .step("  - Regular crossing frequency")
            .step("  - Similar loop lengths on each side")
            .step("  - Symmetric flow (A to B rate = B to A rate)")
            .step("TEST: Analyze crossing rate and flow symmetry.")
            .conclude("Regular alternation confirms lemniscate topology.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        crossings = count_origin_crossings(history)
        loops = analyze_loop_lengths(history)
        
        return (
            Model()
            .add("Crossing rate", crossings['crossing_rate'])
            .add("Flow asymmetry (A->B vs B->A)", crossings['flow_asymmetry'])
            .add("TetA mean loop length", loops['teta_mean_loop'])
            .add("TetB mean loop length", loops['tetb_mean_loop'])
            .add("Loop length symmetry", loops['loop_symmetry'])
        )

    def observations(self):
        # PROBING: What does lemniscate predict?
        # ~50% crossing rate (every other step crosses)
        # Near-zero flow asymmetry (equal A->B and B->A)
        # Similar loop lengths
        return (
            Observed()
            .add("Crossing rate", 0.5)
            .add("Flow asymmetry (A->B vs B->A)", 0.02)  # Near zero
            .add("TetA mean loop length", 2.0)           # ~2 steps per loop
            .add("TetB mean loop length", 2.0)           # Similar
            .add("Loop length symmetry", 0.95)           # High symmetry
        )


class HolographicMirror(Test):
    """
    PROBING: Does TetB mirror TetA through complementary pairs?
    """
    name = "Holographic Mirror (Complementary Correlation)"
    question = (
        "Each TetA vertex has a 'complement' in TetB (XOR with 7). "
        "If the two halves of the lemniscate mirror each other, "
        "complementary vertices should have correlated visit patterns. "
        "Is TetB a 'holographic' reflection of TetA?"
    )
    reference = "Holographic principle, complementary pairs"
    level = Critical
    tolerance = 0.2

    commentary = (
        "DISCOVERY: The holographic principle suggests boundary information "
        "encodes bulk physics. If TetB is the 'boundary' to TetA's 'bulk', "
        "their states should be correlated through complementary vertices. "
        "High correlation would support holographic interpretation."
    )

    audit_score = 90
    audit_notes = "PROBING TEST: Testing holographic mirror hypothesis."

    def derivation(self):
        return (
            Derivation()
            .step("HOLOGRAPHIC MIRROR:")
            .step("Complementary pairs: (0,7), (1,6), (2,5), (3,4)")
            .step("Each pair has one vertex in TetA, one in TetB.")
            .step("If TetB mirrors TetA, complements should have")
            .step("similar visit statistics (inter-visit intervals).")
            .step("TEST: Compare visit patterns of complementary pairs.")
            .step("High correlation means TetB reflects TetA state.")
            .conclude("Mirror correlation tests holographic principle.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        result = compute_mirror_correlation(history)
        
        return (
            Model()
            .add("Mean mirror correlation", result['mean_mirror_correlation'])
            .add("Min mirror correlation", result['min_mirror_correlation'])
        )

    def observations(self):
        # PROBING: If holographic, high correlation expected
        return (
            Observed()
            .add("Mean mirror correlation", 1.0)  # Perfect mirror
            .add("Min mirror correlation", 0.8)   # All pairs correlated
        )


class MitosisAsymmetryProbe(Test):
    """
    PROBING: Is there any detectable asymmetry in the 'mitosis'?
    """
    name = "Mitosis Asymmetry Probe"
    question = (
        "In biological mitosis, small asymmetries determine cell fate "
        "(stem cell vs differentiated). Is there ANY detectable difference "
        "between TetA and TetB beyond random fluctuation? This could reveal "
        "a fundamental 'chirality' or preferred direction in the field."
    )
    reference = "Asymmetric cell division, chirality"
    level = Exploratory  # Exploratory because we're looking for subtle effects
    tolerance = 0.5  # Wide tolerance - we're probing

    commentary = (
        "DISCOVERY: Looking for the unexpected. If we find asymmetry, "
        "it could explain why we experience TetA (our space) differently "
        "from TetB (subspace). Perfect symmetry means they're truly equal; "
        "asymmetry means one is 'special'."
    )

    audit_score = 85
    audit_notes = "PROBING TEST: Looking for subtle asymmetry."

    def derivation(self):
        return (
            Derivation()
            .step("ASYMMETRY PROBE:")
            .step("We expect TetA = TetB (symmetric mitosis).")
            .step("But look for ANY difference:")
            .step("  - First visit timing")
            .step("  - Internal uniformity (CV within chamber)")
            .step("  - Total visit counts")
            .step("Any consistent bias could indicate fundamental chirality.")
            .conclude("Probing for unexpected asymmetry.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        result = detect_asymmetry(history)
        
        # Check which chamber was visited first
        first_is_teta = 1.0 if history[0] in TET_A else 0.0
        
        # Compare internal CV
        cv_ratio = result['teta_internal_cv'] / result['tetb_internal_cv'] if result['tetb_internal_cv'] > 0 else 1.0
        
        return (
            Model()
            .add("First visit is TetA", first_is_teta)
            .add("TetA internal CV", result['teta_internal_cv'])
            .add("TetB internal CV", result['tetb_internal_cv'])
            .add("CV ratio (TetA/TetB)", cv_ratio)
            .add("Visit asymmetry", result['visit_asymmetry'])
        )

    def observations(self):
        # PROBING: We don't know what to expect
        # Use neutral values - deviations are discoveries
        return (
            Observed()
            .add("First visit is TetA", 0.5)  # 50% chance
            .add("CV ratio (TetA/TetB)", 1.0)  # Equal uniformity
            .add("Visit asymmetry", 0.0)  # Perfect symmetry
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ZeroNetFieldAtOrigin,
    ExactHalfPartition,
    LemniscateCirculationPattern,
    HolographicMirror,
    MitosisAsymmetryProbe,
]


def run_all():
    """Run all lemniscate topology probing tests."""
    summary = (
        "LEMNISCATE TOPOLOGY PROBING TESTS\n\n"
        "These tests PROBE the hypothesis that the Merkaba has\n"
        "infinity-sign (lemniscate) topology with Field Origin\n"
        "at the crossing point.\n\n"
        "User insight: 'The gravity field is in mitosis with a\n"
        "subspace gravity field. The net field is only HALF in\n"
        "our (3+1) space. The origin is like an infinity sign.'\n\n"
        "We test:\n"
        "  1. Zero net field at origin (crossing point)\n"
        "  2. Exact 50/50 partition (mitosis symmetry)\n"
        "  3. Figure-8 circulation pattern\n"
        "  4. Holographic mirror (complementary correlation)\n"
        "  5. Any detectable asymmetry\n\n"
        "These tests may FAIL or reveal unexpected structure.\n"
        "That's the point of PROBING."
    )
    return run_tests("Lemniscate Topology Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
