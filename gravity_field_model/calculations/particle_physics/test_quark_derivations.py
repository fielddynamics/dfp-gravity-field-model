"""
Particle Physics: Quark Charge Correspondences

STATUS: NUMERICAL CORRESPONDENCES (not derivations)

MOTIVATION:
Why is the fundamental charge quantum 1/3 and not 1/2 or 1/5? The Standard Model
derives fractional charges from gauge anomaly cancellation, but accepts 1/3 as
an input. GFM offers a geometric origin: the Port Ratio 1/d = 1/(k-1) = 1/3 emerges
from tetrahedral Field Closure.

KEY CORRESPONDENCES:
    Port Ratio = 1/d = 1/3 = quark charge quantum
    Vertices per face = d = 3 = number of colors
    Quarks per baryon = d = 3 = vertices for complete face

CRITICAL HONESTY NOTE:
These are CORRESPONDENCES, not DERIVATIONS. The Standard Model derives charges
from SU(3) x SU(2) x U(1) gauge theory. GFM provides a geometric picture that
produces the same numbers. Whether this indicates deeper structure or coincidence
is for the reader to evaluate.

audit_score = 86
audit_notes = None
"""

from gravity_field_model.framework import *
from gravity_field_model.common import K_CLOSURE


# =============================================================================
# DERIVED CONSTANTS
# =============================================================================

D = K_CLOSURE - 1  # d = k - 1 = 3 (SPATIAL dimensions from Field Closure)
N_STELLATED_VERTICES = 2 * K_CLOSURE  # 8 vertices in stellated octahedron
CORNERS_PER_FACE = D  # 3 corners per triangular Coupling Port face

# The key GFM correspondence (textbook Section 7.7)
PORT_RATIO = 1 / D  # 1/3 (charge quantum from geometry)

# Standard Model values (for comparison, PDG 2024)
SM_QUARK_CHARGE_QUANTUM = 1/3
SM_NUM_COLORS = 3
SM_QUARKS_PER_BARYON = 3


# =============================================================================
# FACE ACTIVATION PATTERNS
# =============================================================================

def get_face_activation_patterns():
    """
    Return all 8 possible face activation patterns (3-bit combinations).
    
    A triangular face has 3 vertices. Each can be active (1) or inactive (0).
    This gives 2^3 = 8 possible states.
    """
    patterns = {}
    for i in range(8):
        binary = format(i, '03b')
        active_corners = []
        if i & 0b001: active_corners.append('C0')
        if i & 0b010: active_corners.append('C1')
        if i & 0b100: active_corners.append('C2')
        patterns[i] = {
            'binary': binary,
            'active_corners': active_corners,
            'num_active': len(active_corners),
        }
    return patterns


# =============================================================================
# TEST CLASSES
# =============================================================================

class ChargeQuantumCorrespondence(Test):
    """
    Why is the fundamental charge quantum exactly 1/3?
    
    The Standard Model accepts e/3 from gauge theory, but does not explain why
    triangular-based 1/3 rather than some other fraction. GFM offers a geometric
    answer: Field Closure requires k = 4 faces, giving d = k - 1 = 3 SPATIAL
    dimensions. The Port Ratio 1/d = 1/3 then sets the charge granularity.
    
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Could the charge quantum be derived rather than just corresponding? "
        "(Answering would improve Derivation by +3 points: moves from correspondence to prediction) "
        "Q2: Why is electric charge quantized at all, not continuous? "
        "(Answering would improve Question by +2 points: addresses Dirac quantization condition) "
        "Q3: Does the 1/3 quantum appear in any other physical constants? "
        "(Answering would improve Commentary by +2 points: uncovers broader patterns)"
    )
    """
    name = "Charge Quantum Correspondence"
    question = "Why is the fundamental charge quantum 1/3 rather than another fraction?"
    reference = "PDG 2024: quark charges are multiples of e/3"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Charge comes in discrete units; what sets the unit size?")
            .step("FIELD CLOSURE: The tetrahedron requires k = 4 faces for closure.")
            .step("SPATIAL DIMENSIONS: d = k - 1 = 3 (one face reserved for TIME).")
            .step("PORT RATIO: 1/d = 1/3 is the smallest fractional unit from triangular faces.")
            .step("MATCH: Standard Model quark charge quantum = e/3 (exact).")
            .conclude("RESULT: 1/3 emerges from d = 3, which comes from k = 4 Field Closure.")
        )
    
    commentary = (
        "The number 1/3 is not arbitrary; it is 1/d where d is the spatial dimension count. "
        "If we lived in d = 4 spatial dimensions, the charge quantum might be 1/4. The fact "
        "that quarks have 1/3-based charges is thus linked to having 3 spatial dimensions, "
        "which itself derives from tetrahedral Field Closure requiring k = 4 faces."
    )
    
    def model(self):
        return Model().add("Port Ratio (1/d)", PORT_RATIO)
    
    def observations(self):
        return Observed().add("Port Ratio (1/d)", SM_QUARK_CHARGE_QUANTUM)


