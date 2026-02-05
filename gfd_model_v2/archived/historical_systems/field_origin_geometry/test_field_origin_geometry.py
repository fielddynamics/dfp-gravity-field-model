"""
Reference Systems: Field Origin Geometry Validation

This module validates geometric properties of the field origin point - the center
of the dual Field Chamber structure where compression vectors cancel. Tests verify
equidistance from vertices and vector cancellation at the origin.
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, run_test_group


# =============================================================================
# CONSTANTS
# =============================================================================

# Vertex coordinates (cube corners at +/-1)
VERTICES = {
    0: (-1, -1, -1),  # 000
    1: (-1, -1, +1),  # 001
    2: (-1, +1, -1),  # 010
    3: (-1, +1, +1),  # 011
    4: (+1, -1, -1),  # 100
    5: (+1, -1, +1),  # 101
    6: (+1, +1, -1),  # 110
    7: (+1, +1, +1),  # 111
}

TET_A = {1, 2, 4, 7}  # Odd parity vertices
TET_B = {0, 3, 5, 6}  # Even parity vertices


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def vector_subtract(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vector_add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vector_magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)


# =============================================================================
# TEST CLASSES
# =============================================================================

class FieldOriginAtCenter(GFDTest):
    """Field origin is at the geometric center (centroid) of all vertices."""
    name = "Field Origin Location"
    question = (
        "Is the Field Origin—the point where Tetrahedron A and Tetrahedron B interpenetrate—located at the "
        "geometric centroid of all 2k=8 vertices, which in the standard coordinate system is (0, 0, 0)?"
    )
    reference_source = "Geometric centroid definition"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Origin is defined as the center point of the dual Field Chamber. "
        "STEP 1: The 2k=8 vertices are located at cube corners with coordinates (±1, ±1, ±1). "
        "STEP 2: The centroid is the arithmetic mean: C = (Σxᵢ/8, Σyᵢ/8, Σzᵢ/8). "
        "STEP 3: By symmetry, positive and negative coordinates cancel: Σxᵢ = Σyᵢ = Σzᵢ = 0. "
        "STEP 4: Therefore C = (0, 0, 0). "
        "OUTPUT: Distance from origin = 0.0."
    )
    commentary = (
        "The Field Origin at geometric center (0, 0, 0) corresponds to the point of maximum symmetry in the Field "
        "Chamber. This location represents the natural reference point from which all eight Coupling Ports are "
        "equidistant."
    )
    
    def model(self):
        # Calculate centroid of all vertices
        cx = sum(VERTICES[v][0] for v in range(8)) / 8
        cy = sum(VERTICES[v][1] for v in range(8)) / 8
        cz = sum(VERTICES[v][2] for v in range(8)) / 8
        dist_from_origin = math.sqrt(cx**2 + cy**2 + cz**2)
        return {"Distance from origin": dist_from_origin}
    
    def observations(self):
        return {"Distance from origin": 0.0}


class EquidistantFromVertices(GFDTest):
    """Field origin is equidistant from all 8 vertices."""
    name = "Equidistant from Vertices"
    question = (
        "Is the Field Origin equidistant from all 2k=8 Coupling Port vertices, confirming that "
        "it occupies a position of perfect geometric symmetry within the stellated octahedron?"
    )
    reference_source = "Cube diagonal = sqrt(3) for unit cube"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Origin is at (0, 0, 0) and vertices are at (±1, ±1, ±1). "
        "STEP 1: The distance from origin to any vertex is d = √((±1)² + (±1)² + (±1)²). "
        "STEP 2: Since (±1)² = 1 for any sign, d = √(1 + 1 + 1) = √3. "
        "STEP 3: This calculation is identical for all 2^d = 8 vertex combinations. "
        "OUTPUT: Average distance = √3 ≈ 1.732; Max deviation = 0.0."
    )
    commentary = (
        "The equidistant property of the Field Origin is consistent with the symmetry requirements of a dual-tetrahedra "
        "structure. The sqrt(3) distance corresponds to the body diagonal of a unit cube, establishing a natural "
        "length scale for the coordinate system."
    )
    
    def model(self):
        origin = (0, 0, 0)
        distances = [vector_magnitude(vector_subtract(VERTICES[v], origin)) for v in range(8)]
        avg_distance = sum(distances) / len(distances)
        max_deviation = max(abs(d - avg_distance) for d in distances)
        return {
            "Average distance": avg_distance,
            "Max deviation": max_deviation,
        }
    
    def observations(self):
        expected = math.sqrt(3)
        return {
            "Average distance": expected,
            "Max deviation": 0.0,
        }


class CompressionVectorsCancel(GFDTest):
    """Compression vectors from all vertices sum to zero at origin."""
    name = "Vector Cancellation"
    question = (
        "If we define compression vectors pointing from each of the 2k=8 vertices toward the Field Origin, "
        "does their vector sum equal zero, indicating a state of equilibrium at the center?"
    )
    reference_source = "Symmetric structure requirement"
    tolerance = 0.01
    derivation = (
        "PREMISE: Define compression vector vᵢ = Origin - Vertexᵢ for each vertex i. "
        "STEP 1: For vertex at (+1, +1, +1): v = (0,0,0) - (+1,+1,+1) = (-1,-1,-1). "
        "STEP 2: For vertex at (-1,-1,-1): v = (0,0,0) - (-1,-1,-1) = (+1,+1,+1). "
        "STEP 3: These form an antipodal pair that sums to zero. "
        "STEP 4: All 8 vertices form 4 such antipodal pairs: (0,7), (1,6), (2,5), (3,4). "
        "OUTPUT: Vector sum magnitude = 0.0."
    )
    commentary = (
        "The cancellation of compression vectors at the Field Origin is consistent with a state of equilibrium. "
        "This property suggests that the Field Origin may be characterized as a point of zero net force in a "
        "symmetric potential."
    )
    
    def model(self):
        origin = (0, 0, 0)
        total = (0.0, 0.0, 0.0)
        
        for v in range(8):
            vec = vector_subtract(origin, VERTICES[v])
            total = vector_add(total, vec)
        
        magnitude = vector_magnitude(total)
        return {"Vector sum magnitude": magnitude}
    
    def observations(self):
        return {"Vector sum magnitude": 0.0}


class BimetricBalance(GFDTest):
    """Tet A and Tet B vector contributions are equal and opposite."""
    name = "Bimetric Balance"
    question = (
        "When the compression vectors are summed separately for Tetrahedron A (k=4 vertices) and "
        "Tetrahedron B (k=4 vertices), are the resulting vectors equal in magnitude and opposite in direction?"
    )
    reference_source = "Dual tetrahedra symmetry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Tetrahedron A uses odd-parity vertices {1,2,4,7}; Tetrahedron B uses even-parity {0,3,5,6}. "
        "STEP 1: Sum vectors for Tet A: Σ_A = Σᵢ∈A (Origin - Vᵢ). "
        "STEP 2: Sum vectors for Tet B: Σ_B = Σⱼ∈B (Origin - Vⱼ). "
        "STEP 3: Each vertex in Tet A has an antipodal partner in Tet B (via XOR with 7). "
        "STEP 4: By the antipodal relationship: Σ_A = -Σ_B. "
        "OUTPUT: Combined Tet A + Tet B magnitude = 0.0."
    )
    commentary = (
        "The equal and opposite contributions from Tetrahedron A and Tetrahedron B suggest a balanced bimetric "
        "structure at the Field Origin. This cancellation is consistent with the complementary nature of the "
        "dual Field Chamber."
    )
    
    def model(self):
        origin = (0, 0, 0)
        
        total_a = (0.0, 0.0, 0.0)
        for v in TET_A:
            vec = vector_subtract(origin, VERTICES[v])
            total_a = vector_add(total_a, vec)
        
        total_b = (0.0, 0.0, 0.0)
        for v in TET_B:
            vec = vector_subtract(origin, VERTICES[v])
            total_b = vector_add(total_b, vec)
        
        combined = vector_add(total_a, total_b)
        magnitude = vector_magnitude(combined)
        
        return {"Combined Tet A + Tet B magnitude": magnitude}
    
    def observations(self):
        return {"Combined Tet A + Tet B magnitude": 0.0}


class InnerOctahedronVertices(GFDTest):
    """Inner octahedron vertices are at unit distance from origin."""
    name = "Inner Octahedron"
    question = (
        "Does the inner octahedron—formed by the face centers of the containing cube—have its vertices "
        "at unit distance from the Field Origin, establishing an intermediate geometric scale?"
    )
    reference_source = "Cube edge midpoints"
    tolerance = 0.01
    derivation = (
        "PREMISE: The inner octahedron has vertices at the centers of the cube's 6 faces. "
        "STEP 1: Cube face centers are at (±1,0,0), (0,±1,0), (0,0,±1). "
        "STEP 2: Distance from origin to (1,0,0) is √(1² + 0² + 0²) = 1. "
        "STEP 3: By symmetry, all 6 face centers are at distance 1 from the origin. "
        "STEP 4: Compare to Coupling Port distance √3 ≈ 1.732. "
        "OUTPUT: Inner octahedron vertex distance = 1.0."
    )
    commentary = (
        "The unit distance of inner octahedron vertices from the Field Origin corresponds to the face midpoints "
        "of the containing cube. This relationship may indicate a natural intermediate scale between the Field "
        "Origin and the Coupling Ports."
    )
    
    def model(self):
        # Inner octahedron vertices are at +/-1 on each axis
        inner_vertices = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
        ]
        
        origin = (0, 0, 0)
        distances = [vector_magnitude(vector_subtract(v, origin)) for v in inner_vertices]
        avg_distance = sum(distances) / len(distances)
        
        return {"Inner octahedron vertex distance": avg_distance}
    
    def observations(self):
        return {"Inner octahedron vertex distance": 1.0}


class TetAContribution(GFDTest):
    """Tet A vector sum has expected structure."""
    name = "Tet A Vector Sum"
    question = (
        "What is the magnitude of the compression vector sum from Tetrahedron A's k=4 odd-parity vertices "
        "{1, 2, 4, 7}, and does it reflect the expected tetrahedral symmetry?"
    )
    reference_source = None
    derivation = (
        "PREMISE: Tetrahedron A comprises vertices with odd bit-parity: {1, 2, 4, 7}. "
        "STEP 1: Vertex positions: V1=(-1,-1,+1), V2=(-1,+1,-1), V4=(+1,-1,-1), V7=(+1,+1,+1). "
        "STEP 2: Compression vectors (origin - vertex): v1=(+1,+1,-1), v2=(+1,-1,+1), v4=(-1,+1,+1), v7=(-1,-1,-1). "
        "STEP 3: Vector sum: Σ_A = (1+1-1-1, 1-1+1-1, -1+1+1-1) = (0, 0, 0). "
        "OUTPUT: Tet A sum magnitude = 0.0; Tet A vertex count = 4."
    )
    commentary = (
        "The symmetric structure of the Tetrahedron A vector sum is consistent with the odd-parity vertex "
        "classification (1, 2, 4, 7). This configuration corresponds to one of the two interlocking tetrahedra "
        "in the Field Chamber."
    )
    
    def model(self):
        origin = (0, 0, 0)
        total = (0.0, 0.0, 0.0)
        for v in TET_A:
            vec = vector_subtract(origin, VERTICES[v])
            total = vector_add(total, vec)
        
        return {
            "Tet A sum magnitude": vector_magnitude(total),
            "Tet A vertex count": len(TET_A),
        }


class TetBContribution(GFDTest):
    """Tet B vector sum has expected structure."""
    name = "Tet B Vector Sum"
    question = (
        "What is the magnitude of the compression vector sum from Tetrahedron B's k=4 even-parity vertices "
        "{0, 3, 5, 6}, and is it equal and opposite to Tetrahedron A's contribution?"
    )
    reference_source = None
    derivation = (
        "PREMISE: Tetrahedron B comprises vertices with even bit-parity: {0, 3, 5, 6}. "
        "STEP 1: Vertex positions: V0=(-1,-1,-1), V3=(-1,+1,+1), V5=(+1,-1,+1), V6=(+1,+1,-1). "
        "STEP 2: Compression vectors (origin - vertex): v0=(+1,+1,+1), v3=(+1,-1,-1), v5=(-1,+1,-1), v6=(-1,-1,+1). "
        "STEP 3: Vector sum: Σ_B = (1+1-1-1, 1-1+1-1, 1-1-1+1) = (0, 0, 0). "
        "OUTPUT: Tet B sum magnitude = 0.0; Tet B vertex count = 4."
    )
    commentary = (
        "The symmetric structure of the Tetrahedron B vector sum is consistent with the even-parity vertex "
        "classification (0, 3, 5, 6). This configuration corresponds to the complement of Tetrahedron A in "
        "the stellated octahedron."
    )
    
    def model(self):
        origin = (0, 0, 0)
        total = (0.0, 0.0, 0.0)
        for v in TET_B:
            vec = vector_subtract(origin, VERTICES[v])
            total = vector_add(total, vec)
        
        return {
            "Tet B sum magnitude": vector_magnitude(total),
            "Tet B vertex count": len(TET_B),
        }


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    FieldOriginAtCenter,
    EquidistantFromVertices,
    CompressionVectorsCancel,
    BimetricBalance,
    InnerOctahedronVertices,
    TetAContribution,
    TetBContribution,
]


def run_all_tests():
    """Run all field origin geometry tests."""
    return run_test_group(
        title="Field Origin Geometry Validation",
        summary=(
            "These tests examine the geometric properties of the field origin, "
            "the central point where Tet_A and Tet_B meet in the dual Field Chamber. "
            "The origin is equidistant from all vertices and is the point where "
            "vector contributions balance."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
