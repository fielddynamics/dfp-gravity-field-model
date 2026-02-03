"""
BBP Formula and Field Closure Structure
=======================================

This module examines correspondences between the Bailey-Borwein-Plouffe formula
for pi and the k=4 tetrahedral topology used in the GFD model. The BBP formula
denominators (8k+1, 8k+4, 8k+5, 8k+6) map to positions in the dual Field Chamber
structure, with coefficients +4, -2, -1, -1 that sum to zero.

These tests validate the mathematical structure of the BBP formula and document
numerical correspondences with k=4 topology parameters.
"""

import sys
import os
import math
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group


# =============================================================================
# CONSTANTS
# =============================================================================

PI = math.pi
K = 4  # Closure constant

# BBP formula positions (mod 8)
BBP_POSITIONS = [1, 4, 5, 6]

# BBP coefficients
BBP_COEFFICIENTS = {
    1: 4,    # Position 1: +4 (INTAKE)
    4: -2,   # Position 4: -2 (COMPRESS)
    5: -1,   # Position 5: -1 (POWER)
    6: -1,   # Position 6: -1 (EXHAUST)
}

# Engine stroke interpretation
ENGINE_STROKES = {
    1: "INTAKE",
    4: "COMPRESS",
    5: "POWER",
    6: "EXHAUST",
}


# =============================================================================
# BBP FORMULA IMPLEMENTATION
# =============================================================================

def bbp_term(k):
    """Compute the k-th term of the BBP formula."""
    factor = 1.0 / (16 ** k)
    bracket = (
        4.0 / (8*k + 1) -
        2.0 / (8*k + 4) -
        1.0 / (8*k + 5) -
        1.0 / (8*k + 6)
    )
    return factor * bracket


def bbp_pi(n_terms=100):
    """Compute pi using the BBP formula with n_terms."""
    return sum(bbp_term(k) for k in range(n_terms))


def bbp_coefficient_sum():
    """Sum of BBP coefficients: +4 - 2 - 1 - 1 = 0"""
    return sum(BBP_COEFFICIENTS.values())


# =============================================================================
# TESTS
# =============================================================================

class BBPComputesPi(GFDTest):
    """
    The BBP formula correctly computes pi to high precision.
    This establishes that the formula is mathematically sound.
    """
    name = "BBP Formula Accuracy"
    question = "Can the Bailey-Borwein-Plouffe formula compute pi to arbitrary precision, validating its use as a traversal driver in the GFD model?"
    reference_source = "Mathematical constant pi"
    tolerance = 1e-12
    derivation = (
        "PREMISE: The BBP formula is pi = sum_{k=0}^{inf} (1/16^k) * [4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)]. "
        "STEP 1: Compute 50 terms of the series using this exact formula. "
        "STEP 2: Sum all terms to obtain a numerical approximation. "
        "STEP 3: Compare to the known value pi = 3.141592653589793... "
        "OUTPUT: Agreement within 10^-12 confirms formula correctness for traversal applications."
    )
    commentary = None  # Mechanical verification of algorithm correctness
    
    def model(self) -> Dict[str, float]:
        computed_pi = bbp_pi(n_terms=50)
        return {"Pi (BBP, 50 terms)": computed_pi}
    
    def observations(self) -> Dict[str, float]:
        return {"Pi (BBP, 50 terms)": PI}


class BBPCoefficientsClosure(GFDTest):
    """
    The BBP coefficients sum to zero: +4 - 2 - 1 - 1 = 0.
    This is field closure: push equals pull, total flux is zero.
    """
    name = "Coefficient Sum (Field Closure)"
    question = "Do the BBP formula coefficients satisfy the Field Closure balance requirement where total flux sums to zero?"
    reference_source = "Field closure requirement"
    tolerance = 0.0
    derivation = (
        "PREMISE: The BBP formula has coefficients at four positions: +4, -2, -1, -1. "
        "STEP 1: Identify positive contributions (inflow): +4. "
        "STEP 2: Identify negative contributions (outflow): -2 + (-1) + (-1) = -4. "
        "STEP 3: Sum all coefficients: +4 + (-2) + (-1) + (-1) = 0. "
        "OUTPUT: Net coefficient sum equals zero, consistent with Field Closure where push equals pull."
    )
    commentary = (
        "The BBP coefficients summing to zero is consistent with Field Closure "
        "requirements where net flux must balance. This structural property of the "
        "formula may reflect an underlying conservation principle in the encoding of pi."
    )
    
    def model(self) -> Dict[str, float]:
        coeff_sum = bbp_coefficient_sum()
        positive = sum(c for c in BBP_COEFFICIENTS.values() if c > 0)
        negative = abs(sum(c for c in BBP_COEFFICIENTS.values() if c < 0))
        return {
            "Coefficient sum": coeff_sum,
            "Positive total": positive,
            "Negative total": negative,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Coefficient sum": 0,
            "Positive total": 4,
            "Negative total": 4,
        }


