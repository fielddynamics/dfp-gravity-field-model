"""
Effective Temperature Probing
=============================

PROBING QUESTION: Does the field have an effective temperature?

In statistical mechanics, temperature relates to energy fluctuations.
For black holes, surface gravity gives the Hawking temperature.
We probe if the field has a well-defined temperature.

MATHEMATICAL FOUNDATION:
- Boltzmann: P(E) ~ exp(-E/kT)
- Fluctuation-dissipation: T ~ <delta_E^2> / (2 * C)
- Equipartition: <E> = (d/2) * kT per degree of freedom

NULL HYPOTHESIS: No well-defined temperature
DISCOVERY: Boltzmann distribution would indicate thermalization

Reference: Statistical mechanics, Hawking temperature
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


def compute_vertex_energies() -> Dict[int, float]:
    """
    Assign energy to each vertex based on distance from origin.
    
    Farther vertices have higher potential energy.
    """
    energies = {}
    for v in range(8):
        r = get_vertex_coordinates(v)
        energies[v] = np.linalg.norm(r)  # Potential energy ~ radius
    return energies


def compute_kinetic_energies(history: List[int]) -> List[float]:
    """
    Compute kinetic energy for each transition.
    
    KE = |v|^2 / 2 where v = dr/dt
    """
    energies = []
    for i in range(len(history) - 1):
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i + 1])
        v = r2 - r1
        ke = np.dot(v, v) / 2
        energies.append(ke)
    return energies


def fit_boltzmann_distribution(energies: List[float]) -> Dict:
    """
    Fit Boltzmann distribution: P(E) ~ exp(-E/kT)
    
    Returns effective temperature.
    """
    energies = np.array(energies)
    energies = energies[energies > 0]  # Filter zeros
    
    if len(energies) < 10:
        return {'temperature': 0, 'fit_quality': 0}
    
    # Bin energies
    hist, bin_edges = np.histogram(energies, bins=20, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Fit log(P) = -E/kT + const
    valid = hist > 0.001
    if np.sum(valid) < 5:
        return {'temperature': 0, 'fit_quality': 0}
    
    log_p = np.log(hist[valid])
    E = bin_centers[valid]
    
    # Linear fit
    slope, intercept = np.polyfit(E, log_p, 1)
    
    # Temperature = -1/slope
    if slope < 0:
        temperature = -1 / slope
    else:
        temperature = float('inf')
    
    # Fit quality (R^2)
    predicted = slope * E + intercept
    ss_res = np.sum((log_p - predicted) ** 2)
    ss_tot = np.sum((log_p - np.mean(log_p)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    
    return {
        'temperature': temperature,
        'fit_quality': r_squared,
        'slope': slope,
    }


def compute_temperature_from_fluctuations(history: List[int]) -> float:
    """
    Compute temperature from energy fluctuations.
    
    Using fluctuation-dissipation: T ~ Var(E) / <E>
    """
    # Total energies in windows
    window = 50
    energies = []
    vertex_E = compute_vertex_energies()
    
    for i in range(len(history) - window):
        segment = history[i:i+window]
        E = sum(vertex_E[v] for v in segment) / window
        energies.append(E)
    
    if not energies:
        return 0
    
    mean_E = np.mean(energies)
    var_E = np.var(energies)
    
    # Temperature ~ Var(E) / <E>
    if mean_E > 0:
        T = var_E / mean_E
    else:
        T = 0
    
    return T


# =============================================================================
# TEST CLASSES
# =============================================================================

class BoltzmannDistributionProbe(Test):
    """
    PROBING: Does the energy distribution follow Boltzmann statistics?
    """
    name = "Boltzmann Distribution Test"
    question = (
        "Does the distribution of energies follow P(E) ~ exp(-E/kT)? "
        "A good Boltzmann fit would indicate the field has thermalized "
        "to a well-defined temperature."
    )
    reference = "Boltzmann distribution, thermalization"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We histogram kinetic energies and fit to exponential. "
        "Good fit (R^2 > 0.8) indicates thermal equilibrium. Poor fit "
        "suggests non-equilibrium or non-thermal dynamics."
    )

    def derivation(self):
        return (
            Derivation()
            .step("BOLTZMANN DISTRIBUTION:")
            .equation("P(E) = (1/Z) * exp(-E/kT)")
            .step("where Z is partition function, T is temperature")
            .step("LOG FORM:")
            .equation("log(P) = -E/kT + const")
            .step("Linear in E with slope -1/kT")
            .step("FITTING:")
            .step("Histogram energies, fit log(P) vs E")
            .step("Extract T from slope")
            .conclude("Boltzmann fit tests for thermalization.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute kinetic energies
        ke_list = compute_kinetic_energies(history)
        
        # Fit Boltzmann
        fit = fit_boltzmann_distribution(ke_list)
        
        # Basic energy statistics
        mean_ke = np.mean(ke_list)
        std_ke = np.std(ke_list)
        
        return (
            Model()
            .add("Mean kinetic energy", mean_ke)
            .add("Std of kinetic energy", std_ke)
            .add("Effective temperature", fit['temperature'])
            .add("Boltzmann fit R^2", fit['fit_quality'])
            .add("Is thermalized (R^2 > 0.7)", 1.0 if fit['fit_quality'] > 0.7 else 0.0)
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
            .add("Mean kinetic energy", 3.00254, abs_tol=0.084)  # random range [2.9424, 3.0752]
            .add("Std of kinetic energy", 1.73352, abs_tol=0.063)  # random range [1.69139, 1.78796]
            .add("Effective temperature", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Boltzmann fit R^2", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Is thermalized (R^2 > 0.7)", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class FluctuationTemperatureProbe(Test):
    """
    PROBING: Compute temperature from energy fluctuations.
    """
    name = "Fluctuation-Dissipation Temperature"
    question = (
        "What temperature does the fluctuation-dissipation theorem give? "
        "T ~ Var(E) / <E> relates fluctuations to temperature. Consistent "
        "temperature from different methods indicates true thermalization."
    )
    reference = "Fluctuation-dissipation theorem"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We compute temperature from energy variance. This should "
        "agree with the Boltzmann fit if the system is truly thermal. "
        "Disagreement indicates non-equilibrium dynamics."
    )

    def derivation(self):
        return (
            Derivation()
            .step("FLUCTUATION-DISSIPATION:")
            .equation("Var(E) = kT^2 * C")
            .step("where C is heat capacity")
            .step("For ideal gas: C ~ <E>")
            .step("TEMPERATURE ESTIMATE:")
            .equation("T ~ Var(E) / <E>")
            .step("CONSISTENCY CHECK:")
            .step("Compare to Boltzmann-derived temperature.")
            .step("Agreement indicates true thermalization.")
            .conclude("Fluctuations give independent temperature estimate.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Temperature from fluctuations
        T_fluct = compute_temperature_from_fluctuations(history)
        
        # Temperature from Boltzmann fit
        ke_list = compute_kinetic_energies(history)
        fit = fit_boltzmann_distribution(ke_list)
        T_boltz = fit['temperature']
        
        # Consistency
        if T_boltz > 0 and T_fluct > 0:
            T_ratio = T_fluct / T_boltz
        else:
            T_ratio = 0
        
        return (
            Model()
            .add("T (fluctuation method)", T_fluct)
            .add("T (Boltzmann method)", T_boltz)
            .add("T ratio (fluct/Boltz)", T_ratio)
            .add("Are consistent (ratio ~ 1)", 1.0 if 0.5 < T_ratio < 2.0 else 0.0)
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
            .add("T (fluctuation method)", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("T (Boltzmann method)", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("T ratio (fluct/Boltz)", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Are consistent (ratio ~ 1)", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BoltzmannDistributionProbe,
    FluctuationTemperatureProbe,
]


def run_all():
    """Run all effective temperature probing tests."""
    summary = (
        "EFFECTIVE TEMPERATURE PROBING\n\n"
        "These probes test for thermodynamic temperature.\n"
        "Boltzmann: P(E) ~ exp(-E/kT)?\n"
        "Fluctuations: T ~ Var(E)/<E>?\n\n"
        "We are DISCOVERING if the field is thermal."
    )
    return run_tests("Effective Temperature Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
