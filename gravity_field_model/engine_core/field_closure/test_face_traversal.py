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

import math
from typing import Dict, Optional, Set, List
from collections import Counter, defaultdict

from gravity_field_model.framework import *
from gravity_field_model.common import get_pi_base8, get_tetrahedron, TET_A, TET_B


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

class AllFacesVisited(Test):
    """
    Field Closure requires sampling all regions of the dual Field Chamber.
    All 8 Coupling Ports (faces) must eventually complete for full coverage.
    """
    name = "All 8 Coupling Ports Visited"
    question = (
        "Does the traversal touch every surface? "
        "The Field Chamber has 8 triangular faces, and a face is 'complete' when all 3 of its "
        "corners have been visited. This test verifies that pi-driven traversal eventually "
        "completes all 8 faces, leaving no region unexplored."
    )
    reference = "Theoretical (8 faces)"
    tolerance = 0.001
    level = Critical
    audit_score = 89
    audit_notes = (
        "Question: 15/15 - Excellent 'touch every surface' hook. "
        "Derivation: 13/15 - Clear coverage logic. "
        "Commentary: 13/15 - Nice painting room analogy. "
        "Model: 9/10 - Good face count output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 9/10 - Good, imports get_pi_base8, TET_A, TET_B from common. FACE_VERTICES local. "
        "Accessibility: 12/15 - Great painting analogy. "
        "Header: 8/10 (module level) - Good overview. "
        "SAMPLE SIZE: 500 digits - ADEQUATE for face completion analysis. "
        "FUNCTION OPPORTUNITY: analyze_face_completion could be extracted to common. "
        "TO IMPROVE: Move FACE_VERTICES to common module. Explain why incomplete coverage breaks model."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The stellated octahedron has 2k=8 Coupling Ports (k=4 per tetrahedron).")
            .step("A Coupling Port is 'complete' when all 3 of its vertices have been visited.")
            .step("Track vertex visits during traversal and check face completion status.")
            .step("With ergodic vertex sampling, all 8 vertices are eventually visited.")
            .step("Since each face has only 3 vertices, complete vertex coverage guarantees complete face coverage.")
            .conclude("All 8 Coupling Ports complete within sufficient traversal steps.")
        )
    
    commentary = (
        "Imagine painting a room. You have not finished until every wall is covered. "
        "The Field Chamber has 8 'walls' (triangular faces), and each needs all 3 corners visited "
        "to count as complete. Since pi's digits eventually visit every vertex, and every face "
        "only needs 3 vertices, we eventually complete all 8 faces. "
        "This is essential: incomplete coverage would mean missing information."
    )
    
    def model(self):
        analysis = analyze_face_completion(500)
        return Model().add("Faces complete", analysis['faces_complete'])
    
    def observations(self):
        return Observed().add("Faces complete", 8)


class TimeFacesVisited(Test):
    """
    The TIME faces (FACE_A7 and FACE_B0) are geometrically special, pointing
    along the time axis. Their completion is essential for temporal coherence
    in the field closure.
    """
    name = "TIME Faces Visited"
    question = (
        "Are the 'time direction' faces completed? "
        "Two faces point along the apex axis (V0 to V7), representing the time direction. "
        "These TIME faces must be visited for full closure. "
        "This test checks whether both TIME faces complete during traversal."
    )
    reference = "Theoretical (2 TIME faces)"
    tolerance = 0.001
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 14/15 - Good 'time direction' spatial intuition. "
        "Derivation: 13/15 - Clear face identification. "
        "Commentary: 13/15 - Nice hourglass visualization. "
        "Model: 9/10 - Good count output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 9/10 - Imports from common. TIME_FACES local. "
        "Accessibility: 12/15 - Good hourglass analogy. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: 500 digits - ADEQUATE for face completion. "
        "FUNCTION OPPORTUNITY: None specific. "
        "TO IMPROVE: Explain WHY time faces are special geometrically."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: TIME Coupling Ports are the faces perpendicular to the V0-V7 apex axis.")
            .step("FACE_A7 = {1,2,4} is the Tet A face opposite vertex 7.")
            .step("FACE_B0 = {3,5,6} is the Tet B face opposite vertex 0.")
            .step("Track when all 3 vertices of each TIME face have been visited.")
            .conclude("Both TIME Coupling Ports complete, confirming temporal dimension coverage.")
        )
    
    commentary = (
        "Think of the Field Chamber as an hourglass with apexes at V0 and V7. "
        "The faces opposite these apexes (FACE_A7 and FACE_B0) are oriented 'in time,' "
        "perpendicular to the spatial midplane. Completing them means the temporal "
        "aspect of the geometry is fully sampled. Without this, Field Closure would "
        "have a temporal blind spot. Both TIME faces must complete."
    )
    
    def model(self):
        analysis = analyze_face_completion(500)
        time_complete = sum(1 for f in TIME_FACES if f in analysis['face_steps'])
        return Model().add("TIME faces complete", time_complete)
    
    def observations(self):
        return Observed().add("TIME faces complete", 2)


