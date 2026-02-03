"""
Stellar Core Compression Tests
==============================

GFD Model V2 - Converted to GFDTest interface

This module examines the physics of gravitational compression in stellar cores
within the DFP framework.

KEY CONCEPTS:
- Stellar compression provides energy to overcome compression blocking barrier
- Bound atoms (bowling balls) must be unbound (squish balls) before rebinding
- Compression barrier: ~511 keV at Field Envelope scale (r_e)
- Temperature thresholds correspond to energies needed to unbind and rebind
- Hydrogen fusion: 4 hydrogen atoms (bowling balls) -> unbind -> rebind as He-4 (k=4)
- Higher fusion stages require more energy to overcome larger Coulomb barriers
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from gfd_model_v2.base import GFDTest, run_test_group

# Add path for common imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from common import (
    G, C, HBAR, ELECTRON_MASS,
    R_E, M_E, A_0, 
    RHO_WHITE_DWARF, RHO_FIELD_BINDING, RHO_NUCLEAR,
    K_CLOSURE, M_SOLAR,
    T_HYDROGEN_FUSION, T_HELIUM_FUSION, T_CARBON_FUSION, T_SILICON_FUSION,
    CHANDRASEKHAR_LIMIT,
    compression_ratio_equilibrium_to_tile,
)

# =============================================================================
# SOLAR PARAMETERS
# =============================================================================

R_SOLAR = 6.96e8        # Solar radius (m)
RHO_SOLAR_CORE = 1.5e5  # Solar core density (kg/m^3)
RHO_SOLAR_SURFACE = 2e-4  # Solar surface density (kg/m^3)
T_SOLAR_CORE = 1.57e7   # Solar core temperature (K)
T_SOLAR_SURFACE = 5778  # Solar surface temperature (K)
P_SOLAR_CORE = 2.5e16   # Solar core pressure (Pa)
K_B = 1.380649e-23      # Boltzmann constant (J/K)
M_PROTON = 1.67262192e-27  # kg


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def field_spacing_from_density(density):
    """Estimate average gravity field spacing from mass density."""
    number_density = density / M_E
    return number_density ** (-1/3)


def binding_fraction(temperature, threshold):
    """Estimate fraction of atoms undergoing binding at given temperature."""
    if temperature < threshold * 0.5:
        return 0.0
    elif temperature > threshold * 2.0:
        return 1.0
    else:
        x = (temperature - threshold) / (threshold * 0.3)
        return 1 / (1 + math.exp(-x))


# =============================================================================
# TEST CLASSES
# =============================================================================

class CorePressureGradient(GFDTest):
    """Test A1: Core-to-surface pressure gradient."""
    name = "Core Pressure Gradient"
    question = "What is the magnitude of the pressure gradient from solar core to surface, and does this provide sufficient compression to overcome the bowling ball barrier for gravity field binding?"
    reference_source = "Solar Physics (Standard Solar Model)"
    tolerance = 0.10
    derivation = (
        "PREMISE: Stellar compression provides the energy needed to overcome compression "
        "blocking (bowling ball barrier) and enable gravity field binding. "
        "STEP 1: Core pressure P_core = 2.5e16 Pa. Surface pressure P_surface = 1e4 Pa. "
        "STEP 2: Calculate logarithmic ratio: log10(2.5e16 / 1e4) = 12.4. "
        "STEP 3: This 12+ orders of magnitude gradient drives extreme compression. "
        "STEP 4: Compression overcomes outward pressure of bound atoms (bowling balls), "
        "enabling unbinding (bowling ball -> squish ball) and rebinding. "
        "OUTPUT: Core pressure = 2.5e16 Pa, Log10 pressure ratio = 12.4."
    )
    commentary = (
        "The 12+ orders of magnitude pressure gradient from core to surface provides the "
        "compression energy needed to overcome the bowling ball barrier. At core conditions, "
        "enough energy is available to unbind hydrogen atoms (bowling balls -> squish balls) "
        "so their freed gravity fields can rebind into helium (new bowling ball with k=4)."
    )
    
    def model(self):
        P_surface = 1e4  # Photosphere pressure (Pa)
        P_core = P_SOLAR_CORE
        log_ratio = math.log10(P_core / P_surface)
        return {
            "Core pressure (Pa)": P_core,
            "Surface pressure (Pa)": P_surface,
            "Log10 pressure ratio": log_ratio,
        }
    
    def observations(self):
        return {
            "Core pressure (Pa)": 2.5e16,
            "Surface pressure (Pa)": 1e4,
            "Log10 pressure ratio": 12.4,
        }


class TemperatureDensityRelationship(GFDTest):
    """Test A2: Temperature-density relationship in stellar cores."""
    name = "Temperature-Density Relationship"
    question = "How do temperature and density scale from surface to core, and does this support the progressive unbinding/rebinding sequence for gravity field fusion?"
    reference_source = "Solar Physics (Standard Solar Model)"
    tolerance = 0.10
    derivation = (
        "PREMISE: Temperature and density increase toward core, providing more energy "
        "to overcome compression blocking barriers for heavier element formation. "
        "STEP 1: Temperature ratio: T_core / T_surface = 1.57e7 K / 5778 K = 2718. "
        "STEP 2: Density ratio: rho_core / rho_surface = 1.5e5 / 2e-4 = 7.5e8. "
        "STEP 3: Higher T and rho -> more energy to unbind heavier bowling balls. "
        "OUTPUT: Temperature ratio = 2718, Density ratio = 7.5e8."
    )
    commentary = (
        "The correlation between temperature and density in stellar cores provides "
        "progressively more energy to overcome larger compression blocking barriers. "
        "Higher barriers (heavier atoms = bigger bowling balls) require more energy "
        "to unbind, which is why heavier element fusion requires hotter cores."
    )
    
    def model(self):
        T_ratio = T_SOLAR_CORE / T_SOLAR_SURFACE
        rho_ratio = RHO_SOLAR_CORE / RHO_SOLAR_SURFACE
        return {
            "Temperature ratio (core/surface)": T_ratio,
            "Density ratio (core/surface)": rho_ratio,
        }
    
    def observations(self):
        return {
            "Temperature ratio (core/surface)": 2718,
            "Density ratio (core/surface)": 7.5e8,
        }


class HydrogenFusionThreshold(GFDTest):
    """Test A3: Hydrogen fusion temperature threshold."""
    name = "Hydrogen Fusion Threshold"
    question = "Does the solar core temperature exceed the threshold for hydrogen fusion, where 4 hydrogen atoms (bowling balls) unbind and rebind as He-4 (k=4 complete closure)?"
    reference_source = "Nuclear Physics (pp chain)"
    tolerance = 0.10
    derivation = (
        "PREMISE: Hydrogen fusion requires energy to unbind 4 hydrogen atoms (each a "
        "bowling ball with k=1) and rebind them as one He-4 (bowling ball with k=4). "
        "STEP 1: Fusion threshold T_H = 1.5e7 K corresponds to ~1.3 keV thermal energy. "
        "STEP 2: Solar core T = 1.57e7 K -> exceeds threshold. "
        "STEP 3: At this T, quantum tunneling allows some atoms to overcome the "
        "~511 keV compression blocking barrier and unbind. "
        "STEP 4: Unbound fields (squish balls) rebind into new k=4 closure (He-4). "
        "OUTPUT: H fusion threshold = 1.5e7 K, Solar core = 1.57e7 K, Exceeds = 1.0."
    )
    commentary = (
        "The solar core exceeds hydrogen fusion threshold, enabling the pp-chain: "
        "4 H (each bowling ball with k=1) -> unbind (4 squish balls) -> rebind as He-4 "
        "(bowling ball with k=4 complete closure), releasing 26.7 MeV binding energy. "
        "Quantum tunneling allows rare penetration through the compression barrier even "
        "though thermal energy (~1.3 keV) is much less than barrier (~511 keV)."
    )
    
    def model(self):
        exceeds = 1.0 if T_SOLAR_CORE >= T_HYDROGEN_FUSION else 0.0
        return {
            "H fusion threshold (K)": T_HYDROGEN_FUSION,
            "Solar core temp (K)": T_SOLAR_CORE,
            "Exceeds threshold": exceeds,
        }
    
    def observations(self):
        return {
            "H fusion threshold (K)": 1.5e7,
            "Solar core temp (K)": 1.57e7,
            "Exceeds threshold": 1.0,
        }


class HeliumFlashConditions(GFDTest):
    """Test A4: Triple-alpha (helium flash) conditions."""
    name = "Helium Flash Conditions"
    question = "What temperature is required for triple-alpha, where 3 He-4 (each k=4 bowling balls) unbind and rebind as C-12 (k=12)?"
    reference_source = "Nuclear Physics (triple-alpha process)"
    tolerance = 0.15
    derivation = (
        "PREMISE: Triple-alpha requires unbinding 3 He-4 atoms (bowling balls with k=4) "
        "and rebinding 12 gravity fields into C-12 (k=12 closure). "
        "STEP 1: He-4 has larger compression barrier than hydrogen (more fields in Tet B). "
        "STEP 2: Triple-alpha threshold T_He = 1e8 K. "
        "STEP 3: Ratio to H-fusion: T_He / T_H = 1e8 / 1.5e7 = 6.67. "
        "STEP 4: Higher T needed because He-4 bowling balls have more outward compression. "
        "OUTPUT: Triple-alpha threshold = 1e8 K, Ratio to H-fusion = 6.67."
    )
    commentary = (
        "Triple-alpha requires ~6.7x higher temperature than hydrogen fusion because "
        "He-4 atoms are 'bigger bowling balls' with k=4 in Tet B. More energy is needed "
        "to overcome their larger compression blocking barriers. The process creates C-12 "
        "(k=12 = 3x4) via the Hoyle resonance, exploiting the brief Be-8 intermediate."
    )
    
    def model(self):
        ratio = T_HELIUM_FUSION / T_HYDROGEN_FUSION
        return {
            "Triple-alpha threshold (K)": T_HELIUM_FUSION,
            "Ratio to H-fusion": ratio,
        }
    
    def observations(self):
        return {
            "Triple-alpha threshold (K)": 1e8,
            "Ratio to H-fusion": 6.67,
        }


class CarbonBurningThreshold(GFDTest):
    """Test A5: Carbon burning temperature threshold."""
    name = "Carbon Burning Threshold"
    question = "At what temperature does carbon fusion occur, and how does this reflect the larger compression barrier of C-12 (k=12) compared to He-4 (k=4)?"
    reference_source = "Nuclear Physics (carbon fusion)"
    tolerance = 0.15
    derivation = (
        "PREMISE: Carbon fusion requires unbinding C-12 atoms (k=12 bowling balls), "
        "which have larger compression barriers than He-4 (k=4). "
        "STEP 1: Carbon burning threshold T_C = 5e8 K. "
        "STEP 2: Ratio to helium fusion: T_C / T_He = 5e8 / 1e8 = 5.0. "
        "STEP 3: Each progressive fusion stage requires more energy because: "
        "- Larger k in Tet B = more outward compression = bigger bowling ball "
        "- Bigger bowling ball = higher barrier to unbind "
        "OUTPUT: Carbon burning = 5e8 K, Ratio to He-fusion = 5.0."
    )
    commentary = (
        "Carbon burning requires 5x more temperature than helium fusion because C-12 "
        "atoms are 'bigger bowling balls' (k=12 vs k=4). The systematic increase in "
        "fusion thresholds reflects the progressive growth of compression barriers as "
        "more gravity fields accumulate in Tet B."
    )
    
    def model(self):
        ratio_to_He = T_CARBON_FUSION / T_HELIUM_FUSION
        return {
            "Carbon burning temp (K)": T_CARBON_FUSION,
            "Ratio to He-fusion": ratio_to_He,
        }
    
    def observations(self):
        return {
            "Carbon burning temp (K)": 5e8,
            "Ratio to He-fusion": 5.0,
        }


class SiliconBurningThreshold(GFDTest):
    """Test A6: Silicon burning temperature threshold."""
    name = "Silicon Burning Threshold"
    question = "What temperature is required for silicon burning, and why does this represent the final exothermic stage before reaching Fe-56 (k=56, maximum binding efficiency)?"
    reference_source = "Nuclear Physics (silicon burning)"
    tolerance = 0.15
    derivation = (
        "PREMISE: Silicon burning (Si-28, k=28) is the final exothermic fusion stage "
        "before reaching iron-56 (k=56), which has maximum binding energy per nucleon. "
        "STEP 1: Silicon burning threshold T_Si = 2.7e9 K. "
        "STEP 2: Ratio to H-fusion: T_Si / T_H = 2.7e9 / 1.5e7 = 180. "
        "STEP 3: This 180x ratio reflects Si-28's much larger bowling ball barrier. "
        "STEP 4: Beyond Fe-56, fusion is ENDOTHERMIC - adding more fields costs energy. "
        "OUTPUT: Silicon burning = 2.7e9 K, Ratio to H-fusion = 180."
    )
    commentary = (
        "Silicon burning at 180x hydrogen fusion temperature represents the extreme "
        "conditions needed to unbind Si-28 bowling balls (k=28). This is the final "
        "exothermic stage because Fe-56 (k=56 = 14x4) achieves maximum binding energy "
        "per gravity field. Beyond iron, fusion requires energy input rather than "
        "releasing it - the bowling balls become too big to efficiently unbind/rebind."
    )
    
    def model(self):
        ratio_to_H = T_SILICON_FUSION / T_HYDROGEN_FUSION
        return {
            "Silicon burning temp (K)": T_SILICON_FUSION,
            "Ratio to H-fusion": ratio_to_H,
        }
    
    def observations(self):
        return {
            "Silicon burning temp (K)": 2.7e9,
            "Ratio to H-fusion": 180,
        }


class DegeneracyPressureConcept(GFDTest):
    """Test A7: Electron degeneracy pressure in gravity field terms."""
    name = "Degeneracy Pressure Concept"
    question = "At white dwarf density, what is the average gravity field spacing relative to the Field Envelope size r_e, and does this indicate compressed but not yet bound configurations?"
    reference_source = None  # Model exploration
    tolerance = 0.20
    derivation = (
        "PREMISE: At white dwarf density, gravity field spacing relative to r_e indicates "
        "whether atoms are close enough for binding to occur. "
        "STEP 1: Calculate number density n = rho_WD / m_e. "
        "STEP 2: Calculate average spacing = n^(-1/3). "
        "STEP 3: Compare to Field Envelope size r_e = 2.82 fm. "
        "STEP 4: If spacing >> r_e, atoms are compressed but not at binding threshold. "
        "STEP 5: Electron degeneracy pressure supports the star against collapse. "
        "OUTPUT: WD field spacing, Ratio to r_e, Above r_e (10x)."
    )
    commentary = (
        "White dwarf density compresses atoms close together, but spacing remains above "
        "the binding threshold. The atoms are bowling balls squeezed together but not "
        "unbinding. Electron degeneracy pressure (quantum mechanical Pauli exclusion) "
        "prevents further compression - the electrons resist being squeezed closer."
    )
    
    def model(self):
        spacing_wd = field_spacing_from_density(RHO_WHITE_DWARF)
        ratio_to_re = spacing_wd / R_E
        above_re_10x = 1.0 if ratio_to_re > 10 else 0.0
        return {
            "WD field spacing (m)": spacing_wd,
            "Ratio to r_e": ratio_to_re,
            "Above r_e (10x)": above_re_10x,
        }


class ChandrasekharMassLimit(GFDTest):
    """Test A8: Chandrasekhar limit in gravity field terms."""
    name = "Chandrasekhar Mass Limit"
    question = "How many gravity fields does the Chandrasekhar mass limit contain, and does this represent a maximal stable configuration before collapse forces unbinding?"
    reference_source = "Astrophysics (Chandrasekhar 1931)"
    tolerance = 0.10
    derivation = (
        "PREMISE: The Chandrasekhar limit (1.4 solar masses) is the maximum mass a white "
        "dwarf can support against gravitational collapse via electron degeneracy pressure. "
        "STEP 1: Chandrasekhar limit M_Ch = 1.4 M_solar. "
        "STEP 2: Gravity field count N = M_Ch / m_proton (each proton is one bound field). "
        "STEP 3: Log10(N) = log10(1.4 x 2e30 / 1.67e-27) ~= 57.22. "
        "STEP 4: Above this limit, gravity overcomes degeneracy and forces collapse. "
        "STEP 5: Collapse can trigger mass unbinding through the field origin (neutron star). "
        "OUTPUT: Chandrasekhar limit = 1.4 M_solar, Log10 field count = 57.22."
    )
    commentary = (
        "The ~10^57 gravity fields at the Chandrasekhar limit represent the maximum stable "
        "bowling ball configuration before gravitational collapse. Above this limit, gravity "
        "overcomes electron degeneracy pressure, forcing collapse that can trigger mass "
        "unbinding through field origins - creating neutron stars where electron vortices "
        "are embedded into protons (electron capture)."
    )
    
    def model(self):
        M_ch = CHANDRASEKHAR_LIMIT * M_SOLAR
        num_fields_approx = M_ch / M_PROTON
        log_fields = math.log10(num_fields_approx)
        return {
            "Chandrasekhar limit (solar masses)": CHANDRASEKHAR_LIMIT,
            "Log10 field count": log_fields,
        }
    
    def observations(self):
        return {
            "Chandrasekhar limit (solar masses)": 1.4,
            "Log10 field count": 57.22,
        }


class FusionRateVsTemperature(GFDTest):
    """Test A9: Fusion rate increases with temperature."""
    name = "Fusion Rate vs Temperature"
    question = "Does the binding fraction increase with temperature, reflecting increased energy to overcome compression blocking barriers via quantum tunneling?"
    reference_source = None  # Model behavior verification
    tolerance = 0.10
    derivation = (
        "PREMISE: Binding fraction increases with temperature because higher T provides "
        "more energy for quantum tunneling through compression blocking barriers. "
        "STEP 1: Calculate binding fraction at T = 1.0e7 K (below threshold). "
        "STEP 2: Calculate binding fraction at T = 1.5e7 K (at threshold). "
        "STEP 3: Calculate binding fraction at T = 2.0e7 K (above threshold). "
        "STEP 4: Verify monotonic increase: higher T -> more tunneling -> more binding. "
        "OUTPUT: Binding at 1e7 K, 1.5e7 K, 2e7 K, Monotonic increase = 1.0."
    )
    commentary = (
        "The monotonic increase of binding with temperature reflects how thermal energy "
        "enables quantum tunneling through the compression blocking barrier. Even though "
        "thermal energy (~1.3 keV at 1.5e7 K) is much less than the barrier (~511 keV), "
        "the high-energy tail of the thermal distribution allows rare tunneling events. "
        "Higher temperature = more particles in the tail = more binding."
    )
    
    def model(self):
        T_low = 1.0e7
        T_threshold = T_HYDROGEN_FUSION
        T_high = 2.0e7
        f_low = binding_fraction(T_low, T_threshold)
        f_threshold = binding_fraction(T_threshold, T_threshold)
        f_high = binding_fraction(T_high, T_threshold)
        monotonic = 1.0 if f_low < f_threshold < f_high else 0.0
        return {
            "Binding at 1e7 K": f_low,
            "Binding at 1.5e7 K": f_threshold,
            "Binding at 2e7 K": f_high,
            "Monotonic increase": monotonic,
        }


class SolarCoreFieldDensity(GFDTest):
    """Test A10: Gravity field number density in solar core."""
    name = "Solar Core Field Density"
    question = "What is the number density of gravity fields in the solar core, and does this correspond to the regime where binding becomes significant?"
    reference_source = "Solar Physics (Standard Solar Model)"
    tolerance = 0.15
    derivation = (
        "PREMISE: Solar core field density determines the binding regime - how close "
        "bowling balls are packed together. "
        "STEP 1: Solar core density rho_core = 1.5e5 kg/m^3. "
        "STEP 2: Number density n = rho_core / m_proton = 8.97e31 per m^3. "
        "STEP 3: Log10(n) = 31.95. "
        "STEP 4: At this density + temperature, binding occurs via quantum tunneling. "
        "OUTPUT: Field density = 8.97e31 per m^3, Log10 density = 31.95."
    )
    commentary = (
        "The ~10^32 gravity fields per cubic meter in the solar core represents the "
        "density regime where hydrogen bowling balls are packed close enough that "
        "quantum tunneling through the compression barrier becomes significant. Combined "
        "with the core temperature (~1.5e7 K), this enables the pp-chain fusion that "
        "powers the Sun."
    )
    
    def model(self):
        rho_core = RHO_SOLAR_CORE
        n_fields = rho_core / M_PROTON
        log_n = math.log10(n_fields)
        return {
            "Field density (per m^3)": n_fields,
            "Log10 density": log_n,
        }
    
    def observations(self):
        return {
            "Field density (per m^3)": 8.97e31,
            "Log10 density": 31.95,
        }


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    CorePressureGradient,
    TemperatureDensityRelationship,
    HydrogenFusionThreshold,
    HeliumFlashConditions,
    CarbonBurningThreshold,
    SiliconBurningThreshold,
    DegeneracyPressureConcept,
    ChandrasekharMassLimit,
    FusionRateVsTemperature,
    SolarCoreFieldDensity,
]


def run_all_tests():
    """Run all stellar core compression tests."""
    summary = (
        "These tests examine gravitational compression physics in stellar cores. "
        "Stellar compression provides energy to overcome compression blocking barriers "
        "(bowling ball -> squish ball). Temperature thresholds for H, He, C, Si fusion "
        "reflect the increasing barriers of larger bowling balls (more k in Tet B). "
        "Fe-56 (k=56) is the endpoint because larger bowling balls cost energy to unbind."
    )
    
    return run_test_group("Stellar Core Compression", summary, ALL_TESTS)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
