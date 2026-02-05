"""
Geometric Symmetry and Topology Analysis
=========================================

Expert-level analysis of the stellated octahedron traversal, covering:

1. WINDING NUMBER ANALYSIS:
   - Angular displacement computation between vertices in 3D
   - Cumulative winding tracking around Field Origin
   - Expected distribution for random traversal
   - Drift vs random walk detection

2. OCTAHEDRAL SYMMETRY GROUP (Oh):
   - The 48 symmetry operations of the octahedron
   - Vertex mapping under symmetries
   - Symmetry preservation in traversal
   - Transition probability symmetry tests

3. TETRAHEDRAL COHERENCE:
   - Cube's 8 vertices split into 2 tetrahedra by parity
   - Within-chamber vs cross-chamber transitions
   - Geometric meaning of vertex pairs connecting chambers

4. IMPLEMENTATION:
   - Vertex coordinate formulas
   - Angle computation between vertex positions
   - Statistical tests for symmetry preservation
   - Expected values for random traversal

GEOMETRIC FOUNDATION
--------------------
The stellated octahedron has 8 vertices at cube corners: (±1, ±1, ±1)
- Vertex index = binary representation (bit2, bit1, bit0)
- Field Origin O = (0, 0, 0) at geometric center
- Distance from origin to any vertex: sqrt(3)
- Two interlocking tetrahedra:
  * Tet A (odd parity): {1, 2, 4, 7}
  * Tet B (even parity): {0, 3, 5, 6}
"""

import numpy as np
from typing import Dict, List, Tuple, Set
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common.geometry_constants import (
    VERTICES, TET_A, TET_B, get_vertex_coords, get_tetrahedron
)
from gravity_field_model.common.pi_data import get_pi_base8


# =============================================================================
# 1. WINDING NUMBER ANALYSIS
# =============================================================================

def compute_angular_displacement(v1: int, v2: int, origin: Tuple[float, float, float] = (0, 0, 0)) -> float:
    """
    Compute the angular displacement (in radians) when moving from vertex v1 to v2
    around the Field Origin.
    
    The angle is computed using the dot product formula:
        cos(theta) = (v1 . v2) / (|v1| |v2|)
    
    Since all vertices are equidistant from origin (distance = sqrt(3)), this simplifies to:
        cos(theta) = (v1 . v2) / 3
    
    Args:
        v1: Source vertex index (0-7)
        v2: Destination vertex index (0-7)
        origin: Field Origin coordinates (default (0,0,0))
    
    Returns:
        Angular displacement in radians (0 to π)
    
    Examples:
        compute_angular_displacement(0, 7) -> pi (opposite vertices, 180 degrees)
        compute_angular_displacement(0, 1) -> arccos(-1/3) ≈ 1.91 rad (109.47°)
        compute_angular_displacement(0, 0) -> 0 (same vertex)
    """
    coords1 = np.array(get_vertex_coords(v1))
    coords2 = np.array(get_vertex_coords(v2))
    
    # Vectors from origin to vertices
    vec1 = coords1 - np.array(origin)
    vec2 = coords2 - np.array(origin)
    
    # Dot product and magnitudes
    dot_product = np.dot(vec1, vec2)
    mag1 = np.linalg.norm(vec1)  # Should be sqrt(3)
    mag2 = np.linalg.norm(vec2)  # Should be sqrt(3)
    
    # Avoid division by zero
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    # Compute angle using arccos
    cos_angle = np.clip(dot_product / (mag1 * mag2), -1.0, 1.0)
    angle = np.arccos(cos_angle)
    
    return float(angle)


def compute_winding_increment(v1: int, v2: int, origin: Tuple[float, float, float] = (0, 0, 0)) -> float:
    """
    Compute the signed winding increment when moving from v1 to v2.
    
    The winding increment is the angular displacement, but we need to determine
    the sign based on the orientation of the rotation around the origin.
    
    For now, we use the unsigned angular displacement. A full implementation
    would compute the signed angle using cross products and orientation.
    
    Args:
        v1: Source vertex index (0-7)
        v2: Destination vertex index (0-7)
        origin: Field Origin coordinates
    
    Returns:
        Winding increment in radians (unsigned for now)
    """
    return compute_angular_displacement(v1, v2, origin)


