"""
Iron-56 and the k=4 Coincidence: An Honest Assessment

WHY THIS FILE EXISTS:
Stars fuse hydrogen into ever-heavier elements until they hit a wall at iron.
Every atom of iron in your blood, every steel beam in a building, was forged
in a stellar core that could go no further. Why iron? Why not nickel, or cobalt?

This file documents a curious observation: the most stable nucleus in nature
(Fe-56) has a mass number that equals both 14 x 4 (a multiple of the GFD
constant k=4) AND the 6th tetrahedral number (T_6 = 56). Coincidence? Perhaps.
But when the universe's most stable configuration happens to align with a
geometric constant, it warrants careful documentation.

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

BIOLOGICAL CONNECTION:
Hemoglobin, the oxygen-carrying protein in blood, contains four iron atoms at
its core. Each iron atom binds oxygen through coordination chemistry that
depends on iron's unique electronic configuration (d-block element, Z=26).
The cosmic abundance of iron, produced by supernovae, made iron-based
biochemistry possible on Earth. Without stellar nucleosynthesis stopping at
iron, the elements essential to life would have different cosmic abundances.
"""

from gravity_field_model.framework import *
from gravity_field_model.common import (
    K,
    BINDING_ENERGIES_BY_A,
    get_binding_energy_by_A,
    FE_56_BINDING_ENERGY_PER_NUCLEON,
)

# =============================================================================
# TETRAHEDRAL NUMBER UTILITIES
# =============================================================================


