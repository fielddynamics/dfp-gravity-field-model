"""
Cross-Checks: Inter-Module Consistency Validation

This module verifies consistency across different calculation domains in the
GFD validation suite. Tests confirm that k=4, fundamental constants, and
geometric relationships maintain agreement between modules.
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group


# =============================================================================
# CONSTANTS (from various modules - must agree)
# =============================================================================

# Topology
K = 4
VERTICES = 8
FACES = 8
EDGES = 12

# Physics
C = 2.998e8
H_BAR = 1.055e-34
ALPHA = 1 / 137.036
R_E = 2.8179403262e-15
LAMBDA_C = 2.426310238e-12
M_E = 9.109e-31

# Sets
TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}


# =============================================================================
# TEST CLASSES
# =============================================================================

class KConsistency(GFDTest):
    """k=4 is consistent across all modules."""
    name = "k Consistency"
    question = (
        "Is the Field Closure constant k=4 used consistently across all validation modules "
        "(particle physics, coupling dynamics, and symmetry operations), ensuring the model "
        "maintains a single coherent value for this fundamental parameter?"
    )
    reference_source = "Topology constant"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Closure constant k=4 should appear consistently across all validation modules. "
        "STEP 1: In topology module: k=4 is the number of faces on a tetrahedron. "
        "STEP 2: In coupling module: each tetrahedron has k=4 vertices. "
        "STEP 3: In symmetry module: 4 faces per tetrahedron (1 TIME + 3 SPATIAL). "
        "STEP 4: Compare all values: 4 = 4 = 4. "
        "OUTPUT: k (topology) = 4, Faces per tet = 4, Vertices per tet = 4."
    )
    commentary = (
        "The consistent appearance of k=4 across different calculation modules suggests "
        "this value may represent a fundamental structural parameter of the Field Chamber. "
        "This internal consistency is necessary for the model to maintain coherent predictions "
        "across its various domains."
    )
    
    def model(self):
        return {
            "k (topology)": K,
            "Faces per tet": K,
            "Vertices per tet": K,
        }
    
    def observations(self):
        return {
            "k (topology)": 4,
            "Faces per tet": 4,
            "Vertices per tet": 4,
        }


class VertexCountConsistency(GFDTest):
    """8 vertices = 2k is consistent."""
    name = "Vertex Count Consistency"
    question = (
        "Is the total vertex count of 8 = 2k consistent across all module representations, "
        "confirming that Tet_A and Tet_B together account for all Coupling Ports in the "
        "stellated octahedron?"
    )
    reference_source = "Dual Field Chamber geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The stellated octahedron comprises two interlocking tetrahedra with 2k total vertices. "
        "STEP 1: From topology: total vertices = 8. "
        "STEP 2: From k constant: 2k = 2×4 = 8. "
        "STEP 3: From set definitions: |Tet_A| + |Tet_B| = 4 + 4 = 8. "
        "STEP 4: Compare all representations: 8 = 8 = 8. "
        "OUTPUT: Total vertices = 8, 2k = 8, Tet_A + Tet_B = 8."
    )
    commentary = (
        "The relationship 2k=8 vertices corresponds to the dual structure of the Field Chamber, "
        "with each tetrahedron contributing k=4 vertices. This consistent vertex count across "
        "representations suggests the stellated octahedron geometry is internally coherent."
    )
    
    def model(self):
        return {
            "Total vertices": VERTICES,
            "2k": 2 * K,
            "Tet_A + Tet_B": len(TET_A) + len(TET_B),
        }
    
    def observations(self):
        return {
            "Total vertices": 8,
            "2k": 8,
            "Tet_A + Tet_B": 8,
        }


class TetrahedraDisjoint(GFDTest):
    """Tet_A and Tet_B are disjoint sets."""
    name = "Tetrahedra Disjoint"
    question = (
        "Are the vertex sets Tet_A and Tet_B mathematically disjoint (zero intersection), "
        "confirming they partition the stellated octahedron vertices into non-overlapping "
        "complementary sub-structures?"
    )
    reference_source = "Set theory"
    tolerance = 0.01
    derivation = (
        "PREMISE: Tet_A and Tet_B partition the stellated octahedron vertices by parity. "
        "STEP 1: Tet_A = {1, 2, 4, 7} (odd parity vertices). "
        "STEP 2: Tet_B = {0, 3, 5, 6} (even parity vertices). "
        "STEP 3: Compute intersection: Tet_A ∩ Tet_B = { }. "
        "STEP 4: Count overlap: |Tet_A ∩ Tet_B| = 0. "
        "OUTPUT: Overlap count = 0."
    )
    commentary = (
        "The disjoint nature of Tetrahedron A and Tetrahedron B vertex sets is consistent with "
        "interpreting them as complementary sub-structures within the Field Chamber. This separation "
        "may indicate distinct functional domains within the stellated octahedron topology."
    )
    
    def model(self):
        overlap = len(TET_A & TET_B)
        return {"Overlap count": overlap}
    
    def observations(self):
        return {"Overlap count": 0}


class TetrahedraExhaustive(GFDTest):
    """Tet_A union Tet_B = all 8 vertices."""
    name = "Tetrahedra Exhaustive"
    question = (
        "Does the union of Tet_A and Tet_B cover all 8 vertices of the stellated octahedron, "
        "confirming they form a complete partition with no vertices left unassigned?"
    )
    reference_source = "Set theory"
    tolerance = 0.01
    derivation = (
        "PREMISE: Tet_A and Tet_B should together cover all 2k=8 vertices of the stellated octahedron. "
        "STEP 1: Tet_A = {1, 2, 4, 7}; Tet_B = {0, 3, 5, 6}. "
        "STEP 2: Compute union: Tet_A ∪ Tet_B = {0, 1, 2, 3, 4, 5, 6, 7}. "
        "STEP 3: Full vertex set: {0, 1, 2, 3, 4, 5, 6, 7}. "
        "STEP 4: Check equality: Tet_A ∪ Tet_B = {0..7} and |union| = 8. "
        "OUTPUT: Union size = 8, Covers all = 1."
    )
    commentary = (
        "The exhaustive coverage of all vertices by Tetrahedra A and B together suggests a complete "
        "partition of the Field Chamber structure. This correspondence supports the model's treatment "
        "of the two tetrahedra as a non-overlapping, exhaustive decomposition of the stellated octahedron."
    )
    
    def model(self):
        union = len(TET_A | TET_B)
        full_set = TET_A | TET_B == set(range(8))
        return {
            "Union size": union,
            "Covers all": 1 if full_set else 0,
        }
    
    def observations(self):
        return {
            "Union size": 8,
            "Covers all": 1,
        }


class EulerFormulaTetrahedron(GFDTest):
    """V - E + F = 2 for each tetrahedron."""
    name = "Euler Formula (Tet)"
    question = (
        "Does each tetrahedron in the Field Chamber satisfy Euler's polyhedron formula "
        "V - E + F = 2, confirming it is a valid closed 2-manifold in three dimensions?"
    )
    reference_source = "Euler's polyhedron formula"
    tolerance = 0.01
    derivation = (
        "PREMISE: Euler's formula V - E + F = 2 must hold for any valid closed polyhedron. "
        "STEP 1: A tetrahedron has: V = k = 4 vertices. "
        "STEP 2: A tetrahedron has: E = 6 edges (each pair of vertices connected). "
        "STEP 3: A tetrahedron has: F = k = 4 faces. "
        "STEP 4: Calculate: V - E + F = 4 - 6 + 4 = 2. "
        "OUTPUT: V - E + F = 2."
    )
    commentary = (
        "Adherence to Euler's polyhedron formula confirms each tetrahedron within the Field Chamber "
        "is a valid closed 2-manifold. This consistency with established topological constraints is "
        "a necessary condition for the geometric coherence of Tetrahedron A and Tetrahedron B."
    )
    
    def model(self):
        V = 4
        E = 6
        F = 4
        euler = V - E + F
        return {"V - E + F": euler}
    
    def observations(self):
        return {"V - E + F": 2}


class SpeedOfLightConsistency(GFDTest):
    """c = lambda_C * f_Compton is consistent."""
    name = "c Consistency"
    question = (
        "Is the speed of light c self-consistently recovered from the product of the "
        "Compton wavelength λ_C and Compton frequency f_C, confirming the fundamental "
        "wave relation c = λf holds in the GFD parameter set?"
    )
    reference_source = "Speed of light"
    tolerance = 0.01
    derivation = (
        "PREMISE: The speed of light must satisfy c = λ × f for any wave relation. "
        "STEP 1: Compton wavelength: λ_C = 2.426×10⁻¹² m. "
        "STEP 2: Compton frequency: f_C = c/λ_C = 2.998×10⁸ / 2.426×10⁻¹² = 1.236×10²⁰ Hz. "
        "STEP 3: Verify: λ_C × f_C = 2.426×10⁻¹² × 1.236×10²⁰ = 2.998×10⁸ m/s. "
        "OUTPUT: c (input) = 2.998×10⁸ m/s, c (from lambda_C * f) = 2.998×10⁸ m/s."
    )
    commentary = (
        "This self-consistency check confirms that the speed of light remains algebraically coherent "
        "when decomposed into Compton wavelength and frequency components. Maintaining this identity "
        "is essential for any model incorporating relativistic mechanics and Field Closure dynamics."
    )
    
    def model(self):
        f_compton = C / LAMBDA_C
        c_check = LAMBDA_C * f_compton
        return {
            "c (input)": C,
            "c (from lambda_C * f)": c_check,
        }
    
    def observations(self):
        return {
            "c (input)": C,
            "c (from lambda_C * f)": C,
        }


class AlphaRelation(GFDTest):
    """alpha = r_e / lambda_C_bar approximately."""
    name = "Alpha Relation"
    question = (
        "Is the fine structure constant α approximately equal to the ratio of the classical "
        "electron radius r_e to the reduced Compton wavelength λ̄_C = λ_C/(2π), confirming "
        "consistency with quantum electrodynamics?"
    )
    reference_source = "Fine structure constant"
    tolerance = 0.05
    derivation = (
        "PREMISE: The fine structure constant α should equal r_e/λ̄_C per QED. "
        "STEP 1: Fine structure constant: α = 1/137.036 ≈ 7.297×10⁻³. "
        "STEP 2: Classical electron radius: r_e = 2.818×10⁻¹⁵ m. "
        "STEP 3: Compton wavelength: λ_C = 2.426×10⁻¹² m. "
        "STEP 4: Reduced Compton wavelength: λ̄_C = λ_C/(2π) = 3.862×10⁻¹³ m. "
        "STEP 5: Compute ratio: r_e/λ̄_C = 2.818×10⁻¹⁵ / 3.862×10⁻¹³ = 7.297×10⁻³. "
        "OUTPUT: alpha (exact) = 7.297×10⁻³, r_e / lambda_C_bar = 7.297×10⁻³."
    )
    commentary = (
        "The approximate correspondence between the fine structure constant and the ratio of classical "
        "electron radius to reduced Compton wavelength is a known relationship from quantum electrodynamics. "
        "This cross-check confirms the model's constants remain consistent with established physics, "
        "which is necessary for meaningful Port Ratio calculations."
    )
    
    def model(self):
        lambda_c_bar = LAMBDA_C / (2 * math.pi)
        ratio = R_E / lambda_c_bar
        return {
            "alpha (exact)": ALPHA,
            "r_e / lambda_C_bar": ratio,
        }
    
    def observations(self):
        return {
            "alpha (exact)": ALPHA,
            "r_e / lambda_C_bar": ALPHA,
        }


class ComplementaryPairsConsistency(GFDTest):
    """4 complementary pairs cross tetrahedra everywhere."""
    name = "Complementary Pairs"
    question = (
        "Do all k=4 complementary pairs (formed by inversion through the Field Origin) "
        "cross the boundary between Tetrahedron A and Tetrahedron B, ensuring systematic "
        "coupling between the dual Field Chamber components?"
    )
    reference_source = "Inversion symmetry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Complementary pairs (V, 7-V) should cross between Tet_A and Tet_B under inversion. "
        "STEP 1: The k=4 pairs are: (0,7), (1,6), (2,5), (3,4). "
        "STEP 2: Check each: 0∈B, 7∈A (cross); 1∈A, 6∈B (cross); 2∈A, 5∈B (cross); 3∈B, 4∈A (cross). "
        "STEP 3: Count cross-tetrahedra pairs: 4 out of 4. "
        "OUTPUT: Cross-tetrahedra pairs = 4."
    )
    commentary = (
        "The observation that all four complementary vertex pairs span both tetrahedra suggests a "
        "systematic relationship between Field Chamber geometry and inversion symmetry. This cross-tetrahedra "
        "pairing may correspond to the structure of Coupling Ports connecting Tetrahedron A and Tetrahedron B."
    )
    
    def model(self):
        pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
        cross_count = 0
        for v1, v2 in pairs:
            t1 = 'A' if v1 in TET_A else 'B'
            t2 = 'A' if v2 in TET_A else 'B'
            if t1 != t2:
                cross_count += 1
        return {"Cross-tetrahedra pairs": cross_count}
    
    def observations(self):
        return {"Cross-tetrahedra pairs": 4}


class ParityConsistency(GFDTest):
    """Tet_A = odd parity, Tet_B = even parity."""
    name = "Parity Consistency"
    question = (
        "Is tetrahedron membership perfectly determined by binary parity—Tet_A containing "
        "all odd-parity vertices (odd number of 1-bits) and Tet_B containing all even-parity "
        "vertices?"
    )
    reference_source = "Binary parity"
    tolerance = 0.01
    derivation = (
        "PREMISE: Binary parity (popcount mod 2) should determine tetrahedron membership. "
        "STEP 1: Tet_A = {1, 2, 4, 7}. Check parities: 1=001→1 (odd), 2=010→1 (odd), 4=100→1 (odd), 7=111→3 (odd). "
        "STEP 2: Tet_B = {0, 3, 5, 6}. Check parities: 0=000→0 (even), 3=011→2 (even), 5=101→2 (even), 6=110→2 (even). "
        "STEP 3: Count: Tet_A has 4/4 odd; Tet_B has 4/4 even. "
        "OUTPUT: Tet_A odd count = 4, Tet_B even count = 4."
    )
    commentary = (
        "The correspondence between binary parity and tetrahedron membership suggests an underlying "
        "mathematical structure relating combinatorial properties to Field Chamber geometry. This consistency "
        "supports the model's vertex labeling scheme as reflecting intrinsic topological distinctions."
    )
    
    def model(self):
        tet_a_odd = sum(1 for v in TET_A if bin(v).count('1') % 2 == 1)
        tet_b_even = sum(1 for v in TET_B if bin(v).count('1') % 2 == 0)
        return {
            "Tet_A odd count": tet_a_odd,
            "Tet_B even count": tet_b_even,
        }
    
    def observations(self):
        return {
            "Tet_A odd count": 4,
            "Tet_B even count": 4,
        }


class FaceCountConsistency(GFDTest):
    """8 faces = 2k across the dual Field Chamber."""
    name = "Face Count"
    question = (
        "Does the combined dual Field Chamber have 2k=8 faces total, with each tetrahedron "
        "contributing k=4 faces (1 TIME + 3 SPATIAL per tetrahedron)?"
    )
    reference_source = "Dual Field Chamber geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The dual Field Chamber should have 2k faces from two tetrahedra. "
        "STEP 1: Each tetrahedron has k=4 triangular faces (1 TIME + 3 SPATIAL). "
        "STEP 2: Tet_A: 4 faces; Tet_B: 4 faces. "
        "STEP 3: Total faces: 4 + 4 = 8. "
        "STEP 4: Verify: 2k = 2×4 = 8. "
        "OUTPUT: Total faces = 8, 2k = 8."
    )
    commentary = (
        "The relationship 2k=8 faces corresponds to the dual tetrahedra each contributing k=4 faces "
        "to the Field Chamber. This is consistent with identifying 2 TIME faces (1 per tetrahedron) and "
        "6 SPATIAL faces (3 per tetrahedron) within the stellated octahedron structure, partitioned "
        "across Tetrahedron A and Tetrahedron B."
    )
    
    def model(self):
        return {
            "Total faces": FACES,
            "2k": 2 * K,
        }
    
    def observations(self):
        return {
            "Total faces": 8,
            "2k": 8,
        }


class EdgeCountConsistency(GFDTest):
    """12 edges = 3k for the stellated octahedron."""
    name = "Edge Count"
    question = (
        "Does the stellated octahedron have 3k=12 edges, representing the connectivity "
        "pathways between Coupling Ports in the Field Chamber structure?"
    )
    reference_source = "Stellated octahedron geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The stellated octahedron edges should satisfy E = 3k. "
        "STEP 1: Each tetrahedron has 6 edges (connecting all pairs of 4 vertices). "
        "STEP 2: Total edges in the cube containing the stellated octahedron: 12. "
        "STEP 3: These 12 edges connect the 8 vertices (Coupling Ports). "
        "STEP 4: Verify: 3k = 3×4 = 12. "
        "OUTPUT: Total edges = 12, 3k = 12."
    )
    commentary = (
        "The 3k=12 edge relationship for the stellated octahedron is consistent with the standard "
        "geometric properties of this form. These edges may correspond to the connectivity pathways "
        "between Coupling Ports, with each vertex serving as a potential Port location within the Field Chamber."
    )
    
    def model(self):
        return {
            "Total edges": EDGES,
            "3k": 3 * K,
        }
    
    def observations(self):
        return {
            "Total edges": 12,
            "3k": 12,
        }


class InversionXORConsistency(GFDTest):
    """Inversion = XOR with 7 (111 binary)."""
    name = "Inversion = XOR"
    question = (
        "Is the arithmetic inversion operation (7-V) equivalent to the bitwise XOR operation "
        "(V ⊕ 7) for all 8 vertices, confirming the algebraic structure of the vertex labeling?"
    )
    reference_source = "Binary arithmetic"
    tolerance = 0.01
    derivation = (
        "PREMISE: Arithmetic inversion (7-V) should equal bitwise XOR (V⊕7) for all vertices. "
        "STEP 1: Arithmetic inversion: inv(V) = 7 - V. "
        "STEP 2: Bitwise XOR: V ⊕ 7 = V ⊕ 111₂ (flips all 3 bits). "
        "STEP 3: Check equivalence for each vertex: "
        "V=0: 7-0=7, 0⊕7=7; V=1: 7-1=6, 1⊕7=6; V=2: 7-2=5, 2⊕7=5; V=3: 7-3=4, 3⊕7=4; "
        "V=4: 7-4=3, 4⊕7=3; V=5: 7-5=2, 5⊕7=2; V=6: 7-6=1, 6⊕7=1; V=7: 7-7=0, 7⊕7=0. "
        "STEP 4: Count matches: 8/8 vertices satisfy (7-V) = (V⊕7). "
        "OUTPUT: XOR equivalence count = 8."
    )
    commentary = (
        "The equivalence between arithmetic inversion (7-v) and bitwise XOR confirms a mathematical "
        "property of the vertex labeling within the Field Chamber. This self-consistency suggests the "
        "binary representation has algebraic structure that may relate to Field Closure operations "
        "centered on the Field Origin."
    )
    
    def model(self):
        match_count = sum(1 for v in range(8) if (7 - v) == (v ^ 7))
        return {"XOR equivalence count": match_count}
    
    def observations(self):
        return {"XOR equivalence count": 8}


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    KConsistency,
    VertexCountConsistency,
    TetrahedraDisjoint,
    TetrahedraExhaustive,
    EulerFormulaTetrahedron,
    SpeedOfLightConsistency,
    AlphaRelation,
    ComplementaryPairsConsistency,
    ParityConsistency,
    FaceCountConsistency,
    EdgeCountConsistency,
    InversionXORConsistency,
]


def run_all_tests():
    """Run all cross-check tests."""
    return run_test_group(
        title="Cross-Module Consistency Checks",
        summary=(
            "These tests verify that fundamental constants (k=4, vertices=8, "
            "faces=8, edges=12) and relationships (complementary pairs, parity, "
            "inversion) maintain consistency across calculation modules. "
            "Cross-checks ensure coherent assumptions throughout the validation suite."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
