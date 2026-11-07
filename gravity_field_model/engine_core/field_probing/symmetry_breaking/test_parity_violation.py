"""
Parity Violation Probing
========================

PROBING QUESTION: Does the field prefer left-handed or right-handed rotations?

Parity (P) transforms r -> -r. A parity-violating system distinguishes
between clockwise and counterclockwise motions.

MATHEMATICAL FOUNDATION:
- Parity: P: (x,y,z) -> (-x,-y,-z)
- Handedness: sign of cross product v1 x v2
- P-violation: preference for one handedness

NULL HYPOTHESIS: Parity symmetric (no handedness preference)
DISCOVERY: Handedness preference would indicate P-violation

Reference: Parity violation, Wu experiment, weak interaction
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


def compute_angular_momentum(r1: np.ndarray, r2: np.ndarray, r3: np.ndarray) -> np.ndarray:
    """
    Compute angular momentum-like vector for three consecutive positions.
    
    L = (r2 - r1) x (r3 - r2)
    
    Sign of L.z indicates handedness (CW vs CCW viewed from above).
    """
    v1 = r2 - r1
    v2 = r3 - r2
    return np.cross(v1, v2)


def compute_handedness_sequence(history: List[int]) -> List[int]:
    """
    Compute handedness (+1 or -1) for each triple of consecutive vertices.
    
    Uses sign of z-component of angular momentum.
    """
    handedness = []
    
    for i in range(len(history) - 2):
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i+1])
        r3 = get_vertex_coordinates(history[i+2])
        
        L = compute_angular_momentum(r1, r2, r3)
        
        # Use sign of L.z (or magnitude if near zero)
        if np.linalg.norm(L) < 1e-10:
            handedness.append(0)  # Collinear
        else:
            handedness.append(1 if L[2] > 0 else -1)
    
    return handedness


def compute_helicity(history: List[int]) -> List[float]:
    """
    Compute helicity: correlation between velocity and angular momentum.
    
    h = v . L / (|v| |L|)
    
    Helicity is a pseudoscalar (changes sign under parity).
    """
    helicities = []
    
    for i in range(len(history) - 2):
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i+1])
        r3 = get_vertex_coordinates(history[i+2])
        
        v = (r3 - r1) / 2  # Average velocity
        L = compute_angular_momentum(r1, r2, r3)
        
        v_norm = np.linalg.norm(v)
        L_norm = np.linalg.norm(L)
        
        if v_norm > 1e-10 and L_norm > 1e-10:
            h = np.dot(v, L) / (v_norm * L_norm)
            helicities.append(h)
    
    return helicities


def test_rotation_direction_bias(history: List[int]) -> Dict:
    """
    Test for bias in rotation direction.
    
    Count left-handed vs right-handed turns.
    """
    handedness = compute_handedness_sequence(history)
    
    # Remove collinear cases
    nonzero = [h for h in handedness if h != 0]
    
    if len(nonzero) == 0:
        return {'left': 0, 'right': 0, 'bias': 0, 'total': 0}
    
    n_left = sum(1 for h in nonzero if h > 0)  # Positive = counterclockwise = left
    n_right = sum(1 for h in nonzero if h < 0)  # Negative = clockwise = right
    
    bias = (n_left - n_right) / len(nonzero)
    
    return {
        'left': n_left,
        'right': n_right,
        'bias': bias,
        'total': len(nonzero),
        'left_fraction': n_left / len(nonzero),
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class ParityViolationProbe(Test):
    """
    PROBING: Test for parity (handedness) violation.
    """
    name = "Parity Violation (Handedness) Test"
    question = (
        "Does the traversal prefer left-handed or right-handed rotations? "
        "Parity symmetry would mean equal preference for both. Nature's weak "
        "force violates parity. Does the field dynamics also?"
    )
    reference = "Parity violation, chirality, Wu experiment"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We count left-handed vs right-handed turns in the trajectory. "
        "For each triple of vertices, we compute the cross product to determine "
        "rotation direction. A significant bias would indicate P-violation."
    )

    def derivation(self):
        return (
            Derivation()
            .step("PARITY (HANDEDNESS):")
            .step("For three consecutive positions r1, r2, r3:")
            .equation("L = (r2 - r1) x (r3 - r2)")
            .step("Sign of L.z indicates rotation direction:")
            .step("  L.z > 0: counterclockwise (left-handed)")
            .step("  L.z < 0: clockwise (right-handed)")
            .step("P-VIOLATION:")
            .equation("Bias = (N_left - N_right) / N_total")
            .step("Bias = 0: parity symmetric")
            .step("Bias != 0: parity violating")
            .conclude("Rotation bias measures parity violation.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Test rotation direction bias
        rotation = test_rotation_direction_bias(history)
        
        # Statistical significance
        n = rotation['total']
        if n > 0:
            expected_std = 0.5 / math.sqrt(n)  # For 50/50 split
            z_score = rotation['bias'] / expected_std if expected_std > 0 else 0
        else:
            z_score = 0
        
        return (
            Model()
            .add("Left-handed turns", rotation['left'])
            .add("Right-handed turns", rotation['right'])
            .add("Handedness bias", rotation['bias'])
            .add("Left fraction", rotation['left_fraction'])
            .add("Z-score", z_score)
            .add("Is P-violating", 1.0 if abs(z_score) > 2 else 0.0)
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
            .add("Left-handed turns", 1880.06, abs_tol=200)  # random range [1764, 2048]
            .add("Right-handed turns", 4686.52, abs_tol=200)  # random range [4513, 4852]
            .add("Handedness bias", -0.427374, abs_tol=0.05)  # random range [-0.460715, -0.38443]
            .add("Left fraction", 0.286313, abs_tol=0.025)  # random range [0.269642, 0.307785]
            .add("Z-score", -69.2642, abs_tol=7.6)  # random range [-74.5277, -62.7001]
            .add("Is P-violating", 1, abs_tol=1e-09)  # same for all 150 random sequences
        )

class HelicityDistributionProbe(Test):
    """
    PROBING: Analyze the distribution of helicity values.
    """
    name = "Helicity Distribution Analysis"
    question = (
        "Is the helicity (spin-momentum correlation) distributed symmetrically? "
        "Helicity is a pseudoscalar that changes sign under parity. Asymmetric "
        "distribution indicates P-violation."
    )
    reference = "Helicity, pseudoscalars, P-odd observables"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: Helicity h = v.L / (|v||L|) measures the correlation between "
        "velocity and rotation. For P-symmetric dynamics, the distribution "
        "should be symmetric around h=0. Skewness would indicate violation."
    )

    def derivation(self):
        return (
            Derivation()
            .step("HELICITY:")
            .equation("h = v . L / (|v| |L|)")
            .step("Range: [-1, 1]")
            .step("  h > 0: velocity aligned with angular momentum")
            .step("  h < 0: velocity anti-aligned")
            .step("P-SYMMETRY:")
            .step("Under parity: h -> -h")
            .step("P-symmetric distribution: symmetric around h=0")
            .step("P-violation: <h> != 0 or skewed distribution")
            .conclude("Helicity distribution probes parity symmetry.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute helicities
        helicities = compute_helicity(history)
        
        if len(helicities) == 0:
            return Model().add("No valid helicities", 0)
        
        h_array = np.array(helicities)
        
        # Distribution statistics
        mean_h = np.mean(h_array)
        std_h = np.std(h_array)
        
        # Skewness
        if std_h > 0:
            skewness = np.mean(((h_array - mean_h) / std_h) ** 3)
        else:
            skewness = 0
        
        # Fraction positive vs negative
        frac_pos = np.mean(h_array > 0)
        
        # t-test for mean != 0
        n = len(h_array)
        t_stat = mean_h / (std_h / math.sqrt(n)) if std_h > 0 else 0
        
        return (
            Model()
            .add("Mean helicity", mean_h)
            .add("Std of helicity", std_h)
            .add("Helicity skewness", skewness)
            .add("Fraction positive", frac_pos)
            .add("t-statistic", t_stat)
            .add("Is P-asymmetric", 1.0 if abs(t_stat) > 2 else 0.0)
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
            .add("Mean helicity", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Std of helicity", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Helicity skewness", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Fraction positive", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("t-statistic", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Is P-asymmetric", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ParityViolationProbe,
    HelicityDistributionProbe,
]


def run_all():
    """Run all parity violation probing tests."""
    summary = (
        "PARITY VIOLATION PROBING\n\n"
        "These probes test for handedness preference.\n"
        "Handedness: left vs right rotation\n"
        "Helicity: spin-momentum correlation\n\n"
        "We are DISCOVERING if parity is violated."
    )
    return run_tests("Parity Violation Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
