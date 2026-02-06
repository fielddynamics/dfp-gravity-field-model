# Scientific Reasoning Module

**Module Type:** STATELESS (utility library, no folder to guard)

**Purpose:** Provides thinking protocols for scientific exploration. This module defines the rules for brainstorming, error analysis, equation derivation, and reasoning chain documentation.

**Called by:** START_RESEARCH_MODULE (Stage 6: Scientific Reasoning Extension)

---

## The Pioneering Question

When you have a working test or validated concept, ask:

> **"What else in physics should this connect to, and why would that connection exist?"**

This module transforms passive test writing into active scientific discovery.

---

## Module Exports (Thresholds)

This module is the **single source of truth** for these thresholds:

| Threshold | Value | Meaning |
|-----------|-------|---------|
| `SELECTION_THRESHOLD_IMMEDIATE` | 80 | Brainstorm idea score >= 80: write test now |
| `SELECTION_THRESHOLD_QUEUE` | 60 | Score >= 60: add to backlog |
| `SELECTION_THRESHOLD_NOTE` | 40 | Score >= 40: document for later |
| `ERROR_SIGNIFICANCE_THRESHOLD` | 5% | Error >= 5% triggers bridge protocol |
| `ERROR_PARTIAL_MATCH_THRESHOLD` | 30% | Error >= 30% is no match |

---

## See Also

- `MODULE_ARCHITECTURE.md` for how modules wire together
- `START_RESEARCH_MODULE.md` for the orchestrating pipeline
- `FUNCTION_REGISTRY_GUIDE.md` for function graduation

---

## Part 1: The Chain of Reasoning

### 1.1 The Feynman Protocol: WHY Before WHAT

Before exploring what might connect, understand WHY it would connect.

**The Three WHY Questions:**

1. **WHY does this phenomenon exist?**
   - What is the underlying mechanism?
   - What geometric/physical principle drives it?

2. **WHY would it connect to something else?**
   - What shared structure might exist?
   - What conservation law or symmetry links them?

3. **WHY would we expect a specific relationship?**
   - What scaling law applies?
   - What dimensional analysis suggests?

**Example: Power Output to Valence Horizon**

```
PHENOMENON: Stellar power output P = (something) * G * M^2 / R

WHY does this exist?
  -> Gravitational potential energy converts to radiation
  -> Field compression creates energy gradient
  -> Bidirectional vortex structure channels energy outward

WHY would it connect to valence horizon?
  -> Both involve field boundary conditions
  -> Both relate to where "inside" meets "outside"
  -> Power output defines energy available at boundary
  -> Valence horizon defines where that boundary sits

WHY would we expect a specific relationship?
  -> If P ~ 1/R^n, and valence horizon r_v ~ R^m
  -> Then P ~ r_v^(-n/m)
  -> The exponents should relate to d or k
```

### 1.2 The Mapping Principle

Every physical quantity can potentially map to another through:

| Connection Type | Example | What to Look For |
|-----------------|---------|------------------|
| **Dimensional** | Energy ~ Mass × Length² / Time² | Same dimensions, different contexts |
| **Geometric** | Surface area ~ R², Volume ~ R³ | Same geometric scaling |
| **Topological** | Faces = 8, Vertices = 6 | Same counting principle |
| **Ratio** | α = 1/137, other dimensionless ratios | Same ratio in different domains |
| **Exponent** | 3/5, 5/3, 21 | Same exponent pattern |

---

## Part 2: The Brainstorming Protocol

### 2.1 The Ten Mapping Brainstorm

When you have a validated concept, systematically brainstorm 10 potential connections:

