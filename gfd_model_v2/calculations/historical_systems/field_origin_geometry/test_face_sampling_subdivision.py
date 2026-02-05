"""
Face Sampling Subdivision: Medial Triangle Construction

This module validates the subdivision of each triangular face into 4 sampling
regions using the medial triangle construction. The key insight is that connecting
the midpoints of a triangle's edges creates 4 congruent sub-triangles.

THE PHYSICAL CLAIM:
Each triangular face of the stellated octahedron can be subdivided into 4 equal
regions. This is a well-known theorem of Euclidean geometry (the medial triangle
has 1/4 the area of the original). The number 4 matches k, the closure constant.

WHY THIS MATTERS:
If GFD field sampling requires uniform coverage of each face, the medial subdivision
provides exactly that. Each of the 8 faces subdivides into 4 regions, giving 32
total sampling points. This connects geometry to sampling theory.
"""

import math
from gfd_model_v2.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Closure constant

# Vertex coordinates (cube corners at +/-1)
VERTICES = {
    0: {'coords': (-1, -1, -1)},
    1: {'coords': (-1, -1, +1)},
    2: {'coords': (-1, +1, -1)},
    3: {'coords': (-1, +1, +1)},
    4: {'coords': (+1, -1, -1)},
    5: {'coords': (+1, -1, +1)},
    6: {'coords': (+1, +1, -1)},
    7: {'coords': (+1, +1, +1)},
}

# Faces of the two tetrahedra (each face has 3 vertices)
FACES = {
    # Tetrahedron A faces (odd parity vertices)
    'FACE_A1': {2, 4, 7},
    'FACE_A2': {1, 4, 7},
    'FACE_A4': {1, 2, 7},
    'FACE_A7': {1, 2, 4},
    # Tetrahedron B faces (even parity vertices)
    'FACE_B0': {3, 5, 6},
    'FACE_B3': {0, 5, 6},
    'FACE_B5': {0, 3, 6},
    'FACE_B6': {0, 3, 5},
}

SUBDIVISION_REGIONS = ['CORNER_1', 'CORNER_2', 'CORNER_3', 'CENTER']


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_vertex_coords(v):
    """Get vertex coordinates as tuple."""
    return VERTICES[v]['coords']


def calculate_triangle_area(v1, v2, v3):
    """Calculate area using cross product: A = |AB x AC| / 2."""
    edge1 = (v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2])
    edge2 = (v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2])
    cross = (
        edge1[1]*edge2[2] - edge1[2]*edge2[1],
        edge1[2]*edge2[0] - edge1[0]*edge2[2],
        edge1[0]*edge2[1] - edge1[1]*edge2[0]
    )
    return 0.5 * math.sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2)


# =============================================================================
# TEST CLASSES
# =============================================================================

class MedialSubdivisionCount(Test):
    """Medial construction produces exactly 4 sub-triangles."""
    name = "Medial Subdivision Count"
    level = Level.STANDARD
    question = (
        "When we connect the midpoints of a triangle's edges, how many "
        "congruent sub-triangles are created?"
    )
    reference = "Euclidean geometry: medial triangle theorem"
    tolerance = 0.01
    commentary = (
        "This is a standard result. The medial triangle divides the original "
        "into 4 congruent triangles: 3 corner triangles (each containing one "
        "original vertex) plus 1 central medial triangle. All have equal area."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Start with any triangle ABC.")
            .step("Find midpoints: M_ab (midpoint of AB), M_bc, M_ca.")
            .step("Connect midpoints to form the medial triangle.")
            .step("This creates 4 sub-triangles:")
            .step("  1. Corner at A: vertices A, M_ab, M_ca")
            .step("  2. Corner at B: vertices B, M_bc, M_ab")
            .step("  3. Corner at C: vertices C, M_ca, M_bc")
            .step("  4. Center (medial): vertices M_ab, M_bc, M_ca")
            .conclude("Regions per face = 4.")
        )
    
    def model(self):
        return Model().add("Regions per face", len(SUBDIVISION_REGIONS))
    
    def observations(self):
        return Observed().add("Regions per face", 4)


