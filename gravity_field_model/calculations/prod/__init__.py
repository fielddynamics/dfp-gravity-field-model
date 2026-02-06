"""
Production Calculations Folder.

GUARDED BY: PROD_MODULE

This folder contains tests that have passed the full pipeline:
1. START_RESEARCH_MODULE assigns audit_score (model also writes academic_paper)
2. UAT_MODULE validates: audit_score >= 85, academic_paper (400-700 words)
3. PROD_MODULE peer review: contribution_score >= 70, total >= 80

Only tests with full peer review acceptance enter this folder.

Structure:
    prod/
    ├── stellar_mechanics/     # Domain folders for accepted tests
    ├── black_holes/
    ├── field_theory/
    ├── particle_physics/
    └── archive/               # Review reports for accepted tests
        └── *_REVIEW.md

Thresholds:
    - ACCEPTANCE_THRESHOLD: 80 (total review score)
    - CRITICAL_THRESHOLD: 14 (minimum for honesty and soundness)
    - CONTRIBUTION_THRESHOLD: 70 (assigned by PROD during review)
"""

ACCEPTANCE_THRESHOLD = 80
CRITICAL_THRESHOLD = 14
CONTRIBUTION_THRESHOLD = 70
