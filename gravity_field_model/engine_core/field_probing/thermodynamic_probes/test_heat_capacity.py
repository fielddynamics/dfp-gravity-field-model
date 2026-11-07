"""
Heat Capacity Probing
=====================

PROBING QUESTION: What is the heat capacity of the field?

Heat capacity measures how much energy is needed to change temperature.
Anomalies in heat capacity can indicate phase transitions.

MATHEMATICAL FOUNDATION:
- Heat capacity: C = dE/dT = Var(E) / (kT^2)
- Peak in C indicates phase transition
- Specific heat exponent characterizes universality class

NULL HYPOTHESIS: Constant heat capacity (no phase transition)
DISCOVERY: Peak would indicate critical point

Reference: Heat capacity, phase transitions
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


def compute_energies(history: List[int]) -> List[float]:
    """
    Compute energy for each step (kinetic + potential).
    """
    energies = []
    
    for i in range(len(history) - 1):
        # Kinetic energy
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i + 1])
        v = r2 - r1
        KE = np.dot(v, v) / 2
        
        # Potential energy (distance from origin)
        PE = np.linalg.norm(r1)
        
        energies.append(KE + PE)
    
    return energies


def compute_heat_capacity_fluctuation(energies: List[float], temperature: float = 1.0) -> float:
    """
    Compute heat capacity from energy fluctuations.
    
    C = Var(E) / (kT^2)
    """
    var_E = np.var(energies)
    return var_E / (temperature ** 2)


def compute_heat_capacity_vs_scale(history: List[int], scales: List[int]) -> Dict:
    """
    Compute effective heat capacity at different scales (window sizes).
    
    Scale dependence can reveal critical behavior.
    """
    capacities = []
    
    for scale in scales:
        # Coarse-grain energy at this scale
        n_windows = len(history) // scale
        window_energies = []
        
        for i in range(n_windows):
            segment = history[i*scale:(i+1)*scale]
            segment_E = compute_energies(segment)
            if segment_E:
                window_energies.append(np.mean(segment_E))
        
        if len(window_energies) > 1:
            C = compute_heat_capacity_fluctuation(window_energies)
            capacities.append(C)
        else:
            capacities.append(0)
    
    return {
        'scales': scales,
        'capacities': capacities,
    }


def test_for_phase_transition(capacities: List[float], scales: List[int]) -> Dict:
    """
    Test for phase transition signature (peak in heat capacity).
    """
    if not capacities:
        return {'has_peak': False, 'peak_scale': 0, 'peak_height': 0}
    
    max_C = max(capacities)
    max_idx = capacities.index(max_C)
    peak_scale = scales[max_idx]
    
    # Is it a significant peak?
    mean_C = np.mean(capacities)
    is_peak = max_C > 2 * mean_C and 0 < max_idx < len(capacities) - 1
    
    return {
        'has_peak': is_peak,
        'peak_scale': peak_scale,
        'peak_height': max_C,
        'mean_capacity': mean_C,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class HeatCapacityProbe(Test):
    """
    PROBING: Measure the heat capacity of the field.
    """
    name = "Heat Capacity Measurement"
    question = (
        "What is the heat capacity of the field? Heat capacity C = Var(E)/T^2 "
        "measures energy fluctuations. Large C means the system can absorb "
        "significant energy without temperature change."
    )
    reference = "Heat capacity, statistical mechanics"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We compute heat capacity from energy fluctuations. "
        "This gives insight into the thermodynamic nature of the field: "
        "how stiff or soft it is energetically."
    )

    def derivation(self):
        return (
            Derivation()
            .step("HEAT CAPACITY:")
            .equation("C = dE/dT = Var(E) / (kT^2)")
            .step("From fluctuation-dissipation theorem")
            .step("INTERPRETATION:")
            .step("  Large C: system can store much energy")
            .step("  Small C: energy changes cause large T changes")
            .step("FOR IDEAL GAS: C ~ N (extensive)")
            .step("Per degree of freedom: C/N ~ constant")
            .conclude("Heat capacity characterizes energy response.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute energies
        energies = compute_energies(history)
        
        # Heat capacity
        C = compute_heat_capacity_fluctuation(energies, temperature=1.0)
        
        # Energy statistics
        mean_E = np.mean(energies)
        var_E = np.var(energies)
        
        # Specific heat (per vertex visit)
        c_specific = C / len(energies)
        
        return (
            Model()
            .add("Mean energy", mean_E)
            .add("Variance of energy", var_E)
            .add("Heat capacity C", C)
            .add("Specific heat (per step)", c_specific)
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
            .add("Mean energy", 4.73459, abs_tol=0.084)  # random range [4.67445, 4.80725]
            .add("Variance of energy", 3.00534, abs_tol=0.23)  # random range [2.8608, 3.1968]
            .add("Heat capacity C", 3.00534, abs_tol=0.23)  # random range [2.8608, 3.1968]
            .add("Specific heat (per step)", 0.000601068, abs_tol=4.5e-05)  # random range [0.000572159, 0.00063936]
        )

class PhaseTransitionProbe(Test):
    """
    PROBING: Look for phase transition signatures in heat capacity.
    """
    name = "Phase Transition Search"
    question = (
        "Is there a peak in heat capacity at some scale? A sharp peak indicates "
        "a phase transition. We scan different coarse-graining scales to "
        "look for critical behavior."
    )
    reference = "Phase transitions, critical phenomena"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: Phase transitions show up as peaks in heat capacity. "
        "We compute C at different scales (window sizes) and look for "
        "peaks that would indicate critical behavior."
    )

    def derivation(self):
        return (
            Derivation()
            .step("PHASE TRANSITION SIGNATURE:")
            .step("Heat capacity diverges or peaks at critical point.")
            .equation("C ~ |T - T_c|^(-alpha)")
            .step("alpha is the specific heat exponent")
            .step("FINITE SIZE SCALING:")
            .step("In finite systems, peak occurs at some scale.")
            .step("Peak height and position depend on system size.")
            .step("TEST: Scan scales, look for peak in C(scale)")
            .conclude("Peak in C indicates phase transition.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute heat capacity at different scales
        scales = [10, 20, 50, 100, 200, 500]
        result = compute_heat_capacity_vs_scale(history, scales)
        
        # Test for phase transition
        transition = test_for_phase_transition(result['capacities'], scales)
        
        # Scale dependence
        if len(result['capacities']) > 3:
            # Fit C ~ scale^alpha
            log_scale = np.log(scales[:len(result['capacities'])])
            log_C = np.log(np.array(result['capacities']) + 0.001)
            alpha, _ = np.polyfit(log_scale, log_C, 1)
        else:
            alpha = 0
        
        return (
            Model()
            .add("C at scale 10", result['capacities'][0] if result['capacities'] else 0)
            .add("C at scale 100", result['capacities'][3] if len(result['capacities']) > 3 else 0)
            .add("Has peak", 1.0 if transition['has_peak'] else 0.0)
            .add("Peak scale", transition['peak_scale'])
            .add("Scaling exponent alpha", alpha)
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
            .add("C at scale 10", 0.333161, abs_tol=0.073)  # random range [0.277511, 0.396512]
            .add("C at scale 100", 0.0287567, abs_tol=0.022)  # random range [0.0155354, 0.0471398]
            .add("Has peak", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Peak scale", 10, abs_tol=1e-08)  # same for all 150 random sequences
            .add("Scaling exponent alpha", -1.02962, abs_tol=0.3)  # random range [-1.22653, -0.777179]
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    HeatCapacityProbe,
    PhaseTransitionProbe,
]


def run_all():
    """Run all heat capacity probing tests."""
    summary = (
        "HEAT CAPACITY PROBING\n\n"
        "These probes measure thermodynamic heat capacity.\n"
        "Heat capacity: C = Var(E)/T^2\n"
        "Phase transition: peak in C at critical point\n\n"
        "We are DISCOVERING the field's thermal response."
    )
    return run_tests("Heat Capacity Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
