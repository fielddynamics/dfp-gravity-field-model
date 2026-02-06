# Module Architecture

Enterprise-grade pipeline architecture for the Gravity Field Model test framework.

---

## Overview

The framework consists of **eight modules** that work together in a CI/CD pipeline. Each module has a single responsibility and clear interfaces to other modules.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           START_RESEARCH_MODULE                                    │
│                      (Development Orchestrator)                             │
│                                                                             │
│   Entry point for test development. Coordinates workflow and SCORING.      │
│   Does NOT promote tests. Hands off to UAT_MODULE after scoring.           │
└─────────────────────────────────────────────────────────────────────────────┘
         │              │                │                │              │
         ▼              ▼                ▼                ▼              ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   TEST      │  │CONTRIBUTION │  │ SCIENTIFIC  │  │  FUNCTION   │  │    UAT      │
│  QUALITY    │  │  SCORING    │  │ REASONING   │  │  REGISTRY   │  │   MODULE    │
│  MODULE     │  │   MODULE    │  │   MODULE    │  │             │  │             │
│             │  │             │  │             │  │             │  │ (Quality    │
│ STATELESS   │  │ STATELESS   │  │ STATELESS   │  │ STATEFUL    │  │ Pipeline    │
│ Audit rules │  │ Value rules │  │ Thinking    │  │ Guards func/│  │ Orchestrator│
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
                                                                          │
                                              ┌───────────────────────────┤
                                              │                           │
                                              ▼                           ▼
                                       ┌─────────────┐             ┌─────────────┐
                                       │WRITE_SUBMIT │             │    PROD     │
                                       │  ACADEMIC   │────────────>│   MODULE    │
                                       │PAPER_MODULE │             │             │
                                       │             │             │ STATEFUL    │
                                       │ STATELESS   │             │ Guards prod/│
                                       │ Validates   │             │ Peer review │
                                       │ papers      │             └─────────────┘
                                       └─────────────┘
```

**Orchestration Responsibilities:**
- **START_RESEARCH_MODULE**: Development + Scoring (hands off to UAT)
- **UAT_MODULE**: Quality Pipeline (orchestrates paper writing + peer review)

**Key Design Principle:** 
- START_RESEARCH_MODULE only SCORES tests (development + scoring)
- UAT_MODULE orchestrates the complete quality pipeline (validation + paper writing + review)
- WRITE_SUBMIT_ACADEMIC_PAPER_MODULE defines paper structure (called by UAT to write paper)
- PROD_MODULE conducts peer review, assigns contribution_score
- gate.py handles file movement (dev -> uat -> prod or deletion)

---

## The Full Pipeline Flow

```
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ submissions/dev/  │───>│ submissions/uat/  │───>│ submissions/prod/ │
│                   │    │                   │    │                   │
│ DEV writes:       │    │ UAT:              │    │ PROD:             │
│ - question        │    │ 1. Validates      │    │ - Peer review     │
│ - commentary      │    │ 2. Moves here     │    │ - Assigns         │
│ - methods         │    │ 3. Writes paper   │    │   contribution    │
│ - audit_score     │    │ 4. Triggers PROD  │    │   score           │
│                   │    │                   │    │                   │
│ academic_paper    │    │ academic_paper    │    │ ACCEPT: move here │
│   = None          │    │   written here    │    │ REJECT: delete    │
│ contribution_score│    │                   │    │   from uat/       │
│   = None          │    │                   │    │                   │
└───────────────────┘    └───────────────────┘    └───────────────────┘
```

**Pipeline folders:** `gravity_field_model/submissions/`
- `dev/` - Development stage (DEV sets question, commentary, audit_score)
- `uat/` - UAT stage (test moves here, UAT writes academic_paper)
- `prod/` - Production (PROD moves accepted tests here)
- `prod/archive/` - Archived review reports

**Flow:** `dev/` -> `uat/` -> `prod/`

**Key:** The `academic_paper` is written by UAT_MODULE (400-700 words) after moving test from dev/ to uat/. DEV must NOT set this property. PROD reviews in uat/, then moves to prod/ or deletes.

---

## Module Types

### Stateless Modules (Utility Libraries)

These modules provide **rules, criteria, and protocols**. They have no folder to manage and no state to maintain. They are pure functions that take inputs and return outputs.

| Module | File | Purpose | Exports |
|--------|------|---------|---------|
| TEST_QUALITY_MODULE | `TEST_QUALITY_MODULE.md` | Audit scoring rules | 8 criteria, scoring guide, thresholds |
| CONTRIBUTION_SCORING_MODULE | `CONTRIBUTION_SCORING_MODULE.md` | Value assessment rules | 4 dimensions, scoring guide, thresholds |
| SCIENTIFIC_REASONING_MODULE | `SCIENTIFIC_REASONING_MODULE.md` | Thinking protocols | Brainstorming, error analysis, equation derivation |
| WRITE_SUBMIT_ACADEMIC_PAPER_MODULE | `WRITE_SUBMIT_ACADEMIC_PAPER_MODULE.md` | Paper validation | 400-700 word structure, honesty validation |

### Stateful Modules (Registries/Gatekeepers)

These modules **guard a folder** and accumulate artifacts over time.

| Module | Files | Purpose | Guards |
|--------|-------|---------|--------|
| UAT_MODULE | `UAT_MODULE.md`, `uat/gate.py` | Test promotion gate + **pipeline orchestrator** | `calculations/uat/` |
| PROD_MODULE | `PROD_MODULE.md`, `prod/reviewer.py` | Peer review gate | `calculations/prod/` |
| FUNCTION_REGISTRY | `FUNCTION_REGISTRY_GUIDE.md`, `functions/registry.py` | Function catalog | `gravity_field_model/functions/` |

**Note:** UAT_MODULE is both a gatekeeper AND an orchestrator. It guards `uat/` and orchestrates calls to WRITE_SUBMIT_ACADEMIC_PAPER_MODULE and PROD_MODULE.

---

## Pipeline Flow (Complete CI/CD)

### Stage Responsibilities

```
STAGE 1-3: DEVELOPMENT (START_RESEARCH_MODULE)
├── Study existing tests
├── Design test progression
├── Implement in sandbox/
└── Run and iterate

STAGE 4: AUDIT (START_RESEARCH_MODULE delegates to TEST_QUALITY_MODULE)
├── Score on 8 criteria
├── Calculate audit_score
└── Document audit_notes
    (START_RESEARCH_MODULE ONLY SCORES, does NOT promote)

STAGE 5: CONTRIBUTION (START_RESEARCH_MODULE delegates to CONTRIBUTION_SCORING_MODULE)
├── Score on 4 dimensions
├── Calculate contribution_score
└── Document contribution_notes
    (START_RESEARCH_MODULE ONLY SCORES, does NOT promote)

STAGE 6: SCIENTIFIC REASONING (START_RESEARCH_MODULE delegates to SCIENTIFIC_REASONING_MODULE)
├── Apply if contribution_score >= 70
├── Brainstorm next mappings
└── Document reasoning chain

STAGE 7: REQUEST PROMOTION (START_RESEARCH_MODULE kicks off UAT_MODULE)
├── START_RESEARCH_MODULE calls: request_promotion(sandbox_file, target_domain)
├── UAT_MODULE checks eligibility (audit >= 85, paper valid)
├── UAT_MODULE promotes to uat/pending/ or rejects
└── START_RESEARCH_MODULE does NOT touch UAT folder directly

STAGE 8: APPROVAL (UAT_MODULE)
├── Manual or automated review
├── approve_for_production() moves to uat/approved/
└── Ready for academic submission

STAGE 9: ACADEMIC VALIDATION (WRITE_SUBMIT_ACADEMIC_PAPER_MODULE)
├── Validates academic_paper property (400-700 words)
├── Checks intellectual honesty requirements
├── Paper is embedded in test class, travels with the file
└── Test file ready for peer review in uat/approved/

STAGE 10: PEER REVIEW (PROD_MODULE)
├── establish_domain_expertise() (Phase 1: become expert)
├── review_submission() scores on 5 criteria (Phase 2)
├── Decision: ACCEPT / MINOR_REVISIONS / MAJOR_REVISIONS / REJECT
└── Review report generated

STAGE 11: PRODUCTION (PROD_MODULE)
├── accept_to_production() moves to prod/<domain>/
├── Papers and reviews archived in prod/archive/
└── Test is now in production

FUNCTION GRADUATION (parallel track)
├── START_RESEARCH_MODULE creates @Fn with scores
├── FUNCTION_REGISTRY checks graduation (audit >= 65, contribution >= 70)
└── FUNCTION_REGISTRY adds to catalog if graduated
```

---

## Module Interfaces

### START_RESEARCH_MODULE (Orchestrator)

**Imports from:**
- TEST_QUALITY_MODULE: Audit criteria and scoring
- CONTRIBUTION_SCORING_MODULE: Value assessment criteria
- SCIENTIFIC_REASONING_MODULE: Brainstorming and reasoning protocols
- UAT_MODULE: Promotion API
- FUNCTION_REGISTRY: Graduation check and function catalog

**Exports:**
- Complete test development workflow
- Templates and checklists
- Pipeline stages

### TEST_QUALITY_MODULE

**Imports from:** None (stateless)

**Exports:**

| Export | Description |
|--------|-------------|
| **8 Audit Criteria** | Question, Derivation, Commentary, Model Output, Observation Quality, Constants Compliance, Audience Accessibility, Test Group Header |
| **Scoring Guide** | Points per criterion (100 total) |
| **Thresholds** | CRITICAL >= 85, STANDARD >= 75, EXPLORATORY >= 65 |
| **Templates** | Question writing, derivation structure, commentary format |

### CONTRIBUTION_SCORING_MODULE

**Imports from:** None (stateless)

**Exports:**

| Export | Description |
|--------|-------------|
| **4 Scoring Dimensions** | Discovery Value (0-40), Precision & Rigor (0-20), Cross-Domain Impact (0-20), Falsifiability (0-20) |
| **Scoring Guide** | Rubric for each dimension |
| **Thresholds** | GRADUATE >= 70, VALUABLE >= 50, INCREMENTAL >= 30 |
| **Interpretation** | What each score level means |

### SCIENTIFIC_REASONING_MODULE

**Imports from:** None (stateless)

**Exports:**

| Export | Description |
|--------|-------------|
| **WHY Protocol** | 3 questions before exploring connections |
| **Brainstorming Protocol** | 10 mapping categories, scoring criteria |
| **Selection Thresholds** | IMMEDIATE >= 80, QUEUE >= 60, NOTE >= 40 |
| **Error Bridge Protocol** | 10 error source categories, bridge test design |
| **Equation Derivation Protocol** | Component analysis, GFD interpretation |
| **Reasoning Chain Template** | Documentation format for discovery chains |

### WRITE_SUBMIT_ACADEMIC_PAPER_MODULE

**Imports from:** None (stateless, but reads test files)

**Exports:**

| Export | Description |
|--------|-------------|
| **validate_paper()** | Validates embedded academic_paper property |
| **extract_paper()** | Extracts academic_paper from test class |
| **extract_test_info()** | Parses test file for metadata |
| **validate_honesty()** | Checks for overclaiming, missing limitations |
| **HONESTY_CHECKS** | Forbidden phrases, required elements, preferred phrases |

**Paper Structure:**
1. Abstract (50 words)
2. Introduction: The Scientific Question (150 words)
3. Methodology (100 words)
4. Results (150 words)
5. Discussion (150 words)
6. Limitations & Honesty Statement (50 words)
7. Conclusion: Merit for Inclusion (50 words)
8. References

**Usage:**
```python
from gravity_field_model.pipeline import validate_honesty, extract_test_info

paper_text = extract_paper("uat/approved/test_my_test.py")
result = validate_paper(paper_text)  # Returns {"passed": bool, "word_count": int, ...}
```

### UAT_MODULE (Gatekeeper)

**Imports from:**
- TEST_QUALITY_MODULE: audit_score threshold (>= 85)
- WRITE_SUBMIT_ACADEMIC_PAPER_MODULE: paper validation (word count, honesty)

**Exports:**

| Export | Description |
|--------|-------------|
| **check_eligibility()** | Check if test meets promotion criteria |
| **request_promotion()** | Promote from sandbox to uat/pending/ |
| **list_uat_tests()** | List tests in UAT by state |
| **approve_for_production()** | Move from pending to approved |
| **submit_for_peer_review()** | Submit from approved to PROD for peer review |

**Guards:**
- `gravity_field_model/calculations/uat/` folder
- Only tests meeting thresholds are promoted

### PROD_MODULE (Gatekeeper + Peer Reviewer)

**Imports from:**
- WRITE_SUBMIT_ACADEMIC_PAPER_MODULE: Submission structure
- Domain knowledge base (internal)

**Exports:**

| Export | Description |
|--------|-------------|
| **establish_domain_expertise()** | Phase 1: Become expert in physics domain |
| **review_submission()** | Phase 2: Score submission on 5 criteria |
| **accept_to_production()** | Move accepted test to prod/<domain>/ |
| **list_prod_tests()** | List tests in production by domain |
| **get_review_report()** | Retrieve review report for submission |

**Review Criteria (APS-style):**
1. Scientific Soundness (0-20)
2. Intellectual Honesty (0-20)
3. Contribution Value (0-20)
4. Clarity & Presentation (0-20)
5. Reproducibility & Rigor (0-20)

**Decision Thresholds:**
- ACCEPT: >= 80 (and no critical failures) -> Move to prod/
- REJECT: < 80 (or critical failure) -> Test is DELETED

**Rejection Policy:** Tests that fail peer review are **deleted**, not revised. If the concept has merit, write a new test from scratch.

**Guards:**
- `gravity_field_model/calculations/prod/` folder
- Only peer-reviewed, accepted tests enter

**Usage:**
```python
from gravity_field_model.prod import review_submission, accept_to_production

result = review_submission("uat/approved/test_my_test.py")
if result["decision"] == "ACCEPT":
    accept_to_production("uat/approved/test_my_test.py", result)
```

### FUNCTION_REGISTRY (Gatekeeper)

**Imports from:**
- TEST_QUALITY_MODULE: audit_score threshold (>= 65)
- CONTRIBUTION_SCORING_MODULE: contribution_score threshold (>= 70)

**Exports:**

| Export | Description |
|--------|-------------|
| **Function Catalog** | All graduated functions by group |
| **Graduation Check** | `assess_function_for_graduation()` API |
| **Discovery Utilities** | `list_all_functions()`, `list_functions_by_group()` |
| **Registration** | `register_function()` (rejects non-graduated) |

**Guards:**
- `gravity_field_model/functions/` folder
- Only graduated functions are added to catalog

---

## Thresholds Summary (Single Source of Truth)

### Validation Guards (Desk Rejection)

Both UAT and PROD perform these checks. Failure = desk rejection before scoring.

| Guard | Requirement | Checked By |
|-------|-------------|------------|
| **SINGLE TEST** | Exactly 1 test class per file | UAT + PROD |
| **question** | Non-empty string | UAT + PROD |
| **commentary** | Non-empty string | UAT + PROD |
| **derivation/observations** | Method exists | UAT |
| **contribution_score** | Must be `None` | UAT + PROD |

### Test Promotion (UAT_MODULE)

| Criterion | Threshold | Source Module |
|-----------|-----------|---------------|
| audit_score | >= 85 | TEST_QUALITY_MODULE |
| academic_paper | 400-700 words | WRITE_SUBMIT_ACADEMIC_PAPER_MODULE |

Note: `contribution_score` is NOT checked by UAT. It is assigned by PROD_MODULE during peer review.

### Academic Paper (WRITE_SUBMIT_ACADEMIC_PAPER_MODULE)

| Criterion | Threshold | Source Module |
|-----------|-----------|---------------|
| Word count | 400-700 | WRITE_SUBMIT_ACADEMIC_PAPER_MODULE |
| Structure | Required sections present | WRITE_SUBMIT_ACADEMIC_PAPER_MODULE |

### Peer Review (PROD_MODULE)

| Criterion | Threshold | Source Module |
|-----------|-----------|---------------|
| Total review score | >= 80 | PROD_MODULE |
| contribution_score | >= 70 | PROD_MODULE (assigned during review) |
| Intellectual Honesty | >= 14 | PROD_MODULE (critical, out of 20) |
| Scientific Soundness | >= 14 | PROD_MODULE (critical, out of 20) |

Note: PROD_MODULE assigns `contribution_score` to the test during peer review. This is the scientific value grade.

### Function Graduation

| Criterion | Threshold | Source Module |
|-----------|-----------|---------------|
| audit_score | >= 65 | FUNCTION_REGISTRY (reads from @Fn) |
| contribution_score | >= 70 | FUNCTION_REGISTRY (reads from @Fn) |

### Brainstorm Selection

| Action | Threshold | Source Module |
|--------|-----------|---------------|
| IMMEDIATE (write test now) | >= 80 | SCIENTIFIC_REASONING_MODULE |
| QUEUE (add to backlog) | >= 60 | SCIENTIFIC_REASONING_MODULE |
| NOTE (revisit later) | >= 40 | SCIENTIFIC_REASONING_MODULE |
| DISCARD | < 40 | SCIENTIFIC_REASONING_MODULE |

---

## File Organization

```
framework/
├── MODULE_ARCHITECTURE.md          # This file (wiring diagram)
├── START_RESEARCH_MODULE.md               # Orchestrator (scores, kicks off UAT)
├── TEST_QUALITY_MODULE.md          # Audit rules (stateless)
├── CONTRIBUTION_SCORING_MODULE.md  # Value rules (stateless)
├── SCIENTIFIC_REASONING_MODULE.md  # Thinking protocols (stateless)
├── WRITE_SUBMIT_ACADEMIC_PAPER_MODULE.md  # Paper generation (stateless)
├── PROD_MODULE.md                  # Peer review gate (stateful)
├── UAT_MODULE.md                   # UAT gate documentation (stateful)
└── FUNCTION_REGISTRY_GUIDE.md      # Function registry guide (stateful)

gravity_field_model/
├── academic/                       # WRITE_SUBMIT_ACADEMIC_PAPER_MODULE API
│   ├── __init__.py                 # Exports paper generation functions
│   └── paper_generator.py          # Paper generation logic
├── prod/                           # PROD_MODULE API
│   ├── __init__.py                 # Exports peer review functions
│   └── reviewer.py                 # Peer review logic
├── uat/                            # UAT MODULE API
│   ├── __init__.py                 # Exports UAT functions
│   └── gate.py                     # Promotion logic
├── functions/                      # GUARDED BY FUNCTION_REGISTRY
│   ├── __init__.py                 # Exports graduated functions
│   └── registry.py                 # Graduation logic, catalog
└── calculations/
    ├── sandbox/                    # Development area (not guarded)
    ├── uat/                        # GUARDED BY UAT_MODULE
    │   ├── pending/                # Tests awaiting approval
    │   └── approved/               # Tests approved, awaiting peer review
    │       ├── test_*.py           # Test with embedded academic_paper
    │       └── *_REVIEW.md         # Review reports (temporary)
    └── prod/                       # GUARDED BY PROD_MODULE
        ├── stellar_mechanics/      # Domain folders
        ├── black_holes/
        ├── field_theory/
        ├── particle_physics/
        └── archive/                # Review reports for accepted tests
            └── *_REVIEW.md
```

---

## Cross-Module Communication

### START_RESEARCH_MODULE calls other modules:

```python
# Stage 4: Audit
# Reference: TEST_QUALITY_MODULE.md for criteria
audit_score = apply_8_criteria(test)  # Conceptual

# Stage 5: Contribution
# Reference: CONTRIBUTION_SCORING_MODULE.md for dimensions
contribution_score = apply_4_dimensions(test)  # Conceptual

# Stage 6: Scientific Reasoning
# Reference: SCIENTIFIC_REASONING_MODULE.md for protocols
if contribution_score >= 70:
    apply_why_protocol()
    brainstorm_10_mappings()

# Stage 7: UAT Promotion
# Actual Python API call
from gravity_field_model.pipeline import process_for_production
request_promotion("sandbox/sandbox_my_test.py", "stellar_mechanics")
```

### UAT_MODULE calls WRITE_SUBMIT_ACADEMIC_PAPER_MODULE:

```python
# After approval, validate embedded paper (paper is a class property)
from gravity_field_model.pipeline import validate_honesty, extract_test_info

paper_text = extract_paper("uat/approved/test_my_test.py")
validation = validate_paper(paper_text)  # Checks word count, honesty
```

### PROD_MODULE reviews tests:

```python
# Peer review process (reviews test file directly, paper is embedded)
from gravity_field_model.prod import review_submission, accept_to_production

result = review_submission("uat/approved/test_my_test.py")
if result["decision"] == "ACCEPT":
    accept_to_production("uat/approved/test_my_test.py", result)
```

---

## Design Principles

1. **Single Responsibility**: Each module does one thing well
2. **Single Source of Truth**: Thresholds defined in one place, referenced elsewhere
3. **Stateless Where Possible**: Most modules are pure utilities
4. **Explicit Dependencies**: Clear imports between modules
5. **Pipeline as Orchestration**: START_RESEARCH_MODULE coordinates, does not duplicate logic
6. **Documentation as Interface**: Markdown modules define the contract
7. **Academic Rigor**: Submissions require intellectual honesty validation
8. **Peer Review as Gate**: Production requires expert review, not just scores

---

## The Academic Pipeline Philosophy

> "A test is not merely code that passes. It is a claim about the physical world. That claim deserves the same scrutiny as any scientific paper."

### Why Academic Papers?

1. **Forces Clarity**: Writing 700 words forces clear articulation of the WHY
2. **Prevents Overclaiming**: Honesty validation catches "this proves..." language
3. **Documents Limitations**: Required limitations section acknowledges weaknesses
4. **Creates Audit Trail**: Papers and reviews archived for future reference
5. **Enables Peer Review**: Structured submission enables meaningful review

### Why Peer Review?

1. **Domain Expertise**: Reviewer must understand the physics before grading
2. **Multiple Criteria**: Not just "does it pass" but scientific soundness, honesty, value
3. **Actionable Feedback**: Revisions guided by specific comments
4. **Quality Gate**: Production only contains rigorously reviewed work

---

*Document version: 2.0*
*Last updated: 2026-02-04*
*Location: framework/MODULE_ARCHITECTURE.md*
