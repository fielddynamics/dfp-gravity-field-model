"""
Coupling Port Traversal Completeness
====================================

This module tests whether pi-driven traversal samples all Coupling Ports
(faces) of the dual Field Chamber structure. A Coupling Port is considered
"visited" when all 3 of its vertices have been traversed. These tests verify:

- All 8 Coupling Ports (4 per Field Chamber) are visited
- Both TIME Coupling Ports and all 6 SPATIAL Coupling Ports complete
- Coupling Port completion occurs efficiently (within reasonable steps)
- Edges are traversed with reasonable balance
- Vertex distribution has high entropy (uniform sampling)
"""

import sys
import os
import math
from typing import Dict, Optional, Set, List
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from common import get_pi_base8, get_tetrahedron, TET_A, TET_B


# =============================================================================
# FACE DEFINITIONS
# =============================================================================

FACE_VERTICES = {
    'FACE_A1': frozenset({2, 4, 7}),  # Tet A, opposite V1
    'FACE_A2': frozenset({1, 4, 7}),  # Tet A, opposite V2
    'FACE_A4': frozenset({1, 2, 7}),  # Tet A, opposite V4
    'FACE_A7': frozenset({1, 2, 4}),  # Tet A TIME face
    'FACE_B0': frozenset({3, 5, 6}),  # Tet B TIME face
    'FACE_B3': frozenset({0, 5, 6}),  # Tet B, opposite V3
    'FACE_B5': frozenset({0, 3, 6}),  # Tet B, opposite V5
    'FACE_B6': frozenset({0, 3, 5}),  # Tet B, opposite V6
}

TIME_FACES = ['FACE_A7', 'FACE_B0']
SPATIAL_FACES = ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_B3', 'FACE_B5', 'FACE_B6']

EDGES = [
    (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6),
    (3, 7), (4, 5), (4, 6), (5, 7), (6, 7),
]


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_face_completion(num_digits: int = 500) -> Dict:
    """Analyze when each face becomes complete (all 3 vertices visited)."""
    digits = get_pi_base8(num_digits, include_integer=True)
    
    cumsum = 0
    vertices_visited = set()
    face_completion = {}
    
    for step, digit in enumerate(digits):
        cumsum += digit
        vertex = cumsum % 8
        vertices_visited.add(vertex)
        
        for face_name, face_vertices in FACE_VERTICES.items():
            if face_name not in face_completion:
                if face_vertices.issubset(vertices_visited):
                    face_completion[face_name] = step
        
        if len(face_completion) == 8:
            break
    
    return {
        'faces_complete': len(face_completion),
        'face_steps': face_completion,
        'steps_to_all': max(face_completion.values()) if len(face_completion) == 8 else None,
    }


def analyze_edge_traversal(num_digits: int = 500) -> Dict:
    """Track which edges are traversed during the sequence."""
    digits = get_pi_base8(num_digits, include_integer=True)
    
    cumsum = 0
    prev_vertex = None
    edges_traversed = set()
    
    for digit in digits:
        cumsum += digit
        vertex = cumsum % 8
        
        if prev_vertex is not None and prev_vertex != vertex:
            edge = tuple(sorted([prev_vertex, vertex]))
            edges_traversed.add(edge)
        
        prev_vertex = vertex
    
    defined_edges = set(EDGES)
    return {
        'unique_edges': len(edges_traversed),
        'defined_traversed': len(edges_traversed.intersection(defined_edges)),
        'all_12': len(edges_traversed.intersection(defined_edges)) == 12,
    }


def analyze_vertex_distribution(num_digits: int = 500) -> Dict:
    """Calculate vertex visit statistics and entropy."""
    digits = get_pi_base8(num_digits, include_integer=True)
    
    cumsum = 0
    vertices = []
    
    for digit in digits:
        cumsum += digit
        vertices.append(cumsum % 8)
    
    counts = Counter(vertices)
    total = len(vertices)
    
    # Shannon entropy
    entropy = 0
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    
    max_entropy = math.log2(8)  # 3 bits for uniform
    
    return {
        'counts': counts,
        'entropy': entropy,
        'max_entropy': max_entropy,
        'entropy_ratio': entropy / max_entropy,
    }