```
STARTING CONCEPT: [e.g., Stellar Power Output]
KNOWN RELATIONSHIP: [e.g., P = (32/5) * G^4 * M^5 / (c^5 * R^5)]

BRAINSTORM MAPPINGS:

1. DIMENSIONAL COUSIN
   What else has dimensions of Power?
   -> Hawking radiation power
   -> Gravitational wave luminosity
   -> Electron radiation in magnetic field

2. GEOMETRIC ANALOG
   What else scales as R^(-5)?
   -> Casimir force between plates
   -> Higher multipole radiation
   -> Tidal disruption rate

3. BOUNDARY PHENOMENON
   What else lives at the boundary?
   -> Event horizon
   -> Valence shell radius
   -> Photon sphere

4. RATIO CONNECTION
   What ratios appear in this formula?
   -> 32/5 = 6.4 (check other formulas for 32/5)
   -> M/R ratio (compactness)
   -> c^5/G (Planck power)

5. EXPONENT PATTERN
   What else has exponent 5?
   -> Orbital decay rate (a^(-5))
   -> Stefan-Boltzmann (T^4, close)
   -> Gravitational binding energy

6. INVERSE RELATIONSHIP
   If P increases, what decreases?
   -> Orbital lifetime
   -> Stability margin
   -> Efficiency of energy retention

7. COMPLEMENTARY QUANTITY
   What is the "other half" of this?
   -> Energy absorbed vs emitted
   -> Inward vs outward flux
   -> Linear vs angular momentum

8. SCALE TRANSITION
   Where does this formula break down?
   -> Quantum regime (Planck scale)
   -> Cosmological regime (Hubble scale)
   -> Strong field regime (compact objects)

9. CROSS-DOMAIN ANALOG
   Same pattern in different physics?
   -> Electromagnetic radiation power
   -> Acoustic power emission
   -> Thermal conduction

10. GFD GEOMETRIC CONNECTION
    What GFD structure might explain this?
    -> Face count (8 faces)
    -> Tetrahedral coupling
    -> Field closure cycle
```

### 2.2 Scoring the Brainstorm

Score each brainstormed idea on five criteria (20 points each, 100 total):

| Criterion | What to Evaluate | Score Guide |
|-----------|------------------|-------------|
| **Testability** | Can we write a test for this? | 20: Clear test path, 10: Possible, 0: Untestable |
| **Plausibility** | Does physics suggest this connection? | 20: Strong reason, 10: Speculative, 0: No basis |
| **Novelty** | Has this been explored before? | 20: New territory, 10: Partial, 0: Well-known |
| **Impact** | If true, does it matter? | 20: Paradigm shift, 10: Useful, 0: Trivial |
| **GFD Relevance** | Does it connect to GFD structure? | 20: Direct, 10: Indirect, 0: None |

**Scoring Example:**

```
IDEA: Power output maps to valence horizon size

Testability:   18/20 - Can calculate P and r_v, compare scaling
Plausibility:  15/20 - Both are boundary phenomena, reasonable link
Novelty:       17/20 - Not explored in literature
Impact:        14/20 - Would connect stellar physics to atomic physics
GFD Relevance: 16/20 - Both involve field boundary, closure

TOTAL: 80/100 - HIGH PRIORITY, proceed to test design
```

### 2.3 Selection Threshold

| Score | Action |
|-------|--------|
| 80-100 | **Immediate**: Write test now |
| 60-79 | **Queue**: Add to backlog, write when time permits |
| 40-59 | **Note**: Document idea, revisit if related evidence emerges |
| 0-39 | **Discard**: Not worth pursuing currently |

---

## Part 3: The Error Bridge Protocol

### 3.1 When Results Don't Match

If a test shows significant error between model and observation:

```
OBSERVED ERROR: Model predicts X, observation shows Y
ERROR MAGNITUDE: |X - Y| / Y = Z%

BEFORE asking "how do I fix this", ask:

WHY might this error exist?
```

### 3.2 The Error Source Brainstorm

Generate hypotheses for the error source:

```
ERROR SOURCES (brainstorm 10):

1. MISSING PHYSICS
   What effect did we neglect?
   -> Relativistic corrections
   -> Quantum corrections
   -> Higher-order terms

2. WRONG APPROXIMATION
   What assumption might be invalid?
   -> Spherical symmetry
   -> Steady state
   -> Weak field

3. MEASUREMENT UNCERTAINTY
   Is the observation reliable?
   -> Systematic bias
   -> Statistical noise
   -> Calibration error

4. WRONG REFERENCE
   Are we comparing apples to oranges?
   -> Different definitions
   -> Different conditions
   -> Different epochs

5. SCALE MISMATCH
   Are we in the right regime?
   -> Too small (quantum effects)
   -> Too large (cosmological effects)
   -> Transition zone

6. COUPLING NEGLECTED
   What interactions did we ignore?
   -> Electromagnetic coupling
   -> Thermal coupling
   -> Spin coupling

7. BOUNDARY CONDITION
   Is the boundary defined correctly?
   -> Wrong radius
   -> Wrong surface
   -> Wrong topology

8. DIMENSIONAL FACTOR
   Is there a missing constant?
   -> Factor of 2 (symmetry)
   -> Factor of π (geometry)
   -> Factor of k or d (GFD)

9. TIME DEPENDENCE
   Are we assuming static when dynamic?
   -> Secular evolution
   -> Oscillation
   -> Transient

10. COMPOSITIONAL EFFECT
    Does internal structure matter?
    -> Density gradient
    -> Composition gradient
    -> Phase transition
```

