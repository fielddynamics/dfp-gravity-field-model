"""
Vortex Eye Transit: Model Definitions
======================================

GFD Model V2

HONESTY STATEMENT:
This module defines GFD model concepts about the "vortex eye" (Field Origin)
and verifies internal consistency of those definitions. These are MODEL
DEFINITIONS, not physics derivations or predictions.

MODEL DEFINITIONS:
- Vortex eye = center of stellated octahedron = Field Origin
- Transit barrier = adopted from nuclear binding energies (~8 MeV)
- Cross-section = geometric calculation from model parameters
- Transit rate = model function (not derived from physics)

WHAT THIS MODULE DOES:
- Defines internal model parameters
- Verifies geometric consistency
- Shows model behavior (e.g., rate increases with temperature)

WHAT THIS MODULE DOES NOT DO:
- Derive nuclear binding energies
- Predict fusion rates
- Provide new physics beyond standard models

The "transit barrier" of ~8 MeV is ADOPTED from measured nuclear binding
energies, not derived from GFD geometry.
"""

import math
import numpy as np
from gravity_field_model.framework import *
from gravity_field_model.common import (
    VERTICES, TET_A, TET_B,
    G, C, HBAR, ELECTRON_MASS,
    R_E, M_E, A_0,
    RHO_FIELD_BINDING, K_CLOSURE,
    vortex_eye_size,
)


# =============================================================================
# CONSTANTS
# =============================================================================

MEV_TO_JOULES = 1.60218e-13
BINDING_ENERGY_PER_NUCLEON = 8.0 * MEV_TO_JOULES  # ~8 MeV adopted from nuclear data


def get_vertex_coords(v):
    coords = VERTICES[v]['coords']
    return np.array(coords, dtype=float)


def calculate_field_origin():
    all_coords = [get_vertex_coords(v) for v in range(8)]
    return np.mean(all_coords, axis=0)


def vortex_eye_cross_section(tile_size=R_E):
    """Model-defined cross-section (not physically derived)."""
    eye_radius = tile_size / 4
    return math.pi * eye_radius**2


def energy_barrier_estimate():
    """Return adopted barrier from nuclear binding energies."""
    return BINDING_ENERGY_PER_NUCLEON


def transit_rate(temperature, barrier):
    """
    Model function for transit rate vs temperature.

    HONESTY: This is a model function, not a derivation of fusion rates.
    It shows qualitative behavior (rate increases with T) but is not
    quantitatively predictive.
    """
    K_B = 1.380649e-23
    if temperature <= 0:
        return 0.0
    thermal_energy = K_B * temperature
    gamow_factor = (thermal_energy / barrier) ** (1/3)
    effective_barrier = barrier * gamow_factor
    exponent = -effective_barrier / thermal_energy
    if exponent < -700:
        return 0.0
    return math.exp(exponent)


# =============================================================================
# TEST 1: TRANSIT ENERGY BARRIER (Adopted from Nuclear Data)
# =============================================================================

