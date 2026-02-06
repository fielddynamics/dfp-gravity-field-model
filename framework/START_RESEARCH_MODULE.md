# Start Research Module

**Module Type:** ORCHESTRATOR (coordinates the full test development pipeline)

**Purpose:** Entry point for all test development. Coordinates workflow and SCORES tests. Does NOT promote tests. Kicks off UAT_MODULE for promotion decisions.

**Delegates to:**
- TEST_QUALITY_MODULE (Stage 4: Audit scoring, sets `audit_score`)
- CONTRIBUTION_SCORING_MODULE (Stage 5: Self-assessment guidance only)
- SCIENTIFIC_REASONING_MODULE (Stage 6: Scientific Reasoning)
- **UAT_MODULE (Stage 7: Promotion decisions)** - START_RESEARCH_MODULE only requests, UAT decides
- FUNCTION_REGISTRY (Function Graduation)

**Note on contribution_score:** START_RESEARCH_MODULE may use CONTRIBUTION_SCORING_MODULE for self-assessment, but the test's `contribution_score` property MUST be `None` at promotion. PROD_MODULE assigns the official contribution score during peer review.

---

## The Central Question

When you open a test folder, ask yourself:

> **"With the tests that are here, how do I contribute something of value by moving forward what we know, in a form of scientific exploration that furthers understanding in this area?"**

This question grounds all probing work. You are not starting from scratch. You are joining an ongoing scientific investigation. The tests already here represent accumulated understanding. Your job is to **build on that foundation** and push it forward.

---

## Purpose

This module guides you in writing academically rigorous **probing tests** that:

1. **Start from what exists** in a test folder
2. **Identify what is already known** from those tests
3. **Ask what would be valuable to know next**
4. **Design tests that answer those questions**
5. **Document findings honestly** (observations vs derivations)

These are CERN-level quality tests that investigate, not merely validate.

---

## CRITICAL: One Test at a Time

**When probing, create ONE TEST per effort, not a test group.**

| DO | DON'T |
|----|-------|
| Create `sandbox_chirp_mass.py` with one test class | Create a file with 5+ test classes |
| Focus on ONE specific question | Try to cover an entire domain |
| One `academic_paper` per test | Multiple papers in one file |
| Depth over breadth | Breadth over depth |

**Why single tests?**
- Each test requires its own `academic_paper` (400-700 words)
- Each test goes through peer review independently
- Quality is easier to achieve with focused scope
- Rejection means deletion, so smaller scope = smaller risk

Test groups are for organizing **graduated** tests in production, not for development.

---

## Required Fields (Source of Truth: test_template.py)

**All required fields are defined in:** `gravity_field_model/templates/test_template.py`

### WHO Sets WHAT (Critical Pipeline Stages)

| Field | Set By | When | Notes |
|-------|--------|------|-------|
| `question` | DEV (you) | During test development | Non-empty string |
| `commentary` | DEV (you) | During test development | Non-empty string |
| `audit_score` | START_RESEARCH_MODULE | After quality audit | Must be >= 85 |
| `academic_paper` | **UAT_MODULE** | After UAT acceptance | **MUST be `None` at DEV submission** |
| `contribution_score` | **PROD_MODULE** | During peer review | **MUST be `None` at DEV submission** |

**DEV stage sets:** `question`, `commentary`, methods, `audit_score`
**DEV MUST NOT set:** `academic_paper`, `contribution_score` (desk rejection if set)

Plus at least ONE of these methods:
- `derivation()` returning Derivation
- `observations()` returning Observed  
- `model()` returning Model

**Desk rejection = test is not reviewed. Fix and resubmit.**

---

## Philosophy

### Contribution Over Creation

The goal is not to write many tests. The goal is to **contribute value**.

A single test that answers a question no one has asked before is worth more than ten tests that confirm what we already know. Before writing anything, ask:

- What does this folder already tell us?
- What question remains unanswered?
- If I knew the answer, would it change our understanding?

### Scientific Exploration, Not Validation

Probing tests are different from validation tests:

| Validation Tests | Probing Tests |
|------------------|---------------|
| Confirm known results | Ask new questions |
| Check that code works | Explore what physics predicts |
| Pass/fail binary | Findings may be surprising |
| "Does X equal Y?" | "WHY does X equal Y?" |

> "The goal is not to prove GFD right, but to understand what it predicts and where those predictions meet reality."

### Building on Previous Work

Every test folder has a history. Before adding to it:

1. **Read what's there** (not skim, read)
2. **Understand the questions asked** (why these tests?)
3. **Note the questions NOT asked** (gaps)
4. **Identify the natural next step** (what would add value?)

---

## Phase 0: Study Existing Tests First

**Before writing any new tests, study existing test files to understand patterns, identify gaps, and find opportunities to build upon previous work.**

### 0.0 The Entry Question

When you enter a test folder, complete this sentence:

> "The tests in this folder tell us that ____________. The next valuable question to answer is ____________."

If you cannot complete this sentence, you have not studied the folder enough.

**Example (field_theory/):**
> "The tests in this folder tell us that GFD's bimetric structure predicts exactly 2 GW polarizations, matching GR and LIGO observations. The next valuable question to answer is: do the numerical coefficients in GW formulas (32/5, 3/8, 5/3) have geometric interpretations?"

### 0.1 Existing Test Domains

The following test domains exist in `gravity_field_model/calculations/`:

| Domain | Folder | Description | Exemplary Tests |
|--------|--------|-------------|-----------------|
| **Stellar Mechanics** | `stellar_mechanics/` | Nuclear binding, fusion, stellar structure | `test_power_output.py`, `test_core_compression.py` |
| **Field Origin Geometry** | `historical_systems/field_origin_geometry/` | Geometric foundations, quantum correspondences | `test_quantum_foundations.py`, `test_origin_centrality.py` |
| **Emergent Constants** | `emergent_constants/` | Deriving G, alpha, spin from geometry | `test_G_derivation.py`, `test_spin_derivation.py` |
| **Particle Physics** | `particle_physics/` | Mass hierarchies, quark properties | `test_mass_hierarchy.py`, `test_quark_derivations.py` |
| **Black Holes** | `black_holes/` | Event horizons, Hawking radiation | `test_black_hole_mechanics.py` |
| **Entanglement** | `entanglement_mechanics/` | Quantum entanglement, nonlocality | `test_entanglement_advanced.py` |
| **Field Theory** | `field_theory/` | GW polarizations, variational methods | `test_gw_polarizations.py` |
| **Biological Mechanics** | `biological_mechanics/` | Iron in hemoglobin, biological field effects | `test_iron_hemoglobin.py` |
| **Coupling Dynamics** | `coupling_dynamics/` | Tetrahedra coupling mechanics | `test_tetrahedra_coupling.py` |
| **Quantum Tunneling** | `quantum_tunneling/` | Tunneling through field barriers | `test_tunneling.py` |

### 0.2 Rotating Study Assignment

**Each time you begin a new probing test effort, study a DIFFERENT existing test group.** This ensures cross-pollination of ideas and prevents tunnel vision.

**Rotation Schedule (pick based on current date or last studied):**

1. **Week 1 Focus**: `historical_systems/field_origin_geometry/`
   - Study: `test_quantum_foundations.py`, `test_geometric_quantum_correspondence.py`
   - Learn: How to document mathematical isomorphisms vs physical claims

2. **Week 2 Focus**: `emergent_constants/`
   - Study: `test_G_derivation.py`, `test_emergent_constants_extended.py`
   - Learn: How to derive constants from geometric principles

3. **Week 3 Focus**: `stellar_mechanics/`
   - Study: `test_binding_pathway_mechanics.py`, `test_subspace_packing.py`
   - Learn: How to verify standard physics while noting GFD patterns

4. **Week 4 Focus**: `particle_physics/`
   - Study: `test_mass_hierarchy.py`, `test_shell_structure.py`
   - Learn: How to explore mass ratios and shell closures

5. **Week 5 Focus**: `entanglement_mechanics/`
   - Study: `test_entanglement_advanced.py`, `test_subspace_nonlinearity.py`
   - Learn: How to probe quantum phenomena geometrically

6. **Week 6 Focus**: `black_holes/`
   - Study: `test_black_hole_mechanics.py`
   - Learn: How to test extreme gravity predictions

7. **Week 7 Focus**: `field_theory/`
   - Study: `test_gw_polarizations.py`, `test_variational_exterior_calculus.py`
   - Learn: How to connect to gravitational wave observations

8. **Week 8 Focus**: `coupling_dynamics/` and `cross_checks/`
   - Study: `test_tetrahedra_coupling.py`, `test_cross_checks.py`
   - Learn: How to verify internal consistency

### 0.3 What to Look For When Studying

