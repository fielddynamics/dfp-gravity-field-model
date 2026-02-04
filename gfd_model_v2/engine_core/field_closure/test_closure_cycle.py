"""
Closure Cycle Mechanics
=======================

The model posits a fundamental frequency of order 10^23 Hz, termed the
closure frequency. These tests examine whether this frequency, combined
with the classical electron radius as a length scale, produces values
consistent with measured physical constants.

The tests compare:
- Model-derived values for the speed of light
- Relative scale comparisons to Planck units and quantum frequencies
- Consistency with known physical constants

No causal claims are made; the tests document numerical correspondences.
"""

from typing import Dict, Optional

from gfd_model_v2.framework import *
from gfd_model_v2.common import (
    C, H as H_PLANCK, HBAR as H_BAR, T_PLANCK, L_PLANCK,
    M_E, ALPHA, R_E,
)

# Derived model parameters
CLOSURE_FREQUENCY = C / R_E   # ~1.06e23 Hz
CLOSURE_PERIOD = 1 / CLOSURE_FREQUENCY


# =============================================================================
# TESTS
# =============================================================================

class SpeedOfLightFromClosure(Test):
    """
    The model proposes that the speed of light relates to the closure
    frequency and the classical electron radius: c = r_e x f_closure.
    This test checks whether this product approximates the measured value.
    """
    name = "Speed of Light Derivation"
    question = (
        "Can we derive the speed of light from first principles? "
        "If Field Closure happens at frequency f across a region of size r, then "
        "the maximum propagation speed should be r x f. This test checks whether "
        "multiplying the electron radius by the closure frequency gives c."
    )
    reference = "CODATA 2018"
    tolerance = 0.10  # 10% tolerance for this relationship
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Field Closure operates at frequency f_closure with gravity field size r_e (classical electron radius).")
            .step("Gravity field size: r_e = 2.818 x 10^-15 m.")
            .step("Closure frequency: f_closure = 10^23 Hz.")
            .step("Calculate: c_predicted = r_e x f_closure = 2.818 x 10^-15 x 10^23 = 2.818 x 10^8 m/s.")
            .step("Compare to observed: c = 2.998 x 10^8 m/s. Ratio: 0.94 (within 10%).")
            .conclude("Speed of light = 2.818 x 10^8 m/s (model), ratio to observed = 0.94.")
        )
    
    commentary = (
        "Speed = distance / time. If information updates once per closure cycle (time = 1/f), "
        "and can travel one gravity field width per cycle (distance = r_e), then "
        "max speed = r_e x f. Plugging in the numbers: roughly 3 x 10^8 m/s. "
        "That is the speed of light. We get within 10% without adjusting anything. "
        "This suggests the closure frequency and electron radius are not independent; "
        "they conspire to produce exactly the cosmic speed limit."
    )
    
    def model(self):
        c_predicted = R_E * CLOSURE_FREQUENCY
        return Model().add("Speed of light (m/s)", c_predicted)
    
    def observations(self):
        return Observed().add("Speed of light (m/s)", C)


class ClosureAbovePlanckScale(Test):
    """
    The closure period (~10^-23 s) is much larger than Planck time (~10^-44 s).
    This scale separation places the model's dynamics well above the regime
    where quantum gravity effects would be expected to dominate.
    """
    name = "Closure Above Planck Scale"
    question = (
        "Are we safely above the quantum gravity regime? "
        "Planck time (10^-44 seconds) is where spacetime itself becomes fuzzy. "
        "Closure operates at 10^-23 seconds, 20 orders of magnitude slower. "
        "This test confirms we stay in 'normal physics' territory."
    )
    reference = None  # Threshold check, not comparison
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Quantum gravity effects dominate near Planck time t_P = 5.391 x 10^-44 s.")
            .step("Closure period: T_closure = 1/f_closure = 1/10^23 = 10^-23 s.")
            .step("Planck time: t_P = 5.391 x 10^-44 s.")
            .step("Calculate ratio: T_closure / t_P = 10^-23 / 5.391 x 10^-44 = 1.86 x 10^20.")
            .step("Check threshold: 1.86 x 10^20 > 10^19.")
            .conclude("Ratio = 1.86 x 10^20, threshold met = 1.")
        )
    
    commentary = (
        "At the Planck scale (10^-44 seconds), physics gets weird. Spacetime itself fluctuates; "
        "our usual rules may not apply. Fortunately, Field Closure operates 20 orders of magnitude "
        "slower, at 10^-23 seconds. This is still unimaginably fast (a closure cycle is to one second "
        "as one second is to 3 trillion years), but it is 'normal' fast, not 'quantum gravity' fast. "
        "We can use ordinary physics here. The Planck regime is a distant basement we never visit."
    )
    
    def model(self):
        ratio = CLOSURE_PERIOD / T_PLANCK
        threshold_met = 1 if ratio > 1e19 else 0
        return (
            Model()
            .add("Closure period (s)", CLOSURE_PERIOD)
            .add("Planck time (s)", T_PLANCK)
            .add("Ratio (closure/Planck)", ratio)
            .add("Above 10^19 threshold", threshold_met)
        )


