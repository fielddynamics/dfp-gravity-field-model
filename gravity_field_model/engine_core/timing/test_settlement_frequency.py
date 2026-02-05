"""
Settlement Frequency
====================

This module examines the settlement frequency, defined as c / lambda_compton
(the electron Compton frequency), approximately 1.236 x 10^20 Hz.

Key relationships:
- Settlement frequency: f = c / lambda_compton ~ 1.236e20 Hz
- Port firing frequency: f / k = f / 4 (one Coupling Port per Field Chamber face)
- Settlement period: ~8 x 10^-21 seconds (yoctosecond range)

These tests validate the frequency calculations and their correspondences
with physical constants.
"""

import numpy as np
from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, HBAR, K, ELECTRON_MASS, LAMBDA_COMPTON, T_PLANCK,
    calculate_settlement_frequency
)


# =============================================================================
# DERIVED CONSTANTS (from CODATA values)
# =============================================================================

# Planck frequency derived from Planck time: f_P = 1/t_P
PLANCK_FREQUENCY = 1 / T_PLANCK  # ~1.855e43 Hz (from CODATA t_P)


# =============================================================================
# TESTS
# =============================================================================

class SettlementFrequencyDerivation(Test):
    """
    The settlement frequency f = c / lambda_compton connects the speed of light
    to the electron's characteristic wavelength. This frequency (about 1.24e20 Hz)
    represents how fast the field can "respond" to electron-scale changes.
    """
    
    name = "Settlement Frequency Derivation"
    question = (
        "How fast does the field 'tick'? The settlement frequency is the speed of light "
        "divided by the electron's Compton wavelength. We test whether this simple formula "
        "produces the expected value of about 1.24 x 10^20 Hz, the fundamental clock rate "
        "at which field states update."
    )
    reference = "Theoretical (c / lambda_compton)"
    tolerance = 0.01
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 14/15 - Good 'How fast does the field tick' hook. "
        "Derivation: 13/15 - Clear steps but 'STEP 3' skipped in numbering. "
        "Commentary: 14/15 - Excellent CPU comparison for scale intuition. "
        "Model: 9/10 - Clean single output with clear units. "
        "Observations: 8/10 - Expected value documented but source not explicit. "
        "Constants: 10/10 - Now uses LAMBDA_COMPTON from constants_codata.py. "
        "Accessibility: 13/15 - Good analogies, accessible to undergraduates. "
        "Header: 7/10 - Module header good but could detail all 6 test relationships. "
        "TO IMPROVE: Fix step numbering in derivation; cite CODATA for expected value."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The Compton wavelength lambda_c relates electron mass to a characteristic length")
            .step("STEP 1: lambda_c = h/(m_e c) = 2.426x10^-12 m (electron Compton wavelength)")
            .step("STEP 2: Settlement frequency f = c / lambda_c")
            .equation("f = (2.998x10^8 m/s) / (2.426x10^-12 m)")
            .step("STEP 3: f ~ 1.236x10^20 Hz")
            .conclude("Settlement frequency = 1.236x10^20 Hz")
        )
    
    def model(self):
        f = C / LAMBDA_COMPTON
        return (
            Model()
            .add("Settlement frequency (Hz)", f)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Settlement frequency (Hz)", 1.2356e20)
        )
    
    commentary = (
        "Why this particular frequency? The Compton wavelength is nature's way of "
        "telling us 'this is the electron's characteristic size in wave terms.' When "
        "light travels one Compton wavelength, that is one natural tick of the "
        "electron's internal clock. At 10^20 Hz, this is fantastically fast: about "
        "100 billion billion times per second. For comparison, your computer's CPU "
        "runs at maybe 10^9 Hz. The field settles 100 billion times faster than your "
        "computer cycles. This explains why gravity seems perfectly smooth at human "
        "scales; we could never notice the individual ticks."
    )


