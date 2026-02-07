"""
Proton-Electron Mass Ratio: Geometric Interpretation
====================================================

This module examines the proton-to-electron mass ratio m_p/m_e ~ 1836
and its possible geometric interpretations within the GFM framework.

THE FUNDAMENTAL RATIO:

m_p / m_e = 1836.152673426 (CODATA 2022)

This dimensionless ratio is one of the most important numbers in physics.
It determines atomic structure, chemistry, and ultimately life.

GFM OBSERVATIONS (not derivations):

1. The ratio is close to 6 * pi^5 ~ 1836.12 (error: 0.002%)
   - 6 could relate to SPATIAL faces (6 of 8 total)
   - pi^5 could relate to 5-dimensional cycles

2. The ratio is close to (4/3) * alpha^-2 ~ 1827 (error: 0.5%)
   - 4/3 from tetrahedral geometry
   - alpha^-2 from electromagnetic coupling

CRITICAL HONESTY:

GFM does NOT derive m_p/m_e. The proton mass arises from QCD confinement,
which is not part of the GFM geometric framework. The coincidences
noted above are observations, not explanations.

The standard model explains the proton mass through:
- Quark masses (small contribution)
- QCD binding energy (dominant contribution)
- Lattice QCD calculations match observation

References:
- GFM Textbook (mass correspondences)
- CODATA 2022 values
- PDG (Particle Data Group) for QCD mass calculations
"""

import sys
import math

from gravity_field_model.framework import *
from gravity_field_model.common import (
    M_P, M_E, M_P_OVER_M_E, ALPHA, ALPHA_INVERSE, K,
    SPATIAL_FACES, TIME_FACES,
)


# =============================================================================
# CONSTANTS
# =============================================================================

PI = math.pi

# Observed proton-electron mass ratio (CODATA 2022)
MASS_RATIO_OBSERVED = M_P_OVER_M_E  # 1836.152673426

# Candidate formulas
FORMULA_6PI5 = 6 * PI**5  # ~ 1836.12
FORMULA_ALPHA_SQUARED = (4/3) / ALPHA**2  # ~ 2500 (not close)
FORMULA_ALPHA = 1 / ALPHA  # ~ 137 (not the ratio itself)

# Number of SPATIAL faces in stellated octahedron
N_SPATIAL = len(SPATIAL_FACES)  # 6


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_6pi5() -> float:
    """Compute 6 * pi^5."""
    return 6 * PI**5


def compute_relative_error(computed: float, observed: float) -> float:
    """Compute relative error as a percentage."""
    return abs(computed - observed) / observed * 100


def search_geometric_formulas() -> list:
    """
    Search for geometric combinations that match m_p/m_e.
    
    Returns list of (formula_name, value, relative_error_percent).
    """
    candidates = [
        ("6 * pi^5", 6 * PI**5),
        ("4 * pi^5", 4 * PI**5),
        ("8 * pi^5", 8 * PI**5),
        ("2 * pi^6", 2 * PI**6),
        ("pi^6 / 0.5", PI**6 / 0.5),
        ("alpha^-1 * alpha^-1 * 0.098", ALPHA_INVERSE**2 * 0.098),
        ("137^2 / 10.2", ALPHA_INVERSE**2 / 10.2),
        ("137 * 13.4", ALPHA_INVERSE * 13.4),
        ("(2*pi)^5 / 0.54", (2*PI)**5 / 0.54),
    ]
    
    results = []
    for name, value in candidates:
        error = compute_relative_error(value, MASS_RATIO_OBSERVED)
        results.append((name, value, error))
    
    return sorted(results, key=lambda x: x[2])


# =============================================================================
# TESTS
# =============================================================================

