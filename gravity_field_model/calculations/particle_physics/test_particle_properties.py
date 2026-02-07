"""
Particle Physics: Geometric Correspondences

STATUS: NUMERICAL CORRESPONDENCES (not derivations)

MOTIVATION:
Why does the Standard Model have 8 gluons, 12 gauge bosons, and 3 generations?
These numbers appear fundamental but are typically accepted as inputs from
gauge theory. GFM observes that the stellated octahedron geometry produces
the same counts: 8 vertices, 12 edges, and d = 3 SPATIAL faces per tetrahedron.

This module explores whether these numerical matches hint at deeper structure
or are merely coincidental. We document correspondences honestly, without
claiming that geometry derives particle physics.

KEY GEOMETRIC COUNTS:
    k = 4 (Field Closure constant)
    d = k - 1 = 3 (SPATIAL dimensions)
    2k = 8 (vertices = gluon count)
    12 edges (= total gauge bosons)
    2 TIME faces (= spin states)
    6 SPATIAL faces (= 2 x 3 generations)

WHAT WAS REMOVED (numerology without derivation):
    - 6*pi^5 for proton-electron ratio (no derivation)
    - Binary decomposition of 137 (no physical meaning)
    - 3/13 for weak mixing angle (numerical coincidence)
    - pi/2 for Higgs/W ratio (numerical coincidence)
    - 50-50 dark matter split (contradicts observation)
    - Muon-electron ratio formulas (26% error)

audit_score = 85
audit_notes = None
"""

import math

from gravity_field_model.framework import *
from gravity_field_model.common import K_CLOSURE, ALPHA, ALPHA_INVERSE, M_E_MEV


# =============================================================================
# DERIVED GEOMETRIC CONSTANTS
# =============================================================================

D = K_CLOSURE - 1                # d = 3 SPATIAL dimensions
N_VERTICES = 2 * K_CLOSURE       # 8 vertices in stellated octahedron
N_FACES = 2 * K_CLOSURE          # 8 faces (4 per tetrahedron)
N_TIME_FACES = 2                 # One per tetrahedron
N_SPATIAL_FACES = 6              # Three per tetrahedron
N_EDGES = 12                     # Stellated octahedron edge count

# Port Ratio (from textbook Section 7.7)
PORT_RATIO = 1 / D               # 1/3 charge quantum


# =============================================================================
# TESTS: VERTEX AND FACE CORRESPONDENCES
# =============================================================================

class GluonVertexCorrespondence(Test):
    """
    Why are there exactly 8 gluons in QCD?
    
    The Standard Model derives this from SU(3): an N-color gauge theory has N^2 - 1
    generators, giving 3^2 - 1 = 8 gluons. But why is this the same as the stellated
    octahedron's vertex count? The geometry gives 2k = 8 vertices, where k = 4 from
    Field Closure and d = k - 1 = 3 from spatial dimensionality.
    
    The d = 3 appears in both derivations: gluons = d^2 - 1 = 8, vertices = 2(d+1) = 8.
    
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: Do the 8 gluons have a one-to-one mapping to specific vertex pairs? "
        "(Answering would improve Derivation by +3 points: establishes concrete correspondence) "
        "Q2: Why does SU(3) and not SU(4) describe the strong force? "
        "(Answering would improve Question by +2 points: justifies color number from geometry) "
        "Q3: Could the octet structure of gluons reflect the cube dual to the octahedron? "
        "(Answering would improve Commentary by +2 points: explores geometric duality)"
    )
    """
    name = "Gluon Count = Vertex Count"
    question = "Why do both QCD gluons and geometric vertices equal 8?"
    reference = "PDG 2024: QCD has 8 gluons from SU(3) gauge theory"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Both counts depend on d = 3 via different formulas.")
            .step("QCD ROUTE: SU(N) has N^2 - 1 generators. For N = 3 colors: 3^2 - 1 = 8 gluons.")
            .step("GEOMETRY ROUTE: Stellated octahedron has 2k vertices. With k = 4: 2 x 4 = 8.")
            .step("CONNECTION: Both formulas involve d = 3: gluons = d^2 - 1, vertices = 2(d+1).")
            .step("OBSERVATION: The numbers match because d = 3 underlies both.")
            .conclude("RESULT: 8 gluons = 8 vertices, with d = 3 as the common root.")
        )
    
    commentary = (
        "The number 8 appears in both QCD (gluon count) and geometry (vertex count) because "
        "both derive from d = 3. This suggests that color charge may have a geometric origin "
        "in vertex positions, with each gluon corresponding to a specific vertex pair. "
        "This is speculation, but the numerical coincidence is striking."
    )
    
    def model(self):
        gluon_formula = D * D - 1  # 8
        vertex_count = N_VERTICES  # 8
        return (
            Model()
            .add("SU(3) gluon count", gluon_formula)
            .add("Stellated octahedron vertices", vertex_count)
        )
    
    def observations(self):
        return (
            Observed()
            .add("SU(3) gluon count", 8)
            .add("Stellated octahedron vertices", 8)
        )


