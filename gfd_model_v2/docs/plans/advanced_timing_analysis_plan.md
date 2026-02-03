# Advanced Timing Analysis — CERN/NASA-Grade Expansion Plan
## Revised: Core / Advanced Split for Contributor Clarity

---

## Design Decision: Two Folders

```
gfd_model_v2/engine/
├── timing_analysis/                    ← CORE: "How the clock works"
│   ├── __init__.py
│   ├── test_closure_simultaneity.py    (existing — 11 tests)
│   ├── test_temporal_hierarchy.py      (new — Phase 1)
│   ├── test_timing_jitter.py          (new — Phase 1)
│   └── test_causal_structure.py       (new — Phase 2)
│
└── timing_analysis_advanced/           ← ADVANCED: "What the clock tells us about physics"
    ├── __init__.py
    ├── test_phase_coherence.py         (new — Phase 3)
    ├── test_spectral_analysis.py       (new — Phase 3)
    ├── test_relativistic_timing.py     (new — Phase 2)
    └── test_quantum_clock.py           (new — Phase 4)
```

### Splitting Rationale

**`timing_analysis/` (CORE)** contains tests that define the GFD timing model itself.
If any of these fail, the engine's timing claims are compromised. Contributors
working on *any* part of the engine should be familiar with these tests. They
answer: **"What are the rules of the clock?"**

- Closure simultaneity — the foundational timing observation
- Temporal hierarchy — the frequency ladder everything references
- Timing jitter — the statistical quality of the timing (precision floor)
- Causal structure — which events can influence which, the light cone

**`timing_analysis_advanced/` (ADVANCED)** contains tests that *use* the established
timing model to explore physics. These extend the model into new territory.
Failure here means "we have more to learn," not "the engine is broken." They
answer: **"What does the clock teach us about the universe?"**

- Phase coherence — Berry phase accumulation dynamics
- Spectral analysis — frequency-domain characterization
- Relativistic timing — GR, GPS corrections, curved spacetime
- Quantum clock — metrological certification

A contributor can safely work in `timing_analysis_advanced/` without touching core.
But changes to `timing_analysis/` should trigger a full review.

---

## Current State

The `timing_analysis` module currently has a single file:

| File | Tests | Covers |
|------|-------|--------|
| `test_closure_simultaneity.py` | 11 | Discrete states, step duration vs. light crossing, instantaneous closure, orbit boundary discreteness, causality, face read accumulation, tetrahedra independence, TIME face completion, complement arithmetic (nonlocality analogy), timing constraint summary |

Related timing work scattered elsewhere:

| File | Location | Relevant Tests |
|------|----------|----------------|
| `test_settlement_frequency.py` | `system_mechanics/` | Settlement frequency derivation, period, port firing, energy-wavelength consistency, dimensional checks, frequency range |
| `test_closure_cycle.py` | `system_mechanics/` | c from closure, Planck scale comparison, Zitterbewegung ratio, energy-time uncertainty, gravity wave comparison, time arrow |
| `test_field_closure_runs.py` | `system_mechanics/` | Closure run statistics, settlement frequency, 137 orbits, orbit length distribution |
| `test_subspace_nonlinearity.py` | `calculations/entanglement_mechanics/` | Settlement simultaneity, Tet_B contribution, coherence survival, decoherence timescale |

**Target state:** 2 folders, 8 files, ~87 tests.

---

## CORE: `timing_analysis/`

### Existing: `test_closure_simultaneity.py` (11 tests) — No changes

The foundation. Establishes discrete state transitions, step duration vs. light
crossing time, instantaneous closure events, and the simultaneity argument.
Already at the quality bar.

---

### New Module 1: `test_temporal_hierarchy.py` — Multi-Scale Frequency Ladder
*Inspired by: CERN LHC multi-level trigger system (L1 → L2 → HLT)*

**Why core:** Every other timing module references these frequencies. If the
ladder is inconsistent, nothing built on top of it is trustworthy. This is the
GFD equivalent of CERN's trigger timing specification — the document every
subsystem must conform to.

**Proposed Tests (~12):**

