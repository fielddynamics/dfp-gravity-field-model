"""
TIME Coupling Port Geometry
===========================

This module examines the geometric properties of TIME Coupling Ports
(FACE_A7 and FACE_B0). These faces have special structural properties:
- They are perpendicular to the V0-V7 apex axis
- Their normals point toward each other through the field origin
- Their vertices form 3 complementary pairs: (1,6), (2,5), (4,3)

The apex axis (V0 to V7) corresponds to a distinguished direction,
with TIME Coupling Ports spanning a plane perpendicular to it.

FACE_A7 = {1,2,4} (opposite V7)
FACE_B0 = {3,5,6} (opposite V0)
"""

import sys
import os
import math
import numpy as np
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

# =============================================================================
# CONSTANTS
# =============================================================================

# Vertex coordinates on unit cube
VERTICES = {
    0: (-1, -1, -1),  # 000
    1: (-1, -1,  1),  # 001
    2: (-1,  1, -1),  # 010
    3: (-1,  1,  1),  # 011
    4: ( 1, -1, -1),  # 100
    5: ( 1, -1,  1),  # 101
    6: ( 1,  1, -1),  # 110
    7: ( 1,  1,  1),  # 111
}

# Face definitions
FACES = {
    'FACE_A1': {2, 4, 7},
    'FACE_A2': {1, 4, 7},
    'FACE_A4': {1, 2, 7},
    'FACE_A7': {1, 2, 4},  # TIME face
    'FACE_B0': {3, 5, 6},  # TIME face
    'FACE_B3': {0, 5, 6},
    'FACE_B5': {0, 3, 6},
    'FACE_B6': {0, 3, 5},
}

TIME_FACES = {'FACE_A7', 'FACE_B0'}
SPATIAL_FACES = {'FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_B3', 'FACE_B5', 'FACE_B6'}

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}


def get_coords(v):
    return np.array(VERTICES[v], dtype=float)


def get_face_centroid(face_name):
    verts = FACES[face_name]
    coords = [get_coords(v) for v in verts]
    return np.mean(coords, axis=0)


def get_face_normal(face_name):
    verts = list(FACES[face_name])
    v0, v1, v2 = [get_coords(v) for v in verts]
    edge1 = v1 - v0
    edge2 = v2 - v0
    normal = np.cross(edge1, edge2)
    return normal / np.linalg.norm(normal)


def get_field_origin():
    all_coords = [get_coords(v) for v in range(8)]
    return np.mean(all_coords, axis=0)


# =============================================================================
# TESTS
# =============================================================================

class ApexAxisThroughOrigin(GFDTest):
    """
    The V0-V7 axis passes through the field origin.
    V0 and V7 are the apex vertices of Tet_B and Tet_A.
    """
    name = "Apex Axis Through Origin"
    question = "Does the V0-V7 apex axis pass exactly through the Field Origin, establishing a distinguished temporal direction?"
    reference_source = "Stellated octahedron geometry"
    tolerance = 1e-10
    derivation = (
        "PREMISE: The apex vertices V0 and V7 define a distinguished axis. "
        "STEP 1: V0 coordinates: (-1,-1,-1); V7 coordinates: (1,1,1) (unit cube). "
        "STEP 2: Midpoint of V0-V7: [(−1+1)/2, (−1+1)/2, (−1+1)/2] = (0,0,0). "
        "STEP 3: Field Origin = centroid of all 8 vertices = (0,0,0). "
        "STEP 4: Midpoint = Origin → axis passes through origin. "
        "OUTPUT: Distance from midpoint to origin = 0."
    )
    commentary = (
        "The apex axis V0-V7 passing through the Field Origin establishes a "
        "distinguished direction in the structure. This axis may correspond to "
        "the temporal dimension in the 3+1 interpretation."
    )
    
    def model(self) -> Dict[str, float]:
        v0 = get_coords(0)
        v7 = get_coords(7)
        midpoint = (v0 + v7) / 2
        origin = get_field_origin()
        distance = np.linalg.norm(midpoint - origin)
        return {
            "V0-V7 midpoint x": midpoint[0],
            "Origin x": origin[0],
            "Distance": distance,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "V0-V7 midpoint x": 0.0,
            "Origin x": 0.0,
            "Distance": 0.0,
        }


