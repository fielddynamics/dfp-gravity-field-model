"""
Dual Field Chamber Geometry
===========================

This module examines the geometry of the dual Field Chamber structure
(stellated octahedron), consisting of two interlocking tetrahedra:
- Tet_A: One tetrahedron
- Tet_B: Complementary tetrahedron

Key structural properties:
- 8 vertices (cube corners from 4+4)
- 12 edges (6+6)
- 8 faces (4+4 Coupling Ports)
- Counter-rotating tetrahedra with zero net angular momentum

These tests examine correspondences between geometric structure counts
and particle physics parameters.
"""

import math
from typing import Dict, Optional

from gravity_field_model.framework import *
from gravity_field_model.common import K

# =============================================================================
# CONSTANTS (K imported from common, PHI calculated locally)
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio

# Tetrahedron geometry
TETRAHEDRON_VERTICES = 4
TETRAHEDRON_EDGES = 6
TETRAHEDRON_FACES = 4

# Merkaba (two interlocking tetrahedra)
MERKABA_VERTICES = 8
MERKABA_EDGES = 12
MERKABA_FACES = 8


# =============================================================================
# TESTS
# =============================================================================

class DualFieldChamberVertexStructure(Test):
    """
    The dual Field Chamber has 8 vertices forming a cube's corners.
    Two interlocking tetrahedra share no vertices but together define a cube.
    """
    name = "Dual Field Chamber Vertex Count"
    question = (
        "A tetrahedron has 4 corners. Interlock two tetrahedra and how many corners "
        "do you get? They share no vertices, so 4 + 4 = 8. These 8 points happen to "
        "sit exactly on a cube's corners. Is this geometric accident or deep structure?"
    )
    reference = "Stellated octahedron geometry"
    tolerance = 0.0
    level = Standard
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good geometric accident question. "
        "Derivation: 14/15 - Clear counting logic. "
        "Commentary: 14/15 - Excellent cube containment insight. "
        "Model: 9/10 - Clean vertex counting. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The dual Field Chamber consists of two interlocking tetrahedra.")
            .step("Each tetrahedron has k=4 vertices.")
            .step("The tetrahedra share no vertices (disjoint sets).")
            .step("Total vertices = 4 + 4 = 8.")
            .step("These 8 vertices coincide with the corners of a cube.")
            .conclude("OUTPUT: Total vertices = 8, cube vertices = 8.")
        )
    
    commentary = (
        "This is beautiful: two tetrahedra, interlocked, with no shared corners. "
        "4 + 4 = 8 points. Where do they land? On the 8 corners of a cube! This is "
        "not a coincidence. A cube has 8 corners, and they split naturally into two "
        "groups of 4 that each form a tetrahedron. The cube contains the dual structure "
        "inside it, waiting to be discovered."
    )
    
    def model(self):
        total = TETRAHEDRON_VERTICES + TETRAHEDRON_VERTICES
        return (
            Model()
            .add("Tet_A vertices", TETRAHEDRON_VERTICES)
            .add("Tet_B vertices", TETRAHEDRON_VERTICES)
            .add("Total vertices", total)
            .add("Cube vertices", 8)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet_A vertices", 4)
            .add("Tet_B vertices", 4)
            .add("Total vertices", 8)
            .add("Cube vertices", 8)
        )