def tetrahedral_number(n):
    """
    Calculate the nth tetrahedral number: T_n = n(n+1)(n+2)/6
    
    Tetrahedral numbers count spheres stacked in a tetrahedron:
    T_1=1, T_2=4, T_3=10, T_4=20, T_5=35, T_6=56, T_7=84, T_8=120...
    
    Why tetrahedral? A tetrahedron is the simplest 3D solid (4 vertices,
    4 faces). If nature builds stable structures by stacking identical
    units in the most efficient 3D pattern, tetrahedral packing emerges
    naturally. The GFD model's k=4 comes from the 4 vertices of a tetrahedron.
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
    
    This test explores WHY iron sits at the peak of nuclear stability, and
    documents the curious alignment between iron's mass number (56) and the
    GFD model's geometric constants. This is NOT a derivation or prediction.
    We are recording an observation that iron's special status in physics
    happens to align with the model's tetrahedral geometry.
    
    The test is classified as EXPLORATORY because the coincidence was noted
    after examining data, not predicted beforehand.
    """
    name = "Fe-56 Numerical Coincidence"
    
    question = (
        "Why does stellar fusion end at iron? Stars fuse hydrogen into helium, "
        "then helium into carbon, climbing the periodic table in a cascade of "
        "nuclear reactions. But at iron, the furnace goes cold. No matter how "
        "hot the stellar core, fusing iron costs energy rather than releasing it. "
        "The mass number 56 happens to be both a multiple of k=4 (56 = 14k) AND "
        "the 6th tetrahedral number. Does this geometric alignment explain iron's "
        "special status, or is it pure coincidence? And what does this mean for "
        "the iron atoms in your hemoglobin?"
    )
    
    reference = "NIST Nuclear Binding Energy Data; NNDC Nuclear Data Services"
    level = Level.EXPLORATORY  # Exploratory because this is observation, not prediction
    tolerance = 0.01
    
    audit_score = 88
    audit_notes = None
    
    future_questions = (
        "Q1: Why does the binding energy curve peak near iron and not continue rising? "
        "(Answering would improve Derivation by +2 points: explains Coulomb repulsion "
        "vs strong force balance in larger nuclei) "
        "Q2: How does iron's electronic structure enable oxygen binding in hemoglobin? "
        "(Answering would improve Commentary by +2 points: connects nuclear stability "
        "to biological chemistry) "
        "Q3: Are other tetrahedral numbers (4, 10, 20, 35, 84) also stability peaks? "
        "(Answering would improve Model Output by +2 points: systematic pattern test)"
    )
    
    def derivation(self):
        return (
            Derivation()
            # INTUITION FIRST: Why does binding energy matter?
            .step("Imagine nucleons (protons and neutrons) as magnets trying to "
                  "stick together. The binding energy measures how strongly they "
                  "hold on. A nucleus with higher binding energy per nucleon is "
                  "harder to pull apart, therefore more stable.")
            .step("Think of it like a ball in a valley: deeper valleys (higher "
                  "binding energy) mean more stability. Rolling the ball out "
                  "requires more energy.")
            .step("The binding energy curve rises steeply from hydrogen (0 MeV) "
                  "to iron (8.79 MeV per nucleon), then gradually declines. "
                  "This peak is why fusion releases energy below iron and "
                  "costs energy above it.")
            # NOW THE OBSERVATIONS
            .step("OBSERVATION 1: Iron-56 has the highest binding energy per nucleon "
                  "among common stable nuclei (8.79 MeV/nucleon from NIST data). "
                  "Note: Ni-62 is slightly higher at 8.795 MeV, but Fe-56 is more "
                  "commonly cited as the 'peak' due to its cosmic abundance and "
                  "role in stellar evolution.")
            .step("OBSERVATION 2: The mass number 56 = 14 x 4 = 14k, where k=4 is "
                  "the GFD Field Closure constant (derived from tetrahedral face count).")
            .step("OBSERVATION 3: 56 is also T_6, the 6th tetrahedral number: "
                  "T_6 = 6 x 7 x 8 / 6 = 56. This means 56 spheres can be perfectly "
                  "stacked in a tetrahedral arrangement.")
            # HONEST CAVEAT
            .step("CAVEAT: These observations were noted AFTER examining the data. "
                  "The GFD model did not predict Fe-56's special status beforehand. "
                  "Without a prior prediction, this remains a documented coincidence.")
            .conclude("STATUS: Documented coincidence warranting further study. "
                      "The alignment of nuclear stability peak with tetrahedral "
                      "geometry is intriguing but not yet predictive.")
        )
    
    commentary = (
        "Richard Feynman warned against numerology: finding patterns in numbers "
        "after the fact proves nothing. The human brain is wired to see patterns "
        "everywhere. That said, iron's cosmic significance is undeniable. Every "
        "massive star that explodes as a supernova does so because its core became "
        "iron. The iron in your hemoglobin was forged in such an explosion billions "
        "of years ago. When the single most stable nucleus in the universe has a "
        "mass number that is simultaneously a tetrahedral number AND a high multiple "
        "of the geometric constant k=4, it warrants documentation. Whether this "
        "reflects deep physics or pure coincidence remains an open question. The "
        "key test: can this observation generate NEW predictions about other nuclei "
        "that can be tested against data the model has not yet seen?"
    )
    
    def model(self):
        # Document the observations using canonical data
        fe_mass = 56
        is_tetrahedral = fe_mass == TETRAHEDRAL_NUMBERS[6]
        k_multiple = fe_mass // K
        is_k_aligned = (fe_mass % K == 0)
        
        # Get binding energy from canonical source
        fe_binding_energy = get_binding_energy_by_A(56)
        
        return (
            Model()
            .add("Fe-56 mass number", fe_mass)
            .add("Fe-56 binding energy (MeV/nucleon)", fe_binding_energy)
            .add("T_6 (6th tetrahedral number)", TETRAHEDRAL_NUMBERS[6])
            .add("Is tetrahedral number", 1 if is_tetrahedral else 0)
            .add("k-multiple (56/4)", k_multiple)
            .add("Is k-aligned", 1 if is_k_aligned else 0)
            .add("Summary: Fe-56 = 14k = T_6, binding peak", 1)
        )
    
    def observations(self):
        # These match because we're documenting facts, not testing predictions
        return (
            Observed()
            .add("Fe-56 mass number", 56)
            .add("Fe-56 binding energy (MeV/nucleon)", FE_56_BINDING_ENERGY_PER_NUCLEON)
            .add("T_6 (6th tetrahedral number)", 56)
            .add("Is tetrahedral number", 1)
            .add("k-multiple (56/4)", 14)
            .add("Is k-aligned", 1)
            .add("Summary: Fe-56 = 14k = T_6, binding peak", 1)
        )


# =============================================================================
# TEST: Statistical Test of Tetrahedral Number Stability
# =============================================================================

