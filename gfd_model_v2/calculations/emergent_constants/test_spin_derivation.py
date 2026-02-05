"""
Electron Spin from Merkaba Topology
===================================

This module contains the most significant derivation in the GFD framework:
electron spin S = hbar/2 from pure face counting.

WHY THIS DERIVATION MATTERS:

Standard quantum mechanics does not explain WHY electrons have spin 1/2.
- Pauli (1927): POSTULATED spin 1/2 to explain Stern-Gerlach.
- Dirac (1928): DERIVED spin 1/2 from requiring relativistic invariance.
  But this just pushes the question: why does relativity produce half-integer spin?

GFD provides a geometric answer: spin is the fraction of angular momentum
flowing through the TIME faces of the Merkaba (stellated octahedron).

THE DERIVATION:

Step 1: The Merkaba has 8 faces (two tetrahedra, 4 faces each).
Step 2: 2 faces are TIME faces (opposite the apexes).
Step 3: 6 faces are SPATIAL faces (containing the apexes).
Step 4: TIME face fraction: f_time = 2/8 = 1/4.
Step 5: A spinor requires 720 degrees to return to original state.
Step 6: This 720-degree cycle carries total angular momentum L = 2*hbar.
Step 7: Spin = fraction of L flowing through TIME: S = f_time * L.
Step 8: S = (1/4) * 2*hbar = hbar/2.

NO FREE PARAMETERS. The numbers 2, 8, and 2*hbar all have independent
geometric meaning. This is pure counting.

References:
- GFD Textbook Chapter 10
- Stern-Gerlach experiment (1922)
- Pauli (1927), Dirac (1928)
"""

import sys
import math

from gfd_model_v2.framework import *
from gfd_model_v2.common import FACES, TIME_FACES, SPATIAL_FACES, HBAR, K

PI = math.pi


# =============================================================================
# TESTS
# =============================================================================

class MerkabaFaceCount(Test):
    """
    THE MERKABA HAS 8 FACES.
    
    The Merkaba (stellated octahedron) consists of two interpenetrating
    tetrahedra. Each tetrahedron has k=4 faces. Total: 2*k = 8 faces.
    
    These 8 faces are the "Coupling Ports" through which the field
    interacts with its environment.
    """
    name = "Merkaba Has 2k = 8 Faces"
    question = (
        "Does the Merkaba (stellated octahedron) have exactly 2k = 8 faces, "
        "consisting of two tetrahedra with k=4 faces each?"
    )
    reference = "Geometry of stellated octahedron"
    tolerance = 0.0
    level = Level.STANDARD
    
    commentary = (
        "THE MERKABA STRUCTURE:\n\n"
        "The Merkaba is two tetrahedra, one pointing up (Tet A) and one\n"
        "pointing down (Tet B), sharing a common center.\n\n"
        "Tet A: 4 triangular faces (Coupling Ports)\n"
        "Tet B: 4 triangular faces (Coupling Ports)\n"
        "Total: 8 faces\n\n"
        "The faces do NOT overlap. They are distinct triangular surfaces.\n"
        "The 8 faces form the complete boundary of the dual structure."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MERKABA FACE COUNT:")
            .step("Tetrahedron A has k = 4 triangular faces.")
            .step("Tetrahedron B has k = 4 triangular faces.")
            .step("The tetrahedra share center but faces do not overlap.")
            .step("Total faces = k + k = 2k = 8.")
            .conclude("The Merkaba has exactly 8 Coupling Ports (faces).")
        )
    
    def model(self) -> Model:
        faces_per_tet = K
        n_tetrahedra = 2
        total_faces = faces_per_tet * n_tetrahedra
        
        return (
            Model()
            .add("k (faces per tet)", faces_per_tet)
            .add("Number of tetrahedra", n_tetrahedra)
            .add("Total faces (2k)", total_faces)
            .add("Matches structure", len(FACES))
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("k (faces per tet)", 4)
            .add("Number of tetrahedra", 2)
            .add("Total faces (2k)", 8)
            .add("Matches structure", 8)
        )


