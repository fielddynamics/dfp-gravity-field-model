"""
Cross-Checks: Structural Validations for the Stellated Octahedron Geometry

This module verifies that the GFD model's geometric definitions are internally
consistent and have the mathematical properties claimed by the model.

WHAT IS A GENUINE CROSS-CHECK?
A real cross-check compares predictions or properties derived from DIFFERENT
starting points that should agree. It's NOT comparing a value to itself.

For example:
- GENUINE: The model claims TET_A and TET_B partition the 8 vertices.
  We verify this by checking BOTH that they don't overlap AND that they
  cover all vertices. Two independent checks that together prove partition.
  
- NOT GENUINE: Defining VERTICES = 2*K at the top of a file, then "checking"
  that VERTICES == 2*K. That's just A = A.

WHAT THIS MODULE VALIDATES:
1. Partition Property: TET_A and TET_B truly partition the 8 vertices
2. Parity Correspondence: Binary parity determines tetrahedron membership
3. Complementary Structure: Inversion pairs cross between tetrahedra
4. Topological Consistency: The tetrahedron satisfies Euler's formula
5. Algebraic Structure: Arithmetic inversion equals bitwise XOR

These are structural validations of the model's definitions, not cross-checks
of independent physical derivations. We are honest about what each test does.
"""

import sys
import math

from gravity_field_model.framework import *
from gravity_field_model.common import (
    K, C, HBAR as H_BAR, ALPHA, R_E, LAMBDA_COMPTON as LAMBDA_C, M_E,
    TET_A, TET_B,
)


# =============================================================================
# PARTITION VALIDATIONS
# =============================================================================
# The GFD model claims the stellated octahedron consists of two interlocking
# tetrahedra (TET_A and TET_B) that PARTITION the 8 vertices. A partition means:
#   1. No overlap (disjoint sets)
#   2. Complete coverage (union = all vertices)
# These two tests together verify the partition claim.
# =============================================================================

class TetrahedraPartitionDisjoint(Test):
    """
    WHAT WE'RE CHECKING:
    The model defines TET_A = {1, 2, 4, 7} and TET_B = {0, 3, 5, 6}.
    For these to be a valid partition, they must not share any vertices.
    
    WHY THIS MATTERS:
    If TET_A and TET_B overlapped, a vertex could belong to both tetrahedra,
    breaking the dual chamber structure that the Field Closure model relies on.
    This test confirms the sets are truly disjoint.
    """
    name = "Tetrahedra Partition: Disjoint"
    question = (
        "Are the vertex sets TET_A and TET_B mathematically disjoint? "
        "This is half of proving they partition the stellated octahedron vertices."
    )
    reference = "Set theory: disjoint sets have empty intersection"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The GFD model requires TET_A and TET_B to be distinct, non-overlapping "
        "vertex sets. This test verifies the model's definitions satisfy that requirement. "
        "We compute the actual set intersection rather than assuming it's empty."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CLAIM: TET_A and TET_B partition the 8 stellated octahedron vertices.")
            .step("TEST 1 OF 2: Check that they are disjoint (no shared vertices).")
            .step("TET_A = {1, 2, 4, 7} as defined in the model.")
            .step("TET_B = {0, 3, 5, 6} as defined in the model.")
            .step("Compute intersection: TET_A & TET_B.")
            .step("If intersection is empty, the sets are disjoint.")
            .conclude("Overlap count = |TET_A & TET_B| should be 0.")
        )
    
    def model(self) -> Model:
        # Actually compute the intersection, don't assume
        intersection = TET_A & TET_B
        overlap_count = len(intersection)
        return Model().add("Overlap count", overlap_count)
    
    def observations(self) -> Observed:
        return Observed().add("Overlap count", 0)


