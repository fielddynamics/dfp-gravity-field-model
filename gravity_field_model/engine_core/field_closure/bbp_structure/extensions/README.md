# Extensions: twenty-seven tests that take the results further

These tests build on [`../PROOF.md`](../PROOF.md). Each starts with a **Role** line, naming what it extends, and an **Expected** line, saying what a pass means. All twenty-seven pass. Tests 23–26 were pre-registered in [`PREDICTIONS.md`](PREDICTIONS.md), and two of their predictions failed; those tests record the outcome rather than being adjusted.

## What they add

### 1. Why pi, and not another constant

Silence on the TIME axis fixes one formula for *any* constant (test 04). What singles out π is the shape that formula takes.

| Test | Finding |
|---|---|
| 01 Slot span basis | Every base-16, period-8 formula, for any constant, evaluates to a rational combination of seven constants: π, ln 2, ln 3, ln 5, arctan(1/2), √2 ln(1+√2) and √2 arctan(1/√2). Two slots are elementary: $S_8 = 2\ln(16/15)$ and $S_4 = \tfrac12\ln(5/3)$. Only $S_8$, Kun's slot, contains ln 2. |
| 02 TIME-silent constants | Six of the seven constants can be written with the parents silent; ln 2 cannot. **Add closure (weights summing to zero) and only π remains.** |
| 03 Octahedral magnitude formulas | Of all 216 formulas with BBP's shape and magnitudes (TIME-silent, 2 + 2, weights ±{4, 2, 1, 1}), only BBP and its negative equal a single named constant, and that constant is π. |
| 04 TIME silence is generic | Every constant with a TIME-silent formula has exactly one. The uniqueness in Theorem 3 is therefore a property of the formula space. **What is particular to π is the octahedral shape of its unique formula.** |
| 05 Minimal period | In base 16, no formula for π exists with period 1 to 7 (PSLQ, coefficients up to $10^9$, 120 digits). Period $8 = 2^D$ is the first, and it returns BBP. |

### 2. What the result depends on

| Test | Finding |
|---|---|
| 06 Encoding invariance | The selection of BBP holds under all six line-to-bit encodings, and so does the 2 + 2 split. The encoding decides only *which* four trigrams BBP uses. The Shuo Gua's encoding gives Mountain, Thunder, Fire and Lake. |
| 07 Slot identification | Reading slot $j$ as vertex $j \bmod 8$, or as its complement, selects BBP. Counting the slots the other way round, or shifting them by one, selects the 3 + 1 formula $r = -\tfrac12$. The identification is the one real input. |
| 08 TIME axis canonical | Of the four body diagonals, only Qian–Kun (000–111) is fixed by every encoding. The TIME axis is singled out by the labels themselves, not by convention. |

### 3. The trigram-line reading (Theorem 5)

| Test | Finding |
|---|---|
| 09 Reading symmetry group | Of the 12 symmetries that keep the TIME axis, exactly two keep the π reading: the identity, and the inversion through the Field Origin that exchanges the two families. |
| 10 Step rule search | With the weight rule fixed, only one of 160 step rules works: step 2t + 1 starting from position 1. |
| 11 Line rule identities | The weight 2b + m + t is the label halved and rounded up, ⌈v/2⌉, which equals the yang count plus the bottom line. Under complement it becomes 4 − w = K − w. The step is 3 for odd labels and 1 for even. These are candidate forms for a derivation, not a derivation. |

### 4. The ladder and the walk

| Test | Finding |
|---|---|
| 12 Family ladders | Digit extraction works for every member of π's family, not only BBP. Fractional members are scaled to integers first. The ladder is a property of base 16; BBP's advantage is economy. |
| 13 Far octal ladder | Forty trigrams between positions 90,000 and 100,000, each taken from its own rung, all match an independent full-precision computation. |
| 14 Hex–octal windows | In 2,000 consecutive 12-bit windows, three hexadecimal digits from the ladder spell exactly four stored trigrams. |
| 15 Walk mod 7 | The walk's digit sum is fixed modulo 7 by π's prefix (casting out sevens), but agrees with it modulo 8 only one time in eight, which is chance. The walk's position is genuinely cumulative. |
| 16 Walk for other constants | π, ln 2, √2 and e all fall inside the random-digit range on the walk's closure step and chamber share. The walk does not single out π. |
| 17 Octal digit uniformity | π's first 10,000 trigrams, singly (p = 0.94) and in consecutive pairs (p = 0.80), are as evenly spread as random digits. |
| 27 The walk is π | The walk is a lossless re-encoding of π's digits: $d_n = (v_n - v_{n-1}) \bmod 8$ recovers all 10,000. Each step can be checked on its own against the BBP ladder: π's walk passes 200 of 200 checks, e's walk 24 (one in eight, as for unrelated digits). The 64 hexagram frequencies of both are as even as random digits. **The sequence identifies π exactly; the walk's statistics do not** (PROOF.md §10). |

### 5. The reading rules confirmed, and rotation