| # | Test | Question | Reference |
|---|------|----------|-----------|
| 1 | **FrequencyLadderCompleteness** | Do the five fundamental frequencies (Planck ~10⁴³, closure ~10²³, settlement ~10²⁰, Zitterbewegung ~2.5×10²⁰, decoherence⁻¹ ~10⁴) span the full range with no unexplained gaps? | Planck units, CODATA |
| 2 | **SettlementToClosureRatio** | Is f_closure / f_settlement ≈ 807 expressible in terms of model constants? Does 861/(2π) × some geometric factor appear? | Internal consistency |
| 3 | **PortFiringAsSubharmonic** | Does f_port = f_settlement/k confirm port firing is a strict k=4 subharmonic? | Tetrahedral topology |
| 4 | **OrbitFrequencyDerivation** | What is f_orbit = f_settlement / ⟨steps_per_orbit⟩? How does it relate to α? | Pi digit statistics |
| 5 | **ElectronCycleFrequency** | Does f_electron = f_orbit / 137 correspond to any known physical frequency? | Fine structure constant |
| 6 | **HierarchyRatiosFromGeometry** | Can each ratio between adjacent levels be derived from k, d, α, or 2π alone? | GFD framework |
| 7 | **TimescaleSeparationAdequacy** | Is each adjacent pair separated by ≥10², ensuring clean decoupling? | CERN trigger independence criterion |
| 8 | **PlanckToSettlementSteps** | How many settlements fit in one Planck time? Sub-Planck resolution of the model. | Planck units |
| 9 | **DecoherenceHorizonInOrbits** | How many 137-orbit electron cycles survive before decoherence? (~10¹⁶ / 137 / ⟨steps⟩) | Qubit experiments |
| 10 | **FrequencyLadderDimensionalCheck** | Does every frequency satisfy f × λ = c for its corresponding length scale? | Wave equation |
| 11 | **BandwidthPerLevel** | Information bandwidth (bits/s) at each level. Monotonically decreasing up the ladder? | Information theory |
| 12 | **TriggerEfficiency** | Fraction of settlement events producing orbit completions. (Analog to L1 accept rate.) | CERN trigger design |

---

### New Module 2: `test_timing_jitter.py` — Statistical Timing Precision
*Inspired by: NIST atomic clock Allan deviation; CERN bunch crossing jitter*

**Why core:** Closure lengths vary because pi is irrational — that IS clock jitter.
Every precision claim in the model implicitly depends on this jitter being
characterized. You can't claim 10²⁰ Hz precision without knowing the variance.

**Proposed Tests (~10):**

