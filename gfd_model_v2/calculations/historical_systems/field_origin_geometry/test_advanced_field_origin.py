"""
Advanced Field Origin Properties: Information and Symmetry

This module examines additional properties of the Field Origin point beyond
basic geometry. Some tests explore speculative connections (marked EXPLORATORY);
others verify concrete mathematical properties (marked STANDARD).

THE PHYSICAL CLAIM:
The Field Origin at (0,0,0) has special properties related to information
content, dimensional structure, and energy minimization. These go beyond
simple geometry to touch on information theory and optimization.

CAVEAT: Exploratory tests document mathematical relationships without claiming
they have physical significance. They are included to explore the structure.
"""

import math
from gfd_model_v2.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Closure constant
D = K - 1  # = 3 spatial dimensions
SQRT_3 = math.sqrt(3)

# Vertex coordinates (cube corners at +/-1)
VERTICES = {
    0: (-1, -1, -1),
    1: (-1, -1, +1),
    2: (-1, +1, -1),
    3: (-1, +1, +1),
    4: (+1, -1, -1),
    5: (+1, -1, +1),
    6: (+1, +1, -1),
    7: (+1, +1, +1),
}


# =============================================================================
# TEST CLASSES
# =============================================================================

class OriginSphericalSymmetry(Test):
    """Compression vectors cancel spherically at the Field Origin."""
    name = "Origin Spherical Symmetry"
    level = Level.STANDARD
    question = (
        "If we define vectors pointing from each vertex toward the origin, "
        "does their sum equal zero (complete cancellation)?"
    )
    reference = "Vector addition for symmetric point sets"
    tolerance = 0.01
    commentary = (
        "The 8 vertices form 4 antipodal pairs. Each pair contributes two "
        "opposite vectors that cancel. Therefore the total vector sum is zero. "
        "This is a fundamental property of the cube's central symmetry."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Define compression vector from vertex V_i as: c_i = O - V_i = -V_i.")
            .step("The 8 vertices form 4 antipodal pairs: (0,7), (1,6), (2,5), (3,4).")
            .step("For pair (i, 7-i): V_i + V_(7-i) = 0 (opposite coordinates).")
            .step("Therefore: c_i + c_(7-i) = -V_i - V_(7-i) = 0.")
            .step("Sum over all vertices: sum(c_i) = 0.")
            .conclude("Vector sum magnitude = 0.0.")
        )
    
    def model(self):
        # Sum vectors from each vertex toward origin
        total = [0.0, 0.0, 0.0]
        for v in VERTICES.values():
            for i in range(3):
                total[i] += -v[i]  # Vector from v toward origin
        
        magnitude = math.sqrt(sum(x**2 for x in total))
        return Model().add("Vector sum magnitude", magnitude)
    
    def observations(self):
        return Observed().add("Vector sum magnitude", 0.0)


class DimensionalHierarchy(Test):
    """The Field Chamber contains a complete dimensional hierarchy."""
    name = "Dimensional Hierarchy"
    level = Level.STANDARD
    question = (
        "Does the stellated octahedron contain geometric elements of all "
        "dimensions from 0D (point) to 3D (volume)?"
    )
    reference = "Euler characteristic for polyhedra"
    tolerance = 0.01
    commentary = (
        "The structure has: 1 central point (0D), 12 edges (1D), 8 triangular "
        "faces (2D), and 1 enclosed region (3D). This is a complete hierarchy. "
        "Note: the edge count is 12, not 24, because edges of the two tetrahedra "
        "are distinct, not shared."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("0D: 1 Field Origin point.")
            .step("1D: Each tetrahedron has 6 edges; the two tetrahedra share no edges.")
            .step("    Total edges = 6 + 6 = 12.")
            .step("2D: Each tetrahedron has 4 triangular faces.")
            .step("    Total faces = 4 + 4 = 8.")
            .step("3D: 1 enclosed volume (the intersection region).")
            .conclude("0D: 1, 1D: 12, 2D: 8, 3D: 1.")
        )
    
    def model(self):
        origin_points = 1
        edges = 12  # 6 per tetrahedron, no sharing
        faces = 8   # 4 per tetrahedron
        volumes = 1
        
        return (
            Model()
            .add("0D elements (origin)", origin_points)
            .add("1D elements (edges)", edges)
            .add("2D elements (faces)", faces)
            .add("3D elements (volume)", volumes)
        )
    
    def observations(self):
        return (
            Observed()
            .add("0D elements (origin)", 1.0)
            .add("1D elements (edges)", 12.0)
            .add("2D elements (faces)", 8.0)
            .add("3D elements (volume)", 1.0)
        )


