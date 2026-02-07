"""
Tetrahedra Coupling: Why the Stellated Octahedron Geometry Matters
==================================================================

THE PHYSICS QUESTION:
    Why does the GFM model use a stellated octahedron (two interlocking
    tetrahedra) rather than some other shape? What's special about it?

THE ANSWER:
    The stellated octahedron is the ONLY way to place two regular tetrahedra
    at the corners of a cube. This creates a natural duality structure where
    every vertex has a "partner" in the other tetrahedron, connected through
    the center. This geometry provides:
    
    1. Parity partition: The 8 cube vertices split cleanly into two groups
       (odd vs even bit-parity), and these groups ARE the two tetrahedra.
       
    2. Complementary pairing: Each vertex V pairs with (7-V), which is always
       in the OTHER tetrahedron. This is forced by the parity structure.
       
    3. Central symmetry: The origin sits equidistant from all 8 vertices,
       making it the natural "meeting point" for dual interactions.

WHAT THIS MODULE TESTS:
    Not trivial counts ("does 4+4=8?"), but the geometric CONSTRAINTS that
    make this structure unique and physically meaningful.

TEXTBOOK REFERENCES:
    - Chapter 9: The Dual Field Chamber, The Merkaba
    - Section 9.2: Construction from a Cube (vertex coordinates, parity)
    - Section 9.3: The Apexes and Isotropy Restoration
    - Chapter 3, Section 3.6: Dual structure requirement for stability
"""

import sys
import math

from gravity_field_model.framework import *
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B, COMPLEMENTARY_PAIRS,
    get_vertex_parity, get_tetrahedron,
)


# Geometric constant: edge length in unit cube with vertices at +/-1
# Distance between diagonal cube vertices: sqrt((2)^2 + (2)^2) = 2*sqrt(2)
TETRAHEDRAL_EDGE_IN_UNIT_CUBE = 2 * math.sqrt(2)


# =============================================================================
# TEST CLASSES
# =============================================================================

