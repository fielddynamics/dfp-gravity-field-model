# BBP structure: the I Ching, the BBP formula and the stellated octahedron

This folder tests one question: **are the I Ching and the Bailey–Borwein–Plouffe (BBP) formula for π descriptions of the same object, the stellated octahedron?**

The theorems and their proofs are in [`PROOF.md`](PROOF.md). This file explains the findings in plain terms, says what is established and what is not, and maps each test to the statement it checks.

---

## 1. What is established

### The I Ching is the stellated octahedron

A trigram has three lines, each yin or yang. Reading the lines as three coordinates puts the eight trigrams at the eight corners of a cube. The I Ching's own organisation of the trigrams is then the geometry of the stellated octahedron:

| I Ching | Stellated octahedron |
|---|---|
| the 8 trigrams | the 8 corners of the cube |
| the father's family (Qian and three sons) and the mother's family (Kun and three daughters) | the two interlocking regular tetrahedra |
| the four opposite pairs (Heaven–Earth, Mountain–Lake, Thunder–Wind, Water–Fire) | the four body diagonals, crossing at the centre (the Field Origin) |
| father and mother, Qian and Kun | the two ends of the TIME axis |
| the 64 hexagrams | the 64 ordered pairs of corners |

All of this holds whichever line is taken as which coordinate. The I Ching also fixes that choice. The Shuo Gua ranks the children by the position of their distinctive line: bottom for the eldest, middle for the middle child, top for the youngest. In the Chinese text each child is obtained at the first, second or third "seeking" (一索, 再索, 三索), and for all six the ordinal is the line's position from the bottom. That ranking holds under only one assignment, bottom line = most significant bit, which is also the one behind Shao Yong's binary numbering (Theorem 1).

### BBP is the octahedron's formula for π

The BBP formula is

$$\pi = \sum_{k\ge0} \frac{1}{16^k}\left[\frac{4}{8k+1} - \frac{2}{8k+4} - \frac{1}{8k+5} - \frac{1}{8k+6}\right].$$

Its base is $16 = K^2$ and its period is $8 = 2^D$. Each of its terms sits at one of eight positions, $8k + 1$ to $8k + 8$, and position $j$ can be read as the corner labelled $j \bmod 8$.

BBP is not the only formula of this kind for π. Every member of a one-parameter family works (Adamchik and Wagon 1997). **New here is a proof that this family is all of them** (Theorem 2). The proof writes each term through seven logarithms, shows those logarithms are independent using the prime factorisation of numbers built from √2 and i, and applies Baker's theorem from number theory.

Given that, one condition from the octahedron picks out BBP: the TIME axis carries no weight, i.e. the father and mother are silent. The mother turns out to be silent in *every* formula of this kind; the father is silent in exactly one. **So exactly one formula for π leaves the TIME axis silent, and it is BBP** (Theorem 3). Silencing either of two other body diagonals leaves no formula at all, and the fourth leaves one that splits 3 + 1. Nothing else about the octahedron is assumed, yet BBP then turns out to have the rest of its structure:
- it uses exactly four corners, Mountain, Thunder, Fire and Lake;
- two of them come from each family;
- its weights sum to zero.

### Where π enters

Written as an integral, BBP has two factors.
- The roots $1 \pm i$ point at 45°. That factor produces π, as $4\arctan 1$.
- The roots $\pm\sqrt2$ cancel a leftover logarithm.

In the octahedron, √2 is the ratio of tetrahedron edge to cube edge, and 45° is the angle at which a tetrahedron edge crosses its cube face (Theorem 4). A single square also has both numbers, so this step shows how π enters but does not by itself need the full octahedron.

### The I Ching order writes out BBP

The family members can be read in order: the parent, then the children by rank. Each child's lines then give one BBP term, using two short rules:
- the weight is 2 × bottom + middle + top;
- the position advances by 3 when the top line is yang and by 1 when it is yin.

This reproduces BBP exactly in both families (Theorem 5). The three children can be ordered in six ways, and these correspond to the six symmetries of the octahedron that keep the TIME axis fixed. Only the I Ching's rank order gives π. The two rules were first found by matching BBP, but they do not depend on π: among all affine readings that meet the octahedron's structural conditions (closure, one orbit, TIME silence, two slots per family), the only one whose output is a named constant is this one, and the constant is π (Theorem 6). Stated relative to the reading order, the rule is: the first child's line counts double, and the last child's line sets the step.

### The BBP ladder reaches the trigrams directly

BBP can compute the digits of π at any position without computing the earlier ones. Since $8 = 2^3$ and $16 = 2^4$, the base-8 digits, one trigram each, can be read the same way:
- the ladder matches independently computed digits at 300 random positions up to 10,000, and at the millionth hexadecimal place it returns the published digits 26C65E52 (Bailey 2006);
- the closure walk driven by the ladder alone is the same walk, closing all 64 hexagrams at step 332;
- for bases that are not powers of 2, such as base 10, π has no ladder of this kind (Borwein, Borwein and Galway 2004).

---

## 2. What is not established