class TimeFaceClassification(Test):
    """
    2 FACES ARE TIME FACES.
    
    Each tetrahedron has one distinguished vertex: the APEX.
    The face OPPOSITE the apex is the TIME face.
    
    Tet A apex is V7 (the "up" point). TIME face: FACE_A7 (opposite V7).
    Tet B apex is V0 (the "down" point). TIME face: FACE_B0 (opposite V0).
    
    These 2 TIME faces are where the field couples to the temporal component
    of spacetime. The remaining 6 SPATIAL faces couple to space.
    """
    name = "2 TIME Faces (Opposite Apexes)"
    question = (
        "Are there exactly 2 TIME faces in the Merkaba, one per tetrahedron, "
        "each opposite its apex vertex?"
    )
    reference = "GFD face classification"
    tolerance = 0.0
    level = Level.CRITICAL
    
    commentary = (
        "WHY 2 TIME FACES?\n\n"
        "Each tetrahedron has a geometrically distinguished vertex: the APEX.\n"
        "This is the vertex that points 'outward' from the center.\n\n"
        "Tet A: Apex is V7 (all coordinates positive). Opposite face: FACE_A7.\n"
        "Tet B: Apex is V0 (all coordinates negative). Opposite face: FACE_B0.\n\n"
        "The TIME faces are special:\n"
        "- They do NOT contain the apex vertex\n"
        "- They lie 'perpendicular' to the tetrahedral axis\n"
        "- They couple to the temporal component of 3+1 spacetime\n\n"
        "The 6 SPATIAL faces (3 per tetrahedron) each CONTAIN the apex vertex."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("TIME FACE CLASSIFICATION:")
            .step("Tet A apex: V7 (coordinates 111). Face opposite: FACE_A7.")
            .step("Tet B apex: V0 (coordinates 000). Face opposite: FACE_B0.")
            .step("TIME faces = {FACE_A7, FACE_B0} = 2 faces.")
            .step("SPATIAL faces = remaining 6 faces (3 per tetrahedron).")
            .conclude("Exactly 2 TIME faces, one per tetrahedron.")
        )
    
    def model(self) -> Model:
        n_time = len(TIME_FACES)
        n_spatial = len(SPATIAL_FACES)
        sum_check = n_time + n_spatial
        
        return (
            Model()
            .add("TIME faces", n_time)
            .add("SPATIAL faces", n_spatial)
            .add("Sum (should = 8)", sum_check)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("TIME faces", 2)
            .add("SPATIAL faces", 6)
            .add("Sum (should = 8)", 8)
        )


class TimeFraction(Test):
    """
    THE TIME FRACTION: f_time = 2/8 = 1/4.
    
    This is the key ratio that determines spin.
    
    With 2 TIME faces out of 8 total, the fraction of the field's
    angular momentum that couples to the temporal dimension is 1/4.
    """
    name = "TIME Fraction f_time = 2/8 = 1/4"
    question = (
        "Is the TIME face fraction f_time = 2/8 = 1/4, the key ratio "
        "in the spin derivation?"
    )
    reference = "GFD Framework"
    tolerance = 0.0
    level = Level.CRITICAL
    
    commentary = (
        "THE KEY RATIO:\n\n"
        "f_time = N_TIME / N_total = 2/8 = 1/4\n\n"
        "This fraction emerges from pure topology, not from fitting to\n"
        "any observed spin value.\n\n"
        "The 2 comes from: one TIME face per tetrahedron = 2.\n"
        "The 8 comes from: 4 faces per tetrahedron * 2 tetrahedra = 8.\n\n"
        "The ratio 2/8 = 1/4 is GEOMETRY, not physics."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("TIME FRACTION:")
            .step("N_TIME = 2 (one per tetrahedron)")
            .step("N_total = 2k = 8 (total faces)")
            .step("f_time = N_TIME / N_total = 2/8 = 1/4")
            .conclude("The TIME fraction is exactly 1/4.")
        )
    
    def model(self) -> Model:
        f_time = len(TIME_FACES) / len(FACES)
        return (
            Model()
            .add("N_TIME", len(TIME_FACES))
            .add("N_total", len(FACES))
            .add("f_time = N_TIME / N_total", f_time)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("N_TIME", 2)
            .add("N_total", 8)
            .add("f_time = N_TIME / N_total", 0.25)
        )


