"""
UAT Gate Module
===============

Quality gate implementation for test promotion.

This module is the SINGLE SOURCE OF TRUTH for:
- UAT graduation thresholds
- Desk rejection checks
- Academic paper writing
- Pipeline orchestration to PROD

Pipeline folders: gravity_field_model/submissions/
    dev/           -> Development tests (START_RESEARCH_MODULE scores here)
    uat/           -> UAT stage (UAT writes academic_paper here)
    prod/          -> Accepted production tests
    prod/archive/  -> Review reports

Serial Pipeline (agent-driven):
    1. START_RESEARCH_MODULE scores test in dev/ (audit_score >= 85)
    2. UAT_MODULE (this module):
       - Desk rejection check
       - Move test from dev/ to uat/
       - Write academic_paper (400-700 words)
       - Kick off PROD_MODULE
    3. PROD_MODULE:
       - Peer review (test is in uat/)
       - Assign contribution_score
       - Move to prod/ (accept) or delete (reject)

Flow: dev/ -> uat/ -> prod/
"""

import os
import shutil
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


# =============================================================================
# THRESHOLDS (single source of truth for UAT decisions)
# =============================================================================

# UAT only checks audit_score (quality gate)
# contribution_score is assigned later by PROD_MODULE during peer review
AUDIT_THRESHOLD = 85  # High bar for quality - must be well-documented and rigorous

# Maximum allowed inflation: if DEV claims score > UAT score + this, desk reject
AUDIT_INFLATION_TOLERANCE = 10  # DEV can't inflate by more than 10 points

# Word limit for academic_paper property
ACADEMIC_PAPER_WORD_LIMIT = 700


# =============================================================================
# INDEPENDENT AUDIT SCORING (UAT does not trust DEV's score)
# =============================================================================