class TimeFacesPerpendicularToAxis(GFDTest):
    """
    TIME Coupling Ports are perpendicular to the V0-V7 axis.
    Their normals are parallel (or anti-parallel) to the apex axis.
    """
    name = "TIME Coupling Ports Perpendicular to Axis"
    question = "Are the TIME Coupling Port normals aligned (parallel or anti-parallel) with the V0-V7 apex axis, perpendicular to the face planes?"
    reference_source = "Geometric construction"
    tolerance = 0.01
    derivation = (
        "PREMISE: TIME faces are defined as those perpendicular to the apex axis. "
        "STEP 1: Apex axis direction: (V7 - V0)/|V7-V0| = (1,1,1)/√3. "
        "STEP 2: FACE_A7 = {1,2,4}: compute face normal via cross product of edges. "
        "STEP 3: FACE_B0 = {3,5,6}: compute face normal similarly. "
        "STEP 4: Calculate |dot(normal, apex_axis)| for each TIME face. "
        "STEP 5: Alignment = 1.0 indicates parallel/anti-parallel (perpendicular face). "
        "OUTPUT: FACE_A7 alignment = 1.0, FACE_B0 alignment = 1.0."
    )
    commentary = (
        "TIME Coupling Port normals aligning with the apex axis geometrically "
        "distinguishes them from SPATIAL Coupling Ports. This perpendicularity "
        "creates a natural TIME/SPACE decomposition in the structure."
    )
    
    def model(self) -> Dict[str, float]:
        v0 = get_coords(0)
        v7 = get_coords(7)
        apex_axis = (v7 - v0) / np.linalg.norm(v7 - v0)
        
        a7_normal = get_face_normal('FACE_A7')
        b0_normal = get_face_normal('FACE_B0')
        
        a7_alignment = abs(np.dot(a7_normal, apex_axis))
        b0_alignment = abs(np.dot(b0_normal, apex_axis))
        
        return {
            "FACE_A7 alignment": a7_alignment,
            "FACE_B0 alignment": b0_alignment,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "FACE_A7 alignment": 1.0,
            "FACE_B0 alignment": 1.0,
        }


class FieldOriginBetweenTimeFaces(GFDTest):
    """
    The field origin lies between the two TIME Coupling Port centroids.
    It lies on the line connecting them.
    """
    name = "Origin Between TIME Coupling Ports"
    question = "Does the Field Origin lie on the line segment connecting FACE_A7 and FACE_B0 centroids, positioned equidistant between them?"
    reference_source = "Geometric construction"
    tolerance = 0.01
    derivation = (
        "PREMISE: The origin should be the balance point between TIME faces. "
        "STEP 1: Calculate FACE_A7 centroid = mean of vertices {1,2,4}. "
        "STEP 2: Calculate FACE_B0 centroid = mean of vertices {3,5,6}. "
        "STEP 3: Parameterize line: P(t) = A7_centroid + t×(B0_centroid - A7_centroid). "
        "STEP 4: Find t where P(t) = Origin. "
        "STEP 5: If 0 < t < 1 and distance to line ≈ 0, origin is between faces. "
        "OUTPUT: Parameter t = 0.5, between faces = 1."
    )
    commentary = (
        "The Field Origin positioned equidistant between TIME Coupling Ports "
        "creates a neutral balance point. This central location is where all "
        "compression vectors cancel, producing Field Closure equilibrium."
    )
    
    def model(self) -> Dict[str, float]:
        a7_centroid = get_face_centroid('FACE_A7')
        b0_centroid = get_face_centroid('FACE_B0')
        origin = get_field_origin()
        
        # Parameterize: point = a7 + t*(b0 - a7)
        direction = b0_centroid - a7_centroid
        t = np.dot(origin - a7_centroid, direction) / np.dot(direction, direction)
        
        closest_point = a7_centroid + t * direction
        distance = np.linalg.norm(origin - closest_point)
        
        between = 1 if 0 < t < 1 else 0
        
        return {
            "Distance to line": distance,
            "Parameter t": t,
            "Between faces": between,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Distance to line": 0.0,
            "Parameter t": 0.5,
            "Between faces": 1,
        }