### 3.3 The Bridge Test Protocol

For each plausible error source, design a test to check it:

```
ERROR HYPOTHESIS: Missing relativistic correction

BRIDGE TEST DESIGN:
  Name: RelativisticCorrectionToStellarPower
  Question: "Does adding the relativistic correction term reduce the error?"
  
  Model:
    P_newtonian = (32/5) * G^4 * M^5 / (c^5 * R^5)
    P_relativistic = P_newtonian * (1 + correction_term)
    correction_term = f(GM/Rc^2)  # compactness parameter
  
  Observation:
    Compare P_relativistic to measured power
  
  Success Criterion:
    If error reduces from Z% to <Z/2%, correction is relevant
    If error unchanged, this is not the source
```

### 3.4 The Error Reduction Chain

```
INITIAL ERROR: 15%
                │
                ▼
    ┌───────────────────────────────────────┐
    │  Test 1: Relativistic Correction      │
    │  Result: Error reduced to 12%         │
    │  Conclusion: Partial contribution     │
    └───────────────────────────────────────┘
                │
                ▼
    ┌───────────────────────────────────────┐
    │  Test 2: Density Gradient Effect      │
    │  Result: Error reduced to 8%          │
    │  Conclusion: Significant contribution │
    └───────────────────────────────────────┘
                │
                ▼
    ┌───────────────────────────────────────┐
    │  Test 3: Boundary Definition          │
    │  Result: Error reduced to 3%          │
    │  Conclusion: Major contribution       │
    └───────────────────────────────────────┘
                │
                ▼
    FINAL ERROR: 3% (within tolerance)
    
    LEARNING: The formula requires:
    1. Relativistic correction (~3%)
    2. Density gradient factor (~4%)
    3. Proper boundary at r = 0.95R (~5%)
```

---

## Part 4: The Vortex Mapping Example

### 4.1 Starting Point

```
CONCEPT: Stellar power output from gravitational field compression

KNOWN:
- Power output P exists and is measurable
- GFD proposes bidirectional vortex structure
- Compression inward, radiation outward
- Field origin at center

WHY VORTEX?
- Gravity field packing creates pressure gradient
- Gradient must resolve at boundary
- Resolution creates bidirectional flow
- Flow is vortex-like (angular momentum)
```

### 4.2 The Ten Mappings for Vortex Power

```
1. VALENCE HORIZON SIZE
   WHY: Vortex boundary = where field influence ends
   MAPPING: r_valence ~ (P / P_0)^(1/n) where n relates to d
   TESTABILITY: High (can calculate both)
   SCORE: 82/100

2. ROTATION PERIOD
   WHY: Vortex has angular velocity
   MAPPING: T_rot ~ R^2 / (P/M)
   TESTABILITY: High (measurable for stars)
   SCORE: 78/100

3. MAGNETIC FIELD STRENGTH
   WHY: Rotating charge creates B field
   MAPPING: B ~ (P × rotation coupling)
   TESTABILITY: Medium (depends on composition)
   SCORE: 65/100

4. PHOTON SPHERE RADIUS
   WHY: Where vortex transitions to radiation
   MAPPING: r_photon ~ (G*M/c^2) × f(P)
   TESTABILITY: High (GR prediction)
   SCORE: 75/100

5. HAWKING TEMPERATURE
   WHY: Vortex at event horizon creates radiation
   MAPPING: T_H ~ ℏc³/(8πGMk_B), check if P appears
   TESTABILITY: Theoretical only
   SCORE: 58/100

6. EDDINGTON LUMINOSITY
   WHY: Maximum stable power output
   MAPPING: L_Edd = 4πGMc/κ, compare to P
   TESTABILITY: High (well-defined)
   SCORE: 85/100

7. TIDAL DISRUPTION RADIUS
   WHY: Where vortex of big object disrupts smaller
   MAPPING: r_tidal ~ R_star × (M_BH/M_star)^(1/3)
   TESTABILITY: High (observational data)
   SCORE: 72/100

8. GRAVITATIONAL WAVE FREQUENCY
   WHY: Vortex oscillation creates GW
   MAPPING: f_GW ~ (P/E_binding)^(1/2)
   TESTABILITY: High (LIGO data)
   SCORE: 80/100

9. ELECTRON ORBITAL RADIUS (atomic scale)
   WHY: Same vortex structure at different scale
   MAPPING: r_e ~ (P_atomic / P_stellar)^(1/n) × r_stellar
   TESTABILITY: Medium (scale gap)
   SCORE: 68/100

10. FIELD CLOSURE CYCLE LENGTH
    WHY: Vortex completes one cycle per closure
    MAPPING: Closure digits ~ f(P, R, k)
    TESTABILITY: High (pi encoding)
    SCORE: 77/100
```