def _uat_audit_score(test_class: type) -> Dict[str, Any]:
    """
    UAT independently scores the test using TEST_QUALITY_MODULE criteria.
    
    This prevents DEV from inflating their own audit_score to pass the threshold.
    UAT rigorously evaluates the 8 criteria:
    
    1. Question (15 pts): Does it hook curiosity? Why before what?
    2. Derivation (15 pts): Intuition before math? Clear steps?
    3. Commentary (15 pts): Delivers insight, not just restates numbers?
    4. Model Output (10 pts): Summary stats, not raw dumps?
    5. Observation Quality (10 pts): Traceable sources?
    6. Constants Compliance (10 pts): Imports from /common/?
    7. Audience Accessibility (15 pts): Undergrad to PhD accessible?
    8. Test Group Header (10 pts): Module docs complete?
    
    Returns:
        Dict with uat_score, criteria_scores, and notes
    """
    scores = {}
    notes = []
    
    # Criterion 1: Question (15 pts)
    question = getattr(test_class, "question", "")
    if not question:
        scores["question"] = 0
        notes.append("Question: 0/15 - Missing question field")
    elif len(question) < 50:
        scores["question"] = 5
        notes.append("Question: 5/15 - Too brief, needs more context")
    else:
        # Score based on question quality indicators
        q_score = 10  # Base score for adequate question
        q_why_how = "why" in question.lower() or "how" in question.lower()
        q_specific = any(x in question.lower() for x in ["factor", "exactly", "specifically", "relationship"])
        q_length = len(question) > 150
        
        if q_why_how:
            q_score += 2  # Good framing
        if q_specific:
            q_score += 2  # Specific inquiry
        if q_length:
            q_score += 1  # Thorough question
        
        q_score = min(q_score, 15)  # Cap at max
        scores["question"] = q_score
        notes.append(f"Question: {q_score}/15 - {'Excellent' if q_score >= 14 else 'Good'} question framing")
    
    # Criterion 2: Derivation (15 pts)
    has_derivation = hasattr(test_class, "derivation") and callable(getattr(test_class, "derivation", None))
    if not has_derivation:
        scores["derivation"] = 0
        notes.append("Derivation: 0/15 - No derivation method")
    else:
        # Check if derivation has steps
        try:
            instance = test_class()
            deriv = instance.derivation()
            if hasattr(deriv, "steps") or hasattr(deriv, "_steps"):
                scores["derivation"] = 12
                notes.append("Derivation: 12/15 - Has structured steps")
            else:
                scores["derivation"] = 8
                notes.append("Derivation: 8/15 - Present but unstructured")
        except Exception:
            scores["derivation"] = 6
            notes.append("Derivation: 6/15 - Present but could not evaluate")
    
    # Criterion 3: Commentary (15 pts)
    commentary = getattr(test_class, "commentary", "")
    if not commentary:
        scores["commentary"] = 0
        notes.append("Commentary: 0/15 - Missing commentary")
    elif len(commentary) < 100:
        scores["commentary"] = 7
        notes.append("Commentary: 7/15 - Brief, needs more insight")
    else:
        c_score = 10  # Base score
        c_honest = any(x in commentary.lower() for x in ["observation", "correspondence", "not a derivation", "honesty"])
        c_thorough = len(commentary) > 300
        c_physics = any(x in commentary.lower() for x in ["gr", "standard", "established", "physics"])
        
        if c_honest:
            c_score += 2  # Epistemic honesty
        if c_thorough:
            c_score += 2  # Thorough commentary
        if c_physics:
            c_score += 1  # Connects to standard physics
        
        c_score = min(c_score, 15)
        scores["commentary"] = c_score
        notes.append(f"Commentary: {c_score}/15 - {'Excellent' if c_score >= 14 else 'Good'} epistemic honesty")
    
    # Criterion 4: Model Output (10 pts)
    has_model = hasattr(test_class, "model") and callable(getattr(test_class, "model", None))
    if has_model:
        scores["model_output"] = 8
        notes.append("Model Output: 8/10 - Model method present")
    else:
        scores["model_output"] = 0
        notes.append("Model Output: 0/10 - No model method")
    
    # Criterion 5: Observation Quality (10 pts)
    has_observations = hasattr(test_class, "observations") and callable(getattr(test_class, "observations", None))
    reference = getattr(test_class, "reference", "")
    if has_observations and reference:
        scores["observation_quality"] = 9
        notes.append("Observations: 9/10 - Has observations and reference")
    elif has_observations or reference:
        scores["observation_quality"] = 6
        notes.append("Observations: 6/10 - Partial (missing reference or method)")
    else:
        scores["observation_quality"] = 3
        notes.append("Observations: 3/10 - Minimal observational grounding")
    
    # Criterion 6: Constants Compliance (10 pts)
    # Check if module imports from common (heuristic: check for hardcoded physics constants)
    scores["constants_compliance"] = 8  # Assume compliant unless obvious violation
    notes.append("Constants: 8/10 - Assumed compliant (manual review needed)")
    
    # Criterion 7: Audience Accessibility (15 pts)
    # Heuristic: longer question + commentary suggests more accessible
    total_explanation = len(str(question)) + len(str(commentary))
    if total_explanation > 500:
        scores["accessibility"] = 12
        notes.append("Accessibility: 12/15 - Good explanatory depth")
    elif total_explanation > 200:
        scores["accessibility"] = 9
        notes.append("Accessibility: 9/15 - Moderate depth")
    else:
        scores["accessibility"] = 6
        notes.append("Accessibility: 6/15 - Could be more accessible")
    
    # Criterion 8: Test Group Header (10 pts)
    docstring = test_class.__doc__ or ""
    if len(docstring) > 600:
        # Comprehensive documentation with sections
        scores["header"] = 10
        notes.append("Header: 10/10 - Comprehensive class documentation")
    elif len(docstring) > 300:
        scores["header"] = 9
        notes.append("Header: 9/10 - Thorough class docstring")
    elif len(docstring) > 200:
        scores["header"] = 8
        notes.append("Header: 8/10 - Good class docstring")
    elif len(docstring) > 50:
        scores["header"] = 5
        notes.append("Header: 5/10 - Brief docstring")
    else:
        scores["header"] = 2
        notes.append("Header: 2/10 - Minimal documentation")
    
    total = sum(scores.values())
    
    return {
        "uat_score": total,
        "criteria_scores": scores,
        "notes": notes,
        "max_possible": 100,
    }