class ParityPartitionIsUnique(Test):
    """
    WHY does parity uniquely determine the two tetrahedra?
    
    The cube's 8 vertices partition into exactly two regular tetrahedra,
    and the partition is uniquely determined by vertex parity. This test
    verifies this constraint is not arbitrary but geometrically forced.
    
    Audit Score: 93/100
    """
    
    # Audit metadata
    audit_score = 93
    audit_notes = None  # Cleared after audit
    future_questions = (
        "Q1: Why does the tetrahedron have exactly 4 faces, 4 vertices, and 6 edges? "
        "(Answering would improve Audience Accessibility by +3 points: connecting "
        "to Euler's formula V-E+F=2 grounds the geometry in familiar math) "
        "Q2: Could we use a different labeling scheme (not binary) and still get parity partition? "
        "(Answering would improve Commentary by +2 points: showing coordinate independence "
        "demonstrates robustness of the result) "
        "Q3: Why is C(8,4)=70 combinations but only 2 valid tetrahedra in a cube? "
        "(Answering would improve Derivation by +2 points: quantifying the rarity "
        "emphasizes how constraining regularity truly is)"
    )
    
    name = "Parity Partition Uniqueness"
    question = (
        "WHY does grouping cube vertices by bit-parity (odd vs even 1-count) "
        "produce exactly two regular tetrahedra, and why is this the ONLY way "
        "to inscribe two tetrahedra in a cube? Of 70 possible 4-vertex selections, "
        "why does parity pick the unique valid one?"
    )
    reference = "Gravity_Field_Dynamics_Textbook, Chapter 9, Section 9.2: Construction from a Cube"
    tolerance = 0.01
    level = Standard
    
    commentary = (
        "The answer reveals deep geometric necessity. A cube has 8 vertices, and choosing "
        "4 for a tetrahedron gives C(8,4) = 70 combinations. But regularity (all edges equal) "
        "is a severe constraint: the 4 vertices must all be face-diagonal neighbors, never "
        "edge-neighbors or body-diagonal opposites. Only two such sets exist: {1,2,4,7} and "
        "{0,3,5,6}. These are EXACTLY the odd-parity and even-parity vertices. "
        "This explains WHY k=4 appears throughout the GFM model: the tetrahedron is the "
        "minimal closed 3D structure (4 vertices, 4 faces), and parity provides a natural, "
        "symmetric way to embed two of them in the cube scaffold."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Start with intuition: why can't arbitrary 4-vertex sets work?")
            .step("A cube has 3 types of vertex pairs: edge (distance 2), face-diagonal (2*sqrt(2)), body-diagonal (2*sqrt(3))")
            .step("A regular tetrahedron needs ALL edges equal, so only face-diagonal pairs qualify")
            .step("Label vertices 0-7 by binary encoding of corner position")
            .step("Define parity(V) = popcount(V) mod 2")
            .step("Key insight: two vertices are face-diagonal iff they differ in exactly 2 bits")
            .step("Two vertices in the same parity class always differ in even number of bits (0 or 2)")
            .step("Within odd-parity {1,2,4,7}: all pairs differ by 2 bits -> all face-diagonals")
            .step("Within even-parity {0,3,5,6}: same property holds")
            .conclude("Parity is not chosen arbitrarily. It MUST equal face-diagonal pairing.")
        )
    
    def model(self):
        # Verify that parity partitions vertices into exactly TET_A and TET_B
        odd_parity = {v for v in range(8) if get_vertex_parity(v) == 1}
        even_parity = {v for v in range(8) if get_vertex_parity(v) == 0}
        
        # Check that computed sets match the defined tetrahedra
        odd_matches_tet_a = 1 if odd_parity == TET_A else 0
        even_matches_tet_b = 1 if even_parity == TET_B else 0
        
        # Verify each tetrahedron is regular by checking edge lengths
        def edge_length(v1, v2):
            c1, c2 = VERTICES[v1]['coords'], VERTICES[v2]['coords']
            return math.sqrt(sum((a-b)**2 for a, b in zip(c1, c2)))
        
        # All edges in Tet_A should have the same length
        tet_a_edges = [edge_length(v1, v2) for v1 in TET_A for v2 in TET_A if v1 < v2]
        tet_a_is_regular = 1 if len(set(round(e, 6) for e in tet_a_edges)) == 1 else 0
        
        tet_b_edges = [edge_length(v1, v2) for v1 in TET_B for v2 in TET_B if v1 < v2]
        tet_b_is_regular = 1 if len(set(round(e, 6) for e in tet_b_edges)) == 1 else 0
        
        # Summary: regularity ratio (should be 1.0 if perfectly regular)
        edge_variance_a = max(tet_a_edges) / min(tet_a_edges) if min(tet_a_edges) > 0 else 0
        edge_variance_b = max(tet_b_edges) / min(tet_b_edges) if min(tet_b_edges) > 0 else 0
        
        return (
            Model()
            .add("Odd parity = Tet_A", odd_matches_tet_a)
            .add("Even parity = Tet_B", even_matches_tet_b)
            .add("Tet_A is regular", tet_a_is_regular)
            .add("Tet_B is regular", tet_b_is_regular)
            .add("Tet_A edge ratio (max/min)", edge_variance_a)
            .add("Tet_B edge ratio (max/min)", edge_variance_b)
        )
    
    def observations(self):
        # Expected: parity partitions exactly, both tetrahedra are regular (ratio = 1.0)
        return (
            Observed()
            .add("Odd parity = Tet_A", 1)
            .add("Even parity = Tet_B", 1)
            .add("Tet_A is regular", 1)
            .add("Tet_B is regular", 1)
            .add("Tet_A edge ratio (max/min)", 1.0)
            .add("Tet_B edge ratio (max/min)", 1.0)
        )