### 4.3 Top Selection: Eddington Luminosity

```
SELECTED: Eddington Luminosity (Score: 85/100)

WHY THIS CONNECTION MAKES SENSE:
1. Both are power/luminosity measures
2. Eddington is the maximum stable output
3. If P > L_Edd, star loses mass (vortex disruption)
4. The ratio P/L_Edd should relate to stability
5. GFD might explain WHY L_Edd has its specific form

TEST DESIGN:
class EddingtonLuminosityVortexLimit(Test):
    """
    Probe the relationship between vortex power output and 
    Eddington luminosity as a stability boundary.
    
    WHY: If power output is vortex-driven, Eddington luminosity
    represents where the outward vortex overcomes gravity.
    
    HONESTY: Eddington luminosity is standard physics.
    The vortex interpretation is GFD speculation.
    """
    
    question = (
        "Why does the Eddington luminosity have the form L_Edd = 4πGMc/κ? "
        "Does the factor 4π relate to the vortex geometry (full sphere)? "
        "Does G*M*c suggest the vortex couples gravity to light speed?"
    )
    
    # ... full test implementation
```

---

## Part 5: The Reasoning Loop

### 5.1 The Full Cycle

```
                    ┌─────────────────┐
                    │  EXISTING TEST  │
                    │  (validated)    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  WHY PROTOCOL   │
                    │  (understand)   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  10 BRAINSTORM  │
                    │  (generate)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  SCORE & SELECT │
                    │  (prioritize)   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  WRITE TEST     │
                    │  (in sandbox)   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  RUN & ANALYZE  │
                    │  (evaluate)     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  MATCH   │  │  PARTIAL │  │  NO MATCH│
        │  (< 5%)  │  │  (5-30%) │  │  (> 30%) │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             ▼             ▼             ▼
        Document      ERROR BRIDGE    Document
        as Finding    PROTOCOL        as Negative
             │             │             │
             └──────────────┼─────────────┘
                           │
                           ▼
                    ┌─────────────────┐
                    │  NEW VALIDATED  │
                    │  CONCEPT        │
                    └────────┬────────┘
                             │
                             ▼
                    (Loop back to start)
```

### 5.2 Documentation Template

Every reasoning chain should be documented:

```markdown
## Reasoning Chain: [Starting Concept] → [Target Concept]

### Starting Point
- **Concept**: [What we know]
- **Test**: [Which test validated this]
- **Key Relationship**: [The formula or pattern]

### WHY Protocol
1. WHY does this exist? [Answer]
2. WHY might it connect? [Answer]
3. WHY would we expect specific form? [Answer]

### Brainstorm (Top 3 of 10)
1. [Idea] - Score: [X]/100 - [Reason]
2. [Idea] - Score: [X]/100 - [Reason]
3. [Idea] - Score: [X]/100 - [Reason]

### Selected Mapping
- **Target**: [What we're testing]
- **Hypothesis**: [The expected relationship]
- **Test File**: [sandbox_xxx.py]

### Results
- **Error**: [X]%
- **Conclusion**: [Match/Partial/No Match]
- **Next Step**: [What we learned, what to try next]

### Chain Continues To
- [Next concept in the chain]
```

---

## Part 6: Integration with Probing Framework

### 6.1 When to Use Scientific Reasoning Framework

Use this framework when:

1. **You have a validated test** and want to explore what else it implies
2. **You see an error** and want to understand why
3. **You want to connect domains** (e.g., stellar to atomic)
4. **You're stuck** on what to test next

