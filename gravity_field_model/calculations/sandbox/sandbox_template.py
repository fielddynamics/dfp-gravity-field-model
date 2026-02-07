"""
SANDBOX: <Specific Descriptive Topic>
=====================================

STATUS: Work in progress.

CRITICAL: ONE TEST PER FILE
---------------------------
Each sandbox file should contain ONE test class investigating ONE question.
Do NOT create test groups during development. Test groups are for organizing
graduated production tests, not for development.

WHY SINGLE TESTS?
- Each test requires its own academic_paper (400-700 words)
- Each test goes through peer review independently
- Quality is easier to achieve with focused scope
- Rejection = DELETION, so smaller scope = smaller risk

NAMING REQUIREMENTS:
--------------------
File names MUST be descriptive and specific. Follow this pattern:
    sandbox_<domain>_<specific_phenomenon>_<focus>.py

GOOD examples:
    sandbox_gw_chirp_mass_exponent.py
    sandbox_bh_isco_geometric_factor.py
    sandbox_ns_density_nuclear_ratio.py

BAD examples:
    sandbox_gw_probing.py        (too vague: "probing" what?)
    sandbox_gw_tests.py          (multiple tests, should be ONE)
    sandbox_stuff.py             (meaningless)

COPY THIS FILE:
    cp sandbox_template.py sandbox_<domain>_<phenomenon>_<focus>.py

RUN:
    python -m gravity_field_model.calculations.sandbox.sandbox_<your_descriptive_name>

EXPLORING:
- <What ONE specific question are you trying to answer?>
- <What ONE specific pattern are you looking for?>
- <What standard physics are you verifying?>

WHO SETS WHAT (Pipeline Stages):
=================================
| Field             | Set By         | When                  |
|-------------------|----------------|-----------------------|
| question          | DEV (you)      | During test creation  |
| commentary        | DEV (you)      | During test creation  |
| audit_score       | START_RESEARCH_MODULE | After quality audit   |
| academic_paper    | UAT_MODULE     | After UAT acceptance  |
| contribution_score| PROD_MODULE    | During peer review    |

DESK REJECTION RULES (UAT Guards):
===================================
Your test will be DESK REJECTED if ANY fail:

  DEV MUST SET:
  [X] ONE TEST CLASS per file         Multiple tests = REJECT
  [X] question = "..."                Empty or missing = REJECT  
  [X] commentary = "..."              Empty or missing = REJECT
  [X] derivation/observations/model   At least ONE method = REJECT
  [X] audit_score >= 85               Below 85 = REJECT

  DEV MUST NOT SET (desk reject if present):
  [X] academic_paper = None           If set by DEV = REJECT (UAT writes it)
  [X] contribution_score = None       If set by DEV = REJECT (PROD sets it)

GRADUATION CHECKLIST (before calling request_promotion):
========================================================
[ ] File name is descriptive (not "probing" or "stuff")
[ ] Only ONE test class in file
[ ] question is set (non-empty string)
[ ] commentary is set (non-empty string)
[ ] Has derivation() or observations() or model() method
[ ] All tests pass
[ ] audit_score >= 85 (quality, see TEST_QUALITY_MODULE.md)
[ ] academic_paper = None (UAT will write this)
[ ] contribution_score = None (PROD will assign this)
[ ] Call request_promotion() to move to UAT

IF AUDIT_SCORE < 85:
- Test remains in sandbox until quality improved
- Review TEST_QUALITY_MODULE.md for scoring criteria
- Improve documentation, derivation clarity, or commentary

GFM Model V2

HONESTY STATEMENT:
This module verifies STANDARD <DOMAIN> PHYSICS and explores potential
GFM correspondences. The physics is well established. GFM provides
a geometric framework for interpretation but does NOT derive these
values from first principles.

WHAT IS VERIFIED (standard physics):
- <List what you're verifying from established theory>

GFM OBSERVATIONS (patterns noted, not derived):
- <List any GFM patterns you're documenting>

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
    
    HONESTY: <What is standard physics vs what is GFM observation>
    """
    # QUALITY: How well is this test written? (0-100)
    # See TEST_QUALITY_MODULE.md for criteria
    audit_score = None  # Set after audit (target >= 75)
    audit_notes = None  # Fill in during audit
    
    # CONTRIBUTION: How valuable are the findings? (0-100)
    # See CONTRIBUTION_SCORING_MODULE.md for criteria
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
        "<Note what is standard physics vs GFM observation.> "
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
            .step("GFM OBSERVATION: <Pattern noted, if any>")
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
            "GRADUATION CRITERIA (for UAT promotion):\n"
            "- audit_score >= 85 (quality, high bar)\n"
            "- academic_paper property (400-700 words)\n\n"
            "If criteria not met, test remains in sandbox for improvement."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
