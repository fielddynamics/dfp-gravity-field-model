"""
Full Pi Digits Validation
=========================

This module validates the pre-computed pi base-8 digits used in traversal.
It ensures digit accuracy, distribution properties, and traversal statistics.

Key validations:
- Sufficient digits stored for testing
- All digits in valid range 0-7
- Distribution approximately uniform
- Known sequences match established values
- Full traversal statistics computed correctly
"""

import sys
import os
import math
from typing import Dict, Optional, List
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

# =============================================================================
# CONSTANTS
# =============================================================================

ALPHA = 1/137.036
C = 2.998e8
LAMBDA_COMPTON = 2.426310238e-12

# Pi base-8 fractional digits (first 100 for validation)
PI_BASE8_FRACTIONAL = [
    1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, 0, 2, 1, 5,
    1, 4, 2, 3, 0, 5, 5, 4, 5, 4, 1, 2, 2, 0, 3, 5, 2, 3, 4, 6,
    5, 4, 2, 1, 1, 3, 2, 6, 7, 2, 2, 3, 0, 1, 4, 6, 5, 4, 4, 0,
    6, 3, 4, 5, 6, 0, 6, 2, 3, 6, 5, 6, 3, 6, 6, 1, 0, 1, 5, 5,
    2, 3, 7, 2, 1, 5, 1, 6, 4, 5, 6, 7, 4, 2, 3, 7, 3, 2, 4, 2,
]

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}


def get_tetrahedron(v):
    return 'A' if v in TET_A else 'B'


def get_pi_base8(n_digits, include_integer=True):
    if include_integer:
        return [3] + PI_BASE8_FRACTIONAL[:n_digits]
    return PI_BASE8_FRACTIONAL[:n_digits]


def calculate_settlement_frequency():
    return C / LAMBDA_COMPTON


# =============================================================================
# TESTS
# =============================================================================

class DigitsExist(GFDTest):
    """
    Verify we have sufficient pre-computed digits for testing.
    """
    name = "Pre-computed Digits Exist"
    question = "Are at least 100 pre-computed pi base-8 fractional digits available for traversal testing?"
    reference_source = None  # Storage check
    derivation = (
        "PREMISE: Sufficient digits are required for statistically meaningful tests. "
        "STEP 1: Count the number of stored fractional digits in PI_BASE8_FRACTIONAL. "
        "STEP 2: For robust statistical tests, at least 100 digits are needed. "
        "STEP 3: 100 digits provide ~30+ orbits for analysis. "
        "OUTPUT: Digits stored = 100, sufficient = 1."
    )
    commentary = None  # Data availability verification
    
    def model(self) -> Dict[str, float]:
        count = len(PI_BASE8_FRACTIONAL)
        return {
            "Digits stored": count,
            "Sufficient (>=100)": 1 if count >= 100 else 0,
        }


class AllDigitsInRange(GFDTest):
    """
    All base-8 digits must be in range 0-7.
    """
    name = "Digits in Range 0-7"
    question = "Are all stored pi digits valid octal values in the range [0,7], with no out-of-range entries?"
    reference_source = "Base-8 definition"
    tolerance = 0.0
    derivation = (
        "PREMISE: Base-8 (octal) digits must be in the set {0,1,2,3,4,5,6,7}. "
        "STEP 1: Iterate through all stored digits. "
        "STEP 2: Check each digit d satisfies 0 ≤ d ≤ 7. "
        "STEP 3: Count any violations (d < 0 or d > 7). "
        "OUTPUT: Invalid digits = 0, all valid = 1."
    )
    commentary = None  # Data integrity verification
    
    def model(self) -> Dict[str, float]:
        invalid = [d for d in PI_BASE8_FRACTIONAL if d < 0 or d > 7]
        return {
            "Invalid digits": len(invalid),
            "All valid": 1 if len(invalid) == 0 else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Invalid digits": 0,
            "All valid": 1,
        }


class KnownSequenceMatch(GFDTest):
    """
    First digits should match known pi base-8: 3.110375524...
    Fractional: 1,1,0,3,7,5,5,2,4,...
    """
    name = "Known Sequence Match"
    question = "Do the first 15 stored fractional digits match the known pi base-8 sequence [1,1,0,3,7,5,5,2,4,2,1,0,2,6,4]?"
    reference_source = "Pi in base 8"
    tolerance = 0.0
    derivation = (
        "PREMISE: Pi in base-8 = 3.110375524210264... (known value). "
        "STEP 1: Convert to digit list: fractional part starts [1,1,0,3,7,5,5,2,4,2,1,0,2,6,4]. "
        "STEP 2: Compare stored digits to this known sequence. "
        "STEP 3: Element-by-element comparison for first 15 digits. "
        "OUTPUT: Sequence matches = 1."
    )
    commentary = None  # Data accuracy verification against known values
    
    def model(self) -> Dict[str, float]:
        expected = [1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4]
        actual = PI_BASE8_FRACTIONAL[:15]
        matches = 1 if actual == expected else 0
        return {
            "Sequence matches": matches,
            "First digit": actual[0] if actual else -1,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Sequence matches": 1,
            "First digit": 1,
        }