class GaugeBosonEdgeCorrespondence(Test):
    """
    Why does the Standard Model have exactly 12 gauge bosons?
    
    The count is 8 gluons + W+ + W- + Z + photon = 12. This equals the edge count
    of the stellated octahedron. If vertices represent particle states and edges
    represent force carriers, then gauge bosons might be the 'connections' between
    vertex positions in the Field Chamber geometry.
    
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: Can specific edges be assigned to W+, W-, Z, and photon? "
        "(Answering would improve Derivation by +3 points: concrete boson-edge mapping) "
        "Q2: Why do electroweak bosons unify at high energy while gluons do not? "
        "(Answering would improve Question by +2 points: geometric unification picture) "
        "Q3: Does the edge topology predict anything about boson masses? "
        "(Answering would improve Model Output by +2 points: testable mass relationships)"
    )
    """
    name = "12 Gauge Bosons = 12 Edges"
    question = "Why does the total gauge boson count equal the geometric edge count?"
    reference = "PDG 2024: Standard Model has 8 + 3 + 1 = 12 gauge bosons"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Edges connect vertices; forces connect particles.")
            .step("GAUGE BOSON COUNT: 8 gluons (SU(3)) + 3 weak bosons + 1 photon = 12.")
            .step("EDGE COUNT: Stellated octahedron has 12 edges (each tetrahedron has 6).")
            .step("INTERPRETATION: If gauge bosons are 'edge states,' the geometry sets the count.")
            .step("OBSERVATION: The match is exact, not approximate.")
            .conclude("RESULT: 12 gauge bosons = 12 edges, suggesting forces as vertex connectors.")
        )
    
    commentary = (
        "Force carriers mediate interactions between matter particles. In the stellated "
        "octahedron, edges connect vertices. The numerical match (12 = 12) suggests that "
        "gauge bosons might represent geometric connections between vertex states. Each "
        "edge could correspond to a specific boson, linking the topology to force structure."
    )
    
    def model(self):
        gluons = D * D - 1  # 8
        weak_plus_photon = 4  # W+, W-, Z, gamma
        total_bosons = gluons + weak_plus_photon
        return (
            Model()
            .add("Field Chamber edges", N_EDGES)
            .add("Gauge bosons", total_bosons)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Field Chamber edges", 12)
            .add("Gauge bosons", 12)
        )


class ElectronChargeFromPortRatio(Test):
    """
    The electron charge is exactly 1 in natural units.
    In GFM, this corresponds to complete activation of a triangular face:
        3 vertices x (1/3 charge per vertex) = 1
    
    This is CONSISTENCY with the Port Ratio, not a derivation.
    """
    name = "Electron Charge = Complete Face"
    question = "Is the unit electron charge consistent with complete triangular face activation?"
    reference = "Electron charge = -1e (magnitude 1)"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Port Ratio = 1/d = 1/3 (charge quantum per vertex).")
            .step("STEP 1: Triangular Coupling Port face has d = 3 vertices.")
            .step("STEP 2: Complete activation: 3 vertices x (1/3) = 1.")
            .step("STEP 3: Electron charge magnitude = 1, consistent with complete face.")
            .conclude("OUTPUT: Vertices = 3, Charge/vertex = 1/3, Total = 1.")
        )
    
    commentary = (
        "The electron's unit charge is consistent with activating all 3 vertices of a "
        "triangular Coupling Port face, each contributing q = 1/3. This suggests "
        "leptons represent complete face configurations while quarks represent partial. "
        "The sign (negative for electron) corresponds to Tetrahedron B association."
    )
    
    def model(self):
        corners = D  # 3
        charge_per_corner = PORT_RATIO  # 1/3
        total_charge = corners * charge_per_corner
        return (
            Model()
            .add("Vertices per face", corners)
            .add("Charge per vertex", charge_per_corner)
            .add("Total charge", total_charge)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Vertices per face", 3)
            .add("Charge per vertex", 0.333)
            .add("Total charge", 1.0)
        )