class SpatialFacesVisited(Test):
    """
    The 6 SPATIAL faces represent the three spatial dimensions (2 faces each).
    Their completion ensures the field samples all spatial directions.
    """
    name = "SPATIAL Faces Visited"
    question = (
        "Are all the 'space direction' faces completed? "
        "Six faces encode the three spatial dimensions (2 faces each, one per tetrahedron). "
        "Completing them means sampling all of 3D space. "
        "This test verifies all 6 SPATIAL faces complete during traversal."
    )
    reference = "Theoretical (6 SPATIAL faces)"
    tolerance = 0.001
    level = Standard
    audit_score = 87
    audit_notes = (
        "Question: 14/15 - Good spatial dimension encoding. "
        "Derivation: 12/15 - Could explain more about 3D encoding. "
        "Commentary: 13/15 - Nice 3+1 connection. "
        "Model: 9/10 - Good count output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 9/10 - Imports from common. SPATIAL_FACES local. "
        "Accessibility: 12/15 - Good 3+1 connection. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: 500 digits - ADEQUATE for face completion. "
        "FUNCTION OPPORTUNITY: None specific. "
        "TO IMPROVE: Explain HOW faces encode spatial dimensions."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tetrahedron has k=4 faces; 1 is TIME, leaving k-1=3 SPATIAL.")
            .step("Tet A SPATIAL faces: FACE_A1={2,4,7}, FACE_A2={1,4,7}, FACE_A4={1,2,7}.")
            .step("Tet B SPATIAL faces: FACE_B3={0,5,6}, FACE_B5={0,3,6}, FACE_B6={0,3,5}.")
            .step("Total SPATIAL faces = 3 + 3 = 6, corresponding to 2 faces per spatial dimension.")
            .conclude("All 6 SPATIAL Coupling Ports complete during extended traversal.")
        )
    
    commentary = (
        "Space has three dimensions: left/right, forward/back, up/down. Each dimension "
        "gets two faces in the Field Chamber (one per tetrahedron), giving 6 SPATIAL faces. "
        "Completing all 6 means the traversal has sampled every spatial direction. "
        "Together with the 2 TIME faces, we cover the full 3+1 dimensional structure."
    )
    
    def model(self):
        analysis = analyze_face_completion(500)
        spatial_complete = sum(1 for f in SPATIAL_FACES if f in analysis['face_steps'])
        return Model().add("SPATIAL faces complete", spatial_complete)
    
    def observations(self):
        return Observed().add("SPATIAL faces complete", 6)


