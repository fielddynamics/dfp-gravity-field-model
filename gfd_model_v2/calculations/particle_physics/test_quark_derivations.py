"""
Particle Physics: Quark Charge Correspondence

The model observes numerical correspondences between geometric properties of the
stellated octahedron and Standard Model parameters. A tetrahedron has k=4 faces,
giving d = k-1 = 3 spatial dimensions. The reciprocal 1/d = 1/3 corresponds
numerically to the quark charge quantum.

These tests document these correspondences without claiming the model derives
or explains the Standard Model. The reader should evaluate whether these
numerical agreements are meaningful or coincidental.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group


# =============================================================================
# CONSTANTS
# =============================================================================

K_CLOSURE = 4  # Tetrahedral face count
D = K_CLOSURE - 1  # Model's derived spatial dimensions
STELLATED_VERTICES = 2 * K_CLOSURE  # 8 vertices in stellated octahedron
CORNERS_PER_FACE = D  # 3 corners per triangular face
TOTAL_CORNER_STATES = STELLATED_VERTICES * CORNERS_PER_FACE  # 24

# Derived charge quantum
Q_MIN = 1 / D  # 1/3 (minimum charge from geometry)

# Standard Model values
SM_QUARK_CHARGE_QUANTUM = 1/3
SM_NUM_COLORS = 3
SM_QUARKS_PER_BARYON = 3
SM_NUM_GENERATIONS = 3


# =============================================================================
# FACE ACTIVATION PATTERNS
# =============================================================================

def get_face_activation_patterns():
    """Return all 8 possible face activation patterns (3-bit combinations)."""
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

class QuarkChargeFromGeometry(GFDTest):
    """
    The model produces 1/d = 1/3 from the structure d = k-1 = 3. This value
    corresponds numerically to the quark charge quantum e/3 in the Standard Model.
    """
    name = "Quark Charge Correspondence"
    question = "What is the minimum electric charge quantum that emerges from the Field Chamber geometry, and how does it compare to observed quark charges?"
    reference_source = "Standard Model (e/3 charge quantum)"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, k = 4 tetrahedral faces determine d = k - 1 = 3 SPATIAL dimensions. "
        "STEP 1: Each Coupling Port presents a triangular face with d = 3 vertices. "
        "STEP 2: Port Ratio = 1/d = 1/3 (minimum charge contribution per vertex). "
        "STEP 3: All quark charges are integer multiples of this quantum. "
        "OUTPUT: Quark charge quantum = 1/3."
    )
    commentary = (
        "The emergence of 1/3 from Field Closure (k=4 faces yielding d=k-1=3 SPATIAL dimensions) "
        "corresponds numerically to the fractional charge quantum observed in quarks. This suggests "
        "that the Port Ratio inherent to the stellated octahedron's triangular faces may encode "
        "information consistent with charge quantization, though the physical mechanism remains unspecified."
    )
    
    def model(self):
        d = D  # 3 spatial dimensions
        q_derived = 1 / d  # 1/3
        return {"Quark charge quantum": q_derived}
    
    def observations(self):
        return {"Quark charge quantum": SM_QUARK_CHARGE_QUANTUM}


class NumberOfColors(GFDTest):
    """
    A triangular face has 3 corners. This number corresponds to the 3 color
    charges of QCD. The correspondence is numerical; no physical mechanism
    linking face geometry to color charge is proposed.
    """
    name = "Color Charge Correspondence"
    question = "How many independent color charges arise from the Coupling Port vertex structure, and does this match quantum chromodynamics?"
    reference_source = "QCD (3 color charges: R, G, B)"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, d = k - 1 = 3 gives d = 3 vertices per Coupling Port face. "
        "STEP 1: Each triangular face has 3 distinguishable vertex positions. "
        "STEP 2: These 3 positions can be independently activated (color states). "
        "STEP 3: QCD SU(3) symmetry requires exactly 3 color charges (R, G, B). "
        "OUTPUT: Number of colors = 3."
    )
    commentary = (
        "Each Coupling Port on the stellated octahedron presents a triangular face with three "
        "vertices, corresponding numerically to QCD's three color charges. The SPATIAL faces of "
        "Tetrahedron A and Tetrahedron B each contribute this threefold structure, which may "
        "indicate a geometric basis for the color degree of freedom."
    )
    
    def model(self):
        return {"Number of colors": CORNERS_PER_FACE}
    
    def observations(self):
        return {"Number of colors": SM_NUM_COLORS}


class BaryonsNeed3Quarks(GFDTest):
    """
    Baryons contain 3 quarks. The model's triangular faces have 3 corners.
    This numerical correspondence is noted without claiming a derivation
    of baryon structure from geometry.
    """
    name = "Baryon Quark Correspondence"
    question = "Why do baryons contain exactly three quarks, and does this constraint emerge from the Coupling Port geometry?"
    reference_source = "Particle physics (proton = uud, neutron = udd)"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, d = k - 1 = 3 vertices per Coupling Port face. "
        "STEP 1: Complete face activation requires populating all d = 3 vertex positions. "
        "STEP 2: Each quark occupies one vertex of the triangular face. "
        "STEP 3: Color-neutral baryon requires 3 quarks to complete the face (R+G+B = white). "
        "OUTPUT: Quarks per baryon = 3."
    )
    commentary = (
        "The requirement for three quarks per baryon is consistent with the three Coupling Port "
        "vertices on each triangular face of the Field Chamber. This correspondence suggests that "
        "baryon composition may reflect an underlying geometric constraint related to SPATIAL face structure."
    )
    
    def model(self):
        return {"Quarks per baryon": CORNERS_PER_FACE}
    
    def observations(self):
        return {"Quarks per baryon": SM_QUARKS_PER_BARYON}


class ColorConfinement(GFDTest):
    """
    The model examines face activation patterns (3-bit combinations for 3 corners).
    Complete (111) and empty (000) states are distinguished from partial states.
    This structure is compared to QCD color confinement without claiming derivation.
    """
    name = "Activation Pattern Structure"
    question = "How many distinct activation patterns exist for a three-vertex Coupling Port face, and which patterns correspond to observable particles?"
    reference_source = None
    derivation = (
        "PREMISE: A Coupling Port face has d = 3 vertices, each either active (1) or inactive (0). "
        "STEP 1: Total patterns = 2^d = 2³ = 8 distinct states. "
        "STEP 2: Pattern 000 (vacuum) and 111 (complete) are color-neutral; others carry net color. "
        "STEP 3: Partial states (1-2 vertices) = 8 - 2 = 6 colored states that cannot propagate freely. "
        "OUTPUT: Complete (111) corners = 3, Empty (000) corners = 0, Partial (colored) states = 6."
    )
    commentary = (
        "The distinction between complete (all three Coupling Port vertices active) and partial "
        "activation states on SPATIAL faces corresponds structurally to the difference between "
        "color-neutral hadrons and color-charged quarks. This pattern is consistent with confinement "
        "phenomenology, where only complete states propagate freely."
    )
    
    def model(self):
        patterns = get_face_activation_patterns()
        complete_pattern = patterns[0b111]
        empty_pattern = patterns[0b000]
        partial_patterns = [p for p in patterns.values() if 0 < p['num_active'] < 3]
        
        return {
            "Complete (111) corners": complete_pattern['num_active'],
            "Empty (000) corners": empty_pattern['num_active'],
            "Partial (colored) states": len(partial_patterns),
        }


class MesonStructure(GFDTest):
    """Mesons correspond to 2-corner (quark-antiquark) patterns."""
    name = "Meson Pattern Count"
    question = "How many distinct two-vertex activation patterns exist on a Coupling Port face, and does this match meson combinatorics?"
    reference_source = None
    derivation = (
        "PREMISE: A Coupling Port face has d = 3 vertices. "
        "STEP 1: Two-vertex patterns = C(d,2) = C(3,2) = 3 (choosing 2 from 3). "
        "STEP 2: Patterns are 011, 101, 110 in binary notation. "
        "STEP 3: These correspond to 3 possible color-anticolor meson pairings. "
        "OUTPUT: Two-corner patterns = 3, Expected C(3,2) = 3."
    )
    commentary = (
        "The three distinct two-vertex activation patterns on a triangular Coupling Port face "
        "correspond numerically to the combinatorics of quark-antiquark pairing. This suggests "
        "that meson structure may be geometrically represented by partial face activations on the "
        "stellated octahedron's SPATIAL faces."
    )
    
    def model(self):
        patterns = get_face_activation_patterns()
        two_corner_patterns = [p for p in patterns.values() if p['num_active'] == 2]
        expected = 3  # C(3,2) = 3 ways to choose 2 from 3
        
        return {
            "Two-corner patterns": len(two_corner_patterns),
            "Expected C(3,2)": expected,
        }


class TotalCornerStates(GFDTest):
    """
    The stellated octahedron has 8 faces, each with 3 corners, giving 24
    total corner states. This number equals the order of the binary
    tetrahedral group, a mathematical correspondence.
    """
    name = "24 Corner States"
    question = "How many total Coupling Port vertex states exist in the complete Field Chamber, and what mathematical structure does this count correspond to?"
    reference_source = "Binary tetrahedral group (order 24)"
    tolerance = 0.01
    derivation = (
        "PREMISE: Field Chamber has 2k = 8 faces, each with d = 3 vertices (Coupling Ports). "
        "STEP 1: Total vertex states = faces × vertices per face = 8 × 3 = 24. "
        "STEP 2: This equals the order of the binary tetrahedral group 2T ⊂ SU(2). "
        "STEP 3: Correspondence suggests Field Chamber symmetry connects to spin physics. "
        "OUTPUT: Total corner states = 24."
    )
    commentary = (
        "The 24 total Coupling Port vertex states arising from the Field Chamber's 8 faces "
        "corresponds to the order of the binary tetrahedral group. This mathematical coincidence "
        "suggests a potential connection between the stellated octahedron's symmetry structure "
        "and discrete subgroups of SU(2) relevant to spin physics."
    )
    
    def model(self):
        num_faces = STELLATED_VERTICES
        corners_each = CORNERS_PER_FACE
        total = num_faces * corners_each
        return {"Total corner states": total}
    
    def observations(self):
        return {"Total corner states": 24}


class StellatedOctahedronVertices(GFDTest):
    """
    The stellated octahedron has 8 vertices. In the model, this equals
    2k where k=4 is the face count of a tetrahedron.
    """
    name = "Vertex Count"
    question = "How many vertices does the Field Chamber possess, and how does this follow from the dual tetrahedron construction?"
    reference_source = "Stellated octahedron geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Chamber is formed by two interpenetrating tetrahedra (A and B). "
        "STEP 1: Tetrahedron A contributes k = 4 vertices. "
        "STEP 2: Tetrahedron B contributes k = 4 vertices. "
        "STEP 3: Total vertices = k + k = 2k = 2 × 4 = 8. "
        "OUTPUT: Vertices = 8."
    )
    commentary = (
        "The 2k=8 vertices of the stellated octahedron arise from the interpenetration of "
        "Tetrahedron A and Tetrahedron B, each contributing k=4 vertices. This structure "
        "defines the Field Chamber's spatial extent and is consistent with the octonary "
        "patterns observed in gluon counting and other Standard Model multiplicities."
    )
    
    def model(self):
        k = K_CLOSURE
        expected = 2 * k
        return {"Vertices": expected}
    
    def observations(self):
        return {"Vertices": 8}


class SpatialDimensions(GFDTest):
    """Spatial dimensions d = k - 1 = 3."""
    name = "Spatial Dimensions"
    question = "How many spatial dimensions emerge from Field Closure, and does this match the observed dimensionality of physical space?"
    reference_source = "Observed 3D space"
    tolerance = 0.01
    derivation = (
        "PREMISE: Field Closure requires k = 4 faces to close the tetrahedron. "
        "STEP 1: Of k faces, one serves as TIME face, leaving d = k - 1 SPATIAL faces. "
        "STEP 2: Calculate: d = 4 - 1 = 3 SPATIAL dimensions. "
        "STEP 3: This matches physical observation of 3 macroscopic spatial dimensions. "
        "OUTPUT: Spatial dimensions = 3."
    )
    commentary = (
        "The derivation d=k-1=3 from Field Closure (k=4) corresponds to observed three-dimensional "
        "space. The SPATIAL faces of each tetrahedron number three, leaving one TIME face, which "
        "suggests a geometric origin for the 3+1 dimensional structure of spacetime."
    )
    
    def model(self):
        k = K_CLOSURE
        d_derived = k - 1
        return {"Spatial dimensions": d_derived}
    
    def observations(self):
        return {"Spatial dimensions": 3}


class ProtonCharge(GFDTest):
    """Proton charge = +1 from quark composition (uud)."""
    name = "Proton Charge"
    question = "Using the geometrically derived charge quantum, what is the predicted electric charge of the proton from its uud quark composition?"
    reference_source = "Measured proton charge = +1e"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, charge quantum q = 1/d = 1/3. "
        "STEP 1: Up quark: Q_up = +2 × (1/3) = +2/3 (2 vertices on Tet A). "
        "STEP 2: Down quark: Q_down = -1 × (1/3) = -1/3 (1 vertex on Tet B). "
        "STEP 3: Proton (uud): Q = Q_up + Q_up + Q_down = (+2/3) + (+2/3) + (-1/3) = +1. "
        "OUTPUT: Proton charge (e) = 1.0."
    )
    commentary = (
        "Using the geometrically-derived charge quantum q=1/d=1/3, the proton's uud composition "
        "yields unit positive charge. This is consistent with the Port Ratio providing the "
        "fundamental charge unit, with quark flavor determining the coefficient applied to each "
        "Coupling Port vertex contribution."
    )
    
    def model(self):
        q = Q_MIN  # 1/3
        up_charge = 2 * q      # +2/3
        down_charge = -1 * q   # -1/3
        proton = up_charge + up_charge + down_charge
        return {"Proton charge (e)": proton}
    
    def observations(self):
        return {"Proton charge (e)": 1.0}


class NeutronCharge(GFDTest):
    """Neutron charge = 0 from quark composition (udd)."""
    name = "Neutron Charge"
    question = "Using the geometrically derived charge quantum, what is the predicted electric charge of the neutron from its udd quark composition?"
    reference_source = "Measured neutron charge = 0"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, charge quantum q = 1/d = 1/3. "
        "STEP 1: Up quark: Q_up = +2 × (1/3) = +2/3. "
        "STEP 2: Down quark: Q_down = -1 × (1/3) = -1/3. "
        "STEP 3: Neutron (udd): Q = Q_up + Q_down + Q_down = (+2/3) + (-1/3) + (-1/3) = 0. "
        "OUTPUT: Neutron charge (e) = 0.0."
    )
    commentary = (
        "The neutron's udd composition produces net zero charge when evaluated with q=1/3. "
        "This corresponds to a balanced configuration of Coupling Port vertex activations "
        "where the Field Chamber achieves charge neutrality through compensating contributions "
        "from the three constituent quarks."
    )
    
    def model(self):
        q = Q_MIN
        up_charge = 2 * q
        down_charge = -1 * q
        neutron = up_charge + down_charge + down_charge
        return {"Neutron charge (e)": neutron}
    
    def observations(self):
        return {"Neutron charge (e)": 0.0}


class ThreeGenerationsHint(GFDTest):
    """Connection between d=3 and 3 particle generations (speculative)."""
    name = "Generation Count Hint"
    question = "Is there a correspondence between the d=3 SPATIAL dimensions from Field Closure and the three generations of fermions in the Standard Model?"
    reference_source = None
    derivation = (
        "PREMISE: From Field Closure, d = k - 1 = 3 SPATIAL dimensions/faces. "
        "STEP 1: Standard Model has exactly 3 fermion generations. "
        "STEP 2: Numerical comparison: d = 3 (geometric) = 3 (generations). "
        "STEP 3: Mechanism linking SPATIAL faces to generations remains speculative. "
        "OUTPUT: Spatial dimensions d = 3, Particle generations = 3, Match = 1."
    )
    commentary = (
        "The numerical coincidence between d=3 SPATIAL dimensions and three particle generations "
        "may indicate a deeper structural relationship. However, the mechanism by which Field "
        "Closure would constrain generation number remains unspecified, and this correspondence "
        "should be regarded as speculative pending further theoretical development."
    )
    
    def model(self):
        return {
            "Spatial dimensions d": D,
            "Particle generations": SM_NUM_GENERATIONS,
            "Match": 1 if D == SM_NUM_GENERATIONS else 0,
        }


class QMinInAlphaFormula(GFDTest):
    """q_min = 1/3 matches the input to Singh's alpha derivation."""
    name = "Alpha Formula Input"
    question = "Does the Port Ratio derived from Field Closure match the minimum charge quantum used in independent derivations of the fine structure constant?"
    reference_source = "Singh alpha derivation (q_min = 1/3)"
    tolerance = 0.01
    derivation = (
        "PREMISE: From Field Closure, d = k - 1 = 3 gives Port Ratio q_min = 1/d = 1/3. "
        "STEP 1: Singh's alpha derivation uses q_min = 1/3 as input parameter. "
        "STEP 2: Compare: GFD Port Ratio = 1/3, Singh parameter = 1/3. "
        "STEP 3: Exact match suggests geometric derivation provides the fundamental charge quantum. "
        "OUTPUT: q_min = 1/3."
    )
    commentary = (
        "The Port Ratio q=1/d=1/3 derived from Field Closure corresponds exactly to the minimum "
        "charge quantum appearing in Singh's fine structure constant calculation. This suggests "
        "that the stellated octahedron geometry may provide a structural basis for the charge "
        "parameter used in electromagnetic coupling strength derivations."
    )
    
    def model(self):
        q_derived = 1 / D
        return {"q_min": q_derived}
    
    def observations(self):
        return {"q_min": 1/3}


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    QuarkChargeFromGeometry,
    NumberOfColors,
    BaryonsNeed3Quarks,
    ColorConfinement,
    MesonStructure,
    TotalCornerStates,
    StellatedOctahedronVertices,
    SpatialDimensions,
    ProtonCharge,
    NeutronCharge,
    ThreeGenerationsHint,
    QMinInAlphaFormula,
]


def run_all_tests():
    """Run all quark derivation tests."""
    return run_test_group(
        title="Quark Charge Correspondences",
        summary=(
            "These tests document numerical correspondences between geometric properties "
            "of the stellated octahedron and Standard Model parameters. The ratio 1/d = 1/3 "
            "(where d = k-1 = 3) matches the quark charge quantum. The 3 corners per "
            "triangular face match the 3 color charges. These correspondences are presented "
            "without claiming the geometry derives or explains the Standard Model."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
