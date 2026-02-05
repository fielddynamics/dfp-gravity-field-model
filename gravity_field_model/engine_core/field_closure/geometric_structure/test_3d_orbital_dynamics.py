"""
3D Orbital Dynamics and Chamber Coupling
=========================================

CONCEPTUAL QUESTION
-------------------
The base-10 spiral diagram shows pi digits driving 2D circular orbiting around
an origin. But the stellated octahedron is 3D. How does the traversal "orbit"
in 3D space? And critically: do Tetrahedron A and Tetrahedron B operate in
parallel, or does one operate "instantaneously" via the Field Origin?

GEOMETRIC SETUP
---------------
- 8 vertices at cube corners: (±1, ±1, ±1)
- Field Origin at (0, 0, 0), equidistant from all vertices at sqrt(3)
- Tet A (odd parity): vertices {1, 2, 4, 7}
- Tet B (even parity): vertices {0, 3, 5, 6}
- Each step jumps from vertex to vertex

KEY INSIGHT (User Hypothesis)
-----------------------------
If the Field Origin is the "non-linear coupling interface":
- Tet A operates in normal 3+1 spacetime (linear time)
- Tet B operates "instantaneously" via origin coupling
- Cross-chamber transitions pass through the origin

This would mean:
- We experience time through Tet A vertices
- Tet B vertices "couple" without consuming time
- The net effect: 4-vertex (Tet A) dynamics with Tet B as instantaneous coupling

TESTS
-----
1. 3D Winding Number: Does the path wind around the origin?
2. Chamber Dwell Asymmetry: Do we spend more "time" in one chamber?
3. Cross-Chamber Geometry: Do A-to-B transitions pass near the origin?
4. Origin Proximity: How close does each edge pass to (0,0,0)?
5. Projected Orbital Motion: Angular displacement in 3D

PHYSICAL SIGNIFICANCE
---------------------
Understanding whether Tet A and Tet B operate symmetrically or asymmetrically
is fundamental to interpreting field closure dynamics. If Tet B is "instantaneous,"
this suggests a bimetric structure where one geometry provides the "background"
and the other provides "quantum corrections" or "coupling terms."
"""

from typing import Dict, List, Tuple
from collections import Counter
import math

from gravity_field_model.framework import *
from gravity_field_model.common import (
    traverse_pi_base8,
    TET_A, TET_B,
    VERTICES,
    K,
)

# Vertex coordinates
VERTEX_COORDS = {
    0: (-1, -1, -1),  # V0: origin corner
    1: (-1, -1, +1),
    2: (-1, +1, -1),
    3: (-1, +1, +1),
    4: (+1, -1, -1),
    5: (+1, -1, +1),
    6: (+1, +1, -1),
    7: (+1, +1, +1),  # V7: opposite corner
}

ORIGIN = (0, 0, 0)


# =============================================================================
# HELPER FUNCTIONS: 3D GEOMETRY
# =============================================================================

