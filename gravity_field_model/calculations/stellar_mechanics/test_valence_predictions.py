"""
Valence Predictions: Empirical Atomic Radius Formula
=====================================================

GFD Model V2

HONESTY STATEMENT:
This module contains an EMPIRICALLY FITTED atomic radius formula that uses
GFD-inspired constants. The formula achieves reasonable accuracy (~13%
average error) by FITTING parameters to measured data, not by deriving
atomic radii from first principles.

THE FORMULA (empirical fit):
    r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [correction]

WHERE:
- 84/137 is an empirical prefactor (happens to be T_7 * alpha)
- a_bohr = 52.9 pm (Bohr radius from QM)
- n = principal quantum number
- A, Z = mass and atomic number
- correction = topology/relativistic adjustment

WHAT THIS IS:
- An empirical formula that fits measured atomic radii
- Uses GFD-inspired constants (k, alpha, tetrahedral numbers)
- Achieves ~10-15% average error

WHAT THIS IS NOT:
- A derivation of atomic radii from GFD geometry
- A prediction that can be tested (it's fitted to the data)
- More accurate than quantum mechanical calculations

The tests verify that the empirical formula produces consistent results
and matches measured data within the fitted accuracy.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    K_CLOSURE, R_E, M_E, A_0, C, HBAR,
    ELEMENTS_118, BINDING_ENERGIES_BY_A,
    IONIZATION_ENERGIES, ELECTRONEGATIVITIES,
    ATOMIC_DATA, MEV_TO_JOULES,
    get_binding_energy_by_A,
)

PI = math.pi
A_BOHR_PM = 52.9177  # Bohr radius in picometers
GFD_FACTOR = 84 / 137.036  # Empirical prefactor (T_7 * alpha)

ELEMENTS = ELEMENTS_118


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_principal_quantum_number(Z):
    """Get principal quantum number from atomic number."""
    if Z <= 2: return 1
    if Z <= 10: return 2
    if Z <= 18: return 3
    if Z <= 36: return 4
    if Z <= 54: return 5
    if Z <= 86: return 6
    return 7


def mu_mond(x):
    """MOND interpolating function mu(x) = x/(1+x)."""
    return x / (1 + x)


def tetrahedral_number(n):
    """Calculate n-th tetrahedral number T_n = n(n+1)(n+2)/6."""
    return n * (n + 1) * (n + 2) // 6


def predict_atomic_radius(Z, A):
    """
    Empirical atomic radius formula.

    HONESTY: This is curve-fitting, not derivation. The formula has been
    tuned to match measured atomic radii. The GFD-inspired constants
    (84, 137, k/pi^2) provide reasonable fits but are not derived from
    first principles.
    """
    n = get_principal_quantum_number(Z)

    # Base formula
    base_radius = GFD_FACTOR * A_BOHR_PM * (n ** 2) * math.sqrt(A) / Z

    # Relativistic/topology correction for heavy elements
    # This is an empirical adjustment, not a derivation
    beta = K_CLOSURE / (PI ** 2)  # ~0.405
    Z_threshold = 56  # Fe-56 as transition point
    correction_factor = 1 - beta * mu_mond(Z / Z_threshold)

    return base_radius * correction_factor


# =============================================================================
# VALIDATED FUNCTION
# =============================================================================

_ELEMENT_LOOKUP = {sym: (name, z, a) for sym, name, z, a, _r, _v in ELEMENTS_118}


@Fn(
    equation="r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [1 - (k/pi^2)*mu(Z/56)]",
    inputs={"symbol": "str: Element symbol (e.g. 'Fe', 'C', 'Pb')"},
    outputs={"radius_pm": "float: Predicted atomic radius in picometers"},
    description=(
        "Empirical atomic radius formula using GFD-inspired constants. "
        "HONESTY: This formula is fitted to measured atomic radii, not derived "
        "from GFD geometry. The parameters (84/137, k/pi^2, Z/56 threshold) "
        "have been tuned to minimize prediction error. "
        "Accuracy: ~13% average error across 118 elements."
    ),
)
def fn_get_element_field_radius(symbol: str) -> float:
    """Empirical atomic radius prediction (fitted formula)."""
    if symbol not in _ELEMENT_LOOKUP:
        raise ValueError(f"Unknown element symbol '{symbol}'.")
    _name, z, a = _ELEMENT_LOOKUP[symbol]
    return predict_atomic_radius(z, a)


# =============================================================================
# TEST 1: BOHR RADIUS IDENTITY (Standard QM)
# =============================================================================

class BohrRadiusIdentity(Test):
    """
    Verify a_bohr = r_e / alpha^2.

    HONESTY: This is a standard QM identity, not a GFD derivation.
    """
    name = "Bohr Radius Identity"
    question = (
        "Does a_bohr = r_e / alpha^2 hold exactly?"
    )
    reference = "CODATA 2018"
    tolerance = 0.01
    level = Level.CRITICAL
    commentary = (
        "The identity a_bohr = r_e / alpha^2 is a standard result connecting "
        "the Bohr radius (atomic scale), classical electron radius (field scale), "
        "and fine structure constant. This is QED, not GFD."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD QM: Bohr radius identity.")
            .equation("a_bohr = hbar / (m_e * c * alpha) = r_e / alpha^2")
            .step("r_e = 2.818e-15 m, alpha = 1/137.036")
            .equation("a_bohr = 2.818e-15 / (1/137)^2 = 5.29e-11 m = 52.9 pm")
            .step("CODATA: a_bohr = 52.9177 pm.")
            .conclude("Identity verified. Standard QM.")
        )

    def model(self) -> Model:
        r_e = 2.8179403262e-15
        alpha = 1 / 137.035999084
        a_bohr_calc = r_e / alpha**2
        a_bohr_pm = a_bohr_calc * 1e12
        match = 1.0 if abs(a_bohr_pm - A_BOHR_PM) / A_BOHR_PM < 0.001 else 0.0
        return (
            Model()
            .add("Calculated a_bohr (pm)", a_bohr_pm)
            .add("CODATA a_bohr (pm)", A_BOHR_PM)
            .add("Match", match)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Calculated a_bohr (pm)", 52.9177)
            .add("CODATA a_bohr (pm)", 52.9177)
            .add("Match", 1.0)
        )


# =============================================================================
# TEST 2: FORMULA ACCURACY (Empirical Fit Quality)
# =============================================================================

class FormulaAccuracy(Test):
    """
    Test empirical formula accuracy on main group elements.

    HONESTY: This tests the quality of the FIT, not a prediction.
    """
    name = "Empirical Formula Accuracy"
    question = (
        "What is the average error of the empirical radius formula on main "
        "group elements?"
    )
    reference = "Measured atomic radii"
    tolerance = 0.50
    level = Level.STANDARD
    commentary = (
        "This test measures how well the empirical formula fits measured data. "
        "It is NOT testing a GFD prediction, since the formula was tuned to "
        "match these values. The ~10% error on main group elements shows the "
        "formula provides a reasonable algebraic approximation."
    )

    # Inject the function using Depends
    get_radius = Depends(fn_get_element_field_radius)

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("FITTING TEST: Measure formula accuracy on main group.")
            .step("Main group: C, N, O, Ne, Si, Cl, Ar")
            .step("Compare predicted vs measured radii.")
            .step("Calculate average percent error.")
            .step("NOTE: This tests fit quality, not prediction accuracy.")
            .conclude("Average error on main group elements.")
        )

    def model(self) -> Model:
        main_group = ['C', 'N', 'O', 'Ne', 'Si', 'Cl', 'Ar']
        errors = []
        for sym in main_group:
            Z, A, actual_r, _, _, _ = ATOMIC_DATA[sym]
            pred_r = self.get_radius(sym)
            if actual_r > 0:
                err = abs((pred_r - actual_r) / actual_r * 100)
                errors.append(err)
        avg_error = sum(errors) / len(errors) if errors else 0
        return (
            Model()
            .add("Average error (%)", avg_error)
            .add("Elements tested", len(errors))
            .add("Below 10%", 1.0 if avg_error < 10 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Average error (%)", 10.0)
            .add("Elements tested", 7)
            .add("Below 10%", 1.0)
        )


# =============================================================================
# TEST 3: PERIODIC TRENDS (Standard Chemistry)
# =============================================================================

class PeriodicTrends(Test):
    """
    Verify atomic radius decreases across a period.

    HONESTY: This is standard chemistry. The formula reproduces it.
    """
    name = "Period 2 Radius Trend"
    question = (
        "Does atomic radius decrease across period 2 (C > N > O > F)?"
    )
    reference = "Chemistry (periodic trends)"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Atomic radius decreases across a period due to increasing nuclear "
        "charge attracting electrons more strongly. This is standard chemistry. "
        "The empirical formula reproduces this trend."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD CHEMISTRY: Radius decreases across period.")
            .step("Increasing Z attracts electrons more strongly.")
            .step("Period 2: C > N > O > F")
            .step("Measured: 76 > 71 > 66 > 57 pm")
            .conclude("Trend verified. Standard chemistry.")
        )

    def model(self) -> Model:
        c_r = ATOMIC_DATA['C'][2]
        n_r = ATOMIC_DATA['N'][2]
        o_r = ATOMIC_DATA['O'][2]
        f_r = ATOMIC_DATA['F'][2]
        decreasing = 1.0 if c_r > n_r > o_r > f_r else 0.0
        return (
            Model()
            .add("C radius (pm)", c_r)
            .add("F radius (pm)", f_r)
            .add("Decreasing trend", decreasing)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("C radius (pm)", 76)
            .add("F radius (pm)", 57)
            .add("Decreasing trend", 1.0)
        )


# =============================================================================
# TEST 4: NOBLE GAS STABILITY (Standard Chemistry)
# =============================================================================

class NobleGasStability(Test):
    """
    Verify He has higher ionization energy than H.

    HONESTY: Standard chemistry from closed shell stability.
    """
    name = "Noble Gas Ionization"
    question = (
        "Does He have higher ionization energy than H?"
    )
    reference = "Chemistry"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Helium's ionization energy (24.59 eV) exceeds hydrogen's (13.6 eV) "
        "because He has a closed shell (1s^2). This is standard quantum "
        "chemistry, not a GFD prediction."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD CHEMISTRY: Noble gas stability.")
            .step("He has closed 1s^2 shell.")
            .step("Closed shell = higher ionization energy.")
            .step("He IE = 24.59 eV > H IE = 13.6 eV")
            .conclude("Noble gas stability verified. Standard chemistry.")
        )

    def model(self) -> Model:
        he_ie = ATOMIC_DATA['He'][3]
        h_ie = ATOMIC_DATA['H'][3]
        return (
            Model()
            .add("He IE (eV)", he_ie)
            .add("H IE (eV)", h_ie)
            .add("He > H", 1.0 if he_ie > h_ie else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("He IE (eV)", 24.59)
            .add("H IE (eV)", 13.60)
            .add("He > H", 1.0)
        )


# =============================================================================
# TEST 5: FLUORINE ELECTRONEGATIVITY (Standard Chemistry)
# =============================================================================

class FluorineElectronegativity(Test):
    """
    Verify F has maximum electronegativity.

    HONESTY: Standard chemistry (Pauling scale).
    """
    name = "Fluorine Max Electronegativity"
    question = (
        "Does fluorine have the highest Pauling electronegativity?"
    )
    reference = "Chemistry (Pauling scale)"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Fluorine has EN = 3.98, the highest on the Pauling scale. This "
        "reflects its small size and high electron affinity. Standard chemistry."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD CHEMISTRY: Electronegativity trends.")
            .step("F is small with high effective nuclear charge.")
            .step("Strong electron attraction = high electronegativity.")
            .step("F EN = 3.98 (maximum).")
            .conclude("Fluorine max EN verified. Standard chemistry.")
        )

    def model(self) -> Model:
        f_en = ATOMIC_DATA['F'][4]
        max_en = max(v[4] for v in ATOMIC_DATA.values() if v[4] is not None)
        return (
            Model()
            .add("F EN", f_en)
            .add("Is maximum", 1.0 if abs(f_en - max_en) < 0.01 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("F EN", 3.98)
            .add("Is maximum", 1.0)
        )


# =============================================================================
# TEST 6: CARBON TETRAVALENCE (Standard Chemistry)
# =============================================================================

class CarbonTetravalence(Test):
    """
    Verify carbon has 4 valence electrons.

    HONESTY: This is electron configuration, standard chemistry.
    """
    name = "Carbon Valence = 4"
    question = (
        "Does carbon have 4 valence electrons?"
    )
    reference = "Chemistry"
    tolerance = 0.01
    level = Level.CRITICAL
    commentary = (
        "Carbon (Z=6) has electron configuration 1s^2 2s^2 2p^2, giving 4 "
        "valence electrons. This allows sp3 tetrahedral bonding. Standard "
        "chemistry. The coincidence that 4 = k is noted by GFD but not explained."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ELECTRON CONFIGURATION: C = 1s^2 2s^2 2p^2")
            .step("Valence electrons = 2 + 2 = 4")
            .step("Allows 4 bonds (sp3 hybridization)")
            .step("OBSERVATION: 4 = k (GFD notes this coincidence)")
            .conclude("Carbon valence = 4. Standard chemistry.")
        )

    def model(self) -> Model:
        c_val = ATOMIC_DATA['C'][5]
        return (
            Model()
            .add("C valence", c_val)
            .add("Equals k", 1.0 if c_val == K_CLOSURE else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("C valence", 4)
            .add("Equals k", 1.0)
        )


# =============================================================================
# TEST 7: TETRAHEDRAL NUMBER OBSERVATIONS (Pattern Matching)
# =============================================================================

class TetrahedralPatterns(Test):
    """
    Note tetrahedral number coincidences.

    HONESTY: These are observations of numerical coincidences, not derivations.
    """
    name = "Tetrahedral Number Patterns"
    question = (
        "Do some stable nuclei have A equal to tetrahedral numbers?"
    )
    reference = "Number theory / Nuclear data"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "He-4 = T_2 = 4, Ne-20 = T_4 = 20, Fe-56 = T_6 = 56. These coincidences "
        "are OBSERVED by GFD. They do NOT explain nuclear stability, which comes "
        "from the shell model. Pattern matching is not physics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("OBSERVATION: Some mass numbers equal tetrahedral numbers.")
            .equation("T_2 = 2*3*4/6 = 4 (He-4)")
            .equation("T_4 = 4*5*6/6 = 20 (Ne-20)")
            .equation("T_6 = 6*7*8/6 = 56 (Fe-56)")
            .step("This is pattern matching, not an explanation.")
            .step("Nuclear stability comes from shell model.")
            .conclude("Coincidences observed. Not explanatory.")
        )

    def model(self) -> Model:
        he4_is_T2 = 1.0 if 4 == tetrahedral_number(2) else 0.0
        ne20_is_T4 = 1.0 if 20 == tetrahedral_number(4) else 0.0
        fe56_is_T6 = 1.0 if 56 == tetrahedral_number(6) else 0.0
        return (
            Model()
            .add("He-4 = T_2", he4_is_T2)
            .add("Ne-20 = T_4", ne20_is_T4)
            .add("Fe-56 = T_6", fe56_is_T6)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("He-4 = T_2", 1.0)
            .add("Ne-20 = T_4", 1.0)
            .add("Fe-56 = T_6", 1.0)
        )


# =============================================================================
# TEST 8: COMPLETE PERIODIC TABLE (Data Verification)
# =============================================================================

class CompletePeriodicTable(Test):
    """
    Verify data for all 118 elements is present.

    HONESTY: This is data completeness, not physics.
    """
    name = "118 Element Data"
    question = (
        "Do we have atomic data for all 118 IUPAC elements?"
    )
    reference = "IUPAC"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Verifies the data set includes all 118 elements from H to Og. "
        "This is data management, not physics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("DATA CHECK: Count elements in ATOMIC_DATA.")
            .step("Expected: 118 (H through Og).")
            .conclude("Complete periodic table coverage.")
        )

    def model(self) -> Model:
        count = len(ATOMIC_DATA)
        return (
            Model()
            .add("Elements defined", count)
            .add("Complete", 1.0 if count == 118 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Elements defined", 118)
            .add("Complete", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BohrRadiusIdentity,
    FormulaAccuracy,
    PeriodicTrends,
    NobleGasStability,
    FluorineElectronegativity,
    CarbonTetravalence,
    TetrahedralPatterns,
    CompletePeriodicTable,
]


def run_all() -> bool:
    """Run all valence prediction tests."""
    return run_tests(
        title="Valence Shell Predictions",
        summary=(
            "These tests verify an EMPIRICAL atomic radius formula and standard\n"
            "chemistry data.\n\n"
            "THE RADIUS FORMULA:\n"
            "r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [correction]\n"
            "This is a FITTED formula using GFD-inspired constants.\n"
            "It achieves ~13% average error by curve-fitting, not derivation.\n\n"
            "STANDARD CHEMISTRY VERIFIED:\n"
            "- Bohr radius identity (QED)\n"
            "- Period trends (increasing nuclear charge)\n"
            "- Noble gas stability (closed shells)\n"
            "- Fluorine max electronegativity\n"
            "- Carbon tetravalence\n\n"
            "PATTERN OBSERVATIONS (not explanations):\n"
            "- Some stable nuclei have A = tetrahedral numbers\n"
            "- Carbon valence = 4 = k\n"
            "These coincidences are noted, not derived."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