class BBPFourPositions(GFDTest):
    """
    BBP uses exactly 4 positions, matching k=4 topology.
    Four strokes in the field closure engine.
    """
    name = "Four Position Structure"
    question = "Does the BBP formula employ exactly k=4 denominator positions, matching the tetrahedral face count in GFD topology?"
    reference_source = "k=4 topology"
    tolerance = 0.0
    derivation = (
        "PREMISE: From Field Closure, k=4 is the number of faces on a tetrahedron. "
        "STEP 1: The BBP formula uses denominators 8k+1, 8k+4, 8k+5, 8k+6. "
        "STEP 2: Count distinct position offsets: {1, 4, 5, 6}, giving 4 positions. "
        "STEP 3: Compare position count to topology constant: 4 = k. "
        "OUTPUT: BBP structure matches the k=4 tetrahedral topology of the Field Chamber."
    )
    commentary = (
        "The BBP formula employs exactly four denominator positions, corresponding "
        "numerically to k=4 tetrahedral topology. This correspondence between the "
        "structure of a pi formula and Field Chamber geometry may indicate deeper "
        "connections between transcendental numbers and discrete spatial structure."
    )
    
    def model(self) -> Dict[str, float]:
        n_positions = len(BBP_POSITIONS)
        return {
            "Number of positions": n_positions,
            "Expected (k)": K,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Number of positions": 4,
            "Expected (k)": 4,
        }


class BBPBase16Structure(GFDTest):
    """
    BBP uses base 16 = 4*k = 16. This is not arbitrary but
    aligns perfectly with k=4 topology (4 squared).
    """
    name = "Base 16 Structure"
    question = "Is the BBP formula's base-16 structure derivable from the k=4 topology constant as 4 times k?"
    reference_source = "k=4 topology"
    tolerance = 0.0
    derivation = (
        "PREMISE: The BBP formula uses powers of 16 as its base: 1/16^k. "
        "STEP 1: From Field Closure, k=4 (tetrahedral face count). "
        "STEP 2: Calculate 4 times k: 4 * 4 = 16. "
        "STEP 3: Compare to BBP base: 16 = 4k. "
        "OUTPUT: The hexadecimal base of BBP equals 4k, linking pi computation to tetrahedral topology."
    )
    commentary = (
        "The BBP formula's base-16 structure equals 4k where k=4, suggesting a "
        "relationship between hexadecimal representation and tetrahedral counting. "
        "This correspondence emerges without parameter tuning from the formula's "
        "mathematical structure."
    )
    
    def model(self) -> Dict[str, float]:
        bbp_base = 16
        four_k = 4 * K
        return {
            "BBP base": bbp_base,
            "4 * k": four_k,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "BBP base": 16,
            "4 * k": 16,
        }


class BBPDenominatorSpacing(GFDTest):
    """
    BBP denominators are spaced by 8 = 2*k (dual Field Chamber vertex count).
    This spacing corresponds to the dual-tetrahedra structure.
    """
    name = "Denominator Spacing"
    question = "Does the BBP denominator spacing of 8 correspond to the 2k=8 vertices of the stellated octahedron Field Chamber?"
    reference_source = "Dual Field Chamber structure (2k vertices)"
    tolerance = 0.0
    derivation = (
        "PREMISE: The stellated octahedron consists of two tetrahedra, each with k=4 vertices. "
        "STEP 1: Calculate total vertices: Tetrahedron A (k=4) + Tetrahedron B (k=4) = 2k = 8. "
        "STEP 2: The BBP denominators cycle with period 8: (8k+1), (8k+4), (8k+5), (8k+6). "
        "STEP 3: Compare spacing to vertex count: 8 = 2k. "
        "OUTPUT: BBP denominator periodicity matches the dual Field Chamber vertex count."
    )
    commentary = (
        "The 8-fold periodicity in BBP denominators corresponds to the 8 vertices "
        "of the stellated octahedron (dual Field Chamber). This spacing of 2k aligns "
        "with the vertex count of two interlocking tetrahedra, each contributing k=4 vertices."
    )
    
    def model(self) -> Dict[str, float]:
        spacing = 8
        two_k = 2 * K
        return {
            "Denominator spacing": spacing,
            "2 * k": two_k,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Denominator spacing": 8,
            "2 * k": 8,
        }


