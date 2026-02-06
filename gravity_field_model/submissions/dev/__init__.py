"""
DEV Stage (Development/Sandbox)
===============================

This folder contains tests under development.

Pipeline flow:
    dev/ -> uat/ -> prod/

REQUIRED at DEV submission:
    - question (non-empty string)
    - commentary (non-empty string)
    - derivation() or observations() or model() method
    - audit_score >= 85

MUST BE None at DEV submission (desk rejection if set):
    - academic_paper (UAT writes this after moving to uat/)
    - contribution_score (PROD assigns this during peer review)

Naming Convention:
    dev_<domain>_<specific_phenomenon>_<focus>.py

Example:
    dev_gw_chirp_mass_exponent.py

To process through pipeline:
    from gravity_field_model.pipeline import process_for_production
    result = process_for_production("dev/dev_my_test.py")
    
What happens:
1. UAT validates desk rejection rules
2. UAT moves test from dev/ to uat/ (renamed dev_* -> test_*)
3. UAT writes academic_paper (400-700 words)
4. UAT triggers PROD peer review
5. PROD moves to prod/ (accept) or deletes from uat/ (reject)
"""
