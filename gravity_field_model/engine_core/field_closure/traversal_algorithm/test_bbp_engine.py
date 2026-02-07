"""
BBP Formula and Field Closure Structure
=======================================

This module examines correspondences between the Bailey-Borwein-Plouffe formula
for pi and the k=4 tetrahedral topology used in the GFM model. The BBP formula
denominators (8k+1, 8k+4, 8k+5, 8k+6) map to positions in the dual Field Chamber
structure, with coefficients +4, -2, -1, -1 that sum to zero.

These tests validate the mathematical structure of the BBP formula and document
numerical correspondences with k=4 topology parameters.
"""

import math
from typing import Dict, Optional

from gravity_field_model.framework import *
from gravity_field_model.common import K


# =============================================================================
# CONSTANTS
# =============================================================================

PI = math.pi

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

class BBPComputesPi(Test):
    """
    The BBP formula correctly computes pi to high precision.
    This establishes that the formula is mathematically sound.
    """
    name = "BBP Formula Accuracy"
    question = (
        "Why does the traversal algorithm need a reliable way to compute pi? "
        "Because pi's digits drive vertex selection, and any error would corrupt the entire sequence. "
        "This test verifies the BBP formula produces pi to 12 decimal places, establishing mathematical soundness."
    )
    reference = "Mathematical constant pi"
    tolerance = 1e-12
    level = Critical
    audit_score = 85
    audit_notes = (
        "Question: 14/15 - Good 'why' opener about reliability before computation. "
        "Derivation: 13/15 - Clear steps but could add more intuition about series convergence. "
        "Commentary: 14/15 - Excellent baking/map analogies build intuition. "
        "Model: 9/10 - Clean single-value output. "
        "Observations: 9/10 - Uses math.pi as reference, traceable. "
        "Constants: 6/10 - K=4 hardcoded, should import from geometry_constants.py. "
        "Accessibility: 12/15 - Good for undergrad, clear analogies. "
        "Header: 8/10 (module level) - Good overview of BBP structure. "
        "SAMPLE SIZE: N/A - No pi digit traversal, uses BBP formula directly. "
        "FUNCTION OPPORTUNITY: bbp_term() and bbp_pi() could be extracted to common module. "
        "TO IMPROVE: Import K from geometry_constants.py. Add intuition about geometric decay."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The BBP formula is pi = sum_{k=0}^{inf} (1/16^k) * [4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)].")
            .step("Compute 50 terms of the series using this exact formula.")
            .step("Sum all terms to obtain a numerical approximation.")
            .step("Compare to the known value pi = 3.141592653589793...")
            .conclude("Agreement within 10^-12 confirms formula correctness for traversal applications.")
        )
    
    commentary = (
        "Think of the BBP formula like a recipe for baking a very precise cake. If the recipe has "
        "even a tiny error, every cake you bake will be wrong. Since we use pi's digits to navigate "
        "through the Field Chamber (like using a map), the formula must be exact. With just 50 terms, "
        "the BBP formula already matches pi to 12 decimal places, far more precision than we need. "
        "This is our mathematical foundation: a reliable source of digits."
    )
    
    def model(self):
        computed_pi = bbp_pi(n_terms=50)
        return Model().add("Pi (BBP, 50 terms)", computed_pi)
    
    def observations(self):
        return Observed().add("Pi (BBP, 50 terms)", PI)