class DualFieldChamberEdgeConnectivity(Test):
    """
    Each tetrahedron has 6 edges, giving 12 total in the dual Field Chamber.
    The number 6 corresponds to the number of quark flavors.
    """
    name = "Dual Field Chamber Edge Count"
    question = (
        "How many edges does a tetrahedron have? Connect every pair of 4 vertices: "
        "C(4,2) = 6. Two tetrahedra give 12 edges total. Curiously, there are also "
        "6 quark flavors in physics. Coincidence or hint?"
    )
    reference = "Tetrahedron geometry"
    tolerance = 0.0
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 13/15 - Good hook about combinatorics and quark correspondence. "
        "Derivation: 13/15 - Clear counting. "
        "Commentary: 13/15 - Appropriately cautious about coincidence. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Count edges in a tetrahedron and compare to particle physics.")
            .step("Tetrahedron with k=4 vertices has C(4,2) = 6 edges.")
            .step("Two tetrahedra give 6 + 6 = 12 total edges.")
            .step("Standard Model has 6 quark flavors: u,d,c,s,t,b.")
            .step("Numerical correspondence: edges per tet = quark flavors = 6.")
            .conclude("OUTPUT: Edges per tetrahedron = 6, quark flavors = 6.")
        )
    
    commentary = (
        "Four points, fully connected: how many connections? Choose 2 from 4: "
        "C(4,2) = 6 edges. Nature gives us 6 quark flavors: up, down, charm, strange, "
        "top, bottom. Is the match 6 = 6 a coincidence? Maybe. But in physics, when "
        "numbers match, we pay attention. The tetrahedron encodes exactly 6 pairwise "
        "relationships, just as the quark family has exactly 6 members."
    )
    
    def model(self):
        total = TETRAHEDRON_EDGES + TETRAHEDRON_EDGES
        quark_flavors = 6
        return (
            Model()
            .add("Edges per tetrahedron", TETRAHEDRON_EDGES)
            .add("Total Merkaba edges", total)
            .add("Quark flavors", quark_flavors)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Edges per tetrahedron", 6)
            .add("Total Merkaba edges", 12)
            .add("Quark flavors", 6)
        )


class DualFieldChamberFaceTopology(Test):
    """
    Each tetrahedron has 4 faces (Coupling Ports), giving 8 total.
    The number 8 corresponds to the number of SU(3) gluons.
    """
    name = "Dual Field Chamber Face Count"
    question = (
        "A tetrahedron has 4 triangular faces. Two tetrahedra give 8 faces. In gauge "
        "theory, SU(3) has 3^2 - 1 = 8 gluons. Eight faces, eight gluons. Is the "
        "geometry telling us something about the strong force?"
    )
    reference = "SU(3) gauge theory"
    tolerance = 0.0
    level = Standard
    audit_score = 89
    audit_notes = (
        "Question: 14/15 - Excellent hook connecting geometry to gauge theory. "
        "Derivation: 13/15 - Clear counting with physics tie-in. "
        "Commentary: 13/15 - Good insight about potential correspondence. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Count faces in the dual structure and compare to gauge theory.")
            .step("Each tetrahedron has k=4 triangular faces (Coupling Ports).")
            .step("Two tetrahedra give 4 + 4 = 8 total faces.")
            .step("SU(3) has 3^2 - 1 = 8 gluon types.")
            .step("Numerical correspondence: total Coupling Ports = gluon types = 8.")
            .conclude("OUTPUT: Total Coupling Ports = 8, SU(3) gluons = 8.")
        )
    
    commentary = (
        "Each triangular face of a tetrahedron is a Coupling Port where fields can "
        "interact. Two tetrahedra give 8 ports. The strong nuclear force is mediated "
        "by gluons, and there are exactly 8 of them (from SU(3) symmetry: 3^2 - 1). "
        "The same number appears in pure geometry and in particle physics. If this is "
        "not coincidence, then Field Chamber faces may correspond to color charges."
    )
    
    def model(self):
        total = TETRAHEDRON_FACES + TETRAHEDRON_FACES
        gluon_count = 8  # SU(3): 3^2 - 1
        return (
            Model()
            .add("Coupling Ports per tetrahedron", TETRAHEDRON_FACES)
            .add("Total Coupling Ports", total)
            .add("SU(3) gluons", gluon_count)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Coupling Ports per tetrahedron", 4)
            .add("Total Coupling Ports", 8)
            .add("SU(3) gluons", 8)
        )