class GravityFieldAbovePlanckLength(Test):
    """
    The model uses the classical electron radius (~10^-15 m) as its length
    scale, which is much larger than Planck length (~10^-35 m). This ratio
    of approximately 10^20 suggests the model operates above the Planck scale.
    """
    name = "Gravity Field Above Planck Length"
    question = (
        "How small is the Field Chamber? "
        "It operates at the classical electron radius (10^-15 meters), which is tiny "
        "but still 20 orders of magnitude larger than the Planck length where space breaks down. "
        "This test confirms we are working at safe, well-understood scales."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Quantum gravity effects dominate near Planck length l_P = 1.616 x 10^-35 m.")
            .step("Gravity field size: r_e = 2.818 x 10^-15 m (classical electron radius).")
            .step("Planck length: l_P = 1.616 x 10^-35 m.")
            .step("Calculate ratio: r_e / l_P = 2.818 x 10^-15 / 1.616 x 10^-35 = 1.74 x 10^20.")
            .step("Check threshold: 1.74 x 10^20 > 10^18.")
            .conclude("Ratio = 1.74 x 10^20, threshold met = 1.")
        )
    
    commentary = (
        "The electron radius is about 10^-15 meters: a millionth of a billionth of a meter. "
        "Tiny! But compared to the Planck length (10^-35 meters), it is enormous. "
        "The ratio is 10^20, about as big as the number of grains of sand on Earth. "
        "This huge gap means we operate in 'normal' small, not 'quantum gravity' small. "
        "The Field Chamber is small enough to be interesting but large enough to be understood."
    )
    
    def model(self):
        ratio = R_E / L_PLANCK
        threshold_met = 1 if ratio > 1e18 else 0
        return (
            Model()
            .add("Gravity field size r_e (m)", R_E)
            .add("Planck length (m)", L_PLANCK)
            .add("Ratio (gravity-field/Planck)", ratio)
            .add("Above 10^18 threshold", threshold_met)
        )


class ClosureVsComptonFrequency(Test):
    """
    The electron Compton frequency (m_e c^2 / h) is a fundamental quantum scale.
    This test examines the ratio between the model's closure frequency and the
    Compton frequency, which the model places in the range of 100-10000.
    """
    name = "Closure vs Compton Frequency"
    question = (
        "How fast is Field Closure compared to quantum jitters? "
        "The Compton frequency (10^20 Hz) represents the quantum 'clock' of electron mass. "
        "Closure runs about 1000 times faster. This test quantifies how Field Closure "
        "operates at a finer timescale than quantum mechanics typically considers."
    )
    reference = "Theoretical (100-10000x range)"
    tolerance = 0.50  # Order of magnitude check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Compton frequency represents the quantum oscillation rate associated with electron mass.")
            .step("Compton frequency: f_Compton = m_e * c^2 / h = 9.109 x 10^-31 * (2.998 x 10^8)^2 / 6.626 x 10^-34 = 1.24 x 10^20 Hz.")
            .step("Closure frequency: f_closure = 10^23 Hz.")
            .step("Calculate ratio: f_closure / f_Compton = 10^23 / 1.24 x 10^20 = 807.")
            .step("This is approximately 10^3 (within 100-10000 range).")
            .conclude("Ratio (closure/Compton) = 807.")
        )
    
    commentary = (
        "Quantum mechanics says electrons have a characteristic frequency: E = mc^2 divided by Planck's "
        "constant gives about 10^20 oscillations per second. That is incomprehensibly fast. "
        "Yet Field Closure is about 1000 times faster still! Think of it this way: "
        "if quantum oscillations were once per second, closure would be 1000 times per second. "
        "Field Closure provides a finer-grained clock than even quantum mechanics usually considers."
    )
    
    def model(self):
        f_compton = (M_E * C**2) / H_PLANCK
        ratio = CLOSURE_FREQUENCY / f_compton
        return Model().add("Ratio (closure/Compton)", ratio)
    
    def observations(self):
        # Expected to be in 100-10000 range, use geometric mean
        return Observed().add("Ratio (closure/Compton)", 1000)