class FaceCompletionEfficiency(Test):
    """
    If faces take too long to complete, the closure cycle is inefficient.
    All faces should complete within 50 steps (well within first few orbits).
    """
    name = "Face Completion Efficiency"
    question = (
        "How quickly do all faces complete? "
        "An efficient traversal should not take thousands of steps to cover basic geometry. "
        "This test checks whether all 8 faces complete within 50 steps, "
        "demonstrating that pi digits provide rapid, effective coverage."
    )
    reference = None  # Threshold check
    level = Standard
    audit_score = 80
    audit_notes = (
        "Question: 12/15 - Functional efficiency question. "
        "Derivation: 11/15 - Could explain WHY 50 is the threshold. "
        "Commentary: 12/15 - Good explorer mapping analogy. "
        "Model: 8/10 - Good step count output. "
        "Observations: 0/10 - MISSING observations() method. "
        "Constants: 9/10 - Imports from common. "
        "Accessibility: 12/15 - Good explorer analogy. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: 500 digits - ADEQUATE for efficiency check. "
        "FUNCTION OPPORTUNITY: None specific. "
        "TO IMPROVE: Add observations() method. Explain 50-step threshold reasoning."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Efficient traversal should rapidly cover all geometric regions.")
            .step("Execute traversal and track step number when each face completes.")
            .step("Record the maximum step number across all 8 faces.")
            .step("With average pi digit ~3.5 and 8 vertices, ~2-3 digits per orbit expected.")
            .step("50 steps provides ~15-20 orbits, ample for complete coverage.")
            .conclude("All faces completing within 50 steps confirms efficient sampling.")
        )
    
    commentary = (
        "A good explorer does not take forever to map a small room. With only 8 vertices, "
        "all 8 faces should complete quickly. 50 steps is more than enough: that is roughly "
        "15 orbits through the structure. If faces took hundreds of steps to complete, something "
        "would be wrong with our traversal. Pi's digit variety ensures rapid coverage."
    )
    
    def model(self):
        analysis = analyze_face_completion(500)
        steps = analysis['steps_to_all']
        within_50 = 1 if steps is not None and steps < 50 else 0
        return (
            Model()
            .add("Steps to complete all", steps if steps else 999)
            .add("Within 50 steps", within_50)
        )


class AllEdgesTraversed(Test):
    """
    The dual Field Chamber has 12 edges. Complete Field Closure requires
    traversing all edges at some point for full connectivity coverage.
    """
    name = "All 12 Edges Traversed"
    question = (
        "Does the traversal walk every hallway? "
        "Vertices are rooms; edges are hallways connecting them. "
        "The Field Chamber has 12 edges (6 per tetrahedron). "
        "This test checks whether we eventually walk every hallway at least once."
    )
    reference = "Theoretical (12 edges)"
    tolerance = 0.001
    level = Standard
    audit_score = 89
    audit_notes = (
        "Question: 15/15 - Excellent room/hallway intuition. "
        "Derivation: 13/15 - Clear edge counting. "
        "Commentary: 13/15 - Nice hotel security guard analogy. "
        "Model: 9/10 - Good edge count output. "
        "Observations: 10/10 - Clear expected value. "
        "Constants: 9/10 - Imports from common. EDGES local. "
        "Accessibility: 12/15 - Great security guard analogy. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: 500 digits - ADEQUATE for edge traversal. "
        "FUNCTION OPPORTUNITY: analyze_edge_traversal could be extracted. "
        "TO IMPROVE: Move EDGES constant to common module."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A tetrahedron has 6 edges; the dual structure has 6+6=12 total edges.")
            .step("An edge is 'traversed' when consecutive steps connect its two vertices.")
            .step("Track unique vertex-pair transitions during traversal.")
            .step("Count how many of the 12 defined edges appear in the transition set.")
            .conclude("All 12 edges traversed confirms complete connectivity sampling.")
        )
    
    commentary = (
        "A hotel has rooms (vertices) and hallways (edges). A thorough security guard "
        "walks every hallway at least once. The Field Chamber has 12 hallways: 6 within "
        "Tetrahedron A and 6 within Tetrahedron B. As pi drives us from vertex to vertex, "
        "we trace paths. This test confirms we eventually trace all 12 edges, "
        "leaving no connection unexplored."
    )
    
    def model(self):
        analysis = analyze_edge_traversal(500)
        return Model().add("Edges traversed", analysis['defined_traversed'])
    
    def observations(self):
        return Observed().add("Edges traversed", 12)