- **The class of readings.** Theorem 6 recovers the two rules within affine readings meeting structural conditions. That class is a choice; a reading outside it is not covered.
- **Formulas outside this kind.** The theorems cover formulas with base 16, period 8 and first-power denominators, and nothing else.
- **The walk's statistics.** Driven by π, the closure walk behaves statistically like a walk driven by well-mixed digits: it closes at a typical step, and it doesn't visit corners in the I Ching order. The case for π rests on the formula (Theorems 2 and 3), not on the walk's statistics.

---

## 3. Corrections to earlier research notes

These are documented by tests in this folder.

| Note | Statement | Finding |
|---|---|---|
| `why_pi_formal_derivation.md` | "No freedom exists": the geometry forces every BBP coefficient | Of the six symmetric relabellings of the axes, only one gives π. The order comes from the I Ching, not from the geometry alone (`test_reading_symmetry.py`). |
| `why_pi_formal_derivation.md` | the numerators come from an "agreement rule" | No agreement rule gives π, and none can. The rule used is ordered (`test_reading_weight_rule.py`). |
| `why_pi_formal_derivation.md` | closure (zero sum) is automatic and forces the series | Zero sum holds for all six relabellings, so it does not single out π (`test_reading_symmetry.py`). |
| `IChing_Solve_Synthesis.md` §3 | parity, the opposite pairs and the TIME-face order validate the encoding "only under" bottom = most significant bit | All three hold under all six encodings. The rank order and Shao Yong's numbering are what fix it (`test_iching_encoding_selection.py`). |
| `bbp_field_closure_synthesis.md` | constraint B ($K^3 = 2^{2D}$) has an integer solution only at $D = 3$ | It has one whenever 3 divides $D$: 6, 9, 12, … (noted in the earlier analysis; not a test here) |

---

## 4. The tests

Twenty-six further tests, which sharpen these results, are in [`extensions/`](extensions/README.md). Tests 23–26 apply the standard of a particle-physics analysis: pre-registered predictions ([`extensions/PREDICTIONS.md`](extensions/PREDICTIONS.md)), a trials factor, a power check, and look-elsewhere audits of GFD's particle formulas.

Every test module starts with a **Role** line, naming the statement it checks, and an **Expected** line, saying what a pass means. All tests are expected to pass.

| Test | Checks | Role |
|---|---|---|
| `test_octahedron_pi_theorems.py` | Theorems 1, 4, 5, with the family selection, exactly | proof |
| `test_bbp_completeness_proof.py` | Theorems 2 and 3, the main result, exactly | proof |
| `test_bbp_integral_mechanism.py` | Theorem 4: which factor of the integral gives π | proof |
| `test_iching_encoding_selection.py` | Theorem 1(e): what fixes the encoding | proof / correction |
| `test_reading_symmetry.py` | Theorem 5: only the rank order gives π | proof / correction |
| `test_iching_visit_order.py` | Theorem 5: the Shuo Gua sequence is the only documented order giving BBP in both families | proof |
| `test_reading_weight_rule.py` | Theorem 5 status: the weight rule is ordered | correction |
| `test_reading_rules_exact.py` | Theorem 5: 1 of 625 linear weight rules gives π; exact values of the other orders | proof |
| `test_shuo_gua_text.py` | Theorem 1: the ranks and opposites read from the Chinese text | proof |
| `test_bbp_octahedral_selection.py` | Theorem 3 remark: each octahedral condition selects BBP | proof |
| `test_bbp_pi_formula_family.py` | Theorem 2, numerically (PSLQ, 100 digits) | cross-check |
| `test_bbp_face_diagonal_reading.py` | √2 and 45° as octahedron ratios, with a square as control | supporting |
| `test_bbp_octahedral_prediction.py` | of seven named BBP constants, only π has the octahedral shape | supporting (exploratory) |
| `test_bbp_ladder_base8.py` | the BBP ladder gives base-8 digits at any position | supporting |
| `test_walk_from_bbp_ladder.py` | the closure walk from the ladder alone | supporting |
| `test_hexagram_closure_null.py` | 64-hexagram closure for π compared with random digits | control |
| `test_pi_walk_visit_order.py` | the π walk's order of first visits | control |

The helper modules are:
- `bbp_slots.py`: the slot series and the formula family;
- `bbp_ladder.py`: digit extraction;
- `closure_reading.py`: the face reading of `why_pi_formal_derivation.md`;
- `iching_orders.py`: the trigram arrangements, with sources.

**Run them.** From the repository root:

```bash
pip install -r requirements.txt          # includes mpmath and sympy
python -m gravity_field_model.engine_core.field_closure.bbp_structure.test_bbp_completeness_proof
python -m gravity_field_model.engine_core.field_closure.bbp_structure.test_octahedron_pi_theorems
```

Each module can be run the same way, and each runs in under ten seconds.

---

## Sources

- R. Wilhelm, *The I Ching or Book of Changes*, trans. C. F. Baynes (Princeton, 1950), Shuo Kua chs. 3, 5, 10.
- D. H. Bailey, P. B. Borwein, S. Plouffe, *Math. Comp.* 66 (1997) 903–913.
- V. Adamchik, S. Wagon, *Amer. Math. Monthly* 104 (1997) 852–855.
- A. Baker, *Mathematika* 13 (1966) 204–216.
- J. M. Borwein, D. Borwein, W. F. Galway, *Canad. J. Math.* 56 (2004) 897–925.
