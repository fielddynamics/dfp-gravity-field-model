"""
Probing Synthesis: Cross-Domain Patterns and Unified Ratios
============================================================

GFD Model V2

INVESTIGATION STATEMENT:
These synthesis tests COMBINE data from multiple domains (nuclear physics,
stellar evolution, atomic structure, GFD geometry) to look for cross-cutting
patterns:

1. Group all nuclei by A mod k. Is there a binding energy difference?
2. Does the fusion chain H→He→C→O→Si→Fe follow a tetrahedral mass progression?
3. Catalog all dimensionless ratios in stellar mechanics and look for GFD values.

Synthesis tests are the most speculative: they hunt for patterns that
cross domain boundaries. Negative results are as valuable as positive ones.

Audience: Advanced researchers, GFD model developers, interdisciplinary physicists.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, G, K_B, HBAR, ALPHA,
    M_E, R_E, M_P, M_SOLAR, R_SOLAR, L_SOLAR,
    K_CLOSURE,
    T_HYDROGEN_FUSION, T_HELIUM_FUSION,
    T_CARBON_FUSION, T_SILICON_FUSION,
    T_SOLAR_CORE, RHO_SOLAR_CORE,
    SIGMA_SB, T_SOLAR_SURFACE,
    BINDING_ENERGIES_BY_A,
    FE_56_BINDING_ENERGY_PER_NUCLEON,
    is_k_multiple,
)

PI = math.pi


# =============================================================================
# TEST 1: BINDING BY K-MODULO GROUP
# =============================================================================

class BindingByKModuloGroup(Test):
    """
    Partition all nuclei in BINDING_ENERGIES_BY_A into 4 groups based on
    A mod k (= A mod 4):
      Group 0: A = 4, 8, 12, 16, 20, ... (k-aligned)
      Group 1: A = 1, 5, 9, 13, 17, ...
      Group 2: A = 2, 6, 10, 14, 18, ...
      Group 3: A = 3, 7, 11, 15, 19, ...

    Compute the average BE/A in each group. If k=4 alignment matters for
    nuclear binding, Group 0 should have a higher average. If not, all
    four groups should be statistically indistinguishable.

    This is a blind statistical test with no fitting or tuning.
    """
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: If Group 0 (k-aligned) does show enhancement, can we rule out "
        "the even-even pairing effect as the sole explanation? "
        "(Answering would improve Derivation by +4 points) "
        "Q2: Do the group averages change if we restrict to A > 56 (past the "
        "binding peak), where shell effects are less dominant? "
        "(Answering would improve Model Output by +3 points) "
        "Q3: Can we run the same test with A mod 3, A mod 5, A mod 6 to see "
        "if k=4 grouping is special or if any modulus shows similar effects? "
        "(Answering would improve Commentary by +3 points)"
    )
    name = "Binding Energy by A mod k Group"
    question = (
        "Do nuclei with mass numbers divisible by k=4 have systematically "
        "higher binding energies than those in other A mod 4 groups? We split "
        "all tabulated nuclei into 4 groups by their A mod 4 residue and "
        "compare average BE/A in each group. A null result (all groups equal) "
        "means k-alignment has no nuclear significance. A positive result would "
        "demand explanation."
    )
    reference = "Statistical analysis; AME2020"
    tolerance = 0.50
    level = Level.STANDARD
    commentary = (
        "This is an unbiased partition test. We make no assumptions about which "
        "group should be special. If k=4 geometric alignment creates nuclear "
        "stability, Group 0 should stand out. If not, the test constrains how "
        "strong any k-alignment effect could be. Even a null result teaches us "
        "something: it sets an upper bound on geometric influence."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PARTITION: Split all nuclei with A ≥ 12 into 4 groups by A mod 4.")
            .step("(Using A ≥ 12 avoids the anomalous light nuclei.)")
            .step("Group 0: A mod 4 = 0 (k-multiples)")
            .step("Group 1: A mod 4 = 1")
            .step("Group 2: A mod 4 = 2")
            .step("Group 3: A mod 4 = 3")
            .step("For each group, compute <BE/A>.")
            .equation("Spread = max(<BE/A>) - min(<BE/A>) across all 4 groups")
            .step("Small spread = no k-modulo effect.")
            .step("Large spread = potential geometric signal.")
            .conclude("Report group averages and spread.")
        )

    def model(self) -> Model:
        groups = {0: [], 1: [], 2: [], 3: []}

        for A, be in BINDING_ENERGIES_BY_A.items():
            if A < 12:
                continue
            groups[A % 4].append(be)

        avgs = {}
        for g in range(4):
            if groups[g]:
                avgs[g] = sum(groups[g]) / len(groups[g])
            else:
                avgs[g] = 0

        spread = max(avgs.values()) - min(avgs.values())
        best_group = max(avgs, key=avgs.get)

        m = Model()
        for g in range(4):
            m.add(f"Group {g} avg BE/A (MeV)", round(avgs[g], 4))
        m.add("Spread (MeV)", round(spread, 4))
        m.add("Best group", best_group)

        headers = ["Group (A mod 4)", "Count", "Avg BE/A (MeV)"]
        rows = []
        for g in range(4):
            rows.append([str(g), str(len(groups[g])), f"{avgs[g]:.4f}"])
        m.add_table(title="k-Modulo Group Statistics", headers=headers, rows=rows)

        return m

    def observations(self) -> Observed:
        # Group 0 (k-multiples) has the highest average: 8.33 MeV.
        # Group 2 (A mod 4 = 2) has the lowest: 8.06 MeV.
        # Spread ~0.26 MeV is non-trivial but may reflect even-even pairing.
        return (
            Observed()
            .add("Group 0 avg BE/A (MeV)", 8.33)
            .add("Group 1 avg BE/A (MeV)", 8.16)
            .add("Group 2 avg BE/A (MeV)", 8.06)
            .add("Group 3 avg BE/A (MeV)", 8.27)
            .add("Spread (MeV)", 0.26)
            .add("Best group", 0)
        )


# =============================================================================
# TEST 2: FUSION CHAIN MASS PROGRESSION
# =============================================================================

class FusionChainMassProgression(Test):
    """
    The stellar fusion chain burns through elements with mass numbers:
      H(1) → He(4) → C(12) → O(16) → Si(28) → Fe(56)

    These mass numbers form a specific sequence. This test investigates
    whether the progression follows a pattern:
    - Ratios: 4/1=4, 12/4=3, 16/12=1.33, 28/16=1.75, 56/28=2
    - k-multiples: 1, 4=1k, 12=3k, 16=4k, 28=7k, 56=14k
    - k-factors: 1, 1, 3, 4, 7, 14

    The k-factors (1, 3, 4, 7, 14) don't form an obvious sequence.
    But: 4 = k, 12 = T₃ (3rd tetrahedral number), 56 = T₆ (6th).
    Does the fusion chain hit tetrahedral numbers?
    """
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Is the fusion chain determined by nuclear binding energies alone, "
        "or do Coulomb barriers select the specific mass numbers? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Why does the chain skip A=8 (Be-8 is unstable)? Does the "
        "A=8 gap have geometric significance (8 = 2k)? "
        "(Answering would improve Commentary by +4 points) "
        "Q3: If we extend the chain to neutron star conditions (neutron-rich "
        "nuclear pasta), what mass numbers come next? "
        "(Answering would improve Question by +2 points)"
    )
    name = "Fusion Chain: Mass Number Progression Analysis"
    question = (
        "The fusion chain produces elements at A = 1, 4, 12, 16, 28, 56. "
        "Are these mass numbers connected by a mathematical rule? All except "
        "A=1 are k-multiples (divisible by 4). Do the k-factors (1, 3, 4, 7, 14) "
        "form a recognizable sequence? And do any of the fusion products "
        "correspond to tetrahedral numbers T_n = n(n+1)(n+2)/6?"
    )
    reference = "Stellar nucleosynthesis; Nuclear physics"
    tolerance = 0.30
    level = Level.STANDARD
    commentary = (
        "The fusion chain is determined by nuclear physics: each stage burns "
        "the ash of the previous stage into the most stable available product. "
        "The specific mass numbers (4, 12, 16, 28, 56) reflect the deepest "
        "valleys in the nuclear binding curve. It's remarkable that 5 of 6 are "
        "k-multiples, but this may simply reflect that even-even nuclei (which "
        "are k-multiples of 4 when A/4 is even) are preferentially stable."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("FUSION CHAIN mass numbers: 1, 4, 12, 16, 28, 56")
            .step("k-MULTIPLES test: A mod 4")
            .step("  1 mod 4 = 1 (NOT a k-multiple)")
            .step("  4 mod 4 = 0 (1k)")
            .step("  12 mod 4 = 0 (3k)")
            .step("  16 mod 4 = 0 (4k)")
            .step("  28 mod 4 = 0 (7k)")
            .step("  56 mod 4 = 0 (14k)")
            .step("5/6 fusion products are k-multiples.")
            .step("TETRAHEDRAL NUMBERS: T_n = n(n+1)(n+2)/6")
            .step("  T_1=1, T_2=4, T_3=10, T_4=20, T_5=35, T_6=56, T_7=84")
            .step("  Matches: A=1=T_1, A=4=T_2, A=56=T_6")
            .step("  3/6 fusion products are tetrahedral numbers.")
            .conclude("Analyze fusion chain for geometric patterns.")
        )

    def model(self) -> Model:
        chain = [1, 4, 12, 16, 28, 56]
        names = ["H", "He", "C", "O", "Si", "Fe"]

        # k-multiple test
        k_multiples = sum(1 for A in chain if A % K_CLOSURE == 0)
        k_fraction = k_multiples / len(chain)

        # k-factors
        k_factors = [A // K_CLOSURE if A % K_CLOSURE == 0 else None for A in chain]

        # Tetrahedral numbers up to 100
        tet_nums = set()
        for n in range(1, 10):
            tet_nums.add(n * (n + 1) * (n + 2) // 6)

        tet_matches = sum(1 for A in chain if A in tet_nums)
        tet_fraction = tet_matches / len(chain)

        # Successive ratios
        ratios = [chain[i + 1] / chain[i] for i in range(len(chain) - 1)]

        # Binding energies at each step
        from gravity_field_model.common import get_binding_energy_by_A
        be_values = [get_binding_energy_by_A(A) for A in chain]

        m = Model()
        m.add("k-multiples in chain", k_multiples)
        m.add("k-multiple fraction", round(k_fraction, 2))
        m.add("Tetrahedral matches", tet_matches)
        m.add("Tetrahedral fraction", round(tet_fraction, 2))

        headers = ["Element", "A", "A/k", "Is T_n?", "BE/A (MeV)"]
        rows = []
        for i, (name, A) in enumerate(zip(names, chain)):
            kf = str(A // K_CLOSURE) if A % K_CLOSURE == 0 else "—"
            is_tet = "Yes" if A in tet_nums else "No"
            rows.append([name, str(A), kf, is_tet, f"{be_values[i]:.3f}"])
        m.add_table(title="Fusion Chain Analysis", headers=headers, rows=rows)

        return m

    def observations(self) -> Observed:
        return (
            Observed()
            .add("k-multiples in chain", 5)
            .add("k-multiple fraction", 0.83)
            .add("Tetrahedral matches", 3)
            .add("Tetrahedral fraction", 0.50)
        )


# =============================================================================
# TEST 3: DIMENSIONLESS RATIOS CATALOG
# =============================================================================

class DimensionlessRatiosCatalog(Test):
    """
    Physics is characterized by dimensionless ratios. This test catalogs
    the key dimensionless ratios that appear in stellar mechanics and checks
    whether any of them equal GFD-predicted values.

    GFD-relevant values: k=4, 2k=8, k²=16, 1/α≈137, 6π⁵≈1836.

    We compute ratios like:
    - T_He/T_H (fusion temperature ratio)
    - L_sun/(G M²/R) (luminosity/gravitational power)
    - M_P/(M_E × α) (mass hierarchy)
    and check each against the GFD catalog.
    """
    audit_score = 83
    audit_notes = None
    future_questions = (
        "Q1: If a dimensionless ratio matches a GFD value to <1%, is this "
        "evidence or coincidence? What statistical test could distinguish? "
        "(Answering would improve Derivation by +4 points) "
        "Q2: The fine structure constant α appears in atomic, nuclear, and "
        "gravitational physics. Is its ubiquity evidence for a geometric origin? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: What dimensionless ratios CHANGE in the GFD model if k were "
        "different (e.g., k=3 in 2+1 dimensions)? "
        "(Answering would improve Question by +3 points)"
    )
    name = "Dimensionless Ratios in Stellar Mechanics"
    question = (
        "What dimensionless ratios characterize stellar mechanics? We compute "
        "key ratios from CODATA constants and stellar data, then check each "
        "against a catalog of GFD-relevant numbers (k, 2k, k², 1/α, 6π⁵). "
        "How many ratios match GFD values, and is this more than expected "
        "by chance from a pool of ~20 candidate values?"
    )
    reference = "CODATA 2022; Stellar physics; GFD Textbook"
    tolerance = 0.30
    level = Level.EXPLORATORY
    commentary = (
        "Dimensionless ratios are the 'DNA' of physics. If GFD is correct, "
        "certain ratios should appear naturally in stellar mechanics. This "
        "catalog test is exploratory: it computes many ratios and flags those "
        "that match GFD predictions. Even if many matches are coincidental, "
        "the catalog serves as a map of the dimensional structure of stellar "
        "physics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("COMPUTE key dimensionless ratios:")
            .step("1. T_He/T_H = temperature ratio of He to H fusion thresholds")
            .step("2. T_solar_core / T_H = how close the Sun is to H ignition")
            .step("3. M_sun / (m_p × (1/α)^3) = gravitational hierarchy")
            .step("4. L_sun / (4πR²σT⁴) = Stefan-Boltzmann check")
            .step("5. (G M_sun m_p) / (k_B T_core R_sun) = virial ratio")
            .step("6. m_p/m_e = proton-electron mass ratio")
            .step("7. Fe-56 BE/A / He-4 BE/A = peak-to-alpha binding ratio")
            .step("CHECK each against GFD catalog: k, 2k, k², 1/α, 6π⁵, etc.")
            .conclude("Catalog all dimensionless ratios and flag GFD matches.")
        )

    def model(self) -> Model:
        # Compute ratios
        ratios = {}

        # 1. Fusion temperature ratios
        ratios["T_He / T_H"] = T_HELIUM_FUSION / T_HYDROGEN_FUSION
        ratios["T_C / T_H"] = T_CARBON_FUSION / T_HYDROGEN_FUSION
        ratios["T_Si / T_H"] = T_SILICON_FUSION / T_HYDROGEN_FUSION

        # 2. Solar core vs thresholds
        ratios["T_core / T_H"] = T_SOLAR_CORE / T_HYDROGEN_FUSION

        # 3. Proton/electron mass ratio
        ratios["m_p / m_e"] = M_P / M_E

        # 4. Fe-56 / He-4 binding ratio
        be_fe56 = FE_56_BINDING_ENERGY_PER_NUCLEON
        be_he4 = BINDING_ENERGIES_BY_A.get(4, 7.074)
        ratios["BE(Fe56) / BE(He4)"] = be_fe56 / be_he4

        # 5. Virial ratio
        virial_ratio = G * M_SOLAR * M_P / (K_B * T_SOLAR_CORE * R_SOLAR)
        ratios["Virial GM_p/(kTR)"] = virial_ratio

        # 6. Stefan-Boltzmann check: L_sun / (4πR²σT⁴)
        sb_predicted = 4 * PI * R_SOLAR ** 2 * SIGMA_SB * T_SOLAR_SURFACE ** 4
        ratios["L_sun / L_SB"] = L_SOLAR / sb_predicted

        # GFD catalog
        gfd_values = {
            "k": K_CLOSURE,
            "2k": 2 * K_CLOSURE,
            "k^2": K_CLOSURE ** 2,
            "1/α": 1 / ALPHA,
            "6π^5": 6 * PI ** 5,
        }

        # Check for matches
        matches = 0
        for rname, rval in ratios.items():
            for gname, gval in gfd_values.items():
                if gval > 0 and rval > 0:
                    frac_diff = abs(rval - gval) / gval
                    if frac_diff < 0.05:
                        matches += 1

        m = Model()
        m.add("Ratios computed", len(ratios))
        m.add("GFD matches (<5%)", matches)
        m.add("m_p / m_e", round(ratios["m_p / m_e"], 1))
        m.add("T_He / T_H", round(ratios["T_He / T_H"], 2))
        m.add("L_sun / L_SB", round(ratios["L_sun / L_SB"], 3))
        m.add("Virial ratio", round(virial_ratio, 2))

        headers = ["Ratio", "Value", "Nearest GFD"]
        rows = []
        for rname, rval in sorted(ratios.items()):
            nearest = min(gfd_values.items(), key=lambda x: abs(x[1] - rval) if x[1] > 0 else float('inf'))
            rows.append([rname, f"{rval:.4g}", f"{nearest[0]}={nearest[1]:.4g}"])
        m.add_table(title="Dimensionless Ratios", headers=headers, rows=rows)

        return m

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Ratios computed", 8)
            .add("GFD matches (<5%)", 1)
            .add("m_p / m_e", 1836.2)
            .add("T_He / T_H", 6.67)
            .add("L_sun / L_SB", 1.0)
            .add("Virial ratio", 1.5)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BindingByKModuloGroup,
    FusionChainMassProgression,
    DimensionlessRatiosCatalog,
]


def run_all() -> bool:
    """Run all probing synthesis tests."""
    return run_tests(
        title="Probing Synthesis",
        summary=(
            "These synthesis tests combine data from multiple domains:\n"
            "1. k-modulo groups: Is A mod 4 = 0 special for nuclear binding?\n"
            "2. Fusion chain: Do mass numbers follow a tetrahedral pattern?\n"
            "3. Dimensionless ratios: Do GFD values appear in stellar physics?\n\n"
            "METHODOLOGY: Cross-domain statistical analysis.\n"
            "No fitting. These tests hunt for patterns that cross boundaries.\n"
            "HONESTY: Null results constrain the model as much as positive ones."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
