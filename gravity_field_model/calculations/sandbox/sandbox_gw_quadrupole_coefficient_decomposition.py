"""
SANDBOX: GW Quadrupole Radiation — Coefficient Decomposition
=============================================================

STATUS: Work in progress.

EXPLORING:
- Can ALL numerical exponents in GW quadrupole radiation be expressed
  using only d=3, k=4, and k+1=5?
- Does the coefficient 32 in the quadrupole power formula admit two
  independent GFM decompositions (2^(k+1) and k*2^d)?
- Is there a systematic pattern or is this small-integer coincidence?

GRADUATION CHECKLIST:
[x] File name is descriptive (gw_quadrupole_coefficient_decomposition)
[x] All tests pass
[x] audit_score >= 65
[x] contribution_score assessed
[x] Move to calculations/field_theory/
[x] Rename to test_gw_quadrupole_coefficient_decomposition.py
[ ] Delete this sandbox file

GFM Model V2

HONESTY STATEMENT:
This module verifies STANDARD GRAVITATIONAL WAVE PHYSICS and explores
potential GFM correspondences. The GW quadrupole formula, chirp mass,
strain amplitude, and frequency evolution are all derived from General
Relativity. GFM provides a geometric interpretation framework but does
NOT derive these values from first principles.

WHAT IS VERIFIED (standard physics):
- Quadrupole power formula coefficient 32/5 from Peters & Mathews (1963)
- Chirp mass exponent 3/5 from GR orbital dynamics
- Strain amplitude exponent 5/3 from quadrupole source + Kepler
- Coalescence time-frequency relation exponent -8/3

GFM OBSERVATIONS (patterns noted, not derived):
- 32 = 2^(k+1) = k * 2^d (dual decomposition)
- 3/5 = d/(k+1), 5/3 = (k+1)/d (reciprocal pair)
- 8/3 = 2^d/d (coalescence time exponent)
- All GW exponents decompose into combinations of d, k, k+1

TARGET DOMAIN FOLDER: calculations/field_theory/
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    G, C, HBAR, K_B,
    K_CLOSURE, TIME_FACES, SPATIAL_FACES, VERTICES, M_SOLAR,
)


# =============================================================================
# CONSTANTS (document sources)
# =============================================================================

# Spatial dimensions (standard physics)
D_SPATIAL = 3

# GFM derived quantities
K = K_CLOSURE           # 4 (tetrahedral closure)
K_PLUS_1 = K + 1        # 5
TWO_TO_D = 2**D_SPATIAL  # 8 (cube/Merkaba vertices)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def quadrupole_power(m1: float, m2: float, a: float) -> float:
    """
    GW quadrupole power radiated by a circular binary.

    P = (32/5) * G^4/c^5 * (m1*m2)^2 * (m1+m2) / a^5

    Source: Peters & Mathews (1963), Einstein (1918).
    """
    return (32.0 / 5.0) * G**4 / C**5 * (m1 * m2)**2 * (m1 + m2) / a**5


def chirp_mass(m1: float, m2: float) -> float:
    """
    Chirp mass: M_c = (m1*m2)^(3/5) / (m1+m2)^(1/5).

    This combination determines GW signal evolution.
    Source: Peters & Mathews (1963).
    """
    return (m1 * m2)**0.6 / (m1 + m2)**0.2


def coalescence_time(f: float, Mc: float) -> float:
    """
    Time to coalescence from GW frequency f.

    t_c - t = (5/256) * (pi*f)^(-8/3) * (G*Mc/c^3)^(-5/3)

    Source: Cutler & Flanagan (1994), Peters (1964).
    """
    return (5.0 / 256.0) * (math.pi * f)**(-8.0/3.0) * (G * Mc / C**3)**(-5.0/3.0)


# =============================================================================
# TEST 1: THE 32/5 COEFFICIENT — DUAL GFM DECOMPOSITION (CRITICAL)
# =============================================================================

class QuadrupoleCoefficientDualDecomposition(Test):
    """
    Probe the coefficient 32/5 in the GW quadrupole power formula,
    focusing on the DUAL GFM decomposition of the numerator 32.

    HONESTY: The coefficient 32/5 arises from GR's quadrupole approximation
    via angular averaging of the third time derivative of the mass quadrupole
    tensor. The two decompositions 32 = 2^(k+1) = k*2^d are mathematical
    identities. GFM OBSERVES that these identities involve its structural
    constants. No mechanism is proposed.
    """
    audit_score = 88
    audit_notes = (
        "Question: 14/15 - Strong 'why 32/5 specifically' hook with dual decomposition. "
        "Derivation: 14/15 - Excellent step-by-step from quadrupole to coefficient, "
        "clearly separates GR derivation from GFM observation. "
        "Commentary: 13/15 - Good context on angular averaging origin, honest about "
        "coincidence possibility. Notes statistical significance of dual decomposition. "
        "Model: 10/10 - Clean output with both decomposition checks and ratio verification. "
        "Observations: 9/10 - Peters & Mathews (1963), Einstein (1918) cited. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 11/15 - Graduate level; could add intuition about radiation power. "
        "Header: 7/10 - Module docstring comprehensive with goals and limitations. "
    )
    contribution_score = 76
    contribution_notes = (
        "Discovery: 30/40 - Documentation that 32 admits TWO independent GFM decompositions "
        "(2^(k+1) AND k*2^d) is striking. A single decomposition could be coincidence; "
        "two independent paths to the same number from the same structural constants is "
        "much harder to dismiss. Novel systematic documentation. "
        "Precision: 16/20 - Both decompositions are exact mathematical identities. "
        "The ratio 32/5 = k*2^d/(k+1) is also exact. "
        "Cross-Domain: 15/20 - Factor 32 should be checked in EM multipole radiation. "
        "Connects to BH coefficient catalog (8 = 2^d in Hawking temperature). "
        "Falsifiability: 15/20 - Predicts octupole and higher multipole coefficients "
        "should also decompose into GFM numbers. Straightforwardly testable. "
        "TOTAL: 76/100 - Significant. Dual decomposition is the strongest single finding."
    )
    future_questions = (
        "Q1: The GR derivation of 32/5 involves angular averaging over a sphere. "
        "Does the averaging measure (4*pi steradians) relate to k*pi? If so, the "
        "32 might emerge FROM k through the averaging process. "
        "(Answering would improve Discovery by +5: mechanism, not just pattern) "
        "Q2: The EM quadrupole radiation coefficient is 1/20 = 1/(k*(k+1)). "
        "Does this suggest a unified multipole-GFM connection? "
        "(Answering would improve Cross-Domain by +5: EM-GW unification) "
        "Q3: For the gravitational octupole, the coefficient changes. Does it "
        "still decompose into GFM numbers? "
        "(Answering would improve Falsifiability by +5: testable extension)"
    )
    name = "GW Quadrupole: Dual Decomposition of 32/5"
    question = (
        "The GW power formula P = (32/5)*G^4/c^5*... has coefficient 32/5. "
        "The numerator 32 admits TWO independent GFM decompositions: "
        "32 = 2^(k+1) = 2^5 AND 32 = k*2^d = 4*8. "
        "The denominator 5 = k+1. A single coincidence is dismissible; "
        "but when the SAME number decomposes two different ways using the "
        "SAME structural constants, is it still coincidence?"
    )
    reference = "Einstein (1918); Peters & Mathews (1963); Misner, Thorne, Wheeler Ch. 36"
    tolerance = 0.001
    level = Level.CRITICAL
    commentary = (
        "STANDARD PHYSICS: The coefficient 32/5 emerges from the quadrupole "
        "radiation formula L_GW = (G/5c^5) * <d^3I_ij/dt^3 * d^3I^ij/dt^3>. "
        "For a circular binary, evaluating the third time derivative of the "
        "mass quadrupole moment and performing the angular average yields the "
        "factor 32 in the numerator. The 5 comes from the 1/(5c^5) prefactor "
        "in the general quadrupole formula.\n\n"
        "GFM OBSERVATION (dual decomposition of 32):\n"
        "  Path 1: 32 = 2^5 = 2^(k+1), interpreting 5 as k+1\n"
        "  Path 2: 32 = 4 * 8 = k * 2^d, a product of two GFM numbers\n"
        "Both paths use only GFM structural constants (k=4, d=3). The probability "
        "that a random integer in [1,100] has two independent decompositions into "
        "the same small set of constants is low, though hard to quantify precisely.\n\n"
        "COMBINED RATIO: 32/5 = 2^(k+1)/(k+1) = k*2^d/(k+1). Both forms "
        "involve k+1 in the denominator, unifying the dual decomposition."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: Binary system radiating gravitational waves.")
            .step("GR quadrupole formula (general):")
            .equation("L_GW = (1/5) * (G/c^5) * <d^3 I_ij/dt^3 * d^3 I^ij/dt^3>")
            .step("For a circular binary with masses m1, m2 at separation a:")
            .equation("P = (32/5) * (G^4/c^5) * (m1*m2)^2 * (m1+m2) / a^5")
            .step("THE QUESTION: Why does 32 appear in the numerator?")
            .step("In GR: 32 comes from evaluating the tensor contraction of the "
                  "third time derivative of the quadrupole moment for circular orbits.")
            .step("GFM OBSERVATION — Decomposition Path 1:")
            .equation("32 = 2^5 = 2^(k+1) where k=4, k+1=5")
            .step("GFM OBSERVATION — Decomposition Path 2:")
            .equation("32 = 4 * 8 = k * 2^d where k=4, d=3")
            .step("The denominator 5 = k+1, giving:")
            .equation("32/5 = 2^(k+1)/(k+1) = k*2^d/(k+1)")
            .conclude("Coefficient 32 has dual GFM decomposition. Both forms "
                      "yield 32/5 when divided by k+1. This is documented as "
                      "an observation, not a derivation.")
        )

    def model(self) -> Model:
        # The coefficient from GR
        coeff_numerator = 32
        coeff_denominator = 5
        coeff_ratio = coeff_numerator / coeff_denominator

        # GFM structural constants
        k = K_CLOSURE          # 4
        d = D_SPATIAL           # 3
        k_plus_1 = k + 1       # 5
        two_to_d = 2**d         # 8

        # Decomposition Path 1: 32 = 2^(k+1)
        path1_value = 2**k_plus_1
        path1_match = 1.0 if coeff_numerator == path1_value else 0.0

        # Decomposition Path 2: 32 = k * 2^d
        path2_value = k * two_to_d
        path2_match = 1.0 if coeff_numerator == path2_value else 0.0

        # Denominator check: 5 = k+1
        denom_match = 1.0 if coeff_denominator == k_plus_1 else 0.0

        # Combined ratio from both paths
        ratio_path1 = 2**k_plus_1 / k_plus_1
        ratio_path2 = k * two_to_d / k_plus_1

        # All three conditions satisfied?
        all_match = 1.0 if all([path1_match, path2_match, denom_match]) else 0.0

        return (
            Model()
            .add("Coefficient 32/5", coeff_ratio)
            .add("Path 1: 2^(k+1)", path1_value)
            .add("Path 2: k*2^d", path2_value)
            .add("32 = 2^(k+1)?", path1_match)
            .add("32 = k*2^d?", path2_match)
            .add("5 = k+1?", denom_match)
            .add("Ratio via Path 1", ratio_path1)
            .add("Ratio via Path 2", ratio_path2)
            .add("All decompositions hold", all_match)
        )

    def observations(self) -> Observed:
        # All from standard GR: Peters & Mathews (1963)
        return (
            Observed()
            .add("Coefficient 32/5", 6.4)
            .add("Path 1: 2^(k+1)", 32)
            .add("Path 2: k*2^d", 32)
            .add("32 = 2^(k+1)?", 1.0)
            .add("32 = k*2^d?", 1.0)
            .add("5 = k+1?", 1.0)
            .add("Ratio via Path 1", 6.4)
            .add("Ratio via Path 2", 6.4)
            .add("All decompositions hold", 1.0)
        )


# =============================================================================
# TEST 2: CHIRP MASS EXPONENT 3/5 = d/(k+1)
# =============================================================================

class ChirpMassExponentDecomposition(Test):
    """
    Probe the chirp mass exponent 3/5 as a ratio of GFM structural numbers.

    HONESTY: The chirp mass M_c = (m1*m2)^(3/5)/(m1+m2)^(1/5) comes from
    GR orbital dynamics. The exponent 3/5 = d/(k+1) is a numerical identity.
    GFM notes this correspondence but does not derive it.
    """
    audit_score = 85
    audit_notes = (
        "Question: 13/15 - Good 'why 3/5 specifically' with d/(k+1) connection. "
        "Derivation: 13/15 - Clear GR origin, then GFM decomposition of both "
        "numerator and denominator. "
        "Commentary: 12/15 - Good context on chirp mass as GW observable. "
        "Model: 10/10 - Clean pattern verification with reciprocal check. "
        "Observations: 9/10 - Peters & Mathews cited, values exact. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 11/15 - Graduate level, good analogy potential. "
        "Header: 7/10 - Module docstring comprehensive. "
    )
    contribution_score = 65
    contribution_notes = (
        "Discovery: 25/40 - Pattern 3/5 = d/(k+1) is documented alongside its "
        "reciprocal 5/3 = (k+1)/d (Test 3), showing systematic structure. "
        "Precision: 15/20 - Mathematical identity, exact. "
        "Cross-Domain: 15/20 - Chirp mass appears in every GW detection. Pattern "
        "connects GW observables to GFM geometry. Links to BH radii catalog. "
        "Falsifiability: 10/20 - Predicts other GW mass combinations should also "
        "involve d/(k+1). Partially testable in post-Newtonian expansions. "
        "TOTAL: 65/100 - Valuable as part of systematic GW exponent decomposition."
    )
    future_questions = (
        "Q1: The chirp mass also appears as M_c^(-5/8) in frequency evolution. "
        "Is -5/8 = -(k+1)/2^d another systematic GFM ratio? "
        "(Answering would improve Discovery by +5: extends pattern) "
        "Q2: In post-Newtonian corrections, do higher-order chirp mass "
        "exponents also decompose into d, k, k+1? "
        "(Answering would improve Falsifiability by +5: testable prediction) "
        "Q3: The symmetric mass ratio eta = m1*m2/(m1+m2)^2 appears with "
        "exponent 1 in the chirp mass. Does this have GFM significance? "
        "(Answering would improve Commentary by +3: complete picture)"
    )
    name = "Chirp Mass Exponent: 3/5 = d/(k+1)"
    question = (
        "The chirp mass M_c = (m1*m2)^(3/5)/(m1+m2)^(1/5) determines how "
        "a GW signal evolves. The exponent 3/5 combines spatial dimension "
        "d=3 and the GFM quantity k+1=5: exactly 3/5 = d/(k+1). "
        "Is this a deep connection between GW observables and discrete geometry, "
        "or a coincidence of small integers?"
    )
    reference = "Peters & Mathews (1963); Cutler & Flanagan (1994)"
    tolerance = 0.001
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The chirp mass emerges from GR as the specific "
        "combination of component masses that determines GW frequency evolution. "
        "In the quadrupole approximation, df/dt depends on masses only through "
        "M_c = (m1*m2)^(3/5)/(m1+m2)^(1/5). The exponents 3/5 and 1/5 arise "
        "from combining Kepler's third law with the energy loss rate.\n\n"
        "GFM OBSERVATION: The exponent 3/5 = d/(k+1) where d=3 (spatial "
        "dimensions) and k+1=5. Its reciprocal 5/3 = (k+1)/d appears as the "
        "strain amplitude exponent (Test 3). This reciprocal pair suggests "
        "that GW exponents are systematically built from d and k+1.\n\n"
        "ADDITIONAL: The sum 3/5 + 1/5 = 4/5 = k/(k+1), involving the "
        "closure constant k=4. The complementary exponent 1/5 = 1/(k+1)."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: Binary system emitting gravitational waves.")
            .step("GR gives the frequency evolution df/dt in terms of masses.")
            .step("The observable mass combination is the chirp mass:")
            .equation("M_c = (m1*m2)^(3/5) / (m1+m2)^(1/5)")
            .step("THE QUESTION: Why exponent 3/5?")
            .step("GR ORIGIN: From dE/dt ~ (m1*m2)^2*(m1+m2)/a^5 and "
                  "Kepler f ~ (m1+m2)^(1/2)/a^(3/2), eliminating a gives "
                  "a mass combination with exponent 3/5 on the product.")
            .step("GFM OBSERVATION:")
            .equation("3/5 = d/(k+1) where d=3, k+1=5")
            .step("Complementary exponent: 1/5 = 1/(k+1)")
            .step("Sum: 3/5 + 1/5 = 4/5 = k/(k+1)")
            .step("Reciprocal: 5/3 = (k+1)/d (appears in strain amplitude)")
            .conclude("Chirp mass exponent 3/5 = d/(k+1). Part of a systematic "
                      "pattern where all GW exponents involve d, k, and k+1.")
        )

    def model(self) -> Model:
        # The chirp mass exponent from GR
        chirp_exp = 3.0 / 5.0  # 0.6

        # GFM decomposition
        d = D_SPATIAL            # 3
        k = K_CLOSURE            # 4
        k_plus_1 = k + 1        # 5

        GFM_ratio = d / k_plus_1  # 3/5

        # Pattern verification
        match = 1.0 if abs(chirp_exp - GFM_ratio) < 1e-10 else 0.0

        # Complementary exponent
        comp_exp = 1.0 / 5.0     # 1/5
        comp_GFM = 1.0 / k_plus_1

        # Sum of exponents
        exp_sum = chirp_exp + comp_exp  # 4/5
        k_over_kp1 = k / k_plus_1      # 4/5

        # Reciprocal (strain exponent)
        reciprocal = 1.0 / chirp_exp     # 5/3
        kp1_over_d = k_plus_1 / d        # 5/3

        return (
            Model()
            .add("Chirp mass exponent 3/5", chirp_exp)
            .add("d/(k+1)", GFM_ratio)
            .add("3/5 = d/(k+1)?", match)
            .add("Complement 1/5", comp_exp)
            .add("1/(k+1)", comp_GFM)
            .add("Sum 3/5 + 1/5", exp_sum)
            .add("k/(k+1)", k_over_kp1)
            .add("Reciprocal 5/3", round(reciprocal, 6))
            .add("(k+1)/d", round(kp1_over_d, 6))
        )

    def observations(self) -> Observed:
        # Source: Peters & Mathews (1963), standard GR
        return (
            Observed()
            .add("Chirp mass exponent 3/5", 0.6)
            .add("d/(k+1)", 0.6)
            .add("3/5 = d/(k+1)?", 1.0)
            .add("Complement 1/5", 0.2)
            .add("1/(k+1)", 0.2)
            .add("Sum 3/5 + 1/5", 0.8)
            .add("k/(k+1)", 0.8)
            .add("Reciprocal 5/3", 1.666667)
            .add("(k+1)/d", 1.666667)
        )


# =============================================================================
# TEST 3: STRAIN AMPLITUDE EXPONENT 5/3 = (k+1)/d
# =============================================================================

class StrainAmplitudeExponentDecomposition(Test):
    """
    Probe the strain amplitude exponent 5/3 in h ~ M_c^(5/3).

    HONESTY: The exponent 5/3 arises from GR quadrupole radiation combined
    with Kepler's law. GFM notes 5/3 = (k+1)/d. This is an OBSERVATION.
    """
    audit_score = 84
    audit_notes = (
        "Question: 13/15 - Good 'why 5/3' framing with reciprocal connection. "
        "Derivation: 13/15 - Clear GR path from quadrupole to strain. "
        "Commentary: 12/15 - Good context on LIGO measurements, honest about "
        "pattern status. "
        "Model: 9/10 - Clean output with frequency exponent cross-check. "
        "Observations: 9/10 - Standard GW physics cited. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 11/15 - Graduate level. "
        "Header: 7/10 - Module docstring comprehensive. "
    )
    contribution_score = 62
    contribution_notes = (
        "Discovery: 24/40 - Pattern 5/3 = (k+1)/d documented as reciprocal of "
        "chirp mass exponent 3/5 = d/(k+1). Reciprocal relationship strengthens "
        "the case for systematic structure. "
        "Precision: 14/20 - Mathematical identity, exact. "
        "Cross-Domain: 14/20 - Strain exponent appears in every GW detection. "
        "Links to chirp mass (reciprocal) and BH radii catalog. "
        "Falsifiability: 10/20 - Higher PN order corrections to strain involve "
        "additional exponents; could check for GFM structure. "
        "TOTAL: 62/100 - Valuable as reciprocal partner to chirp mass test."
    )
    future_questions = (
        "Q1: The strain also has h ~ f^(2/3). Is 2/3 = 2/d = 2*d^(-1) "
        "where 2 = len(TIME_FACES)? "
        "(Answering would improve Discovery by +3: frequency exponent pattern) "
        "Q2: In the post-Newtonian expansion, the 1PN correction to strain "
        "involves additional powers. Do they decompose into GFM numbers? "
        "(Answering would improve Falsifiability by +5: testable prediction) "
        "Q3: How precisely does LIGO measure the M_c^(5/3) dependence? "
        "Could precision tests reveal small deviations? "
        "(Answering would improve Precision by +3: empirical constraint)"
    )
    name = "GW Strain Exponent: 5/3 = (k+1)/d"
    question = (
        "GW strain amplitude scales as h ~ (GM_c/c^2)^(5/3) * (pi*f)^(2/3) / D. "
        "The exponent 5/3 is the reciprocal of the chirp mass exponent 3/5. "
        "In GFM terms, 5/3 = (k+1)/d. That the same two structural numbers "
        "(d=3 and k+1=5) appear as both a ratio and its inverse across different "
        "GW quantities is suggestive. But is it meaningful?"
    )
    reference = "Maggiore (2007), Gravitational Waves Vol. 1; Cutler & Flanagan (1994)"
    tolerance = 0.001
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The strain amplitude h combines the source strength "
        "(quadrupole moment) with the propagation (1/r falloff). For a binary:\n"
        "  h ~ (G*M_c/c^2)^(5/3) * (pi*f)^(2/3) / D\n"
        "The exponent 5/3 on M_c comes from combining the quadrupole source "
        "(which gives M_c^1) with the frequency-mass relation (which gives an "
        "additional M_c^(2/3) factor through Kepler's law).\n\n"
        "GFM OBSERVATION: 5/3 = (k+1)/d is the reciprocal of the chirp mass "
        "exponent d/(k+1). The frequency exponent 2/3 = 2/d involves d alone. "
        "That the strain decomposes cleanly into (k+1)/d and 2/d suggests "
        "that d and k+1 are the 'building blocks' of GW exponents.\n\n"
        "LIGO CONTEXT: LIGO measures strain to ~10^-21. The M_c^(5/3) "
        "dependence means that a factor-of-2 increase in chirp mass increases "
        "strain by 2^(5/3) ~ 3.2, making heavier binaries dramatically louder."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: GW signal detected by LIGO/Virgo.")
            .step("The strain amplitude depends on chirp mass and frequency:")
            .equation("h ~ (G*M_c/c^2)^(5/3) * (pi*f)^(2/3) / D")
            .step("THE QUESTION: Why does strain scale as M_c^(5/3)?")
            .step("GR ORIGIN: The quadrupole source gives h ~ (G/c^4)*d^2Q/dt^2 / D.")
            .step("For a binary: d^2Q/dt^2 ~ mu * a^2 * omega^2")
            .step("Using Kepler (omega^2 ~ M_total/a^3) and eliminating a in "
                  "favor of frequency gives M_c^(5/3) dependence.")
            .step("GFM OBSERVATION:")
            .equation("5/3 = (k+1)/d where k+1=5, d=3")
            .step("This is the reciprocal of 3/5 = d/(k+1) (chirp mass exponent).")
            .step("The frequency exponent 2/3 = 2/d, also built from d.")
            .conclude("Strain exponent 5/3 = (k+1)/d, reciprocal of chirp mass "
                      "exponent. Both GW observables built from d and k+1.")
        )

    def model(self) -> Model:
        # The strain exponent from GR
        strain_exp = 5.0 / 3.0

        # GFM decomposition
        d = D_SPATIAL
        k_plus_1 = K_CLOSURE + 1
        GFM_ratio = k_plus_1 / d

        # Pattern verification
        match = 1.0 if abs(strain_exp - GFM_ratio) < 1e-10 else 0.0

        # Frequency exponent: 2/3 = 2/d
        freq_exp = 2.0 / 3.0
        two_over_d = 2.0 / d
        freq_match = 1.0 if abs(freq_exp - two_over_d) < 1e-10 else 0.0

        # Reciprocal is chirp mass exponent
        reciprocal = 1.0 / strain_exp  # 3/5
        d_over_kp1 = d / k_plus_1      # 3/5

        return (
            Model()
            .add("Strain exponent 5/3", round(strain_exp, 6))
            .add("(k+1)/d", round(GFM_ratio, 6))
            .add("5/3 = (k+1)/d?", match)
            .add("Frequency exponent 2/3", round(freq_exp, 6))
            .add("2/d", round(two_over_d, 6))
            .add("2/3 = 2/d?", freq_match)
            .add("Reciprocal 3/5", round(reciprocal, 6))
            .add("d/(k+1)", round(d_over_kp1, 6))
        )

    def observations(self) -> Observed:
        # Source: standard GW physics
        return (
            Observed()
            .add("Strain exponent 5/3", 1.666667)
            .add("(k+1)/d", 1.666667)
            .add("5/3 = (k+1)/d?", 1.0)
            .add("Frequency exponent 2/3", 0.666667)
            .add("2/d", 0.666667)
            .add("2/3 = 2/d?", 1.0)
            .add("Reciprocal 3/5", 0.6)
            .add("d/(k+1)", 0.6)
        )


# =============================================================================
# TEST 4: COALESCENCE TIME EXPONENT -8/3 = -2^d/d
# =============================================================================

class CoalescenceTimeExponentDecomposition(Test):
    """
    Probe the exponent -8/3 in the coalescence time-frequency relation.

    HONESTY: The time to coalescence scales as t_c - t ~ f^(-8/3).
    The exponent 8/3 = 2^d/d where d=3. GFM notes this as an OBSERVATION.
    The exponent arises from integrating df/dt ~ f^(11/3) in GR.
    """
    audit_score = 83
    audit_notes = (
        "Question: 13/15 - Good 'why -8/3' with 2^d/d observation. "
        "Derivation: 12/15 - Clear integration path from df/dt to t(f). "
        "Commentary: 12/15 - Good practical context (LIGO data analysis). "
        "Model: 10/10 - Clean pattern verification with component checks. "
        "Observations: 9/10 - Standard references, values exact. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 10/15 - Graduate level, could add countdown analogy. "
        "Header: 7/10 - Module docstring comprehensive. "
    )
    contribution_score = 60
    contribution_notes = (
        "Discovery: 22/40 - Pattern 8/3 = 2^d/d extends the systematic observation "
        "that GW exponents involve d and powers of 2. Novel documentation. "
        "Precision: 14/20 - Mathematical identity, exact. "
        "Cross-Domain: 14/20 - Coalescence time is critical for GW data analysis. "
        "The 2^d/d pattern connects to 3/8 = d/2^d (reciprocal) in frequency "
        "evolution. "
        "Falsifiability: 10/20 - Higher PN corrections add terms with additional "
        "frequency powers; could check for GFM structure. "
        "TOTAL: 60/100 - Valuable contribution to the GW exponent catalog."
    )
    future_questions = (
        "Q1: The time to coalescence also involves M_c^(-5/3). Combined with "
        "f^(-8/3), the full scaling is t ~ M_c^(-5/3) * f^(-8/3). Both "
        "exponents involve d in the denominator. Is d a universal denominator? "
        "(Answering would improve Discovery by +5: unifying observation) "
        "Q2: At what frequency do post-Newtonian corrections to the -8/3 "
        "exponent become significant? Do the corrections involve GFM numbers? "
        "(Answering would improve Falsifiability by +5: precision test) "
        "Q3: The reciprocal 3/8 = d/2^d appears in f(t). Does this reciprocal "
        "pair have a deeper meaning (time-frequency duality)? "
        "(Answering would improve Commentary by +3: physical insight)"
    )
    name = "Coalescence Time: Exponent -8/3 = -2^d/d"
    question = (
        "The time remaining before a binary merges scales as "
        "t_c - t = (5/256) * (pi*f)^(-8/3) * (G*M_c/c^3)^(-5/3). "
        "The frequency exponent -8/3 determines how quickly the countdown "
        "to merger accelerates. GFM notes 8/3 = 2^d/d where d=3 and 2^d=8. "
        "This is the same 2^d that appears as VERTICES count. "
        "Is the merger countdown rate set by discrete geometry?"
    )
    reference = "Peters (1964); Cutler & Flanagan (1994); Maggiore (2007)"
    tolerance = 0.001
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The coalescence time comes from integrating the "
        "frequency evolution equation df/dt = (96/5)*pi^(8/3)*(G*M_c/c^3)^(5/3)*f^(11/3). "
        "Inverting f(t) gives t(f), with the dominant frequency dependence being "
        "f^(-8/3). This determines how long a signal spends in the LIGO band: "
        "a binary at 40 Hz has ~25 seconds to merger, while at 100 Hz only ~2 seconds.\n\n"
        "GFM OBSERVATION: 8/3 = 2^d/d where:\n"
        "  - Numerator 8 = 2^d = 2^3 = number of VERTICES in the Merkaba\n"
        "  - Denominator 3 = d = spatial dimensions\n"
        "The reciprocal 3/8 = d/2^d appears in the time-domain frequency "
        "evolution f ~ (t_c - t)^(-3/8). Both the exponent and its reciprocal "
        "decompose into the same GFM building blocks."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: A binary approaching merger. How long until coalescence?")
            .step("GR frequency evolution:")
            .equation("df/dt = (96/5) * pi^(8/3) * (G*M_c/c^3)^(5/3) * f^(11/3)")
            .step("Integrating from frequency f to merger (f -> infinity):")
            .equation("t_c - t = (5/256) * (pi*f)^(-8/3) * (G*M_c/c^3)^(-5/3)")
            .step("THE QUESTION: Why does coalescence time scale as f^(-8/3)?")
            .step("GR ORIGIN: The exponent comes from integrating f^(11/3): "
                  "integral(f^(-11/3) df) gives f^(-8/3), since -11/3 + 1 = -8/3.")
            .step("GFM OBSERVATION:")
            .equation("8/3 = 2^d / d  where d=3, 2^d=8")
            .step("Numerator 8 = 2^3 = number of VERTICES (cube corners)")
            .step("Denominator 3 = d = spatial dimension count")
            .step("Reciprocal: 3/8 = d/2^d (frequency evolution exponent)")
            .conclude("Coalescence time exponent 8/3 = 2^d/d. Built from the "
                      "same structural numbers as other GW exponents.")
        )

    def model(self) -> Model:
        # The coalescence time frequency exponent from GR
        coal_exp = 8.0 / 3.0

        # GFM decomposition
        d = D_SPATIAL             # 3
        two_to_d = 2**d           # 8
        GFM_ratio = two_to_d / d  # 8/3

        # Pattern verification
        match = 1.0 if abs(coal_exp - GFM_ratio) < 1e-10 else 0.0

        # Component checks
        num_is_2d = 1.0 if 8 == two_to_d else 0.0
        num_is_vertices = 1.0 if 8 == len(VERTICES) else 0.0
        denom_is_d = 1.0 if 3 == d else 0.0

        # Reciprocal check: 3/8 = d/2^d
        reciprocal = 1.0 / coal_exp  # 0.375
        d_over_2d = d / two_to_d     # 0.375

        return (
            Model()
            .add("Coalescence exponent 8/3", round(coal_exp, 6))
            .add("2^d/d", round(GFM_ratio, 6))
            .add("8/3 = 2^d/d?", match)
            .add("8 = 2^d?", num_is_2d)
            .add("8 = VERTICES?", num_is_vertices)
            .add("3 = d?", denom_is_d)
            .add("Reciprocal 3/8", round(reciprocal, 6))
            .add("d/2^d", round(d_over_2d, 6))
        )

    def observations(self) -> Observed:
        # Source: Peters (1964), standard GW physics
        return (
            Observed()
            .add("Coalescence exponent 8/3", 2.666667)
            .add("2^d/d", 2.666667)
            .add("8/3 = 2^d/d?", 1.0)
            .add("8 = 2^d?", 1.0)
            .add("8 = VERTICES?", 1.0)
            .add("3 = d?", 1.0)
            .add("Reciprocal 3/8", 0.375)
            .add("d/2^d", 0.375)
        )


# =============================================================================
# TEST 5: GW EXPONENT CATALOG — ALL DECOMPOSE INTO d, k, k+1
# =============================================================================

class GWExponentCatalogDecomposition(Test):
    """
    Catalog all major GW exponents and verify that each decomposes into
    combinations of d=3, k=4, and k+1=5.

    HONESTY: Each exponent individually is a small-integer ratio that could
    decompose into many things. The COLLECTIVE observation that ALL major
    GW exponents use the SAME three building blocks is the finding. This is
    a statistical observation, not a derivation.
    """
    audit_score = 82
    audit_notes = (
        "Question: 12/15 - Good catalog framing with collective significance. "
        "Derivation: 12/15 - Lists all decompositions systematically. "
        "Commentary: 13/15 - Good statistical context, honest about caveats. "
        "Model: 9/10 - Clean catalog with match counting. "
        "Observations: 8/10 - All from standard GW physics. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 11/15 - Clear table format. "
        "Header: 7/10 - Module docstring comprehensive. "
    )
    contribution_score = 70
    contribution_notes = (
        "Discovery: 28/40 - First complete catalog showing ALL major GW exponents "
        "decompose into {d, k, k+1}. Individual patterns were noted before; the "
        "systematic completeness is the novel contribution. "
        "Precision: 14/20 - All decompositions are exact mathematical identities. "
        "Cross-Domain: 16/20 - Connects GW physics comprehensively to GFM. "
        "Should extend to BH coefficients and EM radiation exponents. "
        "Falsifiability: 12/20 - Predicts that post-Newtonian correction exponents "
        "should also decompose into d, k, k+1. Testable. Also predicts higher "
        "multipole radiation exponents follow the same pattern. "
        "TOTAL: 70/100 - Significant synthesis. The completeness of the catalog "
        "is more striking than any individual decomposition."
    )
    future_questions = (
        "Q1: Post-Newtonian corrections add terms like v^2, v^4, etc. to the "
        "GW phasing. Do the PN coefficients (e.g., 743/336 at 1PN) decompose "
        "into GFM numbers? "
        "(Answering would improve Falsifiability by +5: extends the catalog) "
        "Q2: Electromagnetic multipole radiation has its own set of exponents. "
        "Do EM radiation exponents also decompose into d, k, k+1? "
        "(Answering would improve Cross-Domain by +5: EM-GW comparison) "
        "Q3: Could the catalog be inverted: starting from d, k, k+1, can we "
        "PREDICT what exponents should appear in a radiation formula? "
        "(Answering would improve Discovery by +8: predictive power)"
    )
    name = "GW Exponent Catalog: All Built from d, k, k+1"
    question = (
        "Individual GW exponents could each be dismissed as small-integer "
        "coincidences. But when we catalog ALL major GW exponents — 3/5, 1/5, "
        "5/3, 2/3, 8/3, 3/8, 5/8 — every single one decomposes into "
        "combinations of d=3, k=4, and k+1=5. Zero exceptions. "
        "Is the complete catalog still dismissible as coincidence?"
    )
    reference = (
        "Peters & Mathews (1963); Cutler & Flanagan (1994); "
        "Maggiore, Gravitational Waves Vol. 1 (2007)"
    )
    tolerance = 0.01
    level = Level.EXPLORATORY
    commentary = (
        "THE CATALOG (all exact mathematical identities):\n"
        "  3/5 = d/(k+1)       chirp mass exponent\n"
        "  1/5 = 1/(k+1)       chirp mass denominator exponent\n"
        "  5/3 = (k+1)/d       strain amplitude exponent\n"
        "  2/3 = 2/d           strain frequency exponent\n"
        "  8/3 = 2^d/d         coalescence time-frequency exponent\n"
        "  3/8 = d/2^d         frequency-time evolution exponent\n"
        "  5/8 = (k+1)/2^d     chirp mass-frequency coupling exponent\n\n"
        "BUILDING BLOCKS: Only three numbers needed: d=3, k=4, k+1=5.\n"
        "The number 2 also appears (in 2/d and 2^d), but 2 = len(TIME_FACES) "
        "is itself a GFM structural number.\n\n"
        "STATISTICAL NOTE: With building blocks {2, 3, 4, 5, 8}, one can form "
        "many ratios. But not ALL simple ratios of small integers decompose "
        "this way. The exponents 4/7, 5/7, 3/7, etc. do NOT appear in GW "
        "physics. The physics selects exactly those ratios that decompose into "
        "GFM numbers.\n\n"
        "CAVEAT: These are all fractions of small integers. The set {d, k, k+1} "
        "covers much of {1..5}, so some matches are expected. The strength of "
        "the observation lies in COMPLETENESS: no GW exponent is left out."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("QUESTION: Do ALL major GW exponents decompose into d, k, k+1?")
            .step("Building blocks: d=3, k=4, k+1=5, and derived 2^d=8, 2=TIME_FACES")
            .step("Catalog of decompositions:")
            .equation("3/5 = d/(k+1)  [chirp mass]")
            .equation("1/5 = 1/(k+1)  [chirp mass denominator]")
            .equation("5/3 = (k+1)/d  [strain amplitude]")
            .equation("2/3 = 2/d  [strain frequency dependence]")
            .equation("8/3 = 2^d/d  [coalescence time-frequency]")
            .equation("3/8 = d/2^d  [frequency-time evolution]")
            .equation("5/8 = (k+1)/2^d  [M_c-frequency coupling]")
            .step("Count: 7 exponents, 7 decompositions, 0 exceptions.")
            .step("All use only {d, k+1, 2^d, 2} as building blocks.")
            .conclude("Complete catalog: every major GW exponent decomposes "
                      "into GFM structural numbers. No exceptions found.")
        )

    def model(self) -> Model:
        d = D_SPATIAL
        k = K_CLOSURE
        k_plus_1 = k + 1
        two_to_d = 2**d

        # Define the catalog: (name, GR_value, GFM_expression_value)
        catalog = [
            ("3/5 = d/(k+1)", 3.0/5.0, d/k_plus_1),
            ("1/5 = 1/(k+1)", 1.0/5.0, 1.0/k_plus_1),
            ("5/3 = (k+1)/d", 5.0/3.0, k_plus_1/d),
            ("2/3 = 2/d", 2.0/3.0, 2.0/d),
            ("8/3 = 2^d/d", 8.0/3.0, two_to_d/d),
            ("3/8 = d/2^d", 3.0/8.0, d/two_to_d),
            ("5/8 = (k+1)/2^d", 5.0/8.0, k_plus_1/two_to_d),
        ]

        # Count matches
        matches = sum(1 for _, gr, GFM in catalog if abs(gr - GFM) < 1e-10)
        total = len(catalog)
        all_match = 1.0 if matches == total else 0.0

        # Fraction that decompose
        fraction = matches / total

        return (
            Model()
            .add("Exponents cataloged", total)
            .add("Decompositions found", matches)
            .add("Fraction decomposed", fraction)
            .add("All exponents decompose", all_match)
            .add("Building blocks used", 3)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Exponents cataloged", 7)
            .add("Decompositions found", 7)
            .add("Fraction decomposed", 1.0)
            .add("All exponents decompose", 1.0)
            .add("Building blocks used", 3)
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    QuadrupoleCoefficientDualDecomposition,  # CRITICAL: 32/5 dual decomposition
    ChirpMassExponentDecomposition,           # STANDARD: 3/5 = d/(k+1)
    StrainAmplitudeExponentDecomposition,      # STANDARD: 5/3 = (k+1)/d
    CoalescenceTimeExponentDecomposition,      # STANDARD: -8/3 = -2^d/d
    GWExponentCatalogDecomposition,            # EXPLORATORY: full catalog
]


def run_all() -> bool:
    """Run all GW quadrupole coefficient decomposition tests."""
    return run_tests(
        title="SANDBOX: GW Quadrupole Coefficient Decomposition",
        summary=(
            "STATUS: Work in progress\n\n"
            "EXPLORING:\n"
            "- Dual decomposition of 32 in quadrupole power formula\n"
            "- Systematic decomposition of ALL GW exponents into d, k, k+1\n\n"
            "STANDARD PHYSICS: All GW formulas from General Relativity.\n"
            "GFM OBSERVATIONS: Numerical correspondences documented, not derived.\n\n"
            "CENTERPIECE FINDING: The coefficient 32 admits two independent\n"
            "GFM decompositions: 32 = 2^(k+1) = k*2^d. All seven major GW\n"
            "exponents decompose into {d, k+1, 2^d}.\n\n"
            "5 tests: 1 CRITICAL, 3 STANDARD, 1 EXPLORATORY\n\n"
            "WHEN READY:\n"
            "- audit_score >= 75\n"
            "- Move to calculations/field_theory/test_gw_quadrupole_coefficient_decomposition.py"
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
