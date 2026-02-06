"""
SANDBOX: <Specific Descriptive Topic>
=====================================

STATUS: Work in progress.

NAMING REQUIREMENTS:
--------------------
File names MUST be descriptive and specific. Follow this pattern:
    sandbox_<domain>_<specific_phenomenon>_<focus>.py

GOOD examples:
    sandbox_gw_quadrupole_coefficient_32.py
    sandbox_bh_isco_geometric_factor.py
    sandbox_ns_density_nuclear_ratio.py

BAD examples:
    sandbox_gw_probing.py        (too vague: "probing" what?)
    sandbox_stuff.py             (meaningless)
    sandbox_physics.py           (everything is physics)

COPY THIS FILE:
    cp sandbox_template.py sandbox_<domain>_<phenomenon>_<focus>.py

RUN:
    python -m gravity_field_model.calculations.sandbox.sandbox_<your_descriptive_name>

EXPLORING:
- <What specific question are you trying to answer?>
- <What specific patterns are you looking for?>
- <What standard physics are you verifying?>

GRADUATION CHECKLIST:
[ ] File name is descriptive (not "probing" or "stuff")
[ ] All tests pass
[ ] audit_score >= 65 (quality, see TEST_QUALITY_FRAMEWORK.md)
[ ] contribution_score assessed (see CONTRIBUTION_SCORING_FRAMEWORK.md)
[ ] Move to appropriate domain folder
[ ] Rename to test_<domain>_<phenomenon>_<focus>.py
[ ] Delete this sandbox file

GFD Model V2

HONESTY STATEMENT:
This module verifies STANDARD <DOMAIN> PHYSICS and explores potential
GFD correspondences. The physics is well established. GFD provides
a geometric framework for interpretation but does NOT derive these
values from first principles.

WHAT IS VERIFIED (standard physics):
- <List what you're verifying from established theory>

GFD OBSERVATIONS (patterns noted, not derived):
- <List any GFD patterns you're documenting>

TARGET DOMAIN FOLDER: calculations/<domain>/
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    G, C, HBAR, K_B,
    # Add other constants as needed
)


# =============================================================================
# CONSTANTS (document sources)
# =============================================================================

# Example: CODATA 2022 values imported from common module
# If you need domain-specific constants, define them here with sources


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def example_calculation(x: float) -> float:
    """
    Brief description of what this calculates.
    
    Consider: Should this become an @Fn function for reuse?
    """
    return x * 2  # Replace with actual calculation


# =============================================================================
# TESTS
# =============================================================================

class ExampleProbingTest(Test):
    """
    Brief description of what this test probes.
    
    HONESTY: <What is standard physics vs what is GFD observation>
    """
    # QUALITY: How well is this test written? (0-100)
    # See TEST_QUALITY_FRAMEWORK.md for criteria
    audit_score = None  # Set after audit (target >= 75)
    audit_notes = None  # Fill in during audit
    
    # CONTRIBUTION: How valuable are the findings? (0-100)
    # See CONTRIBUTION_SCORING_FRAMEWORK.md for criteria
    # - Discovery Value (0-40): What's new?
    # - Precision & Rigor (0-20): How confident?
    # - Cross-Domain Impact (0-20): Connects domains?
    # - Falsifiability (0-20): Makes predictions?
    contribution_score = None  # Set after contribution assessment
    contribution_notes = None  # Explain the score
    
    future_questions = (
        "Q1: <Probing question that would deepen understanding>? "
        "(Answering would improve <Aspect> by +N points: <benefit>) "
        "Q2: <Another probing question>? "
        "(Answering would improve <Aspect> by +N points: <benefit>) "
        "Q3: <Third probing question>? "
        "(Answering would improve <Aspect> by +N points: <benefit>)"
    )
    name = "Example Probing Test"
    question = (
        "Why does <phenomenon> have <specific value>? "
        "<What is the physical mystery or curiosity?> "
        "<What would it mean if we found an answer?>"
    )
    reference = "<Source, e.g., CODATA 2022, Author (Year)>"
    tolerance = 0.01  # Adjust based on expected precision
    level = Level.EXPLORATORY  # CRITICAL, STANDARD, or EXPLORATORY
    commentary = (
        "<Explain the significance of what we're testing.> "
        "<Connect to the bigger picture.> "
        "<Note what is standard physics vs GFD observation.> "
        "<Add an analogy if helpful.>"
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CONTEXT: <Set up the physical situation>")
            .step("THE QUESTION: <What are we trying to understand?>")
            .step("<Logical step 1>")
            .step("<Logical step 2>")
            .equation("<Key equation>")
            .step("GFD OBSERVATION: <Pattern noted, if any>")
            .conclude("<What we learn from this>")
        )
    
    def model(self) -> Model:
        # Calculate model predictions
        calculated_value = example_calculation(1.0)
        
        return (
            Model()
            .add("Calculated value", calculated_value)
            .add("Pattern check", 1.0 if calculated_value > 0 else 0.0)
        )
    
    def observations(self) -> Observed:
        # Expected values (from standard physics or measurement)
        return (
            Observed()
            .add("Calculated value", 2.0)  # Source: <cite>
            .add("Pattern check", 1.0)
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    ExampleProbingTest,
    # Add more test classes here
]


def run_all() -> bool:
    """Run all sandbox tests."""
    return run_tests(
        title="SANDBOX: <Topic> Probing Tests",
        summary=(
            "STATUS: Work in progress\n\n"
            "EXPLORING:\n"
            "- <What this sandbox is investigating>\n\n"
            "WHEN READY:\n"
            "- audit_score >= 75\n"
            "- Move to calculations/<domain>/test_<topic>.py"
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
