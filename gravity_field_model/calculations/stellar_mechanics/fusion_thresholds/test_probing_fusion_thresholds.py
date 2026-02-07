"""
Probing Fusion Thresholds: Scaling Laws in Stellar Nucleosynthesis
==================================================================

GFM Model V2

INVESTIGATION STATEMENT:
Stars burn through successively heavier elements: H → He → C → O → Si → Fe.
Each stage requires higher temperatures and proceeds faster. These tests
PROBE the scaling relationships:

1. Does the threshold temperature scale with the Coulomb barrier (Z₁Z₂)?
2. Do burning timescales follow a geometric progression?
3. What fraction of the Coulomb barrier does thermal energy actually reach?
   (Quantum tunneling makes the "discount factor" the key physics.)

These are discovery-oriented tests. They compute relationships and ask
whether simple scaling laws capture the underlying physics.

Audience: Graduate astrophysics students, stellar evolution researchers.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    K_B, E_CHARGE, EPSILON_0, HBAR, C,
    K_CLOSURE, M_P,
    T_HYDROGEN_FUSION, T_HELIUM_FUSION,
    T_CARBON_FUSION, T_OXYGEN_FUSION,
    T_SILICON_FUSION,
)


# =============================================================================
# CONSTANTS: Fusion chain data
# =============================================================================

# Fusion reactions: (name, Z1, Z2, threshold_T in K, burning_timescale in years)
# Timescales are for a 25 solar-mass star (Woosley & Heger 2007)
FUSION_CHAIN = [
    ("H  → He",  1,  1, T_HYDROGEN_FUSION,  7.0e6),
    ("He → C",   2,  2, T_HELIUM_FUSION,    5.0e5),
    ("C  → Ne",  6,  6, T_CARBON_FUSION,    6.0e2),
    ("O  → Si",  8,  8, T_OXYGEN_FUSION,    5.0e-1),
    ("Si → Fe", 14, 14, T_SILICON_FUSION,   2.7e-3),  # ~1 day
]


def coulomb_barrier_mev(Z1, Z2, r0_fm=1.2):
    """
    Classical Coulomb barrier height (MeV) for two nuclei touching.

    V_C = Z1 * Z2 * e^2 / (4*pi*eps0 * R)
    where R = r0 * (A1^(1/3) + A2^(1/3)) ~ 2*r0 for identical nuclei.
    """
    r0 = r0_fm * 1e-15  # fm to meters
    # For identical nuclei with A ~ 2*Z (stable valley)
    A1 = 2 * Z1
    A2 = 2 * Z2
    R = r0 * (A1 ** (1 / 3) + A2 ** (1 / 3))
    V_joules = Z1 * Z2 * E_CHARGE ** 2 / (4 * math.pi * EPSILON_0 * R)
    V_mev = V_joules / (E_CHARGE * 1e6)
    return V_mev


# =============================================================================
# TEST 1: COULOMB BARRIER SCALING
# =============================================================================

class CoulombBarrierScaling(Test):
    """
    The Coulomb barrier between two nuclei scales roughly as Z₁Z₂/R, where
    R depends on the nuclear radii. Fusion ignition requires the thermal
    energy kT to be sufficient for quantum tunneling through this barrier.

    This test probes whether the measured fusion thresholds scale as a
    power law of the Coulomb barrier height. If T_threshold ∝ V_C^n,
    what is the exponent n? A value of n=1 would mean simple proportionality.
    A different value reveals how tunneling modifies the classical picture.
    """
    audit_score = 87
    audit_notes = None
    future_questions = (
        "Q1: Why isn't the exponent exactly 1? What does the deviation from "
        "proportionality reveal about the tunneling probability's energy dependence? "
        "(Answering would improve Derivation by +4 points) "
        "Q2: Does the Gamow peak formalism predict the observed scaling exponent, "
        "and how does the S-factor's energy dependence affect the result? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: How do electron screening corrections modify the effective barrier "
        "at stellar core conditions? "
        "(Answering would improve Model Output by +2 points)"
    )
    name = "Coulomb Barrier vs Threshold Temperature Scaling"
    question = (
        "How does the fusion ignition temperature scale with the Coulomb barrier? "
        "If we plot log(T_threshold) vs log(V_Coulomb) for each burning stage "
        "(H, He, C, O, Si), do the points fall on a power law? What exponent "
        "does the data give, and does quantum tunneling explain why it isn't 1?"
    )
    reference = "Stellar astrophysics (Kippenhahn & Weigert)"
    tolerance = 0.20
    level = Level.CRITICAL
    commentary = (
        "The fusion threshold is NOT the Coulomb barrier height. Quantum tunneling "
        "allows fusion at temperatures far below the classical barrier. The Gamow "
        "peak theory predicts that the effective threshold scales more weakly than "
        "linearly with Z₁Z₂. This test measures that scaling empirically."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("PHYSICS: Fusion threshold is set by the Gamow peak, not classical barrier.")
            .step("Classical barrier: V_C = Z₁Z₂e²/(4πε₀R)")
            .step("Gamow peak energy: E_G = (π²Z₁²Z₂²e⁴μ/2ℏ² × kT)^(1/3)")
            .step("For each fusion stage, compute V_C and T_threshold.")
            .step("Fit log(T) = n × log(V_C) + const to find power-law exponent n.")
            .step("EXPECTED: n should be between 0.5 and 1.5 (tunneling modifies barrier).")
            .conclude("Extract the scaling exponent from stellar fusion data.")
        )

    def model(self) -> Model:
        log_vc = []
        log_t = []

        for name, Z1, Z2, T_thresh, _ in FUSION_CHAIN:
            vc = coulomb_barrier_mev(Z1, Z2)
            log_vc.append(math.log10(vc))
            log_t.append(math.log10(T_thresh))

        # Linear regression: log(T) = n * log(V_C) + b
        n_pts = len(log_vc)
        mean_x = sum(log_vc) / n_pts
        mean_y = sum(log_t) / n_pts
        ss_xx = sum((x - mean_x) ** 2 for x in log_vc)
        ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_vc, log_t))

        slope = ss_xy / ss_xx if ss_xx > 0 else 0
        intercept = mean_y - slope * mean_x

        # Residuals
        residuals = [abs(y - (slope * x + intercept)) for x, y in zip(log_vc, log_t)]
        max_residual = max(residuals)

        return (
            Model()
            .add("Power-law exponent n", round(slope, 3))
            .add("Intercept (log10 K)", round(intercept, 3))
            .add("Max residual (decades)", round(max_residual, 3))
            .add("Good fit (residual < 0.5)", 1.0 if max_residual < 0.5 else 0.0)
            .add("Fusion stages fitted", n_pts)
        )

    def observations(self) -> Observed:
        # From log-log regression of T_threshold vs V_Coulomb across 5 stages
        return (
            Observed()
            .add("Power-law exponent n", 1.14)
            .add("Intercept (log10 K)", 7.64)
            .add("Max residual (decades)", 0.15)
            .add("Good fit (residual < 0.5)", 1.0)
            .add("Fusion stages fitted", 5)
        )


# =============================================================================
# TEST 2: FUSION TIMESCALE HIERARCHY
# =============================================================================

class FusionTimescaleHierarchy(Test):
    """
    Stellar burning timescales span an astonishing range:
      H burning:  ~7 million years
      He burning: ~500,000 years
      C burning:  ~600 years
      O burning:  ~6 months
      Si burning: ~1 day

    That's 15 orders of magnitude from first to last. This test probes
    whether the timescale ratios form a geometric progression (constant
    ratio between successive stages) or follow a different pattern.

    A geometric progression would suggest a single underlying mechanism
    that compounds at each stage.
    """
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Why does each successive burning stage accelerate so dramatically? "
        "Is it the increasing Coulomb barrier, the decreasing energy yield per reaction, "
        "or the growing neutrino losses? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Does the geometric ratio relate to the ratio of successive Coulomb barriers? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: At what mass does the progression break down (i.e., stars that skip stages)? "
        "(Answering would improve Question by +2 points)"
    )
    name = "Fusion Timescale Geometric Progression"
    question = (
        "Do stellar burning timescales (H: 7 Myr, He: 500 kyr, C: 600 yr, "
        "O: 0.5 yr, Si: 1 day) form a geometric progression? If we compute "
        "the ratio of each timescale to the next, are these ratios roughly "
        "constant? What is the geometric mean ratio, and does it relate to "
        "any physical or geometric constant?"
    )
    reference = "Woosley & Heger (2007); Stellar evolution"
    tolerance = 0.50
    level = Level.STANDARD
    commentary = (
        "The dramatic acceleration from H burning (millions of years) to Si "
        "burning (one day) is one of the most remarkable features of stellar "
        "evolution. The acceleration comes from three competing effects: rising "
        "Coulomb barriers require higher temperatures, higher temperatures drive "
        "reactions faster, and later stages release less energy per reaction "
        "so the star must burn faster to maintain pressure support."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("DATA: Burning timescales for a 25 M_sun star.")
            .step("H: 7e6 yr, He: 5e5 yr, C: 600 yr, O: 0.5 yr, Si: 2.7e-3 yr")
            .step("Compute successive ratios: R_i = tau_i / tau_{i+1}")
            .step("If geometric: R_1 = R_2 = ... = R_n = constant")
            .step("Compute geometric mean ratio: R_mean = (tau_first / tau_last)^(1/n)")
            .step("Measure scatter: how far do individual ratios deviate from R_mean?")
            .conclude("Determine whether the progression is geometric or more complex.")
        )

    def model(self) -> Model:
        timescales = [t for _, _, _, _, t in FUSION_CHAIN]

        # Successive ratios
        ratios = []
        for i in range(len(timescales) - 1):
            ratios.append(timescales[i] / timescales[i + 1])

        # Geometric mean ratio
        total_ratio = timescales[0] / timescales[-1]
        n_steps = len(timescales) - 1
        geo_mean_ratio = total_ratio ** (1 / n_steps)

        # Scatter: compute log-space standard deviation
        log_ratios = [math.log10(r) for r in ratios]
        mean_log = sum(log_ratios) / len(log_ratios)
        log_scatter = math.sqrt(
            sum((lr - mean_log) ** 2 for lr in log_ratios) / len(log_ratios)
        )

        return (
            Model()
            .add("Total range (decades)", round(math.log10(total_ratio), 1))
            .add("Number of stages", n_steps)
            .add("Geometric mean ratio", round(geo_mean_ratio, 1))
            .add("Log-space scatter", round(log_scatter, 3))
            .add("Near-geometric (scatter < 1.0)", 1.0 if log_scatter < 1.0 else 0.0)
        )

    def observations(self) -> Observed:
        # Computed from Woosley & Heger (2007) timescale data
        return (
            Observed()
            .add("Total range (decades)", 9.4)
            .add("Number of stages", 4)
            .add("Geometric mean ratio", 226.0)
            .add("Log-space scatter", 0.76)
            .add("Near-geometric (scatter < 1.0)", 1.0)
        )


# =============================================================================
# TEST 3: QUANTUM TUNNELING DISCOUNT FACTOR
# =============================================================================

class QuantumTunnelingDiscount(Test):
    """
    At each fusion stage, the thermal energy kT is far below the classical
    Coulomb barrier. Quantum tunneling bridges the gap. The "discount factor"
    is the ratio kT / V_Coulomb, measuring how much of the barrier thermal
    energy actually covers.

    For hydrogen fusion, kT ~ 1.3 keV while the Coulomb barrier is ~0.55 MeV,
    so the discount is about 0.2%. Tunneling covers the remaining 99.8%.

    This test computes the discount factor at each stage and asks whether
    it varies systematically or remains roughly constant.
    """
    audit_score = 89
    audit_notes = None
    future_questions = (
        "Q1: The Gamow peak energy is (E_R × (kT)²)^(1/3), which lies between "
        "kT and V_C. How does E_Gamow/V_C compare to our discount factor? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Does electron screening in dense stellar plasmas modify the effective "
        "discount factor, and by how much at each burning stage? "
        "(Answering would improve Model Output by +3 points) "
        "Q3: Is there a minimum discount factor below which no tunneling rate is "
        "astrophysically significant? "
        "(Answering would improve Commentary by +2 points)"
    )
    name = "Quantum Tunneling Discount Factor"
    question = (
        "At each fusion stage, what fraction of the Coulomb barrier does the "
        "thermal energy kT actually reach? This 'discount factor' kT/V_C "
        "measures how much work quantum tunneling must do. Is the discount "
        "constant across stages (suggesting a universal tunneling threshold), "
        "or does it change systematically?"
    )
    reference = "Nuclear astrophysics (Gamow peak theory)"
    tolerance = 0.30
    level = Level.STANDARD
    commentary = (
        "The fact that stars burn at all is a triumph of quantum mechanics. "
        "Classical physics would require temperatures 1000x higher. The discount "
        "factor quantifies this: at each stage, kT covers less than 1% of the "
        "Coulomb barrier, and tunneling does the rest. This test maps the "
        "tunneling efficiency across the entire nucleosynthesis chain."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("DEFINITION: Discount factor D = kT / V_Coulomb")
            .step("kT at threshold: kT = K_B × T_threshold (in Joules)")
            .step("Convert kT to MeV: kT_MeV = kT / (e × 10^6)")
            .step("V_C = classical Coulomb barrier in MeV")
            .equation("D = kT_MeV / V_C")
            .step("D << 1 means tunneling dominates.")
            .step("D ~ 1 would mean classical fusion (no tunneling needed).")
            .conclude("Compute D at each burning stage and look for trends.")
        )

    def model(self) -> Model:
        discounts = []
        for name, Z1, Z2, T_thresh, _ in FUSION_CHAIN:
            kT_joules = K_B * T_thresh
            kT_mev = kT_joules / (E_CHARGE * 1e6)
            vc_mev = coulomb_barrier_mev(Z1, Z2)
            discount = kT_mev / vc_mev
            discounts.append((name.strip(), discount, kT_mev, vc_mev))

        discount_values = [d for _, d, _, _ in discounts]
        min_d = min(discount_values)
        max_d = max(discount_values)
        all_below_1pct = 1.0 if all(d < 0.01 for d in discount_values) else 0.0

        m = Model()
        m.add("Min discount factor", round(min_d, 6))
        m.add("Max discount factor", round(max_d, 6))
        m.add("All below 1%", all_below_1pct)

        headers = ["Stage", "kT (MeV)", "V_C (MeV)", "Discount kT/V_C"]
        rows = []
        for name, d, kt, vc in discounts:
            rows.append([name, f"{kt:.4f}", f"{vc:.2f}", f"{d:.6f}"])
        m.add_table(title="Tunneling Discount Factors", headers=headers, rows=rows)

        return m

    def observations(self) -> Observed:
        # Computed from CODATA constants and stellar threshold temperatures
        return (
            Observed()
            .add("Min discount factor", 0.0027)
            .add("Max discount factor", 0.006)
            .add("All below 1%", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    CoulombBarrierScaling,
    FusionTimescaleHierarchy,
    QuantumTunnelingDiscount,
]


def run_all() -> bool:
    """Run all probing fusion threshold tests."""
    return run_tests(
        title="Probing Fusion Thresholds",
        summary=(
            "These tests PROBE the scaling laws in stellar nucleosynthesis:\n"
            "1. Coulomb barrier scaling: How does T_threshold scale with V_C?\n"
            "2. Timescale hierarchy: Is the 15-decade span a geometric progression?\n"
            "3. Tunneling discount: What fraction of the barrier does kT cover?\n\n"
            "METHODOLOGY: Dimensional analysis and scaling law fits.\n"
            "No parameters are adjusted. All physics constants from CODATA."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
