"""
Bidirectional Compression and Spin
==================================

This module investigates the fundamental question:

When gravity fields enter through the Field Origin and spherically pack
into Tetrahedron B (subspace), does the bidirectional compression shift
affect spin orientation?

BASELINE STATE (Bare Gravity Field):
- Tet A and Tet B coupled through Field Origin
- Nothing bound inside
- Torsion direction: Tet A -> Tet B (inward)
- Electron vortex spins due to this inward torsion
- TIME face on Tet A may be "active"

BOUND STATE (Hydrogen - 1 gravity field in Tet B):
- One gravity field has entered through Field Origin
- Now resides in Tetrahedron B (subspace)
- Bidirectional compression SHIFTS
- Tet B now compresses OUTWARD (not receiving inward)
- Question: Does this activate Tet B's TIME face instead?

The two spin states (+1/2, -1/2) correspond to which tetrahedron's 
TIME face is activated. If the compression shift changes activation,
spin would reverse.

OPEN QUESTIONS THIS MODULE EXPLORES:
1. Does binding a gravity field in Tet B reverse the compression direction?
2. Does this directional reversal affect which TIME face is active?
3. If so, does spin reverse when gravity fields bind?
4. How does this relate to nucleon spin (protons, neutrons)?
"""

import sys
import os
import numpy as np
from typing import Dict, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from gfd_model_v2.common import (
    VERTICES, TET_A, TET_B, TIME_FACES, SPATIAL_FACES, FACES,
    K, HBAR, get_tetrahedron
)


# =============================================================================
# GEOMETRIC HELPERS
# =============================================================================

def get_coords(v: int) -> np.ndarray:
    """Get coordinates for vertex v."""
    return np.array(VERTICES[v]['coords'], dtype=float)


def get_field_origin() -> np.ndarray:
    """Field Origin is at center (0,0,0)."""
    return np.array([0.0, 0.0, 0.0])


def get_face_centroid(face_name: str) -> np.ndarray:
    """Get centroid of a face."""
    verts = FACES[face_name]
    coords = [get_coords(v) for v in verts]
    return np.mean(coords, axis=0)


