ts# Test Quality Framework

A guide for writing tests that communicate clearly and provide genuine value.

**The Feynman Chain of Logic**: Context establishes curiosity, intuition builds understanding, results confirm or challenge, and mechanism empowers the reader to go further.

## The Golden Rule

**If you can't explain what the test proves in one sentence, rewrite it.**

A test exists to answer a question. If the reader finishes the test output and still doesn't know the answer, the test has failed at its primary job.

---

## The Eight Quality Criteria

Every test is scored on eight dimensions. These criteria ensure tests are pedagogically sound, scientifically rigorous, and engineeringly correct.

| # | Criterion | Points | Domain |
|---|-----------|--------|--------|
| 1 | **Question** | 15 | Feynman Pedagogy |
| 2 | **Derivation** | 15 | Feynman Pedagogy |
| 3 | **Commentary** | 15 | Feynman Pedagogy |
| 4 | **Model Output** | 10 | Data Quality |
| 5 | **Observation Quality** | 10 | Data Quality |
| 6 | **Constants Compliance** | 10 | Engineering Standards |
| 7 | **Audience Accessibility** | 15 | Pedagogical Depth |
| 8 | **Test Group Header** | 10 | Documentation |
| | **Total** | **100** | |

---

## The Feynman Principle: Why Before What

Richard Feynman's pedagogical philosophy holds that **utility and intuition must precede abstraction**. Teaching a formula (the "what") or a derivation (the "how") is meaningless if the reader doesn't first understand the problem it solves or the physical reality it describes (the "why").

### The Problem with "What-First"

Starting with "here are the face counts" is just vocabulary. It doesn't explain:
- Why we're counting faces
- What problem this solves
- What would be concerning if the counts were different

### The "Why" Hook

Feynman started with the **physical mystery**. Before showing any numbers, establish the curiosity:

> "We want to know if the traversal algorithm has a hidden bias. If certain faces get visited more than others, the geometry isn't being explored fairly. But how do we detect bias in 30,000 data points?"

Now the reader **wants** to see the coefficient of variation. The math becomes a relief, a tool they actually want to use.

### The Four-Step Structure

Every test should follow this sequence:

| Step | Purpose | Example |
|------|---------|---------|
| **1. WHY** (Context) | Define the physical tension | "We need to know if the traversal is fair" |
| **2. INTUITION** (Mental Model) | Explain in everyday terms | "Like checking if a die is loaded" |
| **3. WHAT** (Results) | Show the data | "CV = 1.7%, well below 15% threshold" |
| **4. HOW** (Mechanism) | Technical details | "Computed std_dev / mean across 8 faces" |

---

## The Three Questions Every Test Must Answer

Before writing any test, answer these three questions:

### 1. WHY does this matter?
What physical mystery or practical problem does this address? What would it mean if this test failed? Start here, not with what you're measuring.

### 2. WHAT are we measuring?
Define the quantity or property being tested in plain language. Connect it back to the "why."

### 3. WHAT is the verdict?
Provide a clear pass/fail criterion that the reader can verify.

---

## Writing the Question (The Hook)

The question field is your chance to **hook the reader's curiosity**. It should make them want to know the answer before they see any numbers.

### Bad Questions (What-First)

These questions jump straight to measurement without establishing why we care:

| Bad Question | Problem |
|--------------|---------|
| "What are the redundant read counts per face?" | Just asking for data, no mystery |
| "What is the value of alpha?" | Asking for a number, not insight |
| "Are the face counts equal?" | Technical, no physical motivation |

### Good Questions (Why-First)

These questions establish the **physical tension** first:

| Good Question | Why It Works |
|---------------|--------------|
| "Does the traversal algorithm have a hidden bias, or does it explore the geometry fairly?" | Establishes stakes (fairness), creates curiosity (hidden bias) |
| "Why does the fine structure constant have this specific value, and can we derive it from geometry?" | Asks the deep "why", not just "what is it" |
| "If we walk randomly on this shape using pi digits, do some faces get neglected?" | Everyday language (walk, neglected), creates mental image |

### The Question Formula

A good question follows this pattern:

```
[Physical curiosity/mystery] + [What would it mean if true/false]?
```

Examples:
- "Is there a geometric reason for k=4, or is it just a fitting parameter?"
- "Does the traversal treat all faces equally, or does the geometry create bias?"
- "Can we predict atomic radii from this formula, or does it only work by curve-fitting?"

---

## Writing the Derivation (Building Intuition)

The derivation should build a **mental scaffolding** before showing any math. The reader should be nodding along, anticipating what comes next.

### The Intuition-First Structure

```
1. PHYSICAL SETUP: What situation are we examining? (No math yet)
2. THE TENSION: What's the question or puzzle?
3. THE INSIGHT: What key idea resolves the tension?
4. THE MATH: Now the equations (reader is ready for them)
5. THE VERDICT: What does this tell us?
```

### Example: Bad Derivation (Math-First)

```
Derivation
  STEP 1: Compute CV = std_dev / mean
  STEP 2: CV = 0.017
  STEP 3: 0.017 < 0.15, so pass
```

This is a recipe, not an explanation. The reader follows the steps but learns nothing.

### Example: Good Derivation (Intuition-First)

```
Derivation
  THE SITUATION: We have an algorithm that walks around 8 faces of a 
  geometric shape, driven by the digits of pi. 
  
  THE QUESTION: Does every face get visited roughly equally, or does 
  the algorithm favor some faces over others? If certain faces get 
  hit 10x more than others, we'd have a biased explorer.
  
  THE APPROACH: Think of it like checking if a die is loaded. We roll 
  it many times and check if each number comes up equally often. The 
  coefficient of variation (CV) measures spread relative to average. 
  A fair die has CV near 0; a loaded die has high CV.
  
  EQUATION: CV = std_dev(face_counts) / mean(face_counts)
  
  CRITERION: CV < 15% means no significant bias (like a fair die).
  
  VERDICT: If CV is low, the traversal explores all faces equally.
```

Now the math makes sense. The reader understands CV as "the loaded die detector."

---

## Writing the Commentary (The Insight)

The commentary is where you deliver the **"aha" moment**. It should:
1. State what we learned (not just what we measured)
2. Connect back to the original mystery
3. Explain what this means for the bigger picture