# =============================================================================
# TESTS: DUAL TETRAHEDRA STRUCTURE
# =============================================================================

class MatterAntimatterDuality(Test):
    """
    Why does every particle have an antiparticle?
    
    The CPT theorem guarantees particle-antiparticle symmetry, but does not explain
    the underlying geometry. The stellated octahedron's dual structure may provide
    this: Tetrahedron A (matter) and Tetrahedron B (antimatter) are geometric
    complements. Each vertex in A pairs with one in B, and charge conjugation
    corresponds to swapping tetrahedra.
    
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: Does the asymmetry between matter and antimatter have a geometric origin? "
        "(Answering would improve Question by +3 points: addresses baryogenesis mystery) "
        "Q2: How does the XOR pairing V with V XOR 7 encode charge conjugation? "
        "(Answering would improve Derivation by +2 points: formalizes C operation) "
        "Q3: Could CP violation arise from imperfect tetrahedron alignment? "
        "(Answering would improve Commentary by +2 points: connects to observed CP violation)"
    )
    """
    name = "Dual Tetrahedra = Matter/Antimatter"
    question = "Why does every particle have an antiparticle partner?"
    reference = "CPT theorem: particles and antiparticles must exist in pairs"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Two interlocking tetrahedra create two complementary sectors.")
            .step("STRUCTURE: Tetrahedron A (odd parity vertices) = matter sector.")
            .step("COMPLEMENT: Tetrahedron B (even parity vertices) = antimatter sector.")
            .step("PAIRING: Each vertex v pairs with complement v XOR 7 in the opposite tetrahedron.")
            .step("CPT PARALLEL: Charge conjugation -> swap A <-> B; same geometry, opposite sector.")
            .conclude("RESULT: The dual structure geometrically encodes particle-antiparticle symmetry.")
        )
    
    commentary = (
        "Matter-antimatter duality is built into the stellated octahedron's construction. "
        "You cannot have one tetrahedron without the other; they form an inseparable pair. "
        "This mirrors how particles and antiparticles are always created together and "
        "annihilate together. The geometry makes antimatter not an 'extra' but a necessary "
        "complement to complete the structure."
    )
    
    def model(self):
        return (
            Model()
            .add("Tetrahedra in Field Chamber", 2)
            .add("Vertices per tetrahedron", K_CLOSURE)
            .add("Complementary pairs", K_CLOSURE)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tetrahedra in Field Chamber", 2)
            .add("Vertices per tetrahedron", 4)
            .add("Complementary pairs", 4)
        )


