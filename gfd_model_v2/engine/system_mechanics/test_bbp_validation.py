"""
BBP Formula Validation
======================

This module validates the Bailey-Borwein-Plouffe formula (base 16) and examines
its consistency with base-8 traversal. Both bases correspond to k=4 tetrahedral
topology parameters.

Key relationships examined:
- Base 16 = 4k (tetrahedral multiple)
- Base 8 = 2k (vertex count multiple)
- Both bases visit all 8 dual Field Chamber vertices
"""

import sys
import os
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from common import K, pi_base_8, pi_base_16


# =============================================================================
# TESTS
# =============================================================================

class Base16Is4K(GFDTest):
    """Base 16 equals 4k where k=4."""
    name = "Base 16 = 4k"
    question = "Does the hexadecimal base 16 arise naturally from the k=4 topology constant as 4 times k?"
    reference_source = "Theoretical (k=4)"
    tolerance = 0.001
    derivation = (
        "PREMISE: From Field Closure, k=4 is the tetrahedral face count (Field Closure constant). "
        "STEP 1: The BBP formula uses base 16 for digit extraction. "
        "STEP 2: Calculate 4 times k: 4 * 4 = 16. "
        "STEP 3: Verify equality: base 16 = 4k. "
        "OUTPUT: Hexadecimal representation emerges naturally from tetrahedral k=4 topology."
    )
    commentary = (
        "The relationship 16 = 4k where k=4 connects hexadecimal representation "
        "to tetrahedral topology. This correspondence suggests base-16 arithmetic "
        "may have natural affinity with structures built from k=4 geometry."
    )
    
    def model(self) -> Dict[str, float]:
        return {
            "Base 16": 16,
            "4 x k": 4 * K,
            "k value": K,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Base 16": 16,
            "4 x k": 16,
            "k value": 4,
        }


class Base8Is2K(GFDTest):
    """Base 8 equals 2k where k=4."""
    name = "Base 8 = 2k"
    question = "Does base-8 (octal) equal 2k, matching the vertex count of the stellated octahedron Field Chamber?"
    reference_source = "Theoretical (k=4)"
    tolerance = 0.001
    derivation = (
        "PREMISE: The stellated octahedron has two tetrahedra with k=4 vertices each. "
        "STEP 1: Calculate total vertices: k + k = 2k = 2 * 4 = 8. "
        "STEP 2: Pi base-8 traversal uses digits 0-7, requiring exactly 8 values. "
        "STEP 3: Verify equality: base 8 = 2k. "
        "OUTPUT: Octal representation matches the dual Field Chamber vertex count of 2k=8."
    )
    commentary = (
        "Base-8 equals 2k, corresponding to the vertex count of the stellated "
        "octahedron (two tetrahedra, each with k=4 vertices). This relationship "
        "connects octal representation directly to dual Field Chamber structure."
    )
    
    def model(self) -> Dict[str, float]:
        return {
            "Base 8": 8,
            "2 x k": 2 * K,
            "k value": K,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Base 8": 8,
            "2 x k": 8,
            "k value": 4,
        }


class PiBase16Valid(GFDTest):
    """Pi base-16 produces valid hexadecimal digits (0-15)."""
    name = "Pi Base-16 Digits Valid"
    question = "Does the BBP algorithm produce valid hexadecimal digits (0-15) for pi, ensuring proper base-16 representation?"
    reference_source = None  # Validation check
    derivation = (
        "PREMISE: Hexadecimal digits must be in range 0-15 for valid base-16 representation. "
        "STEP 1: Extract 50 pi base-16 digits using the BBP algorithm. "
        "STEP 2: Find minimum and maximum digit values. "
        "STEP 3: Verify all digits satisfy: 0 <= digit <= 15. "
        "OUTPUT: All digits in valid range confirms correct algorithm implementation."
    )
    commentary = None  # Mechanical validation of digit range
    
    def model(self) -> Dict[str, float]:
        digits = pi_base_16(50)
        min_digit = min(digits)
        max_digit = max(digits)
        all_valid = 1 if all(0 <= d <= 15 for d in digits) else 0
        return {
            "Minimum digit": min_digit,
            "Maximum digit": max_digit,
            "All valid (1=yes)": all_valid,
        }