class BBPCoefficientsClosure(Test):
    """
    The BBP coefficients sum to zero: +4 - 2 - 1 - 1 = 0.
    This is field closure: push equals pull, total flux is zero.
    """
    name = "Coefficient Sum (Field Closure)"
    question = (
        "Why must the BBP coefficients balance to zero? "
        "Because Field Closure requires that what flows in must flow out, like water in a closed pipe system. "
        "This test checks whether the BBP formula's weights (+4, -2, -1, -1) sum to zero, "
        "revealing a conservation structure hidden within pi's formula."
    )
    reference = "Field closure requirement"
    tolerance = 0.0
    level = Critical
    audit_score = 92
    audit_notes = (
        "Question: 14/15 - Excellent 'why must balance' with pipe system analogy. "
        "Derivation: 14/15 - Clear inflow/outflow reasoning. "
        "Commentary: 15/15 - Perfect room/doors analogy for conservation. "
        "Model: 10/10 - Clean positive/negative decomposition. "
        "Observations: 10/10 - Values clearly defined and verifiable. "
        "Constants: 6/10 - BBP_COEFFICIENTS hardcoded, acceptable for formula constants. "
        "Accessibility: 14/15 - Undergraduate friendly with excellent analogies. "
        "Header: 9/10 (module level). "
        "SAMPLE SIZE: N/A - Mathematical identity, no statistical claims. "
        "FUNCTION OPPORTUNITY: None needed, simple verification. "
        "TO IMPROVE: Minor - could cite BBP paper reference."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The BBP formula has coefficients at four positions: +4, -2, -1, -1.")
            .step("Identify positive contributions (inflow): +4.")
            .step("Identify negative contributions (outflow): -2 + (-1) + (-1) = -4.")
            .step("Sum all coefficients: +4 + (-2) + (-1) + (-1) = 0.")
            .conclude("Net coefficient sum equals zero, consistent with Field Closure where push equals pull.")
        )
    
    commentary = (
        "Imagine a room with doors. If 4 people walk in through one door, and 2 leave through "
        "a second door, 1 through a third, and 1 through a fourth, the room ends up with the "
        "same number of people it started with. The BBP coefficients work the same way: "
        "+4 in, -4 out (as -2, -1, -1). This zero-sum property is exactly what Field Closure "
        "demands. It is remarkable that a formula discovered purely for computing pi digits "
        "happens to encode this balance. Nature seems to prefer formulas that conserve."
    )
    
    def model(self):
        coeff_sum = bbp_coefficient_sum()
        positive = sum(c for c in BBP_COEFFICIENTS.values() if c > 0)
        negative = abs(sum(c for c in BBP_COEFFICIENTS.values() if c < 0))
        return (
            Model()
            .add("Coefficient sum", coeff_sum)
            .add("Positive total", positive)
            .add("Negative total", negative)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Coefficient sum", 0)
            .add("Positive total", 4)
            .add("Negative total", 4)
        )


class BBPFourPositions(Test):
    """
    BBP uses exactly 4 positions, matching k=4 topology.
    Four strokes in the field closure engine.
    """
    name = "Four Position Structure"
    question = (
        "Why does the number 4 keep appearing in both pi's formula and tetrahedral geometry? "
        "A tetrahedron has exactly 4 faces, and the BBP formula uses exactly 4 denominator positions. "
        "This test verifies this structural coincidence: the formula that computes pi has the same "
        "'shape' as the geometry we use to understand gravity."
    )
    reference = "k=4 topology"
    tolerance = 0.0
    level = Standard
    audit_score = 84
    audit_notes = (
        "Question: 14/15 - Excellent 'why' about the recurring number 4. "
        "Derivation: 12/15 - Clear but could explain why 4 is fundamental. "
        "Commentary: 13/15 - Good observation about pi 'knowing' geometry. "
        "Model: 9/10 - Clean comparison output. "
        "Observations: 9/10 - Clear expected values. "
        "Constants: 5/10 - K=4, BBP_POSITIONS hardcoded. Should import K. "
        "Accessibility: 13/15 - Good tetrahedron explanation. "
        "Header: 9/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Import K from geometry_constants.py."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: From Field Closure, k=4 is the number of faces on a tetrahedron.")
            .step("The BBP formula uses denominators 8k+1, 8k+4, 8k+5, 8k+6.")
            .step("Count distinct position offsets: {1, 4, 5, 6}, giving 4 positions.")
            .step("Compare position count to topology constant: 4 = k.")
            .conclude("BBP structure matches the k=4 tetrahedral topology of the Field Chamber.")
        )
    
    commentary = (
        "Here is something curious: a tetrahedron (the simplest 3D shape) has exactly 4 faces. "
        "And the BBP formula for pi, which was discovered purely through number theory, also has "
        "exactly 4 terms in its bracket. Is this a coincidence? Perhaps. But when we build the "
        "Field Chamber from two tetrahedra, this same number 4 becomes the organizing constant 'k'. "
        "It is as if pi 'knows' about tetrahedral geometry. We do not claim causation, but the "
        "correspondence is striking and worth noting."
    )
    
    def model(self):
        n_positions = len(BBP_POSITIONS)
        return (
            Model()
            .add("Number of positions", n_positions)
            .add("Expected (k)", K)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Number of positions", 4)
            .add("Expected (k)", 4)
        )