### 6.2 Probing Framework Reference

In the Probing Framework, after Step 4 (Contribution Scoring), add:

```
STEP 4.5: SCIENTIFIC REASONING EXTENSION
─────────────────────────────────────────
For high-contribution tests (score >= 70), apply the
Scientific Reasoning Framework to explore implications:

1. Run WHY Protocol on the finding
2. Generate 10 mapping brainstorm
3. Score and select top candidate
4. Write bridge test in sandbox
5. Document reasoning chain

See: framework/SCIENTIFIC_REASONING_MODULE.md
```

---

## Part 7: Worked Example

### 7.1 Full Chain: Power Output → Valence Horizon → Atomic Radius

**Step 1: Starting Point**
```
Test: StellarPowerOutput (validated)
Relationship: P = L_solar × (M/M_solar)^3.5 × (R_solar/R)^0.5
```

**Step 2: WHY Protocol**
```
WHY does power scale as M^3.5?
  -> Nuclear fusion rate ~ density × temperature^4
  -> Density ~ M/R^3, Temperature ~ M/R
  -> Combining: P ~ M^5/R^4, but empirically M^3.5
  -> Suggests additional coupling to mass

WHY might this connect to valence horizon?
  -> Power output defines energy available at surface
  -> Valence horizon is where energy states are defined
  -> If star is "macro-atom", its "valence" is the photosphere

WHY would we expect specific form?
  -> Valence horizon might scale as R_v ~ (P/P_0)^(1/n)
  -> If n = 3.5, then R_v ~ M
  -> This would connect star mass to its "valence" size
```

**Step 3: Brainstorm (abbreviated)**
```
1. Photosphere radius - Score: 88
2. Habitable zone distance - Score: 75
3. Stellar wind termination - Score: 72
...
```

**Step 4: Selected Test**
```
Target: Photosphere radius R_photo
Hypothesis: R_photo ~ (P/σT^4)^(1/2) where σ = Stefan-Boltzmann

Test:
  Model: Calculate R_photo from P and T
  Observation: Measured stellar radii
  Expected: R_photo/R_star ~ constant for main sequence
```

**Step 5: Results**
```
Error: 8% systematic offset
Conclusion: Partial match, need correction

Error Bridge:
  Hypothesis: Limb darkening effect not included
  Bridge Test: Add limb darkening correction
  Result: Error reduced to 2%
  
FINDING: Stellar "valence horizon" is photosphere,
         with limb darkening as boundary effect.
```

**Step 6: Chain Continues**
```
NEW QUESTION: Does photosphere/stellar radius ratio
              relate to electron orbital/atomic radius ratio?

Ratio_star = R_photo / R_star ≈ 1 (by definition)
Ratio_atom = r_electron / r_nucleus ≈ 10^5

WHY such different ratios?
  -> Scale difference: stellar vs atomic
  -> But: What if we use r_Bohr / r_Compton?
  -> r_Bohr / r_Compton = α^(-1) ≈ 137
  
NEXT TEST: Is 137 a universal "valence horizon" ratio
           appearing at all scales?
```

---

## Part 8: Equation Derivation Mode

### 8.1 The Reverse Engineering Question

When you encounter a standard model equation, ask:

> **"Can I derive this equation from first principles using GFD geometry?"**

This is working backwards: starting with a known result and asking if GFD structure can explain WHY it has that form.

### 8.2 The Equation Derivation Protocol

**Step 1: State the Target Equation**
```
TARGET: F = G * M * m / r^2 (Newton's Law of Gravitation)

Known:
  - Empirically verified to high precision
  - G is measured constant
  - Inverse-square law
```

**Step 2: Ask WHY Each Component**
```
WHY is it inverse-square (1/r^2)?
  -> Surface of sphere scales as r^2
  -> Field lines spread over 4πr^2
  -> GFD: 3D space has d=3, surface is d-1=2 dimensional

WHY is it proportional to both masses?
  -> Symmetry: if M pulls m, m pulls M
  -> GFD: Both objects have gravity fields that couple

WHY does G have its specific value?
  -> G = (17/13) × α^21 × ℏc / m_e^2
  -> GFD derives from (3+1)^2 structure
  -> See Paper VI for full derivation
```

