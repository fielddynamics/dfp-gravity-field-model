"""
Field Energy Scales
===================

This module documents energy scales relevant to the GFM framework.

CRITICAL NOTE:
These tests do NOT derive emergent constants. They calculate energy
scales using standard physics formulas (E = mc^2, E = hf, U = Gm^2/r).

WHY THIS FILE EXISTS:
Understanding the energy scales helps establish where GFM effects
should (and should not) be observable. But these are calculations,
not derivations of fundamental constants.

WHAT WAS REMOVED:
- Tests claiming energy calculations are "emergent"
- Speculative interpretations presented as derivations
- Numerology (e.g., 1836/4 = 459)

WHAT REMAINS:
- Verification of standard physics at GFM-relevant scales
- Energy scale comparisons to establish the hierarchy
- The cosmological constant problem (unsolved, honestly noted)
"""

import sys
import math

from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, H as H_PLANCK, HBAR, G, M_E, R_E, E_PLANCK,
    MU_0, EPSILON_0, K, calculate_settlement_frequency,
)

# =============================================================================
# CONSTANTS
# =============================================================================

# Closure frequency from common utilities (f = c / (k * r_e))
CLOSURE_FREQUENCY = calculate_settlement_frequency()


# =============================================================================
# TESTS
# =============================================================================

class ElectronRestEnergy(Test):
    """
    The electron rest energy E = m_e * c^2 = 511 keV.
    
    THIS IS STANDARD PHYSICS, NOT A DERIVATION.
    We document this as a reference scale for GFM.
    """
    name = "Electron Rest Energy (Reference Scale)"
    question = (
        "Why is 511 keV the fundamental energy scale in GFM? The electron rest energy "
        "E = m_e * c^2 sets the Field Envelope scale, anchoring field closure physics."
    )
    reference = "CODATA 2018"
    tolerance = 0.001
    level = Level.STANDARD
    audit_score = 78
    audit_notes = None
    future_questions = (
        "Q1: Why is the electron specifically the anchor scale for GFM rather than another particle? "
        "(Answering would improve Question by +3 points: explaining the choice of reference particle) "
        "Q2: How does 511 keV relate to the Field Envelope radius and settlement frequency? "
        "(Answering would improve Commentary by +3 points: connecting energy to GFM geometry) "
        "Q3: What role does rest energy play in determining the tile interaction strength? "
        "(Answering would improve Derivation by +2 points: linking E=mc^2 to field closure)"
    )
    
    commentary = (
        "This is Einstein's E = mc^2 applied to the electron.\n"
        "It's standard physics, not a GFM derivation.\n"
        "The electron rest energy (511 keV) serves as a reference scale."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: E = mc^2")
            .step("Electron mass m_e = 9.109e-31 kg.")
            .step("Speed of light c = 2.998e8 m/s.")
            .step("E = (9.109e-31) * (2.998e8)^2 = 8.187e-14 J.")
            .step("Convert to keV: E = 8.187e-14 / (1.602e-16) = 511 keV.")
            .conclude("Electron rest energy = 511 keV (standard result).")
        )
    
    def model(self) -> Model:
        E_field = M_E * C**2
        E_keV = E_field / (1.602e-19 * 1000)
        return Model().add("Electron rest energy (keV)", round(E_keV, 1))
    
    def observations(self) -> Observed:
        return Observed().add("Electron rest energy (keV)", 511)