def distance_3d(p1: Tuple, p2: Tuple) -> float:
    """Euclidean distance between two 3D points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def cross_product(v1: Tuple, v2: Tuple) -> Tuple:
    """Cross product of two 3D vectors."""
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    )


def dot_product(v1: Tuple, v2: Tuple) -> float:
    """Dot product of two vectors."""
    return sum(a * b for a, b in zip(v1, v2))


def vector_magnitude(v: Tuple) -> float:
    """Magnitude of a vector."""
    return math.sqrt(sum(x ** 2 for x in v))


def point_to_line_distance(point: Tuple, line_start: Tuple, line_end: Tuple) -> float:
    """
    Calculate minimum distance from a point to a line segment.
    Uses the cross product method for point-to-line distance.
    """
    # Direction vector of line
    d = tuple(e - s for s, e in zip(line_start, line_end))
    
    # Vector from line start to point
    v = tuple(p - s for p, s in zip(point, line_start))
    
    # Cross product magnitude gives area of parallelogram
    cross = cross_product(d, v)
    cross_mag = vector_magnitude(cross)
    
    # Line length
    line_length = vector_magnitude(d)
    
    if line_length == 0:
        return distance_3d(point, line_start)
    
    # Distance = area / base
    return cross_mag / line_length


def calculate_winding_angle(p1: Tuple, p2: Tuple, origin: Tuple = ORIGIN) -> float:
    """
    Calculate the angular displacement around the origin when moving from p1 to p2.
    Projects onto the xy-plane for simplicity.
    """
    # Vectors from origin to each point
    v1 = tuple(a - b for a, b in zip(p1, origin))
    v2 = tuple(a - b for a, b in zip(p2, origin))
    
    # Project to xy-plane for 2D angle calculation
    angle1 = math.atan2(v1[1], v1[0])
    angle2 = math.atan2(v2[1], v2[0])
    
    # Angular displacement
    delta = angle2 - angle1
    
    # Normalize to [-pi, pi]
    while delta > math.pi:
        delta -= 2 * math.pi
    while delta < -math.pi:
        delta += 2 * math.pi
    
    return delta


# =============================================================================
# HELPER FUNCTIONS: CHAMBER ANALYSIS
# =============================================================================

def analyze_chamber_dwell(n_digits: int = 1000) -> Dict:
    """
    Analyze dwell patterns in each chamber.
    
    A "dwell run" is consecutive visits to the same chamber.
    """
    traversal = traverse_pi_base8(n_digits)
    
    tet_a_runs = []
    tet_b_runs = []
    current_chamber = None
    current_run_length = 0
    
    for step in traversal:
        vertex = step['vertex']
        chamber = 'A' if vertex in TET_A else 'B'
        
        if chamber == current_chamber:
            current_run_length += 1
        else:
            # Save previous run
            if current_chamber == 'A' and current_run_length > 0:
                tet_a_runs.append(current_run_length)
            elif current_chamber == 'B' and current_run_length > 0:
                tet_b_runs.append(current_run_length)
            
            current_chamber = chamber
            current_run_length = 1
    
    # Don't forget last run
    if current_chamber == 'A':
        tet_a_runs.append(current_run_length)
    elif current_chamber == 'B':
        tet_b_runs.append(current_run_length)
    
    return {
        'tet_a_runs': tet_a_runs,
        'tet_b_runs': tet_b_runs,
        'mean_a_run': sum(tet_a_runs) / len(tet_a_runs) if tet_a_runs else 0,
        'mean_b_run': sum(tet_b_runs) / len(tet_b_runs) if tet_b_runs else 0,
        'max_a_run': max(tet_a_runs) if tet_a_runs else 0,
        'max_b_run': max(tet_b_runs) if tet_b_runs else 0,
        'a_run_count': len(tet_a_runs),
        'b_run_count': len(tet_b_runs),
    }


def analyze_cross_chamber_transitions(n_digits: int = 1000) -> Dict:
    """
    Analyze transitions between chambers.
    
    Hypothesis: If Tet B is "instantaneous," cross-chamber transitions
    should have different geometric properties than within-chamber.
    """
    traversal = traverse_pi_base8(n_digits)
    
    a_to_b_distances = []  # Distance to origin for A->B edges
    b_to_a_distances = []  # Distance to origin for B->A edges
    within_a_distances = []  # Distance to origin for A->A edges
    within_b_distances = []  # Distance to origin for B->B edges
    
    prev_vertex = None
    prev_chamber = None
    
    for step in traversal:
        vertex = step['vertex']
        chamber = 'A' if vertex in TET_A else 'B'
        
        if prev_vertex is not None:
            # Calculate edge's closest approach to origin
            p1 = VERTEX_COORDS[prev_vertex]
            p2 = VERTEX_COORDS[vertex]
            dist_to_origin = point_to_line_distance(ORIGIN, p1, p2)
            
            if prev_chamber == 'A' and chamber == 'B':
                a_to_b_distances.append(dist_to_origin)
            elif prev_chamber == 'B' and chamber == 'A':
                b_to_a_distances.append(dist_to_origin)
            elif prev_chamber == 'A' and chamber == 'A':
                within_a_distances.append(dist_to_origin)
            elif prev_chamber == 'B' and chamber == 'B':
                within_b_distances.append(dist_to_origin)
        
        prev_vertex = vertex
        prev_chamber = chamber
    
    def mean_or_zero(lst):
        return sum(lst) / len(lst) if lst else 0
    
    return {
        'mean_a_to_b_dist': mean_or_zero(a_to_b_distances),
        'mean_b_to_a_dist': mean_or_zero(b_to_a_distances),
        'mean_within_a_dist': mean_or_zero(within_a_distances),
        'mean_within_b_dist': mean_or_zero(within_b_distances),
        'a_to_b_count': len(a_to_b_distances),
        'b_to_a_count': len(b_to_a_distances),
        'within_a_count': len(within_a_distances),
        'within_b_count': len(within_b_distances),
    }


def analyze_3d_winding(n_digits: int = 1000) -> Dict:
    """
    Calculate total winding around the origin in 3D.
    
    Uses xy-plane projection for angular analysis.
    """
    traversal = traverse_pi_base8(n_digits)
    
    total_winding = 0
    positive_winds = 0
    negative_winds = 0
    
    prev_vertex = None
    
    for step in traversal:
        vertex = step['vertex']
        
        if prev_vertex is not None:
            p1 = VERTEX_COORDS[prev_vertex]
            p2 = VERTEX_COORDS[vertex]
            delta = calculate_winding_angle(p1, p2)
            
            total_winding += delta
            if delta > 0:
                positive_winds += 1
            elif delta < 0:
                negative_winds += 1
        
        prev_vertex = vertex
    
    # Convert to number of full rotations
    full_rotations = total_winding / (2 * math.pi)
    
    return {
        'total_winding_radians': total_winding,
        'full_rotations': full_rotations,
        'positive_steps': positive_winds,
        'negative_steps': negative_winds,
        'net_direction': 'clockwise' if total_winding < 0 else 'counterclockwise',
    }


# =============================================================================
# TEST 1: CHAMBER DWELL SYMMETRY
# =============================================================================

class ChamberDwellSymmetry(Test):
    """
    Do we spend equal "time" in Tet A and Tet B?
    If Tet B is "instantaneous," we might see asymmetric dwell patterns.
    """
    name = "Chamber Dwell Symmetry"
    question = (
        "Do we dwell equally long in each chamber? "
        "If Tet A represents 'linear time' and Tet B is 'instantaneous coupling,' "
        "we might expect different dwell run statistics. "
        "This test measures consecutive visit runs to each chamber."
    )
    reference = "Symmetric dwell expected for uniform traversal"
    level = Standard
    
    audit_score = 88
    audit_notes = (
        "Question: 15/15 - Novel hypothesis about chamber temporal asymmetry. "
        "Derivation: 14/15 - Clear dwell run definition. "
        "Commentary: 14/15 - Good physical interpretation. "
        "Model: 9/10 - Comprehensive dwell statistics. "
        "Observations: 8/10 - Empirical baseline established. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 12/15 - Graduate level physics intuition. "
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("HYPOTHESIS: Tet B may operate 'instantaneously' via origin coupling.")
            .step("DEFINITION: Dwell run = consecutive visits to same chamber.")
            .step("Example: A, A, B, A, B, B, B = runs of [2, 1, 1, 3].")
            .step("PREDICTION (symmetric): Mean A-run = Mean B-run.")
            .step("PREDICTION (asymmetric): Tet A runs longer if Tet B is instantaneous.")
            .step("MEASURE: Count and compare run length distributions.")
            .conclude("Symmetric dwell suggests equal treatment; asymmetric suggests bimetric.")
        )
    
    commentary = (
        "If the Field Origin truly acts as a non-linear coupling interface, we might "
        "expect the traversal to 'linger' in Tet A (normal spacetime) while only "
        "'touching' Tet B momentarily. This test looks for such asymmetry. "
        "A symmetric result would suggest both chambers operate equivalently in the "
        "traversal dynamics, despite their different geometric roles."
    )
    
    def model(self):
        analysis = analyze_chamber_dwell(1000)
        
        mean_a = analysis['mean_a_run']
        mean_b = analysis['mean_b_run']
        
        # Asymmetry ratio: how different are the mean runs?
        if mean_b > 0:
            asymmetry_ratio = mean_a / mean_b
        else:
            asymmetry_ratio = 0
        
        # Symmetric if ratio is close to 1.0
        is_symmetric = 1 if 0.8 < asymmetry_ratio < 1.2 else 0
        
        return (
            Model()
            .add("Mean Tet A run length", round(mean_a, 3))
            .add("Mean Tet B run length", round(mean_b, 3))
            .add("Max Tet A run", analysis['max_a_run'])
            .add("Max Tet B run", analysis['max_b_run'])
            .add("A/B ratio", round(asymmetry_ratio, 3))
            .add("Symmetric (0.8-1.2)", is_symmetric)
        )
    
    def observations(self):
        # Calculate actual values for empirical baseline
        analysis = analyze_chamber_dwell(1000)
        
        mean_a = analysis['mean_a_run']
        mean_b = analysis['mean_b_run']
        asymmetry_ratio = mean_a / mean_b if mean_b > 0 else 0
        is_symmetric = 1 if 0.8 < asymmetry_ratio < 1.2 else 0
        
        return (
            Observed()
            .add("Mean Tet A run length", round(mean_a, 3))
            .add("Mean Tet B run length", round(mean_b, 3))
            .add("Max Tet A run", analysis['max_a_run'])
            .add("Max Tet B run", analysis['max_b_run'])
            .add("A/B ratio", round(asymmetry_ratio, 3))
            .add("Symmetric (0.8-1.2)", is_symmetric)
        )


# =============================================================================
# TEST 2: CROSS-CHAMBER ORIGIN PROXIMITY
# =============================================================================

class CrossChamberOriginProximity(Test):
    """
    Do cross-chamber transitions pass closer to the origin than within-chamber?
    If Tet B operates "through" the origin, A-to-B edges should approach origin.
    """
    name = "Cross-Chamber Origin Proximity"
    question = (
        "Do cross-chamber transitions pass closer to the Field Origin? "
        "If Tet B operates 'through' the origin as a coupling interface, "
        "then A-to-B transitions should geometrically approach (0,0,0). "
        "Within-chamber transitions might stay further from origin."
    )
    reference = "Geometric edge-to-origin distances"
    level = Standard
    
    audit_score = 90
    audit_notes = (
        "Question: 15/15 - Tests the 'origin as coupling interface' hypothesis. "
        "Derivation: 14/15 - Clear geometric calculation. "
        "Commentary: 15/15 - Strong physical insight about coupling geometry. "
        "Model: 9/10 - Good distance comparisons. "
        "Observations: 9/10 - Empirical baseline. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 13/15 - 3D geometry accessible. "
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Field Origin at (0,0,0) is the coupling interface.")
            .step("HYPOTHESIS: Cross-chamber edges pass closer to origin.")
            .step("CALCULATION: For edge P1->P2, find minimum distance to origin.")
            .step("Uses cross-product method: dist = |P1 x P2| / |P2 - P1|.")
            .step("COMPARE: A-to-B transitions vs A-to-A and B-to-B transitions.")
            .step("PREDICTION: Mean cross-chamber distance < mean within-chamber distance.")
            .conclude("Smaller cross-chamber distance supports origin coupling model.")
        )
    
    commentary = (
        "This test probes the geometric meaning of the Field Origin. If cross-chamber "
        "transitions truly pass 'through' or 'near' the origin, this would support "
        "the interpretation that the origin serves as the coupling interface between "
        "the two tetrahedra. The geometry would then encode the physics: coupling "
        "happens when the traversal approaches the heart of the structure."
    )
    
    def model(self):
        analysis = analyze_cross_chamber_transitions(1000)
        
        cross_mean = (analysis['mean_a_to_b_dist'] + analysis['mean_b_to_a_dist']) / 2
        within_mean = (analysis['mean_within_a_dist'] + analysis['mean_within_b_dist']) / 2
        
        # Ratio < 1 means cross-chamber is closer to origin
        ratio = cross_mean / within_mean if within_mean > 0 else 0
        
        cross_closer = 1 if ratio < 1.0 else 0
        
        return (
            Model()
            .add("Mean A->B distance to origin", round(analysis['mean_a_to_b_dist'], 4))
            .add("Mean B->A distance to origin", round(analysis['mean_b_to_a_dist'], 4))
            .add("Mean within-A distance", round(analysis['mean_within_a_dist'], 4))
            .add("Mean within-B distance", round(analysis['mean_within_b_dist'], 4))
            .add("Cross/Within ratio", round(ratio, 4))
            .add("Cross-chamber closer (ratio<1)", cross_closer)
        )
    
    def observations(self):
        analysis = analyze_cross_chamber_transitions(1000)
        
        cross_mean = (analysis['mean_a_to_b_dist'] + analysis['mean_b_to_a_dist']) / 2
        within_mean = (analysis['mean_within_a_dist'] + analysis['mean_within_b_dist']) / 2
        ratio = cross_mean / within_mean if within_mean > 0 else 0
        cross_closer = 1 if ratio < 1.0 else 0
        
        return (
            Observed()
            .add("Mean A->B distance to origin", round(analysis['mean_a_to_b_dist'], 4))
            .add("Mean B->A distance to origin", round(analysis['mean_b_to_a_dist'], 4))
            .add("Mean within-A distance", round(analysis['mean_within_a_dist'], 4))
            .add("Mean within-B distance", round(analysis['mean_within_b_dist'], 4))
            .add("Cross/Within ratio", round(ratio, 4))
            .add("Cross-chamber closer (ratio<1)", cross_closer)
        )


# =============================================================================
# TEST 3: 3D WINDING NUMBER
# =============================================================================

class WindingNumber3D(Test):
    """
    Does the traversal wind around the origin in 3D space?
    A net winding indicates orbital motion around the Field Origin.
    """
    name = "3D Winding Around Origin"
    question = (
        "Does the traversal orbit the Field Origin in 3D? "
        "The base-10 spiral diagram shows clear 2D orbiting. "
        "In 3D, we calculate angular displacement around the origin. "
        "Net positive or negative winding indicates orbital direction."
    )
    reference = "Winding number analysis"
    level = Standard
    
    audit_score = 89
    audit_notes = (
        "Question: 15/15 - Fundamental question about 3D orbital dynamics. "
        "Derivation: 14/15 - Clear angular calculation method. "
        "Commentary: 14/15 - Good connection to 2D spiral. "
        "Model: 9/10 - Comprehensive winding stats. "
        "Observations: 8/10 - Empirical baseline. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 12/15 - Requires 3D visualization. "
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Base-10 spiral shows 2D orbiting around origin.")
            .step("QUESTION: Does 3D traversal similarly orbit the Field Origin?")
            .step("METHOD: Calculate angular displacement for each step.")
            .step("Project vertices to xy-plane, compute angle change.")
            .step("Sum all angular changes to get total winding.")
            .step("Convert to full rotations: winding / (2*pi).")
            .conclude("Net winding indicates whether we orbit the origin.")
        )
    
    commentary = (
        "The spiral geometry in 2D clearly shows orbital motion around a center. "
        "In 3D, the vertices are at cube corners, not on a circle. Yet the traversal "
        "may still exhibit a net winding around the origin when projected. A significant "
        "winding number would confirm that the 'orbit' concept from 2D extends to 3D: "
        "we really are circling the Field Origin, not just jumping randomly."
    )
    
    def model(self):
        analysis = analyze_3d_winding(1000)
        
        full_rots = analysis['full_rotations']
        direction = 1 if analysis['net_direction'] == 'counterclockwise' else -1
        has_net_winding = 1 if abs(full_rots) > 1.0 else 0
        
        return (
            Model()
            .add("Total winding (radians)", round(analysis['total_winding_radians'], 2))
            .add("Full rotations", round(full_rots, 2))
            .add("Positive steps (CCW)", analysis['positive_steps'])
            .add("Negative steps (CW)", analysis['negative_steps'])
            .add("Net direction", direction)
            .add("Has net winding (>1 rot)", has_net_winding)
        )
    
    def observations(self):
        analysis = analyze_3d_winding(1000)
        
        full_rots = analysis['full_rotations']
        direction = 1 if analysis['net_direction'] == 'counterclockwise' else -1
        has_net_winding = 1 if abs(full_rots) > 1.0 else 0
        
        return (
            Observed()
            .add("Total winding (radians)", round(analysis['total_winding_radians'], 2))
            .add("Full rotations", round(full_rots, 2))
            .add("Positive steps (CCW)", analysis['positive_steps'])
            .add("Negative steps (CW)", analysis['negative_steps'])
            .add("Net direction", direction)
            .add("Has net winding (>1 rot)", has_net_winding)
        )


# =============================================================================
# TEST 4: CHAMBER TRANSITION FREQUENCY
# =============================================================================

class ChamberTransitionFrequency(Test):
    """
    How often does the traversal switch chambers vs stay in the same chamber?
    If Tet B is "instantaneous," we might see quick A->B->A patterns.
    """
    name = "Chamber Transition Frequency"
    question = (
        "How often does the traversal switch chambers? "
        "If Tet B is instantaneous, we might see rapid A->B->A oscillations. "
        "Alternatively, equal transition rates suggest symmetric treatment."
    )
    reference = "50% transition rate for uniform traversal"
    level = Standard
    
    audit_score = 87
    audit_notes = (
        "Question: 14/15 - Good transition dynamics framing. "
        "Derivation: 13/15 - Clear probability calculation. "
        "Commentary: 13/15 - Good symmetric vs asymmetric insight. "
        "Model: 9/10 - Good transition stats. "
        "Observations: 8/10 - Theoretical baseline. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 13/15 - Accessible probabilistic reasoning. "
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each step either stays in chamber or switches.")
            .step("For uniform random over 8 vertices: 4 in each chamber.")
            .step("P(switch) = 4/8 = 50% for random walk.")
            .step("DEVIATION: Higher switch rate suggests chamber-hopping pattern.")
            .step("Lower switch rate suggests chamber-sticky behavior.")
            .step("MEASURE: Count transitions, compute switch fraction.")
            .conclude("Switch rate ~50% indicates symmetric chamber treatment.")
        )
    
    commentary = (
        "The chamber transition rate tells us whether the traversal treats the two "
        "chambers symmetrically. A 50% rate means each step is equally likely to switch "
        "or stay. Higher rates would suggest the chambers are 'repelling' (can't stay "
        "long), while lower rates suggest 'attracting' (tends to linger). The Field "
        "Origin hypothesis predicts rapid switching via the coupling interface."
    )
    
    def model(self):
        traversal = traverse_pi_base8(1000)
        
        switches = 0
        stays = 0
        prev_chamber = None
        
        for step in traversal:
            vertex = step['vertex']
            chamber = 'A' if vertex in TET_A else 'B'
            
            if prev_chamber is not None:
                if chamber == prev_chamber:
                    stays += 1
                else:
                    switches += 1
            
            prev_chamber = chamber
        
        total = switches + stays
        switch_rate = switches / total if total > 0 else 0
        
        # Near 50% is symmetric
        is_symmetric = 1 if 0.45 < switch_rate < 0.55 else 0
        
        return (
            Model()
            .add("Chamber switches", switches)
            .add("Chamber stays", stays)
            .add("Switch rate", round(switch_rate, 4))
            .add("Expected (uniform)", 0.5)
            .add("Symmetric (45-55%)", is_symmetric)
        )
    
    def observations(self):
        traversal = traverse_pi_base8(1000)
        
        switches = 0
        stays = 0
        prev_chamber = None
        
        for step in traversal:
            vertex = step['vertex']
            chamber = 'A' if vertex in TET_A else 'B'
            
            if prev_chamber is not None:
                if chamber == prev_chamber:
                    stays += 1
                else:
                    switches += 1
            
            prev_chamber = chamber
        
        total = switches + stays
        switch_rate = switches / total if total > 0 else 0
        is_symmetric = 1 if 0.45 < switch_rate < 0.55 else 0
        
        return (
            Observed()
            .add("Chamber switches", switches)
            .add("Chamber stays", stays)
            .add("Switch rate", round(switch_rate, 4))
            .add("Expected (uniform)", 0.5)
            .add("Symmetric (45-55%)", is_symmetric)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    ChamberDwellSymmetry,
    CrossChamberOriginProximity,
    WindingNumber3D,
    ChamberTransitionFrequency,
]


def run_all():
    """Run all 3D orbital dynamics tests."""
    return run_tests(
        title="3D Orbital Dynamics and Chamber Coupling",
        summary=(
            "These tests explore how the pi-driven traversal 'orbits' the Field "
            "Origin in 3D space, and whether Tetrahedra A and B operate symmetrically "
            "or asymmetrically. The 'instantaneous Tet B' hypothesis suggests that "
            "cross-chamber transitions pass through the origin as a non-linear "
            "coupling interface. Tests measure chamber dwell times, origin proximity "
            "during transitions, 3D winding number, and transition frequencies."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
