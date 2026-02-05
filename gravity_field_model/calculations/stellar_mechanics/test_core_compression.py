"""
Stellar Core Compression Tests: Standard Astrophysics
======================================================

GFD Model V2

HONESTY STATEMENT:
This module examines STANDARD ASTROPHYSICS data about stellar cores and
fusion conditions. The physics is well established. GFD provides a
conceptual framework (bowling ball / squish ball metaphors) but does
NOT derive these values.

STANDARD PHYSICS VERIFIED:
- Solar core conditions (T, P, density) from Standard Solar Model
- Fusion thresholds from nuclear physics
- Chandrasekhar limit from quantum mechanics
- Temperature scaling with fusion products

GFD METAPHORS USED (not derivations):
- "Bowling ball" = bound atom (stable configuration)
- "Squish ball" = unbound state (during fusion reaction)
- "Compression blocking" = Coulomb barrier (standard physics)
- The k=4, k=12, etc. labeling does not EXPLAIN fusion, it annotates it

The tests in this module verify standard astrophysics data is correctly
referenced, with GFD terminology as interpretive commentary.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    G, C, HBAR, ELECTRON_MASS,
    R_E, M_E, A_0,
    RHO_WHITE_DWARF, RHO_FIELD_BINDING, RHO_NUCLEAR,
    K_CLOSURE, M_SOLAR,
    T_HYDROGEN_FUSION, T_HELIUM_FUSION, T_CARBON_FUSION, T_SILICON_FUSION,
    CHANDRASEKHAR_LIMIT,
)


# =============================================================================
# SOLAR PARAMETERS (Standard Solar Model)
# =============================================================================

R_SOLAR = 6.96e8            # Solar radius (m)
RHO_SOLAR_CORE = 1.5e5      # Solar core density (kg/m^3)
RHO_SOLAR_SURFACE = 2e-4    # Solar surface density (kg/m^3)
T_SOLAR_CORE = 1.57e7       # Solar core temperature (K)
T_SOLAR_SURFACE = 5778      # Solar surface temperature (K)
P_SOLAR_CORE = 2.5e16       # Solar core pressure (Pa)
K_B = 1.380649e-23          # Boltzmann constant (J/K)
M_PROTON = 1.67262192e-27   # kg


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def field_spacing_from_density(density):
    """Estimate average particle spacing from mass density."""
    number_density = density / M_E
    return number_density ** (-1/3)


def binding_fraction(temperature, threshold):
    """Model fusion rate vs temperature (Gamow peak approximation)."""
    if temperature < threshold * 0.5:
        return 0.0
    elif temperature > threshold * 2.0:
        return 1.0
    else:
        x = (temperature - threshold) / (threshold * 0.3)
        return 1 / (1 + math.exp(-x))


# =============================================================================
# TEST 1: CORE PRESSURE GRADIENT (Standard Solar Model)
# =============================================================================

class CorePressureGradient(Test):
    """
    Verify solar core pressure from Standard Solar Model.

    HONESTY: This is measured/modeled data from helioseismology and
    standard solar models. GFD does not derive it.
    """
    name = "Core Pressure Gradient"
    question = (
        "What is the pressure ratio from solar core to surface?"
    )
    reference = "Standard Solar Model (Bahcall et al.)"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "The solar core pressure (~2.5e16 Pa) and surface pressure (~1e4 Pa) "
        "create a 12+ orders of magnitude gradient. This is standard stellar "
        "physics derived from hydrostatic equilibrium. The gradient provides "
        "the conditions for fusion by confining hot plasma."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Pressure from hydrostatic equilibrium.")
            .step("Core pressure P_core = 2.5e16 Pa (from solar models).")
            .step("Surface pressure P_surface ~ 1e4 Pa (photosphere).")
            .equation("Pressure ratio = P_core / P_surface = 2.5e12")
            .equation("Log10 ratio = 12.4")
            .step("This gradient maintains core conditions for fusion.")
            .conclude("Core pressure = 2.5e16 Pa, Log10 ratio = 12.4.")
        )

    def model(self) -> Model:
        P_surface = 1e4
        P_core = P_SOLAR_CORE
        log_ratio = math.log10(P_core / P_surface)
        return (
            Model()
            .add("Core pressure (Pa)", P_core)
            .add("Surface pressure (Pa)", P_surface)
            .add("Log10 pressure ratio", log_ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Core pressure (Pa)", 2.5e16)
            .add("Surface pressure (Pa)", 1e4)
            .add("Log10 pressure ratio", 12.4)
        )


# =============================================================================
# TEST 2: TEMPERATURE-DENSITY RELATIONSHIP (Standard Solar Model)
# =============================================================================

class TemperatureDensityRelationship(Test):
    """
    Verify temperature and density gradients in the Sun.

    HONESTY: Standard solar model data. GFD does not derive these values.
    """
    name = "Temperature-Density Relationship"
    question = (
        "What are the temperature and density ratios from surface to core?"
    )
    reference = "Standard Solar Model"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "Temperature increases ~2700x from surface (5778 K) to core (1.57e7 K). "
        "Density increases ~7.5e8x from surface to core. These conditions enable "
        "hydrogen fusion. The values come from solar models constrained by "
        "helioseismology and neutrino observations."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MEASUREMENT: From Standard Solar Model.")
            .equation("T_core = 1.57e7 K, T_surface = 5778 K")
            .equation("Temperature ratio = 1.57e7 / 5778 = 2718")
            .equation("Density ratio = 1.5e5 / 2e-4 = 7.5e8")
            .step("High T and density in core enable fusion reactions.")
            .conclude("T ratio = 2718, Density ratio = 7.5e8.")
        )

    def model(self) -> Model:
        T_ratio = T_SOLAR_CORE / T_SOLAR_SURFACE
        rho_ratio = RHO_SOLAR_CORE / RHO_SOLAR_SURFACE
        return (
            Model()
            .add("Temperature ratio (core/surface)", T_ratio)
            .add("Density ratio (core/surface)", rho_ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Temperature ratio (core/surface)", 2718)
            .add("Density ratio (core/surface)", 7.5e8)
        )


# =============================================================================
# TEST 3: HYDROGEN FUSION THRESHOLD (Nuclear Physics)
# =============================================================================

class HydrogenFusionThreshold(Test):
    """
    Verify hydrogen fusion temperature threshold.

    HONESTY: The threshold is from nuclear physics (Gamow peak calculation).
    The pp-chain releases 26.7 MeV. Standard physics, not a GFD prediction.
    """
    name = "Hydrogen Fusion Threshold"
    question = (
        "Does the solar core temperature exceed the hydrogen fusion threshold?"
    )
    reference = "Nuclear Physics (pp-chain)"
    tolerance = 0.10
    level = Level.CRITICAL
    commentary = (
        "Hydrogen fusion (pp-chain) requires T > 1.5e7 K. The solar core at "
        "1.57e7 K exceeds this threshold. At this temperature, quantum tunneling "
        "through the Coulomb barrier enables proton fusion. The threshold is "
        "determined by the Gamow peak, not GFD geometry."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: pp-chain fusion threshold.")
            .step("Thermal energy at T = 1.5e7 K: kT ~ 1.3 keV.")
            .step("Coulomb barrier for p+p: ~400 keV.")
            .step("Fusion occurs via quantum tunneling through the barrier.")
            .step("Gamow peak determines effective fusion temperature.")
            .equation("Threshold: T_H ~ 1.5e7 K")
            .equation("Solar core: T = 1.57e7 K > threshold")
            .conclude("H fusion threshold = 1.5e7 K, Solar core exceeds it.")
        )

    def model(self) -> Model:
        exceeds = 1.0 if T_SOLAR_CORE >= T_HYDROGEN_FUSION else 0.0
        return (
            Model()
            .add("H fusion threshold (K)", T_HYDROGEN_FUSION)
            .add("Solar core temp (K)", T_SOLAR_CORE)
            .add("Exceeds threshold", exceeds)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("H fusion threshold (K)", 1.5e7)
            .add("Solar core temp (K)", 1.57e7)
            .add("Exceeds threshold", 1.0)
        )


# =============================================================================
# TEST 4: HELIUM FLASH CONDITIONS (Nuclear Physics)
# =============================================================================

class HeliumFlashConditions(Test):
    """
    Verify triple-alpha temperature threshold.

    HONESTY: This is standard nuclear astrophysics. The triple-alpha
    process is well understood. Hoyle resonance is key.
    """
    name = "Helium Flash Conditions"
    question = (
        "What temperature is required for triple-alpha (He -> C) fusion?"
    )
    reference = "Nuclear Astrophysics (triple-alpha)"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "Triple-alpha fusion requires T ~ 1e8 K, about 6.7x hotter than "
        "hydrogen fusion. The higher temperature is needed because: "
        "(1) Higher Coulomb barrier for He-4 (Z=2) vs H (Z=1), "
        "(2) Three-body process requires higher collision rates. "
        "The Hoyle resonance in C-12 makes the process possible."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Triple-alpha threshold.")
            .step("He-4 has Z=2, so Coulomb barrier ~ Z1*Z2 ~ 4x higher than p+p.")
            .step("Three-body process requires higher density and T.")
            .equation("Triple-alpha threshold: T ~ 1e8 K")
            .equation("Ratio to H-fusion: 1e8 / 1.5e7 = 6.67")
            .step("Hoyle resonance (7.65 MeV in C-12) enhances the rate.")
            .conclude("Triple-alpha threshold = 1e8 K, ratio = 6.67.")
        )

    def model(self) -> Model:
        ratio = T_HELIUM_FUSION / T_HYDROGEN_FUSION
        return (
            Model()
            .add("Triple-alpha threshold (K)", T_HELIUM_FUSION)
            .add("Ratio to H-fusion", ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Triple-alpha threshold (K)", 1e8)
            .add("Ratio to H-fusion", 6.67)
        )


# =============================================================================
# TEST 5: CARBON BURNING THRESHOLD (Nuclear Physics)
# =============================================================================

class CarbonBurningThreshold(Test):
    """
    Verify carbon burning temperature threshold.

    HONESTY: Standard nuclear astrophysics. Higher Coulomb barrier
    for C-12 (Z=6) requires higher temperatures.
    """
    name = "Carbon Burning Threshold"
    question = (
        "What temperature is required for carbon burning?"
    )
    reference = "Nuclear Astrophysics (carbon burning)"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "Carbon burning requires T ~ 5e8 K. The higher threshold reflects "
        "the larger Coulomb barrier: Z=6 for carbon vs Z=2 for helium. "
        "Carbon burning produces neon, sodium, and magnesium."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Carbon burning threshold.")
            .step("C-12 has Z=6, so Coulomb barrier ~ Z^2 ~ 36x higher than He-4.")
            .equation("Carbon burning: T ~ 5e8 K")
            .equation("Ratio to He-fusion: 5e8 / 1e8 = 5.0")
            .step("Products: Ne-20, Na-23, Mg-24.")
            .conclude("Carbon burning = 5e8 K, ratio to He = 5.0.")
        )

    def model(self) -> Model:
        ratio_to_He = T_CARBON_FUSION / T_HELIUM_FUSION
        return (
            Model()
            .add("Carbon burning temp (K)", T_CARBON_FUSION)
            .add("Ratio to He-fusion", ratio_to_He)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Carbon burning temp (K)", 5e8)
            .add("Ratio to He-fusion", 5.0)
        )


# =============================================================================
# TEST 6: SILICON BURNING THRESHOLD (Nuclear Physics)
# =============================================================================

class SiliconBurningThreshold(Test):
    """
    Verify silicon burning temperature threshold.

    HONESTY: Standard nuclear astrophysics. Silicon burning is the
    final exothermic stage before iron.
    """
    name = "Silicon Burning Threshold"
    question = (
        "What temperature is required for silicon burning, and why is Fe-56 "
        "the endpoint of exothermic fusion?"
    )
    reference = "Nuclear Astrophysics (silicon burning)"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "Silicon burning at T ~ 2.7e9 K is the final exothermic fusion stage. "
        "It produces iron group elements (Fe, Ni, Co). Beyond Fe-56, fusion "
        "is ENDOTHERMIC because Fe-56 has maximum binding energy per nucleon. "
        "This is standard nuclear physics from the semi-empirical mass formula."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Silicon burning produces iron group.")
            .equation("Silicon burning: T ~ 2.7e9 K")
            .equation("Ratio to H-fusion: 2.7e9 / 1.5e7 = 180")
            .step("Fe-56 is the binding energy peak (8.79 MeV/nucleon).")
            .step("Beyond iron: fusion absorbs energy (endothermic).")
            .step("This is why massive stars develop iron cores before collapse.")
            .conclude("Si burning = 2.7e9 K, Fe-56 is fusion endpoint.")
        )

    def model(self) -> Model:
        ratio_to_H = T_SILICON_FUSION / T_HYDROGEN_FUSION
        return (
            Model()
            .add("Silicon burning temp (K)", T_SILICON_FUSION)
            .add("Ratio to H-fusion", ratio_to_H)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Silicon burning temp (K)", 2.7e9)
            .add("Ratio to H-fusion", 180)
        )


# =============================================================================
# TEST 7: CHANDRASEKHAR MASS LIMIT (Quantum Mechanics / Astrophysics)
# =============================================================================

class ChandrasekharMassLimit(Test):
    """
    Verify Chandrasekhar limit for white dwarfs.

    HONESTY: This is standard astrophysics derived from electron
    degeneracy pressure vs gravity. Chandrasekhar 1931.
    """
    name = "Chandrasekhar Mass Limit"
    question = (
        "What is the maximum mass for a white dwarf supported by electron "
        "degeneracy pressure?"
    )
    reference = "Chandrasekhar (1931)"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "The Chandrasekhar limit (~1.4 solar masses) is the maximum mass "
        "a white dwarf can support via electron degeneracy pressure. Above "
        "this limit, gravity overcomes degeneracy and collapse ensues. "
        "This is derived from relativistic quantum mechanics, not GFD."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Chandrasekhar limit derivation.")
            .step("Electron degeneracy pressure supports white dwarfs.")
            .step("As mass increases, electrons become relativistic.")
            .step("Relativistic degeneracy pressure scales as rho^(4/3).")
            .step("Gravity scales as rho, so there is a maximum stable mass.")
            .equation("M_Ch = 5.83 * mu_e^(-2) * M_solar ~ 1.4 M_solar")
            .step("Above this, collapse to neutron star or black hole.")
            .conclude("Chandrasekhar limit = 1.4 solar masses.")
        )

    def model(self) -> Model:
        M_ch = CHANDRASEKHAR_LIMIT * M_SOLAR
        num_nucleons = M_ch / M_PROTON
        log_nucleons = math.log10(num_nucleons)
        return (
            Model()
            .add("Chandrasekhar limit (solar masses)", CHANDRASEKHAR_LIMIT)
            .add("Log10 nucleon count", log_nucleons)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Chandrasekhar limit (solar masses)", 1.4)
            .add("Log10 nucleon count", 57.22)
        )


# =============================================================================
# TEST 8: FUSION RATE VS TEMPERATURE (Nuclear Physics)
# =============================================================================

class FusionRateVsTemperature(Test):
    """
    Verify fusion rate increases with temperature.

    HONESTY: Standard nuclear physics. The Gamow peak shifts with T.
    """
    name = "Fusion Rate vs Temperature"
    question = (
        "Does fusion rate increase monotonically with temperature?"
    )
    reference = "Nuclear Physics (reaction rates)"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "Fusion rate increases with temperature because: (1) More particles "
        "have enough energy to tunnel through the Coulomb barrier, and "
        "(2) Higher collision rates. The Gamow peak (optimal energy for "
        "tunneling) shifts to higher energies at higher T."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Fusion rate temperature dependence.")
            .step("Rate ~ n^2 * <sigma*v>, where <sigma*v> increases with T.")
            .step("Gamow peak: E_G ~ (E_r * (kT)^2)^(1/3)")
            .step("More particles exceed E_G at higher T.")
            .step("For pp-chain: rate ~ T^4 near solar conditions.")
            .step("Verify monotonic increase with temperature.")
            .conclude("Fusion rate increases monotonically with T.")
        )

    def model(self) -> Model:
        T_low = 1.0e7
        T_threshold = T_HYDROGEN_FUSION
        T_high = 2.0e7
        f_low = binding_fraction(T_low, T_threshold)
        f_threshold = binding_fraction(T_threshold, T_threshold)
        f_high = binding_fraction(T_high, T_threshold)
        monotonic = 1.0 if f_low < f_threshold < f_high else 0.0
        return (
            Model()
            .add("Rate at 1e7 K (relative)", f_low)
            .add("Rate at 1.5e7 K (relative)", f_threshold)
            .add("Rate at 2e7 K (relative)", f_high)
            .add("Monotonic increase", monotonic)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Rate at 1e7 K (relative)", 0.0)
            .add("Rate at 1.5e7 K (relative)", 0.5)
            .add("Rate at 2e7 K (relative)", 1.0)
            .add("Monotonic increase", 1.0)
        )


# =============================================================================
# TEST 9: SOLAR CORE NUMBER DENSITY (Standard Solar Model)
# =============================================================================

class SolarCoreNumberDensity(Test):
    """
    Verify particle number density in solar core.

    HONESTY: Standard calculation from core density.
    """
    name = "Solar Core Number Density"
    question = (
        "What is the nucleon number density in the solar core?"
    )
    reference = "Standard Solar Model"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "At solar core density (1.5e5 kg/m^3), there are ~10^32 nucleons per "
        "cubic meter. This high density, combined with core temperature, "
        "enables fusion via quantum tunneling through Coulomb barriers."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Number density from mass density.")
            .equation("n = rho / m_proton = 1.5e5 / 1.67e-27")
            .equation("n = 8.97e31 per m^3")
            .equation("Log10(n) = 31.95")
            .step("Average spacing: d ~ n^(-1/3) ~ 2.2e-11 m")
            .step("This is ~0.4 Bohr radii, indicating compressed atoms.")
            .conclude("Core number density = 8.97e31 per m^3.")
        )

    def model(self) -> Model:
        rho_core = RHO_SOLAR_CORE
        n_nucleons = rho_core / M_PROTON
        log_n = math.log10(n_nucleons)
        spacing = n_nucleons ** (-1/3)
        return (
            Model()
            .add("Number density (per m^3)", n_nucleons)
            .add("Log10 density", log_n)
            .add("Average spacing (m)", spacing)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Number density (per m^3)", 8.97e31)
            .add("Log10 density", 31.95)
            .add("Average spacing (m)", 2.2e-11)
        )


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
    ChandrasekharMassLimit,
    FusionRateVsTemperature,
    SolarCoreNumberDensity,
]


def run_all() -> bool:
    """Run all stellar core compression tests."""
    return run_tests(
        title="Stellar Core Compression",
        summary=(
            "These tests verify STANDARD ASTROPHYSICS data about stellar cores:\n"
            "1. Solar core conditions (T, P, density) from Standard Solar Model\n"
            "2. Fusion thresholds from nuclear physics (Gamow peak)\n"
            "3. Temperature progression H -> He -> C -> Si burning\n"
            "4. Chandrasekhar limit from electron degeneracy\n"
            "5. Fe-56 as fusion endpoint (maximum BE/nucleon)\n\n"
            "CLARIFICATION: The 'bowling ball' metaphor in original GFD commentary\n"
            "describes standard physics in different language. Coulomb barrier =\n"
            "'compression blocking', quantum tunneling = how fusion overcomes it.\n"
            "GFD does NOT derive these temperatures or the physics behind them."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
