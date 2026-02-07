"""
Kerr Black Hole ISCO: Spin-Dependent Radius and GFM Geometry
=============================================================

The innermost stable circular orbit (ISCO) around a rotating (Kerr) black hole
depends on the spin parameter a (angular momentum per unit mass). For a non-rotating
Schwarzschild black hole (a=0), the ISCO radius is r_ISCO = 6GM/c^2, matching
SPATIAL_FACES=6 in GFM. As spin increases, the ISCO moves inward for prograde orbits
(corotating) and outward for retrograde orbits (counter-rotating). At maximum spin
(a=GM/c^2), prograde ISCO reaches r=GM/c^2 (coefficient 1) while retrograde ISCO
reaches r=9GM/c^2 (coefficient 9=3^2=d^2). This test probes whether the spin-dependent
ISCO coefficients track GFM geometric quantities.

GFM OBSERVATION: At a=0, coefficient 6 matches SPATIAL_FACES. At a_max retrograde,
coefficient 9 = d^2 = 3^2. The factor 9 is the square of spatial dimensions.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    G, C, M_SOLAR, K_CLOSURE, SPATIAL_FACES
)


D_SPATIAL = 3  # Spatial dimensions


def _kerr_isco_radius_coefficient(a_dimensionless: float, prograde: bool = True) -> float:
    """
    Compute ISCO radius coefficient for Kerr black hole.
    
    Args:
        a_dimensionless: Spin parameter a/(GM/c^2), dimensionless, range [0, 1]
        prograde: True for corotating orbit, False for counter-rotating
    
    Returns:
        Coefficient such that r_ISCO = coefficient * GM/c^2
    
    Reference: Bardeen, Press, Teukolsky (1972), ApJ 178, 347, Eq. 2.21
    """
    a = a_dimensionless
    
    # Z functions from BPT72
    Z1 = 1.0 + ((1.0 - a**2)**(1.0/3.0)) * ((1.0 + a)**(1.0/3.0) + (1.0 - a)**(1.0/3.0))
    Z2 = math.sqrt(3.0 * a**2 + Z1**2)
    
    if prograde:
        # Prograde (corotating): negative sign
        r_isco = 3.0 + Z2 - math.sqrt((3.0 - Z1) * (3.0 + Z1 + 2.0 * Z2))
    else:
        # Retrograde (counter-rotating): positive sign
        r_isco = 3.0 + Z2 + math.sqrt((3.0 - Z1) * (3.0 + Z1 + 2.0 * Z2))
    
    return r_isco


class KerrISCOSpinDependence(Test):
    """
    Probe the spin-dependence of Kerr black hole ISCO radius coefficients.

    PHYSICAL CONTEXT:
    The Kerr metric (1963) describes rotating black holes, characterized by mass M
    and angular momentum J = a*M (where a has dimensions of length, GM/c^2). The ISCO
    radius depends on both a and the orbit direction. Bardeen, Press, and Teukolsky
    (1972) derived the exact formula. For Schwarzschild (a=0), r_ISCO = 6GM/c^2.
    For extremal Kerr (a = GM/c^2), prograde ISCO reaches r = GM/c^2 while retrograde
    ISCO reaches r = 9GM/c^2. All astrophysical black holes rotate, making this the
    physically relevant case.

    GFM OBSERVATION:
    The Schwarzschild coefficient 6 matches SPATIAL_FACES=6. The extremal retrograde
    coefficient 9 = 3^2 = d^2, the square of spatial dimensions. The extremal prograde
    coefficient 1 has no obvious GFM interpretation yet. The pattern suggests that
    rotating black holes may probe higher powers of geometric numbers (d, d^2) while
    maintaining the static case (SPATIAL_FACES) as the spin-zero limit.

    EPISTEMIC STATUS:
    This is an OBSERVATION of numerical correspondences in coefficients derived from
    General Relativity. GFM does not derive the Kerr metric or predict these values.
    The test documents whether spin-dependent ISCO radii track GFM geometric quantities.
    """

    name = "Kerr BH ISCO: Spin-Dependent Coefficients"

    question = (
        "A Schwarzschild black hole has ISCO at r = 6GM/c^2, matching SPATIAL_FACES=6. "
        "When the black hole rotates at maximum spin, the retrograde ISCO moves to "
        "r = 9GM/c^2. Why 9? In GFM, 9 = 3^2 = d^2, the square of spatial dimensions. "
        "Does the spin-dependence of ISCO coefficients reveal a geometric pattern, "
        "where higher spin probes higher powers of d?"
    )

    reference = (
        "Bardeen, J.M., Press, W.H., Teukolsky, S.A. (1972). "
        "Rotating Black Holes: Locally Nonrotating Frames, Energy Extraction, "
        "and Scalar Synchrotron Radiation. ApJ 178, 347. Eq. 2.21."
    )

    tolerance = 0.01

    level = Level.CRITICAL

    commentary = (
        "STANDARD PHYSICS: The Kerr metric permits stable circular orbits down to "
        "the ISCO, whose radius depends on spin parameter a and orbit direction. "
        "At a=0 (Schwarzschild), coefficient is 6 for all orbits. At a=M (extremal), "
        "prograde ISCO reaches coefficient 1 (smallest possible stable orbit) while "
        "retrograde ISCO reaches coefficient 9 (largest ISCO for any Kerr solution). "
        "GFM OBSERVATION: The static case gives 6=SPATIAL_FACES. The maximal retrograde "
        "case gives 9=d^2=3^2. This suggests a pattern where spin activates higher "
        "geometric powers. The prograde coefficient 1 remains unexplained by GFM. "
        "This is an observation, not a derivation. The correspondence extends the "
        "Schwarzschild 2-3-4-6 pattern to rotating black holes, the astrophysically "
        "relevant regime. LIGO observations of black hole mergers involve spinning "
        "black holes, making this pattern experimentally accessible."
    )

    audit_score = None
    audit_notes = ""
    academic_paper = None
    contribution_score = None

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Kerr black hole with mass M, spin parameter a.")
            .step("Dimensionless spin: a_star = a / (GM/c^2), range [0, 1].")
            .step("ISCO radius from Bardeen-Press-Teukolsky (1972):")
            .equation("Z1 = 1 + (1 - a^2)^(1/3) * [(1+a)^(1/3) + (1-a)^(1/3)]")
            .equation("Z2 = sqrt(3*a^2 + Z1^2)")
            .equation("r_ISCO = [3 + Z2 +/- sqrt((3-Z1)(3+Z1+2*Z2))] * GM/c^2")
            .step("Minus sign: prograde (corotating). Plus sign: retrograde (counter-rotating).")
            .step("EVALUATE at key spin values:")
            .step("a=0 (Schwarzschild): r_ISCO = 6 GM/c^2 (both directions).")
            .step("a=M prograde: r_ISCO = 1 GM/c^2 (closest stable orbit possible).")
            .step("a=M retrograde: r_ISCO = 9 GM/c^2 (largest ISCO for any Kerr BH).")
            .step("GFM OBSERVATION:")
            .step("Coefficient 6 at a=0 matches SPATIAL_FACES = 6.")
            .step("Coefficient 9 at a=M retrograde matches d^2 = 3^2 = 9.")
            .conclude(
                "The spin-dependent ISCO coefficients at extremal values correspond to "
                "GFM geometric quantities: SPATIAL_FACES at zero spin, d^2 at maximal "
                "retrograde spin. This extends the Schwarzschild pattern to rotating "
                "black holes."
            )
        )

    def model(self) -> Model:
        # Compute ISCO coefficients at key spin values
        coeff_schwarzschild = _kerr_isco_radius_coefficient(0.0, prograde=True)
        coeff_extremal_prograde = _kerr_isco_radius_coefficient(1.0, prograde=True)
        coeff_extremal_retrograde = _kerr_isco_radius_coefficient(1.0, prograde=False)
        
        # GFM structural numbers
        n_spatial_faces = len(SPATIAL_FACES)  # 6
        d_squared = D_SPATIAL ** 2  # 9
        
        # Check correspondences
        match_schwarzschild = 1.0 if abs(coeff_schwarzschild - n_spatial_faces) < 0.01 else 0.0
        match_retrograde = 1.0 if abs(coeff_extremal_retrograde - d_squared) < 0.01 else 0.0
        
        # Physical radius for reference (M = M_solar, a=0)
        M = M_SOLAR
        GM_c2 = G * M / C**2
        r_isco_schwarzschild_meters = coeff_schwarzschild * GM_c2
        
        return (
            Model()
            .add("ISCO coefficient a=0", round(coeff_schwarzschild, 3))
            .add("ISCO coefficient a=M prograde", round(coeff_extremal_prograde, 3))
            .add("ISCO coefficient a=M retrograde", round(coeff_extremal_retrograde, 3))
            .add("Schwarzschild matches SPATIAL_FACES", match_schwarzschild)
            .add("Extremal retrograde matches d^2", match_retrograde)
            .add("ISCO radius a=0, M=M_solar (km)", round(r_isco_schwarzschild_meters / 1000.0, 1))
        )

    def observations(self) -> Observed:
        # Values from Bardeen, Press, Teukolsky (1972), exact analytic results
        return (
            Observed()
            .add("ISCO coefficient a=0", 6.0)
            .add("ISCO coefficient a=M prograde", 1.0)
            .add("ISCO coefficient a=M retrograde", 9.0)
            .add("Schwarzschild matches SPATIAL_FACES", 1.0)
            .add("Extremal retrograde matches d^2", 1.0)
            .add("ISCO radius a=0, M=M_solar (km)", 8.9)
        )


if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Kerr Black Hole ISCO Spin Dependence",
        summary="Probe whether spin-dependent ISCO radii track GFM geometric quantities (SPATIAL_FACES, d^2)",
        test_classes=[KerrISCOSpinDependence],
    )
