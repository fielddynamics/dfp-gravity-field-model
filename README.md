# DFP: Gravity Field Model

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests: 813 Passing](https://img.shields.io/badge/Tests-813%20Passing-brightgreen.svg)](#test-suite)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Distributed Field Processing (DFP)** is a physics framework that derives gravitational dynamics from the topology of spacetime. This repository contains the **Gravity Field Model**, a computational validation suite that tests DFP predictions against physical constants and observations.

**Author:** Stephen Nelson | [fielddynamics.org](https://fielddynamics.org)

---

## Quick Start

Launch the interactive test explorer in three steps:

```bash
# 1. Clone and enter the repository
git clone https://github.com/your-username/dfp-gravity-field-model.git
cd dfp-gravity-field-model

# 2. Install dependencies
pip install flask numpy

# 3. Launch the web interface
python gravity_field_model/web_interface/run_web.py
```

Your browser will open automatically to `http://localhost:5005`. Use the file tree on the left to browse tests, click any test to view its source code, then click **Run** to execute it.

---

## Overview

The model requires no dark matter and no free parameters beyond established physical constants. All predictions derive from a single geometric fact: in 3+1 dimensions, gravitational field closure requires exactly k=4 coupling channels.

---

## The Problem This Model Addresses

For over 90 years, physics has faced a persistent puzzle: galaxies rotate faster than their visible matter can explain. The standard solution posits invisible "dark matter" comprising 85% of all matter in the universe, yet decades of direct detection experiments have found nothing.

The DFP framework offers a different answer: the discrepancy is not missing matter but an incomplete understanding of how gravity operates at large scales. The "missing" mass emerges naturally from the nonlinear response of the gravitational field itself.

---

## The Core Insight

General Relativity requires gravity to "close": field configurations must resolve to a unique, consistent geometric state at every point in spacetime. This closure process has a specific topology determined by the dimensionality of space.

**The central result:** In 3+1 dimensions, field closure requires exactly **k = 4** coupling channels, forming a tetrahedral structure. Two such tetrahedra with opposite orientations (a stellated octahedron) provide the complete, stable architecture for gravitational field dynamics.

This single geometric fact, derived from four independent lines of established physics, determines:

| Constant | Standard Value | GFD Derivation | Agreement |
|----------|---------------|----------------|-----------|
| Fine structure constant | 1/137.036 | Geometric closure cycles | Exact |
| Electron spin | h/2 | (2 TIME faces / 8 total) x 2h | Exact |
| Proton-electron mass ratio | 1836.15 | 6 x pi^5 | 0.002% |
| Gravitational constant G | 6.674 x 10^-11 | Topology formula | 0.12% |
| MOND acceleration a0 | 1.2 x 10^-10 m/s^2 | 16 G m_e / r_e^2 | 2% |
| Hubble constant | 70 km/s/Mpc | Frame correction | 0.11% |

---

## The Papers

This model validates predictions from the Distributed Field Processing paper series:

| Paper | Title | Key Contribution |
|-------|-------|------------------|
| **DFP I** | The Gravitational Constitutive Law | Derives mu(x) = x/(1+x) from closure constraints; explains galactic rotation without dark matter |
| **DFP II** | A Covariant Theory Without Dark Matter | Covariant action matching CMB to 1%; explains Planck lensing anomaly |
| **DFP III** | The Unit of Gravity | Proves field closure is logically necessary given GR; derives a0 from electron scale |
| **DFP IV** | Resolving the Hubble Tension | Derives H = 69.92 km/s/Mpc from tetrad topology; explains measurement scatter |
| **DFP VI** | Deriving G from Spacetime Topology | Derives gravitational constant and electron spin from dual tetrahedra |

---

## Why k = 4?

The coupling constant k = 4 is not assumed but derived from four independent results spanning 50+ years of gravitational theory:

1. **Stability (Alexander et al., 2014):** Single-orientation tetrads produce ghost instabilities; opposite orientations cancel them

2. **Spinor Double Cover (Weinberg 1995, Geroch 1968):** Spinors require 720 degree rotation for identity, demanding two 360 degree circuits through dual structures

3. **Chirality (Ashtekar 1986):** Full gravity requires both left-handed and right-handed chiral contributions

4. **Bimetric Ghost Freedom (Hassan-Rosen 2012):** Ghost-free massive gravity requires exactly two metrics interacting through specific potential

All four roads lead to the same destination: **two tetrahedra with opposite orientations**, the stellated octahedron.

---

## What the Model Computes

### Field Closure Geometry
- Stellated octahedron structure: 8 vertices, 8 faces, 12 edges
- Tetrahedron A (vertices 1,2,4,7) and Tetrahedron B (vertices 0,3,5,6)
- Face classification: 2 TIME faces, 6 SPATIAL faces
- The ratio (2/8) x 2h = h/2 derives electron spin

### Pi-Driven Traversal
- Field closure is governed by pi digits in base-8
- Each digit determines the next vertex visited
- Ergodic traversal visits all 8 vertices uniformly
- Mean orbit length: 8 / mean_digit = 2.4 digits

### Emergent Constants
- Fine structure constant from closure cycle counting
- Mass ratios from dimensional recursion
- Gravitational constant from (3+1) topology
- Hubble constant from frame correction sqrt(k/pi)

### Galactic Dynamics
- Constitutive law mu(x) = x/(1+x) derived, not fitted
- Baryonic Tully-Fisher relation as theorem, not observation
- External Field Effect predictions
- No dark matter required

---

## Running Tests

### Web Interface (Recommended)

See [Quick Start](#quick-start) above. The web interface provides:
- File browser for all test modules
- Syntax-highlighted code viewing
- One-click test execution
- Formatted results with derivations, models, and observations

### Command Line

Run any test file directly:

```bash
python gravity_field_model/engine_core/geometry/test_port_ratio.py
python gravity_field_model/calculations/stellar_mechanics/test_power_output.py
```

Or use the module runner:

```bash
python -m gravity_field_model.run_test ClosureStatisticsReasonable
```

### Custom Port

```bash
python gravity_field_model/web_interface/run_web.py --port 8080
```

---

## Test Suite

The validation suite contains **813 tests** across 16 categories:

### ENGINE Tests (Core Mechanics)

| Category | Tests | What It Validates |
|----------|-------|-------------------|
| Core Geometry | 185 | Stellated octahedron structure, vertex encoding, face classification |
| Traversal Engine | 101 | Pi-driven traversal, BBP algorithm, orbit statistics |
| Timing Analysis | 17 | Settlement frequency, Compton timing |
| Information Theory | 33 | Bits per orbit, entropy, channel capacity |
| Lattice Foundations | 13 | Axioms, bounds, consistency |
| Engine Stress Tests | 21 | Determinism, ergodicity, stability |

### CALC Tests (Physics Predictions)

| Category | Tests | What It Validates |
|----------|-------|-------------------|
| Stellar Mechanics | 124 | Fusion thresholds, element formation, binding densities |
| Particle Physics | 65 | Quark structure, mass derivations |
| Emergent Constants | 72 | alpha, mass ratios, spin, MOND scale, Hubble |
| Entanglement Mechanics | 42 | Quantum correlations, Tsirelson bounds |
| Historical Systems | 86 | I Ching, Gematria, Mitsuuroko correspondences |
| Black Holes | 12 | Bekenstein-Hawking entropy, horizons |
| Other | 52 | Biological mechanics, tunneling, cross-checks |

---

## Project Structure

```
dfp-gravity-field-model/
├── README.md                # This file
├── LICENSE                  # MIT License
│
└── gravity_field_model/     # Main model package
    │
    ├── common/              # Shared constants and data
    │   ├── constants_codata.py  # CODATA 2022 physical constants
    │   ├── pi_data.py           # Verified pi base-8 digits (10,000)
    │   └── stellar_constants.py # Astrophysical constants
    │
    ├── engine_core/         # Core field mechanics
    │   ├── common/              # Traversal and tetragram analyzers
    │   ├── geometry/            # Stellated octahedron structure
    │   ├── field_closure/       # Pi-driven traversal, BBP algorithm
    │   ├── timing/              # Causality, simultaneity, settlement
    │   ├── information/         # Bits, entropy, channel capacity
    │   ├── foundations/         # Lattice axioms and bounds
    │   ├── engine_dynamics/     # Binding, spin, stability
    │   ├── engine_crosschecks/  # NASA-level traversal verification
    │   └── stress_tests/        # Determinism, ergodicity tests
    │
    ├── calculations/        # Physics predictions
    │   ├── stellar_mechanics/      # Fusion, element formation
    │   ├── particle_physics/       # Quarks, mass derivations
    │   ├── emergent_constants/     # alpha, G, H0, a0
    │   ├── entanglement_mechanics/ # Quantum correlations
    │   ├── historical_systems/     # I Ching, Gematria correspondences
    │   └── ...                     # Additional modules
    │
    ├── web_interface/       # Flask web application
    │   ├── app.py               # Flask routes and API
    │   ├── run_web.py           # Server launcher
    │   ├── templates/           # HTML templates
    │   └── static/              # CSS and JavaScript
    │
    ├── framework.py         # New test framework (v2)
    ├── base.py              # Legacy test framework (v1)
    │
    └── docs/                # Documentation
        └── Gravity_Field_Dynamics_Textbook.md
```

---

## Key Concepts

### Field Closure

The mechanism by which gravitational coupling resolves to a unique, consistent geometric state. Field closure is not new physics; it is the process that General Relativity always required but lacked a name for.

### NET Field

The combined gravitational environment from all external sources, encoded locally at each point. Characterized by the local geometry scale l(x) = sqrt(-g00).

### Saturation Scale (a0)

The acceleration below which field closure cannot fully resolve geometric differences:
```
a0 = cH/(2pi) = 1.2 x 10^-10 m/s^2
```
This is the MOND acceleration, derived from horizon thermodynamics.

### Constitutive Law

The function describing how gravitational response depends on acceleration:
```
mu(x) = x / (1 + x)
```
This is not a curve fit. It is the unique solution satisfying closure constraints.

---

## Physical Constants

All constants derive from CODATA 2022 values:

```python
from gravity_field_model.common import C, HBAR, ALPHA, M_E, R_E, K

C = 299792458        # Speed of light (m/s, exact)
HBAR = 1.054571817e-34  # Reduced Planck constant (J*s)
ALPHA = 7.2973525693e-3 # Fine structure constant
M_E = 9.1093837015e-31  # Electron mass (kg)
R_E = 2.8179403262e-15  # Classical electron radius (m)
K = 4                   # Tetrahedral closure constant
```

---

## Writing New Tests

### New Framework (v2)

Tests use the builder pattern with `Test`, `Derivation`, `Model`, and `Observed`:

```python
from gravity_field_model.framework import *
from gravity_field_model.common.constants_codata import C, HBAR

class MyTest(Test):
    name = "My Test Name"
    reference = "Source of observed values"
    level = Level.STANDARD  # or CRITICAL, EXPLORATORY
    
    question = "What does this test verify and why does it matter?"
    
    derivation = (
        Derivation()
        .step("Start with the fundamental relationship")
        .step("Apply the closure constraint")
        .conclusion("The result follows from geometry alone")
    )
    
    def model(self):
        return Model().value("result", 42.0, "units")
    
    def observations(self):
        return Observed().value("result", 42.0, "units")

if __name__ == "__main__":
    run_tests(MyTest)
```

### Legacy Framework (v1)

Older tests inherit from `GFDTest`:

```python
from gravity_field_model.base import GFDTest

class MyTest(GFDTest):
    name = "My Test"
    question = "What does this test verify?"
    reference_source = "Source of observed values"
    tolerance = 0.10  # 10% relative error allowed
    
    def model(self):
        return {"value": 42.0}
    
    def observations(self):
        return {"value": 42.0}
```

Both frameworks are fully supported by the web interface.

---

## Falsifiable Predictions

The DFP framework makes specific, testable predictions:

| Prediction | DFP | Standard (CDM) | Status |
|------------|-----|----------------|--------|
| **Fast galactic bars** | R ~ 1.0-1.4 | R > 1.4-2.0 | Consistent with observations |
| **External Field Effect** | Satellites show reduced discrepancy in strong external fields | No environmental dependence | Testable |
| **Tully-Fisher at z=2** | +21% velocity boost | No evolution | SINS survey shows +27% |
| **Hubble measurements** | All within 65.8-74.3 km/s/Mpc | No constraint | Consistent |
| **Wide binary anomalies** | Slow return to Newtonian at g < a0 | No anomaly | Active discriminator |

---

## Contributing

Contributions are welcome. To add new tests:

1. Fork the repository
2. Create a feature branch
3. Add tests following the GFDTest pattern
4. Ensure all tests pass
5. Submit a pull request

---

## References

**DFP Papers:**
- Nelson, S. (2026). "DFP I: The Gravitational Constitutive Law"
- Nelson, S. (2026). "DFP II: A Covariant Theory Without Dark Matter"
- Nelson, S. (2026). "DFP III: The Unit of Gravity"
- Nelson, S. (2026). "DFP IV: Resolving the Hubble Tension Through Tetrad Topology"
- Nelson, S. (2026). "DFP VI: Deriving the Gravitational Constant from Spacetime Topology"

**Foundational:**
- Bekenstein, J. D. (1973). Black holes and entropy. Physical Review D, 7(8), 2333.
- Milgrom, M. (1983). A modification of the Newtonian dynamics. Astrophysical Journal, 270, 365-370.
- Hassan, S. F., & Rosen, R. A. (2012). Bimetric gravity from ghost-free massive gravity. JHEP, 2012(2), 126.
- Bailey, D., Borwein, P., & Plouffe, S. (1997). On the rapid computation of various polylogarithmic constants.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**DFP: Gravity Field Model**

*The constants of nature are geometric necessities, not accidents.*
