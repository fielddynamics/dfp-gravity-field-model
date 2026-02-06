# Contribution Scoring Framework

A guide for assessing the scientific value of a test's findings.

**The Core Question**: Does this test teach us something we didn't know, confirm something important, or open doors to new understanding?

---

## The Golden Rule

**If the test disappeared, would our understanding of the system be diminished?**

A test with high contribution score answers "yes" emphatically. A test with low contribution score could be removed without losing insight.

---

## The Four Scoring Dimensions (100 points total)

Every test is scored on four dimensions that measure its scientific contribution.

| Dimension | Points | What It Measures |
|-----------|--------|------------------|
| **Discovery Value** | 0-40 | Does this reveal something new? |
| **Precision & Rigor** | 0-20 | How confident are we in the finding? |
| **Cross-Domain Impact** | 0-20 | Does this connect multiple areas? |
| **Falsifiability & Predictions** | 0-20 | Does this make testable predictions? |
| **Total** | **0-100** | |

---

## Dimension 1: Discovery Value (0-40 points)

This is the most important dimension. What does this test tell us that we didn't know before?

### Scoring Guide

| Score | Level | Description | Example |
|-------|-------|-------------|---------|
| **36-40** | **Profound** | Answers a fundamental unsolved problem in physics. Could reshape understanding of the field. | "Why is alpha = 1/137?" answered from geometric first principles |
| **28-35** | **Major Discovery** | Reveals a previously unknown relationship, pattern, or mechanism. Publishable result. | New pattern: all GW exponents expressible as ratios of k, d, 2^d |
| **20-27** | **Significant** | Confirms a theoretical prediction with compelling new evidence. Strengthens a hypothesis. | GFD predicts 2 GW polarizations, LIGO confirms exactly 2 |
| **12-19** | **Valuable** | Extends known physics to a new domain or context. Useful generalization. | Applying GFD patterns from particle physics to stellar mechanics |
| **5-11** | **Incremental** | Minor extension or refinement of known results. | Better precision on a known ratio |
| **0-4** | **Routine** | Verification of well-established results. No new insight. | Confirming Kepler's third law (again) |

### Key Questions

- Would a physicist be surprised by this finding?
- Does this explain something previously unexplained?
- Is this the first time this pattern/relationship has been documented?
- Does this resolve a tension or puzzle in the data?

### Examples

**High Discovery (35 points):**
```
The quadrupole coefficient 32/5 in GW power can be decomposed as:
- 32 = 2^(k+1) = 2^5
- 32 = k * 2^d = 4 * 8
- 5 = k+1
This is the first documentation that a GR coefficient has TWO independent
GFD decompositions, suggesting deep geometric structure.
```

**Medium Discovery (20 points):**
```
The ISCO radius factor of 6 equals the number of SPATIAL faces (3 per tet x 2).
This is a new observation, but it's a single numerical coincidence without
multiple independent confirmations.
```

**Low Discovery (5 points):**
```
Confirmed that neutron star density is ~3x nuclear density.
This is well-known from astrophysics textbooks. No new insight.
```

---

## Dimension 2: Precision & Rigor (0-20 points)

How confident should we be in this finding? Is it rock-solid or suggestive?

### Scoring Guide

| Score | Level | Description | Example |
|-------|-------|-------------|---------|
| **18-20** | **Definitive** | Multiple independent confirmations. Precision <0.1%. Statistical significance >5 sigma. | 8 GW coefficients all match GFD patterns (p < 10^-8) |
| **14-17** | **Strong** | Good confirmation with precision <1%. Clear pattern. | Chirp exponent 3/5 = d/(k+1) exact to numerical precision |
| **10-13** | **Solid** | Reasonable confirmation, precision <5%. Pattern evident but could use more data. | Hulse-Taylor agrees with GR to 0.3% |
| **5-9** | **Suggestive** | Interesting pattern but precision is limited or sample size small. | Single numerical coincidence noted |
| **0-4** | **Inconclusive** | Too much uncertainty to draw conclusions. Needs more work. | Pattern might exist but error bars overlap |

### Key Questions

- How many independent data points confirm this pattern?
- What is the numerical precision?
- Could this be a coincidence? What's P(random)?
- Are there systematic errors that could explain the result?

### Statistical Significance Test

For pattern-matching tests, calculate coincidence probability:

```
If matching to ~10 GFD numbers (k, d, k+1, 2^d, k!, etc.) 
over a range of ~100 plausible values:
  P(single random match) = 10/100 = 10%
  P(8 matches by chance) = (0.1)^8 = 10^-8 (highly significant!)
```

---

## Dimension 3: Cross-Domain Impact (0-20 points)

Does this finding connect different areas of physics? Unification is the holy grail.

### Scoring Guide