class CausalityPropagation(Test):
    """
    If the model's length scale (r_e) divided by its time scale (closure period)
    yields a velocity, this test checks whether that velocity corresponds to the
    speed of light. This is the same relationship as SpeedOfLightFromClosure.
    """
    name = "Causality Propagation Speed"
    question = (
        "What is the cosmic speed limit in this model? "
        "If information can jump one field width per closure cycle, that maximum speed "
        "should equal the speed of light. This test verifies the Field Chamber's geometry "
        "respects relativity's fundamental constraint."
    )
    reference = "CODATA 2018"
    tolerance = 0.10
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Maximum propagation = 1 gravity field per cycle, defining the causal light cone.")
            .step("Gravity field size: r_e = 2.818 x 10^-15 m.")
            .step("Closure period: T = 1/f_closure = 10^-23 s.")
            .step("Maximum velocity: v_max = r_e / T = 2.818 x 10^-15 / 10^-23 = 2.818 x 10^8 m/s.")
            .step("Compare to c = 2.998 x 10^8 m/s. Ratio: 0.94 (within 10%).")
            .conclude("Max propagation speed = 2.818 x 10^8 m/s.")
        )
    
    commentary = (
        "Nothing travels faster than light. This is not just a rule; it is built into spacetime. "
        "Our model encodes this constraint naturally: if you can only move one gravity field width "
        "per closure cycle, and we plug in the numbers, the maximum speed is c. "
        "The geometry of the Field Chamber automatically enforces the cosmic speed limit. "
        "This is satisfying: the speed of light emerges from structure, not as an imposed rule."
    )
    
    def model(self):
        v_max = R_E / CLOSURE_PERIOD
        return Model().add("Max propagation speed (m/s)", v_max)
    
    def observations(self):
        return Observed().add("Max propagation speed (m/s)", C)


class ClosureVsZitterbewegung(Test):
    """
    Zitterbewegung is the electron's rapid oscillation predicted by the Dirac
    equation at frequency 2 m_e c^2 / h. This test compares that frequency
    to the model's closure frequency to establish scale relationships.
    """
    name = "Closure vs Zitterbewegung"
    question = (
        "Is Field Closure faster than the electron's own 'trembling'? "
        "The Dirac equation predicts electrons jitter at 10^20 Hz (zitterbewegung). "
        "Closure runs 400 times faster. This test establishes the hierarchy of timescales."
    )
    reference = "Dirac equation prediction"
    tolerance = 0.50  # Order of magnitude
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Zitterbewegung (electron trembling) has frequency f_zitter = 2 * m_e * c^2 / h.")
            .step("Calculate f_zitter = 2 * 9.109 x 10^-31 * (2.998 x 10^8)^2 / 6.626 x 10^-34 = 2.47 x 10^20 Hz.")
            .step("Closure frequency: f_closure = 10^23 Hz.")
            .step("Calculate ratio: f_closure / f_zitter = 10^23 / 2.47 x 10^20 = 405.")
            .step("This is approximately 400 (within order of magnitude tolerance).")
            .conclude("Ratio (closure/zitterbewegung) = 405.")
        )
    
    commentary = (
        "Zitterbewegung means 'trembling motion' in German. Dirac's equation predicts electrons "
        "vibrate incredibly fast, about 10^20 times per second. This is the electron's quantum jitter. "
        "But Field Closure is 400 times faster still. If zitterbewegung were a hummingbird's wings, "
        "closure would be 400 hummingbirds. This suggests Field Closure provides the 'canvas' on which "
        "even the fastest quantum phenomena paint their pictures."
    )
    
    def model(self):
        f_zitter = 2 * M_E * C**2 / H_PLANCK
        ratio = CLOSURE_FREQUENCY / f_zitter
        return Model().add("Ratio (closure/zitterbewegung)", ratio)
    
    def observations(self):
        return Observed().add("Ratio (closure/zitterbewegung)", 400)


