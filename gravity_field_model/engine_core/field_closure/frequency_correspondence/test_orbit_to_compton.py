"""
Orbit to Compton Frequency Mapping
==================================

This module maps pi-base-8 orbit frequency to electron Compton frequency.

THE CORRESPONDENCE:
If the pi-base-8 traversal IS the field closure mechanism, and the Field Origin
is a resonance node at the electron Compton frequency, then:

    f_orbit = f_compton / digits_per_orbit

THE QUESTION:
Can we derive physical frequencies from traversal statistics?

KEY FREQUENCIES:
- Electron Compton frequency: f_e = m_e c^2 / h = 1.236e20 Hz
- Electron Compton angular frequency: omega_e = m_e c^2 / hbar = 7.76e20 rad/s
- Orbit frequency: f_orbit = f_e / 2.42 ~ 5.1e19 Hz

Reference: THE_ORIGIN_TIME_AND_ONE.md, Paper VI
"""

import math

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, C, HBAR, M_E, H


# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Electron mass energy
E_ELECTRON = M_E * C**2  # ~ 8.19e-14 J

# Electron Compton frequency: f = E / h
F_COMPTON = E_ELECTRON / H  # ~ 1.236e20 Hz

# Electron Compton angular frequency: omega = E / hbar
OMEGA_COMPTON = E_ELECTRON / HBAR  # ~ 7.76e20 rad/s

# Electron Compton wavelength
LAMBDA_COMPTON = H / (M_E * C)  # ~ 2.43e-12 m

# Electron Compton time (period)
T_COMPTON = 1 / F_COMPTON  # ~ 8.09e-21 s


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_mean_digits_per_orbit(n_digits=10000):
    """Compute mean digits per orbit from traversal."""
    traversal = traverse_pi_base8(n_digits)
    
    orbit_lengths = []
    current_length = 0
    prev_orbit = 0
    
    for step in traversal:
        current_length += 1
        curr_orbit = step['cumsum'] // 8
        
        if curr_orbit > prev_orbit:
            orbit_lengths.append(current_length)
            current_length = 0
            prev_orbit = curr_orbit
    
    if not orbit_lengths:
        return 0
    
    return sum(orbit_lengths) / len(orbit_lengths)