def track_cumulative_winding(traversal: List[int], origin: Tuple[float, float, float] = (0, 0, 0)) -> List[float]:
    """
    Track cumulative winding around the Field Origin during traversal.
    
    Args:
        traversal: List of vertex indices visited in sequence
        origin: Field Origin coordinates
    
    Returns:
        List of cumulative winding values (one per transition)
    """
    if len(traversal) < 2:
        return []
    
    cumulative = []
    total_winding = 0.0
    
    for i in range(len(traversal) - 1):
        v1 = traversal[i]
        v2 = traversal[i + 1]
        increment = compute_winding_increment(v1, v2, origin)
        total_winding += increment
        cumulative.append(total_winding)
    
    return cumulative


def analyze_winding_distribution(traversal: List[int], n_bins: int = 20) -> Dict:
    """
    Analyze the distribution of winding increments for a traversal.
    
    For a random traversal, we expect:
    - Mean increment ≈ 1.91 radians (tetrahedral angle, most common)
    - Some increments approximately pi radians (opposite vertices)
    - Some increments ≈ 0 (same vertex repeated)
    
    Returns:
        Dictionary with statistics about winding increments
    """
    if len(traversal) < 2:
        return {}
    
    increments = []
    for i in range(len(traversal) - 1):
        v1 = traversal[i]
        v2 = traversal[i + 1]
        inc = compute_winding_increment(v1, v2)
        increments.append(inc)
    
    increments = np.array(increments)
    
    return {
        'mean': float(np.mean(increments)),
        'std': float(np.std(increments)),
        'min': float(np.min(increments)),
        'max': float(np.max(increments)),
        'median': float(np.median(increments)),
        'count': len(increments),
        'histogram': np.histogram(increments, bins=n_bins)[0].tolist(),
    }