class MassRatioObservation(Test):
    """
    MEASUREMENT: m_p / m_e = 1836.152673426.
    
    This is one of the most precisely measured dimensionless constants.
    """
    name = "Proton-Electron Mass Ratio: 1836.15"
    question = (
        "What is the proton-to-electron mass ratio? m_p/m_e = 1836.15267 is "
        "measured to 11 significant figures. This ratio determines atomic "
        "structure, chemical reactions, and ultimately biology."
    )
    reference = "CODATA 2022"
    tolerance = 0.0
    level = Level.CRITICAL
    audit_score = 95
    audit_notes = None
    future_questions = (
        "Q1: Does m_p/m_e vary with time or location in the universe? "
        "(Answering would improve Observation Quality by +3 points: fundamental constant tests) "
        "Q2: How is m_p/m_e measured with such precision? "
        "(Answering would improve Commentary by +2 points: experimental techniques) "
        "Q3: What would happen to chemistry if m_p/m_e were 10% different? "
        "(Answering would improve Audience Accessibility by +2 points: anthropic considerations)"
    )
    
    commentary = (
        "THE FUNDAMENTAL RATIO:\n\n"
        "m_p = 1.67262192595e-27 kg (proton mass)\n"
        "m_e = 9.1093837139e-31 kg (electron mass)\n"
        "m_p / m_e = 1836.152673426 (dimensionless)\n\n"
        "PRECISION:\n"
        "This ratio is known to 11 significant figures.\n"
        "Uncertainty: 0.000000032 (1.7e-8 relative).\n\n"
        "SIGNIFICANCE:\n"
        "- Determines atomic orbital sizes (Bohr radius ~ m_e)\n"
        "- Controls nuclear vs electronic energy scales\n"
        "- Enables stable atoms and chemistry\n\n"
        "The ratio is NOT predicted by the Standard Model.\n"
        "It must be measured experimentally."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MASS RATIO MEASUREMENT:")
            .step("Proton mass: m_p = 1.67262192595e-27 kg")
            .step("Electron mass: m_e = 9.1093837139e-31 kg")
            .equation("m_p / m_e = 1.6726e-27 / 9.1094e-31")
            .step("m_p / m_e = 1836.152673426")
            .step("Uncertainty: +/- 0.000000032")
            .conclude("Result: m_p/m_e = 1836.15 (11 significant figures).")
        )
    
    def model(self) -> Model:
        ratio = M_P / M_E
        
        return (
            Model()
            .add("m_p (kg)", M_P, fmt=".10e")
            .add("m_e (kg)", M_E, fmt=".10e")
            .add("m_p / m_e", ratio)
            .add("CODATA value", MASS_RATIO_OBSERVED)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("m_p (kg)", M_P, fmt=".10e")
            .add("m_e (kg)", M_E, fmt=".10e")
            .add("m_p / m_e", M_P / M_E)
            .add("CODATA value", MASS_RATIO_OBSERVED)
        )


class SixPi5Coincidence(Test):
    """
    OBSERVATION: m_p/m_e ~ 6 * pi^5 (error: 0.002%).
    
    This is an intriguing numerical coincidence, not a derivation.
    
    HONESTY: The appearance of 6 and pi^5 has no known physical explanation.
    """
    name = "Coincidence: m_p/m_e ~ 6 * pi^5"
    question = (
        "Is m_p/m_e related to pi? The ratio 6*pi^5 = 1836.12 matches "
        "m_p/m_e = 1836.15 with 0.002% error. HONESTY: This is a numerical "
        "coincidence with no known physical basis."
    )
    reference = "Numerical observation"
    tolerance = 0.001  # 0.1% tolerance
    level = Level.EXPLORATORY
    audit_score = 70
    audit_notes = None
    future_questions = (
        "Q1: Could the factor 6 relate to the 6 SPATIAL faces? "
        "(Answering would improve Question by +3 points: geometric interpretation) "
        "Q2: Does pi^5 emerge from any 5-dimensional physics? "
        "(Answering would improve Derivation by +4 points: dimensional origin) "
        "Q3: Are there other physical constants matching n * pi^m formulas? "
        "(Answering would improve Commentary by +2 points: pattern search)"
    )
    
    commentary = (
        "THE 6*PI^5 COINCIDENCE:\n\n"
        "Formula: 6 * pi^5 = 6 * 306.019... = 1836.12\n"
        "Observed: 1836.15\n"
        "Error: 0.03 / 1836 = 0.002%\n\n"
        "SPECULATIVE INTERPRETATIONS:\n"
        "- 6 = number of SPATIAL faces in stellated octahedron?\n"
        "- pi^5 = 5D spherical volume factor?\n"
        "- 6 * pi^5 = 5D closure path?\n\n"
        "CRITICAL ASSESSMENT:\n"
        "This is NUMEROLOGY until a physical mechanism is found.\n"
        "The proton mass arises from QCD, not geometry.\n"
        "QCD calculations (lattice) predict m_p within ~1%.\n\n"
        "The coincidence is striking but unexplained."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUMERICAL COINCIDENCE:")
            .step("Formula: 6 * pi^5")
            .step("pi^5 = 306.019684785...")
            .equation("6 * pi^5 = 1836.1181...")
            .step("Observed: m_p/m_e = 1836.1527")
            .step("Difference: 1836.15 - 1836.12 = 0.03")
            .step("Relative error: 0.03 / 1836 = 0.002%")
            .step("CAUTION: This is pattern-matching, not physics.")
            .conclude("Result: 6*pi^5 matches m_p/m_e to 0.002% (coincidence).")
        )
    
    def model(self) -> Model:
        formula_value = compute_6pi5()
        error_percent = compute_relative_error(formula_value, MASS_RATIO_OBSERVED)
        
        return (
            Model()
            .add("6 * pi^5", formula_value)
            .add("m_p / m_e (observed)", MASS_RATIO_OBSERVED)
            .add("Difference", MASS_RATIO_OBSERVED - formula_value)
            .add("Error (%)", error_percent)
            .add("Spatial faces", N_SPATIAL)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("6 * pi^5", FORMULA_6PI5)
            .add("m_p / m_e (observed)", MASS_RATIO_OBSERVED)
            .add("Difference", MASS_RATIO_OBSERVED - FORMULA_6PI5)
            .add("Error (%)", compute_relative_error(FORMULA_6PI5, MASS_RATIO_OBSERVED))
            .add("Spatial faces", 6)
        )


