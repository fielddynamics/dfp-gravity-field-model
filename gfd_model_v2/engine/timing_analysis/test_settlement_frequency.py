"""
Settlement Frequency
====================

This module examines the settlement frequency, defined as c / λ_compton
(the electron Compton frequency), approximately 1.236 × 10²⁰ Hz.

Key relationships:
- Settlement frequency: f = c / λ_compton ≈ 1.236e20 Hz
- Port firing frequency: f / k = f / 4 (one Coupling Port per Field Chamber face)
- Settlement period: ~8 × 10⁻²¹ seconds (yoctosecond range)

These tests validate the frequency calculations and their correspondences
with physical constants.
"""

import sys
import os
import numpy as np
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from gfd_model_v2.common import C, HBAR, K, ELECTRON_MASS, calculate_settlement_frequency


# =============================================================================
# CONSTANTS
# =============================================================================

COMPTON_WAVELENGTH = 2.426310238e-12  # Electron Compton wavelength (m)
PLANCK_FREQUENCY = 1.85e43  # Planck frequency (Hz)


# =============================================================================
# TESTS
# =============================================================================

class SettlementFrequencyDerivation(GFDTest):
    """
    The settlement frequency f = c / lambda_compton connects the speed of light
    to the electron's characteristic wavelength. This frequency (about 1.24e20 Hz)
    represents how fast the field can "respond" to electron-scale changes.
    """
    name = "Settlement Frequency Derivation"
    question = "Does the formula f = c/λ_Compton yield the settlement frequency of approximately 1.236×10²⁰ Hz?"
    reference_source = "Theoretical (c / lambda_compton)"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Compton wavelength λ_c relates electron mass to a characteristic length. "
        "STEP 1: λ_c = h/(m_e c) = 2.426×10⁻¹² m (electron Compton wavelength). "
        "STEP 2: Settlement frequency f = c / λ_c. "
        "STEP 3: f = (2.998×10⁸ m/s) / (2.426×10⁻¹² m). "
        "STEP 4: f ≈ 1.236×10²⁰ Hz. "
        "OUTPUT: Settlement frequency = 1.236×10²⁰ Hz."
    )
    commentary = (
        "The settlement frequency connects relativistic and quantum scales through "
        "the electron Compton wavelength. This 10^20 Hz timescale places Field "
        "Closure dynamics in the quantum electrodynamic regime."
    )
    
    def model(self) -> Dict[str, float]:
        f = C / COMPTON_WAVELENGTH
        return {"Settlement frequency (Hz)": f}
    
    def observations(self) -> Dict[str, float]:
        return {"Settlement frequency (Hz)": 1.2356e20}


class SettlementPeriod(GFDTest):
    """
    The settlement period T = 1/f is in the yoctosecond range (~8e-21 s).
    This is the time for one complete field settlement cycle, the
    fundamental "tick" of the electron's internal clock.
    """
    name = "Settlement Period"
    question = "Is the settlement period T = 1/f in the yoctosecond range (~10⁻²⁴ to 10⁻²¹ seconds)?"
    reference_source = None  # Model output
    derivation = (
        "PREMISE: The settlement period is the inverse of the settlement frequency. "
        "STEP 1: f ≈ 1.236×10²⁰ Hz. "
        "STEP 2: T = 1/f = 1/(1.236×10²⁰) ≈ 8.09×10⁻²¹ s. "
        "STEP 3: Convert to yoctoseconds: T ≈ 8.09 ys (1 ys = 10⁻²⁴ s). "
        "STEP 4: Range check: 10⁻²⁵ < T < 10⁻¹⁹ confirms yoctosecond regime. "
        "OUTPUT: Settlement period ≈ 8.09×10⁻²¹ s, in yoctosecond range = 1."
    )
    commentary = (
        "The yoctosecond settlement period represents the fundamental time scale "
        "of Field Closure. This period is vastly shorter than any directly "
        "measurable time interval, placing it below current experimental access."
    )
    
    def model(self) -> Dict[str, float]:
        f = calculate_settlement_frequency()
        T = 1 / f
        T_yoctoseconds = T * 1e24
        in_range = 1 if 1e-25 < T < 1e-19 else 0
        return {
            "Settlement period (s)": T,
            "Period (yoctoseconds)": T_yoctoseconds,
            "In yoctosecond range": in_range,
        }