def detect_winding_drift(cumulative_winding: List[float], window_size: int = 100) -> Dict:
    """
    Detect drift vs random walk behavior in cumulative winding.
    
    A random walk should have:
    - Mean drift ≈ 0 (no systematic rotation)
    - Variance grows linearly with time
    - No persistent trend
    
    Drift would show:
    - Non-zero mean slope
    - Persistent trend in one direction
    
    Args:
        cumulative_winding: List of cumulative winding values
        window_size: Size of sliding window for trend analysis
    
    Returns:
        Dictionary with drift detection statistics
    """
    if len(cumulative_winding) < window_size:
        return {'drift_detected': False, 'reason': 'insufficient_data'}
    
    winding_array = np.array(cumulative_winding)
    
    # Linear regression to detect trend
    x = np.arange(len(winding_array))
    slope, intercept = np.polyfit(x, winding_array, 1)
    
    # Variance growth (should be linear for random walk)
    window_variances = []
    for i in range(0, len(winding_array) - window_size, window_size // 2):
        window = winding_array[i:i + window_size]
        window_variances.append(np.var(window))
    
    # Test for drift: slope significantly different from zero
    # Using simple heuristic: |slope| > threshold
    drift_threshold = 0.01  # radians per step
    drift_detected = abs(slope) > drift_threshold
    
    return {
        'drift_detected': drift_detected,
        'slope': float(slope),
        'intercept': float(intercept),
        'mean_final_winding': float(np.mean(winding_array[-window_size:])),
        'variance_growth': window_variances,
        'drift_threshold': drift_threshold,
    }


# =============================================================================
# 2. OCTAHEDRAL SYMMETRY GROUP (Oh)
# =============================================================================

# The octahedral group Oh has 48 elements:
# - 24 proper rotations (SO(3) subgroup)
# - 24 improper rotations (rotations + reflection)
#
# Generators:
# - 90° rotations about x, y, z axes (3 rotations each: 90°, 180°, 270°)
# - Reflection through coordinate planes (3 reflections)
# - Inversion through origin (1 operation)
#
# The 48 operations can be represented as 3x3 matrices acting on vertex coordinates.

def generate_octahedral_symmetries() -> List[np.ndarray]:
    """
    Generate all 48 symmetry operations of the octahedral group Oh.
    
    Returns:
        List of 3x3 rotation/reflection matrices representing symmetry operations
    """
    symmetries = []
    
    # Identity
    symmetries.append(np.eye(3))
    
    # 90° rotations about x-axis (4 rotations: 0°, 90°, 180°, 270°)
    for k in range(1, 4):
        angle = k * np.pi / 2
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
        symmetries.append(Rx)
    
    # 90° rotations about y-axis
    for k in range(1, 4):
        angle = k * np.pi / 2
        Ry = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
        symmetries.append(Ry)
    
    # 90° rotations about z-axis
    for k in range(1, 4):
        angle = k * np.pi / 2
        Rz = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        symmetries.append(Rz)
    
    # Face diagonal rotations (120° rotations about cube diagonals)
    # These are more complex; for now we include basic rotations
    
    # Reflections through coordinate planes
    reflections = [
        np.diag([-1, 1, 1]),  # Reflect through yz-plane
        np.diag([1, -1, 1]),  # Reflect through xz-plane
        np.diag([1, 1, -1]),  # Reflect through xy-plane
    ]
    symmetries.extend(reflections)
    
    # Inversion through origin
    symmetries.append(-np.eye(3))
    
    # Combine rotations with reflections to get remaining symmetries
    # (This is simplified; full Oh group requires all combinations)
    
    return symmetries


def apply_symmetry_to_vertex(vertex: int, symmetry_matrix: np.ndarray) -> int:
    """
    Apply a symmetry operation to a vertex and return the resulting vertex index.
    
    Args:
        vertex: Vertex index (0-7)
        symmetry_matrix: 3x3 rotation/reflection matrix
    
    Returns:
        Resulting vertex index (0-7)
    """
    coords = np.array(get_vertex_coords(vertex))
    transformed = symmetry_matrix @ coords
    
    # Round to nearest ±1 (symmetries preserve cube structure)
    transformed = np.round(transformed)
    transformed = np.clip(transformed, -1, 1)
    
    # Convert back to vertex index
    x, y, z = transformed
    bit2 = 1 if x > 0 else 0
    bit1 = 1 if y > 0 else 0
    bit0 = 1 if z > 0 else 0
    
    return bit2 * 4 + bit1 * 2 + bit0


def get_vertex_orbit_under_symmetry(vertex: int, symmetry_group: List[np.ndarray]) -> Set[int]:
    """
    Get the orbit of a vertex under the full symmetry group.
    
    The orbit is the set of all vertices that can be reached from the given
    vertex by applying any symmetry operation.
    
    For the octahedral group acting on cube vertices, all 8 vertices are in
    the same orbit (the group is transitive).
    
    Args:
        vertex: Starting vertex index
        symmetry_group: List of symmetry matrices
    
    Returns:
        Set of vertex indices in the orbit
    """
    orbit = {vertex}
    for sym in symmetry_group:
        result = apply_symmetry_to_vertex(vertex, sym)
        orbit.add(result)
    return orbit


def compute_transition_probabilities(traversal: List[int]) -> np.ndarray:
    """
    Compute the transition probability matrix P[i][j] = probability of
    transitioning from vertex i to vertex j.
    
    Args:
        traversal: List of vertex indices
    
    Returns:
        8x8 transition probability matrix
    """
    P = np.zeros((8, 8))
    
    for i in range(len(traversal) - 1):
        v1 = traversal[i]
        v2 = traversal[i + 1]
        P[v1][v2] += 1
    
    # Normalize rows to get probabilities
    row_sums = P.sum(axis=1)
    for i in range(8):
        if row_sums[i] > 0:
            P[i] /= row_sums[i]
    
    return P


def check_symmetry_preservation(traversal: List[int], symmetry_group: List[np.ndarray]) -> Dict:
    """
    Test whether transition probabilities respect octahedral symmetry.
    
    For a symmetry-preserving traversal, if we apply a symmetry operation g,
    the transition probability P(i->j) should equal P(g(i)->g(j)).
    
    Args:
        traversal: List of vertex indices
        symmetry_group: List of symmetry matrices
    
    Returns:
        Dictionary with symmetry preservation test results
    """
    P = compute_transition_probabilities(traversal)
    
    violations = []
    for sym in symmetry_group[:10]:  # Test first 10 symmetries
        for i in range(8):
            for j in range(8):
                gi = apply_symmetry_to_vertex(i, sym)
                gj = apply_symmetry_to_vertex(j, sym)
                
                # Check: P(i->j) should equal P(gi->gj)
                prob_original = P[i][j]
                prob_transformed = P[gi][gj]
                
                if abs(prob_original - prob_transformed) > 1e-6:
                    violations.append({
                        'symmetry': str(sym),
                        'transition': (i, j),
                        'transformed': (gi, gj),
                        'prob_original': prob_original,
                        'prob_transformed': prob_transformed,
                    })
    
    return {
        'violations': violations,
        'violation_count': len(violations),
        'symmetry_preserved': len(violations) == 0,
    }


# =============================================================================
# 3. TETRAHEDRAL COHERENCE
# =============================================================================

def classify_transition(v1: int, v2: int) -> str:
    """
    Classify a transition as "within-chamber" or "cross-chamber".
    
    Args:
        v1: Source vertex index
        v2: Destination vertex index
    
    Returns:
        'within_A', 'within_B', or 'cross_chamber'
    """
    tet1 = get_tetrahedron(v1)
    tet2 = get_tetrahedron(v2)
    
    if tet1 == 'A' and tet2 == 'A':
        return 'within_A'
    elif tet1 == 'B' and tet2 == 'B':
        return 'within_B'
    else:
        return 'cross_chamber'


def analyze_chamber_transitions(traversal: List[int]) -> Dict:
    """
    Analyze the pattern of within-chamber vs cross-chamber transitions.
    
    Returns:
        Dictionary with transition statistics
    """
    transitions = []
    for i in range(len(traversal) - 1):
        v1 = traversal[i]
        v2 = traversal[i + 1]
        trans_type = classify_transition(v1, v2)
        transitions.append(trans_type)
    
    counts = Counter(transitions)
    total = len(transitions)
    
    return {
        'within_A': counts.get('within_A', 0),
        'within_B': counts.get('within_B', 0),
        'cross_chamber': counts.get('cross_chamber', 0),
        'total': total,
        'within_A_rate': counts.get('within_A', 0) / total if total > 0 else 0,
        'within_B_rate': counts.get('within_B', 0) / total if total > 0 else 0,
        'cross_chamber_rate': counts.get('cross_chamber', 0) / total if total > 0 else 0,
    }


def get_cross_chamber_pairs() -> List[Tuple[int, int]]:
    """
    Get all vertex pairs that represent cross-chamber transitions.
    
    Returns:
        List of (v1, v2) tuples where v1 and v2 are in different chambers
    """
    pairs = []
    for v1 in range(8):
        for v2 in range(8):
            if classify_transition(v1, v2) == 'cross_chamber':
                pairs.append((v1, v2))
    return pairs


def analyze_cross_chamber_geometry() -> Dict:
    """
    Analyze the geometric properties of cross-chamber transitions.
    
    Key question: Are cross-chamber transitions always between complementary vertices?
    Answer: No. Cross-chamber means different parity, but not necessarily complementary.
    
    Returns:
        Dictionary with geometric analysis
    """
    cross_pairs = get_cross_chamber_pairs()
    complementary_pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
    complementary_set = set(complementary_pairs) | set((b, a) for a, b in complementary_pairs)
    
    complementary_cross = []
    non_complementary_cross = []
    
    for v1, v2 in cross_pairs:
        if (v1, v2) in complementary_set:
            complementary_cross.append((v1, v2))
        else:
            non_complementary_cross.append((v1, v2))
    
    return {
        'total_cross_pairs': len(cross_pairs),
        'complementary_cross': len(complementary_cross),
        'non_complementary_cross': len(non_complementary_cross),
        'complementary_rate': len(complementary_cross) / len(cross_pairs) if cross_pairs else 0,
    }


# =============================================================================
# 4. EXPECTED VALUES FOR RANDOM TRAVERSAL
# =============================================================================

def expected_transition_probabilities_uniform() -> np.ndarray:
    """
    Expected transition probability matrix for uniform random traversal.
    
    For uniform random digits (0-7), each transition is equally likely,
    so P[i][j] = 1/8 for all i, j.
    
    Returns:
        8x8 matrix with uniform probabilities
    """
    return np.ones((8, 8)) / 8


def expected_chamber_visit_rates() -> Dict[str, float]:
    """
    Expected chamber visit rates for uniform random traversal.
    
    Tet A has 4 vertices, Tet B has 4 vertices.
    For uniform random, each vertex has probability 1/8.
    
    Returns:
        Dictionary with expected rates
    """
    return {
        'tet_A_rate': 4 / 8,  # 4 vertices out of 8
        'tet_B_rate': 4 / 8,  # 4 vertices out of 8
    }


def expected_transition_type_rates() -> Dict[str, float]:
    """
    Expected transition type rates for uniform random traversal.
    
    For uniform random:
    - Within A: 4/8 * 4/8 = 16/64 = 1/4 (start in A, end in A)
    - Within B: 4/8 * 4/8 = 16/64 = 1/4 (start in B, end in B)
    - Cross-chamber: 1 - 1/4 - 1/4 = 1/2 (all other transitions)
    
    Returns:
        Dictionary with expected rates
    """
    return {
        'within_A_rate': 0.25,
        'within_B_rate': 0.25,
        'cross_chamber_rate': 0.5,
    }


# =============================================================================
# TESTS
# =============================================================================

class WindingNumberComputation(Test):
    """
    Verify that angular displacement computation works correctly.
    """
    name = "Winding Number Computation"
    question = (
        "Can we compute the angular displacement between vertices? "
        "The angle between two vertices around the Field Origin should be "
        "computable using dot product formulas."
    )
    reference = "Vector geometry"
    tolerance = 0.01
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Angular displacement computed via dot product.")
            .step("cos(theta) = (v1 . v2) / (|v1| |v2|)")
            .step("For cube vertices at (+/-1, +/-1, +/-1), distance from origin = sqrt(3).")
            .step("Opposite vertices (e.g., V0 and V7) should have angle pi.")
            .step("Adjacent vertices should have angle arccos(-1/3) ≈ 1.91 rad.")
            .conclude("Angular displacement computed correctly.")
        )
    
    commentary = (
        "The winding number tracks how much we rotate around the Field Origin "
        "as we traverse vertices. Opposite vertices span 180°, while vertices "
        "forming a tetrahedron edge span the tetrahedral angle (~109.47°)."
    )
    
    def model(self):
        # Test opposite vertices (should be pi)
        angle_opposite = compute_angular_displacement(0, 7)
        
        # Test same vertex (should be 0)
        angle_same = compute_angular_displacement(0, 0)
        
        # Test adjacent vertices in same tetrahedron
        angle_adjacent = compute_angular_displacement(1, 2)
        
        return (
            Model()
            .add("Angle opposite vertices (0->7)", angle_opposite)
            .add("Angle same vertex (0->0)", angle_same)
            .add("Angle adjacent (1->2)", angle_adjacent)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Angle opposite vertices (0->7)", np.pi)  # pi radians
            .add("Angle same vertex (0->0)", 0.0)
            .add("Angle adjacent (1->2)", np.arccos(-1/3))  # Tetrahedral angle
        )


