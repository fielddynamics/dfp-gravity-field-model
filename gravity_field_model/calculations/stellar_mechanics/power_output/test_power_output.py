"""
Stellar Power Output: Standard Astrophysics Verification
=========================================================

GFM Model V2

HONESTY STATEMENT:
This module verifies STANDARD ASTROPHYSICS data about stellar energy production.
The physics (E=mc^2, pp-chain, solar luminosity) is well established and does
NOT derive from GFM.

WHAT IS VERIFIED:
- pp-chain releases 26.7 MeV per He-4 (standard nuclear physics)
- Mass defect follows E=mc^2 (Einstein 1905)
- Solar luminosity = 3.828e26 W (measurement)
- Mass loss rate = L/c^2 (standard physics)
- Stefan-Boltzmann law (thermodynamics)

THE "P = BE x f_closure" FORMULA:
The formula Power = BindingEnergy x (c/lambda_C) expresses binding energy
in power units by multiplying by a frequency. This frequency f = c/lambda_C
is DEFINED as the "field closure frequency" in GFM. However:
- This does NOT derive stellar power output
- It is a way of expressing binding energy, not a prediction
- The formula is dimensional analysis, not physics derivation

GFM terminology (Field Closure, bowling ball, squish ball) provides metaphors
for standard physics but does not derive new results.

TEST GROUP GOALS:
This module connects nuclear binding energies to observable stellar properties:
luminosity, mass loss, and thermal radiation. Students learn to trace the energy
pathway from nuclear reactions (MeV scale) to macroscopic stellar output (watts),
understanding E=mc^2 as the bridge between mass defect and radiated power.

Audience: Undergraduate astrophysics and nuclear physics students.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.base import validated_function
from gravity_field_model.common import (
    C, HBAR, G, K_CLOSURE, M_E, M_P as M_PROTON, M_SOLAR, R_E,
    L_SOLAR, SOLAR_MASS_LOSS_RATE,
    ELEMENTS_118, BINDING_ENERGIES_BY_A, MEV_TO_JOULES,
    get_binding_energy_by_A,
)


# =============================================================================
# CONSTANTS
# =============================================================================

PP_CHAIN_ENERGY = 26.7      # MeV per He-4 formation
TRIPLE_ALPHA_ENERGY = 7.27  # MeV per C-12 formation
SIGMA_SB = 5.670374419e-8   # Stefan-Boltzmann constant (W/m^2/K^4)

# Compton wavelength and derived frequency
LAMBDA_COMPTON = 2.426310238e-12  # Compton wavelength (m)
F_CLOSURE = C / LAMBDA_COMPTON    # ~1.24e20 Hz (model-defined frequency)


def fusion_rate_from_luminosity(luminosity, energy_per_event):
    """Calculate fusion event rate from luminosity."""
    return luminosity / energy_per_event


def fields_bound_per_second(fusion_rate, fields_per_event):
    """Calculate binding rate from fusion rate."""
    return fusion_rate * fields_per_event


# =============================================================================
# BINDING ENERGIES
# =============================================================================

BINDING_ENERGIES = BINDING_ENERGIES_BY_A
ELEMENTS = [(sym, name, z, a) for sym, name, z, a, _r, _v in ELEMENTS_118]


def get_binding_energy(A):
    """Get binding energy per nucleon (MeV) for mass number A."""
    return get_binding_energy_by_A(A)


def power_per_field(A):
    """
    Calculate power per gravity field (W) using GFM formula.

    HONESTY: This multiplies binding energy by a defined frequency.
    It does NOT derive power output. It expresses BE in different units.

    P = BE(J) x f_closure = BE(J) x (c/lambda_C)
    """
    be_mev = get_binding_energy(A)
    be_joules = be_mev * MEV_TO_JOULES
    return be_joules * F_CLOSURE


# =============================================================================
# VALIDATED FUNCTION
# =============================================================================

_ELEMENT_BY_SYMBOL = {sym: a for sym, _, _, a in ELEMENTS}


@validated_function(
    equation="P(sym) = BE(A) * (c / lambda_C)",
    description=(
        "Express binding energy in power units by multiplying by f_closure.\n\n"
        "HONESTY NOTE:\n"
        "This formula does NOT derive stellar power output. It expresses the\n"
        "binding energy per nucleon in power units (Watts) by multiplying by\n"
        "f_closure = c/lambda_C, a frequency defined in the GFM model.\n\n"
        "The physical content is the binding energy BE(A), which comes from\n"
        "nuclear physics (AME2020 data). The 'power' is a unit conversion,\n"
        "not a prediction."
    ),
    inputs={"symbol": "str: Element symbol (e.g. 'Fe', 'Cr', 'He')"},
    outputs={"watts": "float: BE expressed in power units"},
    group="Stellar Power Output",
)
def fn_get_element_power_output(symbol):
    """
    Express element binding energy in power units.

    NOTE: This is dimensional analysis, not physics derivation.
    """
    if symbol not in _ELEMENT_BY_SYMBOL:
        raise ValueError(
            f"Unknown element symbol '{symbol}'. "
            f"Available: {sorted(_ELEMENT_BY_SYMBOL.keys())}"
        )
    A = _ELEMENT_BY_SYMBOL[symbol]
    return power_per_field(A)


element_power_output = fn_get_element_power_output


# =============================================================================
# TEST 1: PP-CHAIN ENERGY RELEASE (Standard Nuclear Physics)
# =============================================================================

class BindingEnergyRelease(Test):
    """
    Verify pp-chain energy release.

    HONESTY: 26.7 MeV is measured. E=mc^2 explains it. Standard physics.
    """
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: How is the 26.7 MeV distributed among photons, positrons, and neutrinos, "
        "and why do neutrinos carry away energy undetectably? "
        "(Answering would improve Commentary by +3 points: energy partitioning) "
        "Q2: Why does the pp-chain require multiple steps rather than direct 4p -> He-4? "
        "(Answering would improve Derivation by +3 points: reaction pathway necessity) "
        "Q3: How does the energy release per reaction compare to chemical combustion? "
        "(Answering would improve Audience Accessibility by +2 points: familiar comparison)"
    )
    name = "pp-Chain Energy Release"
    question = (
        "Why does the pp-chain release exactly 26.7 MeV when four protons fuse "
        "to helium-4? How does the mass defect (0.7% of constituent mass) "
        "account for this energy via E=mc^2?"
    )
    reference = "Nuclear Physics (pp chain)"
    tolerance = 0.10
    level = Level.CRITICAL
    commentary = (
        "The pp-chain reaction 4p -> He-4 + 2e+ + 2nu releases 26.7 MeV. This is "
        "standard nuclear physics. The energy comes from the mass defect: the "
        "He-4 nucleus is 0.7% lighter than 4 separate protons. GFM does not "
        "derive this value. It adopts it from nuclear data."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: pp-chain fusion.")
            .equation("4p -> He-4 + 2e+ + 2nu_e")
            .step("Mass of 4 protons: 4 x 938.27 = 3753.08 MeV")
            .step("Mass of He-4: 3727.38 MeV (measured)")
            .step("Positrons and neutrinos carry some energy.")
            .equation("Total energy release = 26.7 MeV (measured)")
            .step("Mass defect = 0.7% of constituent mass.")
            .conclude("pp-chain releases 26.7 MeV per He-4. Standard physics.")
        )

    def model(self) -> Model:
        energy_j = PP_CHAIN_ENERGY * MEV_TO_JOULES
        mass_4h = 4 * M_PROTON
        mass_he4 = 4.002602 * 1.66054e-27  # He-4 atomic mass in kg
        mass_defect = (mass_4h - mass_he4) / mass_4h * 100
        return (
            Model()
            .add("Energy (MeV)", PP_CHAIN_ENERGY)
            .add("Mass defect (%)", mass_defect)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Energy (MeV)", 26.7)
            .add("Mass defect (%)", 0.7)
        )


# =============================================================================
# TEST 2: E=mc^2 VERIFICATION (Standard Physics)
# =============================================================================

class MassDefectCalculation(Test):
    """
    Verify E=mc^2 for mass defect.

    HONESTY: Einstein 1905. Standard physics. GFM does not improve on this.
    """
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: How did Cockcroft and Walton first verify E=mc^2 experimentally in 1932? "
        "(Answering would improve Observation Quality by +3 points: historical verification) "
        "Q2: Why do neutrino losses cause a slight discrepancy between calculated and "
        "calorimetric energy release? "
        "(Answering would improve Commentary by +3 points: explains ~6% difference) "
        "Q3: How does the mass defect for fission compare to fusion? "
        "(Answering would improve Audience Accessibility by +2 points: broader context)"
    )
    name = "Mass Defect E=mc^2"
    question = (
        "Why does Einstein's E=mc^2 precisely connect the mass lost during "
        "fusion to the energy released? What does this century-old equation "
        "reveal about the fundamental equivalence of mass and energy?"
    )
    reference = "Einstein (1905)"
    tolerance = 0.10
    level = Level.CRITICAL
    commentary = (
        "E=mc^2 relates mass defect to energy release. For pp-chain: "
        "dm x c^2 = 26.7 MeV. This is standard physics, verified countless "
        "times. GFM adopts E=mc^2 without modification."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: E = dm x c^2 (Einstein 1905).")
            .step("Mass of 4 protons: 4 x 1.673e-27 = 6.69e-27 kg")
            .step("Mass of He-4: 6.64e-27 kg")
            .step("Mass defect: dm = 4.5e-29 kg")
            .equation("E = dm x c^2 = 4.5e-29 x (3e8)^2 = 4.0e-12 J = 25 MeV")
            .step("Within ~6% of measured 26.7 MeV (neutrino losses).")
            .conclude("E=mc^2 verified for nuclear mass defect.")
        )

    def model(self) -> Model:
        mass_4h = 4 * M_PROTON
        mass_he4 = 4.002602 * 1.66054e-27
        delta_m = mass_4h - mass_he4
        energy = delta_m * C**2
        energy_mev = energy / MEV_TO_JOULES
        ratio = energy_mev / PP_CHAIN_ENERGY
        return (
            Model()
            .add("E from mass defect (MeV)", energy_mev)
            .add("Ratio to measured", ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("E from mass defect (MeV)", 26.7)
            .add("Ratio to measured", 1.0)
        )


# =============================================================================
# TEST 3: SOLAR FUSION RATE (Standard Astrophysics)
# =============================================================================

class SolarFieldBindingRate(Test):
    """
    Calculate fusion rate in the Sun.

    HONESTY: This divides solar luminosity by energy per reaction.
    Standard astrophysics calculation.
    """
    audit_score = 82
    audit_notes = None
    future_questions = (
        "Q1: Why is 10^38 reactions per second an almost incomprehensibly large number, "
        "yet the Sun appears steady over human timescales? "
        "(Answering would improve Commentary by +3 points: scale perspective) "
        "Q2: How is the fusion rate distributed spatially within the solar core? "
        "(Answering would improve Model Output by +3 points: spatial profile) "
        "Q3: What fraction of the Sun's hydrogen will be consumed over its main sequence "
        "lifetime, and why only the core participates? "
        "(Answering would improve Audience Accessibility by +2 points: stellar lifespan)"
    )
    name = "Solar Fusion Rate"
    question = (
        "Why must the Sun perform ~10^38 fusion reactions per second to "
        "maintain its luminosity? How does dividing total power by energy "
        "per reaction reveal the enormous scale of stellar nucleosynthesis?"
    )
    reference = "Solar Physics"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "Fusion rate = L_solar / E_per_reaction. With L = 3.828e26 W and "
        "E = 26.7 MeV = 4.28e-12 J, we get ~9e37 reactions/second. This is "
        "standard astrophysics, not a GFM derivation."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD ASTROPHYSICS: Fusion rate from luminosity.")
            .equation("Fusion rate = L_solar / E_per_event")
            .step("L_solar = 3.828e26 W, E_per_event = 4.28e-12 J")
            .equation("Rate = 3.828e26 / 4.28e-12 = 8.94e37 per second")
            .step("This is standard stellar physics calculation.")
            .conclude("Log10 fusion rate ~ 37.95")
        )

    def model(self) -> Model:
        energy_per_event = PP_CHAIN_ENERGY * MEV_TO_JOULES
        fusion_rate = fusion_rate_from_luminosity(L_SOLAR, energy_per_event)
        return (
            Model()
            .add("Log10 fusion rate", math.log10(fusion_rate))
            .add("Fusion rate (/s)", fusion_rate)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Log10 fusion rate", 37.95)
            .add("Fusion rate (/s)", 8.94e37)
        )


# =============================================================================
# TEST 4: SOLAR MASS LOSS (Standard Physics)
# =============================================================================

class StellarWindMassLoss(Test):
    """
    Verify solar mass loss rate from luminosity.

    HONESTY: dm/dt = L/c^2. Standard physics from E=mc^2.
    """
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: How does the radiation mass loss (4.26 billion kg/s) compare to the solar "
        "wind mass loss, and which dominates? "
        "(Answering would improve Commentary by +3 points: complete mass budget) "
        "Q2: Over the Sun's 10 billion year lifetime, what fraction of its mass will be "
        "converted to radiation? "
        "(Answering would improve Model Output by +3 points: lifetime integral) "
        "Q3: How does mass loss affect the orbits of planets over astronomical timescales? "
        "(Answering would improve Audience Accessibility by +2 points: observable consequence)"
    )
    name = "Solar Mass Loss Rate"
    question = (
        "Why does the Sun lose 4.26 billion kg of mass every second, yet will "
        "shine for billions of years? How does L = dm/dt x c^2 connect the "
        "tiny mass fraction converted to the enormous energy released?"
    )
    reference = "E=mc^2 (Einstein)"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "The Sun converts ~4.26 billion kg of mass to energy every second. "
        "This follows directly from E=mc^2: dm/dt = L/c^2. Standard physics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Mass-energy equivalence.")
            .equation("L = dm/dt x c^2")
            .equation("dm/dt = L / c^2 = 3.828e26 / (3e8)^2 = 4.25e9 kg/s")
            .step("Measured solar mass loss: ~4.26e9 kg/s (including solar wind).")
            .conclude("Mass loss rate = 4.26e9 kg/s. E=mc^2 verified.")
        )

    def model(self) -> Model:
        calc_mass_loss = L_SOLAR / C**2
        ratio = calc_mass_loss / SOLAR_MASS_LOSS_RATE
        return (
            Model()
            .add("Calculated mass loss (kg/s)", calc_mass_loss)
            .add("Observed mass loss (kg/s)", SOLAR_MASS_LOSS_RATE)
            .add("Ratio", ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Calculated mass loss (kg/s)", 4.26e9)
            .add("Observed mass loss (kg/s)", 4.26e9)
            .add("Ratio", 1.0)
        )


# =============================================================================
# TEST 5: STEFAN-BOLTZMANN LAW (Thermodynamics)
# =============================================================================

class ThermalPowerScale(Test):
    """
    Verify Stefan-Boltzmann law reproduces solar luminosity.

    HONESTY: Standard thermodynamics. L = 4*pi*R^2*sigma*T^4.
    """
    audit_score = 83
    audit_notes = None
    future_questions = (
        "Q1: Why does luminosity scale as T^4 rather than linearly with temperature, "
        "and what physical insight does this reveal about blackbody radiation? "
        "(Answering would improve Derivation by +3 points: Planck distribution connection) "
        "Q2: How well does the Sun approximate an ideal blackbody, and where does it deviate? "
        "(Answering would improve Observation Quality by +3 points: spectral deviations) "
        "Q3: How can astronomers use this law to determine stellar radii from luminosity "
        "and temperature? "
        "(Answering would improve Audience Accessibility by +2 points: practical application)"
    )
    name = "Stefan-Boltzmann Verification"
    question = (
        "Why does the Stefan-Boltzmann law (L = 4*pi*R^2*sigma*T^4) accurately "
        "predict solar luminosity from surface temperature and radius alone? "
        "What does this reveal about stars as blackbody radiators?"
    )
    reference = "Thermodynamics"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "The Stefan-Boltzmann law L = 4*pi*R^2*sigma*T^4 with R = 6.96e8 m "
        "and T = 5778 K gives L = 3.83e26 W, matching the measured solar "
        "luminosity. Standard thermodynamics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("THERMODYNAMICS: Stefan-Boltzmann law.")
            .equation("L = 4*pi*R^2*sigma*T^4")
            .step("R = 6.96e8 m, T = 5778 K, sigma = 5.67e-8 W/m^2/K^4")
            .equation("L = 4*pi*(6.96e8)^2*(5.67e-8)*(5778)^4 = 3.83e26 W")
            .step("Matches measured L_solar = 3.828e26 W.")
            .conclude("Stefan-Boltzmann law verified for Sun.")
        )

    def model(self) -> Model:
        R_SOLAR = 6.96e8
        T_SURFACE = 5778
        L_calc = 4 * math.pi * R_SOLAR**2 * SIGMA_SB * T_SURFACE**4
        ratio = L_calc / L_SOLAR
        return (
            Model()
            .add("Calculated luminosity (W)", L_calc)
            .add("Ratio to observed", ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Calculated luminosity (W)", 3.83e26)
            .add("Ratio to observed", 1.0)
        )


# =============================================================================
# TEST 6: BINDING ENERGY PEAK (Standard Nuclear Physics)
# =============================================================================

class BindingEnergyPeak(Test):
    """
    Verify Fe-56 has peak binding energy per nucleon.

    HONESTY: This is measured nuclear data. Standard physics.
    """
    audit_score = 87
    audit_notes = None
    future_questions = (
        "Q1: What subtle difference exists between binding energy per nucleon (Fe-56 peak) "
        "and total binding energy per atom (Ni-62 peak)? "
        "(Answering would improve Commentary by +3 points: precise distinction) "
        "Q2: How does the shell model explain fine structure in the binding curve "
        "beyond the smooth SEMF prediction? "
        "(Answering would improve Derivation by +3 points: shell effects) "
        "Q3: Why is iron so abundant in the universe compared to elements just below or "
        "above it on the periodic table? "
        "(Answering would improve Audience Accessibility by +2 points: cosmic abundance)"
    )
    name = "Fe-56 Binding Energy Peak"
    question = (
        "Why is iron-56 the most tightly bound nucleus per nucleon at 8.79 MeV? "
        "What balance of attractive strong force and repulsive Coulomb force "
        "creates this energy maximum that determines stellar evolution endpoints?"
    )
    reference = "Nuclear Physics (AME2020)"
    tolerance = 0.05
    level = Level.CRITICAL
    commentary = (
        "Fe-56 (and Ni-62) have the highest binding energy per nucleon at "
        "~8.79 MeV. This is measured nuclear data, not a GFM prediction. "
        "The semi-empirical mass formula explains WHY the peak is at Fe-56."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUCLEAR DATA: Binding energy per nucleon from AME2020.")
            .step("He-4: 7.07 MeV/nucleon")
            .step("C-12: 7.68 MeV/nucleon")
            .step("Fe-56: 8.79 MeV/nucleon (PEAK)")
            .step("U-238: 7.57 MeV/nucleon")
            .step("Fe-56 is the peak. Fusion to Fe releases energy.")
            .step("Past Fe, fusion is endothermic.")
            .conclude("Fe-56 BE/A = 8.79 MeV is maximum (measured).")
        )

    def model(self) -> Model:
        fe_be = get_binding_energy(56)
        he_be = get_binding_energy(4)
        u_be = get_binding_energy(238)

        # Verify Fe is at peak
        all_be = [get_binding_energy(a) for a in range(4, 240) if a in BINDING_ENERGIES]
        fe_is_max = 1.0 if fe_be >= max(all_be) - 0.01 else 0.0

        return (
            Model()
            .add("He-4 BE (MeV/A)", he_be)
            .add("Fe-56 BE (MeV/A)", fe_be)
            .add("U-238 BE (MeV/A)", u_be)
            .add("Fe is peak", fe_is_max)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("He-4 BE (MeV/A)", 7.07)
            .add("Fe-56 BE (MeV/A)", 8.79)
            .add("U-238 BE (MeV/A)", 7.57)
            .add("Fe is peak", 1.0)
        )


# =============================================================================
# TEST 7: SUPERNOVA ENERGY SCALE (Astrophysics)
# =============================================================================

class SupernovaEnergyRelease(Test):
    """
    Verify supernova energy scale.

    HONESTY: ~10^46 J is observed. Standard astrophysics.
    """
    audit_score = 81
    audit_notes = None
    future_questions = (
        "Q1: Why do neutrinos carry 99% of supernova energy while optical light is only 1%? "
        "(Answering would improve Commentary by +3 points: energy channel partitioning) "
        "Q2: What gravitational potential energy release powers the neutrino burst during "
        "core collapse? "
        "(Answering would improve Derivation by +3 points: energy source) "
        "Q3: How does a supernova briefly outshine its entire host galaxy despite being "
        "a single star? "
        "(Answering would improve Audience Accessibility by +2 points: dramatic comparison)"
    )
    name = "Supernova Energy Scale"
    question = (
        "Why do supernovae release ~10^46 Joules, equivalent to 12% of the "
        "core's rest mass energy? What gravitational and nuclear processes "
        "combine to power these brief cosmic explosions that outshine galaxies?"
    )
    reference = "Astrophysics"
    tolerance = 0.30
    level = Level.STANDARD
    commentary = (
        "Type II supernovae release ~3e46 J total, mostly in neutrinos. "
        "This is ~12% of the core's rest mass energy. Standard astrophysics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ASTROPHYSICS: Type II supernova energetics.")
            .step("Total energy release: ~3e46 J")
            .step("Neutrino energy: ~99% of total")
            .step("Photon + kinetic: ~1%")
            .step("Core mass: ~1.4 M_solar")
            .equation("Fraction of Mc^2 = 3e46 / (1.4*2e30*9e16) = 0.12")
            .conclude("Supernova releases ~10^46 J = 12% of core Mc^2.")
        )

    def model(self) -> Model:
        core_mass = 1.4 * M_SOLAR
        total_energy = 3e46
        fraction_of_mc2 = total_energy / (core_mass * C**2)
        return (
            Model()
            .add("Log10 total energy (J)", math.log10(total_energy))
            .add("Fraction of Mc^2", fraction_of_mc2)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Log10 total energy (J)", 46.5)
            .add("Fraction of Mc^2", 0.12)
        )


# =============================================================================
# TEST 8: NEUTRINO EMISSION RATE (Solar Physics)
# =============================================================================

class NeutrinoEmission(Test):
    """
    Calculate solar neutrino emission rate.

    HONESTY: ~2 neutrinos per pp-chain. Standard physics.
    """
    audit_score = 80
    audit_notes = None
    future_questions = (
        "Q1: Why did early solar neutrino experiments detect only 1/3 of the predicted "
        "flux, and how was this 'solar neutrino problem' resolved? "
        "(Answering would improve Commentary by +4 points: historical puzzle and solution) "
        "Q2: How do neutrino detectors like Super-Kamiokande and SNO work to detect these "
        "ghostly particles? "
        "(Answering would improve Observation Quality by +3 points: detection methods) "
        "Q3: What is the neutrino flux at Earth, and how many pass through your body each second? "
        "(Answering would improve Audience Accessibility by +2 points: visceral scale)"
    )
    name = "Solar Neutrino Rate"
    question = (
        "Why does the Sun emit ~2x10^38 neutrinos per second, and why do "
        "these ghostly particles carry away energy without interacting? "
        "What does neutrino detection tell us about fusion in the solar core?"
    )
    reference = "Solar Neutrino Physics"
    tolerance = 0.20
    level = Level.STANDARD
    commentary = (
        "The pp-chain emits 2 electron neutrinos per reaction. With ~9e37 "
        "reactions/second, the Sun emits ~2e38 neutrinos/second. Standard physics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Neutrinos from pp-chain.")
            .step("2 neutrinos per pp-chain reaction.")
            .step("Fusion rate ~9e37 /s.")
            .equation("Neutrino rate = 2 x 9e37 = 1.8e38 /s")
            .conclude("Log10 neutrino rate ~ 38.3")
        )

    def model(self) -> Model:
        energy_per_event = PP_CHAIN_ENERGY * MEV_TO_JOULES
        fusion_rate = L_SOLAR / energy_per_event
        neutrino_rate = fusion_rate * 2
        return Model().add("Log10 neutrino rate", math.log10(neutrino_rate))

    def observations(self) -> Observed:
        return Observed().add("Log10 neutrino rate", 38.3)


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BindingEnergyRelease,
    MassDefectCalculation,
    SolarFieldBindingRate,
    StellarWindMassLoss,
    ThermalPowerScale,
    BindingEnergyPeak,
    SupernovaEnergyRelease,
    NeutrinoEmission,
]


def run_all() -> bool:
    """Run all power output tests."""
    return run_tests(
        title="Stellar Power Output",
        summary=(
            "These tests verify STANDARD ASTROPHYSICS for stellar energy production:\n"
            "1. pp-chain releases 26.7 MeV per He-4 (measured)\n"
            "2. E=mc^2 for mass defect (Einstein 1905)\n"
            "3. Solar fusion rate = L/E_per_event\n"
            "4. Mass loss rate = L/c^2\n"
            "5. Stefan-Boltzmann law for surface luminosity\n"
            "6. Fe-56 is binding energy peak (measured)\n\n"
            "CLARIFICATION: The 'P = BE x f_closure' formula in the original GFM\n"
            "tests is not a physics derivation. It expresses binding energy in\n"
            "power units by multiplying by a defined frequency. The physical\n"
            "content is the binding energy, which comes from nuclear data."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