### Bad Commentary (Restates Numbers)

```
Commentary
  The coefficient of variation is 0.017, which is less than 0.15.
  The test passes.
```

This adds nothing. The reader already saw the numbers.

### Good Commentary (Delivers Insight)

```
Commentary
  The traversal has no geometric bias. Despite the complex 8-faced 
  shape and the seemingly random walk driven by pi digits, every 
  face gets roughly equal attention. The coefficient of variation 
  of just 1.7% is remarkably low, like a casino die that lands on 
  each number within 2% of perfect fairness.
  
  This matters because if certain faces were neglected, the geometric 
  model would have blind spots. Instead, we've confirmed the algorithm 
  explores the full structure uniformly.
```

### The Commentary Formula

```
1. ANSWER: State the conclusion in plain English
2. SIGNIFICANCE: Why does this matter? What does it tell us?
3. ANALOGY: Connect to everyday understanding
4. IMPLICATION: What can we now trust or do as a result?
```

### Commentary Depth Checklist

- [ ] Does it answer the original question explicitly?
- [ ] Does it explain WHY the result matters, not just WHAT it is?
- [ ] Does it use an analogy or everyday language?
- [ ] Could a curious undergraduate understand the significance?
- [ ] Does it connect this result to the bigger picture?

---

## Writing Observations (The Ground Truth)

The `observations()` method defines the **expected values** that the model should produce. This is where you establish what "correct" looks like. Poor observation quality is one of the most common test failures.

### What Makes Good Observations

Observations must be:

1. **Traceable**: Where did this number come from? CODATA? A textbook? An experiment?
2. **Realistic**: Does this represent a real physical quantity or just a guess?
3. **Appropriately Precise**: 10% error tolerance vs 0.01% matters for different quantities
4. **Documented**: If the value is empirical, cite the source

### Observation Quality Scoring (10 points)

| Score | Description |
|-------|-------------|
| **10** | All values traceable to authoritative sources (CODATA, peer-reviewed papers). Tolerances appropriate for the measurement precision. |
| **8** | Values are reasonable and documented, minor traceability gaps. |
| **6** | Values appear correct but lack documentation or source citation. |
| **4** | Some values are guesses or placeholders, unclear provenance. |
| **2** | Values are arbitrary or clearly wrong, no documentation. |
| **0** | Observations missing or nonsensical. |

### Bad Example: Undocumented Observations

```python
def observations(self):
    return (
        Observed()
        .add("Alpha", 0.0073)  # Where did this come from? What precision?
        .add("Error %", 5.0)   # Is 5% expected? Based on what?
    )
```

### Good Example: Traceable Observations

```python
def observations(self):
    # Source: CODATA 2022, NIST Reference on Constants
    # Alpha = 7.2973525643(11) x 10^-3, relative uncertainty 1.5 x 10^-10
    return (
        Observed()
        .add("Alpha (derived)", ALPHA)           # From constants_codata.py
        .add("Alpha (CODATA)", 7.2973525643e-3)  # CODATA 2022 value
        .add("Agreement within 0.01%", 1)        # Binary: 1 = yes, 0 = no
    )
```

### Observation Categories

| Category | Example | Expected Precision | Notes |
|----------|---------|-------------------|-------|
| **CODATA constants** | alpha, c, hbar | < 0.001% | Use `constants_codata.py` values |
| **Derived identities** | QED relations | 0% (exact) | Mathematical identities must be exact |
| **Empirical fits** | Atomic radii | 5-15% | Document the fitted formula source |
| **Statistical properties** | CV, distribution | Threshold-based | Use clear pass/fail criterion |
| **Binary checks** | Invariant holds | 0 or 1 | No partial credit |

---

## Constants Compliance (Engineering Standards)

**Never hardcode constants in test files.** This is a critical engineering standard that ensures:

1. **Single source of truth**: All constants come from verified sources
2. **Traceability**: CODATA values are documented with uncertainties
3. **Maintainability**: Update once, apply everywhere
4. **Auditability**: Reviewers can verify where values originate

### Constants Compliance Scoring (10 points)

| Score | Description |
|-------|-------------|
| **10** | All constants imported from `/common/` modules. No magic numbers. Pi digits from `pi_data.py`. |
| **8** | Most constants imported, 1-2 minor inline definitions with justification. |
| **6** | Several hardcoded constants, but major ones (c, hbar, alpha) imported correctly. |
| **4** | Significant hardcoding, unclear where values originate. |
| **2** | Most constants hardcoded, no use of common modules. |
| **0** | All constants hardcoded, no imports from common modules. |

### The Common Modules

Always import from these verified sources:

| Module | Purpose | Example Constants |
|--------|---------|-------------------|
| `constants_codata.py` | CODATA 2022 physical constants | `C`, `HBAR`, `ALPHA`, `LAMBDA_COMPTON`, `M_E`, `EV` |
| `pi_data.py` | Verified pi base-8 digits (10,000 digits) | `PI_BASE8_FRACTIONAL`, `get_pi_base8()` |
| `geometry_constants.py` | Stellated octahedron geometry | `TET_A`, `TET_B`, `FACES`, `TIME_FACES`, `SPATIAL_FACES` |
| `atomic_data.py` | Atomic/nuclear data | Element properties, binding energies |
| `stellar_constants.py` | Astrophysical constants | Solar mass, luminosity, etc. |

### Bad Example: Hardcoded Constants

```python
# BAD - constants defined in test file
K = 4
ALPHA = 1/137.036
HBAR = 1.055e-34  # J*s
C = 2.998e8  # m/s
ELECTRON_MASS = 9.109e-31  # kg
LAMBDA_COMPTON = 2.426310238e-12  # m

# BAD - pi digits copied inline (may contain errors!)
PI_BASE8_FRACTIONAL = [
    1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, ...
]

# BAD - geometry hardcoded
TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}
```

### Good Example: Imported Constants

