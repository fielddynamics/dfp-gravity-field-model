"""
PROD Reviewer Module
====================

Implements the peer review process for the pipeline.
See: framework/PROD_MODULE.md for full documentation.

Flow:
    1. Test arrives in uat/ with academic_paper written by UAT
    2. PROD validates academic_paper exists (400-700 words)
    3. PROD reviews the test and paper (5 criteria, 100 points total)
    4. PROD assigns contribution_score
    5. Decision: ACCEPT (move to prod/) or REJECT (delete from uat/)

Thresholds:
    - academic_paper must exist and be 400-700 words (prerequisite)
    - Total review score >= 80 for ACCEPT
    - contribution_score >= 70 for production
    - Critical scores (honesty, soundness) >= 14 each
"""

import importlib.util
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


# =============================================================================
# THRESHOLDS
# =============================================================================

ACCEPTANCE_THRESHOLD = 80      # Total score needed for acceptance
CONTRIBUTION_THRESHOLD = 70    # Minimum contribution_score for production
CRITICAL_THRESHOLD = 14        # Minimum for honesty and soundness (out of 20)
PAPER_WORD_MIN = 400           # Minimum words for academic_paper
PAPER_WORD_MAX = 700           # Maximum words for academic_paper


# =============================================================================
# REVIEW CRITERIA
# =============================================================================

REVIEW_CRITERIA = {
    "scientific_soundness": {
        "max_score": 20,
        "description": "Methodology is rigorous, reproducible, and appropriate",
    },
    "intellectual_honesty": {
        "max_score": 20,
        "description": "Clear distinction between derivation and observation",
    },
    "contribution_value": {
        "max_score": 20,
        "description": "Adds meaningful knowledge to the system",
    },
    "clarity_presentation": {
        "max_score": 20,
        "description": "Clear, well-organized, accessible presentation",
    },
    "reproducibility_rigor": {
        "max_score": 20,
        "description": "Fully reproducible with all inputs documented",
    },
}


# =============================================================================
# PAPER VALIDATION (PROD cross-check, UAT should have written it)
# =============================================================================