class TetrahedraPartitionExhaustive(Test):
    """
    WHAT WE'RE CHECKING:
    The second half of the partition property: TET_A union TET_B must equal
    the complete vertex set {0, 1, 2, 3, 4, 5, 6, 7}.
    
    WHY THIS MATTERS:
    If the union were missing vertices, those vertices would belong to neither
    tetrahedron, leaving "orphan" Coupling Ports outside the Field Chamber structure.
    """
    name = "Tetrahedra Partition: Exhaustive"
    question = (
        "Does TET_A union TET_B equal the complete vertex set {0..7}? "
        "This is the second half of proving they partition the vertices."
    )
    reference = "Set theory: exhaustive partition covers all elements"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Combined with the disjoint test, this confirms TET_A and TET_B form a "
        "proper partition of the 8 vertices. Together they cover everything exactly once."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CLAIM: TET_A and TET_B partition the 8 stellated octahedron vertices.")
            .step("TEST 2 OF 2: Check that their union covers all 8 vertices.")
            .step("TET_A = {1, 2, 4, 7}.")
            .step("TET_B = {0, 3, 5, 6}.")
            .step("Expected complete set = {0, 1, 2, 3, 4, 5, 6, 7}.")
            .step("Compute: TET_A | TET_B and compare to expected.")
            .conclude("Union size = 8 and covers_all = 1 if union equals {0..7}.")
        )
    
    def model(self) -> Model:
        union = TET_A | TET_B
        expected = set(range(8))
        covers_all = 1 if union == expected else 0
        return (
            Model()
            .add("Union size", len(union))
            .add("Covers all vertices", covers_all)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Union size", 8)
            .add("Covers all vertices", 1)
        )


# =============================================================================
# PARITY CORRESPONDENCE
# =============================================================================
# The model claims tetrahedron membership is determined by binary parity:
# - TET_A contains vertices with odd parity (popcount is 1 or 3)
# - TET_B contains vertices with even parity (popcount is 0 or 2)
# This is a structural claim we can verify.
# =============================================================================

class ParityDeterminesTetrahedron(Test):
    """
    WHAT WE'RE CHECKING:
    The model claims binary parity determines which tetrahedron a vertex belongs to.
    We verify this by computing parity independently and checking membership.
    
    WHY THIS MATTERS:
    This correspondence isn't just a coincidence in the definitions. It connects
    the abstract algebraic structure (parity) to the geometric structure (tetrahedra).
    If this broke, the parity arguments used elsewhere in the model would be invalid.
    """
    name = "Parity Determines Tetrahedron"
    question = (
        "Is tetrahedron membership perfectly determined by binary parity? "
        "TET_A should contain all odd-parity vertices, TET_B all even-parity."
    )
    reference = "Binary parity: popcount(v) mod 2"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "We independently compute each vertex's parity from its binary representation, "
        "then check it matches the tetrahedron membership defined in the model. "
        "This is a genuine verification, not a tautology."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CLAIM: Binary parity determines tetrahedron membership.")
            .step("Odd parity means popcount(v) mod 2 = 1 (vertices 1, 2, 4, 7).")
            .step("Even parity means popcount(v) mod 2 = 0 (vertices 0, 3, 5, 6).")
            .step("TEST: For each v in TET_A, verify popcount(v) mod 2 = 1.")
            .step("TEST: For each v in TET_B, verify popcount(v) mod 2 = 0.")
            .step("TET_A: 1=001 (pop=1), 2=010 (pop=1), 4=100 (pop=1), 7=111 (pop=3). All odd.")
            .step("TET_B: 0=000 (pop=0), 3=011 (pop=2), 5=101 (pop=2), 6=110 (pop=2). All even.")
            .conclude("TET_A odd count = 4, TET_B even count = 4.")
        )
    
    def model(self) -> Model:
        # Independently compute parity and check against membership
        tet_a_odd = sum(1 for v in TET_A if bin(v).count('1') % 2 == 1)
        tet_b_even = sum(1 for v in TET_B if bin(v).count('1') % 2 == 0)
        return (
            Model()
            .add("TET_A vertices with odd parity", tet_a_odd)
            .add("TET_B vertices with even parity", tet_b_even)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("TET_A vertices with odd parity", 4)
            .add("TET_B vertices with even parity", 4)
        )