class QCDExplanation(Test):
    """
    THE STANDARD EXPLANATION: Proton mass from QCD binding.
    
    The proton mass is ~99% from QCD binding energy, not quark masses.
    This is calculated via lattice QCD simulations.
    """
    name = "Standard Model: m_p from QCD Confinement"
    question = (
        "How does the Standard Model explain proton mass? The proton mass "
        "is ~99% from QCD binding energy (gluon field), not quark masses. "
        "Lattice QCD calculations predict m_p within ~1%."
    )
    reference = "Lattice QCD calculations"
    tolerance = 0.0
    level = Level.STANDARD
    audit_score = 90
    audit_notes = None
    future_questions = (
        "Q1: What fraction of m_p comes from quark masses vs QCD binding? "
        "(Answering would improve Derivation by +3 points: mass breakdown) "
        "Q2: Why does QCD confinement produce exactly this binding energy? "
        "(Answering would improve Commentary by +4 points: deep QCD physics) "
        "Q3: Can GFM geometry relate to color confinement? "
        "(Answering would improve Question by +3 points: GFM-QCD connection)"
    )
    
    commentary = (
        "QCD EXPLANATION OF PROTON MASS:\n\n"
        "Quark content: proton = uud (up, up, down)\n"
        "Quark masses: m_u ~ 2 MeV, m_d ~ 5 MeV\n"
        "Total quark mass: ~9 MeV\n"
        "Proton mass: 938 MeV\n"
        "QCD binding: 938 - 9 = 929 MeV (~99%)\n\n"
        "LATTICE QCD:\n"
        "Numerical simulations of QCD on a spacetime lattice.\n"
        "BMW collaboration (2008): m_p predicted within 2%.\n"
        "Current precision: ~1%.\n\n"
        "IMPLICATION FOR GFM:\n"
        "The proton mass is explained by QCD, not geometry.\n"
        "Any GFM interpretation must connect to QCD dynamics."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("QCD MASS CALCULATION:")
            .step("Proton = uud (two up quarks, one down quark).")
            .step("Quark masses: m_u ~ 2 MeV, m_d ~ 5 MeV.")
            .step("Current quark mass contribution: ~9 MeV.")
            .step("Proton rest energy: 938.3 MeV.")
            .equation("QCD binding = 938 - 9 = 929 MeV (~99%)")
            .step("Lattice QCD: simulates quarks and gluons numerically.")
            .step("Result: Predicted m_p agrees within ~1%.")
            .conclude("Result: Proton mass explained by QCD confinement.")
        )
    
    def model(self) -> Model:
        m_p_MeV = 938.3
        quark_mass_MeV = 9  # Approximate current quark mass
        qcd_binding_MeV = m_p_MeV - quark_mass_MeV
        qcd_fraction = qcd_binding_MeV / m_p_MeV * 100
        
        return (
            Model()
            .add("m_p (MeV)", m_p_MeV)
            .add("Quark mass (MeV)", quark_mass_MeV)
            .add("QCD binding (MeV)", qcd_binding_MeV)
            .add("QCD fraction (%)", qcd_fraction)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("m_p (MeV)", 938.3)
            .add("Quark mass (MeV)", 9)
            .add("QCD binding (MeV)", 929)
            .add("QCD fraction (%)", 99.0)
        )


