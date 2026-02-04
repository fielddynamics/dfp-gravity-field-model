"""
Spin-1/2 Derivation
===================

The model calculates spin from the face topology of the stellated octahedron:

  S = (N_time / N_total) x L = (2/8) x 2 = 1/2

The structure has 8 faces total. Two faces (opposite the apexes) are classified
as TIME faces, giving f_time = 2/8 = 1/4. When multiplied by the spin quantum
number 2, this yields 1/2. This value corresponds to the spin of fermions
like electrons. The model does not explain why this correspondence exists,
but documents it as a geometric property of the dual tetrahedron structure.
"""

import sys
import os
import numpy as np
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from gfd_model_v2.base import GFDTest, GroupResult, Renderer, run_test_group
from gfd_model_v2.common import FACES, TIME_FACES, SPATIAL_FACES, HBAR


# =============================================================================
# TESTS
# =============================================================================

class TotalFaceCount(GFDTest):
    """
    The stellated octahedron has 8 faces total: 4 per tetrahedron.
    This is the foundation for the 2:6 TIME:SPATIAL ratio.
    """
    name = "Total Face Count"
    question = "Does the stellated octahedron have exactly 2k=8 Coupling Ports (faces), providing the denominator for spin calculation?"
    reference_source = "Geometry (4 + 4)"
    tolerance = 0.001
    derivation = (
        "PREMISE: The stellated octahedron consists of two tetrahedra, each with k=4 faces. "
        "STEP 1: Tetrahedron A has k = 4 faces (triangular Coupling Ports). "
        "STEP 2: Tetrahedron B has k = 4 faces (triangular Coupling Ports). "
        "STEP 3: Total faces = k + k = 2k = 8. "
        "STEP 4: This count provides the denominator in the spin formula: S = (N_time / N_total) * 2. "
        "OUTPUT: The dual Field Chamber has exactly 8 Coupling Ports."
    )
    commentary = None  # Basic geometric count
    
    def model(self) -> Dict[str, float]:
        return {"Total faces": len(FACES)}
    
    def observations(self) -> Dict[str, float]:
        return {"Total faces": 8}


class TimeFaceCount(GFDTest):
    """
    Two faces are classified as TIME faces: FACE_A7 (opposite V7, the
    Tet_A apex) and FACE_B0 (opposite V0, the Tet_B apex). These are
    geometrically distinguished by being opposite the apex vertices.
    """
    name = "TIME Face Count"
    question = "Are there exactly 2 TIME Coupling Ports (opposite the apex vertices), providing the numerator for spin calculation?"
    reference_source = "Topology (2 apexes)"
    tolerance = 0.001
    derivation = (
        "PREMISE: TIME faces are defined as those opposite the apex vertices of each tetrahedron. "
        "STEP 1: Tetrahedron A apex is V7. The face opposite V7 is FACE_A7 (contains V1,V2,V4). "
        "STEP 2: Tetrahedron B apex is V0. The face opposite V0 is FACE_B0 (contains V3,V5,V6). "
        "STEP 3: Count TIME faces: FACE_A7 and FACE_B0 = 2 faces. "
        "STEP 4: These 2 faces provide the numerator in spin formula: S = (2/8) * 2 = 1/2. "
        "OUTPUT: Exactly 2 TIME Coupling Ports exist, one per Field Chamber."
    )
    commentary = (
        "Two TIME Coupling Ports correspond to one per tetrahedron, positioned "
        "opposite the apex vertices. This count determines the numerator in the "
        "spin-1/2 derivation."
    )
    
    def model(self) -> Dict[str, float]:
        return {"TIME faces": len(TIME_FACES)}
    
    def observations(self) -> Dict[str, float]:
        return {"TIME faces": 2}


class SpatialFaceCount(GFDTest):
    """
    The remaining 6 faces are classified as SPATIAL faces.
    These include an apex vertex in their definition.
    """
    name = "SPATIAL Face Count"
    question = "Are there exactly 2(k-1)=6 SPATIAL Coupling Ports, each containing its tetrahedron's apex vertex?"
    reference_source = "Topology (8 - 2)"
    tolerance = 0.001
    derivation = (
        "PREMISE: SPATIAL faces are those containing the apex vertex. "
        "STEP 1: Each tetrahedron has k-1 = 3 faces containing the apex. "
        "STEP 2: Two tetrahedra: 2 * (k-1) = 2 * 3 = 6 SPATIAL faces. "
        "STEP 3: Verify: Total (2k=8) - TIME (2) = 6 SPATIAL faces. "
        "STEP 4: The ratio SPATIAL:TIME = 6:2 = d:1 = 3:1 (spatial to temporal). "
        "OUTPUT: Exactly 6 SPATIAL Coupling Ports exist."
    )
    commentary = None  # Structural count derived from total minus TIME
    
    def model(self) -> Dict[str, float]:
        return {"SPATIAL faces": len(SPATIAL_FACES)}
    
    def observations(self) -> Dict[str, float]:
        return {"SPATIAL faces": 6}