class ThreeColorsCorrespondence(Test):
    """
    Why does QCD have exactly 3 color charges?
    
    The Standard Model chooses SU(3) for the strong force, giving 3 colors by
    definition. But why SU(3) and not SU(2) or SU(4)? GFM suggests the answer
    lies in geometry: each Coupling Port face is triangular with d = 3 vertices.
    If each vertex position represents one color state, then triangular geometry
    forces exactly 3 colors.
    
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Why are colors called R, G, B when they have no connection to visible light? "
        "(Answering would improve Audience Accessibility by +2 points: clarifies naming convention) "
        "Q2: How does the triangular color charge diagram relate to the vertex triangle? "
        "(Answering would improve Derivation by +3 points: geometric color diagram mapping) "
        "Q3: Could anticolors correspond to the opposite tetrahedron's vertices? "
        "(Answering would improve Commentary by +2 points: dual structure for anticolor)"
    )
    """
    name = "Three Colors Correspondence"
    question = "Why does QCD have exactly 3 colors rather than 2 or 4?"
    reference = "QCD: SU(3) gauge theory with 3 color charges (R, G, B)"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: A triangular face is the simplest closed polygon with area.")
            .step("VERTEX COUNT: Triangles have d = 3 vertices (from d = k - 1 = 3).")
            .step("COLOR HYPOTHESIS: Each vertex position corresponds to one color charge.")
            .step("QCD STRUCTURE: SU(3) has 3 colors: Red, Green, Blue.")
            .step("MATCH: Vertices per face = 3 = colors per quark.")
            .conclude("RESULT: The triangular Coupling Port geometry may dictate 3 colors.")
        )
    
    commentary = (
        "Triangles are special: they are the simplest 2D closed polygons. Their 3 vertices "
        "may underlie the 3 colors of QCD. If color charge reflects which vertex of a "
        "triangular face is 'activated,' then the geometry naturally limits colors to 3. "
        "This provides a geometric reason for choosing SU(3) over other gauge groups."
    )
    
    def model(self):
        return Model().add("Vertices per face", CORNERS_PER_FACE)
    
    def observations(self):
        return Observed().add("Vertices per face", SM_NUM_COLORS)


class ThreeQuarksCorrespondence(Test):
    """
    Baryons contain 3 quarks. Triangular faces have 3 corners.
    The numerical correspondence suggests baryons may represent
    complete face configurations.
    """
    name = "Three Quarks per Baryon"
    question = "How many quarks do baryons contain, and does this match the vertex count of a triangular Coupling Port face?"
    reference = "Particle physics: baryons = 3 quarks (proton = uud, neutron = udd)"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Triangular Coupling Port faces have d = 3 vertices.")
            .step("STEP 1: Color confinement requires color-neutral combinations (R+G+B or color+anticolor).")
            .step("STEP 2: Complete face activation uses all 3 vertices (one per color).")
            .step("STEP 3: Baryons (3 quarks) correspond to complete face configurations.")
            .conclude("OUTPUT: Quarks per baryon = 3 = vertices per face.")
        )
    
    commentary = (
        "The requirement for 3 quarks per baryon corresponds to the 3 vertices of a "
        "triangular face. In the GFM picture, a baryon represents complete occupation "
        "of all vertex positions on a SPATIAL face, achieving color neutrality through "
        "R+G+B combination. This is a structural correspondence, not a derivation of "
        "confinement physics."
    )
    
    def model(self):
        return Model().add("Quarks per baryon", CORNERS_PER_FACE)
    
    def observations(self):
        return Observed().add("Quarks per baryon", SM_QUARKS_PER_BARYON)


