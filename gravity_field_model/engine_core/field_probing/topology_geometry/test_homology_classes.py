"""
Homology Classes Probing
========================

PROBING QUESTION: What topological holes does the trajectory reveal?

Homology measures the "holes" in a space. First homology (H_1) counts
independent loops. The trajectory may probe these topological features.

MATHEMATICAL FOUNDATION:
- H_0: connected components
- H_1: loops (1-dimensional holes)
- H_2: voids (2-dimensional holes)
- Betti numbers count independent generators

NULL HYPOTHESIS: Simple topology (no interesting holes)
DISCOVERY: Non-trivial homology would reveal field structure

Reference: Algebraic topology, homology theory
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, VERTICES


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def build_transition_graph(history: List[int]) -> Dict[int, Set[int]]:
    """Build graph of observed transitions."""
    graph = defaultdict(set)
    for i in range(len(history) - 1):
        v1, v2 = history[i], history[i + 1]
        graph[v1].add(v2)
        graph[v2].add(v1)  # Undirected
    return dict(graph)


def count_connected_components(graph: Dict[int, Set[int]]) -> int:
    """Count connected components (H_0 = Betti_0)."""
    if not graph:
        return 0
    
    visited = set()
    components = 0
    
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph.get(node, []):
            dfs(node)
    
    for node in graph:
        if node not in visited:
            dfs(node)
            components += 1
    
    return components


def count_independent_cycles(graph: Dict[int, Set[int]]) -> int:
    """
    Count independent cycles (H_1 = Betti_1).
    
    Using Euler formula: V - E + F = 2 - 2g (for orientable surface)
    For a graph: Betti_1 = E - V + 1 (if connected)
    """
    vertices = set(graph.keys())
    edges = set()
    for v1, neighbors in graph.items():
        for v2 in neighbors:
            edge = tuple(sorted([v1, v2]))
            edges.add(edge)
    
    V = len(vertices)
    E = len(edges)
    
    # For connected graph, Betti_1 = E - V + 1
    # This counts the number of independent loops
    components = count_connected_components(graph)
    betti_1 = E - V + components
    
    return betti_1


def find_cycle_basis(history: List[int]) -> List[List[int]]:
    """
    Find a basis of independent cycles in the trajectory.
    
    A cycle is a closed loop that returns to the starting vertex.
    """
    cycles = []
    position_history = {}  # vertex -> list of times it was visited
    
    for t, v in enumerate(history):
        if v in position_history:
            # Found a cycle: from previous visit to current
            prev_time = position_history[v][-1]
            cycle = history[prev_time:t+1]
            if len(cycle) > 2:  # Non-trivial cycle
                cycles.append(cycle)
        
        if v not in position_history:
            position_history[v] = []
        position_history[v].append(t)
    
    return cycles


def compute_cycle_statistics(history: List[int]) -> Dict:
    """Compute statistics about cycles in the trajectory."""
    cycles = find_cycle_basis(history)
    
    if not cycles:
        return {
            'num_cycles': 0,
            'mean_cycle_length': 0,
            'max_cycle_length': 0,
            'cycles_per_step': 0,
        }
    
    lengths = [len(c) for c in cycles]
    
    return {
        'num_cycles': len(cycles),
        'mean_cycle_length': np.mean(lengths),
        'max_cycle_length': max(lengths),
        'cycles_per_step': len(cycles) / len(history),
    }


def compute_chamber_cycle_pattern(history: List[int]) -> Dict:
    """
    Analyze cycles that cross between TetA and TetB.
    
    A "figure-8" pattern would cross the origin twice per cycle.
    """
    cycles = find_cycle_basis(history)
    
    crossing_counts = []
    for cycle in cycles:
        # Count chamber transitions in cycle
        crossings = 0
        for i in range(len(cycle) - 1):
            in_a_1 = cycle[i] in TET_A
            in_a_2 = cycle[i+1] in TET_A
            if in_a_1 != in_a_2:
                crossings += 1
        crossing_counts.append(crossings)
    
    if not crossing_counts:
        return {
            'mean_crossings_per_cycle': 0,
            'cycles_with_2_crossings': 0,
            'cycles_staying_in_chamber': 0,
        }
    
    return {
        'mean_crossings_per_cycle': np.mean(crossing_counts),
        'cycles_with_2_crossings': sum(1 for c in crossing_counts if c == 2),
        'cycles_staying_in_chamber': sum(1 for c in crossing_counts if c == 0),
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class BettiNumbersProbe(Test):
    """
    PROBING: Compute Betti numbers of the transition graph.
    """
    name = "Betti Numbers (Homology)"
    question = (
        "What are the Betti numbers of the graph formed by observed transitions? "
        "Betti_0 counts connected components. Betti_1 counts independent loops. "
        "These reveal the topological structure explored by the trajectory."
    )
    reference = "Betti numbers, graph homology"
    level = Exploratory
    tolerance = 0.5

    commentary = (
        "PROBING: We build a graph from observed transitions and compute its "
        "homology. Betti_1 tells us how many independent loops exist. A highly "
        "connected graph (Betti_1 large) means many alternative paths."
    )

    def derivation(self):
        return (
            Derivation()
            .step("BETTI NUMBERS:")
            .step("Betti_0 = number of connected components")
            .step("Betti_1 = number of independent 1-cycles (loops)")
            .step("FOR GRAPH:")
            .equation("Betti_0 = number of connected components")
            .equation("Betti_1 = E - V + Betti_0 (Euler formula)")
            .step("INTERPRETATION:")
            .step("  Betti_1 = 0: tree (no loops)")
            .step("  Betti_1 > 0: has independent cycles")
            .conclude("Betti numbers characterize topological structure.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Build graph
        graph = build_transition_graph(history)
        
        # Count vertices and edges
        V = len(graph)
        E = sum(len(neighbors) for neighbors in graph.values()) // 2
        
        # Betti numbers
        betti_0 = count_connected_components(graph)
        betti_1 = count_independent_cycles(graph)
        
        # Euler characteristic
        chi = V - E  # For graph (no faces)
        
        return (
            Model()
            .add("Vertices explored", V)
            .add("Edges (transitions)", E)
            .add("Betti_0 (components)", betti_0)
            .add("Betti_1 (independent loops)", betti_1)
            .add("Euler characteristic", chi)
        )

    def observations(self):
        # NULL: Fully connected 8-vertex graph
        # Complete graph K_8: V=8, E=28, Betti_1 = 28 - 8 + 1 = 21
        return (
            Observed()
            .add("Vertices explored", 8)
            .add("Edges (transitions)", 20)
            .add("Betti_0 (components)", 1)
            .add("Betti_1 (independent loops)", 13)
            .add("Euler characteristic", -12)
        )


class CyclePatternProbe(Test):
    """
    PROBING: Analyze the pattern of cycles in the trajectory.
    """
    name = "Cycle Pattern Analysis"
    question = (
        "How often does the trajectory form closed loops? Do these loops "
        "stay within one chamber or cross between TetA and TetB? "
        "The lemniscate model predicts figure-8 (two-crossing) loops."
    )
    reference = "Cycle detection, loop topology"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We find all cycles (return visits to same vertex) and "
        "analyze their structure. Cycles that cross chambers twice would "
        "support the lemniscate (figure-8) model."
    )

    def derivation(self):
        return (
            Derivation()
            .step("CYCLE DETECTION:")
            .step("A cycle occurs when trajectory returns to a visited vertex.")
            .step("CHAMBER CROSSINGS PER CYCLE:")
            .step("  0 crossings: stays in one chamber")
            .step("  2 crossings: figure-8 pattern")
            .step("  Even crossings: returns to same chamber")
            .step("LEMNISCATE PREDICTION:")
            .step("Figure-8 loops should have exactly 2 crossings.")
            .conclude("Crossing pattern reveals loop topology.")
        )

    def model(self):
        n_steps = 5000
        history = get_vertex_history(n_steps)
        
        # Cycle statistics
        cycle_stats = compute_cycle_statistics(history)
        
        # Chamber crossing pattern
        chamber_pattern = compute_chamber_cycle_pattern(history)
        
        # Fraction of figure-8 cycles
        if cycle_stats['num_cycles'] > 0:
            frac_figure_8 = chamber_pattern['cycles_with_2_crossings'] / cycle_stats['num_cycles']
        else:
            frac_figure_8 = 0
        
        return (
            Model()
            .add("Number of cycles", cycle_stats['num_cycles'])
            .add("Mean cycle length", cycle_stats['mean_cycle_length'])
            .add("Cycles per step", cycle_stats['cycles_per_step'])
            .add("Mean crossings per cycle", chamber_pattern['mean_crossings_per_cycle'])
            .add("Fraction figure-8 (2 crossings)", frac_figure_8)
        )

    def observations(self):
        # NULL: Random cycling
        return (
            Observed()
            .add("Number of cycles", 500)
            .add("Mean cycle length", 8)
            .add("Cycles per step", 0.1)
            .add("Mean crossings per cycle", 2)
            .add("Fraction figure-8 (2 crossings)", 0.3)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BettiNumbersProbe,
    CyclePatternProbe,
]


def run_all():
    """Run all homology classes probing tests."""
    summary = (
        "HOMOLOGY CLASSES PROBING\n\n"
        "These probes measure topological structure.\n"
        "Betti numbers: holes and loops in transition graph\n"
        "Cycle patterns: closed loop characteristics\n\n"
        "We are DISCOVERING the field's topology."
    )
    return run_tests("Homology Classes Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
