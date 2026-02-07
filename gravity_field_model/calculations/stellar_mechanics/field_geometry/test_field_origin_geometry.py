"""
Field Origin Geometry: Model Definitions and Internal Consistency
==================================================================

GFM Model V2

HONESTY STATEMENT:
This module defines GFM model geometry and verifies internal consistency.
These are MODEL DEFINITIONS, not physics derivations. The geometry is
chosen to have certain properties, then we verify those properties hold.

MODEL DEFINITIONS (not derivations):
- Field Envelope size r_e = classical electron radius (adopted, not derived)
- Field Origin = center of stellated octahedron (defined, not derived)
- k=4 follows from simplex theorem (geometric definition)
- Stellated octahedron as Field Chamber geometry (model choice)

INTERNAL CONSISTENCY CHECKS:
- Field Origin is at (0,0,0)
- All vertices equidistant from origin
- Tet A and Tet B are symmetric

WHAT THIS MODULE DOES NOT DO:
- It does not derive the classical electron radius
- It does not explain WHY k=4 should relate to nuclear stability
- The observation that A mod 4 = 0 for some stable nuclei is pattern
  matching, not a GFM prediction

TEST GROUP GOALS:
This module establishes the geometric foundation of the GFM model. The stellated
octahedron geometry is introduced as a framework for organizing nuclear structure.
Students learn that r_e and k=4 are adopted constants, not derived predictions,
establishing honesty about what the model assumes vs what it explains.

Audience: Undergraduate physics and mathematics students.
"""

import math
import numpy as np
from gravity_field_model.framework import *
from gravity_field_model.common import (
    VERTICES, TET_A, TET_B, K,
    C, HBAR, ALPHA, ME,
    R_E, A_0, R_PROTON, LAMBDA_COMPTON,
    RHO_NUCLEAR, RHO_WHITE_DWARF, RHO_FIELD_BINDING,
    compression_ratio_equilibrium_to_tile,
    vortex_eye_size as calculate_vortex_eye_size_common,
)


def get_vertex_coords(v):
    coords = VERTICES[v]['coords']
    return np.array(coords, dtype=float)


def calculate_field_origin():
    all_coords = [get_vertex_coords(v) for v in range(8)]
    return np.mean(all_coords, axis=0)


# =============================================================================
# TEST 1: FIELD ENVELOPE SIZE (Model Definition)
# =============================================================================

class FieldEnvelopeSize(Test):
    """
    Verify the Field Envelope size equals classical electron radius.

    HONESTY: r_e is the classical electron radius from CODATA. GFM ADOPTS
    this value as the "Field Envelope" size. This is a model definition,
    not a derivation.
    """
    audit_score = 80
    audit_notes = None
    future_questions = (
        "Q1: What physical interpretation does the classical electron radius have, given "
        "that electrons appear point-like in scattering experiments? "
        "(Answering would improve Question by +4 points: addresses apparent paradox) "
        "Q2: How does r_e emerge from equating electrostatic self-energy to rest mass energy? "
        "(Answering would improve Derivation by +3 points: shows historical derivation) "
        "Q3: Why might GFM choose r_e as the fundamental length scale rather than Compton "
        "wavelength or Bohr radius? "
        "(Answering would improve Commentary by +2 points: model motivation)"
    )
    name = "Field Envelope r_e"
    question = (
        "Why does GFM adopt the classical electron radius (2.818 fm) as its "
        "fundamental length scale? What physical significance does r_e have, "
        "and what does it mean to 'adopt' rather than 'derive' a constant?"
    )
    reference = "CODATA 2018"
    tolerance = 0.01
    level = Level.CRITICAL
    commentary = (
        "The classical electron radius r_e = 2.818 fm is a measured constant. GFM "
        "adopts this value as the 'Field Envelope' size. This is a definition that "
        "sets the model's length scale. GFM does not derive r_e from first principles."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("DEFINITION: GFM adopts the classical electron radius as Field Envelope size.")
            .equation("r_e = e^2 / (4*pi*epsilon_0*m_e*c^2) = 2.818 fm (CODATA)")
            .step("This is the model's fundamental length scale by definition.")
            .conclude("Field Envelope r_e = 2.818e-15 m (adopted from CODATA).")
        )

    def model(self) -> Model:
        return Model().add("Field Envelope r_e (m)", R_E)

    def observations(self) -> Observed:
        return Observed().add("Field Envelope r_e (m)", 2.818e-15)


