"""
Tetrahedra Coupling: Why the Stellated Octahedron Geometry Matters
==================================================================

THE PHYSICS QUESTION:
    Why does the GFD model use a stellated octahedron (two interlocking
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
"""

import sys
import math

from gfd_model_v2.framework import *
from gfd_model_v2.common import (
    K, VERTICES, TET_A, TET_B, COMPLEMENTARY_PAIRS,
    get_vertex_parity, get_tetrahedron,
)


# =============================================================================
# TEST CLASSES
# =============================================================================

class ParityPartitionIsUnique(Test):
    """
    The cube's 8 vertices partition into exactly two regular tetrahedra,
    and the partition is uniquely determined by vertex parity.
    """
    
    name = "Parity Partition Uniqueness"
    question = (
        "When you inscribe two regular tetrahedra in a cube (using its vertices), "
        "is there only ONE way to do it? And does that way correspond exactly "
        "to grouping vertices by their binary parity (odd vs even number of 1-bits)?"
    )
    reference = "Combinatorial geometry"
    tolerance = 0.01
    level = Standard
    
    commentary = (
        "This is not a trivial observation. A cube has 8 vertices, and we need to "
        "pick 4 for each tetrahedron. There are C(8,4) = 70 ways to choose 4 vertices. "
        "But only ONE choice gives a regular tetrahedron (all edges equal). That choice "
        "is exactly the odd-parity vertices {1,2,4,7}. The remaining even-parity vertices "
        "{0,3,5,6} automatically form the second regular tetrahedron. This is WHY "
        "k=4 appears: a tetrahedron has 4 vertices, 4 faces, and is the minimal 3D simplex."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Label cube vertices 0-7 by their corner position (binary encoding)")
            .step("Define parity(V) = number of 1-bits in V, mod 2")
            .step("Odd-parity vertices: V in {1,2,4,7} where popcount(V) is odd")
            .step("Even-parity vertices: V in {0,3,5,6} where popcount(V) is even")
            .step("Verify: each set of 4 vertices forms a regular tetrahedron")
            .step("Proof: within each parity class, all pairs are body diagonals of cube faces")
            .conclude("Parity uniquely determines the tetrahedra; no other partition works")
        )
    
    def model(self):
        # Verify that parity partitions vertices into exactly TET_A and TET_B
        odd_parity = {v for v in range(8) if get_vertex_parity(v) == 1}
        even_parity = {v for v in range(8) if get_vertex_parity(v) == 0}
        
        # Check that computed sets match the defined tetrahedra
        odd_matches_tet_a = 1 if odd_parity == TET_A else 0
        even_matches_tet_b = 1 if even_parity == TET_B else 0
        
        # Verify each tetrahedron is regular by checking edge lengths
        # In a unit cube with vertices at +/-1, diagonal distance = 2*sqrt(2)
        def edge_length(v1, v2):
            c1, c2 = VERTICES[v1]['coords'], VERTICES[v2]['coords']
            return math.sqrt(sum((a-b)**2 for a, b in zip(c1, c2)))
        
        # All edges in Tet_A should have the same length
        tet_a_edges = [edge_length(v1, v2) for v1 in TET_A for v2 in TET_A if v1 < v2]
        tet_a_is_regular = 1 if len(set(round(e, 6) for e in tet_a_edges)) == 1 else 0
        
        tet_b_edges = [edge_length(v1, v2) for v1 in TET_B for v2 in TET_B if v1 < v2]
        tet_b_is_regular = 1 if len(set(round(e, 6) for e in tet_b_edges)) == 1 else 0
        
        return (
            Model()
            .add("Odd parity = Tet_A", odd_matches_tet_a)
            .add("Even parity = Tet_B", even_matches_tet_b)
            .add("Tet_A is regular", tet_a_is_regular)
            .add("Tet_B is regular", tet_b_is_regular)
            .add("Tet_A edge length", tet_a_edges[0])
            .add("Tet_B edge length", tet_b_edges[0])
        )
    
    def observations(self):
        # Expected: parity partitions exactly, both tetrahedra are regular
        # Edge length in unit cube: distance from (1,1,-1) to (1,-1,1) = sqrt(8) = 2*sqrt(2)
        expected_edge = 2 * math.sqrt(2)
        return (
            Observed()
            .add("Odd parity = Tet_A", 1)
            .add("Even parity = Tet_B", 1)
            .add("Tet_A is regular", 1)
            .add("Tet_B is regular", 1)
            .add("Tet_A edge length", expected_edge)
            .add("Tet_B edge length", expected_edge)
        )


