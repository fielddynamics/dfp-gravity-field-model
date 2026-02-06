# Production Module

**Module Type:** STATEFUL (gatekeeper, guards the production folder)

**Purpose:** Rigorous peer review of academic submissions. Acts as senior editor AND domain expert reviewer. Determines whether submissions merit entry into production.

**Guards:** `gravity_field_model/calculations/prod/`

**Receives from:** UAT_MODULE (test files in uat/approved/ with embedded academic_paper)

---

## The Review Philosophy

> "Every piece of code in production represents a claim we stand behind. The review process ensures we can defend that claim to the scientific community."

The PROD_MODULE simulates a rigorous peer review process modeled on APS (American Physical Society) Physical Review standards:

1. **Editorial Assessment**: Is this submission appropriate and complete?
2. **Domain Expertise**: Become expert in the specific physics domain
3. **Scientific Review**: Evaluate methodology, results, and conclusions
4. **Decision**: Accept, revise, or reject with detailed feedback

---

## The Two-Phase Review Process

### Phase 1: Domain Expert Preparation

**Before grading, the reviewer MUST become a subject matter expert.**

This is not optional. The reviewer cannot assess a submission about neutron star density without first understanding:
- What standard physics says about neutron star density
- What measurements exist and their precision
- What the key parameters and relationships are
- What GFD specifically claims about this domain

```
┌─────────────────────────────────────────────────────────────────┐
│  DOMAIN EXPERT PREPARATION PROTOCOL                             │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  1. IDENTIFY THE DOMAIN                                         │
│     What area of physics does this submission address?          │
│     Example: "Gravitational wave chirp mass formula"            │
│                                                                 │
│  2. RESEARCH STANDARD PHYSICS                                   │
│     What does mainstream physics say about this?                │
│     - Key equations and their derivations                       │
│     - Experimental/observational evidence                       │
│     - Current understanding and open questions                  │
│     - Precision of measurements                                 │
│                                                                 │
│  3. UNDERSTAND GFD CLAIMS                                       │
│     What does GFD specifically claim here?                      │
│     - Is it a derivation or observation?                        │
│     - What geometric/structural argument is made?               │
│     - What predictions does it make?                            │
│                                                                 │
│  4. IDENTIFY KEY QUESTIONS                                      │
│     What would a skeptical expert ask?                          │
│     - Is the methodology sound?                                 │
│     - Are the comparisons fair?                                 │
│     - What alternative explanations exist?                      │
│                                                                 │
│  5. ESTABLISH EVALUATION CRITERIA                               │
│     What would constitute success/failure for this claim?       │
│     - What precision is expected?                               │
│     - What would falsify the claim?                             │
│     - What would strengthen it?                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 2: Scientific Review

With domain expertise established, conduct the formal review.

---

## Review Criteria (APS-Style)

The review evaluates five dimensions, each scored 0-20 (100 total):

### 1. Scientific Soundness (0-20)

| Score | Criterion |
|-------|-----------|
| 18-20 | Methodology is rigorous, reproducible, and appropriate. No logical errors. |
| 14-17 | Methodology is sound with minor issues. Conclusions follow from data. |
| 10-13 | Some methodological concerns but core approach is valid. |
| 5-9   | Significant methodological problems. Conclusions may not follow. |
| 0-4   | Fundamental errors in methodology. Results unreliable. |

**Key Questions:**
- Is the calculation correct?
- Is the comparison fair (like with like)?
- Are the error metrics appropriate?
- Would a skeptic accept the methodology?

### 2. Intellectual Honesty (0-20)

| Score | Criterion |
|-------|-----------|
| 18-20 | Exemplary honesty. Clear distinction between derivation and observation. All limitations acknowledged. |
| 14-17 | Good honesty. Minor overclaiming or missing caveats. |
| 10-13 | Adequate honesty. Some conflation of derivation/observation. |
| 5-9   | Concerning dishonesty. Significant overclaiming. |
| 0-4   | Intellectually dishonest. Misrepresents findings. |

**Key Questions:**
- Does the paper distinguish derivation from observation?
- Are limitations honestly acknowledged?
- Are alternative explanations mentioned?
- Does the conclusion overreach the evidence?

### 3. Contribution Value (0-20)

| Score | Criterion |
|-------|-----------|
| 18-20 | Major contribution. Advances understanding significantly. |
| 14-17 | Valuable contribution. Adds meaningful knowledge. |
| 10-13 | Incremental contribution. Useful but limited. |
| 5-9   | Marginal contribution. Little new knowledge. |
| 0-4   | No contribution. Duplicates existing work or adds nothing. |

**Key Questions:**
- What does this add to our understanding?
- Is this already known/documented elsewhere?
- Does this enable future investigations?
- Would the system be diminished without it?

### 4. Clarity & Presentation (0-20)

| Score | Criterion |
|-------|-----------|
| 18-20 | Crystal clear. A non-expert could follow. Beautifully structured. |
| 14-17 | Clear with minor issues. Well organized. |
| 10-13 | Understandable but could be clearer. Some organization issues. |
| 5-9   | Difficult to follow. Poor organization. |
| 0-4   | Incomprehensible. Cannot be reviewed. |

**Key Questions:**
- Can the reader understand the WHY?
- Is the methodology clear enough to reproduce?
- Are results presented clearly?
- Is the paper well-structured?

### 5. Reproducibility & Rigor (0-20)

| Score | Criterion |
|-------|-----------|
| 18-20 | Fully reproducible. All inputs documented. Code runs correctly. |
| 14-17 | Mostly reproducible. Minor details missing. |
| 10-13 | Reproducible with effort. Some assumptions unstated. |
| 5-9   | Difficult to reproduce. Key information missing. |
| 0-4   | Cannot be reproduced. |

**Key Questions:**
- Are all constants from documented sources?
- Are all inputs specified?
- Does the code actually run and produce stated results?
- Could an independent researcher reproduce this?

---

## Decision Thresholds

| Total Score | Decision | Action |
|-------------|----------|--------|
| 80-100 | **ACCEPT** | Move to prod/ |
| < 80 | **REJECT** | Test is DELETED (review archived) |

**Rejection Policy:** Tests that fail peer review are **deleted**, not revised. This enforces quality and prevents endless revision cycles. If a concept has merit, write a new, better test from scratch.

### PROD Guards (Cross-Check with UAT)

Before peer review, PROD performs validation checks (desk rejection):

| Guard | Requirement | Reason |
|-------|-------------|--------|
| **SINGLE TEST** | Exactly 1 test class | Cross-check with UAT |
| **question** | Non-empty string | Cross-check with UAT |
| **commentary** | Non-empty string | Cross-check with UAT |
| **contribution_score** | Must be `None` | PROD assigns this |

### Critical Criteria Gates

Even with score >= 80, REJECT if:
- Intellectual Honesty < 14 (cannot accept dishonest work)
- Scientific Soundness < 14 (cannot accept unsound work)

---

## The Review Report

Every submission receives a detailed review report:

```
================================================================
PEER REVIEW REPORT
================================================================
Submission: [Title]
Reviewer: PROD_MODULE
Date: [ISO date]
================================================================

