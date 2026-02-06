"""
Information Speed Probing
=========================

PROBING QUESTION: How fast does information propagate through the field?

This probe measures the characteristic timescale for correlations
to spread from one vertex to another.

MATHEMATICAL FOUNDATION:
- Cross-correlation: C_{AB}(k) = E[A_t * B_{t+k}]
- Propagation time: lag k where C_{AB}(k) peaks
- Diffusion coefficient from mean-square displacement

NULL HYPOTHESIS: Instantaneous propagation (all vertices connected)
DISCOVERY: Finite speed would indicate locality

Reference: Diffusion theory, signal propagation
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


def compute_cross_correlation(seq_a: List[int], seq_b: List[int], max_lag: int = 20) -> np.ndarray:
    """
    Compute cross-correlation between two binary sequences.
    
    C(k) = E[A_t * B_{t+k}] / sqrt(Var(A) * Var(B))
    """
    a = np.array(seq_a, dtype=float)
    b = np.array(seq_b, dtype=float)
    
    n = min(len(a), len(b))
    a = a[:n]
    b = b[:n]
    
    mean_a, mean_b = np.mean(a), np.mean(b)
    std_a, std_b = np.std(a), np.std(b)
    
    if std_a == 0 or std_b == 0:
        return np.zeros(2 * max_lag + 1)
    
    corr = np.zeros(2 * max_lag + 1)
    for k in range(-max_lag, max_lag + 1):
        if k >= 0:
            c = np.mean((a[:n-k] - mean_a) * (b[k:] - mean_b))
        else:
            c = np.mean((a[-k:] - mean_a) * (b[:n+k] - mean_b))
        corr[k + max_lag] = c / (std_a * std_b)
    
    return corr


def compute_first_passage_time(history: List[int], source: int, target: int) -> List[int]:
    """
    Compute first passage times from source vertex to target vertex.
    
    First passage time = steps to reach target, starting from source.
    """
    fpt_list = []
    in_source = False
    steps_since_source = 0
    
    for v in history:
        if v == source:
            in_source = True
            steps_since_source = 0
        elif in_source:
            steps_since_source += 1
            if v == target:
                fpt_list.append(steps_since_source)
                in_source = False
    
    return fpt_list


def compute_mean_square_displacement(history: List[int], max_lag: int = 50) -> np.ndarray:
    """
    Compute mean square displacement as function of lag.
    
    MSD(k) = E[|r(t+k) - r(t)|^2]
    
    For diffusion: MSD ~ D * k (linear)
    For ballistic: MSD ~ k^2 (quadratic)
    """
    n = len(history)
    msd = np.zeros(max_lag + 1)
    
    for k in range(max_lag + 1):
        if k >= n:
            break
        displacements = []
        for t in range(n - k):
            r_t = get_vertex_coordinates(history[t])
            r_tk = get_vertex_coordinates(history[t + k])
            displacements.append(np.sum((r_tk - r_t) ** 2))
        msd[k] = np.mean(displacements)
    
    return msd


# =============================================================================
# TEST CLASSES
# =============================================================================

class PropagationTimeProbe(Test):
    """
    PROBING: Measure information propagation time between vertices.
    """
    name = "Information Propagation Time"
    question = (
        "How many steps does it take for 'influence' to propagate from one "
        "vertex to another? Is there a characteristic propagation speed, "
        "or is information transfer instantaneous?"
    )
    reference = "Signal propagation, cross-correlation analysis"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We measure first passage times between vertices to "
        "estimate propagation speed. Short times mean fast propagation "
        "(strongly connected). Long times mean slow propagation (locality). "
        "This is discovery about the field's connectivity structure."
    )

    def derivation(self):
        return (
            Derivation()
            .step("FIRST PASSAGE TIME:")
            .step("T_{A->B} = number of steps to reach B, starting from A")
            .step("Mean first passage time characterizes propagation speed.")
            .step("PROPAGATION SPEED:")
            .equation("v = distance(A,B) / mean(T_{A->B})")
            .step("For uniform random walk on graph:")
            .step("  Expected FPT depends on graph structure")
            .step("SHORT FPT: strongly connected, fast mixing")
            .step("LONG FPT: weak connections, slow mixing")
            .conclude("First passage time reveals propagation dynamics.")
        )

    def model(self):
        n_steps = 10000
        history = get_vertex_history(n_steps)
        
        # Compute first passage times for several vertex pairs
        # Same chamber pair
        fpt_same = compute_first_passage_time(history, 1, 2)  # Both in TetA
        # Cross chamber pair
        fpt_cross = compute_first_passage_time(history, 1, 6)  # 1 in TetA, 6 in TetB
        # Complementary pair
        fpt_comp = compute_first_passage_time(history, 1, 6)  # Complements
        
        mean_fpt_same = np.mean(fpt_same) if fpt_same else float('inf')
        mean_fpt_cross = np.mean(fpt_cross) if fpt_cross else float('inf')
        
        # Compare to geometric distance
        d_same = np.linalg.norm(get_vertex_coordinates(1) - get_vertex_coordinates(2))
        d_cross = np.linalg.norm(get_vertex_coordinates(1) - get_vertex_coordinates(6))
        
        # Effective speed
        speed_same = d_same / mean_fpt_same if mean_fpt_same > 0 else 0
        speed_cross = d_cross / mean_fpt_cross if mean_fpt_cross > 0 else 0
        
        return (
            Model()
            .add("Mean FPT (same chamber)", mean_fpt_same)
            .add("Mean FPT (cross chamber)", mean_fpt_cross)
            .add("FPT ratio (cross/same)", mean_fpt_cross / mean_fpt_same if mean_fpt_same > 0 else 1.0)
            .add("Effective speed (same)", speed_same)
            .add("Effective speed (cross)", speed_cross)
        )

    def observations(self):
        # NULL: Uniform random (FPT depends only on graph structure)
        # For 8-vertex complete graph, expected FPT ~ 7 steps
        return (
            Observed()
            .add("Mean FPT (same chamber)", 8.0)
            .add("Mean FPT (cross chamber)", 8.0)
            .add("FPT ratio (cross/same)", 1.0)
            .add("Effective speed (same)", 0.3)
            .add("Effective speed (cross)", 0.3)
        )


class DiffusionProbe(Test):
    """
    PROBING: Is the dynamics diffusive, ballistic, or anomalous?
    """
    name = "Diffusion Characterization"
    question = (
        "Does the trajectory spread diffusively (MSD ~ t) or ballistically "
        "(MSD ~ t^2)? Anomalous diffusion (MSD ~ t^alpha) would indicate "
        "complex dynamics."
    )
    reference = "Diffusion theory, anomalous diffusion"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: Mean square displacement reveals the nature of spreading. "
        "Normal diffusion: MSD ~ t. Ballistic: MSD ~ t^2. Subdiffusion: "
        "MSD ~ t^alpha with alpha < 1. This characterizes transport properties."
    )

    def derivation(self):
        return (
            Derivation()
            .step("MEAN SQUARE DISPLACEMENT:")
            .equation("MSD(t) = E[|r(t) - r(0)|^2]")
            .step("For different transport types:")
            .step("  Diffusive: MSD = 2*D*t (linear)")
            .step("  Ballistic: MSD = v^2 * t^2 (quadratic)")
            .step("  Anomalous: MSD = K * t^alpha")
            .step("DIFFUSION EXPONENT:")
            .equation("alpha = d(log MSD) / d(log t)")
            .step("  alpha = 1: normal diffusion")
            .step("  alpha > 1: superdiffusion")
            .step("  alpha < 1: subdiffusion")
            .conclude("MSD scaling reveals transport mechanism.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute MSD
        max_lag = min(100, n_steps // 10)
        msd = compute_mean_square_displacement(history, max_lag)
        
        # Fit power law: log(MSD) = alpha * log(t) + const
        valid_idx = np.where((msd > 0) & (np.arange(len(msd)) > 0))[0]
        if len(valid_idx) >= 5:
            log_t = np.log(valid_idx)
            log_msd = np.log(msd[valid_idx])
            alpha, intercept = np.polyfit(log_t, log_msd, 1)
            D_eff = np.exp(intercept) / 2  # Effective diffusion coefficient
        else:
            alpha = 1.0
            D_eff = 0.0
        
        # Characterize diffusion type
        if alpha > 1.5:
            diff_type = "superdiffusive"
        elif alpha < 0.5:
            diff_type = "subdiffusive"
        else:
            diff_type = "normal"
        
        return (
            Model()
            .add("MSD at t=10", msd[10] if len(msd) > 10 else 0)
            .add("MSD at t=50", msd[50] if len(msd) > 50 else 0)
            .add("Diffusion exponent alpha", alpha)
            .add("Effective diffusion coeff", D_eff)
            .add("Is normal diffusion", 1.0 if 0.8 < alpha < 1.2 else 0.0)
        )

    def observations(self):
        # NULL: Normal diffusion (alpha = 1)
        return (
            Observed()
            .add("MSD at t=10", 5.0)
            .add("MSD at t=50", 25.0)
            .add("Diffusion exponent alpha", 1.0)
            .add("Effective diffusion coeff", 0.5)
            .add("Is normal diffusion", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    PropagationTimeProbe,
    DiffusionProbe,
]


def run_all():
    """Run all information speed probing tests."""
    summary = (
        "INFORMATION SPEED PROBING\n\n"
        "These probes measure how fast information spreads.\n"
        "First passage time: steps to reach target from source\n"
        "Diffusion: MSD scaling reveals transport type\n\n"
        "We are DISCOVERING propagation dynamics."
    )
    return run_tests("Information Speed Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
