"""
Knot Invariants Probing
=======================

PROBING QUESTION: Does the trajectory form knots or links?

Knot invariants classify the topological complexity of curves.
A knotted trajectory cannot be continuously deformed to a circle.

MATHEMATICAL FOUNDATION:
- Linking number: algebraic count of crossings
- Writhe: sum of signed self-crossings
- Self-linking: measure of trajectory complexity

NULL HYPOTHESIS: Unknotted trajectory (topologically trivial)
DISCOVERY: Knots would indicate topological field structure

Reference: Knot theory, topological invariants
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


def compute_crossing_number(history: List[int], projection: str = 'z') -> int:
    """
    Compute approximate crossing number in 2D projection.
    
    A crossing occurs when two non-adjacent segments intersect in projection.
    """
    # Get 2D projected coordinates
    def project(v):
        r = get_vertex_coordinates(v)
        if projection == 'z':
            return r[0], r[1]
        elif projection == 'y':
            return r[0], r[2]
        else:
            return r[1], r[2]
    
    # Get segments
    segments = []
    for i in range(len(history) - 1):
        p1 = project(history[i])
        p2 = project(history[i + 1])
        segments.append((p1, p2, i))
    
    def segments_intersect(s1, s2):
        """Check if two segments intersect (excluding endpoints)."""
        (x1, y1), (x2, y2), _ = s1
        (x3, y3), (x4, y4), _ = s2
        
        # Parametric intersection
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return False
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        return 0 < t < 1 and 0 < u < 1
    
    # Count crossings (non-adjacent segment pairs)
    crossings = 0
    for i in range(len(segments)):
        for j in range(i + 2, len(segments)):  # Skip adjacent segments
            if segments_intersect(segments[i], segments[j]):
                crossings += 1
    
    return crossings


def compute_writhe(history: List[int]) -> float:
    """
    Compute writhe (signed sum of crossings).
    
    Writhe is a measure of how much the curve twists and coils.
    """
    # Simplified writhe calculation using triple scalar product
    writhe = 0.0
    
    for i in range(len(history) - 3):
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i + 1])
        r3 = get_vertex_coordinates(history[i + 2])
        r4 = get_vertex_coordinates(history[i + 3])
        
        # Vectors
        v1 = r2 - r1
        v2 = r3 - r2
        v3 = r4 - r3
        
        # Triple scalar product (measures twist)
        twist = np.dot(v1, np.cross(v2, v3))
        
        # Normalize
        norm = np.linalg.norm(v1) * np.linalg.norm(v2) * np.linalg.norm(v3)
        if norm > 0:
            writhe += twist / norm
    
    return writhe / (2 * math.pi)  # Normalize to "number of twists"


def compute_linking_number(hist1: List[int], hist2: List[int]) -> float:
    """
    Compute linking number between two trajectories.
    
    Linking number counts how many times the curves wind around each other.
    """
    # Gauss linking integral approximation
    linking = 0.0
    
    for i in range(len(hist1) - 1):
        r1 = get_vertex_coordinates(hist1[i])
        r2 = get_vertex_coordinates(hist1[i + 1])
        
        for j in range(len(hist2) - 1):
            r3 = get_vertex_coordinates(hist2[j])
            r4 = get_vertex_coordinates(hist2[j + 1])
            
            # Gauss linking integral contribution
            r13 = r3 - r1
            r14 = r4 - r1
            r23 = r3 - r2
            r24 = r4 - r2
            
            n1 = np.cross(r13, r14)
            n2 = np.cross(r14, r24)
            n3 = np.cross(r24, r23)
            n4 = np.cross(r23, r13)
            
            for n in [n1, n2, n3, n4]:
                norm = np.linalg.norm(n)
                if norm > 0:
                    n /= norm
            
            # Solid angle contribution
            omega = np.arctan2(
                np.dot(n1, np.cross(n2, n3)),
                1 + np.dot(n1, n2) + np.dot(n2, n3) + np.dot(n3, n1)
            )
            linking += omega
    
    return linking / (4 * math.pi)


# =============================================================================
# TEST CLASSES
# =============================================================================

class CrossingNumberProbe(Test):
    """
    PROBING: Count self-crossings of the trajectory.
    """
    name = "Crossing Number Analysis"
    question = (
        "How many times does the trajectory cross itself when projected to 2D? "
        "High crossing number indicates a complex, potentially knotted path. "
        "Low crossing number means simple, unknotted topology."
    )
    reference = "Crossing number, knot invariants"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We project the 3D trajectory to 2D and count segment crossings. "
        "This is an upper bound on knot complexity. The minimum crossing number "
        "over all projections classifies the knot type."
    )

    def derivation(self):
        return (
            Derivation()
            .step("CROSSING NUMBER:")
            .step("Project 3D curve to 2D plane.")
            .step("Count intersections of non-adjacent segments.")
            .step("KNOT CLASSIFICATION:")
            .step("  Unknot: minimum crossing = 0")
            .step("  Trefoil: minimum crossing = 3")
            .step("  Figure-8: minimum crossing = 4")
            .step("Higher crossing number means more complex topology.")
            .conclude("Crossing number measures topological complexity.")
        )

    def model(self):
        n_steps = 500  # Shorter for crossing computation
        history = get_vertex_history(n_steps)
        
        # Compute crossings in different projections
        cross_z = compute_crossing_number(history, 'z')
        cross_y = compute_crossing_number(history, 'y')
        cross_x = compute_crossing_number(history, 'x')
        
        min_crossing = min(cross_z, cross_y, cross_x)
        avg_crossing = (cross_z + cross_y + cross_x) / 3
        
        # Crossings per step
        crossing_rate = avg_crossing / n_steps
        
        return (
            Model()
            .add("Crossings (z projection)", cross_z)
            .add("Crossings (y projection)", cross_y)
            .add("Crossings (x projection)", cross_x)
            .add("Minimum crossing", min_crossing)
            .add("Crossing rate (per step)", crossing_rate)
        )

    def observations(self):
        # NULL: Some crossings but low rate
        return (
            Observed()
            .add("Crossings (z projection)", 50)
            .add("Crossings (y projection)", 50)
            .add("Crossings (x projection)", 50)
            .add("Minimum crossing", 30)
            .add("Crossing rate (per step)", 0.1)
        )


class WritheProbe(Test):
    """
    PROBING: Measure the writhe of the trajectory.
    """
    name = "Writhe (Self-Linking) Analysis"
    question = (
        "How much does the trajectory coil and twist? Writhe measures the "
        "signed total of self-crossings, capturing the handedness of coiling. "
        "High |writhe| indicates helical structure."
    )
    reference = "Writhe, self-linking number"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: Writhe is computed from the triple scalar product along "
        "the trajectory, measuring local twist. Unlike crossing number, "
        "writhe is signed, so it detects chiral coiling."
    )

    def derivation(self):
        return (
            Derivation()
            .step("WRITHE:")
            .step("Sum of signed self-crossings.")
            .equation("Wr = sum (v1 . (v2 x v3)) / normalization")
            .step("INTERPRETATION:")
            .step("  Wr > 0: right-handed coiling")
            .step("  Wr < 0: left-handed coiling")
            .step("  Wr = 0: no net coiling")
            .step("|Wr| ~ number of helical turns")
            .conclude("Writhe measures coiling/twist of trajectory.")
        )

    def model(self):
        n_steps = 2000
        history = get_vertex_history(n_steps)
        
        # Compute writhe
        writhe = compute_writhe(history)
        
        # Writhe magnitude and sign
        writhe_magnitude = abs(writhe)
        writhe_sign = 1 if writhe > 0 else (-1 if writhe < 0 else 0)
        
        # Writhe per step (coiling rate)
        coiling_rate = writhe / n_steps
        
        # Is there significant coiling?
        is_coiled = writhe_magnitude > 0.5
        
        return (
            Model()
            .add("Total writhe", writhe)
            .add("Writhe magnitude", writhe_magnitude)
            .add("Writhe sign", writhe_sign)
            .add("Coiling rate (per step)", coiling_rate)
            .add("Is significantly coiled", 1.0 if is_coiled else 0.0)
        )

    def observations(self):
        # NULL: Small random writhe
        return (
            Observed()
            .add("Total writhe", 0.0)
            .add("Writhe magnitude", 0.5)
            .add("Writhe sign", 0)
            .add("Coiling rate (per step)", 0.0)
            .add("Is significantly coiled", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    CrossingNumberProbe,
    WritheProbe,
]


def run_all():
    """Run all knot invariants probing tests."""
    summary = (
        "KNOT INVARIANTS PROBING\n\n"
        "These probes measure topological complexity.\n"
        "Crossing number: self-intersections in projection\n"
        "Writhe: signed coiling/twist measure\n\n"
        "We are DISCOVERING trajectory topology."
    )
    return run_tests("Knot Invariants Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