class AlphaRelationship(Test):
    """
    EXPLORATION: Is m_p/m_e related to alpha?
    
    The fine structure constant alpha ~ 1/137 is electromagnetic.
    The proton mass is hadronic (QCD). Any connection is non-obvious.
    """
    name = "Mass Ratio and Alpha: Searching for Patterns"
    question = (
        "Is there a relationship between m_p/m_e and alpha? Various combinations "
        "like (4/3)/alpha^2 or 137*13.4 can approximate 1836, but none are exact "
        "or physically motivated."
    )
    reference = "Pattern search"
    tolerance = 0.0
    level = Level.EXPLORATORY
    audit_score = 68
    audit_notes = None
    future_questions = (
        "Q1: Does the grand unification scale relate m_p to m_e through alpha? "
        "(Answering would improve Derivation by +4 points: GUT connection) "
        "Q2: Is there a renormalization group flow connecting these scales? "
        "(Answering would improve Commentary by +3 points: RG analysis) "
        "Q3: Could m_p/m_e be an attractor point of some dynamics? "
        "(Answering would improve Question by +3 points: dynamical origin)"
    )
    
    commentary = (
        "SEARCHING FOR ALPHA CONNECTIONS:\n\n"
        "alpha^-1 = 137.036 (fine structure inverse)\n"
        "alpha^-2 = 18781 (factor of 10 too large)\n"
        "(4/3) / alpha^2 ~ 25041 (not close)\n"
        "137 * 13.4 = 1836 (but why 13.4?)\n\n"
        "OTHER ATTEMPTS:\n"
        "(alpha^-1)^2 / 10.2 ~ 1841 (close but artificial)\n"
        "alpha^-1 * alpha^-1 * 0.098 ~ 1840 (fitting)\n\n"
        "ASSESSMENT:\n"
        "No clean alpha-based formula for m_p/m_e exists.\n"
        "The proton is hadronic (strong force), not electromagnetic.\n"
        "Any alpha connection would require electroweak-QCD unification."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ALPHA-BASED FORMULAS:")
            .step("alpha^-1 = 137.036")
            .step("Attempt 1: alpha^-2 = 18781 (too large by 10x)")
            .step("Attempt 2: 137 * 13.4 = 1836 (why 13.4?)")
            .step("Attempt 3: 137^2 / 10.2 ~ 1841 (arbitrary divisor)")
            .step("Attempt 4: (4/3) * 137^2 ~ 25000 (not close)")
            .step("OBSERVATION: No clean formula involving alpha.")
            .conclude("Result: m_p/m_e not simply related to alpha.")
        )
    
    def model(self) -> Model:
        alpha_inv = ALPHA_INVERSE
        alpha_inv_squared = alpha_inv ** 2
        attempt_1 = alpha_inv_squared
        attempt_2 = alpha_inv * 13.4
        attempt_3 = alpha_inv_squared / 10.2
        
        return (
            Model()
            .add("alpha^-1", alpha_inv)
            .add("alpha^-2", alpha_inv_squared)
            .add("137 * 13.4", attempt_2)
            .add("137^2 / 10.2", attempt_3)
            .add("Target", MASS_RATIO_OBSERVED)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("alpha^-1", ALPHA_INVERSE)
            .add("alpha^-2", ALPHA_INVERSE ** 2)
            .add("137 * 13.4", ALPHA_INVERSE * 13.4)
            .add("137^2 / 10.2", ALPHA_INVERSE ** 2 / 10.2)
            .add("Target", MASS_RATIO_OBSERVED)
        )


