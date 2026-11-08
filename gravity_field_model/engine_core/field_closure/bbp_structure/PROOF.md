# The I Ching and the BBP formula as the stellated octahedron

**Theorems and proofs.** Every statement below is checked exactly by the tests named in §8. The checks use integer and rational arithmetic, exact algebra in $\mathbb{Q}(\sqrt2, i)$ and symbolic integration. The one result used without a machine check is Baker's theorem on linear forms in logarithms, a standard theorem of number theory.

---

## 0. The result in one paragraph

Label the eight vertices of a cube with the eight I Ching trigrams. The Shuo Gua's ranking of the six children fixes which line is which coordinate (Theorem 1). With that labelling, the two parents, Qian and Kun, sit at the ends of the stellated octahedron's TIME axis.

Now take every formula for π of the form

$$\pi \;=\; \sum_{k=0}^{\infty} \frac{1}{16^{k}} \sum_{j=1}^{8} \frac{w_j}{8k+j}, \qquad w_j \text{ rational}, \tag{$\ast$}$$

and read the term with denominator $8k+j$ as belonging to the vertex labelled $j \bmod 8$. None of these formulas gives the mother's corner any weight, and exactly one also leaves the father's corner empty: the Bailey–Borwein–Plouffe (BBP) formula (Theorems 2 and 3). That one condition implies the rest of the BBP formula's octahedral structure:
- it uses exactly four vertices;
- two of them lie in each tetrahedron;
- its weights sum to zero.

---

## 1. Conventions

**Trigrams.** A trigram has three lines, bottom, middle and top, each yang (1, unbroken) or yin (0, broken).

**Vertices.** The trigram with lines $(\ell_b, \ell_m, \ell_t)$ is the cube vertex $(2\ell_b - 1,\ 2\ell_m - 1,\ 2\ell_t - 1) \in \{-1,+1\}^3$. Its label is $4\ell_b + 2\ell_m + \ell_t$, so the bottom line is the most significant bit. Theorem 1(e) shows that this choice is forced by the Shuo Gua.

| Label | Lines (b, m, t) | Trigram | Shuo Gua role (ch. 10) | Tetrahedron | On the TIME axis |
|---|---|---|---|---|---|
| 7 | 1 1 1 | Qian ☰ Heaven | father | father's (TetA) | yes |
| 4 | 1 0 0 | Zhen ☳ Thunder | eldest son | father's (TetA) | |
| 2 | 0 1 0 | Kan ☵ Water | middle son | father's (TetA) | |
| 1 | 0 0 1 | Gen ☶ Mountain | youngest son | father's (TetA) | |
| 0 | 0 0 0 | Kun ☷ Earth | mother | mother's (TetB) | yes |
| 3 | 0 1 1 | Xun ☴ Wind | eldest daughter | mother's (TetB) | |
| 5 | 1 0 1 | Li ☲ Fire | middle daughter | mother's (TetB) | |
| 6 | 1 1 0 | Dui ☱ Lake | youngest daughter | mother's (TetB) | |

**The text.** The Shuo Gua (section 10) names each child by the ordinal of a "seeking" (索): 震一索而得男, "Zhen: at the first seeking, a son"; 坎再索, at the second; 艮三索, at the third; and likewise 巽, 離 and 兌 for the daughters. For all six children this ordinal is the position of the child's one distinctive line, counted from the bottom (`test_shuo_gua_text.py` checks this against the Chinese text). Section 3 pairs the opposites: 天地, 山澤, 雷風, 水火 (heaven–earth, mountain–lake, thunder–wind, water–fire).

**The stellated octahedron.** This is the compound of the two regular tetrahedra whose vertices are vertices of the cube. Its TIME axis is the body diagonal through $(1,1,1)$ and $(-1,-1,-1)$, i.e. through labels 7 and 0. The Field Origin is the centre.

**Slots.** For $j = 1, \dots, 8$, the slot series is $S_j = \sum_{k \ge 0} 16^{-k}/(8k+j)$. Slot $j$ belongs to the vertex labelled $j \bmod 8$: slots 1–7 are vertices 1–7, and slot 8 is vertex 0, Kun.

**Formulas.** A formula for a number $c$ is a rational vector $w = (w_1, \dots, w_8)$ with $\sum_j w_j S_j = c$. A slot is *active* if $w_j \ne 0$. Formulas of type $(\ast)$ are exactly these. The type is fixed by the octahedron's numbers: base $16 = K^2$ and period $8 = 2^D$, with $K = 4$ and $D = 3$.

