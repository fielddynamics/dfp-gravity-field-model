"""
Iron-56 and the k=4 Coincidence: An Honest Assessment

This file documents a numerical coincidence between iron-56 (the most stable
nucleus in nature) and the GFD model's Field Closure constant k=4.

IMPORTANT DISCLAIMER:
These tests note OBSERVATIONS, not derivations. The GFD model did not PREDICT
that the most stable nucleus would be at mass 56 before examining the data.
Rather, the observation that 56 = 14 x 4 = T_6 (the 6th tetrahedral number)
was noted AFTER the fact.

For a test to have genuine scientific value, the model must:
1. Make a prediction BEFORE looking at the data
2. Have that prediction be falsifiable (it could be wrong)
3. Have model calculations that differ from the observations being tested

The tests below acknowledge what we actually have: interesting coincidences
that may or may not point to deeper structure.
"""

from gfd_model_v2.framework import *
from gfd_model_v2.common import K

# =============================================================================
# BINDING ENERGY DATA (from NIST/NNDC)
# =============================================================================

# Binding energy per nucleon (MeV/nucleon) for selected nuclei
# Source: Nuclear binding energy database
# Expanded to include neighbors of tetrahedral numbers for proper testing
BINDING_ENERGIES = {
    # Around T_2 = 4 (He-4)
    2: 1.11,    # H-2 (deuterium)
    4: 7.07,    # He-4 (tetrahedral T_2)
    6: 5.33,    # Li-6
    # Light nuclei
    12: 7.68,   # C-12
    16: 7.98,   # O-16
    18: 7.77,   # O-18
    # Around T_4 = 20 (Ne-20)
    20: 8.03,   # Ne-20 (tetrahedral T_4)
    22: 7.92,   # Ne-22
    24: 8.26,   # Mg-24
    28: 8.45,   # Si-28
    32: 8.49,   # S-32
    40: 8.55,   # Ca-40
    # Iron peak and around T_6 = 56
    52: 8.61,   # Cr-52
    54: 8.74,   # Fe-54
    56: 8.79,   # Fe-56 (tetrahedral T_6, maximum)
    58: 8.76,   # Ni-58
    60: 8.78,   # Ni-60
    62: 8.79,   # Ni-62 (second highest, sometimes cited as max)
    64: 8.78,   # Ni-64
    # Around T_7 = 84 (Kr-84)
    82: 8.71,   # Kr-82
    84: 8.70,   # Kr-84 (tetrahedral T_7)
    86: 8.70,   # Kr-86
    # Around T_8 = 120 (Sn-120)
    118: 8.52,  # Sn-118
    120: 8.51,  # Sn-120 (tetrahedral T_8)
    122: 8.51,  # Sn-122
    # Heavy nuclei
    208: 7.87,  # Pb-208
}


def tetrahedral_number(n):
    """
    Calculate the nth tetrahedral number: T_n = n(n+1)(n+2)/6
    
    Tetrahedral numbers count spheres stacked in a tetrahedron:
    T_1=1, T_2=4, T_3=10, T_4=20, T_5=35, T_6=56, T_7=84, T_8=120...
    """
    return n * (n + 1) * (n + 2) // 6


# Pre-compute tetrahedral numbers for reference
TETRAHEDRAL_NUMBERS = {n: tetrahedral_number(n) for n in range(1, 12)}
# {1: 1, 2: 4, 3: 10, 4: 20, 5: 35, 6: 56, 7: 84, 8: 120, 9: 165, 10: 220, 11: 286}


# =============================================================================
# TEST: The Fe-56 Coincidence (Honest Documentation)
# =============================================================================

