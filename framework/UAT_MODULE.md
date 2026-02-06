# UAT Module

**Module Type:** STATELESS (validation + pipeline orchestrator)

**Purpose:** Validates test submissions from DEV stage, moves them to uat/, writes the academic paper, and orchestrates the peer review pipeline. Tests flow: `dev/` -> `uat/` -> `prod/`.

**Orchestrates:**
- Validation of submission (fields, scores)
- WRITE_SUBMIT_ACADEMIC_PAPER_MODULE (writes academic_paper, 400-700 words)
- PROD_MODULE (conducts peer review, assigns contribution_score)
- File movement to production

**Kicked off by:** START_RESEARCH_MODULE (after DEV scoring is complete)

**WHO SETS WHAT:**
| Field | Set By | When |
|-------|--------|------|
| question, commentary | DEV | Before submission |
| audit_score | START_RESEARCH_MODULE | At DEV stage |
| academic_paper | **UAT_MODULE** | After UAT acceptance |
| contribution_score | **PROD_MODULE** | During peer review |

---

## Overview

The UAT Module validates submissions and orchestrates the quality pipeline:

### 1. Quality Gate (Desk Rejection)
- Receives test candidates from START_RESEARCH_MODULE (DEV stage)
- Validates DEV provided all required fields (question, commentary, methods)
- Validates `academic_paper` is `None` (UAT writes it, DEV must not)
- Validates `contribution_score` is `None` (PROD assigns it)
- **INDEPENDENTLY SCORES** the test using TEST_QUALITY_MODULE criteria
- Validates UAT's independent `audit_score` >= 85
- Rejects submissions where DEV inflated their score by more than 10 points

### 2. Pipeline Orchestrator
- Writes the `academic_paper` (400-700 words) via WRITE_SUBMIT_ACADEMIC_PAPER_MODULE
- Kicks off PROD_MODULE for peer review
- If ACCEPT: writes `contribution_score`, moves test to `prod/`
- If REJECT: deletes test, archives review report

**DEV must provide:** question, commentary, methods, audit_score
**DEV must NOT set:** academic_paper (UAT writes it), contribution_score (PROD assigns it)

---

## Pipeline Position

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ submissions/ │     │ submissions/ │     │ submissions/ │
│    dev/      │────>│    uat/      │────>│    prod/     │
│              │     │              │     │              │
│  PROBING     │     │  UAT_MODULE  │     │  PROD_MODULE │
│  scores      │     │  writes      │     │  reviews     │
│              │     │  paper       │     │  assigns     │
└──────────────┘     └──────────────┘     └──────────────┘

DEV writes:           UAT does:             PROD does:
- question            1. Validates          - Peer review
- commentary          2. Moves to uat/      - Assigns contribution_score
- methods             3. Writes paper       - ACCEPT: move to prod/
- audit_score >= 85   4. Triggers PROD      - REJECT: delete from uat/
```

---

## Complete Pipeline Flow

```
submissions/dev/dev_*.py
        │
        │ (DEV writes: question, commentary, methods, 
        │  audit_score >= 85, academic_paper = None,
        │  contribution_score = None)
        │
        ▼ START_RESEARCH_MODULE calls process_for_production()
┌───────────────────────────────────────────┐
│ STAGE 1: check_eligibility() [in dev/]    │
│    - Single test class                    │
│    - Required fields present              │
│    - academic_paper = None                │
│    - contribution_score = None            │
│    - UAT INDEPENDENT SCORING (8 criteria) │
│    - Check: UAT score >= 85               │
│    - Check: DEV inflation <= 10 points    │
└───────────────────────────────────────────┘
        │
        │ DESK REJECT if any check fails (test stays in dev/)
        │ Reasons: missing fields, inflated score, low quality
        │
        ▼ If eligible