# =============================================================================
# TEST 2: k=4 FROM SIMPLEX THEOREM (Geometric Definition)
# =============================================================================

class TetrahedralClosureConstant(Test):
    """
    Verify k=4 follows from simplex theorem.

    HONESTY: The simplex theorem states d+1 points are needed to enclose
    d-dimensional space. For d=3, this gives k=4. GFM DEFINES k=4 as the
    "Field Closure constant." This is a geometric fact, not a physics derivation.
    """
    audit_score = 82
    audit_notes = None
    future_questions = (
        "Q1: What makes the tetrahedron mathematically special as the minimal volume-enclosing "
        "simplex in 3D, and why can't fewer points work? "
        "(Answering would improve Derivation by +3 points: geometric necessity) "
        "Q2: Is it coincidence or deep physics that He-4 (4 nucleons) and carbon (4 valence) "
        "both involve the number 4? "
        "(Answering would improve Commentary by +3 points: addresses pattern recognition) "
        "Q3: How does the simplex theorem generalize to higher dimensions (4D, 5D)? "
        "(Answering would improve Audience Accessibility by +2 points: mathematical extension)"
    )
    name = "Tetrahedral Closure k=4"
    question = (
        "Why does the simplex theorem require exactly 4 points to minimally "
        "enclose 3-dimensional space? Is this geometric fact sufficient to "
        "explain why helium-4 is stable, or does physics require more?"
    )
    reference = "Geometry (simplex theorem)"
    tolerance = 0.01
    level = Level.CRITICAL
    commentary = (
        "The simplex theorem is pure geometry: to minimally enclose 3D space, you "
        "need 4 points (a tetrahedron). GFM adopts k=4 as a fundamental constant. "
        "This is a definition inspired by geometry, not a derivation that k=4 has "
        "physical significance for nuclear stability."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Simplex theorem states d+1 points minimally enclose d dimensions.")
            .equation("For d=3: k = d + 1 = 4")
            .step("k=4 = tetrahedron vertices = tetrahedron faces.")
            .step("GFM ADOPTS this as the Field Closure constant.")
            .step("NOTE: This does not EXPLAIN why He-4 is stable. Shell model does.")
            .conclude("k = 4 by geometric definition from simplex theorem.")
        )

    def model(self) -> Model:
        k = K
        d = 3
        simplex = d + 1
        return (
            Model()
            .add("k value", k)
            .add("d+1 for d=3", simplex)
            .add("Match", 1.0 if k == simplex else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("k value", 4)
            .add("d+1 for d=3", 4)
            .add("Match", 1.0)
        )


# =============================================================================
# TEST 3: FIELD ORIGIN AT CENTER (Internal Consistency)
# =============================================================================

class FieldOriginAtCenter(Test):
    """
    Verify Field Origin is at geometric center of stellated octahedron.

    HONESTY: This is an internal consistency check. The stellated octahedron
    is defined with vertices at (+/-1, +/-1, +/-1), so the center is (0,0,0)
    by construction.
    """
    audit_score = 75
    audit_notes = None
    future_questions = (
        "Q1: Why is the centroid the natural choice for the Field Origin rather than "
        "some other special point of the stellated octahedron? "
        "(Answering would improve Question by +3 points: motivates construction) "
        "Q2: What symmetry group does the stellated octahedron possess, and how does this "
        "relate to its physical interpretation? "
        "(Answering would improve Derivation by +3 points: group theory connection) "
        "Q3: How would the model change if a different polyhedron were used as the Field Chamber? "
        "(Answering would improve Commentary by +2 points: explores alternatives)"
    )
    name = "Field Origin Location"
    question = (
        "Why is the Field Origin placed at the geometric center (0,0,0) of "
        "the stellated octahedron by construction? What symmetry properties "
        "does this central position preserve?"
    )
    reference = "Model Definition"
    tolerance = 0.01
    level = Level.CRITICAL
    commentary = (
        "The stellated octahedron vertices are at (+/-1, +/-1, +/-1). By symmetry, "
        "the centroid is at (0,0,0). GFM calls this the 'Field Origin'. This is "
        "a model definition, not a physics prediction."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Stellated octahedron with vertices at (+/-1, +/-1, +/-1).")
            .step("Centroid = average of all vertices = (0, 0, 0).")
            .step("GFM defines this as the 'Field Origin'.")
            .conclude("Field Origin = (0, 0, 0) by construction.")
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
# TEST 4: ORIGIN-VERTEX DISTANCE (Internal Consistency)
# =============================================================================

class OriginVertexDistance(Test):
    """
    Verify distance from Field Origin to vertices = sqrt(3).

    HONESTY: Pure geometry. Distance from (0,0,0) to (+/-1,+/-1,+/-1) is sqrt(3).
    """
    audit_score = 74
    audit_notes = None
    future_questions = (
        "Q1: What is the geometric significance of sqrt(3) appearing as the vertex distance, "
        "and how does this relate to the cube diagonal? "
        "(Answering would improve Derivation by +3 points: connects to familiar geometry) "
        "Q2: How do the edge lengths of the inner octahedron compare to the outer tetrahedra? "
        "(Answering would improve Model Output by +2 points: complete geometric picture) "
        "Q3: Why does uniform vertex distance from the center matter for physical interpretation? "
        "(Answering would improve Commentary by +3 points: symmetry significance)"
    )
    name = "Origin-Vertex Distance"
    question = (
        "Why is the distance from the origin to each vertex exactly sqrt(3) "
        "in unit coordinates? What does this uniform distance mean for the "
        "symmetry of the stellated octahedron?"
    )
    reference = "Geometry"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Distance from origin (0,0,0) to any vertex (+/-1,+/-1,+/-1) is sqrt(1+1+1) = "
        "sqrt(3) = 1.732. This is basic geometry, not a physics prediction."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Vertex coordinates are (+/-1, +/-1, +/-1).")
            .equation("Distance = sqrt(1^2 + 1^2 + 1^2) = sqrt(3) = 1.732")
            .step("All 8 vertices are equidistant from origin by symmetry.")
            .conclude("All vertices at distance sqrt(3) = 1.732 from origin.")
        )

    def model(self) -> Model:
        origin = calculate_field_origin()
        distances = [np.linalg.norm(get_vertex_coords(v) - origin) for v in range(8)]
        avg_dist = sum(distances) / len(distances)
        expected = math.sqrt(3)
        all_equal = 1.0 if all(abs(d - expected) < 0.001 for d in distances) else 0.0
        return (
            Model()
            .add("Average distance", avg_dist)
            .add("Expected sqrt(3)", expected)
            .add("All equal", all_equal)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Average distance", 1.732)
            .add("Expected sqrt(3)", 1.732)
            .add("All equal", 1.0)
        )


# =============================================================================
# TEST 5: BIMETRIC SYMMETRY (Internal Consistency)
# =============================================================================

class BimetricBalance(Test):
    """
    Verify Tet A and Tet B are equidistant from Field Origin.

    HONESTY: The stellated octahedron is constructed from two interpenetrating
    tetrahedra. By symmetry, both are equidistant from the center.
    """
    audit_score = 76
    audit_notes = None
    future_questions = (
        "Q1: What physical meaning do Tet A and Tet B have in the GFM model, and why are "
        "two tetrahedra needed rather than one? "
        "(Answering would improve Question by +4 points: model interpretation) "
        "Q2: How does the interpenetrating geometry relate to matter-antimatter or "
        "other dual structures in physics? "
        "(Answering would improve Commentary by +3 points: physical analogy) "
        "Q3: What happens at the 6 points where Tet A and Tet B edges intersect? "
        "(Answering would improve Model Output by +2 points: geometric detail)"
    )
    name = "Bimetric Balance"
    question = (
        "Why must the two interpenetrating tetrahedra (Tet A and Tet B) be "
        "equidistant from the center by construction? What would break if "
        "this symmetry were violated?"
    )
    reference = "Model Geometry"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The stellated octahedron consists of two tetrahedra (Tet A and Tet B) "
        "with shared center. By construction, both are equidistant from the origin. "
        "This is geometry, not physics."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Stellated octahedron = two interpenetrating tetrahedra.")
            .step("Both tetrahedra share the same center at (0,0,0).")
            .step("By symmetry, avg distance from origin is the same for both.")
            .equation("Tet A avg distance = Tet B avg distance = sqrt(3)")
            .conclude("Bimetric symmetry holds by construction.")
        )

    def model(self) -> Model:
        origin = calculate_field_origin()
        tet_a_dists = [np.linalg.norm(get_vertex_coords(v) - origin) for v in TET_A]
        tet_b_dists = [np.linalg.norm(get_vertex_coords(v) - origin) for v in TET_B]
        avg_a = sum(tet_a_dists) / len(tet_a_dists)
        avg_b = sum(tet_b_dists) / len(tet_b_dists)
        balanced = 1.0 if abs(avg_a - avg_b) < 0.001 else 0.0
        return (
            Model()
            .add("Tet_A avg distance", avg_a)
            .add("Tet_B avg distance", avg_b)
            .add("Balanced", balanced)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Tet_A avg distance", 1.732)
            .add("Tet_B avg distance", 1.732)
            .add("Balanced", 1.0)
        )


