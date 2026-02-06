"""
Sandbox for Probing Test Development
====================================

This folder is for developing and iterating on probing tests BEFORE
moving them to their final location in the calculations folder.

WORKFLOW:
1. Copy sandbox_template.py to sandbox_<topic>.py
2. Write your tests, run and iterate until they pass
3. Run the quality audit (framework/TEST_QUALITY_FRAMEWORK.md)
   -> Set audit_score and audit_notes for each test
4. Run the contribution assessment (framework/CONTRIBUTION_SCORING_FRAMEWORK.md)
   -> Set contribution_score and contribution_notes for each test
5. Once audit_score >= 65 and contribution assessed, move to domain folder
6. Rename sandbox_<topic>.py -> test_<topic>.py
7. Delete the sandbox file

RUN SANDBOX TESTS:
    python -m gravity_field_model.calculations.sandbox.sandbox_<topic>

WHY SANDBOX:
- Rapid iteration without polluting main test folders
- Easy to experiment and discard failed approaches
- Clear separation between "work in progress" and "ready"
- No pressure: it's just a sandbox

NAMING CONVENTION:
- sandbox_<topic>.py for work in progress
- test_<topic>.py for production (after moving to domain folder)

GIT HANDLING:
- Sandbox files are NOT gitignored by default
- This allows sharing work-in-progress with collaborators
- Once moved to production, delete the sandbox file
- For truly temporary experiments, add to .git/info/exclude

FILES HERE ARE TEMPORARY. Target: move or delete within 1 week.
"""