**The BBP formula** is $w_{\text{BBP}} = (4, 0, 0, -2, -1, -1, 0, 0)$, i.e. $\pi = \sum_k 16^{-k}\big[\tfrac{4}{8k+1} - \tfrac{2}{8k+4} - \tfrac{1}{8k+5} - \tfrac{1}{8k+6}\big]$ (Bailey, Borwein and Plouffe 1997).

**The Adamchik–Wagon vector** is $a = (8, -8, -4, -8, -2, -2, 1, 0)$.

---

## 2. Theorem 1: the trigram system is the stellated octahedron

**Theorem 1.**
- **(a)** The map from trigrams to labels is a bijection onto the cube's 8 vertices.
- **(b)** The father's family (Qian and the three sons) and the mother's family (Kun and the three daughters) are the vertex sets of the cube's two inscribed regular tetrahedra.
- **(c)** The Shuo Gua opposites (ch. 3: Qian–Kun, Gen–Dui, Zhen–Xun, Kan–Li) are the antipodal pairs $c \mapsto -c$, i.e. the four body diagonals. Each one joins the two families through the Field Origin. Qian and Kun are the TIME apices.
- **(d)** The 64 hexagrams are the 64 ordered pairs of vertices, 16 for each ordered pair of families.
- **(e)** Statements (a)–(d) hold for all six ways of assigning the three lines to the three bits. Exactly one assignment gives the sons, in rank order (eldest, middle, youngest), the labels 4, 2, 1: bottom = most significant bit. The same assignment is the only one that makes Shao Yong's Fu Xi numbering (Qian 1, Dui 2, …, Kun 8) count down in binary.

**Proof.**
- **(a)** Each of the $2^3$ line patterns is a different vertex.
- **(b)** Two vertices that differ in $h$ coordinates are at squared distance $4h$. Within a family, the number of yang lines has fixed parity, so two distinct members differ in exactly two lines. They are therefore at squared distance 8: the four members are mutually equidistant and form a regular tetrahedron.
- **(c)** Each pair is line-for-line opposite, so $c \mapsto -c$. Flipping all three lines changes the parity, so each pair joins the two families.
- **(d)** $8^2 = 64$ and $4^2 = 16$.
- **(e)** Parity, complements and distances do not depend on which line is which bit. Each son has one yang line, so its label is $2^{\text{(bit of that line)}}$. The rank order therefore gives 4, 2, 1 exactly when bottom, middle and top are bits 2, 1, 0. Shao Yong's order 7, 6, …, 0 needs the same assignment. ∎

---

## 3. Theorem 2: the formulas for π of type $(\ast)$ are exactly one family

**Theorem 2.** The only rational linear relations among $S_1, \dots, S_8$ are the multiples of $\sum_j a_j S_j = 0$. Hence the formulas for π of type $(\ast)$ are exactly

$$w(r) = w_{\text{BBP}} + r\,a, \qquad r \in \mathbb{Q}.$$

That every $w(r)$ is a formula for π was found by Adamchik and Wagon (1997). New here is that there are no others.

**Proof.** The proof has four steps.

**Step 1 (partial fractions).** Since $1/(16 - y^8) = \sum_{k\ge0} y^{8k}/16^{k+1}$ on $[0,1]$, integrating term by term gives

$$S_j = 16 \int_0^1 \frac{y^{j-1}}{16 - y^8}\, dy.$$

The integrand has simple poles at $y = \sqrt2\,\omega$, for the eight roots of unity $\omega^8 = 1$. The residue at each pole is $-(\sqrt2\omega)^j / 128$. Therefore

$$S_j = -\frac18 \sum_{\omega^8 = 1} (\sqrt2\,\omega)^j\, L_\omega, \qquad L_\omega = \int_0^1 \frac{dy}{y - \sqrt2\,\omega} = \operatorname{Log}\!\Big(1 - \frac{\bar\omega}{\sqrt2}\Big).$$

**Step 2 (seven logarithms).** The eight numbers $1 - \bar\omega/\sqrt2$, for $\omega = e^{i\pi n/4}$ with $n = 0, \dots, 7$, factor as