class OriginMinimizesDistanceSquaredSum(Test):
    """Field Origin minimizes sum of squared distances to all vertices."""
    name = "Distance Squared Minimum"
    level = Level.STANDARD
    question = (
        "Is the Field Origin the unique point that minimizes the sum of "
        "squared distances to all 8 vertices?"
    )
    reference = "Centroid minimizes sum of squared distances"
    tolerance = 0.01
    commentary = (
        "This is a standard result: for any point set, the centroid minimizes "
        "the sum of squared distances. Since the centroid of the 8 vertices is "
        "(0,0,0), the origin is this minimum. Any displacement increases the sum."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("For point P, let f(P) = sum over i of |P - V_i|^2.")
            .step("The gradient of f is: grad f = 8P - sum(V_i) = 8P - 0 = 8P.")
            .step("Setting grad f = 0 gives P = 0 (the origin).")
            .step("At origin: f(O) = sum |V_i|^2 = 8 x 3 = 24.")
            .step("At displaced point: f(P) > 24 for any P != O.")
            .conclude("Sum d^2 at origin = 24.0; origin is unique minimum.")
        )
    
    def model(self):
        origin = (0, 0, 0)
        total_dist_sq = 0
        for v in VERTICES.values():
            dist_sq = sum((v[i] - origin[i])**2 for i in range(3))
            total_dist_sq += dist_sq
        
        # Verify with a displaced point
        displaced = (0.1, 0.1, 0.1)
        displaced_sum = 0
        for v in VERTICES.values():
            dist_sq = sum((v[i] - displaced[i])**2 for i in range(3))
            displaced_sum += dist_sq
        
        is_minimum = total_dist_sq < displaced_sum
        
        return (
            Model()
            .add("Sum d^2 at origin", total_dist_sq)
            .add("Sum d^2 at displaced point", displaced_sum)
            .add("Origin is minimum", 1.0 if is_minimum else 0.0)
        )
    
    def observations(self):
        # Each vertex is at distance sqrt(3), so d^2 = 3, and 8 x 3 = 24
        displaced_sum = 0
        for v in VERTICES.values():
            displaced_sum += sum((v[i] - 0.1)**2 for i in range(3))
        
        return (
            Observed()
            .add("Sum d^2 at origin", 24.0)
            .add("Sum d^2 at displaced point", displaced_sum)
            .add("Origin is minimum", 1.0)
        )


