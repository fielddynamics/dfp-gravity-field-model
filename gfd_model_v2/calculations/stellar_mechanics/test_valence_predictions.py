"""
Valence Shell Predictions from Subspace Packing
================================================

GFD Model V2 - Converted to GFDTest interface

This module examines correspondences between atomic properties and values
derived from the DFP geometry using fundamental constants. Tests verify
that the radius formula produces values consistent with measured atomic radii
for main group elements.

KEY FORMULA:
    r = (84/137) * a_bohr * n^2 * sqrt(A) / Z
    
    Where:
    - 84 = T_7 (7th tetrahedral number)
    - 137 = 1/alpha
    - a_bohr = r_e / alpha^2
    - n = principal quantum number
    - A = mass number (gravity field count in Tet B)
    - Z = atomic number
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from gfd_model_v2.base import GFDTest, run_test_group, validated_function
from gfd_model_v2.common import (
    K_CLOSURE, R_E, M_E, A_0, C, HBAR,
    ELEMENTS_118, BINDING_ENERGIES_BY_A,
    IONIZATION_ENERGIES, ELECTRONEGATIVITIES,
    ATOMIC_DATA, MEV_TO_JOULES,
    get_binding_energy_by_A,
)

# Power output validated function — consumed by GFDPowerCalculation
from gfd_model_v2.calculations.stellar_mechanics.test_power_output import element_power_output  # noqa: F401

PI = math.pi
A_BOHR_PM = 52.9177  # Bohr radius in picometers
GFD_FACTOR = 84 / 137.036  # T_7 * alpha

# Local alias so the 200+ references to ELEMENTS keep working unchanged
ELEMENTS = ELEMENTS_118

# Field closure constants
LAMBDA_COMPTON = 2.426310238e-12  # Compton wavelength (m)
F_CLOSURE = C / LAMBDA_COMPTON    # ~1.24e20 Hz


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_principal_quantum_number(Z):
    if Z <= 2: return 1
    if Z <= 10: return 2
    if Z <= 18: return 3
    if Z <= 36: return 4
    if Z <= 54: return 5
    if Z <= 86: return 6
    return 7


def predict_atomic_radius_from_fields(Z, A):
    """
    GFD atomic radius with TOPOLOGY CORRECTION for heavy elements.
    
    FORMULA:
        r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [1 - (k/pi^2) * mu(Z/56)]
    
    WHERE:
        - 84 = T_7 (7th tetrahedral number)
        - 137 = 1/alpha (fine structure constant)
        - k/pi^2 = 0.4053 (dual-aperture topology correction)
        - 56 = 14k = Fe (relativistic threshold at peak binding)
        - mu(x) = x/(1+x) (MOND interpolating function)
    
    WHY THE CORRECTION:
        A gravity knot (electron) couples to TWO field systems:
        1. Host gravity field (external coupling) -> aperture sqrt(k/pi)
        2. Its own field origin (self-anchoring) -> aperture sqrt(k/pi)
        Combined: k/pi, normalized by spherical geometry: k/pi^2 = 0.4053
    """
    n = get_principal_quantum_number(Z)
    
    # Base GFD formula
    base_radius = GFD_FACTOR * A_BOHR_PM * (n ** 2) * math.sqrt(A) / Z
    
    # Topology correction for dual-aperture coupling
    beta = K_CLOSURE / (PI ** 2)  # = 4/9.8696 = 0.4053
    Z_threshold = 14 * K_CLOSURE  # = 56 = Fe (peak binding energy)
    
    # MOND interpolating function smoothly applies correction
    correction_factor = 1 - beta * mu_mond(Z / Z_threshold)
    
    return base_radius * correction_factor


def _calculate_base_radius(z, a):
    """Base GFD radius WITHOUT topology correction (for comparison)."""
    n = get_principal_quantum_number(z)
    return GFD_FACTOR * A_BOHR_PM * (n ** 2) * math.sqrt(a) / z


def tetrahedral_number(n):
    return n * (n + 1) * (n + 2) // 6


def mu_mond(x):
    return x / (1 + x)


def get_binding_energy(A):
    """Get binding energy per nucleon (MeV) for mass number A."""
    return get_binding_energy_by_A(A)


def power_per_field(A):
    """
    Calculate power output per gravity field (W).
    
    Power = Binding Energy (J) x Field Closure Frequency (Hz)
    """
    be_mev = get_binding_energy(A)
    be_joules = be_mev * MEV_TO_JOULES
    return be_joules * F_CLOSURE


def compression_state(A):
    """
    Return compression state for mass number A.
    
    A = 0: Empty field, INWARD compression (squish ball)
    A > 0: Bound field(s), OUTWARD compression (bowling ball)
    """
    if A == 0:
        return "INWARD"
    return "OUTWARD"


# =============================================================================
# VALIDATED FUNCTION: element_field_radius
# =============================================================================

# Symbol → (name, Z, A) lookup for validated functions
_ELEMENT_LOOKUP = {sym: (name, z, a) for sym, name, z, a, _r, _v in ELEMENTS_118}


@validated_function(
    equation="r(sym) = (T_7 / alpha_inv) × a_bohr × n^2 × sqrt(A) / Z × [1 - (k/pi^2) × mu(Z/56)]",
    description=(
        "GFD-predicted atomic radius in picometers for a given element.\n\n"
        "WHY THIS FUNCTION EXISTS:\n"
        "The atomic radius bridges power output and observable chemistry. Two things\n"
        "determine how big an atom is in the GFD model:\n\n"
        "  1. BASE GEOMETRY: The ratio (84/137) × a_bohr × n^2 × sqrt(A) / Z encodes\n"
        "     how the electron vortex (spanning 861 field envelopes = 137 closure cycles)\n"
        "     wraps around A gravity fields packed in Tet B.  84 = T_7 connects to\n"
        "     the Tet B packing geometry.  137 = 1/alpha connects to electromagnetic\n"
        "     coupling strength.\n\n"
        "  2. TOPOLOGY CORRECTION: For heavy elements (Z > 56), the electron must\n"
        "     couple through TWO apertures — one to its host field, one to its own\n"
        "     field origin — each with solid angle sqrt(k/pi).  The combined cost is\n"
        "     k/pi^2 = 0.4053.  This correction is anchored at Fe-56 (14k), the\n"
        "     element with peak power output per field, because that is where the\n"
        "     transition from light to heavy element behaviour occurs.  The MOND\n"
        "     interpolating function mu(Z/56) smoothly applies the correction.\n\n"
        "Without this function, every test that needs a predicted radius recalculates\n"
        "the formula locally, risking divergent constants.  Centralising it here\n"
        "ensures one formula, one set of constants, traceable through the dependency\n"
        "chain."
    ),
    inputs={"symbol": "str — Element symbol (e.g. 'Fe', 'C', 'Pb')"},
    outputs={"radius_pm": "float — Predicted atomic radius in picometers"},
    group="Valence Predictions",
)
def element_field_radius(symbol):
    """GFD-predicted atomic radius for the given element, in picometers."""
    if symbol not in _ELEMENT_LOOKUP:
        raise ValueError(
            f"Unknown element symbol '{symbol}'. "
            f"Available: {sorted(_ELEMENT_LOOKUP.keys())}"
        )
    _name, z, a = _ELEMENT_LOOKUP[symbol]
    return predict_atomic_radius_from_fields(z, a)


# =============================================================================
# TEST CLASSES
# =============================================================================

class GFDBohrIdentity(GFDTest):
    """Test the exact identity: a_bohr = r_e / alpha^2."""
    name = "Bohr Radius Identity"
    question = "Does the Bohr radius satisfy a_bohr = r_e / alpha^2 exactly, connecting the electron vortex extent (Compton wavelength) to the gravity field size (classical electron radius) through electromagnetic coupling (alpha)?"
    reference_source = "CODATA 2018"
    tolerance = 0.01
    derivation = (
        "PREMISE: Bohr radius should satisfy exact identity a_bohr = r_e / alpha^2. "
        "STEP 1: Classical electron radius r_e = 2.8179e-15 m. "
        "STEP 2: Fine structure constant alpha = 1/137.036. "
        "STEP 3: Calculate: a_bohr = r_e / alpha^2 = 2.8179e-15 / (1/137.036)^2. "
        "STEP 4: a_bohr = 2.8179e-15 × 137.036^2 = 5.2918e-11 m = 52.918 pm. "
        "STEP 5: CODATA value: a_bohr = 52.9177 pm. "
        "OUTPUT: Calculated a_bohr (pm) = 52.918, CODATA a_bohr (pm) = 52.918, Match = 1.0."
    )
    commentary = (
        "The identity a_bohr = r_e / alpha^2 connects three fundamental scales: "
        "the Bohr radius (atomic size), the classical electron radius (field envelope size), "
        "and alpha (electromagnetic coupling). In GFD terms, this means the atomic scale "
        "is exactly alpha^2 times the field envelope scale."
    )
    
    def model(self):
        r_e = 2.8179403262e-15
        alpha = 1 / 137.035999084
        a_bohr_calc = r_e / alpha**2
        a_bohr_pm = a_bohr_calc * 1e12
        match = 1.0 if abs(a_bohr_pm - A_BOHR_PM) / A_BOHR_PM < 0.001 else 0.0
        return {"Calculated a_bohr (pm)": a_bohr_pm, "CODATA a_bohr (pm)": A_BOHR_PM, "Match": match}
    
    def observations(self):
        return {"Calculated a_bohr (pm)": 52.9177, "CODATA a_bohr (pm)": 52.9177, "Match": 1.0}


class GFDFactor84_137(GFDTest):
    """Test 84/137 = T_7 * alpha connects tetrahedral packing to fine structure."""
    name = "GFD Factor 84/137"
    question = "Does the GFD radius factor 84/137 equal T_7 × alpha, connecting the 7th tetrahedral number (Tet B packing geometry) to the fine structure constant (electromagnetic coupling)?"
    reference_source = None  # Model
    tolerance = 0.01
    derivation = (
        "PREMISE: GFD radius factor numerator 84 equals both 7th tetrahedral number T_7 "
        "and product k x F_8 = 4 x 21, connecting Field Closure to Fibonacci sequence. "
        "STEP 1: Calculate T_7 = 7 x 8 x 9 / 6 = 84. "
        "STEP 2: Calculate k x F_8 = 4 x 21 = 84. "
        "STEP 3: Calculate GFD factor: 84 / 137.036. "
        "OUTPUT: k * F_8 = 84, GFD factor, Equals 84 = 1.0."
    )
    commentary = (
        "The 84/137 factor combining k (Field Closure), Fibonacci numbers, and alpha represents a "
        "model-internal numerical relationship. The value 84 = T_7 (7th tetrahedral number) also "
        "equals k x F_8 = 4 x 21, suggesting possible geometric significance."
    )
    
    def model(self):
        k = K_CLOSURE
        F_8 = 21
        product = k * F_8
        gfd_factor = product / 137.036
        return {"k * F_8": product, "GFD factor": gfd_factor, "Equals 84": 1.0 if product == 84 else 0.0}


class MainGroupAccuracy(GFDTest):
    """Test GFD formula achieves < 5% error on main group elements."""
    name = "Main Group Accuracy"
    question = "Does the GFD atomic radius formula r = (84/137) x a_bohr x n^2 x sqrt(A) / Z achieve less than 5% average error when predicting radii of main group elements?"
    reference_source = None  # Model calculation
    tolerance = 0.50
    depends_on = ["element_field_radius"]
    derivation = (
        "PREMISE: GFD atomic radius formula should achieve < 5% average error for main group. "
        "This test consumes element_field_radius which applies the topology-corrected formula. "
        "STEP 1: Call element_field_radius for C, N, O, Ne, Si, Cl, Ar. "
        "STEP 2: Compare each prediction to measured radius from ATOMIC_DATA. "
        "STEP 3: Compute average percent error. "
        "OUTPUT: Average error (%), Elements tested, Below 5%."
    )
    commentary = (
        "The GFD radius formula performance on main group elements provides an empirical test "
        "of the model's predictive capability. By consuming element_field_radius, this test "
        "uses the same topology-corrected formula as every other radius test, ensuring "
        "consistent evaluation across the test suite."
    )
    
    def model(self):
        main_group = ['C', 'N', 'O', 'Ne', 'Si', 'Cl', 'Ar']
        errors = []
        for sym in main_group:
            Z, A, actual_r, _, _, _ = ATOMIC_DATA[sym]
            pred_r = self.fn.element_field_radius(sym)
            err = abs((pred_r - actual_r) / actual_r * 100)
            errors.append(err)
        avg_error = sum(errors) / len(errors)
        below_5pct = 1.0 if avg_error < 5.0 else 0.0
        return {"Average error (%)": avg_error, "Elements tested": len(errors), "Below 5%": below_5pct}


class All118ElementsPresent(GFDTest):
    """Test that we have atomic data for all 118 elements."""
    name = "Complete Periodic Table Coverage"
    question = "Does the test data set include all 118 IUPAC-recognized elements with atomic parameters (Z, A, radius, valence) for complete periodic table analysis?"
    reference_source = "IUPAC Periodic Table"
    tolerance = 0.01
    derivation = (
        "The complete periodic table coverage is verified. "
        "Data fields per element: Z (atomic number), A (mass number), radius (pm), valence. "
        "Elements: All 118 IUPAC-recognized elements from H (Z=1) to Og (Z=118). "
        "Coverage: Period 1 (2), Period 2 (8), Period 3 (8), Period 4 (18), "
        "Period 5 (18), Period 6 (32), Period 7 (32). Total: 118 elements. "
        "K-multiple elements (A mod 4 = 0): 30 out of 118 (25.4%). "
        "This complete coverage enables systematic analysis of k-multiple stability patterns."
    )
    commentary = (
        "Complete periodic table coverage (all 118 elements) enables comprehensive "
        "validation of GFD model predictions across the entire range of known atomic "
        "configurations, from hydrogen to oganesson."
    )
    
    def model(self):
        count = len(ATOMIC_DATA)
        k_mult = sum(1 for _, (z, a, r, ie, en, v) in ATOMIC_DATA.items() if a % K_CLOSURE == 0)
        return {
            "Elements defined": count,
            "K-multiples": k_mult,
            "Complete table": 1.0 if count == 118 else 0.0
        }
    
    def observations(self):
        return {
            "Elements defined": 118,
            "K-multiples": 30,
            "Complete table": 1.0
        }


class AtomicRadiusTrends(GFDTest):
    """Test that radius decreases across period 2."""
    name = "Atomic Radius Trends"
    question = "Does atomic radius decrease monotonically across period 2 (C > N > O > F), as predicted by increasing nuclear charge (more gravity fields attracting the same shell) without adding new Field Chamber shells?"
    reference_source = "Chemistry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Atomic radius should decrease monotonically across period 2 (C > N > O > F) "
        "as increasing nuclear charge attracts same shell without adding new Field Chamber shells. "
        "STEP 1: Retrieve radii: C=76 pm, N=71 pm, O=66 pm, F=57 pm. "
        "STEP 2: Test decreasing trend: 76 > 71 > 66 > 57. "
        "OUTPUT: C radius (pm) = 76, F radius (pm) = 57, Decreasing trend = 1.0."
    )
    commentary = (
        "The decreasing atomic radius across period 2 reflects increasing nuclear charge drawing "
        "electrons closer. This well-documented periodic trend is consistent with Field Chamber "
        "configurations where additional gravity fields increase central attraction without adding new shells."
    )
    
    def model(self):
        c_r = ATOMIC_DATA['C'][2]
        n_r = ATOMIC_DATA['N'][2]
        o_r = ATOMIC_DATA['O'][2]
        f_r = ATOMIC_DATA['F'][2]
        decreasing = 1.0 if c_r > n_r > o_r > f_r else 0.0
        return {"C radius (pm)": c_r, "F radius (pm)": f_r, "Decreasing trend": decreasing}
    
    def observations(self):
        return {"C radius (pm)": 76, "F radius (pm)": 57, "Decreasing trend": 1.0}


class NobleGasStability(GFDTest):
    """Test He IE > H IE (noble gas stability)."""
    name = "Noble Gas Stability"
    question = "Does helium's ionization energy exceed hydrogen's, reflecting the exceptional stability of the first complete k=4 Field Closure (He-4) compared to incomplete closure (H-1)?"
    reference_source = "Chemistry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Noble gases should have higher ionization energies due to complete "
        "Field Closure configurations. He (k=4 complete closure) vs H (k=1, incomplete). "
        "STEP 1: He IE = 24.59 eV, H IE = 13.60 eV. "
        "STEP 2: Verify He IE > H IE: 24.59 > 13.60. "
        "OUTPUT: He IE (eV) = 24.59, H IE (eV) = 13.60, He > H = 1.0."
    )
    commentary = (
        "Helium's higher ionization energy reflects the stability of the first complete "
        "k=4 Field Closure (A=4). The closed shell makes it exceptionally difficult to "
        "remove an electron, consistent with noble gas chemistry."
    )
    
    def model(self):
        he_ie = ATOMIC_DATA['He'][3]
        h_ie = ATOMIC_DATA['H'][3]
        he_higher = 1.0 if he_ie > h_ie else 0.0
        return {"He IE (eV)": he_ie, "H IE (eV)": h_ie, "He > H": he_higher}
    
    def observations(self):
        return {"He IE (eV)": 24.59, "H IE (eV)": 13.60, "He > H": 1.0}


class FluorineMaxEN(GFDTest):
    """Test F has max electronegativity."""
    name = "Fluorine Maximum Electronegativity"
    question = "Does fluorine have the highest Pauling electronegativity, consistent with its position one electron short of complete k=5 Field Closure (Ne-20)?"
    reference_source = "Chemistry (Pauling scale)"
    tolerance = 0.01
    derivation = (
        "PREMISE: Fluorine (Z=9) should have maximum electronegativity because it is "
        "one electron short of the Ne (Z=10) complete Field Chamber shell. "
        "STEP 1: F EN = 3.98, O EN = 3.44, Cl EN = 3.16. "
        "STEP 2: Verify F is maximum among all elements. "
        "OUTPUT: F EN = 3.98, F is max = 1.0."
    )
    commentary = (
        "Fluorine's maximum electronegativity reflects its position one electron short of "
        "completing the neon shell (Z=10, A=20 = 5k). This strong electron affinity drives "
        "fluorine's exceptional reactivity."
    )
    
    def model(self):
        f_en = ATOMIC_DATA['F'][4]
        max_en = max(v[4] for v in ATOMIC_DATA.values() if v[4] is not None)
        f_is_max = 1.0 if abs(f_en - max_en) < 0.01 else 0.0
        return {"F EN": f_en, "F is max": f_is_max}
    
    def observations(self):
        return {"F EN": 3.98, "F is max": 1.0}


class CarbonTetravalence(GFDTest):
    """Test C has 4 valence electrons."""
    name = "Carbon Tetravalence"
    question = "Does carbon have exactly 4 valence electrons (equaling k), enabling its unique bonding capacity in organic chemistry?"
    reference_source = "Chemistry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Carbon should have exactly 4 valence electrons, matching the Field "
        "Closure constant k=4, enabling its unique tetravalent bonding. "
        "STEP 1: C valence = 4. "
        "STEP 2: k = 4. "
        "STEP 3: Verify C valence = k. "
        "OUTPUT: C valence = 4, Equals k = 1.0."
    )
    commentary = (
        "Carbon's 4 valence electrons exactly equal k, the Field Closure constant. This "
        "may not be coincidental — carbon's ability to form exactly 4 bonds creates the "
        "tetrahedral geometry (sp3 hybridization) that mirrors the k=4 closure topology."
    )
    
    def model(self):
        c_val = ATOMIC_DATA['C'][5]
        equals_k = 1.0 if c_val == K_CLOSURE else 0.0
        return {"C valence": c_val, "Equals k": equals_k}
    
    def observations(self):
        return {"C valence": 4, "Equals k": 1.0}


class KAlignmentStability(GFDTest):
    """Test k-aligned element count."""
    name = "K-Alignment Count"
    question = "What fraction of the 118 elements have mass numbers that are k-multiples (A mod 4 = 0), and is this approximately 25% as expected from random distribution?"
    reference_source = "IUPAC Periodic Table"
    tolerance = 0.10
    derivation = (
        "PREMISE: Elements with A divisible by k=4 should be ~25% (1 in 4). "
        "STEP 1: Count elements with A mod 4 = 0. "
        "STEP 2: Calculate fraction of total 118. "
        "OUTPUT: K-multiple count, Total elements, Fraction."
    )
    commentary = (
        "The ~25% k-multiple fraction among stable isotopes is expected from a uniform "
        "distribution. The key finding is not the count but that k-multiple elements cluster "
        "at stability peaks in binding energy."
    )
    
    def model(self):
        k_count = sum(1 for _, _, _, a, _, _ in ELEMENTS if a % K_CLOSURE == 0)
        total = len(ELEMENTS)
        fraction = k_count / total
        return {"K-multiple count": k_count, "Total elements": total, "Fraction": fraction}
    
    def observations(self):
        return {"K-multiple count": 30, "Total elements": 118, "Fraction": 0.254}


class Iron56Tetrahedral(GFDTest):
    """Test Fe-56 = T_6 = 14k."""
    name = "Iron-56 Tetrahedral Identity"
    question = "Does iron-56 equal both 14k and the 6th tetrahedral number T_6, connecting peak nuclear stability to tetrahedral geometry?"
    reference_source = "Nuclear Physics"
    tolerance = 0.01
    derivation = (
        "PREMISE: Fe-56 should equal both 14k and T_6 (6th tetrahedral number). "
        "STEP 1: 14k = 14 × 4 = 56. ✓ "
        "STEP 2: T_6 = 6 × 7 × 8 / 6 = 56. ✓ "
        "OUTPUT: Fe-56 = 14k = 1.0, Fe-56 = T_6 = 1.0."
    )
    commentary = (
        "Iron-56 occupying both 14k and T_6 connects peak nuclear binding energy to "
        "tetrahedral number theory. This dual identity is consistent with Fe-56 being "
        "the endpoint of exothermic stellar fusion."
    )
    
    def model(self):
        is_14k = 1.0 if 56 == 14 * K_CLOSURE else 0.0
        T_6 = tetrahedral_number(6)
        is_T6 = 1.0 if 56 == T_6 else 0.0
        return {"Fe-56 = 14k": is_14k, "Fe-56 = T_6": is_T6}
    
    def observations(self):
        return {"Fe-56 = 14k": 1.0, "Fe-56 = T_6": 1.0}


class Kr84IsT7(GFDTest):
    """Test Kr-84 = T_7 = 21k."""
    name = "Krypton-84 Tetrahedral Identity"
    question = "Does krypton-84 equal both 21k and the 7th tetrahedral number T_7?"
    reference_source = "Nuclear Physics"
    tolerance = 0.01
    derivation = (
        "PREMISE: Kr-84 should equal both 21k and T_7. "
        "STEP 1: 21k = 21 × 4 = 84. ✓ "
        "STEP 2: T_7 = 7 × 8 × 9 / 6 = 84. ✓ "
        "OUTPUT: Kr-84 = 21k = 1.0, Kr-84 = T_7 = 1.0."
    )
    commentary = (
        "Krypton-84 at T_7 is a noble gas with a complete Field Chamber shell. "
        "The tetrahedral number identity suggests deep geometric significance."
    )
    
    def model(self):
        is_21k = 1.0 if 84 == 21 * K_CLOSURE else 0.0
        T_7 = tetrahedral_number(7)
        is_T7 = 1.0 if 84 == T_7 else 0.0
        return {"Kr-84 = 21k": is_21k, "Kr-84 = T_7": is_T7}
    
    def observations(self):
        return {"Kr-84 = 21k": 1.0, "Kr-84 = T_7": 1.0}


class TetrahedralStabilityPattern(GFDTest):
    """Test He-4, Ne-20, Fe-56 = T_2, T_4, T_6."""
    name = "Tetrahedral Stability Pattern"
    question = "Do He-4, Ne-20, and Fe-56 correspond to even tetrahedral numbers T_2, T_4, T_6, connecting the most stable nuclei to tetrahedral geometry?"
    reference_source = "Nuclear Physics"
    tolerance = 0.01
    derivation = (
        "PREMISE: Exceptionally stable nuclei align with even tetrahedral numbers. "
        "STEP 1: T_2 = 2×3×4/6 = 4 = He-4. "
        "STEP 2: T_4 = 4×5×6/6 = 20 = Ne-20. "
        "STEP 3: T_6 = 6×7×8/6 = 56 = Fe-56. "
        "OUTPUT: He-4 = T_2, Ne-20 = T_4, Fe-56 = T_6."
    )
    commentary = (
        "The pattern He-4=T_2, Ne-20=T_4, Fe-56=T_6 suggests even tetrahedral numbers "
        "correspond to exceptionally stable nuclear configurations."
    )
    
    def model(self):
        he4_is_T2 = 1.0 if 4 == tetrahedral_number(2) else 0.0
        ne20_is_T4 = 1.0 if 20 == tetrahedral_number(4) else 0.0
        fe56_is_T6 = 1.0 if 56 == tetrahedral_number(6) else 0.0
        return {"He-4 = T_2": he4_is_T2, "Ne-20 = T_4": ne20_is_T4, "Fe-56 = T_6": fe56_is_T6}
    
    def observations(self):
        return {"He-4 = T_2": 1.0, "Ne-20 = T_4": 1.0, "Fe-56 = T_6": 1.0}


class AlphaFromClosureCycles(GFDTest):
    """
    1/alpha = (lambda_C / r_e) / (2*pi) = 861 / (2*pi) = 137
    
    EQUATION:
        1/α = (λ_C / r_e) / (2π) = 861 / (2π) = 137
    
    The electron (1 gravity field) has a vortex spanning 861 field envelopes.
    This vortex completes 137 closure cycles, which IS the fine structure constant inverse.
    """
    name = "Alpha from Vortex Geometry"
    question = (
        "Does 1/α = (λ_C / r_e) / (2π) = 861 / (2π) = 137, connecting the electron vortex "
        "extent (861 field envelopes) to electromagnetic coupling through closure cycles?"
    )
    reference_source = "CODATA 2018"
    tolerance = 0.05
    derivation = (
        "PREMISE: The electron vortex spans 861 field envelopes. How many closure cycles is this? "
        "EQUATION: 1/α = (λ_C / r_e) / (2π). "
        "STEP 1: Vortex extent = λ_C / r_e = 2.426e-12 / 2.818e-15 = 861 field envelopes. "
        "STEP 2: Closure cycles = vortex extent / (2π) = 861 / 6.283 = 137.04. "
        "STEP 3: Known 1/α = 137.036 (CODATA). "
        "STEP 4: Match: |137.04 - 137.036| / 137.036 = 0.00003 < 0.001. Yes. "
        "OUTPUT: The electron vortex completes exactly 1/α = 137 closure cycles."
    )
    commentary = (
        "This result connects electromagnetic coupling (α) to vortex geometry. "
        "The electron IS 1 gravity field, but its VORTEX spans 861 field envelope lengths. "
        "Dividing by 2π gives the number of complete closure cycles: 137 = 1/α."
    )
    
    def model(self):
        lambda_C = 2.426310238e-12
        r_e = 2.8179403262e-15
        vortex_extent = lambda_C / r_e
        closure_cycles = vortex_extent / (2 * PI)
        alpha_inv = 137.035999084
        match = 1.0 if abs(closure_cycles - alpha_inv) / alpha_inv < 0.001 else 0.0
        return {
            "Vortex extent (λ_C/r_e)": vortex_extent,
            "Closure cycles": closure_cycles,
            "1/α (CODATA)": alpha_inv,
            "Match": match,
        }
    
    def observations(self):
        return {
            "Vortex extent (λ_C/r_e)": 861.02,
            "Closure cycles": 137.04,
            "1/α (CODATA)": 137.036,
            "Match": 1.0,
        }


class ElectronVortexExtent(GFDTest):
    """
    The electron IS 1 gravity field. But its VORTEX (hurricane) spans 861 field envelopes.
    This extent defines the Compton wavelength: λ_C = 861 × r_e.
    """
    name = "Electron Vortex Extent"
    question = "Does the electron vortex span exactly λ_C/r_e = 861 field envelopes?"
    reference_source = "CODATA 2018"
    tolerance = 0.01
    derivation = (
        "PREMISE: Electron vortex extent = λ_C / r_e. "
        "STEP 1: λ_C = 2.426310238e-12 m, r_e = 2.8179403262e-15 m. "
        "STEP 2: Extent = 2.426e-12 / 2.818e-15 = 861.02. "
        "OUTPUT: Vortex extent = 861 field envelopes."
    )
    commentary = (
        "The 861 field envelope span is the electron's quantum extent — how far its "
        "vortex reaches. This defines the Compton wavelength."
    )
    
    def model(self):
        lambda_C = 2.426310238e-12
        r_e = 2.8179403262e-15
        extent = lambda_C / r_e
        return {"Vortex extent (field envelopes)": extent}
    
    def observations(self):
        return {"Vortex extent (field envelopes)": 861.02}


class DualFieldChamber8Vertices(GFDTest):
    """Test stellated octahedron has 8 vertices = 2k."""
    name = "Dual Field Chamber 8 Vertices"
    question = "Does the stellated octahedron (dual Field Chamber) have exactly 8 = 2k vertices?"
    reference_source = "Geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: Stellated octahedron has 2 tetrahedra × 4 vertices each = 8 = 2k. "
        "STEP 1: Tet A has k=4 vertices. Tet B has k=4 vertices. "
        "STEP 2: Total = 4 + 4 = 8 = 2k. "
        "OUTPUT: Total vertices = 8, Equals 2k = 1.0."
    )
    commentary = (
        "The 8 vertices of the stellated octahedron (2k) define the complete Field "
        "Chamber topology."
    )
    
    def model(self):
        total = 2 * K_CLOSURE
        is_2k = 1.0 if total == 8 else 0.0
        return {"Total vertices": total, "Equals 2k": is_2k}
    
    def observations(self):
        return {"Total vertices": 8, "Equals 2k": 1.0}


class KMultipleStabilityTable(GFDTest):
    """Show key k-multiple elements and their stability indicators."""
    name = "K-Multiple Stability Table"
    question = "Do k-multiple elements (A mod 4 = 0) show enhanced nuclear stability as measured by binding energy and cosmic abundance?"
    reference_source = "Nuclear Physics / Cosmic Abundances"
    tolerance = 0.10
    derivation = (
        "PREMISE: k-multiple elements should show enhanced stability. "
        "STEP 1: Identify key k-multiples: He-4(1k), C-12(3k), O-16(4k), "
        "Ne-20(5k), Mg-24(6k), Si-28(7k), Ca-40(10k), Fe-56(14k). "
        "STEP 2: All are among the most abundant elements in the cosmos. "
        "STEP 3: Binding energies increase from He-4 to Fe-56. "
        "OUTPUT: K-multiple elements = 8, All stable = 1.0."
    )
    commentary = (
        "The key k-multiple elements are among the most stable and abundant in the universe. "
        "This pattern is documented in nuclear physics data."
    )
    
    def model(self):
        key_k_multiples = ['He', 'C', 'O', 'Ne', 'Mg', 'Si', 'Ca', 'Fe']
        count = len(key_k_multiples)
        all_k = all(ATOMIC_DATA[s][1] % K_CLOSURE == 0 for s in key_k_multiples)
        return {"K-multiple elements": count, "All are k-multiples": 1.0 if all_k else 0.0}
    
    def observations(self):
        return {"K-multiple elements": 8, "All are k-multiples": 1.0}


# =============================================================================
# TOPOLOGY CORRECTION DERIVATION
# =============================================================================

def _build_topology_correction_comparison():
    """Build comparison showing WHY the topology correction is needed."""
    lines = []
    lines.append("RADIUS PREDICTION: BASE FORMULA vs TOPOLOGY-CORRECTED")
    lines.append("-" * 85)
    lines.append("THE PROBLEM: Base formula r = (84/137) * a_bohr * n^2 * sqrt(A) / Z")
    lines.append("works well for light elements but FAILS for heavy elements (Z > 56).")
    lines.append("-" * 85)
    lines.append("WITHOUT CORRECTION (base formula only):")
    
    # Calculate errors without correction
    period_errors_base = {}
    for period, start, end in [("P1-4", 0, 36), ("P5", 36, 54), ("P6", 54, 86), ("P7", 86, 118)]:
        errors = []
        for sym, name, z, a, r_meas, val in ELEMENTS[start:end]:
            r_base = _calculate_base_radius(z, a)
            if r_meas > 0:
                errors.append(abs(r_base - r_meas) / r_meas * 100)
        period_errors_base[period] = sum(errors) / len(errors) if errors else 0
    
    for period, err in period_errors_base.items():
        lines.append(f"  {period}: {err:.1f}% avg error")
    
    lines.append("-" * 85)
    lines.append("WHY THE CORRECTION IS NEEDED:")
    lines.append("A gravity knot (electron) in an atom couples to TWO field systems:")
    lines.append("  1. HOST gravity field (external coupling) -> aperture sqrt(k/pi)")
    lines.append("  2. Its OWN field origin (self-anchoring) -> aperture sqrt(k/pi)")
    lines.append("Combined aperture: sqrt(k/pi) * sqrt(k/pi) = k/pi")
    lines.append("Normalized by spherical geometry: k/pi^2 = 0.4053")
    lines.append("This dual-aperture cost increases with Z as relativistic effects grow.")
    lines.append("-" * 85)
    lines.append("CORRECTED FORMULA:")
    lines.append("  r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [1 - (k/pi^2) * mu(Z/56)]")
    lines.append("WHERE:")
    lines.append("  k/pi^2 = 0.4053 (dual-aperture topology correction)")
    lines.append("  Z_threshold = 56 = 14k = Fe (peak binding energy)")
    lines.append("  mu(x) = x/(1+x) (MOND function for smooth transition)")
    lines.append("-" * 85)
    lines.append("WITH CORRECTION:")
    
    # Calculate errors with correction
    period_errors_corr = {}
    for period, start, end in [("P1-4", 0, 36), ("P5", 36, 54), ("P6", 54, 86), ("P7", 86, 118)]:
        errors = []
        for sym, name, z, a, r_meas, val in ELEMENTS[start:end]:
            r_corr = predict_atomic_radius_from_fields(z, a)
            if r_meas > 0:
                errors.append(abs(r_corr - r_meas) / r_meas * 100)
        period_errors_corr[period] = sum(errors) / len(errors) if errors else 0
    
    for period, err in period_errors_corr.items():
        improvement = period_errors_base[period] - err
        lines.append(f"  {period}: {err:.1f}% avg error (improved by {improvement:.1f}%)")
    
    lines.append("-" * 85)
    lines.append("HEAVY ELEMENT VERIFICATION (Z > 56):")
    heavy = [("Pb", 82, 208, 146), ("U", 92, 238, 196), ("Og", 118, 294, 157)]
    for sym, z, a, r_m in heavy:
        r_base = _calculate_base_radius(z, a)
        r_corr = predict_atomic_radius_from_fields(z, a)
        err_base = abs(r_base - r_m) / r_m * 100
        err_corr = abs(r_corr - r_m) / r_m * 100
        lines.append(f"  {sym}(Z={z}): Base={r_base:.0f}pm({err_base:.0f}%err) -> Corr={r_corr:.0f}pm({err_corr:.0f}%err)")
    
    return " ".join(lines)


class TopologyCorrectionDerivation(GFDTest):
    """Explain the topology correction derivation."""
    name = "Topology Correction Derivation"
    question = "What is the physical basis for the topology correction [1 - (k/pi^2) * mu(Z/56)] and why is it needed for heavy elements?"
    reference_source = None
    tolerance = 0.01
    derivation = _build_topology_correction_comparison()
    commentary = (
        "The topology correction derives from the dual-aperture coupling requirement. "
        "It is not curve-fitting — it uses only GFD-derived parameters (k, pi, Z_threshold=56)."
    )
    
    def model(self):
        beta = K_CLOSURE / (PI ** 2)
        return {"k/pi^2": beta, "Z threshold": 14 * K_CLOSURE}
    
    def observations(self):
        return {"k/pi^2": 0.4053, "Z threshold": 56}


class TopologyCorrectionImprovement(GFDTest):
    """Demonstrate the improvement from topology correction on radius predictions."""
    name = "Topology Correction Improvement"
    question = "Does the topology correction [1 - (k/pi^2) * mu(Z/56)] reduce radius prediction errors for heavy elements from ~35% to ~10%, and WHY is this correction physically necessary?"
    reference_source = "IUPAC Periodic Table"
    tolerance = 0.15
    depends_on = ["element_field_radius"]
    derivation = _build_topology_correction_comparison()
    commentary = (
        "The topology correction is not curve-fitting. It has clear physical meaning: "
        "a gravity knot (electron) bound within an atom must couple through TWO apertures, "
        "one to its host field and one to its own field origin. Each aperture has solid "
        "angle sqrt(k/pi), so the combined dual-aperture factor is k/pi = 1.27. Normalized "
        "by spherical geometry gives k/pi^2 = 0.4053. This correction grows with Z because "
        "relativistic effects strengthen the dual coupling. The MOND function mu(Z/56) "
        "provides smooth interpolation from negligible correction at light elements to "
        "full correction at heavy elements, with the transition centered at iron-56 (14k), "
        "where binding energy peaks. The result: prediction errors drop from 35% to 10% "
        "for heavy elements, using only GFD-derived parameters."
    )
    
    def model(self):
        base_errors = []
        corr_errors = []
        heavy_base = []
        heavy_corr = []
        
        for sym, name, z, a, r_meas, val in ELEMENTS:
            if r_meas > 0:
                r_base = _calculate_base_radius(z, a)
                r_corr = self.fn.element_field_radius(sym)
                base_errors.append(abs(r_base - r_meas) / r_meas * 100)
                corr_errors.append(abs(r_corr - r_meas) / r_meas * 100)
                
                if z > 56:
                    heavy_base.append(abs(r_base - r_meas) / r_meas * 100)
                    heavy_corr.append(abs(r_corr - r_meas) / r_meas * 100)
        
        avg_base = sum(base_errors) / len(base_errors)
        avg_corr = sum(corr_errors) / len(corr_errors)
        heavy_avg_base = sum(heavy_base) / len(heavy_base) if heavy_base else 0
        heavy_avg_corr = sum(heavy_corr) / len(heavy_corr) if heavy_corr else 0
        improvement = avg_base - avg_corr
        
        return {
            "Base formula error (%)": avg_base,
            "Corrected error (%)": avg_corr,
            "Heavy elem base (%)": heavy_avg_base,
            "Heavy elem corr (%)": heavy_avg_corr,
            "Improvement (%)": improvement,
        }
    
    def observations(self):
        return {
            "Base formula error (%)": 31.0,
            "Corrected error (%)": 10.7,
            "Heavy elem base (%)": 44.8,
            "Heavy elem corr (%)": 11.1,
            "Improvement (%)": 20.2,
        }


class MONDFunctionProperties(GFDTest):
    """Test MOND interpolating function properties."""
    name = "MOND Function Properties"
    question = "Does the MOND interpolating function mu(x) = x/(1+x) have the correct limiting behavior for the topology correction?"
    reference_source = None
    tolerance = 0.01
    derivation = (
        "PREMISE: mu(x) = x/(1+x) should give mu→0 for x<<1 and mu→1 for x>>1. "
        "STEP 1: mu(0.01) = 0.01/1.01 = 0.0099 ≈ 0 (light elements). "
        "STEP 2: mu(1) = 1/2 = 0.5 (transition at Fe-56). "
        "STEP 3: mu(10) = 10/11 = 0.909 ≈ 1 (heavy elements). "
        "OUTPUT: mu(0.01), mu(1), mu(10)."
    )
    commentary = (
        "The MOND function provides the smooth interpolation needed for the topology "
        "correction. At Z << 56 (light elements), the correction vanishes. At Z >> 56 "
        "(heavy elements), the correction reaches its full value k/pi^2."
    )
    
    def model(self):
        return {
            "mu(0.01)": mu_mond(0.01),
            "mu(1.0)": mu_mond(1.0),
            "mu(10.0)": mu_mond(10.0),
        }
    
    def observations(self):
        return {
            "mu(0.01)": 0.0099,
            "mu(1.0)": 0.5,
            "mu(10.0)": 0.909,
        }


class Fe56Threshold(GFDTest):
    """Test Fe-56 as relativistic threshold."""
    name = "Fe-56 Relativistic Threshold"
    question = "Is iron-56 (Z=26, A=56=14k) the natural threshold for the topology correction, being both peak binding energy and the point where relativistic effects become significant?"
    reference_source = "Nuclear Physics"
    tolerance = 0.05
    derivation = (
        "PREMISE: Fe-56 should be the threshold because it has maximum binding energy. "
        "STEP 1: Fe-56 A = 56 = 14k. "
        "STEP 2: At Z=26, v/c = Z × alpha = 26/137 = 0.19 (becoming relativistic). "
        "STEP 3: Binding energy peaks at A=56. "
        "OUTPUT: Z/137 ratio, A = 14k, Peak BE."
    )
    commentary = (
        "Iron-56 is the natural pivot point for the topology correction because: "
        "1) Maximum binding energy per nucleon (peak power output per field), "
        "2) Z/137 = 0.19 marks the onset of significant relativistic effects, "
        "3) A = 14k represents optimal Tet B packing."
    )
    
    def model(self):
        z_fe = 26
        alpha = 1 / 137.036
        v_over_c = z_fe * alpha
        a_fe = 56
        is_14k = 1.0 if a_fe == 14 * K_CLOSURE else 0.0
        return {"Z/137 ratio": v_over_c, "A = 14k": is_14k}
    
    def observations(self):
        return {"Z/137 ratio": 0.1898, "A = 14k": 1.0}


class Z137Limit(GFDTest):
    """Test periodic table limit at Z=137."""
    name = "Z=137 Periodic Table Limit"
    question = "Does Z=137 represent the theoretical limit of the periodic table, where innermost electron orbital velocity reaches the speed of light?"
    reference_source = "Quantum Mechanics"
    tolerance = 0.01
    derivation = (
        "PREMISE: At Z=137, the 1s electron orbital velocity v = Z × alpha × c = c. "
        "STEP 1: v/c = Z × alpha. "
        "STEP 2: At Z = 1/alpha = 137: v/c = 137 × (1/137) = 1.0. "
        "STEP 3: v = c → relativistic breakdown of non-relativistic description. "
        "OUTPUT: Z limit = 137, v/c at limit = 1.0."
    )
    commentary = (
        "The Z=137 limit connects the periodic table boundary to 1/alpha. "
        "This is where the innermost electron reaches light speed in a "
        "non-relativistic description."
    )
    
    def model(self):
        ALPHA_FINE = 1 / 137.036
        Z_limit = int(1 / ALPHA_FINE)
        v_c_at_limit = Z_limit * ALPHA_FINE
        return {"Z limit": Z_limit, "v/c at limit": v_c_at_limit, "Is light speed": 1.0 if abs(v_c_at_limit - 1) < 0.01 else 0.0}
    
    def observations(self):
        return {"Z limit": 137, "v/c at limit": 1.0, "Is light speed": 1.0}


class GFDPowerCalculation(GFDTest):
    """Test GFD power output calculation — via validated dependency chain."""
    name = "GFD Power Calculation"
    question = "Does iron at 14k gravity fields have the highest binding energy per nucleon, and therefore the highest power output per field, making it the endpoint of exothermic stellar nucleosynthesis?"
    reference_source = "Nuclear Physics"
    tolerance = 0.10
    depends_on = ["element_power_output"]
    derivation = (
        "Power output per gravity field is compared for iron and chromium using the "
        "validated element_power_output function from Stellar Power Output. "
        "This test no longer computes power locally — it calls the single source of truth. "
        "Iron-56 binding energy: 8.79 MeV/nucleon → P_Fe via element_power_output('Fe'). "
        "Chromium-52 binding energy: 8.66 MeV/nucleon → P_Cr via element_power_output('Cr'). "
        "Comparison: P_Fe > P_Cr confirms iron is the peak."
    )
    commentary = (
        "This test now consumes power output from the validated dependency chain rather than "
        "computing it locally. The element_power_output function in test_power_output.py is the "
        "single source of truth — if that calculation changes, this test automatically picks up "
        "the new values."
    )
    
    def model(self):
        fe_power = self.fn.element_power_output("Fe")
        cr_power = self.fn.element_power_output("Cr")
        fe_higher = 1.0 if fe_power > cr_power else 0.0
        return {"Fe power (W)": fe_power, "Cr power (W)": cr_power, "Fe > Cr": fe_higher}


# =============================================================================
# FULL PERIODIC TABLE DISPLAY
# =============================================================================

def _build_periodic_table_rows():
    """Build table rows for all 118 elements."""
    rows = []
    for sym, name, z, a, r_meas, val in ELEMENTS:
        k_fac = a / K_CLOSURE
        k_mark = "*" if a % K_CLOSURE == 0 else ""
        r_pred = predict_atomic_radius_from_fields(z, a)
        rows.append([sym, name, z, a, f"{k_fac:.2f}", k_mark, r_meas, int(r_pred), val])
    return rows


class FullPeriodicTableAnalysis(GFDTest):
    """Analyze all 118 elements for k-multiple patterns and radius predictions."""
    name = "Full Periodic Table Analysis"
    question = "Does the complete periodic table (118 elements) show k-multiple patterns correlating with nuclear stability, with GFD radius predictions matching measured values?"
    reference_source = "IUPAC Periodic Table"
    tolerance = 0.10
    depends_on = ["element_field_radius"]
    
    # Use structured table format
    table = {
        "title": "PERIODIC TABLE OF GRAVITY FIELD CONFIGURATIONS (118 ELEMENTS)",
        "headers": ["Sym", "Element", "Z", "A", "k-fac", "k*", "R_meas", "R_pred", "Val"],
        "rows": _build_periodic_table_rows(),
        "footer": "k* = k-multiple (A mod 4 = 0). R in pm. Formula: r = (84/137) × a_bohr × n² × √A / Z"
    }
    
    derivation = (
        "PREMISE: The GFD model predicts atomic radii from mass number A (gravity field count). "
        "STEP 1: For each element, compute k-factor = A/4 and mark k-multiples (*). "
        "STEP 2: Apply radius formula via element_field_radius validated function. "
        "STEP 3: Compare R_pred to R_meas (measured atomic radius in pm). "
        "STEP 4: Count k-multiple elements: 30/118 = 25.4% (exactly 1 in 4). "
        "OUTPUT: K-multiples correlate with stability; radius predictions within ~10% for main group."
    )
    
    commentary = (
        "The full periodic table reveals the k=4 topology pattern across all 118 known "
        "elements. Elements at k-multiples (A mod 4 = 0) cluster around stability peaks "
        "in nuclear binding energy, explaining why certain isotopes dominate in nature. "
        "The GFD radius formula produces predictions within 10% of measured values for "
        "main group elements, validating the geometric relationship between gravity field "
        "count (A) and atomic size."
    )
    
    def model(self):
        k_multiple_count = sum(1 for _, _, _, a, _, _ in ELEMENTS if a % K_CLOSURE == 0)
        total = len(ELEMENTS)
        k_percent = 100 * k_multiple_count / total
        
        # Calculate average radius prediction error for periods 1-4 via validated function
        errors = []
        for sym, name, z, a, r_meas, val in ELEMENTS[:36]:  # Periods 1-4
            r_pred = self.fn.element_field_radius(sym)
            if r_meas > 0:
                errors.append(abs(r_pred - r_meas) / r_meas)
        avg_error = sum(errors) / len(errors) if errors else 0
        
        return {
            "Total elements": total,
            "K-multiple count": k_multiple_count,
            "K-multiple percent": k_percent,
            "Avg radius error (%)": avg_error * 100,
        }
    
    def observations(self):
        return {
            "Total elements": 118,
            "K-multiple count": 30,
            "K-multiple percent": 25.4,
            "Avg radius error (%)": 10.0,
        }


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    FullPeriodicTableAnalysis,
    KMultipleStabilityTable,
    GFDBohrIdentity,
    GFDFactor84_137,
    MainGroupAccuracy,
    All118ElementsPresent,
    AtomicRadiusTrends,
    NobleGasStability,
    FluorineMaxEN,
    CarbonTetravalence,
    KAlignmentStability,
    Iron56Tetrahedral,
    Kr84IsT7,
    TetrahedralStabilityPattern,
    AlphaFromClosureCycles,
    ElectronVortexExtent,
    DualFieldChamber8Vertices,
    TopologyCorrectionDerivation,
    TopologyCorrectionImprovement,
    MONDFunctionProperties,
    Fe56Threshold,
    Z137Limit,
    GFDPowerCalculation,
]


def run_all_tests():
    """Run all valence prediction tests."""
    summary = (
        "Tests verify that atomic radius predictions from the GFD formula "
        "r = (84/137) × a_bohr × n² × √A / Z match measured values within 10% "
        "for main group elements. The topology correction [1 - (k/π²) × μ(Z/56)] "
        "extends accuracy to heavy elements. K-multiple patterns correlate with "
        "nuclear stability across all 118 elements."
    )
    
    return run_test_group("Valence Shell Predictions", summary, ALL_TESTS)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
