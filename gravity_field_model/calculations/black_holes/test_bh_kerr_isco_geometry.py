# FILENAME: test_bh_kerr_isco_geometry.py
"""
Kerr Black Hole ISCO: Spin Dependent Characteristic Radii
==========================================================

A Schwarzschild (non spinning) black hole has its innermost stable circular
orbit (ISCO) at r = 6 GM/c^2, where the coefficient 6 equals the number of
spatial faces in GFM geometry (SPATIAL_FACES = 6). For a Kerr (spinning)
black hole, the ISCO radius depends on the dimensionless spin parameter
a* = Jc/(GM^2), ranging from r = 1 GM/c^2 (extremal prograde) through
r = 6 GM/c^2 (zero spin) to r = 9 GM/c^2 (extremal retrograde). Standard
GR derives these from the Kerr metric effective potential (Bardeen, Press,
Teukolsky 1972). The question is whether the boundary coefficients {1, 6, 9}
and the intermediate structure carry geometric significance in the GFM
framework.

GFM OBSERVATION: The three ISCO boundary values {1, 6, 9} correspond to
{Field Origin count, SPATIAL_FACES, 9 = k^2 + k + 1 = (d+1)^2 + (d+1) + 1}.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    C, G, HBAR,
    M_SOLAR,
    K, VERTICES, TET_A, TET_B,
)

# =========================================================================
# DOMAIN CONSTANTS
# =========================================================================

D_SPATIAL = 3
SPATIAL_FACES_COUNT = 6
K_CLOSURE = K  # 4


# =========================================================================
# HELPER FUNCTIONS: Kerr ISCO from Bardeen, Press, Teukolsky (1972)
# =========================================================================

def _kerr_z1(a_star: float) -> float:
    """Z1 auxiliary function for Kerr ISCO. Eq. 2.21 in BPT (1972)."""
    cbrt_term = (1.0 - a_star**2)**(1.0 / 3.0)
    z1 = 1.0 + cbrt_term * (
        (1.0 + a_star)**(1.0 / 3.0) + (1.0 - a_star)**(1.0 / 3.0)
    )
    return z1


def _kerr_z2(a_star: float, z1: float) -> float:
    """Z2 auxiliary function for Kerr ISCO."""
    return math.sqrt(3.0 * a_star**2 + z1**2)


def _kerr_isco_coefficient(a_star: float, prograde: bool = True) -> float:
    """
    ISCO radius in units of GM/c^2 for Kerr BH with spin parameter a_star.

    From Bardeen, Press, Teukolsky (1972), Eq. 2.21:
    r_ISCO / (GM/c^2) = 3 + Z2 -/+ sqrt((3 - Z1)(3 + Z1 + 2*Z2))

    Minus sign for prograde orbits, plus sign for retrograde.
    Valid for 0 <= a_star <= 1.
    """
    z1 = _kerr_z1(a_star)
    z2 = _kerr_z2(a_star, z1)
    inner = math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))
    if prograde:
        return 3.0 + z2 - inner
    else:
        return 3.0 + z2 + inner


def _kerr_photon_sphere(a_star: float, prograde: bool = True) -> float:
    """
    Photon sphere radius in units of GM/c^2 for Kerr BH.

    r_ph / (GM/c^2) = 2 * (1 + cos(2/3 * arccos(-/+ a_star)))

    From Bardeen (1973). Minus for prograde, plus for retrograde.
    """
    sign = -1.0 if prograde else 1.0
    return 2.0 * (1.0 + math.cos(2.0 / 3.0 * math.acos(sign * a_star)))


def _kerr_marginally_bound(a_star: float, prograde: bool = True) -> float:
    """
    Marginally bound orbit radius in units of GM/c^2 for Kerr BH.

    r_mb / (GM/c^2) = 2 -/+ a_star + 2*sqrt(1 -/+ a_star)

    From Bardeen, Press, Teukolsky (1972).
    """
    if prograde:
        return 2.0 - a_star + 2.0 * math.sqrt(1.0 - a_star)
    else:
        return 2.0 + a_star + 2.0 * math.sqrt(1.0 + a_star)


# =========================================================================
# TEST: Kerr ISCO Spin Dependent Geometry
# =========================================================================

class KerrISCOSpinGeometry(Test):
    """
    Investigate how Schwarzschild characteristic radii change with black hole
    spin, and whether GFM structural numbers appear at special spin values.

    PHYSICAL CONTEXT:
    Bardeen, Press, and Teukolsky (1972) derived the ISCO radius for Kerr
    black holes as a function of the dimensionless spin parameter a* (0 to 1).
    The Schwarzschild limit (a*=0) gives r_ISCO = 6 GM/c^2. The extremal
    prograde limit (a*=1) gives r_ISCO = 1 GM/c^2. The extremal retrograde
    limit (a*=1) gives r_ISCO = 9 GM/c^2. At intermediate spins, the photon
    sphere and marginally bound orbit also shift continuously.

    GFM OBSERVATION:
    The three ISCO boundary coefficients are {1, 6, 9}. In GFM: 1 is the
    Field Origin (the central coupling point), 6 = SPATIAL_FACES = 2*d, and
    9 = d^2 = (k^2 + k + 1) evaluated at k = 2 or equivalently 9 = 3^2.
    Additionally, at a* = 0 the photon sphere coefficient 3 = d and the
    marginally bound coefficient 4 = k. This test checks whether these GFM
    correspondences persist, break, or transform as spin increases.

    EPISTEMIC STATUS:
    All Kerr metric results are standard GR. The correspondence with GFM
    numbers is an observation. We document where matches hold and where
    they fail, treating failures as equally informative.
    """

    name = "Kerr ISCO: Spin Dependent Characteristic Radii"

    question = (
        "In Schwarzschild spacetime, the four characteristic radii have "
        "coefficients {2, 3, 4, 6} matching GFM numbers {TIME_FACES, d, k, "
        "SPATIAL_FACES}. For a Kerr black hole, these coefficients become "
        "spin dependent. Do the extremal limits (a*=0 and a*=1) produce "
        "coefficients that map to GFM structural numbers? Specifically, does "
        "the prograde extremal ISCO at r = 1 GM/c^2 correspond to the Field "
        "Origin (1), and does the retrograde ISCO at r = 9 GM/c^2 correspond "
        "to d^2 = 9?"
    )

    reference = (
        "Bardeen, Press, Teukolsky (1972) ApJ 178, 347; "
        "Bardeen (1973) in Black Holes, eds. DeWitt & DeWitt; "
        "Shapiro & Teukolsky (1983) Black Holes, White Dwarfs, Neutron Stars"
    )

    tolerance = 0.001  # Integer coefficients from exact GR formulae

    level = Level.STANDARD

    commentary = (
        "STANDARD PHYSICS: The Kerr ISCO formula is an exact result from GR. "
        "The three boundary values {1, 6, 9} are not adjustable. At zero spin "
        "we recover {2, 3, 4, 6} for all four characteristic radii, matching "
        "the pattern documented in CharacteristicRadiiGFMSequence. "
        "GFM OBSERVATION: The prograde extremal ISCO coefficient 1 equals the "
        "Field Origin count (the single coupling point at the center of the "
        "stellated octahedron). The retrograde extremal ISCO coefficient 9 "
        "equals d^2, the square of spatial dimensions. The zero spin ISCO "
        "coefficient 6 equals SPATIAL_FACES. These three values {1, 6, 9} "
        "form the sequence {1, 2d, d^2} which factors as {1, d}^2 in a "
        "polynomial sense: (1 + d)^2 = 1 + 2d + d^2 = 16 = k^2, though the "
        "middle term 2d = 6 appears at a* = 0 rather than at an intermediate "
        "spin. This is an observation, not a derivation. The intermediate spin "
        "values do not obviously correspond to GFM integers, which limits the "
        "strength of the pattern."
    )

    # Audit scoring
    audit_score = 83
    audit_notes = (
        "Question: 13/15 (strong mystery hook connecting Schwarzschild pattern to spin dependence, asks specific numbers, but could sharpen the stakes by emphasizing what a failure would mean for the {2,3,4,6} observation). Derivation: 13/15 (good physical setup with Kerr metric context, clear progression from BPT equations to boundary evaluations, but jumps from listing equations to GFM observation without building intuition for WHY the coefficients take those values in GR, the Z1/Z2 machinery feels like a recipe). Commentary: 12/15 (delivers the {1, 2d, d^2} polynomial insight which is genuinely interesting, honest about intermediate spins not matching, but the (1+d)^2 = k^2 connection feels strained and the commentary lacks an analogy or implication for what this means physically). Model: 8/10 (13 outputs is slightly heavy but well organized into three spin regimes plus four binary verdicts, the binary match flags are good practice, could consolidate by dropping redundant individual coefficients already tested in the parent file). Observations: 9/10 (all values from exact GR with BPT 1972 and Bardeen 1973 explicitly cited, the 5.828427 value for retrograde marginally bound is correct as 3 + 2*sqrt(2), minor gap: no explicit equation number citation for the photon sphere formula). Constants: 8/10 (G, C, HBAR, M_SOLAR imported from common but C, HBAR, M_SOLAR are never used in the test body, K and VERTICES properly imported, SPATIAL_FACES_COUNT and D_SPATIAL are hardcoded as module level constants rather than imported from geometry_constants). Accessibility: 12/15 (graduate level reader follows well, good explanation of what a* means and what prograde vs retrograde means, but the Z1/Z2 auxiliary functions are presented without intuition for what they represent physically, an undergrad would lose the thread at that point). Header: 8/10 (module docstring is thorough with physical context and honest epistemic framing, clearly states observation not derivation, includes GFM pattern, but does not state target audience level or explicitly list what is verified vs speculative in a structured way)."
    )

    academic_paper = """\
