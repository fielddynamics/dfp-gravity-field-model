"""
Subspace Packing: Nuclear Physics Observations
===============================================

GFD Model V2

HONESTY STATEMENT:
This module verifies STANDARD NUCLEAR PHYSICS data and makes observations
about patterns. GFD provides terminology (Field Chamber, Tet B, k-packing)
but does not DERIVE nuclear physics from geometry.

WHAT IS VERIFIED (standard physics):
- Binding energy curve shape (rises to Fe-56, falls after)
- Be-8 instability (positive Q-value for alpha decay)
- Triple-alpha process (energy release C-12 > 3*He-4)
- Alpha decay ejects He-4 (k=4 nucleons)
- Neutron-proton mass difference (~1.3 MeV)

PATTERN OBSERVATIONS (not derivations):
- He-4 has A=4 (happens to equal k)
- Fe-56 has A=56=14*4 (happens to be a k-multiple)
- Some magic numbers are k-multiples, some are not

The k=4 comes from the simplex theorem. The OBSERVATION that stable nuclei
like He-4 have A=4 is a COINCIDENCE or CORRELATION, not an explanation.
Nuclear stability is explained by the shell model, not by k-alignment.

TEST GROUP GOALS:
This module explores nuclear stability patterns, distinguishing between physical
explanations (shell model, Q-values) and numerical observations (k-multiples).
Students learn to recognize pattern-matching vs causal derivation: the shell
model explains stability, while k-alignment merely describes some patterns.

Audience: Undergraduate nuclear physics students.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, HBAR, ELECTRON_MASS,
    K_CLOSURE, M_E,
    is_k_multiple, k_factor,
    MAGIC_NUMBERS, DOUBLY_MAGIC,
    MASS_RATIO_PROTON_ELECTRON,
    R_E,
)


# =============================================================================
# CONSTANTS
# =============================================================================

MEV_TO_JOULES = 1.60218e-13

# Binding energies per nucleon (MeV) from AME2020
BINDING_ENERGY = {
    'H-2': 1.11, 'He-3': 2.57, 'He-4': 7.07, 'Li-6': 5.33, 'Li-7': 5.61,
    'Be-8': 7.06, 'C-12': 7.68, 'N-14': 7.48, 'O-16': 7.98,
    'Fe-56': 8.79, 'Ni-62': 8.79, 'U-238': 7.57,
}

HALF_LIVES = {
    'Be-8': 8.19e-17,  # Extremely unstable
    'C-14': 1.81e11,   # Relatively stable
    'U-238': 1.41e17,  # Very long-lived
}

ALPHA_DECAY_ENERGY = {
    'Po-210': 5.41, 'Ra-226': 4.87, 'U-238': 4.27,
}


# =============================================================================
# TEST 1: k=4 FROM SIMPLEX THEOREM (Model Definition)
# =============================================================================

class K4PackingGeometry(Test):
    """
    Verify k=4 is the simplex closure number for d=3.

    HONESTY: This is a geometric definition, not a physics derivation.
    The simplex theorem says d+1 points minimally enclose d dimensions.
    """
    audit_score = 79
    audit_notes = None
    future_questions = (
        "Q1: Is the k=4 = He-4 correspondence physically meaningful or merely numerical "
        "coincidence, and how could we distinguish between these possibilities? "
        "(Answering would improve Question by +4 points: addresses core interpretive issue) "
        "Q2: How does the shell model independently explain He-4 stability through "
        "doubly-magic closure at Z=N=2? "
        "(Answering would improve Derivation by +3 points: standard physics explanation) "
        "Q3: What other physics theories have attempted to connect geometry with "
        "nuclear structure? "
        "(Answering would improve Commentary by +2 points: broader context)"
    )
    name = "k=4 Simplex Theorem"
    question = (
        "Why does geometry require exactly 4 points (tetrahedron) to minimally "
        "enclose 3D space? Is this mathematical fact alone sufficient to explain "
        "why He-4 (also 4 nucleons) is exceptionally stable?"
    )
    reference = "Geometry"
    tolerance = 0.01
    level = Level.CRITICAL
    commentary = (
        "The simplex theorem states d+1 points minimally enclose d-dimensional "
        "space. For d=3, this gives k=4 (tetrahedron). GFD DEFINES k=4 as the "
        "'closure number'. This is geometry, not physics. The observation that "
        "He-4 has A=4 is a COINCIDENCE that GFD notes, not explains."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY: Simplex theorem for d dimensions.")
            .equation("Minimal enclosure requires d+1 points.")
            .equation("For d=3: k = 3 + 1 = 4")
            .step("k=4 is the tetrahedron vertex count.")
            .step("GFD DEFINES this as the closure constant.")
            .step("NOTE: This does not EXPLAIN why He-4 is stable.")
            .step("Nuclear shell model explains He-4 stability (doubly magic).")
            .conclude("k = 4 by geometric definition.")
        )

    def model(self) -> Model:
        k = K_CLOSURE
        tetrahedron_vertices = 4
        he4_A = 4
        return (
            Model()
            .add("k (closure number)", k)
            .add("Tetrahedron vertices", tetrahedron_vertices)
            .add("He-4 mass number", he4_A)
            .add("All equal", 1.0 if k == tetrahedron_vertices == he4_A else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("k (closure number)", 4)
            .add("Tetrahedron vertices", 4)
            .add("He-4 mass number", 4)
            .add("All equal", 1.0)
        )


# =============================================================================
# TEST 2: BINDING ENERGY CURVE (Standard Nuclear Physics)
# =============================================================================

class BindingEnergyCurve(Test):
    """
    Verify binding energy curve rises to Fe-56, falls after.

    HONESTY: This is measured nuclear data. Standard physics.
    """
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Why does the binding curve show saw-tooth fine structure superimposed on "
        "the smooth SEMF trend? "
        "(Answering would improve Commentary by +3 points: shell and pairing effects) "
        "Q2: How does each term in the semi-empirical mass formula (volume, surface, "
        "Coulomb, asymmetry, pairing) shape the curve? "
        "(Answering would improve Derivation by +3 points: term-by-term understanding) "
        "Q3: At what mass number does the Coulomb term begin to dominate over the volume term? "
        "(Answering would improve Model Output by +2 points: quantitative crossover)"
    )
    name = "Binding Energy Curve Shape"
    question = (
        "Why does the binding energy curve rise from light nuclei to iron, "
        "then fall for heavy nuclei? What competition between attractive "
        "strong force and repulsive Coulomb force shapes this curve?"
    )
    reference = "Nuclear Physics (AME2020)"
    tolerance = 0.05
    level = Level.CRITICAL
    commentary = (
        "The binding energy curve is well measured. It rises from light nuclei "
        "to Fe-56 (8.79 MeV/nucleon), then falls for heavy nuclei. This is "
        "EXPLAINED by the semi-empirical mass formula, not by k-packing."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUCLEAR DATA: Binding energies from AME2020.")
            .step("He-4: BE/A = 7.07 MeV/nucleon")
            .step("C-12: BE/A = 7.68 MeV/nucleon")
            .step("O-16: BE/A = 7.98 MeV/nucleon")
            .step("Fe-56: BE/A = 8.79 MeV/nucleon (PEAK)")
            .step("U-238: BE/A = 7.57 MeV/nucleon")
            .step("Curve rises He-4 -> Fe-56, falls Fe-56 -> U-238.")
            .step("EXPLAINED by semi-empirical mass formula (volume, surface,")
            .step("Coulomb, asymmetry, pairing terms).")
            .conclude("Binding curve verified. Standard nuclear physics.")
        )

    def model(self) -> Model:
        be_he4 = BINDING_ENERGY['He-4']
        be_c12 = BINDING_ENERGY['C-12']
        be_o16 = BINDING_ENERGY['O-16']
        be_fe56 = BINDING_ENERGY['Fe-56']
        be_u238 = BINDING_ENERGY['U-238']

        increasing = 1.0 if be_he4 < be_c12 < be_o16 < be_fe56 else 0.0
        decreasing = 1.0 if be_fe56 > be_u238 else 0.0

        return (
            Model()
            .add("He-4 BE/A (MeV)", be_he4)
            .add("Fe-56 BE/A (MeV)", be_fe56)
            .add("U-238 BE/A (MeV)", be_u238)
            .add("Rises to Fe-56", increasing)
            .add("Falls after Fe-56", decreasing)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("He-4 BE/A (MeV)", 7.07)
            .add("Fe-56 BE/A (MeV)", 8.79)
            .add("U-238 BE/A (MeV)", 7.57)
            .add("Rises to Fe-56", 1.0)
            .add("Falls after Fe-56", 1.0)
        )


# =============================================================================
# TEST 3: BE-8 INSTABILITY (Standard Nuclear Physics)
# =============================================================================

class Be8Instability(Test):
    """
    Verify Be-8 is unstable despite high BE/A.

    HONESTY: Be-8 instability is explained by the positive Q-value for
    alpha decay. Standard nuclear physics, not a GFD prediction.
    """
    audit_score = 88
    audit_notes = None
    future_questions = (
        "Q1: Why is BE/A misleading as a stability criterion, and what makes Q-value "
        "the correct measure for decay energetics? "
        "(Answering would improve Question by +3 points: corrects common misconception) "
        "Q2: How does the Be-8 decay width (Gamma ~ 6 eV) relate to its femtosecond lifetime "
        "through the uncertainty principle? "
        "(Answering would improve Derivation by +3 points: quantum mechanics connection) "
        "Q3: What other nuclei are 'unbound' like Be-8 and decay immediately after formation? "
        "(Answering would improve Audience Accessibility by +2 points: broader examples)"
    )
    name = "Be-8 Instability"
    question = (
        "Why is beryllium-8 unstable in 8x10^-17 seconds despite having high "
        "binding energy per nucleon? What does the positive Q-value for alpha "
        "decay reveal about total vs per-nucleon binding?"
    )
    reference = "Nuclear Physics (Q-value)"
    tolerance = 0.20
    level = Level.STANDARD
    commentary = (
        "Be-8 has high binding energy per nucleon (7.06 MeV) but decays "
        "instantly to 2 alpha particles. EXPLANATION: The Q-value for "
        "Be-8 -> 2*He-4 is positive (+92 keV). The products have more total "
        "binding than the parent, so decay is energetically favorable. "
        "This is standard nuclear physics, not k-alignment."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUCLEAR PHYSICS: Be-8 decay energetics.")
            .step("Be-8 total BE: 8 x 7.06 = 56.48 MeV")
            .step("2*He-4 total BE: 2 x 4 x 7.07 = 56.56 MeV")
            .equation("Q-value = 56.56 - 56.48 = +0.08 MeV")
            .step("Positive Q-value means decay is favorable.")
            .step("CONCLUSION: Be-8 unstable due to Q > 0 for alpha decay.")
            .step("This is NOT explained by 8 = 2k. It's explained by Q-value.")
            .conclude("Be-8 unstable due to positive Q-value. Standard physics.")
        )

    def model(self) -> Model:
        half_life = HALF_LIVES['Be-8']
        be_per_nucleon = BINDING_ENERGY['Be-8']
        he4_be = BINDING_ENERGY['He-4']

        be8_total = 8 * be_per_nucleon
        two_alpha_total = 2 * 4 * he4_be
        q_value = two_alpha_total - be8_total

        return (
            Model()
            .add("Be-8 half-life (s)", half_life)
            .add("Be-8 BE/A (MeV)", be_per_nucleon)
            .add("Q-value (MeV)", q_value)
            .add("Q > 0 (decay favorable)", 1.0 if q_value > 0 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Be-8 half-life (s)", 8.19e-17)
            .add("Be-8 BE/A (MeV)", 7.06)
            .add("Q-value (MeV)", 0.092)
            .add("Q > 0 (decay favorable)", 1.0)
        )


# =============================================================================
# TEST 4: TRIPLE-ALPHA PROCESS (Standard Nuclear Physics)
# =============================================================================

class TripleAlphaPathway(Test):
    """
    Verify triple-alpha process releases energy.

    HONESTY: The energy release is measured. Hoyle resonance enables it.
    Standard nuclear astrophysics.
    """
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: How does the Hoyle state at 7.65 MeV in C-12 enable the triple-alpha process "
        "that would otherwise be impossibly slow? "
        "(Answering would improve Derivation by +4 points: resonance enhancement mechanism) "
        "Q2: Why is the triple-alpha process considered evidence for fine-tuning or "
        "anthropic selection in physics? "
        "(Answering would improve Commentary by +3 points: deeper significance) "
        "Q3: What experimental facilities have measured the Hoyle state properties most precisely? "
        "(Answering would improve Observation Quality by +2 points: measurement provenance)"
    )
    name = "Triple-Alpha Energy Release"
    question = (
        "Why does combining three helium-4 nuclei into carbon-12 release "
        "7.3 MeV of energy? What role does the Hoyle resonance play in making "
        "this crucial step in stellar nucleosynthesis possible?"
    )
    reference = "Nuclear Astrophysics"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "Triple-alpha: 3*He-4 -> C-12 releases 7.27 MeV. The Hoyle resonance "
        "(excited state at 7.65 MeV in C-12) enables the reaction. This is "
        "well-understood nuclear astrophysics. The observation that 3x4=12 "
        "is arithmetic, not an explanation of WHY the reaction proceeds."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUCLEAR ASTROPHYSICS: Triple-alpha energetics.")
            .step("3*He-4 total BE: 3 x 4 x 7.07 = 84.84 MeV")
            .step("C-12 total BE: 12 x 7.68 = 92.16 MeV")
            .equation("Energy release = 92.16 - 84.84 = 7.32 MeV")
            .step("Reaction proceeds because C-12 is more tightly bound.")
            .step("Hoyle resonance (7.65 MeV excited state) enables process.")
            .conclude("Triple-alpha releases ~7.3 MeV. Standard astrophysics.")
        )

    def model(self) -> Model:
        he4_A = 4
        c12_A = 12
        combined = 3 * he4_A

        be_he4_total = BINDING_ENERGY['He-4'] * he4_A * 3
        be_c12_total = BINDING_ENERGY['C-12'] * c12_A
        energy_release = be_c12_total - be_he4_total

        return (
            Model()
            .add("3*He-4 total BE (MeV)", be_he4_total)
            .add("C-12 total BE (MeV)", be_c12_total)
            .add("Energy release (MeV)", energy_release)
            .add("C-12 more bound", 1.0 if be_c12_total > be_he4_total else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("3*He-4 total BE (MeV)", 84.84)
            .add("C-12 total BE (MeV)", 92.16)
            .add("Energy release (MeV)", 7.32)
            .add("C-12 more bound", 1.0)
        )


# =============================================================================
# TEST 5: ALPHA DECAY EJECTS He-4 (Standard Nuclear Physics)
# =============================================================================

class AlphaDecayEjection(Test):
    """
    Verify alpha decay universally emits He-4.

    HONESTY: Alpha decay emits He-4 because it's doubly magic (very stable).
    The observation that A=4=k is noted, not explanatory.
    """
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Why is alpha particle emission favored over proton, deuteron, or triton "
        "emission in heavy nuclei? "
        "(Answering would improve Question by +3 points: explains preformation) "
        "Q2: How does the Geiger-Nuttall law connect alpha decay half-lives to alpha "
        "particle energies? "
        "(Answering would improve Derivation by +3 points: tunneling relationship) "
        "Q3: What is alpha clustering, and how do physicists detect it in nuclear structure? "
        "(Answering would improve Observation Quality by +2 points: experimental signatures)"
    )
    name = "Alpha Decay Emits He-4"
    question = (
        "Why does alpha decay always emit helium-4 rather than other light "
        "nuclei? What makes He-4 'doubly magic' and energetically favorable "
        "as a decay product?"
    )
    reference = "Nuclear Physics (alpha decay)"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "Alpha decay always emits He-4 (alpha particles). EXPLANATION: He-4 is "
        "doubly magic (Z=2, N=2 are magic numbers) and exceptionally bound. "
        "It's energetically favorable to emit a tightly bound cluster. The "
        "observation that 4=k is a coincidence GFD notes, not an explanation."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUCLEAR PHYSICS: Alpha decay mechanism.")
            .step("Alpha particle = He-4 nucleus (2p + 2n).")
            .step("He-4 is doubly magic: Z=2, N=2 are shell closures.")
            .step("High BE/A (7.07 MeV) makes it energetically favored.")
            .step("Alpha energies: Po-210 = 5.4 MeV, U-238 = 4.3 MeV.")
            .step("OBSERVATION: A=4 equals k (GFD notes this coincidence).")
            .conclude("Alpha = He-4 due to shell closure stability.")
        )

    def model(self) -> Model:
        alpha_A = 4
        energies = list(ALPHA_DECAY_ENERGY.values())
        avg_energy = sum(energies) / len(energies)

        return (
            Model()
            .add("Alpha mass number", alpha_A)
            .add("Avg alpha energy (MeV)", avg_energy)
            .add("In 4-6 MeV range", 1.0 if 4 < avg_energy < 6 else 0.0)
            .add("A equals k", 1.0 if alpha_A == K_CLOSURE else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Alpha mass number", 4)
            .add("Avg alpha energy (MeV)", 4.85)
            .add("In 4-6 MeV range", 1.0)
            .add("A equals k", 1.0)
        )


# =============================================================================
# TEST 6: MAGIC NUMBERS (Standard Nuclear Physics)
# =============================================================================

class MagicNumbersComparison(Test):
    """
    Compare magic numbers to k-multiples.

    HONESTY: Magic numbers are explained by the nuclear shell model.
    The partial overlap with k-multiples is an observation, not an explanation.
    """
    audit_score = 82
    audit_notes = None
    future_questions = (
        "Q1: How does spin-orbit coupling in the nuclear shell model generate the "
        "specific magic numbers 2, 8, 20, 28, 50, 82, 126? "
        "(Answering would improve Derivation by +4 points: shell model mechanism) "
        "Q2: Why are some magic numbers k-multiples (8, 20, 28) while others are not "
        "(2, 50, 82, 126), and is this pattern meaningful? "
        "(Answering would improve Commentary by +3 points: addresses pattern skeptically) "
        "Q3: Are there superheavy magic numbers beyond 126, and what nuclear structure "
        "calculations predict them? "
        "(Answering would improve Audience Accessibility by +2 points: current research)"
    )
    name = "Magic Numbers vs k-Multiples"
    question = (
        "Why do some magic numbers (8, 20, 28) happen to be k-multiples while "
        "others (2, 50, 82, 126) are not? Does the shell model or k-geometry "
        "provide the true explanation for nuclear stability?"
    )
    reference = "Nuclear Physics (shell model)"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "Nuclear magic numbers (2, 8, 20, 28, 50, 82, 126) come from the shell "
        "model (spin-orbit coupling creates energy gaps). Some are k-multiples "
        "(8=2k, 20=5k, 28=7k), some are not (2, 50, 82, 126). GFD observes this "
        "partial correlation but does not derive magic numbers from k."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUCLEAR SHELL MODEL: Magic numbers from shell closures.")
            .step("Magic numbers: 2, 8, 20, 28, 50, 82, 126.")
            .step("k-multiples among these: 8=2k, 20=5k, 28=7k.")
            .step("Non-k-multiples: 2, 50, 82, 126.")
            .step("CONCLUSION: Partial correlation, not a derivation.")
            .step("Shell model explains ALL magic numbers.")
            .step("k-alignment explains NONE of them (it's observation).")
            .conclude("Magic numbers from shell model, not k-geometry.")
        )

    def model(self) -> Model:
        k_multiples = [n for n in MAGIC_NUMBERS if n % K_CLOSURE == 0]
        non_k_multiples = [n for n in MAGIC_NUMBERS if n % K_CLOSURE != 0]

        return (
            Model()
            .add("Magic numbers", len(MAGIC_NUMBERS))
            .add("k-multiple magics", len(k_multiples))
            .add("Non-k magics", len(non_k_multiples))
            .add("Partial overlap", 1.0 if len(k_multiples) > 0 and len(non_k_multiples) > 0 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Magic numbers", 7)
            .add("k-multiple magics", 3)
            .add("Non-k magics", 4)
            .add("Partial overlap", 1.0)
        )


# =============================================================================
# TEST 7: NEUTRON-PROTON MASS DIFFERENCE (Standard Physics)
# =============================================================================

class NeutronProtonMassDifference(Test):
    """
    Verify neutron-proton mass difference.

    HONESTY: ~1.3 MeV difference is measured. Standard physics.
    """
    audit_score = 80
    audit_notes = None
    future_questions = (
        "Q1: Why is the neutron heavier than the proton even though the d quark is heavier "
        "than the u quark (neutron = udd, proton = uud)? "
        "(Answering would improve Question by +4 points: QCD mass puzzle) "
        "Q2: How does the neutron-proton mass difference enable beta decay and determine "
        "which nuclei are stable? "
        "(Answering would improve Commentary by +3 points: stability consequences) "
        "Q3: What would happen to nuclear physics if the neutron were lighter than the proton? "
        "(Answering would improve Audience Accessibility by +2 points: counterfactual insight)"
    )
    name = "Neutron-Proton Mass Difference"
    question = (
        "Why is the neutron only 0.14% heavier than the proton, and why does "
        "this tiny difference (1.3 MeV) determine whether free neutrons decay "
        "and which nuclei are stable against beta decay?"
    )
    reference = "CODATA"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "The neutron is ~1.3 MeV heavier than the proton (~0.14% of nucleon mass). "
        "This small difference allows beta decay (n -> p + e + nu) and determines "
        "nuclear stability. Standard physics, not a GFD prediction."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MEASUREMENT: Neutron and proton masses from CODATA.")
            .step("m_n = 939.565 MeV, m_p = 938.272 MeV")
            .equation("Mass difference = 939.565 - 938.272 = 1.293 MeV")
            .step("Fraction of proton mass: 1.293 / 938.272 = 0.138%")
            .step("Small difference allows beta decay neutron -> proton.")
            .conclude("n-p mass difference = 1.3 MeV (measured).")
        )

    def model(self) -> Model:
        mass_diff_mev = 939.565 - 938.272
        fraction = mass_diff_mev / 938.272

        return (
            Model()
            .add("Mass difference (MeV)", mass_diff_mev)
            .add("Fraction of proton mass", fraction)
            .add("Small difference", 1.0 if fraction < 0.002 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Mass difference (MeV)", 1.293)
            .add("Fraction of proton mass", 0.00138)
            .add("Small difference", 1.0)
        )


# =============================================================================
# TEST 8: NUCLEAR RADIUS (Standard Nuclear Physics)
# =============================================================================

class NuclearRadiusScale(Test):
    """
    Verify nuclear radius constant r_0.

    HONESTY: r_0 ~ 1.2 fm is measured. Standard nuclear physics.
    """
    audit_score = 78
    audit_notes = None
    future_questions = (
        "Q1: Why does the nuclear radius scale as A^(1/3), indicating constant nuclear "
        "density regardless of nucleus size? "
        "(Answering would improve Derivation by +3 points: explains incompressibility) "
        "Q2: How do electron scattering experiments measure nuclear radii, and what does "
        "the charge distribution look like? "
        "(Answering would improve Observation Quality by +3 points: measurement technique) "
        "Q3: How does the nuclear radius compare to the range of the strong force (~1 fm)? "
        "(Answering would improve Commentary by +2 points: scale connection)"
    )
    name = "Nuclear Radius Constant"
    question = (
        "Why does the nuclear radius follow R = r_0 * A^(1/3) with r_0 ~ 1.2 fm? "
        "What does this cube-root scaling reveal about nuclear matter being "
        "approximately incompressible?"
    )
    reference = "Nuclear Physics"
    tolerance = 0.30
    level = Level.STANDARD
    commentary = (
        "Nuclear radii follow R = r_0 * A^(1/3) with r_0 ~ 1.2 fm. This is "
        "measured by electron scattering. The fact that r_0 ~ 0.4 * r_e is "
        "an observation GFD notes, not an explanation."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NUCLEAR PHYSICS: Nuclear radius formula.")
            .equation("R = r_0 * A^(1/3), with r_0 ~ 1.2 fm")
            .step("This empirical formula fits nuclear data.")
            .step("Compare to classical electron radius r_e = 2.82 fm.")
            .equation("r_0 / r_e = 1.2 / 2.82 = 0.43")
            .step("OBSERVATION: r_0 ~ 0.4 * r_e (GFD notes this).")
            .conclude("r_0 = 1.2 fm (measured), r_0/r_e ~ 0.4.")
        )

    def model(self) -> Model:
        r_0 = 1.2e-15  # fm
        ratio = r_0 / R_E

        return (
            Model()
            .add("Nuclear r_0 (m)", r_0)
            .add("Classical r_e (m)", R_E)
            .add("r_0/r_e ratio", ratio)
            .add("Same order of magnitude", 1.0 if 0.1 < ratio < 10 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Nuclear r_0 (m)", 1.2e-15)
            .add("Classical r_e (m)", 2.82e-15)
            .add("r_0/r_e ratio", 0.43)
            .add("Same order of magnitude", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    K4PackingGeometry,
    BindingEnergyCurve,
    Be8Instability,
    TripleAlphaPathway,
    AlphaDecayEjection,
    MagicNumbersComparison,
    NeutronProtonMassDifference,
    NuclearRadiusScale,
]


def run_all() -> bool:
    """Run all subspace packing tests."""
    return run_tests(
        title="Subspace Packing",
        summary=(
            "These tests verify STANDARD NUCLEAR PHYSICS data:\n"
            "1. Binding energy curve peaks at Fe-56 (measured)\n"
            "2. Be-8 unstable due to positive Q-value for alpha decay\n"
            "3. Triple-alpha releases ~7.3 MeV (Hoyle resonance)\n"
            "4. Alpha decay emits He-4 (doubly magic)\n"
            "5. Magic numbers from shell model\n"
            "6. Neutron-proton mass difference = 1.3 MeV\n\n"
            "CLARIFICATION: GFD's k=4 from simplex theorem is a geometric\n"
            "DEFINITION. The observations that He-4 has A=4 and Fe-56 has\n"
            "A=14*4 are COINCIDENCES or CORRELATIONS, not explanations.\n"
            "Nuclear stability is explained by the shell model, not k-alignment."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