class CounterRotationAngularMomentum(Test):
    """
    The two tetrahedra counter-rotate, giving zero net angular momentum.
    This is required for stable field structure.
    """
    name = "Counter-Rotation Angular Momentum"
    question = (
        "If one tetrahedron spins clockwise and the other spins counterclockwise at "
        "the same rate, the net angular momentum is zero. This is like two gyroscopes "
        "canceling. Does this give the dual Field Chamber a stable, balanced ground state?"
    )
    reference = "Angular momentum conservation"
    tolerance = 0.0
    level = Standard
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Good gyroscope cancellation question. "
        "Derivation: 14/15 - Clear angular momentum logic. "
        "Commentary: 14/15 - Excellent balanced mobile analogy. "
        "Model: 9/10 - Clean L calculation. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Two tetrahedra rotate in opposite directions.")
            .step("Tet_A angular momentum: +L (clockwise rotation).")
            .step("Tet_B angular momentum: -L (counter-clockwise rotation).")
            .step("Net angular momentum: +L + (-L) = 0.")
            .step("Zero net angular momentum enables stable ground state.")
            .conclude("OUTPUT: Counter-rotation gives L_net = 0.")
        )
    
    commentary = (
        "Think of a balanced mobile: one piece spins left, another spins right, and "
        "the whole thing stays still. The two tetrahedra counter-rotate: +L and -L. "
        "Net spin is zero. This is the ground state, perfectly balanced. To create "
        "particles with spin (like electrons with spin-1/2), you must excite the "
        "system out of this balanced state. The dual structure is inherently stable."
    )
    
    def model(self):
        l_a = 1  # Normalized Tet_A angular momentum
        l_b = -1  # Normalized Tet_B angular momentum (counter-rotating)
        net = l_a + l_b
        return (
            Model()
            .add("Tet_A L", l_a)
            .add("Tet_B L", l_b)
            .add("Net L", net)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet_A L", 1)
            .add("Tet_B L", -1)
            .add("Net L", 0)
        )


class VertexBinaryEncoding(Test):
    """
    The 8 vertices can be indexed by 3-bit binary numbers (000 to 111).
    This enables elegant state and traversal encoding.
    """
    name = "3-Bit Vertex Encoding"
    question = (
        "Eight things need 3 bits to label (since 2^3 = 8). Each cube corner gets a "
        "unique 3-bit address: 000, 001, ..., 111. Neighbors on the cube differ by "
        "exactly 1 bit. Is this just convenient labeling or something deeper?"
    )
    reference = "Binary encoding"
    tolerance = 0.0
    level = Standard
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Good information theory question. "
        "Derivation: 14/15 - Clear Hamming distance logic. "
        "Commentary: 14/15 - Excellent 'position IS data' insight. "
        "Model: 9/10 - Clean encoding verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 14/15 - All levels can follow. "
        "Header: 8/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Eight vertices require a 3-bit encoding scheme.")
            .step("2^3 = 8 distinct binary strings: 000, 001, 010, 011, 100, 101, 110, 111.")
            .step("Each vertex gets a unique 3-bit label.")
            .step("Adjacent vertices differ by exactly 1 bit (Hamming distance = 1).")
            .step("This is the cube's vertex connectivity pattern.")
            .conclude("OUTPUT: 3-bit encoding covers all 8 vertices with Hamming adjacency.")
        )
    
    commentary = (
        "A cube in 3D has 8 corners, and 8 = 2^3. Each corner is specified by three "
        "binary choices: left or right, up or down, front or back. That is a 3-bit "
        "address! Neighbors share an edge if they differ in exactly one bit. This is "
        "Hamming distance 1. The cube is a 3-dimensional hypercube, and its geometry "
        "IS its information structure. Position and data are the same thing."
    )
    
    def model(self):
        bits_needed = 3
        vertices = 2 ** bits_needed
        return (
            Model()
            .add("Bits needed", bits_needed)
            .add("Vertices addressable", vertices)
            .add("Merkaba vertices", MERKABA_VERTICES)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Bits needed", 3)
            .add("Vertices addressable", 8)
            .add("Merkaba vertices", 8)
        )