class FaceActivationPatterns(Test):
    """
    A 3-vertex face has 2^3 = 8 activation patterns.
    Pattern 000 (empty) and 111 (complete) are distinguished from partial states.
    This structure is compared to color confinement phenomenology.
    """
    name = "Face Activation Patterns"
    question = "How many distinct activation patterns exist for a 3-vertex face, and which represent color-neutral states?"
    reference = "Combinatorics: 2^3 = 8 patterns"
    level = Level.STANDARD
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A triangular face has d = 3 vertices, each active (1) or inactive (0).")
            .step("STEP 1: Total patterns = 2^d = 2^3 = 8 distinct states.")
            .step("STEP 2: Pattern 000 (vacuum) and 111 (baryon) represent color-neutral complete states.")
            .step("STEP 3: Partial patterns (1 or 2 vertices) carry net color, corresponding to confined states.")
            .conclude("OUTPUT: Total patterns = 8, Neutral states = 2 (000, 111), Colored states = 6.")
        )
    
    commentary = (
        "The 8 activation patterns of a 3-vertex face provide a combinatorial framework. "
        "The complete state (111) corresponds to a baryon; the empty state (000) to vacuum. "
        "Partial states with 1 or 2 active vertices would carry net color and cannot "
        "propagate freely, consistent with confinement. This is a structural analogy, "
        "not a derivation of QCD dynamics."
    )
    
    def model(self):
        patterns = get_face_activation_patterns()
        complete = patterns[0b111]
        empty = patterns[0b000]
        partial = [p for p in patterns.values() if 0 < p['num_active'] < 3]
        
        return (
            Model()
            .add("Total patterns", len(patterns))
            .add("Complete (111) vertices", complete['num_active'])
            .add("Empty (000) vertices", empty['num_active'])
            .add("Partial (colored) states", len(partial))
        )


class MesonPatterns(Test):
    """
    Two-vertex activation patterns correspond to meson (quark-antiquark) states.
    There are C(3,2) = 3 such patterns.
    """
    name = "Meson Patterns"
    question = "How many 2-vertex activation patterns exist, corresponding to quark-antiquark mesons?"
    reference = "Combinatorics: C(3,2) = 3"
    level = Level.STANDARD
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: A meson contains one quark and one antiquark (color + anticolor).")
            .step("STEP 1: Two-vertex patterns on a 3-vertex face: C(3,2) = 3 combinations.")
            .step("STEP 2: Patterns are: 011, 101, 110 (each missing one vertex).")
            .step("STEP 3: Each pattern represents a distinct color-anticolor pairing.")
            .conclude("OUTPUT: Two-vertex patterns = 3.")
        )
    
    commentary = (
        "The 3 two-vertex patterns correspond to quark-antiquark configurations. "
        "A meson achieves color neutrality through color-anticolor cancellation "
        "rather than RGB completion. The geometric representation shows partial "
        "face activation with compensating contributions."
    )
    
    def model(self):
        patterns = get_face_activation_patterns()
        two_vertex = [p for p in patterns.values() if p['num_active'] == 2]
        
        return Model().add("Two-vertex patterns", len(two_vertex))


class TwentyFourCornerStates(Test):
    """
    The stellated octahedron has 8 faces, each with 3 corners, giving 24
    total corner states. This equals the order of the binary tetrahedral group.
    """
    name = "24 Corner States"
    question = "How many total Coupling Port vertex states exist in the stellated octahedron?"
    reference = "Binary tetrahedral group 2T has order 24"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Stellated octahedron has 2k = 8 faces (4 per tetrahedron).")
            .step("STEP 1: Each face has d = 3 vertices.")
            .step("STEP 2: Total vertex states = 8 faces x 3 vertices = 24.")
            .step("STEP 3: This equals the order of binary tetrahedral group 2T in SU(2).")
            .conclude("OUTPUT: Total corner states = 24.")
        )
    
    commentary = (
        "The 24 corner states correspond to the order of the binary tetrahedral group, "
        "a discrete subgroup of SU(2) with connections to spin physics. Whether this "
        "numerical coincidence indicates deeper structure remains speculative."
    )
    
    def model(self):
        return Model().add("Total corner states", N_STELLATED_VERTICES * CORNERS_PER_FACE)
    
    def observations(self):
        return Observed().add("Total corner states", 24)