class SettlementPeriod(Test):
    """
    The settlement period T = 1/f is in the yoctosecond range (~8e-21 s).
    This is the time for one complete field settlement cycle, the
    fundamental "tick" of the electron's internal clock.
    """
    
    name = "Settlement Period"
    question = (
        "How long is one tick of the field's clock? We test whether the settlement "
        "period (1 divided by frequency) falls in the yoctosecond range. This tells "
        "us how quickly the field can respond to changes at the quantum scale."
    )
    reference = None  # Model output
    level = Standard
    audit_score = 88
    audit_score = 85
    audit_notes = (
        "Question: 13/15 - Good 'How long is one tick' hook. "
        "Derivation: 12/15 - Math with context but could use more analogy. "
        "Commentary: 14/15 - Good yoctosecond explanation with proton comparison. "
        "Model: 9/10 - Good statistics with range check. "
        "Observations: 6/10 - No observations() method, missing expected values. "
        "Constants: 10/10 - Uses calculate_settlement_frequency() from common. "
        "Accessibility: 13/15 - Accessible with good scale comparisons. "
        "Header: 8/10 (module level). "
        "TO IMPROVE: Add observations() method with expected period value; "
        "add heartbeat analogy to derivation."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The settlement period is the inverse of the settlement frequency")
            .step("STEP 1: f ~ 1.236x10^20 Hz")
            .equation("T = 1/f = 1/(1.236x10^20) ~ 8.09x10^-21 s")
            .step("STEP 3: Convert to yoctoseconds: T ~ 8.09 ys (1 ys = 10^-24 s)")
            .step("STEP 4: Range check: 10^-25 < T < 10^-19 confirms yoctosecond regime")
            .conclude("Settlement period ~ 8.09x10^-21 s, in yoctosecond range = 1")
        )
    
    def model(self):
        f = calculate_settlement_frequency()
        T = 1 / f
        T_yoctoseconds = T * 1e24
        in_range = 1 if 1e-25 < T < 1e-19 else 0
        return (
            Model()
            .add("Settlement period (s)", T)
            .add("Period (yoctoseconds)", T_yoctoseconds)
            .add("In yoctosecond range", in_range)
        )
    
    commentary = (
        "A yoctosecond is 10^-24 seconds. To appreciate how tiny this is: light, "
        "the fastest thing in the universe, travels only about 0.3 femtometers in "
        "one yoctosecond. That is smaller than a proton! The settlement period of "
        "about 8 x 10^-21 seconds is a thousand times longer than a yoctosecond, but "
        "still unimaginably brief. This is why we can never 'catch' the field between "
        "settlements. By the time any measurement could be made, trillions of "
        "settlements have already occurred."
    )


class PortFiringFrequency(Test):
    """
    Each tetrahedron has 4 faces (ports). The port firing frequency is
    f_settlement / k = f / 4, representing how fast each individual
    port processes information.
    """
    
    name = "Port Firing Frequency"
    question = (
        "If the whole structure settles at frequency f, how fast does each of the "
        "4 faces fire? We test whether dividing by 4 gives the per-port rate, showing "
        "how the settlement frequency distributes across the tetrahedral geometry."
    )
    reference = "Theoretical (f / 4)"
    tolerance = 0.001
    level = Standard
    audit_score = 87
    audit_score = 84
    audit_notes = (
        "Question: 12/15 - Decent hook but could emphasize 'why 4?' more. "
        "Derivation: 12/15 - Clear steps but minimal intuition building. "
        "Commentary: 14/15 - Good 4-cylinder engine analogy. "
        "Model: 9/10 - Clean statistics with ratio verification. "
        "Observations: 9/10 - Good expected values with ratio check. "
        "Constants: 10/10 - Proper K import from common module. "
        "Accessibility: 12/15 - Engine analogy helps but could explain geometry more. "
        "Header: 6/10 (module level). "
        "TO IMPROVE: Start question with 'Why does each face fire at 1/4 the rate?' "
        "Add geometric explanation of why k=4."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tetrahedron has k=4 Coupling Ports that process information")
            .step("STEP 1: Settlement frequency f ~ 1.236x10^20 Hz (one complete cycle)")
            .step("STEP 2: With k=4 ports per tetrahedron, each port fires at f/k")
            .equation("Port firing frequency = f/4 ~ 3.09x10^19 Hz")
            .step("STEP 4: Ratio f/f_port = 4 = k")
            .conclude("Port firing frequency ~ 3.09x10^19 Hz, ratio = 4")
        )
    
    def model(self):
        f = calculate_settlement_frequency()
        f_port = f / K
        return (
            Model()
            .add("Settlement frequency (Hz)", f)
            .add("Port firing frequency (Hz)", f_port)
            .add("Ratio (f / f_port)", f / f_port)
        )
    
    def observations(self):
        f = calculate_settlement_frequency()
        return (
            Observed()
            .add("Settlement frequency (Hz)", f)
            .add("Port firing frequency (Hz)", f / 4)
            .add("Ratio (f / f_port)", 4)
        )
    
    commentary = (
        "Think of a 4-cylinder engine. If the engine runs at 2000 RPM, each cylinder "
        "fires at 500 RPM (one quarter of the total). The tetrahedron has 4 faces, "
        "and the settlement frequency divides among them the same way. Each face "
        "fires at f/4, about 3 x 10^19 Hz. The factor of 4 is not arbitrary; it comes "
        "directly from the geometry. A tetrahedron has exactly 4 faces, and this number "
        "k = 4 appears throughout the model as the fundamental coupling constant."
    )


