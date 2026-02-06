"""
Uncertainty Relations Probing
=============================

PROBING QUESTION: Are there trade-offs between position and momentum analogs?

Quantum mechanics has Heisenberg uncertainty: Delta_x * Delta_p >= hbar/2.
We test if similar trade-offs exist in the field dynamics.

MATHEMATICAL FOUNDATION:
- Position: vertex location
- Momentum: velocity (change in position)
- Uncertainty: variances of position and momentum
- Product of uncertainties has minimum value?

NULL HYPOTHESIS: No uncertainty trade-off (independent distributions)
DISCOVERY: Minimum uncertainty product would suggest quantum-like structure

Reference: Heisenberg uncertainty, Robertson-Schrodinger inequality
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


def compute_position_uncertainty(history: List[int], window: int) -> float:
    """
    Compute position uncertainty (variance in coordinates).
    """
    n_windows = len(history) - window + 1
    variances = []
    
    for i in range(n_windows):
        segment = history[i:i+window]
        coords = [get_vertex_coordinates(v) for v in segment]
        coords = np.array(coords)
        
        # Variance in each direction
        var_per_dim = np.var(coords, axis=0)
        total_var = np.sum(var_per_dim)
        variances.append(total_var)
    
    return np.mean(variances)


def compute_momentum_uncertainty(history: List[int], window: int) -> float:
    """
    Compute momentum uncertainty (variance in velocities).
    
    Velocity = r(t+1) - r(t)
    """
    n_windows = len(history) - window
    variances = []
    
    for i in range(n_windows):
        segment = history[i:i+window+1]
        
        # Compute velocities
        velocities = []
        for j in range(len(segment) - 1):
            r1 = get_vertex_coordinates(segment[j])
            r2 = get_vertex_coordinates(segment[j + 1])
            v = r2 - r1
            velocities.append(v)
        
        velocities = np.array(velocities)
        
        # Variance in velocities
        var_per_dim = np.var(velocities, axis=0)
        total_var = np.sum(var_per_dim)
        variances.append(total_var)
    
    return np.mean(variances)


def compute_uncertainty_product(history: List[int], windows: List[int]) -> Dict:
    """
    Compute position-momentum uncertainty product at different scales.
    """
    products = []
    pos_uncertainties = []
    mom_uncertainties = []
    
    for window in windows:
        delta_x = compute_position_uncertainty(history, window)
        delta_p = compute_momentum_uncertainty(history, window)
        
        pos_uncertainties.append(delta_x)
        mom_uncertainties.append(delta_p)
        products.append(delta_x * delta_p)
    
    return {
        'windows': windows,
        'position_uncertainties': pos_uncertainties,
        'momentum_uncertainties': mom_uncertainties,
        'products': products,
        'min_product': min(products),
    }


def compute_energy_time_uncertainty(history: List[int]) -> Dict:
    """
    Test energy-time uncertainty analog.
    
    Delta_E * Delta_t >= hbar/2
    
    Energy ~ kinetic energy = v^2
    Time ~ duration between events
    """
    # Compute kinetic energies
    energies = []
    for i in range(len(history) - 1):
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i + 1])
        v = np.linalg.norm(r2 - r1)
        E = v ** 2 / 2  # Kinetic energy
        energies.append(E)
    
    # Energy uncertainty
    delta_E = np.std(energies)
    mean_E = np.mean(energies)
    
    # Time between chamber crossings
    crossing_times = []
    last_chamber = 0 if history[0] in TET_A else 1
    last_crossing = 0
    
    for t, v in enumerate(history[1:], 1):
        chamber = 0 if v in TET_A else 1
        if chamber != last_chamber:
            crossing_times.append(t - last_crossing)
            last_crossing = t
            last_chamber = chamber
    
    if crossing_times:
        delta_t = np.std(crossing_times)
        mean_t = np.mean(crossing_times)
    else:
        delta_t = 0
        mean_t = 0
    
    # Uncertainty product
    et_product = delta_E * delta_t
    
    return {
        'delta_E': delta_E,
        'mean_E': mean_E,
        'delta_t': delta_t,
        'mean_t': mean_t,
        'product': et_product,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class PositionMomentumUncertaintyProbe(Test):
    """
    PROBING: Test for position-momentum uncertainty relation.
    """
    name = "Position-Momentum Uncertainty"
    question = (
        "Is there a minimum value for Delta_x * Delta_p? In quantum mechanics, "
        "this product has a minimum (hbar/2). We test if the field dynamics "
        "shows a similar trade-off between position and momentum uncertainties."
    )
    reference = "Heisenberg uncertainty principle"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We compute position variance (in 3D) and momentum/velocity "
        "variance, then their product. A consistent minimum value across "
        "different scales would suggest quantum-like uncertainty."
    )

    def derivation(self):
        return (
            Derivation()
            .step("HEISENBERG UNCERTAINTY:")
            .equation("Delta_x * Delta_p >= hbar/2")
            .step("CLASSICAL ANALOG:")
            .step("  Position: variance of vertex coordinates")
            .step("  Momentum: variance of velocities")
            .step("PRODUCT:")
            .equation("U = Var(x) * Var(v)")
            .step("If U has consistent minimum, suggests uncertainty relation.")
            .conclude("Test if position-momentum product has minimum.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute uncertainty at different scales
        windows = [10, 20, 50, 100]
        uncertainty = compute_uncertainty_product(history, windows)
        
        # Minimum product
        min_product = uncertainty['min_product']
        
        # Product at scale 20
        idx_20 = windows.index(20)
        product_20 = uncertainty['products'][idx_20]
        pos_20 = uncertainty['position_uncertainties'][idx_20]
        mom_20 = uncertainty['momentum_uncertainties'][idx_20]
        
        return (
            Model()
            .add("Delta_x (window=20)", pos_20)
            .add("Delta_p (window=20)", mom_20)
            .add("Product (window=20)", product_20)
            .add("Minimum product", min_product)
            .add("Product consistency", np.std(uncertainty['products']))
        )

    def observations(self):
        # NULL: Products vary with scale
        return (
            Observed()
            .add("Delta_x (window=20)", 1.0)
            .add("Delta_p (window=20)", 1.5)
            .add("Product (window=20)", 1.5)
            .add("Minimum product", 1.0)
            .add("Product consistency", 0.5)
        )


class EnergyTimeUncertaintyProbe(Test):
    """
    PROBING: Test for energy-time uncertainty relation.
    """
    name = "Energy-Time Uncertainty Analog"
    question = (
        "Is there a trade-off between energy uncertainty and timing? "
        "The quantum Delta_E * Delta_t >= hbar/2 suggests high energy "
        "fluctuations occur over short times. We test this classically."
    )
    reference = "Energy-time uncertainty"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We use kinetic energy (v^2) as energy proxy and time "
        "between chamber crossings as time scale. If their variances show "
        "a trade-off, it mimics quantum energy-time uncertainty."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ENERGY-TIME UNCERTAINTY:")
            .equation("Delta_E * Delta_t >= hbar/2")
            .step("CLASSICAL ANALOGS:")
            .step("  Energy: kinetic energy E = v^2/2")
            .step("  Time: intervals between chamber crossings")
            .step("PRODUCT:")
            .equation("U_ET = Var(E) * Var(t)")
            .step("Test if product has consistent minimum.")
            .conclude("Test energy-time uncertainty analog.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute energy-time uncertainty
        et = compute_energy_time_uncertainty(history)
        
        return (
            Model()
            .add("Delta_E (energy std)", et['delta_E'])
            .add("Mean energy", et['mean_E'])
            .add("Delta_t (crossing time std)", et['delta_t'])
            .add("Mean crossing time", et['mean_t'])
            .add("Product Delta_E * Delta_t", et['product'])
        )

    def observations(self):
        # NULL: Some variation
        return (
            Observed()
            .add("Delta_E (energy std)", 0.5)
            .add("Mean energy", 1.0)
            .add("Delta_t (crossing time std)", 2.0)
            .add("Mean crossing time", 4.0)
            .add("Product Delta_E * Delta_t", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    PositionMomentumUncertaintyProbe,
    EnergyTimeUncertaintyProbe,
]


def run_all():
    """Run all uncertainty relations probing tests."""
    summary = (
        "UNCERTAINTY RELATIONS PROBING\n\n"
        "These probes test for quantum-like uncertainty trade-offs.\n"
        "Position-momentum: Delta_x * Delta_p minimum?\n"
        "Energy-time: Delta_E * Delta_t minimum?\n\n"
        "We are DISCOVERING uncertainty-like bounds."
    )
    return run_tests("Uncertainty Relations Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