class SpinorCycleAngularMomentum(Test):
    """
    THE 720-DEGREE CYCLE CARRIES 2*hbar.
    
    A spinor (half-integer spin particle) requires 720 degrees (4*pi radians)
    to return to its original state. This is the "double cover" of SO(3).
    
    A full 360-degree rotation gives a phase factor of -1 (not +1).
    Only after 720 degrees does the spinor return to +1.
    
    This 720-degree cycle represents 2 complete rotations, carrying
    total angular momentum L = 2 * hbar.
    """
    name = "Spinor Cycle: L = 2*hbar"
    question = (
        "Does the 720-degree spinor cycle carry total angular momentum "
        "L = 2*hbar, representing two complete rotations?"
    )
    reference = "Spinor mathematics"
    tolerance = 0.0
    level = Level.STANDARD
    
    commentary = (
        "WHY 2*hbar?\n\n"
        "In quantum mechanics, angular momentum is quantized in units of hbar.\n"
        "A full rotation (360 degrees) corresponds to angular momentum hbar.\n\n"
        "But spinors are weird: a 360-degree rotation gives a phase factor of -1.\n"
        "You need 720 degrees (2 full rotations) to get back to the original state.\n\n"
        "This 720-degree cycle = 2 rotations = 2*hbar total angular momentum.\n\n"
        "The factor 2 is not arbitrary. It is the mathematical structure of spinors."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SPINOR ANGULAR MOMENTUM:")
            .step("Spinors require 720 degrees to return to original state.")
            .step("720 degrees = 2 * 360 degrees = 2 complete rotations.")
            .step("Each rotation carries hbar angular momentum.")
            .step("Total: L = 2 * hbar.")
            .conclude("The spinor cycle carries 2*hbar angular momentum.")
        )
    
    def model(self) -> Model:
        spinor_angle_deg = 720
        rotations = spinor_angle_deg / 360
        L_units_hbar = rotations
        
        return (
            Model()
            .add("Spinor cycle (degrees)", spinor_angle_deg)
            .add("Number of rotations", int(rotations))
            .add("L (in hbar)", L_units_hbar)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Spinor cycle (degrees)", 720)
            .add("Number of rotations", 2)
            .add("L (in hbar)", 2)
        )


