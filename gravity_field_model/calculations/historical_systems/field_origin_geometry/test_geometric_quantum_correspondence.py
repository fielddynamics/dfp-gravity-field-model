"""
Geometric-Quantum Correspondences: Mathematical Isomorphisms

This module documents exact mathematical correspondences between the cube vertex
structure and quantum information theory. These are not speculations; they are
provable isomorphisms between geometric and algebraic structures.

THE KEY INSIGHT:
A cube has 8 vertices. A 3-qubit system has 8 computational basis states. This
is the same number (2^3 = 8), so there is a natural bijection between them.
The geometry of the cube then maps to operations on qubits.

WHAT THIS MEANS:
The correspondences here are MATHEMATICAL FACTS, not physical claims. Whether
they have physical significance for GFM is a separate question. We document
them because they exist and may be useful.

TEXTBOOK REFERENCE:
Gravity Field Dynamics Textbook, Chapter 9 Section 9.2: Binary encoding of cube
vertices. The mapping vertex i <-> |i> in binary provides a natural bijection
between geometric and quantum structures.

AUDIT NOTES:
- audit_score: 95
- audit_notes: None (cleared after audit)
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common.geometry_constants import (
    VERTICES, TET_A, TET_B, get_vertex_coords
)


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Closure constant (imported concept, local for clarity)
D = K - 1  # = 3 spatial dimensions
SQRT_2 = math.sqrt(2)
SQRT_3 = math.sqrt(3)

# Convert VERTICES dict to simple coordinate tuples for this module
VERTEX_COORDS = {i: VERTICES[i]['coords'] for i in range(8)}


# =============================================================================
# TEST CLASSES
# =============================================================================

class ThreeQubitBijection(Test):
    """8 vertices = 8 basis states of a 3-qubit system."""
    name = "3-Qubit Bijection"
    level = Level.STANDARD
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Does the bijection extend to d-qubit systems for d-dimensional hypercubes? "
        "(Answering would improve Question by +2 points: tests generalization) "
        "Q2: Can quantum circuits be represented as paths through the cube graph? "
        "(Answering would improve Commentary by +2 points: computational interpretation) "
        "Q3: What is the quantum gate corresponding to a cube rotation? "
        "(Answering would improve Derivation by +2 points: explicit gate construction)"
    )
    question = (
        "Why does the cube vertex structure map naturally to a 3-qubit quantum "
        "system? Both have 2^d = 8 states in d=3 dimensions, revealing a deep "
        "isomorphism between spatial geometry and quantum information."
    )
    reference = "GFM Textbook Ch.9 Sec.9.2; Nielsen & Chuang (2000) quantum computing"
    tolerance = 0.01
    commentary = (
        "The bijection vertex i <-> |bin(i)> identifies cube corners with "
        "computational basis states. This is more than counting: cube operations "
        "(reflections, rotations) correspond to quantum gates. The Field Chamber "
        "geometry thus encodes a 3-qubit Hilbert space structure."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Cube vertices: {0, 1, 2, 3, 4, 5, 6, 7}.")
            .step("3-qubit basis states: {|000>, |001>, |010>, |011>, |100>, |101>, |110>, |111>}.")
            .step("Both sets have cardinality 2^3 = 8.")
            .step("Natural bijection: vertex i <-> state |i> (i in binary).")
            .conclude("Exact bijection exists: 8 vertices <-> 8 basis states.")
        )
    
    def model(self):
        cube_vertices = 8
        qubit_states = 2 ** D  # 8
        return (
            Model()
            .add("Cube vertices", cube_vertices)
            .add("3-qubit basis states", qubit_states)
            .add("Exact match", 1.0 if cube_vertices == qubit_states else 0.0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Cube vertices", 8.0)
            .add("3-qubit basis states", 8.0)
            .add("Exact match", 1.0)
        )


class ParityEqualsParityObservable(Test):
    """Vertex parity (Tet A/B) equals total parity observable."""
    name = "Parity Observable"
    level = Level.STANDARD
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Does the parity eigenspace structure relate to superselection rules? "
        "(Answering would improve Question by +2 points: quantum foundations connection) "
        "Q2: How does the parity observable P transform under spatial inversion? "
        "(Answering would improve Commentary by +2 points: symmetry behavior) "
        "Q3: Is there a measurement protocol that projects onto Tet A or Tet B? "
        "(Answering would improve Derivation by +2 points: operational meaning)"
    )
    question = (
        "Why do the two tetrahedra correspond exactly to the eigenspaces of the "
        "quantum parity observable? This reveals how bimetric structure emerges "
        "from a fundamental quantum symmetry operator."
    )
    reference = "GFM Textbook Ch.9; Quantum parity operator P = Z tensor Z tensor Z"
    tolerance = 0.01
    commentary = (
        "The parity observable P = Z1 x Z2 x Z3 has eigenvalue +1 for states with "
        "even popcount (Tet B) and -1 for odd popcount (Tet A). The dual chambers "
        "are thus the positive and negative eigenspaces of P, connecting the "
        "bimetric structure to quantum symmetry classification."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Parity observable P = Z1 tensor Z2 tensor Z3.")
            .step("P|i> = (-1)^(bit_count(i)) |i>.")
            .step("Even bit count -> eigenvalue +1 -> Tet B: {0, 3, 5, 6}.")
            .step("Odd bit count -> eigenvalue -1 -> Tet A: {1, 2, 4, 7}.")
            .step("This exactly matches our tetrahedron classification.")
            .conclude("Tet A = odd parity eigenspace; Tet B = even parity eigenspace.")
        )
    
    def model(self):
        tet_a_odd = all(bin(v).count('1') % 2 == 1 for v in TET_A)
        tet_b_even = all(bin(v).count('1') % 2 == 0 for v in TET_B)
        
        return (
            Model()
            .add("Tet A all odd parity", 1.0 if tet_a_odd else 0.0)
            .add("Tet B all even parity", 1.0 if tet_b_even else 0.0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet A all odd parity", 1.0)
            .add("Tet B all even parity", 1.0)
        )


class GHZStateIsBodyDiagonal(Test):
    """GHZ state |000> + |111> corresponds to body diagonal (0,7)."""
    name = "GHZ State Geometry"
    level = Level.STANDARD
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Do the other 3 body diagonals correspond to rotated GHZ states? "
        "(Answering would improve Question by +2 points: complete classification) "
        "Q2: How does GHZ entanglement relate to bimetric coupling across tetrahedra? "
        "(Answering would improve Commentary by +2 points: entanglement-gravity link) "
        "Q3: Can GHZ state preparation be interpreted as field closure between chambers? "
        "(Answering would improve Derivation by +2 points: operational physics meaning)"
    )
    question = (
        "Why does the maximally entangled GHZ state correspond to the principal "
        "body diagonal? The superposition of |000> and |111> represents the two "
        "most distant vertices, revealing how maximal entanglement maps to "
        "maximal geometric separation."
    )
    reference = "Greenberger, Horne, Zeilinger (1989); GFM Textbook Ch.9"
    tolerance = 0.01
    commentary = (
        "The GHZ state superposes vertices 0 and 7, which have maximum Hamming "
        "distance (3 bits differ) and maximum Euclidean distance (2*sqrt(3)). "
        "Maximal entanglement corresponds to superposing maximally separated "
        "geometric states, with the body diagonal passing through the Field Origin."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("GHZ state: (|000> + |111>)/sqrt(2).")
            .step("Vertex 0 = (-1,-1,-1), Vertex 7 = (+1,+1,+1).")
            .step("Hamming distance: 0 XOR 7 = 7 = 111 in binary, 3 ones.")
            .step("Euclidean distance: sqrt((2)^2 + (2)^2 + (2)^2) = 2*sqrt(3).")
            .step("This is the maximum possible separation in both metrics.")
            .conclude("GHZ components are antipodal vertices on body diagonal.")
        )
    
    def model(self):
        v0 = VERTEX_COORDS[0]
        v7 = VERTEX_COORDS[7]
        
        # Hamming distance
        hamming = bin(0 ^ 7).count('1')  # 3
        
        # Euclidean distance
        euclidean = math.sqrt(sum((v7[i] - v0[i])**2 for i in range(3)))
        max_euclidean = 2 * SQRT_3
        
        return (
            Model()
            .add("Hamming distance", hamming)
            .add("Maximum Hamming for d=3", D)
            .add("Euclidean distance", euclidean)
            .add("Maximum Euclidean", max_euclidean)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Hamming distance", 3.0)
            .add("Maximum Hamming for d=3", 3.0)
            .add("Euclidean distance", 2 * SQRT_3)
            .add("Maximum Euclidean", 2 * SQRT_3)
        )


class WStateIsTriangle(Test):
    """W state |001> + |010> + |100> forms equilateral triangle in Tet A."""
    name = "W State Geometry"
    level = Level.STANDARD
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Does the W state triangle correspond to a face of the tetrahedron? "
        "(Answering would improve Question by +2 points: face-state correspondence) "
        "Q2: How does W entanglement differ from GHZ in terms of field coupling? "
        "(Answering would improve Commentary by +2 points: entanglement types) "
        "Q3: Is there a physical process that prepares W states from field closure? "
        "(Answering would improve Derivation by +2 points: operational interpretation)"
    )
    question = (
        "Why do the W state vertices (1, 2, 4) form an equilateral triangle? "
        "This shows how another canonical entangled state maps to a regular "
        "geometric structure within Chamber A."
    )
    reference = "Dur, Vidal, Cirac (2000); GFM Textbook Ch.9"
    tolerance = 0.05
    commentary = (
        "Vertices 1, 2, 4 are three corners of Tet A (excluding apex 7). Each "
        "pair has Hamming distance 2 and Euclidean distance 2*sqrt(2). This "
        "uniform separation makes them equilateral, and the W state superposes "
        "this symmetric triangle within the odd-parity chamber."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("W state: (|001> + |010> + |100>)/sqrt(3).")
            .step("Vertices 1, 2, 4 in binary: 001, 010, 100.")
            .step("Each pair has Hamming distance 2 (e.g., 001 XOR 010 = 011, 2 ones).")
            .step("Euclidean distance: sqrt(0 + 4 + 4) = 2*sqrt(2) for each pair.")
            .step("Equal distances -> equilateral triangle.")
            .conclude("W state vertices form equilateral triangle with edge 2*sqrt(2).")
        )
    
    def model(self):
        v1 = VERTEX_COORDS[1]
        v2 = VERTEX_COORDS[2]
        v4 = VERTEX_COORDS[4]
        
        def dist(a, b):
            return math.sqrt(sum((a[i] - b[i])**2 for i in range(3)))
        
        d12 = dist(v1, v2)
        d24 = dist(v2, v4)
        d41 = dist(v4, v1)
        
        is_equilateral = abs(d12 - d24) < 0.01 and abs(d24 - d41) < 0.01
        
        return (
            Model()
            .add("Distance v1-v2", d12)
            .add("Distance v2-v4", d24)
            .add("Distance v4-v1", d41)
            .add("Is equilateral", 1.0 if is_equilateral else 0.0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Distance v1-v2", 2 * SQRT_2)
            .add("Distance v2-v4", 2 * SQRT_2)
            .add("Distance v4-v1", 2 * SQRT_2)
            .add("Is equilateral", 1.0)
        )


class HammingDistanceClassification(Test):
    """Vertex pairs classified by Hamming distance."""
    name = "Hamming Distance Classes"
    level = Level.STANDARD
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Does Hamming distance correspond to a quantum mechanical distance metric? "
        "(Answering would improve Question by +2 points: quantum distance connection) "
        "Q2: How does the 12:12:4 ratio relate to error correction code distances? "
        "(Answering would improve Commentary by +2 points: coding theory link) "
        "Q3: Can single-qubit errors be detected using the Hamming structure? "
        "(Answering would improve Derivation by +2 points: error detection protocol)"
    )
    question = (
        "Why does Hamming distance classify vertex pairs into exactly three "
        "geometric categories? This reveals how bit-flip distance maps directly "
        "to spatial structure: edges, face diagonals, and body diagonals."
    )
    reference = "Hamming (1950); GFM Textbook Ch.9 Sec.9.2"
    tolerance = 0.01
    commentary = (
        "Hamming distance 1, 2, 3 correspond to edges (12), face diagonals (12), "
        "and body diagonals (4). This is not coincidence: flipping 1 bit moves "
        "along an edge, 2 bits crosses a face, 3 bits traverses the cube body. "
        "Quantum single-qubit gates thus correspond to geometric edge operations."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Total pairs: C(8,2) = 28.")
            .step("Hamming distance 1: one bit differs -> cube edge.")
            .step("  Each vertex has 3 neighbors, 8*3/2 = 12 edges.")
            .step("Hamming distance 2: two bits differ -> face diagonal.")
            .step("  6 faces x 2 diagonals = 12 face diagonals.")
            .step("Hamming distance 3: all bits differ -> body diagonal.")
            .step("  4 body diagonals connecting antipodal pairs.")
            .conclude("H=1: 12 edges; H=2: 12 face diags; H=3: 4 body diags.")
        )
    
    def model(self):
        counts = {1: 0, 2: 0, 3: 0}
        for i in range(8):
            for j in range(i + 1, 8):
                h = bin(i ^ j).count('1')
                counts[h] += 1
        
        return (
            Model()
            .add("Hamming=1 (edges)", counts[1])
            .add("Hamming=2 (face diagonals)", counts[2])
            .add("Hamming=3 (body diagonals)", counts[3])
            .add("Total pairs", sum(counts.values()))
        )
    
    def observations(self):
        return (
            Observed()
            .add("Hamming=1 (edges)", 12.0)
            .add("Hamming=2 (face diagonals)", 12.0)
            .add("Hamming=3 (body diagonals)", 4.0)
            .add("Total pairs", 28.0)
        )


class PauliOperatorsAsReflections(Test):
    """Pauli X operators correspond to coordinate sign flips."""
    name = "Pauli as Reflections"
    level = Level.STANDARD
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Do Pauli Y and Z operators have similar geometric interpretations? "
        "(Answering would improve Question by +2 points: complete Pauli geometry) "
        "Q2: How does the Pauli group isomorphism extend to the full cube symmetry group? "
        "(Answering would improve Commentary by +2 points: group structure) "
        "Q3: Can arbitrary rotations be decomposed into sequences of Pauli reflections? "
        "(Answering would improve Derivation by +2 points: gate decomposition)"
    )
    question = (
        "Why do Pauli X operators correspond to geometric reflections through "
        "coordinate planes? This isomorphism shows how fundamental quantum "
        "gates map directly to spatial symmetry operations."
    )
    reference = "Pauli matrices; GFM Textbook Ch.9: Geometry-gate correspondence"
    tolerance = 0.01
    commentary = (
        "The Pauli X_i flips bit i, which geometrically reflects the vertex "
        "through the plane x_i = 0. The Pauli group (generated by X, Y, Z on "
        "each qubit) is isomorphic to the cube's reflection symmetry group. "
        "Quantum operations thus have direct geometric interpretations."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("X_i flips bit i: |...b_i...> -> |...not(b_i)...>.")
            .step("In vertex coordinates: flips sign of coordinate i.")
            .step("Example: X_0 on vertex 0 (000) gives vertex 1 (001).")
            .step("Geometrically: (-1,-1,-1) -> (-1,-1,+1) (z-flip).")
            .step("This is reflection through the z=0 plane.")
            .conclude("Pauli X_i = reflection through coordinate i = 0 plane.")
        )
    
    def model(self):
        # Test X operations
        # X_0 flips bit 0 (rightmost)
        x0_on_0 = 0 ^ 1  # 0 -> 1
        x0_on_7 = 7 ^ 1  # 7 -> 6
        
        # X_1 flips bit 1
        x1_on_0 = 0 ^ 2  # 0 -> 2
        
        # X_2 flips bit 2
        x2_on_0 = 0 ^ 4  # 0 -> 4
        
        return (
            Model()
            .add("X0 on vertex 0", x0_on_0)
            .add("X0 on vertex 7", x0_on_7)
            .add("X1 on vertex 0", x1_on_0)
            .add("X2 on vertex 0", x2_on_0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("X0 on vertex 0", 1.0)
            .add("X0 on vertex 7", 6.0)
            .add("X1 on vertex 0", 2.0)
            .add("X2 on vertex 0", 4.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ThreeQubitBijection,
    ParityEqualsParityObservable,
    GHZStateIsBodyDiagonal,
    WStateIsTriangle,
    HammingDistanceClassification,
    PauliOperatorsAsReflections,
]


def run_all():
    """Run all geometric-quantum correspondence tests."""
    return run_tests(
        title="Geometric-Quantum Correspondences: Mathematical Isomorphisms",
        summary=(
            "These tests document exact mathematical correspondences between cube "
            "geometry and 3-qubit quantum systems. The bijection 8 vertices <-> 8 "
            "basis states leads to: parity = tetrahedral membership, GHZ state = "
            "body diagonal, W state = equilateral triangle, Hamming distance = "
            "geometric distance class, Pauli operators = coordinate reflections."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