class EightVertices(Test):
    """
    The stellated octahedron has 8 vertices = 2k where k=4.
    This also equals the gluon count (d^2 - 1 = 8).
    """
    name = "Eight Vertices"
    question = "How many vertices does the stellated octahedron Field Chamber have?"
    reference = "Stellated octahedron geometry"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Field Chamber = two interpenetrating tetrahedra (A and B).")
            .step("STEP 1: Each tetrahedron contributes k = 4 vertices.")
            .step("STEP 2: Total vertices = k + k = 2k = 8.")
            .step("STEP 3: This also equals d^2 - 1 = 9 - 1 = 8 (SU(3) generator count).")
            .conclude("OUTPUT: Vertices = 8.")
        )
    
    commentary = (
        "The 8 vertices of the stellated octahedron arise from two tetrahedra with "
        "4 vertices each. The same count appears as the gluon number (d^2-1 = 8) "
        "and represents complete Coupling Port occupation in the L shell."
    )
    
    def model(self):
        return Model().add("Vertices", 2 * K_CLOSURE)
    
    def observations(self):
        return Observed().add("Vertices", 8)


class ThreeDimensions(Test):
    """
    Why does space have exactly 3 dimensions?
    
    Physics typically accepts d = 3 as given. GFM derives it: Field Closure
    requires the minimum closed 3D shape, a tetrahedron with k = 4 faces.
    One face handles TIME, leaving d = k - 1 = 3 for SPATIAL dimensions.
    
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Why do string theories require extra dimensions while GFM predicts exactly 3? "
        "(Answering would improve Question by +3 points: contrasts with other theories) "
        "Q2: How does the TIME face differ geometrically from SPATIAL faces? "
        "(Answering would improve Derivation by +2 points: clarifies time-space distinction) "
        "Q3: Could compact extra dimensions fit within the tetrahedral framework? "
        "(Answering would improve Commentary by +2 points: addresses Kaluza-Klein compatibility)"
    )
    """
    name = "Three Spatial Dimensions"
    question = "Why does physical space have exactly 3 dimensions?"
    reference = "Observation: space has 3 orthogonal directions"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: A tetrahedron is the simplest closed 3D polyhedron.")
            .step("FIELD CLOSURE: Gravity requires k = 4 coupling faces for consistency.")
            .step("TIME ALLOCATION: 1 face per tetrahedron dedicated to TIME direction.")
            .step("SPATIAL COUNT: d = k - 1 = 4 - 1 = 3 SPATIAL faces/dimensions.")
            .step("VERIFICATION: We observe exactly 3 orthogonal spatial directions.")
            .conclude("RESULT: d = 3 is not arbitrary but follows from k = 4 Field Closure.")
        )
    
    commentary = (
        "Most theories accept d = 3 as an unexplained fact. GFM proposes it emerges from "
        "Field Closure: consistency requires k = 4 coupling channels (tetrahedral), and "
        "reserving one for TIME leaves d = 3 for space. This links spatial dimensionality "
        "to the requirements of gravitational consistency, not to arbitrary choice."
    )
    
    def model(self):
        return Model().add("Spatial dimensions", K_CLOSURE - 1)
    
    def observations(self):
        return Observed().add("Spatial dimensions", 3)


class ProtonChargeConsistency(Test):
    """
    Using q = 1/3 as the charge quantum, the proton (uud) has charge +1.
    This is CONSISTENCY, not derivation. The charge assignments (u = +2/3, d = -1/3)
    are inputs, not outputs.
    """
    name = "Proton Charge Consistency"
    question = "Is the proton charge consistent with the 1/3 charge quantum and uud quark composition?"
    reference = "Proton charge = +1e"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Charge quantum q = 1/d = 1/3 from Port Ratio.")
            .step("STEP 1: Up quark assigned Q_u = +2q = +2/3 (2 vertices active on Tet A).")
            .step("STEP 2: Down quark assigned Q_d = -q = -1/3 (1 vertex active on Tet B).")
            .step("STEP 3: Proton (uud): Q = (+2/3) + (+2/3) + (-1/3) = +3/3 = +1.")
            .conclude("OUTPUT: Proton charge = +1 (consistent with assignments).")
        )
    
    commentary = (
        "The proton charge calculation verifies CONSISTENCY of the charge assignments "
        "with the 1/3 quantum. Note that u = +2/3 and d = -1/3 are ASSIGNED based on "
        "the Standard Model values, not derived from geometry. GFM provides a picture "
        "(vertex activations) consistent with these assignments, but does not derive them."
    )
    
    def model(self):
        q = PORT_RATIO
        up_charge = 2 * q      # +2/3 (assigned)
        down_charge = -1 * q   # -1/3 (assigned)
        proton = up_charge + up_charge + down_charge
        return Model().add("Proton charge", proton)
    
    def observations(self):
        return Observed().add("Proton charge", 1.0)