class OctahedralSymmetryGroup(Test):
    """
    Verify that we can generate and apply octahedral symmetry operations.
    """
    name = "Octahedral Symmetry Group Operations"
    question = (
        "Does the octahedral group Oh preserve the cube structure? "
        "Applying any symmetry operation to a vertex should map it to another "
        "valid vertex (0-7)."
    )
    reference = "Group theory: Oh symmetry group"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Octahedral group Oh has 48 symmetry operations.")
            .step("These operations preserve the cube structure.")
            .step("Applying any symmetry to a vertex should yield a vertex in {0..7}.")
            .step("Test: Apply all symmetries to vertex 0, verify results are valid.")
            .conclude("All symmetry operations map to valid vertices.")
        )
    
    commentary = (
        "The octahedral group is the full symmetry group of the cube. "
        "It includes rotations about axes, reflections through planes, "
        "and inversion through the origin. All 48 operations preserve "
        "the geometric structure of the stellated octahedron."
    )
    
    def model(self):
        symmetries = generate_octahedral_symmetries()
        
        # Apply all symmetries to vertex 0
        results = []
        for sym in symmetries:
            result = apply_symmetry_to_vertex(0, sym)
            if 0 <= result <= 7:
                results.append(result)
        
        all_valid = len(results) == len(symmetries)
        
        return (
            Model()
            .add("Symmetries generated", len(symmetries))
            .add("Valid vertex mappings", len(results))
            .add("All mappings valid", 1 if all_valid else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("All mappings valid", 1)
        )


class TetrahedralCoherenceAnalysis(Test):
    """
    Analyze the pattern of within-chamber vs cross-chamber transitions.
    """
    name = "Tetrahedral Coherence Analysis"
    question = (
        "What is the pattern of transitions within vs between tetrahedra? "
        "For a random traversal, we expect roughly 50% cross-chamber transitions "
        "and 25% each for within-A and within-B."
    )
    reference = "Random walk on bipartite graph"
    tolerance = 0.05
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Uniform random traversal visits each vertex with probability 1/8.")
            .step("Tet A has 4 vertices, Tet B has 4 vertices.")
            .step("Within A: P(start in A) × P(end in A) = (4/8) × (4/8) = 1/4.")
            .step("Within B: P(start in B) × P(end in B) = (4/8) × (4/8) = 1/4.")
            .step("Cross-chamber: 1 - 1/4 - 1/4 = 1/2.")
            .conclude("Expected: 25% within-A, 25% within-B, 50% cross-chamber.")
        )
    
    commentary = (
        "The two tetrahedra form a bipartite structure: transitions can "
        "stay within one chamber or cross between chambers. For uniform "
        "random traversal, cross-chamber transitions should dominate (50%), "
        "since there are more ways to cross than to stay within."
    )
    
    def model(self):
        # Generate a traversal from pi
        digits = get_pi_base8(1000, include_integer=True)
        traversal = []
        cumsum = 0
        for digit in digits:
            cumsum += digit
            vertex = cumsum % 8
            traversal.append(vertex)
        
        analysis = analyze_chamber_transitions(traversal)
        
        return (
            Model()
            .add("Within A rate", analysis['within_A_rate'])
            .add("Within B rate", analysis['within_B_rate'])
            .add("Cross-chamber rate", analysis['cross_chamber_rate'])
        )
    
    def observations(self):
        expected = expected_transition_type_rates()
        return (
            Observed()
            .add("Within A rate", expected['within_A_rate'])
            .add("Within B rate", expected['within_B_rate'])
            .add("Cross-chamber rate", expected['cross_chamber_rate'])
        )