$$\tfrac{\sqrt2-1}{\sqrt2},\quad \tfrac{1+i}{2},\quad \tfrac{\sqrt2+i}{\sqrt2},\quad \tfrac{(1+i)(2-i)}{2},\quad \tfrac{\sqrt2+1}{\sqrt2},\quad \tfrac{(1-i)(2+i)}{2},\quad \tfrac{\sqrt2-i}{\sqrt2},\quad \tfrac{1-i}{2}.$$

So each $L_\omega$ is a rational combination of the seven logarithms

$$\Lambda = \big(\, i\pi,\ \log 2,\ \log(1+\sqrt2),\ \log(2+i),\ \log(2-i),\ \log(\sqrt2+i),\ \log(\sqrt2-i) \,\big).$$

For example, $L_{e^{i\pi/4}} = \log\frac{1+i}{2} = -\tfrac12\log 2 + \tfrac14 i\pi$. The test checks each factorisation exactly. It also checks each combination against the integral to 60 digits, which fixes the branch of every logarithm. With Step 1, every $S_j$ is a combination of $\Lambda$ whose coefficients lie in $\mathbb{Q}(\sqrt2, i)$.

**Step 3 (the seven logarithms are independent).** Suppose $\sum_k n_k \Lambda_k = 0$ with integers $n_k$. Exponentiating gives

$$(-1)^{n_1}\, 2^{n_2}\, (1+\sqrt2)^{n_3}\, (2+i)^{n_4}\, (2-i)^{n_5}\, (\sqrt2+i)^{n_6}\, (\sqrt2-i)^{n_7} = 1$$

in the ring of integers of $\mathbb{Q}(\sqrt2, i) = \mathbb{Q}(\zeta_8)$. Prime ideals factor uniquely in that ring, so each prime must appear with total exponent 0:

- **The prime above 2.** $2$ is a unit times $(1 - \zeta_8)^4$. All the other factors have odd norm. So $n_2 = 0$.
- **The primes above 5.** $5$ has order 2 modulo 8, so it splits into two primes of norm 25. $2 + i$ and $2 - i$ each have norm 25, so each generates one of them. The two primes are distinct because $(2+i)(2-i) - \big((2+i) + (2-i)\big) = 1$. So $n_4 = n_5 = 0$.
- **The primes above 3.** Likewise, $\sqrt2 \pm i$ have norm 9 and $3$ has order 2 modulo 8. They are distinct because $3(\sqrt2+i)(\sqrt2-i) - \big((\sqrt2+i) + (\sqrt2-i)\big)^2 = 1$. So $n_6 = n_7 = 0$.
- **What is left** is $(-1)^{n_1}(1+\sqrt2)^{n_3} = 1$. Since $|1 + \sqrt2| > 1$, $n_3 = 0$. The original relation is then $n_1\, i\pi = 0$, so $n_1 = 0$.

So $\Lambda$ is linearly independent over $\mathbb{Q}$. Baker's theorem (1966) states that logarithms of algebraic numbers which are linearly independent over $\mathbb{Q}$ are also linearly independent over the field of all algebraic numbers. So $\Lambda$ is independent over that field too.

**Step 4 (solving for the relations).** By Step 3, a rational relation $\sum_j q_j S_j = 0$ holds exactly when, for every $\Lambda_k$, its total coefficient is zero. Each coefficient is a number in $\mathbb{Q}(\sqrt2, i)$. Writing it in the basis $1, \sqrt2, i, i\sqrt2$ gives 4 rational equations per logarithm: 28 equations in the 8 unknowns $q_j$. The coefficient matrix has rank 7, so the solutions form a line, spanned by $a$. Since $\pi = -i \cdot (i\pi)$, the same linear system can be solved for π. Its particular solution is $w_{\text{BBP}}$. ∎

---

## 4. Theorem 3: the TIME axis selects BBP, and the rest follows

**Theorem 3.** No formula for π of type $(\ast)$ uses Kun's slot (slot 8). Exactly one also leaves Qian's slot (slot 7) empty, so that both TIME apices are silent. It is the BBP formula. Its active slots are 1, 4, 5 and 6: Gen (Mountain), Zhen (Thunder), Li (Fire) and Dui (Lake). Gen and Zhen are in the father's tetrahedron, and Li and Dui in the mother's. The weights $4, -2, -1, -1$ sum to zero.

**Proof.** By Theorem 2, every formula is $w(r)$. Its slot-8 weight is $0 + 0 \cdot r = 0$ for every $r$, and its slot-7 weight is $r$. So both apices are silent exactly when $r = 0$. The tetrahedron memberships are read off the table in §1. ∎