class PiBase8Valid(GFDTest):
    """Pi base-8 produces valid octal digits (0-7)."""
    name = "Pi Base-8 Digits Valid"
    question = "Does pi base-8 produce valid octal digits (0-7), ensuring each digit maps to exactly one Field Chamber vertex?"
    reference_source = None  # Validation check
    derivation = (
        "PREMISE: Octal digits must be in range 0-7, matching the 8 vertices of the stellated octahedron. "
        "STEP 1: Extract 50 pi base-8 digits. "
        "STEP 2: Find minimum and maximum digit values. "
        "STEP 3: Verify all digits satisfy: 0 <= digit <= 7. "
        "OUTPUT: Valid digit range ensures each pi digit addresses exactly one Field Chamber vertex."
    )
    commentary = None  # Mechanical validation of digit range
    
    def model(self) -> Dict[str, float]:
        digits = pi_base_8(50)
        min_digit = min(digits)
        max_digit = max(digits)
        all_valid = 1 if all(0 <= d <= 7 for d in digits) else 0
        return {
            "Minimum digit": min_digit,
            "Maximum digit": max_digit,
            "All valid (1=yes)": all_valid,
        }


class BothBasesVisitAllVertices(GFDTest):
    """Both bases visit all 8 vertices when computing cumsum mod 8."""
    name = "Both Bases Visit All Vertices"
    question = "Do both base-8 and base-16 pi traversals achieve ergodic coverage of all 8 Field Chamber vertices?"
    reference_source = "Theoretical (8 vertices)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Complete Field Chamber coverage requires visiting all 8 vertices (0-7). "
        "STEP 1: For base-8, compute cumulative sum of pi digits mod 8, track unique vertices visited. "
        "STEP 2: For base-16, compute cumulative sum of pi digits mod 8, track unique vertices visited. "
        "STEP 3: Verify both traversals visit all 8 vertices: {0, 1, 2, 3, 4, 5, 6, 7}. "
        "OUTPUT: Both bases produce ergodic traversal covering the complete dual Field Chamber."
    )
    commentary = (
        "Both base-8 and base-16 representations of pi produce complete vertex "
        "coverage when reduced modulo 8. This ergodic property ensures traversal "
        "samples the entire dual Field Chamber structure regardless of base choice."
    )
    
    def model(self) -> Dict[str, float]:
        # Base 8
        digits_8 = pi_base_8(100)
        cumsum_8 = 0
        vertices_8 = set()
        for d in digits_8:
            cumsum_8 += d
            vertices_8.add(cumsum_8 % 8)
        
        # Base 16
        digits_16 = pi_base_16(100)
        cumsum_16 = 0
        vertices_16 = set()
        for d in digits_16:
            cumsum_16 += d
            vertices_16.add(cumsum_16 % 8)
        
        return {
            "Base-8 unique vertices": len(vertices_8),
            "Base-16 unique vertices": len(vertices_16),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Base-8 unique vertices": 8,
            "Base-16 unique vertices": 8,
        }


class BBPCoefficientBalance(GFDTest):
    """BBP coefficients (+4, -2, -1, -1) sum to zero (balance)."""
    name = "BBP Coefficient Balance"
    question = "Do the BBP formula coefficients satisfy Field Closure balance by summing to zero?"
    reference_source = "BBP Formula"
    tolerance = 0.001
    derivation = (
        "PREMISE: Field Closure requires net flux to be zero (conservation). "
        "STEP 1: List BBP coefficients: +4, -2, -1, -1. "
        "STEP 2: Count coefficients: 4 positions (matching k=4). "
        "STEP 3: Sum: +4 + (-2) + (-1) + (-1) = 0. "
        "OUTPUT: Zero coefficient sum satisfies Field Closure balance requirement."
    )
    commentary = (
        "The BBP coefficients sum to zero, consistent with Field Closure balance. "
        "This zero-sum property in a formula for pi suggests the transcendental "
        "constant may encode conservation principles at a structural level."
    )
    
    def model(self) -> Dict[str, float]:
        coefficients = [4, -2, -1, -1]
        return {
            "Coefficient sum": sum(coefficients),
            "Coefficient count": len(coefficients),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Coefficient sum": 0,
            "Coefficient count": 4,
        }