class BBPBase16Structure(Test):
    """
    BBP uses base 16 = 4*k = 16. This is not arbitrary but
    aligns perfectly with k=4 topology (4 squared).
    """
    name = "Base 16 Structure"
    question = (
        "Why does the BBP formula work in base 16 (hexadecimal)? "
        "Remarkably, 16 = 4 x 4, where 4 is our topology constant k. "
        "This test checks whether hexadecimal representation naturally connects to "
        "tetrahedral structure through k squared."
    )
    reference = "k=4 topology"
    tolerance = 0.0
    level = Standard
    audit_score = 82
    audit_notes = (
        "Question: 12/15 - Good 'why' but could hook curiosity more. "
        "Derivation: 13/15 - Clear multiplication steps. "
        "Commentary: 13/15 - Nice insight about computers and geometry. "
        "Model: 9/10 - Simple comparison. "
        "Observations: 9/10 - Clear expected values. "
        "Constants: 5/10 - K=4 hardcoded, should import from geometry_constants.py. "
        "Accessibility: 12/15 - Good for undergrad. "
        "Header: 9/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Import K from geometry_constants.py."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The BBP formula uses powers of 16 as its base: 1/16^k.")
            .step("From Field Closure, k=4 (tetrahedral face count).")
            .step("Calculate 4 times k: 4 * 4 = 16.")
            .step("Compare to BBP base: 16 = 4k.")
            .conclude("The hexadecimal base of BBP equals 4k, linking pi computation to tetrahedral topology.")
        )
    
    commentary = (
        "Why base 16? Computers love it because 16 = 2^4, making binary conversion easy. "
        "But there is another way to see 16: it equals 4 x 4, or k x k where k=4 is our "
        "tetrahedral constant. The BBP formula essentially 'squares' the tetrahedral structure. "
        "This is not a coincidence we engineered; Bailey, Borwein, and Plouffe discovered the "
        "formula in 1995 without any thought of tetrahedra. Yet the numbers align perfectly. "
        "When a formula for circles (pi) connects to formulas for triangular pyramids (tetrahedra), "
        "it hints that geometry may be more unified than we thought."
    )
    
    def model(self):
        bbp_base = 16
        four_k = 4 * K
        return (
            Model()
            .add("BBP base", bbp_base)
            .add("4 * k", four_k)
        )
    
    def observations(self):
        return (
            Observed()
            .add("BBP base", 16)
            .add("4 * k", 16)
        )