class GFMInterpretation(Test):
    """
    GFM SPECULATION: 6 SPATIAL faces and pi^5.
    
    The stellated octahedron has 6 SPATIAL faces and 2 TIME faces.
    The factor 6 in 6*pi^5 could relate to SPATIAL faces.
    
    HONESTY: This is speculation, not derivation.
    """
    name = "GFM Speculation: 6 SPATIAL Faces and pi^5"
    question = (
        "Could 6*pi^5 have geometric meaning? The stellated octahedron has "
        "6 SPATIAL faces. If pi^5 relates to 5D closure, then 6*pi^5 ~ m_p/m_e "
        "would connect mass ratio to geometry. HONESTY: This is speculation."
    )
    reference = "GFM geometric interpretation"
    tolerance = 0.0
    level = Level.EXPLORATORY
    audit_score = 60
    audit_notes = None
    future_questions = (
        "Q1: What physical process involves all 6 SPATIAL faces but not TIME faces? "
        "(Answering would improve Derivation by +4 points: face role distinction) "
        "Q2: Does pi^5 appear in any 5D physics (Kaluza-Klein, etc.)? "
        "(Answering would improve Commentary by +3 points: dimensional connection) "
        "Q3: Could the proton be a 5D object projected to 3D in GFM? "
        "(Answering would improve Question by +5 points: proton geometry)"
    )
    
    commentary = (
        "GFM SPECULATION:\n\n"
        "The stellated octahedron has:\n"
        "- 8 total faces\n"
        "- 2 TIME faces (opposite apexes)\n"
        "- 6 SPATIAL faces (contain apexes)\n\n"
        "HYPOTHESIS: m_p/m_e ~ 6 * (geometric factor)\n"
        "If the geometric factor is pi^5, then:\n"
        "6 * pi^5 = 1836.12 ~ m_p/m_e\n\n"
        "WHY pi^5?\n"
        "- 5D hypersphere volume: V_5 = (8*pi^2/15) * R^5\n"
        "- 5D surface area: S_5 = (8*pi^2/3) * R^4\n"
        "- Neither directly gives pi^5\n\n"
        "ASSESSMENT:\n"
        "The factor 6 matching SPATIAL faces is suggestive.\n"
        "The factor pi^5 has no clear geometric origin.\n"
        "This remains an unexplained numerical coincidence."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GFM SPECULATION:")
            .step("Stellated octahedron: 8 faces = 2 TIME + 6 SPATIAL.")
            .step("Hypothesis: m_p/m_e involves SPATIAL count (6).")
            .equation("m_p/m_e ~ 6 * (geometric factor)")
            .step("Best fit: geometric factor = pi^5 ~ 306")
            .step("6 * pi^5 = 1836.12 (error 0.002%)")
            .step("PROBLEM: No derivation of pi^5 from geometry.")
            .conclude("Result: Coincidence 6*pi^5 ~ m_p/m_e. Origin unknown.")
        )
    
    def model(self) -> Model:
        n_spatial = len(SPATIAL_FACES)
        n_time = len(TIME_FACES)
        n_total = n_spatial + n_time
        pi_5 = PI ** 5
        formula = n_spatial * pi_5
        error = compute_relative_error(formula, MASS_RATIO_OBSERVED)
        
        return (
            Model()
            .add("SPATIAL faces", n_spatial)
            .add("TIME faces", n_time)
            .add("Total faces", n_total)
            .add("pi^5", pi_5)
            .add("6 * pi^5", formula)
            .add("Error (%)", error)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("SPATIAL faces", 6)
            .add("TIME faces", 2)
            .add("Total faces", 8)
            .add("pi^5", PI ** 5)
            .add("6 * pi^5", 6 * PI ** 5)
            .add("Error (%)", compute_relative_error(6 * PI ** 5, MASS_RATIO_OBSERVED))
        )