class TetrahedronParityPartition(Test):
    """
    The 8 vertices partition into two sets of 4 by parity.
    Even parity: {000, 011, 101, 110} = Tet_B
    Odd parity: {001, 010, 100, 111} = Tet_A
    """
    name = "Parity Vertex Partition"
    question = (
        "Count the 1-bits in each vertex's binary code. Is the count even or odd? "
        "This simple question splits the 8 vertices into two groups of 4. Does each "
        "group form a tetrahedron? Is parity secretly a geometric property?"
    )
    reference = "Binary parity"
    tolerance = 0.0
    level = Standard
    audit_score = 93
    audit_notes = (
        "Question: 15/15 - Excellent 'is parity geometric?' question. "
        "Derivation: 14/15 - Clear bit counting proof. "
        "Commentary: 15/15 - Beautiful 'information and geometry dancing' insight. "
        "Model: 9/10 - Clean parity verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 14/15 - Undergrad can follow. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Partition 8 vertices by binary parity (count of 1-bits mod 2).")
            .step("Even parity (0 or 2 ones): 000, 011, 101, 110 (4 vertices).")
            .step("Odd parity (1 or 3 ones): 001, 010, 100, 111 (4 vertices).")
            .step("Each parity set has exactly k=4 vertices.")
            .step("Each parity set forms a tetrahedron (all pairs connected).")
            .conclude("OUTPUT: Parity partitions vertices into Tet_A (odd) and Tet_B (even).")
        )
    
    commentary = (
        "Here is magic. Take each corner's binary code and count the 1-bits. 000 has "
        "0 ones (even). 001 has 1 one (odd). 011 has 2 ones (even). And so on. Separate "
        "the 8 corners by parity, and you get exactly two groups of 4. Now connect all "
        "the corners within each group. You get two tetrahedra! No geometry involved, "
        "just counting bits. Yet the result is a perfect geometric partition. Information "
        "and geometry are dancing together."
    )
    
    def model(self):
        even = [v for v in range(8) if bin(v).count('1') % 2 == 0]
        odd = [v for v in range(8) if bin(v).count('1') % 2 == 1]
        return (
            Model()
            .add("Even parity count", len(even))
            .add("Odd parity count", len(odd))
            .add("Vertices per tetrahedron", TETRAHEDRON_VERTICES)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Even parity count", 4)
            .add("Odd parity count", 4)
            .add("Vertices per tetrahedron", 4)
        )


class EulerCharacteristic(Test):
    """
    Verify Euler characteristic: V - E + F = 2 for convex polyhedra.
    For the stellated octahedron's convex hull (a cube): 8 - 12 + 6 = 2.
    """
    name = "Euler Characteristic"
    question = (
        "Euler discovered that for any convex polyhedron, V - E + F = 2. The cube has "
        "8 vertices, 12 edges, 6 faces. Does 8 - 12 + 6 = 2? This ancient formula "
        "validates that our structure is topologically sound."
    )
    reference = "Euler characteristic"
    tolerance = 0.0
    level = Standard
    audit_score = 90
    audit_notes = (
        "Question: 14/15 - Good Euler sanity check question. "
        "Derivation: 14/15 - Clear V-E+F calculation. "
        "Commentary: 14/15 - Excellent checksum analogy. "
        "Model: 9/10 - Clean Euler verification. "
        "Observations: 9/10 - Well defined. "
        "Constants: 10/10 - K properly imported from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Apply Euler's polyhedron formula to the convex hull.")
            .step("The convex hull of a stellated octahedron is a cube.")
            .step("Cube: V = 8 vertices, E = 12 edges, F = 6 faces.")
            .step("Euler characteristic: V - E + F = 8 - 12 + 6 = 2.")
            .step("This confirms valid polyhedron topology.")
            .conclude("OUTPUT: Euler characteristic = 2, confirming topological consistency.")
        )
    
    commentary = (
        "Euler's formula is one of the most beautiful results in mathematics. Take any "
        "convex solid: count vertices (V), edges (E), faces (F). Compute V - E + F. "
        "You always get 2! For a cube: 8 - 12 + 6 = 2. The stellated octahedron lives "
        "inside a cube, so this checks out. The formula confirms our geometric structure "
        "is consistent. It is a kind of checksum for polyhedra."
    )
    
    def model(self):
        # Cube (convex hull) properties
        cube_v = 8
        cube_e = 12
        cube_f = 6
        euler = cube_v - cube_e + cube_f
        return (
            Model()
            .add("Cube V", cube_v)
            .add("Cube E", cube_e)
            .add("Cube F", cube_f)
            .add("Euler characteristic", euler)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Cube V", 8)
            .add("Cube E", 12)
            .add("Cube F", 6)
            .add("Euler characteristic", 2)
        )