DOMAIN EXPERTISE ESTABLISHED
-----------------------------
Domain: [e.g., Gravitational Wave Physics]
Key concepts reviewed:
- [Concept 1]
- [Concept 2]
Standard physics baseline:
- [What mainstream physics says]
GFD claim understood:
- [What this submission specifically claims]

SCORES
------
Scientific Soundness:     [X]/20
Intellectual Honesty:     [X]/20
Contribution Value:       [X]/20
Clarity & Presentation:   [X]/20
Reproducibility & Rigor:  [X]/20
-----------------------------
TOTAL:                    [X]/100

DECISION: [ACCEPT / MINOR REVISIONS / MAJOR REVISIONS / REJECT]

DETAILED FEEDBACK
-----------------

Scientific Soundness:
[Detailed comments on methodology, calculations, comparisons]

Intellectual Honesty:
[Comments on epistemic claims, limitations, honesty]

Contribution Value:
[Comments on what this adds to the system]

Clarity & Presentation:
[Comments on writing, structure, accessibility]

Reproducibility & Rigor:
[Comments on code quality, documentation, reproducibility]

REQUIRED CHANGES (if not ACCEPT)
--------------------------------
1. [Specific change required]
2. [Specific change required]
...

COMMENDATIONS (what was done well)
----------------------------------
1. [Positive feedback]
2. [Positive feedback]

RECOMMENDATION FOR AUTHORS
--------------------------
[Constructive guidance for improvement]

================================================================
```

---

## API Reference

### Review Submission

```python
from gravity_field_model.prod import review_submission

result = review_submission(
    submission_path="uat/approved/test_chirp_mass.py",  # Direct file path
)