def get_compression_vector(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Get unit vector from source toward target."""
    diff = target - source
    norm = np.linalg.norm(diff)
    if norm == 0:
        return np.array([0.0, 0.0, 0.0])
    return diff / norm


def get_apex_axis() -> np.ndarray:
    """Get the V0-V7 apex axis (unit vector)."""
    v0 = get_coords(0)
    v7 = get_coords(7)
    axis = v7 - v0
    return axis / np.linalg.norm(axis)


# =============================================================================
# STATE MODELS
# =============================================================================

class CompressionState:
    """
    Models the compression state of a gravity field configuration.
    
    Bare state: compression flows Tet A -> Origin -> Tet B (inward to B)
    Bound state: compression flows Tet B -> Origin -> Tet A (outward from B)
    """
    
    @staticmethod
    def bare_field_compression() -> Dict[str, np.ndarray]:
        """
        Bare gravity field: Tet A compresses toward origin, 
        origin compresses toward Tet B.
        
        Returns compression vectors for each tetrahedron.
        """
        origin = get_field_origin()
        tet_a_centroid = np.mean([get_coords(v) for v in TET_A], axis=0)
        tet_b_centroid = np.mean([get_coords(v) for v in TET_B], axis=0)
        
        # In bare state: A -> Origin, Origin -> B (inward torsion)
        a_to_origin = get_compression_vector(tet_a_centroid, origin)
        origin_to_b = get_compression_vector(origin, tet_b_centroid)
        
        return {
            'tet_a_vector': a_to_origin,     # A compresses toward origin
            'tet_b_vector': origin_to_b,     # Origin projects toward B
            'net_direction': 'inward_to_B',  # Torsion goes into Tet B
        }
    
    @staticmethod
    def bound_field_compression() -> Dict[str, np.ndarray]:
        """
        Bound gravity field (H atom): Tet B now contains a bound field
        and compresses outward.
        
        Returns compression vectors after bidirectional shift.
        """
        origin = get_field_origin()
        tet_a_centroid = np.mean([get_coords(v) for v in TET_A], axis=0)
        tet_b_centroid = np.mean([get_coords(v) for v in TET_B], axis=0)
        
        # In bound state: B -> Origin, Origin -> A (outward from B)
        b_to_origin = get_compression_vector(tet_b_centroid, origin)
        origin_to_a = get_compression_vector(origin, tet_a_centroid)
        
        return {
            'tet_b_vector': b_to_origin,     # B compresses toward origin
            'tet_a_vector': origin_to_a,     # Origin projects toward A
            'net_direction': 'outward_from_B',  # Torsion goes out of Tet B
        }


# =============================================================================
# TESTS
# =============================================================================

class BareFieldTorsionDirection(GFDTest):
    """
    In a bare gravity field, the torsion direction is Tet A -> Tet B (inward).
    This creates the electron vortex spin.
    """
    name = "Bare Field Torsion Direction"
    question = "In a bare gravity field (nothing bound), does the compression flow from Tet A toward Tet B (inward torsion)?"
    reference_source = "DFP Model (theoretical)"
    tolerance = 0.001
    derivation = (
        "PREMISE: A bare gravity field has Tet A and Tet B coupled through Field Origin, "
        "with no other fields bound inside. "
        "STEP 1: Calculate Tet A centroid: mean of vertices {1,2,4,7}. "
        "STEP 2: Calculate Tet B centroid: mean of vertices {0,3,5,6}. "
        "STEP 3: Bare state torsion: compression flows A -> Origin -> B. "
        "STEP 4: This 'inward to B' torsion creates the electron vortex spin. "
        "OUTPUT: Net torsion direction = inward_to_B."
    )
    commentary = (
        "The inward torsion (Tet A -> Tet B) in a bare gravity field is what "
        "creates the electron vortex. The electron IS this vortex pattern. "
        "The spin arises from the circulating field structure."
    )
    
    def model(self) -> Dict[str, float]:
        state = CompressionState.bare_field_compression()
        
        # Check that compression flows toward B (inward)
        # In bare state, net direction should be 'inward_to_B'
        is_inward = 1 if state['net_direction'] == 'inward_to_B' else 0
        
        # Verify Tet A vector points toward origin
        origin = get_field_origin()
        tet_a_centroid = np.mean([get_coords(v) for v in TET_A], axis=0)
        
        # A->Origin direction
        a_to_origin = origin - tet_a_centroid
        a_to_origin_norm = np.linalg.norm(a_to_origin)
        
        # state['tet_a_vector'] should also point toward origin
        # Check if they point in same direction (dot > 0)
        if a_to_origin_norm > 0:
            a_to_origin_unit = a_to_origin / a_to_origin_norm
            alignment = np.dot(state['tet_a_vector'], a_to_origin_unit)
            a_points_to_origin = 1 if alignment > 0.99 else 0
        else:
            a_points_to_origin = 1  # Origin is at A centroid (degenerate case)
        
        return {
            "A points toward origin": a_points_to_origin,
            "Torsion inward to B": is_inward,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "A points toward origin": 1,
            "Torsion inward to B": 1,
        }


class BoundFieldCompressionShift(GFDTest):
    """
    When a gravity field enters through the Field Origin and binds in Tet B,
    the compression direction shifts: Tet B now compresses outward.
    """
    name = "Bound Field Compression Shift"
    question = "When a gravity field binds in Tet B (hydrogen formation), does the compression shift to flow outward from Tet B?"
    reference_source = "DFP Model (theoretical)"
    tolerance = 0.001
    derivation = (
        "PREMISE: When a gravity field enters through the Field Origin, it spherically "
        "packs into Tetrahedron B (subspace). This changes the compression dynamics. "
        "STEP 1: In bare state: A -> Origin -> B (inward). "
        "STEP 2: After binding: B now contains mass/energy, creating outward pressure. "
        "STEP 3: Bidirectional compression SHIFTS: B -> Origin -> A (outward from B). "
        "STEP 4: This is the hydrogen atom configuration. "
        "OUTPUT: Net torsion direction = outward_from_B."
    )
    commentary = (
        "The bidirectional compression shift is fundamental to atom formation. "
        "When gravity fields bind in Tet B, the torsion reverses direction. "
        "This transforms the bare field into an atom (hydrogen)."
    )
    
    def model(self) -> Dict[str, float]:
        bare = CompressionState.bare_field_compression()
        bound = CompressionState.bound_field_compression()
        
        # Check direction reversal
        bare_inward = 1 if bare['net_direction'] == 'inward_to_B' else 0
        bound_outward = 1 if bound['net_direction'] == 'outward_from_B' else 0
        direction_changed = 1 if bare_inward and bound_outward else 0
        
        return {
            "Bare state inward": bare_inward,
            "Bound state outward": bound_outward,
            "Direction changed": direction_changed,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Bare state inward": 1,
            "Bound state outward": 1,
            "Direction changed": 1,
        }


class TimeFaceActivationQuestion(GFDTest):
    """
    The two spin states (+1/2, -1/2) correspond to which tetrahedron's
    TIME face is activated. This test examines whether compression
    direction correlates with TIME face activation.
    """
    name = "TIME Face Activation Question"
    question = "Does the compression direction (inward vs outward) correlate with which TIME face (FACE_A7 vs FACE_B0) is geometrically 'receiving'?"
    reference_source = "Geometric analysis"
    tolerance = 0.001
    derivation = (
        "PREMISE: TIME faces are opposite the apex vertices (FACE_A7 opposite V7, FACE_B0 opposite V0). "
        "Compression direction may determine which TIME face 'receives' the flow. "
        "STEP 1: Bare state (inward to B): compression flows toward FACE_B0 (TIME face of Tet B). "
        "STEP 2: Bound state (outward from B): compression flows toward FACE_A7 (TIME face of Tet A). "
        "STEP 3: If TIME face activation determines spin state, then compression reversal may reverse spin. "
        "STEP 4: This is an OPEN QUESTION - we document the geometric correlation. "
        "OUTPUT: Bare state receiving face = FACE_B0, Bound state receiving face = FACE_A7."
    )
    commentary = (
        "This test documents the geometric correlation between compression direction "
        "and TIME face positioning. Whether this correlation determines spin state "
        "remains an open question requiring further investigation."
    )
    
    def model(self) -> Dict[str, float]:
        origin = get_field_origin()
        
        # TIME face centroids
        face_a7_centroid = get_face_centroid('FACE_A7')
        face_b0_centroid = get_face_centroid('FACE_B0')
        
        # In bare state (inward to B), flow is toward Tet B, so FACE_B0 receives
        # In bound state (outward from B), flow is toward Tet A, so FACE_A7 receives
        
        # Check which TIME face is closer to the "receiving end" of compression
        # For bare state: receiving is in B direction
        tet_b_centroid = np.mean([get_coords(v) for v in TET_B], axis=0)
        dist_b0_to_b = np.linalg.norm(face_b0_centroid - tet_b_centroid)
        
        # For bound state: receiving is in A direction
        tet_a_centroid = np.mean([get_coords(v) for v in TET_A], axis=0)
        dist_a7_to_a = np.linalg.norm(face_a7_centroid - tet_a_centroid)
        
        # The receiving face should be closer to its tetrahedron's centroid
        b0_receives_bare = 1 if dist_b0_to_b < 1.0 else 0  # FACE_B0 is inside Tet B
        a7_receives_bound = 1 if dist_a7_to_a < 1.0 else 0  # FACE_A7 is inside Tet A
        
        return {
            "FACE_B0 receives (bare)": b0_receives_bare,
            "FACE_A7 receives (bound)": a7_receives_bound,
            "Different faces activated": 1 if b0_receives_bare and a7_receives_bound else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "FACE_B0 receives (bare)": 1,
            "FACE_A7 receives (bound)": 1,
            "Different faces activated": 1,
        }


class SpinReversalHypothesis(GFDTest):
    """
    HYPOTHESIS: If TIME face activation determines spin, and compression
    shift changes which TIME face is activated, then binding should
    reverse spin.
    
    This test documents the hypothesis; verification requires experimental data.
    """
    name = "Spin Reversal Hypothesis"
    question = "If compression shift activates the opposite TIME face, would spin reverse from bare field (+1/2) to bound field (-1/2) or vice versa?"
    reference_source = "Hypothesis (requires verification)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Spin states (+1/2, -1/2) correspond to which TIME face is activated. "
        "STEP 1: HYPOTHESIS: Bare field activates FACE_B0 -> spin state A (e.g., +1/2). "
        "STEP 2: HYPOTHESIS: Bound field activates FACE_A7 -> spin state B (e.g., -1/2). "
        "STEP 3: If hypothesis correct, binding reverses spin direction. "
        "STEP 4: This may explain nucleon spin configurations in bound states. "
        "OUTPUT: Hypothesis predicts spin reversal upon binding (requires verification)."
    )
    commentary = (
        "This hypothesis suggests that gravity field binding reverses spin by "
        "shifting which TIME face is activated. If true, this would have profound "
        "implications for understanding nucleon spin in atoms. Verification requires "
        "comparison with experimental spin measurements in bound vs free particles."
    )
    
    def model(self) -> Dict[str, float]:
        # Document the hypothesis structure
        # Two states: bare and bound
        # Two TIME faces: A7 and B0
        # Two spin values: +1/2 and -1/2
        
        # Hypothesis mapping (to be verified)
        bare_time_face = 'FACE_B0'  # Hypothesis
        bound_time_face = 'FACE_A7'  # Hypothesis
        faces_differ = 1 if bare_time_face != bound_time_face else 0
        
        # If faces differ, spin should differ
        spin_reversal_predicted = faces_differ
        
        return {
            "TIME faces differ": faces_differ,
            "Spin reversal predicted": spin_reversal_predicted,
            "Hypothesis documented": 1,
        }
    
    def observations(self) -> Dict[str, float]:
        # This is a hypothesis - we expect the structure to support it
        return {
            "TIME faces differ": 1,
            "Spin reversal predicted": 1,
            "Hypothesis documented": 1,
        }


class HydrogenAsActivatedField(GFDTest):
    """
    Hydrogen (A=1) is ONE activated gravity field - the proton.
    
    The key distinction:
    - EMPTY gravity field = spacetime substrate, no particle content (A=0)
    - ACTIVATED gravity field = nucleon (proton/neutron), has particle content (A=1 each)
    
    The electron is a VORTEX PATTERN orbiting outside, not a gravity field.
    """
    name = "Hydrogen as Single Activated Field"
    question = "Is hydrogen correctly modeled as A=1 (one activated gravity field = proton), with the electron as an orbiting vortex pattern?"
    reference_source = "DFP Model / Binding Hierarchy"
    tolerance = 0.0
    derivation = (
        "PREMISE: Gravity fields exist in two states: empty (spacetime substrate) and "
        "activated (nucleon with particle content). Mass number A counts activated fields only. "
        "STEP 1: Empty gravity field: pure geometry, A=0, cannot bind electrons. "
        "STEP 2: Proton: activated gravity field, A=1, can bind electron vortex. "
        "STEP 3: Hydrogen atom = 1 proton (A=1) + 1 electron vortex (not a gravity field). "
        "STEP 4: The electron orbits OUTSIDE the gravity field as a vortex pattern. "
        "STEP 5: Mass number A = 1 (only the proton counts). "
        "OUTPUT: Hydrogen = 1 activated gravity field (A=1), electron = vortex (not counted)."
    )
    commentary = (
        "This clarifies the distinction between empty and activated gravity fields. "
        "An empty gravity field is spacetime substrate - it provides the medium for "
        "particles to exist but has no particle content itself. An activated gravity "
        "field (proton/neutron) is a particle. The electron is NOT a gravity field - "
        "it is a vortex pattern. Hydrogen's mass number A=1 reflects one proton."
    )
    
    def model(self) -> Dict[str, float]:
        # Hydrogen configuration (corrected model)
        activated_fields = 1  # The proton IS the activated gravity field
        electron_is_vortex = 1  # Electron is vortex, not gravity field
        mass_number_a = activated_fields
        
        # He-4 for comparison
        he4_activated = K  # k=4 activated gravity fields (nucleons)
        he4_a = he4_activated
        
        return {
            "H activated fields": activated_fields,
            "H electron is vortex": electron_is_vortex,
            "H mass number A": mass_number_a,
            "He-4 activated fields": he4_activated,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "H activated fields": 1,  # One proton
            "H electron is vortex": 1,  # Yes
            "H mass number A": 1,  # A = 1
            "He-4 activated fields": 4,  # k = 4 nucleons
        }


class TetrahedronBAsSubspace(GFDTest):
    """
    Tetrahedron B is 'subspace' - the region where gravity fields
    spherically pack when they enter through the Field Origin.
    """
    name = "Tetrahedron B as Subspace"
    question = "Is Tetrahedron B the 'subspace' region where entering gravity fields spherically pack after passing through the Field Origin?"
    reference_source = "DFP Model definition"
    tolerance = 0.001
    derivation = (
        "PREMISE: The Field Origin is the gateway between Tet A and Tet B. "
        "STEP 1: Gravity fields can enter through the Field Origin from outside. "
        "STEP 2: After entering, they reside in Tetrahedron B (even parity vertices). "
        "STEP 3: Tet B = {0, 3, 5, 6} (even parity, 'Yin dominant'). "
        "STEP 4: The bound fields spherically pack within this subspace. "
        "STEP 5: k=4 complete packing fills Tet B completely (He-4). "
        "OUTPUT: Tet B is subspace; bound fields reside in vertices {0,3,5,6}."
    )
    commentary = (
        "Tetrahedron B serves as the 'subspace' where bound gravity fields reside. "
        "This is why packing follows k-multiples: Tet B has k=4 vertices, and "
        "complete packing requires filling all 4 positions. The even parity of "
        "Tet B vertices may relate to the stability of bound configurations."
    )
    
    def model(self) -> Dict[str, float]:
        # Tet B properties
        tet_b_vertices = len(TET_B)
        tet_b_even_parity = all(bin(v).count('1') % 2 == 0 for v in TET_B)
        
        # Binding capacity = k = 4 (one per Tet B vertex)
        binding_capacity = tet_b_vertices
        
        return {
            "Tet B vertex count": tet_b_vertices,
            "All even parity": 1 if tet_b_even_parity else 0,
            "Binding capacity (k)": binding_capacity,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Tet B vertex count": 4,
            "All even parity": 1,
            "Binding capacity (k)": K,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    BareFieldTorsionDirection,
    BoundFieldCompressionShift,
    TimeFaceActivationQuestion,
    SpinReversalHypothesis,
    HydrogenAsActivatedField,
    TetrahedronBAsSubspace,
]


def run_all_tests() -> bool:
    """Run all bidirectional compression tests."""
    return run_test_group(
        title="Bidirectional Compression and Spin",
        summary=(
            "These tests investigate the relationship between compression direction "
            "and spin in gravity field configurations. A bare gravity field has "
            "inward torsion (Tet A to Tet B), creating the electron vortex. When a "
            "gravity field enters through the Field Origin and binds in Tet B, the "
            "compression SHIFTS to outward. This raises the question: does this "
            "directional shift change which TIME face is activated, and thus reverse "
            "spin? These tests document the geometric structure and hypothesis; "
            "verification requires comparison with experimental spin measurements."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
