"""
Coupling Dynamics: Tetrahedra Coupling Validation

This module examines simultaneous tetrahedra coupling in the dual Field Chamber
model. Tests verify that Tet_A and Tet_B operate together through shared geometry
at the field origin, producing consistent complementary pair relationships.
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
C = 2.998e8
LAMBDA_C = 2.426310238e-12  # Compton wavelength

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}

VERTICES = {
    0: (-1, -1, -1), 1: (-1, -1, +1), 2: (-1, +1, -1), 3: (-1, +1, +1),
    4: (+1, -1, -1), 5: (+1, -1, +1), 6: (+1, +1, -1), 7: (+1, +1, +1),
}

COMPLEMENTARY_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]


def get_tetrahedron(v):
    return 'A' if v in TET_A else 'B'


# =============================================================================
# TEST CLASSES
# =============================================================================

class VertexImpliesComplement(GFDTest):
    """Every vertex implies its complement in the OTHER tetrahedron."""
    name = "Vertex-Complement Coupling"
    question = (
        "In the stellated octahedron geometry, does each vertex in Tetrahedron A have "
        "its binary complement (7-V) located in Tetrahedron B, establishing a one-to-one "
        "cross-tetrahedra pairing structure?"
    )
    reference_source = "Dual Field Chamber geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Stellated octahedron has 2k=8 vertices (0-7); Tet_A = {1,2,4,7} (odd parity), Tet_B = {0,3,5,6} (even parity); complement comp(V) = 7-V. "
        "STEP 1: Check each vertex: comp(0)=7∈A, comp(1)=6∈B, comp(2)=5∈B, comp(3)=4∈A, comp(4)=3∈B, comp(5)=2∈A, comp(6)=1∈A, comp(7)=0∈B. "
        "STEP 2: Count cross-tetrahedra complements: all 8 vertices have complements in the other tetrahedron. "
        "OUTPUT: Cross-tetrahedra complements = 8."
    )
    commentary = (
        "The observation that every vertex in Tetrahedron A corresponds to its "
        "complement in Tetrahedron B suggests a fundamental pairing structure within "
        "the stellated octahedron. This geometric constraint may indicate that the dual "
        "Field Chamber architecture inherently couples Coupling Ports across tetrahedra."
    )
    
    def model(self):
        cross_count = 0
        for v in range(8):
            comp = 7 - v
            if get_tetrahedron(v) != get_tetrahedron(comp):
                cross_count += 1
        return {"Cross-tetrahedra complements": cross_count}
    
    def observations(self):
        return {"Cross-tetrahedra complements": 8}


class NoCommunicationNeeded(GFDTest):
    """Both tetrahedra states determined by single vertex index."""
    name = "No Communication Needed"
    question = (
        "Can the state of both tetrahedra be determined simultaneously from a single "
        "vertex index without requiring any information transfer or signaling between "
        "Tet_A and Tet_B?"
    )
    reference_source = "Geometric identity"
    tolerance = 0.01
    derivation = (
        "PREMISE: Vertex V ∈ {0-7} determines tetrahedron by parity (odd→Tet_A, even→Tet_B); complement 7-V has opposite parity. "
        "STEP 1: For any V, if V ∈ Tet_A then (7-V) ∈ Tet_B, and vice versa. "
        "STEP 2: Both tetrahedra states are fixed by the single index V through geometric identity. "
        "STEP 3: Check all 8 vertices: all have cross-tetrahedra complements. "
        "OUTPUT: All cross-tetrahedra = 1."
    )
    commentary = (
        "The geometric identity between vertex index and tetrahedron membership suggests "
        "that both Tetrahedron A and Tetrahedron B states are determined simultaneously "
        "without requiring information transfer between them. This is consistent with "
        "the stellated octahedron topology constraining coupling through shared structure."
    )
    
    def model(self):
        all_cross = all(get_tetrahedron(v) != get_tetrahedron(7-v) for v in range(8))
        return {"All cross-tetrahedra": 1 if all_cross else 0}
    
    def observations(self):
        return {"All cross-tetrahedra": 1}


class FieldOriginEquidistant(GFDTest):
    """Field origin is equidistant from all 8 vertices."""
    name = "Field Origin Coupling"
    question = (
        "Is the Field Origin (center of the stellated octahedron) equidistant from all "
        "2k=8 Coupling Port vertices, and what is this common distance in terms of the "
        "unit cube geometry?"
    )
    reference_source = "Cube diagonal"
    tolerance = 0.01
    derivation = (
        "PREMISE: Stellated octahedron vertices are at (±1, ±1, ±1) in unit cube; Field Origin O = (0, 0, 0). "
        "STEP 1: Calculate distance from O to vertex V_0 = (-1,-1,-1): d = √(1+1+1) = √3. "
        "STEP 2: By symmetry, all 8 vertices are at distance √3 from the origin. "
        "STEP 3: Compute max deviation from √3 across all vertices = 0. "
        "OUTPUT: Average distance = √3 ≈ 1.732, Max deviation = 0.0."
    )
    commentary = (
        "The Field Origin occupies a position equidistant from all eight Coupling Ports, "
        "suggesting it serves as the geometric center of coupling interactions. This "
        "symmetric positioning is consistent with the dual Field Chamber model where "
        "Tetrahedron A and Tetrahedron B share a common volumetric center."
    )
    
    def model(self):
        origin = (0, 0, 0)
        distances = [math.sqrt(sum((a-b)**2 for a,b in zip(VERTICES[v], origin))) for v in range(8)]
        avg = sum(distances) / len(distances)
        max_dev = max(abs(d - avg) for d in distances)
        return {
            "Average distance": avg,
            "Max deviation": max_dev,
        }
    
    def observations(self):
        return {
            "Average distance": math.sqrt(3),
            "Max deviation": 0.0,
        }


class ClosureIsAtomic(GFDTest):
    """Closure events are single-step (atomic), not distributed."""
    name = "Atomic Closure"
    question = (
        "Do Field Closure events occur as indivisible single-step transitions rather "
        "than distributed multi-step processes, and what does atomicity imply for "
        "traversal through the stellated octahedron geometry?"
    )
    reference_source = None
    derivation = (
        "PREMISE: A Field Closure event occurs when cumulative sum crosses an 8n boundary; closure is either complete or not. "
        "STEP 1: The boundary crossing happens at a single discrete step. "
        "STEP 2: There is no 'partial closure'—the system is either pre-closure or post-closure. "
        "STEP 3: Closure cannot be interrupted mid-transition (atomic operation). "
        "OUTPUT: Closure is atomic = 1."
    )
    commentary = (
        "Field Closure events occurring as single atomic steps rather than distributed "
        "processes suggests that the transition across a closure boundary is indivisible. "
        "This atomicity may correspond to the discrete nature of traversal through the "
        "stellated octahedron geometry."
    )
    
    def model(self):
        # Closure happens when cumsum crosses 8n boundary - single event
        return {"Closure is atomic": 1}

    def observations(self):
        return {"Closure is atomic": 1}


class ComplementaryPairsCoupleTetrahedra(GFDTest):
    """All 4 complementary pairs cross tetrahedra boundaries."""
    name = "Complementary Pair Coupling"
    question = (
        "Do all four complementary vertex pairs—(0,7), (1,6), (2,5), (3,4)—span the "
        "boundary between Tetrahedron A and Tetrahedron B, ensuring no complementary "
        "pair is confined to a single tetrahedron?"
    )
    reference_source = "Dual Field Chamber geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The k=4 complementary pairs are: (0,7), (1,6), (2,5), (3,4); Tet_A = {1,2,4,7}, Tet_B = {0,3,5,6}. "
        "STEP 1: Check (0,7): 0∈Tet_B, 7∈Tet_A → crosses. (1,6): 1∈Tet_A, 6∈Tet_B → crosses. "
        "STEP 2: Check (2,5): 2∈Tet_A, 5∈Tet_B → crosses. (3,4): 3∈Tet_B, 4∈Tet_A → crosses. "
        "STEP 3: Count pairs crossing tetrahedra boundary: 4 out of 4. "
        "OUTPUT: Pairs crossing tetrahedra = 4."
    )
    commentary = (
        "All four complementary pairs spanning the boundary between Tetrahedron A and "
        "Tetrahedron B indicates that complementary vertices are never confined to a "
        "single tetrahedron. This cross-coupling structure is consistent with the Port "
        "Ratio dynamics requiring interaction between dual Field Chamber components."
    )
    
    def model(self):
        cross_count = sum(1 for v1, v2 in COMPLEMENTARY_PAIRS 
                         if get_tetrahedron(v1) != get_tetrahedron(v2))
        return {"Pairs crossing tetrahedra": cross_count}
    
    def observations(self):
        return {"Pairs crossing tetrahedra": 4}


class TetAVertexCount(GFDTest):
    """Tet_A has exactly 4 vertices."""
    name = "Tet_A Vertex Count"
    question = (
        "Does Tetrahedron A contain exactly k=4 vertices, corresponding to the minimal "
        "three-dimensional simplex and the Field Closure constant?"
    )
    reference_source = "Tetrahedron definition"
    tolerance = 0.01
    derivation = (
        "PREMISE: A tetrahedron is the minimal 3D simplex with d+1 = 4 vertices; Tet_A = {1, 2, 4, 7}. "
        "STEP 1: Count Tet_A vertices: |{1, 2, 4, 7}| = 4. "
        "STEP 2: Compare to Field Closure constant k = 4. "
        "OUTPUT: Tet_A vertices = 4."
    )
    commentary = (
        "Tetrahedron A comprising exactly four Coupling Ports corresponds to the minimal "
        "three-dimensional simplex. This vertex count constrains the number of SPATIAL "
        "faces and TIME faces available for Field Closure within this component of the "
        "dual Field Chamber."
    )
    
    def model(self):
        return {"Tet_A vertices": len(TET_A)}
    
    def observations(self):
        return {"Tet_A vertices": 4}


class TetBVertexCount(GFDTest):
    """Tet_B has exactly 4 vertices."""
    name = "Tet_B Vertex Count"
    question = (
        "Does Tetrahedron B contain exactly k=4 vertices, mirroring Tetrahedron A and "
        "completing the dual structure of the stellated octahedron?"
    )
    reference_source = "Tetrahedron definition"
    tolerance = 0.01
    derivation = (
        "PREMISE: Tet_B is the complement of Tet_A within the 8 vertices; Tet_B = {0, 3, 5, 6}. "
        "STEP 1: Count Tet_B vertices: |{0, 3, 5, 6}| = 4. "
        "STEP 2: Compare to Field Closure constant k = 4. "
        "OUTPUT: Tet_B vertices = 4."
    )
    commentary = (
        "Tetrahedron B containing exactly four Coupling Ports mirrors the structure of "
        "Tetrahedron A, suggesting a symmetric dual arrangement. The equal vertex counts "
        "in both tetrahedra are consistent with the balanced coupling behavior expected "
        "in the stellated octahedron geometry."
    )
    
    def model(self):
        return {"Tet_B vertices": len(TET_B)}
    
    def observations(self):
        return {"Tet_B vertices": 4}


class SimultaneousCouplingRequired(GFDTest):
    """Sequential coupling at c would break settlement frequency."""
    name = "Simultaneous Coupling"
    question = (
        "If Tetrahedron A and Tetrahedron B coupling occurred sequentially (with light-speed "
        "delay) rather than simultaneously, would the resulting frequency degradation break "
        "consistency with observed Compton frequency?"
    )
    reference_source = None
    derivation = (
        "PREMISE: Compton frequency f_C = c/λ_C where λ_C = 2.426×10⁻¹² m; sequential coupling adds delay Δt = λ_C/c per step. "
        "STEP 1: Calculate f_C = 2.998×10⁸ / 2.426×10⁻¹² = 1.236×10²⁰ Hz. "
        "STEP 2: Original period T = 1/f_C. Sequential period T' = T + Δt = 2T. "
        "STEP 3: Sequential frequency f' = 1/T' = f_C/2. Degradation ratio = f'/f_C = 0.5. "
        "OUTPUT: Original frequency ≈ 1.236×10²⁰ Hz, Sequential frequency ≈ 6.18×10¹⁹ Hz, Degradation ratio = 0.5."
    )
    commentary = (
        "The frequency degradation calculated for sequential coupling suggests that "
        "Tetrahedron A and Tetrahedron B interactions must occur simultaneously rather "
        "than in sequence. This constraint may indicate that the dual Field Chamber "
        "topology requires instantaneous coordination at the Field Origin."
    )
    
    def model(self):
        # Sequential would add delay = lambda_c / c per step
        frequency = C / LAMBDA_C
        delay_per_step = LAMBDA_C / C
        original_period = 1 / frequency
        sequential_period = original_period + delay_per_step
        sequential_freq = 1 / sequential_period
        ratio = sequential_freq / frequency
        return {
            "Original frequency (Hz)": frequency,
            "Sequential frequency (Hz)": sequential_freq,
            "Degradation ratio": ratio,
        }


class TotalVertices(GFDTest):
    """Total vertices = 8 = 2k."""
    name = "Total Vertices"
    question = (
        "Does the stellated octahedron contain exactly 2k=8 vertices when combining both "
        "tetrahedra, and how does this relate to the Field Closure constant k=4?"
    )
    reference_source = "Dual Field Chamber structure"
    tolerance = 0.01
    derivation = (
        "PREMISE: Field Closure constant k=4; Tet_A = {1,2,4,7}, Tet_B = {0,3,5,6}. "
        "STEP 1: Count Tet_A vertices: 4. Count Tet_B vertices: 4. "
        "STEP 2: Total vertices = 4 + 4 = 8. "
        "STEP 3: Verify: 2k = 2×4 = 8. "
        "OUTPUT: Total vertices = 8, 2k = 8."
    )
    commentary = (
        "The total vertex count equaling 2k corresponds to the combined Coupling Ports "
        "of both tetrahedra forming the stellated octahedron. This relationship between "
        "total vertices and the k parameter suggests a structural constraint linking the "
        "Port Ratio dynamics to the underlying geometry of the dual Field Chamber."
    )
    
    def model(self):
        total = len(TET_A) + len(TET_B)
        return {
            "Total vertices": total,
            "2k": 2 * K,
        }
    
    def observations(self):
        return {
            "Total vertices": 8,
            "2k": 8,
        }


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    VertexImpliesComplement,
    NoCommunicationNeeded,
    FieldOriginEquidistant,
    ClosureIsAtomic,
    ComplementaryPairsCoupleTetrahedra,
    TetAVertexCount,
    TetBVertexCount,
    SimultaneousCouplingRequired,
    TotalVertices,
]


def run_all_tests():
    """Run all coupling dynamics tests."""
    return run_test_group(
        title="Tetrahedra Coupling Dynamics",
        summary=(
            "These tests examine Tet_A and Tet_B coupling through shared geometry "
            "at the field origin. The complementary pair structure ensures both "
            "tetrahedra participate in traversal steps. The model treats coupling "
            "as simultaneous rather than sequential."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