┌───────────────────────────────────────────┐
│ STAGE 2: Move dev/ -> uat/                │
│    dev/dev_my_test.py                     │
│         -> uat/test_my_test.py            │
└───────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│ STAGE 3: Write academic_paper [in uat/]   │
│    UAT writes 400-700 words               │
└───────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│ STAGE 4: PROD peer review [test in uat/]  │
│    Reviews academic_paper                 │
│    Assigns contribution_score             │
└───────────────────────────────────────────┘
        │
        ├──> ACCEPT (score >= 80, contribution >= 70)
        │           │
        │           ▼
        │    ┌───────────────────────┐
        │    │   submissions/prod/   │  <-- moved from uat/
        │    │   test_*.py           │
        │    └───────────────────────┘
        │
        └──> REJECT
                    │
                    ▼
             Test DELETED from uat/, review archived
```

---

## UAT Guards (Desk Rejection Checks)

Before processing, UAT performs validation checks. Failure = desk rejection.

| Guard | Requirement | Reason |
|-------|-------------|--------|
| **SINGLE TEST** | Exactly 1 test class | No test groups during development |
| **question** | Non-empty string | Must state what you're investigating |
| **commentary** | Non-empty string | Must interpret results |
| **derivation/observations/model** | Method exists | Must have test logic |
| **academic_paper** | Must be `None` | UAT writes this, DEV must not set it |
| **contribution_score** | Must be `None` | PROD assigns this, DEV must not set it |
| **UAT audit_score** | >= 85 | UAT's independent scoring (not DEV's claim) |
| **Score inflation** | <= 10 points | DEV cannot inflate score to game the system |

## Independent Audit Scoring

**UAT does NOT trust DEV's claimed audit_score.** UAT independently re-scores the test using TEST_QUALITY_MODULE criteria:

| Criterion | Points | UAT Checks |
|-----------|--------|------------|
| Question | 15 | Why/how framing, specificity, length |
| Derivation | 15 | Structured steps present |
| Commentary | 15 | Epistemic honesty, thoroughness |
| Model Output | 10 | Model method present |
| Observation Quality | 10 | Has observations and reference |
| Constants Compliance | 10 | Uses framework constants |
| Audience Accessibility | 15 | Explanation depth |
| Test Group Header | 10 | Docstring completeness |
| **Total** | **100** | |

**Inflation Detection:**
- If `DEV_score - UAT_score > 10`, the test is desk rejected
- This prevents DEV from gaming the system by inflating their own scores
- DEV should self-assess honestly; UAT will catch inflation

## Graduation Thresholds

| Criterion | Threshold | Module |
|-----------|-----------|--------|
| `audit_score` (UAT verified) | >= 85 | UAT_MODULE (independent scoring) |
| `contribution_score` | >= 70 | PROD_MODULE (peer review) |
| Total review score | >= 80 | PROD_MODULE (peer review) |

**After UAT acceptance:** UAT writes the `academic_paper` (400-700 words) via WRITE_SUBMIT_ACADEMIC_PAPER_MODULE.
**After peer review:** PROD assigns `contribution_score` (>= 70 required for production).

---

## Folder Structure

```
gravity_field_model/submissions/
├── dev/                        # Development (DEV stage)
│   └── dev_*.py                # Work in progress tests
├── uat/                        # UAT stage (academic_paper written here)
│   └── test_*.py               # Tests undergoing peer review
└── prod/                       # Production (GUARDED BY PROD_MODULE)
    ├── test_*.py               # Accepted production tests
    └── archive/                # Archived review reports
```

**Flow:** `dev/` -> `uat/` -> `prod/`

Tests move from dev/ to uat/ after passing desk rejection checks.
UAT writes academic_paper in uat/. PROD reviews, then moves to prod/ or deletes from uat/.

---

## API Reference

All pipeline functions are in `gravity_field_model.pipeline`.

### Main Entry Point: process_for_production()

```python
from gravity_field_model.pipeline import process_for_production