class SpatialFacesNotOnAxis(GFDTest):
    """
    SPATIAL face normals are NOT parallel to the apex axis.
    They point in various directions for inter-tile coupling.
    """
    name = "SPATIAL Faces Not on Axis"
    question = "Are SPATIAL Coupling Port normals angled away from the apex axis (alignment < 0.9), enabling spatial coupling in multiple directions?"
    reference_source = "Geometric construction"
    tolerance = 0.1
    derivation = (
        "PREMISE: SPATIAL faces should have normals NOT aligned with apex axis. "
        "STEP 1: Calculate normals for all 6 SPATIAL faces {A1, A2, A4, B3, B5, B6}. "
        "STEP 2: For each, compute |dot(normal, apex_axis)|. "
        "STEP 3: Alignment < 1.0 indicates non-parallel normal. "
        "STEP 4: If max alignment < 0.9, no SPATIAL face is nearly parallel to axis. "
        "OUTPUT: Max alignment < 0.9, none parallel = 1."
    )
    commentary = (
        "SPATIAL Coupling Port normals angled away from the apex axis enables "
        "spatial coupling in multiple directions. This contrasts with TIME "
        "Coupling Ports oriented along the distinguished axis."
    )
    
    def model(self) -> Dict[str, float]:
        v0 = get_coords(0)
        v7 = get_coords(7)
        apex_axis = (v7 - v0) / np.linalg.norm(v7 - v0)
        
        alignments = []
        for face_name in SPATIAL_FACES:
            normal = get_face_normal(face_name)
            alignment = abs(np.dot(normal, apex_axis))
            alignments.append(alignment)
        
        avg_alignment = np.mean(alignments)
        max_alignment = max(alignments)
        
        return {
            "Average alignment": avg_alignment,
            "Max alignment": max_alignment,
            "None parallel (max < 0.9)": 1 if max_alignment < 0.9 else 0,
        }


class TimeFacesShareNoVertices(GFDTest):
    """
    TIME Coupling Ports share no vertices - they reside in separate Field Chambers.
    """
    name = "TIME Coupling Ports Share No Vertices"
    question = "Do FACE_A7 and FACE_B0 share zero vertices, confirming they reside in separate (disjoint) Field Chambers?"
    reference_source = "Tetrahedra are disjoint"
    tolerance = 0.0
    derivation = (
        "PREMISE: Disjoint tetrahedra have disjoint vertex sets, hence disjoint faces. "
        "STEP 1: FACE_A7 = {1, 2, 4} (Tet A vertices). "
        "STEP 2: FACE_B0 = {3, 5, 6} (Tet B vertices). "
        "STEP 3: Intersection = {1,2,4} ∩ {3,5,6} = ∅ (empty set). "
        "STEP 4: |Intersection| = 0 vertices shared. "
        "OUTPUT: Shared vertices = 0."
    )
    commentary = None  # Structural consequence of disjoint tetrahedra
    
    def model(self) -> Dict[str, float]:
        a7_verts = FACES['FACE_A7']
        b0_verts = FACES['FACE_B0']
        shared = len(a7_verts & b0_verts)
        return {"Shared vertices": shared}
    
    def observations(self) -> Dict[str, float]:
        return {"Shared vertices": 0}