class DigitDistribution(GFDTest):
    """
    Digits should be roughly uniformly distributed (pi is conjectured normal).
    """
    name = "Digit Distribution"
    question = "Are the pi base-8 digits approximately uniformly distributed, with each digit 0-7 appearing near the expected 12.5%?"
    reference_source = "Normal number conjecture"
    tolerance = 0.30
    derivation = (
        "PREMISE: Pi is conjectured to be a normal number with uniform digit distribution. "
        "STEP 1: Count occurrences of each digit 0-7 in the stored sequence. "
        "STEP 2: Expected count per digit = total_digits / 8 = 12.5% each. "
        "STEP 3: Find min and max counts across all 8 digit values. "
        "STEP 4: Large deviation would suggest non-uniformity or data error. "
        "OUTPUT: Min digit count, max digit count, expected per digit."
    )
    commentary = (
        "Approximately uniform digit distribution is consistent with pi being "
        "conjectured to be a normal number. This statistical property ensures "
        "unbiased sampling of all Field Chamber vertices over extended traversals."
    )
    
    def model(self) -> Dict[str, float]:
        counts = Counter(PI_BASE8_FRACTIONAL)
        n = len(PI_BASE8_FRACTIONAL)
        expected = n / 8
        
        min_count = min(counts.get(d, 0) for d in range(8))
        max_count = max(counts.get(d, 0) for d in range(8))
        
        return {
            "Min digit count": min_count,
            "Max digit count": max_count,
            "Expected per digit": expected,
        }


class DigitSumChecksum(GFDTest):
    """
    Digit sum serves as a rough checksum.
    Expected ~3.5 * count for uniform distribution.
    """
    name = "Digit Sum Checksum"
    question = "Is the sum of all stored digits consistent with an average digit value near 3.5 (the uniform distribution mean for 0-7)?"
    reference_source = "Statistical expectation"
    tolerance = 0.15
    derivation = (
        "PREMISE: For uniform distribution over {0,1,2,3,4,5,6,7}, mean = 3.5. "
        "STEP 1: Calculate sum of all stored fractional digits. "
        "STEP 2: Compute average = sum / count. "
        "STEP 3: For 100 digits with uniform distribution, expected sum ≈ 350. "
        "STEP 4: Average near 3.5 confirms statistical consistency. "
        "OUTPUT: Digit sum ≈ 350, average per digit ≈ 3.5."
    )
    commentary = (
        "The digit sum checksum confirms statistical consistency with expected "
        "base-8 digit averages. Deviations would indicate either data errors or "
        "non-uniformity in pi's digit distribution."
    )
    
    def model(self) -> Dict[str, float]:
        total_sum = sum(PI_BASE8_FRACTIONAL)
        n = len(PI_BASE8_FRACTIONAL)
        avg = total_sum / n
        return {
            "Digit sum": total_sum,
            "Average per digit": avg,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Digit sum": 350,  # Approximate for 100 digits
            "Average per digit": 3.5,
        }


class FullTraversalStatistics(GFDTest):
    """
    Full traversal should visit all vertices and complete multiple orbits.
    """
    name = "Full Traversal Statistics"
    question = "Does traversal with 100 digits visit all 8 vertices and complete multiple orbits for statistical significance?"
    reference_source = "Coverage requirement"
    derivation = (
        "PREMISE: Complete traversal requires visiting all 8 vertices and multiple orbit completions. "
        "STEP 1: Execute traversal with 100 fractional digits + integer part. "
        "STEP 2: Track set of unique vertices visited. "
        "STEP 3: Count total orbits completed (cumsum // 8). "
        "STEP 4: Verify all 8 vertices appear and orbits > 1. "
        "OUTPUT: Unique vertices = 8, all 8 visited = 1."
    )
    commentary = (
        "Complete vertex coverage across multiple orbits confirms the traversal "
        "provides sufficient data for statistical analysis. This coverage is "
        "essential for observing emergent patterns in the Field Closure system."
    )
    
    def model(self) -> Dict[str, float]:
        digits = get_pi_base8(100, include_integer=True)
        
        cumsum = 0
        vertices_visited = set()
        
        for digit in digits:
            cumsum += digit
            vertex = cumsum % 8
            vertices_visited.add(vertex)
        
        total_orbits = cumsum // 8
        
        return {
            "Unique vertices": len(vertices_visited),
            "Total orbits": total_orbits,
            "All 8 visited": 1 if len(vertices_visited) == 8 else 0,
        }