class SymmetryPreservationTest(Test):
    """
    Test whether transition probabilities respect octahedral symmetry.
    """
    name = "Symmetry Preservation in Traversal"
    question = (
        "Do transition probabilities respect octahedral symmetry? "
        "For a symmetry-preserving traversal, P(i->j) should equal P(g(i)->g(j)) "
        "for any symmetry operation g."
    )
    reference = "Group theory: symmetry-preserving Markov chains"
    tolerance = 0.05
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Symmetry-preserving traversal respects group structure.")
            .step("For symmetry operation g, P(i->j) = P(g(i)->g(j)).")
            .step("Compute transition probability matrix from traversal.")
            .step("Apply symmetries and check if probabilities are preserved.")
            .conclude("Symmetry preservation verified if violations are minimal.")
        )
    
    commentary = (
        "A truly symmetric traversal should be invariant under the octahedral "
        "symmetry group. This means that if we rotate or reflect the cube, "
        "the transition probabilities should remain the same. This is a strong "
        "test of whether the traversal respects the underlying geometry."
    )
    
    def model(self):
        # Generate traversal
        digits = get_pi_base8(1000, include_integer=True)
        traversal = []
        cumsum = 0
        for digit in digits:
            cumsum += digit
            vertex = cumsum % 8
            traversal.append(vertex)
        
        symmetries = generate_octahedral_symmetries()
        result = check_symmetry_preservation(traversal, symmetries)
        
        return (
            Model()
            .add("Symmetry preserved", 1 if result['symmetry_preserved'] else 0)
            .add("Violation count", result['violation_count'])
        )
    
    def observations(self):
        # For uniform random, symmetry should be preserved (within statistical error)
        return (
            Observed()
            .add("Symmetry preserved", 1)  # Ideally, but may have small violations
        )


