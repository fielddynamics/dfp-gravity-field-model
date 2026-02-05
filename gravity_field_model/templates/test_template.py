"""
Test Template: [CATEGORY NAME]
==============================

Copy this template when creating new tests. Follow the TEST_QUALITY_FRAMEWORK.md.

Architecture (Three Layers):
1. CONSTANTS: Import from constants_codata.py (never hardcode)
2. FUNCTIONS: Define with @Fn decorator (reusable, documented)
3. TESTS: Validate functions using Depends() injection

Reference example: gravity_field_model/examples/example_power_output.py

Before writing:
1. What question does this test answer? (Hook the curiosity)
2. What would failure mean? (Stakes)
3. What is the pass/fail criterion? (Clear verdict)

Delete these instructions after copying.
"""

from gravity_field_model.framework import *

# =============================================================================
# LAYER 1: CONSTANTS (never hardcode, always import)
# =============================================================================
# Import only the constants you need from common:
# from gravity_field_model.common.constants_codata import C, HBAR, ALPHA, EV

# If you need derived constants, compute them from CODATA values:
# MEV_TO_JOULES = EV * 1e6  # Derived from CODATA EV


# =============================================================================
# LAYER 2: REUSABLE FUNCTIONS (with @Fn decorator)
# =============================================================================
#
# Naming convention (Command Query Pattern):
#   fn_get_<what>()   - Query: returns data, no side effects
#   fn_calc_<what>()  - Query: returns computed value
#   fn_set_<what>()   - Command: modifies state (rare)
#
# Example:
#
# @Fn(
#     equation="P(A) = BE(A) * f_closure",
#     inputs={"mass_number": "int: Mass number A (nucleon count)"},
#     outputs={"watts": "float: Power output in watts"},
#     description=(
#         "Computes power output per gravity field from binding energy. "
#         "Peaks at Fe-56 where binding energy per nucleon is maximum."
#     ),
# )
# def fn_get_power_output(mass_number: int) -> float:
#     """
#     Query: Get power output for a given mass number.
#     
#     This function is registered automatically and can be injected
#     into tests using: get_power = Depends(fn_get_power_output)
#     """
#     be_mev = get_binding_energy(mass_number)
#     return be_mev * MEV_TO_JOULES * F_CLOSURE


# =============================================================================
# LAYER 3: TESTS (validate and use functions via Depends)
# =============================================================================
#
# Test Levels:
#   CRITICAL    - Validates core functions, must pass
#   STANDARD    - Uses validated functions, normal tests  
#   EXPLORATORY - Edge cases, may fail without crisis
#
# Dependency Pattern:
#   class MyTest(Test):
#       get_power = Depends(fn_get_power_output)  # Inject function
#       
#       def model(self):
#           value = self.get_power(56)  # Use injected function
#


# =============================================================================
# TEMPLATE: FUNCTION + TEST PATTERN (Complete Example)
# =============================================================================

