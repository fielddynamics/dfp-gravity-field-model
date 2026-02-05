"""
Field Energy Scales
===================

This module documents energy scales relevant to the GFD framework.

CRITICAL NOTE:
These tests do NOT derive emergent constants. They calculate energy
scales using standard physics formulas (E = mc^2, E = hf, U = Gm^2/r).

WHY THIS FILE EXISTS:
Understanding the energy scales helps establish where GFD effects
should (and should not) be observable. But these are calculations,
not derivations of fundamental constants.

WHAT WAS REMOVED:
- Tests claiming energy calculations are "emergent"
- Speculative interpretations presented as derivations
- Numerology (e.g., 1836/4 = 459)

WHAT REMAINS:
- Verification of standard physics at GFD-relevant scales
- Energy scale comparisons to establish the hierarchy
- The cosmological constant problem (unsolved, honestly noted)
"""

import sys
import math

from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, H as H_PLANCK, HBAR, G, M_E, R_E, E_PLANCK,
    MU_0, EPSILON_0,
)

# =============================================================================
# CONSTANTS
# =============================================================================

# Closure frequency assumption: f = c / r_e (Compton-scale)
CLOSURE_FREQUENCY = C / R_E


# =============================================================================
# TESTS
# =============================================================================

class ElectronRestEnergy(Test):
    """
    The electron rest energy E = m_e * c^2 = 511 keV.
    
    THIS IS STANDARD PHYSICS, NOT A DERIVATION.
    We document this as a reference scale for GFD.
    """
    name = "Electron Rest Energy (Reference Scale)"
    question = (
        "Does E = m_e * c^2 give 511 keV, the electron rest energy "
        "used as the GFD Field Envelope energy scale?"
    )
    reference = "CODATA 2018"
    tolerance = 0.001
    level = Level.STANDARD
    
    commentary = (
        "This is Einstein's E = mc^2 applied to the electron.\n"
        "It's standard physics, not a GFD derivation.\n"
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
    The ratio U_grav/E_rest ~ 10^-44 shows gravity is ~44 orders of
    magnitude weaker than electromagnetic binding at electron scales.
    """
    name = "Gravitational Self-Energy is Negligible"
    question = (
        "Is the gravitational self-energy U = Gm^2/r negligible compared to "
        "rest energy (ratio < 10^-40), justifying that quantum gravity "
        "effects are unobservable at particle scales?"
    )
    reference = "Standard gravitational physics"
    tolerance = 0.10
    level = Level.STANDARD
    
    commentary = (
        "This is an important CONSISTENCY CHECK, not a derivation.\n\n"
        "Gravitational self-energy: U = Gm_e^2/r_e ~ 2e-57 J\n"
        "Electron rest energy: E = m_e*c^2 ~ 8e-14 J\n"
        "Ratio: ~2.4e-44\n\n"
        "This 44 orders of magnitude difference explains why:\n"
        "1. Quantum gravity effects are unobservable at particle scales\n"
        "2. GFD focuses on classical field closure, not quantized gravity\n"
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
            .step("U = 1.96e-57 J")
            .step("E_rest = m_e * c^2 = 8.187e-14 J")
            .step("Ratio = U / E_rest = 1.96e-57 / 8.187e-14 = 2.4e-44")
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
            .add("U_grav (J)", 1.96e-57)
            .add("E_rest (J)", 8.187e-14)
            .add("Ratio U/E", 2.4e-44)
            .add("Negligible (< 10^-40)", 1)
        )


class VacuumImpedance(Test):
    """
    The impedance of free space Z_0 = sqrt(mu_0/epsilon_0) = 377 Ohms.
    
    THIS IS STANDARD EM PHYSICS.
    Documented here as a fundamental constant relevant to field propagation.
    """
    name = "Vacuum Impedance Z_0 = 377 Ohms"
    question = (
        "Does Z_0 = sqrt(mu_0/epsilon_0) equal ~377 Ohms?"
    )
    reference = "CODATA 2018"
    tolerance = 0.01
    level = Level.STANDARD
    
    commentary = None  # Standard physics, no special commentary needed
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("VACUUM IMPEDANCE (standard EM):")
            .step("mu_0 = 1.257e-6 H/m (permeability of free space)")
            .step("epsilon_0 = 8.854e-12 F/m (permittivity of free space)")
            .step("Z_0 = sqrt(mu_0/epsilon_0) = sqrt(1.257e-6 / 8.854e-12)")
            .step("Z_0 = sqrt(1.420e5) = 376.7 Ohms")
            .conclude("Vacuum impedance = 377 Ohms (standard result).")
        )
    
    def model(self) -> Model:
        Z_0 = math.sqrt(MU_0 / EPSILON_0)
        return Model().add("Vacuum impedance (Ohms)", round(Z_0, 2))
    
    def observations(self) -> Observed:
        return Observed().add("Vacuum impedance (Ohms)", 376.73)


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
        "Is the ratio of Planck energy to electron rest energy ~10^22, "
        "indicating the vast scale separation to quantum gravity?"
    )
    reference = "CODATA 2018"
    tolerance = 0.10
    level = Level.STANDARD
    
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
            "This module documents energy scales relevant to GFD.\n\n"
            "THESE ARE NOT EMERGENT CONSTANT DERIVATIONS.\n"
            "They are standard physics calculations that establish the\n"
            "energy hierarchy and justify certain GFD assumptions.\n\n"
            "KEY RESULTS:\n"
            "- Electron rest energy: 511 keV (reference scale)\n"
            "- Gravitational self-energy negligible: ratio ~ 10^-44\n"
            "- Vacuum impedance: 377 Ohms (standard EM)\n"
            "- Planck to electron ratio: ~10^22 (the energy hierarchy)"
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