```python
# GOOD - import from verified common modules
from gravity_field_model.common.constants_codata import (
    C, HBAR, ALPHA, LAMBDA_COMPTON, M_E, EV
)
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL, get_pi_base8
from gravity_field_model.common.geometry_constants import (
    TET_A, TET_B, FACES, TIME_FACES, SPATIAL_FACES,
    get_tetrahedron, get_vertex_parity
)

# If you need a derived constant, document the derivation
F_CLOSURE = C / LAMBDA_COMPTON  # Settlement frequency, derived from CODATA
```

### Why This Matters: The Pi Digits Bug

The `pi_data.py` module header contains this warning:

> CRITICAL NOTE: The previous PI_BASE8_FRACTIONAL arrays scattered across
> the codebase contain INCORRECT digits from position 25 onwards.

This is exactly why constants must be centralized. A bug in one copy propagates everywhere. By importing from a single verified source, we fix bugs once and all tests benefit.

### Sample Size Adequacy (Pi Digits)

When using pi digits for traversal tests, **use at least 1,000 digits** for statistical validity. Using only 50 digits is insufficient for:

- Ergodicity claims (need long-run averages)
- Distribution analysis (need sufficient samples per bucket)
- Closure cycle counting (need multiple complete cycles)

| Sample Size | Verdict | Use Case |
|-------------|---------|----------|
| < 100 | **INSUFFICIENT** | Only for quick unit tests of logic, not statistical claims |
| 100-500 | **MARGINAL** | Basic sanity checks, not rigorous validation |
| 1,000+ | **ADEQUATE** | Standard statistical tests, distribution analysis |
| 10,000 | **COMPREHENSIVE** | Full validation, stress tests, rare event detection |

**Bad Example: Insufficient Sample**

```python
# BAD - 50 digits is statistically meaningless
def model(self):
    digits = get_pi_base8(50)  # TOO FEW!
    # ... claims about "uniform distribution" with n=50
```

**Good Example: Adequate Sample**

```python
# GOOD - 1000+ digits for statistical validity
def model(self):
    digits = get_pi_base8(1000)  # Adequate for distribution tests
    # Or for comprehensive validation:
    digits = get_pi_base8(5000)  # Even better for ergodicity claims
```

**Audit Flag**: If a test uses fewer than 100 pi digits and makes statistical claims, flag it for improvement.

---

## Function Extraction Opportunities (Audit Consideration)

During an audit, **actively look for opportunities to extract reusable functions**. A well-designed function can benefit many future tests. This is one of the highest-value improvements you can make.

### The Function Extraction Question

Ask yourself:

> "Is there a calculation here that other tests might need? Could this become a building block?"

Examples of extraction opportunities:

| In-Test Calculation | Potential Reusable Function |
|--------------------|-----------------------------|
| Computing binding energy from mass number | `fn_get_binding_energy(mass_number)` |
| Calculating field radius from element properties | `fn_get_element_field_radius(symbol)` |
| Determining tetrahedron from vertex | `fn_get_tetrahedron(vertex)` |
| Computing closure frequency | `fn_calc_closure_frequency()` |

### The @Fn Decorator Pattern

When extracting a function, follow the pattern in `gravity_field_model/examples/example_power_output.py`:

```python
# NAMING CONVENTION (Command Query Pattern):
#
#   fn_get_<what>(<params>)   - Query: returns data, no side effects
#   fn_set_<what>(<params>)   - Command: modifies state
#   fn_calc_<what>(<params>)  - Query: returns computed value
#
# Examples:
#   fn_get_power_output_of_atom(mass_number)
#   fn_get_element_field_radius(element_symbol)
#   fn_calc_binding_energy(protons, neutrons)

@Fn(
    equation="P(A) = BE(A) * (c / lambda_C)",
    inputs={"mass_number": "int: Mass number A (nucleon count)"},
    outputs={"watts": "float: Power output per gravity field"},
    description=(
        "Query: Returns power output per gravity field from binding energy. "
        "Power = Binding Energy x Field Closure Frequency. "
        "Peaks at Fe-56 where BE/nucleon is maximum (8.79 MeV)."
    ),
)
def fn_get_power_output_per_field(mass_number: int) -> float:
    """
    Query: Get power output per gravity field for a given mass number.
    
    This function is automatically registered when the module is imported.
    Other tests can depend on it using: power = Depends(fn_get_power_output_per_field)
    
    Args:
        mass_number: Mass number A (number of nucleons / gravity fields)
    
    Returns:
        Power in watts per gravity field
    """
    be_mev = get_binding_energy(mass_number)
    be_joules = be_mev * MEV_TO_JOULES
    return be_joules * F_CLOSURE
```

### Function Definition Checklist

Before defining a new @Fn function:

- [ ] **Name follows convention**: `fn_get_*`, `fn_set_*`, or `fn_calc_*`
- [ ] **Equation documented**: Clear mathematical relationship
- [ ] **Inputs documented**: Each parameter with type and description
- [ ] **Outputs documented**: Return type and units
- [ ] **Description explains purpose**: What does this function answer?
- [ ] **Docstring complete**: Args, Returns, and usage example
- [ ] **Constants imported**: No hardcoded values, use `/common/` modules
- [ ] **Testable in isolation**: Function works without test context

### How Tests Use Extracted Functions

Once extracted, other tests can depend on the function:

```python
class StellarFusionChain(Test):
    """Uses fn_get_power_output_per_field for stellar analysis."""
    
    # Declare dependency on the validated function
    get_power = Depends(fn_get_power_output_per_field)
    
    def model(self):
        # Use the injected function
        he4 = self.get_power(4)
        fe56 = self.get_power(56)
        return (
            Model()
            .add("He-4 power (W)", he4)
            .add("Fe-56 power (W)", fe56)
            .add("Fe is peak", 1.0 if fe56 > he4 else 0.0)
        )
```

### Audit Notes for Function Extraction

When you identify an extraction opportunity, note it in `audit_notes`:

```python
audit_notes = (
    "... existing notes ... "
    "FUNCTION OPPORTUNITY: The vertex-to-tetrahedron lookup is repeated in 5 tests. "
    "Should extract to fn_get_tetrahedron(vertex) in geometry_constants.py. "
    "Benefits: Single source of truth, testable in isolation, reusable across modules."
)
```

**Reference**: See `gravity_field_model/examples/example_power_output.py` for the complete pattern including Critical test validation and Standard test usage.

---