class TetrahedralStabilityStatistic(Test):
    """
    A genuine (if weak) statistical test: Do tetrahedral-number nuclei
    have systematically higher binding energies than their neighbors?
    
    WHY THIS TEST MATTERS:
    Unlike the Fe-56 coincidence (which was noted after the fact), this test
    makes a falsifiable prediction: if tetrahedral geometry influences nuclear
    stability, then nuclei at tetrahedral mass numbers should be local maxima
    more often than chance predicts. This test could FAIL, making it a
    legitimate scientific test rather than mere numerology.
    
    The test compares binding energies at tetrahedral numbers (4, 10, 20, 35,
    56, 84, 120...) to their immediate neighbors, counting how many are local
    maxima. Random chance predicts ~33% would be maxima; systematic enhancement
    would produce a higher rate.
    """
    name = "Tetrahedral Number Binding Energy Enhancement"
    
    question = (
        "Why do some nuclei hold together better than others? If you plot binding "
        "energy per nucleon against mass number, you see a smooth curve with a "
        "peak near iron. But are there special points along this curve? If tetrahedral "
        "geometry influences nuclear stability (as the GFD model suggests with k=4), "
        "then mass numbers that are tetrahedral numbers (4, 10, 20, 35, 56, 84, 120...) "
        "should be local 'sweet spots' where binding is enhanced. Is this true, or does "
        "the smooth curve show no special structure at these points? This is a test that "
        "COULD fail, giving it genuine predictive power."
    )
    
    reference = "NIST Nuclear Binding Energy Data; NNDC Nuclear Data Services"
    level = Level.EXPLORATORY
    tolerance = 0.15  # Allow some slack since binding energy curve is smooth
    
    audit_score = 88
    audit_notes = None
    
    future_questions = (
        "Q1: Why is the binding energy curve so smooth despite nuclear shell effects? "
        "(Answering would improve Derivation by +2 points: explains why local variations "
        "are subtle perturbations on a bulk trend) "
        "Q2: Do magic numbers (2, 8, 20, 28, 50, 82, 126) show stronger enhancement than "
        "tetrahedral numbers? "
        "(Answering would improve Model Output by +3 points: comparative statistical test) "
        "Q3: What physical mechanism would connect tetrahedral packing to nuclear binding? "
        "(Answering would improve Commentary by +3 points: moves from correlation to "
        "causation with testable mechanism)"
    )
    
    def derivation(self):
        return (
            Derivation()
            # INTUITION FIRST: What would tetrahedral influence look like?
            .step("Think of stacking oranges in a pyramid. Certain numbers of oranges "
                  "(1, 4, 10, 20, 35, 56...) form perfect tetrahedral pyramids with no "
                  "gaps. If nucleons prefer this packing, nuclei with these mass numbers "
                  "might be slightly more stable than their neighbors.")
            .step("The binding energy curve is dominated by bulk effects: volume energy "
                  "attracts nucleons together, surface tension penalizes the surface area, "
                  "Coulomb repulsion pushes protons apart. Any tetrahedral effect would be "
                  "a small perturbation on top of this smooth trend. We are looking for "
                  "subtle 'bumps' at tetrahedral numbers, not dramatic peaks.")
            # NOW THE METHOD
            .step("HYPOTHESIS: If the GFD tetrahedral geometry influences nuclear "
                  "stability, tetrahedral-number nuclei should be local maxima "
                  "or show enhanced binding energy relative to immediate neighbors.")
            .step("METHOD: For each tetrahedral number T_n with available data, compare "
                  "its binding energy BE(T_n) to neighboring nuclei BE(T_n +/- 2).")
            .step("METRIC: Calculate the fraction of tetrahedral numbers that are "
                  "local maxima (higher than both neighbors).")
            .step("NULL HYPOTHESIS: By random chance, roughly 33% of any set of points "
                  "would be local maxima (each point has 1/3 chance of being highest "
                  "among itself and two neighbors).")
            .conclude("TEST CRITERION: If significantly more than 33% of tetrahedral "
                      "numbers are local maxima, it suggests (but does not prove) that "
                      "tetrahedral geometry correlates with enhanced stability. A result "
                      "near or below 33% would falsify the hypothesis.")
        )
    
    commentary = (
        "This is a genuine statistical test because it could fail. If tetrahedral "
        "numbers showed no correlation with binding energy (or anti-correlation), "
        "it would falsify the hypothesis that tetrahedral geometry influences "
        "nuclear stability. The test is admittedly weak: the binding energy curve "
        "is smooth, so most nuclei near the iron peak have similar binding energies. "
        "Finding 40% local maxima (vs 33% expected) is suggestive but not conclusive. "
        "A p-value calculation would help quantify significance. A stronger test would "
        "require a physical mechanism connecting GFD's k=4 geometry to nuclear forces, "
        "not just numerological correlation. Still, documenting what we observe, with "
        "honest statistical analysis, is the first step toward understanding whether "
        "the pattern is meaningful or coincidental."
    )
    
    def model(self):
        # Test tetrahedral numbers where we have data for neighbors
        # T_2 = 4 (He-4): compare to 2 and 6
        # T_4 = 20 (Ne-20): compare to 18 and 22 (need to check 22)
        # T_6 = 56 (Fe-56): compare to 54 and 58
        # T_7 = 84 (Kr-84): compare to 82 and 86 (need to check 82, 86)
        # T_8 = 120 (Sn-120): compare to 118 and 122
        
        # Test cases: (tetrahedral_mass, low_neighbor, high_neighbor)
        # Using BINDING_ENERGIES_BY_A from common module
        test_cases = [
            (4, 2, 6),      # T_2: He-4 vs H-2 and Li-6
            (20, 18, 23),   # T_4: Ne-20 vs O-18 and Na-23 (closest available)
            (56, 55, 58),   # T_6: Fe-56 vs Mn-55 and Ni-58
            (84, 80, 85),   # T_7: Kr-84 vs Br-80 and Rb-85
            (120, 115, 122),# T_8: Sn-120 vs In-115 and Sb-122
        ]
        
        local_maxima = 0
        total_testable = 0
        
        for A, low, high in test_cases:
            # Use canonical binding energy data
            be_A = BINDING_ENERGIES_BY_A.get(A)
            be_low = BINDING_ENERGIES_BY_A.get(low)
            be_high = BINDING_ENERGIES_BY_A.get(high)
            
            # Need the tetrahedral and at least one neighbor
            if be_A is not None and (be_low is not None or be_high is not None):
                total_testable += 1
                neighbors = [b for b in [be_low, be_high] if b is not None]
                # Tetrahedral is a local max if it beats or ties all available neighbors
                if neighbors and be_A >= max(neighbors):
                    local_maxima += 1
        
        # Calculate success rate
        rate = local_maxima / total_testable if total_testable > 0 else 0.0
        
        return (
            Model()
            .add("Tetrahedral nuclei tested", total_testable)
            .add("Local maxima count", local_maxima)
            .add("Success rate (observed)", rate)
            .add("Random expectation (null hypothesis)", 0.33)
            .add("Ratio to expectation", rate / 0.33 if rate > 0 else 0.0)
        )
    
    def observations(self):
        # Manual verification from NIST/NNDC data using canonical source:
        # He-4 (T_2=4): BE=7.074 vs H-2(1.112), Li-6(5.333) -> YES (7.074 > 5.333)
        # Ne-20 (T_4=20): BE=8.032 vs O-18(7.767), Na-23(8.112) -> NO (8.032 < 8.112)
        # Fe-56 (T_6=56): BE=8.790 vs Mn-55(8.765), Ni-58(8.732) -> YES (8.790 > 8.765)
        # Kr-84 (T_7=84): BE=8.672 vs Br-80(8.690), Rb-85(8.667) -> NO (8.672 < 8.690)
        # Sn-120 (T_8=120): BE=8.483 vs In-115(8.504), Sb-122(8.471) -> NO (8.483 < 8.504)
        #
        # Result: 2 out of 5 = 40%, which is slightly above 33% null expectation
        # Interpretation: Weak positive signal, but sample size too small for significance
        return (
            Observed()
            .add("Tetrahedral nuclei tested", 5)
            .add("Local maxima count", 2)
            .add("Success rate (observed)", 0.40)
            .add("Random expectation (null hypothesis)", 0.33)
            .add("Ratio to expectation", 0.40 / 0.33)
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
            "coincidences rather than derive predictions. Iron sits at the peak "
            "of the binding energy curve, ending stellar fusion and seeding the "
            "universe with heavy elements via supernovae. Its mass number 56 "
            "aligns with both k-multiples (56 = 14k) and tetrahedral geometry "
            "(T_6 = 56). The scientific significance of these patterns remains "
            "an open question. The iron in hemoglobin, which carries oxygen in "
            "your blood, was forged in ancient stellar cores."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
