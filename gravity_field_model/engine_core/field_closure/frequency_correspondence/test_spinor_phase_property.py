"""
Spinor Phase Property
=====================

This module verifies the 720-degree (2-orbit) phase return property.

THE SPINOR PROPERTY:
Spin-1/2 particles are spinors: they need 720 degrees (not 360) to return
to their original state. Under a 360-degree rotation:
    psi -> -psi (sign flip)
Under 720 degrees:
    psi -> +psi (original state)

THE GFM CONNECTION:
In the Merkaba traversal:
- 1 orbit = 360 degrees = cumsum increases by 8
- 2 orbits = 720 degrees = spinor returns to original phase

THE PREDICTION:
Physical properties should show periodicity at 2 orbits, not 1 orbit.

Reference: Spinor mathematics, ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md
"""

from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def analyze_phase_periodicity(n_digits=10000):
    """
    Analyze phase periodicity in traversal statistics.
    
    Look for patterns that repeat every 2 orbits vs every 1 orbit.
    """
    traversal = traverse_pi_base8(n_digits)
    
    # Track vertex at each orbit boundary
    orbit_boundary_vertices = []
    current_orbit = 0
    
    for step in traversal:
        orbit_num = step['cumsum'] // 8
        if orbit_num > current_orbit:
            orbit_boundary_vertices.append(step['vertex'])
            current_orbit = orbit_num
    
    # Check 1-orbit periodicity: do we return to same vertex?
    one_orbit_returns = 0
    for i in range(len(orbit_boundary_vertices) - 1):
        if orbit_boundary_vertices[i] == orbit_boundary_vertices[i + 1]:
            one_orbit_returns += 1
    
    # Check 2-orbit periodicity: do we return after 2 orbits?
    two_orbit_returns = 0
    for i in range(len(orbit_boundary_vertices) - 2):
        if orbit_boundary_vertices[i] == orbit_boundary_vertices[i + 2]:
            two_orbit_returns += 1
    
    n_one = len(orbit_boundary_vertices) - 1
    n_two = len(orbit_boundary_vertices) - 2
    
    return {
        'total_orbits': len(orbit_boundary_vertices),
        'one_orbit_returns': one_orbit_returns,
        'two_orbit_returns': two_orbit_returns,
        'one_orbit_return_rate': one_orbit_returns / n_one if n_one > 0 else 0,
        'two_orbit_return_rate': two_orbit_returns / n_two if n_two > 0 else 0,
        'expected_random': 0.125,  # 1/8 chance of same vertex
    }