**The goal is to find where you can contribute value.** When studying existing tests, ask:

**Understanding What's Here:**
- [ ] What question does this test answer?
- [ ] What understanding does this folder give us collectively?
- [ ] What assumptions are made that could be tested?

**Finding Value Opportunities:**
- [ ] What would be the NEXT question that builds on this?
- [ ] Is there a boundary condition not yet tested?
- [ ] Is there a related phenomenon in a different domain?
- [ ] Could a ratio or coefficient be tested for geometric significance?
- [ ] Is there a function that could be extracted for reuse?
- [ ] Are there cross-checks with other test domains?
- [ ] **NEW**: Does a standard physics formula have an unexplained numerical coefficient (e.g., why 6 in r_ISCO = 6GM/c^2)?
- [ ] **NEW**: Does an exponent in a scaling law match d, k, k+1, or combinations like d/(k+1)?
- [ ] **NEW**: Can this test be extended by asking "what happens at the boundary?"

### 0.4 Value Contribution Analysis

After studying a test group, document your analysis:

```markdown
## Value Contribution Analysis: <Test Group Name>

### What This Folder Tells Us
<2-3 sentences summarizing the collective understanding from existing tests>

### Existing Coverage
- Test 1: <what it covers>
- Test 2: <what it covers>

### Where I Can Add Value
| # | Opportunity | Why It Matters | Expected Contribution |
|---|-------------|----------------|----------------------|
| 1 | <Question not yet answered> | <Why knowing this would advance understanding> | <What we'd learn> |
| 2 | <Boundary not explored> | <Why the boundary is scientifically interesting> | <What we'd learn> |
| 3 | <Connection not made> | <Why this connection could unify understanding> | <What we'd learn> |

### Selected Contribution (Pick ONE to focus on)
**I will contribute value by answering:** <specific question>

**This advances understanding because:** <why it matters>

### Proposed Tests (to answer the question)
1. <Test name>: <one-line description>
2. <Test name>: <one-line description>

### Cross-Domain Connections
- Connects to <other domain>: <how>
- Could inform <other test file>: <why>
```

**Key principle:** Don't try to fill every gap. Pick the ONE contribution that would add the most value to the collective understanding, and do it well.

### 0.5 Pattern Catalog (Growing Reference)

As probing tests discover patterns, document them here for cross-reference:

| Pattern | Formula | GFD Interpretation | Status | Found In |
|---------|---------|-------------------|--------|----------|
| ISCO factor | 6 | SPATIAL faces (3 per tet x 2) | OBSERVATION | test_gw_probing.py |
| Photon sphere | 3 | d (spatial dimensions) | OBSERVATION | test_gw_probing.py |
| Chirp exponent | 3/5 | d/(k+1) | OBSERVATION | test_gw_probing.py |
| Chirp sum | 4/5 | k/(k+1) | OBSERVATION | test_gw_probing.py |
| Frequency evolution | 3/8 | d/2^d | OBSERVATION | test_gw_probing.py |
| Quadrupole numerator | 32 | 2^(k+1) = k*2^d | OBSERVATION | test_gw_probing.py |
| Quadrupole denominator | 5 | k+1 | OBSERVATION | test_gw_probing.py |
| Strain exponent | 5/3 | (k+1)/d | OBSERVATION | test_gw_probing.py |

**Pattern Status Key:**
- OBSERVATION: Numerical match documented, no physical derivation
- DERIVED: Mathematical derivation exists from GFD principles
- COINCIDENCE: Investigated and found to be coincidental
- CONFIRMED: Pattern verified across multiple domains

---

## Phase 0.6: Advanced Probing Methodology

This section provides systematic methods for answering the central question:

> **"With the tests that are here, how do I contribute something of value?"**

### The Value Test

Before writing any test, it must pass the **Value Test**:

> **"What would really make a difference if we knew this, given what we already know from the tests here?"**

If you cannot articulate why knowing the answer would matter, you are not ready to write the test.

**Value indicators:**
- **Leverage**: Does knowing X unlock understanding of Y, Z, and W?
- **Falsifiability**: If this pattern fails, what does that tell us?
- **Convergence**: Do multiple independent tests point the same direction?
- **Foundation**: Does this answer enable future questions to be asked?

### 0.6.1 Statistical Methods for Pattern Validation

Numerical coincidences are cheap. Statistical significance is expensive. Apply these methods:

**A) Coincidence Probability Analysis**

For any observed pattern (e.g., "factor of 6 = SPATIAL faces"), calculate:

```
P(coincidence) = (plausible interpretations) / (total integer range tested)
```

Example: If we look for patterns in coefficients 1-100 and have ~10 GFD numbers to match (k, d, k+1, k-1, 2^d, k!, d!, etc.), then:
- P(random match) ≈ 10/100 = 10% for any single coefficient
- Finding 5 matches in 5 coefficients: P ≈ (0.1)^5 = 0.001% (significant!)

**Test Template for Statistical Significance:**
```python
class PatternStatisticalSignificance(Test):
    """
    Assess whether observed patterns exceed random chance.
    """
    def model(self) -> Model:
        n_patterns_found = 8  # e.g., from GW probing
        n_coefficients_examined = 8
        n_gfd_numbers = 10  # k, d, k+1, 2^d, etc.
        p_single_match = n_gfd_numbers / 100  # assuming range 1-100
        p_all_match = p_single_match ** n_patterns_found
        
        return Model().add("P(all by chance)", p_all_match)
```

**B) Sensitivity Analysis**

Ask: "What if k were 3 or 5 instead of 4?"

This tests whether patterns are robust or fine-tuned:
- If patterns ONLY work for k=4, that's either profound or suspicious
- If patterns work for ANY k, they may be trivial identities
- If patterns work for k=4 and partially for k=3,5, that's interesting

**C) Cross-Domain Correlation**

When the same GFD ratio appears in unrelated domains, track it:

| Ratio | Domain 1 | Domain 2 | Domain 3 | Correlation |
|-------|----------|----------|----------|-------------|
| d/(k+1) = 3/5 | Chirp mass | ? | ? | Check stellar |
| (k+1)/d = 5/3 | GW strain | ? | ? | Check particle |
| d/2^d = 3/8 | GW frequency | ? | ? | Check tunneling |

### 0.6.2 The 10-Idea Brainstorm Protocol

**Before implementing any test, force yourself to brainstorm 10 ideas.** This prevents tunnel vision and surfaces unexpected connections.

**Step 1: Pick a Subtopic**

Choose a specific subtopic from existing tests (not the whole domain):
- NOT "stellar mechanics" (too broad)
- YES "nuclear binding energy scaling" (specific)
- YES "neutron star maximum mass" (specific)

**Step 2: Generate 10 Ideas (No Filtering Yet)**

For the subtopic, rapidly generate 10 probing questions. Use these prompts:

1. **Boundary Push**: What happens at the extreme limit?
2. **Inverse Question**: If X causes Y, does Y constrain X?
3. **Missing Factor**: What coefficient in the formula is unexplained?
4. **Cross-Domain**: Where else does this ratio/exponent appear?
5. **Historical**: Did the original derivation make an assumption we can test?
6. **Dimensional**: What does dimensional analysis predict vs. what we see?
7. **Statistical**: Is the observed precision suspicious or expected?
8. **Scaling**: How does this change with mass/length/time scale?
9. **Degeneracy**: Are there multiple ways to get the same number?
10. **Failure Mode**: What observation would DISPROVE this pattern?

**Step 3: Impact-Effort Matrix**

Rank each idea on two axes:

```
                    HIGH IMPACT IF TRUE
                           |
         [DO THESE]        |        [DO THESE FIRST]
         Complex but       |        Quick wins with
         worthwhile        |        major insight
                           |
    LOW  ------------------+------------------ HIGH
    EFFORT                 |                   EFFORT
                           |
         [SKIP]            |        [MAYBE LATER]
         Low value         |        Hard and
                           |        uncertain payoff
                           |
                    LOW IMPACT IF TRUE
```

**Step 4: Select Top 3**

From the 10 ideas, select 3 that are:
- In the upper-right quadrant (high impact, reasonable effort)
- Span different types of insight (not all "boundary push")
- Build on each other (test 2 uses results from test 1)

### 0.6.3 Expanding on Previous Test Thinking

When a test passes, don't stop. Ask:

**A) What Assumptions Were Made?**

Every test has implicit assumptions. List them and probe:

| Assumption | How to Test | What If Wrong? |
|------------|-------------|----------------|
| Circular orbit | Test eccentric orbits | Different coefficients? |
| Point masses | Include finite size effects | Corrections appear? |
| Weak field | Test strong field regime | Pattern breaks? |
| d=3 fixed | Vary d mathematically | Formula generalizes? |

