"""
Winding Number Probing
======================

PROBING QUESTION: Does the trajectory wind around the origin?

The winding number counts how many times a path wraps around a point.
For the Merkaba, this probes rotational dynamics around the Field Origin.

MATHEMATICAL FOUNDATION:
- Winding number: W = (1/2pi) * integral d(theta)
- Integer for closed paths
- Measures "net rotation" around origin

NULL HYPOTHESIS: Zero net winding (no preferred rotation)
DISCOVERY: Non-zero winding would indicate vortex-like dynamics

Reference: Winding number, topological invariants
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


def compute_angle_from_origin(r: np.ndarray, axis: str = 'z') -> float:
    """
    Compute angle of position vector projected onto plane perpendicular to axis.
    
    Returns angle in [-pi, pi].
    """
    if axis == 'z':
        x, y = r[0], r[1]
    elif axis == 'y':
        x, y = r[0], r[2]
    else:  # axis == 'x'
        x, y = r[1], r[2]
    
    return math.atan2(y, x)


def compute_winding_number(history: List[int], axis: str = 'z') -> float:
    """
    Compute winding number of trajectory around origin.
    
    W = (total angle swept) / (2 * pi)
    """
    total_angle = 0.0
    
    for i in range(len(history) - 1):
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i + 1])
        
        theta1 = compute_angle_from_origin(r1, axis)
        theta2 = compute_angle_from_origin(r2, axis)
        
        # Angular difference, handling wraparound
        d_theta = theta2 - theta1
        
        # Normalize to [-pi, pi]
        while d_theta > math.pi:
            d_theta -= 2 * math.pi
        while d_theta < -math.pi:
            d_theta += 2 * math.pi
        
        total_angle += d_theta
    
    return total_angle / (2 * math.pi)


def compute_winding_rate(history: List[int], axis: str = 'z') -> float:
    """
    Compute average winding rate (windings per step).
    """
    winding = compute_winding_number(history, axis)
    return winding / len(history)


def compute_local_winding(history: List[int], window: int = 50, axis: str = 'z') -> np.ndarray:
    """
    Compute local winding number in sliding windows.
    """
    n_windows = len(history) - window + 1
    windings = []
    
    for i in range(n_windows):
        segment = history[i:i+window]
        w = compute_winding_number(segment, axis)
        windings.append(w)
    
    return np.array(windings)


def test_winding_direction_bias(history: List[int]) -> Dict:
    """
    Test for bias in winding direction (CW vs CCW).
    """
    # Compute winding around all three axes
    w_x = compute_winding_number(history, 'x')
    w_y = compute_winding_number(history, 'y')
    w_z = compute_winding_number(history, 'z')
    
    # Total winding magnitude
    total_winding = math.sqrt(w_x**2 + w_y**2 + w_z**2)
    
    # Dominant axis
    max_w = max(abs(w_x), abs(w_y), abs(w_z))
    if max_w == abs(w_x):
        dominant_axis = 'x'
    elif max_w == abs(w_y):
        dominant_axis = 'y'
    else:
        dominant_axis = 'z'
    
    return {
        'w_x': w_x,
        'w_y': w_y,
        'w_z': w_z,
        'total_winding': total_winding,
        'dominant_axis': dominant_axis,
        'is_rotating': total_winding > 1.0,  # More than one full rotation
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class WindingNumberProbe(Test):
    """
    PROBING: Does the trajectory wind around the origin?
    """
    name = "Winding Number Analysis"
    question = (
        "How many times does the trajectory wrap around the Field Origin? "
        "Non-zero winding would indicate vortex-like, rotational dynamics. "
        "The lemniscate model predicts circulation through the origin."
    )
    reference = "Winding number, vorticity"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We compute the winding number around all three principal "
        "axes. Significant winding would support the vortex model where the "
        "field circulates around the origin like in a figure-8 pattern."
    )

    def derivation(self):
        return (
            Derivation()
            .step("WINDING NUMBER:")
            .equation("W = (1/2pi) * integral d(theta)")
            .step("Where theta is the angle in the plane perpendicular to axis.")
            .step("INTERPRETATION:")
            .step("  W > 0: net counterclockwise rotation")
            .step("  W < 0: net clockwise rotation")
            .step("  W = 0: no net rotation")
            .step("For closed loop: W is integer")
            .step("For open trajectory: W can be fractional")
            .conclude("Winding number measures rotational topology.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute winding numbers
        winding = test_winding_direction_bias(history)
        
        # Winding rate
        rate_z = compute_winding_rate(history, 'z')
        
        # Local winding variability
        local_w = compute_local_winding(history, window=100, axis='z')
        winding_std = np.std(local_w)
        
        return (
            Model()
            .add("Winding around x-axis", winding['w_x'])
            .add("Winding around y-axis", winding['w_y'])
            .add("Winding around z-axis", winding['w_z'])
            .add("Total winding magnitude", winding['total_winding'])
            .add("Winding rate (per step)", rate_z)
            .add("Local winding variability", winding_std)
        )

    def observations(self):
        # NULL: No net winding (random)
        return (
            Observed()
            .add("Winding around x-axis", 0.0)
            .add("Winding around y-axis", 0.0)
            .add("Winding around z-axis", 0.0)
            .add("Total winding magnitude", 0.0)
            .add("Winding rate (per step)", 0.0)
            .add("Local winding variability", 0.5)
        )


class WindingDistributionProbe(Test):
    """
    PROBING: What is the distribution of local winding numbers?
    """
    name = "Local Winding Distribution"
    question = (
        "Are local winding numbers uniformly distributed (random rotation "
        "directions) or peaked (preferred rotation)? The distribution shape "
        "reveals the character of rotational dynamics."
    )
    reference = "Winding statistics, rotational bias"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We analyze the distribution of winding numbers computed "
        "in short windows. Symmetric distribution means no preferred rotation. "
        "Skewed distribution indicates rotational bias."
    )

    def derivation(self):
        return (
            Derivation()
            .step("LOCAL WINDING DISTRIBUTION:")
            .step("Compute winding in windows of size W.")
            .step("Analyze the distribution of these local windings.")
            .step("SYMMETRIC: mean = 0, no skewness")
            .step("BIASED: mean != 0 or skewed")
            .step("BIMODAL: two preferred rotation directions")
            .conclude("Winding distribution reveals rotational preferences.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute local windings
        local_w = compute_local_winding(history, window=50, axis='z')
        
        # Distribution statistics
        mean_w = np.mean(local_w)
        std_w = np.std(local_w)
        
        # Skewness
        if std_w > 0:
            skewness = np.mean(((local_w - mean_w) / std_w) ** 3)
        else:
            skewness = 0
        
        # Fraction positive vs negative
        frac_positive = np.mean(local_w > 0)
        
        # t-test for mean != 0
        n = len(local_w)
        t_stat = mean_w / (std_w / math.sqrt(n)) if std_w > 0 else 0
        
        return (
            Model()
            .add("Mean local winding", mean_w)
            .add("Std of local winding", std_w)
            .add("Skewness", skewness)
            .add("Fraction positive", frac_positive)
            .add("t-statistic", t_stat)
            .add("Has rotation bias", 1.0 if abs(t_stat) > 2 else 0.0)
        )

    def observations(self):
        # NULL: Symmetric winding distribution
        return (
            Observed()
            .add("Mean local winding", 0.0)
            .add("Std of local winding", 0.3)
            .add("Skewness", 0.0)
            .add("Fraction positive", 0.5)
            .add("t-statistic", 0.0)
            .add("Has rotation bias", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    WindingNumberProbe,
    WindingDistributionProbe,
]


def run_all():
    """Run all winding number probing tests."""
    summary = (
        "WINDING NUMBER PROBING\n\n"
        "These probes measure rotational topology.\n"
        "Winding number: how many times path wraps around origin\n"
        "Distribution: symmetry of rotation directions\n\n"
        "We are DISCOVERING rotational structure."
    )
    return run_tests("Winding Number Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