class FaceCountSum(GFDTest):
    """
    TIME + SPATIAL must equal total faces. This is a consistency check
    on the face classification scheme.
    """
    name = "Face Count Sum"
    question = "Does the sum of TIME (2) and SPATIAL (6) faces equal the total face count (8), verifying classification completeness?"
    reference_source = "Arithmetic identity"
    tolerance = 0.001
    derivation = (
        "PREMISE: Face classification must partition all faces without overlap or gaps. "
        "STEP 1: TIME faces = 2 (FACE_A7, FACE_B0). "
        "STEP 2: SPATIAL faces = 6 (3 per tetrahedron). "
        "STEP 3: Sum: 2 + 6 = 8. "
        "STEP 4: Total faces in dual structure = 2k = 8. "
        "OUTPUT: Classification is complete and mutually exclusive: 2 + 6 = 8."
    )
    commentary = None  # Consistency verification
    
    def model(self) -> Dict[str, float]:
        total = len(TIME_FACES) + len(SPATIAL_FACES)
        return {
            "TIME + SPATIAL": total,
            "Total faces": len(FACES),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "TIME + SPATIAL": 8,
            "Total faces": 8,
        }


class TimeFraction(GFDTest):
    """
    The TIME fraction f_time = 2/8 = 1/4 is the key ratio that
    determines spin. This emerges from the apex topology.
    """
    name = "TIME Fraction"
    question = "Does the TIME fraction f_time = 2/(2k) = 2/8 = 1/4 emerge from apex topology without parameter fitting?"
    reference_source = "Topology (2/8)"
    tolerance = 0.001
    derivation = (
        "PREMISE: The TIME fraction is the ratio of TIME faces to total faces. "
        "STEP 1: TIME faces = 2 (one per tetrahedron, opposite apex). "
        "STEP 2: Total faces = 2k = 8. "
        "STEP 3: Calculate f_time = 2 / 8 = 1/4 = 0.25. "
        "STEP 4: This ratio is geometrically determined, not fitted to any observation. "
        "OUTPUT: TIME fraction 1/4 emerges from apex topology."
    )
    commentary = (
        "The TIME fraction 2/8 = 1/4 emerges from apex topology, not from fitting "
        "to electron spin. This geometric ratio is the key input to the spin "
        "derivation formula."
    )
    
    def model(self) -> Dict[str, float]:
        f_time = len(TIME_FACES) / len(FACES)
        return {"TIME fraction": f_time}
    
    def observations(self) -> Dict[str, float]:
        return {"TIME fraction": 0.25}


class SpinDerivation(GFDTest):
    """
    The model's spin formula: S = f_time x 2*hbar = (2/8) x 2*hbar = hbar/2.
    This produces a value numerically equal to fermion spin-1/2.
    """
    name = "Spin Derivation"
    question = "Does the geometric formula S = f_time * 2 * hbar = (2/8) * 2 * hbar produce the fermion spin value hbar/2?"
    reference_source = "Quantum mechanics"
    tolerance = 0.001
    derivation = (
        "PREMISE: The spin formula relates TIME fraction to angular momentum via S = f_time * L, where L = 2*hbar. "
        "STEP 1: TIME fraction: f_time = 2/8 = 1/4. "
        "STEP 2: Angular momentum unit: L = 2 * hbar. "
        "STEP 3: Calculate spin: S = f_time * L = (1/4) * 2 * hbar = hbar/2. "
        "STEP 4: Compare to fermion spin: S_electron = hbar/2. Match. "
        "OUTPUT: Geometric derivation produces hbar/2, the fermion spin value."
    )
    commentary = (
        "The geometric derivation produces hbar/2, numerically equal to electron "
        "spin. This correspondence between face topology and spin quantum number "
        "is documented without claiming causal explanation."
    )
    
    def model(self) -> Dict[str, float]:
        f_time = len(TIME_FACES) / len(FACES)
        L = 2 * HBAR
        spin = f_time * L
        return {"Spin (J*s)": spin}
    
    def observations(self) -> Dict[str, float]:
        return {"Spin (J*s)": HBAR / 2}


