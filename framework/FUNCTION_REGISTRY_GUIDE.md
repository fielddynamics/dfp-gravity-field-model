# Function Registry Guide

**Module Type:** STATEFUL (gatekeeper, guards a folder)

**Purpose:** Central catalog of graduated `@Fn` functions. This is the ONLY module that guards a folder. It accumulates artifacts over time and enforces graduation rules.

**Guards:** `gravity_field_model/functions/`

**Called by:** START_RESEARCH_MODULE (Stage 7: Function Graduation)

**Imports thresholds from:**
- TEST_QUALITY_MODULE: `audit_score >= 65`
- CONTRIBUTION_SCORING_MODULE: `contribution_score >= 70`

---

## Overview

The Function Registry is a central catalog of **GRADUATED** `@Fn` decorated functions in the gravity field model. 

**Only functions that meet graduation criteria are included:**
- `audit_score >= 65` (quality threshold)
- `contribution_score >= 70` (must be "Significant" or higher)

This ensures the registry contains only high-quality, valuable functions.

**Location:** `gravity_field_model/functions/`

---

## Graduation Criteria (Same as Tests)

Functions follow the same graduation process as tests:

| Score | Threshold | What It Measures |
|-------|-----------|------------------|
| `audit_score` | >= 65 | Quality: documentation, validation, constants |
| `contribution_score` | >= 70 | Value: must be "Significant" or higher |

**Contribution Score Interpretation:**

| Score | Assessment | Registry Status |
|-------|------------|-----------------|
| 90-100 | Profound | **In Registry** |
| 70-89 | Significant | **In Registry** |
| 50-69 | Valuable | NOT in registry (improve first) |
| < 50 | Below threshold | NOT in registry |

---

## Quick Start

### Discover Available Functions

```python
from gravity_field_model.functions import list_all_functions
list_all_functions()
```

Output:
```
======================================================================
GRAVITY FIELD MODEL - FUNCTION REGISTRY
======================================================================

### STELLAR MECHANICS ###

  fn_get_power_output_per_field
    Equation: P(A) = BE(A) * (c / lambda_C)
    Purpose:  Power output per gravity field from binding energy. Peaks at Fe-56.
    Source:   examples/example_power_output.py

### ATOMIC PHYSICS ###

  fn_get_element_field_radius
    Equation: r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [1 - (k/pi^2)*mu(Z/56)]
    Purpose:  Empirical atomic radius prediction (fitted formula, ~13% accuracy).
    Source:   calculations/stellar_mechanics/test_valence_predictions.py

======================================================================
Total functions registered: 2
======================================================================
```

### Use a Function Directly

```python
from gravity_field_model.functions import fn_get_power_output_per_field

# Get power output for Iron-56
power = fn_get_power_output_per_field(56)
print(f"Fe-56 power: {power:.2e} W")
```

### Use a Function in Tests (Dependency Injection)

```python
from gravity_field_model.framework import Test, Depends
from gravity_field_model.functions import fn_get_power_output_per_field

class MyStellarTest(Test):
    # Inject the function
    get_power = Depends(fn_get_power_output_per_field)
    
    def model(self):
        # Use the injected function
        power_he = self.get_power(4)   # Helium-4
        power_fe = self.get_power(56)  # Iron-56
        return Model().add("Power ratio Fe/He", power_fe / power_he)
```

---

## Function Groups

Functions are organized by physics domain:

| Group | Description | Example Functions |
|-------|-------------|-------------------|
| `stellar_mechanics` | Nuclear binding, power output, fusion | `fn_get_power_output_per_field` |
| `atomic_physics` | Atomic radii, valence, electron shells | `fn_get_element_field_radius` |
| `black_holes` | ISCO, horizons, Hawking radiation | (planned) |
| `gravitational_waves` | Chirp mass, strain, frequency | (planned) |
| `field_closure` | Pi encoding, closure cycles | (planned) |

### Import by Group

```python
from gravity_field_model.functions import stellar_mechanics

# List functions in the group
stellar_mechanics.list_functions()

# Use a function from the group
power = stellar_mechanics.fn_get_power_output_per_field(56)
```