# Returns:
# {
#     "decision": "ACCEPT" | "MINOR_REVISIONS" | "MAJOR_REVISIONS" | "REJECT",
#     "contribution_score": int,  # Assigned by PROD_MODULE
#     "scores": {
#         "scientific_soundness": int,
#         "intellectual_honesty": int,
#         "contribution_value": int,
#         "clarity_presentation": int,
#         "reproducibility_rigor": int,
#         "total": int,
#     },
#     "domain_expertise": {
#         "domain": str,
#         "concepts_reviewed": List[str],
#         "standard_physics": str,
#         "gfd_claim": str,
#     },
#     "feedback": {
#         "scientific_soundness": str,
#         "intellectual_honesty": str,
#         "contribution_value": str,
#         "clarity_presentation": str,
#         "reproducibility_rigor": str,
#     },
#     "required_changes": List[str],
#     "commendations": List[str],
#     "report_path": str,
# }
```

### Accept to Production

```python
from gravity_field_model.prod import accept_to_production

result = accept_to_production(
    submission_path="uat/approved/test_chirp_mass.py",  # Direct file path
    review_result=review_result,
)

# Writes contribution_score to test file
# Moves test file to prod/<domain>/
# Archives review report in prod/archive/
```

### List Production Contents

```python
from gravity_field_model.prod import list_prod_tests

tests = list_prod_tests()
tests_by_domain = list_prod_tests(domain="stellar_mechanics")
```

---

## Folder Structure

```
gravity_field_model/calculations/
├── sandbox/                    # Development
├── uat/
│   ├── pending/                # Awaiting approval
│   └── approved/               # Paper validated, awaiting peer review
│       ├── test_chirp_mass.py  # Test with embedded academic_paper
│       └── test_chirp_mass_REVIEW.md  # Review report (temporary)
└── prod/                       # GUARDED BY PROD_MODULE
    ├── stellar_mechanics/      # Domain folders
    ├── black_holes/
    ├── field_theory/
    └── archive/                # Review reports for accepted tests
        └── test_chirp_mass_REVIEW.md
```

---

## The Senior Editor Mindset

When reviewing, adopt this mindset:

> "I am the last line of defense before this claim joins our collective knowledge. Future researchers will trust that anything in production has been rigorously vetted. My review must be thorough enough that I would be comfortable defending this work at a conference."

### Questions a Senior Editor Asks

1. **Appropriateness**: Does this belong in our system at all?
2. **Completeness**: Is everything needed for evaluation present?
3. **Quality**: Does this meet our standards?
4. **Integrity**: Is this intellectually honest?
5. **Value**: Does this justify the space it will occupy?

### The Domain Expert Mindset

> "I must understand this domain well enough to catch errors that a generalist would miss. I must know what questions a specialist would ask. I must evaluate this as if I were reviewing for Physical Review."

### Questions a Domain Expert Asks

1. **Correctness**: Are the physics and math correct?
2. **Context**: Does this fit with what we know?
3. **Novelty**: Is this actually new or interesting?
4. **Soundness**: Is the methodology appropriate for this domain?
5. **Significance**: Does this matter to this field?

---

## Integration with Pipeline

```
uat/approved/test_*.py (with embedded academic_paper)
    │
    ▼
PROD_MODULE
    │
    ├─── Phase 1: Domain Expert Preparation
    │    (Research the physics, understand the claim)
    │
    ├─── Phase 2: Scientific Review
    │    (Score on 5 criteria, assign contribution_score)
    │
    ├─── Generate Review Report
    │
    └─── Decision
         │
         ├─── ACCEPT (>= 80, no critical failures)
         │    └─── Move to prod/<domain>/
         │
         └─── REJECT (< 80 or critical failure)
              └─── Test DELETED (review archived in prod/archive/rejected/)
```

---

## Quality Assurance

### Self-Consistency Checks

The PROD_MODULE should verify:
- [ ] Domain expertise was actually established (not skipped)
- [ ] All 5 criteria were scored with justification
- [ ] Feedback is actionable, not vague
- [ ] Decision is consistent with scores
- [ ] Report is complete

### Appeal Process

If the submitter disagrees with the review:
1. Author can respond to specific feedback
2. PROD_MODULE re-reviews with response in mind
3. Second review decision is final

---

*Document version: 1.0*
*Last updated: 2026-02-04*
*Location: framework/PROD_MODULE.md*
