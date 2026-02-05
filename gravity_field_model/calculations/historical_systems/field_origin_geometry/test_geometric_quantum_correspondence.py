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
they have physical significance for GFD is a separate question. We document
them because they exist and may be useful.
"""

import math
from gravity_field_model.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Closure constant
D = K - 1  # = 3 spatial dimensions
SQRT_2 = math.sqrt(2)
SQRT_3 = math.sqrt(3)

# Vertex coordinates (cube corners at +/-1)
VERTICES = {
    0: (-1, -1, -1),  # Binary: 000
    1: (-1, -1, +1),  # Binary: 001
    2: (-1, +1, -1),  # Binary: 010
    3: (-1, +1, +1),  # Binary: 011
    4: (+1, -1, -1),  # Binary: 100
    5: (+1, -1, +1),  # Binary: 101
    6: (+1, +1, -1),  # Binary: 110
    7: (+1, +1, +1),  # Binary: 111
}

TET_A = {1, 2, 4, 7}  # Odd parity vertices
TET_B = {0, 3, 5, 6}  # Even parity vertices


# =============================================================================
# TEST CLASSES
# =============================================================================

class ThreeQubitBijection(Test):
    """8 vertices = 8 basis states of a 3-qubit system."""
    name = "3-Qubit Bijection"
    level = Level.STANDARD
    question = (
        "The cube has 8 vertices; a 3-qubit system has 8 computational basis "
        "states. Is there a natural bijection between them?"
    )
    reference = "Counting: 2^3 = 8"
    tolerance = 0.01
    commentary = (
        "This is trivially true: both sets have 8 elements. The natural map "
        "sends vertex i to state |i> where i is written in binary. Vertex 0 "
        "maps to |000>, vertex 7 maps to |111>, etc."
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
    question = (
        "In quantum computing, the parity observable measures whether the "
        "total number of 1-bits is odd or even. Does this match Tet A/B membership?"
    )
    reference = "Parity observable P = Z1 tensor Z2 tensor Z3"
    tolerance = 0.01
    commentary = (
        "Yes, exactly. The parity observable has eigenvalue +1 for even parity "
        "states (Tet B) and -1 for odd parity states (Tet A). The two tetrahedra "
        "are exactly the two eigenspaces of the parity observable."
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
    question = (
        "The GHZ state (|000> + |111>)/sqrt(2) is a maximally entangled 3-qubit "
        "state. Does it correspond to the body diagonal from vertex 0 to 7?"
    )
    reference = "Greenberger-Horne-Zeilinger (1989)"
    tolerance = 0.01
    commentary = (
        "Yes. The GHZ state superposes the two extreme vertices (all -1s and "
        "all +1s). These are connected by a body diagonal through the origin. "
        "The Hamming distance (number of bit flips) is maximal: 3."
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
        v0 = VERTICES[0]
        v7 = VERTICES[7]
        
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
    question = (
        "The W state (|001> + |010> + |100>)/sqrt(3) uses vertices 1, 2, 4. "
        "Do these form an equilateral triangle?"
    )
    reference = "Dur, Vidal, Cirac (2000)"
    tolerance = 0.05
    commentary = (
        "Yes. Vertices 1, 2, 4 are three corners of Tet A (the fourth is 7). "
        "Each pair differs by exactly 2 bits, so all pairwise Hamming distances "
        "are equal. Geometrically, they form an equilateral triangle."
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
        v1 = VERTICES[1]
        v2 = VERTICES[2]
        v4 = VERTICES[4]
        
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
    question = (
        "How many vertex pairs have Hamming distance 1, 2, and 3? And what are "
        "their geometric interpretations?"
    )
    reference = "Hamming distance in coding theory"
    tolerance = 0.01
    commentary = (
        "Hamming distance 1: cube edges (12 pairs). Hamming distance 2: face "
        "diagonals (12 pairs). Hamming distance 3: body diagonals (4 pairs). "
        "Total: 12 + 12 + 4 = 28 = C(8,2) pairs."
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
    question = (
        "Does the Pauli X operator on qubit i correspond to flipping the sign "
        "of coordinate i in the geometric representation?"
    )
    reference = "Pauli matrices in quantum computing"
    tolerance = 0.01
    commentary = (
        "Yes. X_i flips bit i, which in our encoding flips coordinate i from "
        "+1 to -1 or vice versa. This is a reflection through the plane "
        "perpendicular to axis i. The Pauli group is isomorphic to the "
        "coordinate reflection group."
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
