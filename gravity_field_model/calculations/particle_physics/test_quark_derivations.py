"""
Particle Physics: Quark Charge Correspondences

STATUS: NUMERICAL CORRESPONDENCES (not derivations)

These tests document numerical correspondences between geometric properties of the
stellated octahedron and Standard Model parameters. The key correspondence is:

    Port Ratio = 1/d = 1/(k-1) = 1/3

This matches the quark charge quantum. Additionally:
    - 3 vertices per triangular face matches 3 color charges
    - 3 quarks per baryon matches 3 vertices to complete a face

CRITICAL HONESTY NOTE:
These are CORRESPONDENCES, not DERIVATIONS. GFD observes that:
    d = k - 1 = 3    and    quark charge quantum = 1/3

This numerical match is interesting but does not constitute a derivation.
The Standard Model derives fractional charges from SU(3)_color x SU(2)_weak x U(1)_Y
gauge theory and anomaly cancellation. GFD provides a geometric picture that
happens to produce the same numbers.

The reader should evaluate whether these numerical agreements indicate deeper
structure or are coincidental.
"""

from gravity_field_model.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

K_CLOSURE = 4  # Tetrahedral face count (Field Closure constant)
D = K_CLOSURE - 1  # d = k - 1 = 3 (SPATIAL dimensions)
STELLATED_VERTICES = 2 * K_CLOSURE  # 8 vertices in stellated octahedron
CORNERS_PER_FACE = D  # 3 corners per triangular face

# The key GFD correspondence
PORT_RATIO = 1 / D  # 1/3 (charge quantum from geometry)

# Standard Model values (for comparison)
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
    GFD produces 1/d = 1/3 from the tetrahedral structure d = k-1 = 3.
    This value equals the quark charge quantum e/3 in the Standard Model.
    
    NOTE: This is a numerical correspondence, not a physical derivation.
    The Standard Model derives e/3 from gauge theory constraints.
    GFD observes that 1/d happens to equal the same value.
    """
    name = "Charge Quantum Correspondence"
    question = "What is the Port Ratio from Field Closure, and does it numerically match the quark charge quantum?"
    reference = "Standard Model: quark charges are multiples of e/3"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Field Closure requires k = 4 faces; hence d = k - 1 = 3 SPATIAL dimensions.")
            .step("STEP 1: Port Ratio = 1/d = 1/3 (geometric property of triangular Coupling Port faces).")
            .step("STEP 2: Standard Model quark charge quantum = e/3 (from gauge theory).")
            .step("STEP 3: Numerical comparison: 1/d = 1/3 = e/3 (exact match).")
            .conclude("OUTPUT: Port Ratio = 1/3 corresponds to quark charge quantum = 1/3.")
        )
    
    commentary = (
        "The emergence of 1/3 from Field Closure (k=4 giving d=k-1=3) matches the fractional "
        "charge quantum of quarks. This correspondence is NUMERICAL, not CAUSAL. The Standard "
        "Model derives e/3 from SU(3) color symmetry and anomaly cancellation. GFD observes "
        "that tetrahedral geometry produces the same ratio. Whether this indicates deeper "
        "structure or coincidence remains an open question."
    )
    
    def model(self):
        return Model().add("Port Ratio (1/d)", PORT_RATIO)
    
    def observations(self):
        return Observed().add("Port Ratio (1/d)", SM_QUARK_CHARGE_QUANTUM)


class ThreeColorsCorrespondence(Test):
    """
    A triangular face has 3 corners. QCD has 3 color charges.
    This numerical correspondence is noted.
    """
    name = "Three Colors Correspondence"
    question = "How many vertices does each triangular Coupling Port face have, and does this match the number of QCD color charges?"
    reference = "QCD: 3 color charges (Red, Green, Blue)"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: From Field Closure, d = k - 1 = 3 vertices per Coupling Port face.")
            .step("STEP 1: Each triangular face has exactly 3 vertex positions.")
            .step("STEP 2: QCD requires exactly 3 color charges (SU(3) fundamental representation).")
            .step("STEP 3: Numerical comparison: 3 vertices = 3 colors.")
            .conclude("OUTPUT: Vertices per face = 3, Color charges = 3 (numerical match).")
        )
    
    commentary = (
        "Each Coupling Port presents a triangular face with 3 vertices. QCD has 3 color charges. "
        "The match is numerical. The Standard Model derives 3 colors from the SU(3) gauge group. "
        "GFD observes that triangular faces have 3 corners. No mechanism linking geometry to "
        "color charge is proposed."
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
        "triangular face. In the GFD picture, a baryon represents complete occupation "
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
        return Model().add("Total corner states", STELLATED_VERTICES * CORNERS_PER_FACE)
    
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
    d = k - 1 = 3 spatial dimensions from Field Closure.
    This matches observed physical space dimensionality.
    """
    name = "Three Spatial Dimensions"
    question = "How many SPATIAL dimensions emerge from Field Closure?"
    reference = "Observed: 3 spatial dimensions"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Field Closure requires k = 4 faces to form a closed tetrahedron.")
            .step("STEP 1: One face serves as TIME face; the rest are SPATIAL faces.")
            .step("STEP 2: SPATIAL dimensions d = k - 1 = 4 - 1 = 3.")
            .step("STEP 3: This matches the observed dimensionality of physical space.")
            .conclude("OUTPUT: Spatial dimensions = 3.")
        )
    
    commentary = (
        "The derivation d = k - 1 = 3 from Field Closure is one of GFD's foundational claims. "
        "Whether this constitutes a genuine explanation for why space has 3 dimensions, or "
        "is simply an observation that the mathematics produces the right number, depends on "
        "the physical interpretation of Field Closure itself."
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
        "the Standard Model values, not derived from geometry. GFD provides a picture "
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
    GFD has d = 3 SPATIAL dimensions.
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
        "not explain WHY there are 3 generations; GFD's d = 3 provides a number that matches "
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
            "derives fractional charges from gauge theory. GFD observes that tetrahedral "
            "geometry produces the same numbers. Whether this indicates deeper structure "
            "or coincidence is left for the reader to evaluate."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