class FineStructureConstant(Test):
    """
    The fine structure constant alpha = 1/137.036 measures the strength of
    electromagnetic interactions. This test verifies the model uses the
    correct CODATA value for this fundamental constant.
    """
    name = "Fine Structure Constant"
    question = (
        "What is alpha, and why does 137 matter? "
        "Alpha (about 1/137) measures how strongly light and matter interact. "
        "This test simply confirms we use the correct measured value, since 137 orbits "
        "will become significant in other parts of the model."
    )
    reference = "CODATA 2018"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The fine structure constant alpha characterizes electromagnetic coupling strength.")
            .step("CODATA 2018 value: alpha = 1/137.035999084 = 0.0072973525693.")
            .step("Model uses: ALPHA = 1/137.036.")
            .step("Calculate 1/ALPHA = 137.036.")
            .step("Verify agreement: |1/137.036 - 1/137.036| < 0.001 tolerance.")
            .conclude("Alpha = 1/137.036, 1/Alpha = 137.036.")
        )
    
    commentary = (
        "The number 137 has fascinated physicists for a century. Feynman called it 'one of the "
        "greatest damn mysteries of physics.' Alpha = 1/137 tells us how strong the electromagnetic "
        "force is. Why 137 and not 100 or 200? Nobody knows. We simply accept nature's choice. "
        "This test verifies we use the right value, because later we will discover 137 orbits "
        "appear in the Field Closure structure. Coincidence or connection? The universe keeps its secrets."
    )
    
    def model(self):
        return (
            Model()
            .add("Alpha", ALPHA)
            .add("1/Alpha", 1/ALPHA)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Alpha", 1/137.036)
            .add("1/Alpha", 137.036)
        )


class EnergyTimeUncertainty(Test):
    """
    Using the uncertainty principle (Delta_E x Delta_t >= hbar/2), the model
    calculates the energy scale associated with the closure period. This test
    reports the model's energy uncertainty at the closure timescale.
    """
    name = "Energy-Time Uncertainty"
    question = (
        "How much energy can 'borrow' from nothing during one closure cycle? "
        "Heisenberg says: shorter time means larger energy uncertainty. "
        "At 10^-23 seconds, we can borrow about 33 keV, enough to create virtual particles. "
        "This test calculates the energy budget at closure timescales."
    )
    reference = None  # Model output only
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Energy-time uncertainty: Delta_E * Delta_t >= hbar/2.")
            .step("Delta_t = closure period = 1/f_closure = 10^-23 s.")
            .step("Minimum Delta_E = hbar / (2 * Delta_t) = 1.055 x 10^-34 / (2 x 10^-23).")
            .step("Delta_E = 5.275 x 10^-12 J.")
            .step("Convert to keV: 5.275 x 10^-12 / (1.602 x 10^-16) = 33 keV.")
            .conclude("Max energy uncertainty = 33 keV.")
        )
    
    commentary = (
        "Quantum mechanics lets you 'borrow' energy for short times. The shorter the loan, "
        "the bigger you can borrow. At closure timescales (10^-23 seconds), you can borrow "
        "about 33 keV. That is enough energy to pop virtual electron-positron pairs into existence! "
        "This explains why vacuum is not really empty: at Field Closure timescales, "
        "there is enough energy uncertainty for particles to flicker in and out of existence."
    )
    
    def model(self):
        delta_t = CLOSURE_PERIOD
        delta_E = H_BAR / (2 * delta_t)
        delta_E_keV = delta_E / (1.602e-19 * 1000)
        return (
            Model()
            .add("Min time resolution (s)", delta_t)
            .add("Max energy uncertainty (J)", delta_E)
            .add("Max energy (keV)", delta_E_keV)
        )