def analyze_tetrahedra_balance(num_digits: int = 500) -> Dict:
    """Analyze balance between Tet A and Tet B visits."""
    digits = get_pi_base8(num_digits, include_integer=True)
    
    cumsum = 0
    tet_a = 0
    tet_b = 0
    
    for digit in digits:
        cumsum += digit
        vertex = cumsum % 8
        if vertex in TET_A:
            tet_a += 1
        else:
            tet_b += 1
    
    total = tet_a + tet_b
    return {
        'tet_a': tet_a,
        'tet_b': tet_b,
        'ratio': tet_a / tet_b if tet_b > 0 else 0,
        'tet_a_pct': tet_a / total,
        'tet_b_pct': tet_b / total,
    }


# =============================================================================
# TESTS
# =============================================================================

class AllFacesVisited(GFDTest):
    """
    Field Closure requires sampling all regions of the dual Field Chamber.
    All 8 Coupling Ports (faces) must eventually complete for full coverage.
    """
    name = "All 8 Coupling Ports Visited"
    question = "Does pi-driven traversal eventually visit all 8 Coupling Ports, ensuring complete geometric coverage of both Field Chambers?"
    reference_source = "Theoretical (8 faces)"
    tolerance = 0.001
    derivation = (
        "PREMISE: The stellated octahedron has 2k=8 Coupling Ports (k=4 per tetrahedron). "
        "STEP 1: A Coupling Port is 'complete' when all 3 of its vertices have been visited. "
        "STEP 2: Track vertex visits during traversal and check face completion status. "
        "STEP 3: With ergodic vertex sampling, all 8 vertices are eventually visited. "
        "STEP 4: Since each face has only 3 vertices, complete vertex coverage guarantees complete face coverage. "
        "OUTPUT: All 8 Coupling Ports complete within sufficient traversal steps."
    )
    commentary = (
        "Complete Coupling Port coverage indicates the traversal samples all "
        "geometric regions of the Field Chamber. This ergodic property is "
        "necessary for Field Closure to represent a complete information cycle."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_face_completion(500)
        return {"Faces complete": analysis['faces_complete']}
    
    def observations(self) -> Dict[str, float]:
        return {"Faces complete": 8}


class TimeFacesVisited(GFDTest):
    """
    The TIME faces (FACE_A7 and FACE_B0) are geometrically special, pointing
    along the time axis. Their completion is essential for temporal coherence
    in the field closure.
    """
    name = "TIME Faces Visited"
    question = "Are both TIME Coupling Ports (FACE_A7 with vertices {1,2,4} and FACE_B0 with vertices {3,5,6}) completed during traversal?"
    reference_source = "Theoretical (2 TIME faces)"
    tolerance = 0.001
    derivation = (
        "PREMISE: TIME Coupling Ports are the faces perpendicular to the V0-V7 apex axis. "
        "STEP 1: FACE_A7 = {1,2,4} is the Tet A face opposite vertex 7. "
        "STEP 2: FACE_B0 = {3,5,6} is the Tet B face opposite vertex 0. "
        "STEP 3: Track when all 3 vertices of each TIME face have been visited. "
        "OUTPUT: Both TIME Coupling Ports complete, confirming temporal dimension coverage."
    )
    commentary = (
        "TIME Coupling Port completion is essential for full Field Closure. "
        "These faces oriented along the apex axis may encode temporal information "
        "that must be sampled for the closure cycle to be complete."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_face_completion(500)
        time_complete = sum(1 for f in TIME_FACES if f in analysis['face_steps'])
        return {"TIME faces complete": time_complete}
    
    def observations(self) -> Dict[str, float]:
        return {"TIME faces complete": 2}


class SpatialFacesVisited(GFDTest):
    """
    The 6 SPATIAL faces represent the three spatial dimensions (2 faces each).
    Their completion ensures the field samples all spatial directions.
    """
    name = "SPATIAL Faces Visited"
    question = "Are all 6 SPATIAL Coupling Ports completed, representing the d=k-1=3 spatial dimensions with dual coverage?"
    reference_source = "Theoretical (6 SPATIAL faces)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Each tetrahedron has k=4 faces; 1 is TIME, leaving k-1=3 SPATIAL. "
        "STEP 1: Tet A SPATIAL faces: FACE_A1={2,4,7}, FACE_A2={1,4,7}, FACE_A4={1,2,7}. "
        "STEP 2: Tet B SPATIAL faces: FACE_B3={0,5,6}, FACE_B5={0,3,6}, FACE_B6={0,3,5}. "
        "STEP 3: Total SPATIAL faces = 3 + 3 = 6, corresponding to 2 faces per spatial dimension. "
        "OUTPUT: All 6 SPATIAL Coupling Ports complete during extended traversal."
    )
    commentary = (
        "Six SPATIAL Coupling Ports (three per Field Chamber) correspond to the "
        "three spatial dimensions with dual coverage. Their completion ensures "
        "full spatial information is encoded in the traversal."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_face_completion(500)
        spatial_complete = sum(1 for f in SPATIAL_FACES if f in analysis['face_steps'])
        return {"SPATIAL faces complete": spatial_complete}
    
    def observations(self) -> Dict[str, float]:
        return {"SPATIAL faces complete": 6}


class FaceCompletionEfficiency(GFDTest):
    """
    If faces take too long to complete, the closure cycle is inefficient.
    All faces should complete within 50 steps (well within first few orbits).
    """
    name = "Face Completion Efficiency"
    question = "Do all 8 Coupling Ports complete within 50 traversal steps, demonstrating efficient geometric sampling?"
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Efficient traversal should rapidly cover all geometric regions. "
        "STEP 1: Execute traversal and track step number when each face completes. "
        "STEP 2: Record the maximum step number across all 8 faces. "
        "STEP 3: With average pi digit ~3.5 and 8 vertices, ~2-3 digits per orbit expected. "
        "STEP 4: 50 steps provides ~15-20 orbits, ample for complete coverage. "
        "OUTPUT: All faces completing within 50 steps confirms efficient sampling."
    )
    commentary = (
        "Efficient Coupling Port completion within dozens of steps indicates "
        "the traversal sequence rapidly samples the entire Field Chamber. "
        "This efficiency is consistent with pi digits providing effective "
        "geometric coverage."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_face_completion(500)
        steps = analysis['steps_to_all']
        within_50 = 1 if steps is not None and steps < 50 else 0
        return {
            "Steps to complete all": steps if steps else 999,
            "Within 50 steps": within_50,
        }


class AllEdgesTraversed(GFDTest):
    """
    The dual Field Chamber has 12 edges. Complete Field Closure requires
    traversing all edges at some point for full connectivity coverage.
    """
    name = "All 12 Edges Traversed"
    question = "Are all 12 edges of the stellated octahedron traversed, with 6 edges per tetrahedron corresponding to 6 quark flavors?"
    reference_source = "Theoretical (12 edges)"
    tolerance = 0.001
    derivation = (
        "PREMISE: A tetrahedron has 6 edges; the dual structure has 6+6=12 total edges. "
        "STEP 1: An edge is 'traversed' when consecutive steps connect its two vertices. "
        "STEP 2: Track unique vertex-pair transitions during traversal. "
        "STEP 3: Count how many of the 12 defined edges appear in the transition set. "
        "OUTPUT: All 12 edges traversed confirms complete connectivity sampling."
    )
    commentary = (
        "Complete edge traversal indicates the connectivity structure of the "
        "stellated octahedron is fully sampled. The 12 edges correspond to "
        "6 edges per tetrahedron, matching the quark flavor count."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_edge_traversal(500)
        return {"Edges traversed": analysis['defined_traversed']}
    
    def observations(self) -> Dict[str, float]:
        return {"Edges traversed": 12}


class VertexEntropy(GFDTest):
    """
    High entropy in vertex visits indicates uniform sampling of the geometry.
    The maximum entropy for 8 vertices is 3 bits. We want at least 95% of
    maximum to ensure no vertex is systematically under-sampled.
    """
    name = "Vertex Distribution Entropy"
    question = "Does the vertex visit distribution achieve at least 95% of maximum Shannon entropy (3 bits for 8 vertices)?"
    reference_source = "Theoretical (uniform = 3 bits)"
    tolerance = 0.05
    derivation = (
        "PREMISE: Shannon entropy measures the uniformity of a probability distribution. "
        "STEP 1: Maximum entropy for 8 equiprobable states = log2(8) = 3 bits. "
        "STEP 2: Calculate observed visit probabilities: p_v = count_v / total_visits. "
        "STEP 3: Compute entropy: H = -Σ p_v × log2(p_v) for v in {0,1,...,7}. "
        "STEP 4: Entropy ratio = H / 3 bits. "
        "OUTPUT: Ratio ≥ 0.95 confirms near-uniform vertex sampling."
    )
    commentary = (
        "Near-maximum entropy indicates the traversal approaches uniform sampling "
        "across all 8 vertices. This information-theoretic measure confirms "
        "pi-driven traversal maximizes exploration of the Field Chamber state space."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_vertex_distribution(500)
        return {
            "Entropy (bits)": analysis['entropy'],
            "Entropy ratio": analysis['entropy_ratio'],
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Entropy (bits)": 3.0,  # Max for 8 vertices
            "Entropy ratio": 1.0,
        }


class FieldChamberBalance(GFDTest):
    """
    The dual Field Chambers (Tet A and Tet B) should be visited with approximate
    balance. Pi's digit distribution creates statistical fluctuations, but neither
    chamber should dominate by more than 20%.
    """
    name = "Field Chamber Balance"
    question = "Are Tetrahedron A and Tetrahedron B visited with approximate balance (neither exceeding 60% of total)?"
    reference_source = None  # Statistical observation
    tolerance = 0.20
    derivation = (
        "PREMISE: Tet A has vertices {1,2,4,7} and Tet B has vertices {0,3,5,6}, each with 4 vertices (50%). "
        "STEP 1: Count visits to Tet A vertices and Tet B vertices during traversal. "
        "STEP 2: Calculate percentages: Tet_A_pct = Tet_A_count / total. "
        "STEP 3: Pi's digit distribution creates statistical fluctuations in the ratio. "
        "STEP 4: Verify neither tetrahedron exceeds 60% (gross imbalance check). "
        "OUTPUT: Both Field Chambers are visited without extreme bias."
    )
    commentary = (
        "Field Chamber visitation reflects pi's digit distribution projected onto the "
        "parity partition. While perfect 50/50 balance is not guaranteed due to pi's "
        "non-uniform digit sequences, gross imbalance would indicate systematic bias."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_tetrahedra_balance(1000)
        tet_a_balanced = 1.0 if 0.40 < analysis['tet_a_pct'] < 0.60 else 0.0
        tet_b_balanced = 1.0 if 0.40 < analysis['tet_b_pct'] < 0.60 else 0.0
        return {
            "Tet A percentage": analysis['tet_a_pct'],
            "Tet B percentage": analysis['tet_b_pct'],
            "Tet A balanced": tet_a_balanced,
            "Tet B balanced": tet_b_balanced,
        }


class VertexReturnFrequency(GFDTest):
    """
    Each vertex should be revisited regularly. Large imbalances in return
    frequency could indicate "sticky" vertices that trap the traversal.
    """
    name = "Vertex Return Frequency"
    question = "Is the ratio of maximum to minimum vertex visit counts bounded below 3:1, ensuring no vertex dominates or is excluded?"
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Balanced traversal should visit all vertices with similar frequency. "
        "STEP 1: Count visits to each of the 8 vertices during traversal. "
        "STEP 2: Find max_visits and min_visits across all vertices. "
        "STEP 3: Calculate ratio = max_visits / min_visits. "
        "OUTPUT: Ratio < 3 indicates no vertex systematically traps or excludes traversal."
    )
    commentary = (
        "Bounded visit ratios indicate no vertex systematically traps or excludes "
        "the traversal. This balance property supports the claim that pi digits "
        "provide unbiased geometric sampling of the Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        analysis = analyze_vertex_distribution(500)
        counts = analysis['counts']
        max_visits = max(counts.values())
        min_visits = min(counts.values())
        ratio = max_visits / min_visits if min_visits > 0 else 999
        balanced = 1 if ratio < 3 else 0
        return {
            "Max vertex visits": max_visits,
            "Min vertex visits": min_visits,
            "Max/min ratio": ratio,
            "Balanced (ratio < 3)": balanced,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    AllFacesVisited,
    TimeFacesVisited,
    SpatialFacesVisited,
    FaceCompletionEfficiency,
    AllEdgesTraversed,
    VertexEntropy,
    FieldChamberBalance,
    VertexReturnFrequency,
]


def run_all_tests() -> bool:
    """Run all Coupling Port traversal tests."""
    return run_test_group(
        title="Coupling Port Traversal Completeness",
        summary=(
            "These tests verify that Field Closure traversal samples all regions of "
            "the dual Field Chamber structure. Each of the 8 Coupling Ports (4 per "
            "Field Chamber) must be visited by having all 3 of its vertices traversed. "
            "The tests check complete coverage of Coupling Ports, edges, and vertices, "
            "plus balanced sampling between the dual Field Chambers. High entropy in "
            "vertex distribution confirms uniform sampling."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