# =============================================================================
# TEST 6: INNER OCTAHEDRON (Internal Consistency)
# =============================================================================

class InnerOctahedronBoundary(Test):
    """
    Verify inner octahedron at distance 1.0 from origin.

    HONESTY: The inner octahedron has vertices at (+/-1,0,0), (0,+/-1,0), (0,0,+/-1).
    Distance from origin is 1.0 by construction.
    """
    audit_score = 73
    audit_notes = None
    future_questions = (
        "Q1: What role does the inner octahedron play in the GFM model geometry, and how "
        "does it differ from the outer stellated structure? "
        "(Answering would improve Question by +3 points: clarifies model structure) "
        "Q2: Why are the inner octahedron vertices at axis-aligned positions while the "
        "outer vertices are at cube corners? "
        "(Answering would improve Derivation by +3 points: geometric relationship) "
        "Q3: How do the 8 faces of the inner octahedron correspond to the 8 cells of "
        "the stellated structure? "
        "(Answering would improve Model Output by +2 points: face-cell correspondence)"
    )
    name = "Inner Octahedron Boundary"
    question = (
        "Why do the 6 axis-aligned vertices of the inner octahedron all lie at "
        "unit distance from the origin? How does this inner boundary relate to "
        "the outer stellated vertices at sqrt(3)?"
    )
    reference = "Geometry"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The inner octahedron vertices are at the axis points (+/-1, 0, 0), etc. "
        "Distance from (0,0,0) to (1,0,0) is 1.0. This is basic geometry."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Inner octahedron at edge midpoints.")
            .step("Vertices: (+/-1,0,0), (0,+/-1,0), (0,0,+/-1).")
            .equation("Distance from origin: sqrt(1+0+0) = 1.0")
            .step("All 6 vertices at distance 1.0 from origin.")
            .conclude("Inner octahedron at distance 1.0 by construction.")
        )

    def model(self) -> Model:
        inner_vertices = [
            np.array([1, 0, 0]), np.array([-1, 0, 0]),
            np.array([0, 1, 0]), np.array([0, -1, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1]),
        ]
        origin = calculate_field_origin()
        distances = [np.linalg.norm(v - origin) for v in inner_vertices]
        all_at_1 = 1.0 if all(abs(d - 1.0) < 0.001 for d in distances) else 0.0
        return (
            Model()
            .add("Average distance", sum(distances)/len(distances))
            .add("All at 1.0", all_at_1)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Average distance", 1.0)
            .add("All at 1.0", 1.0)
        )