## Audience Accessibility (Pedagogical Depth)

Tests should be readable by anyone from **undergraduate to senior PhD**, not just the original author. This means explaining **why** we use specific constants, formulas, and approaches.

### Audience Accessibility Scoring (15 points)

| Score | Description |
|-------|-------------|
| **15** | An undergraduate can follow the logic. A PhD learns something new. Constants and choices are explained with physical motivation. |
| **12** | Clear explanation, but some assumed knowledge. Most readers can follow. |
| **9** | Technically correct but assumes significant background. Graduate level. |
| **6** | Expert-only: requires deep domain knowledge to understand. |
| **3** | Opaque: even experts struggle to understand the intent. |
| **0** | No explanation provided, pure code with no context. |

### The Accessibility Test

Ask yourself: Could a bright undergraduate taking their first quantum mechanics course understand:

1. **Why this constant?** "We use alpha because it governs electromagnetic coupling strength"
2. **Why this formula?** "The Compton wavelength appears because it sets the quantum scale for the electron"
3. **Why this test?** "We check this invariant because if it fails, our entire state machine is broken"

### Bad Example: Unexplained Magic Numbers

```python
class AlphaFromOrbits(Test):
    """137 orbits corresponds to 1/alpha."""  # What? Why? How?
    
    def model(self):
        orbits_per_electron = 137  # Where does this come from?
        derived_alpha = 1 / orbits_per_electron  # Why divide by orbits?
        return Model().add("Derived alpha", derived_alpha)
```

### Good Example: Explained Reasoning

```python
class AlphaFromOrbits(Test):
    """
    The fine structure constant alpha governs the strength of electromagnetic
    interactions. It appears in virtually every QED calculation. The fact that
    1/alpha is approximately 137 has puzzled physicists for a century.
    
    This test documents a correspondence: if we count 137 orbits in our Field
    Closure model, we get a value that matches alpha to high precision. This
    may be coincidence or may hint at deeper structure.
    """
    
    def derivation(self):
        return (
            Derivation()
            .step("CONTEXT: The fine structure constant alpha = e^2/(4*pi*epsilon_0*hbar*c) "
                  "is dimensionless and fundamental to QED.")
            .step("OBSERVATION: 1/alpha is approximately 137, a 'magic number' in physics.")
            .step("MODEL CLAIM: The Field Closure model predicts 137 orbits per electron.")
            .step("DERIVATION: derived_alpha = 1/137 = 0.00730")
            .step("COMPARISON: CODATA alpha = 0.00729735 (agreement within 0.03%)")
            .conclude("The orbit count produces alpha. Coincidence or insight remains open.")
        )
```

### The Feynman Accessibility Hierarchy

When explaining a concept, build up through these levels:

| Level | Audience | Approach | Example |
|-------|----------|----------|---------|
| 1 | High school | Everyday analogy | "Like an odometer that only shows the last digit" |
| 2 | Undergraduate | Physical intuition | "The vertex cycles because we take mod 8, wrapping around" |
| 3 | Graduate | Mathematical structure | "The state machine is deterministic with 8-fold periodicity" |
| 4 | Expert | Deep implications | "This connects to the BBP formula's base-16/8 structure" |

A great test touches all four levels, starting from analogy and building to implication.

---

## Test Group Header Quality (Documentation)

Every test file begins with a module-level docstring that should explain:

1. **What this test group validates** (the goal)
2. **How the tests achieve full coverage** (completeness)
3. **What might be missing or future work** (limitations)

### Test Group Header Scoring (10 points)

| Score | Description |
|-------|-------------|
| **10** | Clear goal statement, explains coverage strategy, acknowledges limitations, tests achieve stated goals. |
| **8** | Good overview, coverage mostly explained, minor gaps in documentation. |
| **6** | Basic description present but incomplete coverage explanation. |
| **4** | Minimal header, unclear what test group validates or why. |
| **2** | Header exists but is misleading or contradicted by tests. |
| **0** | No header or completely absent documentation. |

### Bad Example: Minimal Header

```python
"""
Field Closure System Validation
===============================

Tests for the field closure system.
"""
```

This tells us nothing about what aspects are tested, what's covered, or what's missing.

### Good Example: Comprehensive Header

```python
"""
Field Closure System Validation
===============================

This module provides comprehensive validation of the Field Closure state
machine treating pi-driven traversal as a deterministic system.

VALIDATION CATEGORIES:

1. State Machine Integrity (4 tests)
   - Vertex = cumsum mod 8 (invariant)
   - Orbit = cumsum // 8 (invariant)
   - Tetrahedron assignment by parity
   - Determinism: same input produces same output
   
2. Closure Event Detection (2 tests)
   - Cumsum monotonicity (non-decreasing)
   - Increment = digit (accounting check)

3. Statistical Properties (3 tests)
   - Digit distribution (pi normality)
   - Vertex ergodicity (uniform visits)
   - Tetrahedron balance (50/50 split)

4. Cross-Validation Correspondences (3 tests)
   - Alpha from 137 orbits
   - Spin 1/2 from face ratio
   - k=4 throughout topology

COVERAGE ASSESSMENT:
- Core invariants: COMPLETE (4/4 critical properties)
- Statistical properties: COMPLETE (3 key distributions)
- Cross-validation: PARTIAL (3 correspondences documented, more exist)

KNOWN LIMITATIONS:
- Does not test edge cases beyond 10,000 digits
- Ergodicity tested over 100 steps (larger samples in stress tests)
- Alpha correspondence noted but not derived from first principles

DEPENDENCIES:
- Requires gravity_field_model.common.pi_data for verified pi digits
- Requires gravity_field_model.common.geometry_constants for TET_A, TET_B
- Requires gravity_field_model.common.constants_codata for ALPHA
"""
```

### Header Checklist

- [ ] **Goal**: What physical or mathematical property does this test group validate?
- [ ] **Structure**: How are tests organized into categories?
- [ ] **Coverage**: What aspects are fully covered vs partially covered?
- [ ] **Limitations**: What is NOT tested, and why?
- [ ] **Dependencies**: What common modules or external data are required?
- [ ] **Alignment**: Do the actual tests match the stated coverage?

---

## Function and Test Architecture