**B) What Was Held Constant?**

Parameters held constant are probing opportunities:

```
Previous test fixed: M = M_solar
Probing question: Does the pattern hold for M = 0.1 M_solar? M = 100 M_solar?
                  Is there a mass scale where the pattern changes?
```

**C) What Would the NEXT Decimal Place Tell Us?**

If a test shows 0.3% agreement, ask:
- Is 0.3% the measurement precision, or is there real physics there?
- What would 0.03% precision reveal?
- Is there a GFD correction that predicts the 0.3% deviation?

**D) Combining Insights Across Tests**

Look for multiplicative insights:

```
Test A found: Coefficient X = k * 2^d = 32
Test B found: Coefficient Y = (k+1)/d = 5/3
Question: Does X * Y or X / Y appear anywhere?
          32 * (5/3) = 53.3...  (check other formulas)
          32 / (5/3) = 19.2     (check other formulas)
```

### 0.6.4 The "What Would Make a Difference" Filter

For every proposed test, complete this statement:

> "If this test confirms the pattern, it would make a difference because ___."
> "If this test refutes the pattern, it would make a difference because ___."

**Strong answers:**
- "...it would unify GW physics with particle mass hierarchies through a common geometric origin."
- "...it would rule out coincidence for the entire family of 3/8-type exponents."
- "...it would predict a measurable deviation from GR at the 0.1% level."

**Weak answers (reconsider the test):**
- "...it would add another data point."
- "...it would confirm what we already suspected."
- "...it would be interesting."

### 0.6.5 Example: Applying the Methodology

**Subtopic**: Chirp mass formula exponents (3/5, 1/5) from test_gw_probing.py

**10-Idea Brainstorm:**

1. **Boundary Push**: What happens to chirp mass formula for extreme mass ratios (q -> 0)?
2. **Inverse Question**: If 3/5 = d/(k+1), can we derive d=3 from chirp mass observations?
3. **Missing Factor**: The chirp mass appears in f(t) ~ M_c^(-5/8). Is -5/8 = -(k+1)/8?
4. **Cross-Domain**: Does 3/5 appear in any particle physics mass ratios?
5. **Historical**: Peters & Mathews derived this in 1963. What approximations did they make?
6. **Dimensional**: Dimensional analysis allows M_c ~ (m1*m2)^a / (m1+m2)^b with a+b=1. Why a=3/5 specifically?
7. **Statistical**: How precisely do LIGO measurements constrain the exponent? Is 3/5 exact or 0.600 ± 0.001?
8. **Scaling**: Does the chirp mass formula change in higher dimensions (d=4)?
9. **Degeneracy**: Are there other combinations of k,d that give 3/5? (e.g., k=5, d=3 gives 3/6=1/2, no)
10. **Failure Mode**: If we found a system where chirp mass exponent was 0.55, what would that mean?

**Impact-Effort Ranking:**

| # | Idea | Impact | Effort | Select? |
|---|------|--------|--------|---------|
| 1 | Extreme mass ratio | MED | LOW | Yes |
| 3 | -5/8 = -(k+1)/8 | HIGH | LOW | YES |
| 4 | Cross-domain to particles | HIGH | MED | YES |
| 6 | Why 3/5 specifically | HIGH | HIGH | Maybe |
| 7 | LIGO precision on exponent | MED | MED | Yes |

**Top 3 Tests to Implement:**
1. Test if -5/8 = -(k+1)/8 (extends the 3/8 pattern)
2. Search particle physics for 3/5 or 5/3 mass ratios
3. Check LIGO constraints on exponent precision

---

## Phase 1: Preparation and Domain Expertise

### 1.1 Determine Test Location

Before writing tests, determine where they belong:

**A) CHECK EXISTING FOLDERS:**
```
gravity_field_model/calculations/
├── biological_mechanics/     # Biological field effects
├── black_holes/              # Extreme gravity tests
├── coupling_dynamics/        # Tetrahedra coupling
├── cross_checks/             # Internal consistency
├── emergent_constants/       # Fundamental constants
├── entanglement_mechanics/   # Quantum entanglement
├── field_theory/             # GW, variational methods
├── historical_systems/       # Binary systems, field origin
│   └── field_origin_geometry/  # Geometric foundations
├── particle_physics/         # Particle properties
├── quantum_tunneling/        # Tunneling mechanics
└── stellar_mechanics/        # Nuclear/stellar physics
```

**B) DECISION CRITERIA:**
- If tests fit an existing folder's theme -> ADD to existing folder
- If tests form a NEW logical grouping with 4+ tests -> CREATE new folder
- If tests are closely related to existing file -> ADD to existing file
- If tests form a new theme within a folder -> CREATE new file in folder

**C) FOLDER CREATION (if needed):**
```python
# 1. Create folder: gravity_field_model/calculations/<new_topic>/
# 2. Create __init__.py:
"""<Topic> Tests for Gravity Field Model."""
# 3. Create test_<specific_topic>.py files
```

### 1.2 Become a Subject Matter Expert

Before writing a test group, research the domain thoroughly:

**A) CONSULT AUTHORITATIVE SOURCES:**
- Textbooks: Shapiro & Teukolsky (Black Holes), Weinberg (Gravitation)
- Review papers: Living Reviews in Relativity, Annual Reviews of Astronomy
- Data sources: CODATA, AME2020, NASA ADS, arXiv
- Observatories: LIGO/Virgo results, NICER data, Fermi catalogs

**B) IDENTIFY KEY QUANTITIES:**
For each domain, identify:
- Fundamental scales (mass, length, time, energy)
- Dimensionless ratios (these often reveal physics)
- Critical thresholds (phase transitions, limits, boundaries)
- Measured values with uncertainties

**C) MAP THE PARAMETER SPACE:**
- What are the extremes? (minimum, maximum values)
- What are the transitions? (regime changes)
- What are the anomalies? (unexplained observations)
- What are the predictions? (testable consequences)

**D) DOCUMENT YOUR RESEARCH:**
In the module docstring, cite your sources and explain what standard physics says vs what GFD might contribute.

### 1.3 Identify Probing Opportunities

Look for these test opportunities:

**A) NUMERICAL COINCIDENCES:**
- Does a ratio equal k=4, d=3, 2^d=8, k!=24?
- Does a coefficient match a tetrahedral number T_n?
- Does a power law exponent have a simple form?
- **HONESTY**: Document these as OBSERVATIONS, not explanations.

**B) BOUNDARY CONDITIONS:**
- Maximum/minimum values (Chandrasekhar limit, TOV limit)
- Phase transitions (neutronization, deconfinement)
- Stability limits (rotational breakup, tidal disruption)

**C) SCALING RELATIONS:**
- Power laws (L-M, M-R, P-P_dot relations)
- Dimensional analysis constraints
- Self-similarity in hierarchical structures

**D) UNEXPLAINED PATTERNS:**
- Why THIS specific value and not another?
- Why does the exponent equal THAT number?
- What sets the normalization?

---

## Phase 2: Test Design and Iteration

### 2.1 Design Test Progression

Tests should BUILD on each other. Structure your test file as:

```
TEST 1 (CRITICAL): Establish foundational measurement
  │
  ▼
TEST 2 (STANDARD): Derive a consequence from Test 1
  │
  ▼
TEST 3 (STANDARD): Compare derived value to independent measurement
  │
  ▼
TEST 4 (STANDARD): Explore a boundary or limiting case
  │
  ▼
TEST 5 (EXPLORATORY): Probe a speculative connection or pattern
  │
  ▼
TEST 6 (EXPLORATORY): Look for geometric correspondence
```

**EXAMPLE PROGRESSION (Neutron Stars):**
1. Verify nuclear saturation density (CRITICAL, establishes baseline)
2. Calculate NS central density range (STANDARD, uses Test 1)
3. Compare to observed NS mass-radius (STANDARD, independent check)
4. Test maximum mass limit (STANDARD, boundary condition)
5. Probe density/dimension correspondence (EXPLORATORY, pattern)
6. Explore k-packing interpretation (EXPLORATORY, GFD connection)

### 2.2 Iterative Refinement

After running tests, look at results and ask:

**A) WHAT DID WE LEARN?**
- Did the test reveal expected behavior?
- Were there surprises in the numbers?
- Did a ratio come out suspiciously close to an integer?

**B) WHAT SHOULD WE PROBE NEXT?**
- If result matched expectation: test a boundary condition
- If result showed deviation: investigate the source
- If ratio was near-integer: test if it's exact

**C) HOW CAN WE DIG DEEPER?**
- Add more precision to see if coincidence is exact
- Vary parameters to see if relationship is general
- Cross-check against independent measurements