# =============================================================================
# TEST 7: SCALE COMPARISON (Observation, Not Derivation)
# =============================================================================

class ScaleComparison(Test):
    """
    Compare r_e to proton radius.

    HONESTY: This is an observation. r_e > r_proton is a measured fact.
    GFM does not explain WHY this is so.
    """
    audit_score = 78
    audit_notes = None
    future_questions = (
        "Q1: Why is the electromagnetic length scale (r_e) larger than the strong force "
        "length scale (proton radius) despite QED being a weaker interaction? "
        "(Answering would improve Question by +4 points: addresses counterintuitive result) "
        "Q2: How was the proton charge radius measured, and why did the muonic hydrogen "
        "puzzle arise? "
        "(Answering would improve Observation Quality by +3 points: measurement details) "
        "Q3: What other characteristic length scales exist between r_e and r_proton? "
        "(Answering would improve Audience Accessibility by +2 points: scale hierarchy)"
    )
    name = "Field Envelope vs Proton Size"
    question = (
        "Why is the classical electron radius (~2.8 fm) about 3 times larger "
        "than the proton charge radius (~0.87 fm)? What does this scale ratio "
        "tell us about electromagnetic vs strong force length scales?"
    )
    reference = "Nuclear Physics (proton radius)"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "r_e = 2.818 fm (classical electron radius) is ~3.2x larger than "
        "r_proton = 0.87 fm (proton charge radius). This is an observation. "
        "GFM does not derive either value."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MEASUREMENT: r_e = 2.818 fm (CODATA).")
            .step("MEASUREMENT: r_proton = 0.87 fm (electron scattering).")
            .equation("Ratio = 2.818 / 0.87 = 3.24")
            .step("OBSERVATION: Field Envelope > proton radius.")
            .step("GFM does not explain this ratio. It is adopted as given.")
            .conclude("r_e/r_proton = 3.24 (measured ratio).")
        )

    def model(self) -> Model:
        ratio = R_E / R_PROTON
        return (
            Model()
            .add("r_e (fm)", R_E * 1e15)
            .add("r_proton (fm)", R_PROTON * 1e15)
            .add("Ratio", ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("r_e (fm)", 2.818)
            .add("r_proton (fm)", 0.87)
            .add("Ratio", 3.24)
        )


# =============================================================================
# TEST 8: COMPTON WAVELENGTH RATIO (Observation, Not Derivation)
# =============================================================================

class ComptonWavelengthRatio(Test):
    """
    Calculate ratio of Compton wavelength to r_e.

    HONESTY: lambda_C / r_e = 2*pi/alpha ~ 861 is a known result from QED.
    GFM does not derive this. It observes and adopts it.
    """
    audit_score = 81
    audit_notes = None
    future_questions = (
        "Q1: Why does alpha (the fine structure constant) appear in the ratio between "
        "quantum and classical electron length scales? "
        "(Answering would improve Derivation by +3 points: alpha as coupling strength) "
        "Q2: What is the physical meaning of the Compton wavelength as a 'quantum size' "
        "for the electron? "
        "(Answering would improve Commentary by +3 points: wave-particle duality) "
        "Q3: How do these length scale relationships generalize to other particles like muons? "
        "(Answering would improve Audience Accessibility by +2 points: extends concept)"
    )
    name = "Compton / r_e Ratio"
    question = (
        "Why is the Compton wavelength exactly 2*pi/alpha times larger than "
        "the classical electron radius? What does this relationship between "
        "quantum and classical electron scales reveal about the fine structure "
        "constant?"
    )
    reference = "QED"
    tolerance = 0.05
    level = Level.STANDARD
    commentary = (
        "lambda_C / r_e = 2*pi/alpha = 861. This is a standard QED result. "
        "The classical electron radius r_e = alpha * lambda_C / (2*pi), so "
        "lambda_C / r_e = 2*pi / alpha. GFM observes this ratio but does not "
        "derive it."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD QED: lambda_C = h/(m_e*c) = 2.426e-12 m.")
            .step("r_e = alpha^2 * a_0 = alpha * lambda_bar_C = 2.818e-15 m.")
            .step("lambda_bar_C = lambda_C / (2*pi) (reduced Compton wavelength).")
            .equation("r_e = alpha * lambda_C / (2*pi)")
            .equation("lambda_C / r_e = 2*pi / alpha = 861")
            .step("GFM OBSERVES this ratio. It does not derive it.")
            .conclude("lambda_C / r_e = 861 (standard QED).")
        )

    def model(self) -> Model:
        ratio = LAMBDA_COMPTON / R_E
        expected = 2 * math.pi / ALPHA
        return (
            Model()
            .add("lambda_C / r_e", ratio)
            .add("2*pi/alpha", expected)
            .add("Match", 1.0 if abs(ratio - expected) / expected < 0.001 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("lambda_C / r_e", 861)
            .add("2*pi/alpha", 861)
            .add("Match", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    FieldEnvelopeSize,
    TetrahedralClosureConstant,
    FieldOriginAtCenter,
    OriginVertexDistance,
    BimetricBalance,
    InnerOctahedronBoundary,
    ScaleComparison,
    ComptonWavelengthRatio,
]


def run_all() -> bool:
    """Run all field origin geometry tests."""
    return run_tests(
        title="Field Origin Geometry",
        summary=(
            "These tests verify GFM MODEL DEFINITIONS and internal consistency:\n"
            "1. r_e = 2.818 fm (adopted from CODATA, not derived)\n"
            "2. k = 4 from simplex theorem (geometric definition)\n"
            "3. Field Origin at (0,0,0) by construction\n"
            "4. Stellated octahedron symmetry properties\n\n"
            "CLARIFICATION: These are model definitions and geometry checks.\n"
            "GFM does not DERIVE the classical electron radius, proton radius,\n"
            "or Compton wavelength. It adopts measured values and defines\n"
            "internal geometric relationships.\n\n"
            "REMOVED: Tests claiming k-alignment 'explains' nuclear stability.\n"
            "The observation that some stable nuclei have A mod 4 = 0 is\n"
            "pattern matching, not a GFM prediction."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
