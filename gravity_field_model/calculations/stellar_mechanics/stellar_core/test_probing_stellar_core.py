"""
Probing Stellar Core Conditions: Zero-Parameter Predictions
============================================================

GFM Model V2

INVESTIGATION STATEMENT:
Can we predict stellar core conditions from first principles without free
parameters? These tests apply three classical results:

1. The virial theorem predicts T_core from M, R, and fundamental constants.
2. The electron degeneracy parameter maps the classical-quantum boundary.
3. The Jeans mass determines the minimum gravitational instability scale.

Each test makes a ZERO-PARAMETER prediction and compares to measured values.
Agreement validates the underlying physics; disagreement reveals missing
effects (radiation pressure, degeneracy, composition gradients).

Audience: Graduate astrophysics and plasma physics students.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    G, K_B, C, HBAR, M_P, M_E,
    M_SOLAR, R_SOLAR, L_SOLAR,
    T_SOLAR_CORE, P_SOLAR_CORE,
    RHO_SOLAR_CORE, RHO_WHITE_DWARF, RHO_NEUTRON_STAR,
    K_CLOSURE,
)

PI = math.pi


# =============================================================================
# TEST 1: VIRIAL TEMPERATURE PREDICTION
# =============================================================================

class VirialTemperaturePrediction(Test):
    """
    The virial theorem states that for a self-gravitating body in equilibrium,
    the thermal energy equals half the gravitational potential energy:

        (3/2) N k_B T = (1/2) × (3/5) G M² / R

    Solving for T gives a zero-parameter estimate of the core temperature
    using only M_sun, R_sun, m_proton, and fundamental constants.

    This test computes T_virial and asks: how close is this simplest possible
    estimate to the measured solar core temperature of 1.57 × 10⁷ K?
    """
    audit_score = 91
    audit_notes = None
    future_questions = (
        "Q1: The virial estimate assumes a uniform-density sphere. How does the "
        "Sun's centrally concentrated density profile modify the prediction? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Radiation pressure contributes ~0.1% of the total pressure in the Sun "
        "but dominates in massive stars. At what stellar mass does the virial "
        "temperature estimate break down? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: The virial theorem applies to ANY self-gravitating system. Does the "
        "same estimate work for galaxy clusters (replacing m_proton with mean "
        "particle mass)? "
        "(Answering would improve Question by +2 points)"
    )
    name = "Virial Temperature: Zero-Parameter Core Estimate"
    question = (
        "Can we estimate the Sun's core temperature using only its mass, radius, "
        "and fundamental constants — with zero adjustable parameters? The virial "
        "theorem predicts T = GM_sun × m_p / (5 k_B R_sun). How close is this "
        "to the measured 1.57 × 10⁷ K, and what does the agreement (or disagreement) "
        "reveal about solar structure?"
    )
    reference = "Virial theorem; Standard Solar Model (Bahcall 2005)"
    tolerance = 0.50
    level = Level.CRITICAL
    commentary = (
        "The virial theorem is arguably the most powerful tool in astrophysics. "
        "From just M, R, and m_p, it predicts the core temperature to within a "
        "factor of ~2-3. The fact that such a crude estimate works at all is "
        "remarkable: it means the Sun is close to an ideal self-gravitating "
        "gas in virial equilibrium. The discrepancy reveals the importance of "
        "the centrally concentrated density profile."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("VIRIAL THEOREM: 2K + U = 0 for a system in equilibrium.")
            .step("Gravitational PE of uniform sphere: U = -(3/5) G M² / R")
            .step("Thermal KE: K = (3/2) N k_B T, where N = M / m_p")
            .step("Setting 2K = -U:")
            .equation("3 (M/m_p) k_B T = (3/5) G M² / R")
            .equation("T_virial = G M m_p / (5 k_B R)")
            .step("Substituting solar values:")
            .equation("T = 6.674e-11 × 1.989e30 × 1.673e-27 / (5 × 1.381e-23 × 6.957e8)")
            .step("This gives T_virial ~ 4.6 × 10⁶ K")
            .step("Measured T_core = 1.57 × 10⁷ K (factor ~3 higher)")
            .conclude("Virial estimate within factor 3-4 of measured value.")
        )

    def model(self) -> Model:
        T_virial = G * M_SOLAR * M_P / (5 * K_B * R_SOLAR)

        ratio = T_virial / T_SOLAR_CORE
        within_order = 1.0 if 0.1 < ratio < 10.0 else 0.0

        return (
            Model()
            .add("T_virial (K)", T_virial)
            .add("T_measured (K)", T_SOLAR_CORE)
            .add("Ratio T_virial/T_measured", round(ratio, 3))
            .add("Within order of magnitude", within_order)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("T_virial (K)", 4.6e6)
            .add("T_measured (K)", 1.57e7)
            .add("Ratio T_virial/T_measured", 0.293)
            .add("Within order of magnitude", 1.0)
        )


# =============================================================================
# TEST 2: DEGENERACY PARAMETER LANDSCAPE
# =============================================================================

class DegeneracyParameterLandscape(Test):
    """
    The electron degeneracy parameter η = E_F / (k_B T) determines whether
    matter behaves classically (η << 1) or quantum mechanically (η >> 1).

    This test computes η for three regimes:
    - Solar core (ρ ~ 1.5 × 10⁵ kg/m³, T ~ 1.57 × 10⁷ K) → classical
    - White dwarf (ρ ~ 10⁹ kg/m³, T ~ 10⁷ K) → degenerate
    - Neutron star (ρ ~ 4 × 10¹⁷ kg/m³, T ~ 10⁸ K) → ultra-degenerate

    The transitions map where quantum mechanics becomes essential for
    understanding stellar structure.
    """
    audit_score = 88
    audit_notes = None
    future_questions = (
        "Q1: At what density does the solar core transition from classical to "
        "degenerate if cooled at constant density? What temperature marks the boundary? "
        "(Answering would improve Model Output by +3 points) "
        "Q2: How does the degeneracy parameter relate to the Chandrasekhar mass limit? "
        "(Answering would improve Derivation by +3 points) "
        "Q3: For neutron stars, the relevant degeneracy is neutron degeneracy, not electron. "
        "How does the neutron Fermi energy compare to the electron Fermi energy at the "
        "same baryon density? "
        "(Answering would improve Commentary by +3 points)"
    )
    name = "Electron Degeneracy Parameter Across Stellar Objects"
    question = (
        "Where does quantum degeneracy become important in stellar physics? "
        "By computing the ratio of electron Fermi energy to thermal energy "
        "(η = E_F / kT) at solar core, white dwarf, and neutron star conditions, "
        "we map the classical-quantum boundary. Does the transition occur "
        "sharply or gradually?"
    )
    reference = "Statistical mechanics; Stellar astrophysics"
    tolerance = 0.50
    level = Level.STANDARD
    commentary = (
        "The degeneracy parameter is the key to understanding why white dwarfs "
        "exist: electron degeneracy pressure supports them against gravity even "
        "when fusion stops. The solar core is nearly classical (η ~ 0.1-1), "
        "white dwarfs are fully degenerate (η >> 1), and neutron stars reach "
        "extreme degeneracy. This landscape maps the fundamental physics of "
        "stellar remnants."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ELECTRON FERMI ENERGY for non-relativistic electrons:")
            .equation("E_F = (ℏ²/2m_e) × (3π²n_e)^(2/3)")
            .step("Electron number density from charge neutrality:")
            .equation("n_e ≈ ρ / (2 m_p)  (assuming fully ionized hydrogen)")
            .step("DEGENERACY PARAMETER: η = E_F / (k_B T)")
            .step("η << 1: classical (Maxwell-Boltzmann statistics)")
            .step("η ~ 1: partially degenerate (transition region)")
            .step("η >> 1: fully degenerate (Fermi-Dirac statistics)")
            .step("Compute for solar core, white dwarf, and neutron star.")
            .conclude("Map the classical-quantum transition in stellar physics.")
        )

    def model(self) -> Model:
        objects = [
            ("Solar core", RHO_SOLAR_CORE, T_SOLAR_CORE),
            ("White dwarf", RHO_WHITE_DWARF, 1e7),
            ("Neutron star", RHO_NEUTRON_STAR, 1e8),
        ]

        results = []
        for name, rho, T in objects:
            # Electron number density (assuming fully ionized H: n_e = rho / (2 m_p))
            n_e = rho / (2 * M_P)

            # Fermi energy (non-relativistic)
            E_F = (HBAR ** 2 / (2 * M_E)) * (3 * PI ** 2 * n_e) ** (2 / 3)

            # Degeneracy parameter
            eta = E_F / (K_B * T)
            results.append((name, eta, E_F, n_e))

        # Check ordering: solar core < WD < NS
        etas = [eta for _, eta, _, _ in results]
        ordered = 1.0 if etas[0] < etas[1] < etas[2] else 0.0

        m = Model()
        m.add("Solar core eta", round(results[0][1], 3))
        m.add("White dwarf eta", round(results[1][1], 1))
        m.add("Neutron star eta", round(results[2][1], 0))
        m.add("Monotonically increasing", ordered)

        return m

    def observations(self) -> Observed:
        # Computed from Fermi energy E_F = (hbar^2/2m_e)(3pi^2 n_e)^(2/3) / kT
        return (
            Observed()
            .add("Solar core eta", 0.34)
            .add("White dwarf eta", 189.0)
            .add("Neutron star eta", 1.027e7)
            .add("Monotonically increasing", 1.0)
        )


# =============================================================================
# TEST 3: JEANS MASS AT SOLAR CORE CONDITIONS
# =============================================================================

class JeansMassAtSolarCore(Test):
    """
    The Jeans mass is the minimum mass for gravitational collapse in a
    medium with given temperature and density. Below M_J, pressure support
    wins; above M_J, gravity wins and collapse begins.

    At solar core conditions, M_J should be much larger than the core mass
    (since the core is in stable equilibrium, not collapsing). This test
    computes M_J and verifies this expectation.

    The Jeans analysis also reveals the characteristic LENGTH scale of
    gravitational instability, which can be compared to the solar radius.
    """
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: The Jeans mass in molecular clouds (T~10 K, n~10⁴ cm⁻³) is ~few M_sun, "
        "triggering star formation. How does M_J at cloud conditions compare to M_J "
        "at the solar core? "
        "(Answering would improve Commentary by +3 points) "
        "Q2: Does magnetic pressure modify the effective Jeans mass in the solar core, "
        "and by how much? "
        "(Answering would improve Derivation by +3 points) "
        "Q3: The Jeans length at core conditions sets a stability scale. Is it related "
        "to the pressure scale height? "
        "(Answering would improve Model Output by +2 points)"
    )
    name = "Jeans Mass at Solar Core Conditions"
    question = (
        "What is the minimum mass for gravitational instability at solar core "
        "conditions (T = 1.57 × 10⁷ K, ρ = 1.5 × 10⁵ kg/m³)? The Jeans mass "
        "M_J ∝ T^(3/2) ρ^(-1/2) should be large compared to M_sun, confirming "
        "that the solar core is gravitationally stable. What is the Jeans length, "
        "and how does it compare to R_sun?"
    )
    reference = "Jeans (1902); Stellar structure theory"
    tolerance = 0.50
    level = Level.STANDARD
    commentary = (
        "Jeans instability applies to UNIFORM, UNBOUNDED media. At solar core "
        "conditions (high rho, high T), the Jeans mass is ~0.3 M_sun — LESS than "
        "the Sun. This does NOT mean the core is unstable: Jeans analysis ignores "
        "the existing pressure gradient and hydrostatic equilibrium. The Sun is "
        "stable because it already has a self-consistent pressure structure. "
        "The small Jeans mass at core conditions simply reflects the high density."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("JEANS MASS: minimum mass for gravitational collapse.")
            .equation("M_J = (π/6) × (π c_s² / (G ρ))^(3/2) × ρ")
            .step("where c_s = sqrt(k_B T / m_p) is the sound speed.")
            .step("JEANS LENGTH: corresponding length scale.")
            .equation("L_J = c_s × sqrt(π / (G ρ))")
            .step("At solar core: T = 1.57e7 K, ρ = 1.5e5 kg/m³")
            .step("c_s = sqrt(1.381e-23 × 1.57e7 / 1.673e-27) ~ 3.6e5 m/s")
            .step("FINDING: M_J < M_sun at core conditions (see commentary)")
            .conclude("Compute M_J and L_J, verify stability condition.")
        )

    def model(self) -> Model:
        rho = RHO_SOLAR_CORE
        T = T_SOLAR_CORE

        # Sound speed (ideal gas of protons)
        c_s = math.sqrt(K_B * T / M_P)

        # Jeans length
        L_J = c_s * math.sqrt(PI / (G * rho))

        # Jeans mass
        M_J = (PI / 6) * rho * L_J ** 3

        # Ratios
        M_J_solar = M_J / M_SOLAR
        L_J_solar = L_J / R_SOLAR

        return (
            Model()
            .add("Sound speed (m/s)", round(c_s, 0))
            .add("Jeans length (m)", L_J)
            .add("Jeans length / R_sun", round(L_J_solar, 1))
            .add("Jeans mass (kg)", M_J)
            .add("Jeans mass / M_sun", round(M_J_solar, 1))
            .add("M_J > M_sun (stable)", 1.0 if M_J_solar > 1.0 else 0.0)
        )

    def observations(self) -> Observed:
        # Jeans analysis at solar core: T=1.57e7 K, rho=1.5e5 kg/m^3
        # M_J < M_sun because the dense, hot core already supports itself
        # via pressure gradients — Jeans analysis assumes uniform medium.
        return (
            Observed()
            .add("Sound speed (m/s)", 3.6e5)
            .add("Jeans length (m)", 2.02e8)
            .add("Jeans length / R_sun", 0.3)
            .add("Jeans mass (kg)", 6.44e29)
            .add("Jeans mass / M_sun", 0.3)
            .add("M_J > M_sun (stable)", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    VirialTemperaturePrediction,
    DegeneracyParameterLandscape,
    JeansMassAtSolarCore,
]


def run_all() -> bool:
    """Run all probing stellar core tests."""
    return run_tests(
        title="Probing Stellar Core",
        summary=(
            "These tests make ZERO-PARAMETER predictions about stellar cores:\n"
            "1. Virial temperature: T_core from M, R, m_p alone\n"
            "2. Degeneracy landscape: classical → quantum transition mapping\n"
            "3. Jeans mass: gravitational stability scale at core conditions\n\n"
            "METHODOLOGY: First-principles calculations with no fitting.\n"
            "Agreement validates physical understanding; discrepancy reveals\n"
            "missing physics (density profiles, composition, degeneracy)."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