# =============================================================================
# COMPLEMENTARY PAIR STRUCTURE
# =============================================================================
# The model identifies 4 "complementary pairs" where each vertex pairs with
# its bitwise complement (v XOR 7). The claim is that these pairs ALWAYS
# cross between tetrahedra: one member in TET_A, one in TET_B.
# =============================================================================

class ComplementaryPairsCrossTetrahedra(Test):
    """
    WHAT WE'RE CHECKING:
    For each complementary pair (v, 7-v), does one vertex belong to TET_A
    and the other to TET_B? The model claims all 4 pairs cross tetrahedra.
    
    WHY THIS MATTERS:
    The complementary pair structure is central to Field Closure dynamics.
    If any pair were contained within a single tetrahedron, it would break
    the inter-tetrahedra coupling that the model claims drives field dynamics.
    
    NOTE: This follows mathematically from the parity correspondence (since
    v and 7-v always have opposite parities), but we test it explicitly to
    validate the geometric claim about the stellated octahedron structure.
    """
    name = "Complementary Pairs Cross Tetrahedra"
    question = (
        "Do all 4 complementary pairs (v, 7-v) cross between TET_A and TET_B? "
        "This ensures systematic coupling between the dual Field Chamber components."
    )
    reference = "Inversion symmetry through the Field Origin"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "We check each of the 4 pairs: (0,7), (1,6), (2,5), (3,4). For each pair, "
        "we verify one vertex is in TET_A and the other in TET_B. This is a consequence "
        "of the parity structure, but worth verifying explicitly as a structural property."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CLAIM: All 4 complementary pairs cross between tetrahedra.")
            .step("Pairs: (0,7), (1,6), (2,5), (3,4) where each sums to 7.")
            .step("Check (0,7): 0 in TET_B, 7 in TET_A. CROSSES.")
            .step("Check (1,6): 1 in TET_A, 6 in TET_B. CROSSES.")
            .step("Check (2,5): 2 in TET_A, 5 in TET_B. CROSSES.")
            .step("Check (3,4): 3 in TET_B, 4 in TET_A. CROSSES.")
            .conclude("Cross-tetrahedra pairs = 4 (all pairs cross).")
        )
    
    def model(self) -> Model:
        pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
        cross_count = 0
        for v1, v2 in pairs:
            in_different_tetrahedra = (v1 in TET_A) != (v2 in TET_A)
            if in_different_tetrahedra:
                cross_count += 1
        return Model().add("Pairs that cross tetrahedra", cross_count)
    
    def observations(self) -> Observed:
        return Observed().add("Pairs that cross tetrahedra", 4)


# =============================================================================
# TOPOLOGICAL CONSISTENCY
# =============================================================================
# Euler's formula V - E + F = 2 must hold for any valid closed polyhedron.
# The GFD model claims a tetrahedron has k=4 vertices and k=4 faces.
# We verify this is topologically consistent.
# =============================================================================