So the mother is silent in every formula for π of this kind, and the father in exactly one.

**Remark (the other octahedral conditions).** Each of the other octahedral conditions also selects BBP on its own:

| Condition | Solutions in the family $w(r)$ |
|---|---|
| Weights sum to zero | sum is $-15r$, so only $r = 0$ |
| Exactly four active slots | $r = 0$ (slots 1, 4, 5, 6) or $r = -\tfrac12$ (slots 2, 3, 4, 7) |
| Four slots, two in each tetrahedron | only $r = 0$ (the $r = -\tfrac12$ formula splits 3 + 1 and uses Qian's slot 7) |

Silencing a body diagonal other than the TIME axis asks two equations of the one parameter $r$, and in general has no solution:

| Diagonal silenced | Formulas for π |
|---|---|
| Kun–Qian (TIME) | one: $r = 0$, BBP |
| Gen–Dui | one: $r = -\tfrac12$ (four slots, split 3 + 1, weights summing to $\tfrac{15}{2}$) |
| Kan–Li | none |
| Xun–Zhen | none |

The compact base $-4$ formula $\pi = \sum_k (-\tfrac14)^k\big[\tfrac{2}{4k+1} + \tfrac{2}{4k+2} + \tfrac{1}{4k+3}\big]$ is the member $r = -\tfrac14$. It is not TIME-silent.

---

## 5. Theorem 4: where π comes from inside BBP

**Theorem 4.**

$$4S_1 - 2S_4 - S_5 - S_6 \;=\; 16 \int_0^1 \frac{y - 1}{(y^2 - 2)(y^2 - 2y + 2)}\, dy \;=\; \pi.$$

In partial fractions:
- the factor $y^2 - 2y + 2 = (y-1)^2 + 1$, with roots $1 \pm i$ at 45°, gives $4\arctan 1 = \pi$, plus a logarithm $+\ln 4$;
- the factor $y^2 - 2$, with roots $\pm\sqrt2$, gives $-\ln 4$, which cancels it.

**Proof.** Exact integration. ∎

In the stellated octahedron, $\sqrt2$ is the ratio of tetrahedron edge to cube edge. 45° is the angle at which a tetrahedron edge crosses the cube face that contains it. A single square has both numbers as well, so this theorem shows where π enters, but it does not by itself require the full octahedron.

---

## 6. Theorem 5: BBP written in the trigram lines, and why the I Ching order matters

**Theorem 5.** List the father's tetrahedron as Qian, then the sons in rank order: Zhen, Kan, Gen. Give the $i$-th row (counting from 0) the weight $\pm(2\ell_b + \ell_m + \ell_t)$, with $+$ for Qian and $-$ for the sons. Place it at position $p_i$, where $p_0 = 1$ and $p_{i+1} = p_i + 2\ell_t + 1$, taking $\ell_t$ from row $i$. This reproduces BBP:

| Row | Lines (b, m, t) | Position | Step to next | Weight |
|---|---|---|---|---|
| Qian | 1 1 1 | 1 | 3 | +4 |
| Zhen | 1 0 0 | 4 | 1 | −2 |
| Kan | 0 1 0 | 5 | 1 | −1 |
| Gen | 0 0 1 | 6 | 3 | −1 |

The four steps sum to 8, one full orbit. The mother's tetrahedron gives the same table: list Kun, then the daughters in rank order (Xun, Li, Dui), and flip every line. Kun flips to Qian, and each daughter flips to the son of the same rank.

The three children can be ordered in $3! = 6$ ways, and these are exactly the six symmetries of the octahedron that fix the TIME axis. All six orders give weights summing to zero, but only the rank order gives π. The other five give, for example, $\ln(675/256) + 2\arctan 2 \approx 3.1838$ for the order (Zhen, Gen, Kan) and $\ln(50625\sqrt{15}/65536) + 2\arctan 2 \approx 3.3102$ for (Kan, Gen, Zhen); every one is at least 0.04 from π.

**Proof.** Direct computation and exact integration. ∎

**Status.** The main result (Theorems 1–3) does not use Theorem 5. The two rules of Theorem 5 are not fitted to π: Theorem 6 recovers them from structural conditions alone.

---

## 6a. Theorem 6: the reading rules, recovered without assuming π

**Admissible readings.** Read the father's tetrahedron with Qian first and the three sons in any order. Give each row
- a weight that is an affine function of its lines, $a\ell_b + c\ell_m + d\ell_t + e$;
- a step that is an affine function of its lines, $\alpha\ell_b + \beta\ell_m + \gamma\ell_t + \delta$.

Start at any position $p_0 \in \{0, \dots, 7\}$, and put $+w$ for Qian and $-w$ for each son at the running positions. Call the reading *admissible* if it meets these structural conditions, none of which mentions π:
- weights and steps are positive;
- closure: Qian's weight equals the sum of the sons' weights, so the weights sum to zero;
- one orbit: the four steps sum to $2^D = 8$;
- the four positions are distinct slots;
- TIME silence: no slot falls on vertex 0 or 7;
- chamber balance: two slots fall in each tetrahedron.

**Theorem 6.** Take coefficients $a, c, d \in \{0..4\}$, $e \in \{-2..2\}$ and $\alpha, \beta, \gamma, \delta \in \{0..3\}$, over all six orders of the sons. Then:

- **(a)** Closure forces $e = 0$, so the weight is linear in the lines. Qian's weight is $a + c + d + e$, and the sons' weights sum to $a + c + d + 3e$.
- **(b)** The admissible readings produce 704 distinct formulas. Exactly two of them equal a rational multiple of a single basis constant (test 01): BBP, which is π, and twice BBP. No admissible formula equals a multiple of ln 2, ln 3, ln 5, arctan(1/2), √2 ln(1+√2) or √2 arctan(1/√2).
- **(c)** In every order of the sons, the readings that give π follow one rule, stated relative to the reading order. The weight is the line sum plus the line of the *first* son read. The step is $1 + 2\times$(the line of the *last* son read). The start is position 1.
- **(d)** In the I Ching's rank order (eldest first, whose distinctive line is the bottom one), this rule is exactly the weight $2\ell_b + \ell_m + \ell_t$ and the step $2\ell_t + 1$ of Theorem 5.

**Proof.**
- **(a)** follows from the weights listed in the statement.
- **(b)** and **(c)** are an exact enumeration (`extensions/test_21_reading_rules_confirmed.py`).
- **(d)** In rank order, the first son is Zhen, whose line is the bottom one, and the last is Gen, whose line is the top one. ∎

So the rules of Theorem 5 are the unique admissible reading whose output is a single named constant, and that constant is π. The class of affine readings and the structural conditions are inputs. The rules within that class are not.

## 7. Scope

| | |
|---|---|
| **Proved** | The I Ching trigram system is the stellated octahedron, with an encoding fixed by the Shuo Gua (Theorem 1). π has exactly a one-parameter family of formulas of type $(\ast)$ (Theorem 2). The TIME axis selects the BBP formula, and its four slots, 2 + 2 split and zero sum follow (Theorem 3). |
| **Used without machine check** | Baker's theorem (1966). Standard facts on how primes split in $\mathbb{Q}(\zeta_8)$: the prime 3 or 5 has order 2 modulo 8, so it splits into two primes. |
| **Inputs** | The formula type $(\ast)$: base $16 = K^2$, period $8 = 2^D$, first-power denominators. Reading slot $j$ as vertex $j \bmod 8$. |
| **Characterised, within a class** | The two rules of Theorem 5: unique among affine readings meeting the structural conditions (Theorem 6). The class itself is a choice. |
| **Not claimed** | Anything about formulas for π outside type $(\ast)$. |

---

## 8. Where each statement is checked

| Statement | Test file | Metric prefix |
|---|---|---|
| Theorem 1 | `test_octahedron_pi_theorems.py` | `Thm 1(a)` … `Thm 1(e)` |
| Theorem 1(e), against the synthesis's claims | `test_iching_encoding_selection.py` | |
| Theorem 1(c), (e), against the Chinese text | `test_shuo_gua_text.py` | |
| Theorem 2 (proof, Steps 1–4) | `test_bbp_completeness_proof.py` | `Step 1` … `Step 4` |
| Theorem 2 (numerical cross-check, PSLQ) | `test_bbp_pi_formula_family.py` | |
| Theorem 3, and the body-diagonal table | `test_bbp_completeness_proof.py` | `Thm 3` |
| Theorem 3 remark | `test_bbp_octahedral_selection.py`, `test_octahedron_pi_theorems.py` | `Thm 3` |
| Theorem 4 | `test_bbp_integral_mechanism.py`, `test_octahedron_pi_theorems.py` | `Thm 4` |
| Theorem 5 | `test_octahedron_pi_theorems.py`, `test_reading_symmetry.py`, `test_iching_visit_order.py`, `test_reading_weight_rule.py` | `Thm 5` |
| Theorem 5: the rule search and the exact values | `test_reading_rules_exact.py` | |
| Theorem 6 | `extensions/test_21_reading_rules_confirmed.py` | |

---

## 9. Further results (the `extensions/` tests)

Twenty-eight further tests ([`extensions/README.md`](extensions/README.md)) sharpen the statements above.

- **Uniqueness is generic; the shape is not.** Fixing $w_7 = 0$ leaves at most one formula for *any* constant, because the only relation among the slots (Theorem 2) involves $S_7$. What is particular to π is that its unique TIME-silent formula has the octahedral shape (test 04).
- **Closure singles out π among the basis constants.** Every formula of type $(\ast)$ evaluates in the rational span of π, ln 2, ln 3, ln 5, arctan(1/2), √2 ln(1+√2) and √2 arctan(1/√2) (test 01). Of these seven, six have TIME-silent formulas, and only π has one whose weights sum to zero (test 02).
- **Every octahedral arrangement of BBP's magnitudes was tried.** Of the 216 formulas with BBP's shape and magnitudes, only ±BBP equals a single named constant (test 03).
- **Period 8 is the minimum.** In base 16, π has no formula with period 1 to 7 within the PSLQ bound $10^9$ (test 05).
- **The one real input is the identification of slot with vertex.** The selection does not depend on the line-to-bit encoding (test 06), and the TIME axis is the one diagonal every encoding fixes (test 08). Reading slot $j$ as vertex $-j \bmod 8$ instead of $j \bmod 8$ selects the 3 + 1 formula $r = -\tfrac12$ (test 07).
- **A sense of rotation, but not a handedness.** The π reading is kept by the identity and the central inversion only (test 09). Because it has a centre of inversion, it is achiral. Yet it is not kept by the 120° turns about the TIME axis, and its mirror images do not give π, so it fixes one sense of circulation about that axis: eldest, middle, youngest runs counterclockwise seen from Qian. Axial vectors are unchanged by inversion, so this sense is compatible with the reading's symmetry. Its sign, however, is set by assigning bottom, middle and top to a right-handed $x, y, z$, which is a convention (test 22).
- **Where π comes from, more sharply.** The BBP numerator is $-(y-1)(y^2+2)(y^2+2y+2)$. It cancels four of the eight poles of the slot integrand and keeps $\pm\sqrt2$ and $1 \pm i$ (test 18).
- **Only three dimensions.** Generalise BBP to base $2^{D+1}$ and period $2^D$. The poles of the slot integrand are the roots of $y^{2^D} = 2^{D+1}$, at radius $2^{(D+1)/2^D}$. The radius is $\sqrt2$, and the poles include the Gaussian integer $1+i$ that produces π, exactly when $2(D+1) = 2^D$, i.e. only at $D = 3$. PSLQ finds no formula for π at $D = 1, 2, 4$ (coefficients up to $10^6$) and recovers BBP at $D = 3$ (test 23). The condition $2(D+1) = 2^D$ is the one GFD uses for spatial uniqueness; here it is the condition for a Gaussian-integer pole.
- **The walk before closure, at a blind-analysis standard.** Ten statistics of π's pre-closure segment, fixed in advance (`extensions/PREDICTIONS.md`), give a smallest local p of 0.33 and a global p of 0.97 after the trials factor. The same battery detects a walk with a 60% tendency to stay in one tetrahedron in 59% of trials, so a modest real effect would have been seen (test 24).

## 10. The sequence that drives the walk

This section states exactly in what sense the closure walk "is π", so that no ambiguity remains between the formula, the digits and the walk's statistics.

**Definitions.** Let $d_0 = 3$ and let $d_1, d_2, \ldots \in \{0,\ldots,7\}$ be the base-8 digits of π, so $\pi = \sum_{n\ge0} d_n 8^{-n}$. The **walk** is
$$v_n = (d_0 + d_1 + \cdots + d_n) \bmod 8, \qquad n \ge 0,$$
a sequence of trigrams (vertices of the cube). The **hexagrams** are the pairs $h_n = (v_{n-1}, v_n)$, $n \ge 1$. The walk **closes** at the least $N$ with $\{h_1, \ldots, h_N\}$ equal to all $64$ pairs; for π, $N = 332$.

Three levels must be kept apart:
- **the rule** that produces the number (Theorems 2–6),
- **the sequence** of its digits and the walk built from them,
- **the statistics** of that walk.

**Theorem 2–3, restated as a selection.** Among formulas of type $(\ast)$, those that are TIME-silent, closed and split $2+2$ across the families evaluate to a rational multiple of a single basis constant only for π, and the formula is BBP; the I Ching's rank order is the only order of the children that writes it out (Theorems 3, 5, 6; tests 02–04, 21). *The rule selects π.*

**Proposition 7 (the walk is the sequence).** The map $\Phi : (d_n)_{n\ge0} \mapsto (v_n)_{n\ge0}$ is a bijection from digit sequences with $d_0 = 3$ to walks with $v_0 = 3$. Its inverse is
$$d_n = (v_n - v_{n-1}) \bmod 8 \quad (n \ge 1).$$
*Proof.* $v_n - v_{n-1} \equiv d_n \pmod 8$ and $0 \le d_n \le 7$. $\square$

So the walk of π loses nothing: it is π, re-encoded as a path on the cube.

**Proposition 8 (each step is checkable on its own).** For every $n \ge 1$,
$$v_n - v_{n-1} \equiv d_n \pmod 8,$$
and $d_n$ is computable from the BBP formula alone, without $d_1, \ldots, d_{n-1}$ (§6; `bbp_ladder.py`). Hence any proposed walk $w$ can be tested at any step $n$ independently of all other steps. If $w$ is not π's walk, it fails at every step where its increment differs from $d_n$. For the walk of an unrelated constant the increments agree with π's digits about one time in eight, so $k$ independent checks accept it with probability about $8^{-k}$. For e, 24 of 200 checks pass (0.12), and π's walk passes all 200 (test 27).

**Proposition 9 (the statistics are those of random digits).** If the digits were independent and uniform, $(v_n)$ would be a uniform random walk on $\mathbb Z_8$; each $v_n$ would be uniform and independent of $d_{n+1}$, so every hexagram would have frequency $1/64$, and the closure time would be close to the coupon-collector value $64 H_{64} \approx 304$. π's walk agrees with this model in every statistic tested:
- the closure step (test `test_hexagram_closure_null.py`);
- digit and pair frequencies (test 17);
- ten pre-registered properties of the pre-closure walk, with a trials factor (test 24);
- the 64 hexagram frequencies (test 27);
- five balance measures over 100,000 digits, pre-registered: π drifts from balance by about $\sqrt n$, as random digits do (test 28).

So do the walks of ln 2, √2 and e (tests 16, 27). This is empirical, not a theorem. Even normality of π in base 8, which is unproved, would not by itself imply it, because $v_n$ depends on the whole prefix of digits and not on a block of fixed length.

**Corollary (where the identification lives).**
1. *By the rule:* the stellated octahedron, read by its own conditions, selects π (Theorems 2–6).
2. *By the sequence:* the walk is π's digits (Proposition 7), and any step can be verified against π alone (Proposition 8).
3. *Not by the statistics:* frequencies, closure time and the other aggregate properties of the walk are those of random digits (Proposition 9), and do not distinguish π from other constants.

In one line: **the sequence is π, exactly and verifiably. The walk's statistics are ordinary, so they are not where the evidence for π lies.**

## References

- R. Wilhelm, *The I Ching or Book of Changes*, trans. C. F. Baynes (Princeton University Press, 1950), Shuo Kua chs. 3 and 10.
- A. Baker, "Linear forms in the logarithms of algebraic numbers I", *Mathematika* 13 (1966) 204–216.
- D. H. Bailey, P. B. Borwein, S. Plouffe, "On the rapid computation of various polylogarithmic constants", *Math. Comp.* 66 (1997) 903–913.
- V. Adamchik, S. Wagon, "A simple formula for π", *Amer. Math. Monthly* 104 (1997) 852–855.
- J. M. Borwein, D. Borwein, W. F. Galway, "Finding and excluding b-ary Machin-type individual digit formulae", *Canad. J. Math.* 56 (2004) 897–925.
- D. A. Marcus, *Number Fields* (Springer, 1977), ch. 3: the splitting of primes in cyclotomic fields.
