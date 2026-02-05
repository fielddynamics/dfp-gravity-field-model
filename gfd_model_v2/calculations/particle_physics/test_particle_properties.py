"""
Particle Physics: Geometric Correspondences

STATUS: NUMERICAL CORRESPONDENCES (not derivations)

These tests document numerical correspondences between the stellated octahedron
geometry and particle physics multiplicities. The geometric counts:

    k = 4 (tetrahedral faces)
    d = k - 1 = 3 (SPATIAL dimensions)
    2k = 8 (vertices)
    2 x TIME faces = 2 (spin states)
    12 edges

are compared to Standard Model particle counts.

WHAT THESE TESTS DO AND DO NOT SHOW:

DO SHOW:
    - Geometric counts that happen to match particle physics numbers
    - Structural features (dual tetrahedra) consistent with matter/antimatter

DO NOT SHOW:
    - Derivations of Standard Model physics from geometry
    - Predictions that differ from the Standard Model
    - Physical mechanisms linking geometry to particles

REMOVED FROM PREVIOUS VERSION (numerology without derivation):
    - 6*pi^5 for proton-electron ratio (no derivation)
    - Binary decomposition of 137 (no physical meaning)
    - 3/13 for weak mixing angle (numerical coincidence)
    - pi/2 for Higgs/W ratio (numerical coincidence)
    - 50-50 dark matter split (contradicts observation)
    - Muon-electron ratio formulas (26% error)
"""

import math

from gfd_model_v2.framework import *
from gfd_model_v2.common import K_CLOSURE, ALPHA, ALPHA_INVERSE


# =============================================================================
# GEOMETRIC CONSTANTS
# =============================================================================

D = K_CLOSURE - 1                # d = 3 SPATIAL dimensions
VERTICES = 2 * K_CLOSURE         # 8 vertices in stellated octahedron
FACES = 2 * K_CLOSURE            # 8 faces (4 per tetrahedron)
TIME_FACES = 2                   # One per tetrahedron
SPATIAL_FACES = 6                # Three per tetrahedron
EDGES = 12                       # Stellated octahedron edge count

# Port Ratio
PORT_RATIO = 1 / D               # 1/3 charge quantum

# Particle masses for reference
M_ELECTRON = 0.511               # MeV/c^2


# =============================================================================
# TESTS: VERTEX AND FACE CORRESPONDENCES
# =============================================================================

