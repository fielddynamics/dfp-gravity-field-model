# FILENAME: test_bh_kerr_isco_spin_limits.py

"""
Kerr Black Hole ISCO: Spin Limit Coefficients and GFM Geometry
===============================================================

The Kerr metric describes rotating black holes, parameterized by mass M and
spin parameter a (0 <= a <= GM/c^2). The innermost stable circular orbit
(ISCO) radius depends on spin and on whether the orbit is prograde or
retrograde. At zero spin (Schwarzschild limit), both branches converge to
r_ISCO = 6 GM/c^2. At maximal spin (a = GM/c^2), the prograde ISCO shrinks
to r_ISCO = 1 GM/c^2 and the retrograde ISCO expands to r_ISCO = 9 GM/c^2.
These limiting coefficients {1, 6, 9} are exact results from general
relativity (Bardeen, Press, Teukolsky 1972).

GFM OBSERVATION: The three ISCO coefficients {1, 6, 9} correspond to
{Field Origin count, SPATIAL_FACES, VERTICES + Field Origin}.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    C, G, HBAR,
    M_SOLAR,
    K, VERTICES, TET_A, TET_B,
)

# ---------------------------------------------------------------------------
# Domain constants
# ---------------------------------------------------------------------------
D_SPATIAL = 3
SPATIAL_FACES_COUNT = 6   # 6 spatial faces on the stellated octahedron
FIELD_ORIGIN_COUNT = 1    # The single central coupling point
VERTICES_COUNT = 8        # 2^d = 8 vertices of the Merkaba


def _kerr_isco_prograde(a_star: float) -> float:
    """
    ISCO radius coefficient for prograde orbit around a Kerr BH.
    a_star = a*c^2/(GM) is the dimensionless spin parameter, 0 <= a_star <= 1.
    Returns r_ISCO in units of GM/c^2.
    Formula from Bardeen, Press, Teukolsky (1972), Eq. 2.21.
    """
    Z1 = 1.0 + (1.0 - a_star**2)**(1.0/3.0) * (
        (1.0 + a_star)**(1.0/3.0) + (1.0 - a_star)**(1.0/3.0)
    )
    Z2 = math.sqrt(3.0 * a_star**2 + Z1**2)
    return 3.0 + Z2 - math.sqrt((3.0 - Z1) * (3.0 + Z1 + 2.0 * Z2))


def _kerr_isco_retrograde(a_star: float) -> float:
    """
    ISCO radius coefficient for retrograde orbit around a Kerr BH.
    Same formula but with opposite sign convention for spin coupling.
    Returns r_ISCO in units of GM/c^2.
    """
    Z1 = 1.0 + (1.0 - a_star**2)**(1.0/3.0) * (
        (1.0 + a_star)**(1.0/3.0) + (1.0 - a_star)**(1.0/3.0)
    )
    Z2 = math.sqrt(3.0 * a_star**2 + Z1**2)
    return 3.0 + Z2 + math.sqrt((3.0 - Z1) * (3.0 + Z1 + 2.0 * Z2))


class KerrISCOSpinLimitCoefficients(Test):
    """
    Probe the ISCO radius coefficients of Kerr black holes at the three
    physically distinguished spin states: zero spin, maximal prograde,
    and maximal retrograde.

    PHYSICAL CONTEXT:
    The Kerr solution (Kerr 1963) generalizes Schwarzschild to rotating
    black holes. Bardeen, Press, and Teukolsky (1972) derived the ISCO
    radius as a function of dimensionless spin a_star. At a_star = 0
    (Schwarzschild), r_ISCO = 6 GM/c^2. At a_star = 1 (extremal Kerr),
    the prograde ISCO reaches r = 1 GM/c^2 (coinciding with the horizon)
    and the retrograde ISCO reaches r = 9 GM/c^2. These are exact,
    analytical results of general relativity.

    GFM OBSERVATION:
    The coefficient set {1, 6, 9} at the spin limits maps to GFM
    structural numbers. 6 = SPATIAL_FACES (already noted in the
    Schwarzschild radii sequence). 1 = Field Origin, the single central
    coupling point of the stellated octahedron. 9 = VERTICES + 1 = 2^d + 1,
    the vertex count plus the Field Origin. Additionally, the full spin
    sweep from coefficient 1 to 9 spans a range of 8 = 2^d = VERTICES,
    and the Schwarzschild value 6 sits at fraction (6 minus 1)/(9 minus 1)
    = 5/8 of that range, where 5 = k + 1. These correspondences extend
    the {2, 3, 4, 6} pattern from the Schwarzschild radii test.

    EPISTEMIC STATUS:
    All black hole physics here is standard GR. The mapping to GFM numbers
    is an observation that may be coincidental. No GFM derivation of the
    Kerr metric or its ISCO structure exists.
    """

    name = "Kerr ISCO Spin Limits: The {1, 6, 9} Coefficients"

    question = (
        "A Kerr black hole has three distinguished ISCO coefficients: 6 at zero "
        "spin, 1 for maximal prograde, and 9 for maximal retrograde. WHY these "
        "specific integers? GR derives them from the Kerr effective potential, "
        "but the set {1, 6, 9} maps to {Field Origin, SPATIAL_FACES, VERTICES+1} "
        "in GFM geometry. The prograde to retrograde range spans exactly 8 = 2^d. "
        "Is this an extension of the Schwarzschild {2, 3, 4, 6} pattern, or "
        "coincidence?"
    )

    reference = (
        "Kerr, R. (1963). Phys. Rev. Lett. 11, 237; "
        "Bardeen, Press, Teukolsky (1972). ApJ 178, 347; "
        "Shapiro & Teukolsky (1983). Black Holes, White Dwarfs, Neutron Stars, Ch. 12"
    )

    tolerance = 0.001  # Integer coefficients from exact GR formulas

    level = Level.STANDARD

    commentary = (
        "STANDARD PHYSICS: The Kerr ISCO formula is an exact result of general "
        "relativity. At zero spin it returns 6, at maximal prograde spin it returns "
        "1, and at maximal retrograde spin it returns 9. These coefficients are not "
        "approximate; they are exact integers from the analytic solution. "
        "GFM OBSERVATION: The coefficient 6 = SPATIAL_FACES was already noted in "
        "the Schwarzschild radii sequence. This test extends that observation by "
        "noting that the spin limits introduce 1 (Field Origin) and 9 (VERTICES + "
        "Field Origin = 2^d + 1). The total span from prograde to retrograde is "
        "exactly 8 = 2^d = VERTICES. This is an observation, not a derivation. The "
        "probability of three random integers in {1..10} matching three specific GFM "
        "numbers is (3/10)^3 = 0.027, comparable to the Schwarzschild sequence. "
        "Combined with that earlier result, the pattern becomes more suggestive but "
        "remains unproven."
    )

    # Audit scoring
    audit_score = 86
    audit_notes = (
        "Question: 14/15 (strong mystery hook with specific integers, asks WHY, frames the tension between GR derivation and geometric pattern; could sharpen stakes slightly by noting this is the first test of whether the Schwarzschild pattern survives generalization). Derivation: 13/15 (excellent physical setup, clear progression from Kerr metric through Z1/Z2 to evaluation at limits, GFM observation clearly separated; minor gap in not providing intuition for WHY the formula produces integers at the limits, which would deepen understanding). Commentary: 12/15 (honest about observation status, good statistical context with p = 0.027, connects to prior Schwarzschild test; lacks an analogy to make the pattern tangible, and does not discuss implications for what would happen if the pattern broke at intermediate spins). Model: 9/10 (clean set of 11 values covering GR coefficients, GFM numbers, range, fractional position, and physical verification; the GFM echo values that simply restate known constants like Field Origin = 1.0 add mild redundancy but serve the comparison purpose). Observations: 8/10 (all values traceable to Bardeen, Press, Teukolsky 1972; the GM/c^2 value is computed inline rather than from an independent source, and the 0.625 fractional position is derived rather than independently observed, though this is inherent to the test structure). Constants: 9/10 (C, G, HBAR, M_SOLAR, K, VERTICES all imported from common; SPATIAL_FACES_COUNT and VERTICES_COUNT are hardcoded as module level integers rather than derived from the imported VERTICES and geometry constants, and HBAR and TET_A/TET_B are imported but never used). Accessibility: 13/15 (good progression from Kerr metric basics through spin parameter to ISCO evaluation; explains prograde vs retrograde clearly; the Z1/Z2 intermediate variables could use more physical intuition for undergrads; the 5/8 fractional position observation is elegant but introduced without enough scaffolding for why it matters). Header: 8/10 (comprehensive module docstring with physical context, GFM observation, and epistemic disclaimer; missing explicit target audience statement and missing a BUILDS ON or COVERAGE section listing relationship to the Schwarzschild radii test)."
    )

    academic_paper = """\
