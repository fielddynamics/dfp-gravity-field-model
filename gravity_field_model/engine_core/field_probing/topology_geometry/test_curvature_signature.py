"""
Curvature Signature Probing
===========================

PROBING QUESTION: Does the Merkaba have effective curvature?

In general relativity, gravity is curvature of spacetime. This probe
measures discrete analogs of curvature in the Merkaba structure.

MATHEMATICAL FOUNDATION:
- Gaussian curvature K from angle deficits
- Ricci curvature from volume growth
- Scalar curvature from local geometry

NULL HYPOTHESIS: Flat (zero curvature) or simple discrete geometry
DISCOVERY: Non-trivial curvature would reveal gravitational effects

Reference: Discrete differential geometry, Regge calculus
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def get_vertex_coordinates(vertex: int) -> np.ndarray:
    """Get 3D coordinates of a vertex."""
    coords = VERTICES[vertex]['coords']
    return np.array(coords, dtype=float)


def compute_angle_deficit(vertex: int) -> float:
    """
    Compute angle deficit at a vertex.
    
    In a flat space, angles around a point sum to 2*pi.
    Deficit = 2*pi - sum(angles)
    
    For discrete curvature: K = deficit / area
    """
    # Find neighboring vertices (all other vertices in same tetrahedron)
    if vertex in TET_A:
        neighbors = [v for v in TET_A if v != vertex]
    else:
        neighbors = [v for v in TET_B if v != vertex]
    
    # Add vertices from the other tetrahedron that share faces
    # (All 4 vertices of the other tetrahedron are neighbors in the Merkaba)
    if vertex in TET_A:
        neighbors.extend(TET_B)
    else:
        neighbors.extend(TET_A)
    
    # Compute angles between adjacent neighbor pairs
    r_center = get_vertex_coordinates(vertex)
    angles = []
    
    for i in range(len(neighbors)):
        for j in range(i + 1, len(neighbors)):
            r_i = get_vertex_coordinates(neighbors[i]) - r_center
            r_j = get_vertex_coordinates(neighbors[j]) - r_center
            
            cos_angle = np.dot(r_i, r_j) / (np.linalg.norm(r_i) * np.linalg.norm(r_j))
            cos_angle = np.clip(cos_angle, -1, 1)
            angle = math.acos(cos_angle)
            angles.append(angle)
    
    # For a vertex on a polyhedron, we sum angles of faces meeting at vertex
    # Approximation: sum all angles and compare to expected
    angle_sum = sum(angles)
    
    # For 7 neighbors (3 same tet + 4 other tet), expected sum depends on geometry
    # We use 4*pi as rough expected value for solid angle
    expected = 4 * math.pi  
    
    return expected - angle_sum


def compute_volume_growth_rate(history: List[int], r_max: int = 3) -> np.ndarray:
    """
    Compute how "volume" (number of reachable vertices) grows with distance.
    
    In flat space: V(r) ~ r^d (d = dimension)
    In curved space: different growth rate
    """
    # Build graph adjacency from transitions
    adj = np.zeros((8, 8), dtype=int)
    for i in range(len(history) - 1):
        adj[history[i], history[i+1]] = 1
        adj[history[i+1], history[i]] = 1  # Undirected
    
    # Count reachable vertices at each distance
    volume_at_r = []
    
    for source in range(8):
        reached = {source}
        frontier = {source}
        
        for r in range(1, r_max + 1):
            new_frontier = set()
            for v in frontier:
                for w in range(8):
                    if adj[v, w] == 1 and w not in reached:
                        new_frontier.add(w)
                        reached.add(w)
            frontier = new_frontier
            volume_at_r.append(len(reached))
    
    return np.array(volume_at_r)


def compute_local_acceleration(history: List[int]) -> List[float]:
    """
    Compute local acceleration (deviation from geodesic).
    
    Acceleration = r'' = (v_{t+1} - v_t) - (v_t - v_{t-1})
    
    Non-zero acceleration indicates curvature or force.
    """
    accelerations = []
    
    for i in range(1, len(history) - 1):
        r_prev = get_vertex_coordinates(history[i-1])
        r_curr = get_vertex_coordinates(history[i])
        r_next = get_vertex_coordinates(history[i+1])
        
        v_in = r_curr - r_prev
        v_out = r_next - r_curr
        
        accel = v_out - v_in
        accelerations.append(np.linalg.norm(accel))
    
    return accelerations


# =============================================================================
# TEST CLASSES
# =============================================================================

class AngleDeficitProbe(Test):
    """
    PROBING: Measure curvature via angle deficits.
    """
    name = "Angle Deficit (Gaussian Curvature)"
    question = (
        "What is the curvature at each vertex of the Merkaba? In Regge calculus, "
        "curvature is localized at vertices and measured by angle deficit: "
        "how much the angles around a vertex differ from flat space."
    )
    reference = "Regge calculus, discrete curvature"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We compute the angle deficit at each vertex, which is a "
        "discrete analog of Gaussian curvature. Non-zero deficit indicates "
        "intrinsic curvature of the discrete space."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ANGLE DEFICIT (Regge curvature):")
            .equation("delta = 2*pi - sum(angles around vertex)")
            .step("GAUSSIAN CURVATURE (discrete):")
            .equation("K = delta / A")
            .step("where A is area of dual cell around vertex")
            .step("FLAT SPACE: delta = 0")
            .step("POSITIVE CURVATURE: delta > 0 (sphere-like)")
            .step("NEGATIVE CURVATURE: delta < 0 (saddle-like)")
            .conclude("Angle deficit measures discrete curvature.")
        )

    def model(self):
        # Compute angle deficit at each vertex
        deficits = {}
        for v in range(8):
            deficits[v] = compute_angle_deficit(v)
        
        teta_deficits = [deficits[v] for v in TET_A]
        tetb_deficits = [deficits[v] for v in TET_B]
        
        mean_deficit_a = np.mean(teta_deficits)
        mean_deficit_b = np.mean(tetb_deficits)
        
        # Total curvature (Gauss-Bonnet: sum of deficits = 4*pi for sphere)
        total_deficit = sum(deficits.values())
        
        return (
            Model()
            .add("Mean deficit TetA", mean_deficit_a)
            .add("Mean deficit TetB", mean_deficit_b)
            .add("Total deficit (all vertices)", total_deficit)
            .add("Expected for sphere (4*pi)", 4 * math.pi)
            .add("Curvature ratio", total_deficit / (4 * math.pi))
        )

    def observations(self) -> Observed:
        # Random-digit baseline. Each expected value is the mean of the metric
        # over 150 uniformly random base-8 digit sequences of the same length
        # as the pi digits (seeds 5000-5149), and the absolute tolerance is
        # 1.15 times the largest distance from that mean to the most extreme
        # of the 150 values. A pass means pi is indistinguishable from random
        # digits on this metric; a fail would be a property of pi itself.
        # Metrics marked 'same for all random sequences' are fixed by the
        # traversal rule for any generic sequence (degenerate sequences such
        # as all zeros change them). The previous expected values were
        # unsourced guesses.
        return (
            Observed()
            .add("Mean deficit TetA", -9.424777960769, abs_tol=9e-09)  # same for all 150 random sequences
            .add("Mean deficit TetB", -9.424777960769, abs_tol=9e-09)  # same for all 150 random sequences
            .add("Total deficit (all vertices)", -75.398223686155, abs_tol=8e-08)  # same for all 150 random sequences
            .add("Expected for sphere (4*pi)", 12.566370614359, abs_tol=1e-08)  # same for all 150 random sequences
            .add("Curvature ratio", -6, abs_tol=6e-09)  # same for all 150 random sequences
        )

class EffectiveAccelerationProbe(Test):
    """
    PROBING: Measure effective acceleration (geodesic deviation).
    """
    name = "Effective Acceleration Analysis"
    question = (
        "Does the trajectory experience 'acceleration' (deviation from straight "
        "motion)? In curved space, geodesics accelerate relative to each other. "
        "High acceleration suggests curvature or external forces."
    )
    reference = "Geodesic deviation, curvature from dynamics"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We compute acceleration as the second derivative of position. "
        "In flat space with no forces, geodesics are straight (zero acceleration). "
        "Non-zero acceleration indicates curvature effects."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ACCELERATION (second derivative):")
            .equation("a = r'' = v_{out} - v_{in}")
            .step("where v_{in} = r(t) - r(t-1), v_{out} = r(t+1) - r(t)")
            .step("IN FLAT SPACE:")
            .step("Geodesics are straight: a = 0")
            .step("IN CURVED SPACE:")
            .step("Geodesic deviation: a != 0 due to curvature")
            .step("|a| measures local curvature or force")
            .conclude("Acceleration reveals curvature effects.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute accelerations
        accelerations = compute_local_acceleration(history)
        
        mean_accel = np.mean(accelerations)
        std_accel = np.std(accelerations)
        max_accel = np.max(accelerations)
        
        # Fraction with high acceleration
        frac_high = np.mean(np.array(accelerations) > mean_accel + std_accel)
        
        return (
            Model()
            .add("Mean acceleration", mean_accel)
            .add("Std of acceleration", std_accel)
            .add("Max acceleration", max_accel)
            .add("Fraction high acceleration", frac_high)
            .add("Is curved (accel > 0)", 1.0 if mean_accel > 0.1 else 0.0)
        )

    def observations(self) -> Observed:
        # Random-digit baseline. Each expected value is the mean of the metric
        # over 150 uniformly random base-8 digit sequences of the same length
        # as the pi digits (seeds 5000-5149), and the absolute tolerance is
        # 1.15 times the largest distance from that mean to the most extreme
        # of the 150 values. A pass means pi is indistinguishable from random
        # digits on this metric; a fail would be a property of pi itself.
        # Metrics marked 'same for all random sequences' are fixed by the
        # traversal rule for any generic sequence (degenerate sequences such
        # as all zeros change them). The previous expected values were
        # unsourced guesses.
        return (
            Observed()
            .add("Mean acceleration", 4.0335, abs_tol=0.091)  # random range [3.96924, 4.11226]
            .add("Std of acceleration", 1.32227, abs_tol=0.06)  # random range [1.28163, 1.37374]
            .add("Max acceleration", 6.928203230276, abs_tol=7e-09)  # same for all 150 random sequences
            .add("Fraction high acceleration", 0.156798, abs_tol=0.021)  # random range [0.143829, 0.174635]
            .add("Is curved (accel > 0)", 1, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    AngleDeficitProbe,
    EffectiveAccelerationProbe,
]


def run_all():
    """Run all curvature signature probing tests."""
    summary = (
        "CURVATURE SIGNATURE PROBING\n\n"
        "These probes measure discrete curvature.\n"
        "Angle deficit: Gaussian curvature at vertices\n"
        "Acceleration: geodesic deviation from curvature\n\n"
        "We are DISCOVERING the field's geometry."
    )
    return run_tests("Curvature Signature Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