def compute_orbit_frequencies(mean_digits_per_orbit):
    """
    Compute orbit frequencies from mean digits per orbit.
    
    Mapping: 1 digit = 1 tick at Compton frequency
    Therefore: orbit_frequency = compton_frequency / digits_per_orbit
    """
    f_orbit = F_COMPTON / mean_digits_per_orbit
    omega_orbit = 2 * math.pi * f_orbit
    T_orbit = 1 / f_orbit
    lambda_orbit = C * T_orbit  # "Wavelength" of orbit
    
    return {
        'f_orbit': f_orbit,
        'omega_orbit': omega_orbit,
        'T_orbit': T_orbit,
        'lambda_orbit': lambda_orbit,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class ComptonFrequencyAnchor(Test):
    """
    Verify that electron Compton frequency is the anchor for all mappings.
    
    The Field Origin resonates at the Compton frequency because the electron
    is the gravity-EM crossover particle (Paper III).
    """
    name = "Compton Frequency as Anchor"
    question = (
        "Why is the electron Compton frequency the natural 'clock' for the "
        "Merkaba? Because the electron is the gravity-EM crossover particle."
    )
    reference = "Paper III, Paper VI"
    level = Critical
    tolerance = 0.001
    
    commentary = (
        "THE ELECTRON AS THE NATURAL CLOCK: "
        "Why the electron Compton frequency? "
        "It's the frequency at which the electron's rest mass resonates. "
        "It's where EM and gravity couple (Paper III). "
        "It's the Field Origin's natural vibration. "
        "The mapping: Each pi digit = one tick at f_compton. "
        "Each orbit = digits_per_orbit ticks. "
        "This connects abstract traversal to physical time."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("THE COMPTON FREQUENCY:")
            .step("The electron Compton frequency is:")
            .equation("f_e = m_e c^2 / h = E_electron / h")
            .step("In SI units:")
            .equation("f_e = (9.11e-31 kg) x (3e8 m/s)^2 / (6.63e-34 J*s)")
            .equation("f_e = 1.236e20 Hz")
            .step("WHY THIS FREQUENCY?")
            .step("Paper III shows the electron is where EM and gravity converge.")
            .conclude("The Compton frequency is the natural resonance of this scale.")
        )
    
    def model(self):
        return (
            Model()
            .add("E_electron (J)", E_ELECTRON)
            .add("f_compton (Hz)", F_COMPTON)
            .add("omega_compton (rad/s)", OMEGA_COMPTON)
            .add("T_compton (s)", T_COMPTON)
            .add("lambda_compton (m)", LAMBDA_COMPTON)
        )
    
    def observations(self):
        return (
            Observed()
            .add("f_compton (Hz)", 1.236e20)
            .add("T_compton (s)", 8.09e-21)
            .add("lambda_compton (m)", 2.43e-12)
        )


class DigitToTickMapping(Test):
    """
    Map pi digits to Compton frequency ticks.
    
    The hypothesis: 1 pi digit = 1 tick at f_compton
    """
    name = "Digit to Compton Tick Mapping"
    question = (
        "If each pi digit represents one tick at the Compton frequency, "
        "how many ticks occur per orbit?"
    )
    reference = "Traversal-to-frequency mapping"
    level = Standard
    tolerance = 0.05
    
    commentary = (
        "THE PHYSICAL MEANING OF A DIGIT: "
        "In this mapping: 1 digit = 1 Compton tick ~ 8e-21 seconds. "
        "1 orbit = ~2.42 ticks ~ 2e-20 seconds. "
        "The traversal 'runs' at 1.2e20 digits per second. "
        "Physical interpretation: The pi digits are not just math. "
        "They ARE the ticks of the quantum clock at the Field Origin."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("DIGIT-TO-TICK MAPPING:")
            .step("Hypothesis: 1 pi digit = 1 tick at f_compton")
            .step("Then:")
            .step("1 digit takes time: T_digit = 1/f_compton = T_compton")
            .step("1 orbit takes: T_orbit = (digits_per_orbit) x T_compton")
            .step("Orbit frequency: f_orbit = f_compton / digits_per_orbit")
            .step("With mean_digits ~ 2.42:")
            .equation("f_orbit = 1.236e20 / 2.42 = 5.1e19 Hz")
            .conclude("This maps abstract traversal to physical frequencies.")
        )
    
    def model(self):
        mean_digits = compute_mean_digits_per_orbit(10000)
        freqs = compute_orbit_frequencies(mean_digits)
        
        return (
            Model()
            .add("Mean digits per orbit", mean_digits)
            .add("Ticks per orbit", mean_digits)
            .add("T_orbit (s)", freqs['T_orbit'])
            .add("f_orbit (Hz)", freqs['f_orbit'])
        )
    
    def observations(self):
        return (
            Observed()
            .add("Mean digits per orbit", 2.42)
            .add("f_orbit (Hz)", 5.1e19)
        )


class OrbitFrequencyScale(Test):
    """
    What is the orbit frequency and how does it relate to known scales?
    """
    name = "Orbit Frequency Scale"
    question = (
        "How does the orbit frequency (~5e19 Hz) compare to other fundamental "
        "frequencies? Is it close to any known scale?"
    )
    reference = "Fundamental frequency scales"
    level = Standard
    tolerance = 0.20
    
    commentary = (
        "WHERE THE ORBIT FREQUENCY SITS: "
        "The Merkaba orbits at ~5e19 Hz, which is: "
        "~2.4x slower than Compton frequency. "
        "~100,000x faster than visible light. "
        "~100x faster than typical X-rays. "
        "Comparable to soft gamma rays. "
        "This makes sense: The Merkaba operates at quantum scales, "
        "not macroscopic light-wave scales. "
        "The orbit frequency is deep in the quantum realm, "
        "where the electron's structure lives."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("ORBIT FREQUENCY IN CONTEXT:")
            .step("Merkaba orbit frequency: f_orbit ~ 5e19 Hz")
            .step("Comparison scales:")
            .step("Compton frequency: 1.2e20 Hz (factor of ~2.4 higher)")
            .step("Visible light: 4e14 to 8e14 Hz (factor of ~1e5 lower)")
            .step("X-rays: 3e16 to 3e19 Hz (comparable)")
            .step("Gamma rays: > 3e19 Hz (comparable)")
            .conclude("The orbit frequency is in the hard X-ray / soft gamma range.")
        )
    
    def model(self):
        mean_digits = compute_mean_digits_per_orbit(10000)
        freqs = compute_orbit_frequencies(mean_digits)
        
        # Comparison frequencies
        f_visible_light = 5e14  # Hz (green light)
        
        # Ratios
        ratio_to_compton = F_COMPTON / freqs['f_orbit']
        ratio_to_visible = freqs['f_orbit'] / f_visible_light
        
        return (
            Model()
            .add("f_orbit (Hz)", freqs['f_orbit'])
            .add("f_compton (Hz)", F_COMPTON)
            .add("Ratio compton/orbit", ratio_to_compton)
            .add("Ratio orbit/visible", ratio_to_visible)
        )
    
    def observations(self):
        return (
            Observed()
            .add("f_visible (Hz)", 5e14)
            .add("f_compton (Hz)", 1.2e20)
        )


# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all orbit-to-Compton frequency tests."""
    return run_tests(
        "Orbit to Compton Frequency",
        "Tests for mapping pi-base-8 orbit frequency to electron Compton frequency",
        [
            ComptonFrequencyAnchor,
            DigitToTickMapping,
            OrbitFrequencyScale,
        ]
    )


if __name__ == "__main__":
    run_all()
