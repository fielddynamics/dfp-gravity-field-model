"""
Pipeline Module
===============

All CI/CD pipeline implementation code lives here.

Files:
    gate.py            - UAT gate (eligibility checks, orchestration)
    reviewer.py        - PROD reviewer (peer review, contribution_score)
    paper_generator.py - Academic paper validation and generation

Drop folders for test files:
    gravity_field_model/submissions/dev/   - Development
    gravity_field_model/submissions/uat/   - UAT processing
    gravity_field_model/submissions/prod/  - Production

Flow: dev/ -> uat/ -> prod/
"""

from .gate import (
    check_eligibility,
    process_for_production,
    list_dev_tests,
    list_prod_tests,
    print_pipeline_status,
    AUDIT_THRESHOLD,
    AUDIT_INFLATION_TOLERANCE,
)
from .reviewer import (
    review_submission,
    ACCEPTANCE_THRESHOLD,
    CONTRIBUTION_THRESHOLD,
)
from .paper_generator import (
    validate_honesty,
    extract_test_info,
    generate_paper,
    PAPER_WORD_MIN,
    PAPER_WORD_MAX,
)

__all__ = [
    # Gate
    "check_eligibility",
    "process_for_production",
    "list_dev_tests",
    "list_prod_tests",
    "print_pipeline_status",
    "AUDIT_THRESHOLD",
    "AUDIT_INFLATION_TOLERANCE",
    # Reviewer
    "review_submission",
    "ACCEPTANCE_THRESHOLD",
    "CONTRIBUTION_THRESHOLD",
    # Paper
    "validate_honesty",
    "extract_test_info",
    "generate_paper",
    "PAPER_WORD_MIN",
    "PAPER_WORD_MAX",
]