class TetrahedronTopologyValid(Test):
    """
    WHAT WE'RE CHECKING:
    A tetrahedron has V=4 vertices, E=6 edges, F=4 faces.
    Euler's polyhedron formula requires V - E + F = 2 for any closed surface.
    
    WHY THIS MATTERS:
    This is NOT a GFD cross-check. It's a sanity check that the basic geometry
    the model uses (tetrahedra with 4 vertices and 4 faces) is topologically valid.
    If this failed, the tetrahedron wouldn't be a legitimate 3D polyhedron.
    
    HONESTY NOTE:
    The edge count E=6 comes from geometry (4 vertices, each pair connected = C(4,2) = 6).
    This test verifies topological consistency of the tetrahedron parameters.
    """
    name = "Tetrahedron Topology Valid"
    question = (
        "Does the tetrahedron (V=4, E=6, F=4) satisfy Euler's formula V - E + F = 2? "
        "This confirms it is a valid closed polyhedron."
    )
    reference = "Euler's polyhedron formula (Euler, 1758)"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Euler's formula is a fundamental topological constraint for closed polyhedra. "
        "A tetrahedron with 4 vertices has C(4,2)=6 edges (each pair of vertices connected) "
        "and 4 triangular faces. We verify: 4 - 6 + 4 = 2."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("Euler's formula: V - E + F = 2 for any closed convex polyhedron.")
            .step("Tetrahedron vertices: V = k = 4.")
            .step("Tetrahedron edges: E = C(4,2) = 4*3/2 = 6 (each pair of vertices connected).")
            .step("Tetrahedron faces: F = k = 4 (each face is a triangle).")
            .step("Calculate: V - E + F = 4 - 6 + 4 = 2.")
            .step("This matches Euler's requirement.")
            .conclude("Euler characteristic = 2.")
        )
    
    def model(self) -> Model:
        V = K  # 4 vertices (from GFD model)
        E = V * (V - 1) // 2  # 6 edges (derived from combinatorics)
        F = K  # 4 faces (from GFD model)
        euler = V - E + F
        return Model().add("V - E + F", euler)
    
    def observations(self) -> Observed:
        return Observed().add("V - E + F", 2)


# =============================================================================
# ALGEBRAIC STRUCTURE
# =============================================================================
# The model uses both arithmetic inversion (7-v) and bitwise XOR (v ^ 7).
# For 3-bit numbers (0-7), these are equivalent. We verify this.
# =============================================================================

class InversionEqualsXOR(Test):
    """
    WHAT WE'RE CHECKING:
    For all vertices v in {0..7}, is (7 - v) equal to (v XOR 7)?
    
    WHY THIS MATTERS:
    The model uses both notations interchangeably. If they weren't equivalent,
    different parts of the model would compute different "complements."
    
    MATHEMATICAL NOTE:
    This equivalence holds for 3-bit numbers because 7 = 111 in binary,
    and XOR with 111 flips all bits, which for 3-bit unsigned integers
    equals subtraction from 7. This is NOT a general property of arithmetic.
    """
    name = "Inversion Equals XOR"
    question = (
        "Is arithmetic inversion (7-v) equivalent to bitwise XOR (v^7) "
        "for all 8 vertices? This validates the algebraic structure."
    )
    reference = "Binary arithmetic for 3-bit integers"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "For 3-bit unsigned integers, XOR with 7 (111 binary) flips all bits. "
        "Flipping all bits of v gives the ones-complement, which for 3-bit numbers "
        "equals 7 - v. This equivalence is specific to 3-bit numbers."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CLAIM: For v in {0..7}, (7 - v) = (v XOR 7).")
            .step("v=0: 7-0=7, 0 XOR 7 = 000 XOR 111 = 111 = 7. MATCH.")
            .step("v=1: 7-1=6, 1 XOR 7 = 001 XOR 111 = 110 = 6. MATCH.")
            .step("v=2: 7-2=5, 2 XOR 7 = 010 XOR 111 = 101 = 5. MATCH.")
            .step("v=3: 7-3=4, 3 XOR 7 = 011 XOR 111 = 100 = 4. MATCH.")
            .step("v=4: 7-4=3, 4 XOR 7 = 100 XOR 111 = 011 = 3. MATCH.")
            .step("v=5: 7-5=2, 5 XOR 7 = 101 XOR 111 = 010 = 2. MATCH.")
            .step("v=6: 7-6=1, 6 XOR 7 = 110 XOR 111 = 001 = 1. MATCH.")
            .step("v=7: 7-7=0, 7 XOR 7 = 111 XOR 111 = 000 = 0. MATCH.")
            .conclude("Vertices where (7-v) = (v XOR 7): 8 out of 8.")
        )
    
    def model(self) -> Model:
        match_count = sum(1 for v in range(8) if (7 - v) == (v ^ 7))
        return Model().add("Vertices with matching inversion methods", match_count)
    
    def observations(self) -> Observed:
        return Observed().add("Vertices with matching inversion methods", 8)