**D) CAPTURE INSIGHTS IN FUTURE_QUESTIONS:**
When you think of a follow-up, encode it in the test's `future_questions` tuple for future investigation.

### 2.3 Cross-Domain Connections

Look for connections between test domains:

| If studying... | Look for connections to... |
|----------------|---------------------------|
| Stellar mechanics | Black holes (endpoint), Particle physics (nuclear) |
| Black holes | Field theory (horizons), Emergent constants (G) |
| Particle physics | Entanglement (quantum), Emergent constants (masses) |
| Field origin geometry | All domains (foundational geometry) |
| Emergent constants | All domains (constants appear everywhere) |

---

## Phase 3: Function Creation

### 3.1 Recognize Function Opportunities

Create a reusable `@Fn` function when:

**A) CALCULATION IS USED IN 2+ TESTS:**
If you're copying the same formula, extract it to a function.

**B) CALCULATION HAS PHYSICS MEANING:**
If the calculation represents a physical quantity that others might want, make it accessible.

**C) CALCULATION COULD BE USEFUL ELSEWHERE:**
If the calculation might be used in web interface, API, or other test modules, create a function.

**D) CALCULATION IS NON-TRIVIAL:**
If the calculation involves multiple steps, interpolation, or conditional logic, encapsulate it.

### 3.2 Function Definition Pattern

**See `gravity_field_model/examples/example_power_output.py` for complete pattern.**

**NAMING CONVENTION (Command Query Pattern):**
```python
fn_get_<what>(<params>)   # Query: returns data, no side effects
fn_set_<what>(<params>)   # Command: modifies state
fn_calc_<what>(<params>)  # Query: returns computed value
```

**EXAMPLE:**
```python
@Fn(
    equation="M_TOV = 0.7 * (hbar*c/G)^(3/2) / m_n^2",
    inputs={"stiffness": "float: EOS stiffness parameter (0.5-1.0)"},
    outputs={"mass_kg": "float: Maximum neutron star mass in kg"},
    description=(
        "Query: Returns Tolman-Oppenheimer-Volkoff maximum mass. "
        "Combines quantum degeneracy pressure with general relativistic "
        "self-gravity. Result depends on equation of state stiffness."
    ),
)
def fn_get_tov_mass_limit(stiffness: float = 0.7) -> float:
    """
    Query: Get maximum neutron star mass from TOV equation.
    
    Args:
        stiffness: EOS stiffness parameter (default 0.7 for realistic NS)
    
    Returns:
        Maximum mass in kg
    """
    m_planck_cubed = (HBAR * C / G) ** 1.5
    return stiffness * m_planck_cubed / M_N**2
```

### 3.3 Using Functions in Tests

```python
class TOVMassValidation(Test):
    """Validates fn_get_tov_mass_limit against observed NS masses."""
    
    name = "TOV Mass Limit"
    level = Level.CRITICAL
    
    # Inject the function using Depends
    get_tov = Depends(fn_get_tov_mass_limit)
    
    def model(self):
        return (
            Model()
            .add("TOV limit (M_solar)", self.get_tov(0.7) / M_SOLAR)
            .add("Stiff EOS limit", self.get_tov(1.0) / M_SOLAR)
        )
```

---

## Phase 4: Test Implementation

### 4.0 Sandbox First: Develop in Isolation

**Always write new tests in the sandbox folder first.** This allows rapid iteration without polluting the main test folders.

**Location:** `gravity_field_model/submissions/dev/`

**IMPORTANT: ONE TEST PER FILE**

Each sandbox file should contain **ONE test class** investigating **ONE question**. Do not create test groups during development. Test groups are for organizing graduated production tests.

**Workflow:**