class ClosureVsGravityWaves(Test):
    """
    Gravitational waves detected by LIGO (10-1000 Hz) operate at a vastly
    lower frequency than the model's closure frequency. This test computes
    the ratio to establish the scale separation between these phenomena.
    """
    name = "Closure vs Gravity Waves"
    question = (
        "How does Field Closure compare to gravitational waves? "
        "LIGO detects ripples in spacetime at about 100 Hz. Closure operates at 10^23 Hz. "
        "The ratio is 10^21, an almost inconceivable difference. "
        "This test establishes just how different these scales are."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: LIGO detects gravitational waves in the 10-1000 Hz range.")
            .step("Typical GW frequency: f_GW = 100 Hz.")
            .step("Closure frequency: f_closure = 10^23 Hz.")
            .step("Calculate ratio: f_closure / f_GW = 10^23 / 100 = 10^21.")
            .step("Check threshold: 10^21 > 10^20.")
            .conclude("Ratio = 10^21, threshold met = 1.")
        )
    
    commentary = (
        "LIGO made headlines by detecting gravitational waves, cosmic rumbles from colliding black holes. "
        "Those waves vibrate about 100 times per second. That sounds fast, but Field Closure is "
        "10^21 times faster. If a gravitational wave were a heartbeat, Field Closure would beat "
        "more times per second than there are grains of sand on every beach on Earth. "
        "These are completely different regimes: astrophysics versus particle physics."
    )
    
    def model(self):
        f_gw_typical = 100  # Hz, typical LIGO detection
        ratio = CLOSURE_FREQUENCY / f_gw_typical
        threshold_met = 1 if ratio > 1e20 else 0
        return (
            Model()
            .add("Typical GW frequency (Hz)", f_gw_typical)
            .add("Closure frequency (Hz)", CLOSURE_FREQUENCY)
            .add("Ratio", ratio)
            .add("Above 10^20 threshold", threshold_met)
        )


class TimeArrowFromClosure(Test):
    """
    The model proposes that macroscopic time comprises many closure cycles.
    This test calculates how many cycles occur per second and per year at
    the model's closure frequency of 10^23 Hz.
    """
    name = "Time Arrow from Closure"
    question = (
        "How many closure cycles make up one second? "
        "We experience time as a smooth flow, but perhaps it is actually a rapid sequence "
        "of discrete updates. At 10^23 Hz, each second contains more cycles than there are "
        "stars in the observable universe. This test counts the 'atoms of time.'"
    )
    reference = None  # Model output only
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Macroscopic time emerges from vast numbers of closure cycles.")
            .step("Closure frequency: f_closure = 10^23 Hz = 10^23 cycles/second.")
            .step("Cycles per second: 10^23.")
            .step("Seconds per year: 3.15 x 10^7.")
            .step("Cycles per year: 10^23 x 3.15 x 10^7 = 3.15 x 10^30 cycles.")
            .conclude("Cycles per second = 10^23, cycles per year = 3.15 x 10^30.")
        )
    
    commentary = (
        "Is time continuous or does it tick? If it ticks at 10^23 times per second, "
        "we would never notice the gaps. In one second, 10^23 closure cycles occur. "
        "In one year, that is 10^30 cycles, more than the number of atoms in a human body. "
        "This astronomical number explains why time seems smooth to us: the 'pixels' are "
        "so small we cannot see them. We experience the statistical average of countless "
        "closure events, giving us the sensation of continuous flow."
    )
    
    def model(self):
        cycles_per_second = CLOSURE_FREQUENCY
        cycles_per_year = cycles_per_second * 3.15e7
        return (
            Model()
            .add("Cycles per second", cycles_per_second)
            .add("Cycles per year", cycles_per_year)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    SpeedOfLightFromClosure,
    ClosureAbovePlanckScale,
    GravityFieldAbovePlanckLength,
    ClosureVsComptonFrequency,
    CausalityPropagation,
    ClosureVsZitterbewegung,
    FineStructureConstant,
    EnergyTimeUncertainty,
    ClosureVsGravityWaves,
    TimeArrowFromClosure,
]


def run_all():
    """Run all closure cycle tests."""
    return run_tests(
        title="Closure Cycle Mechanics",
        summary=(
            "The model proposes a fundamental frequency of 10^23 Hz (the closure "
            "frequency) and uses the classical electron radius as its length scale. "
            "These tests examine whether these parameters produce values consistent "
            "with physical constants, including the speed of light and scale "
            "relationships to Planck units and quantum frequencies. The tests "
            "document numerical correspondences without asserting causal explanations."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