result = process_for_production("dev/dev_my_test.py")
# Returns:
# {
#     "success": True/False,
#     "source_file": "dev/dev_my_test.py",
#     "stage_reached": "production",  # or "eligibility", "uat", "paper", "review"
#     "uat_path": "uat/test_my_test.py",
#     "prod_path": "prod/test_my_test.py",
#     "contribution_score": 77,
#     "reason": "ACCEPTED: Promoted to production with contribution_score=77",
#     "suggestions": [],
#     "timestamp": "2026-02-04T..."
# }
```

This function runs the entire pipeline:
1. Check eligibility (desk rejection guards)
2. Move test from dev/ to uat/
3. Write academic_paper (UAT responsibility)
4. PROD peer review
5. Move to prod/ (accept) or delete (reject)

### Check Eligibility Only

```python
from gravity_field_model.pipeline import check_eligibility

result = check_eligibility("dev/dev_my_test.py")
# Returns:
# {
#     "eligible": True/False,
#     "desk_rejected": False,
#     "desk_rejection_reason": None,
#     "audit_score": 87,
#     "audit_passed": True,
#     "reason": "Meets all UAT criteria"
# }
```

### Management Functions

```python
from gravity_field_model.pipeline import list_dev_tests, list_prod_tests, print_pipeline_status

dev_tests = list_dev_tests()    # Tests in submissions/dev/
prod_tests = list_prod_tests()  # Tests in submissions/prod/
print_pipeline_status()         # Print full status
```

---

## Pipeline Flow

```
dev/dev_my_test.py
    │
    ├── [STAGE 1: check_eligibility()]
    │   Desk rejection guards (6 checks)
    │
    ├── [STAGE 2: Move dev/ -> uat/]
    │   dev_my_test.py -> test_my_test.py
    │
    ├── [STAGE 3: _write_academic_paper()]
    │   UAT writes academic_paper (400-700 words)
    │
    ├── [STAGE 4: review_submission()]
    │   PROD peer review, assigns contribution_score
    │
    └── [STAGE 5: Final disposition]
        ├── ACCEPT: Move uat/ -> prod/, archive report
        └── REJECT: Delete from uat/, archive report
```

---

## Integration with Other Modules

### Called by START_RESEARCH_MODULE

```python
# In START_RESEARCH_MODULE Phase 7:
from gravity_field_model.pipeline import process_for_production

result = process_for_production(source_file="dev/dev_my_test.py")
# Pipeline takes over from here
```

### Uses paper_generator for validation

```python
# Internal to pipeline:
from gravity_field_model.pipeline import validate_honesty, extract_test_info
```

### Calls reviewer for peer review

```python
# Internal to gate.py:
from gravity_field_model.pipeline.reviewer import review_submission

review_result = review_submission(str(uat_path))
if review_result["decision"] == "ACCEPT":
    accept_to_production(submission_name, review_result)
```

---

## Design Principles

1. **Separation of Concerns**: START_RESEARCH_MODULE scores, UAT_MODULE orchestrates
2. **Single Orchestrator**: UAT_MODULE coordinates the entire quality pipeline
3. **Modular Delegation**: Delegates to WRITE_SUBMIT_ACADEMIC_PAPER_MODULE and PROD_MODULE
4. **Pipeline as Code**: All transitions are API calls, automatable in CI/CD
5. **Audit Trail**: Every stage produces artifacts (paper, review report)
6. **Reversibility**: Rejections provide feedback, not dead ends

---

## Summary: The Delegation Chain

```
START_RESEARCH_MODULE (dev + scoring, academic_paper=None, contribution_score=None)
    │
    └─► UAT_MODULE (orchestrator)
            │
            ├─► Gatekeeper: guards uat/ folder, rejects if academic_paper or contribution_score set
            │
            ├─► WRITES academic_paper (400-700 words) via WRITE_SUBMIT_ACADEMIC_PAPER_MODULE
            │
            └─► Kicks off PROD_MODULE (peer review, assigns contribution_score)
                    │
                    └─► Gatekeeper: guards prod/ folder
```

UAT_MODULE is the **central orchestrator** of the quality assurance pipeline. It receives tests from START_RESEARCH_MODULE (DEV stage, without academic_paper), writes the academic paper, and drives them through peer review to production.

---

*Document version: 2.0*
*Last updated: 2026-02-04*
*Location: framework/UAT_MODULE.md*
