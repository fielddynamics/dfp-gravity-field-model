"""
Quantum Foundations: Geometric Interpretations

This module examines how foundational quantum mechanical concepts can be
given geometric interpretations in the Field Chamber structure. Some of these
are exact correspondences; others are suggestive analogies.

THE KEY INSIGHT:
Many quantum concepts have natural geometric counterparts when we identify
vertices with basis states. Superposition becomes the centroid, measurement
becomes projection onto vertices, and orthogonal observables correspond to
orthogonal coordinate axes.

CAVEAT: These are mathematical analogies. Whether they reflect actual physics
requires separate investigation. We document the correspondences without
claiming they have operational meaning for GFD.
"""

import math
from gravity_field_model.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Closure constant
D = K - 1  # = 3 spatial dimensions
SQRT_3 = math.sqrt(3)

# Vertex coordinates
VERTICES = {
    0: (-1, -1, -1), 1: (-1, -1, +1), 2: (-1, +1, -1), 3: (-1, +1, +1),
    4: (+1, -1, -1), 5: (+1, -1, +1), 6: (+1, +1, -1), 7: (+1, +1, +1),
}


# =============================================================================
# TEST CLASSES
# =============================================================================

class BasisStateVertexCorrespondence(Test):
    """Each vertex corresponds to a computational basis state."""
    name = "Basis State Correspondence"
    level = Level.STANDARD
    question = (
        "In a 3-qubit system, there are 2^3 = 8 computational basis states. "
        "Does this match the 8 vertices of the cube?"
    )
    reference = "Quantum computing basics"
    tolerance = 0.01
    commentary = (
        "Yes, exactly. The map vertex i <-> |i> (in binary) is a bijection. "
        "This is not a physical claim; it is a counting correspondence."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("3-qubit Hilbert space has dimension 2^3 = 8.")
            .step("Computational basis: {|000>, |001>, ..., |111>}.")
            .step("Cube has 8 vertices: {0, 1, 2, 3, 4, 5, 6, 7}.")
            .step("Bijection: vertex i <-> |bin(i)>.")
            .conclude("Dimension d=3: 2^d = 8 states = 8 vertices.")
        )
    
    def model(self):
        dimension = D
        hilbert_dim = 2 ** D
        vertex_count = len(VERTICES)
        
        return (
            Model()
            .add("Spatial dimension d", dimension)
            .add("Hilbert space dimension 2^d", hilbert_dim)
            .add("Vertex count", vertex_count)
            .add("Match", 1.0 if hilbert_dim == vertex_count else 0.0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Spatial dimension d", 3.0)
            .add("Hilbert space dimension 2^d", 8.0)
            .add("Vertex count", 8.0)
            .add("Match", 1.0)
        )


class SuperpositionAsCentroid(Test):
    """Equal superposition corresponds to the centroid (origin)."""
    name = "Superposition as Centroid"
    level = Level.STANDARD
    question = (
        "If we interpret each vertex as a point mass, the centroid is the "
        "center of mass. Does the equal superposition state |+>^3 'correspond' "
        "to the centroid?"
    )
    reference = "Expectation value of position"
    tolerance = 0.01
    commentary = (
        "In a rough sense, yes. The equal superposition |+>^3 = (1/sqrt(8)) "
        "sum(|i>) gives equal weight to all vertices. The expected position "
        "(average of vertex positions) is the centroid at (0,0,0)."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("|+>^3 = (1/sqrt(8)) x (|000> + |001> + ... + |111>).")
            .step("Expected position = sum of p_i x V_i where p_i = 1/8.")
            .step("= (1/8) x (V_0 + V_1 + ... + V_7).")
            .step("= (1/8) x (0, 0, 0) by cube symmetry.")
            .step("= origin.")
            .conclude("Centroid = (0, 0, 0) = expected position under |+>^3.")
        )
    
    def model(self):
        # Compute centroid
        cx = sum(v[0] for v in VERTICES.values()) / 8
        cy = sum(v[1] for v in VERTICES.values()) / 8
        cz = sum(v[2] for v in VERTICES.values()) / 8
        
        dist_from_origin = math.sqrt(cx**2 + cy**2 + cz**2)
        
        return (
            Model()
            .add("Centroid x", cx)
            .add("Centroid y", cy)
            .add("Centroid z", cz)
            .add("Distance from origin", dist_from_origin)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Centroid x", 0.0)
            .add("Centroid y", 0.0)
            .add("Centroid z", 0.0)
            .add("Distance from origin", 0.0)
        )


class MeasurementAsProjection(Test):
    """Measurement 'collapses' the centroid to a vertex."""
    name = "Measurement as Projection"
    level = Level.EXPLORATORY
    question = (
        "If superposition corresponds to the centroid, can we interpret "
        "measurement as 'projecting' from the centroid to a specific vertex?"
    )
    reference = "Projective measurement postulate"
    tolerance = 0.01
    commentary = (
        "This is an analogy, not a claim. Geometrically, measuring corresponds "
        "to moving from the center (equal superposition) to a specific vertex. "
        "The 'distance' of this collapse is sqrt(3) for all vertices."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Before measurement: state is 'at' centroid (0,0,0).")
            .step("After measurement: state is 'at' one vertex V_i.")
            .step("Geometric displacement = |V_i - O| = |V_i|.")
            .step("For any vertex: |V_i| = sqrt(1+1+1) = sqrt(3).")
            .step("All vertices are equidistant from origin.")
            .conclude("Collapse distance = sqrt(3) for any outcome.")
        )
    
    def model(self):
        # All vertices at same distance from origin
        distances = [math.sqrt(sum(v[i]**2 for i in range(3))) for v in VERTICES.values()]
        avg_dist = sum(distances) / len(distances)
        max_dev = max(abs(d - avg_dist) for d in distances)
        
        return (
            Model()
            .add("Average collapse distance", avg_dist)
            .add("Max deviation", max_dev)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Average collapse distance", SQRT_3)
            .add("Max deviation", 0.0)
        )


class OrthogonalAxesAsObservables(Test):
    """Three orthogonal axes correspond to three observables."""
    name = "Axes as Observables"
    level = Level.STANDARD
    question = (
        "In quantum mechanics, Pauli Z operators on different qubits commute, "
        "but X and Z on the same qubit don't. How does this map to geometry?"
    )
    reference = "Pauli algebra commutation relations"
    tolerance = 0.01
    commentary = (
        "The three coordinate axes are mutually orthogonal. Each axis defines "
        "a binary observable (positive or negative sign). Observables on "
        "different axes commute (measuring x doesn't disturb y). This is "
        "analogous to commuting operators in quantum mechanics."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Three axes: x, y, z (orthogonal).")
            .step("Each axis defines an observable: sign(coord_i) = +/- 1.")
            .step("Measuring one axis gives 2 outcomes, independent of others.")
            .step("In QM: Z_1, Z_2, Z_3 all commute (can be measured simultaneously).")
            .step("In geometry: the three coordinates can be measured independently.")
            .conclude("Three orthogonal axes = 3 commuting observables.")
        )
    
    def model(self):
        axes = 3
        commuting_pairs = 3  # (x,y), (y,z), (z,x) all commute
        
        return (
            Model()
            .add("Number of axes", axes)
            .add("Commuting axis pairs", commuting_pairs)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Number of axes", 3.0)
            .add("Commuting axis pairs", 3.0)
        )


class PhaseSpaceDimension(Test):
    """Phase space has dimension 2d = 6."""
    name = "Phase Space Dimension"
    level = Level.EXPLORATORY
    question = (
        "In classical mechanics, phase space has 2d dimensions (d positions "
        "and d momenta). For d=3, this gives 6. Does this number appear in "
        "the Field Chamber structure?"
    )
    reference = "Hamiltonian mechanics"
    tolerance = 0.01
    commentary = (
        "The inner octahedron (cube face centers) has 6 vertices. This equals "
        "2d = 6. Whether this is significant or coincidental is unclear. We "
        "note it without claiming causation."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Phase space dimension = 2d = 2 x 3 = 6.")
            .step("Cube has 6 faces; face centers form an octahedron.")
            .step("Octahedron has 6 vertices.")
            .step("Numerical correspondence: 6 = 6.")
            .step("This is documented as an observation, not a claim.")
            .conclude("Phase space dim = 6 = octahedron vertices.")
        )
    
    def model(self):
        phase_space_dim = 2 * D  # 6
        octahedron_vertices = 6  # Cube face centers
        
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


class UncertaintyAndConjugateAxes(Test):
    """Position and momentum on same axis are conjugate."""
    name = "Conjugate Variables"
    level = Level.EXPLORATORY
    question = (
        "The uncertainty principle relates conjugate pairs (x, p_x), (y, p_y), "
        "(z, p_z). Does the cube structure encode 3 such pairs?"
    )
    reference = "Heisenberg uncertainty principle"
    tolerance = 0.01
    commentary = (
        "The cube has 3 pairs of opposite faces. Each pair is perpendicular "
        "to one axis. This gives 3 axis directions, matching the 3 conjugate "
        "pairs in 3D quantum mechanics. This is a counting correspondence."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Uncertainty principle: Delta x * Delta p_x >= hbar/2.")
            .step("Three such pairs for d=3: (x, p_x), (y, p_y), (z, p_z).")
            .step("Cube has 6 faces in 3 opposite pairs.")
            .step("Each pair perpendicular to one axis.")
            .step("Number of axes = number of conjugate pairs = 3.")
            .conclude("Conjugate pairs = 3 = spatial dimension d.")
        )
    
    def model(self):
        face_pairs = 3  # (top/bottom), (left/right), (front/back)
        conjugate_pairs = D  # (x, p_x), (y, p_y), (z, p_z)
        
        return (
            Model()
            .add("Face pairs", face_pairs)
            .add("Conjugate variable pairs", conjugate_pairs)
            .add("Match", 1.0 if face_pairs == conjugate_pairs else 0.0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Face pairs", 3.0)
            .add("Conjugate variable pairs", 3.0)
            .add("Match", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BasisStateVertexCorrespondence,
    SuperpositionAsCentroid,
    MeasurementAsProjection,
    OrthogonalAxesAsObservables,
    PhaseSpaceDimension,
    UncertaintyAndConjugateAxes,
]


def run_all():
    """Run all quantum foundations tests."""
    return run_tests(
        title="Quantum Foundations: Geometric Interpretations",
        summary=(
            "These tests examine geometric analogies for quantum concepts: "
            "8 vertices = 8 basis states, superposition = centroid, measurement = "
            "projection to vertex, orthogonal axes = commuting observables. "
            "EXPLORATORY tests note numerical correspondences (phase space dim = 6) "
            "without claiming physical significance."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