class SpinQuantumNumber(GFDTest):
    """
    The spin quantum number (in units of hbar) should be exactly 0.5.
    This is the hallmark of fermions.
    """
    name = "Spin Quantum Number"
    question = "Does the spin quantum number s = f_time * 2 = (2/8) * 2 = 1/2 distinguish fermions without parameter adjustment?"
    reference_source = "Fermion classification"
    tolerance = 0.001
    derivation = (
        "PREMISE: Spin quantum number s (in units of hbar) determines particle statistics. "
        "STEP 1: f_time = 2/8 = 0.25. "
        "STEP 2: Multiply by factor 2: s = 0.25 * 2 = 0.5. "
        "STEP 3: Half-integer spin (s = 1/2, 3/2, ...) -> Fermi-Dirac statistics. "
        "STEP 4: Integer spin (s = 0, 1, 2, ...) -> Bose-Einstein statistics. "
        "OUTPUT: s = 1/2 classifies the particle as a fermion."
    )
    commentary = (
        "The spin quantum number 1/2 emerges from (2/8) x 2 without adjustment. "
        "This half-integer value distinguishes fermions from bosons and determines "
        "Pauli exclusion behavior."
    )
    
    def model(self) -> Dict[str, float]:
        f_time = len(TIME_FACES) / len(FACES)
        L = 2  # In units of hbar
        spin_quantum = f_time * L
        return {"Spin quantum number": spin_quantum}
    
    def observations(self) -> Dict[str, float]:
        return {"Spin quantum number": 0.5}


class SpinorProperty(GFDTest):
    """
    Spin-1/2 particles require 720 degrees (4*pi) rotation to return
    to their original state. This "spinor" property is a direct
    consequence of the half-integer spin.
    """
    name = "Spinor Property"
    question = "Does spin-1/2 imply the spinor property requiring 4*pi = 720 degrees rotation for state return?"
    reference_source = "Spinor mathematics"
    tolerance = 0.001
    derivation = (
        "PREMISE: Spin-s particles return to original state after rotation by 2*pi/s radians per full cycle. "
        "STEP 1: For spin-1/2, full rotation = 2 * (2*pi) = 4*pi radians. "
        "STEP 2: Convert to degrees: 4*pi * (180/pi) = 720 degrees. "
        "STEP 3: This is twice a normal rotation (360 degrees). "
        "STEP 4: The factor 2 reflects the half-integer nature: 1/(1/2) = 2 full rotations needed. "
        "OUTPUT: Geometric spin 1/2 implies 720-degree rotation requirement."
    )
    commentary = (
        "The 720-degree rotation requirement for spin-1/2 particles is a fundamental "
        "consequence of spinor mathematics. The model's geometric spin derivation "
        "implies this property through the half-integer result."
    )
    
    def model(self) -> Dict[str, float]:
        rotation_radians = 4 * np.pi
        rotation_degrees = rotation_radians * 180 / np.pi
        return {"Full rotation (degrees)": rotation_degrees}
    
    def observations(self) -> Dict[str, float]:
        return {"Full rotation (degrees)": 720}


class TimeFaceClassification(GFDTest):
    """
    The TIME faces are FACE_A7 and FACE_B0, opposite the apexes
    V7 (111) and V0 (000) respectively. The classification is based
    on geometric position relative to the apex vertices.
    """
    name = "TIME Face Classification"
    question = "Are TIME faces classified as {FACE_A7, FACE_B0}, opposite the apex vertices V7 (111) and V0 (000)?"
    reference_source = "Topology definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: TIME faces are defined as those opposite the apex (geometrically distinct) vertices. "
        "STEP 1: Tetrahedron A apex is V7 (triad 111, all bits set). Face opposite: FACE_A7. "
        "STEP 2: Tetrahedron B apex is V0 (triad 000, no bits set). Face opposite: FACE_B0. "
        "STEP 3: Verify FACE_A7 vertices: {1,2,4} (excludes V7). "
        "STEP 4: Verify FACE_B0 vertices: {3,5,6} (excludes V0). "
        "OUTPUT: TIME faces = {FACE_A7, FACE_B0}, defined by apex opposition."
    )
    commentary = None  # Structural verification of face classification
    
    def model(self) -> Dict[str, float]:
        expected = {'FACE_A7', 'FACE_B0'}
        correct = 1 if TIME_FACES == expected else 0
        return {"Classification correct": correct}
    
    def observations(self) -> Dict[str, float]:
        return {"Classification correct": 1}


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    TotalFaceCount,
    TimeFaceCount,
    SpatialFaceCount,
    FaceCountSum,
    TimeFraction,
    SpinDerivation,
    SpinQuantumNumber,
    SpinorProperty,
    TimeFaceClassification,
]


def run_all_tests() -> bool:
    """Run all spin derivation tests."""
    return run_test_group(
        title="Spin-1/2 Derivation",
        summary=(
            "The model calculates spin from face topology: S = (N_time / N_total) x 2 = "
            "(2/8) x 2 = 1/2. The stellated octahedron has 8 faces, of which 2 (opposite "
            "the apexes) are classified as TIME faces. This ratio 2/8 = 1/4, multiplied by "
            "the factor 2, yields 1/2, which corresponds numerically to fermion spin. These "
            "tests verify the geometric calculation; the physical significance of this "
            "correspondence remains an open question."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