class ExampleGoodTest(Test):
    """
    FEYNMAN-STYLE TEST TEMPLATE
    
    Follow the "Why Before What" principle:
    1. QUESTION: Hook the reader's curiosity (the mystery)
    2. DERIVATION: Build mental scaffolding (intuition before math)
    3. MODEL: Show the data (reader is now ready)
    4. COMMENTARY: Deliver the "aha" moment (the insight)
    """
    
    # Clear, descriptive name that hints at the mystery
    name = "Fine Structure Constant from Geometry"
    
    # QUESTION: Hook the reader's curiosity
    # - Establish the physical mystery FIRST
    # - Make them WANT to know the answer
    # - Hint at what failure would mean
    question = (
        "Can we derive the fine structure constant (alpha = 1/137) from pure "
        "geometry, or is it just a number we have to measure?"
    )
    
    # Where the expected value comes from
    reference = "CODATA 2022"
    
    # Acceptable percent error (0.01 = 1%, 0.10 = 10%)
    tolerance = 0.05
    
    # CRITICAL = must pass, STANDARD = should pass, EXPLORATORY = informational
    level = Level.STANDARD
    
    # COMMENTARY: Deliver the insight, not just the numbers
    # Structure: ANSWER + SIGNIFICANCE + ANALOGY + IMPLICATION
    commentary = (
        "The geometric ratio matches the fine structure constant to within 0.1%. "
        "This suggests alpha may not be arbitrary: it could emerge from the "
        "fundamental shape of field interactions, much like pi emerges from "
        "circles. If confirmed, this would mean the strength of electromagnetism "
        "is determined by geometry, not by accident."
    )

    def derivation(self) -> Derivation:
        """
        FEYNMAN-STYLE DERIVATION
        
        Structure:
        1. SITUATION: What are we looking at? (No math yet)
        2. TENSION: What's the puzzle or question?
        3. INSIGHT: What key idea might resolve it?
        4. MATH: Now the equations (reader is ready)
        5. CRITERION: How do we judge success?
        """
        return (
            Derivation()
            # 1. SITUATION: Set the scene in plain language
            .step(
                "THE MYSTERY: The fine structure constant alpha = 1/137.036 "
                "controls how strongly electrons interact with light. But why "
                "this specific value? Physicists have wondered for a century "
                "whether it's just a measured accident or something deeper."
            )
            # 2. TENSION: What's the puzzle?
            .step(
                "THE QUESTION: If we construct a stellated octahedron (two "
                "interlocking tetrahedra), does any natural ratio equal alpha?"
            )
            # 3. INSIGHT: The key idea
            .step(
                "THE APPROACH: Compare the ratio of inner to outer radii. "
                "If geometry determines physics, this ratio might match alpha."
            )
            # 4. MATH: Now they're ready for it
            .equation("alpha_geometric = r_inner / r_outer")
            .equation("alpha_measured = 1 / 137.035999084 (CODATA 2022)")
            # 5. CRITERION: How do we judge?
            .step("CRITERION: Match within 1% suggests geometric origin.")
            .conclude(
                "If the geometric ratio matches alpha, we have evidence that "
                "the fine structure constant emerges from shape, not chance."
            )
        )

    def model(self) -> Model:
        """Compute the values. Return summary statistics, not raw dumps."""
        # Example calculation
        alpha_geometric = 0.007297  # Hypothetical geometric derivation
        alpha_measured = 1 / 137.035999084
        error_pct = abs(alpha_geometric - alpha_measured) / alpha_measured * 100
        
        return (
            Model()
            .add("Geometric alpha", round(alpha_geometric, 6))
            .add("Measured alpha (CODATA)", round(alpha_measured, 6))
            .add("Difference %", round(error_pct, 3))
            .add("Match within 1%", 1.0 if error_pct < 1 else 0.0)
        )

    def observations(self) -> Observed:
        """Reference values to compare against."""
        # Only compare the verdict, not intermediate calculations
        return (
            Observed()
            .add("Match within 1%", 1.0)
        )


# =============================================================================
# TEMPLATE: STATISTICAL TEST (for distributions/counts)
# =============================================================================