class TimeFaceVerticesComplementary(GFDTest):
    """
    TIME Coupling Port vertices form 3 complementary pairs: (1,6), (2,5), (4,3).
    Each vertex in FACE_A7 has its complement in FACE_B0.
    """
    name = "TIME Vertices Complementary"
    question = "Do the vertices of TIME Coupling Ports form 3 complementary pairs (v + v' = 7): (1,6), (2,5), (4,3)?"
    reference_source = "Complementary structure (n + 7-n = 7)"
    tolerance = 0.0
    derivation = (
        "PREMISE: Complementary vertices satisfy v + v' = 7 (bitwise complements). "
        "STEP 1: FACE_A7 = {1, 2, 4}; for each v, compute 7-v. "
        "STEP 2: 7-1=6, 7-2=5, 7-4=3 → complements are {6, 5, 3}. "
        "STEP 3: FACE_B0 = {3, 5, 6}. "
        "STEP 4: Check: {6,5,3} = {3,5,6} = FACE_B0 ✓. "
        "OUTPUT: Complementary pairs = 3."
    )
    commentary = (
        "TIME Coupling Port vertices forming 3 complementary pairs connects the "
        "temporal structure to the cross-chamber pairing mechanism. Each TIME "
        "vertex has a partner in the opposite Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        a7_verts = FACES['FACE_A7']
        b0_verts = FACES['FACE_B0']
        
        pairs_found = 0
        for v in a7_verts:
            complement = 7 - v
            if complement in b0_verts:
                pairs_found += 1
        
        return {
            "Complementary pairs": pairs_found,
            "Expected pairs": 3,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Complementary pairs": 3,
            "Expected pairs": 3,
        }


class TimeFaceEquidistantFromOrigin(GFDTest):
    """
    Both TIME Coupling Ports are equidistant from the field origin.
    """
    name = "TIME Coupling Ports Equidistant"
    question = "Are the centroids of FACE_A7 and FACE_B0 exactly equidistant from the Field Origin, reflecting bimetric symmetry?"
    reference_source = "Symmetric structure"
    tolerance = 1e-10
    derivation = (
        "PREMISE: Symmetric structure requires equal distances to both TIME faces. "
        "STEP 1: Calculate FACE_A7 centroid and its distance to origin. "
        "STEP 2: Calculate FACE_B0 centroid and its distance to origin. "
        "STEP 3: By symmetry of the stellated octahedron, distances should be equal. "
        "STEP 4: Compare: distance_A7 = distance_B0. "
        "OUTPUT: FACE_A7 distance = FACE_B0 distance."
    )
    commentary = (
        "Equal distances from Field Origin to both TIME Coupling Ports reflects "
        "the symmetric relationship between Tetrahedron A and Tetrahedron B. "
        "Neither Field Chamber is privileged geometrically."
    )
    
    def model(self) -> Dict[str, float]:
        origin = get_field_origin()
        a7_centroid = get_face_centroid('FACE_A7')
        b0_centroid = get_face_centroid('FACE_B0')
        
        dist_a7 = np.linalg.norm(a7_centroid - origin)
        dist_b0 = np.linalg.norm(b0_centroid - origin)
        
        return {
            "FACE_A7 distance": dist_a7,
            "FACE_B0 distance": dist_b0,
        }
    
    def observations(self) -> Dict[str, float]:
        # Both should be equal
        dist = np.linalg.norm(get_face_centroid('FACE_A7') - get_field_origin())
        return {
            "FACE_A7 distance": dist,
            "FACE_B0 distance": dist,
        }


class ApexVerticesAsPoles(GFDTest):
    """
    V0 (000) and V7 (111) may represent temporal poles.
    V0: all bits zero (past?), V7: all bits one (future?).
    """
    name = "Apex Vertices as Temporal Poles"
    question = "Are V0 (binary 000) and V7 (binary 111) complementary apex vertices that are excluded from TIME faces, suggesting temporal pole interpretation?"
    reference_source = "Interpretation"
    tolerance = 0.0
    derivation = (
        "PREMISE: Apex vertices may represent temporal limits in the structure. "
        "STEP 1: V0 = 0 = 000 in binary (all bits zero, minimum information). "
        "STEP 2: V7 = 7 = 111 in binary (all bits one, maximum information). "
        "STEP 3: V0 + V7 = 7 (complementary pair). "
        "STEP 4: V0 is NOT in FACE_B0 (B0's apex); V7 is NOT in FACE_A7 (A7's apex). "
        "STEP 5: Apexes are opposite their TIME faces, not vertices OF them. "
        "OUTPUT: V0 + V7 = 7, V0 not in TIME face = 1, V7 not in TIME face = 1."
    )
    commentary = (
        "V0 (000) and V7 (111) as extreme binary states may encode temporal "
        "endpoints or information bounds. Their exclusion from TIME faces yet "
        "role as apexes suggests they represent limits rather than accessible states."
    )
    
    def model(self) -> Dict[str, float]:
        # V0 and V7 are complementary
        complementary = 1 if (0 + 7 == 7) else 0
        
        # V0 has no 1-bits, V7 has all 1-bits
        v0_ones = bin(0).count('1')
        v7_ones = bin(7).count('1')
        
        # Neither is in a TIME face
        v0_not_in_time = 1 if 0 not in FACES['FACE_B0'] else 0
        v7_not_in_time = 1 if 7 not in FACES['FACE_A7'] else 0
        
        return {
            "V0 + V7 = 7": complementary,
            "V0 ones": v0_ones,
            "V7 ones": v7_ones,
            "V0 not in TIME face": v0_not_in_time,
            "V7 not in TIME face": v7_not_in_time,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "V0 + V7 = 7": 1,
            "V0 ones": 0,
            "V7 ones": 3,
            "V0 not in TIME face": 1,
            "V7 not in TIME face": 1,
        }


class CompressionCancelsAtOrigin(GFDTest):
    """
    Compression vectors from all 8 vertices cancel at the field origin.
    Net force at center is zero.
    """
    name = "Compression Cancels at Origin"
    question = "Do compression vectors from all 8 vertices toward the Field Origin sum to zero, creating a stable equilibrium point?"
    reference_source = "Force balance"
    tolerance = 1e-10
    derivation = (
        "PREMISE: Symmetric vertex arrangement should produce force cancellation at center. "
        "STEP 1: Field Origin = (0,0,0) (centroid of 8 cube vertices). "
        "STEP 2: Compression vector from vertex v = Origin - v (pointing toward center). "
        "STEP 3: Sum all 8 compression vectors: Σ(Origin - v_i) = 8×Origin - Σv_i. "
        "STEP 4: Σv_i = 0 (centroid property), so sum = 8×0 - 0 = 0. "
        "OUTPUT: Net compression magnitude = 0."
    )
    commentary = (
        "Compression vector cancellation at the Field Origin creates a stable "
        "equilibrium point. This balance is a geometric consequence of the "
        "symmetric vertex arrangement around the center."
    )
    
    def model(self) -> Dict[str, float]:
        origin = get_field_origin()
        total = np.array([0.0, 0.0, 0.0])
        
        for v in range(8):
            coord = get_coords(v)
            toward_origin = origin - coord
            total += toward_origin
        
        net_magnitude = np.linalg.norm(total)
        return {"Net compression magnitude": net_magnitude}
    
    def observations(self) -> Dict[str, float]:
        return {"Net compression magnitude": 0.0}


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    ApexAxisThroughOrigin,
    TimeFacesPerpendicularToAxis,
    FieldOriginBetweenTimeFaces,
    SpatialFacesNotOnAxis,
    TimeFacesShareNoVertices,
    TimeFaceVerticesComplementary,
    TimeFaceEquidistantFromOrigin,
    ApexVerticesAsPoles,
    CompressionCancelsAtOrigin,
]


def run_all_tests() -> bool:
    """Run all TIME Coupling Port geometry tests."""
    return run_test_group(
        title="TIME Coupling Port Geometry",
        summary=(
            "These tests examine the geometric properties of TIME Coupling Ports "
            "(FACE_A7 and FACE_B0) that distinguish them from SPATIAL Coupling Ports. "
            "They are perpendicular to the V0-V7 apex axis, their normals point toward "
            "each other through the field origin, and their vertices form 3 complementary "
            "pairs: (1,6), (2,5), (4,3). The apex axis corresponds to a distinguished "
            "direction. Compression vectors from all vertices cancel at the origin, "
            "creating the Field Closure balance point."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