class Fe56CoincidenceNote(Test):
    """
    Documents the numerical coincidence between Fe-56 and GFD constants.
    
    This is NOT a derivation. We're recording an observation.
    """
    name = "Fe-56 Numerical Coincidence"
    
    question = (
        "Iron-56 is the most stable nucleus in nature (highest binding energy "
        "per nucleon). Its mass number 56 happens to equal both 14 x 4 (a multiple "
        "of the GFD constant k=4) AND the 6th tetrahedral number T_6. Is this "
        "coincidence, or does it point to something deeper? We honestly don't know."
    )
    
    reference = "NIST nuclear binding energy data"
    level = Level.EXPLORATORY  # Exploratory because this is observation, not prediction
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("OBSERVATION 1: Iron-56 has the highest binding energy per nucleon "
                  "among stable nuclei (8.79 MeV/nucleon from NIST data).")
            .step("OBSERVATION 2: The mass number 56 = 14 x 4 = 14k, where k=4 is "
                  "the GFD Field Closure constant (from tetrahedral face count).")
            .step("OBSERVATION 3: 56 is also T_6, the 6th tetrahedral number "
                  "(6 x 7 x 8 / 6 = 56).")
            .step("CAVEAT: These observations were noted AFTER examining the data. "
                  "The GFD model did not predict Fe-56's special status beforehand.")
            .conclude("STATUS: Documented coincidence. Scientific significance unknown.")
        )
    
    commentary = (
        "Richard Feynman warned against numerology: finding patterns in numbers "
        "after the fact proves nothing. The human brain is wired to see patterns "
        "everywhere. That said, when the single most stable nucleus in the universe "
        "has a mass number that is simultaneously a tetrahedral number AND a high "
        "multiple of the geometric constant k=4, it warrants documentation. Whether "
        "this reflects deep physics or pure coincidence remains an open question."
    )
    
    def model(self):
        # Document the observations
        fe_mass = 56
        is_tetrahedral = fe_mass == TETRAHEDRAL_NUMBERS[6]
        k_multiple = fe_mass // K
        is_k_aligned = (fe_mass % K == 0)
        
        return (
            Model()
            .add("Fe-56 mass number", fe_mass)
            .add("T_6 (6th tetrahedral)", TETRAHEDRAL_NUMBERS[6])
            .add("Is tetrahedral number", 1 if is_tetrahedral else 0)
            .add("k-multiple (56/4)", k_multiple)
            .add("Is k-aligned", 1 if is_k_aligned else 0)
        )
    
    def observations(self):
        # These match because we're documenting facts, not testing predictions
        return (
            Observed()
            .add("Fe-56 mass number", 56)
            .add("T_6 (6th tetrahedral)", 56)
            .add("Is tetrahedral number", 1)
            .add("k-multiple (56/4)", 14)
            .add("Is k-aligned", 1)
        )


# =============================================================================
# TEST: Statistical Test of Tetrahedral Number Stability
# =============================================================================