Tests don't exist in isolation. They validate **reusable functions** that form the building blocks of the model. Understanding this architecture is essential.

### Reference Example

See `gravity_field_model/examples/example_power_output.py` for the complete pattern.

```
python -m gravity_field_model.examples.example_power_output
```

### The Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: CONSTANTS (from constants_codata.py)              │
│  ─────────────────────────────────────────────────────────  │
│  C, HBAR, ALPHA, LAMBDA_COMPTON, EV, etc.                   │
│  Single source of truth. CODATA-traceable. Never hardcode.  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: FUNCTIONS (decorated with @Fn)                    │
│  ─────────────────────────────────────────────────────────  │
│  @Fn(equation="...", inputs={...}, outputs={...})           │
│  def fn_get_power_output(mass_number: int) -> float:        │
│      ...                                                    │
│  Reusable, documented, registered for dependency injection. │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: TESTS (inherit from Test, use Depends())          │
│  ─────────────────────────────────────────────────────────  │
│  class PowerOutputValidation(Test):                         │
│      get_power = Depends(fn_get_power_output)               │
│      ...                                                    │
│  Validate functions. Depend on them. Never duplicate logic. │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Constants

**Never define constants in test files.** Import from `constants_codata.py`:

```python
# BAD - hardcoded magic numbers
MEV_TO_JOULES = 1.60218e-13  # Where did this come from?

# GOOD - traceable to CODATA
from gravity_field_model.common.constants_codata import EV
MEV_TO_JOULES = EV * 1e6  # Derived from CODATA value
```

### Layer 2: Functions with @Fn Decorator

Functions that compute model predictions should be decorated with `@Fn`:

```python
@Fn(
    equation="P(A) = BE(A) * (c / lambda_C)",
    inputs={"mass_number": "int: Mass number A"},
    outputs={"watts": "float: Power output per field"},
    description="Returns power output from binding energy.",
)
def fn_get_power_output_per_field(mass_number: int) -> float:
    """
    Naming convention: fn_get_<what>() for queries, fn_calc_<what>() for computations.
    """
    be_mev = get_binding_energy(mass_number)
    be_joules = be_mev * MEV_TO_JOULES
    return be_joules * F_CLOSURE
```

**Why @Fn matters:**
- Documents the equation, inputs, and outputs
- Registers the function for dependency injection
- Creates a reusable building block other tests can depend on

### Layer 3: Tests with Depends()

Tests **inject** functions using `Depends()`, then validate them:

```python
class PowerOutputValidation(Test):
    """
    CRITICAL test: validates the core power function.
    """
    name = "Power Output per Gravity Field"
    question = (
        "Why does iron have the highest binding energy, and can we compute "
        "the power output at each stage of stellar fusion?"
    )
    level = Critical  # Foundational: must pass before other tests run
    
    # INJECT the function we're testing
    get_power = Depends(fn_get_power_output_per_field)
    
    def model(self):
        # USE the injected function
        return (
            Model()
            .add("He-4 power (W)", self.get_power(4))
            .add("Fe-56 power (W)", self.get_power(56))
            .add("Fe is peak", 1.0 if self.get_power(56) > self.get_power(4) else 0.0)
        )
    
    commentary = (
        "Iron-56 has the highest power output because it has the maximum "
        "binding energy per nucleon. This explains why stellar fusion stops "
        "at iron: beyond Fe-56, fusion consumes energy rather than releasing it."
    )
```

### Test Levels and Dependencies

```
CRITICAL Tests
  │  Validate core functions (e.g., fn_get_power_output)
  │  Must pass before anything else makes sense
  │
  ▼
STANDARD Tests
  │  Use validated functions via Depends()
  │  Explore consequences and applications
  │
  ▼
EXPLORATORY Tests
     Push boundaries, test edge cases
     May fail without indicating a fundamental problem
```

### The Depends() Pattern

**Why Depends() instead of direct calls?**

```python
# BAD - tight coupling, no validation guarantee
class StellarFusionChain(Test):
    def model(self):
        power = fn_get_power_output_per_field(56)  # Direct call
        
# GOOD - dependency injection, validated function
class StellarFusionChain(Test):
    get_power = Depends(fn_get_power_output_per_field)  # Injected
    
    def model(self):
        power = self.get_power(56)  # Uses validated function
```

Benefits of `Depends()`:
1. **Explicit dependencies**: Clear what each test relies on
2. **Validation chain**: CRITICAL tests validate functions before STANDARD tests use them
3. **Testability**: Functions can be mocked or replaced
4. **Documentation**: The dependency graph is visible

### Complete Example Structure

```python
"""
Module: Power Output Calculations
"""

# LAYER 1: Import constants (never define here)
from gravity_field_model.framework import *
from gravity_field_model.common.constants_codata import C, LAMBDA_COMPTON, EV


# LAYER 2: Define reusable functions
@Fn(equation="P = BE * f", inputs={...}, outputs={...}, description="...")
def fn_get_power_output(mass_number: int) -> float:
    ...


# LAYER 3: Write tests that validate and use functions
class PowerValidation(Test):
    """CRITICAL: Validates fn_get_power_output"""
    level = Critical
    get_power = Depends(fn_get_power_output)
    ...


class StellarFusion(Test):
    """STANDARD: Uses validated function for analysis"""
    level = Standard
    get_power = Depends(fn_get_power_output)
    ...


# Test runner
ALL_TESTS = [PowerValidation, StellarFusion]

def run_all():
    return run_tests(title="Power Output", summary="...", test_classes=ALL_TESTS)

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_all() else 1)
```

---

## Anti-Pattern: The Data Dump

### Bad Example (Before)

```
REDUNDANT READ DISTRIBUTION
STANDARD
PASS

Are redundant vertex reads distributed evenly across faces?

Model
  Total redundant reads                         29979
  TIME face redundant                            7477
  SPATIAL face redundant                        22502
  FACE_A1 redundant                              3731
  FACE_A2 redundant                              3710
  FACE_A4 redundant                              3657
  FACE_A7 redundant                              3656
  FACE_B0 redundant                              3821
  FACE_B3 redundant                              3789
  FACE_B5 redundant                              3820
  FACE_B6 redundant                              3795
```