def _validate_academic_paper(submission_path: str) -> Dict[str, Any]:
    """
    Validate that academic_paper exists and meets requirements.
    
    PROD does NOT trust that UAT wrote the paper properly.
    This is a cross-check: if the paper is missing or invalid,
    PROD desk-rejects the submission.
    
    Returns:
        Dict with validation result
    """
    path = Path(submission_path)
    
    result = {
        "valid": False,
        "has_paper": False,
        "word_count": 0,
        "reason": "",
    }
    
    # Load the module and extract academic_paper
    try:
        spec = importlib.util.spec_from_file_location("review_module", str(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        result["reason"] = f"Failed to load module: {e}"
        return result
    
    # Find the test class and get academic_paper
    from gravity_field_model.framework import Test as BaseTest
    paper_text = None
    
    for attr_name in dir(module):
        obj = getattr(module, attr_name)
        if isinstance(obj, type) and obj is not BaseTest:
            if issubclass(obj, BaseTest) and not attr_name.startswith("_"):
                paper_text = getattr(obj, "academic_paper", None)
                break
    
    if paper_text is None or not isinstance(paper_text, str) or not paper_text.strip():
        result["reason"] = (
            "academic_paper is missing or empty. "
            "UAT_MODULE should have written the paper before sending to PROD."
        )
        return result
    
    result["has_paper"] = True
    word_count = len(paper_text.split())
    result["word_count"] = word_count
    
    if word_count < PAPER_WORD_MIN:
        result["reason"] = (
            f"academic_paper is too short: {word_count} words "
            f"(minimum: {PAPER_WORD_MIN}). UAT paper generation may have failed."
        )
        return result
    
    if word_count > PAPER_WORD_MAX + 50:  # Small buffer for formatting
        result["reason"] = (
            f"academic_paper is too long: {word_count} words "
            f"(maximum: {PAPER_WORD_MAX}). Paper needs trimming."
        )
        return result
    
    result["valid"] = True
    result["reason"] = f"Paper present: {word_count} words"
    return result


# =============================================================================
# MAIN REVIEW FUNCTION
# =============================================================================

def review_submission(submission_path: str) -> Dict[str, Any]:
    """
    Conduct peer review of a submission in uat/.
    
    This is called by gate.py after UAT writes the academic_paper.
    
    PREREQUISITE: academic_paper must exist and be 400-700 words.
    If the paper is missing, PROD desk-rejects without scoring.
    
    Args:
        submission_path: Path to test file in uat/
        
    Returns:
        Dict with review result
    """
    path = Path(submission_path)
    
    # =========================================================================
    # PREREQUISITE: Validate academic_paper exists
    # =========================================================================
    paper_check = _validate_academic_paper(submission_path)
    
    if not paper_check["valid"]:
        # Desk reject: paper missing or invalid
        report = _generate_review_report(
            submission_path=submission_path,
            scores={k: 0 for k in REVIEW_CRITERIA},
            total=0,
            contribution_score=0,
            decision="REJECT",
            reason=f"DESK REJECT (paper validation): {paper_check['reason']}",
            paper_word_count=paper_check["word_count"],
        )
        
        report_path = path.parent / f"{path.stem}_REVIEW.md"
        report_path.write_text(report, encoding="utf-8")
        
        return {
            "decision": "REJECT",
            "scores": {k: 0 for k in REVIEW_CRITERIA},
            "total": 0,
            "contribution_score": 0,
            "feedback": {"paper_validation": paper_check["reason"]},
            "report": report,
            "report_path": str(report_path),
            "reason": f"DESK REJECT: {paper_check['reason']}",
        }
    
    # =========================================================================
    # PEER REVIEW SCORING
    # =========================================================================
    # Score each criterion based on the test content and academic paper.
    # This is a heuristic scorer. A full AI review would do deeper analysis.
    
    scores = _score_submission(submission_path, paper_check)
    total = sum(scores.values())
    
    # Contribution score is the total review score
    contribution_score = total
    
    # =========================================================================
    # DECISION
    # =========================================================================
    # Check critical thresholds
    honesty_ok = scores["intellectual_honesty"] >= CRITICAL_THRESHOLD
    soundness_ok = scores["scientific_soundness"] >= CRITICAL_THRESHOLD
    
    if not honesty_ok:
        decision = "REJECT"
        reason = f"Critical failure: intellectual_honesty {scores['intellectual_honesty']}/20 < {CRITICAL_THRESHOLD}"
    elif not soundness_ok:
        decision = "REJECT"
        reason = f"Critical failure: scientific_soundness {scores['scientific_soundness']}/20 < {CRITICAL_THRESHOLD}"
    elif total >= ACCEPTANCE_THRESHOLD and contribution_score >= CONTRIBUTION_THRESHOLD:
        decision = "ACCEPT"
        reason = f"Meets all criteria (total={total}, contribution={contribution_score})"
    else:
        decision = "REJECT"
        reason = f"Below threshold (total={total}, contribution={contribution_score})"
    
    # Generate and save report
    report = _generate_review_report(
        submission_path=submission_path,
        scores=scores,
        total=total,
        contribution_score=contribution_score,
        decision=decision,
        reason=reason,
        paper_word_count=paper_check["word_count"],
    )
    
    report_path = path.parent / f"{path.stem}_REVIEW.md"
    report_path.write_text(report, encoding="utf-8")
    
    return {
        "decision": decision,
        "scores": scores,
        "total": total,
        "contribution_score": contribution_score,
        "feedback": {k: f"Score: {v}/20" for k, v in scores.items()},
        "report": report,
        "report_path": str(report_path),
        "reason": reason,
    }


def _score_submission(submission_path: str, paper_check: Dict) -> Dict[str, int]:
    """
    Score a submission on the 5 review criteria.
    
    Uses heuristic analysis of the test class properties and academic paper.
    """
    path = Path(submission_path)
    
    # Load the module
    try:
        spec = importlib.util.spec_from_file_location("score_module", str(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        return {k: 10 for k in REVIEW_CRITERIA}  # Default middle scores on load failure
    
    # Find the test class
    from gravity_field_model.framework import Test as BaseTest
    test_class = None
    for attr_name in dir(module):
        obj = getattr(module, attr_name)
        if isinstance(obj, type) and obj is not BaseTest:
            if issubclass(obj, BaseTest) and not attr_name.startswith("_"):
                test_class = obj
                break
    
    if not test_class:
        return {k: 10 for k in REVIEW_CRITERIA}
    
    scores = {}
    
    # --- Scientific Soundness (20) ---
    has_derivation = hasattr(test_class, "derivation") and callable(getattr(test_class, "derivation", None))
    has_model = hasattr(test_class, "model") and callable(getattr(test_class, "model", None))
    has_observations = hasattr(test_class, "observations") and callable(getattr(test_class, "observations", None))
    method_count = sum([has_derivation, has_model, has_observations])
    
    soundness = 10 + (method_count * 3)  # 10 base + 3 per method (max 19)
    reference_val = getattr(test_class, "reference", "")
    if reference_val and len(reference_val) > 10:
        soundness = min(soundness + 1, 20)
    scores["scientific_soundness"] = min(soundness, 20)
    
    # --- Intellectual Honesty (20) ---
    commentary = getattr(test_class, "commentary", "")
    docstring = test_class.__doc__ or ""
    paper = getattr(test_class, "academic_paper", "") or ""
    combined_text = (commentary + " " + docstring + " " + paper).lower()
    
    honesty = 12  # Base score
    honesty_markers = ["observation", "not a derivation", "does not constitute",
                       "could be coincidental", "epistemic", "honest", "limitation"]
    for marker in honesty_markers:
        if marker in combined_text:
            honesty += 1
    
    overclaim_markers = ["proves", "undeniable", "conclusively", "beyond doubt"]
    for marker in overclaim_markers:
        if marker in combined_text:
            honesty -= 3
    
    scores["intellectual_honesty"] = max(0, min(honesty, 20))
    
    # --- Contribution Value (20) ---
    question = getattr(test_class, "question", "")
    contribution = 12  # Base
    if len(question) > 150:
        contribution += 2  # Substantial question
    if "why" in question.lower() or "how" in question.lower():
        contribution += 2  # Probing question
    if len(commentary) > 300:
        contribution += 2  # Thorough commentary
    if method_count >= 3:
        contribution += 2  # Complete test
    scores["contribution_value"] = min(contribution, 20)
    
    # --- Clarity & Presentation (20) ---
    clarity = 12  # Base
    if len(docstring) > 300:
        clarity += 3  # Good documentation
    if paper_check["word_count"] >= PAPER_WORD_MIN:
        clarity += 3  # Paper meets length
    if len(question) > 100:
        clarity += 2  # Clear question
    scores["clarity_presentation"] = min(clarity, 20)
    
    # --- Reproducibility & Rigor (20) ---
    rigor = 14  # Base (if it got this far, basic rigor is met)
    tolerance = getattr(test_class, "tolerance", None)
    if tolerance is not None:
        rigor += 2  # Explicit tolerance
    if reference_val:
        rigor += 2  # Sources cited
    if has_model and has_observations:
        rigor += 2  # Both model and observation (reproducible comparison)
    scores["reproducibility_rigor"] = min(rigor, 20)
    
    return scores


def _generate_review_report(
    submission_path: str,
    scores: Dict[str, int],
    total: int,
    contribution_score: int,
    decision: str,
    reason: str,
    paper_word_count: int = 0,
) -> str:
    """Generate the full review report."""
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    path = Path(submission_path)
    
    report = f"""================================================================
PEER REVIEW REPORT
================================================================
Submission: {path.stem}
Reviewer: PROD_MODULE
Date: {date}
================================================================

PREREQUISITE CHECK
------------------
Academic Paper: {"PRESENT" if paper_word_count > 0 else "MISSING"}
Paper Word Count: {paper_word_count}
Required Range: {PAPER_WORD_MIN} to {PAPER_WORD_MAX} words

SCORES
------
Scientific Soundness:     {scores.get('scientific_soundness', 0)}/20
Intellectual Honesty:     {scores.get('intellectual_honesty', 0)}/20
Contribution Value:       {scores.get('contribution_value', 0)}/20
Clarity & Presentation:   {scores.get('clarity_presentation', 0)}/20
Reproducibility & Rigor:  {scores.get('reproducibility_rigor', 0)}/20
-----------------------------
TOTAL:                    {total}/100

CONTRIBUTION SCORE: {contribution_score}
THRESHOLDS: total >= {ACCEPTANCE_THRESHOLD}, contribution >= {CONTRIBUTION_THRESHOLD}
CRITICAL MINIMUMS: honesty >= {CRITICAL_THRESHOLD}, soundness >= {CRITICAL_THRESHOLD}

DECISION: {decision}

REASON
------
{reason}

================================================================
"""
    return report