class GravitationalSelfEnergy(Test):
    """
    The gravitational self-energy U = Gm^2/r is negligible at electron scale.
    
    THIS EXPLAINS WHY QUANTUM GRAVITY CAN BE IGNORED:
    The ratio U_grav/E_rest ~ 10^-43 shows gravity is ~43 orders of
    magnitude weaker than electromagnetic binding at electron scales.
    """
    name = "Gravitational Self-Energy is Negligible"
    question = (
        "Why can quantum gravity be ignored at particle scales? The ratio U_grav/E_rest ~ 10^-43 "
        "shows gravitational self-energy is 44 orders of magnitude below rest energy."
    )
    reference = "Standard gravitational physics"
    tolerance = 0.10
    level = Level.STANDARD
    audit_score = 82
    audit_notes = None
    future_questions = (
        "Q1: At what scale does gravitational self-energy become comparable to rest energy? "
        "(Answering would improve Derivation by +3 points: quantifying the Planck scale crossover) "
        "Q2: Does the 10^-43 ratio have any relation to the alpha^21 hierarchy in the G derivation? "
        "(Answering would improve Commentary by +3 points: connecting to other emergent constant tests) "
        "Q3: Why does GFM focus on classical field closure rather than quantized gravity effects? "
        "(Answering would improve Audience Accessibility by +2 points: clarifying framework scope)"
    )
    
    commentary = (
        "This is an important CONSISTENCY CHECK, not a derivation.\n\n"
        "Gravitational self-energy: U = Gm_e^2/r_e ~ 2e-56 J\n"
        "Electron rest energy: E = m_e*c^2 ~ 8e-14 J\n"
        "Ratio: ~2.4e-43\n\n"
        "This 44 orders of magnitude difference explains why:\n"
        "1. Quantum gravity effects are unobservable at particle scales\n"
        "2. GFM focuses on classical field closure, not quantized gravity\n"
        "3. The hierarchy problem (why gravity is weak) is real and important"
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GRAVITATIONAL SELF-ENERGY (standard calculation):")
            .step("U = G * m^2 / r for mass m at scale r.")
            .step("G = 6.674e-11 m^3/(kg*s^2)")
            .step("m = m_e = 9.109e-31 kg")
            .step("r = r_e = 2.818e-15 m")
            .step("U = (6.674e-11) * (9.109e-31)^2 / (2.818e-15)")
            .step("U = 1.965e-56 J")
            .step("E_rest = m_e * c^2 = 8.187e-14 J")
            .step("Ratio = U / E_rest = 1.965e-56 / 8.187e-14 = 2.40e-43")
            .conclude("Gravity is 10^44 times weaker than EM at electron scale.")
        )
    
    def model(self) -> Model:
        U_grav = G * M_E**2 / R_E
        E_rest = M_E * C**2
        ratio = U_grav / E_rest
        negligible = 1 if ratio < 1e-40 else 0
        return (
            Model()
            .add("U_grav (J)", U_grav)
            .add("E_rest (J)", E_rest)
            .add("Ratio U/E", ratio)
            .add("Negligible (< 10^-40)", negligible)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("U_grav (J)", 1.965e-56)  # G m_e^2 / r_e (CODATA); was 1.96e-57, an arithmetic slip
            .add("E_rest (J)", 8.187e-14)
            .add("Ratio U/E", 2.40e-43)  # = G m_e / (r_e c^2)
            .add("Negligible (< 10^-40)", 1)
        )