**Problems:**
1. **No context**: What is a "redundant read"? Why should I care?
2. **Raw numbers without meaning**: Is 3731 good or bad? How does it compare?
3. **No clear verdict**: The test "passes" but I don't know what criterion was met
4. **Internal jargon**: FACE_A1, TIME/SPATIAL mean nothing to the reader
5. **No statistical summary**: 8 numbers when one would suffice

---

## Pattern: The Clear Verdict

### Good Example (After)

```
FACE TRAVERSAL BIAS CHECK
STANDARD
PASS

Does the pi-driven traversal favor certain faces, or does it 
distribute work evenly across the geometry?

Derivation
  WHAT: After a face 'completes' (all 3 vertices visited), further 
  hits to that face are 'redundant' - extra work on an already-done 
  face. 
  
  WHY: An unbiased traversal should spread redundant hits evenly. 
  Bias would show as some faces getting hit much more than others. 
  
  HOW: Count redundant hits per face. Compute coefficient of 
  variation (CV = std_dev / mean). Low CV means even distribution.
  
  THRESHOLD: CV < 15% indicates no significant geometric bias.

Model
  Faces analyzed                                    8
  Mean hits per face                             3747
  Spread (max-min)/mean %                         4.4
  Coefficient of variation                      0.017
  Bias detected (CV > 0.15)                         0

Commentary
  The traversal distributes work evenly across all 8 faces. 
  CV of 1.7% confirms no geometric bias.
```

**Improvements:**
1. **Self-explanatory title**: "Bias Check" tells you what we're testing
2. **Plain English derivation**: WHAT/WHY/HOW structure
3. **Statistical summary**: One number (CV) captures the essence
4. **Clear threshold**: CV < 15% is the pass criterion
5. **Binary verdict**: "Bias detected" is 0 or 1, not a wall of numbers
6. **Meaningful commentary**: States the conclusion in plain English

---

## The Test Quality Checklist

Before finalizing any test, verify:

### Structure
- [ ] **Title** clearly states what's being tested (not internal code names)
- [ ] **Question** can be answered with yes/no or a single value
- [ ] **Derivation** explains WHAT, WHY, and HOW
- [ ] **Model** outputs are summarized, not raw dumps

### Clarity
- [ ] A non-expert could understand the conclusion
- [ ] Technical terms are defined on first use
- [ ] Numbers have context (what's good? what's bad?)
- [ ] Pass/fail criterion is explicitly stated