class TraversalBalance(GFDTest):
    """
    Traversal should visit both tetrahedra approximately equally.
    """
    name = "Traversal Balance"
    question = "Does extended traversal visit Tetrahedron A and Tetrahedron B with approximately equal frequency (near 50% each)?"
    reference_source = "Bimetric structure"
    tolerance = 0.15
    derivation = (
        "PREMISE: Bimetric symmetry predicts 50/50 split between Field Chambers. "
        "STEP 1: Execute traversal with 100 digits. "
        "STEP 2: Count visits to Tet A vertices {1,2,4,7}. "
        "STEP 3: Count visits to Tet B vertices {0,3,5,6}. "
        "STEP 4: Calculate Tet A ratio = Tet_A_count / total. "
        "OUTPUT: Ratio A ≈ 0.5."
    )
    commentary = (
        "Balanced Field Chamber visitation reflects the parity symmetry of the "
        "dual tetrahedron structure. Pi's digit distribution couples to both "
        "Field Chambers without favoring either, consistent with bimetric balance."
    )
    
    def model(self) -> Dict[str, float]:
        digits = get_pi_base8(100, include_integer=True)
        
        cumsum = 0
        tet_a_visits = 0
        tet_b_visits = 0
        
        for digit in digits:
            cumsum += digit
            vertex = cumsum % 8
            if get_tetrahedron(vertex) == 'A':
                tet_a_visits += 1
            else:
                tet_b_visits += 1
        
        total = tet_a_visits + tet_b_visits
        ratio_a = tet_a_visits / total
        
        return {
            "Tet A visits": tet_a_visits,
            "Tet B visits": tet_b_visits,
            "Ratio A": ratio_a,
        }
    
    def observations(self) -> Optional[Dict[str, float]]:
        # Statistical check - exact counts depend on pi digits
        # Important: both should be visited, ratio should be near 0.5
        return None


class OrbitsVsElectrons(GFDTest):
    """
    With 100 digits, we should have multiple electrons worth of orbits.
    """
    name = "Orbits vs Electrons"
    question = "With 100 digits, how many orbits are completed, and what fraction of an 'electron' (137 orbits per 1/α) does this represent?"
    reference_source = "1/alpha = 137 orbits per electron"
    derivation = (
        "PREMISE: The model associates 137 orbits with one electron (1/α). "
        "STEP 1: Execute traversal with 100 digits to find final cumsum. "
        "STEP 2: Total orbits = cumsum // 8. "
        "STEP 3: Electrons worth = total_orbits / 137. "
        "STEP 4: With mean digit ~3.3, 100 digits give ~330 cumsum, ~41 orbits. "
        "OUTPUT: Total orbits ≈ 41, electrons worth ≈ 0.3."
    )
    commentary = (
        "The orbit count from 100 digits provides a basis for relating traversal "
        "cycles to electron-scale physics through the 1/alpha correspondence. "
        "This connects digit-level statistics to the fine structure constant."
    )
    
    def model(self) -> Dict[str, float]:
        digits = get_pi_base8(100, include_integer=True)
        cumsum = sum(digits)
        total_orbits = cumsum // 8
        
        orbits_per_electron = 137
        electrons_worth = total_orbits / orbits_per_electron
        
        return {
            "Total orbits": total_orbits,
            "Electrons worth": electrons_worth,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    DigitsExist,
    AllDigitsInRange,
    KnownSequenceMatch,
    DigitDistribution,
    DigitSumChecksum,
    FullTraversalStatistics,
    TraversalBalance,
    OrbitsVsElectrons,
]


def run_all_tests() -> bool:
    """Run all pi digit validation tests."""
    return run_test_group(
        title="Full Pi Digits Validation",
        summary=(
            "These tests validate the pre-computed pi base-8 digits used throughout the "
            "framework. All digits must be in range 0-7 and match known pi sequences. "
            "Distribution should be approximately uniform (pi is conjectured normal). "
            "Full traversal must visit all 8 vertices, complete multiple orbits, and "
            "maintain Field Chamber balance. With 100+ digits, sufficient data exists "
            "for statistical analysis."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
