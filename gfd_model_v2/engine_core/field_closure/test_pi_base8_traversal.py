"""
Pi Base-8 Traversal Algorithm
=============================

The core traversal algorithm uses pi base-8 digits to drive vertex
transitions through the stellated octahedron. Each digit (0-7) advances
the cumulative sum, with the current vertex given by cumsum mod 8.

The model includes pi's integer part (3) in the traversal. This places
the first vertex at V3 (Tetrahedron B), and the second at V4 (Tetrahedron A),
creating an immediate transition between tetrahedra. These tests verify
the algorithm's deterministic behavior and vertex coverage properties.
"""

from typing import Dict, Optional, List

from gfd_model_v2.framework import *

# =============================================================================
# CONSTANTS
# =============================================================================

# Pi base-8 fractional digits (first 100)
PI_BASE8_FRACTIONAL = [
    1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, 0, 2, 1, 5,
    1, 4, 2, 3, 0, 5, 5, 4, 5, 4, 1, 2, 2, 0, 3, 5, 2, 3, 4, 6,
    5, 4, 2, 1, 1, 3, 2, 6, 7, 2, 2, 3, 0, 1, 4, 6, 5, 4, 4, 0,
    6, 3, 4, 5, 6, 0, 6, 2, 3, 6, 5, 6, 3, 6, 6, 1, 0, 1, 5, 5,
    2, 3, 7, 2, 1, 5, 1, 6, 4, 5, 6, 7, 4, 2, 3, 7, 3, 2, 4, 2,
]

# Tet A = odd parity vertices
TET_A = {1, 2, 4, 7}
# Tet B = even parity vertices
TET_B = {0, 3, 5, 6}


def get_pi_base8(n_digits, include_integer=True):
    """Get pi base-8 digits."""
    if include_integer:
        return [3] + PI_BASE8_FRACTIONAL[:n_digits]
    return PI_BASE8_FRACTIONAL[:n_digits]


def get_tetrahedron(vertex):
    """Get tetrahedron assignment for vertex."""
    return 'A' if vertex in TET_A else 'B'


def traverse_pi_base8(n_digits, include_integer=True):
    """Execute traversal and return step-by-step results."""
    digits = get_pi_base8(n_digits, include_integer)
    results = []
    cumsum = 0
    
    for step, digit in enumerate(digits):
        cumsum += digit
        vertex = cumsum % 8
        tet = get_tetrahedron(vertex)
        orbit = cumsum // 8
        orbit_complete = cumsum > 0 and cumsum % 8 == 0
        
        results.append({
            'step': step,
            'digit': digit,
            'cumsum': cumsum,
            'vertex': vertex,
            'tetrahedron': tet,
            'orbit': orbit,
            'orbit_complete': orbit_complete,
        })
    
    return results


# =============================================================================
# TESTS
# =============================================================================

class TraversalProducesSequence(Test):
    """
    The traversal algorithm produces a deterministic vertex sequence
    from pi base-8 digits.
    """
    name = "Algorithm Produces Sequence"
    question = (
        "Does the algorithm work at all? "
        "Given pi's digits, we should get a sequence of vertex states, one per digit. "
        "This test verifies the algorithm produces the expected number of steps."
    )
    reference = None  # Algorithm verification
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The algorithm should produce one state per input digit.")
            .step("Input N fractional digits plus 1 integer digit (3).")
            .step("For N=20, total inputs = 21 (1 integer + 20 fractional).")
            .step("Each input produces exactly one traversal state.")
            .step("Verify output count equals input count.")
            .conclude("Steps produced = 21, produces sequence = 1.")
        )
    
    commentary = (
        "This is the most basic sanity check: does the machine produce output? "
        "Feed it 21 digits, get 21 steps. No more, no less. "
        "If this fails, nothing else matters."
    )
    
    def model(self):
        results = traverse_pi_base8(20)
        return (
            Model()
            .add("Steps produced", len(results))
            .add("Expected steps", 21)  # 1 integer + 20 fractional
            .add("Produces sequence", 1 if len(results) == 21 else 0)
        )