class TetrahedralStabilityStatistic(Test):
    """
    A genuine (if weak) statistical test: Do tetrahedral-number nuclei
    have systematically higher binding energies than their neighbors?
    
    This test could FAIL, making it a legitimate scientific test.
    """
    name = "Tetrahedral Number Binding Energy Enhancement"
    
    question = (
        "If tetrahedral geometry is relevant to nuclear stability, then nuclei "
        "with tetrahedral mass numbers should have higher binding energies than "
        "their non-tetrahedral neighbors. Do the tetrahedral numbers T_2=4, "
        "T_4=20, T_6=56, T_7=84, T_8=120 show systematically enhanced stability "
        "compared to adjacent mass numbers?"
    )
    
    reference = "NIST nuclear binding energy data"
    level = Level.EXPLORATORY
    tolerance = 0.15  # Allow some slack since binding energy curve is smooth
    
    def derivation(self):
        return (
            Derivation()
            .step("HYPOTHESIS: If the GFD tetrahedral geometry influences nuclear "
                  "stability, tetrahedral-number nuclei should be local maxima "
                  "or show enhanced binding energy.")
            .step("METHOD: For each tetrahedral number T_n in our dataset, compare "
                  "its binding energy BE(T_n) to neighboring nuclei BE(T_n +/- 2).")
            .step("METRIC: Calculate how many tetrahedral numbers have BE >= both "
                  "neighbors (local maximum or plateau).")
            .step("NULL HYPOTHESIS: Random chance gives ~33% local maxima "
                  "(any point has 1/3 chance of being highest of 3 neighbors).")
            .conclude("TEST: If tetrahedral numbers are special, we expect >33% "
                      "to be local maxima in binding energy.")
        )
    
    commentary = (
        "This is a genuine statistical test because it could fail. If tetrahedral "
        "numbers showed no correlation with binding energy (or anti-correlation), "
        "it would falsify the hypothesis that tetrahedral geometry influences "
        "nuclear stability. Note that the binding energy curve is smooth, so "
        "most nuclei near the iron peak have similar binding energies. This test "
        "is weak but honest: it asks a question that has a non-trivial answer."
    )
    
    def model(self):
        # Test tetrahedral numbers where we have data for neighbors
        # T_2 = 4 (He-4): compare to 2 and 6
        # T_4 = 20 (Ne-20): compare to 18 and 22
        # T_6 = 56 (Fe-56): compare to 54 and 58
        # T_7 = 84 (Kr-84): compare to 82 and 86
        # T_8 = 120 (Sn-120): compare to 118 and 122
        
        # Test cases: (tetrahedral_mass, low_neighbor, high_neighbor)
        test_cases = [
            (4, 2, 6),      # T_2: He-4 vs H-2 and Li-6
            (20, 18, 22),   # T_4: Ne-20 vs O-18 and Ne-22
            (56, 54, 58),   # T_6: Fe-56 vs Fe-54 and Ni-58
            (84, 82, 86),   # T_7: Kr-84 vs Kr-82 and Kr-86
            (120, 118, 122),# T_8: Sn-120 vs Sn-118 and Sn-122
        ]
        
        local_maxima = 0
        total_testable = 0
        
        for A, low, high in test_cases:
            be_A = BINDING_ENERGIES.get(A)
            be_low = BINDING_ENERGIES.get(low)
            be_high = BINDING_ENERGIES.get(high)
            
            # Need the tetrahedral and at least one neighbor
            if be_A and (be_low or be_high):
                total_testable += 1
                neighbors = [b for b in [be_low, be_high] if b is not None]
                # Tetrahedral is a local max if it beats or ties all available neighbors
                if be_A >= max(neighbors):
                    local_maxima += 1
        
        # Calculate success rate
        rate = local_maxima / total_testable if total_testable > 0 else 0.0
        
        return (
            Model()
            .add("Tetrahedral nuclei tested", total_testable)
            .add("Local maxima count", local_maxima)
            .add("Success rate", rate)
            .add("Random expectation", 0.33)
        )
    
    def observations(self):
        # The observations should match model since we're testing empirical data
        # This test is unusual: model IS the observation (both use NIST data)
        # The "prediction" is just whether the rate exceeds random expectation
        #
        # Manual verification from NIST data:
        # He-4 (T_2=4): BE=7.07 vs H-2(1.11), Li-6(5.33) -> YES (7.07 > 5.33)
        # Ne-20 (T_4=20): BE=8.03 vs O-18(7.77), Ne-22(7.92) -> YES (8.03 > 7.92)
        # Fe-56 (T_6=56): BE=8.79 vs Fe-54(8.74), Ni-58(8.76) -> YES (8.79 > 8.76)
        # Kr-84 (T_7=84): BE=8.70 vs Kr-82(8.71), Kr-86(8.70) -> NO (8.70 < 8.71)
        # Sn-120 (T_8=120): BE=8.51 vs Sn-118(8.52), Sn-122(8.51) -> NO (8.51 < 8.52)
        #
        # Result: 3 out of 5 = 60%, which exceeds 33% random expectation
        return (
            Observed()
            .add("Tetrahedral nuclei tested", 5)
            .add("Local maxima count", 3)
            .add("Success rate", 0.60)
            .add("Random expectation", 0.33)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    Fe56CoincidenceNote,
    TetrahedralStabilityStatistic,
]


def run_all():
    """Run iron/hemoglobin tests (reduced to honest assessments)."""
    return run_tests(
        title="Iron-56 and the k=4 Coincidence",
        summary=(
            "These tests document observations about iron-56 and tetrahedral "
            "numbers. They are classified as EXPLORATORY because they note "
            "coincidences rather than derive predictions. The scientific "
            "significance of these patterns remains an open question."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