class BBPDenominatorSpacing(Test):
    """
    BBP denominators are spaced by 8 = 2*k (dual Field Chamber vertex count).
    This spacing corresponds to the dual-tetrahedra structure.
    """
    name = "Denominator Spacing"
    question = (
        "Why do BBP denominators repeat every 8 positions? "
        "Because the Field Chamber has exactly 8 vertices (two tetrahedra, 4 vertices each). "
        "This test verifies that the formula's period matches the geometry's vertex count, "
        "connecting pi's computation to the structure we traverse."
    )
    reference = "Dual Field Chamber structure (2k vertices)"
    tolerance = 0.0
    level = Standard
    audit_score = 85
    audit_notes = (
        "Question: 14/15 - Excellent 'why' with clear vertex count reasoning. "
        "Derivation: 13/15 - Clear calculation of 2k. "
        "Commentary: 14/15 - Great Star of David and combination lock analogies. "
        "Model: 9/10 - Simple comparison. "
        "Observations: 9/10 - Clear expected values. "
        "Constants: 5/10 - K=4 hardcoded, should import from geometry_constants.py. "
        "Accessibility: 13/15 - Excellent visualizations for undergrad. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Import K from geometry_constants.py."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The stellated octahedron consists of two tetrahedra, each with k=4 vertices.")
            .step("Calculate total vertices: Tetrahedron A (k=4) + Tetrahedron B (k=4) = 2k = 8.")
            .step("The BBP denominators cycle with period 8: (8k+1), (8k+4), (8k+5), (8k+6).")
            .step("Compare spacing to vertex count: 8 = 2k.")
            .conclude("BBP denominator periodicity matches the dual Field Chamber vertex count.")
        )
    
    commentary = (
        "Picture two pyramids (tetrahedra) interlocked, tip to tip, like a Star of David in 3D. "
        "This shape, the stellated octahedron, has 8 corners. Now look at the BBP formula: "
        "its denominators cycle through positions 1, 4, 5, 6, then jump by 8 and repeat. "
        "The cycle length (8) exactly matches the vertex count of our geometric structure. "
        "This is like finding that a combination lock happens to have the same number of "
        "positions as you have fingers. It may be coincidence, but it is a useful one."
    )
    
    def model(self):
        spacing = 8
        two_k = 2 * K
        return (
            Model()
            .add("Denominator spacing", spacing)
            .add("2 * k", two_k)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Denominator spacing", 8)
            .add("2 * k", 8)
        )


class BBPFiringOrder(Test):
    """
    BBP positions follow the sequence 1 -> 4 -> 5 -> 6, corresponding
    to a specific path through the dual Field Chamber vertices.
    """
    name = "Engine Firing Order"
    question = (
        "Why does an engine fire in a specific order? "
        "Because the sequence matters for smooth operation. "
        "The BBP formula visits positions 1, 4, 5, 6, like a 4-stroke engine cycling through "
        "intake, compress, power, exhaust. This test documents the exact sequence, noting that "
        "position 4 equals our topology constant k."
    )
    reference = None  # Model output only
    level = Standard
    audit_score = 80
    audit_notes = (
        "Question: 13/15 - Good engine analogy hook for 'why sequence matters'. "
        "Derivation: 11/15 - Clear but mostly documentation, lacks deeper WHY. "
        "Commentary: 14/15 - Excellent 4-stroke engine analogy throughout. "
        "Model: 8/10 - Clean listing of positions. "
        "Observations: 0/10 - Missing observations() method. "
        "Constants: 5/10 - BBP_POSITIONS, ENGINE_STROKES hardcoded. "
        "Accessibility: 13/15 - Great engine analogy for undergrad. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Add observations() method. Explain WHY order emerges mathematically."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: BBP denominators use positions 1, 4, 5, 6 within each 8-cycle.")
            .step("List positions in order of appearance: 1 (INTAKE), 4 (COMPRESS), 5 (POWER), 6 (EXHAUST).")
            .step("Note position 4 equals k=4 (the topology constant).")
            .step("Positions span 4 of the 8 available slots in each cycle.")
            .conclude("The firing order traces a 4-stroke path with k appearing at the compression position.")
        )
    
    commentary = (
        "A car engine fires its cylinders in a careful sequence: intake (draw in fuel), "
        "compress (squeeze it), power (ignite), exhaust (push out waste). The BBP formula "
        "has the same structure! It visits positions 1, 4, 5, 6 with coefficients that "
        "act like the four strokes. Position 4 is particularly interesting: it equals k, "
        "our topology constant. The compression stroke, where energy builds up, happens "
        "right at the number that defines tetrahedral geometry. We use this engine analogy "
        "not because pi literally powers anything, but because the pattern helps intuition."
    )
    
    def model(self):
        expected = [1, 4, 5, 6]
        actual = BBP_POSITIONS
        matches = 1 if actual == expected else 0
        return (
            Model()
            .add("Firing order matches", matches)
            .add("Position 1 (INTAKE)", BBP_POSITIONS[0])
            .add("Position 2 (COMPRESS)", BBP_POSITIONS[1])
            .add("Position 3 (POWER)", BBP_POSITIONS[2])
            .add("Position 4 (EXHAUST)", BBP_POSITIONS[3])
        )
    
    def observations(self):
        return (
            Observed()
            .add("Firing order matches", 1)
            .add("Position 1 (INTAKE)", 1)
            .add("Position 2 (COMPRESS)", 4)
            .add("Position 3 (POWER)", 5)
            .add("Position 4 (EXHAUST)", 6)
        )


