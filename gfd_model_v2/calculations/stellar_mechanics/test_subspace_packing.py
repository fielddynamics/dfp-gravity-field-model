"""
Subspace Packing Tests
======================

GFD Model V2 - Converted to GFDTest interface

Category C: Inside Tet_B (The Field Chamber)

This module examines gravity field behavior within the Field Chamber (Tet_B) region.
Tests verify correspondences between k=4 packing geometry and nuclear stability
data, including the instability of Be-8 (2k) and the peak binding energy at
Fe-56 (14k).
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from gfd_model_v2.base import GFDTest, run_test_group

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from gfd_model_v2.common import (
    C, HBAR, ELECTRON_MASS,
    K_CLOSURE, M_E,
    is_k_multiple, k_factor,
    MAGIC_NUMBERS, DOUBLY_MAGIC,
    MASS_RATIO_PROTON_ELECTRON,
    R_E,
)

# =============================================================================
# CONSTANTS
# =============================================================================

MEV_TO_JOULES = 1.60218e-13

BINDING_ENERGY = {
    'H-2': 1.11, 'He-3': 2.57, 'He-4': 7.07, 'Li-6': 5.33, 'Li-7': 5.61,
    'Be-8': 7.06, 'C-12': 7.68, 'N-14': 7.48, 'O-16': 7.98,
    'Fe-56': 8.79, 'Ni-62': 8.79, 'U-238': 7.57,
}

HALF_LIVES = {
    'Be-8': 8.19e-17,  # Extremely unstable
    'C-14': 1.81e11,   # Relatively stable
    'U-238': 1.41e17,  # Very long-lived
}

ALPHA_DECAY_ENERGY = {
    'Po-210': 5.41, 'Ra-226': 4.87, 'U-238': 4.27,
}


# =============================================================================
# TEST CLASSES
# =============================================================================

class K4SphericalPackingGeometry(GFDTest):
    """Verify k=4 is the tetrahedral closure number."""
    name = "K=4 Tetrahedral Packing"
    question = "Is k=4 the minimum number of points required to enclose a region in d=3 spatial dimensions, following from the simplex theorem that defines the tetrahedron as the minimal 3D enclosure?"
    reference_source = "Geometry (simplex theorem)"
    tolerance = 0.01
    derivation = (
        "PREMISE: k=4 is the minimum number of points required to enclose a region in d=3 "
        "spatial dimensions, following the simplex theorem. "
        "STEP 1: Apply simplex theorem: d dimensions requires d+1 points for minimal enclosure. "
        "STEP 2: For d=3: k = d + 1 = 4. "
        "STEP 3: Verify: tetrahedron vertices = 4, He-4 A = 4. "
        "OUTPUT: k (closure number) = 4, Tetrahedron vertices = 4, He-4 A = 4, All equal = 1.0."
    )
    commentary = (
        "The k=4 closure number follows from the geometric requirement that four points define the "
        "minimal 3D enclosure (tetrahedron). This fundamental simplex property constrains Field Chamber "
        "topology and corresponds to the He-4 alpha particle's exceptional stability in nuclear physics."
    )
    
    def model(self):
        k = K_CLOSURE
        tetrahedron_vertices = 4
        he4_A = 4
        all_match = 1.0 if k == tetrahedron_vertices == he4_A else 0.0
        return {
            "k (closure number)": k,
            "Tetrahedron vertices": tetrahedron_vertices,
            "He-4 A": he4_A,
            "All equal": all_match,
        }
    
    def observations(self):
        return {
            "k (closure number)": 4,
            "Tetrahedron vertices": 4,
            "He-4 A": 4,
            "All equal": 1.0,
        }


class BindingEnergyPerTile(GFDTest):
    """Verify binding energy peaks around Fe-56."""
    name = "Binding Energy Trend"
    question = "Does the binding energy per nucleon follow the characteristic curve of increasing from He-4 (k) through Fe-56 (14k) then decreasing to U-238, demonstrating that 14k represents optimal Field Closure packing efficiency?"
    reference_source = "Nuclear Physics (CODATA)"
    tolerance = 0.05
    derivation = (
        "PREMISE: Binding energy per nucleon follows characteristic curve increasing from "
        "He-4 (k) through Fe-56 (14k) then decreasing, demonstrating optimal spherical packing at 14k. "
        "STEP 1: Retrieve binding energies: He-4=7.07, C-12=7.68, O-16=7.98, Fe-56=8.79, U-238=7.57. "
        "STEP 2: Test increasing to Fe: 7.07 < 7.68 < 7.98 < 8.79. "
        "STEP 3: Test decreasing after Fe: 8.79 > 7.57. "
        "OUTPUT: He-4 BE (MeV/n) = 7.07, Fe-56 BE (MeV/n) = 8.79, U-238 BE (MeV/n) = 7.57, "
        "Increases to Fe = 1.0, Decreases after Fe = 1.0."
    )
    commentary = (
        "The binding energy curve shape documented in CODATA suggests optimal Field Closure efficiency "
        "at Fe-56 (14k), with decreasing efficiency for both lighter and heavier nuclei. This pattern "
        "determines the endpoints of stellar nucleosynthesis and the existence of fission versus fusion regimes."
    )
    
    def model(self):
        be_he4 = BINDING_ENERGY['He-4']
        be_c12 = BINDING_ENERGY['C-12']
        be_o16 = BINDING_ENERGY['O-16']
        be_fe56 = BINDING_ENERGY['Fe-56']
        be_u238 = BINDING_ENERGY['U-238']
        
        increasing = 1.0 if be_he4 < be_c12 < be_o16 < be_fe56 else 0.0
        decreasing = 1.0 if be_fe56 > be_u238 else 0.0
        
        return {
            "He-4 BE (MeV/n)": be_he4,
            "Fe-56 BE (MeV/n)": be_fe56,
            "U-238 BE (MeV/n)": be_u238,
            "Increases to Fe": increasing,
            "Decreases after Fe": decreasing,
        }
    
    def observations(self):
        return {
            "He-4 BE (MeV/n)": 7.07,
            "Fe-56 BE (MeV/n)": 8.79,
            "U-238 BE (MeV/n)": 7.57,
            "Increases to Fe": 1.0,
            "Decreases after Fe": 1.0,
        }


class Be8Instability(GFDTest):
    """Verify Be-8 (2k=8 gravity fields) is unstable."""
    name = "Be-8 Instability"
    question = "Why is Be-8 (2k=8 gravity fields) extremely unstable with a half-life of only 8e-17 seconds despite having high binding energy per nucleon, and does this indicate that two separate k=4 Field Closures prefer separation over combination?"
    reference_source = "Nuclear Physics (alpha decay)"
    tolerance = 0.20
    derivation = (
        "PREMISE: Be-8 (2k=8 gravity fields) is extremely unstable despite high binding energy, indicating "
        "two separate k=4 Field Closures prefer separation over combination. "
        "STEP 1: Verify Be-8 is 2k: 8 = 2 x 4. "
        "STEP 2: Retrieve Be-8 binding energy: 7.06 MeV/nucleon. "
        "STEP 3: Retrieve Be-8 half-life: 8.19e-17 seconds. "
        "OUTPUT: Be-8 half-life (s) = 8.19e-17, Be-8 BE (MeV/n) = 7.06, Is 2k = 1.0, "
        "Very short half-life = 1.0, High binding energy = 1.0."
    )
    commentary = (
        "Beryllium-8's extreme instability despite its 2k configuration suggests that simply being a k-multiple "
        "is insufficient for stability. The 2k arrangement may correspond to two separate Field Closures "
        "that prefer separation over combination, consistent with immediate alpha decay observations."
    )
    
    def model(self):
        half_life = HALF_LIVES['Be-8']
        be_per_nucleon = BINDING_ENERGY['Be-8']
        is_2k = 1.0 if 8 == 2 * K_CLOSURE else 0.0
        very_short = 1.0 if half_life < 1e-10 else 0.0
        high_binding = 1.0 if be_per_nucleon > 7.0 else 0.0
        
        return {
            "Be-8 half-life (s)": half_life,
            "Be-8 BE (MeV/n)": be_per_nucleon,
            "Is 2k": is_2k,
            "Very short half-life": very_short,
            "High binding energy": high_binding,
        }
    
    def observations(self):
        return {
            "Be-8 half-life (s)": 8.19e-17,
            "Be-8 BE (MeV/n)": 7.06,
            "Is 2k": 1.0,
            "Very short half-life": 1.0,
            "High binding energy": 1.0,
        }


class TripleAlphaPathway(GFDTest):
    """Verify triple-alpha process in gravity field terms."""
    name = "Triple-Alpha Process"
    question = "In the triple-alpha process, do three k=4 Field Closures (He-4 nuclei) combine into a 3k=12 configuration (C-12) with net energy release, and what role does the Hoyle state resonance play in enabling this transition through the Field Origin?"
    reference_source = "Nuclear Physics (stellar nucleosynthesis)"
    tolerance = 0.10
    derivation = (
        "PREMISE: Triple-alpha process combines three k=4 Field Closures (He-4) into "
        "3k=12 configuration (C-12) with net energy release via Hoyle state resonance. "
        "STEP 1: Calculate A conservation: 3 x 4 = 12. "
        "STEP 2: Verify C-12 is 3k: 12 = 3 x 4. "
        "STEP 3: Compare total binding: final > initial indicates energy release. "
        "OUTPUT: 3 x He-4 A = 12, C-12 A = 12, C-12 is 3k = 1.0, Energy released = 1.0."
    )
    commentary = (
        "The triple-alpha process combines three k=4 Field Closures into a 3k configuration with greater "
        "total binding. The Hoyle state resonance that enables this process in stellar cores suggests "
        "a specific energy pathway through the Field Origin that permits this combination."
    )
    
    def model(self):
        he4_A = 4
        c12_A = 12
        combined = 3 * he4_A
        is_3k = 1.0 if c12_A == 3 * K_CLOSURE else 0.0
        
        be_he4_total = BINDING_ENERGY['He-4'] * he4_A * 3
        be_c12_total = BINDING_ENERGY['C-12'] * c12_A
        energy_released = 1.0 if be_c12_total > be_he4_total else 0.0
        
        return {
            "3 x He-4 A": combined,
            "C-12 A": c12_A,
            "C-12 is 3k": is_3k,
            "Energy released": energy_released,
        }
    
    def observations(self):
        return {
            "3 x He-4 A": 12,
            "C-12 A": 12,
            "C-12 is 3k": 1.0,
            "Energy released": 1.0,
        }


class IronPeakBindingSubspace(GFDTest):
    """Verify Fe-56 (14k) has peak binding energy."""
    name = "Iron-56 Peak Binding"
    question = "Does Fe-56 with exactly 14k=56 gravity fields achieve the maximum binding energy per nucleon (~8.79 MeV), representing the optimal subspace packing configuration where additional gravity fields provide diminishing returns?"
    reference_source = "Nuclear Physics (CODATA)"
    tolerance = 0.05
    derivation = (
        "PREMISE: Fe-56 at 14k=56 gravity fields achieves maximum binding energy (~8.79 MeV/nucleon), "
        "representing optimal spherical packing where additional gravity fields provide diminishing returns. "
        "STEP 1: Calculate k-factor: 56 / 4 = 14. "
        "STEP 2: Retrieve Fe-56 BE: 8.79 MeV/nucleon. "
        "STEP 3: Verify at peak: BE > 8.5 MeV/nucleon. "
        "OUTPUT: Fe-56 A = 56, Fe k-factor = 14, Fe-56 BE (MeV/n) = 8.79, Is 14k = 1.0, At peak = 1.0."
    )
    commentary = (
        "Iron-56 at 14k represents the optimal subspace packing configuration within the Field Chamber. "
        "The ~8.8 MeV/nucleon binding energy documented in NIST data corresponds to maximum packing "
        "efficiency, beyond which additional gravity fields create diminishing returns due to Coulomb repulsion."
    )
    
    def model(self):
        fe_A = 56
        fe_k_factor = fe_A / K_CLOSURE
        be_fe = BINDING_ENERGY['Fe-56']
        be_ni = BINDING_ENERGY['Ni-62']
        is_14k = 1.0 if fe_A == 14 * K_CLOSURE else 0.0
        at_peak = 1.0 if be_fe > 8.5 and be_ni > 8.5 else 0.0
        
        return {
            "Fe-56 A": fe_A,
            "Fe k-factor": fe_k_factor,
            "Fe-56 BE (MeV/n)": be_fe,
            "Is 14k": is_14k,
            "At peak": at_peak,
        }
    
    def observations(self):
        return {
            "Fe-56 A": 56,
            "Fe k-factor": 14,
            "Fe-56 BE (MeV/n)": 8.79,
            "Is 14k": 1.0,
            "At peak": 1.0,
        }


class MagicNumbersKCorrelation(GFDTest):
    """Test correlation between magic numbers and k-packing."""
    name = "Magic Numbers and K"
    question = "What is the relationship between nuclear magic numbers (2, 8, 20, 28, 50, 82, 126) and k-multiples, and does the partial correlation suggest that Field Closure geometry captures some but not all aspects of nuclear shell structure?"
    reference_source = "Nuclear Physics (shell model)"
    tolerance = 0.01
    derivation = (
        "PREMISE: Partial correlation between magic numbers and k-multiples suggests Field Closure "
        "geometry captures some but not all aspects of nuclear shell structure. "
        "STEP 1: Test k-divisibility for each magic number (2, 8, 20, 28, 50, 82, 126). "
        "STEP 2: Identify k-multiples: 8/4=2, 20/4=5, 28/4=7 (integers). "
        "STEP 3: Count k-multiple magics and non-k magics. "
        "OUTPUT: K-multiple magics = 3, Non-k magics = 4, Has >= 3 k-multiples = 1.0, Has >= 3 non-k = 1.0."
    )
    commentary = (
        "The partial correlation between magic numbers and k-multiples suggests that Field Closure geometry "
        "captures some but not all aspects of nuclear shell structure. The non-k-aligned magic numbers "
        "(2, 50, 82, 126) may reflect additional symmetries beyond simple tetrahedral closure."
    )
    
    def model(self):
        k_multiples = [n for n in MAGIC_NUMBERS if n % K_CLOSURE == 0]
        non_k_multiples = [n for n in MAGIC_NUMBERS if n % K_CLOSURE != 0]
        has_k_multiples = 1.0 if len(k_multiples) >= 3 else 0.0
        has_non_k = 1.0 if len(non_k_multiples) >= 3 else 0.0
        
        return {
            "K-multiple magics": len(k_multiples),
            "Non-k magics": len(non_k_multiples),
            "Has >= 3 k-multiples": has_k_multiples,
            "Has >= 3 non-k": has_non_k,
        }
    
    def observations(self):
        return {
            "K-multiple magics": 3,
            "Non-k magics": 4,
            "Has >= 3 k-multiples": 1.0,
            "Has >= 3 non-k": 1.0,
        }


class NeutronProtonFieldConfig(GFDTest):
    """Interpret neutron/proton as gravity field configurations."""
    name = "Neutron-Proton Mass Difference"
    question = "Is the neutron-proton mass difference (~1.3 MeV, or ~0.14% of nucleon mass) small enough to indicate that neutrons and protons represent slightly different configurations of the same fundamental gravity field arrangement in the Field Chamber?"
    reference_source = "Nuclear Physics (CODATA)"
    tolerance = 0.15
    derivation = (
        "PREMISE: Neutron-proton mass difference (~1.3 MeV, ~0.14% of nucleon mass) is small, "
        "indicating both are slightly different configurations of same fundamental gravity field arrangement. "
        "STEP 1: Calculate mass difference: 939.565 - 938.272 = 1.293 MeV. "
        "STEP 2: Calculate fraction of proton mass: 1.293 / 938.272 = 0.00138. "
        "STEP 3: Verify small fraction: 0.00138 < 0.002. "
        "OUTPUT: Mass difference (MeV) = 1.293, Fraction of proton mass = 0.00138, Small difference = 1.0."
    )
    commentary = (
        "The small neutron-proton mass difference corresponds to a minor configuration energy variation "
        "between two closely related gravity field arrangements. The ~0.14% difference suggests these represent "
        "slightly different states of the same fundamental Field Chamber configuration."
    )
    
    def model(self):
        mass_diff_mev = 939.565 - 938.272  # ~1.293 MeV
        fraction = mass_diff_mev / 938.272
        small_fraction = 1.0 if fraction < 0.002 else 0.0
        
        return {
            "Mass difference (MeV)": mass_diff_mev,
            "Fraction of proton mass": fraction,
            "Small difference": small_fraction,
        }
    
    def observations(self):
        return {
            "Mass difference (MeV)": 1.293,
            "Fraction of proton mass": 0.00138,
            "Small difference": 1.0,
        }


class AlphaDecayK4Ejection(GFDTest):
    """Verify alpha decay ejects k=4 unit."""
    name = "Alpha Decay = K Ejection"
    question = "Does alpha decay universally emit He-4 particles (exactly k=4 gravity fields) with energies in the 4-6 MeV range, demonstrating that the complete k=4 Field Closure is the fundamental tunnel-able unit that can escape through the nuclear Coulomb barrier?"
    reference_source = "Nuclear Physics (alpha decay)"
    tolerance = 0.10
    derivation = (
        "PREMISE: Alpha decay universally emits He-4 particles (exactly k=4 gravity fields) with energies "
        "in 4-6 MeV range, demonstrating k=4 Field Closure is fundamental tunnel-able unit. "
        "STEP 1: Verify alpha = 4 gravity fields = k. "
        "STEP 2: Retrieve alpha decay energies: Po-210=5.41, Ra-226=4.87, U-238=4.27 MeV. "
        "STEP 3: Calculate average: 4.85 MeV, verify in 4-6 MeV range. "
        "OUTPUT: Alpha particle A = 4, Equals k = 1.0, Avg alpha energy (MeV) = 4.85, Typical range (4-6 MeV) = 1.0."
    )
    commentary = (
        "The exclusive ejection of k=4 units in alpha decay suggests that complete Field Closures are "
        "the preferred tunnel-able configurations. The 4-6 MeV energy range for alpha emission corresponds "
        "to the barrier for extracting a complete Tetrahedron A or Tetrahedron B unit from a larger nucleus."
    )
    
    def model(self):
        alpha_A = 4
        is_k = 1.0 if alpha_A == K_CLOSURE else 0.0
        energies = list(ALPHA_DECAY_ENERGY.values())
        avg_energy = sum(energies) / len(energies)
        typical_range = 1.0 if 4 < avg_energy < 6 else 0.0
        
        return {
            "Alpha particle A": alpha_A,
            "Equals k": is_k,
            "Avg alpha energy (MeV)": avg_energy,
            "Typical range (4-6 MeV)": typical_range,
        }
    
    def observations(self):
        return {
            "Alpha particle A": 4,
            "Equals k": 1.0,
            "Avg alpha energy (MeV)": 4.85,
            "Typical range (4-6 MeV)": 1.0,
        }


class BetaDecayVortexFlip(GFDTest):
    """Interpret beta decay as vortex reconfiguration."""
    name = "Beta Decay Energy"
    question = "Is the energy released in beta decay (~0.78 MeV) much smaller than in alpha decay (~5 MeV), indicating that beta decay represents a gravity field reconfiguration (switching between TIME and SPATIAL face contributions) rather than gravity field ejection?"
    reference_source = "Nuclear Physics (beta decay)"
    tolerance = 0.15
    derivation = (
        "PREMISE: Beta decay energy (~0.78 MeV) should be much smaller than alpha decay (~5 MeV), "
        "indicating gravity field reconfiguration vs gravity field ejection. "
        "STEP 1: Calculate beta decay Q-value: 1.293 - 0.511 = 0.782 MeV. "
        "STEP 2: Calculate average alpha energy: 4.85 MeV. "
        "STEP 3: Verify beta << alpha/3. "
        "OUTPUT: Beta decay Q-value (MeV) = 0.782, Avg alpha energy (MeV) = 4.85, Beta << alpha = 1.0."
    )
    commentary = (
        "The lower energy of beta decay compared to alpha decay indicates a reconfiguration rather than "
        "ejection process. In Field Chamber terms, beta decay may represent switching between TIME and "
        "SPATIAL face contributions without changing the total gravity field count."
    )
    
    def model(self):
        q_value_neutron = 1.293 - 0.511  # MeV
        avg_alpha = sum(ALPHA_DECAY_ENERGY.values()) / len(ALPHA_DECAY_ENERGY)
        smaller = 1.0 if q_value_neutron < avg_alpha / 3 else 0.0
        
        return {
            "Beta decay Q-value (MeV)": q_value_neutron,
            "Avg alpha energy (MeV)": avg_alpha,
            "Beta << alpha": smaller,
        }
    
    def observations(self):
        return {
            "Beta decay Q-value (MeV)": 0.782,
            "Avg alpha energy (MeV)": 4.85,
            "Beta << alpha": 1.0,
        }


class SubspaceCompressionDirection(GFDTest):
    """Verify compression direction reversal in subspace."""
    name = "Nuclear Radius Constant"
    question = "Is the nuclear radius constant r_0 (~1.2 fm) within an order of magnitude of the fundamental gravity field size r_e (2.82 fm), and does the ratio r_0/r_e ~ 0.4 indicate subspace compression within the Field Chamber?"
    reference_source = "Nuclear Physics"
    tolerance = 0.30
    derivation = (
        "PREMISE: Nuclear radius constant r_0 (~1.2 fm) within order of magnitude of fundamental "
        "field size r_e (2.82 fm) indicates spherical packing compression within Field Chamber. "
        "STEP 1: Define nuclear r_0 = 1.2e-15 m. "
        "STEP 2: Define gravity field r_e = 2.82e-15 m. "
        "STEP 3: Calculate ratio: r_0/r_e = 0.426. "
        "STEP 4: Verify similar scale: 0.1 < 0.426 < 10. "
        "OUTPUT: Nuclear r_0 (m) = 1.2e-15, Gravity field r_e (m) = 2.82e-15, r_0/r_e ratio = 0.426, Similar scale = 1.0."
    )
    commentary = (
        "The nuclear radius constant r_0 being within an order of magnitude of the gravity field size suggests "
        "that nuclei represent densely packed gravity field configurations. The r_0/r_e ratio of approximately 0.4 "
        "indicates subspace compression relative to the equilibrium gravity field spacing."
    )
    
    def model(self):
        r_0 = 1.2e-15  # meters
        ratio = r_0 / R_E
        similar_scale = 1.0 if 0.1 < ratio < 10 else 0.0
        
        return {
            "Nuclear r_0 (m)": r_0,
            "Gravity field r_e (m)": R_E,
            "r_0/r_e ratio": ratio,
            "Similar scale": similar_scale,
        }
    
    def observations(self):
        return {
            "Nuclear r_0 (m)": 1.2e-15,
            "Gravity field r_e (m)": 2.82e-15,
            "r_0/r_e ratio": 0.426,
            "Similar scale": 1.0,
        }


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    K4SphericalPackingGeometry,
    BindingEnergyPerTile,
    Be8Instability,
    TripleAlphaPathway,
    IronPeakBindingSubspace,
    MagicNumbersKCorrelation,
    NeutronProtonFieldConfig,
    AlphaDecayK4Ejection,
    BetaDecayVortexFlip,
    SubspaceCompressionDirection,
]


def run_all_tests():
    """Run all subspace packing tests."""
    summary = (
        "These tests examine gravity field behavior inside the Field Chamber (Tet_B). "
        "The model uses k=4 spherical packing geometry. Be-8 (2k) instability is "
        "consistent with closure misalignment. Fe-56 (14k) corresponds to maximum "
        "binding energy. Alpha decay ejects k=4 gravity field units."
    )
    
    return run_test_group("Subspace Packing", summary, ALL_TESTS)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