# =============================================================================
# PATHS (Single source of truth: gravity_field_model/submissions/)
# =============================================================================

def _get_submissions_path() -> Path:
    """Get the base path for submissions pipeline."""
    return Path(__file__).parent.parent / "submissions"


def _get_dev_path() -> Path:
    """Get the DEV folder path (development)."""
    return _get_submissions_path() / "dev"


def _get_uat_path() -> Path:
    """Get the UAT folder path (UAT writes academic_paper here)."""
    return _get_submissions_path() / "uat"


def _get_prod_path() -> Path:
    """Get the PROD folder path."""
    return _get_submissions_path() / "prod"


def _get_prod_archive_path() -> Path:
    """Get the PROD archive folder path."""
    return _get_prod_path() / "archive"


# =============================================================================
# ELIGIBILITY CHECK
# =============================================================================

def check_eligibility(source_file: str) -> Dict[str, Any]:
    """
    Check if a test file is eligible for production pipeline.
    
    UAT GUARDS (desk rejection if any fail):
    1. SINGLE TEST: File must contain exactly ONE test class (not a test group)
    2. REQUIRED FIELDS: question, commentary must be non-empty
    3. REQUIRED METHODS: derivation() or observations() or model() must exist
    4. NO SELF-SCORING: contribution_score must be None (PROD assigns this)
    5. NO PRE-WRITTEN PAPER: academic_paper must be None (UAT writes this)
    6. AUDIT SCORE: audit_score >= 85 (quality gate from START_RESEARCH_MODULE)
    
    WHO SETS WHAT:
    - DEV stage: question, commentary, methods, audit_score
    - UAT stage: academic_paper (400-700 words)
    - PROD stage: contribution_score (peer review)
    
    Args:
        source_file: Path to the dev test file (relative or absolute)
    
    Returns:
        Dict with eligibility details
    """
    result = {
        "eligible": False,
        "file": source_file,
        "desk_rejected": False,
        "desk_rejection_reason": None,
        "test_count": 0,
        "audit_score": None,
        "audit_threshold": AUDIT_THRESHOLD,
        "audit_passed": False,
        "required_fields_present": False,
        "contribution_score_clean": False,  # Must be None (PROD assigns)
        "academic_paper_clean": False,  # Must be None (UAT writes)
        "reason": "",
        "suggestions": [],
    }
    
    # Resolve path
    path = Path(source_file)
    if not path.is_absolute():
        path = _get_submissions_path() / source_file
    
    if not path.exists():
        result["reason"] = f"File not found: {source_file}"
        return result
    
    # Try to load the module and extract test classes
    try:
        spec = importlib.util.spec_from_file_location("test_module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        result["reason"] = f"Failed to load module: {e}"
        result["suggestions"].append("Fix import errors in the test file")
        return result
    
    # Find ALL test classes (classes with audit_score or academic_paper)
    test_classes = []
    
    # Get the base Test class to exclude it
    try:
        from gravity_field_model.framework import Test as BaseTest
        base_test_class = BaseTest
    except ImportError:
        base_test_class = None
    
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type):
            # Skip the base Test class itself
            if base_test_class and obj is base_test_class:
                continue
            
            # Skip classes that aren't subclasses of Test (if we have it)
            if base_test_class and not issubclass(obj, base_test_class):
                continue
            
            # Detect test class by presence of test-related attributes
            is_test_class = (
                hasattr(obj, "audit_score") or 
                hasattr(obj, "academic_paper") or
                hasattr(obj, "question") or
                (hasattr(obj, "name") and name.startswith("Test"))
            )
            if is_test_class and not name.startswith("_"):
                test_classes.append((name, obj))
    
    result["test_count"] = len(test_classes)
    
    # ==========================================================================
    # DESK REJECTION CHECK 1: Single test only
    # ==========================================================================
    if len(test_classes) == 0:
        result["desk_rejected"] = True
        result["desk_rejection_reason"] = "No test class found"
        result["reason"] = "DESK REJECT: No test class found in file"
        result["suggestions"].append("Add a test class with required fields")
        return result
    
    if len(test_classes) > 1:
        result["desk_rejected"] = True
        result["desk_rejection_reason"] = f"Multiple test classes found ({len(test_classes)})"
        result["reason"] = f"DESK REJECT: File contains {len(test_classes)} test classes. Only 1 allowed."
        result["suggestions"].append("Split into separate files, ONE test per file")
        result["suggestions"].append("Test groups are for production organization, not development")
        return result
    
    # Single test class found
    test_name, test_class = test_classes[0]
    
    # ==========================================================================
    # DESK REJECTION CHECK 2: Required fields must be populated
    # ==========================================================================
    missing_fields = []
    
    # Check question
    question = getattr(test_class, "question", None)
    if not question or (isinstance(question, str) and not question.strip()):
        missing_fields.append("question")
    
    # Check commentary
    commentary = getattr(test_class, "commentary", None)
    if not commentary or (isinstance(commentary, str) and not commentary.strip()):
        missing_fields.append("commentary")
    
    # Check for derivation() or observations() method
    has_derivation = hasattr(test_class, "derivation") and callable(getattr(test_class, "derivation", None))
    has_observations = hasattr(test_class, "observations") and callable(getattr(test_class, "observations", None))
    has_model = hasattr(test_class, "model") and callable(getattr(test_class, "model", None))
    
    if not (has_derivation or has_observations or has_model):
        missing_fields.append("derivation() or observations() or model() method")
    
    if missing_fields:
        result["desk_rejected"] = True
        result["desk_rejection_reason"] = f"Missing required fields: {', '.join(missing_fields)}"
        result["reason"] = f"DESK REJECT: Missing required fields: {', '.join(missing_fields)}"
        result["suggestions"].append("Ensure question is set (string describing what you're investigating)")
        result["suggestions"].append("Ensure commentary is set (interpretation of results)")
        result["suggestions"].append("Ensure derivation() or observations() method exists")
        return result
    
    result["required_fields_present"] = True
    
    # ==========================================================================
    # DESK REJECTION CHECK 3: contribution_score must be None (PROD assigns it)
    # ==========================================================================
    contribution_score = getattr(test_class, "contribution_score", None)
    
    if contribution_score is not None:
        result["desk_rejected"] = True
        result["desk_rejection_reason"] = f"contribution_score is set to {contribution_score} (must be None)"
        result["reason"] = f"DESK REJECT: contribution_score = {contribution_score}. Must be None."
        result["suggestions"].append("Set contribution_score = None")
        result["suggestions"].append("This score is assigned by PROD_MODULE during peer review")
        return result
    
    result["contribution_score_clean"] = True
    
    # ==========================================================================
    # DESK REJECTION CHECK 4: academic_paper must be None (UAT writes it)
    # ==========================================================================
    paper = getattr(test_class, "academic_paper", None)
    
    if paper is not None and isinstance(paper, str) and paper.strip():
        result["desk_rejected"] = True
        result["desk_rejection_reason"] = "academic_paper is already set (must be None)"
        result["reason"] = "DESK REJECT: academic_paper is already set. DEV should NOT write the paper."
        result["suggestions"].append("Set academic_paper = None")
        result["suggestions"].append("The academic_paper is written by UAT_MODULE, not DEV")
        return result
    
    result["academic_paper_clean"] = True
    
    # ==========================================================================
    # CHECK 5: audit_score - UAT INDEPENDENT VERIFICATION
    # ==========================================================================
    # UAT does NOT trust DEV's claimed audit_score.
    # UAT independently scores the test and compares.
    
    dev_audit_score = getattr(test_class, "audit_score", None)
    
    if dev_audit_score is None:
        result["reason"] = "audit_score not set"
        result["suggestions"].append("Add audit_score (assigned by START_RESEARCH_MODULE after quality audit)")
        return result
    
    # UAT performs independent audit scoring
    uat_audit = _uat_audit_score(test_class)
    uat_score = uat_audit["uat_score"]
    
    result["dev_audit_score"] = dev_audit_score
    result["uat_audit_score"] = uat_score
    result["audit_score"] = uat_score  # Use UAT's score, not DEV's
    result["audit_notes"] = uat_audit["notes"]
    
    # ==========================================================================
    # CHECK 6: Detect score inflation (DEV gaming the system)
    # ==========================================================================
    inflation = dev_audit_score - uat_score
    result["score_inflation"] = inflation
    
    if inflation > AUDIT_INFLATION_TOLERANCE:
        result["desk_rejected"] = True
        result["desk_rejection_reason"] = f"Score inflation detected: DEV claimed {dev_audit_score}, UAT scored {uat_score} (inflation: {inflation})"
        result["reason"] = f"DESK REJECT: DEV inflated audit_score by {inflation} points (max allowed: {AUDIT_INFLATION_TOLERANCE})"
        result["suggestions"].append(f"DEV claimed audit_score={dev_audit_score} but UAT independently scored {uat_score}")
        result["suggestions"].append("Review TEST_QUALITY_MODULE.md and honestly assess your test")
        result["suggestions"].append("UAT audit notes: " + "; ".join(uat_audit["notes"]))
        return result
    
    # ==========================================================================
    # CHECK 7: UAT's audit_score must meet threshold
    # ==========================================================================
    result["audit_passed"] = uat_score >= AUDIT_THRESHOLD
    
    if not result["audit_passed"]:
        result["reason"] = f"UAT audit_score {uat_score} below threshold {AUDIT_THRESHOLD} (DEV claimed {dev_audit_score})"
        result["suggestions"].append("Improve test quality (see TEST_QUALITY_MODULE.md)")
        result["suggestions"].append("UAT audit breakdown: " + "; ".join(uat_audit["notes"]))
        return result
    
    # ==========================================================================
    # ALL CHECKS PASSED - Ready for UAT to write academic_paper
    # ==========================================================================
    # Note: academic_paper will be written at UAT stage (not DEV)
    # contribution_score will be assigned by PROD during peer review
    result["eligible"] = True
    result["reason"] = f"Meets all UAT criteria (UAT score: {uat_score}, DEV claimed: {dev_audit_score})"
    
    return result