---

## Adding New Functions

### Step 1: Define the Function WITH SCORES

In your domain file (e.g., `calculations/black_holes/test_black_hole_mechanics.py`):

```python
from gravity_field_model.framework import Fn
from gravity_field_model.common import G, C

@Fn(
    equation="r_ISCO = 6GM/c^2",
    inputs={"mass": "float: Black hole mass in kg"},
    outputs={"meters": "float: ISCO radius in meters"},
    description=(
        "Query: Returns the innermost stable circular orbit radius. "
        "For Schwarzschild black holes, r_ISCO = 6 * r_s / 2 = 3 * r_s."
    ),
    # GRADUATION SCORES (required for central registry)
    audit_score=80,
    audit_notes=(
        "Equation: Clear GR formula. "
        "Inputs/Outputs: Well specified with units. "
        "Description: Explains physics. "
        "Validation: CRITICAL test validates. "
        "Constants: G, C from CODATA."
    ),
    contribution_score=72,
    contribution_notes=(
        "Discovery: 25/40 - Standard GR formula, documents 6 = spatial faces connection. "
        "Precision: 18/20 - Exact analytical formula. "
        "Cross-Domain: 15/20 - Used in black hole, GW, and accretion tests. "
        "Falsifiability: 14/20 - Testable against GR predictions."
    ),
)
def fn_get_isco_radius(mass: float) -> float:
    """Get ISCO radius for a Schwarzschild black hole."""
    return 6 * G * mass / C**2
```

**Without scores or below threshold, the function will NOT be added to the registry.**

### Step 2: Check Graduation Status

Before registering, verify the function meets criteria:

```python
from gravity_field_model.functions import check_graduation

result = check_graduation(fn_get_isco_radius)
print(result)
# {'name': 'fn_get_isco_radius', 'audit_score': 80, 'contribution_score': 72, 
#  'graduated': True, 'issues': []}
```

### Step 3: Register in the Catalog (Only If Graduated)

In `gravity_field_model/functions/registry.py`:

```python
# Add import
from gravity_field_model.calculations.black_holes.test_black_hole_mechanics import (
    fn_get_isco_radius
)

# Register with metadata (scores are read from @Fn decorator)
register_function(
    fn_get_isco_radius,
    group="black_holes",
    equation="r_ISCO = 6GM/c^2",
    description="ISCO radius for Schwarzschild black hole.",
    source_file="calculations/black_holes/test_black_hole_mechanics.py",
)
```

**Note:** If the function doesn't meet graduation criteria, a warning will be printed and it will NOT be added to the catalog.

### Step 4: Add to Namespace (Optional)

If the group namespace class exists, add the function:

```python
class BlackHolesNamespace:
    fn_get_isco_radius = fn_get_isco_radius
    
    @staticmethod
    def list_functions() -> List[str]:
        return [name for name, entry in FUNCTION_CATALOG.items() 
                if entry.group == "black_holes"]

black_holes = BlackHolesNamespace()
```

### Step 5: Export from `__init__.py`

```python
from gravity_field_model.functions.registry import (
    # ... existing imports ...
    fn_get_isco_radius,
    black_holes,
)

__all__ = [
    # ... existing exports ...
    "fn_get_isco_radius",
    "black_holes",
]
```

---

## Function Naming Convention

| Prefix | Purpose | Example |
|--------|---------|---------|
| `fn_get_<what>` | Query: returns data, no side effects | `fn_get_power_output_per_field` |
| `fn_calc_<what>` | Query: returns computed value | `fn_calc_chirp_mass` |
| `fn_set_<what>` | Command: modifies state | `fn_set_field_configuration` |

---

## Function Scoring Guide

### audit_score (0-100): Quality

How well documented and validated is the function?

| Criterion | Points | What to Check |
|-----------|--------|---------------|
| **Equation** | 0-20 | Clear, correct, documented in @Fn |
| **Inputs/Outputs** | 0-20 | Types and units specified |
| **Description** | 0-20 | Explains physics meaning |
| **Validation** | 0-20 | At least one CRITICAL test uses it |
| **Constants** | 0-20 | All from common module (CODATA) |