| # | Test | Question | Method |
|---|------|----------|--------|
| 1 | **InterClosureIntervalDistribution** | What is the probability distribution of closure intervals (in digits)? Geometric? Poisson? | Histogram fit over 10,000+ closures |
| 2 | **InterClosureVariance** | σ² of closure interval in digits and seconds? | Direct computation |
| 3 | **AllanVarianceAnalog** | σ²_y(τ) at averaging times of 1, 10, 100, 1000 orbits. 1/τ (white) or 1/τ² (random walk)? | Allan deviation protocol |
| 4 | **AutocorrelationOfClosureLengths** | Serial correlation between successive closure lengths? Pi digits should decorrelate. | Lag-1 through lag-10 autocorrelation |
| 5 | **RunsTestOnIntervals** | Wald-Wolfowitz runs test on above/below-mean closure lengths. Consistent with randomness? | Statistical hypothesis test |
| 6 | **LongestClosureRun** | Maximum closure length in 10,000 digits. Matches extreme value statistics? | Gumbel distribution fit |
| 7 | **ShortestClosureRun** | Frequency of single-step closures (digit ≥ 8, i.e., digit = 0 doesn't count, need digit that crosses boundary). | Counting |
| 8 | **JitterBudget** | Decompose total variance: (a) digit distribution, (b) vertex assignment, (c) tet switching. Which dominates? | Variance decomposition |
| 9 | **FractionalFrequencyStability** | σ_y = σ_T / ⟨T⟩. Better than 10⁻²? 10⁻⁶? | Standard clock metric |
| 10 | **PhaseNoiseSpectralDensity** | L(f) for the closure event sequence. White phase noise or flicker? | PSD of phase deviations |

---

### New Module 3: `test_causal_structure.py` — Light Cone & Causality
*Inspired by: NASA JPL deep-space network timing; LIGO causal veto system*

**Why core:** The simultaneity claim in `test_closure_simultaneity.py` asserts
that light-crossing time exceeds step duration. But it doesn't map the *full*
causal structure — which vertex pairs are spacelike-separated, what the discrete
light cone looks like, whether face completions can be causally ordered. This is
the rigorous foundation for the nonlocality argument.

**Proposed Tests (~12):**

| # | Test | Question | Approach |
|---|------|----------|----------|
| 1 | **VertexCausalReachability** | From vertex V at step n, which vertices are reachable at step n+1 while respecting c? | Discrete light cone forward map |
| 2 | **CausalDiameter** | How many settlement ticks for a signal at c to traverse the full Field Chamber diagonal? | ceil(T_cross / T_step) |
| 3 | **SpacelikeSeparatedPairs** | Which vertex pairs are spacelike-separated within one settlement tick? These require nonlocal coordination. | Distance > c × T_step |
| 4 | **CausalOrderingOfFaceReads** | Do face completions follow causal ordering within an orbit, or do some complete acausally? | Compare face completion step to causal bound |
| 5 | **RetardedGreenFunction** | Perturbation at V₀, step 0 — at what step does it first affect each other vertex? Discrete Green function. | BFS on causal graph |
| 6 | **TimeFaceCausalStatus** | Are TIME faces (FACE_A7, FACE_B0) causally connected to all SPATIAL faces within one orbit? | Distance analysis |
| 7 | **NoSignalingVerification** | Marginals at Tet_A independent of Tet_B choices over N=1000 orbits. Numerical no-signaling check. | Statistical independence test |
| 8 | **CausalDiamondVolume** | For one settlement event: causal diamond volume (intersection of future + past light cones). | Vertex-step count |
| 9 | **NonlocalFraction** | Ratio of acausal face completions to total. Quantifies how much timing advantage requires nonlocal explanation. | Counting |
| 10 | **FrameIndependenceOfFaceReads** | Under Lorentz boost, does the face read accumulation pattern remain unchanged? | Boost transformation on step sequence |
| 11 | **CausalConsistencyAcrossOrbits** | Does the causal structure remain identical across orbits 1, 10, 100, 1000? No drift in causal diameter? | Orbit-by-orbit comparison |
| 12 | **InformationPropagationVelocity** | Measured information propagation speed through the traversal (bits/step × steps/second × meters/step). Compare to c. | Dimensional analysis |

---

### Core `__init__.py`

```python
# Core Timing Analysis — Foundational GFD timing mechanics
#
# These tests define how the GFD clock works. If any test here fails,
# the engine's timing claims are compromised.
#
# Modules:
#   test_closure_simultaneity  — Discrete state transitions, simultaneity
#   test_temporal_hierarchy    — Multi-scale frequency ladder
#   test_timing_jitter         — Statistical precision characterization
#   test_causal_structure      — Light cone and causality analysis
```

---

## ADVANCED: `timing_analysis_advanced/`

### New Module 4: `test_phase_coherence.py` — Geometric Phase Accumulation
*Inspired by: CERN beam phase lock; LIGO/Virgo interferometric phase tracking*

**Why advanced:** Berry phase is established in `quantum_foundations` as a static
property. These tests ask the dynamic question: does phase accumulate coherently
through the actual traversal? This extends the timing model into quantum
geometry territory — important but not load-bearing for the core engine.

**Proposed Tests (~10):**

| # | Test | Question |
|---|------|----------|
| 1 | **BerryPhasePerStep** | How much Berry phase accrues per settlement step? Constant or vertex-dependent? |
| 2 | **PhaseAccumulationOverOrbit** | Total Berry phase over one 8-vertex orbit. Equals 2π (spinor rotation)? |
| 3 | **PhaseCoherenceOver137Orbits** | Accumulated phase after 137 orbits — physically meaningful value? Resonance structure? |
| 4 | **PhaseSlipEvents** | Traversal configurations where Berry phase jumps discontinuously? Which digit sequences trigger slips? |
| 5 | **InterferenceVisibility** | Two paths reconverging at same vertex — phase difference? Visibility V = (I_max − I_min)/(I_max + I_min). |
| 6 | **PhaseAutocorrelation** | Per-step phase increments: random walk or coherent accumulation? |
| 7 | **AharonovBohmAnalog** | Does cumulative phase depend only on enclosed solid angle (topological) or on path details? |
| 8 | **SpinorPhaseReturn** | After how many orbits does total phase return to 0 (mod 2π)? Poincaré recurrence time? |
| 9 | **DecoherenceFromPhaseRandomization** | Random ±ε perturbation per step. Steps to coherence < 1/e? Compare to 10¹⁶ decoherence horizon. |
| 10 | **GeometricVsDynamicPhaseRatio** | Separate total phase into geometric (Berry) and dynamic (energy × time). Which dominates per orbit? |

---

### New Module 5: `test_spectral_analysis.py` — Frequency Domain Characterization
*Inspired by: CERN RF cavity analysis; LIGO sensitivity curves*

**Why advanced:** Every serious timing system gets a spectral characterization.
The closure event sequence, vertex transitions, and face completions all have
spectral content that has never been examined. This could reveal hidden structure
(octave patterns from base-8?) or confirm the expected noise profile.

**Proposed Tests (~10):**

| # | Test | Question |
|---|------|----------|
| 1 | **ClosureEventPowerSpectrum** | PSD of binary closure sequence (1 at closure, 0 otherwise). White? 1/f? Harmonic peaks? |
| 2 | **VertexTransitionSpectrum** | Vertex index as time series — power spectrum. Dominant frequency? |
| 3 | **TetrahedronSwitchingFrequency** | Spectrum of A/B switching. Expected ~50% duty cycle fundamental at f_settlement/2. |
| 4 | **OctaveStructure** | Power at octave intervals (powers of 2) reflecting base-8 arithmetic? |
| 5 | **OrbitCompletionHarmonics** | Orbit completion rate spectrum. Harmonics at f_settlement/⟨N_steps⟩? |
| 6 | **CrossSpectrumVertexAndTet** | Cross-spectral density between vertex index and tet membership. Coherence at what frequencies? |
| 7 | **SpectralFlatness** | Geometric mean / arithmetic mean of PSD. 1 = white noise, 0 = tonal. Where does closure fall? |
| 8 | **Spectrogram** | Windowed FFT over blocks of 100 digits. Stationary or evolving spectral character? |
| 9 | **NyquistFrequency** | Effective sampling rate of traversal. Nyquist corresponds to known physical frequency? |
| 10 | **NoiseFloor** | Minimum detectable signal above pi-digit randomness. Express as equivalent sensitivity. |

---

### New Module 6: `test_relativistic_timing.py` — Frame Transformations & Gravity
*Inspired by: NASA GPS corrections; Pound-Rebka; gravitational wave timing residuals*

**Why advanced:** The core timing model operates in flat space at Compton scale.
Real physics is curved. This module bridges the gap — GPS corrections, neutron
star surfaces, black hole horizons, gravitational wave strain sensitivity.
Important for connecting the engine to observational physics, but not required
for the engine to function.

**Proposed Tests (~12):**

| # | Test | Question |
|---|------|----------|
| 1 | **LorentzTimeDilation** | At v = 0.99c, settlements per second in moving frame? γ-factor consistency. |
| 2 | **TransverseDopplerEffect** | Transverse motion redshifts settlement frequency by γ even with no radial motion. |
| 3 | **GravitationalRedshiftEarth** | Settlement frequency difference: sea level vs. 10 km altitude. Settlements/year difference. |
| 4 | **GPSRelativisticCorrection** | Combined SR + GR correction for GPS orbit. Match the 38 μs/day correction? |
| 5 | **SchwarzschildSettlementProfile** | f_local = f_∞ × (1 − R_s/r)^(−1/2). Profile vs. r for solar mass. Divergence radius. |
| 6 | **NeutronStarSurfaceTiming** | Settlement frequency at surface of 1.4 M_sun, 10 km NS. Redshift factor. Extra settlements/s vs. infinity. |
| 7 | **CosmologicalRedshift** | f_obs = f_emit/(1+z). Settlements in first second after Big Bang (z ≈ 10¹⁰) vs. now. |
| 8 | **GravitationalWaveStrainSensitivity** | GW strain h modulates Field Chamber by δL = hL. At what strain does δf/f equal one settlement period? |
| 9 | **SagnacEffect** | Rotating Field Chamber: Sagnac phase shift = 4Aω/c². Match standard formula? |
| 10 | **EquivalencePrinciple** | Acceleration a produces same settlement shift as g = a (Rindler). Verify consistency. |
| 11 | **HorizonTimingParadox** | At event horizon: f → ∞ (distant observer) but f_local is normal. Local settlements per distant-observer second at r = 1.001 R_s? |
| 12 | **PoundRebkaAnalog** | Frequency shift between two Field Chambers at h = 22.5 m separation. Settlement count difference per year. |

---

### New Module 7: `test_quantum_clock.py` — Metrological Certification
*Inspired by: NIST optical lattice clocks; SI second redefinition; Ramsey interferometry*

**Why advanced:** The capstone. Treats the GFD timing system as a clock and evaluates
it against the same metrics used for atomic frequency standards. This is the
"certification exam" — it relies on all preceding modules and produces the final
verdict on the timing model's quality.

**Proposed Tests (~10):**

| # | Test | Question |
|---|------|----------|
| 1 | **QFactor** | Q = f/Δf using closure jitter as Δf. Compare to cesium (10¹⁰) and optical clocks (10¹⁵). |
| 2 | **FractionalFrequencyInstability** | σ_y at 1, 10, 137 orbit averaging. Improves as 1/√N? |
| 3 | **DickEffectAnalog** | Dead time from digit-0 events (no advancement). How does this degrade timing? |
| 4 | **RamseyFringeAnalog** | Face-read-Face pattern creates timing fringes? Fringe spacing? |
| 5 | **QuantumProjectionNoise** | For N parallel Field Chambers, timing uncertainty scales as 1/√N. Verify N = 1, 10, 100, 1000. |
| 6 | **SystematicShiftBudget** | All known systematics: (a) digit bias, (b) gravitational redshift, (c) Doppler, (d) blackbody analog. Total uncertainty? |
| 7 | **CesiumComparison** | f_settlement / f_Cs (9,192,631,770 Hz). Expressible in model constants? |
| 8 | **StrontiumComparison** | f_settlement / f_Sr (4.29×10¹⁴ Hz). Clean ratio? |
| 9 | **TimekeepingCapacity** | Bits of time information per electron per second = log₂(f_settlement) ≈ 66.7 bits. |
| 10 | **ClockComparisonProtocol** | Two independent traversals — frequency difference consistent with zero? (Same pi digits → same clock.) |

---

### Advanced `__init__.py`

```python
# Advanced Timing Analysis — Physics extensions of the GFD timing model
#
# These tests USE the established core timing model to explore broader physics.
# Failure here means "we have more to learn," not "the engine is broken."
#
# Modules:
#   test_phase_coherence      — Berry phase accumulation dynamics
#   test_spectral_analysis    — Frequency domain characterization
#   test_relativistic_timing  — GR, GPS corrections, curved spacetime
#   test_quantum_clock        — Metrological certification
#
# Prerequisites: All tests in timing_analysis/ (core) should pass first.
```

---

## Implementation Priority & Phasing

```
PHASE 1 — Foundation (Core)                  PHASE 2 — Physics
┌─────────────────────────────┐              ┌────────────────────────────────┐
│ timing_analysis/            │              │ timing_analysis/               │
│   test_temporal_hierarchy   │─────────────▶│   test_causal_structure        │
│   test_timing_jitter        │              │                                │
└─────────────────────────────┘              │ timing_analysis_advanced/      │
                                             │   test_relativistic_timing     │
                                             └────────────────────────────────┘

PHASE 3 — Advanced                           PHASE 4 — Capstone
┌─────────────────────────────┐              ┌────────────────────────────────┐
│ timing_analysis_advanced/   │              │ timing_analysis_advanced/      │
│   test_spectral_analysis    │─────────────▶│   test_quantum_clock           │
│   test_phase_coherence      │              │                                │
└─────────────────────────────┘              └────────────────────────────────┘
```

### Phase 1 — Foundation (Immediate)
Build the frequency ladder and characterize the jitter. Everything else depends
on these two modules being solid.

### Phase 2 — Physics (Near-term)
Causal structure resolves the simultaneity claim rigorously. Relativistic timing
connects to real-world measurements (GPS, Pound-Rebka).

### Phase 3 — Advanced (Medium-term)
Spectral analysis and phase coherence are independent explorations that could
yield surprising findings (hidden octave structure? coherent phase accumulation?).

### Phase 4 — Capstone (Long-term)
Quantum clock metrology is the final certification. Requires all other modules.

---

## Cross-Module Dependency Map

```
                    CORE                                    ADVANCED
    ┌────────────────────────────────┐     ┌────────────────────────────────┐
    │                                │     │                                │
    │  test_closure_simultaneity     │     │                                │
    │         (existing)             │     │                                │
    │              │                 │     │                                │
    │              ▼                 │     │                                │
    │  test_temporal_hierarchy ──────│────▶│  test_relativistic_timing      │
    │         │         │            │     │         │                      │
    │         ▼         │            │     │         │                      │
    │  test_timing_jitter            │     │  test_spectral_analysis        │
    │         │         │            │     │         │                      │
    │         ▼         ▼            │     │         │                      │
    │  test_causal_structure ────────│────▶│  test_phase_coherence          │
    │                                │     │         │                      │
    │                                │     │         ▼                      │
    │                                │     │  test_quantum_clock            │
    │                                │     │    (requires ALL above)        │
    │                                │     │                                │
    └────────────────────────────────┘     └────────────────────────────────┘
```

Key dependencies:
- **Temporal hierarchy** provides frequency values → everything references it
- **Timing jitter** feeds into causal structure (precision limits causal claims)
  and spectral analysis (jitter IS the spectral content)
- **Causal structure** is prerequisite for relativistic timing (flat-space first,
  then curve it)
- **Phase coherence** + spectral analysis both feed into quantum clock capstone

---

## Console Registration (`dfp_console.py`)

```python
"timing_analysis": {
    "name": "Timing Analysis",
    "type": "ENGINE",
    "description": "Core timing: closure simultaneity, frequency hierarchy, "
                   "jitter statistics, causal structure",
    "modules": [
        "gfd_model_v2.engine.timing_analysis.test_closure_simultaneity",
        "gfd_model_v2.engine.timing_analysis.test_temporal_hierarchy",
        "gfd_model_v2.engine.timing_analysis.test_timing_jitter",
        "gfd_model_v2.engine.timing_analysis.test_causal_structure",
    ]
},
"timing_analysis_advanced": {
    "name": "Timing Analysis (Advanced)",
    "type": "ENGINE",
    "description": "Advanced timing: phase coherence, spectral analysis, "
                   "relativistic effects, quantum clock metrology",
    "modules": [
        "gfd_model_v2.engine.timing_analysis_advanced.test_phase_coherence",
        "gfd_model_v2.engine.timing_analysis_advanced.test_spectral_analysis",
        "gfd_model_v2.engine.timing_analysis_advanced.test_relativistic_timing",
        "gfd_model_v2.engine.timing_analysis_advanced.test_quantum_clock",
    ]
},
```

---

## Test Count Summary

| Folder | Module | Tests | Status |
|--------|--------|-------|--------|
| **timing_analysis/** | `test_closure_simultaneity` | 11 | Existing |
| **timing_analysis/** | `test_temporal_hierarchy` | ~12 | Phase 1 |
| **timing_analysis/** | `test_timing_jitter` | ~10 | Phase 1 |
| **timing_analysis/** | `test_causal_structure` | ~12 | Phase 2 |
| | **Core subtotal** | **~45** | |
| **timing_analysis_advanced/** | `test_phase_coherence` | ~10 | Phase 3 |
| **timing_analysis_advanced/** | `test_spectral_analysis` | ~10 | Phase 3 |
| **timing_analysis_advanced/** | `test_relativistic_timing` | ~12 | Phase 2 |
| **timing_analysis_advanced/** | `test_quantum_clock` | ~10 | Phase 4 |
| | **Advanced subtotal** | **~42** | |
| | **GRAND TOTAL** | **~87** | |

---

## Key Physical Questions Answered by Each Folder

### Core (`timing_analysis/`) — "Is the clock correct?"
1. Is the timing model internally consistent across 24 orders of magnitude?
2. What is the precision floor? (Allan variance)
3. Does simultaneity survive causal analysis?
4. Which events are spacelike-separated and require nonlocal explanation?

### Advanced (`timing_analysis_advanced/`) — "What can the clock measure?"
5. Does Berry phase accumulate coherently over 137 orbits?
6. Is there hidden spectral structure in the closure sequence?
7. How does the timing model behave in curved spacetime?
8. What strain sensitivity would a GFD-based detector have?
9. How does the clock compare to cesium and optical standards?

---

## Contributor Guidance

### Working on Core
- **Read first:** `test_closure_simultaneity.py` — understand the baseline
- **Build on:** The constants and helpers in `common/`
- **Test with:** Full engine stress test suite must still pass
- **Review:** Changes here require review from engine maintainers

### Working on Advanced
- **Prerequisites:** All core timing tests pass
- **Freedom:** These modules are exploratory — negative findings are valuable
- **Dependencies:** May require numpy/scipy for FFT (spectral analysis)
- **Pattern:** Follow existing `GFDTest` base class with `name`, `question`,
  `reference_source`, `tolerance`, `derivation`, `commentary`, `model()`,
  `observations()`