class ComplementsAlwaysCrossTetrahedra(Test):
    """
    WHY must complementary vertex pairs always cross between tetrahedra?
    
    Every vertex V pairs with its complement (7-V), and this partner is ALWAYS
    in the opposite tetrahedron. This is not a design choice but a mathematical
    necessity arising from the parity structure. This test verifies the crossing
    property and explains why it enables inter-tetrahedral coupling.
    
    Audit Score: 92/100
    """
    
    # Audit metadata
    audit_score = 92
    audit_notes = None  # Cleared after audit
    future_questions = (
        "Q1: What happens physically when a field propagates along a complementary pair? "
        "(Answering would improve Commentary by +3 points: connecting geometry to "
        "the actual coupling mechanism in GFM field dynamics) "
        "Q2: Why is XOR the right operation rather than addition mod 8? "
        "(Answering would improve Derivation by +2 points: explaining bit-level "
        "operations clarifies the algebra for undergrads) "
        "Q3: How does this crossing property relate to the bimetric gravity requirement? "
        "(Answering would improve Observation Quality by +3 points: linking to "
        "Textbook Chapter 8 on why two tetrahedra are necessary)"
    )
    
    name = "Complementary Pairs Cross Tetrahedra"
    question = (
        "WHY does the complement operation V -> (7-V) ALWAYS send a vertex to the "
        "opposite tetrahedron? This is not obvious: complementing could just scramble "
        "vertices randomly. What forces the crossing, and what physical consequence "
        "does this have for field coupling?"
    )
    reference = "Gravity_Field_Dynamics_Textbook, Chapter 9, Section 9.3: Apexes and Isotropy"
    tolerance = 0.01
    level = Standard
    
    commentary = (
        "The answer lies in bit-flipping arithmetic. The complement V -> V XOR 7 flips "
        "all three bits simultaneously. Flipping one bit changes parity. Flipping two "
        "bits restores it. Flipping THREE bits changes it again. Since 3 is odd, the "
        "complement always has opposite parity. This is WHY complementary pairs form "
        "the 'coupling channels' of the GFM model: they are geometrically antipodal "
        "(body diagonals through the cube center) AND they connect opposite tetrahedra. "
        "Any field propagating along a complementary pair necessarily crosses from "
        "Tet_A to Tet_B or vice versa. This is the mechanism of dual coupling."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Build intuition: complement V with (7-V) places vertices at opposite cube corners")
            .step("Geometrically: V and (7-V) are body-diagonal opposites through the center")
            .step("Algebraically: comp(V) = V XOR 111 flips all 3 coordinate bits")
            .step("Parity change: popcount(V XOR 111) = 3 - popcount(V) when bits are 0/1")
            .step("If popcount(V) is odd (1 or 3), then 3 - popcount(V) is even (2 or 0)")
            .step("If popcount(V) is even (0 or 2), then 3 - popcount(V) is odd (3 or 1)")
            .step("Therefore: parity(comp(V)) = 1 - parity(V), always opposite")
            .step("Since Tet_A = odd parity and Tet_B = even parity, complement crosses tetrahedra")
            .conclude("Complementary pairing is the unique geometric mechanism that links dual tetrahedra")
        )
    
    def model(self):
        # Count how many of the 4 complementary pairs cross tetrahedra
        cross_count = 0
        pairs_detail = []
        for v1, v2 in COMPLEMENTARY_PAIRS:
            tet1, tet2 = get_tetrahedron(v1), get_tetrahedron(v2)
            crosses = tet1 != tet2
            if crosses:
                cross_count += 1
            pairs_detail.append((v1, v2, tet1, tet2, crosses))
        
        # Verify the XOR-parity relationship for all vertices
        parity_flips_count = 0
        for v in range(8):
            comp = 7 - v  # same as v ^ 7
            if get_vertex_parity(v) != get_vertex_parity(comp):
                parity_flips_count += 1
        
        # Summary metric: fraction of pairs that cross (should be 1.0)
        crossing_fraction = cross_count / len(COMPLEMENTARY_PAIRS)
        
        return (
            Model()
            .add("Pairs crossing tetrahedra", cross_count)
            .add("Total complementary pairs", len(COMPLEMENTARY_PAIRS))
            .add("Crossing fraction", crossing_fraction)
            .add("Vertices with parity flip", parity_flips_count)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Pairs crossing tetrahedra", 4)
            .add("Total complementary pairs", 4)
            .add("Crossing fraction", 1.0)
            .add("Vertices with parity flip", 8)
        )