TITLE Kerr Black Hole ISCO Coefficients and GFM Structural Numbers: Spin Dependent Correspondence ABSTRACT We investigate whether GFM structural numbers appear in the characteristic radii of spinning (Kerr) black holes. The Schwarzschild {2, 3, 4, 6} pattern extends to extremal spin limits where ISCO coefficients {1, 6, 9} correspond to {Field Origin, SPATIAL_FACES, d^2}. This is documented as an OBSERVATION. 1. INTRODUCTION: THE SCIENTIFIC QUESTION A prior test in this series established that the four Schwarzschild characteristic radii have coefficients {2, 3, 4, 6} matching the GFM structural numbers {TIME_FACES, d, k, SPATIAL_FACES}. That observation, while striking, applies only to non spinning black holes. Real astrophysical black holes possess significant angular momentum. The natural follow up question is: does the pattern survive when spin is introduced? For a Kerr black hole with dimensionless spin parameter a* = Jc/(GM^2), the ISCO radius varies continuously. Bardeen, Press, and Teukolsky (1972) derived the exact formula, yielding three boundary values: r_ISCO = 6 GM/c^2 at a* = 0, r_ISCO = 1 GM/c^2 for extremal prograde orbits, and r_ISCO = 9 GM/c^2 for extremal retrograde orbits. The photon sphere and marginally bound orbit shift similarly. GFM observes that these boundary coefficients {1, 6, 9} correspond to structural numbers: 1 is the Field Origin (the central coupling point of the stellated octahedron), 6 is SPATIAL_FACES, and 9 equals d^2 where d = 3. This test systematically evaluates all nine characteristic radius coefficients across three spin regimes. 2. METHODOLOGY We implement the exact Bardeen, Press, Teukolsky (1972) formulae for ISCO, photon sphere, and marginally bound orbit radii as functions of spin parameter a*. We evaluate at three points: a* = 0 (Schwarzschild), a* = 1 prograde and a* = 1 retrograde. The formulas are finite at a* = 1. (A near-extremal value such as 0.999999 does not recover the prograde limit to six decimals: the ISCO approaches 1 as (1 - a*)^(1/3) and is still 1.016 there.) Each computed coefficient is compared against GR exact values from BPT (1972) and Bardeen (1973). Four binary match tests check whether specific coefficients equal GFM numbers: ISCO at a* = 0 versus SPATIAL_FACES (6), prograde extremal ISCO versus Field Origin (1), retrograde extremal ISCO versus d^2 (9), and retrograde photon sphere versus k (4). Agreement threshold is 0.1%. 3. RESULTS At zero spin, the model reproduces the known Schwarzschild values: ISCO = 6.000000, photon sphere = 3.000000, marginally bound = 4.000000. These match {SPATIAL_FACES, d, k} exactly, consistent with the parent test. At prograde extremal spin, all three radii collapse toward 1.000000. The ISCO, photon sphere, and marginally bound orbit all converge to the event horizon at r = 1 GM/c^2. This coalescence at the Field Origin value (1) is noted. At retrograde extremal spin, the radii disperse: ISCO = 9.000000, photon sphere = 4.000000, marginally bound = 5.828427. The ISCO coefficient 9 = d^2 and the photon sphere coefficient 4 = k are both GFM structural numbers. The marginally bound value 3 + 2*sqrt(2) is irrational and does not correspond to any GFM integer. All four binary match tests return 1.0, confirming the correspondences hold. 4. DISCUSSION The results reveal an asymmetric pattern. Prograde spin collapses all characteristic radii to 1 (Field Origin), while retrograde spin expands the ISCO to 9 = d^2 and recovers k = 4 for the photon sphere. The three ISCO boundary values {1, 6, 9} form the sequence {1, 2d, d^2}. We observe that 1 + 2d + d^2 = (1 + d)^2 = 16 = k^2, though this algebraic relationship does not map directly onto the spin parameterization. EPISTEMIC STATUS: OBSERVATION. Standard GR derives all these coefficients from the Kerr metric effective potential. GFM does not derive the Kerr solution. We note that the boundary coefficients happen to equal GFM structural numbers. The marginally bound retrograde orbit (5.828427) breaks the pattern, providing an honest boundary on where the correspondence holds. 5. LIMITATIONS AND HONESTY STATEMENT This is not a derivation of Kerr geometry from GFM principles. Intermediate spin values produce non integer coefficients with no obvious GFM correspondence. The pattern is restricted to extremal limits. Small integer bias may inflate the apparent significance, as integers 1 through 9 inevitably overlap with some GFM constants. 6. CONCLUSION We document that Kerr black hole ISCO boundary coefficients {1, 6, 9} correspond to GFM
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD PHYSICS: The Kerr metric describes spacetime around "
                "a rotating black hole with mass M and angular momentum J. "
                "The dimensionless spin parameter is a* = Jc/(GM^2), ranging "
                "from 0 (Schwarzschild) to 1 (extremal Kerr)."
            )
            .step(
                "The ISCO radius for a Kerr BH is given by the Bardeen, Press, "
                "Teukolsky (1972) formula involving auxiliary functions Z1 and Z2."
            )
            .equation(
                "Z1 = 1 + (1 - a*^2)^(1/3) * [(1+a*)^(1/3) + (1-a*)^(1/3)]"
            )
            .equation(
                "Z2 = sqrt(3*a*^2 + Z1^2)"
            )
            .equation(
                "r_ISCO/(GM/c^2) = 3 + Z2 -/+ sqrt((3-Z1)(3+Z1+2*Z2))"
            )
            .step(
                "Evaluating at three boundary spins:"
            )
            .equation(
                "a* = 0 (Schwarzschild): r_ISCO = 6 GM/c^2"
            )
            .equation(
                "a* = 1 (prograde extremal): r_ISCO = 1 GM/c^2"
            )
            .equation(
                "a* = 1 (retrograde extremal): r_ISCO = 9 GM/c^2"
            )
            .step(
                "Similarly, the photon sphere shifts from 3 (a*=0) to 1 "
                "(prograde, a*=1) to 4 (retrograde, a*=1). The marginally "
                "bound orbit shifts from 4 (a*=0) to 1 (prograde, a*=1) "
                "to 3 + 2*sqrt(2) ~ 5.828 (retrograde, a*=1)."
            )
            .step(
                "GFM OBSERVATION: At zero spin, {2, 3, 4, 6} maps to "
                "{TIME_FACES, d, k, SPATIAL_FACES}. At extremal prograde "
                "spin, three radii collapse to coefficient 1 (the event "
                "horizon remains at 1, photon sphere at 1, marginally bound "
                "at 1, ISCO at 1). This coalescence at the Field Origin "
                "value is noted."
            )
            .step(
                "At extremal retrograde spin, the ISCO reaches 9 = d^2 and "
                "the photon sphere reaches 4 = k. The retrograde photon "
                "sphere recovering the closure constant k is a secondary "
                "observation."
            )
            .conclude(
                "The Kerr ISCO boundary coefficients {1, 6, 9} and the "
                "retrograde photon sphere value 4 all correspond to GFM "
                "structural numbers. The prograde coalescence at 1 and "
                "the retrograde dispersal to {~5.83, 4, 9} partially "
                "preserve the GFM pattern. Intermediate spins do not show "
                "obvious GFM correspondences."
            )
        )

    def model(self) -> Model:
        # Schwarzschild limit (a* = 0)
        isco_a0 = _kerr_isco_coefficient(0.0, prograde=True)
        photon_a0 = _kerr_photon_sphere(0.0, prograde=True)
        mb_a0 = _kerr_marginally_bound(0.0, prograde=True)

        # Extremal prograde (a* = 1)
        # Use a* = 0.999999 to avoid numerical edge issues
        a_ext = 1.0  # The formulas are finite at a* = 1. At 0.999999 the prograde ISCO is
        # still 1.016, because it approaches 1 as (1 - a*)^(1/3).
        isco_pro = _kerr_isco_coefficient(a_ext, prograde=True)
        photon_pro = _kerr_photon_sphere(a_ext, prograde=True)
        mb_pro = _kerr_marginally_bound(a_ext, prograde=True)

        # Extremal retrograde (a* = 1)
        isco_retro = _kerr_isco_coefficient(a_ext, prograde=False)
        photon_retro = _kerr_photon_sphere(a_ext, prograde=False)
        mb_retro = _kerr_marginally_bound(a_ext, prograde=False)

        # GFM structural numbers for comparison
        field_origin_count = 1.0
        d_spatial = 3.0
        k_closure = float(K_CLOSURE)
        spatial_faces = float(SPATIAL_FACES_COUNT)
        d_squared = d_spatial ** 2

        # Check key correspondences
        match_isco_a0 = 1.0 if abs(isco_a0 - spatial_faces) < 0.01 else 0.0
        match_isco_pro = 1.0 if abs(isco_pro - field_origin_count) < 0.01 else 0.0
        match_isco_retro = 1.0 if abs(isco_retro - d_squared) < 0.01 else 0.0
        match_photon_retro = 1.0 if abs(photon_retro - k_closure) < 0.01 else 0.0

        return (
            Model()
            .add("ISCO coeff at a*=0", round(isco_a0, 6))
            .add("Photon sphere coeff at a*=0", round(photon_a0, 6))
            .add("Marg bound coeff at a*=0", round(mb_a0, 6))
            .add("ISCO coeff prograde extremal", round(isco_pro, 6))
            .add("Photon sphere coeff prograde extremal", round(photon_pro, 6))
            .add("Marg bound coeff prograde extremal", round(mb_pro, 6))
            .add("ISCO coeff retrograde extremal", round(isco_retro, 6))
            .add("Photon sphere coeff retrograde extremal", round(photon_retro, 6))
            .add("Marg bound coeff retrograde extremal", round(mb_retro, 6))
            .add("ISCO a*=0 matches SPATIAL_FACES", match_isco_a0)
            .add("ISCO prograde matches Field Origin", match_isco_pro)
            .add("ISCO retrograde matches d^2", match_isco_retro)
            .add("Photon retro matches k", match_photon_retro)
        )

    def observations(self) -> Observed:
        # All values from exact Kerr GR: BPT (1972), Bardeen (1973)
        return (
            Observed()
            .add("ISCO coeff at a*=0", 6.0)
            .add("Photon sphere coeff at a*=0", 3.0)
            .add("Marg bound coeff at a*=0", 4.0)
            .add("ISCO coeff prograde extremal", 1.0)
            .add("Photon sphere coeff prograde extremal", 1.0)
            .add("Marg bound coeff prograde extremal", 1.0)
            .add("ISCO coeff retrograde extremal", 9.0)
            .add("Photon sphere coeff retrograde extremal", 4.0)
            .add("Marg bound coeff retrograde extremal", 5.828427)
            .add("ISCO a*=0 matches SPATIAL_FACES", 1.0)
            .add("ISCO prograde matches Field Origin", 1.0)
            .add("ISCO retrograde matches d^2", 1.0)
            .add("Photon retro matches k", 1.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Kerr ISCO: Spin Dependent Characteristic Radii",
        summary="Probes whether GFM structural numbers appear in Kerr BH radii at extremal spins",
        test_classes=[KerrISCOSpinGeometry],
    )
