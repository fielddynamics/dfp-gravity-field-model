"""
Free Energy Landscape Probing
=============================

PROBING QUESTION: What is the free energy landscape of the field?

Free energy F = E - TS combines energy and entropy.
Minima of F are stable equilibria. Barriers determine transition rates.

MATHEMATICAL FOUNDATION:
- Helmholtz free energy: F = E - TS
- Equilibrium: dF/dx = 0
- Stability: d^2F/dx^2 > 0

NULL HYPOTHESIS: Flat landscape (no preferred states)
DISCOVERY: Structured landscape would reveal field organization

Reference: Free energy, Landau theory, landscape theory
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


def compute_state_energy(state: int) -> float:
    """
    Compute energy of a state (vertex or chamber).
    
    Using distance from origin as potential.
    """
    r = get_vertex_coordinates(state)
    return np.linalg.norm(r)


def compute_effective_free_energy(history: List[int], temperature: float = 1.0) -> Dict[int, float]:
    """
    Compute effective free energy for each vertex from occupation statistics.
    
    F_v = -T * log(P_v) (up to constant)
    
    More visited states have lower free energy.
    """
    counts = Counter(history)
    n = len(history)
    
    free_energies = {}
    for v in range(8):
        p = counts.get(v, 1) / n  # Add 1 to avoid log(0)
        free_energies[v] = -temperature * math.log(p)
    
    # Normalize to mean = 0
    mean_F = np.mean(list(free_energies.values()))
    for v in free_energies:
        free_energies[v] -= mean_F
    
    return free_energies


def compute_chamber_free_energy(history: List[int], temperature: float = 1.0) -> Dict:
    """
    Compute free energy for each chamber (TetA vs TetB).
    """
    n_a = sum(1 for v in history if v in TET_A)
    n_b = len(history) - n_a
    n = len(history)
    
    p_a = n_a / n
    p_b = n_b / n
    
    # Free energy
    F_a = -temperature * math.log(p_a) if p_a > 0 else float('inf')
    F_b = -temperature * math.log(p_b) if p_b > 0 else float('inf')
    
    # Barrier from transition rates
    trans_a_to_b = sum(1 for i in range(len(history)-1) 
                      if history[i] in TET_A and history[i+1] in TET_B)
    trans_b_to_a = sum(1 for i in range(len(history)-1) 
                      if history[i] in TET_B and history[i+1] in TET_A)
    
    # Detailed balance: k_ab/k_ba = exp(-(F_b - F_a)/T)
    # So barrier = -T * log(k)
    
    return {
        'F_TetA': F_a,
        'F_TetB': F_b,
        'delta_F': F_b - F_a,
        'transitions_A_to_B': trans_a_to_b,
        'transitions_B_to_A': trans_b_to_a,
    }


def analyze_landscape_structure(free_energies: Dict[int, float]) -> Dict:
    """
    Analyze the structure of the free energy landscape.
    """
    F_values = list(free_energies.values())
    
    # Find minima and maxima
    F_min = min(F_values)
    F_max = max(F_values)
    F_range = F_max - F_min
    
    # Identify minima (vertices with F within 10% of minimum)
    threshold = F_min + 0.1 * F_range if F_range > 0 else F_min + 0.1
    minima = [v for v, F in free_energies.items() if F < threshold]
    
    # Count minima in each chamber
    minima_A = len([v for v in minima if v in TET_A])
    minima_B = len([v for v in minima if v in TET_B])
    
    # Landscape roughness (variance of F)
    roughness = np.var(F_values)
    
    return {
        'F_min': F_min,
        'F_max': F_max,
        'F_range': F_range,
        'num_minima': len(minima),
        'minima_in_TetA': minima_A,
        'minima_in_TetB': minima_B,
        'roughness': roughness,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class FreeEnergyLandscapeProbe(Test):
    """
    PROBING: Map the free energy landscape.
    """
    name = "Free Energy Landscape Analysis"
    question = (
        "What is the structure of the free energy landscape? How many minima "
        "are there? Is the landscape rough (many barriers) or smooth (easy "
        "transitions)? Where are the stable states?"
    )
    reference = "Free energy landscapes, protein folding"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We compute effective free energy F_v = -T*log(P_v) for each "
        "vertex from its occupation probability. The landscape structure "
        "(minima, barriers, roughness) reveals the organization of the field."
    )

    def derivation(self):
        return (
            Derivation()
            .step("FREE ENERGY:")
            .equation("F = E - TS")
            .step("At equilibrium, P(state) ~ exp(-F/T)")
            .step("EFFECTIVE FREE ENERGY:")
            .equation("F_v = -T * log(P_v)")
            .step("Derived from occupation statistics")
            .step("LANDSCAPE PROPERTIES:")
            .step("  Minima: stable states")
            .step("  Barriers: transition obstacles")
            .step("  Roughness: variance of F")
            .conclude("Free energy landscape reveals field organization.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute free energies
        F = compute_effective_free_energy(history, temperature=1.0)
        
        # Analyze landscape
        landscape = analyze_landscape_structure(F)
        
        # TetA vs TetB free energies
        F_a_mean = np.mean([F[v] for v in TET_A])
        F_b_mean = np.mean([F[v] for v in TET_B])
        
        return (
            Model()
            .add("F range (max - min)", landscape['F_range'])
            .add("Number of minima", landscape['num_minima'])
            .add("Minima in TetA", landscape['minima_in_TetA'])
            .add("Minima in TetB", landscape['minima_in_TetB'])
            .add("Landscape roughness", landscape['roughness'])
            .add("Mean F(TetA) - F(TetB)", F_a_mean - F_b_mean)
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
            .add("F range (max - min)", 0.117407, abs_tol=0.11)  # random range [0.0397825, 0.206971]
            .add("Number of minima", 1.41333, abs_tol=3)  # random range [1, 4]
            .add("Minima in TetA", 0.773333, abs_tol=2.6)  # random range [0, 3]
            .add("Minima in TetB", 0.64, abs_tol=1.6)  # random range [0, 2]
            .add("Landscape roughness", 0.00149674, abs_tol=0.0031)  # random range [0.000192509, 0.00415809]
            .add("Mean F(TetA) - F(TetB)", -0.00146949, abs_tol=0.11)  # random range [-0.0899778, 0.0580045]
        )

class ChamberFreeEnergyProbe(Test):
    """
    PROBING: Compare free energies of TetA and TetB chambers.
    """
    name = "Chamber Free Energy Comparison"
    question = (
        "Is there a free energy difference between TetA and TetB? "
        "The ~1% TetB bias we observed should correspond to a small "
        "free energy difference favoring TetB."
    )
    reference = "Free energy difference, detailed balance"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We compute F_A and F_B from occupation probabilities. "
        "If TetB is slightly preferred, F_B < F_A. The free energy difference "
        "quantifies the thermodynamic bias."
    )

    def derivation(self):
        return (
            Derivation()
            .step("CHAMBER FREE ENERGY:")
            .equation("F_A = -T * log(P_A)")
            .equation("F_B = -T * log(P_B)")
            .step("BIAS:")
            .equation("delta_F = F_B - F_A = -T * log(P_B/P_A)")
            .step("If P_B > P_A, then delta_F < 0 (TetB favored)")
            .step("DETAILED BALANCE:")
            .equation("k_AB / k_BA = exp(-delta_F / T)")
            .step("Transition rates should satisfy this relation.")
            .conclude("Free energy difference explains chamber bias.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Chamber free energies
        chamber_F = compute_chamber_free_energy(history, temperature=1.0)
        
        # Check detailed balance
        if chamber_F['transitions_B_to_A'] > 0:
            rate_ratio = chamber_F['transitions_A_to_B'] / chamber_F['transitions_B_to_A']
        else:
            rate_ratio = 1.0
        
        # Expected from free energy
        expected_ratio = math.exp(-chamber_F['delta_F'])
        
        return (
            Model()
            .add("F(TetA)", chamber_F['F_TetA'])
            .add("F(TetB)", chamber_F['F_TetB'])
            .add("delta_F (B - A)", chamber_F['delta_F'])
            .add("Transition rate ratio", rate_ratio)
            .add("Expected ratio from F", expected_ratio)
            .add("TetB favored", 1.0 if chamber_F['delta_F'] < 0 else 0.0)
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
            .add("F(TetA)", 0.692473, abs_tol=0.05)  # random range [0.649139, 0.721747]
            .add("F(TetB)", 0.69403, abs_tol=0.052)  # random range [0.665343, 0.739182]
            .add("delta_F (B - A)", 0.00155782, abs_tol=0.11)  # random range [-0.0564037, 0.0900428]
            .add("Transition rate ratio", 0.999569, abs_tol=0.0005)  # random range [0.999173, 1]
            .add("Expected ratio from F", 0.998858, abs_tol=0.098)  # random range [0.913892, 1.05802]
            .add("TetB favored", 0.46, abs_tol=0.63)  # random range [0, 1]
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    FreeEnergyLandscapeProbe,
    ChamberFreeEnergyProbe,
]


def run_all():
    """Run all free energy landscape probing tests."""
    summary = (
        "FREE ENERGY LANDSCAPE PROBING\n\n"
        "These probes map the thermodynamic landscape.\n"
        "Landscape structure: minima, barriers, roughness\n"
        "Chamber comparison: F(TetA) vs F(TetB)\n\n"
        "We are DISCOVERING the field's energy structure."
    )
    return run_tests("Free Energy Landscape Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