**Threshold: >= 65 to graduate**

### contribution_score (0-100): Value

How valuable is this function to the system?

| Dimension | Points | What to Evaluate |
|-----------|--------|------------------|
| **Discovery Value** | 0-40 | Does it encapsulate novel/important calculation? |
| **Precision & Rigor** | 0-20 | How reliable and accurate? |
| **Cross-Domain Impact** | 0-20 | Used across multiple test domains? |
| **Falsifiability** | 0-20 | Does it make testable predictions? |

**Threshold: >= 70 to graduate ("Significant" or higher)**

### Example Scoring

```python
@Fn(
    equation="P(A) = BE(A) * (c / lambda_C)",
    inputs={"mass_number": "int: Mass number A"},
    outputs={"watts": "float: Power output"},
    description="Power output per gravity field from binding energy.",
    
    # Quality assessment
    audit_score=82,
    audit_notes=(
        "Equation: 18/20 - Clear and documented. "
        "Inputs/Outputs: 18/20 - Well specified with units. "
        "Description: 16/20 - Explains physics meaning. "
        "Validation: 15/20 - CRITICAL test validates. "
        "Constants: 15/20 - All from CODATA."
    ),
    
    # Contribution assessment
    contribution_score=75,
    contribution_notes=(
        "Discovery: 28/40 - Core GFD concept. "
        "Precision: 18/20 - Exact calculation. "
        "Cross-Domain: 17/20 - Used in stellar, fusion, element studies. "
        "Falsifiability: 12/20 - Predicts Fe-56 peak."
    ),
)
def fn_get_power_output_per_field(mass_number: int) -> float:
    ...
```

---

## Pipeline API: Graduation Assessment

The registry provides a single source of truth for graduation rules.
Other frameworks call these APIs to assess functions:

### Quick Check (Returns Bool)

```python
from gravity_field_model.functions import assess_function_for_graduation

# In your pipeline:
if assess_function_for_graduation(my_function):
    # Add to central registry
    pass
else:
    # Keep in source file, improve first
    pass
```

### Detailed Check (Returns Dict)

```python
from gravity_field_model.functions import check_graduation

result = check_graduation(my_function)
print(result)
# {
#   'name': 'my_function',
#   'audit_score': 80,
#   'contribution_score': 72,
#   'graduated': True,
#   'issues': [],
#   'recommendation': 'GRADUATED: Add to central registry'
# }
```

### Pipeline Integration

The START_RESEARCH_MODULE and SCIENTIFIC_REASONING_MODULE pipelines
should call `assess_function_for_graduation()` after scoring a function
to determine if it's ready for the central registry.

---

## Before Writing a New Function

**Always check the registry first!**

```python
from gravity_field_model.functions import list_all_functions
list_all_functions()
```

The function you need may already exist. Reuse is better than duplication.

---

## The Power of Function Chains

Functions enable building chains of calculations:

```python
from gravity_field_model.functions import (
    fn_get_power_output_per_field,
    fn_get_element_field_radius,
)

# Chain: Mass number -> Power -> ... -> Radius prediction
def analyze_element(symbol: str, mass_number: int):
    power = fn_get_power_output_per_field(mass_number)
    radius = fn_get_element_field_radius(symbol)
    
    # Now you can explore relationships between power and radius!
    return {
        "power": power,
        "radius": radius,
        "power_per_pm": power / radius,  # New derived quantity
    }
```

This is the essence of the Scientific Reasoning Framework: building chains of validated calculations to discover new patterns.

---

## Integration with Frameworks

- **Probing Framework** (Phase 6.6): Guidance on extracting functions from tests
- **Scientific Reasoning Framework** (Part 9): Full protocol for function extraction
- **Test Quality Framework**: Functions should be validated by CRITICAL tests

---

*Document version: 1.0*
*Last updated: 2026-02-04*