| Score | Level | Description | Example |
|-------|-------|-------------|---------|
| **18-20** | **Unifying** | Connects 3+ previously separate domains through a common principle. | Same geometric factor appears in GW, QED, and cosmology |
| **14-17** | **Bridging** | Connects two domains that were previously separate. | Chirp mass exponent 3/5 also appears in particle mass ratios |
| **10-13** | **Suggestive Link** | Hints at connection worth investigating. Pattern seen in one domain might apply to another. | 3/8 = d/2^d in GW; should check if it appears in tunneling |
| **5-9** | **Domain-Specific** | Insight is valuable but limited to one domain. | Better understanding of neutron star structure |
| **0-4** | **Isolated** | No apparent connection to other domains. | Technical detail with no broader implication |

### Key Questions

- Does the same pattern/ratio appear in multiple domains?
- Does this explain a connection that was previously mysterious?
- Does this suggest where to look next in other domains?
- Would specialists in other fields care about this finding?

### Cross-Domain Checklist

When you find a pattern, check if it appears in:

| Domain | Key Quantities to Check |
|--------|------------------------|
| Gravitational Waves | Chirp mass, strain, frequency, ISCO |
| Particle Physics | Mass ratios, coupling constants, decay rates |
| Quantum Mechanics | Tunneling rates, spin, entanglement |
| Cosmology | Hubble constant, dark energy, CMB temperature |
| Black Holes | Schwarzschild radius, Hawking temperature, entropy |
| Nuclear Physics | Binding energy, magic numbers, shell structure |

---

## Dimension 4: Falsifiability & Predictions (0-20 points)

Does this finding make testable predictions? Good science predicts.

### Scoring Guide

| Score | Level | Description | Example |
|-------|-------|-------------|---------|
| **18-20** | **Experimentally Testable** | Makes specific predictions that could be tested with current or near-future experiments. | "GFD predicts no scalar GW modes; next-gen detectors can test this" |
| **14-17** | **Observationally Testable** | Predictions could be checked with future astronomical observations. | "Pattern predicts specific ringdown frequency ratio" |
| **10-13** | **Constraining** | Narrows parameter space meaningfully. Rules something out. | "If pattern holds, then X cannot exceed Y" |
| **5-9** | **Directional** | Suggests what to look for next. Points toward future tests. | "Should check if this pattern appears in binary pulsars" |
| **0-4** | **Descriptive Only** | Documents what is, without predicting what could be. | "We observe this coincidence" (no prediction) |

### Key Questions

- What would falsify this finding?
- What specific prediction does this make?
- How could we test this prediction?
- What observation would strengthen or weaken our confidence?

### The Falsifiability Test

A finding has high predictive value if you can complete:

> "If this pattern is real, then we predict ______. If we observe ______ instead, the pattern is falsified."

**Example (High Falsifiability):**
> "If ISCO = 6GM/c^2 because 6 = SPATIAL faces, then for Kerr black holes the factor should change with spin in a way that reflects face geometry. If ISCO varies continuously with spin without geometric correspondence, the pattern is coincidental."

---

## Score Interpretation

| Total Score | Assessment | What It Means |
|-------------|------------|---------------|
| **90-100** | **Profound** | Potential paradigm shift. Should be highlighted prominently. |
| **70-89** | **Significant** | Materially advances understanding. High-value test. |
| **50-69** | **Valuable** | Solid contribution. Worth keeping and building on. |
| **30-49** | **Incremental** | Useful but not groundbreaking. Supporting evidence. |
| **0-29** | **Routine** | Verification only. Consider if needed. |

---

## Recording Contribution Scores

### The Properties

```python
class MyProbingTest(Test):
    # ... other properties ...
    
    # Contribution assessment
    contribution_score = 72
    contribution_notes = (
        "Discovery: 30/40 - First documentation of 8 GW coefficients matching GFD patterns. "
        "Precision: 15/20 - All matches are exact to numerical precision, P(random) < 10^-8. "
        "Cross-Domain: 15/20 - Suggests checking particle physics for same patterns. "
        "Falsifiability: 12/20 - Predicts patterns should appear in ringdown; testable. "
        "TOTAL: 72/100 - Significant contribution, advances GW-geometry connection."
    )
```

### The Format

Contribution notes should follow this structure:

```
"Discovery: X/40 - <specific finding and why it's novel>. "
"Precision: X/20 - <confidence level and statistical support>. "
"Cross-Domain: X/20 - <connections identified or suggested>. "
"Falsifiability: X/20 - <predictions made or constraints set>. "
"TOTAL: X/100 - <one-sentence summary of contribution value>."
```

---

## Contribution vs Quality: Two Different Scores

| Score | Measures | High Score Means |
|-------|----------|------------------|
| `audit_score` (quality) | How well the test is written | Clear, pedagogical, well-documented |
| `contribution_score` | How valuable the findings are | Novel, rigorous, connected, predictive |