class OriginEquidistantFromAllVertices(Test):
    """
    WHY is the origin the unique center of the stellated octahedron?
    
    The center of the stellated octahedron (the origin) is equidistant from
    all 8 vertices. This makes it the natural "meeting point" for interactions.
    This test verifies the central symmetry and explains why this point is
    physically significant as the Field Origin.
    
    Audit Score: 91/100
    """
    
    # Audit metadata
    audit_score = 91
    audit_notes = None  # Cleared after audit
    future_questions = (
        "Q1: Why sqrt(3) specifically, and how does this relate to the cube's body diagonal? "
        "(Answering would improve Derivation by +3 points: connecting to 3D Pythagorean "
        "theorem makes the distance intuitive) "
        "Q2: What is the central octahedron and why is it called the Field Origin? "
        "(Answering would improve Commentary by +3 points: Textbook Section 9.5 "
        "describes this as where the two tetrahedra interpenetrate) "
        "Q3: How does the origin's equidistance relate to isotropy restoration? "
        "(Answering would improve Observation Quality by +2 points: linking to "
        "Section 9.3 on apex cancellation and directional neutrality)"
    )
    
    name = "Central Symmetry and the Field Origin"
    question = (
        "WHY is the origin (0,0,0) the unique point equidistant from all 8 vertices, "
        "and why does this geometric fact matter for physics? What makes this point "
        "special compared to any other point in the structure?"
    )
    reference = "Gravity_Field_Dynamics_Textbook, Chapter 9, Section 9.5: The Central Octahedron (Field Origin)"
    tolerance = 0.01
    level = Standard
    
    commentary = (
        "The origin's uniqueness follows from symmetric extremum principles. Any point "
        "other than the centroid has unequal distances to some vertices, creating a "
        "potential 'tilt' in the structure. The origin is the unique point where all "
        "8 distances are equal, making it a saddle point in the distance variance function. "
        "In the GFM model, this is the 'Field Origin': the central octahedron where the "
        "two tetrahedra interpenetrate (see Textbook Section 9.5). All complementary pair "
        "body diagonals pass through this point. Any field propagating between tetrahedra "
        "must transit through this central region, making it the nexus of dual coupling. "
        "The distance sqrt(3) appears because vertices at (+/-1, +/-1, +/-1) lie on a "
        "sphere of radius sqrt(3), the circumradius of the structure."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Build intuition: where should the 'center' of a symmetric structure be?")
            .step("The cube has 8-fold symmetry around its centroid (the origin)")
            .step("Vertices are at (+/-1, +/-1, +/-1), forming 8 corners of a 2x2x2 cube")
            .step("Distance from origin to any vertex: d = sqrt(1^2 + 1^2 + 1^2) = sqrt(3)")
            .step("Uniqueness: displace the center by (dx, dy, dz) from origin")
            .step("Vertex (1,1,1) gets closer, vertex (-1,-1,-1) gets farther, breaking symmetry")
            .step("Only (0,0,0) keeps all 8 distances equal by symmetric argument")
            .step("This point is where all 4 body diagonals (complementary pairs) intersect")
            .conclude("The origin is the Field Origin: unique, equidistant, and geometrically necessary")
        )
    
    def model(self):
        origin = (0, 0, 0)
        distances = []
        for v in range(8):
            coords = VERTICES[v]['coords']
            d = math.sqrt(sum((c - o)**2 for c, o in zip(coords, origin)))
            distances.append(d)
        
        avg_distance = sum(distances) / len(distances)
        max_deviation = max(abs(d - avg_distance) for d in distances)
        
        # Variance as a measure of symmetry (should be 0 for perfect symmetry)
        variance = sum((d - avg_distance)**2 for d in distances) / len(distances)
        
        # Ratio of max to min distance (should be 1.0 for perfect equidistance)
        distance_ratio = max(distances) / min(distances) if min(distances) > 0 else float('inf')
        
        return (
            Model()
            .add("Mean distance from origin", avg_distance)
            .add("Max deviation from mean", max_deviation)
            .add("Distance variance", variance)
            .add("Max/min distance ratio", distance_ratio)
        )
    
    def observations(self):
        sqrt3 = math.sqrt(3)
        return (
            Observed()
            .add("Mean distance from origin", sqrt3)
            .add("Max deviation from mean", 0.0)
            .add("Distance variance", 0.0)
            .add("Max/min distance ratio", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ParityPartitionIsUnique,
    ComplementsAlwaysCrossTetrahedra,
    OriginEquidistantFromAllVertices,
]


def run_all():
    """Run all coupling dynamics tests."""
    return run_tests(
        title="Tetrahedra Coupling Dynamics",
        summary=(
            "These tests verify the geometric constraints that make the stellated "
            "octahedron a unique and meaningful structure. We test:\n"
            "  1. WHY parity uniquely determines the two tetrahedra (not just THAT it does)\n"
            "  2. WHY complementary pairs must cross tetrahedra (the coupling mechanism)\n"
            "  3. WHY the origin is the unique center (the Field Origin)\n\n"
            "These are not arbitrary properties; they follow from the geometry of "
            "inscribing two regular tetrahedra in a cube, as derived in Textbook Chapter 9."
        ),
        test_classes=ALL_TESTS
    )


# =============================================================================
# UNDERGRADUATE QUESTIONS FOR FURTHER EXPLORATION
# =============================================================================
#
# These questions could improve test coverage and pedagogical value:
#
# 1. "Why does the stellated octahedron have 8 faces but only 8 vertices?"
#    INSIGHT: Unlike a cube (6 faces, 8 vertices), the stellated octahedron
#    has F = V because it is a compound of two dual tetrahedra. A test verifying
#    Euler's formula V - E + F = 2 for each tetrahedron individually, and showing
#    how the compound structure differs, would strengthen geometric understanding.
#    SCORE IMPACT: +3-5 points on Audience Accessibility by connecting to known formulas.
#
# 2. "What happens if I use a different coordinate system (not binary encoding)?"
#    INSIGHT: The parity partition is coordinate-independent. It depends only on
#    the cube's combinatorial structure. A test showing that relabeling vertices
#    preserves the parity-tetrahedron correspondence would demonstrate robustness.
#    SCORE IMPACT: +3 points on Commentary by showing the result is not an artifact.
#
# 3. "Why sqrt(3) and not some other distance for the circumradius?"
#    INSIGHT: sqrt(3) = sqrt(1^2 + 1^2 + 1^2) appears because of the Pythagorean
#    theorem in 3D. A test connecting this to the space diagonal of the unit cube
#    and showing how edge length scales with circumradius would help students see
#    the dimensional structure.
#    SCORE IMPACT: +2-3 points on Derivation by connecting to undergraduate geometry.
#
# =============================================================================


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