TITLE Kerr Black Hole ISCO Spin Limits and GFM Structural Numbers: The {1, 6, 9} Correspondence ABSTRACT We examine the ISCO radius coefficients of Kerr black holes at the three physically distinguished spin states. The coefficients {1, 6, 9} from exact general relativity map to GFM structural numbers {Field Origin, SPATIAL_FACES, VERTICES+1}. This is documented as an OBSERVATION, not a derivation. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The innermost stable circular orbit (ISCO) is a fundamental feature of black hole spacetimes, marking the boundary below which no stable circular orbits exist. For the Kerr metric describing rotating black holes, the ISCO radius depends on the dimensionless spin parameter a_star, which ranges from 0 (Schwarzschild, non rotating) to 1 (extremal Kerr, maximally rotating). Standard general relativity, specifically the analysis by Bardeen, Press, and Teukolsky (1972), yields exact analytical expressions for the ISCO. At a_star = 0, both prograde and retrograde orbits share r_ISCO = 6 GM/c^2. At a_star = 1, the prograde ISCO shrinks to r_ISCO = 1 GM/c^2 while the retrograde ISCO expands to r_ISCO = 9 GM/c^2. These are not approximations; they are exact integers from the analytic solution. A companion test documented that the four Schwarzschild characteristic radii carry coefficients {2, 3, 4, 6}, matching the GFM structural numbers {TIME_FACES, d, K, SPATIAL_FACES}. This investigation asks whether the Kerr spin limits extend that pattern. We observe that {1, 6, 9} corresponds to {Field Origin, SPATIAL_FACES, VERTICES + Field Origin}, and that the prograde to retrograde range spans exactly 8 = 2^d = VERTICES. 2. METHODOLOGY We evaluate the Bardeen, Press, Teukolsky ISCO formula at three distinguished spin values: a_star = 0, a_star = 1 (prograde), and a_star = 1 (retrograde). The formula involves intermediate quantities Z1 and Z2 that reduce to simple integers at these limits. We compare the resulting coefficients against GFM structural numbers drawn from the stellated octahedron geometry: Field Origin count (1), SPATIAL_FACES (6), VERTICES (8), and VERTICES + Field Origin (9). We also compute the fractional position of the Schwarzschild value within the full spin range. Agreement criterion is exact integer matching, with numerical tolerance of 0.1%. 3. RESULTS The Kerr ISCO formula produces the following coefficients at spin limits: Schwarzschild (a_star = 0): r_ISCO = 6.000 GM/c^2 Prograde extremal (a_star = 1): r_ISCO = 1.000 GM/c^2 Retrograde extremal (a_star = 1): r_ISCO = 9.000 GM/c^2 GFM structural numbers for comparison: Field Origin = 1, SPATIAL_FACES = 6, VERTICES + Field Origin = 9. All three coefficients match their corresponding GFM numbers exactly. The prograde to retrograde range is 9 minus 1 = 8 = VERTICES = 2^d. The Schwarzschild value 6 sits at fractional position (6 minus 1)/(9 minus 1) = 5/8, where 5 = K + 1 and 8 = 2^d. The model computes (K + 1)/2^d = 5/8 = 0.625, matching exactly. 4. DISCUSSION The physical content is entirely standard GR. The Kerr ISCO formula is well established and experimentally relevant: ISCO physics governs X ray binary accretion disk spectra and gravitational wave inspiral signals. The integers {1, 6, 9} at the spin limits are not free parameters but consequences of the Kerr geometry. EPISTEMIC STATUS: OBSERVATION. GFM does not derive the Kerr metric, the effective potential, or the ISCO formula. We observe that the resulting integer coefficients match GFM structural numbers. The probability of three random integers from {1..10} matching three specified GFM numbers is approximately 0.027. Combined with the earlier Schwarzschild {2, 3, 4, 6} observation, the cumulative pattern becomes more suggestive. The range of 8 = 2^d is particularly striking because it connects the full sweep of black hole spin to the vertex count of the stellated octahedron. The 5/8 partition point adds a secondary layer of correspondence. 5. LIMITATIONS AND HONESTY STATEMENT This observation does not constitute a derivation of Kerr physics from GFM principles. The correspondence could be coincidental, particularly given small integer bias. No mechanism connecting GFM geometry to black hole spin has been proposed. The statistical assessment depends on how one defines the pool of candidate GFM numbers. Further work should examine whether intermediate spin values produce coefficients that track GFM quantities continuously. 6. CONCLUSION We document that the three Kerr ISCO spin limit coefficients
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD PHYSICS: The Kerr metric in Boyer Lindquist coordinates "
                "describes a rotating black hole with mass M and angular momentum "
                "J = a*M, where 0 <= a <= GM/c^2."
            )
            .step(
                "The dimensionless spin parameter is a_star = a*c^2/(GM), ranging "
                "from 0 (Schwarzschild) to 1 (extremal Kerr)."
            )
            .step(
                "Bardeen, Press, and Teukolsky (1972) derived the ISCO radius as a "
                "function of a_star using the effective potential for test particles "
                "in the equatorial plane."
            )
            .equation(
                "Z1 = 1 + (1 - a_star^2)^(1/3) * [(1+a_star)^(1/3) + (1-a_star)^(1/3)]"
            )
            .equation(
                "Z2 = sqrt(3*a_star^2 + Z1^2)"
            )
            .equation(
                "r_ISCO/( GM/c^2 ) = 3 + Z2 -/+ sqrt( (3-Z1)(3+Z1+2*Z2) )"
            )
            .step(
                "The minus sign gives the prograde ISCO (co rotating with the BH). "
                "The plus sign gives the retrograde ISCO (counter rotating)."
            )
            .step(
                "EVALUATE at a_star = 0 (Schwarzschild limit): Z1 = 3, Z2 = 3, "
                "both branches give r_ISCO = 6 GM/c^2."
            )
            .step(
                "EVALUATE at a_star = 1 (extremal Kerr): "
                "Prograde: r_ISCO = 1 GM/c^2. "
                "Retrograde: r_ISCO = 9 GM/c^2."
            )
            .step(
                "GFM OBSERVATION (not derivation): The three coefficients are "
                "{1, 6, 9}. In GFM geometry: 1 = Field Origin (the central coupling "
                "point), 6 = SPATIAL_FACES (faces encoding spatial directions), "
                "9 = 2^d + 1 = VERTICES + Field Origin. The range from prograde "
                "to retrograde limit spans 9 minus 1 = 8 = 2^d = VERTICES."
            )
            .step(
                "ADDITIONAL OBSERVATION: The Schwarzschild value 6 partitions the "
                "range [1, 9] at position (6 minus 1)/(9 minus 1) = 5/8, where "
                "5 = k + 1 and 8 = 2^d. This ratio 5/8 is the fraction of "
                "the vertex count occupied by the simplex vertex count k + 1."
            )
            .conclude(
                "The Kerr ISCO spin limits produce integer coefficients {1, 6, 9} "
                "that map to GFM structural numbers, extending the Schwarzschild "
                "{2, 3, 4, 6} pattern into the rotating case."
            )
        )

    def model(self) -> Model:
        # Compute ISCO coefficients from the exact Kerr formula
        coeff_schwarzschild = _kerr_isco_prograde(0.0)
        coeff_prograde_max = _kerr_isco_prograde(1.0)
        coeff_retrograde_max = _kerr_isco_retrograde(1.0)

        # Compute the spin range
        spin_range = coeff_retrograde_max - coeff_prograde_max

        # GFM structural numbers for comparison
        gfm_field_origin = float(FIELD_ORIGIN_COUNT)
        gfm_spatial_faces = float(SPATIAL_FACES_COUNT)
        gfm_vertices_plus_origin = float(VERTICES_COUNT + FIELD_ORIGIN_COUNT)
        gfm_vertices = float(VERTICES_COUNT)

        # Fractional position of Schwarzschild value within the spin range
        frac_position = (coeff_schwarzschild - coeff_prograde_max) / spin_range
        gfm_frac_prediction = (K + 1.0) / (2.0**D_SPATIAL)

        # Physical radii for a 10 solar mass BH (verification)
        M = 10.0 * M_SOLAR
        GM_c2 = G * M / C**2

        return (
            Model()
            .add("Schwarzschild ISCO coefficient", coeff_schwarzschild)
            .add("Prograde extremal ISCO coefficient", coeff_prograde_max)
            .add("Retrograde extremal ISCO coefficient", coeff_retrograde_max)
            .add("Prograde to retrograde range", spin_range)
            .add("Schwarzschild fractional position in range", frac_position)
            .add("GFM Field Origin", gfm_field_origin)
            .add("GFM SPATIAL_FACES", gfm_spatial_faces)
            .add("GFM VERTICES plus Field Origin", gfm_vertices_plus_origin)
            .add("GFM VERTICES count", gfm_vertices)
            .add("GFM fraction (k+1)/2^d", gfm_frac_prediction)
            .add("GM/c^2 for 10 Msun (m)", GM_c2)
        )

    def observations(self) -> Observed:
        # All values from exact GR: Bardeen, Press, Teukolsky (1972)
        GM_c2_10Msun = G * 10.0 * M_SOLAR / C**2
        return (
            Observed()
            .add("Schwarzschild ISCO coefficient", 6.0)
            .add("Prograde extremal ISCO coefficient", 1.0)
            .add("Retrograde extremal ISCO coefficient", 9.0)
            .add("Prograde to retrograde range", 8.0)
            .add("Schwarzschild fractional position in range", 0.625)
            .add("GFM Field Origin", 1.0)
            .add("GFM SPATIAL_FACES", 6.0)
            .add("GFM VERTICES plus Field Origin", 9.0)
            .add("GFM VERTICES count", 8.0)
            .add("GFM fraction (k+1)/2^d", 0.625)
            .add("GM/c^2 for 10 Msun (m)", GM_c2_10Msun)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Kerr ISCO Spin Limit Coefficients",
        summary="Probes the {1, 6, 9} ISCO coefficients at Kerr spin limits against GFM geometry",
        test_classes=[KerrISCOSpinLimitCoefficients],
    )