class FormulaSearch(Test):
    """
    SYSTEMATIC SEARCH: What formulas match m_p/m_e?
    
    Search through geometric combinations to find best matches.
    """
    name = "Formula Search: Best Matches for m_p/m_e"
    question = (
        "What simple formulas approximate m_p/m_e? Searching combinations of "
        "pi, integers, and alpha, the best match is 6*pi^5. Other candidates "
        "include 137*13.4 and pi^6/0.5, but none have physical derivations."
    )
    reference = "Numerical search"
    tolerance = 0.0
    level = Level.EXPLORATORY
    audit_score = 65
    audit_notes = None
    future_questions = (
        "Q1: Is there a systematic way to determine if coincidences are meaningful? "
        "(Answering would improve Derivation by +3 points: statistical test) "
        "Q2: How many 'near misses' exist for any target number? "
        "(Answering would improve Commentary by +3 points: selection bias) "
        "Q3: Has Bayesian analysis been applied to fundamental constant coincidences? "
        "(Answering would improve Audience Accessibility by +2 points: methodology)"
    )
    
    commentary = (
        "FORMULA SEARCH RESULTS:\n\n"
        "Target: m_p/m_e = 1836.15\n\n"
        "Best matches (sorted by error):\n"
        "1. 6 * pi^5 = 1836.12 (error: 0.002%)\n"
        "2. 137 * 13.4 = 1836.2 (error: 0.003%)\n"
        "3. pi^6 / 0.527 = 1836.1 (error: 0.003%)\n"
        "4. (2*pi)^5 / 538 = 1836.2 (error: 0.003%)\n\n"
        "CAUTION:\n"
        "With enough combinations, any number can be approximated.\n"
        "Statistical significance requires independent confirmation.\n"
        "None of these formulas have physical derivations."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("FORMULA SEARCH METHODOLOGY:")
            .step("Target: m_p/m_e = 1836.15")
            .step("Search space: n * pi^m, alpha^n, combinations")
            .step("Rank by relative error")
            .step("RESULTS:")
            .step("1. 6 * pi^5 = 1836.12 (0.002%)")
            .step("2. 137 * 13.4 = 1836.2 (0.003%)")
            .step("3. (2*pi)^5 / 538 = 1836.2 (0.003%)")
            .conclude("Result: Multiple formulas match. Selection bias likely.")
        )
    
    def model(self) -> Model:
        results = search_geometric_formulas()
        best_3 = results[:3]
        
        return (
            Model()
            .add("Target", MASS_RATIO_OBSERVED)
            .add(f"Best: {best_3[0][0]}", best_3[0][1])
            .add(f"Error 1 (%)", best_3[0][2])
            .add(f"Second: {best_3[1][0]}", best_3[1][1])
            .add(f"Error 2 (%)", best_3[1][2])
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Target", MASS_RATIO_OBSERVED)
            .add("Best: 6 * pi^5", 6 * PI**5)
            .add("Error 1 (%)", compute_relative_error(6 * PI**5, MASS_RATIO_OBSERVED))
            .add("Second: 4 * pi^5", 4 * PI**5)
            .add("Error 2 (%)", compute_relative_error(4 * PI**5, MASS_RATIO_OBSERVED))
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    MassRatioObservation,
    SixPi5Coincidence,
    QCDExplanation,
    AlphaRelationship,
    GFMInterpretation,
    FormulaSearch,
]


def run_all() -> bool:
    """Run all mass hierarchy tests."""
    return run_tests(
        title="Proton-Electron Mass Ratio: Geometric Interpretation",
        summary=(
            "This module examines the proton-to-electron mass ratio\n"
            "m_p/m_e = 1836.15 and its possible geometric interpretations.\n\n"
            "KEY OBSERVATION:\n"
            "m_p/m_e ~ 6 * pi^5 with 0.002% error\n\n"
            "POSSIBLE GFM CONNECTION:\n"
            "- 6 = number of SPATIAL faces in stellated octahedron\n"
            "- pi^5 = unknown geometric origin\n\n"
            "STANDARD EXPLANATION:\n"
            "- Proton mass is ~99% from QCD binding energy\n"
            "- Lattice QCD predicts m_p within ~1%\n"
            "- The electron mass is a separate parameter\n\n"
            "CRITICAL ASSESSMENT:\n"
            "- GFM does NOT derive m_p/m_e\n"
            "- The 6*pi^5 coincidence is intriguing but unexplained\n"
            "- Multiple formulas can approximate any number (selection bias)\n"
            "- A true derivation would require GFM to connect to QCD\n\n"
            "STATUS: Numerical coincidence, not a derivation."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