| Test | Finding |
|---|---|
| 21 Reading rules confirmed | Without using π: all affine readings meeting the structural conditions (closure, one orbit of 8, distinct slots, TIME silence, 2 + 2) give 704 formulas. Exactly two equal a multiple of a single basis constant, BBP (π) and 2·BBP. **The rule is unique: the first son read counts double, the last son read sets the step (3 or 1), start at 1. In the I Ching's rank order this is 2b + m + t and 2t + 1** (PROOF.md, Theorem 6). |
| 22 Rotation sense | The π reading is kept only by the identity and the central inversion, so it is achiral. But it fixes a sense of circulation about the TIME axis: eldest → middle → youngest runs counterclockwise seen from Qian. The sign of that sense is set by mapping bottom, middle and top to a right-handed x, y, z, which is a convention. |

### 6. Geometry and audit

| Test | Finding |
|---|---|
| 18 BBP integrand poles | $16 - y^8$ factors into four quadratics. The BBP numerator is exactly $-(y-1)(y^2+2)(y^2+2y+2)$: it cancels the poles $\pm i\sqrt2$ and $-1 \pm i$ and keeps $\pm\sqrt2$ and $1 \pm i$. That is one half of each of the octagon's two squares, the half facing the positive real axis. |
| 19 Hexagram parity | The Hamming distribution 8/24/24/8 is $8\binom{3}{h}$, which holds for any complete set of hexagrams. A hexagram crosses between the tetrahedra exactly when an odd number of lines change. The 8 hexagrams with all three lines changing are the body diagonals. |
| 20 Numerology audit | Among the 9 octahedral slot sets, only BBP's sums to 16 = K² (1 in 9). Among all 70 four-slot subsets, 7 sum to 16 (1 in 10). Constraint B of the synthesis ($K^3 = 2^{2D}$ only at D = 3) is false: it has 10 solutions with D ≤ 30. |

### 7. The standard of a particle-physics analysis

An experiment at CERN fixes its predictions and its statistics before it looks (blinding), corrects for the number of things it looked at (the trials factor, or look-elsewhere effect), shows that it could have seen an effect if one were there (a power check), and compares only with current measurements. Tests 23–26 apply that standard. Their predictions were committed before they were run; the outcomes, including the two that failed, are in [`PREDICTIONS.md`](PREDICTIONS.md).

| Test | Finding |
|---|---|
| 23 Dimension scan | In base $2^{D+1}$, period $2^D$, the poles of the slot integrand reach radius √2, and the pole $1+i$ that produces π, only when $2(D+1) = 2^D$: only at D = 3 (checked to D = 64). PSLQ finds no π formula at D = 1, 2, 4 and recovers BBP at D = 3. **BBP has no analogue in other dimensions of this family.** |
| 24 Pre-closure read, global significance | Ten pre-registered statistics of π's walk before closure: smallest local p = 0.33, global p = 0.97. A walk biased 60/40 towards staying in one tetrahedron is detected in 59% of trials. **The read before closure does not carry π's signature, and the analysis was sensitive enough to see a modest one.** |
| 25 m_p/m_e look-elsewhere | GFD's Form IV, $1836 + 21\alpha/(1+\alpha/2) - \alpha^2/4 - 3\alpha^3/2$, agrees with CODATA 2018 (−15 ppt) and 2022 (−0.8σ). Pre-registered: over 20% of fake targets would be fitted as closely. **Outcome: 2%; prediction failed.** Exploring afterwards: the one unlikely step is the denominator $1+\alpha/2$ (about 1 in 150); the α² and α³ terms add no evidence. With trials counted, about 2σ at most. |
| 26 sin²θ_W look-elsewhere | GFD's $(3/13)(1+\alpha/4+13\alpha^2/8) = 0.231210$ was matched to 0.23121(4). The PDG 2024 MS-bar value is 0.23129(4): **the formula is 2.0σ low.** The same grammar has 9 formulas within 1σ of the new value (10 or more pre-registered: failed) and fits every fake value tried; $(3/13)(1+\alpha/4+8\alpha^2)$ fits the new value by changing one coefficient. |

## The picture these tests give

The case that BBP is the stellated octahedron's formula for π rests on three things:
- the formula space has exactly one free direction (Theorem 2);
- silence on the TIME axis removes it (Theorem 3);
- π is the only basis constant whose silent formula also closes, with the octahedral 2 + 2 shape (tests 02–04).

The ladder belongs to the whole family (test 12). The walk does not distinguish π from other constants (tests 16–17). Several numerical readings are weaker than the theorems (test 20).

The standard of tests 23–26 separates two kinds of result. The mathematics (Theorems 2–6, and test 23) is proved or computed exactly and needs no statistics. The links to physics (the walk, the particle formulas) are where evidence must be weighed: the walk shows no signal, and the particle formulas, judged against fake targets and current data, are at most a 2σ coincidence (m_p/m_e) and a fit that now misses (sin²θ_W).

Two things remain open:
- **The class of readings.** The weight and step rules are recovered by Theorem 6 within affine readings. The choice of that class remains an input.
- **Combinations of constants.** Uniqueness among them is open. The closed, TIME-silent values form a 5-dimensional space, and π is its only basis direction.

## Run

```bash
python -m gravity_field_model.engine_core.field_closure.bbp_structure.extensions.test_02_time_silent_constants
```

Each test runs in under ten seconds. Tests 13, 14 and 23 take about ten seconds each.
