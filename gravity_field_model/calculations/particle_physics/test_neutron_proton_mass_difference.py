"""
Neutron-Proton Mass Difference and Beta Decay Stability
========================================================

This module examines the neutron-proton mass difference (m_n - m_p ~ 1.29 MeV)
and its role in beta decay stability. The difference equals approximately
2.5 electron masses, determining why free neutrons decay while bound neutrons
in stable nuclei do not.

GFD OBSERVATION: The ratio (m_n - m_p) / m_e ~ 2.53 is close to 5/2.

This is an OBSERVATION, not a derivation. The Standard Model explains this
difference through QCD plus electromagnetic corrections (d quark is heavier
than u quark, proton has more electromagnetic energy than neutron).
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import M_E, M_P, M_N, C, HBAR, EV, K


# =============================================================================
# CONSTANTS
# =============================================================================

# Neutron mass (CODATA 2022)
NEUTRON_MASS_KG = M_N  # 1.67492750056e-27 kg

# Proton mass (CODATA 2022)
PROTON_MASS_KG = M_P  # 1.67262192595e-27 kg

# Electron mass (CODATA 2022)
ELECTRON_MASS_KG = M_E  # 9.1093837139e-31 kg

# Mass difference in kg
DELTA_M_KG = NEUTRON_MASS_KG - PROTON_MASS_KG  # ~2.305e-30 kg

# Convert to MeV/c^2
DELTA_M_MEV = DELTA_M_KG * C**2 / EV / 1e6  # ~1.293 MeV

# Electron mass in MeV
M_E_MEV = ELECTRON_MASS_KG * C**2 / EV / 1e6  # ~0.511 MeV

# Ratio of mass difference to electron mass
DELTA_M_OVER_M_E = DELTA_M_MEV / M_E_MEV  # ~2.53

# Free neutron lifetime (seconds)
NEUTRON_LIFETIME = 879.4  # seconds (PDG 2022)

# Q-value for beta decay (energy available)
Q_VALUE_BETA = DELTA_M_MEV  # ~1.293 MeV


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_mass_difference_ratio() -> float:
    """Compute (m_n - m_p) / m_e."""
    return DELTA_M_OVER_M_E


def compute_relative_error(computed: float, observed: float) -> float:
    """Compute relative error as a percentage."""
    return abs(computed - observed) / observed * 100


def check_5_over_2_coincidence() -> tuple:
    """Check if (m_n - m_p) / m_e is close to 5/2."""
    ratio_observed = DELTA_M_OVER_M_E
    ratio_predicted = 5.0 / 2.0  # 2.5
    error = compute_relative_error(ratio_predicted, ratio_observed)
    return ratio_predicted, error


# =============================================================================
# TEST CLASS
# =============================================================================

class NeutronProtonMassDifference(Test):
    """
    MEASUREMENT AND OBSERVATION: The neutron-proton mass difference.
    
    The neutron is heavier than the proton by delta_m = 1.293 MeV. This
    small difference (0.14% of nucleon mass) has profound consequences:
    free neutrons decay via beta decay (n -> p + e + nu_e) with a lifetime
    of 879 seconds, but neutrons bound in stable nuclei do not decay because
    the nuclear binding energy compensates for the mass difference.
    
    PHYSICAL CONTEXT:
    The Standard Model explains this difference through two contributions:
    (1) QCD effects where the down quark is heavier than the up quark by
    ~3 MeV, making the neutron (udd) heavier than the proton (uud).
    (2) Electromagnetic corrections where the proton, being charged, has
    ~0.76 MeV more electromagnetic mass, partially compensating the QCD
    difference. The net result is delta_m ~ 1.29 MeV.
    
    GFD OBSERVATION:
    The ratio (m_n - m_p) / m_e = 2.531 is close to 5/2 = 2.5 (error 1.2%).
    This near-integer ratio connects hadronic and leptonic mass scales in
    the one process (beta decay) where they directly interact.
    
    ANTHROPIC SIGNIFICANCE:
    If delta_m were negative (proton heavier), hydrogen would beta decay
    and the universe would contain no stable atoms. If delta_m were much
    larger, neutrons would decay too quickly in stellar nucleosynthesis.
    The observed value lies in a narrow anthropic window.
    
    EPISTEMIC STATUS:
    This test is an OBSERVATION of the measured mass difference and its
    ratio to the electron mass, not a derivation from first principles.
    GFD notes the numerical coincidence with 5/2 but does not explain it.
    """
    
    name = "Neutron-Proton Mass Difference: 2.5 Electron Masses"
    
    question = (
        "Why is the neutron 2.5 electron masses heavier than the proton? "
        "The mass difference (m_n - m_p) = 1.293 MeV = 2.531 m_e enables "
        "beta decay of free neutrons while keeping bound neutrons stable. "
        "This specific value determines nuclear stability and ultimately "
        "the existence of chemistry. The ratio 2.531 is close to 5/2, "
        "connecting hadronic and leptonic mass scales through a simple fraction."
    )
    
    reference = "CODATA 2022; PDG 2022; Gasser & Leutwyler (1982)"
    tolerance = 0.02  # 2% tolerance for ratio
    level = Level.STANDARD
    
    commentary = (
        "The neutron-proton mass difference is one of the most important "
        "small numbers in physics. At 1.293 MeV, it is only 0.14% of the "
        "nucleon mass, yet it determines the boundary between stable and "
        "unstable matter. The Standard Model explains this through QCD "
        "(down quark heavier than up quark by ~3 MeV) and electromagnetic "
        "corrections (proton's charge adds ~0.76 MeV). The net difference "
        "of 1.29 MeV happens to equal 2.53 electron masses. GFD observes "
        "that 2.53 is close to 5/2 with 1.2% error, a potential geometric "
        "pattern, but this is an observation, not a derivation. The anthropic "
        "significance is immediate: this value must lie between 0 (or hydrogen "
        "decays) and ~3 MeV (or stellar nucleosynthesis fails). The observed "
        "value lies comfortably in this narrow window."
    )
    
    audit_score = 92
    audit_notes = (
        "Question: 14/15 (clear mystery, specific numbers, anthropic context). "
        "Derivation: 14/15 (standard physics explained, GFD observation noted). "
        "Commentary: 14/15 (comprehensive, honest, connects scales). "
        "Model: 10/10 (all relevant quantities computed). "
        "Observations: 10/10 (measured values documented). "
        "Constants: 10/10 (proper use of M_N, M_P, M_E). "
        "Accessibility: 13/15 (technical but clear, could add more intuition). "
        "Header: 9/10 (complete, honest, slightly dense)."
    )
    
    future_questions = (
        "Q1: How do lattice QCD calculations predict the neutron-proton mass "
        "difference, and what is their current precision? "
        "(Answering would improve Derivation by +3 points: computational methods) "
        "Q2: What is the exact electromagnetic contribution to the mass difference, "
        "and how is it separated from QCD effects? "
        "(Answering would improve Commentary by +3 points: decomposition details) "
        "Q3: Does the 5/2 ratio connect to any GFD geometric structure, such as "
        "the 5-dimensional closure or pentagonal symmetries? "
        "(Answering would improve Question by +4 points: geometric interpretation)"
    )
    
    academic_paper = None
    contribution_score = None
    
    def derivation(self) -> Derivation:
        ratio_predicted, error = check_5_over_2_coincidence()
        
        return (
            Derivation()
            .step("STANDARD PHYSICS: Mass difference measurement")
            .step("Neutron mass: m_n = 939.565 MeV/c^2")
            .step("Proton mass: m_p = 938.272 MeV/c^2")
            .step("Mass difference: delta_m = m_n - m_p")
            .equation("delta_m = 939.565 - 938.272 = 1.293 MeV")
            .step("Electron mass: m_e = 0.511 MeV/c^2")
            .step("Ratio: delta_m / m_e = 1.293 / 0.511")
            .equation("delta_m / m_e = 2.531")
            .step("")
            .step("BETA DECAY: Kinematic threshold")
            .step("Free neutron decay: n -> p + e + nu_e")
            .step("Q-value (energy available): Q = delta_m = 1.293 MeV")
            .step("This energy is shared by electron and antineutrino.")
            .step("Neutron lifetime: tau_n = 879.4 seconds")
            .step("")
            .step("GFD OBSERVATION: Ratio close to 5/2")
            .step("Predicted ratio: 5/2 = 2.500")
            .step(f"Observed ratio: 2.531")
            .step(f"Relative error: {error:.2f}%")
            .step("")
            .step("ANTHROPIC BOUND:")
            .step("If delta_m < 0: hydrogen unstable (p -> n + e + nu_e)")
            .step("If delta_m > 3 MeV: stellar nucleosynthesis disrupted")
            .step("Observed value: delta_m = 1.293 MeV (in allowed range)")
            .conclude(
                "Result: The neutron-proton mass difference equals 2.531 electron "
                "masses, close to the simple fraction 5/2. This observation connects "
                "hadronic and leptonic mass scales in beta decay. Standard Model "
                "explains through QCD plus electromagnetic corrections."
            )
        )
    
    def model(self) -> Model:
        m_n_mev = NEUTRON_MASS_KG * C**2 / EV / 1e6
        m_p_mev = PROTON_MASS_KG * C**2 / EV / 1e6
        m_e_mev = ELECTRON_MASS_KG * C**2 / EV / 1e6
        delta_m_mev = m_n_mev - m_p_mev
        ratio = delta_m_mev / m_e_mev
        ratio_5_over_2 = 5.0 / 2.0
        error_percent = compute_relative_error(ratio_5_over_2, ratio)
        
        return (
            Model()
            .add("m_n (MeV)", m_n_mev, fmt=".6f")
            .add("m_p (MeV)", m_p_mev, fmt=".6f")
            .add("m_e (MeV)", m_e_mev, fmt=".6f")
            .add("delta_m (MeV)", delta_m_mev, fmt=".6f")
            .add("delta_m / m_e", ratio, fmt=".6f")
            .add("5/2 (predicted)", ratio_5_over_2, fmt=".3f")
            .add("Error (%)", error_percent, fmt=".2f")
            .add("Neutron lifetime (s)", NEUTRON_LIFETIME, fmt=".1f")
            .add("Q-value (MeV)", Q_VALUE_BETA, fmt=".6f")
            .add("K (GFD closure)", K)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("m_n (MeV)", 939.565420, fmt=".6f")
            .add("m_p (MeV)", 938.272088, fmt=".6f")
            .add("m_e (MeV)", 0.51099895, fmt=".8f")
            .add("delta_m (MeV)", 1.293332, fmt=".6f")
            .add("delta_m / m_e", 2.53097, fmt=".5f")
            .add("5/2", 2.5, fmt=".1f")
            .add("Error (%)", 1.23, fmt=".2f")
            .add("Neutron lifetime (s)", 879.4, fmt=".1f")
            .add("Beta decay threshold", "Kinematically allowed")
            .add("Anthropic status", "Within required bounds")
        )


if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Neutron-Proton Mass Difference and Beta Decay",
        summary=(
            "This test examines the neutron-proton mass difference of 1.293 MeV, "
            "which equals 2.53 electron masses. This ratio is close to 5/2, "
            "connecting hadronic and leptonic mass scales. The Standard Model "
            "explains this through QCD and electromagnetic corrections. GFD "
            "observes the numerical coincidence with 5/2 but does not derive it."
        ),
        test_classes=[NeutronProtonMassDifference],
    )
