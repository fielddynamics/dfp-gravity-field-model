"""
PROD Stage (Production)
=======================

Tests that passed peer review. PROD_MODULE has assigned contribution_score.

Pipeline flow:
    dev/ -> uat/ -> prod/

Tests move here from uat/ after PROD_MODULE accepts them.

Subfolders:
    archive/   - Archived review reports (accepted and rejected)

At PROD stage:
    - PROD_MODULE reviews test in uat/
    - PROD_MODULE assigns contribution_score
    - If accepted (score >= 70): move from uat/ to prod/
    - If rejected: delete from uat/, archive report

Thresholds:
    - contribution_score >= 70 for production acceptance
    - Total review score >= 80 for acceptance
"""

CONTRIBUTION_THRESHOLD = 70
ACCEPTANCE_THRESHOLD = 80