class VacuumImpedance(Test):
    """
    The impedance of free space Z_0 = sqrt(mu_0/epsilon_0) = 377 Ohms.
    
    GFM CONNECTION:
    The vacuum impedance is deeply connected to the speed of light through:
        c = 1/sqrt(mu_0 * epsilon_0)
        Z_0 = sqrt(mu_0/epsilon_0) = c * mu_0 = 1/(c * epsilon_0)
    
    LIGO's detection of gravitational waves at speed c (GFM Textbook Section 2.5)
    confirms that both EM and gravitational fields propagate at the same speed,
    determined by the same vacuum properties. This suggests a common geometric
    origin: the speed c emerges from the Field Envelope structure (Chapter 7.4)
    where the tetrahedral boundary conditions constrain propagation.
    
    The value 377 Ohms = c * mu_0 encodes the ratio of electric to magnetic
    field amplitudes in propagating waves, a geometric constraint from Maxwell's
    equations that GFM interprets as boundary matching at Coupling Ports.
    
    Textbook References: Section 2.5 (LIGO), Chapter 7.4 (Field Envelope)
    """
    name = "Vacuum Impedance and Field Propagation"
    question = (
        "Why does spacetime have a characteristic impedance of 377 Ohms, and what does "
        "this reveal about the vacuum structure? The same vacuum properties that give "
        "Z_0 = sqrt(mu_0/epsilon_0) also give c = 1/sqrt(mu_0*epsilon_0). When LIGO "
        "detected gravitational waves at speed c, it confirmed that gravity propagates "
        "through the same structured vacuum, suggesting a common geometric origin."
    )
    reference = "CODATA 2018; GFM Textbook Section 2.5 (LIGO)"
    tolerance = 0.01
    level = Level.STANDARD
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: If both EM and gravitational waves propagate at c, does this imply "
        "a unified vacuum structure, and could Z_0 have a gravitational analog? "
        "(Answering would improve Question by +2 points: deeper unification insight) "
        "Q2: How does the Field Envelope boundary condition at Coupling Ports "
        "constrain wave propagation speed to c? "
        "(Answering would improve Derivation by +3 points: geometric origin of c) "
        "Q3: Could variations in mu_0 or epsilon_0 at Planck scales modify Z_0, "
        "and would this affect gravitational wave propagation? "
        "(Answering would improve Commentary by +2 points: quantum gravity implications)"
    )
    
    commentary = (
        "The vacuum impedance Z_0 = 376.73 Ohms encodes fundamental structure: "
        "the same mu_0 and epsilon_0 that define Z_0 also define c = 1/sqrt(mu_0*epsilon_0). "
        "LIGO's detection of gravitational waves traveling at speed c confirms that "
        "gravity propagates through the same structured vacuum (GFM Textbook Section 2.5). "
        "In GFM terms, the Field Envelope boundary conditions constrain both EM and "
        "gravitational wave propagation. The value 377 Ohms = c * mu_0 sets the ratio "
        "of electric to magnetic amplitudes, analogous to how Coupling Port geometry "
        "constrains field closure. This is standard EM but hints at deeper structure."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("INTUITION: Why does empty space have 'impedance'?")
            .step("When a wave propagates, electric and magnetic fields oscillate together.")
            .step("Their amplitude ratio E/H = Z_0 is set by vacuum properties.")
            .step("VACUUM PROPERTIES: mu_0 (magnetic permeability) and epsilon_0 (electric permittivity)")
            .step("These same properties determine the speed of light: c = 1/sqrt(mu_0*epsilon_0)")
            .equation("Z_0 = sqrt(mu_0/epsilon_0) = c * mu_0 = 376.73 Ohms")
            .step("GFM CONNECTION: LIGO confirmed gravitational waves travel at c.")
            .step("Both EM and gravity propagate through the same structured vacuum.")
            .conclude("Z_0 = 377 Ohms encodes vacuum structure that constrains all field propagation.")
        )
    
    def model(self) -> Model:
        Z_0 = math.sqrt(MU_0 / EPSILON_0)
        c_from_vacuum = 1 / math.sqrt(MU_0 * EPSILON_0)
        Z_0_via_c = C * MU_0  # Alternative formula
        return (
            Model()
            .add("Z_0 = sqrt(mu_0/epsilon_0) (Ohms)", round(Z_0, 2))
            .add("Z_0 = c * mu_0 (Ohms)", round(Z_0_via_c, 2))
            .add("c from vacuum (m/s)", round(c_from_vacuum, 0))
            .add("Formulas agree", 1.0 if abs(Z_0 - Z_0_via_c) < 0.01 else 0.0)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Z_0 = sqrt(mu_0/epsilon_0) (Ohms)", 376.73)
            .add("Z_0 = c * mu_0 (Ohms)", 376.73)
            .add("c from vacuum (m/s)", 299792458.0)
            .add("Formulas agree", 1.0)
        )