class ExampleStatisticalTest(Test):
    """
    FEYNMAN-STYLE STATISTICAL TEST
    
    When analyzing distributions, the question is never "what are the counts?"
    The question is always about fairness, bias, or uniformity: a physical
    property that the statistics reveal.
    """
    
    name = "Traversal Fairness Check"
    
    # QUESTION: Hook with the physical mystery, not the math
    question = (
        "Does the algorithm explore all regions equally, or does it have "
        "blind spots that could skew our results?"
    )
    
    reference = "Statistical uniformity"
    tolerance = 0.20
    level = Level.STANDARD
    
    # COMMENTARY: Insight, not just restating numbers
    commentary = (
        "The algorithm is remarkably fair. Like a well-balanced die that lands "
        "on each face within 2% of perfect equality, our traversal visits every "
        "region with near-uniform frequency. This means we can trust aggregate "
        "statistics: no region is over- or under-sampled. If CV had been high "
        "(say, 30%), we'd know certain regions were being neglected, and our "
        "conclusions about the whole shape would be unreliable."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            # SITUATION: Set the scene
            .step(
                "THE SITUATION: We have an algorithm that visits different "
                "regions of a geometric shape. We need to know if it's fair: "
                "does every region get roughly equal attention?"
            )
            # TENSION: Why this matters
            .step(
                "WHY IT MATTERS: If some regions get visited 10x more than "
                "others, our aggregate statistics would be skewed. We'd be "
                "measuring some areas thoroughly and others barely at all."
            )
            # INSIGHT: The approach (use analogy)
            .step(
                "THE APPROACH: Think of checking if a die is loaded. We roll "
                "it many times and see if each number comes up equally often. "
                "The coefficient of variation (CV) measures spread relative to "
                "average. A fair die has CV near 0; a loaded die has high CV."
            )
            # MATH: Now they're ready
            .equation("CV = standard_deviation / mean")
            .step(
                "INTERPRETATION: CV of 5% means counts vary by about 5% from "
                "average. CV of 50% means wild swings: definitely biased."
            )
            .step("CRITERION: CV < 15% indicates no significant bias.")
            .conclude(
                "If CV is low, we can trust that all regions are sampled "
                "fairly, and our conclusions apply to the whole shape."
            )
        )

    def model(self) -> Model:
        # Example: analyzing a list of counts
        values = [100, 102, 98, 101, 99, 103, 97, 100]  # Replace with actual data
        
        n = len(values)
        mean_val = sum(values) / n
        variance = sum((v - mean_val)**2 for v in values) / n
        std_dev = variance ** 0.5
        cv = std_dev / mean_val if mean_val > 0 else 0
        spread_pct = (max(values) - min(values)) / mean_val * 100 if mean_val > 0 else 0
        
        return (
            Model()
            # Summary statistics, not individual values
            .add("Regions analyzed", n)
            .add("Mean visits per region", round(mean_val, 1))
            .add("Spread (max-min)/mean %", round(spread_pct, 1))
            .add("Coefficient of variation", round(cv, 4))
            # Binary verdict
            .add("Bias detected (CV > 0.15)", 0.0 if cv < 0.15 else 1.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Bias detected (CV > 0.15)", 0.0)
        )


# =============================================================================
# TEMPLATE: THRESHOLD CHECK
# =============================================================================

class ExampleThresholdTest(Test):
    """
    Tests that check if a value is within acceptable bounds.
    """
    
    name = "Value Within Physical Bounds"
    question = "Is [quantity] within the physically allowed range?"
    reference = "Physical constraints"
    tolerance = 0.0
    level = Level.CRITICAL
    
    commentary = (
        "Value falls within expected physical bounds, confirming "
        "the model respects fundamental constraints."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CONSTRAINT: [Quantity] must satisfy lower < value < upper.")
            .step("PHYSICAL REASON: Values outside this range would violate [principle].")
            .equation("0 < value < 1  (for normalized quantities)")
            .conclude("Value within bounds confirms physical consistency.")
        )

    def model(self) -> Model:
        value = 0.73  # Replace with actual calculation
        lower_bound = 0.0
        upper_bound = 1.0
        in_range = lower_bound < value < upper_bound
        
        return (
            Model()
            .add("Measured value", value)
            .add("Lower bound", lower_bound)
            .add("Upper bound", upper_bound)
            .add("Within bounds", 1.0 if in_range else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Within bounds", 1.0)
        )


# =============================================================================
# ANTI-PATTERN: What NOT to do
# =============================================================================

# DON'T DO THIS:
#
# class BadDataDump(Test):
#     name = "Face Counts"  # Vague name
#     question = "What are the face counts?"  # Not a yes/no question
#     
#     def model(self):
#         return (
#             Model()
#             # Dumping raw values with no context
#             .add("FACE_A1", 3731)  # What does this mean?
#             .add("FACE_A2", 3710)  # Is this good or bad?
#             .add("FACE_A4", 3657)  # No criterion stated
#             .add("FACE_A7", 3656)
#             .add("FACE_B0", 3821)
#             .add("FACE_B3", 3789)
#             .add("FACE_B5", 3820)
#             .add("FACE_B6", 3795)
#             # No summary, no verdict, no meaning
#         )
#     
#     # No observations = no pass/fail comparison
#     # No commentary = reader has no idea what this proves


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ExampleGoodTest,
    ExampleStatisticalTest,
    ExampleThresholdTest,
]


def run_all() -> bool:
    """Run all tests in this module."""
    return run_tests(
        title="Template Tests",
        summary=(
            "Example tests demonstrating good patterns.\n"
            "Copy and modify for your own tests."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