class PortFiringFrequency(GFDTest):
    """
    Each tetrahedron has 4 faces (ports). The port firing frequency is
    f_settlement / k = f / 4, representing how fast each individual
    port processes information.
    """
    name = "Port Firing Frequency"
    question = "Does the per-Coupling-Port firing frequency equal f_settlement/k = f/4, connecting cycle rate to tetrahedral topology?"
    reference_source = "Theoretical (f / 4)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Each tetrahedron has k=4 Coupling Ports that process information. "
        "STEP 1: Settlement frequency f ≈ 1.236×10²⁰ Hz (one complete cycle). "
        "STEP 2: With k=4 ports per tetrahedron, each port fires at f/k. "
        "STEP 3: Port firing frequency = f/4 ≈ 3.09×10¹⁹ Hz. "
        "STEP 4: Ratio f/f_port = 4 = k. "
        "OUTPUT: Port firing frequency ≈ 3.09×10¹⁹ Hz, ratio = 4."
    )
    commentary = (
        "Dividing the settlement frequency by k=4 gives the per-Coupling-Port "
        "firing rate. This connects the overall cycle frequency to the "
        "k-fold tetrahedral topology of the Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        f = calculate_settlement_frequency()
        f_port = f / K
        return {
            "Settlement frequency (Hz)": f,
            "Port firing frequency (Hz)": f_port,
            "Ratio (f / f_port)": f / f_port,
        }
    
    def observations(self) -> Dict[str, float]:
        f = calculate_settlement_frequency()
        return {
            "Settlement frequency (Hz)": f,
            "Port firing frequency (Hz)": f / 4,
            "Ratio (f / f_port)": 4,
        }


class FrequencyFromEnergy(GFDTest):
    """
    The settlement frequency can also be derived from the electron rest
    energy: f = E / h = mc^2 / h. This should match c / lambda_compton exactly,
    confirming the deep connection between mass and frequency.
    """
    name = "Frequency from Energy"
    question = "Does the frequency derived from electron rest energy f = m_e c²/h exactly match f = c/λ_Compton?"
    reference_source = "E = hf identity"
    tolerance = 0.01
    derivation = (
        "PREMISE: Both E = hf and λ = h/(mc) relate frequency to mass. "
        "STEP 1: From energy: f_E = m_e c² / h. "
        "STEP 2: From wavelength: f_λ = c / λ_c = c / [h/(m_e c)] = m_e c² / h. "
        "STEP 3: Both expressions give f = m_e c² / h. "
        "STEP 4: Calculate ratio f_E / f_λ = 1.0. "
        "OUTPUT: Ratio = 1.0."
    )
    commentary = (
        "The identity between energy-derived and wavelength-derived frequencies "
        "confirms the settlement frequency connects to electron mass through "
        "standard quantum relations. This is a consistency check, not a prediction."
    )
    
    def model(self) -> Dict[str, float]:
        E = ELECTRON_MASS * C**2
        h = HBAR * 2 * np.pi
        f_energy = E / h
        f_compton = C / COMPTON_WAVELENGTH
        ratio = f_energy / f_compton
        return {
            "f from energy (Hz)": f_energy,
            "f from Compton (Hz)": f_compton,
            "Ratio": ratio,
        }
    
    def observations(self) -> Dict[str, float]:
        f = C / COMPTON_WAVELENGTH
        return {
            "f from energy (Hz)": f,
            "f from Compton (Hz)": f,
            "Ratio": 1.0,
        }


class DimensionalConsistency(GFDTest):
    """
    Dimensional analysis: f x lambda should equal c. This confirms the
    frequency and wavelength are correctly related through the
    fundamental wave equation. Uses Compton frequency (not settlement frequency).
    """
    name = "Dimensional Consistency"
    question = "Does the product f_Compton × λ_Compton equal c, verifying dimensional consistency of the wave equation?"
    reference_source = "Wave equation"
    tolerance = 0.001
    derivation = (
        "PREMISE: The wave equation relates wavelength, frequency, and phase velocity: c = fλ. "
        "STEP 1: Compton frequency f_c = c / λ_c ≈ 1.236×10²⁰ Hz. "
        "STEP 2: λ_c = 2.426×10⁻¹² m. "
        "STEP 3: Product = f_c × λ_c = c (by definition of f_c). "
        "STEP 4: This is a consistency check, not a prediction. "
        "OUTPUT: Ratio = 1.0."
    )
    commentary = None  # Dimensional consistency verification
    
    def model(self) -> Dict[str, float]:
        # Use Compton frequency directly (not settlement frequency)
        f_compton = C / COMPTON_WAVELENGTH
        c_check = f_compton * COMPTON_WAVELENGTH
        ratio = c_check / C
        return {
            "f x lambda (m/s)": c_check,
            "c (m/s)": C,
            "Ratio": ratio,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "f x lambda (m/s)": C,
            "c (m/s)": C,
            "Ratio": 1.0,
        }


class FrequencyInPhysicalRange(GFDTest):
    """
    The settlement frequency should be much greater than optical (about 10^15 Hz)
    but much less than Planck frequency (about 10^43 Hz). This places it in the
    quantum electrodynamics regime, not the quantum gravity regime.
    """
    name = "Frequency in Physical Range"
    question = "Is the settlement frequency (~10²⁰ Hz) between optical frequencies (~10¹⁵ Hz) and Planck frequency (~10⁴³ Hz)?"
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Physical relevance requires the frequency to be in an accessible regime. "
        "STEP 1: Optical frequency scale: f_optical ≈ 10¹⁵ Hz (visible light). "
        "STEP 2: Planck frequency: f_Planck ≈ 1.85×10⁴³ Hz (quantum gravity scale). "
        "STEP 3: Settlement frequency f ≈ 1.24×10²⁰ Hz. "
        "STEP 4: Check: 10¹⁵ < 10²⁰ < 10⁴³ → in QED regime, not QG regime. "
        "OUTPUT: In valid range = 1."
    )
    commentary = (
        "The settlement frequency occupying the range between optical and Planck "
        "frequencies places Field Closure in the quantum electrodynamic regime. "
        "This scale separation justifies treating the model without quantum gravity."
    )
    
    def model(self) -> Dict[str, float]:
        f = calculate_settlement_frequency()
        optical = 1e15
        planck = PLANCK_FREQUENCY
        in_range = 1 if optical < f < planck else 0
        return {
            "Settlement frequency (Hz)": f,
            "Above optical (10^15 Hz)": 1 if f > optical else 0,
            "Below Planck (10^43 Hz)": 1 if f < planck else 0,
            "In valid range": in_range,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    SettlementFrequencyDerivation,
    SettlementPeriod,
    PortFiringFrequency,
    FrequencyFromEnergy,
    DimensionalConsistency,
    FrequencyInPhysicalRange,
]


def run_all_tests() -> bool:
    """Run all settlement frequency tests."""
    return run_test_group(
        title="Settlement Frequency",
        summary=(
            "These tests validate the settlement frequency f = c / λ_compton (about "
            "1.24e20 Hz). This frequency corresponds to the electron's Compton wavelength "
            "and connects to rest mass energy through E = hf. The Coupling Port firing "
            "frequency f/4 reflects the tetrahedral geometry with 4 Coupling Ports per "
            "Field Chamber."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