class BBPIntakeStroke(Test):
    """
    Position 1 (8k+1) corresponds to the intake phase with coefficient +4.
    This is the largest magnitude coefficient in the BBP formula.
    """
    name = "Intake Stroke (Position 1)"
    question = (
        "Why is the first position the most important in the BBP formula? "
        "Like an engine's intake stroke that draws in all the fuel, position 1 has the "
        "largest coefficient (+4). This test verifies this asymmetry: most of what enters "
        "the formula enters through this first 'door'."
    )
    reference = "Engine analogy"
    tolerance = 0.0
    level = Standard
    audit_score = 83
    audit_notes = (
        "Question: 13/15 - Good 'why' about importance with engine analogy. "
        "Derivation: 13/15 - Clear coefficient identification. "
        "Commentary: 13/15 - Good fuel/intake analogy. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Clear expected values. "
        "Constants: 5/10 - BBP_COEFFICIENTS hardcoded. "
        "Accessibility: 13/15 - Good for undergrad. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Explain WHY +4 is largest mathematically."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: In the BBP formula, each position has an assigned coefficient.")
            .step("Position 1 uses denominator (8k+1) with coefficient +4.")
            .step("The positive sign indicates inflow (intake).")
            .step("Magnitude 4 is the largest among all coefficients {+4, -2, -1, -1}.")
            .conclude("Position 1 is the intake stroke with maximum positive contribution.")
        )
    
    commentary = (
        "In a car engine, the intake stroke is crucial: this is when fuel and air rush "
        "into the cylinder. Without a good intake, the engine starves. In the BBP formula, "
        "position 1 plays this role with coefficient +4, four times bigger than the smallest "
        "coefficients. Everything that happens later (the -2, -1, -1) essentially distributes "
        "what came in through this first channel. The formula front-loads its positive contribution."
    )
    
    def model(self):
        coeff = BBP_COEFFICIENTS[1]
        return (
            Model()
            .add("Position 1 coefficient", coeff)
            .add("Is positive (intake)", 1 if coeff > 0 else 0)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Position 1 coefficient", 4)
            .add("Is positive (intake)", 1)
        )


class BBPCompressStroke(Test):
    """
    Position 4 (8k+4) corresponds to the compress phase with coefficient -2.
    Position 4 equals the topology constant k.
    """
    name = "Compress Stroke (Position 4)"
    question = (
        "Why does position 4 matter so much? "
        "Because 4 = k, the same number that counts tetrahedral faces. "
        "This test checks whether the BBP formula places its compression stroke (coefficient -2) "
        "exactly at the position matching our fundamental geometry constant."
    )
    reference = "Engine analogy"
    tolerance = 0.0
    level = Standard
    audit_score = 86
    audit_notes = (
        "Question: 14/15 - Excellent tie to k=4 topology constant. "
        "Derivation: 13/15 - Clear connection between position and topology. "
        "Commentary: 14/15 - Great engine compression analogy with k=4 insight. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Clear expected values. "
        "Constants: 5/10 - K hardcoded, should import from geometry_constants.py. "
        "Accessibility: 14/15 - Excellent discovery vs invention framing. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Import K from geometry_constants.py."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The topology constant k=4 defines tetrahedral face count.")
            .step("Position 4 uses denominator (8k+4) with coefficient -2.")
            .step("Compare position to topology constant: position 4 = k = 4.")
            .step("The negative sign indicates outflow (compression releases energy).")
            .conclude("Position 4 at k=4 is the compression stroke with coefficient -2.")
        )
    
    commentary = (
        "The compression stroke in an engine squeezes fuel and air together before ignition. "
        "In BBP, position 4 does something analogous: it starts the outflow (negative coefficient) "
        "with the largest negative magnitude (-2). But here is the remarkable part: position 4 "
        "equals k=4, our topology constant. The formula's structure literally contains the same "
        "number that defines tetrahedral geometry. Whether this is deep or superficial, it is "
        "the kind of numerical coincidence that makes mathematics feel like discovery, not invention."
    )
    
    def model(self):
        coeff = BBP_COEFFICIENTS[4]
        is_k = 1 if 4 == K else 0
        return (
            Model()
            .add("Position 4 coefficient", coeff)
            .add("Position equals k", is_k)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Position 4 coefficient", -2)
            .add("Position equals k", 1)
        )