class BBPOffsetsUnique(GFDTest):
    """BBP denominator offsets (1, 4, 5, 6) are all unique mod 8."""
    name = "BBP Offsets Unique"
    question = "Do the BBP denominator offsets {1, 4, 5, 6} address exactly k=4 unique positions within the 8-vertex Field Chamber cycle?"
    reference_source = "BBP Formula"
    tolerance = 0.001
    derivation = (
        "PREMISE: The Field Chamber has 8 vertices; BBP uses 4 positions per cycle. "
        "STEP 1: List BBP offsets: {1, 4, 5, 6}. "
        "STEP 2: Reduce each mod 8: {1, 4, 5, 6} (already less than 8). "
        "STEP 3: Count unique values: 4 unique offsets = k positions. "
        "OUTPUT: BBP addresses exactly k=4 unique vertices per cycle, leaving 4 unaddressed."
    )
    commentary = (
        "The four BBP offsets occupy distinct positions modulo 8, addressing half "
        "of the available vertex slots. This selective sampling pattern may relate "
        "to how pi encodes information through Tetrahedron A vertices specifically."
    )
    
    def model(self) -> Dict[str, float]:
        offsets = [1, 4, 5, 6]
        unique_mod_8 = len(set(o % 8 for o in offsets))
        return {
            "Offsets count": len(offsets),
            "Unique mod 8": unique_mod_8,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Offsets count": 4,
            "Unique mod 8": 4,
        }


class IntegerPartIs3(GFDTest):
    """Both bases give integer part of pi = 3."""
    name = "Integer Part = 3"
    question = "Does pi's integer part (3) place the initial traversal position at V3 in Tetrahedron B, enabling immediate cross-chamber coupling?"
    reference_source = "Mathematical (pi = 3.14159...)"
    tolerance = 0.001
    derivation = (
        "PREMISE: Pi = 3.14159... has integer part 3 in any base. "
        "STEP 1: In both base-8 and base-16, the first digit is 3. "
        "STEP 2: Initial cumsum = 3, so initial vertex = 3 mod 8 = V3. "
        "STEP 3: V3 is in Tetrahedron B (even parity vertices: {0, 3, 5, 6}). "
        "STEP 4: First fractional digit is 1, advancing to V4 (Tetrahedron A). "
        "OUTPUT: Pi's integer part 3 initiates traversal in Tet B; 3+1=k=4 links to topology constant."
    )
    commentary = (
        "Pi's integer part (3) initiates traversal at vertex V3, placing the first "
        "step in Tetrahedron B. When combined with the first fractional digit (1), "
        "the sum 3+1=4 corresponds to k, establishing an immediate connection to "
        "the topology constant."
    )
    
    def model(self) -> Dict[str, float]:
        digits_8 = pi_base_8(5)
        digits_16 = pi_base_16(5)
        return {
            "Base-8 integer part": digits_8[0],
            "Base-16 integer part": digits_16[0],
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Base-8 integer part": 3,
            "Base-16 integer part": 3,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    Base16Is4K,
    Base8Is2K,
    PiBase16Valid,
    PiBase8Valid,
    BothBasesVisitAllVertices,
    BBPCoefficientBalance,
    BBPOffsetsUnique,
    IntegerPartIs3,
]


def run_all_tests() -> bool:
    """Run all BBP validation tests."""
    return run_test_group(
        title="BBP Formula Validation",
        summary=(
            "These tests validate the Bailey-Borwein-Plouffe formula and examine its "
            "correspondence with k=4 tetrahedral topology. Base 16 equals 4k and base 8 "
            "equals 2k where k=4 is the topology constant. Both bases produce valid digits "
            "and visit all 8 dual Field Chamber vertices. The BBP coefficients sum to zero, "
            "consistent with Field Closure balance requirements."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