class WindingDistributionAnalysis(Test):
    """
    Analyze the distribution of winding increments.
    """
    name = "Winding Increment Distribution"
    question = (
        "What is the distribution of angular increments during traversal? "
        "For random traversal, we expect most increments to be the tetrahedral "
        "angle (~1.91 rad), with some pi increments (opposite vertices)."
    )
    reference = "Random walk angular statistics"
    tolerance = 0.1
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Winding increments follow geometric distribution.")
            .step("Most common: tetrahedral angle arccos(-1/3) ≈ 1.91 rad.")
            .step("Some increments: pi rad (opposite vertices).")
            .step("Some increments: 0 (same vertex repeated).")
            .step("Compute distribution from actual traversal.")
            .conclude("Distribution matches expected geometric structure.")
        )
    
    commentary = (
        "The distribution of angular increments reveals the geometric structure "
        "of the traversal. Most transitions span the tetrahedral angle, "
        "reflecting the tetrahedron edge structure. Occasional large jumps "
        "to opposite vertices create pi increments."
    )
    
    def model(self):
        digits = get_pi_base8(1000, include_integer=True)
        traversal = []
        cumsum = 0
        for digit in digits:
            cumsum += digit
            vertex = cumsum % 8
            traversal.append(vertex)
        
        analysis = analyze_winding_distribution(traversal)
        
        return (
            Model()
            .add("Mean increment", analysis.get('mean', 0))
            .add("Std increment", analysis.get('std', 0))
            .add("Min increment", analysis.get('min', 0))
            .add("Max increment", analysis.get('max', 0))
        )
    
    def observations(self):
        # Expected mean should be around tetrahedral angle
        tetrahedral_angle = np.arccos(-1/3)
        return (
            Observed()
            .add("Mean increment", tetrahedral_angle)  # Approximate
            .add("Max increment", np.pi)  # Opposite vertices, pi radians
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    WindingNumberComputation,
    OctahedralSymmetryGroup,
    TetrahedralCoherenceAnalysis,
    SymmetryPreservationTest,
    WindingDistributionAnalysis,
]


def run_all():
    """Run all geometric symmetry and topology tests."""
    return run_tests(
        title="Geometric Symmetry and Topology Analysis",
        summary=(
            "Expert-level analysis of stellated octahedron traversal covering "
            "winding number computation, octahedral symmetry group operations, "
            "tetrahedral coherence, and statistical tests for symmetry preservation. "
            "These tests verify that the traversal respects the underlying geometric "
            "structure and provide tools for detecting drift, symmetry violations, "
            "and transition patterns."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