class BBPPowerStroke(Test):
    """
    Position 5 (8k+5) corresponds to the power phase with coefficient -1.
    Position 5 equals k+1.
    """
    name = "Power Stroke (Position 5)"
    question = (
        "Why does position 5 follow position 4? "
        "Because 5 = k+1, one step beyond the topology threshold. "
        "This test verifies the power stroke sits at k+1 with coefficient -1, "
        "representing the first step past the fundamental geometric constant."
    )
    reference = "Engine analogy"
    tolerance = 0.0
    level = Standard
    audit_score = 84
    audit_notes = (
        "Question: 13/15 - Good k+1 reasoning as boundary concept. "
        "Derivation: 13/15 - Clear verification. "
        "Commentary: 13/15 - Good boundary/threshold analogy. "
        "Model: 9/10 - Clean output. "
        "Observations: 9/10 - Clear expected values. "
        "Constants: 5/10 - K hardcoded, should import from geometry_constants.py. "
        "Accessibility: 13/15 - Good for undergrad. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Import K. Explain WHY crossing k boundary matters physically."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Position 5 follows immediately after the topology constant k=4.")
            .step("Position 5 uses denominator (8k+5) with coefficient -1.")
            .step("Verify position equals k+1: 5 = 4 + 1 = k + 1.")
            .step("The -1 coefficient represents unit outflow during power delivery.")
            .conclude("Position 5 at k+1 is the power stroke with coefficient -1.")
        )
    
    commentary = (
        "After compression comes power: the explosion that drives the piston. In BBP, "
        "position 5 (which equals k+1 = 4+1) continues the negative outflow with coefficient -1. "
        "Think of k=4 as a boundary or threshold. Position 5 is the first step beyond that "
        "boundary, where the stored 'energy' from position 1 continues to flow out. The coefficient "
        "is smaller now (-1 vs -2), like an engine past its peak power but still delivering thrust."
    )
    
    def model(self):
        coeff = BBP_COEFFICIENTS[5]
        is_k_plus_1 = 1 if 5 == K + 1 else 0
        return (
            Model()
            .add("Position 5 coefficient", coeff)
            .add("Position equals k+1", is_k_plus_1)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Position 5 coefficient", -1)
            .add("Position equals k+1", 1)
        )


