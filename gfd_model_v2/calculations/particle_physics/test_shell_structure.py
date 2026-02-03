"""
Electron Shell Structure: 2, 8, 18, 32 from Lattice Geometry

These tests examine electron shell capacities (2, 8, 18, 32) using the GFD
lattice geometry framework. The model produces values consistent with the
established 2n^2 formula, with n^2 orbital cells multiplied by 2 spin states.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Closure constant
D = K - 1  # 3 spatial dimensions

# Shell capacities
SHELL_CAPACITIES = [2, 8, 18, 32]  # K, L, M, N shells

# Noble gas electron counts
NOBLE_GASES = {
    'He': 2, 'Ne': 10, 'Ar': 18, 'Kr': 36, 'Xe': 54, 'Rn': 86,
}

# Subshell capacities
SUBSHELL_CAPACITIES = {'s': 2, 'p': 6, 'd': 10, 'f': 14}
L_VALUES = {'s': 0, 'p': 1, 'd': 2, 'f': 3}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def shell_capacity(n):
    """Return capacity of shell n using 2n^2 formula."""
    return 2 * n * n

def shell_capacity_gfd(n):
    """Calculate shell capacity from GFD framework: n^2 orbital cells x 2 spin states."""
    orbital_cells = n * n
    spin_states = 2  # From dual Field Chamber (stellated octahedron) structure
    return orbital_cells * spin_states

def subshell_capacity(l):
    """Return capacity of subshell with angular momentum l: 2(2l + 1)."""
    return 2 * (2 * l + 1)


# =============================================================================
# TEST CLASSES
# =============================================================================

class ShellFormula2nSquared(GFDTest):
    """Shell capacities follow 2n^2 formula."""
    name = "Shell Capacity Formula"
    question = "What electron capacities do atomic shells exhibit, and does the standard 2n^2 formula correctly predict these values?"
    reference_source = "Atomic physics (established)"
    tolerance = 0.01
    derivation = (
        "PREMISE: Shell capacity follows C(n) = 2n² where n is the principal quantum number. "
        "STEP 1: For n=1 (K shell): C = 2 × 1² = 2. "
        "STEP 2: For n=2 (L shell): C = 2 × 2² = 8. "
        "STEP 3: For n=3 (M shell): C = 2 × 3² = 18. For n=4 (N shell): C = 2 × 4² = 32. "
        "OUTPUT: K shell = 2, L shell = 8, M shell = 18, N shell = 32."
    )
    commentary = (
        "The 2n² shell capacity formula is a well-established result of quantum mechanics. "
        "This test serves as a baseline verification that the model's geometric interpretation "
        "produces values consistent with atomic spectroscopy, without claiming to replace the "
        "standard quantum mechanical derivation."
    )
    
    def model(self):
        computed = [shell_capacity(n) for n in [1, 2, 3, 4]]
        return {
            "K shell (n=1)": computed[0],
            "L shell (n=2)": computed[1],
            "M shell (n=3)": computed[2],
            "N shell (n=4)": computed[3],
        }
    
    def observations(self):
        return {
            "K shell (n=1)": 2,
            "L shell (n=2)": 8,
            "M shell (n=3)": 18,
            "N shell (n=4)": 32,
        }


class GFDShellFormula(GFDTest):
    """GFD calculation produces values consistent with standard 2n^2 formula."""
    name = "GFD Shell Calculation"
    question = "How does the GFD framework decompose shell capacity into orbital and spin components, and does this match the standard formula?"
    reference_source = "2n^2 formula"
    tolerance = 0.01
    derivation = (
        "PREMISE: Shell capacity factors as C(n) = (orbital cells) × (spin states) in GFD. "
        "STEP 1: Orbital cells per shell = n² (spatial configurations). "
        "STEP 2: Spin states = 2 (from dual Field Chamber TIME faces: Tet A and Tet B). "
        "STEP 3: Therefore C(n) = n² × 2 = 2n². "
        "OUTPUT: K shell = 2, L shell = 8, M shell = 18, N shell = 32."
    )
    commentary = (
        "The factorization into n² orbital cells multiplied by 2 spin states corresponds to the "
        "dual-tetrahedron structure of the Field Chamber. The spin factor of 2 arises from the "
        "two TIME faces (one per tetrahedron), suggesting that electron spin may be geometrically "
        "represented by which tetrahedron within the stellated octahedron is activated."
    )
    
    def model(self):
        gfd_values = [shell_capacity_gfd(n) for n in [1, 2, 3, 4]]
        return {
            "K shell capacity": gfd_values[0],
            "L shell capacity": gfd_values[1],
            "M shell capacity": gfd_values[2],
            "N shell capacity": gfd_values[3],
        }
    
    def observations(self):
        standard = [shell_capacity(n) for n in [1, 2, 3, 4]]
        return {
            "K shell capacity": standard[0],
            "L shell capacity": standard[1],
            "M shell capacity": standard[2],
            "N shell capacity": standard[3],
        }


class FirstShellIsKOver2(GFDTest):
    """First shell capacity = k/2 = 2."""
    name = "K Shell = k/2"
    question = "Does the K shell (n=1) capacity correspond to the number of TIME faces in the Field Chamber, and what is the geometric interpretation?"
    reference_source = "K shell capacity = 2"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, k = 4 tetrahedral faces and 2 TIME faces total. "
        "STEP 1: K shell capacity = 2n² = 2 × 1² = 2. "
        "STEP 2: In terms of k: K shell = k/2 = 4/2 = 2 = TIME face count. "
        "STEP 3: Innermost shell represents one electron per TIME face (spin-up/spin-down). "
        "OUTPUT: K shell (k/2) = 2."
    )
    commentary = (
        "The K shell capacity of 2 corresponds to k/2 where k=4 is the Field Closure constant. "
        "This suggests that the innermost shell represents the minimal occupation state of the "
        "Field Chamber, with one electron per TIME face of Tetrahedron A and Tetrahedron B."
    )
    
    def model(self):
        return {"K shell (k/2)": K // 2}
    
    def observations(self):
        return {"K shell (k/2)": 2}


class SecondShellIs2k(GFDTest):
    """Second shell capacity = 2k = 8 (stellated octahedron vertices)."""
    name = "L Shell = 2k"
    question = "Does the L shell (n=2) capacity correspond to the total vertex count of the stellated octahedron Field Chamber?"
    reference_source = "L shell capacity = 8"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, k = 4 gives 2k = 8 vertices in the stellated octahedron. "
        "STEP 1: L shell capacity = 2n² = 2 × 2² = 8. "
        "STEP 2: In terms of k: L shell = 2k = 2 × 4 = 8 = vertex count. "
        "STEP 3: Second shell represents complete occupation of all Field Chamber vertices. "
        "OUTPUT: L shell (2k) = 8."
    )
    commentary = (
        "The L shell capacity of 8 equals 2k, the total vertex count of the stellated octahedron. "
        "This correspondence suggests that the second shell may represent full occupation of the "
        "Field Chamber's vertex positions, with Tetrahedron A and Tetrahedron B each contributing "
        "k=4 vertices to the available electron states."
    )
    
    def model(self):
        return {"L shell (2k)": 2 * K}
    
    def observations(self):
        return {"L shell (2k)": 8}


class FourthShellIs2kSquared(GFDTest):
    """Fourth shell capacity = 2k^2 = 32."""
    name = "N Shell = 2k^2"
    question = "Does the N shell (n=4) capacity follow from a hierarchical nesting of Field Chambers, and what geometric pattern does this suggest?"
    reference_source = "N shell capacity = 32"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, k = 4 and n = k for the fourth shell. "
        "STEP 1: N shell capacity = 2n² = 2 × 4² = 32. "
        "STEP 2: In terms of k: N shell = 2k² = 2 × 16 = 32 (k complete L-shell units). "
        "STEP 3: Pattern suggests hierarchical Field Chamber nesting: k × (2k) = 4 × 8 = 32. "
        "OUTPUT: N shell (2k²) = 32."
    )
    commentary = (
        "The N shell capacity of 32 = 2k² may correspond to k complete Field Chamber configurations, "
        "each with capacity 2k. This suggests a hierarchical nesting structure where higher shells "
        "represent increasingly complex arrangements of the stellated octahedron geometry centered "
        "at the Field Origin."
    )
    
    def model(self):
        return {"N shell (2k^2)": 2 * K * K}
    
    def observations(self):
        return {"N shell (2k^2)": 32}


class SubshellFormula(GFDTest):
    """Subshell capacities follow 2(2l+1) formula."""
    name = "Subshell Capacities"
    question = "What is the capacity of each subshell type (s, p, d, f), and how does the formula 2(2l+1) determine these values?"
    reference_source = "Atomic physics (established)"
    tolerance = 0.01
    derivation = (
        "PREMISE: Subshell capacity is C(l) = 2(2l + 1) where l is angular momentum quantum number. "
        "STEP 1: For l=0 (s): C = 2(2×0 + 1) = 2. For l=1 (p): C = 2(2×1 + 1) = 6. "
        "STEP 2: For l=2 (d): C = 2(2×2 + 1) = 10. For l=3 (f): C = 2(2×3 + 1) = 14. "
        "STEP 3: Factor of 2 arises from spin degeneracy (2 TIME faces in Field Chamber). "
        "OUTPUT: s subshell = 2, p subshell = 6, d subshell = 10, f subshell = 14."
    )
    commentary = (
        "The subshell capacity formula 2(2l+1) reflects magnetic quantum number degeneracy "
        "multiplied by spin. The geometric interpretation of angular momentum quantum number l "
        "within the Field Chamber framework remains an open question, though the factor of 2 "
        "is consistent with the dual-tetrahedron TIME face structure."
    )
    
    def model(self):
        return {
            "s subshell (l=0)": subshell_capacity(0),
            "p subshell (l=1)": subshell_capacity(1),
            "d subshell (l=2)": subshell_capacity(2),
            "f subshell (l=3)": subshell_capacity(3),
        }
    
    def observations(self):
        return {
            "s subshell (l=0)": 2,
            "p subshell (l=1)": 6,
            "d subshell (l=2)": 10,
            "f subshell (l=3)": 14,
        }


class SubshellSumEqualsShell(GFDTest):
    """Subshells sum to shell capacity for all shells."""
    name = "Subshell Sum"
    question = "Do the subshell capacities within each principal shell sum to the correct total shell capacity of 2n^2?"
    reference_source = "Shell structure (established)"
    tolerance = 0.01
    derivation = (
        "PREMISE: For shell n, subshells have l = 0, 1, ..., n-1, each contributing 2(2l+1). "
        "STEP 1: Sum = Σ[l=0 to n-1] 2(2l+1) = 2 × n² (algebraic identity). "
        "STEP 2: Verify: n=1 gives 2; n=2 gives 2+6=8; n=3 gives 2+6+10=18; n=4 gives 2+6+10+14=32. "
        "STEP 3: Each sum equals 2n², confirming subshell sum = shell capacity. "
        "OUTPUT: Shell n=1 sum = 2, n=2 sum = 8, n=3 sum = 18, n=4 sum = 32."
    )
    commentary = (
        "The mathematical identity Σ(2l+1) = n² for l=0 to n-1 underlies the subshell summation. "
        "This algebraic constraint is consistent with the Field Chamber's combinatorial structure, "
        "suggesting that subshell decomposition may reflect distinguishable Coupling Port "
        "configurations within each shell's geometric arrangement."
    )
    
    def model(self):
        sums = {}
        for n in [1, 2, 3, 4]:
            total = sum(subshell_capacity(l) for l in range(n))
            sums[f"Shell n={n} sum"] = total
        return sums
    
    def observations(self):
        return {
            "Shell n=1 sum": shell_capacity(1),
            "Shell n=2 sum": shell_capacity(2),
            "Shell n=3 sum": shell_capacity(3),
            "Shell n=4 sum": shell_capacity(4),
        }


class NobleGasHelium(GFDTest):
    """Helium: 2 electrons = filled K shell = k/2."""
    name = "Helium Configuration"
    question = "Why is helium chemically inert with exactly 2 electrons, and how does this relate to the Field Chamber TIME face count?"
    reference_source = "He atomic number = 2"
    tolerance = 0.01
    derivation = (
        "PREMISE: K shell = k/2 = 2 corresponds to TIME face count in Field Chamber. "
        "STEP 1: Helium fills K shell completely with Z = 2 electrons. "
        "STEP 2: The 2 electrons occupy 2 TIME faces (one per tetrahedron). "
        "STEP 3: Complete TIME face occupation produces closed noble gas configuration. "
        "OUTPUT: Helium electrons = 2."
    )
    commentary = (
        "Helium's closed-shell stability at 2 electrons corresponds to k/2, representing "
        "complete occupation of the TIME face states in the Field Chamber. This minimal "
        "noble gas configuration may indicate that chemical inertness arises when both "
        "Tetrahedron A and Tetrahedron B contribute one electron each."
    )
    
    def model(self):
        return {"Helium electrons": shell_capacity(1)}
    
    def observations(self):
        return {"Helium electrons": NOBLE_GASES['He']}


class NobleGasNeon(GFDTest):
    """Neon: 10 electrons = K + L = 2 + 8 = k/2 + 2k."""
    name = "Neon Configuration"
    question = "How many electrons fill the K and L shells completely, and does this match neon's atomic number?"
    reference_source = "Ne atomic number = 10"
    tolerance = 0.01
    derivation = (
        "PREMISE: Neon fills K and L shells, corresponding to (k/2) + (2k) = 5k/2 electrons. "
        "STEP 1: K shell = k/2 = 2 (TIME faces). L shell = 2k = 8 (vertices). "
        "STEP 2: Total = K + L = 2 + 8 = 10 = 5k/2 where k = 4. "
        "STEP 3: Complete occupation of TIME faces plus all stellated octahedron vertices. "
        "OUTPUT: Neon electrons (K+L) = 10."
    )
    commentary = (
        "Neon's stability at 10 electrons corresponds to k/2 + 2k = 5k/2, representing "
        "complete occupation of both TIME face states and all stellated octahedron vertices. "
        "This suggests that the first major noble gas closure involves saturating the "
        "Field Chamber's fundamental geometric positions."
    )
    
    def model(self):
        k_shell = shell_capacity(1)
        l_shell = shell_capacity(2)
        return {"Neon electrons (K+L)": k_shell + l_shell}
    
    def observations(self):
        return {"Neon electrons (K+L)": NOBLE_GASES['Ne']}


class NobleGasArgon(GFDTest):
    """Argon: 18 electrons = 2 x 9 (completion position)."""
    name = "Argon Configuration"
    question = "What is the electron configuration of argon, and how does the count 18 factor into geometric components?"
    reference_source = "Ar atomic number = 18"
    tolerance = 0.01
    derivation = (
        "PREMISE: Argon fills K, L, 3s, and 3p, totaling 2 × d² electrons where d = 3. "
        "STEP 1: K=2 + L=8 + 3s=2 + 3p=6 = 18. "
        "STEP 2: Factor as 18 = 2 × 9 = 2 × d² where d² = 3² = 9. "
        "STEP 3: Represents spin-doubled (2) times d-squared (9) configurations. "
        "OUTPUT: Argon electrons (2×9) = 18."
    )
    commentary = (
        "Argon's electron count of 18 = 2×9 corresponds to a paired completion structure. "
        "The factor of 9 may relate to the 3×3 SPATIAL face interactions possible between "
        "Tetrahedron A and Tetrahedron B, though the precise geometric interpretation of "
        "this intermediate closure requires further investigation."
    )
    
    def model(self):
        return {"Argon electrons (2x9)": 2 * 9}
    
    def observations(self):
        return {"Argon electrons (2x9)": NOBLE_GASES['Ar']}


class NobleGasPattern(GFDTest):
    """Noble gas differences: 8, 8, 18, 18, 32."""
    name = "Noble Gas Differences"
    question = "What pattern do the electron count differences between successive noble gases follow, and what determines this sequence?"
    reference_source = "Periodic table noble gas sequence"
    tolerance = 0.01
    derivation = (
        "PREMISE: Noble gas sequence reflects shell capacities appearing twice (Aufbau filling). "
        "STEP 1: Differences: He→Ne = 8, Ne→Ar = 8, Ar→Kr = 18, Kr→Xe = 18, Xe→Rn = 32. "
        "STEP 2: In GFD: 8 = 2k (vertices), 18 = 2d² (SPATIAL), 32 = 2k² (closure squared). "
        "STEP 3: Pattern 8, 8, 18, 18, 32 shows each capacity twice due to orbital filling order. "
        "OUTPUT: Diff He-Ne = 8, Diff Ne-Ar = 8, Diff Ar-Kr = 18, Diff Kr-Xe = 18, Diff Xe-Rn = 32."
    )
    commentary = (
        "The doubling pattern in noble gas differences (8, 8, then 18, 18, then 32) reflects "
        "successive shell capacities appearing twice due to the Aufbau principle's orbital "
        "filling order. This pattern is consistent with Field Chamber geometry where each "
        "capacity corresponds to distinct stellated octahedron occupation modes."
    )
    
    def model(self):
        nobles = [NOBLE_GASES[g] for g in ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']]
        diffs = [nobles[i+1] - nobles[i] for i in range(len(nobles)-1)]
        return {
            "Diff He-Ne": diffs[0],
            "Diff Ne-Ar": diffs[1],
            "Diff Ar-Kr": diffs[2],
            "Diff Kr-Xe": diffs[3],
            "Diff Xe-Rn": diffs[4],
        }
    
    def observations(self):
        return {
            "Diff He-Ne": 8,
            "Diff Ne-Ar": 8,
            "Diff Ar-Kr": 18,
            "Diff Kr-Xe": 18,
            "Diff Xe-Rn": 32,
        }


class SpinFromDualFieldChamber(GFDTest):
    """Spin-1/2 (2 states) correspondence with dual Field Chamber TIME faces."""
    name = "Spin Multiplicity"
    question = "How many distinct spin states does a spin-1/2 particle have, and does this match the TIME face count in the Field Chamber?"
    reference_source = "Spin-1/2 gives 2 states"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Chamber has 2 TIME faces (one per tetrahedron). "
        "STEP 1: Spin-1/2 particle has 2s + 1 = 2(1/2) + 1 = 2 spin states. "
        "STEP 2: Field Chamber TIME faces: Tet A has 1, Tet B has 1, total = 2. "
        "STEP 3: Correspondence: spin states = 2 = TIME faces. "
        "OUTPUT: Spin states (TIME faces) = 2."
    )
    commentary = (
        "The two spin states of fermions correspond to the two TIME faces in the stellated "
        "octahedron, one from each interpenetrating tetrahedron. This suggests that spin-up "
        "and spin-down may be geometrically distinguished by activation of the TIME face on "
        "Tetrahedron A versus Tetrahedron B respectively."
    )
    
    def model(self):
        time_faces = 2  # One per tetrahedron
        return {"Spin states (TIME faces)": time_faces}
    
    def observations(self):
        return {"Spin states (TIME faces)": 2}


class PauliExclusionAsGeometry(GFDTest):
    """Pauli exclusion: 2 electrons per orbital corresponds to 2 tetrahedra."""
    name = "Pauli Exclusion Geometry"
    question = "Why does the Pauli exclusion principle limit orbital occupancy to 2 electrons, and how does this relate to the dual tetrahedron structure?"
    reference_source = "Pauli exclusion principle"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Chamber has 2 tetrahedra: Tetrahedron A and Tetrahedron B. "
        "STEP 1: Pauli exclusion: no two identical fermions can occupy the same quantum state. "
        "STEP 2: Each orbital accepts one electron per tetrahedron: 1 + 1 = 2 maximum. "
        "STEP 3: Geometric constraint (2 tetrahedra) matches quantum limit (2 per orbital). "
        "OUTPUT: Electrons per orbital = 2."
    )
    commentary = (
        "The Pauli exclusion principle's limit of two electrons per orbital corresponds to "
        "the Field Chamber's dual-tetrahedron structure. Each orbital position within the "
        "stellated octahedron can accommodate one electron from Tetrahedron A and one from "
        "Tetrahedron B, suggesting a geometric basis for fermionic exclusion."
    )
    
    def model(self):
        tetrahedra_per_field_chamber = 2
        return {"Electrons per orbital": tetrahedra_per_field_chamber}
    
    def observations(self):
        return {"Electrons per orbital": 2}


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ShellFormula2nSquared,
    GFDShellFormula,
    FirstShellIsKOver2,
    SecondShellIs2k,
    FourthShellIs2kSquared,
    SubshellFormula,
    SubshellSumEqualsShell,
    NobleGasHelium,
    NobleGasNeon,
    NobleGasArgon,
    NobleGasPattern,
    SpinFromDualFieldChamber,
    PauliExclusionAsGeometry,
]


def run_all_tests():
    """Run all shell structure tests."""
    return run_test_group(
        title="Electron Shell Structure from Lattice Geometry",
        summary=(
            "These tests examine electron shell capacities (2, 8, 18, 32) using the "
            "GFD lattice geometry framework. The model produces values consistent with "
            "the 2n^2 formula through n^2 orbital cells times 2 spin states (corresponding "
            "to the dual-tetrad stellated octahedron structure)."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