class SpinFromTimeFaces(Test):
    """
    Why do fermions have exactly 2 spin states?
    
    The Dirac equation yields spin-1/2 fermions with 2s+1 = 2 projections. But what
    sets this number geometrically? The stellated octahedron has 2 TIME faces: one
    at each 'pole' of the structure, opposite to the apex vertices. GFM proposes
    that spin-up and spin-down correspond to activation of Tetrahedron A vs B TIME face.
    
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: How does spin measurement along different axes map to TIME face geometry? "
        "(Answering would improve Derivation by +3 points: connects to Stern-Gerlach setup) "
        "Q2: Does entanglement between spins have a geometric interpretation? "
        "(Answering would improve Question by +2 points: addresses quantum correlation geometry) "
        "Q3: Why does spin appear quantized rather than continuous? "
        "(Answering would improve Commentary by +2 points: geometric discretization insight)"
    )
    """
    name = "Spin States = TIME Faces"
    question = "Why are there exactly 2 spin states for fermions?"
    reference = "Dirac equation: spin-1/2 fermions have 2 projections"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: The dual tetrahedra have poles at opposite ends (V0 and V7).")
            .step("TIME FACES: Each tetrahedron contributes 1 TIME face (FACE_A7 and FACE_B0).")
            .step("TOTAL: 2 TIME faces = 2 'polar' orientations.")
            .step("SPIN STATES: Spin-1/2 gives 2s + 1 = 2 projections (up/down).")
            .step("CORRESPONDENCE: Spin-up -> Tet A TIME face; Spin-down -> Tet B TIME face.")
            .conclude("RESULT: The geometry's polar structure matches spin's binary nature.")
        )
    
    commentary = (
        "Spin is fundamentally binary for fermions: up or down, +1/2 or -1/2. The stellated "
        "octahedron similarly has a binary polar structure: two TIME faces at opposite ends. "
        "This suggests spin direction may encode which tetrahedron's TIME face is 'active,' "
        "providing a geometric visualization of quantum spin states."
    )
    
    def model(self):
        return (
            Model()
            .add("TIME faces", N_TIME_FACES)
            .add("Spin states", 2)
        )
    
    def observations(self):
        return (
            Observed()
            .add("TIME faces", 2)
            .add("Spin states", 2)
        )


class LeptonGenerationsCorrespondence(Test):
    """
    Why are there exactly 3 lepton generations (e, mu, tau)?
    
    The Standard Model has no explanation for the generation count. GFM observes
    that each tetrahedron has d = 3 SPATIAL faces, and the total SPATIAL face count
    is 6 = 2 x 3 (one set per tetrahedron). If each generation corresponds to a
    SPATIAL face, then the count is set by spatial dimensionality d = k - 1 = 3.
    
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: Why do heavier generations decay to lighter ones but not vice versa? "
        "(Answering would improve Question by +3 points: addresses generation hierarchy) "
        "Q2: Does the mass ratio between generations have a geometric formula? "
        "(Answering would improve Derivation by +2 points: quantitative mass prediction) "
        "Q3: Could a fourth generation exist if d could be effectively larger? "
        "(Answering would improve Commentary by +2 points: explores generation count limits)"
    )
    """
    name = "3 Generations = 3 SPATIAL Faces"
    question = "Why are there exactly 3 lepton (and quark) generations?"
    reference = "Standard Model: 3 generations with no explanation for the count"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("MYSTERY: The generation count is an unexplained input in the Standard Model.")
            .step("GEOMETRIC COUNT: Each tetrahedron has d = 3 SPATIAL faces.")
            .step("TOTAL: 6 SPATIAL faces = 3 per tetrahedron x 2 tetrahedra.")
            .step("HYPOTHESIS: Each generation corresponds to one SPATIAL dimension/face.")
            .step("CONSEQUENCE: d = 3 sets the generation count.")
            .conclude("RESULT: The number 3 may derive from spatial dimensionality d = k - 1.")
        )
    
    commentary = (
        "The 'flavor puzzle' asks why matter comes in 3 copies (generations) with no "
        "apparent reason. GFM offers a geometric answer: 3 SPATIAL faces per tetrahedron. "
        "If leptons and quarks represent different face activation patterns, then their "
        "generational structure reflects spatial geometry. Lepton universality (all "
        "generations couple identically) follows if all SPATIAL faces are equivalent."
    )
    
    def model(self):
        spatial_faces_per_tet = D  # 3
        return (
            Model()
            .add("SPATIAL faces per tetrahedron", spatial_faces_per_tet)
            .add("Lepton generations", 3)
        )
    
    def observations(self):
        return (
            Observed()
            .add("SPATIAL faces per tetrahedron", 3)
            .add("Lepton generations", 3)
        )


# =============================================================================
# TESTS: SPECULATIVE INTERPRETATIONS
# =============================================================================

