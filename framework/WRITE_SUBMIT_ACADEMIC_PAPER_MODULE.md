# Write & Submit Academic Paper Module

**Module Type:** STATELESS (defines structure and validation rules)

**Purpose:** Defines the structure and requirements for the `academic_paper` property on test classes. The paper is written by UAT_MODULE after the test passes DEV checks, then travels with the test to PROD for peer review.

**Key Concept:** The test file IS the submission. No separate files.

**WHO WRITES WHAT:**
| Property | Written By | When |
|----------|------------|------|
| `academic_paper` | **UAT_MODULE** | After test passes UAT guards |
| `contribution_score` | **PROD_MODULE** | During peer review |

**DEV MUST NOT SET `academic_paper`.** UAT writes it after acceptance.

---

## The Self-Contained Test Philosophy

> "A test is not merely code that passes. It is a claim about the physical world. That claim deserves the same scrutiny as any scientific paper."

Every test carries its own academic submission as the `academic_paper` property:

**At DEV stage (sandbox):**
```python
class MyTest(Test):
    name = "..."
    question = "..."
    audit_score = 87  # Assigned by START_RESEARCH_MODULE (>= 85 for UAT)
    academic_paper = None  # UAT_MODULE will write this
    contribution_score = None  # PROD_MODULE will assign this
```

**After UAT writes the paper:**
```python
class MyTest(Test):
    name = "..."
    question = "..."
    audit_score = 87
    academic_paper = """
    TITLE
    ...
    
    [400-700 words]
    """.strip()  # Written by UAT_MODULE
    contribution_score = None  # PROD_MODULE will assign this
```

**Benefits:**
- Single file to manage (no separate SUBMISSION.md)
- Paper travels WITH the test through CI/CD
- When in production, test contains its full academic justification
- `contribution_score` is written back by PROD_MODULE after review

---

## Word Limit

**Maximum: 700 words**
**Minimum: ~400 words** (to ensure substance)

The limit forces clarity and precision. If you cannot explain your contribution in 700 words, you do not understand it well enough.

---

## Required Structure

```
TITLE
[Concise title describing the investigation]

ABSTRACT (50 words)
[Brief summary: question, method, key finding]

1. INTRODUCTION: THE SCIENTIFIC QUESTION (150 words)
[1.1] What physical phenomenon demands explanation?
[1.2] What does standard physics say?
[1.3] What does GFD propose?
[1.4] What does this test specifically investigate?

2. METHODOLOGY (100 words)
[2.1] What calculations does the model perform?
[2.2] What data is used for comparison?
[2.3] What defines agreement?

3. RESULTS (150 words)
[3.1] Model output values with units
[3.2] Observational data with sources
[3.3] Comparison metrics
[3.4] Patterns observed (documented, not explained)

4. DISCUSSION (150 words)
[4.1] What do results mean physically?
[4.2] Epistemic status: DERIVATION or OBSERVATION?
[4.3] Significance
[4.4] Relation to other tests

5. LIMITATIONS & HONESTY STATEMENT (50 words)
[5.1] What this does NOT prove
[5.2] Assumptions made
[5.3] Potential weaknesses
[5.4] Further work needed

6. CONCLUSION (50 words)
[6.1] Summary of contribution
[6.2] Why this merits inclusion
```

---

## Intellectual Honesty Requirements

### Epistemic Clarity

| Claim Type | Label | When to Use |
|------------|-------|-------------|
| **DERIVATION** | "GFD derives X from first principles" | Mathematical proof exists |
| **PREDICTION** | "GFD predicted X before observation" | Prediction preceded data |
| **OBSERVATION** | "GFD notes X matches Y" | Numerical correspondence only |
| **SPECULATION** | "GFD suggests X might relate to Y" | Untested hypothesis |

### Forbidden Phrases

Never use:
- "This proves that..."
- "Clearly demonstrates..."
- "Undeniable evidence..."
- "GFD explains why..." (unless actual derivation)

### Required Phrases

Use:
- "The model calculates..."
- "This is consistent with..."
- "We observe that..."
- "The correspondence suggests..."

### Mandatory Disclosures

Every paper MUST include:
- At least one limitation
- At least one assumption
- At least one alternative interpretation

---

## Scoring Flow

```
START_RESEARCH_MODULE                          PROD_MODULE
     │                                       │
     ▼                                       ▼
┌─────────────┐                       ┌─────────────┐
│ audit_score │                       │contribution │
│  (quality)  │                       │   _score    │
│             │                       │ (peer review│
│ Assigned by │                       │    grade)   │
│ PROBING     │                       │             │
│             │                       │ Assigned by │
│ Threshold:  │                       │ PROD during │
│   >= 85     │                       │ review      │
│             │                       │             │
│ For UAT     │                       │ Threshold:  │
│ promotion   │                       │   >= 70     │
└─────────────┘                       └─────────────┘
```

**Key:** `contribution_score = None` until PROD_MODULE reviews the paper and assigns it.

---

## Test Class Template