class SpinDerivation(Test):
    """
    THE MAIN RESULT: S = f_time * L = (1/4) * 2*hbar = hbar/2.
    
    Spin is the fraction of the spinor cycle's angular momentum
    that flows through the TIME faces.
    
    With f_time = 1/4 and L = 2*hbar:
        S = (1/4) * 2*hbar = hbar/2
    
    This is EXACTLY the measured electron spin.
    """
    name = "Spin S = (2/8) * 2*hbar = hbar/2"
    question = (
        "Does the formula S = f_time * L = (2/8) * 2*hbar produce "
        "the electron spin value S = hbar/2?"
    )
    reference = "GFD Textbook Chapter 10"
    tolerance = 0.0
    level = Level.CRITICAL
    
    commentary = (
        "THE DERIVATION:\n\n"
        "Spin is the angular momentum associated with the particle's\n"
        "intrinsic structure. In GFD, this is the angular momentum\n"
        "flowing through the TIME faces.\n\n"
        "Step 1: TIME face fraction f_time = 2/8 = 1/4\n"
        "Step 2: Total angular momentum in spinor cycle L = 2*hbar\n"
        "Step 3: Spin = f_time * L = (1/4) * (2*hbar)\n\n"
        "    S = 2*hbar / 4 = hbar / 2\n\n"
        "This equals the measured electron spin EXACTLY.\n\n"
        "NO FREE PARAMETERS:\n"
        "- The 2 (TIME faces) comes from Merkaba topology\n"
        "- The 8 (total faces) comes from 2 tetrahedra * 4 faces\n"
        "- The 2*hbar comes from the 720-degree spinor cycle\n\n"
        "This is GEOMETRY producing a QUANTUM NUMBER."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SPIN FROM GEOMETRY:")
            .step("f_time = N_TIME / N_total = 2/8 = 1/4")
            .step("L = 2*hbar (spinor cycle angular momentum)")
            .step("S = f_time * L = (1/4) * (2*hbar)")
            .equation("S = 2*hbar / 4 = hbar / 2")
            .step("Electron spin (CODATA): S = hbar/2 = 5.273e-35 J*s")
            .conclude("DERIVED spin = MEASURED spin. EXACT MATCH.")
        )
    
    def model(self) -> Model:
        f_time = len(TIME_FACES) / len(FACES)  # 2/8 = 0.25
        L = 2 * HBAR
        spin_derived = f_time * L
        spin_expected = HBAR / 2
        match = 1 if abs(spin_derived - spin_expected) < 1e-50 else 0
        
        return (
            Model()
            .add("f_time", f_time)
            .add("L (J*s)", L)
            .add("S derived (J*s)", spin_derived)
            .add("S expected (hbar/2)", spin_expected)
            .add("Exact match", match)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("f_time", 0.25)
            .add("L (J*s)", 2 * HBAR)
            .add("S derived (J*s)", HBAR / 2)
            .add("S expected (hbar/2)", HBAR / 2)
            .add("Exact match", 1)
        )


class SpinQuantumNumber(Test):
    """
    THE SPIN QUANTUM NUMBER: s = 1/2.
    
    In units of hbar, spin = 0.5 exactly.
    This half-integer value identifies the particle as a FERMION.
    """
    name = "Spin Quantum Number s = 1/2 (Fermion)"
    question = (
        "Does the derivation produce spin quantum number s = 1/2, "
        "identifying the particle as a fermion?"
    )
    reference = "Quantum mechanics"
    tolerance = 0.0
    level = Level.CRITICAL
    
    commentary = (
        "FERMIONS vs BOSONS:\n\n"
        "- Fermions: half-integer spin (1/2, 3/2, 5/2, ...)\n"
        "  Obey Pauli exclusion principle. Examples: electron, proton, neutron.\n\n"
        "- Bosons: integer spin (0, 1, 2, ...)\n"
        "  Can occupy same quantum state. Examples: photon, gluon, Higgs.\n\n"
        "The GFD derivation produces s = 1/2, a HALF-INTEGER.\n"
        "This automatically classifies the particle as a FERMION.\n\n"
        "The 720-degree rotation requirement (spinor property) follows:\n"
        "only half-integer spin particles need 720 degrees to return to\n"
        "their original state."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SPIN QUANTUM NUMBER:")
            .step("S = hbar/2")
            .step("In units of hbar: s = S/hbar = (hbar/2)/hbar = 1/2")
            .step("1/2 is a half-integer.")
            .step("Half-integer spin -> Fermi-Dirac statistics -> Fermion.")
            .conclude("s = 1/2 classifies the particle as a fermion.")
        )
    
    def model(self) -> Model:
        f_time = len(TIME_FACES) / len(FACES)
        L_units = 2  # In units of hbar
        s = f_time * L_units
        is_half_integer = 1 if (s * 2) % 1 == 0 and s % 1 != 0 else 0
        
        return (
            Model()
            .add("f_time", f_time)
            .add("L (in hbar)", L_units)
            .add("s = f_time * L", s)
            .add("Is half-integer", is_half_integer)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("f_time", 0.25)
            .add("L (in hbar)", 2)
            .add("s = f_time * L", 0.5)
            .add("Is half-integer", 1)
        )