```
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: CREATE SINGLE TEST IN SANDBOX                              │
│  ─────────────────────────────────────────────────────────────────  │
│  File: dev/dev_<specific_topic>.py                                  │
│  Example: dev/dev_chirp_mass_exponent.py (ONE test)                 │
│                                                                     │
│  Write ONE test class. Focus on ONE question.                       │
│  Include ONE academic_paper property (400-700 words).               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: RUN AND ITERATE                                            │
│  ─────────────────────────────────────────────────────────────────  │
│  python -m gravity_field_model.calculations.sandbox.sandbox_<topic> │
│                                                                     │
│  Keep iterating until:                                              │
│  - All tests pass                                                   │
│  - Results make sense                                               │
│  - Code is clean                                                    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: QUALITY AUDIT                                              │
│  ─────────────────────────────────────────────────────────────────  │
│  Apply TEST_QUALITY_MODULE.md to your sandbox tests.                │
│  Add audit_score and audit_notes to each test class.                │
│  Target: audit_score >= 85 for UAT promotion (high quality bar)     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: PRE-SUBMISSION CHECKLIST (REQUIRED FIELDS)                 │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  Before requesting promotion, verify ALL required fields are set.   │
│  Missing fields = DESK REJECTION (test won't even be reviewed).     │
│                                                                     │
│  See: gravity_field_model/templates/test_template.py for full spec  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  DESK REJECTION CHECKLIST (UAT Guards)                      │    │
│  │  ─────────────────────────────────────────────────────────  │    │
│  │                                                             │    │
│  │  DEV MUST SET:                                              │    │
│  │  [ ] ONE TEST CLASS per file (no test groups)               │    │
│  │  [ ] question = "..." (non-empty string)                    │    │
│  │  [ ] commentary = "..." (non-empty string)                  │    │
│  │  [ ] derivation() OR observations() OR model() method       │    │
│  │  [ ] audit_score = NN (>= 85 required)                      │    │
│  │                                                             │    │
│  │  DEV MUST NOT SET (desk reject if present):                 │    │
│  │  [ ] academic_paper = None (UAT writes this)                │    │
│  │  [ ] contribution_score = None (PROD assigns this)          │    │
│  │                                                             │    │
│  │  If ANY check fails: DESK REJECT                            │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 5: REQUEST PROMOTION (KICK OFF UAT_MODULE)                    │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  IMPORTANT: START_RESEARCH_MODULE only SCORES tests. It does NOT promote.  │
│  Promotion decisions are made by UAT_MODULE.                        │
│                                                                     │
│  GRADUATION CRITERIA (checked by UAT_MODULE):                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  All desk rejection checks pass (see Step 4 checklist)      │    │
│  │  audit_score >= 85         (quality threshold, high bar)    │    │
│  │  academic_paper = None     (UAT writes it after acceptance) │    │
│  │  contribution_score = None (PROD assigns during review)     │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  TO REQUEST PROMOTION:                                              │
│  ```python                                                          │
│  from gravity_field_model.pipeline import process_for_production         │
│                                                                     │
│  result = process_for_production(                                   │
│      source_file="dev/dev_my_test.py",                              │
│  )                                                                  │
│                                                                     │
│  if result["success"]:                                              │
│      print(f"Promoted to prod: {result['prod_path']}")              │
│      print(f"Contribution score: {result['contribution_score']}")   │
│  else:                                                              │
│      print(f"Rejected: {result['reason']}")                         │
│  ```                                                                │
│                                                                     │
│  IF ACCEPTED -> Test moves to prod/                                 │
│  IF REJECTED -> Test DELETED, review archived                       │
│                                                                     │
│  See UAT_MODULE.md for the full CI/CD pipeline.                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Test Naming Requirements:**

Test names must be **descriptive and specific**. A good test name tells you:
1. What physics domain is being explored
2. What specific question or phenomenon is investigated
3. What makes this test unique

| Quality | Example | Why |
|---------|---------|-----|
| **BAD** | `test_gw_probing.py` | Too vague. "Probing" what exactly? |
| **BAD** | `test_stuff.py` | Meaningless |
| **BAD** | `test_physics.py` | Every test is physics |
| **GOOD** | `test_gw_quadrupole_coefficient_32.py` | Specific: investigating 32/5 coefficient |
| **GOOD** | `test_isco_radius_factor_six.py` | Specific: why factor of 6? |
| **GOOD** | `test_chirp_mass_exponent_patterns.py` | Specific: exponent relationships |
| **GOOD** | `test_ns_density_nuclear_ratio.py` | Specific: NS to nuclear density ratio |

**Naming Pattern:**

```
test_<domain>_<specific_phenomenon>_<focus>.py
```

Examples:
- `test_gw_strain_scaling_chirp_mass.py` (domain: GW, phenomenon: strain, focus: chirp mass)
- `test_bh_isco_geometric_correspondence.py` (domain: black hole, phenomenon: ISCO, focus: geometry)
- `test_stellar_fusion_cno_efficiency.py` (domain: stellar, phenomenon: fusion, focus: CNO cycle)

**File Naming Convention (Stages):**

| Stage | Filename | Location |
|-------|----------|----------|
| Development | `dev_gw_quadrupole_coefficient_32.py` | `submissions/dev/` |
| Production | `test_gw_quadrupole_coefficient_32.py` | `submissions/prod/` |

**Class Naming Convention:**

Test class names should be equally descriptive:

| Quality | Example |
|---------|---------|
| **BAD** | `class GWTest(Test)` |
| **GOOD** | `class QuadrupoleCoefficientThirtyTwo(Test)` |
| **GOOD** | `class ISCORadiusSixFaces(Test)` |
| **GOOD** | `class ChirpMassExponentsDKPattern(Test)` |

**Benefits of Sandbox-First:**

1. **Rapid iteration**: No fear of breaking anything
2. **Clean git history**: Sandbox files can be .gitignored
3. **Clear status**: "sandbox_" prefix means "work in progress"
4. **Easy cleanup**: Delete failed experiments without trace
5. **Focus on learning**: Explore freely, formalize later

**Example sandbox file:**

```python
# gravity_field_model/submissions/dev/dev_ns_density_nuclear_ratio.py
# NOTE: Name is specific! Not "dev_ns_probing.py" or "dev_neutron_stuff.py"
"""
SANDBOX: Neutron Star Central Density to Nuclear Saturation Ratio
=================================================================

STATUS: Work in progress. Do not move until audit_score >= 85.

WHY THIS NAME:
- Domain: ns (neutron star)
- Phenomenon: density
- Focus: nuclear_ratio (comparing to nuclear saturation density)
- NOT "probing" (too vague) or "tests" (redundant)

EXPLORING:
- NS central density vs nuclear saturation density ratio
- Factor of ~3 correspondence to d (spatial dimensions)
- Density gradient at core boundary

WHAT WOULD BE VALUABLE TO KNOW:
- Is the ~3x ratio fundamental or coincidental?
- Does it vary systematically with NS mass?
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import G, C, HBAR, M_N

class NSDensityNuclearRatio(Test):
    """Compare neutron star central density to nuclear saturation density."""
    # Note: class name is also descriptive, not just "DensityTest"
    # ...

if __name__ == "__main__":
    run_all()
```

### 4.1 Contribution Scoring: Assessing Scientific Value

After the quality audit, assess each test's contribution using `CONTRIBUTION_SCORING_MODULE.md`.

**IMPORTANT:** This is for SELF-ASSESSMENT and GUIDANCE only. Use this to gauge whether your test is worth submitting. However, the `contribution_score` property on the test class **MUST be `None`** when you submit. PROD_MODULE assigns the official contribution score during peer review.

```python
# CORRECT: contribution_score must be None at submission
contribution_score = None  # PROD assigns this during peer review
contribution_notes = "..."  # You can keep notes for your own reference
```

**The Four Dimensions (100 points total):**

| Dimension | Points | Key Question |
|-----------|--------|--------------|
| **Discovery Value** | 0-40 | What's new here? |
| **Precision & Rigor** | 0-20 | How confident are we? |
| **Cross-Domain Impact** | 0-20 | Does this connect domains? |
| **Falsifiability** | 0-20 | Does this make predictions? |

**Quick Scoring Guide:**

**Discovery Value (0-40):**
- 35-40: Answers a fundamental unsolved problem
- 25-34: Reveals a previously unknown pattern/relationship  
- 15-24: Confirms a prediction with new evidence
- 5-14: Extends known physics to new domain
- 0-4: Routine verification

**Precision & Rigor (0-20):**
- 16-20: Multiple confirmations, high precision, P(random) < 10^-6
- 11-15: Strong confirmation, precision <1%
- 6-10: Reasonable confirmation, precision <5%
- 0-5: Suggestive but needs more evidence

**Cross-Domain Impact (0-20):**
- 16-20: Unifies 3+ domains
- 11-15: Connects two previously separate domains
- 6-10: Suggests connections worth investigating
- 0-5: Domain-specific only

**Falsifiability (0-20):**
- 16-20: Experimentally testable predictions
- 11-15: Observationally testable predictions
- 6-10: Constrains parameter space
- 0-5: Descriptive only

**Score Interpretation:**

| Score | Assessment | Action |
|-------|------------|--------|
| 70+ | Significant | High priority, highlight in documentation |
| 50-69 | Valuable | Keep and build on |
| 30-49 | Incremental | Useful supporting evidence |
| <30 | Routine | Consider if test adds value |

**Example contribution_notes (for self-assessment):**

```python
# Self-assessed score for guidance (use to decide if worth submitting)
# DO NOT set contribution_score on the test class, it MUST be None
contribution_score = None  # <-- REQUIRED: PROD assigns the official score
contribution_notes = (
    "Self-assessment: ~72/100. "
    "Discovery: 28/40 - Pattern 3/5 = d/(k+1) is novel observation. "
    "Precision: 15/20 - Mathematical exactness, part of larger pattern set. "
    "Cross-Domain: 17/20 - Chirp mass appears in all GW observations. "
    "Falsifiability: 12/20 - Predicts other exponents should follow same pattern."
)
```

### 4.2 Honesty Requirement

Each test MUST clearly distinguish between:
- **STANDARD PHYSICS**: What is measured or calculated from established theory
- **GFD OBSERVATIONS**: Numerical correspondences or patterns GFD notes
- **SPECULATIVE CONNECTIONS**: Exploratory ideas that may or may not have physical significance

### 4.2 Module Docstring Template

```python
"""
<Topic>: Probing Tests for <Specific Domain>
============================================

GFD Model V2

HONESTY STATEMENT:
This module verifies STANDARD <DOMAIN> PHYSICS and explores potential
GFD correspondences. The physics is well established. GFD provides
a geometric framework for interpretation but does NOT derive these
values from first principles.

WHAT IS VERIFIED (standard physics):
- <Measured quantity 1> from <source>
- <Measured quantity 2> from <source>
- <Theoretical prediction> from <theory>

GFD OBSERVATIONS (patterns noted, not derived):
- <Numerical coincidence 1>
- <Geometric correspondence 1>

TEXTBOOK REFERENCE:
GFD Textbook, Chapter N: <Relevant chapter title>

TEST GROUP GOALS:
This module explores <domain> by <approach>. Each test builds on
previous results to probe deeper into the physics. We seek to
understand not just WHAT the values are, but WHY they take these
specific values and WHETHER geometric constraints play a role.