**Step 3: Attempt GFD Derivation**
```
GFD APPROACH:
  1. Gravity field has k=4 vertices, d=3 spatial faces
  2. Two fields coupling: (k)^2 = 16 interaction modes
  3. Normalized by total structure: 16/13 ≈ 17/13
  4. Field closure at Compton scale gives α coupling
  5. Result: G = f(k, d, α, ℏ, c, m_e)

COMPARE TO TARGET:
  - Does GFD predict 1/r^2? YES (d-1 = 2)
  - Does GFD predict M×m? YES (two-field coupling)
  - Does GFD predict G value? YES (to 0.02% precision)
```

**Step 4: Document as Test**
```python
class NewtonGravityFromGFD(Test):
    """
    Derive Newton's gravitational law from GFD first principles.
    
    HONESTY: Newton's law is empirical. GFD attempts to explain
    WHY it has its specific form from geometric structure.
    """
    question = (
        "Can the form F = GMm/r^2 be derived from GFD geometry? "
        "Specifically: why inverse-square, why mass-product, why G?"
    )
    # ...
```

### 8.3 Equation Derivation Brainstorm

For any standard equation, generate derivation hypotheses:

| Component | GFD Derivation Hypothesis |
|-----------|---------------------------|
| **Exponent** | d, k, or combination (d-1, k+1, etc.) |
| **Coefficient** | Ratio of geometric counts (faces/vertices, etc.) |
| **Constant** | Derived from α, ℏ, c, m_e via closure |
| **Functional Form** | Topology of field interaction |

### 8.4 Example: Deriving Stefan-Boltzmann

```
TARGET: P = σ × A × T^4

WHY T^4?
  -> Planck distribution integral gives T^4
  -> GFD: k=4 vertices, thermal excitation samples all modes
  -> Hypothesis: T^4 because k=4

WHY σ has its value?
  -> σ = 2π^5 k_B^4 / (15 h^3 c^2)
  -> Contains π^5 (geometry), k_B^4 (thermal), h^3 c^2 (quantum/relativity)
  -> GFD: Can we derive the 2/15 and π^5 from closure?

TEST: Does σ relate to GFD constants?
  -> Calculate: σ / (some GFD combination)
  -> Look for simple ratios (1, 2, π, k, d)
```

---

## Part 9: Function Extraction Mode

### 9.1 The Reusability Question

When a test produces useful results, ask:

> **"Can I extract this into a reusable function (`@Fn`) that the rest of the system can use?"**

Functions are just as valuable as tests. A good function:
- Encapsulates a validated calculation
- Can be used by multiple tests via `Depends()`
- Documents the equation, inputs, outputs, and physics meaning
- Is registered in the central **Function Registry** for discovery

### 9.1.1 The Function Registry

All `@Fn` functions are registered in `gravity_field_model/functions/` for easy discovery:

```python
# Discover available functions
from gravity_field_model.functions import list_all_functions
list_all_functions()  # Prints all registered functions

# Import and use a function
from gravity_field_model.functions import fn_get_power_output_per_field
power = fn_get_power_output_per_field(56)  # Fe-56 power output

# Use in tests via Depends
from gravity_field_model.framework import Depends
from gravity_field_model.functions import fn_get_power_output_per_field

class MyTest(Test):
    get_power = Depends(fn_get_power_output_per_field)
```

**Before writing a new function, check the registry!** The function you need may already exist.

### 9.2 When to Extract a Function

Extract a function when:

| Condition | Why Extract |
|-----------|-------------|
| **Used in 2+ tests** | Avoid code duplication |
| **Has clear equation** | Document the physics |
| **Returns useful value** | Other tests need this result |
| **Represents physical quantity** | Named concept worth encapsulating |

### 9.3 The Function Extraction Protocol

**Step 1: Identify the Calculation**
```python
# In your test, you have:
def model(self):
    be_mev = get_binding_energy(mass_number)
    be_joules = be_mev * MEV_TO_JOULES
    power = be_joules * F_CLOSURE  # <-- This is the key calculation
    return Model().add("Power (W)", power)
```

**Step 2: Ask the Extraction Questions**
```
1. Is this calculation used elsewhere? 
   -> Check other tests in the domain
   
2. Does it have a clear equation?
   -> P = BE × f_closure (YES)
   
3. What are the inputs and outputs?
   -> Input: mass_number (int)
   -> Output: power in watts (float)
   
4. What physics does it represent?
   -> Power output per gravity field from binding energy
```

