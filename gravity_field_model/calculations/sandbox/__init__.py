"""
Sandbox for Probing Test Development
====================================

This folder is for developing and iterating on probing tests BEFORE
moving them to their final location via the CI/CD pipeline.

CRITICAL: ONE TEST PER FILE
---------------------------
Each sandbox file should contain ONE test class investigating ONE question.
Do NOT create test groups. Test groups are for organizing graduated tests.

WHY?
- Each test requires its own academic_paper (400-700 words)
- Peer review happens per test
- Rejection = DELETION (smaller scope = smaller risk)

WORKFLOW:
1. Copy sandbox_template.py to sandbox_<specific_topic>.py
2. Write ONE test class, run and iterate until it passes
3. Write the academic_paper property (400-700 words)
4. Run the quality audit (set audit_score and audit_notes)
5. Call request_promotion() to submit to UAT
6. UAT validates, PROD conducts peer review
7. ACCEPT = production, REJECT = test deleted

GRADUATION CRITERIA (for UAT promotion):
========================================
    audit_score >= 85         (quality threshold, high bar)
    academic_paper exists     (400-700 words, embedded as class property)

Tests that don't meet these thresholds REMAIN IN SANDBOX.
contribution_score is assigned by PROD_MODULE during peer review.

SANDBOX RETENTION POLICY:
=========================
- audit_score >= 85 + valid paper: PROMOTE to UAT via request_promotion()
- contribution_score 50-69: MAY STAY if building toward larger investigation
- contribution_score < 50:  ARCHIVE or DELETE (not valuable enough)
- Tests > 2 weeks without progress: review for archival

RUN SANDBOX TESTS:
    python -m gravity_field_model.calculations.sandbox.sandbox_<topic>

WHY SANDBOX:
- Rapid iteration without polluting main test folders
- Easy to experiment and discard failed approaches
- Clear separation between "work in progress" and "ready"
- Quality gate prevents low-value tests from entering production

NAMING CONVENTION:
- sandbox_<topic>.py for work in progress
- test_<topic>.py for production (after moving to domain folder)

GIT HANDLING:
- Sandbox files are NOT gitignored by default
- This allows sharing work-in-progress with collaborators
- Once moved to production, delete the sandbox file
- For truly temporary experiments, add to .git/info/exclude

FILES HERE ARE TEMPORARY. Target: graduate or archive within 2 weeks.
"""