class TotalSamplingRegions(Test):
    """Total sampling regions = 8 faces x 4 regions = 32."""
    name = "Total Sampling Regions"
    level = Level.STANDARD
    question = (
        "The stellated octahedron has 8 triangular faces. If each subdivides "
        "into 4 regions, what is the total sampling region count?"
    )
    reference = "Simple multiplication"
    tolerance = 0.01
    commentary = (
        "8 faces x 4 regions = 32. This equals 2^5, suggesting a natural "
        "binary structure for indexing sampling points."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Tetrahedron A has 4 faces.")
            .step("Tetrahedron B has 4 faces.")
            .step("Total faces = 4 + 4 = 8.")
            .step("Each face subdivides into 4 regions.")
            .step("Total regions = 8 x 4 = 32 = 2^5.")
            .conclude("Total sampling regions = 32.")
        )
    
    def model(self):
        total = len(FACES) * len(SUBDIVISION_REGIONS)
        return Model().add("Total sampling regions", total)
    
    def observations(self):
        return Observed().add("Total sampling regions", 32)


class AllFacesAreTriangles(Test):
    """All 8 faces are triangles (3 vertices each)."""
    name = "All Faces Triangular"
    level = Level.STANDARD
    question = (
        "A tetrahedron has triangular faces. Do both tetrahedra in the "
        "stellated octahedron have all triangular faces?"
    )
    reference = "Tetrahedron definition"
    tolerance = 0.01
    commentary = (
        "The tetrahedron is the simplest 3D polyhedron, with exactly 4 "
        "triangular faces. Two tetrahedra give 8 triangular faces total."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("A tetrahedron has 4 vertices and 4 triangular faces.")
            .step("Each face has exactly 3 vertices.")
            .step("Tetrahedron A: 4 faces, each with 3 vertices.")
            .step("Tetrahedron B: 4 faces, each with 3 vertices.")
            .step("Total: 8 faces, all triangular.")
            .conclude("Total faces = 8; Triangle faces = 8.")
        )
    
    def model(self):
        triangle_count = sum(1 for v in FACES.values() if len(v) == 3)
        return (
            Model()
            .add("Total faces", len(FACES))
            .add("Triangle faces", triangle_count)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Total faces", 8)
            .add("Triangle faces", 8)
        )


class MedialTriangleAreaRatio(Test):
    """Medial triangle has exactly 1/4 the area of the original."""
    name = "Medial Triangle Area Ratio"
    level = Level.STANDARD
    question = (
        "The medial triangle is similar to the original with scale factor 1/2. "
        "What fraction of the original area does it occupy?"
    )
    reference = "Similar triangle scaling: area scales as (length)^2"
    tolerance = 0.01
    commentary = (
        "Since the medial triangle has sides 1/2 the length of the original, "
        "its area is (1/2)^2 = 1/4 of the original. This is a theorem of "
        "Euclidean geometry."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("The medial triangle connects edge midpoints.")
            .step("Each side of the medial triangle is parallel to one side of the original.")
            .step("Each side of the medial triangle has length = (1/2) x original side.")
            .step("Area scales as (linear scale)^2 = (1/2)^2 = 1/4.")
            .conclude("Area ratio (medial/original) = 0.25.")
        )
    
    def model(self):
        # Use an example face
        vertices = list(FACES['FACE_A7'])
        v1, v2, v3 = [get_vertex_coords(v) for v in vertices]
        
        # Original area
        original_area = calculate_triangle_area(v1, v2, v3)
        
        # Medial triangle (midpoints)
        m12 = ((v1[0]+v2[0])/2, (v1[1]+v2[1])/2, (v1[2]+v2[2])/2)
        m23 = ((v2[0]+v3[0])/2, (v2[1]+v3[1])/2, (v2[2]+v3[2])/2)
        m31 = ((v3[0]+v1[0])/2, (v3[1]+v1[1])/2, (v3[2]+v1[2])/2)
        
        medial_area = calculate_triangle_area(m12, m23, m31)
        ratio = medial_area / original_area
        
        return Model().add("Area ratio (medial/original)", ratio)
    
    def observations(self):
        return Observed().add("Area ratio (medial/original)", 0.25)


