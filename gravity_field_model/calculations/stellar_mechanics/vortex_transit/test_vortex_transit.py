"""
Vortex Eye Transit: Model Definitions
======================================

GFM Model V2

HONESTY STATEMENT:
This module defines GFM model concepts about the "vortex eye" (Field Origin)
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
energies, not derived from GFM geometry.

TEST GROUP GOALS:
This module introduces the concept of the Field Origin (vortex eye) and its
role in the GFM model. Students learn to distinguish model definitions from
physics predictions, understanding that the ~8 MeV barrier is adopted from
nuclear data rather than derived from geometry.

Audience: Undergraduate physics students familiar with the GFM model basics.
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
    It is NOT derived from GFM geometry.
    """
    audit_score = 76
    audit_notes = None
    future_questions = (
        "Q1: Why is ~8 MeV (the average binding energy per nucleon) an appropriate "
        "choice for the transit barrier rather than the Coulomb barrier height? "
        "(Answering would improve Derivation by +3 points: parameter choice justification) "
        "Q2: How would the model predictions change if the barrier were 5 MeV or 12 MeV? "
        "(Answering would improve Model Output by +3 points: sensitivity analysis) "
        "Q3: What physical mechanism does the 'transit barrier' represent in GFM language "
        "versus standard nuclear physics? "
        "(Answering would improve Commentary by +2 points: terminology mapping)"
    )
    name = "Transit Energy Barrier"
    question = (
        "Why does GFM adopt ~8 MeV as the transit barrier energy, and why is "
        "this value taken from nuclear binding data rather than derived from "
        "the model's geometry?"
    )
    reference = "Nuclear Physics (binding energies)"
    tolerance = 0.20
    level = Level.STANDARD
    commentary = (
        "The transit barrier of ~8 MeV is ADOPTED from measured nuclear "
        "binding energies (average BE/nucleon near Fe-56). GFM does not "
        "derive this value. It is a model parameter taken from nuclear data."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MODEL PARAMETER: Transit barrier adopted from nuclear data.")
            .step("Nuclear binding energies peak at ~8.8 MeV/nucleon (Fe-56).")
            .step("GFM adopts ~8 MeV as representative barrier energy.")
            .equation("Barrier = 8.0 MeV = 1.28e-12 J")
            .step("This is NOT derived from GFM. It is taken from measurements.")
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
    audit_score = 74
    audit_notes = None
    future_questions = (
        "Q1: Why is the stellated octahedron (star tetrahedron, Merkaba) chosen as the "
        "fundamental geometry rather than other polyhedra? "
        "(Answering would improve Question by +4 points: motivates geometry choice) "
        "Q2: What is the physical interpretation of Tet A versus Tet B in the GFM model? "
        "(Answering would improve Commentary by +3 points: model meaning) "
        "Q3: How does the point group symmetry of the stellated octahedron relate to "
        "nuclear symmetries? "
        "(Answering would improve Derivation by +2 points: group theory connection)"
    )
    name = "Tet A / Tet B Symmetry"
    question = (
        "Why must the two interpenetrating tetrahedra (Tet A and Tet B) be "
        "perfectly symmetric about the Field Origin? What would it mean "
        "physically if this geometric symmetry were broken?"
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
    audit_score = 75
    audit_notes = None
    future_questions = (
        "Q1: Why is r_e/4 chosen as the vortex eye size rather than r_e/2 or r_e/8, "
        "and is there physical motivation for the factor of 4? "
        "(Answering would improve Question by +3 points: parameter motivation) "
        "Q2: How does the vortex eye size (~0.7 fm) compare to the proton radius (~0.87 fm) "
        "and other nuclear length scales? "
        "(Answering would improve Commentary by +3 points: scale comparison) "
        "Q3: What observable predictions depend on the vortex eye size? "
        "(Answering would improve Model Output by +2 points: testable consequences)"
    )
    name = "Vortex Eye Size"
    question = (
        "Why is the vortex eye size defined as r_e/4 rather than some other "
        "fraction? Is the factor of 1/4 derived from physics or chosen as a "
        "model parameter?"
    )
    reference = "Model Definition"
    tolerance = 0.05
    level = Level.STANDARD
    commentary = (
        "The vortex eye size is defined as r_e/4 in the GFM model. This is "
        "a MODEL DEFINITION, not a derivation. The factor 1/4 is chosen, "
        "not derived from first principles."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MODEL DEFINITION: Vortex eye size.")
            .step("r_e = 2.818 fm (classical electron radius).")
            .step("GFM DEFINES eye radius = r_e / 4.")
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
    audit_score = 78
    audit_notes = None
    future_questions = (
        "Q1: How does the model transit rate function compare to actual Gamow peak "
        "calculations for fusion cross-sections? "
        "(Answering would improve Observation Quality by +3 points: comparison to theory) "
        "Q2: What temperature range does the model predict significant transit, and how "
        "does this compare to stellar core conditions? "
        "(Answering would improve Model Output by +3 points: numerical predictions) "
        "Q3: Could the qualitative model be made quantitative by fitting to measured "
        "reaction rates? "
        "(Answering would improve Derivation by +2 points: path to quantitative model)"
    )
    name = "Transit Rate vs Temperature"
    question = (
        "Why does the model transit rate increase with temperature, consistent "
        "with thermally activated processes? Is this behavior derived from the "
        "model or imposed to match physical intuition?"
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
        increasing = 1.0 if rate_low < rate_med < rate_high else 0.0
        # transit_rate is a qualitative model (see its docstring): what can be
        # tested is that it rises steeply, by many orders of magnitude per
        # decade of temperature, as a barrier-penetration rate must.
        steep = 1.0 if rate_low > 0 and math.log10(rate_med / rate_low) > 10 else 0.0
        return (
            Model()
            .add("Rate at 10^7 K", rate_low)
            .add("Rate at 10^8 K", rate_med)
            .add("Rate at 10^9 K", rate_high)
            .add("Monotonic increase", increasing)
            .add("Rises > 10 decades from 10^7 to 10^8 K", steep)
        )

    def observations(self) -> Observed:
        # The function is not normalised, so its absolute values are reported
        # for information. (They were compared with 0, 0 and 1, which the
        # function was never meant to return.)
        return (
            Observed()
            .add("Monotonic increase", 1.0)
            .add("Rises > 10 decades from 10^7 to 10^8 K", 1.0)
        )

# =============================================================================
# TEST 5: FIELD ORIGIN STABILITY (Geometry)
# =============================================================================

class FieldOriginStability(Test):
    """
    Verify Field Origin is at center: the "eye of the hurricane."
    
    GFM TEXTBOOK CONNECTION (Chapter 7, Section 9.5):
    The Field Origin is not an arbitrary choice. From Section 7.4:
    "At the exact center of the Field Chamber, all four coupling directions balance.
    This point is the Field Origin, the location where the field object 'sits.'"
    
    From Section 9.5 "The Central Octahedron: The Field Origin":
    "The central octahedron is the Field Origin, the geometric heart of the dual
    Field Chamber, where the two tetrahedral contributions couple and field closure
    ultimately resolves."
    
    THREE FUNCTIONS OF THE FIELD ORIGIN (Section 9.5):
    1. NEUTRAL POINT: Compression from Tet A and Tet B cancel here. No net preference.
    2. COUPLING ZONE: Information from both Field Chambers meets here during READ.
    3. PROCESSING CENTER: Field equations are "solved" here during SETTLE.
    
    The nucleus IS the Field Origin (Chapter 15): "what you call the 'nucleus' is
    actually the Field Origin itself, the eye of the hurricane where all compression
    flows meet."
    
    Textbook References: Ch 7.4 (Field Origin definition), Ch 9.5 (Central Octahedron),
    Ch 15 (Nucleus as Field Origin)
    """
    audit_score = 88
    audit_notes = None
    future_questions = (
        "Q1: Why is the Field Origin equidistant from all 4 faces of each tetrahedron, "
        "and how does this relate to isotropic coupling? "
        "(Answering would improve Derivation by +2 points: symmetry physics) "
        "Q2: In bimetric gravity terms, the Field Origin is where g_mu_nu = f_mu_nu. "
        "What does metric equality at one point imply for field closure? "
        "(Answering would improve Commentary by +3 points: bimetric connection) "
        "Q3: Chapter 15 says the nucleus IS the Field Origin. How does this reframe "
        "our understanding of atomic structure? "
        "(Answering would improve Question by +2 points: paradigm shift insight)"
    )
    name = "Field Origin: The Eye of the Hurricane"
    question = (
        "Why must the Field Origin be at the exact center where all coupling directions "
        "balance? The GFM Textbook (Section 9.5) describes three essential functions: "
        "(1) Neutral point where Tet A and Tet B compressions cancel, "
        "(2) Coupling zone where information from both Field Chambers meets, and "
        "(3) Processing center where field closure 'solves' the field equations. "
        "Without this central positioning, none of these functions would work."
    )
    reference = "GFM Textbook Sections 7.4, 9.5; Chapter 15"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The Field Origin at (0,0,0) is where field closure happens. All four coupling "
        "directions balance here (Section 7.4). In bimetric terms (Section 9.5), this is "
        "where the two metrics are equal: g_mu_nu = f_mu_nu (the 'symmetric vielbein point'). "
        "Chapter 15 reveals that the atomic nucleus IS the Field Origin: 'the eye of the "
        "hurricane where all compression flows meet.' The centroid position is not arbitrary. "
        "It is the unique point with the symmetry required for field closure to resolve "
        "to a consistent solution. Displacing the origin would break the balance between "
        "Tet A and Tet B, making SETTLE impossible."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("INTUITION: Why does the Field Origin matter?")
            .step("Think of two hurricanes (Tet A and Tet B) facing each other.")
            .step("The 'eye' is where their circulations cancel, creating calm.")
            .step("GEOMETRY: Stellated octahedron has 8 vertices at (+/-1, +/-1, +/-1).")
            .step("Tet A vertices: (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)")
            .step("Tet B vertices: (-1,-1,-1), (-1,1,1), (1,-1,1), (1,1,-1)")
            .step("Average of all 8 vertices = (0, 0, 0)")
            .equation("Field Origin = centroid = (0, 0, 0)")
            .step("THREE FUNCTIONS (Textbook Section 9.5):")
            .step("1. Neutral point: Tet A and Tet B compressions cancel")
            .step("2. Coupling zone: READ captures information from both")
            .step("3. Processing center: SETTLE resolves field equations here")
            .conclude("Field Origin at center enables all three field closure functions.")
        )

    def model(self) -> Model:
        origin = calculate_field_origin()
        at_center = 1.0 if np.allclose(origin, [0, 0, 0]) else 0.0
        
        # Verify equidistance from all vertices
        distances = [np.linalg.norm(get_vertex_coords(v) - origin) for v in range(8)]
        all_equal = 1.0 if np.allclose(distances, distances[0]) else 0.0
        
        return (
            Model()
            .add("Origin x", origin[0])
            .add("Origin y", origin[1])
            .add("Origin z", origin[2])
            .add("At center", at_center)
            .add("Distance to each vertex", round(distances[0], 4))
            .add("All vertices equidistant", all_equal)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Origin x", 0.0)
            .add("Origin y", 0.0)
            .add("Origin z", 0.0)
            .add("At center", 1.0)
            .add("Distance to each vertex", 1.7321)
            .add("All vertices equidistant", 1.0)
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
            "These tests define GFM model parameters and verify internal consistency.\n\n"
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
            "barrier is taken from nuclear physics, not derived from GFM.\n"
            "The geometric relationships follow from the stellated octahedron\n"
            "construction, not from physics principles."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
