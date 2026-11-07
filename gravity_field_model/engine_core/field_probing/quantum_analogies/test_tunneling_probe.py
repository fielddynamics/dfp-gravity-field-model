"""
Tunneling Probing
=================

PROBING QUESTION: Can the field "tunnel" across classically forbidden regions?

Quantum tunneling allows particles to cross barriers they classically cannot.
We test if the field shows analogous behavior.

MATHEMATICAL FOUNDATION:
- Barrier: high energy region between chambers
- Tunneling: transition without "enough" energy
- Tunneling rate depends on barrier height and width

NULL HYPOTHESIS: Only classical transitions (enough energy to cross)
DISCOVERY: Tunneling-like transitions would indicate quantum-like behavior

Reference: Quantum tunneling, WKB approximation
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


def compute_kinetic_energy(v1: int, v2: int) -> float:
    """
    Compute kinetic energy for transition.
    
    E = |v|^2 / 2 where v = r2 - r1
    """
    r1 = get_vertex_coordinates(v1)
    r2 = get_vertex_coordinates(v2)
    v = r2 - r1
    return np.dot(v, v) / 2


def compute_potential_energy(vertex: int) -> float:
    """
    Define a potential energy based on distance from origin.
    
    Vertices farther from origin have higher potential.
    """
    r = get_vertex_coordinates(vertex)
    return np.linalg.norm(r)  # Simple radial potential


def compute_barrier_height(v1: int, v2: int) -> float:
    """
    Compute effective barrier between two vertices.
    
    Barrier = max potential along path - initial potential
    """
    # For simplicity, use potential at midpoint
    r1 = get_vertex_coordinates(v1)
    r2 = get_vertex_coordinates(v2)
    r_mid = (r1 + r2) / 2
    
    # Midpoint potential (distance from origin)
    V_mid = np.linalg.norm(r_mid)
    V_initial = np.linalg.norm(r1)
    
    return max(0, V_mid - V_initial)


def identify_tunneling_events(history: List[int]) -> List[Dict]:
    """
    Identify potential tunneling events.
    
    A tunneling event is a transition where kinetic energy is less than
    the barrier height (classically forbidden).
    """
    tunneling_events = []
    
    for i in range(len(history) - 2):
        v_prev = history[i]
        v_curr = history[i + 1]
        v_next = history[i + 2]
        
        # Kinetic energy entering the transition
        KE = compute_kinetic_energy(v_prev, v_curr)
        
        # Barrier for next transition
        barrier = compute_barrier_height(v_curr, v_next)
        
        # Is it a chamber crossing?
        is_crossing = (v_curr in TET_A) != (v_next in TET_A)
        
        if barrier > 0 and KE < barrier and is_crossing:
            tunneling_events.append({
                'time': i + 1,
                'kinetic_energy': KE,
                'barrier_height': barrier,
                'deficit': barrier - KE,
                'vertices': (v_curr, v_next),
            })
    
    return tunneling_events


def compute_barrier_transmission(history: List[int]) -> Dict:
    """
    Compute transmission coefficient through different barrier heights.
    
    In quantum mechanics: T ~ exp(-2 * kappa * L) for barrier
    """
    # Group transitions by barrier height
    barrier_groups = {'low': [], 'medium': [], 'high': []}
    
    for i in range(len(history) - 1):
        v1, v2 = history[i], history[i + 1]
        barrier = compute_barrier_height(v1, v2)
        
        if barrier < 0.3:
            barrier_groups['low'].append(1)
        elif barrier < 0.6:
            barrier_groups['medium'].append(1)
        else:
            barrier_groups['high'].append(1)
    
    # Compute transmission rates (transitions / opportunities)
    total = len(history) - 1
    rates = {
        'low_barrier_fraction': len(barrier_groups['low']) / total,
        'medium_barrier_fraction': len(barrier_groups['medium']) / total,
        'high_barrier_fraction': len(barrier_groups['high']) / total,
    }
    
    return rates


# =============================================================================
# TEST CLASSES
# =============================================================================

class TunnelingEventProbe(Test):
    """
    PROBING: Identify and count tunneling-like events.
    """
    name = "Tunneling Event Detection"
    question = (
        "Does the field undergo transitions that are classically forbidden? "
        "Tunneling events occur when kinetic energy is less than the barrier "
        "height, yet the transition still occurs."
    )
    reference = "Quantum tunneling"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We define a simple potential (distance from origin) and "
        "check if transitions occur with insufficient kinetic energy. Such "
        "events would be classically forbidden but quantum-allowed."
    )

    def derivation(self):
        return (
            Derivation()
            .step("TUNNELING CONDITION:")
            .step("Classical: transition allowed if KE > Barrier")
            .step("Quantum: transition possible even if KE < Barrier")
            .step("DETECTION:")
            .step("  KE = |v|^2 / 2 (kinetic energy)")
            .step("  Barrier = V(midpoint) - V(start)")
            .step("  Tunneling event: KE < Barrier but transition occurs")
            .step("TUNNELING RATE:")
            .equation("Gamma ~ exp(-sqrt(2m(V-E)) * L / hbar)")
            .conclude("Count events where KE < Barrier.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Find tunneling events
        events = identify_tunneling_events(history)
        
        # Statistics
        n_tunneling = len(events)
        total_crossings = sum(1 for i in range(len(history)-1) 
                            if (history[i] in TET_A) != (history[i+1] in TET_A))
        
        if total_crossings > 0:
            tunneling_fraction = n_tunneling / total_crossings
        else:
            tunneling_fraction = 0
        
        # Energy deficit statistics
        if events:
            deficits = [e['deficit'] for e in events]
            mean_deficit = np.mean(deficits)
            max_deficit = np.max(deficits)
        else:
            mean_deficit = 0
            max_deficit = 0
        
        return (
            Model()
            .add("Total chamber crossings", total_crossings)
            .add("Tunneling events", n_tunneling)
            .add("Tunneling fraction", tunneling_fraction)
            .add("Mean energy deficit", mean_deficit)
            .add("Max energy deficit", max_deficit)
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
            .add("Total chamber crossings", 2502.39, abs_tol=110)  # random range [2417, 2598]
            .add("Tunneling events", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Tunneling fraction", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Mean energy deficit", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Max energy deficit", 0, abs_tol=1e-09)  # same for all 150 random sequences
        )

class BarrierTransmissionProbe(Test):
    """
    PROBING: Test if high barriers suppress transmission.
    """
    name = "Barrier Transmission Rate"
    question = (
        "Do high barriers reduce transition rates? In quantum mechanics, "
        "transmission probability decreases exponentially with barrier height. "
        "We test if the field shows similar behavior."
    )
    reference = "Barrier penetration, transmission coefficient"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We group transitions by barrier height and compute rates. "
        "Quantum-like behavior would show exponential suppression with "
        "barrier height. Classical would show sharp cutoff."
    )

    def derivation(self):
        return (
            Derivation()
            .step("QUANTUM TRANSMISSION:")
            .equation("T = exp(-2 * sqrt(2m(V-E)) * L / hbar)")
            .step("Exponential suppression with barrier height V")
            .step("CLASSICAL:")
            .step("  T = 1 if E > V (allowed)")
            .step("  T = 0 if E < V (forbidden)")
            .step("TEST: Compare transition rates at different barriers")
            .step("Exponential decay suggests quantum-like behavior")
            .conclude("Transmission vs barrier height reveals mechanism.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Compute barrier transmission rates
        rates = compute_barrier_transmission(history)
        
        # Ratio of high to low barrier transmission
        if rates['low_barrier_fraction'] > 0:
            suppression_ratio = rates['high_barrier_fraction'] / rates['low_barrier_fraction']
        else:
            suppression_ratio = 0
        
        return (
            Model()
            .add("Low barrier fraction", rates['low_barrier_fraction'])
            .add("Medium barrier fraction", rates['medium_barrier_fraction'])
            .add("High barrier fraction", rates['high_barrier_fraction'])
            .add("High/Low suppression ratio", suppression_ratio)
            .add("Shows barrier suppression", 1.0 if suppression_ratio < 0.5 else 0.0)
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
            .add("Low barrier fraction", 1, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Medium barrier fraction", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("High barrier fraction", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("High/Low suppression ratio", 0, abs_tol=1e-09)  # same for all 150 random sequences
            .add("Shows barrier suppression", 1, abs_tol=1e-09)  # same for all 150 random sequences
        )

# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    TunnelingEventProbe,
    BarrierTransmissionProbe,
]


def run_all():
    """Run all tunneling probing tests."""
    summary = (
        "TUNNELING PROBING\n\n"
        "These probes test for quantum-like tunneling.\n"
        "Tunneling events: transitions with insufficient energy\n"
        "Barrier transmission: rate vs barrier height\n\n"
        "We are DISCOVERING tunneling-like behavior."
    )
    return run_tests("Tunneling Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
