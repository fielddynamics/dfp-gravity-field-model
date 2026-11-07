"""
Work Extraction Probing
=======================

PROBING QUESTION: Can useful work be extracted from the field dynamics?

In thermodynamics, work can be extracted from non-equilibrium systems.
This probe tests if the field has exploitable structure.

MATHEMATICAL FOUNDATION:
- Maximum extractable work: W_max = F_initial - F_final
- Second law: W <= -delta_F
- Efficiency: eta = W / Q_in

NULL HYPOTHESIS: At equilibrium (no extractable work)
DISCOVERY: Extractable work would indicate exploitable structure

Reference: Work extraction, thermodynamic engines, Maxwell's demon
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


def compute_kinetic_energy(history: List[int]) -> List[float]:
    """Compute kinetic energy for each transition."""
    energies = []
    for i in range(len(history) - 1):
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i + 1])
        v = r2 - r1
        ke = np.dot(v, v) / 2
        energies.append(ke)
    return energies


def compute_extractable_work_from_bias(history: List[int]) -> Dict:
    """
    Compute work extractable from TetA/TetB bias.
    
    If there's a bias, we could extract work by biasing transitions.
    """
    n_a = sum(1 for v in history if v in TET_A)
    n_b = len(history) - n_a
    n = len(history)
    
    p_a = n_a / n
    p_b = n_b / n
    
    # Free energy from bias (relative to uniform)
    # F = -T * sum(p * log(p)) for T=1
    # Uniform: F_0 = -log(0.5) = log(2)
    # Biased: F = -p_a*log(p_a) - p_b*log(p_b)
    
    if p_a > 0 and p_b > 0:
        F_biased = -p_a * math.log(p_a) - p_b * math.log(p_b)
        F_uniform = math.log(2)
        delta_F = F_uniform - F_biased
    else:
        delta_F = 0
    
    # Maximum extractable work (Landauer principle)
    # For biased -> uniform transition
    W_max = delta_F
    
    return {
        'p_A': p_a,
        'p_B': p_b,
        'bias': abs(p_a - p_b),
        'extractable_work': W_max,
        'is_exploitable': W_max > 0.01,
    }


def compute_information_work(history: List[int]) -> Dict:
    """
    Compute work equivalent of information in the sequence.
    
    Using Landauer's principle: W = kT * ln(2) per bit erased.
    """
    # Shannon entropy of the sequence
    counts = Counter(history)
    n = len(history)
    
    H = 0.0
    for c in counts.values():
        p = c / n
        if p > 0:
            H -= p * math.log2(p)
    
    # Maximum entropy
    H_max = math.log2(8)
    
    # Information content (bits of non-randomness)
    info_content = H_max - H
    
    # Work equivalent (Landauer, kT = 1)
    work_per_bit = math.log(2)  # kT * ln(2)
    total_work = info_content * work_per_bit * n
    
    return {
        'entropy': H,
        'max_entropy': H_max,
        'info_content_per_symbol': info_content,
        'total_info_content': info_content * n,
        'work_equivalent': total_work,
    }


def simulate_heat_engine(history: List[int], window: int = 50) -> Dict:
    """
    Simulate a simple heat engine using chamber oscillations.
    
    Extract work when transitioning between chambers.
    """
    # Track chamber state
    chambers = [0 if v in TET_A else 1 for v in history]
    
    work_extracted = 0.0
    heat_absorbed = 0.0
    
    for i in range(len(history) - 1):
        # Kinetic energy (heat)
        r1 = get_vertex_coordinates(history[i])
        r2 = get_vertex_coordinates(history[i + 1])
        v = r2 - r1
        ke = np.dot(v, v) / 2
        
        heat_absorbed += ke
        
        # Work from chamber crossing (potential difference)
        if chambers[i] != chambers[i + 1]:
            # "Work" from crossing the barrier
            work = 0.1  # Small work per crossing
            work_extracted += work
    
    # Efficiency
    efficiency = work_extracted / heat_absorbed if heat_absorbed > 0 else 0
    
    return {
        'work_extracted': work_extracted,
        'heat_absorbed': heat_absorbed,
        'efficiency': efficiency,
        'carnot_limit': 1.0,  # Ideal limit
        'efficiency_ratio': efficiency / 1.0,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class WorkFromBiasProbe(Test):
    """
    PROBING: Can work be extracted from the TetA/TetB bias?
    """
    name = "Work Extraction from Bias"
    question = (
        "Is there extractable work in the TetA/TetB bias? Any deviation from "
        "50/50 represents free energy that could theoretically be converted "
        "to work (like a Maxwell's demon exploiting information)."
    )
    reference = "Work extraction, Maxwell's demon"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: The ~1% TetB bias we found represents free energy. "
        "We compute how much work could be extracted by exploiting this "
        "bias, using thermodynamic principles."
    )

    def derivation(self):
        return (
            Derivation()
            .step("WORK FROM BIAS:")
            .step("Biased distribution has lower entropy than uniform.")
            .step("This free energy can be converted to work.")
            .equation("W_max = F_uniform - F_biased")
            .equation("F = -T * sum(p * log(p))")
            .step("LANDAUER PRINCIPLE:")
            .equation("W = kT * ln(2) per bit of information")
            .step("Information in bias = reduction from max entropy")
            .conclude("Bias represents extractable thermodynamic work.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Work from bias
        bias_work = compute_extractable_work_from_bias(history)
        
        # Information work
        info_work = compute_information_work(history)
        
        return (
            Model()
            .add("P(TetA)", bias_work['p_A'])
            .add("P(TetB)", bias_work['p_B'])
            .add("Bias magnitude", bias_work['bias'])
            .add("Extractable work (per symbol)", bias_work['extractable_work'])
            .add("Info content (bits/symbol)", info_work['info_content_per_symbol'])
            .add("Is exploitable", 1.0 if bias_work['is_exploitable'] else 0.0)
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
            .add("P(TetA)", 0.500389, abs_tol=0.026)  # random range [0.485903, 0.522496]
            .add("P(TetB)", 0.499611, abs_tol=0.026)  # random range [0.477504, 0.514097]
            .add("Bias magnitude", 0.0117177, abs_tol=0.039)  # random range [0.00019996, 0.044991]
            .add("Extractable work (per symbol)", 0.000104292, abs_tol=0.0011)  # random range [1.9992e-08, 0.00101244]
            .add("Info content (bits/symbol)", 0.00107759, abs_tol=0.0023)  # random range [0.000139637, 0.00301032]
            .add("Is exploitable", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class HeatEngineSimulationProbe(Test):
    """
    PROBING: Can the field dynamics drive a heat engine?
    """
    name = "Heat Engine Efficiency"
    question = (
        "If we use chamber oscillations to drive a heat engine, what efficiency "
        "can we achieve? This tests whether the field dynamics can do "
        "thermodynamic work."
    )
    reference = "Heat engines, Carnot efficiency"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We simulate extracting work from chamber transitions "
        "(like a piston moving between states). The efficiency tells us "
        "how useful the field dynamics is as a thermodynamic engine."
    )

    def derivation(self):
        return (
            Derivation()
            .step("HEAT ENGINE:")
            .step("Extract work from chamber crossings.")
            .step("Heat absorbed from kinetic energy.")
            .step("EFFICIENCY:")
            .equation("eta = W_out / Q_in")
            .step("CARNOT LIMIT:")
            .equation("eta_max = 1 - T_cold/T_hot")
            .step("No engine can exceed Carnot efficiency.")
            .conclude("Engine efficiency measures thermodynamic usefulness.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Simulate heat engine
        engine = simulate_heat_engine(history)
        
        # Number of chamber crossings
        n_crossings = sum(1 for i in range(len(history)-1) 
                        if (history[i] in TET_A) != (history[i+1] in TET_A))
        
        # Work per crossing
        work_per_crossing = engine['work_extracted'] / n_crossings if n_crossings > 0 else 0
        
        return (
            Model()
            .add("Total work extracted", engine['work_extracted'])
            .add("Total heat absorbed", engine['heat_absorbed'])
            .add("Efficiency", engine['efficiency'])
            .add("Number of crossings", n_crossings)
            .add("Work per crossing", work_per_crossing)
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
            .add("Total work extracted", 250.239, abs_tol=11)  # random range [241.7, 259.8]
            .add("Total heat absorbed", 15012.7, abs_tol=420)  # random range [14712, 15376]
            .add("Efficiency", 0.0166698, abs_tol=0.00093)  # random range [0.0158636, 0.017367]
            .add("Number of crossings", 2502.39, abs_tol=110)  # random range [2417, 2598]
            .add("Work per crossing", 0.1, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    WorkFromBiasProbe,
    HeatEngineSimulationProbe,
]


def run_all():
    """Run all work extraction probing tests."""
    summary = (
        "WORK EXTRACTION PROBING\n\n"
        "These probes test for extractable thermodynamic work.\n"
        "Bias work: free energy from non-uniform distribution\n"
        "Heat engine: efficiency of work extraction\n\n"
        "We are DISCOVERING exploitable structure."
    )
    return run_tests("Work Extraction Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