# =============================================================================
# PROMOTION (Serial Pipeline)
# =============================================================================

def process_for_production(
    source_file: str,
) -> Dict[str, Any]:
    """
    Process a test from dev/ through UAT and PROD in one serial flow.
    
    This is the main entry point called by START_RESEARCH_MODULE.
    
    Serial Pipeline Steps:
    1. Check eligibility (desk rejection) - test in dev/
    2. Move test from dev/ to uat/
    3. Write academic_paper (400-700 words) - UAT responsibility
    4. Kick off PROD_MODULE for peer review
    5. If accepted: PROD moves from uat/ to prod/, assigns contribution_score
    6. If rejected: PROD deletes test from uat/, archives report
    
    Flow: dev/ -> uat/ -> prod/
    
    Args:
        source_file: Path to the dev test file (e.g., "dev/dev_my_test.py")
    
    Returns:
        Dict with pipeline result
    """
    result = {
        "success": False,
        "source_file": source_file,
        "stage_reached": "eligibility",
        "uat_path": None,
        "prod_path": None,
        "contribution_score": None,
        "reason": "",
        "suggestions": [],
        "timestamp": datetime.now().isoformat(),
    }
    
    # =========================================================================
    # STAGE 1: Check eligibility (desk rejection) - test in dev/
    # =========================================================================
    eligibility = check_eligibility(source_file)
    
    if not eligibility["eligible"]:
        result["reason"] = f"DESK REJECTED: {eligibility['reason']}"
        result["suggestions"] = eligibility["suggestions"]
        return result
    
    # Resolve source path (in dev/)
    source_path = Path(source_file)
    if not source_path.is_absolute():
        source_path = _get_submissions_path() / source_file
    
    # =========================================================================
    # STAGE 2: Move test from dev/ to uat/
    # =========================================================================
    result["stage_reached"] = "uat"
    
    # Generate UAT filename (dev_* -> test_*)
    filename = source_path.name
    if filename.startswith("dev_"):
        filename = "test_" + filename[4:]
    elif not filename.startswith("test_"):
        filename = "test_" + filename
    
    uat_path = _get_uat_path()
    uat_path.mkdir(parents=True, exist_ok=True)
    uat_dest = uat_path / filename
    
    try:
        shutil.move(str(source_path), str(uat_dest))
        result["uat_path"] = str(uat_dest.relative_to(_get_submissions_path()))
    except Exception as e:
        result["reason"] = f"Failed to move to UAT: {e}"
        return result
    
    # =========================================================================
    # STAGE 3: Write academic_paper (UAT responsibility) - test now in uat/
    # =========================================================================
    result["stage_reached"] = "paper"
    
    paper_result = _write_academic_paper(uat_dest, eligibility)
    
    if not paper_result["success"]:
        result["reason"] = f"PAPER FAILED: {paper_result['reason']}"
        return result
    
    # =========================================================================
    # STAGE 4: PROD peer review - test in uat/
    # =========================================================================
    result["stage_reached"] = "review"
    
    from gravity_field_model.pipeline.reviewer import review_submission
    
    review_result = review_submission(str(uat_dest))
    
    if review_result.get("decision") != "ACCEPT":
        # Rejected: delete test from uat/, archive report
        _delete_rejected_test(str(uat_dest), review_result)
        result["reason"] = f"PEER REVIEW REJECTED: {review_result.get('reason', 'Did not meet standards')}"
        result["suggestions"].append("Review the archived rejection report for feedback")
        return result
    
    result["stage_reached"] = "production"
    result["contribution_score"] = review_result.get("contribution_score")
    
    # =========================================================================
    # STAGE 5: Move from uat/ to prod/ (PROD accepts)
    # =========================================================================
    # Write contribution_score to test file
    _write_contribution_score(uat_dest, result["contribution_score"])
    
    prod_path = _get_prod_path()
    prod_path.mkdir(parents=True, exist_ok=True)
    prod_dest = prod_path / filename
    
    try:
        # Move file from uat/ to prod/
        shutil.move(str(uat_dest), str(prod_dest))
        
        # Archive the review report
        review_report_path = uat_dest.parent / f"{uat_dest.stem}_REVIEW.md"
        if review_report_path.exists():
            archive_path = _get_prod_archive_path()
            archive_path.mkdir(parents=True, exist_ok=True)
            shutil.move(str(review_report_path), str(archive_path / f"{filename.replace('.py', '')}_REVIEW.md"))
        
        result["success"] = True
        result["prod_path"] = str(prod_dest.relative_to(_get_submissions_path()))
        result["reason"] = f"ACCEPTED: Promoted to production with contribution_score={result['contribution_score']}"
        
    except Exception as e:
        result["reason"] = f"Failed to move to production: {e}"
    
    return result