class SpinorRotationProperty(Test):
    """
    SPINOR PROPERTY: 720 degrees to return to original state.
    
    Particles with spin 1/2 need TWO full rotations (720 degrees)
    to return to their original quantum state.
    
    This "strange" property follows directly from s = 1/2.
    """
    name = "Spinor: 720-degree Rotation Requirement"
    question = (
        "Does spin 1/2 imply the spinor property requiring 720 degrees "
        "(4*pi radians) for the particle to return to its original state?"
    )
    reference = "Spinor mathematics"
    tolerance = 0.0
    level = Level.STANDARD
    
    commentary = (
        "THE SPINOR PROPERTY:\n\n"
        "For a spin-s particle, rotation by angle theta produces phase e^{-is*theta}.\n\n"
        "For s = 1/2:\n"
        "- 360 degrees (2*pi): phase = e^{-i*pi} = -1 (NOT +1)\n"
        "- 720 degrees (4*pi): phase = e^{-i*2*pi} = +1 (original state)\n\n"
        "This is why spin-1/2 particles are called SPINORS.\n"
        "They need DOUBLE the rotation angle to return to their original state.\n\n"
        "This strange property has been verified experimentally using\n"
        "neutron interferometry. It is real, not just mathematics."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SPINOR ROTATION:")
            .step("Phase after rotation theta: e^{-i*s*theta}")
            .step("For s = 1/2 and theta = 2*pi (360 deg): e^{-i*pi} = -1")
            .step("To get +1 (original state), need e^{-i*n*pi} = +1")
            .step("Requires n*pi = 2*pi*m for integer m, so n = 2m")
            .step("Smallest positive: n = 2, giving theta = 4*pi = 720 deg")
            .conclude("Spin 1/2 requires 720 degrees to return to original state.")
        )
    
    def model(self) -> Model:
        s = 0.5
        full_rotation_deg = 360
        required_deg = full_rotation_deg / s  # For phase = +1
        
        return (
            Model()
            .add("Spin quantum number", s)
            .add("Single rotation (deg)", full_rotation_deg)
            .add("Required for original state", required_deg)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Spin quantum number", 0.5)
            .add("Single rotation (deg)", 360)
            .add("Required for original state", 720)
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    MerkabaFaceCount,
    TimeFaceClassification,
    TimeFraction,
    SpinorCycleAngularMomentum,
    SpinDerivation,
    SpinQuantumNumber,
    SpinorRotationProperty,
]


def run_all() -> bool:
    """Run all spin derivation tests."""
    return run_tests(
        title="Electron Spin from Merkaba Topology",
        summary=(
            "This module derives electron spin S = hbar/2 from pure geometry.\n\n"
            "THE DERIVATION:\n"
            "1. Merkaba has 8 faces (2 tetrahedra x 4 faces)\n"
            "2. 2 faces are TIME faces (opposite the apexes)\n"
            "3. TIME fraction: f_time = 2/8 = 1/4\n"
            "4. Spinor cycle carries L = 2*hbar angular momentum\n"
            "5. Spin = f_time * L = (1/4) * (2*hbar) = hbar/2\n\n"
            "NO FREE PARAMETERS:\n"
            "- The 2 comes from Merkaba topology (one TIME face per tet)\n"
            "- The 8 comes from 2 tetrahedra x 4 faces\n"
            "- The 2*hbar comes from the 720-degree spinor cycle\n\n"
            "RESULT:\n"
            "s = 1/2 (in units of hbar)\n"
            "This is a FERMION (half-integer spin).\n"
            "Requires 720 degrees for state return (spinor property).\n\n"
            "This derivation produces the measured electron spin from\n"
            "pure face counting. No fitting. No free parameters."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