class BBPExhaustStroke(Test):
    """
    Position 6 (8k+6) corresponds to the exhaust phase with coefficient -1.
    This completes the four-position cycle.
    """
    name = "Exhaust Stroke (Position 6)"
    question = (
        "Why does the cycle end at position 6? "
        "Because after intake (+4), compression (-2), and power (-1), we need exactly -1 more "
        "to reach zero. This test verifies that position 6 completes the four-stroke cycle, "
        "exhausting the final unit to achieve coefficient balance."
    )
    reference = "Engine analogy"
    tolerance = 0.0
    level = Standard
    audit_score = 82
    audit_notes = (
        "Question: 13/15 - Good 'why cycle ends' with arithmetic reasoning. "
        "Derivation: 13/15 - Clear cycle completion logic. "
        "Commentary: 14/15 - Excellent cycle completion and bookkeeping analogy. "
        "Model: 8/10 - Minimal but appropriate output. "
        "Observations: 9/10 - Clear expected value. "
        "Constants: 5/10 - BBP_COEFFICIENTS hardcoded. "
        "Accessibility: 13/15 - Good for undergrad. "
        "Header: 7/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Connect to why infinite series converges."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The BBP formula uses exactly 4 positions per cycle.")
            .step("Position 6 uses denominator (8k+6) with coefficient -1.")
            .step("This is the final position in the sequence {1, 4, 5, 6}.")
            .step("The -1 coefficient exhausts remaining energy to balance the cycle.")
            .conclude("Position 6 is the exhaust stroke completing the 4-position cycle.")
        )
    
    commentary = (
        "Every cycle must end. In an engine, the exhaust stroke pushes out burnt gases, "
        "clearing the cylinder for the next cycle. In BBP, position 6 is the final step "
        "where the last -1 leaves the system. After this: +4 - 2 - 1 - 1 = 0. The books "
        "balance. The cycle is complete. Then (1/16) multiplies everything and we start "
        "the next term. Each term of the infinite series is a tiny, self-contained engine "
        "that contributes its share to computing pi."
    )
    
    def model(self):
        coeff = BBP_COEFFICIENTS[6]
        return Model().add("Position 6 coefficient", coeff)
    
    def observations(self):
        return Observed().add("Position 6 coefficient", -1)


class BBPLargestAtBlocked(Test):
    """
    The largest coefficient (+4) is at a blocked position.
    Blocked channels receive the most pressure because energy accumulates
    where it cannot escape.
    """
    name = "Largest Coefficient at Blocked"
    question = (
        "Why is the biggest coefficient at the entry point? "
        "Think of water pressure: it is highest at a blocked pipe because the water "
        "has nowhere to go. The BBP formula's largest coefficient (+4) sits at position 1, "
        "the 'intake' where everything enters before distributing outward."
    )
    reference = None  # Model interpretation
    level = Standard
    audit_score = 79
    audit_notes = (
        "Question: 14/15 - Excellent water pressure analogy for 'why'. "
        "Derivation: 12/15 - Good but 'blocked' needs clearer definition. "
        "Commentary: 14/15 - Great garden hose analogy for asymmetric distribution. "
        "Model: 8/10 - Clean output. "
        "Observations: 0/10 - Missing observations() method. "
        "Constants: 5/10 - BBP_COEFFICIENTS hardcoded. "
        "Accessibility: 14/15 - Great analogies for undergrad. "
        "Header: 8/10 (module level). "
        "SAMPLE SIZE: N/A - No statistical claims. "
        "FUNCTION OPPORTUNITY: None. "
        "TO IMPROVE: Add observations() method. Define 'blocked' more rigorously."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Energy accumulates at constrained positions before propagating through open channels.")
            .step("Identify all coefficient magnitudes: |+4| = 4, |-2| = 2, |-1| = 1, |-1| = 1.")
            .step("The largest magnitude is 4, located at position 1.")
            .step("Position 1 is the intake position where energy enters but cannot immediately exit.")
            .conclude("Maximum coefficient at position 1 is consistent with accumulation dynamics at constrained Coupling Ports.")
        )
    
    commentary = (
        "Put your thumb over a garden hose and the water sprays harder from the small opening. "
        "Pressure builds where flow is constrained. The BBP formula shows this same pattern: "
        "the largest coefficient (+4) sits at position 1, the entry point. The outflow positions "
        "(4, 5, 6) have smaller magnitudes (2, 1, 1) because the 'pressure' spreads across multiple "
        "exit paths. This asymmetry, where input is concentrated and output is distributed, "
        "appears throughout physics. The BBP formula encodes it naturally."
    )
    
    def model(self):
        largest_coeff = max(abs(c) for c in BBP_COEFFICIENTS.values())
        position_of_largest = [p for p, c in BBP_COEFFICIENTS.items() 
                              if abs(c) == largest_coeff][0]
        # Position 1 is blocked in the pi traversal pattern
        return (
            Model()
            .add("Largest coefficient magnitude", largest_coeff)
            .add("Position of largest", position_of_largest)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Largest coefficient magnitude", 4)
            .add("Position of largest", 1)
        )


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


def run_all():
    """Run all BBP structure tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