### Value
- [ ] The test answers a meaningful question
- [ ] Failure would indicate a real problem
- [ ] The result is actionable (you'd know what to fix)

### Output
- [ ] Summary statistics over raw data (mean, CV, %)
- [ ] Binary verdicts where possible (0/1, yes/no)
- [ ] Observations match what the model actually produces
- [ ] Commentary explains the result, not just restates numbers

---

## Transforming Bad Tests: A Recipe

### Step 1: Identify the Core Question
Look at your test. Strip away all the numbers. What question are you actually trying to answer?

**Bad**: "What are the redundant read counts per face?"
**Good**: "Is the traversal biased toward certain faces?"

### Step 2: Define the Success Criterion
How would you know if the answer is "yes" or "no"? Make it concrete.

**Bad**: (no criterion - just dump numbers)
**Good**: "CV < 15% means no significant bias"

### Step 3: Choose Summary Statistics
Replace N values with 1-3 summary statistics that capture the essence.

| Instead of... | Use... |
|---------------|--------|
| 8 individual counts | Mean, min, max, spread % |
| Raw differences | Percent error |
| Lists of values | Coefficient of variation |
| Multiple boolean flags | Single "all passed" flag |

### Step 4: Add Context to Every Number
For every number in your output, the reader should know:
- What does this number represent?
- Is this value good or bad?
- What would make it fail?

### Step 5: Write the Commentary First
Write the commentary BEFORE you write the test code. If you can't explain what a passing test means, you don't understand what you're testing.

---

## Output Patterns

### Pattern: Binary Verdict
When testing a condition, output a 0/1 flag.

```python
def model(self):
    # ... compute cv ...
    return (
        Model()
        .add("Coefficient of variation", round(cv, 4))
        .add("Bias detected (CV > 0.15)", 0.0 if cv < 0.15 else 1.0)
    )

def observations(self):
    return Observed().add("Bias detected (CV > 0.15)", 0.0)
```

### Pattern: Percentage Match
When comparing to a reference, show percent error.

```python
def model(self):
    calculated = compute_value()
    expected = 137.036
    error_pct = abs(calculated - expected) / expected * 100
    return (
        Model()
        .add("Calculated", calculated)
        .add("Expected", expected)
        .add("Error %", round(error_pct, 2))
    )
```

### Pattern: Statistical Summary
When analyzing distributions, summarize don't enumerate.

```python
def model(self):
    values = get_all_values()
    return (
        Model()
        .add("Count", len(values))
        .add("Mean", round(statistics.mean(values), 2))
        .add("Std Dev", round(statistics.stdev(values), 2))
        .add("CV %", round(statistics.stdev(values) / statistics.mean(values) * 100, 1))
        .add("Min", min(values))
        .add("Max", max(values))
    )
```

### Pattern: Threshold Check
When a value must be within bounds, state the bounds.

```python
def model(self):
    value = measure_something()
    in_range = lower_bound <= value <= upper_bound
    return (
        Model()
        .add("Measured value", value)
        .add("Lower bound", lower_bound)
        .add("Upper bound", upper_bound)
        .add("Within tolerance", 1.0 if in_range else 0.0)
    )
```

---

## The Feynman Test

Richard Feynman said: "If you can't explain it simply, you don't understand it well enough."

Apply this to your tests:

1. **Read your test output aloud** to someone unfamiliar with the code
2. **Ask them**: "What did we just learn?"
3. **If they can't answer**, your test needs rewriting

A test that only the author understands is a test that will confuse everyone else, including the author in 6 months.

---

## Quick Reference: Transform Table

| Bad Pattern | Good Pattern |
|-------------|--------------|
| "What are the values?" | "Is there hidden bias in the traversal?" |
| Dump all 8 face counts | Show mean, spread %, CV |
| Internal names (FACE_A1) | Descriptive names or summaries |
| No pass/fail criterion | Explicit threshold (CV < 0.15) |
| "See data above" | Binary verdict (0 = pass, 1 = fail) |
| Technical jargon | Plain English + analogies |
| Numbers without context | Numbers with comparison/bounds |
| Math-first derivation | Intuition-first, then math |
| Commentary restates numbers | Commentary delivers insight |

---

## The Feynman Checklist (8 Criteria)

Before finalizing any test, verify all eight quality criteria:

### 1. Question (15 pts) - The Hook
- [ ] Does it establish a physical mystery or curiosity?
- [ ] Would someone want to know the answer before seeing the data?
- [ ] Does it avoid jargon and internal code names?
- [ ] Does it hint at what failure would mean?

### 2. Derivation (15 pts) - Building Intuition
- [ ] Does it explain the SITUATION before any math?
- [ ] Does it establish the TENSION (what's the puzzle)?
- [ ] Does it provide an ANALOGY from everyday experience?
- [ ] Does the math feel like a RELIEF (a tool the reader wants)?
- [ ] Is the CRITERION explicitly stated?

### 3. Commentary (15 pts) - The Insight
- [ ] Does it ANSWER the original question in plain English?
- [ ] Does it explain SIGNIFICANCE (why this matters)?
- [ ] Does it use an ANALOGY or everyday language?
- [ ] Does it state the IMPLICATION (what we can now trust)?

### 4. Model Output (10 pts) - The Results
- [ ] Summary statistics over raw data dumps?
- [ ] Numbers have context (good/bad, bounds, comparison)?
- [ ] Binary verdict where possible (0/1)?

### 5. Observation Quality (10 pts) - Ground Truth
- [ ] Are expected values traceable to authoritative sources?
- [ ] Is the source documented (CODATA, paper, derivation)?
- [ ] Are tolerances appropriate for the measurement precision?
- [ ] Do observations match what the model actually produces?

### 6. Constants Compliance (10 pts) - Engineering Standards
- [ ] All physical constants imported from `constants_codata.py`?
- [ ] Pi digits imported from `pi_data.py`, never hardcoded?
- [ ] Geometry constants imported from `geometry_constants.py`?
- [ ] No magic numbers without explicit derivation?
- [ ] Derived constants documented with their formula?
- [ ] **Sample size adequate?** (1000+ pi digits for statistical claims, not 50)

### 7. Audience Accessibility (15 pts) - Pedagogical Depth
- [ ] Could a bright undergraduate follow the logic?
- [ ] Does it explain WHY we use these specific constants?
- [ ] Does it explain WHY this formula or approach?
- [ ] Does it build from everyday analogy to technical detail?
- [ ] Would a PhD researcher learn something new?

### 8. Test Group Header (10 pts) - Module Documentation
- [ ] Does the module docstring state the validation goal?
- [ ] Does it list what categories of tests are included?
- [ ] Does it explain what coverage is achieved?
- [ ] Does it acknowledge limitations or future work?
- [ ] Do the actual tests match the stated coverage?

### Audit Bonus Considerations (Not Scored, But Valuable)
- [ ] **Function extraction opportunity?** Is there a reusable calculation to extract with `@Fn`?
- [ ] **Sample size adequate?** Are pi digits >= 1000 for statistical claims?
- [ ] **Cross-test patterns?** Is the same logic duplicated across multiple tests?

---

## Summary: The Feynman Way

**Why before What. Intuition before Abstraction. Insight before Numbers.**

Every test should follow this arc:

```
1. QUESTION: Hook the reader's curiosity (the mystery)           [15 pts]
2. DERIVATION: Build the mental scaffolding (intuition first)    [15 pts]
3. COMMENTARY: Deliver the "aha" moment (the insight)            [15 pts]
4. MODEL OUTPUT: Show summarized data (reader is ready for it)   [10 pts]
5. OBSERVATIONS: Ground truth from traceable sources             [10 pts]
6. CONSTANTS: Import from /common/, never hardcode               [10 pts]
7. ACCESSIBILITY: Undergrad to PhD can follow                    [15 pts]
8. HEADER: Module documents goals and coverage                   [10 pts]
                                                          TOTAL: [100 pts]
```

The reader should finish the test thinking:

> "I understand why we measured this, what the result means, 
> and why it matters. I could explain this to someone else."

**The Feynman Test**: Read your test output to someone unfamiliar with the code. Ask them: "What did we just learn, and why does it matter?" 

If they can't answer, rewrite until they can.

**The Engineering Test**: Show the code to a colleague. Ask: "Where do these numbers come from?" If they have to search the file for hardcoded values instead of seeing imports from `/common/`, the test fails engineering standards.

---

## Recording Audit Findings

When auditing tests, **always record your findings** using the built-in properties. This ensures audit work is not lost and creates a backlog of improvements.

### The `audit_score` Property

Score each test from 0-100 based on eight quality criteria:

| Criterion | Points | What to Evaluate |
|-----------|--------|------------------|
| **Question** | 0-15 | Does it hook curiosity with "why" before "what"? |
| **Derivation** | 0-15 | Does it build intuition before math? Use analogies? |
| **Commentary** | 0-15 | Does it deliver insight? Not just restate numbers? |
| **Model Output** | 0-10 | Does it summarize with statistics? No data dumps? |
| **Observation Quality** | 0-10 | Are expected values traceable? Documented sources? |
| **Constants Compliance** | 0-10 | Does it import from `/common/`? No hardcoded values? |
| **Audience Accessibility** | 0-15 | Could an undergrad follow? Does it explain WHY? |
| **Test Group Header** | 0-10 | Does the module docstring explain goals and coverage? |

**Scoring Quick Reference:**

| Criterion | Excellent | Good | Needs Work | Poor |
|-----------|-----------|------|------------|------|
| Question (15) | 14-15: Mystery hook | 11-13: Clear but flat | 7-10: Technical only | 0-6: Just "what is X" |
| Derivation (15) | 14-15: Intuition-first | 11-13: Clear steps | 7-10: Math-first | 0-6: No explanation |
| Commentary (15) | 14-15: Delivers insight | 11-13: Explains result | 7-10: Restates numbers | 0-6: Missing/empty |
| Model Output (10) | 9-10: Summary stats | 7-8: Mostly clean | 4-6: Some raw dumps | 0-3: All raw data |
| Observations (10) | 9-10: CODATA traceable | 7-8: Documented | 4-6: Undocumented | 0-3: Arbitrary values |
| Constants (10) | 9-10: All imported | 7-8: Mostly imported | 4-6: Mixed | 0-3: All hardcoded |
| Accessibility (15) | 14-15: All levels | 11-13: Graduate OK | 7-10: Expert only | 0-6: Opaque |
| Header (10) | 9-10: Full coverage | 7-8: Good overview | 4-6: Minimal | 0-3: Missing |

**Score interpretation:**

| Score | Assessment | Action |
|-------|------------|--------|
| 90-100 | Exemplary | No changes needed |
| 75-89 | Good | Minor improvements optional |
| 50-74 | Needs Work | Should be improved |
| 25-49 | Poor | Requires significant rework |
| 0-24 | Failing | Mark as `level = Ignore` |

### The `audit_notes` Property

Record specific findings and recommendations. Be concrete about what needs to change.

### Example: Recording an Audit

```python
class RedundantReadDistribution(Test):
    name = "Redundant Read Distribution"
    level = Standard
    
    # AUDIT FINDINGS (not shown in test output)
    audit_score = 42
    audit_notes = (
        "Question: 8/15 - Asks 'what are the counts' not 'why do we care'. "
        "Derivation: 7/15 - No intuition, just lists steps. "
        "Commentary: 7/15 - Says 'reveals biases' but doesn't explain what that means. "
        "Model: 4/10 - Dumps 8 raw face counts without summary. "
        "Observations: 5/10 - Expected values undocumented. "
        "Constants: 8/10 - Most imported, but K=4 hardcoded. "
        "Accessibility: 3/15 - Expert-only, no analogies or physical motivation. "
        "Header: N/A (scored at module level). "
        "SAMPLE SIZE: Uses only 50 pi digits - INSUFFICIENT for distribution claims. "
        "RECOMMENDATION: Reframe as bias detection test. Replace raw counts with CV. "
        "Add analogy (loaded die). Explain what bias would mean physically. "
        "Import K from geometry_constants.py. Use 1000+ pi digits."
    )
```

### Example: High-Quality Audit

```python
class VertexEqualsCumsumMod8(Test):
    name = "Vertex = Cumsum mod 8"
    level = Critical
    
    audit_score = 94
    audit_notes = (
        "Question: 14/15 - Excellent 'how do we know' with simple rule explanation. "
        "Derivation: 14/15 - Clear modular arithmetic logic with context. "
        "Commentary: 14/15 - Great odometer analogy for mod operation. "
        "Model: 10/10 - Good violations count with states checked. "
        "Observations: 9/10 - Binary check well-defined. "
        "Constants: 10/10 - All geometry from common modules. "
        "Accessibility: 14/15 - Undergraduate can follow, odometer analogy excellent. "
        "Header: 9/10 (module header comprehensive). "
        "SAMPLE SIZE: Uses 100 digits, adequate for invariant checking (not statistical). "
        "TO IMPROVE: Minor polish only, perhaps add 'what would failure mean' to derivation."
    )
```

### Example: Audit with Function Extraction Opportunity

```python
class AlphaFromOrbits(Test):
    name = "Alpha from Orbits"
    level = Standard
    
    audit_score = 78
    audit_notes = (
        "Question: 14/15 - Excellent 'why does 137 keep appearing' mystery hook. "
        "Derivation: 12/15 - Clear but could explain more about alpha. "
        "Commentary: 14/15 - Great 'coincidence or insight' framing. "
        "Model: 9/10 - Good alpha comparison. "
        "Observations: 8/10 - Alpha value traceable but could cite CODATA explicitly. "
        "Constants: 6/10 - Alpha hardcoded as 1/137.036, should import from constants_codata. "
        "Accessibility: 12/15 - Graduate level, could add more intuition. "
        "Header: 3/10 - Module header minimal. "
        "FUNCTION OPPORTUNITY: The orbit counting logic (build_state_sequence) is used "
        "in 5+ tests. Should extract to fn_count_orbits(n_digits) in a traversal module. "
        "This would provide: single source of truth, testable in isolation, Depends() pattern. "
        "See examples/example_power_output.py for the @Fn decorator pattern."
    )
```

### Running an Audit

When auditing a test file:

1. **Read each test** through the Feynman lens
2. **Score each of the 8 criteria** (see point allocations above)
3. **Check sample sizes**: Are pi digits >= 1000 for statistical claims?
4. **Look for function extraction opportunities**: Is there reusable logic to extract?
5. **Add `audit_score`** to the test class (sum of all criteria, 0-100)
6. **Add `audit_notes`** with specific per-criterion findings
7. **Mark `level = Ignore`** if score < 25

**Bonus value items** (not scored but documented):
- Note any `SAMPLE SIZE` issues (using 50 digits when 1000 needed)
- Note any `FUNCTION OPPORTUNITY` for extraction with `@Fn` decorator
- Reference `examples/example_power_output.py` for the function pattern

This creates a persistent record of quality issues and a prioritized backlog for improvement.

### Querying Audit Status

To find tests needing attention:

```python
# Tests with low scores
low_score_tests = [t for t in ALL_TESTS if getattr(t, 'audit_score', 100) < 75]

# Tests not yet audited
unaudited_tests = [t for t in ALL_TESTS if getattr(t, 'audit_score', None) is None]
```

---

## Closing Thought

Feynman said: "The first principle is that you must not fool yourself, and you are the easiest person to fool."

A test that only the author understands is a test that fools you into thinking you've communicated something. The true test of a test is whether it teaches, not whether it passes.

A test with hardcoded constants fools you into thinking the values are verified. A test without source documentation fools you into thinking the expectations are correct. A test with no explanatory header fools you into thinking the coverage is complete.

Write tests that **teach**. Use constants that are **traceable**. Build explanations that span from **undergraduate to PhD**. Document coverage that is **honest about gaps**.

The pass/fail is just a bonus. The true measure is whether a bright undergraduate could read your test and walk away understanding both the physics AND the engineering.
