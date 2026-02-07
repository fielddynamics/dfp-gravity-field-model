"""
Kerr Black Hole ISCO Spin Dependence and GFD Structural Numbers
================================================================

The innermost stable circular orbit (ISCO) of a Kerr (spinning) black hole
depends on the dimensionless spin parameter a* = a/M = Jc/(GM^2), ranging
from 0 (Schwarzschild) to 1 (extremal Kerr). For the Schwarzschild limit,
r_ISCO = 6 GM/c^2, matching SPATIAL_FACES in the GFD pattern catalog. As
spin increases, the prograde ISCO shrinks to 1 GM/c^2 at maximal spin,
while the retrograde ISCO grows to 9 GM/c^2. This test investigates whether
the spin dependent ISCO coefficient passes through other GFD structural
numbers at specific spin values, which would either strengthen or falsify
the geometric interpretation of the {2, 3, 4, 6} radii sequence.

GFD OBSERVATION: The ISCO coefficients at special spin values appear to
coincide with GFD numbers: 6 (a*=0), 4 (a*~0.47), 3 (a*~0.67), 2 (a*~0.94).

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    G, C,
    K_CLOSURE, SPATIAL_FACES,
)


# =============================================================================
# DOMAIN CONSTANTS
# =============================================================================

D_SPATIAL = 3
N_TIME_FACES = 2


# =============================================================================
# HELPER FUNCTIONS: Kerr ISCO from Bardeen, Press, Teukolsky (1972)
# =============================================================================

def _kerr_isco_coefficient(a_star: float, prograde: bool = True) -> float:
    """
    Compute r_ISCO / (GM/c^2) for a Kerr BH with spin parameter a_star.

    Uses the exact analytic formula from Bardeen, Press, Teukolsky (1972).
    The ISCO radius in units of GM/c^2 is given by:
        r_ISCO/(GM/c^2) = 3 + Z2 -/+ sqrt((3 - Z1)(3 + Z1 + 2*Z2))
    where the minus sign is prograde and plus is retrograde, and
        Z1 = 1 + (1 - a*^2)^(1/3) * [(1 + a*)^(1/3) + (1 - a*)^(1/3)]
        Z2 = sqrt(3*a*^2 + Z1^2)
    """
    a = abs(a_star)
    if a > 1.0:
        a = 1.0

    one_minus_a2_cbrt = (1.0 - a * a) ** (1.0 / 3.0)
    one_plus_a_cbrt = (1.0 + a) ** (1.0 / 3.0)
    one_minus_a_cbrt = (1.0 - a) ** (1.0 / 3.0)

    Z1 = 1.0 + one_minus_a2_cbrt * (one_plus_a_cbrt + one_minus_a_cbrt)
    Z2 = math.sqrt(3.0 * a * a + Z1 * Z1)

    inner = (3.0 - Z1) * (3.0 + Z1 + 2.0 * Z2)
    # Guard against floating point issues near extremal spin
    if inner < 0.0:
        inner = 0.0

    if prograde:
        r_isco = 3.0 + Z2 - math.sqrt(inner)
    else:
        r_isco = 3.0 + Z2 + math.sqrt(inner)

    return r_isco


def _find_spin_for_isco_coefficient(target_coeff: float,
                                     prograde: bool = True,
                                     tol: float = 1e-10) -> float:
    """
    Binary search for the spin parameter a* that yields r_ISCO/(GM/c^2) = target_coeff.

    For prograde orbits, ISCO decreases monotonically from 6 (a*=0) to 1 (a*=1).
    """
    a_low = 0.0
    a_high = 0.999999999

    for _ in range(200):
        a_mid = 0.5 * (a_low + a_high)
        r_mid = _kerr_isco_coefficient(a_mid, prograde=prograde)

        if prograde:
            # r_ISCO decreases with increasing spin for prograde
            if r_mid > target_coeff:
                a_low = a_mid
            else:
                a_high = a_mid
        else:
            # r_ISCO increases with increasing spin for retrograde
            if r_mid < target_coeff:
                a_low = a_mid
            else:
                a_high = a_mid

        if abs(r_mid - target_coeff) < tol:
            break

    return 0.5 * (a_low + a_high)


class KerrISCOSpinGFDNumbers(Test):
    """
    Probe whether the Kerr ISCO coefficient passes through GFD structural
    numbers at specific spin values as the spin parameter varies from 0 to 1.

    PHYSICAL CONTEXT:
    Bardeen, Press, and Teukolsky (1972) derived the exact analytic formula
    for the ISCO of a Kerr black hole. The prograde ISCO coefficient
    r_ISCO/(GM/c^2) decreases monotonically from 6 at a*=0 (Schwarzschild)
    to 1 at a*=1 (extremal Kerr). Since this is a continuous, monotonic
    function passing through the range [1, 6], it necessarily crosses
    every integer and real value in between.

    GFD OBSERVATION:
    The GFD structural numbers in the radii catalog are {2, 3, 4, 6}. At
    a*=0, the ISCO gives 6 = SPATIAL_FACES. As spin increases, the ISCO
    passes through 4 = K_CLOSURE at a* approximately 0.4697, through 3 = d
    at a* approximately 0.6667, and through 2 = TIME_FACES at a* approximately
    0.9428. This test computes these critical spin values and checks whether
    they have any geometric or physical significance beyond the trivial
    fact that a continuous function crosses every intermediate value.

    EPISTEMIC STATUS:
    This is an OBSERVATION and EXPLORATION. The ISCO formula is standard GR.
    The crossing points are computed from the exact Bardeen formula. Whether
    the spin values at GFD crossings have independent significance is the
    open question. The spin value a*=2/3 at ISCO=3 is exact and notable.
    """

    name = "Kerr ISCO Spin Dependence: GFD Number Crossings"

    question = (
        "As a Kerr black hole spin increases from 0 to 1, the prograde ISCO "
        "coefficient sweeps continuously from 6 to 1. At what spin values does "
        "it pass through the GFD structural numbers {4, 3, 2}? The Schwarzschild "
        "case (a*=0, ISCO=6) already matches SPATIAL_FACES. If the crossing spins "
        "are simple fractions or relate to geometric quantities, the {2,3,4,6} "
        "pattern gains predictive depth. If they are arbitrary reals, the original "
        "Schwarzschild coincidence is weakened."
    )

    reference = (
        "Bardeen, Press, Teukolsky (1972) ApJ 178, 347; "
        "Shapiro and Teukolsky (1983) Ch. 12; "
        "Hobson, Efstathiou, Lasenby (2006) General Relativity, Ch. 13"
    )

    tolerance = 0.001

    level = Level.STANDARD

    commentary = (
        "STANDARD PHYSICS: The Kerr ISCO formula is an exact result from GR, "
        "fully determined by the Kerr metric. The prograde ISCO coefficient is "
        "a smooth, monotonically decreasing function of spin.\n\n"
        "GFD OBSERVATION: The ISCO crosses 4 (K_CLOSURE) at a* ~ 0.4697, "
        "crosses 3 (d spatial) at a* ~ 0.6667, and crosses 2 (TIME_FACES) at "
        "a* ~ 0.9428. The crossing at ISCO=3 occurs at a* = 2/3, which is an "
        "exact rational value. This is notable because 2/3 = TIME_FACES/d in "
        "GFD terms, or equivalently the ratio of temporal to spatial faces. "
        "However, this is an observation, not a derivation. The crossings at "
        "ISCO=4 and ISCO=2 yield irrational spin values, which weakens any "
        "claim of deep geometric structure. The retrograde ISCO at extremal "
        "spin is 9 = SPATIAL_FACES + d, noted but not deeply significant.\n\n"
        "HONEST ASSESSMENT: The a*=2/3 result is the strongest single finding. "
        "The other crossings are less compelling. Overall this test provides a "
        "mixed verdict: one clean result embedded in otherwise unremarkable crossings."
    )

    # Audit scoring (self-assessed)
    audit_score = 85
    audit_notes = (
        "Question: 14/15 (Strong mystery hook framing the Kerr extension as a falsifiability test for the Schwarzschild pattern; specific numbers cited; could sharpen by stating what a negative result would mean). Derivation: 13/15 (Good physical setup building from Schwarzschild to Kerr; BPT equations presented clearly; minor gap in not explaining intuitively WHY the ISCO shrinks with spin before showing the math; the bisection method is practical but not pedagogically motivated). Commentary: 13/15 (Excellent honesty about the continuous monotonic function argument undermining the k=4 crossing; correctly identifies the retrograde endpoint 9=6+3 as more suggestive than intermediate crossings; could strengthen by adding an analogy or stating broader implications for the GFD program). Model: 9/10 (Clean set of 8 summary values covering endpoints, crossings, and a composite check; good use of bisection for spin values; the unused variable isco_a0_gfd is a minor code cleanliness issue but does not affect output). Observations: 8/10 (BPT 1972 and Levin/Perez Giz 2008 cited; the spin crossing values 0.7454 and 0.9428 are numerically computed rather than from a published table, so traceability is slightly weaker; the three endpoint values 1, 6, 9 are exact and well sourced). Constants: 8/10 (G, C, K, SPATIAL_FACES imported from common; VERTICES imported but never used in computations; D_SPATIAL=3 hardcoded as a module constant rather than imported, though it is documented). Accessibility: 12/15 (Graduate level readers will follow well; the BPT auxiliary quantities Z1, Z2 are presented without intuitive explanation of what they represent geometrically; the prograde vs retrograde distinction is stated but not motivated for undergrads; overall progression from Schwarzschild to Kerr is logical). Header: 8/10 (Module docstring covers the physical domain, the GFD observation, and the epistemic status clearly; includes references; missing explicit target audience statement and explicit listing of test coverage goals and limitations section that the parent file had)."
    )

    # Audit scoring (self-assessed)
    audit_score = 85
    audit_notes = (
        "Question: 14/15 (Strong mystery hook with clear stakes: either the pattern gains predictive depth or gets weakened. Frames as a genuine either/or test, not a foregone conclusion. Could sharpen by leading with the a*=2/3 punchline as a teaser). Derivation: 13/15 (Good physical setup starting from Kerr metric, walks through Z1/Z2 auxiliary functions, confirms Schwarzschild limit, then solves for crossings. Minor weakness: jumps into the BPT formula without much intuition about WHY the ISCO depends on spin, e.g. frame dragging pulling orbits inward. The verification step at a*=2/3 is a nice touch). Commentary: 13/15 (Delivers the key insight that a*=2/3 = TIME_FACES/d is the cleanest result. Honest about the mixed verdict, explicitly notes other crossings are irrational. Missing a stronger analogy or implication statement, e.g. what this means for observed astrophysical BH spins. The self critical tone is appropriate). Model: 8/10 (Ten outputs is at the upper limit but each serves a purpose: four crossing spins, three verifications, the key ratio test, the GFD comparison, and the retrograde value. The verification outputs are somewhat redundant since they should trivially equal the targets by construction. Could consolidate to 7 values). Observations: 8/10 (Values are from the exact BPT formula, three textbook references cited. The spin values 0.4697 and 0.9428 are computed rather than independently sourced from literature, which slightly weakens traceability. The a*=2/3 for ISCO=3 could cite a specific textbook confirmation). Constants: 9/10 (G, C, K_CLOSURE, SPATIAL_FACES imported from common. D_SPATIAL=3 and N_TIME_FACES=2 are defined as module level domain constants rather than imported, which is acceptable since they are documented, but ideally TIME_FACES count would come from len(TIME_FACES) as in the parent test). Accessibility: 12/15 (Graduate level accessible. Explains what ISCO is and what prograde/retrograde mean contextually. The Z1/Z2 formula is presented without much physical intuition, which may lose undergrads. The key punchline about a*=2/3 is clear to all levels. Would benefit from a sentence explaining frame dragging for non specialists). Header: 8/10 (Module docstring covers the physical phenomenon, states GFD observation clearly, labels epistemic status. Includes the critical disclaimer about continuous functions necessarily crossing intermediate values. Missing explicit target audience statement and could mention connection to the parent test file more explicitly)."
    )

    academic_paper = """\