class NeutronChargeConsistency(Test):
    """
    Using the same charge assignments, the neutron (udd) has charge 0.
    """
    name = "Neutron Charge Consistency"
    question = "Is the neutron charge consistent with the 1/3 charge quantum and udd quark composition?"
    reference = "Neutron charge = 0"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Charge quantum q = 1/d = 1/3 from Port Ratio.")
            .step("STEP 1: Up quark: Q_u = +2q = +2/3. Down quark: Q_d = -q = -1/3.")
            .step("STEP 2: Neutron (udd): Q = (+2/3) + (-1/3) + (-1/3) = 0.")
            .step("STEP 3: Net charge vanishes, consistent with observed neutron neutrality.")
            .conclude("OUTPUT: Neutron charge = 0 (consistent).")
        )
    
    commentary = (
        "The neutron's zero charge follows from the udd composition with the standard "
        "quark charge assignments. This is a consistency check, not a prediction. "
        "The Field Chamber picture shows compensating vertex activations yielding net zero."
    )
    
    def model(self):
        q = PORT_RATIO
        up_charge = 2 * q
        down_charge = -1 * q
        neutron = up_charge + down_charge + down_charge
        return Model().add("Neutron charge", neutron)
    
    def observations(self):
        return Observed().add("Neutron charge", 0.0)


class ThreeGenerationsCorrespondence(Test):
    """
    The Standard Model has 3 fermion generations.
    GFM has d = 3 SPATIAL dimensions.
    This numerical correspondence is noted as SPECULATIVE.
    """
    name = "Three Generations Correspondence"
    question = "Does the number of fermion generations correspond to the SPATIAL dimension count d = 3?"
    reference = "Standard Model: 3 generations (e/mu/tau, u/c/t, d/s/b)"
    level = Level.EXPLORATORY
    
    def derivation(self):
        return (
            Derivation()
            .step("SPECULATIVE CORRESPONDENCE - No mechanism proposed.")
            .step("PREMISE: d = k - 1 = 3 SPATIAL dimensions from Field Closure.")
            .step("STEP 1: Standard Model has exactly 3 fermion generations.")
            .step("STEP 2: Numerical match: d = 3 = number of generations.")
            .step("STEP 3: No mechanism linking SPATIAL faces to generation structure is known.")
            .conclude("OUTPUT: Correspondence d = 3 = generations is noted but not explained.")
        )
    
    commentary = (
        "SPECULATIVE: The numerical match between d = 3 SPATIAL dimensions and 3 fermion "
        "generations is intriguing but lacks a proposed mechanism. The Standard Model does "
        "not explain WHY there are 3 generations; GFM's d = 3 provides a number that matches "
        "but not an explanation. This should be regarded as an open question."
    )
    
    def model(self):
        return (
            Model()
            .add("SPATIAL dimensions (d)", D)
            .add("Fermion generations", 3)
            .add("Match", 1)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ChargeQuantumCorrespondence,
    ThreeColorsCorrespondence,
    ThreeQuarksCorrespondence,
    FaceActivationPatterns,
    MesonPatterns,
    TwentyFourCornerStates,
    EightVertices,
    ThreeDimensions,
    ProtonChargeConsistency,
    NeutronChargeConsistency,
    ThreeGenerationsCorrespondence,
]


def run_all():
    """Run all quark correspondence tests."""
    return run_tests(
        title="Quark Charge Correspondences",
        summary=(
            "These tests document NUMERICAL CORRESPONDENCES between geometric properties "
            "of the stellated octahedron and Standard Model quark physics. The key "
            "correspondence is Port Ratio = 1/d = 1/3, matching the quark charge quantum. "
            "\n\n"
            "IMPORTANT: These are correspondences, not derivations. The Standard Model "
            "derives fractional charges from gauge theory. GFM observes that tetrahedral "
            "geometry produces the same numbers. Whether this indicates deeper structure "
            "or coincidence is left for the reader to evaluate."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