class GluonVertexCorrespondence(Test):
    """
    QCD has 8 gluons (SU(3) generators: 3^2 - 1 = 8).
    The stellated octahedron has 8 vertices (2k = 8).
    
    Both formulas use d = 3:
        - Gluons: d^2 - 1 = 8
        - Vertices: 2k = 2(d+1) = 8
    
    This is a numerical correspondence, not a derivation.
    """
    name = "Gluon Count = Vertex Count"
    question = "Do the stellated octahedron vertices correspond numerically to the QCD gluon count?"
    reference = "QCD: 8 gluons from SU(3)"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: From Field Closure, d = k - 1 = 3; vertices = 2k = 8.")
            .step("STEP 1: SU(3) gluon count: d^2 - 1 = 3^2 - 1 = 8.")
            .step("STEP 2: Field Chamber vertex count: 2k = 2 x 4 = 8.")
            .step("STEP 3: Both equal 8. Correspondence is numerical; no mechanism proposed.")
            .conclude("OUTPUT: Gluons = 8, Vertices = 8 (numerical match).")
        )
    
    commentary = (
        "The 8 gluons of QCD and 8 vertices of the stellated octahedron both arise from "
        "d = 3: gluons from SU(3) structure (d^2-1), vertices from 2k = 2(d+1). "
        "Whether this indicates a connection between color charge and vertex position "
        "or is coincidental remains an open question."
    )
    
    def model(self):
        gluon_formula = D * D - 1  # 8
        vertex_count = 2 * K_CLOSURE  # 8
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
    The Standard Model has 12 gauge bosons: 8 gluons + W+ + W- + Z + photon.
    The stellated octahedron has 12 edges.
    
    This is a numerical correspondence, not a derivation.
    """
    name = "12 Gauge Bosons = 12 Edges"
    question = "Do the stellated octahedron edges correspond numerically to the Standard Model gauge boson count?"
    reference = "Standard Model: 8 gluons + 3 weak bosons + 1 photon = 12"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Stellated octahedron has 12 edges connecting its 8 vertices.")
            .step("STEP 1: Gluons = d^2 - 1 = 8 (SU(3) generators).")
            .step("STEP 2: Weak bosons = 3 (W+, W-, Z) + photon = 1. Total = 8 + 3 + 1 = 12.")
            .step("STEP 3: Field Chamber edges = 12. Numerical correspondence noted.")
            .conclude("OUTPUT: Gauge bosons = 12, Edges = 12 (numerical match).")
        )
    
    commentary = (
        "The 12 edges of the stellated octahedron match the 12 gauge bosons of the "
        "Standard Model. Force carriers might geometrically correspond to edge connections "
        "between vertices. This is speculative; no physical mechanism is proposed."
    )
    
    def model(self):
        gluons = D * D - 1  # 8
        weak_plus_photon = 4  # W+, W-, Z, gamma
        total_bosons = gluons + weak_plus_photon
        return (
            Model()
            .add("Field Chamber edges", EDGES)
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
    In GFD, this corresponds to complete activation of a triangular face:
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
    The stellated octahedron consists of two interpenetrating tetrahedra.
    This dual structure provides a natural geometric basis for 
    particle-antiparticle pairing.
    
    This is a STRUCTURAL correspondence, not a derivation of CPT.
    """
    name = "Dual Tetrahedra = Matter/Antimatter"
    question = "Does the dual tetrahedron structure provide a geometric basis for particle-antiparticle symmetry?"
    reference = "CPT theorem requires particle-antiparticle pairs"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Field Chamber = Tetrahedron A + Tetrahedron B, interpenetrating.")
            .step("STEP 1: Tetrahedron A has k = 4 vertices (matter sector).")
            .step("STEP 2: Tetrahedron B has k = 4 vertices (antimatter sector).")
            .step("STEP 3: Each vertex in A has a complementary vertex in B.")
            .conclude("OUTPUT: Tetrahedra = 2, Vertices each = 4, Complementary pairs = 4.")
        )
    
    commentary = (
        "The dual-tetrahedron structure naturally provides two equal sectors. If matter "
        "corresponds to Tetrahedron A and antimatter to Tetrahedron B, the geometry "
        "encodes particle-antiparticle symmetry. Charge conjugation swaps A <-> B. "
        "This is a structural analogy consistent with CPT, not a derivation of it."
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
    Fermions have spin-1/2, giving 2 spin states.
    The Field Chamber has 2 TIME faces (one per tetrahedron).
    
    GFD proposes this correspondence: spin states = TIME face count.
    This is a CLAIM, not a standard physics derivation.
    """
    name = "Spin States = TIME Faces"
    question = "Do the 2 TIME faces of the Field Chamber correspond to the 2 spin states of fermions?"
    reference = "Spin-1/2 fermions have 2 states (up/down)"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Each tetrahedron has 1 TIME face; total = 2 TIME faces.")
            .step("STEP 1: Spin-1/2 particles have 2s + 1 = 2 spin projections.")
            .step("STEP 2: GFD correspondence: spin-up = Tet A TIME face, spin-down = Tet B TIME face.")
            .step("STEP 3: Numerical match: 2 TIME faces = 2 spin states.")
            .conclude("OUTPUT: TIME faces = 2, Spin states = 2.")
        )
    
    commentary = (
        "The 2 TIME faces of the stellated octahedron correspond to the 2 spin states "
        "of fermions. GFD proposes that spin-up and spin-down represent activation of "
        "the TIME face on Tetrahedron A versus Tetrahedron B. This provides a geometric "
        "picture for spin but does not derive spin-1/2 from first principles."
    )
    
    def model(self):
        return (
            Model()
            .add("TIME faces", TIME_FACES)
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
    There are 3 lepton generations (e, mu, tau).
    There are d = 3 SPATIAL dimensions from Field Closure.
    Each tetrahedron has 3 SPATIAL faces.
    
    This is a numerical correspondence, not a derivation.
    """
    name = "3 Generations = 3 SPATIAL Faces"
    question = "Does the count of lepton generations correspond to the SPATIAL face count per tetrahedron?"
    reference = "Standard Model: 3 lepton generations"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: From Field Closure, each tetrahedron has d = 3 SPATIAL faces.")
            .step("STEP 1: Standard Model has 3 lepton generations: e, mu, tau.")
            .step("STEP 2: Each generation may correspond to one SPATIAL face.")
            .step("STEP 3: Numerical match: d = 3 = generations. No mechanism proposed.")
            .conclude("OUTPUT: SPATIAL faces per tetrahedron = 3, Generations = 3.")
        )
    
    commentary = (
        "The 3 lepton generations match the 3 SPATIAL faces per tetrahedron. "
        "If each generation corresponds to one SPATIAL face, lepton universality "
        "(equal couplings) follows from equivalent face structure. This is "
        "speculative; the Standard Model does not explain WHY there are 3 generations."
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
    SPECULATIVE: GFD interpretation of photon masslessness.
    
    The photon is massless. GFD proposes this corresponds to balanced
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
            .step("PREMISE: GFD proposes mass arises from net vertex activation imbalance.")
            .step("STEP 1: Photon: balanced A/B oscillation, no net activation.")
            .step("STEP 2: Net activation = Tet_A - Tet_B = 0 (speculative).")
            .step("STEP 3: Zero net activation interpreted as zero rest mass.")
            .conclude("OUTPUT: This interpretation is consistent with, but does not derive, masslessness.")
        )
    
    commentary = (
        "SPECULATIVE: The photon's masslessness is explained in the Standard Model by "
        "gauge invariance. GFD proposes an alternative picture: the photon represents "
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
    SPECULATIVE: GFD interpretation of graviton spin-2.
    
    The hypothetical graviton has spin-2. GFD proposes this corresponds
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
            .step("PREMISE: GFD proposes spin corresponds to TIME face activation patterns.")
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
            .add("TIME faces (coherent)", TIME_FACES)
            .add("Contribution per face", 1)
            .add("Predicted graviton spin", TIME_FACES * 1)
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