class TransitEnergyBarrier(Test):
    """
    State the adopted transit barrier.

    HONESTY: ~8 MeV is adopted from nuclear binding energies.
    It is NOT derived from GFD geometry.
    """
    name = "Transit Energy Barrier"
    question = (
        "What is the adopted transit barrier in the GFD model?"
    )
    reference = "Nuclear Physics (binding energies)"
    tolerance = 0.20
    level = Level.STANDARD
    commentary = (
        "The transit barrier of ~8 MeV is ADOPTED from measured nuclear "
        "binding energies (average BE/nucleon near Fe-56). GFD does not "
        "derive this value. It is a model parameter taken from nuclear data."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MODEL PARAMETER: Transit barrier adopted from nuclear data.")
            .step("Nuclear binding energies peak at ~8.8 MeV/nucleon (Fe-56).")
            .step("GFD adopts ~8 MeV as representative barrier energy.")
            .equation("Barrier = 8.0 MeV = 1.28e-12 J")
            .step("This is NOT derived from GFD. It is taken from measurements.")
            .conclude("Transit barrier = 8 MeV (adopted).")
        )

    def model(self) -> Model:
        barrier = energy_barrier_estimate()
        barrier_mev = barrier / MEV_TO_JOULES
        return (
            Model()
            .add("Transit barrier (J)", barrier)
            .add("Transit barrier (MeV)", barrier_mev)
            .add("In 1-20 MeV range", 1.0 if 1 < barrier_mev < 20 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Transit barrier (J)", 1.28e-12)
            .add("Transit barrier (MeV)", 8.0)
            .add("In 1-20 MeV range", 1.0)
        )


# =============================================================================
# TEST 2: STELLATED OCTAHEDRON SYMMETRY (Geometry)
# =============================================================================

class StellatedOctahedronSymmetry(Test):
    """
    Verify Tet A and Tet B are equidistant from center.

    HONESTY: This is geometry, not physics.
    """
    name = "Tet A / Tet B Symmetry"
    question = (
        "Are Tet A and Tet B equidistant from the Field Origin?"
    )
    reference = "Geometry"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The stellated octahedron consists of two interpenetrating tetrahedra "
        "centered at the origin. By construction, both are equidistant from "
        "the center. This is geometry, not a physics prediction."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Stellated octahedron structure.")
            .step("Two tetrahedra share center at (0,0,0).")
            .step("All vertices at (+/-1, +/-1, +/-1).")
            .equation("Distance = sqrt(3) = 1.732 for all vertices")
            .step("By symmetry, avg(Tet A) = avg(Tet B) = sqrt(3).")
            .conclude("Symmetric by construction.")
        )

    def model(self) -> Model:
        origin = calculate_field_origin()
        tet_a_dists = [np.linalg.norm(get_vertex_coords(v) - origin) for v in TET_A]
        tet_b_dists = [np.linalg.norm(get_vertex_coords(v) - origin) for v in TET_B]
        avg_a = np.mean(tet_a_dists)
        avg_b = np.mean(tet_b_dists)
        return (
            Model()
            .add("Tet A avg distance", avg_a)
            .add("Tet B avg distance", avg_b)
            .add("Symmetric", 1.0 if abs(avg_a - avg_b) < 0.001 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Tet A avg distance", 1.732)
            .add("Tet B avg distance", 1.732)
            .add("Symmetric", 1.0)
        )


# =============================================================================
# TEST 3: VORTEX EYE SIZE (Model Definition)
# =============================================================================

class VortexEyeSize(Test):
    """
    State the model-defined vortex eye size.

    HONESTY: r_e/4 is a model definition, not a derivation.
    """
    name = "Vortex Eye Size"
    question = (
        "What is the vortex eye size in the GFD model?"
    )
    reference = "Model Definition"
    tolerance = 0.05
    level = Level.STANDARD
    commentary = (
        "The vortex eye size is defined as r_e/4 in the GFD model. This is "
        "a MODEL DEFINITION, not a derivation. The factor 1/4 is chosen, "
        "not derived from first principles."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MODEL DEFINITION: Vortex eye size.")
            .step("r_e = 2.818 fm (classical electron radius).")
            .step("GFD DEFINES eye radius = r_e / 4.")
            .equation("Eye radius = 2.818 / 4 = 0.705 fm")
            .step("This is a model parameter, not derived.")
            .conclude("Vortex eye = r_e/4 by definition.")
        )

    def model(self) -> Model:
        eye_size = vortex_eye_size(R_E)
        expected = R_E / 4
        return (
            Model()
            .add("Eye size (m)", eye_size)
            .add("r_e/4 (m)", expected)
            .add("Match", 1.0 if abs(eye_size - expected) / expected < 0.01 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Eye size (m)", R_E / 4)
            .add("r_e/4 (m)", R_E / 4)
            .add("Match", 1.0)
        )


# =============================================================================
# TEST 4: TRANSIT RATE VS TEMPERATURE (Model Behavior)
# =============================================================================

class TransitRateTemperature(Test):
    """
    Show model rate increases with temperature.

    HONESTY: This shows model behavior, not a physics derivation.
    The model function is qualitative, not quantitatively predictive.
    """
    name = "Transit Rate vs Temperature"
    question = (
        "Does the model transit rate increase with temperature?"
    )
    reference = "Model Definition"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The model transit rate function increases with temperature. This "
        "is qualitatively consistent with thermally activated processes but "
        "is not a derivation of fusion rates. It shows model behavior."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MODEL FUNCTION: Transit rate vs temperature.")
            .step("Higher T = more thermal energy = higher tunneling probability.")
            .step("Qualitatively correct behavior for activated processes.")
            .step("NOT a quantitative derivation of fusion rates.")
            .conclude("Rate increases with T (model behavior).")
        )

    def model(self) -> Model:
        barrier = energy_barrier_estimate()
        T_low = 1e7
        T_med = 1e8
        T_high = 1e9
        rate_low = transit_rate(T_low, barrier)
        rate_med = transit_rate(T_med, barrier)
        rate_high = transit_rate(T_high, barrier)
        increasing = 1.0 if rate_low <= rate_med <= rate_high else 0.0
        return (
            Model()
            .add("Rate at 10^7 K", rate_low)
            .add("Rate at 10^8 K", rate_med)
            .add("Rate at 10^9 K", rate_high)
            .add("Monotonic increase", increasing)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Rate at 10^7 K", 0.0)
            .add("Rate at 10^8 K", 0.0)
            .add("Rate at 10^9 K", 1.0)
            .add("Monotonic increase", 1.0)
        )


# =============================================================================
# TEST 5: FIELD ORIGIN STABILITY (Geometry)
# =============================================================================

class FieldOriginStability(Test):
    """
    Verify Field Origin is at center.

    HONESTY: By construction, the origin is at (0,0,0).
    """
    name = "Field Origin Position"
    question = (
        "Is the Field Origin at the center (0,0,0) of the stellated octahedron?"
    )
    reference = "Geometry"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The Field Origin is defined as the centroid of the stellated "
        "octahedron vertices. With vertices at (+/-1, +/-1, +/-1), the "
        "centroid is (0,0,0) by symmetry. This is geometry, not physics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Centroid of stellated octahedron.")
            .step("Vertices at (+/-1, +/-1, +/-1).")
            .step("Centroid = average = (0, 0, 0).")
            .conclude("Field Origin at center by construction.")
        )

    def model(self) -> Model:
        origin = calculate_field_origin()
        at_center = 1.0 if np.allclose(origin, [0, 0, 0]) else 0.0
        return (
            Model()
            .add("Origin x", origin[0])
            .add("Origin y", origin[1])
            .add("Origin z", origin[2])
            .add("At center", at_center)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Origin x", 0.0)
            .add("Origin y", 0.0)
            .add("Origin z", 0.0)
            .add("At center", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    TransitEnergyBarrier,
    StellatedOctahedronSymmetry,
    VortexEyeSize,
    TransitRateTemperature,
    FieldOriginStability,
]


def run_all() -> bool:
    """Run all vortex transit tests."""
    return run_tests(
        title="Vortex Eye Transit",
        summary=(
            "These tests define GFD model parameters and verify internal consistency.\n\n"
            "MODEL DEFINITIONS (not derivations):\n"
            "- Transit barrier = 8 MeV (adopted from nuclear data)\n"
            "- Vortex eye size = r_e/4 (defined, not derived)\n"
            "- Field Origin = stellated octahedron center\n\n"
            "GEOMETRY VERIFIED:\n"
            "- Tet A and Tet B symmetric about origin\n"
            "- Field Origin at (0,0,0) by construction\n\n"
            "MODEL BEHAVIOR:\n"
            "- Transit rate increases with temperature (qualitative)\n\n"
            "CLARIFICATION: This module defines model parameters. The ~8 MeV\n"
            "barrier is taken from nuclear physics, not derived from GFD.\n"
            "The geometric relationships follow from the stellated octahedron\n"
            "construction, not from physics principles."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
