"""
UAT (User Acceptance Testing) Folder
=====================================

This folder is GUARDED by UAT_MODULE.

Tests here have passed automated quality checks:
- audit_score >= 85 (quality gate from TEST_QUALITY_MODULE)
- academic_paper property exists (400-700 words)

NOTE: contribution_score is NOT checked by UAT.
      It is assigned by PROD_MODULE during peer review.

STATES:
- pending/: Passed automated checks, awaiting approval
- approved/: Approved, awaiting peer review

DO NOT manually add files here. Use the UAT API:
    from gravity_field_model.pipeline import process_for_production

See framework/UAT_MODULE.md for full documentation.
"""

# Graduation thresholds (single source of truth for UAT decisions)
AUDIT_THRESHOLD = 85
ACADEMIC_PAPER_WORD_LIMIT = 700