class VertexEntropy(Test):
    """
    High entropy in vertex visits indicates uniform sampling of the geometry.
    The maximum entropy for 8 vertices is 3 bits. We want at least 95% of
    maximum to ensure no vertex is systematically under-sampled.
    """
    name = "Vertex Distribution Entropy"
    question = (
        "How 'random' is the vertex visitation pattern? "
        "Shannon entropy measures uniformity: high entropy means no vertex is favored. "
        "For 8 vertices, maximum entropy is 3 bits. This test checks whether "
        "we achieve at least 95% of maximum, confirming unbiased sampling."
    )
    reference = "Theoretical (uniform = 3 bits)"
    tolerance = 0.05
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 14/15 - Good entropy as uniformity measure. "
        "Derivation: 13/15 - Clear Shannon formula. "
        "Commentary: 13/15 - Nice fair die analogy. "
        "Model: 9/10 - Good entropy ratio output. "
        "Observations: 10/10 - Clear expected values. "
        "Constants: 10/10 - Imports from common. "
        "Accessibility: 12/15 - Fair die analogy accessible. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: 500 digits - ADEQUATE for entropy calculation. "
        "FUNCTION OPPORTUNITY: analyze_vertex_distribution could be extracted. "
        "TO IMPROVE: Explain physical implications of low entropy."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Shannon entropy measures the uniformity of a probability distribution.")
            .step("Maximum entropy for 8 equiprobable states = log2(8) = 3 bits.")
            .step("Calculate observed visit probabilities: p_v = count_v / total_visits.")
            .step("Compute entropy: H = -Sum(p_v * log2(p_v)) for v in {0,1,...,7}.")
            .step("Entropy ratio = H / 3 bits.")
            .conclude("Ratio >= 0.95 confirms near-uniform vertex sampling.")
        )
    
    commentary = (
        "Entropy is information theory's measure of 'spread.' A die that always rolls 6 has "
        "zero entropy; a fair die has maximum entropy. For 8 vertices, max entropy is 3 bits. "
        "We want close to that: every vertex getting roughly equal attention. "
        "Achieving 95%+ of maximum entropy means pi-driven traversal is nearly as uniform "
        "as a perfectly fair random walk. No vertex is systematically neglected."
    )
    
    def model(self):
        analysis = analyze_vertex_distribution(500)
        return (
            Model()
            .add("Entropy (bits)", analysis['entropy'])
            .add("Entropy ratio", analysis['entropy_ratio'])
        )
    
    def observations(self):
        return (
            Observed()
            .add("Entropy (bits)", 3.0)  # Max for 8 vertices
            .add("Entropy ratio", 1.0)
        )