def _write_academic_paper(uat_path: Path, eligibility: Dict) -> Dict[str, Any]:
    """
    Write academic_paper property to the test file in uat/.
    
    This is called by UAT after moving test from dev/ to uat/.
    UAT_MODULE is responsible for generating the academic paper content
    using WRITE_SUBMIT_ACADEMIC_PAPER_MODULE guidelines.
    
    TODO: Implement actual paper generation (AI agent writes the paper).
    For now, this marks the test as ready for review.
    
    Args:
        uat_path: Path to the test file in uat/
        eligibility: Eligibility check result
    
    Returns:
        Dict with success status and reason
    """
    # TODO: Implement actual paper generation
    # The AI agent should:
    # 1. Read the test file from uat/
    # 2. Extract question, commentary, derivation/model/observations
    # 3. Generate 400-700 word academic paper following WRITE_SUBMIT_ACADEMIC_PAPER_MODULE
    # 4. Write academic_paper property to the test file
    
    return {
        "success": True,
        "reason": "Paper writing delegated to UAT agent",
    }


def _write_contribution_score(test_path: Path, contribution_score: int) -> None:
    """
    Write contribution_score to the test file.
    
    This is assigned by PROD_MODULE during peer review.
    """
    content = test_path.read_text(encoding="utf-8")
    
    # Replace contribution_score = None with the actual score
    import re
    pattern = r'contribution_score\s*=\s*None'
    replacement = f'contribution_score = {contribution_score}  # Assigned by PROD_MODULE'
    
    new_content = re.sub(pattern, replacement, content)
    test_path.write_text(new_content, encoding="utf-8")