class PlanckToElectronRatio(Test):
    """
    The ratio E_Planck / E_electron ~ 2.4e22.
    
    THIS IS THE HIERARCHY IN ENERGY TERMS:
    The Planck energy is ~10^22 times the electron rest energy.
    This scale separation is relevant to understanding why
    quantum gravity effects are inaccessible.
    """
    name = "Planck to Electron Energy Ratio"
    question = (
        "Why are quantum gravity effects inaccessible? The Planck to electron energy ratio "
        "~10^22 represents alpha^-10.5, showing the vast scale gap is geometric, not arbitrary."
    )
    reference = "CODATA 2018"
    tolerance = 0.10
    level = Level.STANDARD
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Why does alpha^-10.5 appear as the energy hierarchy exponent (half of 21)? "
        "(Answering would improve Derivation by +3 points: connecting to G derivation structure) "
        "Q2: What experiments could probe intermediate scales between electron and Planck? "
        "(Answering would improve Observation Quality by +3 points: identifying testable regimes) "
        "Q3: Does the 10^22 gap have implications for GFM's cosmological predictions? "
        "(Answering would improve Commentary by +2 points: exploring scale hierarchy consequences)"
    )
    
    commentary = (
        "The ratio E_Planck / E_electron ~ 2.4e22 shows the scale gap.\n\n"
        "This is related to the hierarchy problem:\n"
        "- E_Planck = sqrt(hbar*c^5/G) ~ 1.96e9 J ~ 1.22e19 GeV\n"
        "- E_electron = m_e*c^2 ~ 8.19e-14 J ~ 0.511 MeV\n"
        "- Ratio ~ 2.4e22\n\n"
        "If the G derivation is correct, this ratio is:\n"
        "m_P/m_e ~ alpha^-10.5 ~ (137)^10.5 ~ 2.5e22\n\n"
        "The hierarchy is geometric (alpha^-10.5), not fine-tuned."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ENERGY HIERARCHY:")
            .step("Planck energy: E_P = sqrt(hbar*c^5/G) = 1.96e9 J")
            .step("Electron rest energy: E_e = m_e*c^2 = 8.19e-14 J")
            .step("Ratio: E_P/E_e = 1.96e9 / 8.19e-14 = 2.4e22")
            .step("This corresponds to alpha^-10.5 ~ (137)^10.5 ~ 2.5e22")
            .conclude("The Planck scale is 10^22 above electron scale.")
        )
    
    def model(self) -> Model:
        E_electron = M_E * C**2
        ratio = E_PLANCK / E_electron
        log_ratio = math.log10(ratio)
        return (
            Model()
            .add("E_Planck (J)", E_PLANCK)
            .add("E_electron (J)", E_electron)
            .add("Ratio", ratio)
            .add("log10(ratio)", round(log_ratio, 2))
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("E_Planck (J)", 1.96e9)
            .add("E_electron (J)", 8.19e-14)
            .add("Ratio", 2.4e22)
            .add("log10(ratio)", 22.38)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    ElectronRestEnergy,
    GravitationalSelfEnergy,
    VacuumImpedance,
    PlanckToElectronRatio,
]


def run_all() -> bool:
    """Run all field energy tests."""
    return run_tests(
        title="Field Energy Scales",
        summary=(
            "This module documents energy scales relevant to GFM.\n\n"
            "THESE ARE NOT EMERGENT CONSTANT DERIVATIONS.\n"
            "They are standard physics calculations that establish the\n"
            "energy hierarchy and justify certain GFM assumptions.\n\n"
            "KEY RESULTS:\n"
            "- Electron rest energy: 511 keV (reference scale)\n"
            "- Gravitational self-energy negligible: ratio ~ 10^-43\n"
            "- Vacuum impedance: 377 Ohms (standard EM)\n"
            "- Planck to electron ratio: ~10^22 (the energy hierarchy)"
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