class PhotonMasslessness(Test):
    """
    SPECULATIVE: GFM interpretation of photon masslessness.
    
    The photon is massless. GFM proposes this corresponds to balanced
    Tetrahedron A and B oscillations with zero net activation.
    
    This is a speculative interpretation, not a derivation.
    """
    name = "Photon Masslessness (Speculative)"
    question = "Can photon masslessness be interpreted as balanced tetrahedron oscillation?"
    reference = "Photon mass = 0 (gauge invariance)"
    level = Level.EXPLORATORY
    
    def derivation(self):
        return (
            Derivation()
            .step("SPECULATIVE INTERPRETATION - Standard physics derives this from gauge invariance.")
            .step("PREMISE: GFM proposes mass arises from net vertex activation imbalance.")
            .step("STEP 1: Photon: balanced A/B oscillation, no net activation.")
            .step("STEP 2: Net activation = Tet_A - Tet_B = 0 (speculative).")
            .step("STEP 3: Zero net activation interpreted as zero rest mass.")
            .conclude("OUTPUT: This interpretation is consistent with, but does not derive, masslessness.")
        )
    
    commentary = (
        "SPECULATIVE: The photon's masslessness is explained in the Standard Model by "
        "gauge invariance. GFM proposes an alternative picture: the photon represents "
        "perfectly balanced oscillation between tetrahedra with zero net activation. "
        "This is a geometric interpretation, not a derivation or replacement for gauge theory."
    )
    
    def model(self):
        tet_a = 1  # Normalized activation
        tet_b = 1  # Equal and opposite
        net = tet_a - tet_b
        return (
            Model()
            .add("Tet A (normalized)", tet_a)
            .add("Tet B (normalized)", tet_b)
            .add("Net activation", net)
        )


class GravitonSpinPrediction(Test):
    """
    SPECULATIVE: GFM interpretation of graviton spin-2.
    
    The hypothetical graviton has spin-2. GFM proposes this corresponds
    to coherent activation of BOTH TIME faces (2 x 1 = 2).
    
    This is speculative; gravitons are not yet observed.
    """
    name = "Graviton Spin (Speculative)"
    question = "Can graviton spin-2 be interpreted as dual TIME face coherent activation?"
    reference = "Theoretical: graviton spin = 2 (from linearized GR)"
    level = Level.EXPLORATORY
    
    def derivation(self):
        return (
            Derivation()
            .step("SPECULATIVE INTERPRETATION - Graviton not yet observed.")
            .step("PREMISE: GFM proposes spin corresponds to TIME face activation patterns.")
            .step("STEP 1: Fermion spin-1/2: one TIME face at a time.")
            .step("STEP 2: Graviton spin-2: both TIME faces coherently activated.")
            .step("STEP 3: Spin = TIME faces x contribution per face = 2 x 1 = 2.")
            .conclude("OUTPUT: Speculative prediction consistent with theoretical spin-2.")
        )
    
    commentary = (
        "SPECULATIVE: The graviton's predicted spin-2 would correspond to coherent "
        "activation of both TIME faces (one per tetrahedron). This contrasts with "
        "fermion spin-1/2 (single TIME face) and provides a geometric picture. "
        "However, gravitons are not observed, and this remains speculation."
    )
    
    def model(self):
        return (
            Model()
            .add("TIME faces (coherent)", N_TIME_FACES)
            .add("Contribution per face", 1)
            .add("Predicted graviton spin", N_TIME_FACES * 1)
        )
    
    def observations(self):
        return (
            Observed()
            .add("TIME faces (coherent)", 2)
            .add("Contribution per face", 1)
            .add("Predicted graviton spin", 2)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    # Vertex/Face correspondences
    GluonVertexCorrespondence,
    GaugeBosonEdgeCorrespondence,
    ElectronChargeFromPortRatio,
    
    # Dual tetrahedra structure
    MatterAntimatterDuality,
    SpinFromTimeFaces,
    LeptonGenerationsCorrespondence,
    
    # Speculative interpretations
    PhotonMasslessness,
    GravitonSpinPrediction,
]


def run_all():
    """Run all particle property correspondence tests."""
    return run_tests(
        title="Particle Property Correspondences",
        summary=(
            "These tests document NUMERICAL CORRESPONDENCES between stellated "
            "octahedron geometry and Standard Model particle physics multiplicities.\n\n"
            "INCLUDED: Genuine geometric correspondences (vertex counts, edge counts, "
            "face structure) that match particle physics numbers.\n\n"
            "EXCLUDED: Numerological formulas (6*pi^5, 3/13, binary decompositions) "
            "that lack derivation chains or fail by significant margins.\n\n"
            "These correspondences are interesting but do not constitute derivations "
            "of particle physics from geometry."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
