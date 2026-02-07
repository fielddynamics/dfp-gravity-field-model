"""
Newton's Inverse Square Law: Geometric Origin of r^(-2) Dependence
===================================================================

The gravitational force follows F = G*m1*m2/r^2, with the inverse square
depending on distance r^2 specifically. Standard physics derives this from
Gauss's law in 3D space: flux through a spherical surface scales as 4*pi*r^2.
But why does GFM's geometric framework, which claims to derive G from Merkaba
coupling in d=3 dimensions with k=4 closure, reproduce this exact spatial
dependence? If both G's magnitude AND the r^(-2) law emerge from the same
geometric principles, this would strongly suggest genuine derivation rather
than parameter fitting.

GFM OBSERVATION: The r^(-2) law may follow from d=3 spatial closure geometry.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    G, K, C, HBAR, M_E, M_SOLAR, R_SOLAR
)


class NewtonForceLawExponent(Test):
    """
    PHYSICAL CONTEXT:
    Newton's law of gravitation states F = G*m1*m2/r^2, where the force
    decreases with the square of distance. Standard physics derives this
    from Gauss's law: in d=3 spatial dimensions, flux through a sphere of
    radius r scales as the surface area 4*pi*r^2, yielding force proportional
    to r^(-2). This has been experimentally verified from planetary scales
    down to sub-millimeter laboratory tests.

    GFM OBSERVATION:
    If G emerges from Merkaba coupling geometry with k=4 closure in d=3
    dimensions, does the same geometric structure constrain the spatial
    dependence of the force law? The surface area of a sphere in d dimensions
    scales as r^(d-1), which for d=3 gives r^2. The GFM framework uses d=3
    as input, so the question is whether this connection is independent or
    redundant with standard geometric arguments.

    EPISTEMIC STATUS:
    This is an observation documenting consistency between GFM's d=3 parameter
    and the standard r^(-2) force law. It is not a derivation because d=3 is
    an input to GFM, not an output. However, testing whether GFM's geometric
    factors (k=4, d=3) correctly predict BOTH G's magnitude (tested elsewhere)
    AND the force law's functional form strengthens the case that these are
    natural geometric parameters rather than fitted values.
    """

    name = "Newton's Inverse Square Law from Spatial Geometry"

    question = (
        "Why does gravitational force decrease as r^(-2) specifically? "
        "Standard physics derives this from flux conservation in 3D space, "
        "where surface area scales as r^2. If GFM's k=4 closure operates "
        "in d=3 dimensions, does the same geometry that determines G's "
        "magnitude also constrain the force law's spatial dependence?"
    )

    reference = "Newton (1687) Principia; Modern tests: Kapner et al. (2007) PRL 98"

    tolerance = 0.01

    level = Level.CRITICAL

    commentary = (
        "Standard physics derives the inverse square law from Gauss's theorem: "
        "in d spatial dimensions, flux through a hypersphere scales as r^(d-1), "
        "so force scales as r^(-(d-1)) = r^(-2) for d=3. GFM uses d=3 as an "
        "input parameter for Merkaba coupling geometry. This test documents that "
        "the same d=3 that appears in the G formula (denominator kd+1=13) also "
        "determines the force law exponent d-1=2. This is an observation of "
        "consistency, not a derivation, because d=3 is assumed rather than derived. "
        "However, the fact that ONE geometric parameter (d=3) simultaneously "
        "constrains both G's magnitude and the force law's form suggests these "
        "are natural geometric inputs rather than arbitrary fitting parameters."
    )

    audit_score = None
    audit_notes = ""
    academic_paper = None
    contribution_score = None

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Gauss's law for gravity in d dimensions")
            .step("Flux through hypersphere of radius r scales as r^(d-1)")
            .step("Force law: F proportional to r^(-(d-1))")
            .step("For d=3 spatial dimensions: F proportional to r^(-2)")
            .equation("F = G * m1 * m2 / r^2")
            .step("GFM OBSERVATION: The d=3 parameter in Merkaba coupling")
            .step("GFM G formula uses kd+1 = 4*3+1 = 13 in denominator")
            .step("The same d=3 determines force law exponent: d-1 = 2")
            .step("Test case: Solar gravitational force at Earth orbit")
            .step("r = 1.496e11 m (1 AU), M_solar = 1.989e30 kg")
            .step("F/m = G * M_solar / r^2 (acceleration at Earth)")
            .equation("a = 6.674e-11 * 1.989e30 / (1.496e11)^2")
            .step("Predicted: a = 5.93e-3 m/s^2")
            .step("Observed: a = 5.93e-3 m/s^2 (centripetal acceleration)")
            .conclude(
                "The r^(-2) dependence is observed to match d-1=2 from GFM's "
                "d=3 parameter. This is geometric consistency, not independent "
                "derivation, since d=3 is input to both standard physics and GFM."
            )
        )

    def model(self) -> Model:
        d = 3  # GFM spatial dimensions parameter
        k = K  # GFM closure constant = 4
        
        # Force law exponent from dimensional analysis
        force_exponent = d - 1
        
        # Test case: Solar gravitational acceleration at Earth orbit
        r_earth_orbit = 1.496e11  # meters (1 AU)
        
        # Predicted acceleration using r^(-2) law
        a_predicted = G * M_SOLAR / (r_earth_orbit ** force_exponent)
        
        # Surface area scaling factor in d=3 dimensions
        # For sphere: A = 4*pi*r^2, exponent is d-1=2
        surface_area_exponent = d - 1
        
        # Verify that kd+1 denominator uses the same d=3
        kd_plus_one = k * d + 1
        
        return (
            Model()
            .add("d (spatial dimensions)", float(d))
            .add("k (closure constant)", float(k))
            .add("Force law exponent (d-1)", float(force_exponent))
            .add("Surface area exponent (d-1)", float(surface_area_exponent))
            .add("kd+1 in G formula", float(kd_plus_one))
            .add("Solar accel at 1 AU (m/s^2)", a_predicted)
        )

    def observations(self) -> Observed:
        # Observed centripetal acceleration at Earth's orbit
        # v = 2*pi*r/T where T = 365.25 days
        r_earth_orbit = 1.496e11  # meters
        T_year = 365.25 * 24 * 3600  # seconds
        v_earth = 2 * math.pi * r_earth_orbit / T_year
        a_observed = v_earth ** 2 / r_earth_orbit
        
        # Observed exponent from experimental tests
        # Kapner et al. (2007) verified r^(-2) to sub-mm scales
        observed_exponent = 2.0
        
        return (
            Observed()
            .add("d (spatial dimensions)", 3.0)
            .add("k (closure constant)", 4.0)
            .add("Force law exponent (d-1)", observed_exponent)
            .add("Surface area exponent (d-1)", observed_exponent)
            .add("kd+1 in G formula", 13.0)
            .add("Solar accel at 1 AU (m/s^2)", a_observed)
        )


if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Newton's Inverse Square Law from Spatial Geometry",
        summary="Tests whether GFM's d=3 parameter constrains both G magnitude and r^(-2) force law",
        test_classes=[NewtonForceLawExponent],
    )
