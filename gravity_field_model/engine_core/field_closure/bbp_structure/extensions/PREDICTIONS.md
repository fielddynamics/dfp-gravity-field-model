# Pre-registered predictions for tests 23–26

Written and committed **before** tests 24–26 were coded or run. The commit that adds this file is the timestamp. Each test will report the outcome against the prediction here, whether or not it matches.

Test 23 is the exception: a PSLQ scan for D = 1, 2, 4, 5 was run first, as exploration, before this file was written. Its prediction is stated here for completeness, not as a blind test.

## Why pre-register

A particle-physics analysis fixes its selection, its statistics and its significance threshold before it looks at the signal region ("blinding"), so that the result cannot be tuned to the data. The research in this repository has mostly worked the other way round: a pattern is found, then explained. That is legitimate exploration, but it does not count as evidence at the level a collider experiment requires. These four tests apply the stricter standard.

## Test 23: only D = 3 gives π (dimension scan)

Generalise BBP to base $2^{D+1}$ and period $2^D$.

- **Prediction (theorem):** the roots of $y^{2^D} = 2^{D+1}$ lie at radius $\sqrt2$, and so include the Gaussian integer $1+i$ that produces π (Theorem 4), only when $2(D+1) = 2^D$, i.e. only at D = 3. This will be checked exactly for D = 1 to 64.
- **Prediction (numerical):** PSLQ finds no formula for π at D = 1, 2, 4 (coefficients up to $10^6$), and finds one at D = 3 as a positive control.

## Test 24: the pre-closure read of π's walk, with a trials factor

The walk before closure (steps 0 to 332 for π) is described as the read of the stellated octahedron. Ten statistics of that segment are fixed here, before looking:

1. closure step;
2. TetA share of visited vertices;
3. TIME-axis share (Qian or Kun);
4. body-diagonal jumps (v → 7 − v);
5. self-loops (v → v);
6. longest run inside one tetrahedron;
7. step at which all eight trigrams have appeared;
8. χ² of the eight trigram counts;
9. Kendall τ between the order of first visits and the order Qian, Zhen, Kan, Gen, Kun, Xun, Li, Dui;
10. tetrahedron crossings (consecutive vertices in different tetrahedra).

Each walk is compared over its own pre-closure segment. Local p-values are two-sided, from 20,000 random walks. The global p-value is the probability that a random walk's smallest local p is as small as π's.

- **Prediction:** no local p below 0.01; global p above 0.05. That is, the pre-closure read is statistically indistinguishable from a read driven by random digits.
- **Power check (also predicted):** a walk whose digits are biased to stay in one tetrahedron 60% of the time instead of 50% is detected (global p < 0.01) in most trials. If it is not, the battery is too weak to be informative and the test fails.

## Test 25: look-elsewhere audit of the proton–electron mass ratio formulas

Research note `32_proton_electron_mass_ratio_breakthrough.md` gives
$m_p/m_e = 1836 + 21\alpha/(1+\alpha/2) - \alpha^2/4 - 3\alpha^3/2$ (Form IV), agreeing with CODATA to about 15 parts per trillion. Each correction term was added after the previous residual was seen.

- **Prediction:** with the same grammar (bulk 1836, three α-correction terms, coefficients from a fixed menu of small framework rationals), fake targets placed at random within ±1 ppm of the true value are fitted about as well as the true value. The fraction of fake targets fitted at least as well as the real one will exceed 0.2. If so, the agreement carries no evidential weight beyond the first term.

## Test 26: look-elsewhere audit of the weak mixing angle formula

Research note `33_weinberg_angle_planck_mass_from_K4.md` gives
$\sin^2\theta_W = \tfrac{3}{13}(1 + \alpha/4 + 13\alpha^2/8) = 0.231210$, compared there with the MS-bar value 0.23121(4).

- **Prediction:** the current PDG value (2024) differs from the one used. The formula will be more than 1.5σ from it. With the same grammar, more than ten menu formulas lie within 1σ of the current value, so a formula of this form can be found for either value.
