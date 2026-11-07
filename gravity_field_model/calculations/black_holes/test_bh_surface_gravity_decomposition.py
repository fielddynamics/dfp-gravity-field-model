"""
Black Hole Surface Gravity Decomposition: The 4 and 2*pi Factors
=================================================================

The Hawking temperature of a Schwarzschild black hole is T_H = hbar*c^3 / (8*pi*G*M*k_B).
The coefficient 8*pi is not a single indivisible number. It arises as the product of two
independent physical factors: the surface gravity kappa = c^4 / (4*G*M), which contributes
the factor 4, and the Unruh thermal periodicity relation T = hbar*kappa / (2*pi*c*k_B),
which contributes the factor 2*pi. These two factors have completely different physical
origins: 4 comes from the Schwarzschild metric structure, while 2*pi comes from the
periodicity of Euclidean time required to eliminate the conical singularity at the horizon
(Gibbons and Hawking 1977).

GFM OBSERVATION: The factor 4 in kappa = c^4/(4GM) equals K (closure constant).

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    C, G, HBAR, K_B,
    M_SOLAR,
    K,
)


# =============================================================================
# DOMAIN CONSTANTS
# =============================================================================

D_SPATIAL = 3
TWO_PI = 2.0 * math.pi
N_VERTICES = 8  # 2^d = 2^3, total vertices of stellated octahedron


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _surface_gravity_schwarzschild(M: float) -> float:
    """Surface gravity kappa = c^4 / (4*G*M) for Schwarzschild BH."""
    return C**4 / (4.0 * G * M)


def _hawking_temp_from_surface_gravity(kappa: float) -> float:
    """T_H = hbar * kappa / (2*pi*c*k_B) from Unruh relation."""
    return HBAR * kappa / (TWO_PI * C * K_B)


def _hawking_temp_direct(M: float) -> float:
    """T_H = hbar*c^3 / (8*pi*G*M*k_B) direct formula."""
    return HBAR * C**3 / (8.0 * math.pi * G * M * K_B)


class SurfaceGravityDecomposition(Test):
    """
    Decompose the 8*pi coefficient in Hawking temperature into its two
    independent physical factors and check each against GFM geometry.

    PHYSICAL CONTEXT:
    Hawking (1974) showed that black holes radiate thermally at temperature
    T_H = hbar*c^3 / (8*pi*G*M*k_B). This result combines two independent
    pieces of physics. First, the Schwarzschild metric yields a surface
    gravity kappa = c^4 / (4*G*M), where the factor 4 arises because the
    event horizon sits at r = 2GM/c^2 and the metric component g_tt has a
    specific gradient there. Second, the Unruh relation T = hbar*kappa /
    (2*pi*c*k_B) converts surface gravity to temperature, where the 2*pi
    comes from the periodicity of imaginary time in the Euclidean section
    of the spacetime (Gibbons and Hawking 1977). The product 4 * 2*pi =
    8*pi reconstructs the full Hawking denominator.

    GFM OBSERVATION:
    The factor 4 in the surface gravity equals K_CLOSURE = 4, the number
    of vertices per tetrahedron and the fundamental closure constant. The
    factor 2*pi is the standard full rotation angle. Their product 8*pi
    decomposes as K * VERTICES * pi / K = VERTICES * pi, since 8 = 2^d =
    VERTICES. The decomposition reveals that the Hawking coefficient is not
    monolithic but is the product of a geometric factor (K = 4) from the
    metric structure and a topological factor (2*pi) from thermal periodicity.

    EPISTEMIC STATUS:
    This is an observation documenting numerical correspondences between
    GR coefficients and GFM structural constants. No GFM derivation of
    surface gravity or Hawking radiation exists. The correspondences may
    be coincidental.
    """

    name = "BH Surface Gravity: Decomposing 8*pi into 4 and 2*pi"

    question = (
        "The Hawking temperature denominator contains the factor 8*pi, but this "
        "is actually the product of two independent factors from different physics: "
        "4 from the Schwarzschild surface gravity and 2*pi from Euclidean thermal "
        "periodicity. The factor 4 in kappa = c^4/(4GM) equals K_CLOSURE in GFM. "
        "Is this decomposition physically meaningful, or is it a small integer "
        "coincidence? Does verifying that the two routes (direct formula vs. "
        "surface gravity composition) agree exactly strengthen the observation?"
    )

    reference = (
        "Hawking, S. (1974). Nature 248, 30; "
        "Gibbons, G.W. and Hawking, S.W. (1977). PRD 15, 2752; "
        "Unruh, W.G. (1976). PRD 14, 870; "
        "Wald, R.M. (1994). Quantum Field Theory in Curved Spacetime, Ch. 5"
    )

    tolerance = 0.001

    level = Level.STANDARD

    commentary = (
        "STANDARD PHYSICS: The surface gravity of a Schwarzschild black hole is "
        "kappa = c^4/(4GM). The 4 arises from differentiating the metric component "
        "g_tt = 1 minus 2GM/(rc^2) and evaluating at r = 2GM/c^2. The Unruh "
        "relation then converts kappa to temperature via T = hbar*kappa/(2*pi*c*k_B), "
        "where the 2*pi reflects the periodicity beta = 2*pi/kappa of Euclidean time. "
        "GFM OBSERVATION: The factor 4 equals K (closure constant, tetrahedral vertex "
        "count). The factor 8 in the combined 8*pi equals VERTICES = 2^d = 2*K. "
        "This decomposition is an observation, not a derivation. It is noted because "
        "the existing test (CharacteristicRadiiGFMSequence) already documents that "
        "the coefficient 2 in the event horizon r = 2GM/c^2 maps to TIME_FACES, and "
        "the surface gravity factor 4 arises directly from differentiating at that "
        "same horizon. The two observations are therefore structurally linked."
    )

    # Audit scoring
    audit_score = 82
    audit_notes = (
        "Question: 13/15 (good mystery framing with the decomposition angle and asks whether it is coincidence or meaningful, but could sharpen the stakes by leading with the physical puzzle before mentioning GFM). Derivation: 13/15 (strong physical scaffolding from metric to surface gravity to Unruh relation, the 4 = 2*2 explanation is a nice insight, but the three numbered layers at the end feel slightly list like rather than building to a climax). Commentary: 12/15 (solid connection back to the existing radii test and honest about observation status, but lacks an analogy for non experts and does not state broader implications beyond consistency with the {2,3,4,6} set). Model: 9/10 (clean summary with 7 values, good mix of binary verdicts and physical quantities, the log10 surface gravity adds grounding). Observations: 8/10 (values are correct and references are strong with four citations, but the log10 surface gravity observed value 12.18 is not explicitly traced to a specific source or computed inline for verification). Constants: 9/10 (all physics constants imported from common, N_VERTICES defined as module level constant with documentation, but VERTICES was imported in the original version and the switch to a hardcoded 8 loses traceability even though it fixed the runtime error). Accessibility: 11/15 (graduate students in GR will follow well, but the Euclidean time periodicity concept is introduced without intuition for undergrads, and terms like conical singularity and surface gravity could use brief plain language glosses). Header: 7/10 (module docstring covers the physics, states the GFM observation, and declares epistemic status clearly, but does not mention target audience, does not list what builds on this test or what it builds on, and lacks a limitations section separate from the epistemic status)."
    )

    academic_paper = """\
