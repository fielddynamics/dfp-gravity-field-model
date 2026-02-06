"""
Submissions Pipeline Folders
============================

This is the SINGLE location for all test submissions through the CI/CD pipeline.

Structure:
    submissions/
    ├── dev/           # Development stage (tests being created)
    └── prod/          # Production (peer-reviewed, accepted tests)
        └── archive/   # Archived review reports

Serial Pipeline Flow (agent-driven):
    1. DEV: Test created in dev/, scored (audit_score >= 85)
    2. UAT: Desk rejection check, write academic_paper, kick off PROD
    3. PROD: Peer review, assign contribution_score
       - Accept: Move to prod/
       - Reject: Delete test, archive report

Note: UAT is a processing step, not a folder. Tests move directly from dev/ to prod/.

WHO SETS WHAT:
    DEV stage:  question, commentary, methods, audit_score
    UAT step:   academic_paper (400-700 words)
    PROD step:  contribution_score (peer review)

Thresholds:
    - audit_score >= 85 for UAT processing
    - contribution_score >= 70 for PROD acceptance
"""

# Pipeline folder paths (relative to this package)
DEV_FOLDER = "dev"
PROD_FOLDER = "prod"
PROD_ARCHIVE_FOLDER = "prod/archive"