```python
class MyTest(Test):
    """
    Test docstring with question/derivation/commentary.
    """
    
    name = "My Investigation Title"
    question = "Can we derive X from Y?"
    reference = "CODATA 2022"
    tolerance = 0.05
    level = Level.STANDARD
    
    commentary = "The results show..."
    
    # =========================================================================
    # SCORING
    # =========================================================================
    
    # Assigned by START_RESEARCH_MODULE (quality check)
    audit_score = 78
    audit_notes = "Question: 13/15, Derivation: 14/15, ..."
    
    # Assigned by PROD_MODULE during peer review
    # DO NOT set this yourself
    contribution_score = None
    
    # =========================================================================
    # ACADEMIC PAPER (700 words max)
    # =========================================================================
    
    academic_paper = """
TITLE
[Your title here]

ABSTRACT
[50 words]

1. INTRODUCTION: THE SCIENTIFIC QUESTION
[150 words]

2. METHODOLOGY
[100 words]

3. RESULTS
[150 words]

4. DISCUSSION
[150 words]

5. LIMITATIONS & HONESTY STATEMENT
[50 words]

6. CONCLUSION
[50 words]
    """.strip()
    
    def derivation(self) -> Derivation:
        ...
    
    def model(self) -> Model:
        ...
    
    def observations(self) -> Observed:
        ...
```

---

## Validation (UAT_MODULE)

When promoting to UAT, the module validates:

1. **academic_paper**: Must be `None` (UAT writes it, DEV must not set it)
2. **contribution_score**: Must be `None` (PROD assigns it)

After validation passes, UAT writes the paper:

1. **Word Count**: 400 <= words <= 700
2. **Structure**: Contains expected sections (advisory)

```python
from gravity_field_model.pipeline import check_eligibility

result = check_eligibility("dev/dev_my_test.py")
# {
#     "eligible": True/False,
#     "audit_score": 87,
#     "audit_passed": True,
#     "academic_paper_clean": True,  # Must be None (UAT writes it)
#     "contribution_score_clean": True,  # Must be None
# }
```

---

## Review (PROD_MODULE)

PROD_MODULE reviews the `academic_paper` and assigns `contribution_score`:

```python
from gravity_field_model.prod import review_submission

result = review_submission("uat/approved/test_my_test.py")
# {
#     "decision": "ACCEPT",
#     "contribution_score": 82,  # Assigned by this review
#     "total": 82,
#     "scores": {...},
# }
```

If accepted, PROD_MODULE writes `contribution_score` back to the test file.

---

## Example Paper

```python
academic_paper = """
TITLE
Chirp Mass Exponents and GFD Geometry: A Numerical Correspondence

ABSTRACT
This investigation examines whether chirp mass formula exponents (3/5, 1/5)
correspond to ratios of GFD parameters. The model calculates d/(k+1) = 3/5
exactly. This is documented as a numerical OBSERVATION, not a derivation.

1. INTRODUCTION: THE SCIENTIFIC QUESTION
The chirp mass formula M_c = (m1*m2)^(3/5) / (m1+m2)^(1/5) is fundamental to
gravitational wave astronomy. The exponents 3/5 and 1/5 emerge from General
Relativity. But why these values?

Standard physics derives them from quadrupole radiation mathematics. GFD
observes that 3/5 = d/(k+1) where d=3 (spatial dimensions) and k=4 (simplex
vertices). This suggests a geometric interpretation.

This test investigates whether the correspondence is exact.

2. METHODOLOGY
We calculate the ratio d/(k+1) using GFD parameters d=3, k=4. We compare
against the chirp mass exponent 3/5. Agreement criterion: exact match to
available precision.

3. RESULTS
Model output:
  - d/(k+1) = 3/5 = 0.6 (exact)
  - Chirp mass exponent: 3/5 = 0.6 (exact)
  - Difference: 0

The correspondence is exact, not approximate.

4. DISCUSSION
The match is exact by construction: both are rational numbers. However,
the significance is that GFD parameters (d, k) produce the same ratio that
appears in gravitational wave physics.

EPISTEMIC STATUS: OBSERVATION. GFD does not derive the chirp mass formula.
We note that the exponent equals a GFD ratio.

5. LIMITATIONS & HONESTY STATEMENT
This is NOT a derivation of gravitational wave physics from GFD. The
correspondence could be coincidental. GFD has not been validated. The
pattern gains weight only from multiple similar correspondences.

6. CONCLUSION
We document an exact correspondence between the chirp mass exponent and
the GFD ratio d/(k+1). This merits inclusion as part of the broader GFD-GW
correspondence pattern.
""".strip()
```

---

## Pipeline Summary

```
1. DEV writes test (question, commentary, methods)
2. START_RESEARCH_MODULE assigns audit_score (quality check)
3. UAT_MODULE validates: audit_score >= 85, academic_paper = None
4. UAT_MODULE writes academic_paper (400-700 words)
5. PROD_MODULE reviews paper, assigns contribution_score
6. If contribution_score >= 70 and decision = ACCEPT: move to prod/
7. If REJECT: test DELETED, review archived
8. Test in prod/ contains academic_paper + contribution_score
```

---

*Document version: 2.0*
*Last updated: 2026-02-04*
*Location: framework/WRITE_SUBMIT_ACADEMIC_PAPER_MODULE.md*