TITLE Decomposition of the Hawking Temperature Coefficient: Surface Gravity Factor 4 and Thermal Periodicity Factor 2*pi ABSTRACT The coefficient 8*pi in the Hawking temperature formula is decomposed into its two independent physical origins: the factor 4 from Schwarzschild surface gravity and the factor 2*pi from Euclidean thermal periodicity. The metric factor 4 matches the GFM closure constant K exactly. Six of seven test quantities agree at 0.00% error. This correspondence is documented as an observation. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The Hawking temperature of a Schwarzschild black hole, T_H = hbar*c^3 / (8*pi*G*M*k_B), contains the coefficient 8*pi in its denominator. This coefficient is typically treated as a single number emerging from the full derivation. It is not. The factor arises as the product of two quantities from independent domains of physics. The first factor is 4, appearing in the surface gravity kappa = c^4/(4GM). This quantity derives from the gradient of the Schwarzschild metric component g_tt = 1 minus 2GM/(rc^2), evaluated at the event horizon r_s = 2GM/c^2. The factor 4 = 2 * 2 reflects the horizon radius coefficient appearing twice in the differentiation. The second factor is 2*pi, appearing in the Unruh relation T = hbar*kappa/(2*pi*c*k_B), which converts surface gravity to temperature through the periodicity of Euclidean time required to produce a regular geometry at the horizon (Gibbons and Hawking 1977). In GFM geometry, the number 4 is the closure constant K: the vertex count of a single tetrahedron and the fundamental structural parameter from which the stellated octahedron is constructed. A companion test (CharacteristicRadiiGFMSequence) has documented that all four Schwarzschild characteristic radii carry coefficients {2, 3, 4, 6} matching {TIME_FACES, d, K, SPATIAL_FACES}. The present investigation asks whether the surface gravity factor 4 is the same K appearing in a thermodynamic context, and whether the full 8*pi decomposes into identifiable geometric components. 2. METHODOLOGY The test performs three operations. First, it verifies the algebraic decomposition: the surface gravity coefficient (4) multiplied by the thermal periodicity coefficient (2*pi) must reconstruct the Hawking denominator coefficient (8*pi). Second, it checks each factor against GFM structural numbers, specifically whether 4 = K and whether 8 = 2^d = VERTICES. Third, it computes the Hawking temperature for a solar mass black hole via both routes independently, the direct formula and the composed surface gravity path, confirming they produce identical results. Agreement is defined as 0.00% error for exact integer and algebraic correspondences, with a tolerance of 0.1% for physical quantities. 3. RESULTS The surface gravity coefficient is 4, matching K_CLOSURE = 4 exactly (0.00% error). The thermal periodicity coefficient is 2*pi = 6.283185, matching exactly (0.00% error). The combined Hawking coefficient divided by pi is 8, matching VERTICES = 2^d = 8 exactly (0.00% error). Both binary consistency checks, kappa coefficient equals K and 8 equals VERTICES, return 1.0 (true), each at 0.00% error. The ratio of T_H computed via the composed route to T_H computed via the direct formula is 1.0 exactly (0.00% error), confirming the decomposition is algebraically exact. The model computes log10 of the solar mass surface gravity as 13.18, in agreement with c^4/(4 GM_sun) from the IAU solar mass parameter. (An earlier version recorded 12.18 here, a typo.) The model value log10(kappa) = 13.18, corresponding to kappa approximately 1.5 * 10^13 m/s^2 for one solar mass, is consistent with standard references (Shapiro and Teukolsky 1983). 4. DISCUSSION All seven quantities match. The core result is exact: the Hawking coefficient 8*pi factors into a metric contribution (4 = K) and a thermal contribution (2*pi), and both routes to T_H agree identically. The identification 4 = K extends the pattern from the companion radii test, where 4 appears as the marginally bound orbit coefficient. In the surface gravity context, the same 4 emerges from differentiating the metric at the horizon whose own coefficient (2 = TIME_FACES) was already cataloged. The two observations are structurally linked: the horizon factor 2 generates the surface gravity factor 4 = 2 * 2. 5. SCOPE AND ASSUMPTIONS This test assumes a non rotating, uncharged Schwarzschild black hole. The decomposition is standard GR.
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Begin with the Schwarzschild metric.")
            .equation("ds^2 = -(1 - 2GM/(rc^2))c^2 dt^2 + (1 - 2GM/(rc^2))^(-1) dr^2 + r^2 dOmega^2")
            .step("The event horizon is at r_s = 2GM/c^2 where g_tt = 0.")
            .step("Surface gravity is defined as kappa = lim(r->r_s) of d(sqrt(-g_tt))/dr times c^2, "
                  "evaluated for a static observer.")
            .equation("kappa = c^4 / (4 * G * M)")
            .step("The factor 4 arises because: g_tt = 1 - r_s/r, so dg_tt/dr = r_s/r^2. "
                  "At r = r_s: dg_tt/dr = 1/r_s = c^2/(2GM). Then kappa = (c^2/2) * (1/r_s) * c^2/(c^2) "
                  "which simplifies to c^4/(4GM). The 4 = 2 * 2 comes from the horizon factor 2 appearing twice.")
            .step("STANDARD PHYSICS: The Unruh relation converts surface gravity to temperature.")
            .equation("T_H = hbar * kappa / (2 * pi * c * k_B)")
            .step("Substituting kappa = c^4/(4GM):")
            .equation("T_H = hbar * c^3 / (8 * pi * G * M * k_B)")
            .step("The 8*pi = 4 * 2*pi. The factor 4 is from the metric (surface gravity). "
                  "The factor 2*pi is from thermal periodicity (Euclidean time).")
            .step("GFM OBSERVATION: The decomposition reveals two layers:")
            .step("Layer 1: The metric factor 4 = K_CLOSURE. This is the same K that appears "
                  "as the closure constant throughout GFM geometry.")
            .step("Layer 2: The thermal factor 2*pi is the standard angular period. "
                  "No specific GFM correspondence is claimed for this factor.")
            .step("Layer 3: The combined factor 8 = 2^d = VERTICES = 2*K. This connects "
                  "to the existing observation that 8 = VERTICES count in the stellated octahedron.")
            .step("VERIFICATION: Compute T_H via both routes for a solar mass BH and confirm "
                  "exact agreement, validating the decomposition.")
            .conclude("The 8*pi in Hawking temperature decomposes into a metric factor (4 = K) "
                      "and a thermal periodicity factor (2*pi). The metric factor matches "
                      "the GFM closure constant. This is consistent with and extends the "
                      "existing {2, 3, 4, 6} radii observation.")
        )

    def model(self) -> Model:
        # ---- Factor decomposition ----
        # Surface gravity coefficient from Schwarzschild metric
        kappa_coefficient = 4.0

        # Thermal periodicity coefficient from Unruh relation
        thermal_coefficient = TWO_PI

        # Combined Hawking denominator coefficient
        hawking_coefficient = kappa_coefficient * thermal_coefficient

        # ---- GFM structural numbers ----
        k_closure = float(K)          # 4
        n_vertices = float(N_VERTICES)  # 8
        two_k = 2.0 * k_closure       # 8

        # ---- Consistency checks ----
        # kappa_coefficient should equal K
        kappa_matches_k = 1.0 if abs(kappa_coefficient - k_closure) < 1e-10 else 0.0

        # 8 in 8*pi should equal VERTICES = 2^d = 2*K
        eight_matches_vertices = 1.0 if abs(hawking_coefficient / math.pi - n_vertices) < 1e-10 else 0.0

        # ---- Physical verification: solar mass BH ----
        M = M_SOLAR
        kappa = _surface_gravity_schwarzschild(M)
        T_composed = _hawking_temp_from_surface_gravity(kappa)
        T_direct = _hawking_temp_direct(M)

        # Ratio should be exactly 1.0
        route_ratio = T_composed / T_direct

        # Surface gravity for solar mass (m/s^2)
        kappa_solar_log10 = math.log10(kappa)

        return (
            Model()
            .add("Surface gravity coefficient", kappa_coefficient)
            .add("Thermal periodicity coefficient", round(thermal_coefficient, 6))
            .add("Combined Hawking coefficient over pi", hawking_coefficient / math.pi)
            .add("Kappa coeff matches K_CLOSURE (binary)", kappa_matches_k)
            .add("8 matches VERTICES (binary)", eight_matches_vertices)
            .add("T composed over T direct ratio", round(route_ratio, 10))
            .add("Log10 surface gravity solar mass", round(kappa_solar_log10, 2))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Surface gravity coefficient", 4.0)
            .add("Thermal periodicity coefficient", round(TWO_PI, 6))
            .add("Combined Hawking coefficient over pi", 8.0)
            .add("Kappa coeff matches K_CLOSURE (binary)", 1.0)
            .add("8 matches VERTICES (binary)", 1.0)
            .add("T composed over T direct ratio", 1.0)
            # kappa = c^4 / (4 G M_sun), using the IAU nominal solar mass parameter
            # GM_sun = 1.3271244e20 m^3 s^-2 (independent of G and M_sun separately).
            # (The earlier value 12.18 was a typo for 13.18.)
            .add("Log10 surface gravity solar mass", round(math.log10(299792458.0**4 / (4 * 1.3271244e20)), 2))
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="BH Surface Gravity Decomposition: 4 and 2*pi",
        summary="Decomposes the 8*pi Hawking coefficient into metric factor 4=K and thermal factor 2*pi",
        test_classes=[SurfaceGravityDecomposition],
    )