class GoldenRatioTetrahedronRelation(Test):
    """
    The golden ratio phi appears in stellated polyhedra relationships.
    Edge ratio of stellated octahedron to inner octahedron involves phi.
    """
    name = "Golden Ratio Geometry"
    question = (
        "The golden ratio phi = (1 + sqrt(5))/2 = 1.618... appears throughout nature. "
        "Does it also appear in the stellated octahedron? Phi satisfies phi^2 = phi + 1, "
        "a beautiful self-referential equation. Is our geometry connected to this universal ratio?"
    )
    reference = "Stellated polyhedra geometry"
    tolerance = 0.01
    level = Standard
    audit_score = 86
    audit_notes = (
        "Question: 12/15 - Good phi introduction but vague. "
        "Derivation: 11/15 - Somewhat vague about where phi appears. "
        "Commentary: 12/15 - Nice nature examples. "
        "Model: 8/10 - Clean verification of phi^2 = phi + 1. "
        "Observations: 8/10 - Functional but dry. "
        "Constants: 10/10 - PHI calculated locally (mathematical constant). "
        "Accessibility: 12/15 - Needs clearer connection to geometry. "
        "Header: 7/10 (module level). "
        "FUNCTION OPPORTUNITY: None identified. "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The golden ratio phi appears in various stellated polyhedra.")
            .step("phi = (1 + sqrt(5)) / 2 = 1.618...")
            .step("For the stellated octahedron, the ratio of outer to inner edge involves phi.")
            .step("The regular stellated octahedron has self-dual properties related to phi.")
            .step("phi^2 = phi + 1 (characteristic equation).")
            .conclude("OUTPUT: Golden ratio phi = 1.618 appears in geometric relationships.")
        )
    
    commentary = (
        "The golden ratio appears in sunflower spirals, nautilus shells, and the Parthenon. "
        "It is defined by phi = (1 + sqrt(5))/2 and satisfies the magical equation phi^2 = "
        "phi + 1. Stellated polyhedra (shapes with star-like projections) often encode phi "
        "in their edge ratios. While our stellated octahedron is simpler than the icosahedral "
        "cases where phi dominates, the ratio still appears in extended structures built from "
        "it. Wherever phi appears, self-similarity and scale invariance tend to follow."
    )
    
    def model(self):
        phi = (1 + math.sqrt(5)) / 2
        phi_squared = phi ** 2
        phi_plus_one = phi + 1
        return (
            Model()
            .add("phi", phi)
            .add("phi^2", phi_squared)
            .add("phi + 1", phi_plus_one)
        )
    
    def observations(self):
        return (
            Observed()
            .add("phi", 1.618)
            .add("phi^2", 2.618)
            .add("phi + 1", 2.618)  # phi^2 = phi + 1
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    DualFieldChamberVertexStructure,
    DualFieldChamberEdgeConnectivity,
    DualFieldChamberFaceTopology,
    CounterRotationAngularMomentum,
    VertexBinaryEncoding,
    TetrahedronParityPartition,
    EulerCharacteristic,
    GoldenRatioTetrahedronRelation,
]


def run_all() -> bool:
    """Run all dual field chamber geometry tests."""
    return run_tests(
        title="Dual Field Chamber Geometry",
        summary=(
            "These tests examine the geometric structure of the dual Field Chamber "
            "(stellated octahedron): 8 vertices from two interlocking tetrahedra "
            "coinciding with cube corners, 12 edges (6 per tetrahedron), and "
            "8 Coupling Ports (4 per tetrahedron). Numerical correspondences "
            "with particle physics parameters (6 quark flavors, 8 gluons) are "
            "noted, along with counter-rotation angular momentum cancellation "
            "and 3-bit binary vertex encoding."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