Audience: Graduate-level physics students familiar with <prerequisites>.
"""
```

### 4.3 Test Class Template

```python
class ExampleProbingTest(Test):
    """
    Brief description of what this test probes.
    
    HONESTY: <What is standard physics vs GFD observation>
    """
    audit_score = 82  # Integer 74-95 reflecting test maturity
    audit_notes = None  # Or specific improvement notes
    future_questions = (
        "Q1: <Probing question that goes deeper into physics>? "
        "(Answering would improve <Aspect> by +N points: <benefit>) "
        "Q2: <Question that explores model connections>? "
        "(Answering would improve <Aspect> by +N points: <benefit>) "
        "Q3: <Question that suggests experimental/observational test>? "
        "(Answering would improve <Aspect> by +N points: <benefit>)"
    )
    name = "Clear, Descriptive Test Name"
    question = (
        "The 'Why' question driving this investigation. Should be 2-4 sentences "
        "that explain what we're trying to understand, not just what we're measuring."
    )
    reference = "Source citations (Author Year; Data source)"
    tolerance = 0.10  # Numerical tolerance (0.01 to 0.30 typically)
    level = Level.STANDARD  # CRITICAL, STANDARD, or EXPLORATORY
    commentary = (
        "3-5 sentences explaining the significance of this test and any caveats. "
        "Include what standard physics says, what GFD observes, and what remains "
        "unexplained. Be intellectually honest about what is derived vs observed."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("INTUITION: <Why should we expect this result?>")
            .step("STANDARD PHYSICS: <Established theoretical framework>")
            .step("<Logical step from theory>")
            .equation("<Key equation with symbols defined>")
            .step("<Numerical evaluation>")
            .step("GFD OBSERVATION: <Pattern or correspondence noted>")
            .conclude("<What this test establishes>")
        )
    
    def model(self) -> Model:
        calculated_value = some_calculation()
        
        return (
            Model()
            .add("Quantity name (units)", calculated_value)
            .add("Related quantity", another_value)
            .add("Ratio or comparison", ratio_value)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Quantity name (units)", expected_value)
            .add("Related quantity", expected_value)
            .add("Ratio or comparison", expected_value)
        )
```

### 4.4 Test Runner Template

```python
ALL_TESTS = [
    Test1,
    Test2,
    Test3,
    # ... in logical progression order
]

def run_all() -> bool:
    """Run all <topic> tests."""
    return run_tests(
        title="<Topic> Probing Tests",
        summary=(
            "Brief summary of what this test file investigates.\n"
            "STANDARD PHYSICS: <What is verified>\n"
            "GFD OBSERVATIONS: <What patterns are noted>"
        ),
        test_classes=ALL_TESTS,
    )

if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
```

---

## Phase 5: Probing Test Characteristics

### 5.1 Ask Deep "Why" Questions

**NOT:** "What is the neutron star mass limit?"
**BUT:** "Why does the TOV limit involve BOTH quantum degeneracy AND general relativity?"

### 5.2 Probe Boundaries and Edge Cases

- Maximum densities, minimum periods, critical thresholds
- Where do regimes transition? What controls the boundary?
- What happens at the limit? What breaks down?

### 5.3 Look for Geometric Correspondences

- Does a physical constant relate to k=4, tetrahedral numbers, cube geometry?
- Does a ratio match 2^d, d!, (d+1), T_n?
- **Note these as OBSERVATIONS, not explanations**

### 5.4 Connect to Cutting-Edge Observations

- Gravitational wave observations (LIGO/Virgo/KAGRA)
- Neutron star mass measurements (radio pulsars, X-ray binaries)
- X-ray timing (NICER mass-radius constraints)
- Multi-messenger astronomy

### 5.5 Maintain Intellectual Honesty

- "This is standard physics" vs "GFD notes this coincidence"
- "This is explained by [mechanism]" vs "This is observed"
- Never claim a GFD derivation where there is only a pattern match

### 5.6 Build on Previous Results

- Reference earlier tests in derivations
- Use values established by CRITICAL tests in later tests
- Show how understanding deepens through the progression

---

## Phase 6: Scientific Reasoning Extension

For high-contribution tests (contribution_score >= 70), apply the **SCIENTIFIC_REASONING_MODULE** to explore implications and generate the next chain of discovery.

**This phase delegates to SCIENTIFIC_REASONING_MODULE for all rules and thresholds.**

See: `framework/SCIENTIFIC_REASONING_MODULE.md` for full documentation.

### 6.0 Module Delegation

START_RESEARCH_MODULE delegates scientific reasoning logic to SCIENTIFIC_REASONING_MODULE. That module is the **single source of truth** for:

| Threshold | Value | Defined In |
|-----------|-------|------------|
| Brainstorm IMMEDIATE | >= 80 | SCIENTIFIC_REASONING_MODULE |
| Brainstorm QUEUE | >= 60 | SCIENTIFIC_REASONING_MODULE |
| Error Significance | >= 5% | SCIENTIFIC_REASONING_MODULE |
| Error Partial Match | >= 30% | SCIENTIFIC_REASONING_MODULE |

### 6.1 Three Modes of Reasoning

The SCIENTIFIC_REASONING_MODULE provides three complementary modes:

| Mode | Question | When to Use |
|------|----------|-------------|
| **Mapping Mode** | "What else should this connect to?" | After a validated test |
| **Equation Derivation** | "Can I derive this from GFD first principles?" | When encountering known physics |
| **Function Extraction** | "Can I make this reusable?" | When calculation appears in 2+ tests |

**Functions are just as valuable as tests.** See `examples/example_power_output.py` for the full pattern.

### 6.2 Brainstorming (delegates to SCIENTIFIC_REASONING_MODULE)

When a test validates a concept, apply the **Ten Mapping Brainstorm**:

1. Generate 10 ideas across the mapping categories
2. Score each on 5 criteria (Testability, Plausibility, Novelty, Impact, GFD Relevance)
3. Select based on thresholds (>= 80 immediate, >= 60 queue)

See `SCIENTIFIC_REASONING_MODULE.md` Part 2 for full protocol.

### 6.3 Error Bridge (delegates to SCIENTIFIC_REASONING_MODULE)

When error >= 5%, apply the **Error Bridge Protocol**:

1. Brainstorm 10 error source hypotheses
2. Design bridge tests for each plausible source
3. Track error reduction through the chain

See `SCIENTIFIC_REASONING_MODULE.md` Part 3 for full protocol.

### 6.4 Equation Derivation (delegates to SCIENTIFIC_REASONING_MODULE)

When encountering a standard physics equation:

1. Apply WHY protocol (3 questions)
2. Analyze components for GFD interpretation
3. Assess derivability score

See `SCIENTIFIC_REASONING_MODULE.md` Part 8 for full protocol.

### 6.5 Function Extraction (delegates to SCIENTIFIC_REASONING_MODULE + FUNCTION_REGISTRY)

When same calculation appears in 2+ tests:

1. Assess extraction criteria (from SCIENTIFIC_REASONING_MODULE Part 9)
2. Create @Fn function with audit_score and contribution_score
3. Check graduation status via FUNCTION_REGISTRY:

```python
from gravity_field_model.functions import assess_function_for_graduation

if assess_function_for_graduation(my_function):
    # Register in central catalog
    pass
```

### 6.6 Function Registry Integration

Functions must meet graduation criteria before being added to the central registry:
- `audit_score >= 65` (quality, from TEST_QUALITY_MODULE)
- `contribution_score >= 70` (value, from CONTRIBUTION_SCORING_MODULE)

The FUNCTION_REGISTRY is the **single source of truth** for graduation rules.

```python
# Check graduation status
from gravity_field_model.functions import assess_function_for_graduation
assess_function_for_graduation(my_function)

# Discover existing graduated functions
from gravity_field_model.functions import list_all_functions
list_all_functions()
```

See `framework/FUNCTION_REGISTRY_GUIDE.md` for full documentation.

---

## Imports Reference

```python
import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    # Fundamental constants (CODATA)
    G, C, HBAR, H, K_B,
    ALPHA, EPSILON_0, E_CHARGE,
    
    # Particle masses
    M_P, M_N, M_E, ELECTRON_MASS,
    M_P_MEV, M_N_MEV, M_E_MEV,
    
    # Solar/stellar constants
    M_SOLAR, R_SOLAR, L_SOLAR,
    
    # GFD geometric constants
    K_CLOSURE, VERTICES, TET_A, TET_B,
    
    # Length scales
    R_E, A_0, LAMBDA_COMPTON,
    
    # Energy conversions
    MEV_TO_JOULES, EV,
    
    # Additional as needed...
)
```

---

## Quality Checklist

Before submitting tests, verify:

### Module Level
- [ ] Module docstring includes HONESTY STATEMENT
- [ ] Sources cited for all data values
- [ ] Constants imported from `gravity_field_model.common`
- [ ] No magic numbers without documentation
- [ ] `ALL_TESTS` list in logical progression order
- [ ] `run_all()` function with informative summary

### Test Level
- [ ] `audit_score`, `audit_notes`, `future_questions` present
- [ ] `name`, `question`, `reference`, `tolerance`, `level`, `commentary` present
- [ ] `derivation()`, `model()`, `observations()` implemented
- [ ] Derivation includes STANDARD PHYSICS vs GFD OBSERVATION labels
- [ ] Commentary acknowledges limitations and caveats
- [ ] `future_questions` propose deeper investigations

### Function Level (if applicable)
- [ ] `@Fn` decorator with equation, inputs, outputs, description
- [ ] Naming follows `fn_get_`, `fn_calc_`, `fn_set_` convention
- [ ] Function is used in 2+ tests (justifies extraction)
- [ ] Docstring explains args and returns

### Execution
- [ ] Test file runs: `python -m gravity_field_model.calculations.<folder>.<file>`
- [ ] All tests pass or fail with clear explanation
- [ ] No import errors or missing dependencies

---

## Example: Complete Probing Test

```python
class NeutronStarDensityScale(Test):
    """
    Compare neutron star density to nuclear density.
    
    HONESTY: The ~3x ratio is measured astrophysical data.
    GFD notes that 3 = k-1 = d (spatial dimensions) as a correspondence.
    """
    audit_score = 82
    audit_notes = None
    future_questions = (
        "Q1: Why is neutron star central density 2-6x nuclear density rather than "
        "exactly matching? What physics allows the range? "
        "(Answering would improve Question by +3 points: explains density variation) "
        "Q2: Does the ~3x average ratio connect to d=3 spatial dimensions or to "
        "k-1 = 3 in any derivable way? "
        "(Answering would improve Commentary by +3 points: tests geometric connection) "
        "Q3: How do observations from NICER X-ray timing constrain the density range? "
        "(Answering would improve Observation Quality by +2 points: modern data)"
    )
    name = "Neutron Star Density Scale"
    question = (
        "Why does the average neutron star central density equal approximately "
        "3 times nuclear saturation density? Is this factor of ~3 (= d = k-1) "
        "coincidental or does it reflect a geometric packing constraint?"
    )
    reference = "Nuclear Physics; Lattimer & Prakash (2001)"
    tolerance = 0.30
    level = Level.EXPLORATORY
    commentary = (
        "Nuclear saturation density is ~2.3e17 kg/m^3. Neutron star central "
        "densities range from 2-6x this value, averaging ~3x. This factor of 3 "
        "equals both d (spatial dimensions) and k-1 (simplex vertices minus 1). "
        "GFD documents this correspondence without claiming it is explanatory. "
        "The actual density is determined by the equation of state."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Nuclear saturation density.")
            .equation("rho_0 = 2.3e17 kg/m^3 (measured)")
            .step("Neutron star central densities: 2-6 x rho_0")
            .step("Average: ~3 x rho_0 = 7e17 kg/m^3")
            .step("GFD OBSERVATION: 3 = d = k-1 (noted, not explained)")
            .conclude("NS density ~ 3 x nuclear density (astrophysics data)")
        )
    
    def model(self) -> Model:
        rho_nuclear = 2.3e17  # kg/m^3
        ratio_avg = 3.0
        rho_ns = rho_nuclear * ratio_avg
        k_minus_1 = K_CLOSURE - 1  # 3
        d = 3  # spatial dimensions
        
        return (
            Model()
            .add("Nuclear density (kg/m^3)", rho_nuclear)
            .add("NS/nuclear ratio", ratio_avg)
            .add("Ratio equals d", 1.0 if abs(ratio_avg - d) < 0.5 else 0.0)
            .add("Ratio equals k-1", 1.0 if abs(ratio_avg - k_minus_1) < 0.5 else 0.0)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Nuclear density (kg/m^3)", 2.3e17)
            .add("NS/nuclear ratio", 3.0)
            .add("Ratio equals d", 1.0)
            .add("Ratio equals k-1", 1.0)
        )
```

---

## Phase 4: Quality Assurance Pipeline

After writing a new test group, you MUST run the quality assurance pipeline before considering the work complete. This ensures tests meet the CERN-level quality standard.

### 4.1 The Pipeline (Execute in Order)

```
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: RUN TESTS                                                  │
│  ─────────────────────────────────────────────────────────────────  │
│  python -m gravity_field_model.calculations.<domain>.<test_file>    │
│                                                                     │
│  All tests must PASS before proceeding.                             │
│  If tests fail, fix the code first.                                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: AUDIT AGAINST QUALITY FRAMEWORK                            │
│  ─────────────────────────────────────────────────────────────────  │
│  Apply TEST_QUALITY_MODULE.md to each test class.                   │
│  Score all 8 criteria (100 points total):                           │
│                                                                     │
│  | Criterion              | Points | Key Question                   │
│  |------------------------|--------|--------------------------------|
│  | Question               | 15     | Does it hook curiosity?        │
│  | Derivation             | 15     | Intuition before math?         │
│  | Commentary             | 15     | Delivers insight?              │
│  | Model Output           | 10     | Summary stats, not dumps?      │
│  | Observation Quality    | 10     | Traceable sources?             │
│  | Constants Compliance   | 10     | Imports from /common/?         │
│  | Audience Accessibility | 15     | Undergrad to PhD?              │
│  | Test Group Header      | 10     | Module docs complete?          │
│                                                                     │
│  Record: audit_score and audit_notes for each test class.           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: IMPLEMENT REVISIONS                                        │
│  ─────────────────────────────────────────────────────────────────  │
│  For each test with audit_score < 85:                               │
│                                                                     │
│  1. Read audit_notes to identify specific issues                    │
│  2. Prioritize by point value (Question/Derivation/Commentary       │
│     are worth 15 pts each, highest impact)                          │
│  3. Make revisions following the framework guidance                 │
│  4. Update audit_score and audit_notes to reflect changes           │
│                                                                     │
│  Target: All tests should reach audit_score >= 80                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: RE-RUN TESTS                                               │
│  ─────────────────────────────────────────────────────────────────  │
│  python -m gravity_field_model.calculations.<domain>.<test_file>    │
│                                                                     │
│  Verify all tests still PASS after revisions.                       │
│  If any fail, fix and repeat from Step 1.                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 5: FINAL REVIEW                                               │
│  ─────────────────────────────────────────────────────────────────  │
│  Confirm:                                                           │
│  [ ] All tests pass                                                 │
│  [ ] All audit_scores >= 80 (or justified exceptions documented)    │
│  [ ] Module docstring complete (goals, coverage, limitations)       │
│  [ ] Pattern Catalog updated with any new discoveries               │
│  [ ] Cross-Domain Correlation table updated if applicable           │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Audit Checklist (Quick Reference)

For each test class, evaluate and score:

**Feynman Pedagogy (45 points)**
- [ ] **Question (15)**: Mystery hook? Why before what? Stakes clear?
- [ ] **Derivation (15)**: Situation, tension, insight, math, verdict? Analogies?
- [ ] **Commentary (15)**: Answers the question? Explains significance? Implication?

**Data Quality (20 points)**
- [ ] **Model Output (10)**: Summary statistics? Binary verdicts? No raw dumps?
- [ ] **Observation Quality (10)**: CODATA traceable? Sources documented?

**Engineering Standards (10 points)**
- [ ] **Constants Compliance (10)**: All from `/common/`? No hardcoded values?

**Pedagogical Depth (15 points)**
- [ ] **Audience Accessibility (15)**: Undergrad can follow? PhD learns something?

**Documentation (10 points)**
- [ ] **Test Group Header (10)**: Goals, categories, coverage, limitations stated?

**Bonus Checks (not scored but valuable)**
- [ ] Function extraction opportunity identified?
- [ ] Sample size adequate (1000+ pi digits for statistical claims)?
- [ ] future_questions drive next iteration?

### 4.3 Common Audit Findings and Fixes

| Finding | Points Lost | Fix |
|---------|-------------|-----|
| Question asks "what is X" not "why does X" | -8 Question | Reframe as mystery: "Why does X have this specific value?" |
| Derivation jumps to math without setup | -10 Derivation | Add SITUATION and TENSION steps before equations |
| Commentary restates numbers | -10 Commentary | State the insight in plain English, add analogy |
| Model dumps 8+ raw values | -6 Model | Replace with mean, CV, binary verdict |
| Observations have no source | -6 Observations | Add "Source: CODATA 2022" or paper citation |
| Constants hardcoded | -5 to -10 | Import from `gravity_field_model.common` |
| Expert-only language | -8 Accessibility | Add analogies, explain jargon, build from simple |
| Module docstring minimal | -6 Header | Add categories, coverage assessment, limitations |

### 4.4 Audit Notes Format

When writing audit_notes, use this structure:

```python
audit_score = 78
audit_notes = (
    "Question: 12/15 - Good curiosity hook but could emphasize stakes more. "
    "Derivation: 14/15 - Excellent intuition-first approach with analogy. "
    "Commentary: 10/15 - Explains result but could connect to bigger picture. "
    "Model: 9/10 - Good summary statistics. "
    "Observations: 8/10 - Values reasonable but source not explicitly cited. "
    "Constants: 10/10 - All imported from common modules. "
    "Accessibility: 12/15 - Graduate level, could add undergraduate-friendly intro. "
    "Header: 3/10 - Module docstring minimal, needs coverage assessment. "
    "FUNCTION OPPORTUNITY: Chirp mass calculation could be extracted to @Fn. "
    "RECOMMENDATION: Add 2-3 sentences to commentary connecting to GFD framework."
)
```

### 4.5 Revision Priority Matrix

When audit reveals multiple issues, prioritize by impact:

| Priority | Criteria | Rationale |
|----------|----------|-----------|
| **HIGH** | Question, Derivation, Commentary | 45 points combined; defines test quality |
| **MEDIUM** | Audience Accessibility, Header | 25 points; affects understanding |
| **LOWER** | Model Output, Observations, Constants | 30 points; engineering correctness |

**Rule**: Fix HIGH priority items first. A test with excellent pedagogy (Question/Derivation/Commentary) but imperfect constants is better than a test with perfect constants but no explanatory value.

### 4.6 Example: Audit and Revision Cycle

**Before Audit:**

```python
class ChirpMassExponents(Test):
    """Test chirp mass formula exponents."""
    
    audit_score = None  # Not yet audited
    audit_notes = None
    
    name = "Chirp Mass Exponents"
    question = "What are the exponents in the chirp mass formula?"  # BAD: asks "what"
    # ... rest of test ...
```

**After Audit (Step 2):**

```python
class ChirpMassExponents(Test):
    """Test chirp mass formula exponents."""
    
    audit_score = 62
    audit_notes = (
        "Question: 6/15 - Asks 'what' not 'why'. No mystery or stakes. "
        "Derivation: 10/15 - Has steps but no intuition setup. "
        "Commentary: 8/15 - Restates findings, doesn't deliver insight. "
        "Model: 9/10 - Good pattern matching output. "
        "Observations: 8/10 - Values correct but not cited. "
        "Constants: 10/10 - All imported. "
        "Accessibility: 8/15 - Graduate level, no analogies. "
        "Header: 3/10 - Minimal module docstring. "
        "RECOMMENDATION: Reframe question as mystery about why 3/5 specifically."
    )
    
    name = "Chirp Mass Exponents"
    question = "What are the exponents in the chirp mass formula?"
    # ... rest of test ...
```

**After Revision (Step 3):**

```python
class ChirpMassExponents(Test):
    """
    Probe the exponents 3/5 and 1/5 in the chirp mass formula.
    
    HONESTY: These exponents come from GR orbital dynamics.
    GFD notes that 3/5 + 1/5 = 4/5, and 4 = k. Also 3 = d, 5 = k+1.
    These are numerical observations, not derivations.
    """
    
    audit_score = 84  # Updated after revision
    audit_notes = (
        "Question: 13/15 - Now asks 'why 3/5 specifically' with GFD connection. "
        "Derivation: 13/15 - Added intuition about chirp mass meaning. "
        "Commentary: 12/15 - Better insight but could add more significance. "
        "Model: 9/10 - Unchanged, still good. "
        "Observations: 8/10 - Unchanged. "
        "Constants: 10/10 - Unchanged. "
        "Accessibility: 11/15 - Improved with GR context. "
        "Header: 8/10 - Module docstring now explains coverage. "
        "REMAINING: Could add analogy for chirp mass concept."
    )
    
    name = "Chirp Mass: Why 3/5 and 1/5?"  # Improved
    question = (
        "Why does the chirp mass have the specific form M_c = (m1*m2)^(3/5)/(m1+m2)^(1/5)? "
        "GFD observes that 3 = d (dimensions), 5 = k+1, and 3/5 + 1/5 = 4/5 where 4 = k. "
        "Are these numerological coincidences or hints of deeper structure?"
    )  # Now asks WHY with GFD context
    # ... improved derivation and commentary ...
```

### 4.7 Minimum Quality Thresholds

| Test Level | Minimum audit_score | Rationale |
|------------|---------------------|-----------|
| **CRITICAL** | 85 | Foundational tests must be exemplary |
| **STANDARD** | 75 | Core tests should be high quality |
| **EXPLORATORY** | 65 | Speculative tests have more latitude |

Tests below these thresholds should either be:
1. **Revised** to meet the threshold
2. **Demoted** to a lower level (e.g., STANDARD to EXPLORATORY)
3. **Marked** `level = Level.IGNORE` if not worth fixing

### 4.8 Pipeline Automation (Future)

The audit step is currently manual. Future automation could include:

```python
# Hypothetical automated audit (not yet implemented)
def audit_test_group(test_file_path: str) -> dict:
    """
    Run automated quality checks on a test file.
    
    Returns:
        dict with keys: 'scores', 'recommendations', 'function_opportunities'
    """
    # Check for hardcoded constants
    # Check for raw data dumps vs summary statistics
    # Check for missing docstrings
    # Check for question phrasing ("what" vs "why")
    # Suggest function extraction opportunities
    pass
```

Until automation exists, the manual checklist in 4.2 serves as the audit protocol.

---

## Phase 5: Contribution Summary

After completing a probing effort, document what you contributed. This closes the loop on the central question.

### 5.1 The Contribution Statement

Complete this template:

```markdown
## Contribution Summary: <Test File Name>

### Starting Point
Before this work, the tests in `<folder>` told us:
<What was already known>

### The Question I Asked
<The specific question you chose to investigate>

### What I Found
<Key findings, 2-4 bullet points>

### How This Advances Understanding
<Why these findings matter, what they enable>

### New Patterns Discovered
| Pattern | Value | GFD Interpretation | Status |
|---------|-------|-------------------|--------|
| <pattern> | <value> | <interpretation> | OBSERVATION/DERIVED |

### Questions This Opens
1. <Next question enabled by this work>
2. <Another question>
3. <Another question>

### Honest Assessment
- What worked well: <what>
- What could be improved: <what>
- Confidence level: HIGH/MEDIUM/LOW
```

### 5.2 Example Contribution Summary

```markdown
## Contribution Summary: test_gw_probing.py

### Starting Point
Before this work, the tests in `field_theory/` told us:
GFD's bimetric structure predicts exactly 2 GW polarizations, matching GR 
and LIGO observations. The geometric reason (2 TIME faces) was documented.

### The Question I Asked
Do the numerical coefficients in gravitational wave formulas (ISCO factor, 
chirp mass exponents, frequency evolution exponent, quadrupole coefficient, 
strain scaling) have geometric interpretations in terms of k, d, and 2^d?

### What I Found
- ISCO factor 6 = number of SPATIAL faces (3 per tet x 2)
- Chirp exponents 3/5 = d/(k+1), and sum 4/5 = k/(k+1)
- Frequency exponent 3/8 = d/2^d (dimensions over cube vertices)
- Quadrupole coefficient 32 = 2^(k+1) = k * 2^d (two independent decompositions)
- Strain exponent 5/3 = (k+1)/d

### How This Advances Understanding
Eight distinct GW coefficients match GFD geometric numbers. The probability 
of this by chance is ~(10/100)^8 = 10^-8 (one in 100 million). This suggests
the patterns are not coincidental, though they remain OBSERVATIONS not derivations.
The 3+5=8 relationship (exponents sum to unity) is particularly striking.

### New Patterns Discovered
| Pattern | Value | GFD Interpretation | Status |
|---------|-------|-------------------|--------|
| ISCO factor | 6 | SPATIAL faces | OBSERVATION |
| Chirp exponent | 3/5 | d/(k+1) | OBSERVATION |
| Frequency evolution | 3/8 | d/2^d | OBSERVATION |
| Quadrupole numerator | 32 | 2^(k+1) = k*2^d | OBSERVATION |
| Strain exponent | 5/3 | (k+1)/d | OBSERVATION |

### Questions This Opens
1. Does 3/8 = d/2^d appear in quantum tunneling rates?
2. Does 5/3 = (k+1)/d appear in particle mass ratios?
3. Can any of these patterns be DERIVED rather than observed?

### Honest Assessment
- What worked well: Systematic coefficient hunting, honest labeling of observations
- What could be improved: Could probe eccentric orbits, strong-field regime
- Confidence level: MEDIUM (patterns are striking but remain unexplained)
```

### 5.3 Update the Pattern Catalog

After completing a probing effort, **update the Pattern Catalog in Section 0.5** with any new patterns discovered. This ensures future probing efforts can build on your work.

---

## Appendix: Suggested Probing Test Topics

### Stellar Mechanics (expand existing)
1. Neutron star density scales
2. TOV mass limit derivation
3. White dwarf mass-radius inversion
4. Chandrasekhar coefficient (5.83)
5. Pulsar period limits
6. Gravitational wave chirp mass formula

### Black Holes (expand existing)
1. Schwarzschild radius coefficient (2)
2. ISCO radius (6GM/c^2)
3. Hawking temperature formula
4. Bekenstein-Hawking entropy
5. Photon sphere radius (3GM/c^2)

### Nucleosynthesis (new folder potential)
1. s-process abundance peaks
2. r-process neutron density threshold
3. Iron peak cosmic abundance
4. Odd-even abundance effect
5. Primordial lithium problem

### Gravitational Waves (expand field_theory)
1. Strain amplitude scaling
2. Frequency evolution (chirp)
3. Polarization modes
4. Energy flux formula
5. Ringdown frequencies

### Cosmology (new folder potential)
1. Hubble constant geometric interpretation
2. Dark energy density scale
3. Baryon asymmetry
4. CMB temperature
5. Cosmological constant problem

---

*Document version: 6.0*
*Last updated: 2026-02-04*
*Location: framework/START_RESEARCH_MODULE.md*

**Changelog:**
- v6.0: START_RESEARCH_MODULE no longer graduates tests. It only SCORES them. Graduation is delegated to UAT_MODULE which guards uat/ folder. This creates proper CI/CD pipeline separation. Step 5 now kicks off UAT_MODULE instead of doing promotion directly.
- v5.0: Renamed from FRAMEWORK to MODULE. Established as ORCHESTRATOR.
- v4.2: (Deprecated) Phase 6 delegated to Python module
- v4.1: Added sandbox-first workflow (Section 4.0)
- v4.0: Reframed around central question "How do I contribute value?"
- v3.0: Added Phase 4 (Quality Assurance Pipeline) with audit integration
- v2.0: Added Phase 0.6 (Advanced Probing Methodology)
- v1.0: Initial framework