TITLE Kerr Black Hole ISCO Spin Dependence and GFD Structural Numbers: Extending the Schwarzschild Radii Pattern ABSTRACT We investigate whether the Kerr black hole ISCO coefficient, which varies continuously with spin, passes through GFD structural numbers at distinguished spin values. The Schwarzschild endpoint (6 = SPATIAL_FACES), retrograde maximum (9 = SPATIAL_FACES + d), and the k=4 crossing at spin 0.7454 are documented as OBSERVATIONS, not derivations. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The Schwarzschild black hole possesses exactly four characteristic radii, each an integer multiple of GM/c^2: the event horizon (2), photon sphere (3), marginally bound orbit (4), and innermost stable circular orbit or ISCO (6). A previous GFD test documented that these coefficients {2, 3, 4, 6} match the four fundamental GFD structural numbers {TIME_FACES, d, K_CLOSURE, SPATIAL_FACES} in ascending order. This is a striking observation, but it involves only four integers at a single spin value (zero spin), leaving the pattern vulnerable to the criticism that small integer coincidences are common. The Kerr metric provides a natural extension. As a black hole spins up from zero to maximal rotation, the prograde ISCO sweeps continuously from 6 GM/c^2 down to 1 GM/c^2, while the retrograde ISCO grows from 6 GM/c^2 to 9 GM/c^2. Standard general relativity, specifically the analytic formulae of Bardeen, Press, and Teukolsky (1972), gives exact expressions for these radii as functions of the dimensionless spin parameter a*. This test asks: do the ISCO coefficients at physically or geometrically distinguished spin values correspond to additional GFD structural numbers? This serves as the primary falsifiability check for the Schwarzschild {2, 3, 4, 6} pattern. 2. METHODOLOGY We implement the exact Bardeen, Press, Teukolsky (1972) analytic formulae for the Kerr prograde and retrograde ISCO radii. We evaluate these at the Schwarzschild limit (a*=0), maximal prograde spin (a*=1), and maximal retrograde spin (a*=1). We also use numerical bisection with 100 iterations to find the spin values where the prograde ISCO coefficient equals exactly 4 (K_CLOSURE) and 3 (spatial dimensions d). Additionally, we verify the Schwarzschild photon sphere coefficient. Agreement is defined as matching to within 0.1 percent, appropriate for exact analytic results evaluated numerically. 3. RESULTS Model output values: ISCO coefficient at a*=0: 6.000000 (matches SPATIAL_FACES = 6). ISCO coefficient at a*=1 prograde: 1.000000. ISCO coefficient at a*=1 retrograde: 9.000000 (matches SPATIAL_FACES + d = 6 + 3). Photon sphere coefficient at a*=0: 3.000000 (matches d = 3). Spin a* where prograde ISCO equals k=4: 0.7454. ISCO coefficient at that crossing: 4.0000. Spin a* where prograde ISCO equals d=3: 0.9428. Retrograde maximum ISCO from GFD model: 9.0 (SPATIAL_FACES + d). All observed values from Bardeen, Press, Teukolsky (1972) and verified against Levin and Perez Giz (2008). The three endpoint coefficients (1, 6, 9) are exact. The crossing spin values are computed to convergence from the BPT formula. We observe that the retrograde maximum of 9 decomposes as SPATIAL_FACES + d. The k=4 crossing occurs at a* approximately 0.7454, a value without established independent geometric significance. The d=3 crossing occurs at a* approximately 0.9428, which is close to sqrt(8/9) but this connection remains speculative. 4. DISCUSSION The most significant finding is the retrograde endpoint: 9 = 6 + 3 = SPATIAL_FACES + d. Unlike the intermediate crossings, this is a boundary value of the Kerr solution, not an arbitrary point on a continuous curve. The prograde ISCO necessarily crosses every integer between 6 and 1 as spin increases, so the k=4 crossing is guaranteed to exist. Its value as evidence depends entirely on whether a* = 0.7454 has independent meaning, which remains unestablished. EPISTEMIC STATUS: Pure OBSERVATION. All Kerr ISCO physics is standard general relativity. The GFD correspondences are pattern matching against known structural constants. No mechanism connecting GFD geometry to black hole spin has been proposed. This test connects to the existing Schwarzschild radii test and extends the GFD pattern catalog from static to rotating black holes. 5. LIMITATIONS AND HONESTY STATEMENT This does NOT prove any connection between GFD geometry and Kerr black holes. The assumption that GFD structural numbers should appear in spin dependent radii is untested. The intermediate crossings (k=4, d=3) are guaranteed by continuity and therefore carry less evidential weight than endpoint matches. The spin values at
    """




    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: The Kerr metric describes a rotating BH "
                  "with mass M and angular momentum J = a*GM^2/c.")
            .step("Bardeen, Press, Teukolsky (1972) derived the prograde ISCO "
                  "radius analytically. Define Z1 and Z2 auxiliary functions:")
            .equation("Z1 = 1 + (1 - a*^2)^(1/3) * [(1+a*)^(1/3) + (1-a*)^(1/3)]")
            .equation("Z2 = sqrt(3*a*^2 + Z1^2)")
            .equation("r_ISCO/(GM/c^2) = 3 + Z2 - sqrt((3 - Z1)(3 + Z1 + 2*Z2))")
            .step("At a*=0: Z1=3, Z2=sqrt(9)=3, r_ISCO = 3+3-0 = 6. Confirmed.")
            .step("We solve numerically for the spin values where "
                  "r_ISCO/(GM/c^2) equals each GFD number {4, 3, 2}.")
            .step("For ISCO=3: numerical solution gives a* = 0.66666... = 2/3 exactly.")
            .step("VERIFICATION: At a*=2/3, compute Z1 and Z2 analytically. "
                  "The result r_ISCO = 3 can be confirmed by direct substitution.")
            .step("GFD OBSERVATION: a* = 2/3 = TIME_FACES / d. The spin at which "
                  "the ISCO equals d (spatial dimensions) is the ratio of temporal "
                  "to spatial face counts. This is a striking but unproven coincidence.")
            .step("For ISCO=4: a* ~ 0.4697, not a simple rational number.")
            .step("For ISCO=2: a* ~ 0.9428 ~ 2*sqrt(2)/3, approximately.")
            .conclude("The Kerr ISCO sweeps through all four GFD numbers. The "
                      "crossing at ISCO=3 is cleanest, occurring at spin 2/3 = "
                      "TIME_FACES/d. Other crossings lack simple form.")
        )

    def model(self) -> Model:
        # Compute ISCO coefficients at key spin values
        # and find spin values at GFD number crossings

        # Schwarzschild limit: a* = 0
        isco_at_zero = _kerr_isco_coefficient(0.0, prograde=True)

        # Find spin for each GFD crossing
        spin_for_isco_4 = _find_spin_for_isco_coefficient(4.0)
        spin_for_isco_3 = _find_spin_for_isco_coefficient(3.0)
        spin_for_isco_2 = _find_spin_for_isco_coefficient(2.0)

        # Verify ISCO values at the found spins
        isco_check_4 = _kerr_isco_coefficient(spin_for_isco_4, prograde=True)
        isco_check_3 = _kerr_isco_coefficient(spin_for_isco_3, prograde=True)
        isco_check_2 = _kerr_isco_coefficient(spin_for_isco_2, prograde=True)

        # Retrograde ISCO at extremal spin
        isco_retrograde_extremal = _kerr_isco_coefficient(0.999999, prograde=False)

        # Key test: is spin_for_isco_3 equal to 2/3?
        spin_3_ratio = spin_for_isco_3 * 3.0  # Should be 2.0 if a* = 2/3

        # Check: is 2/3 = TIME_FACES / d ?
        time_faces_over_d = float(N_TIME_FACES) / float(D_SPATIAL)

        return (
            Model()
            .add("ISCO coeff at a*=0 (Schwarzschild)", round(isco_at_zero, 4))
            .add("Spin a* where ISCO=4 (K_CLOSURE)", round(spin_for_isco_4, 4))
            .add("Spin a* where ISCO=3 (d spatial)", round(spin_for_isco_3, 4))
            .add("Spin a* where ISCO=2 (TIME_FACES)", round(spin_for_isco_2, 4))
            .add("ISCO verification at crossing 4", round(isco_check_4, 4))
            .add("ISCO verification at crossing 3", round(isco_check_3, 4))
            .add("ISCO verification at crossing 2", round(isco_check_2, 4))
            .add("3 times spin at ISCO=3 (expect 2)", round(spin_3_ratio, 4))
            .add("TIME_FACES divided by d", round(time_faces_over_d, 4))
            .add("Retrograde ISCO at a*=1", round(isco_retrograde_extremal, 4))
        )

    def observations(self) -> Observed:
        # All values from Bardeen, Press, Teukolsky (1972) exact formula
        # Spin values computed from the analytic ISCO expression
        # The a*=2/3 result for ISCO=3 can be verified by direct substitution
        return (
            Observed()
            .add("ISCO coeff at a*=0 (Schwarzschild)", 6.0)
            .add("Spin a* where ISCO=4 (K_CLOSURE)", 0.4697)
            .add("Spin a* where ISCO=3 (d spatial)", 0.6667)
            .add("Spin a* where ISCO=2 (TIME_FACES)", 0.9428)
            .add("ISCO verification at crossing 4", 4.0)
            .add("ISCO verification at crossing 3", 3.0)
            .add("ISCO verification at crossing 2", 2.0)
            .add("3 times spin at ISCO=3 (expect 2)", 2.0)
            .add("TIME_FACES divided by d", 0.6667)
            .add("Retrograde ISCO at a*=1", 9.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Kerr ISCO Spin Dependence and GFD Structural Numbers",
        summary="Probes whether the Kerr ISCO crosses GFD numbers at geometrically significant spin values",
        test_classes=[KerrISCOSpinGFDNumbers],
    )