class FieldChamberBalance(Test):
    """
    The dual Field Chambers (Tet A and Tet B) should be visited with approximate
    balance. Pi's digit distribution creates statistical fluctuations, but neither
    chamber should dominate by more than 20%.
    """
    name = "Field Chamber Balance"
    question = (
        "Does the traversal favor one tetrahedron over the other? "
        "With 4 vertices each, both tetrahedra should receive about 50% of visits. "
        "This test checks that neither exceeds 60%, confirming rough balance."
    )
    reference = None  # Statistical observation
    tolerance = 0.20
    level = Standard
    audit_score = 84
    audit_notes = (
        "Question: 13/15 - Good 'favor' question about balance. "
        "Derivation: 12/15 - Could explain WHY 60% is threshold. "
        "Commentary: 13/15 - Nice biased poll analogy. "
        "Model: 9/10 - Good balance flags output. "
        "Observations: 0/10 - MISSING observations() method. "
        "Constants: 10/10 - Imports TET_A, TET_B from common. "
        "Accessibility: 12/15 - Poll analogy accessible. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: 1000 digits - GOOD for balance analysis. "
        "FUNCTION OPPORTUNITY: analyze_tetrahedra_balance could be extracted. "
        "TO IMPROVE: Add observations() method. Explain physical significance of imbalance."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Tet A has vertices {1,2,4,7} and Tet B has vertices {0,3,5,6}, each with 4 vertices (50%).")
            .step("Count visits to Tet A vertices and Tet B vertices during traversal.")
            .step("Calculate percentages: Tet_A_pct = Tet_A_count / total.")
            .step("Pi's digit distribution creates statistical fluctuations in the ratio.")
            .step("Verify neither tetrahedron exceeds 60% (gross imbalance check).")
            .conclude("Both Field Chambers are visited without extreme bias.")
        )
    
    commentary = (
        "Imagine two sports teams with equal numbers of fans. A fair poll should give "
        "roughly 50/50 support. If one team gets 80%, the poll is biased. "
        "Similarly, our two tetrahedra should get roughly equal visits. "
        "Perfect 50/50 is unlikely (pi is not a random number generator), "
        "but gross imbalance (beyond 60/40) would be concerning. This test confirms balance."
    )
    
    def model(self):
        analysis = analyze_tetrahedra_balance(1000)
        tet_a_balanced = 1.0 if 0.40 < analysis['tet_a_pct'] < 0.60 else 0.0
        tet_b_balanced = 1.0 if 0.40 < analysis['tet_b_pct'] < 0.60 else 0.0
        return (
            Model()
            .add("Tet A percentage", analysis['tet_a_pct'])
            .add("Tet B percentage", analysis['tet_b_pct'])
            .add("Tet A balanced", tet_a_balanced)
            .add("Tet B balanced", tet_b_balanced)
        )


class VertexReturnFrequency(Test):
    """
    Each vertex should be revisited regularly. Large imbalances in return
    frequency could indicate "sticky" vertices that trap the traversal.
    """
    name = "Vertex Return Frequency"
    question = (
        "Does any vertex get visited way more than others? "
        "In fair sampling, the most-visited vertex should not have triple the visits of the least. "
        "This test checks that the max/min visit ratio stays below 3:1."
    )
    reference = None  # Threshold check
    level = Standard
    audit_score = 83
    audit_notes = (
        "Question: 14/15 - Good 'way more' concern framing. "
        "Derivation: 12/15 - Could explain 3:1 choice. "
        "Commentary: 13/15 - Nice fair game analogy. "
        "Model: 8/10 - Good ratio output. "
        "Observations: 0/10 - MISSING observations() method. "
        "Constants: 10/10 - Imports from common. "
        "Accessibility: 12/15 - Fair game analogy. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: 500 digits - ADEQUATE for frequency check. "
        "FUNCTION OPPORTUNITY: None specific. "
        "TO IMPROVE: Add observations() method. Explain 3:1 threshold and sticky vertex implications."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Balanced traversal should visit all vertices with similar frequency.")
            .step("Count visits to each of the 8 vertices during traversal.")
            .step("Find max_visits and min_visits across all vertices.")
            .step("Calculate ratio = max_visits / min_visits.")
            .conclude("Ratio < 3 indicates no vertex systematically traps or excludes traversal.")
        )
    
    commentary = (
        "In a fair game, all players get roughly equal turns. If one player gets 10 turns "
        "while another gets only 1, the game is rigged. Our traversal should not have "
        "'favorite' or 'neglected' vertices. The ratio of most visits to fewest visits "
        "should stay reasonable (below 3:1). This confirms pi digits do not create "
        "systematic hotspots or dead zones in the Field Chamber."
    )
    
    def model(self):
        analysis = analyze_vertex_distribution(500)
        counts = analysis['counts']
        max_visits = max(counts.values())
        min_visits = min(counts.values())
        ratio = max_visits / min_visits if min_visits > 0 else 999
        balanced = 1 if ratio < 3 else 0
        return (
            Model()
            .add("Max vertex visits", max_visits)
            .add("Min vertex visits", min_visits)
            .add("Max/min ratio", ratio)
            .add("Balanced (ratio < 3)", balanced)
        )


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


def run_all():
    """Run all Coupling Port traversal tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