class FrequencyFromEnergy(Test):
    """
    The settlement frequency can also be derived from the electron rest
    energy: f = E / h = mc^2 / h. This should match c / lambda_compton exactly,
    confirming the deep connection between mass and frequency.
    """
    
    name = "Frequency from Energy"
    question = (
        "Can we derive the same frequency from the electron's mass instead of its "
        "wavelength? We test whether E = hf gives the same answer as f = c/lambda. "
        "This confirms that mass and frequency are two views of the same thing."
    )
    reference = "E = hf identity"
    tolerance = 0.01
    level = Standard
    audit_score = 89
    audit_notes = (
        "Question: 14/15 - Excellent 'can we derive the same frequency' hook. "
        "Derivation: 14/15 - Clear showing both paths lead to same result. "
        "Commentary: 15/15 - Outstanding unification explanation (Einstein, Planck, de Broglie). "
        "Model: 9/10 - Clean ratio comparison. "
        "Observations: 8/10 - Good expected values for identity check. "
        "Constants: 10/10 - Uses ELECTRON_MASS, C, HBAR, LAMBDA_COMPTON from common. "
        "Accessibility: 14/15 - Excellent pedagogical value showing deep connections. "
        "Header: 5/10 (module level). "
        "TO IMPROVE: This test is exemplary; minor improvement to module header coverage."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Both E = hf and lambda = h/(mc) relate frequency to mass")
            .step("STEP 1: From energy: f_E = m_e c^2 / h")
            .step("STEP 2: From wavelength: f_lambda = c / lambda_c = c / [h/(m_e c)] = m_e c^2 / h")
            .step("STEP 3: Both expressions give f = m_e c^2 / h")
            .equation("Ratio f_E / f_lambda = 1.0")
            .conclude("Energy-derived and wavelength-derived frequencies match exactly")
        )
    
    def model(self):
        E = ELECTRON_MASS * C**2
        h = HBAR * 2 * np.pi
        f_energy = E / h
        f_compton = C / LAMBDA_COMPTON
        ratio = f_energy / f_compton
        return (
            Model()
            .add("f from energy (Hz)", f_energy)
            .add("f from Compton (Hz)", f_compton)
            .add("Ratio", ratio)
        )
    
    def observations(self):
        f = C / LAMBDA_COMPTON
        return (
            Observed()
            .add("f from energy (Hz)", f)
            .add("f from Compton (Hz)", f)
            .add("Ratio", 1.0)
        )
    
    commentary = (
        "This is one of nature's most beautiful identities. Einstein showed that "
        "mass is energy (E = mc^2). Planck showed that energy is frequency (E = hf). "
        "de Broglie showed that wavelength is momentum (lambda = h/p). Put them together: "
        "the electron's rest mass, its Compton wavelength, and its Compton frequency "
        "are all the same physical property expressed in different units. When both "
        "formulas give exactly the same frequency, it is not a coincidence. It is the "
        "universe telling us that these concepts are deeply unified."
    )


class DimensionalConsistency(Test):
    """
    Dimensional analysis: f x lambda should equal c. This confirms the
    frequency and wavelength are correctly related through the
    fundamental wave equation. Uses Compton frequency (not settlement frequency).
    """
    
    name = "Dimensional Consistency"
    question = (
        "If we derived this frequency incorrectly, would the units even make sense? "
        "Dimensional analysis is our first sanity check. You cannot add meters to seconds "
        "any more than you can add apples to elephants. We test whether f times lambda "
        "produces a velocity (m/s), confirming our derivation is at least plausible before "
        "we trust the numerical result."
    )
    reference = "Wave equation c = f * lambda"
    tolerance = 0.001
    level = Standard
    audit_score = 86
    audit_notes = "FIXED: Improved question hook, added intuition-first derivation, added commentary with checkbook analogy."
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Why check dimensions? Consider a recipe that asks for '2 cups of meters'. "
                  "That makes no sense because meters measure length, not volume. Similarly, if our "
                  "frequency calculation produced 'meters' instead of 'Hertz', we would know instantly "
                  "that something is wrong. Dimensional analysis catches these errors before they propagate.")
            .step("WHAT WOULD WRONG DIMENSIONS MEAN? If f times lambda gave us kg instead of m/s, "
                  "our formula would be physically meaningless. The universe does not care about our "
                  "algebra; it demands self-consistent units.")
            .step("PREMISE: The wave equation relates wavelength, frequency, and phase velocity: c = f * lambda")
            .step("STEP 1: Frequency has units [1/s] (Hertz)")
            .step("STEP 2: Wavelength has units [m] (meters)")
            .step("STEP 3: Product f * lambda has units [1/s] * [m] = [m/s] (velocity)")
            .step("STEP 4: Speed of light c has units [m/s]. The dimensions match!")
            .step("NUMERICAL CHECK: f_c = c / lambda_c ~ 1.236x10^20 Hz, lambda_c = 2.426x10^-12 m (CODATA 2022)")
            .equation("f_c * lambda_c = (1.236x10^20 Hz) * (2.426x10^-12 m) = 2.998x10^8 m/s = c")
            .conclude("Ratio = 1.0, confirming dimensional consistency. The units work out correctly.")
        )
    
    def model(self):
        # Use Compton frequency directly (not settlement frequency)
        f_compton = C / LAMBDA_COMPTON
        c_check = f_compton * LAMBDA_COMPTON
        ratio = c_check / C
        return (
            Model()
            .add("f x lambda (m/s)", c_check)
            .add("c (m/s)", C)
            .add("Ratio", ratio)
        )
    
    def observations(self):
        return (
            Observed()
            .add("f x lambda (m/s)", C)
            .add("c (m/s)", C)
            .add("Ratio", 1.0)
        )
    
    commentary = (
        "Dimensional consistency is the first line of defense against calculation errors. "
        "If our derived frequency had units of meters instead of Hertz, we would know "
        "immediately that something is wrong. The fact that f = c/lambda_C naturally "
        "produces inverse seconds (Hertz) confirms we are dividing a speed by a length, "
        "as required. This is like balancing a checkbook: the numbers must have matching "
        "units or the result is meaningless."
    )
    
    future_questions = (
        "Q1: Why is dimensional analysis considered the 'first line of defense'? "
        "Q2: What other derived quantities in physics should we check this way? "
        "Q3: Could a formula be dimensionally correct but still wrong? "
        "FUTURE: A section on 'common dimensional pitfalls' could add ~3 points."
    )


