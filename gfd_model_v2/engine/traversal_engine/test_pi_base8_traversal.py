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

import sys
import os
import math
from typing import Dict, Optional, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

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

class TraversalProducesSequence(GFDTest):
    """
    The traversal algorithm produces a deterministic vertex sequence
    from pi base-8 digits.
    """
    name = "Algorithm Produces Sequence"
    question = "Does the pi base-8 traversal algorithm produce a deterministic vertex sequence with correct step count?"
    reference_source = None  # Algorithm verification
    derivation = (
        "PREMISE: The algorithm should produce one state per input digit. "
        "STEP 1: Input N fractional digits plus 1 integer digit (3). "
        "STEP 2: For N=20, total inputs = 21 (1 integer + 20 fractional). "
        "STEP 3: Each input produces exactly one traversal state. "
        "STEP 4: Verify output count equals input count. "
        "OUTPUT: Steps produced = 21, produces sequence = 1."
    )
    commentary = None  # Algorithm verification
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(20)
        return {
            "Steps produced": len(results),
            "Expected steps": 21,  # 1 integer + 20 fractional
            "Produces sequence": 1 if len(results) == 21 else 0,
        }


class FirstVertexIsV3(GFDTest):
    """
    The traversal starts at V3 because pi's integer part is 3.
    This places the first step in Tet_B (even parity).
    """
    name = "First Vertex is V3"
    question = "Does traversal start at vertex V3 (cumsum=3 mod 8 = 3), placing the initial state in Tetrahedron B?"
    reference_source = "Pi integer part = 3"
    tolerance = 0.0
    derivation = (
        "PREMISE: Pi in base-8 begins with integer part 3. "
        "STEP 1: First digit is 3, so initial cumsum = 3. "
        "STEP 2: First vertex = cumsum mod 8 = 3 mod 8 = 3. "
        "STEP 3: V3 has binary 011, popcount=2 (even), so V3 ∈ Tet_B. "
        "OUTPUT: First vertex = 3, first tetrahedron = B."
    )
    commentary = (
        "Pi's integer part 3 determines the initial vertex V3, placing traversal "
        "in Tetrahedron B at the outset. This starting point follows deterministically "
        "from pi's mathematical value."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(5)
        first_vertex = results[0]['vertex']
        return {
            "First vertex": first_vertex,
            "First tetrahedron": 1 if results[0]['tetrahedron'] == 'B' else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "First vertex": 3,
            "First tetrahedron": 1,  # B
        }


class FirstTwoVerticesBimetric(GFDTest):
    """
    First two vertices (V3, V4) are from opposite tetrahedra,
    establishing bimetric coupling immediately.
    """
    name = "Bimetric Coupling (V3, V4)"
    question = "Do the first two vertices V3 and V4 belong to opposite tetrahedra, establishing bimetric coupling from the first step?"
    reference_source = "Bimetric structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: Bimetric coupling requires engagement of both Field Chambers. "
        "STEP 1: First vertex V3: binary 011, popcount=2 (even) → Tet_B. "
        "STEP 2: Second digit is 1, so cumsum = 3+1 = 4. "
        "STEP 3: Second vertex V4: binary 100, popcount=1 (odd) → Tet_A. "
        "STEP 4: V3 ∈ Tet_B and V4 ∈ Tet_A → different tetrahedra. "
        "OUTPUT: First vertex = 3, second vertex = 4, opposite tetrahedra = 1."
    )
    commentary = (
        "The immediate transition from Tetrahedron B to Tetrahedron A establishes "
        "bimetric coupling from the first step. This cross-chamber transition "
        "emerges from pi's first two digits without adjustment."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(5)
        v1 = results[0]['vertex']
        v2 = results[1]['vertex']
        tet1 = results[0]['tetrahedron']
        tet2 = results[1]['tetrahedron']
        
        opposite_tets = 1 if tet1 != tet2 else 0
        
        return {
            "First vertex": v1,
            "Second vertex": v2,
            "Opposite tetrahedra": opposite_tets,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "First vertex": 3,
            "Second vertex": 4,
            "Opposite tetrahedra": 1,
        }


class FirstPairComplementary(GFDTest):
    """
    First pair (3, 4) sums to 7. In the model, vertex pairs summing to 7
    are termed complementary, as their binary representations are bitwise
    complements (e.g., 3=011 and 4=100, XOR gives 111=7).
    """
    name = "First Pair is Complementary"
    question = "Do vertices V3 and V4 form a complementary pair (sum=7), with binary representations that are bitwise complements?"
    reference_source = "Complementary pair structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: Complementary vertices have binary representations that XOR to 111. "
        "STEP 1: V3 = 3 = 011 in binary. "
        "STEP 2: V4 = 4 = 100 in binary. "
        "STEP 3: 011 XOR 100 = 111 = 7. "
        "STEP 4: Equivalently: V3 + V4 = 3 + 4 = 7. "
        "OUTPUT: Pair sum = 7."
    )
    commentary = (
        "V3 (011) and V4 (100) are bitwise complements XORing to 111. This "
        "complementary pairing at the first transition suggests pi naturally "
        "encodes geometric opposition into the initial traversal step."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(5)
        v1 = results[0]['vertex']
        v2 = results[1]['vertex']
        pair_sum = v1 + v2
        
        return {
            "First vertex": v1,
            "Second vertex": v2,
            "Pair sum": pair_sum,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "First vertex": 3,
            "Second vertex": 4,
            "Pair sum": 7,
        }


class ThreePlusOneEncoding(GFDTest):
    """
    Pi's first digits (3.1) sum to 4, which the model associates with
    the coupling constant k=4 (the number of faces on a tetrahedron).
    This numerical coincidence is noted but not claimed as causal.
    """
    name = "3+1 Spacetime Encoding"
    question = "Do pi's first two digits (3 and 1) sum to k=4, numerically corresponding to 3+1 spacetime dimensionality?"
    reference_source = "3+1 spacetime structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: The model's topology constant k=4 governs tetrahedral structure. "
        "STEP 1: Pi's integer part = 3. "
        "STEP 2: Pi's first fractional digit = 1. "
        "STEP 3: Sum = 3 + 1 = 4 = k. "
        "STEP 4: This also corresponds to 3 spatial + 1 time dimension. "
        "OUTPUT: First digit = 3, second digit = 1, sum (k) = 4."
    )
    commentary = (
        "Pi's first digits summing to 4 corresponds to the topology constant k "
        "and the 3+1 dimensional structure of spacetime. This numerical "
        "correspondence is documented without claiming causal connection."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(5)
        first_digit = results[0]['digit']  # 3
        second_digit = results[1]['digit']  # 1
        encoding_sum = first_digit + second_digit
        
        return {
            "First digit": first_digit,
            "Second digit": second_digit,
            "Sum (k)": encoding_sum,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "First digit": 3,
            "Second digit": 1,
            "Sum (k)": 4,
        }


class OrbitCompletesAtMultiplesOf8(GFDTest):
    """
    Orbits complete when cumsum reaches multiples of 8.
    This corresponds to a return to vertex V0.
    """
    name = "Orbit at Cumsum Multiples of 8"
    question = "Do all orbit completions occur precisely when cumsum reaches a multiple of 2k=8, returning to vertex V0?"
    reference_source = "8-vertex structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: An orbit represents one complete cycle through the 2k=8 vertex space. "
        "STEP 1: Orbit completion is flagged when cumsum mod 8 = 0 (after cumsum > 0). "
        "STEP 2: This means cumsum = 8n for some positive integer n. "
        "STEP 3: At these points, vertex = cumsum mod 8 = 0, which is V0. "
        "STEP 4: Verify all flagged orbit completions have cumsum divisible by 8. "
        "OUTPUT: All multiples of 8 = 1."
    )
    commentary = (
        "Orbit completion at cumsum multiples of 8 reflects the cyclic structure "
        "of the 8-vertex Field Chamber. Each return to V0 marks completion of one "
        "traversal cycle through vertex space."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(50)
        
        completions = [(r['orbit'], r['cumsum']) for r in results if r['orbit_complete']]
        
        all_multiples_of_8 = all(c[1] % 8 == 0 for c in completions)
        
        return {
            "Orbits found": len(completions),
            "All multiples of 8": 1 if all_multiples_of_8 else 0,
        }
    
    def observations(self) -> Optional[Dict[str, float]]:
        # The number of orbits depends on the digit sequence
        # The important invariant is that ALL are multiples of 8
        return None  # Model-only - verifies invariant holds


class AllVerticesVisited(GFDTest):
    """
    All 8 vertices (0-7) are visited during traversal.
    Pi's digit diversity ensures complete vertex coverage.
    """
    name = "All 8 Vertices Visited"
    question = "Are all 2k=8 vertices (0 through 7) visited during extended traversal, ensuring complete geometric coverage?"
    reference_source = "Complete vertex coverage"
    tolerance = 0.0
    derivation = (
        "PREMISE: Ergodic traversal requires visiting all regions of the state space. "
        "STEP 1: The state space consists of 8 vertices {0,1,2,3,4,5,6,7}. "
        "STEP 2: Pi's digit diversity (all values 0-7 appear) enables reaching any vertex. "
        "STEP 3: Track unique vertices visited during traversal. "
        "STEP 4: Verify the visited set equals {0,1,2,3,4,5,6,7} after sufficient steps. "
        "OUTPUT: Unique vertices = 8, all 8 visited = 1."
    )
    commentary = (
        "Complete vertex visitation confirms pi-driven traversal samples all "
        "regions of the Field Chamber. This ergodic coverage is necessary for "
        "the traversal to encode complete geometric information."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(50)
        visited = set(r['vertex'] for r in results)
        
        return {
            "Unique vertices": len(visited),
            "All 8 visited": 1 if visited == {0,1,2,3,4,5,6,7} else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Unique vertices": 8,
            "All 8 visited": 1,
        }


class TetrahedraInterleaved(GFDTest):
    """
    The traversal visits both tetrahedra in interleaved fashion,
    not one then the other.
    """
    name = "Tetrahedra Interleaved"
    question = "Does traversal visit both tetrahedra in an interleaved fashion (multiple visits to each) rather than sequentially?"
    reference_source = "Bimetric coupling"
    derivation = (
        "PREMISE: Continuous bimetric coupling requires interleaved engagement. "
        "STEP 1: Count visits to Tet A vertices {1,2,4,7} during first 20 steps. "
        "STEP 2: Count visits to Tet B vertices {0,3,5,6} during first 20 steps. "
        "STEP 3: Check that both counts exceed 3 (not just 1-2 visits). "
        "STEP 4: Multiple visits to each tetrahedron confirms interleaving. "
        "OUTPUT: Both visited (>3 each) = 1."
    )
    commentary = (
        "Interleaved Field Chamber visitation demonstrates the traversal couples "
        "both tetrahedra throughout, rather than exhausting one before addressing "
        "the other. This continuous bimetric engagement reflects the dual structure."
    )
    
    def model(self) -> Dict[str, float]:
        results = traverse_pi_base8(20)
        tet_a_visits = sum(1 for r in results if r['tetrahedron'] == 'A')
        tet_b_visits = sum(1 for r in results if r['tetrahedron'] == 'B')
        
        both_visited = 1 if (tet_a_visits > 3 and tet_b_visits > 3) else 0
        
        return {
            "Tet A visits": tet_a_visits,
            "Tet B visits": tet_b_visits,
            "Both visited (>3 each)": both_visited,
        }


class Integer3Required(GFDTest):
    """
    Including the integer 3 is required for bimetric coupling.
    Without it, the first pair would not be complementary.
    """
    name = "Integer 3 Required for Coupling"
    question = "Does omitting pi's integer part 3 break the complementary pair structure, demonstrating the integer is essential?"
    reference_source = "Bimetric initialization"
    tolerance = 0.0
    derivation = (
        "PREMISE: The complementary pair structure depends on including the integer 3. "
        "STEP 1: WITH integer 3: first digits [3,1], cumsum=[3,4], vertices=[3,4], sum=7 (complementary). "
        "STEP 2: WITHOUT integer 3: first digits [1,1], cumsum=[1,2], vertices=[1,2], sum=3 (not 7). "
        "STEP 3: Compare: 3+4=7 (complementary) vs 1+2=3 (not complementary). "
        "OUTPUT: With 3 sum = 7, without 3 sum = 3, with 3 complementary = 1, without 3 complementary = 0."
    )
    commentary = (
        "Omitting pi's integer part disrupts the complementary pair structure, "
        "demonstrating the specific mathematical value of pi contributes to the "
        "model's bimetric initialization. The integer 3 is not an arbitrary choice."
    )
    
    def model(self) -> Dict[str, float]:
        with_3 = traverse_pi_base8(5, include_integer=True)
        without_3 = traverse_pi_base8(5, include_integer=False)
        
        v1_with = with_3[0]['vertex']
        v2_with = with_3[1]['vertex']
        sum_with = v1_with + v2_with
        
        v1_without = without_3[0]['vertex']
        v2_without = without_3[1]['vertex']
        sum_without = v1_without + v2_without
        
        return {
            "With 3 sum": sum_with,
            "Without 3 sum": sum_without,
            "With 3 complementary": 1 if sum_with == 7 else 0,
            "Without 3 complementary": 1 if sum_without == 7 else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "With 3 sum": 7,
            "Without 3 sum": 3,  # vertex 1 + vertex 2 = 3
            "With 3 complementary": 1,
            "Without 3 complementary": 0,
        }


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


def run_all_tests() -> bool:
    """Run all pi base-8 traversal tests."""
    return run_test_group(
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
    success = run_all_tests()
    sys.exit(0 if success else 1)