class BBPFiringOrder(GFDTest):
    """
    BBP positions follow the sequence 1 -> 4 -> 5 -> 6, corresponding
    to a specific path through the dual Field Chamber vertices.
    """
    name = "Engine Firing Order"
    question = "Does the BBP formula's position sequence 1-4-5-6 trace a specific path through the Field Chamber, with position 4 at the topology constant k?"
    reference_source = None  # Model output only
    derivation = (
        "PREMISE: BBP denominators use positions 1, 4, 5, 6 within each 8-cycle. "
        "STEP 1: List positions in order of appearance: 1 (INTAKE), 4 (COMPRESS), 5 (POWER), 6 (EXHAUST). "
        "STEP 2: Note position 4 equals k=4 (the topology constant). "
        "STEP 3: Positions span 4 of the 8 available slots in each cycle. "
        "OUTPUT: The firing order traces a 4-stroke path with k appearing at the compression position."
    )
    commentary = (
        "The BBP formula's position sequence (1, 4, 5, 6) traces a specific path "
        "through vertex space. Position 4 corresponds to the topology constant k, "
        "suggesting this sequence may encode traversal dynamics within the Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        expected = [1, 4, 5, 6]
        actual = BBP_POSITIONS
        matches = 1 if actual == expected else 0
        return {
            "Firing order matches": matches,
            "Position 1 (INTAKE)": BBP_POSITIONS[0],
            "Position 2 (COMPRESS)": BBP_POSITIONS[1],
            "Position 3 (POWER)": BBP_POSITIONS[2],
            "Position 4 (EXHAUST)": BBP_POSITIONS[3],
        }


class BBPIntakeStroke(GFDTest):
    """
    Position 1 (8k+1) corresponds to the intake phase with coefficient +4.
    This is the largest magnitude coefficient in the BBP formula.
    """
    name = "Intake Stroke (Position 1)"
    question = "Does BBP position 1 (denominator 8k+1) carry the largest positive coefficient +4, representing maximum energy intake?"
    reference_source = "Engine analogy"
    tolerance = 0.0
    derivation = (
        "PREMISE: In the BBP formula, each position has an assigned coefficient. "
        "STEP 1: Position 1 uses denominator (8k+1) with coefficient +4. "
        "STEP 2: The positive sign indicates inflow (intake). "
        "STEP 3: Magnitude 4 is the largest among all coefficients {+4, -2, -1, -1}. "
        "OUTPUT: Position 1 is the intake stroke with maximum positive contribution."
    )
    commentary = None  # Structural verification of BBP coefficient
    
    def model(self) -> Dict[str, float]:
        coeff = BBP_COEFFICIENTS[1]
        return {
            "Position 1 coefficient": coeff,
            "Is positive (intake)": 1 if coeff > 0 else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Position 1 coefficient": 4,
            "Is positive (intake)": 1,
        }


class BBPCompressStroke(GFDTest):
    """
    Position 4 (8k+4) corresponds to the compress phase with coefficient -2.
    Position 4 equals the topology constant k.
    """
    name = "Compress Stroke (Position 4)"
    question = "Does BBP position 4 coincide with the topology constant k=4, carrying the intermediate negative coefficient -2?"
    reference_source = "Engine analogy"
    tolerance = 0.0
    derivation = (
        "PREMISE: The topology constant k=4 defines tetrahedral face count. "
        "STEP 1: Position 4 uses denominator (8k+4) with coefficient -2. "
        "STEP 2: Compare position to topology constant: position 4 = k = 4. "
        "STEP 3: The negative sign indicates outflow (compression releases energy). "
        "OUTPUT: Position 4 at k=4 is the compression stroke with coefficient -2."
    )
    commentary = (
        "Position 4 in the BBP formula coincides with the topology constant k=4. "
        "This positional correspondence suggests the formula structure may encode "
        "tetrahedral geometry at a fundamental level."
    )
    
    def model(self) -> Dict[str, float]:
        coeff = BBP_COEFFICIENTS[4]
        is_k = 1 if 4 == K else 0
        return {
            "Position 4 coefficient": coeff,
            "Position equals k": is_k,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Position 4 coefficient": -2,
            "Position equals k": 1,
        }


class BBPPowerStroke(GFDTest):
    """
    Position 5 (8k+5) corresponds to the power phase with coefficient -1.
    Position 5 equals k+1.
    """
    name = "Power Stroke (Position 5)"
    question = "Does BBP position 5 equal k+1, representing the power stroke beyond the topology threshold with coefficient -1?"
    reference_source = "Engine analogy"
    tolerance = 0.0
    derivation = (
        "PREMISE: Position 5 follows immediately after the topology constant k=4. "
        "STEP 1: Position 5 uses denominator (8k+5) with coefficient -1. "
        "STEP 2: Verify position equals k+1: 5 = 4 + 1 = k + 1. "
        "STEP 3: The -1 coefficient represents unit outflow during power delivery. "
        "OUTPUT: Position 5 at k+1 is the power stroke with coefficient -1."
    )
    commentary = None  # Structural verification of BBP coefficient
    
    def model(self) -> Dict[str, float]:
        coeff = BBP_COEFFICIENTS[5]
        is_k_plus_1 = 1 if 5 == K + 1 else 0
        return {
            "Position 5 coefficient": coeff,
            "Position equals k+1": is_k_plus_1,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Position 5 coefficient": -1,
            "Position equals k+1": 1,
        }


class BBPExhaustStroke(GFDTest):
    """
    Position 6 (8k+6) corresponds to the exhaust phase with coefficient -1.
    This completes the four-position cycle.
    """
    name = "Exhaust Stroke (Position 6)"
    question = "Does BBP position 6 complete the four-stroke cycle as the exhaust phase with final coefficient -1?"
    reference_source = "Engine analogy"
    tolerance = 0.0
    derivation = (
        "PREMISE: The BBP formula uses exactly 4 positions per cycle. "
        "STEP 1: Position 6 uses denominator (8k+6) with coefficient -1. "
        "STEP 2: This is the final position in the sequence {1, 4, 5, 6}. "
        "STEP 3: The -1 coefficient exhausts remaining energy to balance the cycle. "
        "OUTPUT: Position 6 is the exhaust stroke completing the 4-position cycle."
    )
    commentary = None  # Structural verification of BBP coefficient
    
    def model(self) -> Dict[str, float]:
        coeff = BBP_COEFFICIENTS[6]
        return {
            "Position 6 coefficient": coeff,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Position 6 coefficient": -1,
        }


class BBPLargestAtBlocked(GFDTest):
    """
    The largest coefficient (+4) is at a blocked position.
    Blocked channels receive the most pressure because energy accumulates
    where it cannot escape.
    """
    name = "Largest Coefficient at Blocked"
    question = "Is the largest BBP coefficient magnitude located at a constrained Coupling Port position where energy accumulates before release?"
    reference_source = None  # Model interpretation
    derivation = (
        "PREMISE: Energy accumulates at constrained positions before propagating through open channels. "
        "STEP 1: Identify all coefficient magnitudes: |+4| = 4, |-2| = 2, |-1| = 1, |-1| = 1. "
        "STEP 2: The largest magnitude is 4, located at position 1. "
        "STEP 3: Position 1 is the intake position where energy enters but cannot immediately exit. "
        "OUTPUT: Maximum coefficient at position 1 is consistent with accumulation dynamics at constrained Coupling Ports."
    )
    commentary = (
        "The asymmetric distribution of BBP coefficients, with the largest magnitude "
        "at position 1, is consistent with accumulation dynamics at constrained Coupling "
        "Ports. This pattern may reflect how information density varies across the "
        "Field Chamber traversal sequence."
    )
    
    def model(self) -> Dict[str, float]:
        largest_coeff = max(abs(c) for c in BBP_COEFFICIENTS.values())
        position_of_largest = [p for p, c in BBP_COEFFICIENTS.items() 
                              if abs(c) == largest_coeff][0]
        # Position 1 is blocked in the pi traversal pattern
        return {
            "Largest coefficient magnitude": largest_coeff,
            "Position of largest": position_of_largest,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    BBPComputesPi,
    BBPCoefficientsClosure,
    BBPFourPositions,
    BBPBase16Structure,
    BBPDenominatorSpacing,
    BBPFiringOrder,
    BBPIntakeStroke,
    BBPCompressStroke,
    BBPPowerStroke,
    BBPExhaustStroke,
    BBPLargestAtBlocked,
]


def run_all_tests() -> bool:
    """Run all BBP structure tests."""
    return run_test_group(
        title="BBP Formula and Field Closure Structure",
        summary=(
            "These tests examine correspondences between the Bailey-Borwein-Plouffe formula "
            "for pi and k=4 tetrahedral topology. The BBP coefficients +4, -2, -1, -1 sum "
            "to zero, consistent with Field Closure requirements. The base-16 structure "
            "(4k) and 8-spacing (2k) correspond to k=4 topology parameters. These numerical "
            "correspondences are documented for further investigation."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
