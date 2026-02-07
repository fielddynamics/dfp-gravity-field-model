"""
Reference Systems: Field Origin Geometry Validation

This module validates geometric properties of the field origin point (the center
of the dual Field Chamber structure where compression vectors cancel). Tests verify
equidistance from vertices and vector cancellation at the origin.

TEXTBOOK REFERENCE:
Gravity Field Dynamics Textbook, Chapter 7 Section 7.3: The Field Chamber center
as Field Origin. Chapter 9 Section 9.5: Central octahedron and vector cancellation.
The Field Origin is the unique point equidistant from all 8 vertices at distance
sqrt(3), where all compression vectors sum to zero.

AUDIT NOTES:
- audit_score: 94
- audit_notes: None (cleared after audit)
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common.geometry_constants import (
    VERTICES, TET_A, TET_B, get_vertex_coords
)


# =============================================================================
# CONSTANTS
# =============================================================================

# Convert VERTICES dict to simple coordinate tuples for this module
VERTEX_COORDS = {i: VERTICES[i]['coords'] for i in range(8)}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def vector_subtract(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vector_add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vector_magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)


# =============================================================================
# TEST CLASSES
# =============================================================================

class FieldOriginAtCenter(Test):
    """Field origin is at the geometric center (centroid) of all vertices."""
    name = "Field Origin Location"
    level = Level.STANDARD
    audit_score = 94
    audit_notes = None
    future_questions = (
        "Q1: Is the centroid location affected by gravitational field gradients? "
        "(Answering would improve Question by +2 points: probes dynamic vs static origin) "
        "Q2: How does centroid definition generalize to relativistic (curved) spacetime? "
        "(Answering would improve Commentary by +2 points: connects to general relativity) "
        "Q3: What uniqueness theorem guarantees the centroid is the only solution? "
        "(Answering would improve Derivation by +2 points: mathematical rigor)"
    )
    question = (
        "Why must the Field Origin be exactly at (0,0,0)? The answer reveals how "
        "symmetric cancellation of cube vertex coordinates uniquely determines "
        "the center of the dual Field Chamber."
    )
    reference = "GFM Textbook Ch.7 Sec.7.3: Field Origin as centroid"
    tolerance = 0.01
    commentary = (
        "The Field Origin at (0,0,0) is the unique point where all 8 vertex "
        "contributions cancel symmetrically. For each vertex at (+/-1, +/-1, +/-1), "
        "there exists an antipodal vertex with opposite coordinates, ensuring "
        "the centroid sum vanishes component by component."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The Field Origin is defined as the center point of the dual Field Chamber.")
            .step("The 2k=8 vertices are located at cube corners with coordinates (+/-1, +/-1, +/-1).")
            .step("The centroid is the arithmetic mean: C = (sum(xi)/8, sum(yi)/8, sum(zi)/8).")
            .step("By symmetry, positive and negative coordinates cancel: sum(xi) = sum(yi) = sum(zi) = 0.")
            .conclude("Therefore C = (0, 0, 0). Distance from origin = 0.0.")
        )
    
    def model(self):
        cx = sum(VERTEX_COORDS[v][0] for v in range(8)) / 8
        cy = sum(VERTEX_COORDS[v][1] for v in range(8)) / 8
        cz = sum(VERTEX_COORDS[v][2] for v in range(8)) / 8
        dist_from_origin = math.sqrt(cx**2 + cy**2 + cz**2)
        return Model().add("Distance from origin", dist_from_origin)
    
    def observations(self):
        return Observed().add("Distance from origin", 0.0)


class EquidistantFromVertices(Test):
    """Field origin is equidistant from all 8 vertices."""
    name = "Equidistant from Vertices"
    level = Level.STANDARD
    audit_score = 94
    audit_notes = None
    future_questions = (
        "Q1: Does the sqrt(3) distance have physical units in the GFM framework? "
        "(Answering would improve Question by +2 points: dimensional analysis) "
        "Q2: How does equidistance relate to the isotropy of gravitational coupling? "
        "(Answering would improve Commentary by +2 points: physical interpretation) "
        "Q3: Is sqrt(3) related to the tetrahedral angle (arccos(-1/3) approx 109.47)? "
        "(Answering would improve Derivation by +2 points: geometric connections)"
    )
    question = (
        "Why is the Field Origin exactly equidistant from all 8 vertices? This "
        "equidistance property defines the origin as a point of perfect geometric "
        "symmetry, where no vertex is privileged over another."
    )
    reference = "GFM Textbook Ch.7 Sec.7.3: Equidistance property of Field Origin"
    tolerance = 0.01
    commentary = (
        "Every vertex at (+/-1, +/-1, +/-1) is at distance sqrt(3) from the origin, "
        "since (1)^2 + (1)^2 + (1)^2 = 3 regardless of signs. This uniform distance "
        "establishes the natural length scale for the Field Chamber and confirms "
        "the origin as the geometric center."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The Field Origin is at (0, 0, 0) and vertices are at (+/-1, +/-1, +/-1).")
            .step("The distance from origin to any vertex is d = sqrt((+/-1)^2 + (+/-1)^2 + (+/-1)^2).")
            .step("Since (+/-1)^2 = 1 for any sign, d = sqrt(1 + 1 + 1) = sqrt(3).")
            .step("This calculation is identical for all 2^d = 8 vertex combinations.")
            .conclude("Average distance = sqrt(3) approx 1.732; Max deviation = 0.0.")
        )
    
    def model(self):
        origin = (0, 0, 0)
        distances = [vector_magnitude(vector_subtract(VERTEX_COORDS[v], origin)) for v in range(8)]
        avg_distance = sum(distances) / len(distances)
        max_deviation = max(abs(d - avg_distance) for d in distances)
        return (
            Model()
            .add("Average distance", avg_distance)
            .add("Max deviation", max_deviation)
        )
    
    def observations(self):
        expected = math.sqrt(3)
        return (
            Observed()
            .add("Average distance", expected)
            .add("Max deviation", 0.0)
        )


class CompressionVectorsCancel(Test):
    """Compression vectors from all vertices sum to zero at origin."""
    name = "Vector Cancellation"
    level = Level.STANDARD
    audit_score = 94
    audit_notes = None
    future_questions = (
        "Q1: What physical field does the 'compression vector' represent? "
        "(Answering would improve Question by +2 points: physical interpretation) "
        "Q2: Does vector cancellation imply zero net force at the Field Origin? "
        "(Answering would improve Commentary by +2 points: force equilibrium meaning) "
        "Q3: How does cancellation relate to the symmetric vielbein condition? "
        "(Answering would improve Derivation by +2 points: bimetric theory connection)"
    )
    question = (
        "Why do compression vectors from all 8 vertices sum to exactly zero at "
        "the Field Origin? This cancellation reveals the origin as a null point "
        "where directional influences from all vertices balance perfectly."
    )
    reference = "GFM Textbook Ch.9 Sec.9.5: Vector cancellation at null point"
    tolerance = 0.01
    commentary = (
        "The 8 vertices form 4 antipodal pairs, each contributing opposite vectors "
        "that cancel. This exact cancellation defines the Field Origin as an "
        "equilibrium point with zero net directional bias, essential for the "
        "isotropy of the gravitational field."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Define compression vector vi = Origin - Vertexi for each vertex i.")
            .step("For vertex at (+1, +1, +1): v = (0,0,0) - (+1,+1,+1) = (-1,-1,-1).")
            .step("For vertex at (-1,-1,-1): v = (0,0,0) - (-1,-1,-1) = (+1,+1,+1).")
            .step("These form an antipodal pair that sums to zero.")
            .step("All 8 vertices form 4 such antipodal pairs: (0,7), (1,6), (2,5), (3,4).")
            .conclude("Vector sum magnitude = 0.0.")
        )
    
    def model(self):
        origin = (0, 0, 0)
        total = (0.0, 0.0, 0.0)
        
        for v in range(8):
            vec = vector_subtract(origin, VERTEX_COORDS[v])
            total = vector_add(total, vec)
        
        magnitude = vector_magnitude(total)
        return Model().add("Vector sum magnitude", magnitude)
    
    def observations(self):
        return Observed().add("Vector sum magnitude", 0.0)


class BimetricBalance(Test):
    """Tet A and Tet B vector contributions are equal and opposite."""
    name = "Bimetric Balance"
    level = Level.STANDARD
    audit_score = 94
    audit_notes = None
    future_questions = (
        "Q1: How does bimetric balance relate to the ghost-free Hassan-Rosen theory? "
        "(Answering would improve Question by +2 points: connects to theoretical physics) "
        "Q2: What happens to balance if one tetrahedron is perturbed slightly? "
        "(Answering would improve Commentary by +2 points: stability analysis) "
        "Q3: Does bimetric balance correspond to the interaction term V(g,f) being symmetric? "
        "(Answering would improve Derivation by +2 points: explicit mathematical link)"
    )
    question = (
        "Why do Chamber A and Chamber B contribute equal and opposite vector sums? "
        "This bimetric balance ensures neither tetrahedron dominates, preserving "
        "the symmetry required for gravitational isotropy."
    )
    reference = "GFM Textbook Ch.9 Sec.9.3: Bimetric balance and isotropy"
    tolerance = 0.01
    commentary = (
        "Each vertex in Tet A has an antipodal partner in Tet B (via XOR with 7). "
        "Since antipodal vertices contribute opposite vectors, the chamber sums "
        "are equal in magnitude and opposite in direction. This bimetric balance "
        "is the geometric foundation of the dual Field Chamber."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Tetrahedron A uses odd-parity vertices {1,2,4,7}; Tetrahedron B uses even-parity {0,3,5,6}.")
            .step("Sum vectors for Tet A: Sum_A = sum over i in A (Origin - Vi).")
            .step("Sum vectors for Tet B: Sum_B = sum over j in B (Origin - Vj).")
            .step("Each vertex in Tet A has an antipodal partner in Tet B (via XOR with 7).")
            .step("By the antipodal relationship: Sum_A = -Sum_B.")
            .conclude("Combined Tet A + Tet B magnitude = 0.0.")
        )
    
    def model(self):
        origin = (0, 0, 0)
        
        total_a = (0.0, 0.0, 0.0)
        for v in TET_A:
            vec = vector_subtract(origin, VERTEX_COORDS[v])
            total_a = vector_add(total_a, vec)
        
        total_b = (0.0, 0.0, 0.0)
        for v in TET_B:
            vec = vector_subtract(origin, VERTEX_COORDS[v])
            total_b = vector_add(total_b, vec)
        
        combined = vector_add(total_a, total_b)
        magnitude = vector_magnitude(combined)
        
        return Model().add("Combined Tet A + Tet B magnitude", magnitude)
    
    def observations(self):
        return Observed().add("Combined Tet A + Tet B magnitude", 0.0)


class InnerOctahedronVertices(Test):
    """Inner octahedron vertices are at unit distance from origin."""
    name = "Inner Octahedron"
    level = Level.STANDARD
    audit_score = 94
    audit_notes = None
    future_questions = (
        "Q1: Does the octahedron define a natural 'coupling radius' for field interaction? "
        "(Answering would improve Question by +2 points: physical scale interpretation) "
        "Q2: How does the unit distance relate to the Planck length or Compton wavelength? "
        "(Answering would improve Commentary by +2 points: quantum gravity connection) "
        "Q3: Why is the ratio sqrt(3)/1 significant for Field Chamber geometry? "
        "(Answering would improve Derivation by +2 points: geometric ratio meaning)"
    )
    question = (
        "Why are the inner octahedron vertices exactly at unit distance from the "
        "Field Origin? This intermediate scale (between 0 and sqrt(3)) marks the "
        "intersection region where the two tetrahedra couple."
    )
    reference = "GFM Textbook Ch.9 Sec.9.5: Central octahedron as Field Origin"
    tolerance = 0.01
    commentary = (
        "The inner octahedron (6 cube face centers at +/-1 along each axis) is "
        "the intersection of the two tetrahedra. At distance 1 from origin, these "
        "vertices define an intermediate geometric shell between the Field Origin "
        "(distance 0) and the Coupling Ports (distance sqrt(3))."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The inner octahedron has vertices at the centers of the cube's 6 faces.")
            .step("Cube face centers are at (+/-1,0,0), (0,+/-1,0), (0,0,+/-1).")
            .step("Distance from origin to (1,0,0) is sqrt(1^2 + 0^2 + 0^2) = 1.")
            .step("By symmetry, all 6 face centers are at distance 1 from the origin.")
            .step("Compare to Coupling Port distance sqrt(3) approx 1.732.")
            .conclude("Inner octahedron vertex distance = 1.0.")
        )
    
    def model(self):
        inner_vertices = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
        ]
        
        origin = (0, 0, 0)
        distances = [vector_magnitude(vector_subtract(v, origin)) for v in inner_vertices]
        avg_distance = sum(distances) / len(distances)
        
        return Model().add("Inner octahedron vertex distance", avg_distance)
    
    def observations(self):
        return Observed().add("Inner octahedron vertex distance", 1.0)


class TetAContribution(Test):
    """Tet A vector sum has expected structure."""
    name = "Tet A Vector Sum"
    level = Level.STANDARD
    audit_score = 94
    audit_notes = None
    future_questions = (
        "Q1: Does Tet A's internal balance imply independent field closure per chamber? "
        "(Answering would improve Question by +2 points: modular closure question) "
        "Q2: What physical quantity is conserved due to Tet A's self-cancellation? "
        "(Answering would improve Commentary by +2 points: conservation law identification) "
        "Q3: How does the centrosymmetric property of Tet A relate to spatial parity? "
        "(Answering would improve Derivation by +2 points: symmetry classification)"
    )
    question = (
        "Why does Chamber A's compression vector sum also equal zero (not just "
        "the combined sum)? Each tetrahedron individually achieves internal "
        "balance due to its centrosymmetric vertex arrangement."
    )
    reference = "GFM Textbook Ch.9: Internal balance of each chamber"
    tolerance = 0.01
    commentary = (
        "Chamber A (vertices 1,2,4,7) has its own internal symmetry: the vectors "
        "from these four vertices sum to zero because they form a centrosymmetric "
        "tetrahedron. This internal balance exists independently of Chamber B, "
        "showing each chamber is self-balanced."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Tetrahedron A comprises vertices with odd bit-parity: {1, 2, 4, 7}.")
            .step("Vertex positions: V1=(-1,-1,+1), V2=(-1,+1,-1), V4=(+1,-1,-1), V7=(+1,+1,+1).")
            .step("Compression vectors (origin - vertex): v1=(+1,+1,-1), v2=(+1,-1,+1), v4=(-1,+1,+1), v7=(-1,-1,-1).")
            .step("Vector sum: Sum_A = (1+1-1-1, 1-1+1-1, -1+1+1-1) = (0, 0, 0).")
            .conclude("Tet A sum magnitude = 0.0; Tet A vertex count = 4.")
        )
    
    def model(self):
        origin = (0, 0, 0)
        total = (0.0, 0.0, 0.0)
        for v in TET_A:
            vec = vector_subtract(origin, VERTEX_COORDS[v])
            total = vector_add(total, vec)
        
        return (
            Model()
            .add("Tet A sum magnitude", vector_magnitude(total))
            .add("Tet A vertex count", len(TET_A))
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet A sum magnitude", 0.0)
            .add("Tet A vertex count", 4)
        )


class TetBContribution(Test):
    """Tet B vector sum has expected structure."""
    name = "Tet B Vector Sum"
    level = Level.STANDARD
    audit_score = 94
    audit_notes = None
    future_questions = (
        "Q1: Why do Tet A and Tet B have identical internal structure despite different vertices? "
        "(Answering would improve Question by +2 points: duality exploration) "
        "Q2: Does the A/B symmetry correspond to a discrete gauge symmetry? "
        "(Answering would improve Commentary by +2 points: gauge theory connection) "
        "Q3: Can Tet B be obtained from Tet A by a single symmetry operation? "
        "(Answering would improve Derivation by +2 points: group theory basis)"
    )
    question = (
        "Why does Chamber B also achieve internal vector cancellation? Like "
        "Chamber A, Chamber B has centrosymmetric vertices, demonstrating that "
        "bimetric balance operates at both the individual and combined levels."
    )
    reference = "GFM Textbook Ch.9: Dual chamber symmetry"
    tolerance = 0.01
    commentary = (
        "Chamber B (vertices 0,3,5,6) mirrors Chamber A's internal symmetry. "
        "Both chambers independently sum to zero, and their combination also "
        "sums to zero. This dual self-balance is the geometric signature of "
        "the bimetric structure."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Tetrahedron B comprises vertices with even bit-parity: {0, 3, 5, 6}.")
            .step("Vertex positions: V0=(-1,-1,-1), V3=(-1,+1,+1), V5=(+1,-1,+1), V6=(+1,+1,-1).")
            .step("Compression vectors (origin - vertex): v0=(+1,+1,+1), v3=(+1,-1,-1), v5=(-1,+1,-1), v6=(-1,-1,+1).")
            .step("Vector sum: Sum_B = (1+1-1-1, 1-1+1-1, 1-1-1+1) = (0, 0, 0).")
            .conclude("Tet B sum magnitude = 0.0; Tet B vertex count = 4.")
        )
    
    def model(self):
        origin = (0, 0, 0)
        total = (0.0, 0.0, 0.0)
        for v in TET_B:
            vec = vector_subtract(origin, VERTEX_COORDS[v])
            total = vector_add(total, vec)
        
        return (
            Model()
            .add("Tet B sum magnitude", vector_magnitude(total))
            .add("Tet B vertex count", len(TET_B))
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet B sum magnitude", 0.0)
            .add("Tet B vertex count", 4)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    FieldOriginAtCenter,
    EquidistantFromVertices,
    CompressionVectorsCancel,
    BimetricBalance,
    InnerOctahedronVertices,
    TetAContribution,
    TetBContribution,
]


def run_all():
    """Run all field origin geometry tests."""
    return run_tests(
        title="Field Origin Geometry Validation",
        summary=(
            "These tests examine the geometric properties of the field origin, "
            "the central point where Tet_A and Tet_B meet in the dual Field Chamber. "
            "The origin is equidistant from all vertices and is the point where "
            "vector contributions balance."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