# =============================================================================
# PHYSICS CONSTANTS SANITY CHECK
# =============================================================================
# This is NOT a GFD cross-check. It verifies that the physical constants
# used in the model are consistent with known QED relationships.
# =============================================================================

class AlphaFromLengthScales(Test):
    """
    WHAT WE'RE CHECKING:
    The fine structure constant alpha approximately equals r_e / lambda_bar_C,
    where r_e is the classical electron radius and lambda_bar_C is the reduced
    Compton wavelength. This is a known QED relationship.
    
    WHY THIS MATTERS:
    The GFD model uses alpha, r_e, and lambda_C as parameters. If these
    constants weren't mutually consistent (per QED), the model's calculations
    involving these quantities would be internally inconsistent.
    
    HONESTY NOTE:
    This is a sanity check on the physical constants, not a GFD derivation.
    The model imports these values from CODATA; we verify they satisfy
    the QED relationship alpha = r_e / lambda_bar_C.
    """
    name = "Alpha from Length Scales (QED Consistency)"
    question = (
        "Is alpha approximately equal to r_e / lambda_bar_C as required by QED? "
        "This is a sanity check on the physical constants, not a GFD derivation."
    )
    reference = "Quantum Electrodynamics"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The fine structure constant relates the classical electron radius to the "
        "reduced Compton wavelength: alpha = r_e / lambda_bar_C. We verify the CODATA "
        "constants used in the model satisfy this relationship within 1%."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("QED RELATION: alpha = r_e / lambda_bar_C.")
            .step("alpha = 1/137.036 = 7.297e-3 (fine structure constant).")
            .step("r_e = 2.818e-15 m (classical electron radius).")
            .step("lambda_C = 2.426e-12 m (Compton wavelength).")
            .step("lambda_bar_C = lambda_C / (2*pi) = 3.862e-13 m (reduced).")
            .step("Compute: r_e / lambda_bar_C = 2.818e-15 / 3.862e-13 = 7.297e-3.")
            .step("Compare to alpha: 7.297e-3 vs 7.297e-3. MATCH.")
            .conclude("alpha from CODATA vs alpha from r_e/lambda_bar_C.")
        )
    
    def model(self) -> Model:
        lambda_bar = LAMBDA_C / (2 * math.pi)
        alpha_from_lengths = R_E / lambda_bar
        return (
            Model()
            .add("alpha (CODATA)", ALPHA)
            .add("r_e / lambda_bar_C", alpha_from_lengths)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("alpha (CODATA)", ALPHA)
            .add("r_e / lambda_bar_C", ALPHA)  # Should match if constants are consistent
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    # Partition property (two tests that together prove the claim)
    TetrahedraPartitionDisjoint,
    TetrahedraPartitionExhaustive,
    # Structural correspondences
    ParityDeterminesTetrahedron,
    ComplementaryPairsCrossTetrahedra,
    # Topological and algebraic consistency
    TetrahedronTopologyValid,
    InversionEqualsXOR,
    # Physics sanity check (not a GFD derivation)
    AlphaFromLengthScales,
]


def run_all() -> bool:
    """Run all cross-check tests."""
    return run_tests(
        title="Structural Validations and Consistency Checks",
        summary=(
            "These tests verify the GFD model's geometric definitions are internally "
            "consistent. We validate the partition property (TET_A and TET_B truly "
            "partition the 8 vertices), the parity correspondence, complementary pair "
            "structure, and topological validity. We also include a QED sanity check "
            "on physical constants. These are structural validations, not cross-checks "
            "of independent physical derivations."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
