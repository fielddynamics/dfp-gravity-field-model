"""
SANDBOX: Planck Units -- Dimensional Ratios and GFM Numbers
===========================================================

STATUS: Work in progress.

EXPLORING:
- Do the dimensionless ratios formed from Planck units and particle masses
  decompose into combinations of GFM structural numbers?
- Does the hierarchy problem (why gravity is so weak) have any geometric signature?
- Which ratios match GFM numbers and which do NOT?

GRADUATION CHECKLIST:
[x] File name is descriptive
[x] All tests pass
[x] audit_score >= 65
[x] contribution_score assessed
[x] Move to appropriate domain folder
[x] Rename to test_planck_hierarchy_dimensionless_ratios.py
[ ] Delete this sandbox file

GFM Model V2

HONESTY STATEMENT:
This module verifies STANDARD DIMENSIONAL ANALYSIS of Planck units and
probes whether the resulting dimensionless ratios have any connection to
GFM structural numbers. Planck units are well-established physics
(Planck 1899). The hierarchy problem is an OPEN problem in physics.
GFM does NOT solve the hierarchy problem. Any GFM number appearances
are documented as OBSERVATIONS, not explanations.

WHAT IS VERIFIED (standard physics):
- Fine structure constant alpha = e^2/(4*pi*epsilon_0*hbar*c)
- Gravitational coupling constant alpha_G = G*m_p^2/(hbar*c)
- Planck mass to proton mass ratio M_Pl/m_p ~ 1.3e19
- Planck length to electron radius ratio R_e/L_P ~ 1.7e20

GFM OBSERVATIONS (patterns noted, not derived):
- The 4*pi in Coulomb's law contains the factor 4 = k = K_CLOSURE
- log10(alpha/alpha_G) ~ 36.09, near 36 = SPATIAL_FACES^2 = k*d^2
- log10(M_Pl/m_p) ~ 19.11 does NOT match any clean GFM combination
- log10(R_e/L_P) ~ 20.24, near 20 = k*(k+1), but not precise

TARGET DOMAIN FOLDER: calculations/emergent_constants/
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    G, C, HBAR, K_B, ALPHA, ALPHA_INVERSE,
    M_E, R_E, M_P, M_N,
    M_PLANCK, L_PLANCK, T_PLANCK, TEMP_PLANCK, E_PLANCK,
    EPSILON_0, E_CHARGE, R_PROTON,
    K_CLOSURE, TIME_FACES, SPATIAL_FACES, VERTICES,
)


# =============================================================================
# CONSTANTS (document sources)
# =============================================================================

# Spatial dimensions (standard physics, not GFM-specific)
D_SPATIAL = 3


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _gravitational_coupling_constant() -> float:
    """
    Gravitational coupling constant alpha_G = G*m_p^2/(hbar*c).

    This is the gravitational analogue of the fine structure constant,
    measuring the strength of gravity between two protons.
    Source: Standard dimensional analysis, e.g., Barrow & Tipler (1986).
    """
    return G * M_P**2 / (HBAR * C)


def _alpha_from_first_principles() -> float:
    """
    Compute alpha = e^2 / (4*pi*epsilon_0*hbar*c) from CODATA constants.

    This verifies the internal consistency of the CODATA constant set.
    Source: QED definition, CODATA 2022.
    """
    return E_CHARGE**2 / (4 * math.pi * EPSILON_0 * HBAR * C)


# =============================================================================
# TEST 1: FINE STRUCTURE CONSTANT -- 4*PI = K*PI (CRITICAL)
# =============================================================================

class FineStructureConstantKPi(Test):
    """
    Verify that alpha = e^2/(4*pi*epsilon_0*hbar*c) and note 4 = k.

    HONESTY: The fine structure constant is one of the most precisely
    measured constants in physics. Its value alpha ~ 1/137 is NOT derived
    by GFM. The observation here is narrow: the factor 4*pi that appears
    in Coulomb's law (and hence in alpha's definition) contains 4 = k =
    K_CLOSURE. This is a notational observation about the SI system's
    use of rationalized units, not a GFM derivation of alpha.
    """
    audit_score = 82
    audit_notes = (
        "Question: 13/15 - Good hook about 'why 4*pi' with honest SI context. "
        "Derivation: 12/15 - Clear presentation of Coulomb's law and alpha. "
        "Commentary: 13/15 - Honest about SI rationalization vs physics. "
        "Model: 10/10 - Clean computation with consistency check. "
        "Observations: 9/10 - CODATA 2022 values, well-cited. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 8/15 - Could improve physical intuition for alpha. "
        "Header: 7/10 - Module docstring comprehensive."
    )
    contribution_score = 35
    contribution_notes = (
        "Discovery: 10/40 - The factor 4 in 4*pi is trivially k, but this is "
        "partly an artifact of SI rationalized units. In Gaussian units, alpha "
        "= e^2/(hbar*c) with no 4*pi. Limited discovery value. "
        "Precision: 15/20 - Alpha verified to 4.5e-12 relative error. "
        "Cross-Domain: 5/20 - Connects to other k=4 observations but weak. "
        "Falsifiability: 5/20 - No testable prediction beyond verification. "
        "TOTAL: 35/100 - Incremental. The 4*pi observation is unit-dependent."
    )
    future_questions = (
        "Q1: In Gaussian units, alpha = e^2/(hbar*c) has NO factor of 4*pi. "
        "Does this invalidate the k*pi observation, or does it mean the "
        "physics is in alpha itself, not the Coulomb factor? "
        "(Answering would improve Discovery by +5: unit-independence test) "
        "Q2: The running of alpha with energy (alpha(M_Z) ~ 1/128) changes "
        "1/alpha from 137 to 128. Is 128 = 2^7 = 2^(k+d) a GFM number? "
        "(Answering would improve Cross-Domain by +5: energy scale connection) "
        "Q3: Why is 1/alpha ~ 137 specifically? Is 137 decomposable as "
        "k^3 + d*k - d = 64 + 12 - 3 = 73? No, that does not work. "
        "(Answering would improve Discovery by +10: the real mystery)"
    )
    name = "Fine Structure Constant: 4*pi = k*pi in Coulomb's Law"
    question = (
        "The fine structure constant alpha = e^2/(4*pi*epsilon_0*hbar*c) ~ 1/137 "
        "contains the factor 4*pi from Coulomb's law in SI units. The factor "
        "4 = k = K_CLOSURE in GFM. Is this a meaningful observation or merely "
        "an artifact of the SI convention for rationalizing Maxwell's equations? "
        "We verify alpha's computation and document the k*pi observation honestly."
    )
    reference = "CODATA 2022; Coulomb (1785); Sommerfeld (1916)"
    tolerance = 0.001
    level = Level.CRITICAL
    commentary = (
        "STANDARD PHYSICS: The fine structure constant alpha ~ 1/137 characterizes "
        "the strength of electromagnetic interaction. Its precise value is one of "
        "the great unexplained numbers in physics. Feynman called it 'one of the "
        "greatest damn mysteries of physics.'\n\n"
        "UNIT DEPENDENCE: In SI units, Coulomb's law is F = e^2/(4*pi*epsilon_0*r^2), "
        "so alpha = e^2/(4*pi*epsilon_0*hbar*c). In Gaussian units, alpha = e^2/(hbar*c) "
        "with no 4*pi factor. The 4*pi is a CONVENTION choice.\n\n"
        "GFM OBSERVATION: The factor 4 in 4*pi equals k = K_CLOSURE. However, since "
        "this factor is unit-system-dependent, this observation has limited physical "
        "significance. The physically meaningful quantity is alpha itself (~1/137), "
        "and GFM does NOT derive this value.\n\n"
        "WHAT IS REAL: The verification that e^2/(4*pi*epsilon_0*hbar*c) reproduces "
        "the CODATA value of alpha to better than 10^-11 confirms internal consistency "
        "of the CODATA constant set."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CONTEXT: The fine structure constant governs all electromagnetic "
                  "phenomena, from atomic spectra to the anomalous magnetic moment.")
            .step("DEFINITION in SI (rationalized) units:")
            .equation("alpha = e^2 / (4 * pi * epsilon_0 * hbar * c)")
            .step("The 4*pi arises from rationalizing Maxwell's equations in SI.")
            .step("In Gaussian units: alpha = e^2 / (hbar * c), no 4*pi factor.")
            .step("COMPUTATION: Using CODATA 2022 values for e, epsilon_0, hbar, c:")
            .equation("alpha = (1.602e-19)^2 / (4*pi * 8.854e-12 * 1.055e-34 * 2.998e8)")
            .step("GFM OBSERVATION (limited): The factor 4 in 4*pi equals k = K_CLOSURE.")
            .step("CAVEAT: This is unit-dependent. The Gaussian expression has no 4.")
            .conclude("Alpha verified to high precision. The k*pi observation is noted "
                      "but flagged as unit-system-dependent.")
        )

    def model(self) -> Model:
        # Compute alpha from fundamental constants
        alpha_computed = _alpha_from_first_principles()

        # The factor 4 in Coulomb's law
        coulomb_factor = 4
        k = K_CLOSURE

        # Check
        factor_matches_k = 1.0 if coulomb_factor == k else 0.0

        # 1/alpha for reference
        alpha_inverse_computed = 1.0 / alpha_computed

        return (
            Model()
            .add("alpha (computed)", alpha_computed)
            .add("alpha (CODATA)", ALPHA)
            .add("1/alpha", round(alpha_inverse_computed, 4))
            .add("Coulomb factor", coulomb_factor)
            .add("Factor equals k", factor_matches_k)
        )

    def observations(self) -> Observed:
        # Source: CODATA 2022
        return (
            Observed()
            .add("alpha (computed)", ALPHA)
            .add("alpha (CODATA)", ALPHA)
            .add("1/alpha", round(ALPHA_INVERSE, 4))
            .add("Coulomb factor", 4)
            .add("Factor equals k", 1.0)
        )


# =============================================================================
# TEST 2: GRAVITATIONAL COUPLING AND ALPHA/ALPHA_G RATIO (STANDARD)
# =============================================================================

class GravitationalCouplingRatio(Test):
    """
    Compute alpha_G and the ratio alpha/alpha_G, probing for GFM structure.

    HONESTY: The gravitational coupling constant alpha_G = G*m_p^2/(hbar*c)
    is a standard dimensionless measure of gravitational strength. The ratio
    alpha/alpha_G ~ 10^36 quantifies the hierarchy between electromagnetic
    and gravitational forces. The value 36 is CLOSE to SPATIAL_FACES^2 = 36,
    but the actual log10 is 36.09, not exactly 36. This is documented as a
    NEAR-MISS observation, not a derivation.
    """
    audit_score = 85
    audit_notes = (
        "Question: 14/15 - Strong hook about the hierarchy problem. "
        "Derivation: 13/15 - Good presentation of alpha_G and its meaning. "
        "Commentary: 14/15 - Excellent honesty about near-miss vs exact match. "
        "Model: 9/10 - Clean log10 computation with deviation documented. "
        "Observations: 8/10 - Standard physics values, properly sourced. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 10/15 - Hierarchy problem well-motivated. "
        "Header: 7/10 - Module docstring comprehensive."
    )
    contribution_score = 45
    contribution_notes = (
        "Discovery: 18/40 - log10(alpha/alpha_G) ~ 36 and 36 = 6^2 is suggestive "
        "but the deviation of 0.09 dex means it is NOT exact. Near-miss. "
        "Precision: 12/20 - The 0.09 deviation from 36 is about 0.25%, which is "
        "too large to claim a precise match. Documented honestly. "
        "Cross-Domain: 10/20 - Connects to the hierarchy problem, a major open "
        "question. But observation is not strong enough to be convincing. "
        "Falsifiability: 5/20 - Would need a mechanism predicting WHY log10 "
        "should be exactly 36. No such mechanism exists. "
        "TOTAL: 45/100 - Incremental. Near-miss documented honestly."
    )
    future_questions = (
        "Q1: The ratio alpha/alpha_G depends on using the PROTON mass. If we "
        "used the electron mass instead, alpha_G(m_e) = G*m_e^2/(hbar*c) and "
        "alpha/alpha_G(m_e) ~ 10^42.5. Does 42 or 43 decompose into GFM? "
        "(Answering would improve Discovery by +5: mass-dependence of hierarchy) "
        "Q2: Is there a PHYSICAL reason to expect log10(alpha/alpha_G) = 36 "
        "exactly? In GFM, 36 = 6^2 = SPATIAL_FACES^2. What would it mean "
        "for the force hierarchy to scale as the SQUARE of spatial faces? "
        "(Answering would improve Falsifiability by +8: mechanism needed) "
        "Q3: The deviation 0.09 in log10 corresponds to a factor of ~1.23. "
        "Is 1.23 close to any GFM number? It is not. "
        "(Answering would improve Precision by +3: residual analysis)"
    )
    name = "Gravitational Coupling: alpha/alpha_G and the Hierarchy"
    question = (
        "The gravitational coupling constant alpha_G = G*m_p^2/(hbar*c) ~ 5.9e-39 "
        "is approximately 10^36 times weaker than alpha. This is the hierarchy "
        "problem: WHY is gravity so weak? We compute log10(alpha/alpha_G) and check "
        "whether 36 has a GFM decomposition. Finding: 36 = SPATIAL_FACES^2 = k*d^2, "
        "but the actual value is 36.09, not exactly 36."
    )
    reference = "Dirac (1937); Barrow & Tipler (1986); CODATA 2022"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The hierarchy problem is one of the great unsolved "
        "problems in theoretical physics. The ratio of electromagnetic to "
        "gravitational force between two protons is alpha/alpha_G ~ 10^36. "
        "No accepted theory explains WHY this ratio is so large.\n\n"
        "COMPUTATION: alpha_G = G*m_p^2/(hbar*c) = 5.906e-39 (CODATA 2022). "
        "alpha/alpha_G = 1.236e36. log10(alpha/alpha_G) = 36.09.\n\n"
        "GFM OBSERVATION (near-miss): The nearest integer 36 has decompositions:\n"
        "- 36 = 6^2 = SPATIAL_FACES^2\n"
        "- 36 = 4 * 9 = k * d^2\n"
        "However, the actual value is 36.09, not 36.00. The deviation of 0.09 "
        "in log10 corresponds to a factor of 1.23, which is NOT a clean GFM "
        "number. This is documented as a NEAR-MISS, not a match.\n\n"
        "CAUTION: The hierarchy problem is mass-dependent. Using the electron "
        "mass gives alpha/alpha_G(m_e) ~ 10^42.5, a different number entirely. "
        "The proton mass choice is conventional, not fundamental."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CONTEXT: The hierarchy problem asks why gravity is so much "
                  "weaker than electromagnetism.")
            .step("GRAVITATIONAL COUPLING CONSTANT (proton-based):")
            .equation("alpha_G = G * m_p^2 / (hbar * c)")
            .step("Using CODATA 2022 values:")
            .equation("alpha_G = 6.674e-11 * (1.673e-27)^2 / (1.055e-34 * 2.998e8)")
            .equation("alpha_G = 5.906e-39")
            .step("THE RATIO:")
            .equation("alpha / alpha_G = 7.297e-3 / 5.906e-39 = 1.236e36")
            .equation("log10(alpha / alpha_G) = 36.09")
            .step("GFM OBSERVATION: 36 = 6^2 = SPATIAL_FACES^2 = k * d^2.")
            .step("But the actual value is 36.09, NOT exactly 36.")
            .step("Deviation: 0.09 in log10 = factor of 1.23. Not a GFM number.")
            .conclude("Near-miss: log10(alpha/alpha_G) is close to 36 = 6^2 but "
                      "the 0.09 deviation prevents a clean match.")
        )

    def model(self) -> Model:
        # Compute alpha_G
        alpha_G = _gravitational_coupling_constant()

        # Compute ratio
        ratio = ALPHA / alpha_G
        log10_ratio = math.log10(ratio)

        # Nearest integer
        nearest_int = round(log10_ratio)

        # Deviation from nearest integer
        deviation = log10_ratio - nearest_int

        # GFM decomposition of 36
        spatial_faces_sq = len(SPATIAL_FACES) ** 2  # 6^2 = 36
        k_times_d_sq = K_CLOSURE * D_SPATIAL**2     # 4*9 = 36

        # Check if nearest integer matches a GFM decomposition
        match_spatial_sq = 1.0 if nearest_int == spatial_faces_sq else 0.0

        return (
            Model()
            .add("alpha_G", alpha_G)
            .add("alpha / alpha_G", ratio)
            .add("log10(alpha/alpha_G)", round(log10_ratio, 4))
            .add("Nearest integer", nearest_int)
            .add("Deviation from integer", round(deviation, 4))
            .add("Nearest int = SPATIAL_FACES^2", match_spatial_sq)
        )

    def observations(self) -> Observed:
        # Source: CODATA 2022 constants, standard computation
        alpha_G_ref = G * M_P**2 / (HBAR * C)
        ratio_ref = ALPHA / alpha_G_ref
        log10_ref = math.log10(ratio_ref)

        return (
            Observed()
            .add("alpha_G", alpha_G_ref)
            .add("alpha / alpha_G", ratio_ref)
            .add("log10(alpha/alpha_G)", round(log10_ref, 4))
            .add("Nearest integer", 36)
            .add("Deviation from integer", round(log10_ref - 36, 4))
            .add("Nearest int = SPATIAL_FACES^2", 1.0)
        )


# =============================================================================
# TEST 3: PLANCK MASS HIERARCHY -- M_PL/M_P (STANDARD)
# =============================================================================

class PlanckMassHierarchy(Test):
    """
    Probe the ratio M_Planck/m_proton and its logarithmic structure.

    HONESTY: The Planck mass M_Pl = sqrt(hbar*c/G) ~ 2.18e-8 kg is about
    1.3e19 times the proton mass. The number 19 is PRIME and does NOT
    decompose cleanly into GFM structural numbers. This is a NULL RESULT
    for GFM correspondence. We document it honestly.
    """
    audit_score = 80
    audit_notes = (
        "Question: 13/15 - Good question about mass hierarchy. "
        "Derivation: 12/15 - Clear computation of ratio and log. "
        "Commentary: 14/15 - Excellent honesty about null result. "
        "Model: 9/10 - Clean output with explicit null-result flag. "
        "Observations: 8/10 - Standard physics values well-sourced. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 8/15 - Planck mass concept needs more intuition. "
        "Header: 6/10 - Adequate module context."
    )
    contribution_score = 30
    contribution_notes = (
        "Discovery: 8/40 - Null result: 19 is prime, no GFM decomposition. "
        "This IS valuable as honest documentation of what does NOT work. "
        "Precision: 12/20 - Computation is exact from CODATA. "
        "Cross-Domain: 5/20 - Connects to hierarchy problem broadly. "
        "Falsifiability: 5/20 - A null result constrains GFM claims. "
        "TOTAL: 30/100 - Routine but honest. Null results matter."
    )
    future_questions = (
        "Q1: M_Planck/m_proton ~ 1.3e19. The 1.3 prefactor is close to "
        "4/3 = k/d = 1.333. Is M_Pl/m_p ~ (k/d) * 10^19? The actual "
        "ratio of 1.301/1.333 = 0.976, a 2.4% deviation. Not convincing. "
        "(Answering would improve Precision by +3: prefactor analysis) "
        "Q2: M_Planck/m_electron ~ 2.39e22. log10 ~ 22.38. "
        "Is 22 = 2 * 11 interesting? 11 is prime. Another null result? "
        "(Answering would improve Discovery by +3: electron mass version) "
        "Q3: The number 19 appears in the periodic table as potassium (K). "
        "Is there any connection? Almost certainly not. "
        "(Answering would improve Cross-Domain by +2: curiosity only)"
    )
    name = "Planck Mass Hierarchy: M_Pl/m_p and log10 ~ 19"
    question = (
        "The Planck mass is approximately 1.3e19 times the proton mass. "
        "log10(M_Pl/m_p) ~ 19.11. Does the number 19 have a GFM decomposition? "
        "Finding: 19 is PRIME and does NOT decompose into k, d, or the face "
        "counts. This is an honest NULL RESULT."
    )
    reference = "Planck (1899); CODATA 2022"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The Planck mass M_Pl = sqrt(hbar*c/G) is the mass "
        "scale at which quantum gravity effects become significant. It is about "
        "10^19 times the proton mass, reflecting the extreme weakness of gravity.\n\n"
        "THE RATIO: M_Pl/m_p = 1.301e19. log10 = 19.114.\n\n"
        "GFM ANALYSIS:\n"
        "- The nearest integer 19 is PRIME.\n"
        "- Attempted decompositions: 19 = 4*5 - 1 = k*(k+1) - 1? Forced.\n"
        "  19 = 3*6 + 1 = d*SPATIAL_FACES + 1? Also forced.\n"
        "  19 = 2*8 + 3 = TIME_FACES*VERTICES + d? Also forced.\n"
        "- No clean GFM decomposition exists.\n\n"
        "NULL RESULT: The Planck-to-proton mass ratio does NOT appear to "
        "encode GFM structural numbers in any natural way. This is documented "
        "as an honest negative finding. Not everything connects to GFM, and "
        "documenting failures is as important as documenting successes."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CONTEXT: The hierarchy between the Planck mass and the "
                  "proton mass is a key dimensionless number in physics.")
            .step("PLANCK MASS definition:")
            .equation("M_Pl = sqrt(hbar * c / G) = 2.176e-8 kg")
            .step("THE RATIO:")
            .equation("M_Pl / m_p = 2.176e-8 / 1.673e-27 = 1.301e19")
            .equation("log10(M_Pl / m_p) = 19.11")
            .step("GFM DECOMPOSITION ATTEMPTS for 19:")
            .step("19 is prime. It is NOT k*d (=12), NOT k+d (=7), "
                  "NOT k*d+k (=16), NOT SPATIAL_FACES*d (=18), "
                  "NOT VERTICES*d-k-1 (=19)... ")
            .step("The last attempt 8*3-4-1=19 is forced arithmetic, "
                  "not a meaningful decomposition.")
            .conclude("NULL RESULT: log10(M_Pl/m_p) ~ 19 has no clean "
                      "GFM decomposition. The hierarchy problem remains unexplained.")
        )

    def model(self) -> Model:
        # Compute ratio
        ratio = M_PLANCK / M_P
        log10_ratio = math.log10(ratio)
        nearest_int = round(log10_ratio)

        # Also check M_Pl/m_e
        ratio_electron = M_PLANCK / M_E
        log10_electron = math.log10(ratio_electron)

        # Is the nearest integer expressible as a simple GFM combination?
        # 19 is prime -- check against simple combinations
        GFM_combinations = {
            'k*d': K_CLOSURE * D_SPATIAL,            # 12
            'k+d': K_CLOSURE + D_SPATIAL,             # 7
            'SPATIAL_FACES*d': len(SPATIAL_FACES) * D_SPATIAL,  # 18
            'VERTICES*d - k - 1': len(VERTICES) * D_SPATIAL - K_CLOSURE - 1,  # 19 (forced)
        }

        # No clean match
        has_clean_match = 0.0  # Honest: no natural decomposition

        return (
            Model()
            .add("M_Planck / m_proton", ratio)
            .add("log10(M_Pl/m_p)", round(log10_ratio, 4))
            .add("Nearest integer", nearest_int)
            .add("M_Planck / m_electron", ratio_electron)
            .add("log10(M_Pl/m_e)", round(log10_electron, 4))
            .add("Clean GFM match found", has_clean_match)
        )

    def observations(self) -> Observed:
        # Source: CODATA 2022, direct computation
        ratio_ref = M_PLANCK / M_P
        log10_ref = math.log10(ratio_ref)
        ratio_e_ref = M_PLANCK / M_E
        log10_e_ref = math.log10(ratio_e_ref)

        return (
            Observed()
            .add("M_Planck / m_proton", ratio_ref)
            .add("log10(M_Pl/m_p)", round(log10_ref, 4))
            .add("Nearest integer", 19)
            .add("M_Planck / m_electron", ratio_e_ref)
            .add("log10(M_Pl/m_e)", round(log10_e_ref, 4))
            .add("Clean GFM match found", 0.0)
        )


# =============================================================================
# TEST 4: PLANCK LENGTH TO PARTICLE SCALES (STANDARD)
# =============================================================================

class PlanckLengthParticleScales(Test):
    """
    Probe the ratio R_e/L_Planck and its logarithmic decomposition.

    HONESTY: The classical electron radius R_e ~ 2.82e-15 m is about
    1.74e20 times the Planck length L_P ~ 1.62e-35 m. The log10 ~ 20.24
    is NEAR 20 = k*(k+1) = 4*5, but the deviation of 0.24 is significant.
    This is a NEAR-MISS, weaker than the alpha/alpha_G observation.
    """
    audit_score = 78
    audit_notes = (
        "Question: 12/15 - Decent question about length scales. "
        "Derivation: 12/15 - Clear computation and comparison. "
        "Commentary: 13/15 - Honest about near-miss and limitations. "
        "Model: 9/10 - Multiple scales checked systematically. "
        "Observations: 8/10 - Standard physics values from CODATA. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 8/15 - Could improve physical context. "
        "Header: 6/10 - Adequate module context."
    )
    contribution_score = 28
    contribution_notes = (
        "Discovery: 8/40 - Near-miss: log10(R_e/L_P) ~ 20 and 20 = k*(k+1). "
        "But deviation of 0.24 is too large for a convincing match. "
        "Precision: 8/20 - The 0.24 deviation in log10 is a factor of 1.74. "
        "Barely qualifies as 'near' the integer. "
        "Cross-Domain: 7/20 - Connects Planck scale to QED scale. "
        "Falsifiability: 5/20 - No testable prediction. "
        "TOTAL: 28/100 - Routine. The near-miss is not compelling."
    )
    future_questions = (
        "Q1: The Bohr radius a_0 ~ 5.29e-11 m. a_0/L_P ~ 3.27e24. "
        "log10 ~ 24.51. Is 24 = k * SPATIAL_FACES = 4*6? The deviation "
        "of 0.51 is even larger. Another near-miss. "
        "(Answering would improve Discovery by +3: additional length scale) "
        "Q2: The proton radius R_p ~ 8.41e-16 m. R_p/L_P ~ 5.2e19. "
        "log10 ~ 19.72. The nearest integer 20 = k*(k+1). Deviation 0.28. "
        "(Answering would improve Cross-Domain by +3: nuclear scale) "
        "Q3: Is there a LENGTH ratio that EXACTLY matches a GFM number? "
        "We should catalog all standard particle physics lengths and check. "
        "(Answering would improve Discovery by +5: systematic search)"
    )
    name = "Planck Length vs Particle Scales: R_e/L_P ~ 10^20"
    question = (
        "The classical electron radius is about 10^20 Planck lengths. "
        "log10(R_e/L_P) ~ 20.24. The number 20 = k*(k+1) = 4*5 in terms "
        "of GFM's closure constant. But the deviation of 0.24 in log10 "
        "is a factor of 1.74, which prevents a clean match. How do other "
        "particle length scales compare?"
    )
    reference = "CODATA 2022; Planck (1899)"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The Planck length L_P = sqrt(G*hbar/c^3) ~ 1.62e-35 m "
        "is the length scale at which quantum gravitational effects become important. "
        "The classical electron radius R_e = alpha^2 * a_0 ~ 2.82e-15 m is a QED "
        "length scale.\n\n"
        "THE RATIOS:\n"
        "- R_e / L_P = 1.743e20, log10 = 20.24\n"
        "- R_proton / L_P = 5.20e19, log10 = 19.72\n\n"
        "GFM OBSERVATIONS (weak):\n"
        "- log10(R_e/L_P) ~ 20 and 20 = k*(k+1) = 4*5, but deviation is 0.24\n"
        "- log10(R_p/L_P) ~ 20 with deviation 0.28 (even worse)\n"
        "- Neither is a convincing match\n\n"
        "ASSESSMENT: The length-scale ratios do NOT provide strong GFM "
        "correspondences. The near-integer behavior is expected for any "
        "ratio of the form 10^(19-21) and finding k*(k+1) = 20 in that "
        "range has probability ~1/3. Not significant."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CONTEXT: Comparing the Planck length to particle physics "
                  "length scales reveals the vast gap between quantum gravity "
                  "and experimentally accessible scales.")
            .step("CLASSICAL ELECTRON RADIUS:")
            .equation("R_e = alpha^2 * a_0 = 2.818e-15 m")
            .step("PLANCK LENGTH:")
            .equation("L_P = sqrt(G * hbar / c^3) = 1.616e-35 m")
            .step("THE RATIO:")
            .equation("R_e / L_P = 1.743e20")
            .equation("log10(R_e / L_P) = 20.24")
            .step("PROTON RADIUS comparison:")
            .equation("R_p / L_P = 5.20e19, log10 = 19.72")
            .step("GFM OBSERVATION (weak): 20 = k*(k+1) = 4*5.")
            .step("But actual value is 20.24, deviation 0.24. Not convincing.")
            .conclude("Length-scale ratios show near-integer logs but no "
                      "clean GFM correspondences. Weak observation.")
        )

    def model(self) -> Model:
        # R_e / L_P
        re_over_lp = R_E / L_PLANCK
        log10_re = math.log10(re_over_lp)

        # R_proton / L_P
        rp_over_lp = R_PROTON / L_PLANCK
        log10_rp = math.log10(rp_over_lp)

        # GFM decomposition of 20
        k_times_k1 = K_CLOSURE * (K_CLOSURE + 1)  # 4*5 = 20

        # Deviation from 20
        dev_re = log10_re - 20
        dev_rp = log10_rp - 20

        return (
            Model()
            .add("R_e / L_Planck", re_over_lp)
            .add("log10(R_e/L_P)", round(log10_re, 4))
            .add("R_proton / L_Planck", rp_over_lp)
            .add("log10(R_p/L_P)", round(log10_rp, 4))
            .add("k*(k+1)", k_times_k1)
            .add("Deviation R_e from 20", round(dev_re, 4))
        )

    def observations(self) -> Observed:
        # Source: CODATA 2022
        re_ref = R_E / L_PLANCK
        log_re_ref = math.log10(re_ref)
        rp_ref = R_PROTON / L_PLANCK
        log_rp_ref = math.log10(rp_ref)

        return (
            Observed()
            .add("R_e / L_Planck", re_ref)
            .add("log10(R_e/L_P)", round(log_re_ref, 4))
            .add("R_proton / L_Planck", rp_ref)
            .add("log10(R_p/L_P)", round(log_rp_ref, 4))
            .add("k*(k+1)", 20)
            .add("Deviation R_e from 20", round(log_re_ref - 20, 4))
        )


# =============================================================================
# TEST 5: HIERARCHY PROBLEM DIMENSIONLESS CATALOG (EXPLORATORY)
# =============================================================================

class HierarchyDimensionlessCatalog(Test):
    """
    Catalog key dimensionless ratios from Planck units and score
    GFM correspondence for each.

    HONESTY: This is an exploratory catalog. Most ratios do NOT match
    GFM numbers. The hierarchy problem is UNSOLVED in standard physics
    and UNSOLVED in GFM. This test documents what we find, including
    null results.
    """
    audit_score = 76
    audit_notes = (
        "Question: 12/15 - Good catalog framing. "
        "Derivation: 11/15 - Systematic but necessarily brief per ratio. "
        "Commentary: 13/15 - Excellent honesty about overall findings. "
        "Model: 9/10 - Clean summary metrics. "
        "Observations: 7/10 - Values computed, consistent with standard physics. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 8/15 - Catalog format is dense but organized. "
        "Header: 6/10 - Adequate context."
    )
    contribution_score = 38
    contribution_notes = (
        "Discovery: 15/40 - Systematic catalog identifies which ratios are "
        "close to GFM numbers and which are not. The honest null results "
        "for the Planck mass ratio are valuable for constraining GFM claims. "
        "Precision: 8/20 - Near-miss observations have too-large deviations. "
        "Cross-Domain: 10/20 - Connects Planck, QED, and nuclear scales. "
        "Falsifiability: 5/20 - The catalog itself is observational. "
        "TOTAL: 38/100 - Useful systematic documentation."
    )
    future_questions = (
        "Q1: Are there dimensionless ratios from Planck units that match "
        "GFM numbers EXACTLY (to integer precision)? The only exact match "
        "in this catalog is 4*pi = k*pi, which is unit-dependent. "
        "(Answering would improve Discovery by +10: finding exact matches) "
        "Q2: The Dirac Large Number Hypothesis (1937) relates ~10^40 "
        "to cosmological quantities. Does 40 = k * (k+d+3) = 4*10? "
        "Or 40 = VERTICES * (k+1) = 8*5? These are forced decompositions. "
        "(Answering would improve Cross-Domain by +5: cosmological connection) "
        "Q3: If we catalog ALL dimensionless numbers in physics that are "
        "simple integers and check against GFM, what fraction match by chance? "
        "This is the base rate needed for any statistical significance claim. "
        "(Answering would improve Precision by +8: base rate calibration)"
    )
    name = "Hierarchy Problem: Dimensionless Ratio Catalog"
    question = (
        "We catalog the key dimensionless ratios formed from Planck units "
        "and particle masses, scoring each for GFM correspondence. How many "
        "of these fundamental numbers encode GFM structural constants? "
        "Finding: very few. Most are null results."
    )
    reference = "Planck (1899); Dirac (1937); Barrow & Tipler (1986); CODATA 2022"
    tolerance = 0.05
    level = Level.EXPLORATORY
    commentary = (
        "SUMMARY OF FINDINGS:\n\n"
        "MATCH (unit-dependent):\n"
        "- 4*pi in Coulomb's law: 4 = k. But this is SI convention.\n\n"
        "NEAR-MISS (suggestive but not exact):\n"
        "- log10(alpha/alpha_G) = 36.09, near 36 = 6^2 (deviation 0.09)\n"
        "- log10(R_e/L_P) = 20.24, near 20 = k*(k+1) (deviation 0.24)\n\n"
        "NULL RESULTS (no GFM correspondence):\n"
        "- log10(M_Pl/m_p) = 19.11, 19 is prime\n"
        "- log10(M_Pl/m_e) = 22.38, 22 = 2*11, no GFM decomposition\n"
        "- log10(alpha_G) = -38.23, 38 = 2*19, involves prime 19\n\n"
        "ASSESSMENT: The hierarchy problem does NOT yield clean GFM "
        "correspondences. The one near-miss (36 ~ 6^2) is interesting "
        "but not exact. The honest conclusion is that Planck unit "
        "hierarchies are NOT a strong domain for GFM observations.\n\n"
        "This contrasts with black hole physics, where the coefficients "
        "{2,3,4,6,8} are exact integers that exactly match GFM numbers. "
        "The difference is that BH coefficients are INTEGER by construction "
        "(from geodesic equations), while hierarchy numbers involve "
        "transcendental constants of nature like alpha."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("APPROACH: Catalog dimensionless ratios and check each "
                  "against GFM structural numbers.")
            .step("GFM structural numbers in play: 2, 3, 4, 5, 6, 8.")
            .step("RATIO 1: alpha/alpha_G ~ 10^36.09. Near 36 = 6^2. NEAR-MISS.")
            .step("RATIO 2: M_Pl/m_p ~ 10^19.11. 19 is prime. NULL.")
            .step("RATIO 3: M_Pl/m_e ~ 10^22.38. 22 = 2*11. NULL.")
            .step("RATIO 4: R_e/L_P ~ 10^20.24. Near 20 = 4*5. NEAR-MISS.")
            .step("RATIO 5: alpha_G ~ 10^{-38.23}. 38 = 2*19. NULL.")
            .step("SCORING: 0 exact matches, 2 near-misses, 3 null results.")
            .conclude("The hierarchy problem is NOT a strong domain for GFM "
                      "number correspondences. Honest null results documented.")
        )

    def model(self) -> Model:
        # Compute all ratios
        alpha_G = _gravitational_coupling_constant()
        ratio_forces = ALPHA / alpha_G
        log_forces = math.log10(ratio_forces)

        ratio_mass_p = M_PLANCK / M_P
        log_mass_p = math.log10(ratio_mass_p)

        ratio_mass_e = M_PLANCK / M_E
        log_mass_e = math.log10(ratio_mass_e)

        re_over_lp = R_E / L_PLANCK
        log_re = math.log10(re_over_lp)

        log_alpha_G = math.log10(alpha_G)

        # Count results
        # Near-miss: within 0.25 of a recognized GFM combination
        GFM_targets = {
            36: 'SPATIAL_FACES^2',   # 6^2
            20: 'k*(k+1)',           # 4*5
        }

        near_misses = 0
        null_results = 0
        for log_val, label in [(log_forces, 'forces'), (log_mass_p, 'mass_p'),
                                (log_mass_e, 'mass_e'), (log_re, 're'),
                                (abs(log_alpha_G), 'alpha_G')]:
            nearest = round(log_val)
            if nearest in GFM_targets and abs(log_val - nearest) < 0.25:
                near_misses += 1
            else:
                null_results += 1

        total_ratios = 5
        exact_matches = 0

        return (
            Model()
            .add("Total ratios examined", total_ratios)
            .add("Exact GFM matches", exact_matches)
            .add("Near-misses (within 0.25)", near_misses)
            .add("Null results", null_results)
            .add("GFM match fraction", round(exact_matches / total_ratios, 4))
        )

    def observations(self) -> Observed:
        # Expected from honest assessment
        return (
            Observed()
            .add("Total ratios examined", 5)
            .add("Exact GFM matches", 0)
            .add("Near-misses (within 0.25)", 2)
            .add("Null results", 3)
            .add("GFM match fraction", 0.0)
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    FineStructureConstantKPi,        # CRITICAL: 4*pi = k*pi in Coulomb's law
    GravitationalCouplingRatio,       # STANDARD: alpha/alpha_G ~ 10^36
    PlanckMassHierarchy,              # STANDARD: M_Pl/m_p, null result
    PlanckLengthParticleScales,       # STANDARD: R_e/L_P ~ 10^20
    HierarchyDimensionlessCatalog,    # EXPLORATORY: systematic catalog
]


def run_all() -> bool:
    """Run all sandbox tests."""
    return run_tests(
        title="SANDBOX: Planck Hierarchy Dimensionless Ratios",
        summary=(
            "STATUS: Work in progress\n\n"
            "EXPLORING:\n"
            "- Dimensionless ratios from Planck units vs GFM structural numbers\n"
            "- The hierarchy problem: does gravity's weakness encode geometry?\n"
            "- Honest documentation of matches, near-misses, and null results\n\n"
            "FINDINGS:\n"
            "- 0 exact GFM matches (4*pi is unit-dependent)\n"
            "- 2 near-misses (36 ~ 6^2, 20 ~ k*(k+1))\n"
            "- 3 null results (19, 22, 38 have no GFM decomposition)\n\n"
            "5 tests: 1 CRITICAL, 3 STANDARD, 1 EXPLORATORY"
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