def analyze_chamber_phase(n_digits=10000):
    """
    Analyze chamber (TetA/TetB) phase pattern.
    
    The spinor property suggests chamber patterns should have 2-orbit period.
    """
    traversal = traverse_pi_base8(n_digits)
    
    # Track chamber at each orbit boundary
    orbit_chambers = []  # 'A' or 'B'
    current_orbit = 0
    
    for step in traversal:
        orbit_num = step['cumsum'] // 8
        if orbit_num > current_orbit:
            chamber = 'A' if step['vertex'] in TET_A else 'B'
            orbit_chambers.append(chamber)
            current_orbit = orbit_num
    
    # Pattern analysis
    # Check for alternating pattern (ABAB...)
    alternating_count = 0
    for i in range(len(orbit_chambers) - 1):
        if orbit_chambers[i] != orbit_chambers[i + 1]:
            alternating_count += 1
    
    # Check for 2-orbit pattern (AABB...)
    two_orbit_pattern = 0
    for i in range(len(orbit_chambers) - 2):
        if orbit_chambers[i] == orbit_chambers[i + 2]:
            two_orbit_pattern += 1
    
    n_one = len(orbit_chambers) - 1
    n_two = len(orbit_chambers) - 2
    
    return {
        'total_orbits': len(orbit_chambers),
        'alternating_rate': alternating_count / n_one if n_one > 0 else 0,
        'two_orbit_match_rate': two_orbit_pattern / n_two if n_two > 0 else 0,
        'chamber_sequence': ''.join(orbit_chambers[:20]) + '...',
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class TwoOrbitPhasePeriod(Test):
    """
    Does the traversal show 2-orbit periodicity (spinor property)?
    
    Spinors need 720 degrees (2 orbits) to return to original state.
    We test whether the vertex return rate is higher at 2 orbits vs 1 orbit.
    """
    name = "Two-Orbit Phase Period"
    question = (
        "Does the traversal show 2-orbit periodicity? "
        "Spinors need 720 degrees to return to their original state. "
        "Is the 2-orbit return rate higher than 1-orbit?"
    )
    reference = "Spinor mathematics"
    level = Critical
    tolerance = 0.20
    
    commentary = (
        "INTERPRETING PHASE PERIODICITY: "
        "If both rates are ~12.5% (1/8), the traversal is random. No spinor signature. "
        "If 2-orbit rate > 1-orbit rate significantly, there's a 720-degree periodic structure. "
        "What this would mean: The Merkaba 'prefers' to return after 2 orbits, "
        "matching the spinor phase period. This is a PREDICTION of the hourglass model."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("SPINOR PHASE PERIOD:")
            .step("For a spinor (spin-1/2):")
            .step("360 deg rotation: psi -> -psi (sign flip)")
            .step("720 deg rotation: psi -> +psi (original)")
            .step("In Merkaba language:")
            .step("1 orbit (360 deg): may not return to original state")
            .step("2 orbits (720 deg): returns to original state")
            .conclude("Test: Is 2-orbit return rate > 1-orbit return rate?")
        )
    
    def model(self):
        analysis = analyze_phase_periodicity(10000)
        return (
            Model()
            .add("Total orbits", analysis['total_orbits'])
            .add("1-orbit returns", analysis['one_orbit_returns'])
            .add("2-orbit returns", analysis['two_orbit_returns'])
            .add("1-orbit return rate", analysis['one_orbit_return_rate'], tol=0.12)
            .add("2-orbit return rate", analysis['two_orbit_return_rate'], tol=0.09)
        )
    
    def observations(self):
        # Return rates at orbit boundaries for independent uniform digits (mean
        # of 60 random sequences): 0.143 after one orbit and 0.175 after two.
        # Both differ from 1/8 because orbit boundaries are correlated, and the
        # 2-orbit rate exceeds the 1-orbit rate for random digits too, so a
        # higher 2-orbit return rate is not by itself evidence of a spinor
        # period. Pi is compared with this baseline.
        return (
            Observed()
            .add("1-orbit return rate", 0.143)
            .add("2-orbit return rate", 0.175)
        )

class ChamberAlternation(Test):
    """
    Do chambers alternate every orbit, or show 2-orbit patterns?
    
    ABAB... would be 1-orbit period
    AABB... would be 2-orbit period
    """
    name = "Chamber Alternation Pattern"
    question = (
        "What is the chamber (TetA/TetB) pattern at orbit boundaries? "
        "Does it alternate (ABAB) or show 2-orbit structure (AABB)?"
    )
    reference = "Bimetric coupling, spinor property"
    level = Standard
    tolerance = 0.15
    
    commentary = (
        "CHAMBER PATTERNS AND SPINORS: "
        "If alternation rate ~ 50% and 2-orbit match ~ 50%, the pattern is random (no preferred period). "
        "A spinor signature would show: 2-orbit match rate significantly > 50%. "
        "Chambers tend to 'pair up' over 2 orbits. "
        "Physical meaning: The vortex 'breathes' with a 2-orbit period, spending paired orbits in each chamber."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("CHAMBER ALTERNATION:")
            .step("At each orbit boundary, record which chamber we're in:")
            .step("A = in TetA, B = in TetB")
            .step("Possible patterns:")
            .step("ABABAB: pure alternation (50% alternation rate)")
            .step("AABBAA: 2-orbit blocks")
            .step("Random: ~50% alternation (but no structure)")
            .conclude("Spinor property suggests 2-orbit periodicity.")
        )
    
    def model(self):
        analysis = analyze_chamber_phase(10000)
        return (
            Model()
            .add("Total orbits", analysis['total_orbits'])
            .add("Alternation rate", analysis['alternating_rate'], tol=0.04)
            .add("2-orbit match rate", analysis['two_orbit_match_rate'], tol=0.05)
        )
    
    def observations(self):
        # Expected for independent uniform digits (mean of 60 random sequences):
        # chamber alternation at orbit boundaries 0.526 and 2-orbit match 0.497.
        # These differ slightly from 0.5 because orbit boundaries are not
        # independent draws. A real 2-orbit (spinor) period would push the
        # 2-orbit match rate well above this baseline.
        return (
            Observed()
            .add("Alternation rate", 0.526)
            .add("2-orbit match rate", 0.497)
        )

class SpinorFrequencyRatio(Test):
    """
    Verify that spinor frequency = orbit frequency / 2.
    
    The spinor period is 2 orbits, so f_spinor = f_orbit / 2.
    """
    name = "Spinor Frequency Ratio"
    question = (
        "Is the spinor frequency exactly half the orbit frequency? "
        "This is a direct consequence of the 720-degree phase period."
    )
    reference = "Spinor mathematics"
    level = Ignore
    ignore_reason = (
        'f_orbit is typed in (5.1e19 Hz) and f_spinor is defined as f_orbit / 2, so the ratio is 2 by definition.'
    )
    tolerance = 0.001
    
    commentary = (
        "THE FACTOR OF 2: "
        "This factor of 2 appears everywhere in spin physics: "
        "Spinor period = 2 x geometric period. "
        "Spin quantum number = 1/2 (not 1). g-factor anomaly ~ 2. "
        "In the Merkaba: f_spinor = f_orbit / 2. "
        "The electron doesn't 'spin' at the orbit frequency. "
        "Its intrinsic phase cycles at HALF that rate, "
        "because it takes 2 orbits to complete a phase cycle."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("SPINOR VS ORBIT FREQUENCY:")
            .step("Definition:")
            .step("1 orbit = 360 degrees")
            .step("1 spinor period = 720 degrees = 2 orbits")
            .step("Therefore:")
            .equation("T_spinor = 2 x T_orbit")
            .equation("f_spinor = f_orbit / 2")
            .conclude("This is EXACT, not approximate.")
        )
    
    def model(self):
        # This is pure math, no traversal needed
        f_orbit = 5.1e19  # Hz (from previous tests)
        f_spinor = f_orbit / 2
        
        T_orbit = 1 / f_orbit
        T_spinor = 1 / f_spinor
        
        ratio = f_orbit / f_spinor
        
        return (
            Model()
            .add("f_orbit (Hz)", f_orbit)
            .add("f_spinor (Hz)", f_spinor)
            .add("T_orbit (s)", T_orbit)
            .add("T_spinor (s)", T_spinor)
            .add("Ratio f_orbit / f_spinor", ratio)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Expected ratio", 2.0)
        )


# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all spinor phase property tests."""
    return run_tests(
        "Spinor Phase Property",
        "Tests for the 720-degree (2-orbit) phase return property",
        [
            TwoOrbitPhasePeriod,
            ChamberAlternation,
            SpinorFrequencyRatio,
        ]
    )


if __name__ == "__main__":
    run_all()