class FirstVertexIsV3(Test):
    """
    The traversal starts at V3 because pi's integer part is 3.
    This places the first step in Tet_B (even parity).
    """
    name = "First Vertex is V3"
    question = (
        "Where does the traversal begin? "
        "Pi starts with 3 (in base 8: 3.11037...), so the first vertex is V3. "
        "This test confirms we land on V3, which is in Tetrahedron B."
    )
    reference = "Pi integer part = 3"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Pi in base-8 begins with integer part 3.")
            .step("First digit is 3, so initial cumsum = 3.")
            .step("First vertex = cumsum mod 8 = 3 mod 8 = 3.")
            .step("V3 has binary 011, popcount=2 (even), so V3 in Tet_B.")
            .conclude("First vertex = 3, first tetrahedron = B.")
        )
    
    commentary = (
        "The very first step is determined by pi itself: 3 in base 8. "
        "So we start at vertex 3. This is not arbitrary. "
        "The universe (if this model means anything) starts in Tetrahedron B."
    )
    
    def model(self):
        results = traverse_pi_base8(5)
        first_vertex = results[0]['vertex']
        return (
            Model()
            .add("First vertex", first_vertex)
            .add("First tetrahedron", 1 if results[0]['tetrahedron'] == 'B' else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("First vertex", 3)
            .add("First tetrahedron", 1)  # B
        )


class FirstTwoVerticesBimetric(Test):
    """
    First two vertices (V3, V4) are from opposite tetrahedra,
    establishing bimetric coupling immediately.
    """
    name = "Bimetric Coupling (V3, V4)"
    question = (
        "Does the traversal immediately engage both tetrahedra? "
        "V3 is in Tet B, V4 is in Tet A. If the first two steps cross between tetrahedra, "
        "bimetric coupling is established from the start."
    )
    reference = "Bimetric structure"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Bimetric coupling requires engagement of both Field Chambers.")
            .step("First vertex V3: binary 011, popcount=2 (even) -> Tet_B.")
            .step("Second digit is 1, so cumsum = 3+1 = 4.")
            .step("Second vertex V4: binary 100, popcount=1 (odd) -> Tet_A.")
            .step("V3 in Tet_B and V4 in Tet_A -> different tetrahedra.")
            .conclude("First vertex = 3, second vertex = 4, opposite tetrahedra = 1.")
        )
    
    commentary = (
        "From the very first step, we jump from one tetrahedron to the other: "
        "V3 (Tet B) to V4 (Tet A). This immediate cross-talk is not a coincidence; "
        "it emerges directly from pi's digits (3, then 1, giving cumsum 4). "
        "Bimetric coupling is baked in from the beginning."
    )
    
    def model(self):
        results = traverse_pi_base8(5)
        v1 = results[0]['vertex']
        v2 = results[1]['vertex']
        tet1 = results[0]['tetrahedron']
        tet2 = results[1]['tetrahedron']
        
        opposite_tets = 1 if tet1 != tet2 else 0
        
        return (
            Model()
            .add("First vertex", v1)
            .add("Second vertex", v2)
            .add("Opposite tetrahedra", opposite_tets)
        )
    
    def observations(self):
        return (
            Observed()
            .add("First vertex", 3)
            .add("Second vertex", 4)
            .add("Opposite tetrahedra", 1)
        )


class FirstPairComplementary(Test):
    """
    First pair (3, 4) sums to 7. In the model, vertex pairs summing to 7
    are termed complementary, as their binary representations are bitwise
    complements (e.g., 3=011 and 4=100, XOR gives 111=7).
    """
    name = "First Pair is Complementary"
    question = (
        "Are V3 and V4 'complementary' vertices? "
        "Two vertices are complementary if their indices sum to 7 (binary opposites). "
        "3 + 4 = 7, so the first pair is indeed complementary."
    )
    reference = "Complementary pair structure"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Complementary vertices have binary representations that XOR to 111.")
            .step("V3 = 3 = 011 in binary.")
            .step("V4 = 4 = 100 in binary.")
            .step("011 XOR 100 = 111 = 7.")
            .step("Equivalently: V3 + V4 = 3 + 4 = 7.")
            .conclude("Pair sum = 7.")
        )
    
    commentary = (
        "Write 3 in binary: 011. Write 4 in binary: 100. "
        "They are exact opposites (flip every bit to get from one to the other). "
        "XOR them: 011 XOR 100 = 111 = 7. Or just add: 3 + 4 = 7. "
        "The first transition lands on a 'complementary pair,' "
        "suggesting pi encodes geometric opposition right away."
    )
    
    def model(self):
        results = traverse_pi_base8(5)
        v1 = results[0]['vertex']
        v2 = results[1]['vertex']
        pair_sum = v1 + v2
        
        return (
            Model()
            .add("First vertex", v1)
            .add("Second vertex", v2)
            .add("Pair sum", pair_sum)
        )
    
    def observations(self):
        return (
            Observed()
            .add("First vertex", 3)
            .add("Second vertex", 4)
            .add("Pair sum", 7)
        )


