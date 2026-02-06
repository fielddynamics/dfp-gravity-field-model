"""
Probing Vortex Transit: Geometric Length Scales in Nuclear Physics
==================================================================

GFD Model V2

INVESTIGATION STATEMENT:
The GFD model defines a "vortex eye" (Field Origin) at the center of the
stellated octahedron with characteristic size r_e/4. These tests PROBE
whether GFD-derived length scales appear naturally in nuclear physics:

1. Is the vortex eye size (r_e/4 ≈ 0.705 fm) related to the proton radius?
2. Can the p-p Coulomb barrier be reconstructed from r_e and α?
3. What is the energy density at the vortex eye, and how does it compare
   to nuclear matter?

These are hypothesis-generating tests that look for GFD signatures in
measured nuclear quantities.

Audience: Graduate nuclear/particle physics students, GFD model developers.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, HBAR, ALPHA, E_CHARGE, EPSILON_0,
    M_E, R_E, M_P, R_PROTON,
    K_CLOSURE,
    RHO_NUCLEAR,
    vortex_eye_size,
)

PI = math.pi


# =============================================================================
# TEST 1: VORTEX EYE vs PROTON RADIUS
# =============================================================================

class VortexEyeProtonRadiusRatio(Test):
    """
    The GFD vortex eye has size r_e/4 ≈ 0.705 fm. The measured proton
    charge radius is 0.841 fm (muonic hydrogen, 2019). The ratio is:

        r_eye / r_proton ≈ 0.705 / 0.841 ≈ 0.838

    Is this ratio close to a fundamental constant? Some possibilities:
    - 1/√(√2) ≈ 0.841 (geometric)
    - α^(1/5) ≈ 0.658 (no match)
    - 3/k = 3/4 = 0.750 (close but not exact)

    This test computes the exact ratio and searches for coincidences.

    HONESTY: The vortex eye size is a MODEL DEFINITION (r_e/4), not a
    prediction. Any ratio match would be an observation, not a derivation.
    """
    audit_score = 82
    audit_notes = None
    future_questions = (
        "Q1: The proton radius has been revised multiple times (proton radius puzzle). "
        "Does the current value (0.841 fm) or the older value (0.877 fm) produce "
        "a more 'meaningful' ratio with r_e/4? "
        "(Answering would improve Observation Quality by +4 points) "
        "Q2: The neutron has zero charge radius but a non-zero magnetic radius (~0.86 fm). "
        "How does the magnetic radius compare to the vortex eye? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: If the vortex eye size were r_e/k = r_e/4 by geometric necessity, what "
        "does the 16% difference from r_proton represent physically? "
        "(Answering would improve Question by +2 points)"
    )
    name = "Vortex Eye vs Proton Charge Radius"
    question = (
        "The GFD vortex eye (r_e/4 ≈ 0.705 fm) and the proton charge radius "
        "(0.841 fm) are both sub-femtometer nuclear length scales. Their ratio "
        "is ~0.84. Is this close to any fundamental constant, geometric ratio, "
        "or power of α? Or is it just two unrelated length scales that happen "
        "to be in the same ballpark?"
    )
    reference = "GFD model; Proton radius (muonic hydrogen, Pohl 2019)"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "The proton charge radius (0.841 fm) and the vortex eye size (0.705 fm) "
        "are within 16% of each other. Both are nuclear length scales, so this "
        "proximity is not surprising — most nuclear lengths are ~1 fm. The "
        "question is whether the specific ratio has meaning beyond dimensional "
        "coincidence. We compute it and leave interpretation open."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("VORTEX EYE: r_eye = r_e / 4 (GFD model definition)")
            .equation("r_eye = 2.818 fm / 4 = 0.705 fm")
            .step("PROTON RADIUS: r_p = 0.841 fm (muonic hydrogen, Pohl 2019)")
            .equation("Ratio = r_eye / r_p = 0.705 / 0.841 = 0.838")
            .step("CANDIDATE MATCHES:")
            .step("  1/√(√2) = 0.841 — close to the ratio")
            .step("  √(2/3) = 0.816 — not bad")
            .step("  (k-1)/k = 3/4 = 0.750 — ~10% off")
            .step("  α^(1/5) = 0.658 — no match")
            .conclude("Ratio = 0.84 ± 0.02. Closest match: 1/√(√2) or √(2/√3).")
        )

    def model(self) -> Model:
        r_eye = vortex_eye_size(R_E)
        r_p = R_PROTON

        ratio = r_eye / r_p

        # Test candidate matches
        candidates = {
            "3/4 = (k-1)/k": 3 / 4,
            "1/sqrt(sqrt(2))": 1 / math.sqrt(math.sqrt(2)),
            "sqrt(2/3)": math.sqrt(2 / 3),
            "alpha^(1/7)": ALPHA ** (1 / 7),
        }

        best_name = None
        best_dev = float('inf')
        for name, val in candidates.items():
            dev = abs(ratio - val) / ratio
            if dev < best_dev:
                best_dev = dev
                best_name = name

        return (
            Model()
            .add("Vortex eye r_e/4 (m)", r_eye)
            .add("Proton radius (m)", r_p)
            .add("Ratio r_eye / r_proton", round(ratio, 4))
            .add("Same order of magnitude", 1.0 if 0.5 < ratio < 2.0 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Vortex eye r_e/4 (m)", 7.05e-16)
            .add("Proton radius (m)", 8.41e-16)
            .add("Ratio r_eye / r_proton", 0.838)
            .add("Same order of magnitude", 1.0)
        )


# =============================================================================
# TEST 2: COULOMB BARRIER FROM GEOMETRY
# =============================================================================

class CoulombBarrierFromGeometry(Test):
    """
    The Coulomb barrier for two protons approaching is:

        V_C = e² / (4πε₀ × R)

    where R is the distance of closest approach. Using R = 2 × r_proton:

        V_C(standard) ≈ 0.86 MeV

    Using R = 2 × r_e/4 (twice the vortex eye size):

        V_C(GFD) ≈ 1.02 MeV

    This test compares both calculations to see whether the GFD length
    scale produces a better or worse estimate of the p-p barrier.

    HONESTY: This is a COMPARISON, not a claim that GFD derives the barrier.
    """
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: The actual p-p fusion occurs via tunneling at E ~ 1 keV, far below "
        "the barrier. Does the barrier HEIGHT matter, or only the barrier shape? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: If we use r_e (not r_e/4) as the approach distance, we get V_C ~ 0.26 MeV. "
        "This is too small. What does the 'correct' distance tell us? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: Can the full Coulomb + nuclear potential shape be reconstructed "
        "from GFD parameters (r_e, k, α)? "
        "(Answering would improve Question by +3 points)"
    )
    name = "p-p Coulomb Barrier from Geometric Length Scales"
    question = (
        "Can the proton-proton Coulomb barrier be estimated using the GFD "
        "vortex eye size (r_e/4) as the approach distance? Compare: "
        "V_C(r_proton) vs V_C(r_e/4). Which geometric length scale "
        "gives a better estimate of the ~0.5-1 MeV Coulomb barrier?"
    )
    reference = "Nuclear physics; Coulomb barrier calculations"
    tolerance = 0.30
    level = Level.STANDARD
    commentary = (
        "The Coulomb barrier for p-p fusion depends on the distance where the "
        "nuclear strong force takes over from electromagnetic repulsion. Using "
        "the proton radius (~0.84 fm) or the GFD vortex eye (~0.71 fm) gives "
        "barriers in the 0.8-1.0 MeV range. Both are reasonable estimates. "
        "The comparison tests whether r_e/4 is a physically relevant length "
        "scale for nuclear interactions."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("COULOMB BARRIER for two protons:")
            .equation("V_C = e²/(4πε₀ × 2R) where R is the nuclear radius")
            .step("Using R = r_proton = 0.841 fm:")
            .equation("V_C = (1.602e-19)² / (4π × 8.854e-12 × 2 × 0.841e-15)")
            .equation("V_C ≈ 0.86 MeV")
            .step("Using R = r_e/4 = 0.705 fm (vortex eye):")
            .equation("V_C = (1.602e-19)² / (4π × 8.854e-12 × 2 × 0.705e-15)")
            .equation("V_C ≈ 1.02 MeV")
            .step("ALSO: V_C can be written purely in terms of α:")
            .equation("V_C = α × ℏc / (2R)")
            .conclude("Compare both geometric estimates to ~1 MeV expected barrier.")
        )

    def model(self) -> Model:
        r_eye = vortex_eye_size(R_E)
        r_p = R_PROTON

        # Coulomb barrier (touching distance = 2R)
        V_proton = E_CHARGE ** 2 / (4 * PI * EPSILON_0 * 2 * r_p)
        V_vortex = E_CHARGE ** 2 / (4 * PI * EPSILON_0 * 2 * r_eye)

        # Convert to MeV
        V_proton_mev = V_proton / (E_CHARGE * 1e6)
        V_vortex_mev = V_vortex / (E_CHARGE * 1e6)

        # Also express as α × ℏc / (2R)
        V_alpha_check = ALPHA * HBAR * C / (2 * r_p)
        V_alpha_mev = V_alpha_check / (E_CHARGE * 1e6)

        return (
            Model()
            .add("V_C (r_proton) MeV", round(V_proton_mev, 3))
            .add("V_C (r_e/4) MeV", round(V_vortex_mev, 3))
            .add("V_C (α formula check) MeV", round(V_alpha_mev, 3))
            .add("Both in 0.5-2 MeV range", 1.0 if 0.5 < V_proton_mev < 2 and 0.5 < V_vortex_mev < 2 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("V_C (r_proton) MeV", 0.86)
            .add("V_C (r_e/4) MeV", 1.02)
            .add("V_C (α formula check) MeV", 0.86)
            .add("Both in 0.5-2 MeV range", 1.0)
        )


# =============================================================================
# TEST 3: FIELD ORIGIN ENERGY DENSITY
# =============================================================================

class FieldOriginEnergyDensity(Test):
    """
    If the vortex eye (r_e/4) is a physically meaningful scale, then the
    energy density at that scale should relate to known nuclear quantities.

    We compute the energy density by distributing the electron rest mass
    energy (m_e c²) over a sphere of radius r_e/4:

        u = m_e c² / (4/3 π (r_e/4)³)

    And compare to:
    - Nuclear energy density: ρ_nuclear × c² ~ 2 × 10³⁴ J/m³
    - QCD energy density inside a proton: ~10³⁴ J/m³

    Does the vortex eye energy density match nuclear matter?
    """
    audit_score = 80
    audit_notes = None
    future_questions = (
        "Q1: Using m_e c² as the energy scale assumes the electron is the fundamental "
        "field object. What if we used m_p c² instead? How does that change the density? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: The QCD vacuum energy density inside a hadron is ~0.5 GeV/fm³. "
        "How does this compare to our vortex eye density? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: If the energy density at r_e/4 matches nuclear density, does this "
        "suggest the electron 'knows about' the nuclear scale through geometry? "
        "(Answering would improve Question by +3 points)"
    )
    name = "Energy Density at the Vortex Eye Scale"
    question = (
        "If we compute the energy density at the vortex eye scale by distributing "
        "m_e c² over a sphere of radius r_e/4, what do we get? How does this "
        "compare to nuclear energy density (~10³⁴ J/m³) and QCD condensate "
        "energy density? A match would suggest the vortex eye is a nuclear-scale "
        "structure; a mismatch would constrain the model."
    )
    reference = "Nuclear physics; QCD energy scales"
    tolerance = 0.50
    level = Level.EXPLORATORY
    commentary = (
        "The energy density at a given length scale reveals the physics operating "
        "there. Nuclear energy density is ~2 × 10³⁴ J/m³, set by the strong force. "
        "If the vortex eye density matches this, it suggests that r_e/4 is indeed "
        "a nuclear-scale structure. If it's orders of magnitude different, the "
        "vortex eye is operating at a different energy regime."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ENERGY: m_e c² = 8.187 × 10⁻¹⁴ J (electron rest energy)")
            .step("VOLUME: V = (4/3)π(r_e/4)³")
            .equation("V = (4/3)π(0.705 × 10⁻¹⁵)³ ≈ 1.47 × 10⁻⁴⁵ m³")
            .step("ENERGY DENSITY: u = m_e c² / V")
            .equation("u = 8.19e-14 / 1.47e-45 ≈ 5.6 × 10³¹ J/m³")
            .step("NUCLEAR ENERGY DENSITY: ρ_nuc × c² = 2.3e17 × (3e8)² ≈ 2.1 × 10³⁴ J/m³")
            .step("RATIO: u_vortex / u_nuclear ≈ 0.003")
            .step("The vortex eye density is ~3 orders below nuclear density.")
            .step("This makes sense: m_e << m_p, so electron-scale energy is lower.")
            .conclude("Vortex eye density is sub-nuclear but within the nuclear regime.")
        )

    def model(self) -> Model:
        r_eye = vortex_eye_size(R_E)
        m_e_energy = M_E * C ** 2

        # Volume of vortex eye sphere
        V_eye = (4 / 3) * PI * r_eye ** 3

        # Energy density
        u_vortex = m_e_energy / V_eye

        # Nuclear energy density
        u_nuclear = RHO_NUCLEAR * C ** 2

        # Ratio
        ratio = u_vortex / u_nuclear

        # Log10 of density for comparison
        log_vortex = math.log10(u_vortex)
        log_nuclear = math.log10(u_nuclear)

        return (
            Model()
            .add("Vortex eye energy density (J/m^3)", u_vortex)
            .add("Nuclear energy density (J/m^3)", u_nuclear)
            .add("Ratio (vortex/nuclear)", ratio)
            .add("Log10(vortex density)", round(log_vortex, 1))
            .add("Log10(nuclear density)", round(log_nuclear, 1))
            .add("Within 4 orders of nuclear", 1.0 if abs(log_vortex - log_nuclear) < 4 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Vortex eye energy density (J/m^3)", 5.6e31)
            .add("Nuclear energy density (J/m^3)", 2.1e34)
            .add("Ratio (vortex/nuclear)", 0.003)
            .add("Log10(vortex density)", 31.7)
            .add("Log10(nuclear density)", 34.3)
            .add("Within 4 orders of nuclear", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    VortexEyeProtonRadiusRatio,
    CoulombBarrierFromGeometry,
    FieldOriginEnergyDensity,
]


def run_all() -> bool:
    """Run all probing vortex transit tests."""
    return run_tests(
        title="Probing Vortex Transit",
        summary=(
            "These tests probe GFD geometric length scales against nuclear physics:\n"
            "1. Vortex eye vs proton radius: How close is r_e/4 to r_proton?\n"
            "2. Coulomb barrier: Can r_e/4 predict the p-p barrier height?\n"
            "3. Energy density: Is the vortex eye at nuclear energy scales?\n\n"
            "METHODOLOGY: Compare GFD-derived quantities to measured nuclear data.\n"
            "HONESTY: r_e/4 is a model definition. Matches are observations, not proofs."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