class InformationEntropyAtOrigin(Test):
    """Maximum entropy for uniform distribution over 8 vertices."""
    name = "Information Entropy"
    level = Level.EXPLORATORY
    question = (
        "If all 8 vertices are equally probable (uniform distribution), what "
        "is the Shannon entropy, and how does it relate to the dimension d=3?"
    )
    reference = "Shannon entropy: H = -sum(p log p)"
    tolerance = 0.01
    commentary = (
        "The maximum entropy for N equally likely outcomes is log_2(N). For "
        "N = 8 = 2^3 vertices, H_max = log_2(8) = 3 bits. This equals d, the "
        "spatial dimension. Whether this has physical meaning is speculative."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Shannon entropy: H = -sum(p_i log_2 p_i).")
            .step("For uniform distribution: p_i = 1/N for all i.")
            .step("H = -N x (1/N) x log_2(1/N) = log_2(N).")
            .step("With N = 8: H = log_2(8) = 3 bits.")
            .step("This equals d = 3 (spatial dimension).")
            .conclude("Max entropy = 3.0 bits = d.")
        )
    
    def model(self):
        n_vertices = 8
        max_entropy = math.log2(n_vertices)  # 3.0
        
        return (
            Model()
            .add("Number of vertices", n_vertices)
            .add("Max entropy (bits)", max_entropy)
            .add("Spatial dimension d", D)
            .add("Entropy equals d", 1.0 if max_entropy == D else 0.0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Number of vertices", 8.0)
            .add("Max entropy (bits)", 3.0)
            .add("Spatial dimension d", 3.0)
            .add("Entropy equals d", 1.0)
        )


class InnerOctahedronStructure(Test):
    """The inner octahedron has 6 vertices at unit distance from origin."""
    name = "Inner Octahedron"
    level = Level.STANDARD
    question = (
        "The cube face centers form an octahedron. Are these 6 points all at "
        "distance 1 from the origin?"
    )
    reference = "Cube-octahedron duality"
    tolerance = 0.01
    commentary = (
        "The 6 face centers of the cube are at (+/-1, 0, 0), (0, +/-1, 0), and "
        "(0, 0, +/-1). Each is at distance 1 from the origin. These form a "
        "regular octahedron inscribed in the cube."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Cube has 6 faces, one perpendicular to each axis direction.")
            .step("Face centers: (+1,0,0), (-1,0,0), (0,+1,0), (0,-1,0), (0,0,+1), (0,0,-1).")
            .step("Distance from origin to (+1,0,0) = sqrt(1+0+0) = 1.")
            .step("By symmetry, all 6 face centers are at distance 1.")
            .step("These 6 points form a regular octahedron.")
            .conclude("Inner octahedron vertex distance = 1.0.")
        )
    
    def model(self):
        face_centers = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
        ]
        
        distances = [math.sqrt(sum(c[i]**2 for i in range(3))) for c in face_centers]
        avg_distance = sum(distances) / len(distances)
        
        return Model().add("Inner octahedron vertex distance", avg_distance)
    
    def observations(self):
        return Observed().add("Inner octahedron vertex distance", 1.0)


class PhaseSpaceCorrespondence(Test):
    """Phase space dimension 2d matches inner octahedron vertex count."""
    name = "Phase Space Dimension"
    level = Level.EXPLORATORY
    question = (
        "In classical mechanics, phase space has 2d dimensions (d positions, "
        "d momenta). Does this match the 6 inner octahedron vertices?"
    )
    reference = "Hamiltonian mechanics"
    tolerance = 0.01
    commentary = (
        "This is a numerical coincidence: 2d = 2 x 3 = 6 = number of octahedron "
        "vertices. Whether this has physical meaning is speculative. The "
        "correspondence is noted but not claimed to be significant."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Phase space has 2d dimensions: d positions + d momenta.")
            .step("For d = 3: phase space dimension = 6.")
            .step("Inner octahedron has 6 vertices (cube face centers).")
            .step("Numerical match: 2d = 6 = octahedron vertices.")
            .step("This is documented as a correspondence, not a claim of causation.")
            .conclude("Phase space dim = 6; Octahedron vertices = 6.")
        )
    
    def model(self):
        phase_space_dim = 2 * D  # 6
        octahedron_vertices = 6
        
        return (
            Model()
            .add("Phase space dimension (2d)", phase_space_dim)
            .add("Octahedron vertices", octahedron_vertices)
            .add("Match", 1.0 if phase_space_dim == octahedron_vertices else 0.0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Phase space dimension (2d)", 6.0)
            .add("Octahedron vertices", 6.0)
            .add("Match", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    OriginSphericalSymmetry,
    DimensionalHierarchy,
    OriginMinimizesDistanceSquaredSum,
    InformationEntropyAtOrigin,
    InnerOctahedronStructure,
    PhaseSpaceCorrespondence,
]


def run_all():
    """Run all advanced field origin tests."""
    return run_tests(
        title="Advanced Field Origin Properties: Information and Symmetry",
        summary=(
            "These tests examine additional properties of the Field Origin. "
            "STANDARD tests verify: spherical symmetry (vector cancellation), "
            "dimensional hierarchy, distance squared minimization, and inner "
            "octahedron structure. EXPLORATORY tests note numerical correspondences "
            "(entropy = d, phase space dim = 6) without claiming physical significance."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