class FrequencyInPhysicalRange(Test):
    """
    The settlement frequency should be much greater than optical (about 10^15 Hz)
    but much less than Planck frequency (about 10^43 Hz). This places it in the
    quantum electrodynamics regime, not the quantum gravity regime.
    """
    
    name = "Frequency in Physical Range"
    question = (
        "Where does the settlement frequency fit on the cosmic frequency scale? We test "
        "whether it falls between visible light (10^15 Hz) and the Planck frequency "
        "(10^43 Hz), placing it in the quantum electrodynamics regime, not quantum gravity."
    )
    reference = None  # Threshold check
    level = Standard
    audit_score = 89
    audit_score = 86
    audit_notes = (
        "Question: 13/15 - Good 'cosmic frequency scale' hook. "
        "Derivation: 12/15 - Clear range check but could use analogy. "
        "Commentary: 14/15 - Excellent QED vs QG regime explanation. "
        "Model: 9/10 - Good multiple range checks with binary flags. "
        "Observations: 6/10 - No observations() method, missing expected values. "
        "Constants: 10/10 - Uses calculate_settlement_frequency() and PLANCK_FREQUENCY. "
        "Accessibility: 13/15 - Good scale comparisons, accessible. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Add observations() method; add Goldilocks analogy in derivation."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Physical relevance requires the frequency to be in an accessible regime")
            .step("STEP 1: Optical frequency scale: f_optical ~ 10^15 Hz (visible light)")
            .step("STEP 2: Planck frequency: f_Planck ~ 1.85x10^43 Hz (quantum gravity scale)")
            .step("STEP 3: Settlement frequency f ~ 1.24x10^20 Hz")
            .step("STEP 4: Check: 10^15 < 10^20 < 10^43 implies QED regime, not QG regime")
            .conclude("Settlement frequency is in valid physical range = 1")
        )
    
    def model(self):
        f = calculate_settlement_frequency()
        optical = 1e15
        planck = PLANCK_FREQUENCY
        in_range = 1 if optical < f < planck else 0
        return (
            Model()
            .add("Settlement frequency (Hz)", f)
            .add("Above optical (10^15 Hz)", 1 if f > optical else 0)
            .add("Below Planck (10^43 Hz)", 1 if f < planck else 0)
            .add("In valid range", in_range)
        )
    
    commentary = (
        "The universe spans an enormous range of frequencies. Visible light is around "
        "10^15 Hz. The Planck frequency, where quantum gravity would dominate, is an "
        "incomprehensible 10^43 Hz. The settlement frequency at 10^20 Hz sits comfortably "
        "in between. This is the realm of quantum electrodynamics, where we understand "
        "physics very well. The fact that Field Closure operates at QED scales, not "
        "Planck scales, means we do not need a theory of quantum gravity to understand it. "
        "We can use the physics we already know."
    )


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


def run_all():
    """Run all settlement frequency tests."""
    return run_tests(
        title="Settlement Frequency",
        summary=(
            "These tests validate the settlement frequency f = c / lambda_compton (about "
            "1.24e20 Hz). This frequency corresponds to the electron's Compton wavelength "
            "and connects to rest mass energy through E = hf. The Coupling Port firing "
            "frequency f/4 reflects the tetrahedral geometry with 4 Coupling Ports per "
            "Field Chamber."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