**Step 3: Define the Function**
```python
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
    
    Args:
        mass_number: Mass number A (number of nucleons)
    
    Returns:
        Power in watts per gravity field
    """
    be_mev = get_binding_energy(mass_number)
    be_joules = be_mev * MEV_TO_JOULES
    return be_joules * F_CLOSURE
```

**Step 4: Use in Tests via Depends**
```python
class StellarFusionChain(Test):
    # Inject the validated function
    get_power = Depends(fn_get_power_output_per_field)
    
    def model(self):
        return (
            Model()
            .add("He-4 power (W)", self.get_power(4))
            .add("Fe-56 power (W)", self.get_power(56))
        )
```

### 9.4 Function Naming Convention

Follow the Command Query pattern:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `fn_get_<what>` | Query: returns data, no side effects | `fn_get_power_output_per_field` |
| `fn_calc_<what>` | Query: returns computed value | `fn_calc_binding_energy` |
| `fn_set_<what>` | Command: modifies state | `fn_set_field_configuration` |

### 9.5 Function Extraction Checklist

Before extracting a function, verify:

- [ ] **Equation documented**: The `@Fn` decorator has the equation
- [ ] **Inputs described**: Each input has type and physics meaning
- [ ] **Outputs described**: Return value has units and meaning
- [ ] **Description explains**: WHY this function exists, WHAT it computes
- [ ] **Constants imported**: All values from `gravity_field_model.common`
- [ ] **Test validates it**: At least one CRITICAL test uses and validates the function
- [ ] **Registered**: Function is added to `gravity_field_model/functions/registry.py`

### 9.5.1 Assessing a Function for Graduation

Before registering, use the registry's graduation API to check status:

```python
from gravity_field_model.functions import assess_function_for_graduation

# In your pipeline, assess the function:
if assess_function_for_graduation(fn_your_function):
    print("Ready for central registry!")
else:
    print("Keep in source file, improve scores first")
```

Output:
```
============================================================
FUNCTION GRADUATION ASSESSMENT: fn_your_function
============================================================
  audit_score:        80 (threshold: 65)
  contribution_score: 72 (threshold: 70)
  audit_passed:       True
  contribution_passed: True
  ========================================================
  STATUS: GRADUATED - Ready for central registry
============================================================
```

### 9.5.2 Registering a Graduated Function

Only after graduation, register in the central registry:

1. **Add import** to `gravity_field_model/functions/registry.py`:
   ```python
   from gravity_field_model.calculations.your_domain.your_file import fn_your_function
   ```

2. **Register with metadata** (scores are read from @Fn decorator):
   ```python
   register_function(
       fn_your_function,
       group="your_domain",  # e.g., "stellar_mechanics", "black_holes"
       equation="your equation here",
       description="One-line description of what it does.",
       source_file="calculations/your_domain/your_file.py",
   )
   ```

3. **Add to namespace class** (if group exists) or create new namespace

4. **Export** from `gravity_field_model/functions/__init__.py`

**Note:** The registry will reject non-graduated functions with a warning.

### 9.6 Function Discovery from Test Results

When reviewing test results, actively look for function opportunities:

```
TEST RESULT ANALYSIS:

Test: ISCORadiusSixFaces
Result: r_ISCO = 6 × G × M / c^2

FUNCTION OPPORTUNITY:
  -> This is a general formula for ISCO radius
  -> Other black hole tests might need it
  -> Extract as: fn_get_isco_radius(mass)

Test: ChirpMassExponents
Result: M_chirp = (m1 × m2)^(3/5) / (m1 + m2)^(1/5)

FUNCTION OPPORTUNITY:
  -> Chirp mass is used in all GW calculations
  -> Extract as: fn_calc_chirp_mass(m1, m2)

Test: HawkingTemperature
Result: T_H = ℏ × c^3 / (8π × G × M × k_B)

FUNCTION OPPORTUNITY:
  -> Used in black hole thermodynamics
  -> Extract as: fn_calc_hawking_temperature(mass)
```

### 9.7 The Function -> Test -> Function Loop

Functions and tests reinforce each other:

