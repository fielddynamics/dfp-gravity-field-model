"""
UAT Stage (User Acceptance Testing)
===================================

Tests move here from dev/ after passing desk rejection checks.
UAT writes the academic_paper here, then triggers PROD peer review.

Pipeline flow:
    dev/ -> uat/ -> prod/

In the serial pipeline:
1. Test is in dev/ (START_RESEARCH_MODULE scores, audit_score >= 85)
2. UAT checks desk rejection rules
3. UAT moves test from dev/ to uat/
4. UAT writes academic_paper (400-700 words) to test in uat/
5. UAT kicks off PROD for peer review
6. PROD moves test from uat/ to prod/ (accepted) or deletes from uat/ (rejected)

Tests in this folder:
    - Have passed desk rejection checks
    - Have academic_paper written by UAT
    - Are awaiting or undergoing peer review

Thresholds:
    - audit_score >= 85 (checked at entry)
    - academic_paper: 400-700 words (written by UAT)
"""

AUDIT_THRESHOLD = 85
ACADEMIC_PAPER_MIN_WORDS = 400
ACADEMIC_PAPER_MAX_WORDS = 700