**A test can have:**
- High quality, low contribution: Beautifully written but verifies the obvious
- Low quality, high contribution: Important finding but poorly documented
- High quality, high contribution: The goal! Important finding, well presented

**Both scores matter.** Quality determines if others can understand the test. Contribution determines if the test is worth understanding.

---

## Examples: Full Contribution Assessments

### Example 1: High Contribution (82 points)

```python
class QuadrupoleCoefficient(Test):
    """Probe the coefficient 32/5 in GW power formula."""
    
    contribution_score = 82
    contribution_notes = (
        "Discovery: 35/40 - First finding that 32 has TWO independent GFD decompositions "
        "(2^(k+1) AND k*2^d). This is not mere numerology; the double decomposition "
        "suggests deep geometric structure in the quadrupole formula. "
        "Precision: 17/20 - Both decompositions are mathematically exact. Combined with "
        "7 other GW coefficient matches, statistical significance is very high. "
        "Cross-Domain: 15/20 - The factor 32 should be checked in other radiation "
        "formulas (electromagnetic, scalar fields). Suggests unified origin. "
        "Falsifiability: 15/20 - Predicts that octupole and higher multipole coefficients "
        "should also decompose into GFD numbers. Testable with calculation. "
        "TOTAL: 82/100 - Significant finding. The double decomposition is striking."
    )
```

### Example 2: Medium Contribution (58 points)

```python
class ISCORadiusSixFaces(Test):
    """Probe the factor of 6 in r_ISCO = 6*GM/c^2."""
    
    contribution_score = 58
    contribution_notes = (
        "Discovery: 22/40 - Observation that 6 = SPATIAL faces is new but is a single "
        "coincidence. Need more evidence to distinguish from numerology. "
        "Precision: 12/20 - Match is exact, but single data point. Would be stronger "
        "if photon sphere (factor 3) and other radii also match GFD numbers. "
        "Cross-Domain: 14/20 - Also found photon sphere factor 3 = d, suggesting a "
        "pattern. Should check other characteristic radii in black hole physics. "
        "Falsifiability: 10/20 - For Kerr black holes, ISCO varies with spin. Could "
        "test if variation tracks any geometric quantity. Partially testable. "
        "TOTAL: 58/100 - Valuable observation. Needs more investigation to confirm."
    )
```

### Example 3: Low Contribution (25 points)

```python
class HulseTaylorDecay(Test):
    """Verify Hulse-Taylor binary matches GR."""
    
    contribution_score = 25
    contribution_notes = (
        "Discovery: 5/40 - This is well-established physics. The 0.3% agreement between "
        "Hulse-Taylor and GR has been known since the 1990s. No new insight. "
        "Precision: 12/20 - High precision verification (0.3%), well-documented sources. "
        "Cross-Domain: 3/20 - Confirms GR works, but no new cross-domain connections. "
        "Falsifiability: 5/20 - This is verification, not prediction. Establishes that "
        "GR is correct, which is baseline for probing, but no new predictions. "
        "TOTAL: 25/100 - Routine verification. Valuable as foundation, not as discovery."
    )
```

---

## The Contribution Self-Assessment Process

After running tests in the sandbox, assess contribution as follows:

### Step 1: Ask the Discovery Question

> "What does this test tell us that we didn't know before?"

If the answer is "nothing new," Discovery score is 0-10.
If the answer is "a new pattern," Discovery score is 20-30.
If the answer is "solves a mystery," Discovery score is 30-40.

### Step 2: Assess Confidence

> "How sure are we that this finding is real, not coincidence?"

Calculate P(random) if applicable. Check precision. Count independent confirmations.

### Step 3: Look for Connections

> "Does this finding appear in or connect to other domains?"

Check the cross-domain checklist. Note any patterns that should be investigated elsewhere.

### Step 4: Identify Predictions

> "What does this finding predict that we could test?"

Complete the falsifiability statement. Note specific predictions.

### Step 5: Compute Total and Write Notes

Sum the four dimensions. Write contribution_notes explaining each score.

---

## When to Update Contribution Scores

- **After initial sandbox development**: First assessment
- **After finding cross-domain connections**: May increase Cross-Domain score
- **After predictions are tested**: May increase or decrease Falsifiability score
- **After replication**: May increase Precision score
- **After publication/external validation**: May increase Discovery score

---

## Summary: The Contribution Mindset

When assessing contribution, channel your inner skeptical physicist:

1. **Discovery**: "So what? What's actually new here?"
2. **Precision**: "How do you know it's not coincidence?"
3. **Cross-Domain**: "Does this connect to anything else?"
4. **Falsifiability**: "What would prove you wrong?"

A test that can answer all four questions convincingly has earned a high contribution score.

---

*Document version: 1.0*
*Last updated: 2026-02-04*
*Location: framework/CONTRIBUTION_SCORING_FRAMEWORK.md*