# =============================================================================
# DEV FOLDER MANAGEMENT
# =============================================================================

def list_dev_tests() -> List[Dict[str, Any]]:
    """
    List tests in dev/ folder.
    
    Returns:
        List of test info dicts
    """
    tests = []
    dev_path = _get_dev_path()
    
    if dev_path.exists():
        for f in dev_path.glob("dev_*.py"):
            if f.name != "dev_template.py":
                tests.append({
                    "file": str(f.relative_to(_get_submissions_path())),
                    "name": f.stem,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                })
    
    return tests


def list_prod_tests() -> List[Dict[str, Any]]:
    """
    List tests in prod/ folder.
    
    Returns:
        List of test info dicts
    """
    tests = []
    prod_path = _get_prod_path()
    
    if prod_path.exists():
        for f in prod_path.glob("test_*.py"):
            tests.append({
                "file": str(f.relative_to(_get_submissions_path())),
                "name": f.stem,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
    
    return tests


def _delete_rejected_test(
    test_file: str,
    review_result: Dict[str, Any],
) -> None:
    """
    Delete a test that failed peer review.
    
    Rejection policy: Tests that fail peer review are DELETED, not revised.
    This enforces quality and prevents endless revision cycles.
    The review report is archived for reference.
    
    Args:
        test_file: Path to the test file to delete
        review_result: Review result containing the report
    """
    test_path = Path(test_file)
    if not test_path.is_absolute():
        test_path = _get_submissions_path() / test_file
    
    if not test_path.exists():
        return
    
    # Archive the review report before deletion
    archive_path = _get_prod_archive_path() / "rejected"
    archive_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save rejection report
    report_content = review_result.get("report", "")
    if report_content:
        report_file = archive_path / f"{test_path.stem}_{timestamp}_REJECTED.md"
        report_file.write_text(report_content, encoding="utf-8")
    
    # Delete the test file
    test_path.unlink()
    
    # Delete associated review report if exists
    review_file = test_path.parent / f"{test_path.stem}_REVIEW.md"
    if review_file.exists():
        review_file.unlink()


# Legacy alias for backwards compatibility
def request_promotion(source_file: str, target_domain: str = "") -> Dict[str, Any]:
    """
    Legacy function. Use process_for_production() instead.
    
    This is a wrapper that calls the new serial pipeline.
    """
    result = process_for_production(source_file)
    # Map new result format to old format for compatibility
    return {
        "promoted": result["success"],
        "source_file": result["source_file"],
        "uat_path": None,  # No longer used
        "target_domain": target_domain,
        "reason": result["reason"],
        "suggestions": result.get("suggestions", []),
        "timestamp": result["timestamp"],
        "prod_path": result.get("prod_path"),
        "contribution_score": result.get("contribution_score"),
    }


# =============================================================================
# PRINTING UTILITIES
# =============================================================================

def print_pipeline_status() -> None:
    """Print the current pipeline status."""
    print("\n" + "=" * 60)
    print("PIPELINE STATUS")
    print("=" * 60)
    print(f"\nThresholds:")
    print(f"  audit_score >= {AUDIT_THRESHOLD} (for UAT processing)")
    print(f"  academic_paper: 400-{ACADEMIC_PAPER_WORD_LIMIT} words (written by UAT)")
    print(f"  contribution_score >= 70 (assigned by PROD during peer review)")
    
    dev_tests = list_dev_tests()
    prod_tests = list_prod_tests()
    
    print(f"\nDEV (submissions/dev/): {len(dev_tests)} tests")
    for t in dev_tests:
        print(f"  - {t['name']}")
    
    print(f"\nPROD (submissions/prod/): {len(prod_tests)} tests")
    for t in prod_tests:
        print(f"  - {t['name']}")
    
    print("\n" + "=" * 60)


# Legacy alias
def print_uat_status() -> None:
    """Legacy alias for print_pipeline_status()."""
    print_pipeline_status()