```
                    ┌──────────────────────┐
                    │  WRITE TEST          │
                    │  (explore physics)   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  IDENTIFY PATTERN    │
                    │  (equation emerges)  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  EXTRACT FUNCTION    │
                    │  (@Fn decorator)     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  VALIDATE FUNCTION   │
                    │  (CRITICAL test)     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  USE IN NEW TESTS    │
                    │  (Depends injection) │
                    └──────────┬───────────┘
                               │
                               ▼
                    (Discover new patterns, loop back)
```

---

## Part 10: Combining Modes

The most powerful reasoning combines multiple modes:

### 10.1 Full Discovery Chain Example

```
1. START: Test stellar power output (Part 7 worked example)
   RESULT: P = BE × f_closure

2. EXTRACT FUNCTION (Part 9):
   -> fn_get_power_output_per_field(mass_number)

3. BRAINSTORM CONNECTIONS (Part 2):
   -> Score top 10 mappings
   -> Select: Eddington luminosity (score 85)

4. EQUATION DERIVATION (Part 8):
   -> L_Edd = 4πGMc/κ
   -> WHY 4π? (spherical geometry)
   -> WHY G×M×c? (gravity-light coupling)
   -> Can GFD derive κ (opacity)?

5. WRITE TEST:
   -> Compare P to L_Edd
   -> If P/L_Edd has simple form, extract as function

6. ERROR BRIDGE (Part 3):
   -> If 15% error, brainstorm sources
   -> Test each hypothesis
   -> Refine understanding

7. CHAIN CONTINUES:
   -> New function: fn_calc_eddington_ratio(mass, power)
   -> Next question: Does this ratio predict stellar stability?
```

### 10.2 Mode Selection Guide

| Situation | Mode to Use |
|-----------|-------------|
| Have a validated test | Part 2: Brainstorm mappings |
| Results don't match | Part 3: Error bridge |
| See a standard equation | Part 8: Equation derivation |
| Same calculation in 2+ tests | Part 9: Function extraction |
| High contribution test | Part 6 (Probing Framework): Full reasoning chain |

### 10.3 Sandbox Graduation Thresholds

Tests developed in `calculations/sandbox/` must meet these criteria to graduate:

| Score | Threshold | Meaning |
|-------|-----------|---------|
| `audit_score` | >= 65 | Quality: Well-documented, clear question, proper structure |
| `contribution_score` | >= 70 | Value: "Significant" or higher (see table below) |

**Contribution Score Interpretation:**

| Score | Assessment | Sandbox Action |
|-------|------------|----------------|
| 90-100 | Profound | **Graduate** immediately |
| 70-89 | Significant | **Graduate** |
| 50-69 | Valuable | **Remain in sandbox**: may stay if building toward larger chain |
| 30-49 | Incremental | **Remain in sandbox**: improve or merge |
| 0-49 | Below threshold | **Archive or delete**: not valuable enough |

**If criteria not met:**
- Improve the test to increase value
- Merge insights into an existing test
- Archive as "explored but not valuable enough"

Tests that remain in sandbox > 2 weeks without progress should be reviewed for archival.

---

## Summary: The Scientific Reasoning Mindset

1. **Never stop at one test** - Every finding opens doors to ten more
2. **Always ask WHY first** - Understanding precedes exploration
3. **Brainstorm systematically** - Don't rely on inspiration alone
4. **Score honestly** - Prioritize based on testability and impact
5. **Embrace error** - Discrepancies are data, not failures
6. **Document the chain** - Future you will thank present you
7. **Connect domains** - The deepest insights cross boundaries
8. **Derive from first principles** - Can GFD explain WHY this equation?
9. **Extract reusable functions** - Build the system as you discover

> "The first principle is that you must not fool yourself, and you are the easiest person to fool." - Richard Feynman

Apply this principle: Score your ideas honestly, test them rigorously, extract what's reusable, and follow the evidence wherever it leads.

---

*Document version: 3.0*
*Last updated: 2026-02-04*
*Location: framework/SCIENTIFIC_REASONING_MODULE.md*

**Changelog:**
- v3.0: Renamed from FRAMEWORK to MODULE. Clarified as STATELESS utility (no folder to guard). Removed Python module folder (reasoning is documented protocol, not code). Updated cross-references to use MODULE names.
- v2.0: (Deprecated) Attempted Python module implementation
- v1.1: Added Equation Derivation Mode (Part 8), Function Extraction Mode (Part 9), Sandbox Graduation Thresholds (Part 10)
- v1.0: Initial framework with WHY protocol, brainstorming, error bridge