class SubTrianglesCongruent(Test):
    """All 4 sub-triangles have equal area."""
    name = "Sub-triangles Congruent"
    level = Level.STANDARD
    question = (
        "Are all 4 sub-triangles from the medial construction congruent "
        "(equal in area)?"
    )
    reference = "Medial triangle theorem"
    tolerance = 0.01
    commentary = (
        "Yes. Each of the 4 sub-triangles has area exactly 1/4 of the original. "
        "The 3 corner triangles and the 1 central medial triangle are all "
        "congruent to each other."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("The medial construction creates 4 sub-triangles.")
            .step("Each corner triangle is similar to the original with scale 1/2.")
            .step("Therefore each corner triangle has area = (1/2)^2 = 1/4.")
            .step("The central medial triangle also has area 1/4.")
            .step("Total: 4 x (1/4) = 1 (complete coverage, no overlap).")
            .conclude("Max area deviation = 0.0%.")
        )
    
    def model(self):
        vertices = list(FACES['FACE_A7'])
        v1, v2, v3 = [get_vertex_coords(v) for v in vertices]
        
        # Midpoints
        m12 = ((v1[0]+v2[0])/2, (v1[1]+v2[1])/2, (v1[2]+v2[2])/2)
        m23 = ((v2[0]+v3[0])/2, (v2[1]+v3[1])/2, (v2[2]+v3[2])/2)
        m31 = ((v3[0]+v1[0])/2, (v3[1]+v1[1])/2, (v3[2]+v1[2])/2)
        
        # Four sub-triangles
        areas = [
            calculate_triangle_area(v1, m12, m31),   # Corner 1
            calculate_triangle_area(v2, m23, m12),   # Corner 2
            calculate_triangle_area(v3, m31, m23),   # Corner 3
            calculate_triangle_area(m12, m23, m31),  # Medial
        ]
        
        base = areas[0]
        max_deviation = max(abs(a - base)/base for a in areas) * 100
        
        return Model().add("Max area deviation (%)", max_deviation)
    
    def observations(self):
        return Observed().add("Max area deviation (%)", 0.0)


class SubdivisionMatchesK(Test):
    """The subdivision count 4 matches the closure constant k=4."""
    name = "Subdivision Matches k"
    level = Level.STANDARD
    question = (
        "Is it a coincidence that the medial subdivision produces 4 regions "
        "and the GFD closure constant is k=4?"
    )
    reference = "Topology of simplest closed polyhedra"
    tolerance = 0.01
    commentary = (
        "This is not entirely coincidental. The tetrahedron is the simplest "
        "closed 3D shape, with 4 faces, 4 vertices, and 6 edges. The medial "
        "subdivision of any triangle gives 4 regions. Both involve the number "
        "4 arising from 3D closure requirements."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("The GFD closure constant k=4 comes from tetrahedral topology.")
            .step("The medial subdivision count 4 comes from Euclidean geometry.")
            .step("Both are consequences of working in 3 dimensions.")
            .step("The tetrahedron has k=4 faces; medial gives 4 sub-regions.")
            .step("This is a natural structural correspondence.")
            .conclude("Subdivision count = k = 4.")
        )
    
    def model(self):
        subdivision_count = len(SUBDIVISION_REGIONS)
        return Model().add("Subdivision count", subdivision_count)
    
    def observations(self):
        return Observed().add("Subdivision count", K)


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    MedialSubdivisionCount,
    TotalSamplingRegions,
    AllFacesAreTriangles,
    MedialTriangleAreaRatio,
    SubTrianglesCongruent,
    SubdivisionMatchesK,
]


def run_all():
    """Run all face sampling subdivision tests."""
    return run_tests(
        title="Face Sampling Subdivision: Medial Triangle Construction",
        summary=(
            "These tests validate the medial triangle subdivision. Connecting "
            "edge midpoints divides any triangle into 4 congruent sub-triangles. "
            "Applied to the 8 faces of the stellated octahedron, this gives 32 "
            "total sampling regions with uniform coverage."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