class ThreePlusOneEncoding(Test):
    """
    Pi's first digits (3.1) sum to 4, which the model associates with
    the coupling constant k=4 (the number of faces on a tetrahedron).
    This numerical coincidence is noted but not claimed as causal.
    """
    name = "3+1 Spacetime Encoding"
    question = (
        "Is there a '3+1' pattern in pi's first digits? "
        "Pi starts with 3.1... in base 8. 3 + 1 = 4, which matches k=4 (tetrahedron faces) "
        "and 3+1 dimensional spacetime. Coincidence or not, the test notes it."
    )
    reference = "3+1 spacetime structure"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The model's topology constant k=4 governs tetrahedral structure.")
            .step("Pi's integer part = 3.")
            .step("Pi's first fractional digit = 1.")
            .step("Sum = 3 + 1 = 4 = k.")
            .step("This also corresponds to 3 spatial + 1 time dimension.")
            .conclude("First digit = 3, second digit = 1, sum (k) = 4.")
        )
    
    commentary = (
        "Physics operates in 3+1 dimensions: 3 spatial, 1 temporal. "
        "Pi in base 8 starts: 3.1... The first two digits sum to 4. "
        "A tetrahedron has 4 faces. We are not claiming pi 'knows' about spacetime, "
        "but this numerical echo is at least interesting to document."
    )
    
    def model(self):
        results = traverse_pi_base8(5)
        first_digit = results[0]['digit']  # 3
        second_digit = results[1]['digit']  # 1
        encoding_sum = first_digit + second_digit
        
        return (
            Model()
            .add("First digit", first_digit)
            .add("Second digit", second_digit)
            .add("Sum (k)", encoding_sum)
        )
    
    def observations(self):
        return (
            Observed()
            .add("First digit", 3)
            .add("Second digit", 1)
            .add("Sum (k)", 4)
        )


class OrbitCompletesAtMultiplesOf8(Test):
    """
    Orbits complete when cumsum reaches multiples of 8.
    This corresponds to a return to vertex V0.
    """
    name = "Orbit at Cumsum Multiples of 8"
    question = (
        "When do orbits complete? "
        "An orbit finishes when cumsum hits a multiple of 8 (8, 16, 24...). "
        "This test verifies all orbit completions occur at these exact boundaries."
    )
    reference = "8-vertex structure"
    tolerance = 0.0
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: An orbit represents one complete cycle through the 2k=8 vertex space.")
            .step("Orbit completion is flagged when cumsum mod 8 = 0 (after cumsum > 0).")
            .step("This means cumsum = 8n for some positive integer n.")
            .step("At these points, vertex = cumsum mod 8 = 0, which is V0.")
            .step("Verify all flagged orbit completions have cumsum divisible by 8.")
            .conclude("All multiples of 8 = 1.")
        )
    
    commentary = (
        "Think of a clock with 8 hours instead of 12. Each time the hand completes "
        "a full circle (8 hours), an orbit is complete. Cumsum = 8 means one orbit, "
        "cumsum = 16 means two orbits, and so on. The test ensures we only flag "
        "orbit completions when cumsum is exactly divisible by 8."
    )
    
    def model(self):
        results = traverse_pi_base8(50)
        
        completions = [(r['orbit'], r['cumsum']) for r in results if r['orbit_complete']]
        
        all_multiples_of_8 = all(c[1] % 8 == 0 for c in completions)
        
        return (
            Model()
            .add("Orbits found", len(completions))
            .add("All multiples of 8", 1 if all_multiples_of_8 else 0)
        )


class AllVerticesVisited(Test):
    """
    All 8 vertices (0-7) are visited during traversal.
    Pi's digit diversity ensures complete vertex coverage.
    """
    name = "All 8 Vertices Visited"
    question = (
        "Does the traversal visit every vertex? "
        "There are 8 vertices (0 through 7). If some are never visited, we have incomplete coverage. "
        "This test verifies all 8 vertices are reached during traversal."
    )
    reference = "Complete vertex coverage"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Ergodic traversal requires visiting all regions of the state space.")
            .step("The state space consists of 8 vertices {0,1,2,3,4,5,6,7}.")
            .step("Pi's digit diversity (all values 0-7 appear) enables reaching any vertex.")
            .step("Track unique vertices visited during traversal.")
            .step("Verify the visited set equals {0,1,2,3,4,5,6,7} after sufficient steps.")
            .conclude("Unique vertices = 8, all 8 visited = 1.")
        )
    
    commentary = (
        "A mailman who never delivers to certain houses is not doing the job. "
        "Our traversal must visit all 8 'houses' (vertices). "
        "Because pi's base-8 digits include all values from 0 to 7, "
        "we can eventually reach any vertex. This test confirms no vertex is left out."
    )
    
    def model(self):
        results = traverse_pi_base8(50)
        visited = set(r['vertex'] for r in results)
        
        return (
            Model()
            .add("Unique vertices", len(visited))
            .add("All 8 visited", 1 if visited == {0,1,2,3,4,5,6,7} else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Unique vertices", 8)
            .add("All 8 visited", 1)
        )


class TetrahedraInterleaved(Test):
    """
    The traversal visits both tetrahedra in interleaved fashion,
    not one then the other.
    """
    name = "Tetrahedra Interleaved"
    question = (
        "Does the traversal bounce between tetrahedra, or stay in one? "
        "Interleaving means alternating or mixing visits to Tet A and Tet B, "
        "not finishing one before starting the other. This test checks for interleaving."
    )
    reference = "Bimetric coupling"
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Continuous bimetric coupling requires interleaved engagement.")
            .step("Count visits to Tet A vertices {1,2,4,7} during first 20 steps.")
            .step("Count visits to Tet B vertices {0,3,5,6} during first 20 steps.")
            .step("Check that both counts exceed 3 (not just 1-2 visits).")
            .step("Multiple visits to each tetrahedron confirms interleaving.")
            .conclude("Both visited (>3 each) = 1.")
        )
    
    commentary = (
        "Imagine a tennis match where each player hits the ball back and forth. "
        "That is interleaving. If one player hit 20 times in a row, then the other, "
        "that would be sequential. Our traversal should interleave: "
        "jumping between Tet A and Tet B repeatedly, not camping in one."
    )
    
    def model(self):
        results = traverse_pi_base8(20)
        tet_a_visits = sum(1 for r in results if r['tetrahedron'] == 'A')
        tet_b_visits = sum(1 for r in results if r['tetrahedron'] == 'B')
        
        both_visited = 1 if (tet_a_visits > 3 and tet_b_visits > 3) else 0
        
        return (
            Model()
            .add("Tet A visits", tet_a_visits)
            .add("Tet B visits", tet_b_visits)
            .add("Both visited (>3 each)", both_visited)
        )


