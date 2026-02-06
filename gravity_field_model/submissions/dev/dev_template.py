"""
DEV: <Specific Descriptive Topic>
=================================

STATUS: Work in progress.

CRITICAL: ONE TEST PER FILE
---------------------------
Each dev file should contain ONE test class investigating ONE question.
Do NOT create test groups during development. Test groups are for organizing
graduated production tests, not for development.

WHY SINGLE TESTS?
- Each test requires its own academic_paper (written by UAT, not DEV)
- Each test goes through peer review independently
- Quality is easier to achieve with focused scope
- Rejection = DELETION, so smaller scope = smaller risk

NAMING REQUIREMENTS:
--------------------
File names MUST be descriptive and specific. Follow this pattern:
    dev_<domain>_<specific_phenomenon>_<focus>.py

GOOD examples:
    dev_gw_chirp_mass_exponent.py
    dev_bh_isco_geometric_factor.py
    dev_ns_density_nuclear_ratio.py

BAD examples:
    dev_gw_probing.py        (too vague: "probing" what?)
    dev_gw_tests.py          (multiple tests, should be ONE)
    dev_stuff.py             (meaningless)

COPY THIS FILE:
    cp dev_template.py dev_<domain>_<phenomenon>_<focus>.py

RUN:
    python -m gravity_field_model.submissions.dev.dev_<your_descriptive_name>

PIPELINE FOLDER: gravity_field_model/submissions/
    dev/ -> uat/ -> prod/

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

GRADUATION CHECKLIST (before calling process_for_production):
=============================================================
[ ] File name is descriptive (not "probing" or "stuff")
[ ] Only ONE test class in file
[ ] question is set (non-empty string)
[ ] commentary is set (non-empty string)
[ ] Has derivation() or observations() or model() method
[ ] All tests pass
[ ] audit_score >= 85 (quality, see TEST_QUALITY_MODULE.md)
[ ] academic_paper = None (UAT will write this)
[ ] contribution_score = None (PROD will assign this)
[ ] Call process_for_production() to submit for peer review

IF AUDIT_SCORE < 85:
- Test remains in dev until quality improved
- Review TEST_QUALITY_MODULE.md for scoring criteria
- Improve documentation, derivation clarity, or commentary

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

TARGET DOMAIN FOLDER: submissions/prod/
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    G, C, HBAR, K_B,
    # Add other constants as needed
)


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
#     equation="result = input * constant",
#     inputs={"input_var": "type: description"},
#     outputs={"result": "type: description"},
#     description="Clear description of what this function does.",
# )
# def fn_calc_something(input_var: float) -> float:
#     """Compute something from input."""
#     return input_var * CONSTANT


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
#       get_something = Depends(fn_calc_something)  # Inject function
#       
#       def model(self):
#           value = self.get_something(input)  # Use injected function


class YourDescriptiveTestName(Test):
    """
    FEYNMAN-STYLE TEST TEMPLATE
    
    Follow the "Why Before What" principle:
    1. QUESTION: Hook the reader's curiosity (the mystery)
    2. DERIVATION: Build mental scaffolding (intuition before math)
    3. MODEL: Show the data (reader is now ready)
    4. COMMENTARY: Deliver the "aha" moment (the insight)
    """
    
    # Clear, descriptive name that hints at the mystery
    name = "<Descriptive Test Name>"
    
    # QUESTION: Hook the reader's curiosity
    # - Establish the physical mystery FIRST
    # - Make them WANT to know the answer
    # - Hint at what failure would mean
    question = (
        "<What specific question are you investigating? "
        "Make it compelling and clear.>"
    )
    
    # Where the expected value comes from
    reference = "<Source of expected value>"
    
    # Acceptable percent error (0.01 = 1%, 0.10 = 10%)
    tolerance = 0.05
    
    # CRITICAL = must pass, STANDARD = should pass, EXPLORATORY = informational
    level = Level.STANDARD
    
    # COMMENTARY: Deliver the insight, not just the numbers
    # Structure: ANSWER + SIGNIFICANCE + ANALOGY + IMPLICATION
    commentary = (
        "<What do the results mean? What's the insight? "
        "What would this imply if true?>"
    )
    
    # =========================================================================
    # SCORING (assigned at different pipeline stages)
    # =========================================================================
    
    # audit_score: Assigned by START_RESEARCH_MODULE (test quality assessment)
    # Range: 0-100, threshold >= 85 for UAT promotion
    audit_score = None  # START_RESEARCH_MODULE assigns this
    audit_notes = ""
    
    # =========================================================================
    # DO NOT SET THESE IN DEV (desk rejection if present)
    # =========================================================================
    
    # academic_paper: Written by UAT_MODULE after test is accepted to UAT
    # DO NOT set this in DEV stage. UAT writes the 400-700 word paper.
    academic_paper = None  # UAT_MODULE writes this
    
    # contribution_score: Assigned by PROD_MODULE during peer review
    # Range: 0-100, threshold >= 70 for production acceptance
    # DO NOT set this yourself. PROD_MODULE assigns it as the journal review.
    contribution_score = None  # PROD_MODULE assigns this

    def derivation(self):
        """
        DERIVATION: Build mental scaffolding
        
        Guide through the logic step by step:
        1. What physical law are we starting from?
        2. What assumptions are we making?
        3. What GFD patterns do we observe?
        
        Returns:
            Derivation object with detailed steps
        """
        return Derivation(
            steps=[
                "Step 1: <Start with what the reader already knows>",
                "Step 2: <Build the intuition before showing math>",
                "Step 3: <Show the mathematical relationship>",
                "Step 4: <Apply to our specific case>",
            ],
        )

    def model(self):
        """
        MODEL: Compute and compare
        
        Now that the reader understands WHY, show them the data.
        
        Returns:
            Model object with expected and actual values
        """
        # Expected from established physics/literature
        expected = 0.0  # Replace with actual expected value
        
        # Computed from GFD model
        computed = 0.0  # Replace with actual computation
        
        return Model(
            expected=expected,
            actual=computed,
            tolerance=self.tolerance,
        )


# =============================================================================
# MAIN (for testing)
# =============================================================================
if __name__ == "__main__":
    from gravity_field_model.run_test import run_tests
    run_tests([YourDescriptiveTestName])