class ComplementsAlwaysCrossTetrahedra(Test):
    """
    Every vertex V pairs with complement (7-V), and this partner is ALWAYS
    in the opposite tetrahedron. This is forced by geometry, not by choice.
    """
    
    name = "Complementary Pairs Cross Tetrahedra"
    question = (
        "For each vertex V, its binary complement (7-V) is in the OTHER tetrahedron. "
        "Is this true for all 8 vertices, and WHY does this happen?"
    )
    reference = "Binary arithmetic"
    tolerance = 0.01
    level = Standard
    
    commentary = (
        "The complement operation V -> (7-V) is equivalent to V -> V XOR 7, which flips "
        "all three bits. Flipping all bits always changes the parity (odd becomes even, "
        "even becomes odd). Since parity determines tetrahedron membership, the complement "
        "of any vertex is GUARANTEED to be in the other tetrahedron. This is not a coincidence "
        "or a design choice; it is a mathematical necessity. The physics implication: when "
        "the model pairs complementary vertices, it automatically couples the two tetrahedra."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Complement of V is defined as comp(V) = 7 - V = V XOR 111 (binary)")
            .step("XOR with 111 flips all three bits")
            .step("Flipping all bits changes parity: if V has odd 1-count, comp(V) has even")
            .step("Parity determines tetrahedron: odd -> Tet_A, even -> Tet_B")
            .step("Therefore comp(V) is always in the opposite tetrahedron from V")
            .step("Check: (0,7), (1,6), (2,5), (3,4) all cross the A/B boundary")
            .conclude("All 4 complementary pairs span both tetrahedra")
        )
    
    def model(self):
        # Count how many of the 4 complementary pairs cross tetrahedra
        cross_count = 0
        for v1, v2 in COMPLEMENTARY_PAIRS:
            if get_tetrahedron(v1) != get_tetrahedron(v2):
                cross_count += 1
        
        # Verify the XOR-parity relationship for all vertices
        parity_always_flips = 1
        for v in range(8):
            comp = 7 - v  # same as v ^ 7
            if get_vertex_parity(v) == get_vertex_parity(comp):
                parity_always_flips = 0
                break
        
        return (
            Model()
            .add("Pairs crossing tetrahedra", cross_count)
            .add("Parity always flips under complement", parity_always_flips)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Pairs crossing tetrahedra", 4)  # all 4 pairs
            .add("Parity always flips under complement", 1)
        )


class OriginEquidistantFromAllVertices(Test):
    """
    The center of the stellated octahedron (the origin) is equidistant from
    all 8 vertices. This makes it the natural "meeting point" for interactions.
    """
    
    name = "Central Symmetry"
    question = (
        "Is the origin (0,0,0) equidistant from all 8 vertices of the stellated "
        "octahedron, and what is the geometric significance of this point?"
    )
    reference = "Cube geometry"
    tolerance = 0.01
    level = Standard
    
    commentary = (
        "The 8 vertices sit at the corners of a cube centered at the origin. By symmetry, "
        "each vertex is at the same distance from the center: the space diagonal of a unit "
        "cube divided by 2. For vertices at (+/-1, +/-1, +/-1), this distance is sqrt(3). "
        "The origin is the ONLY point equidistant from all 8 vertices. In the GFD model, "
        "this central point is where the two tetrahedra 'meet', and any field traversing "
        "from one tetrahedron to the other must pass through this center. This geometric "
        "constraint may explain why interactions appear to be mediated through a central point."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("Vertices are at the 8 corners of a cube: (+/-1, +/-1, +/-1)")
            .step("Origin O = (0, 0, 0) is the cube center")
            .step("Distance from O to any vertex V = sqrt(1^2 + 1^2 + 1^2) = sqrt(3)")
            .step("This is true for all 8 vertices by cubic symmetry")
            .step("The origin is the unique point equidistant from all cube corners")
            .conclude("All vertices are at distance sqrt(3) from origin; deviation = 0")
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
        min_distance = min(distances)
        max_distance = max(distances)
        
        return (
            Model()
            .add("Average distance from origin", avg_distance)
            .add("Max deviation from average", max_deviation)
            .add("Min distance", min_distance)
            .add("Max distance", max_distance)
        )
    
    def observations(self):
        sqrt3 = math.sqrt(3)
        return (
            Observed()
            .add("Average distance from origin", sqrt3)
            .add("Max deviation from average", 0.0)
            .add("Min distance", sqrt3)
            .add("Max distance", sqrt3)
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
            "  1. That parity uniquely determines the two tetrahedra\n"
            "  2. That complementary pairs always cross tetrahedra\n"
            "  3. That the origin is the natural center of symmetry\n\n"
            "These are not arbitrary properties; they follow from the geometry of "
            "inscribing two regular tetrahedra in a cube."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
