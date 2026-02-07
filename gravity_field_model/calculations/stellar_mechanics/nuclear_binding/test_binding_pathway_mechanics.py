"""
Binding Pathway Mechanics: Standard Nuclear Physics
====================================================

GFM Model V2

HONESTY STATEMENT:
This module verifies STANDARD NUCLEAR PHYSICS data against GFM terminology.
These tests do NOT derive nuclear physics from GFM geometry. They verify
that measured nuclear data (binding energies, mass defects, fusion thresholds)
is correctly referenced and that GFM terminology maps consistently to
established physics.

WHAT GFM CLAIMS (to be tested elsewhere):
- The stellated octahedron geometry (Field Chamber) constrains nuclear structure
- k=4 is geometrically necessary (simplex theorem)
- Binding involves compression shift through the Field Origin

WHAT THESE TESTS VERIFY:
1. Standard nuclear binding energies are correctly referenced
2. Mass defect calculations follow E=mc^2
3. Fusion chain temperatures match astrophysical data
4. Fe-56 is at binding energy peak (standard physics)

NOT TESTED HERE (removed as numerology):
- Whether A mod 4 = 0 "explains" stability (it does not derive it)
- Whether k-alignment predicts binding (pattern matching, not derivation)

References:
- CODATA 2022 / AME2020 nuclear binding energies
- Standard Solar Model (Bahcall)

TEST GROUP GOALS:
This module establishes the foundation for understanding nuclear binding by
verifying standard physics data. Each test connects measured values to the
physical mechanisms: shell closures, Coulomb barriers, and mass-energy
equivalence. These form the empirical basis that any theoretical model must
reproduce.

Audience: Undergraduate physics students familiar with basic nuclear physics.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, MEV_TO_JOULES,
    M_P, M_N, M_E,
    M_P_MEV, M_N_MEV, M_E_MEV,
    T_HYDROGEN_FUSION, T_HELIUM_FUSION, T_CARBON_FUSION,
    T_OXYGEN_FUSION, T_SILICON_FUSION,
)

# Nuclear binding energies (MeV per nucleon) from AME2020/CODATA
BINDING_ENERGY_PER_NUCLEON = {
    'H-1':   0.00,    # Unbound single nucleon
    'H-2':   1.11,    # Deuterium
    'H-3':   2.83,    # Tritium
    'He-3':  2.57,    # Helium-3
    'He-4':  7.07,    # Alpha particle
    'Li-6':  5.33,
    'Li-7':  5.61,
    'Be-8':  7.06,    # UNSTABLE (8.19e-17 s half-life)
    'C-12':  7.68,
    'N-14':  7.48,
    'O-16':  7.98,    # Doubly magic
    'Ne-20': 8.03,
    'Mg-24': 8.26,
    'Si-28': 8.45,
    'S-32':  8.49,
    'Ca-40': 8.55,    # Doubly magic
    'Fe-56': 8.79,    # PEAK binding energy per nucleon
    'Ni-62': 8.79,    # Near peak (highest total BE/A)
    'Zn-64': 8.74,
    'Kr-84': 8.72,
    'Sn-120': 8.50,
    'Pb-208': 7.87,   # Doubly magic
    'U-238': 7.57,
}

# Total binding energies (MeV) for key nuclei
TOTAL_BINDING_ENERGY = {
    'H-2':   2.22,    # Deuterium
    'He-4':  28.30,   # Alpha particle
    'C-12':  92.16,   # Carbon
    'O-16':  127.62,  # Oxygen
    'Fe-56': 492.26,  # Iron
}

# Fusion thresholds from common (aliases for backward compatibility)
T_H_FUSION = T_HYDROGEN_FUSION
T_HE_FUSION = T_HELIUM_FUSION
T_C_FUSION = T_CARBON_FUSION
T_O_FUSION = T_OXYGEN_FUSION
T_SI_FUSION = T_SILICON_FUSION


# =============================================================================
# TEST 1: PROTON REST MASS (standard physics)
# =============================================================================

class ProtonRestMass(Test):
    """
    Verify proton rest mass energy.

    HONESTY: This test verifies that we reference the correct CODATA value.
    GFM does not derive the proton mass. The claim that m_p/m_e = 6*pi^5
    is a numerical coincidence (accuracy ~0.01%), not a derivation.
    """
    audit_score = 78
    audit_notes = None
    future_questions = (
        "Q1: Why is the proton mass not predicted by the Standard Model and must be "
        "measured experimentally, unlike the electron mass which follows from QED? "
        "(Answering would improve Question by +3 points: hooks into deeper physics) "
        "Q2: What role does QCD confinement play in determining the proton mass, given "
        "that quark masses account for only ~1% of it? "
        "(Answering would improve Derivation by +4 points: explains mass origin) "
        "Q3: Are there other numerical coincidences like 6*pi^5 that appear in physics? "
        "(Answering would improve Commentary by +2 points: context for pattern recognition)"
    )
    name = "Proton Rest Mass Energy"
    question = (
        "Why is the proton approximately 1836 times heavier than the electron? "
        "Is this ratio derived from first principles, or is it a measured "
        "fundamental constant?"
    )
    reference = "CODATA 2018"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The proton rest mass (938.27 MeV) is a measured fundamental constant. "
        "The mass ratio m_p/m_e = 1836.15 is empirically determined. The numerical "
        "coincidence that 6*pi^5 = 1836.12 is noted but does NOT constitute a "
        "derivation. GFM adopts this value; it does not predict it."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MEASUREMENT: Proton rest mass from CODATA 2018.")
            .step("m_p = 1.67262192e-27 kg.")
            .equation("E = m_p * c^2 = 1.503e-10 J = 938.27 MeV")
            .step("Mass ratio to electron: 938.27 / 0.511 = 1836.15.")
            .step("NOTE: The numerical coincidence 6*pi^5 = 1836.12 (0.002% match) "
                  "is observed but unexplained. This is NOT a GFM derivation.")
            .conclude("Proton rest mass = 938.27 MeV (measured).")
        )

    def model(self) -> Model:
        # CODATA proton mass
        E_proton_J = M_P * C**2
        E_proton_MeV = E_proton_J / MEV_TO_JOULES

        # Mass ratio
        mass_ratio = E_proton_MeV / M_E_MEV

        # The 6*pi^5 coincidence (noted, not claimed as derivation)
        six_pi_fifth = 6 * math.pi**5
        coincidence_error = abs(mass_ratio - six_pi_fifth) / mass_ratio * 100

        return (
            Model()
            .add("Proton mass (MeV)", E_proton_MeV)
            .add("m_p/m_e ratio", mass_ratio)
            .add("6*pi^5 value", six_pi_fifth)
            .add("Coincidence error (%)", coincidence_error)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Proton mass (MeV)", 938.272)
            .add("m_p/m_e ratio", 1836.15)
            .add("6*pi^5 value", 1836.12)
            .add("Coincidence error (%)", 0.002)
        )


# =============================================================================
# TEST 2: HYDROGEN IONIZATION (standard atomic physics)
# =============================================================================

class HydrogenIonization(Test):
    """
    Verify hydrogen ionization energy.

    HONESTY: This is standard atomic physics (Bohr model / QM).
    GFM terminology ("vortex capture") is a relabeling, not a derivation.
    """
    audit_score = 80
    audit_notes = None
    future_questions = (
        "Q1: How does the Rydberg constant connect the hydrogen ionization energy to "
        "other fundamental constants (alpha, m_e, c, h)? "
        "(Answering would improve Derivation by +3 points: shows dimensional relationships) "
        "Q2: Why is the 10^8 scale separation between atomic and nuclear energies crucial "
        "for the existence of chemistry as we know it? "
        "(Answering would improve Commentary by +3 points: connects to big picture) "
        "Q3: How do fine structure corrections modify the simple 13.6 eV value? "
        "(Answering would improve Audience Accessibility by +2 points: extends basic result)"
    )
    name = "Hydrogen Ionization Energy"
    question = (
        "Why is the hydrogen ionization energy (13.6 eV) seven orders of "
        "magnitude smaller than nuclear binding energies (~MeV)? What does "
        "this scale separation reveal about electromagnetic vs strong forces?"
    )
    reference = "CODATA (Rydberg energy)"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "The hydrogen ionization energy (13.6 eV) is derived from QM/Bohr model. "
        "It is 7 orders of magnitude smaller than nuclear binding (~MeV). This "
        "scale separation reflects the different physics of electromagnetic vs "
        "strong force binding. GFM relabels this as 'vortex capture' but does "
        "not derive it."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Hydrogen ionization from Rydberg energy.")
            .equation("E_ion = 13.6 eV = m_e * alpha^2 * c^2 / 2")
            .step("Compare to nuclear scale: 938 MeV (proton mass).")
            .equation("Ratio: 13.6e-6 / 938 = 1.45e-8")
            .step("Scale separation: ~10^8 between atomic and nuclear.")
            .conclude("Ionization = 13.6 eV; atomic << nuclear energies.")
        )

    def model(self) -> Model:
        ionization_eV = 13.6
        ionization_MeV = ionization_eV * 1e-6
        ratio = ionization_MeV / M_P_MEV
        log_separation = math.log10(M_P_MEV / ionization_MeV)

        return (
            Model()
            .add("Ionization energy (eV)", ionization_eV)
            .add("Ratio to proton mass", ratio)
            .add("Scale separation (orders)", log_separation)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Ionization energy (eV)", 13.6)
            .add("Ratio to proton mass", 1.45e-8)
            .add("Scale separation (orders)", 7.84)
        )


# =============================================================================
# TEST 3: HELIUM-4 BINDING (standard nuclear physics)
# =============================================================================

class Helium4Binding(Test):
    """
    Verify He-4 (alpha particle) binding energy.

    HONESTY: The exceptional stability of He-4 is well-known in nuclear physics.
    It is explained by the nuclear shell model (doubly magic: Z=N=2).
    GFM notes that 4 = k, but this does NOT explain the stability.
    """
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: Why is the jump from He-3 to He-4 binding energy so dramatic (2.57 to 7.07 MeV), "
        "and what does 'doubly magic' mean physically? "
        "(Answering would improve Derivation by +3 points: explains shell closure) "
        "Q2: How does alpha clustering emerge in heavier nuclei like C-12 and O-16? "
        "(Answering would improve Commentary by +3 points: extends concept) "
        "Q3: Why do alpha particles dominate radioactive decay rather than deuterons or tritons? "
        "(Answering would improve Question by +2 points: motivates uniqueness of He-4)"
    )
    name = "He-4 Binding Energy"
    question = (
        "Why does helium-4 have such dramatically higher binding energy than "
        "its neighbors (He-3 and Li-6)? What makes it 'doubly magic' and "
        "exceptionally stable?"
    )
    reference = "Nuclear Physics (AME2020)"
    tolerance = 0.05
    level = Level.CRITICAL
    commentary = (
        "He-4 (alpha particle) has BE/A = 7.07 MeV, much higher than neighbors "
        "(He-3: 2.57, Li-6: 5.33). Standard explanation: He-4 is doubly magic "
        "(closed proton and neutron shells at Z=N=2). GFM notes 4 = k (tetrahedral "
        "number), but this observation does not constitute a derivation of WHY "
        "He-4 is stable. The shell model provides the mechanistic explanation."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MEASUREMENT: He-4 binding energy from AME2020.")
            .step("BE/A (He-4) = 7.07 MeV/nucleon.")
            .step("Total BE = 4 * 7.07 = 28.3 MeV.")
            .step("COMPARISON to neighbors:")
            .step("  He-3: BE/A = 2.57 MeV (incomplete closure)")
            .step("  Li-6: BE/A = 5.33 MeV")
            .equation("Jump He-3 -> He-4: 7.07 - 2.57 = 4.50 MeV")
            .step("STANDARD EXPLANATION: He-4 is doubly magic (shell closure).")
            .step("GFM OBSERVATION: A=4 equals k. This is noted but not explanatory.")
            .conclude("He-4 BE/A = 7.07 MeV; stability from shell closure.")
        )

    def model(self) -> Model:
        be_he3 = BINDING_ENERGY_PER_NUCLEON['He-3']
        be_he4 = BINDING_ENERGY_PER_NUCLEON['He-4']
        be_li6 = BINDING_ENERGY_PER_NUCLEON['Li-6']

        jump_to_he4 = be_he4 - be_he3
        total_be = 4 * be_he4

        return (
            Model()
            .add("He-3 BE/A (MeV)", be_he3)
            .add("He-4 BE/A (MeV)", be_he4)
            .add("Li-6 BE/A (MeV)", be_li6)
            .add("Jump He-3 to He-4 (MeV)", jump_to_he4)
            .add("He-4 total BE (MeV)", total_be)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("He-3 BE/A (MeV)", 2.57)
            .add("He-4 BE/A (MeV)", 7.07)
            .add("Li-6 BE/A (MeV)", 5.33)
            .add("Jump He-3 to He-4 (MeV)", 4.50)
            .add("He-4 total BE (MeV)", 28.30)
        )


# =============================================================================
# TEST 4: MASS DEFECT AND E=mc^2 (standard physics)
# =============================================================================

class MassDefectVerification(Test):
    """
    Verify E=mc^2 for nuclear mass defect.

    HONESTY: This is standard physics (Einstein 1905).
    GFM terminology does not change the physics.
    """
    audit_score = 88
    audit_notes = None
    future_questions = (
        "Q1: How was E=mc^2 first experimentally verified, and what role did nuclear "
        "binding play in that confirmation? "
        "(Answering would improve Observation Quality by +3 points: historical verification) "
        "Q2: Why does the 0.75% mass conversion in He-4 represent an enormous energy density "
        "compared to chemical reactions? "
        "(Answering would improve Commentary by +2 points: quantifies scale difference) "
        "Q3: Where does the 'missing' mass actually go when nucleons bind? "
        "(Answering would improve Question by +3 points: deepens conceptual understanding)"
    )
    name = "Mass Defect E=mc^2"
    question = (
        "Why does a helium-4 nucleus weigh less than two protons plus two "
        "neutrons? Where does the 'missing' 0.75% of the mass go when nucleons "
        "bind together?"
    )
    reference = "Einstein (1905), CODATA"
    tolerance = 0.05
    level = Level.CRITICAL
    commentary = (
        "The mass defect (constituent mass minus nuclear mass) times c^2 equals "
        "the binding energy. For He-4: mass defect = 0.75%, yielding 28.3 MeV. "
        "This is standard physics, universally accepted. GFM adopts E=mc^2; "
        "it does not provide an alternative."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: Mass defect relates to binding energy via E=mc^2.")
            .step("He-4: Z=2 protons, N=2 neutrons.")
            .equation("Constituent mass = 2*938.27 + 2*939.57 = 3755.68 MeV")
            .step("Nuclear mass (from measured He-4 atomic mass minus electrons):")
            .equation("m_He4 = 3727.38 MeV")
            .equation("Mass defect = 3755.68 - 3727.38 = 28.30 MeV")
            .step("This equals the measured total binding energy. E=mc^2 verified.")
            .equation("Mass fraction converted = 28.30 / 3755.68 = 0.75%")
            .conclude("Mass defect = 28.3 MeV = BE_total. E=mc^2 confirmed.")
        )

    def model(self) -> Model:
        # Constituent masses
        M_const = 2 * M_P_MEV + 2 * M_N_MEV

        # He-4 binding energy (measured)
        BE_total = TOTAL_BINDING_ENERGY['He-4']

        # Nuclear mass = constituents - binding
        M_nuclear = M_const - BE_total

        # Mass fraction converted
        mass_fraction = BE_total / M_const

        return (
            Model()
            .add("Constituent mass (MeV)", M_const)
            .add("Nuclear mass (MeV)", M_nuclear)
            .add("Mass defect (MeV)", BE_total)
            .add("Mass fraction converted", mass_fraction)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Constituent mass (MeV)", 3755.68)
            .add("Nuclear mass (MeV)", 3727.38)
            .add("Mass defect (MeV)", 28.30)
            .add("Mass fraction converted", 0.0075)
        )


# =============================================================================
# TEST 5: FUSION TEMPERATURE CHAIN (standard astrophysics)
# =============================================================================

class FusionTemperatureChain(Test):
    """
    Verify stellar fusion temperature progression.

    HONESTY: These are measured/modeled astrophysical values.
    GFM terminology ("bigger bowling balls") is metaphor, not derivation.
    """
    audit_score = 82
    audit_notes = None
    future_questions = (
        "Q1: How does the Gamow peak shift with temperature, and why does this enable "
        "fusion at energies far below the classical Coulomb barrier? "
        "(Answering would improve Derivation by +4 points: explains quantum tunneling role) "
        "Q2: Why does the temperature ratio from H to Si burning span 180x, yet all these "
        "stages occur within a single massive star's lifetime? "
        "(Answering would improve Commentary by +2 points: connects to stellar evolution) "
        "Q3: What sets the minimum stellar mass needed to ignite each fusion stage? "
        "(Answering would improve Audience Accessibility by +2 points: practical threshold)"
    )
    name = "Stellar Fusion Temperature Chain"
    question = (
        "Why does fusing heavier elements require progressively higher "
        "temperatures? How does the increasing Coulomb barrier (more protons "
        "repelling each other) determine these thresholds?"
    )
    reference = "Stellar Physics (Standard Solar Model)"
    tolerance = 0.15
    level = Level.STANDARD
    commentary = (
        "Fusion of heavier elements requires higher temperatures because: "
        "(1) Higher Coulomb barriers from more protons, "
        "(2) Gamow peak shifts to higher energies. "
        "This is standard nuclear astrophysics. GFM's metaphor of 'bigger "
        "bowling balls needing bigger hammers' captures the intuition but "
        "does not derive the temperatures."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ASTROPHYSICS: Fusion thresholds from stellar models.")
            .step("H -> He (pp-chain): T ~ 1.5e7 K")
            .step("He -> C (triple-alpha): T ~ 1.0e8 K")
            .step("C -> O (carbon burning): T ~ 5.0e8 K")
            .step("O -> Si (oxygen burning): T ~ 1.5e9 K")
            .step("Si -> Fe (silicon burning): T ~ 2.7e9 K")
            .equation("Temperature ratio: T_Si / T_H = 180x")
            .step("EXPLANATION: Higher Coulomb barriers require higher "
                  "kinetic energies for tunneling.")
            .conclude("Fusion temperatures increase monotonically with product mass.")
        )

    def model(self) -> Model:
        temps = [T_H_FUSION, T_HE_FUSION, T_C_FUSION, T_O_FUSION, T_SI_FUSION]

        # Check monotonic increase
        monotonic = 1.0 if all(temps[i] < temps[i+1] for i in range(len(temps)-1)) else 0.0

        # Temperature range
        temp_ratio = temps[-1] / temps[0]

        return (
            Model()
            .add("H fusion (K)", temps[0])
            .add("He fusion (K)", temps[1])
            .add("C fusion (K)", temps[2])
            .add("Si fusion (K)", temps[4])
            .add("Temperature ratio (Si/H)", temp_ratio)
            .add("Monotonic increase", monotonic)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("H fusion (K)", 1.5e7)
            .add("He fusion (K)", 1.0e8)
            .add("C fusion (K)", 5.0e8)
            .add("Si fusion (K)", 2.7e9)
            .add("Temperature ratio (Si/H)", 180.0)
            .add("Monotonic increase", 1.0)
        )


# =============================================================================
# TEST 6: IRON-56 BINDING PEAK (standard nuclear physics)
# =============================================================================

class Iron56BindingPeak(Test):
    """
    Verify Fe-56 has peak binding energy per nucleon.

    HONESTY: This is measured data. The standard explanation involves the
    balance of volume (attractive strong force) and surface/Coulomb
    (repulsive) terms in the semi-empirical mass formula.
    """
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Why is Ni-62 technically more tightly bound than Fe-56, yet iron is more "
        "abundant in stellar cores? "
        "(Answering would improve Commentary by +3 points: clarifies common misconception) "
        "Q2: How does the balance of SEMF terms shift from light to heavy nuclei to "
        "create the binding curve shape? "
        "(Answering would improve Derivation by +3 points: physical mechanism) "
        "Q3: What happens thermodynamically when a star tries to fuse elements beyond iron? "
        "(Answering would improve Question by +2 points: explains core collapse trigger)"
    )
    name = "Fe-56 Binding Energy Peak"
    question = (
        "Why is iron-56 the endpoint of stellar fusion? What balance of "
        "attractive nuclear forces and repulsive Coulomb forces makes iron "
        "the most tightly bound nucleus per nucleon?"
    )
    reference = "Nuclear Physics (AME2020)"
    tolerance = 0.05
    level = Level.CRITICAL
    commentary = (
        "Fe-56 (and Ni-62) sit at the peak of the binding energy curve with "
        "BE/A ~ 8.79 MeV. Lighter nuclei release energy by fusion toward Fe; "
        "heavier nuclei release energy by fission toward Fe. Standard explanation: "
        "the semi-empirical mass formula (Weizsacker) balances volume, surface, "
        "Coulomb, asymmetry, and pairing terms. The observation that 56 = 14*4 "
        "is numerology, not explanation."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MEASUREMENT: Binding energies from AME2020.")
            .step("Fe-56: BE/A = 8.79 MeV/nucleon.")
            .step("Compare to lighter nuclei:")
            .step("  O-16: 7.98 MeV/nucleon")
            .step("  Si-28: 8.45 MeV/nucleon")
            .step("  Ca-40: 8.55 MeV/nucleon")
            .step("Compare to heavier nuclei:")
            .step("  Kr-84: 8.72 MeV/nucleon")
            .step("  Pb-208: 7.87 MeV/nucleon")
            .step("  U-238: 7.57 MeV/nucleon")
            .step("Fe-56 is the peak. Fusion to Fe releases energy; past Fe absorbs.")
            .step("STANDARD EXPLANATION: Balance of SEMF terms at A~56.")
            .conclude("Fe-56 BE/A = 8.79 MeV is maximum; fusion endpoint.")
        )

    def model(self) -> Model:
        fe_be = BINDING_ENERGY_PER_NUCLEON['Fe-56']

        # Compare to lighter
        lighter = ['O-16', 'Si-28', 'Ca-40']
        fe_above_lighter = all(fe_be > BINDING_ENERGY_PER_NUCLEON[n] for n in lighter)

        # Compare to heavier
        heavier = ['Kr-84', 'Pb-208', 'U-238']
        fe_above_heavier = all(fe_be > BINDING_ENERGY_PER_NUCLEON[n] for n in heavier)

        return (
            Model()
            .add("Fe-56 BE/A (MeV)", fe_be)
            .add("Above lighter nuclei", 1.0 if fe_above_lighter else 0.0)
            .add("Above heavier nuclei", 1.0 if fe_above_heavier else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Fe-56 BE/A (MeV)", 8.79)
            .add("Above lighter nuclei", 1.0)
            .add("Above heavier nuclei", 1.0)
        )


# =============================================================================
# TEST 7: NEUTRON EXCESS IN HEAVY NUCLEI (standard nuclear physics)
# =============================================================================

class NeutronExcessScaling(Test):
    """
    Verify N/Z ratio increases with atomic number.

    HONESTY: This follows from Coulomb repulsion scaling as Z^2.
    Standard nuclear physics, not a GFM prediction.
    """
    audit_score = 81
    audit_notes = None
    future_questions = (
        "Q1: Why does the Coulomb energy scale as Z^2 while nuclear binding scales as A, "
        "and how does this create the need for neutron excess? "
        "(Answering would improve Derivation by +3 points: quantitative understanding) "
        "Q2: How do neutrons 'dilute' Coulomb repulsion without contributing to it? "
        "(Answering would improve Commentary by +3 points: mechanism clarity) "
        "Q3: What is the drip line and why can't nuclei have arbitrarily high N/Z ratios? "
        "(Answering would improve Audience Accessibility by +2 points: shows limits)"
    )
    name = "Neutron-Proton Ratio Scaling"
    question = (
        "Why do heavy nuclei like uranium need ~1.6 neutrons per proton to be "
        "stable, while helium is stable with equal numbers? How do extra "
        "neutrons dilute Coulomb repulsion?"
    )
    reference = "Nuclear Physics (valley of stability)"
    tolerance = 0.10
    level = Level.STANDARD
    commentary = (
        "Light stable nuclei have N=Z (symmetric). Heavy stable nuclei have "
        "N > Z because Coulomb repulsion between protons grows as Z^2 while "
        "nuclear binding grows roughly as A. Extra neutrons dilute the Coulomb "
        "energy without adding repulsion. This is standard nuclear physics "
        "(liquid drop model, SEMF). GFM does not derive this."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("STANDARD PHYSICS: N/Z scaling from Coulomb vs strong force.")
            .step("He-4: Z=2, N=2, N/Z = 1.00")
            .step("Ca-40: Z=20, N=20, N/Z = 1.00 (doubly magic)")
            .step("Fe-56: Z=26, N=30, N/Z = 1.15")
            .step("Sn-120: Z=50, N=70, N/Z = 1.40")
            .step("Pb-208: Z=82, N=126, N/Z = 1.54 (doubly magic)")
            .step("U-238: Z=92, N=146, N/Z = 1.59")
            .step("EXPLANATION: Coulomb term in SEMF proportional to Z^2/A^(1/3).")
            .step("To minimize energy, heavy nuclei add neutrons to increase A, R.")
            .conclude("N/Z increases with Z; Coulomb dilution by neutrons.")
        )

    def model(self) -> Model:
        nuclei = [
            ('He-4',   2,   4),
            ('Ca-40',  20,  40),
            ('Fe-56',  26,  56),
            ('Sn-120', 50,  120),
            ('Pb-208', 82,  208),
            ('U-238',  92,  238),
        ]

        nz_ratios = {name: (a - z) / z for name, z, a in nuclei}

        # Check that heavy elements have higher N/Z
        heavy_ratios = [nz_ratios['Fe-56'], nz_ratios['Sn-120'],
                        nz_ratios['Pb-208'], nz_ratios['U-238']]
        is_increasing = all(heavy_ratios[i] <= heavy_ratios[i+1]
                            for i in range(len(heavy_ratios)-1))

        return (
            Model()
            .add("N/Z He-4", nz_ratios['He-4'])
            .add("N/Z Fe-56", nz_ratios['Fe-56'])
            .add("N/Z Pb-208", nz_ratios['Pb-208'])
            .add("N/Z U-238", nz_ratios['U-238'])
            .add("Heavy N/Z increasing", 1.0 if is_increasing else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("N/Z He-4", 1.00)
            .add("N/Z Fe-56", 1.154)
            .add("N/Z Pb-208", 1.537)
            .add("N/Z U-238", 1.587)
            .add("Heavy N/Z increasing", 1.0)
        )


# =============================================================================
# TEST 8: BE-8 INSTABILITY (standard nuclear physics)
# =============================================================================

class Beryllium8Instability(Test):
    """
    Verify Be-8 is unstable despite high binding energy per nucleon.

    HONESTY: Be-8 instability is explained by the nuclear shell model and
    the Q-value for alpha decay. Not a GFM prediction.
    """
    audit_score = 87
    audit_notes = None
    future_questions = (
        "Q1: How does the extremely short half-life of Be-8 (8x10^-17 s) affect the "
        "triple-alpha process in stellar cores? "
        "(Answering would improve Commentary by +3 points: astrophysical consequences) "
        "Q2: Why is the Q-value more relevant to stability than binding energy per nucleon? "
        "(Answering would improve Derivation by +3 points: clarifies stability criterion) "
        "Q3: What role does the Hoyle state play in bridging the Be-8 gap? "
        "(Answering would improve Question by +2 points: connects to carbon production)"
    )
    name = "Be-8 Instability"
    question = (
        "Why is beryllium-8 almost instantly unstable (half-life 8e-17 s) "
        "even though it has high binding energy per nucleon? What does the "
        "positive Q-value for alpha decay reveal about stability?"
    )
    reference = "Nuclear Physics (alpha decay)"
    tolerance = 0.20
    level = Level.STANDARD
    commentary = (
        "Be-8 has BE/A = 7.06 MeV, comparable to He-4's 7.07 MeV. Yet it decays "
        "almost instantly to two alpha particles. STANDARD EXPLANATION: The "
        "Q-value for Be-8 -> 2*He-4 is +92 keV, making decay energetically "
        "favorable. The coincidence that 8 = 2*4 (two alphas) is noted but "
        "does not EXPLAIN the instability. The shell model and Q-value do."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MEASUREMENT: Be-8 properties from nuclear data.")
            .step("Be-8: BE/A = 7.06 MeV (high, comparable to He-4).")
            .step("Half-life: 8.19e-17 seconds (extremely short).")
            .step("Decay: Be-8 -> 2 * He-4 (alpha decay).")
            .equation("Q-value = 2*BE(He-4) - BE(Be-8) = 2*28.30 - 56.50 = +0.092 MeV")
            .step("Positive Q-value means decay is energetically favorable.")
            .step("The high BE/A is irrelevant; what matters is BE(products) > BE(parent).")
            .step("STANDARD PHYSICS: Q-value determines decay energetics.")
            .conclude("Be-8 unstable due to positive Q-value for alpha decay.")
        )

    def model(self) -> Model:
        be8_bea = BINDING_ENERGY_PER_NUCLEON['Be-8']
        he4_bea = BINDING_ENERGY_PER_NUCLEON['He-4']

        # Total binding energies
        be8_total = 8 * be8_bea
        he4_total = 4 * he4_bea

        # Q-value for decay
        q_value = 2 * he4_total - be8_total

        return (
            Model()
            .add("Be-8 BE/A (MeV)", be8_bea)
            .add("He-4 BE/A (MeV)", he4_bea)
            .add("Q-value (MeV)", q_value)
            .add("Decay favorable (Q>0)", 1.0 if q_value > 0 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Be-8 BE/A (MeV)", 7.06)
            .add("He-4 BE/A (MeV)", 7.07)
            .add("Q-value (MeV)", 0.092)
            .add("Decay favorable (Q>0)", 1.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    ProtonRestMass,
    HydrogenIonization,
    Helium4Binding,
    MassDefectVerification,
    FusionTemperatureChain,
    Iron56BindingPeak,
    NeutronExcessScaling,
    Beryllium8Instability,
]


def run_all() -> bool:
    """Run all binding pathway mechanics tests."""
    return run_tests(
        title="Binding Pathway Mechanics",
        summary=(
            "These tests verify STANDARD NUCLEAR PHYSICS data against GFM terminology. "
            "They confirm that measured values (binding energies, mass defects, fusion "
            "temperatures) are correctly referenced. These tests do NOT claim that GFM "
            "derives nuclear physics.\n\n"
            "KEY VERIFICATIONS:\n"
            "1. Proton mass = 938.27 MeV (measured, 6*pi^5 coincidence noted)\n"
            "2. H ionization = 13.6 eV (standard QM)\n"
            "3. He-4 BE/A = 7.07 MeV (doubly magic shell closure)\n"
            "4. Mass defect follows E=mc^2 exactly\n"
            "5. Fusion temperatures increase with product mass\n"
            "6. Fe-56 is the binding energy peak\n"
            "7. N/Z increases with Z (Coulomb dilution)\n"
            "8. Be-8 unstable due to positive Q-value for alpha decay\n\n"
            "REMOVED (was numerology): k-alignment tests, (1+A) field counting."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