class Integer3Required(Test):
    """
    Including the integer 3 is required for bimetric coupling.
    Without it, the first pair would not be complementary.
    """
    name = "Integer 3 Required for Coupling"
    question = (
        "Why include the integer part (3) of pi? "
        "Without it, the first two vertices would be V1 and V2 (sum = 3), not complementary. "
        "With it, we get V3 and V4 (sum = 7), a complementary pair. The integer matters."
    )
    reference = "Bimetric initialization"
    tolerance = 0.0
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The complementary pair structure depends on including the integer 3.")
            .step("WITH integer 3: first digits [3,1], cumsum=[3,4], vertices=[3,4], sum=7 (complementary).")
            .step("WITHOUT integer 3: first digits [1,1], cumsum=[1,2], vertices=[1,2], sum=3 (not 7).")
            .step("Compare: 3+4=7 (complementary) vs 1+2=3 (not complementary).")
            .conclude("With 3 sum = 7, without 3 sum = 3, with 3 complementary = 1, without 3 complementary = 0.")
        )
    
    commentary = (
        "You might wonder: why not start at pi's fractional part (0.11037...)? "
        "Then the first digits are 1, 1, giving vertices V1, V2. Their sum is 3, not 7: "
        "not a complementary pair. Including pi's integer (3) shifts everything: "
        "we get V3, V4, summing to 7 (complementary). The integer is essential."
    )
    
    def model(self):
        with_3 = traverse_pi_base8(5, include_integer=True)
        without_3 = traverse_pi_base8(5, include_integer=False)
        
        v1_with = with_3[0]['vertex']
        v2_with = with_3[1]['vertex']
        sum_with = v1_with + v2_with
        
        v1_without = without_3[0]['vertex']
        v2_without = without_3[1]['vertex']
        sum_without = v1_without + v2_without
        
        return (
            Model()
            .add("With 3 sum", sum_with)
            .add("Without 3 sum", sum_without)
            .add("With 3 complementary", 1 if sum_with == 7 else 0)
            .add("Without 3 complementary", 1 if sum_without == 7 else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("With 3 sum", 7)
            .add("Without 3 sum", 3)  # vertex 1 + vertex 2 = 3
            .add("With 3 complementary", 1)
            .add("Without 3 complementary", 0)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    TraversalProducesSequence,
    FirstVertexIsV3,
    FirstTwoVerticesBimetric,
    FirstPairComplementary,
    ThreePlusOneEncoding,
    OrbitCompletesAtMultiplesOf8,
    AllVerticesVisited,
    TetrahedraInterleaved,
    Integer3Required,
]


def run_all():
    """Run all pi base-8 traversal tests."""
    return run_tests(
        title="Pi Base-8 Traversal Algorithm",
        summary=(
            "The traversal algorithm uses pi base-8 digits to step through the stellated "
            "octahedron's 8 vertices. Each digit advances a cumulative sum, with the current "
            "vertex given by cumsum mod 8. Including pi's integer part (3) places the first "
            "vertex at V3 and the second at V4, which belong to opposite tetrahedra. These "
            "tests verify the algorithm's deterministic behavior, vertex coverage, and the "
            "structure of the traversal sequence."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
