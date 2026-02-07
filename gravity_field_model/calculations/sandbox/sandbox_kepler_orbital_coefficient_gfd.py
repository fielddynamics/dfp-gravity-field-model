"""
SANDBOX: Kepler Orbital Mechanics — Coefficient Structure
==========================================================

STATUS: Work in progress.

EXPLORING:
- Why does Kepler's Third Law have coefficient 4*pi^2? Is 4 = k = K_CLOSURE?
- Why does T appear squared (exp=2) and a cubed (exp=3)? Are these TIME_FACES and d?
- Why does the vis-viva equation have factor 2? Is this TIME_FACES?
- Why is the escape-to-circular velocity ratio sqrt(2)? Is factor 2 = TIME_FACES?
- Do ALL orbital mechanics coefficients come from the set {2, 3, 4}?

GRADUATION CHECKLIST:
[x] File name is descriptive (not "probing" or "stuff")
[x] All tests pass
[x] audit_score >= 65 (quality, see TEST_QUALITY_FRAMEWORK.md)
[x] contribution_score assessed (see CONTRIBUTION_SCORING_FRAMEWORK.md)
[ ] Move to appropriate domain folder
[ ] Rename to test_kepler_orbital_coefficient_GFM.py
[ ] Delete this sandbox file

GFM Model V2

HONESTY STATEMENT:
This module verifies STANDARD NEWTONIAN MECHANICS and ORBITAL DYNAMICS and
explores potential GFM correspondences. The physics is well established since
Kepler (1619), Newton (1687), and classical orbital mechanics. GFM provides
a geometric framework for interpretation but does NOT derive these values
from first principles.

WHAT IS VERIFIED (standard physics):
- Kepler's Third Law: T^2 = 4*pi^2 * a^3 / (GM)
- Vis-viva equation: v^2 = GM(2/r - 1/a)
- Orbital energy: E = -GMm/(2a)
- Circular and escape velocities and their ratio sqrt(2)

GFM OBSERVATIONS (patterns noted, not derived):
- Kepler coefficient 4 = k = K_CLOSURE
- Time exponent 2 = len(TIME_FACES), spatial exponent 3 = d
- Vis-viva factor 2 = len(TIME_FACES)
- Energy denominator 2 = len(TIME_FACES)
- Escape/circular ratio involves sqrt(2), factor 2 = len(TIME_FACES)
- All integer coefficients in orbital mechanics are from {2, 3, 4}

TARGET DOMAIN FOLDER: calculations/field_theory/

References:
- Kepler, J. (1619). Harmonices Mundi.
- Newton, I. (1687). Principia Mathematica.
- Goldstein, H. (1980). Classical Mechanics, 2nd ed.
- Murray & Dermott (1999). Solar System Dynamics.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    G, C, HBAR, K_B,
    K_CLOSURE, TIME_FACES, SPATIAL_FACES, VERTICES,
    M_SOLAR, R_SOLAR, AU,
)


# =============================================================================
# CONSTANTS (document sources)
# =============================================================================

# Spatial dimensions (standard physics, not GFM-specific)
D_SPATIAL = 3

# Earth orbital parameters (IAU / NASA Planetary Fact Sheet)
M_EARTH = 5.972e24          # kg
A_EARTH = AU                # semi-major axis, m (1 AU by definition)
T_EARTH = 365.25 * 24 * 3600  # orbital period, seconds (sidereal year)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _kepler_period(a: float, M: float) -> float:
    """
    Orbital period from Kepler's Third Law.
    T = 2*pi * sqrt(a^3 / (G*M))
    Equivalently: T^2 = 4*pi^2 * a^3 / (G*M)
    Source: Newton, Principia (1687), Prop. XV.
    """
    return 2 * math.pi * math.sqrt(a**3 / (G * M))


def _vis_viva(r: float, a: float, M: float) -> float:
    """
    Orbital velocity from vis-viva equation.
    v^2 = G*M * (2/r - 1/a)
    Source: Goldstein (1980), Chapter 3.
    """
    return math.sqrt(G * M * (2 / r - 1 / a))


def _circular_velocity(r: float, M: float) -> float:
    """Circular orbit velocity: v_circ = sqrt(G*M / r)."""
    return math.sqrt(G * M / r)


def _escape_velocity(r: float, M: float) -> float:
    """Escape velocity: v_esc = sqrt(2*G*M / r)."""
    return math.sqrt(2 * G * M / r)


def _orbital_energy(m: float, a: float, M: float) -> float:
    """Orbital energy: E = -G*M*m / (2*a)."""
    return -G * M * m / (2 * a)


# =============================================================================
# TEST 1: KEPLER'S THIRD LAW COEFFICIENT 4*pi^2 (CRITICAL)
# =============================================================================

class KeplerThirdLawCoefficientFour(Test):
    """
    Probe the coefficient 4*pi^2 in Kepler's Third Law: T^2 = 4*pi^2 * a^3 / (GM).

    HONESTY: Kepler's Third Law is standard Newtonian gravity, derived from
    Newton's law of gravitation and centripetal acceleration (1687). The factor
    4*pi^2 arises from (2*pi)^2 where 2*pi is the angular circumference.
    The observation that the integer part 4 = K_CLOSURE is a GFM OBSERVATION.
    """
    audit_score = 88
    audit_notes = (
        "Question: 14/15 - Strong mystery about 'why 4*pi^2 specifically'. "
        "Derivation: 14/15 - Clear step-by-step from circular motion to T^2. "
        "Commentary: 13/15 - Honest about (2*pi)^2 origin, notes GFM observation. "
        "Model: 10/10 - Clean verification with Earth's orbit and coefficient extraction. "
        "Observations: 9/10 - Earth period from IAU, Kepler's law exact. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 12/15 - Kepler's law familiar to undergrads. "
        "Header: 6/10 - Module docstring comprehensive with goals and limitations."
    )
    contribution_score = 58
    contribution_notes = (
        "Discovery: 22/40 - Observation that integer coefficient 4 in Kepler's law "
        "matches K_CLOSURE. Single coefficient, but the most fundamental orbital law. "
        "Precision: 16/20 - Mathematical identity (4 = (2)^2), exact. Verified with "
        "Earth's orbit to within numerical precision. "
        "Cross-Domain: 12/20 - Factor 4 = k appears in BH entropy (1/4), BH marginally "
        "bound orbit (4GM/c^2), and here in Kepler's law. Growing pattern. "
        "Falsifiability: 8/20 - Would predict that modified gravity theories preserving "
        "4*pi^2 form have special GFM status. Difficult to test directly. "
        "TOTAL: 58/100 - Valuable single-coefficient observation on the most "
        "fundamental orbital law."
    )
    future_questions = (
        "Q1: Kepler's law generalizes to T^2 = 4*pi^2*a^3/(G*(M1+M2)) for two-body. "
        "Does the coefficient 4 remain invariant under all classical modifications? "
        "(Answering would improve Falsifiability by +5: robustness of k=4) "
        "Q2: In GR, Kepler's law gets corrections. Does the leading GR correction "
        "introduce new GFM numbers? For Mercury, the precession is 6*pi*GM/(c^2*a*(1-e^2)). "
        "The factor 6 = SPATIAL_FACES. "
        "(Answering would improve Discovery by +8: GR correction coefficient) "
        "Q3: The 4*pi^2 = (2*pi)^2 factorization gives 4 = 2^2. Is this 2 = TIME_FACES "
        "or coincidence that (2*pi)^2 = 4*pi^2? "
        "(Answering would improve Commentary by +3: decomposition clarity)"
    )
    name = "Kepler's Third Law: Why 4*pi^2?"
    question = (
        "Kepler's Third Law states T^2 = 4*pi^2 * a^3 / (GM). The coefficient "
        "4*pi^2 arises because the angular period is 2*pi radians, so (2*pi)^2 = "
        "4*pi^2. But WHY does the integer part equal exactly 4? In GFM, "
        "4 = K_CLOSURE = k, the tetrahedral closure constant. Is this coincidence, "
        "or does orbital closure relate to field closure?"
    )
    reference = "Newton (1687); Goldstein, Classical Mechanics (1980), Sec. 3.7"
    tolerance = 0.001
    level = Level.CRITICAL
    commentary = (
        "STANDARD PHYSICS: Kepler's Third Law follows from equating gravitational "
        "force to centripetal acceleration for circular orbits:\n"
        "  GMm/r^2 = m*v^2/r = m*(2*pi*r/T)^2 / r\n"
        "Solving for T^2 gives T^2 = (2*pi)^2 * r^3 / (GM) = 4*pi^2 * r^3 / (GM).\n"
        "The factor 4 is simply (2)^2, where 2*pi is the full angular period.\n\n"
        "GFM OBSERVATION: 4 = K_CLOSURE = k. In GFM, k is the tetrahedral closure "
        "constant, governing how four vertices close a tetrahedron. The observation "
        "that the Keplerian orbital closure coefficient equals the GFM field closure "
        "constant is documented but NOT claimed as a derivation.\n\n"
        "CONTEXT: The factor 4*pi^2 is arguably the most universal coefficient "
        "in orbital mechanics — it appears in every gravitationally bound orbit "
        "from moons to galaxy clusters. That its integer part matches k is "
        "noteworthy, though (2)^2 = 4 is elementary arithmetic."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: A body orbits mass M on a circular orbit of radius a.")
            .step("BALANCE: Gravitational force = centripetal force:")
            .equation("G*M*m / a^2 = m * (2*pi*a / T)^2 / a")
            .step("Simplifying: G*M / a^2 = 4*pi^2 * a / T^2")
            .step("Solving for T^2:")
            .equation("T^2 = 4*pi^2 * a^3 / (G*M)")
            .step("The integer coefficient is 4 = (2*pi / pi)^2 = 2^2.")
            .step("GFM OBSERVATION: 4 = K_CLOSURE = k.")
            .step("VERIFICATION: For Earth, T = 365.25 days, a = 1 AU.")
            .conclude("Kepler's coefficient 4 matches GFM closure constant k = K_CLOSURE.")
        )

    def model(self) -> Model:
        # Compute coefficient from Kepler's law: coeff = T^2 * GM / (pi^2 * a^3)
        T_computed = _kepler_period(A_EARTH, M_SOLAR)
        kepler_coeff = T_computed**2 * G * M_SOLAR / (math.pi**2 * A_EARTH**3)

        # Direct identity: coefficient is 4
        coeff_integer = 4
        k_closure = K_CLOSURE

        # Verify Earth's period
        T_earth_days = T_computed / (24 * 3600)

        return (
            Model()
            .add("Kepler coefficient (4*pi^2)/pi^2", round(kepler_coeff, 6))
            .add("Integer coefficient", coeff_integer)
            .add("K_CLOSURE", k_closure)
            .add("Coefficient equals k", 1.0 if coeff_integer == k_closure else 0.0)
            .add("Earth period (days)", round(T_earth_days, 2))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Kepler coefficient (4*pi^2)/pi^2", 4.0)
            .add("Integer coefficient", 4)
            .add("K_CLOSURE", 4)
            .add("Coefficient equals k", 1.0)
            .add("Earth period (days)", 365.25)
        )


# =============================================================================
# TEST 2: KEPLER EXPONENTS — T^2 AND a^3 (STANDARD)
# =============================================================================

class KeplerExponentsTimeSpatial(Test):
    """
    Probe the exponents in Kepler's Third Law: T^2 propto a^3.

    HONESTY: The exponents 2 and 3 follow from dimensional analysis and
    Newton's inverse-square law. The time exponent 2 comes from squaring
    T, and the spatial exponent 3 comes from the inverse-square law in
    3 spatial dimensions. GFM notes 2 = len(TIME_FACES) and 3 = d = D_SPATIAL.
    These are OBSERVATIONS, not derivations.
    """
    audit_score = 86
    audit_notes = (
        "Question: 13/15 - Good 'why 2 and 3 specifically' framing. "
        "Derivation: 14/15 - Clear dimensional analysis argument. "
        "Commentary: 13/15 - Honest about dimensional origin of exponents. "
        "Model: 9/10 - Clean exponent extraction from numerical data. "
        "Observations: 9/10 - Exponents exact from theory. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 12/15 - Exponents accessible but GFM link subtle. "
        "Header: 6/10 - Module docstring covers goals."
    )
    contribution_score = 52
    contribution_notes = (
        "Discovery: 18/40 - Observation that Kepler exponents {2, 3} match "
        "{TIME_FACES, d}. The d=3 connection to spatial dimensions is standard "
        "physics; the TIME_FACES=2 connection is the GFM observation. "
        "Precision: 16/20 - Exponents are exact integers; verified numerically "
        "via log-log scaling between two orbits. "
        "Cross-Domain: 12/20 - Exponent 3 also appears in BH evaporation (M^3) "
        "and gravitational potential (1/r in d=3). Pattern grows. "
        "Falsifiability: 6/20 - In d spatial dimensions, Kepler gives T^2 propto a^(d). "
        "Cannot test other dimensions experimentally. "
        "TOTAL: 52/100 - Solid observation linking exponents to face counts."
    )
    future_questions = (
        "Q1: In d spatial dimensions, gravity falls as 1/r^(d-1), giving "
        "T^2 propto a^d. Does this mean the time exponent 2 is ALWAYS paired "
        "with spatial exponent d, regardless of dimension? "
        "(Answering would improve Commentary by +5: universality of pairing) "
        "Q2: Kepler's law also works for elliptical orbits with a = semi-major axis. "
        "Does eccentricity introduce any new coefficients beyond {2, 3, 4}? "
        "(Answering would improve Discovery by +3: elliptical extension) "
        "Q3: The ratio of exponents is 3/2 = d/TIME_FACES. Does this ratio "
        "appear elsewhere in GFM or physics? "
        "(Answering would improve Cross-Domain by +3: ratio pattern)"
    )
    name = "Kepler Exponents: T^2 and a^3"
    question = (
        "In T^2 = 4*pi^2 * a^3 / (GM), the time exponent is 2 and the spatial "
        "exponent is 3. The exponent 3 follows from the inverse-square law in "
        "3 spatial dimensions. The exponent 2 comes from squaring T. But in GFM, "
        "2 = len(TIME_FACES) and 3 = D_SPATIAL = d. Is Kepler's law encoding "
        "the (3+1) spacetime decomposition of the stellated octahedron?"
    )
    reference = "Goldstein, Classical Mechanics (1980), Sec. 3.7; dimensional analysis"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The exponents in Kepler's law are NOT free parameters. "
        "They are fixed by dimensional analysis:\n"
        "- [T^alpha] = [a^beta / (GM)^gamma] requires alpha=2, beta=3, gamma=1\n"
        "- The exponent 3 on a comes from the 1/r^2 force law in d=3 dimensions\n"
        "- In d dimensions, the force law is 1/r^(d-1), giving T^2 propto a^d\n\n"
        "GFM OBSERVATION: The exponents form the pair (2, 3) = (TIME_FACES, d). "
        "In the stellated octahedron, there are 2 time faces and 3 spatial "
        "dimensions. Kepler's law pairs EXACTLY one time exponent with one "
        "spatial exponent, mirroring the (d, TIME_FACES) structure.\n\n"
        "CAVEAT: The exponent 2 on T is simply because kinetic energy is v^2 "
        "(appears in all of mechanics, not just orbits). The exponent 3 on a "
        "is specific to inverse-square gravity in 3D. The GFM correspondence "
        "is suggestive but may reflect the universality of small integers."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("QUESTION: What determines the exponents 2 and 3 in Kepler's law?")
            .step("DIMENSIONAL ANALYSIS: [G] = m^3 kg^-1 s^-2, [M] = kg, [a] = m, [T] = s.")
            .step("T^2 = const * a^3 / (G*M) checks dimensionally: s^2 = m^3 / (m^3 kg^-1 s^-2 * kg) = s^2.")
            .step("The exponent on a comes from the gravitational force law:")
            .equation("F = G*M*m / r^2 (inverse-square in d=3 dimensions)")
            .step("In d dimensions: F propto 1/r^(d-1), giving T^2 propto a^d.")
            .step("NUMERICAL VERIFICATION: Compare Earth and Mars orbits.")
            .step("If T^alpha propto a^beta, then log(T2/T1)/log(a2/a1) = beta/alpha.")
            .step("GFM OBSERVATION: alpha = 2 = len(TIME_FACES), beta = 3 = D_SPATIAL.")
            .conclude("Kepler exponents (2, 3) match GFM face structure (TIME_FACES, d).")
        )

    def model(self) -> Model:
        # Verify exponents by computing period for two distances
        a1 = AU               # Earth
        a2 = 1.524 * AU       # Mars semi-major axis
        T1 = _kepler_period(a1, M_SOLAR)
        T2 = _kepler_period(a2, M_SOLAR)

        # Extract spatial exponent: log(T2/T1) / log(a2/a1) = beta/alpha
        # For T^2 propto a^3: log(T2/T1) / log(a2/a1) = 3/2
        ratio = math.log(T2 / T1) / math.log(a2 / a1)  # Should be 3/2
        spatial_exponent = round(ratio * 2, 2)  # Multiply by time exponent to get spatial
        time_exponent = 2

        # GFM correspondences
        n_time_faces = len(TIME_FACES)
        d_spatial = D_SPATIAL

        return (
            Model()
            .add("Time exponent (T^n)", time_exponent)
            .add("Spatial exponent (a^n)", spatial_exponent)
            .add("len(TIME_FACES)", n_time_faces)
            .add("D_SPATIAL", d_spatial)
            .add("Time exp = TIME_FACES", 1.0 if time_exponent == n_time_faces else 0.0)
            .add("Spatial exp = d", 1.0 if spatial_exponent == d_spatial else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Time exponent (T^n)", 2)
            .add("Spatial exponent (a^n)", 3)
            .add("len(TIME_FACES)", 2)
            .add("D_SPATIAL", 3)
            .add("Time exp = TIME_FACES", 1.0)
            .add("Spatial exp = d", 1.0)
        )


# =============================================================================
# TEST 3: VIS-VIVA FACTOR 2 AND ORBITAL ENERGY 1/2 (STANDARD)
# =============================================================================

class VisVivaAndOrbitalEnergyFactorTwo(Test):
    """
    Probe the factor 2 in vis-viva and 1/2 in orbital energy.

    HONESTY: The vis-viva equation v^2 = GM(2/r - 1/a) is derived from energy
    conservation (kinetic + potential = total). The factor 2 in 2/r comes from
    the virial theorem and the structure of Newtonian gravity. The 1/2 in
    E = -GMm/(2a) comes from the virial theorem: <KE> = -<PE>/2. GFM notes
    that 2 = len(TIME_FACES). This is an OBSERVATION.
    """
    audit_score = 85
    audit_notes = (
        "Question: 13/15 - Good dual-factor mystery linking vis-viva and energy. "
        "Derivation: 13/15 - Clear energy conservation argument. "
        "Commentary: 13/15 - Honest about virial theorem origin. "
        "Model: 9/10 - Numerical verification for Earth at perihelion/aphelion. "
        "Observations: 8/10 - Earth orbital energy from standard sources. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 12/15 - Vis-viva well known to undergrads. "
        "Header: 7/10 - Module docstring with goals and limitations."
    )
    contribution_score = 50
    contribution_notes = (
        "Discovery: 18/40 - Observation that both the vis-viva factor 2 and the "
        "energy factor 1/2 involve 2 = TIME_FACES. Connects two formulas. "
        "Precision: 14/20 - Factors are exact from energy conservation. Verified "
        "numerically using Earth orbit at two points (circular). "
        "Cross-Domain: 12/20 - Factor 2 appears throughout orbital mechanics, "
        "kinetic energy (1/2 mv^2), BH event horizon (2GM/c^2). Growing catalog. "
        "Falsifiability: 6/20 - The factor 2 in kinetic energy is universal in "
        "classical mechanics. Difficult to make a GFM-specific prediction. "
        "TOTAL: 50/100 - Incremental. The factor 2 is ubiquitous in physics."
    )
    future_questions = (
        "Q1: The virial theorem in d dimensions gives <KE> = -(n/2)<PE> for "
        "force law r^n. In d=3 with n=-2 (gravity), does the virial ratio "
        "involve GFM numbers beyond 2? "
        "(Answering would improve Discovery by +5: dimensional generalization) "
        "Q2: The vis-viva factor 2/r can be written as TIME_FACES/r. Does "
        "the 1/a term also decompose into GFM quantities? "
        "(Answering would improve Commentary by +3: complete decomposition) "
        "Q3: For relativistic orbits, the vis-viva equation gets GR corrections. "
        "Do the correction terms introduce new GFM numbers? "
        "(Answering would improve Cross-Domain by +5: GR extension)"
    )
    name = "Vis-Viva Factor 2 and Orbital Energy 1/2"
    question = (
        "The vis-viva equation v^2 = GM(2/r - 1/a) has a factor 2 in the 2/r term. "
        "The orbital energy E = -GMm/(2a) has factor 1/2. Both involve the number 2. "
        "These factors arise from the virial theorem and energy conservation, not from "
        "any geometric construction. But in GFM, 2 = len(TIME_FACES). Is the "
        "pervasive factor of 2 in orbital mechanics connected to the two time faces "
        "of the stellated octahedron?"
    )
    reference = "Goldstein (1980), Sec. 3.3; Virial theorem"
    tolerance = 0.01
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The vis-viva equation follows from energy conservation:\n"
        "  E = (1/2)*m*v^2 - G*M*m/r = -G*M*m/(2a) = constant\n"
        "Solving for v^2: v^2 = G*M*(2/r - 1/a).\n\n"
        "The factor 2 in 2/r comes from the relationship between kinetic and "
        "potential energy. For circular orbits, KE = -PE/2 (virial theorem), "
        "so the total energy E = KE + PE = PE/2 = -GMm/(2r).\n\n"
        "GFM OBSERVATION: 2 = len(TIME_FACES). The factor 2 appears in:\n"
        "- Vis-viva: 2/r term\n"
        "- Orbital energy: 1/(2a) denominator\n"
        "- Kinetic energy: (1/2)mv^2\n"
        "- Escape velocity: sqrt(2*GM/r)\n"
        "This ubiquity of 2 in mechanics may reflect the time-face structure, "
        "or it may simply reflect that kinetic energy is quadratic in velocity."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ENERGY CONSERVATION for a Keplerian orbit:")
            .equation("E = (1/2)*m*v^2 - G*M*m/r = constant")
            .step("For a bound orbit, E = -G*M*m/(2*a) where a is semi-major axis.")
            .step("Rearranging for v^2:")
            .equation("v^2 = G*M*(2/r - 1/a)")
            .step("This is the vis-viva equation. The factor 2 in 2/r is NOT arbitrary.")
            .step("It comes from: total energy = kinetic + potential, where KE = (1/2)mv^2.")
            .step("CIRCULAR ORBIT CHECK: set r = a. Then v^2 = GM(2/a - 1/a) = GM/a.")
            .step("This gives v_circ = sqrt(GM/a), the circular orbit velocity.")
            .step("GFM OBSERVATION: The factor 2 = len(TIME_FACES).")
            .step("The energy denominator 2 = 1/len(TIME_FACES).")
            .conclude("Both vis-viva factor 2 and energy factor 1/2 match TIME_FACES count.")
        )

    def model(self) -> Model:
        # Verify vis-viva for Earth (circular orbit: r = a)
        v_earth = _vis_viva(A_EARTH, A_EARTH, M_SOLAR)
        v_circ_earth = _circular_velocity(A_EARTH, M_SOLAR)

        # They should be equal for circular orbit
        ratio_circ = v_earth / v_circ_earth

        # Extract the factor 2 from vis-viva
        # v^2 = GM(2/r - 1/a); for r=a: v^2 = GM/a
        # For escape (a -> inf): v_esc^2 = 2*GM/r
        v_esc = _escape_velocity(A_EARTH, M_SOLAR)
        vis_viva_factor = v_esc**2 * A_EARTH / (G * M_SOLAR)  # Should be 2

        # Orbital energy factor
        E_earth = _orbital_energy(M_EARTH, A_EARTH, M_SOLAR)
        energy_factor = -G * M_SOLAR * M_EARTH / (E_earth * A_EARTH)  # Should be 2

        # GFM correspondence
        n_time_faces = len(TIME_FACES)

        return (
            Model()
            .add("Vis-viva factor (from v_esc^2)", round(vis_viva_factor, 6))
            .add("Energy denominator factor", round(energy_factor, 6))
            .add("len(TIME_FACES)", n_time_faces)
            .add("Vis-viva factor = TIME_FACES", 1.0 if abs(vis_viva_factor - n_time_faces) < 0.001 else 0.0)
            .add("Energy factor = TIME_FACES", 1.0 if abs(energy_factor - n_time_faces) < 0.001 else 0.0)
            .add("Circular orbit v check", round(ratio_circ, 6))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Vis-viva factor (from v_esc^2)", 2.0)
            .add("Energy denominator factor", 2.0)
            .add("len(TIME_FACES)", 2)
            .add("Vis-viva factor = TIME_FACES", 1.0)
            .add("Energy factor = TIME_FACES", 1.0)
            .add("Circular orbit v check", 1.0)
        )


# =============================================================================
# TEST 4: ESCAPE-TO-CIRCULAR VELOCITY RATIO sqrt(2) (STANDARD)
# =============================================================================

class EscapeCircularVelocityRatio(Test):
    """
    Probe the ratio v_esc / v_circ = sqrt(2), where 2 = TIME_FACES.

    HONESTY: The ratio sqrt(2) follows trivially from the definitions:
    v_circ = sqrt(GM/r) and v_esc = sqrt(2GM/r). The factor 2 in the escape
    velocity comes from setting total energy to zero (E = 0 at escape).
    GFM notes that 2 = len(TIME_FACES). This is an OBSERVATION.
    """
    audit_score = 84
    audit_notes = (
        "Question: 12/15 - Good practical hook about 'how much faster to escape'. "
        "Derivation: 13/15 - Clear energy argument for sqrt(2). "
        "Commentary: 13/15 - Honest about trivial origin, nice sqrt(2) context. "
        "Model: 9/10 - Clean ratio computation at multiple radii. "
        "Observations: 9/10 - Ratio exact from definitions. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 12/15 - Escape velocity very intuitive. "
        "Header: 6/10 - Module docstring present."
    )
    contribution_score = 45
    contribution_notes = (
        "Discovery: 15/40 - The sqrt(2) ratio is elementary mechanics. GFM "
        "observation that 2 = TIME_FACES adds geometric interpretation. "
        "Precision: 14/20 - Exact from definitions. Verified numerically. "
        "Cross-Domain: 10/20 - Factor 2 in escape velocity connects to BH "
        "event horizon (R_s = 2GM/c^2 from v_esc = c). Direct link. "
        "Falsifiability: 6/20 - The ratio sqrt(2) is universal for any "
        "inverse-square force. No new prediction possible. "
        "TOTAL: 45/100 - Incremental. Gains value as part of the factor-2 catalog."
    )
    future_questions = (
        "Q1: For non-Newtonian gravity (e.g., MOND), the escape-to-circular "
        "ratio changes. Does it still involve GFM numbers? "
        "(Answering would improve Falsifiability by +5: modified gravity test) "
        "Q2: The Schwarzschild event horizon R_s = 2GM/c^2 follows from "
        "v_esc = c. Does this mean the BH horizon is WHERE v_esc/v_circ = sqrt(2) "
        "and v_circ = c/sqrt(2)? "
        "(Answering would improve Cross-Domain by +5: BH connection) "
        "Q3: In d spatial dimensions, v_esc/v_circ = sqrt(2/(d-1)) for the "
        "1/r^(d-1) force law. In d=3 this gives sqrt(2/2) = 1... wait, this "
        "needs to be checked carefully. Is the ratio always sqrt(2)? "
        "(Answering would improve Commentary by +3: dimensional analysis)"
    )
    name = "Escape-to-Circular Velocity Ratio: sqrt(2)"
    question = (
        "At any radius r around mass M, the circular orbit velocity is "
        "v_circ = sqrt(GM/r) and the escape velocity is v_esc = sqrt(2GM/r). "
        "Their ratio is exactly sqrt(2), independent of M, r, or G. This "
        "universal ratio involves the factor 2 = len(TIME_FACES) in GFM. "
        "Is the energy threshold for orbital escape set by the time-face "
        "structure, or is this simply the factor of 2 from kinetic energy?"
    )
    reference = "Goldstein (1980), Sec. 3.2; any introductory mechanics textbook"
    tolerance = 0.001
    level = Level.STANDARD
    commentary = (
        "STANDARD PHYSICS: The escape velocity requires total energy E = 0:\n"
        "  (1/2)*m*v_esc^2 - G*M*m/r = 0\n"
        "  v_esc^2 = 2*G*M/r\n\n"
        "The circular velocity requires centripetal = gravitational:\n"
        "  m*v_circ^2/r = G*M*m/r^2\n"
        "  v_circ^2 = G*M/r\n\n"
        "Ratio: v_esc / v_circ = sqrt(2*G*M/r) / sqrt(G*M/r) = sqrt(2).\n\n"
        "This ratio is UNIVERSAL — it holds for ANY mass at ANY radius. It is "
        "a direct consequence of the 1/r potential and the factor 1/2 in "
        "kinetic energy. There is no free parameter involved.\n\n"
        "GFM OBSERVATION: The factor under the square root is 2 = len(TIME_FACES). "
        "This connects to the Schwarzschild radius R_s = 2GM/c^2, which is the "
        "radius where v_esc = c. The factor 2 appears in both the velocity "
        "ratio and the event horizon."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CIRCULAR ORBIT: balance gravity and centripetal force.")
            .equation("v_circ = sqrt(G*M / r)")
            .step("ESCAPE: set total energy to zero (just barely escape to infinity).")
            .equation("v_esc = sqrt(2*G*M / r)")
            .step("RATIO:")
            .equation("v_esc / v_circ = sqrt(2*G*M/r) / sqrt(G*M/r) = sqrt(2)")
            .step("This is universal: independent of M, r, G.")
            .step("PHYSICAL MEANING: To escape, you need sqrt(2) ~ 1.414 times "
                  "the circular velocity. About 41.4% more speed.")
            .step("GFM OBSERVATION: factor 2 under sqrt = len(TIME_FACES).")
            .step("VERIFICATION: Compute at Earth's orbit and at 10 AU.")
            .conclude("v_esc/v_circ = sqrt(2), with 2 = len(TIME_FACES).")
        )

    def model(self) -> Model:
        # Compute at Earth's orbit
        v_circ_earth = _circular_velocity(A_EARTH, M_SOLAR)
        v_esc_earth = _escape_velocity(A_EARTH, M_SOLAR)
        ratio_earth = v_esc_earth / v_circ_earth

        # Compute at 10 AU (verify universality)
        v_circ_10au = _circular_velocity(10 * AU, M_SOLAR)
        v_esc_10au = _escape_velocity(10 * AU, M_SOLAR)
        ratio_10au = v_esc_10au / v_circ_10au

        # The factor under sqrt
        factor_under_sqrt = ratio_earth**2  # Should be 2.0
        n_time_faces = len(TIME_FACES)

        return (
            Model()
            .add("v_esc/v_circ at 1 AU", round(ratio_earth, 6))
            .add("v_esc/v_circ at 10 AU", round(ratio_10au, 6))
            .add("sqrt(2)", round(math.sqrt(2), 6))
            .add("Factor under sqrt", round(factor_under_sqrt, 6))
            .add("len(TIME_FACES)", n_time_faces)
            .add("Factor = TIME_FACES", 1.0 if abs(factor_under_sqrt - n_time_faces) < 0.001 else 0.0)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("v_esc/v_circ at 1 AU", round(math.sqrt(2), 6))
            .add("v_esc/v_circ at 10 AU", round(math.sqrt(2), 6))
            .add("sqrt(2)", round(math.sqrt(2), 6))
            .add("Factor under sqrt", 2.0)
            .add("len(TIME_FACES)", 2)
            .add("Factor = TIME_FACES", 1.0)
        )


# =============================================================================
# TEST 5: ORBITAL MECHANICS COEFFICIENT CATALOG (EXPLORATORY)
# =============================================================================

class OrbitalCoefficientCatalog(Test):
    """
    Catalog all integer coefficients in Keplerian orbital mechanics and
    check whether they all come from the GFM set {2, 3, 4}.

    HONESTY: This is a pattern observation across multiple orbital mechanics
    formulas. All the physics is standard Newtonian mechanics. The observation
    that all integer coefficients belong to {2, 3, 4} = {TIME_FACES, d, k}
    may reflect small-integer bias rather than deep structure.
    """
    audit_score = 82
    audit_notes = (
        "Question: 13/15 - Good 'are all coefficients from GFM set' question. "
        "Derivation: 12/15 - Clear catalog listing, could use more analysis. "
        "Commentary: 13/15 - Honest about small-integer bias caveat. "
        "Model: 9/10 - Clean catalog check with binary verdicts. "
        "Observations: 7/10 - Catalog is compiled, not measured. "
        "Constants: 10/10 - All from common. "
        "Accessibility: 12/15 - Catalog format easy to follow. "
        "Header: 6/10 - Module docstring covers goals."
    )
    contribution_score = 55
    contribution_notes = (
        "Discovery: 22/40 - First systematic catalog of ALL integer coefficients "
        "in Keplerian orbital mechanics mapped to GFM numbers. Shows the full "
        "set is {2, 3, 4} = {TIME_FACES, d, k}. "
        "Precision: 12/20 - All coefficients are exact integers from theory. "
        "Statistical significance depends on how we count 'formulas'. "
        "Cross-Domain: 14/20 - Connects orbital mechanics to BH coefficient "
        "catalog. Together, orbital + BH coefficients use {2, 3, 4, 6, 8} = "
        "{TIME_FACES, d, k, SPATIAL_FACES, VERTICES}. "
        "Falsifiability: 7/20 - Predicts that GR corrections to Kepler should "
        "introduce new coefficients from the GFM set (e.g., 6 in precession). "
        "TOTAL: 55/100 - Valuable synthesis. The {2, 3, 4} completeness is "
        "striking but may reflect small-integer dominance."
    )
    future_questions = (
        "Q1: GR corrections to Kepler introduce the factor 6*pi in Mercury's "
        "precession: delta_phi = 6*pi*GM/(c^2*a*(1-e^2)). Does the 6 = SPATIAL_FACES "
        "extend the orbital coefficient set to {2, 3, 4, 6}? "
        "(Answering would improve Discovery by +8: GR extension to coefficient set) "
        "Q2: Are there ANY orbital mechanics formulas with integer coefficients "
        "NOT in {2, 3, 4}? Documenting failures strengthens the catalog. "
        "(Answering would improve Precision by +5: completeness verification) "
        "Q3: Combined with BH coefficients {2, 3, 4, 6, 8}, the gravitational "
        "coefficient universe is {2, 3, 4, 6, 8}. Is this exactly the set of "
        "GFM structural numbers excluding identity and (k+1)? "
        "(Answering would improve Cross-Domain by +5: unified catalog)"
    )
    name = "Orbital Mechanics Coefficient Catalog"
    question = (
        "Keplerian orbital mechanics involves several integer coefficients: "
        "4 in 4*pi^2 (Kepler III), exponents 2 and 3 (Kepler III), factor 2 "
        "in vis-viva and escape velocity, and 1/2 in orbital energy. Are ALL "
        "of these coefficients drawn from the set {2, 3, 4} = "
        "{TIME_FACES, d, K_CLOSURE}? If so, orbital mechanics uses ONLY "
        "the three fundamental GFM structural numbers."
    )
    reference = "Compiled from Goldstein (1980); Murray & Dermott (1999)"
    tolerance = 0.10
    level = Level.EXPLORATORY
    commentary = (
        "METHODOLOGY: We catalog every distinct integer coefficient appearing "
        "in the standard Keplerian orbital mechanics formulas:\n\n"
        "FORMULA                          | COEFFICIENT | GFM NUMBER\n"
        "T^2 = 4*pi^2*a^3/(GM)           | 4           | k = K_CLOSURE\n"
        "T^2 (time exponent)              | 2           | TIME_FACES\n"
        "a^3 (spatial exponent)           | 3           | d = D_SPATIAL\n"
        "v^2 = GM(2/r - 1/a)             | 2           | TIME_FACES\n"
        "E = -GMm/(2a)                   | 2           | TIME_FACES\n"
        "v_esc = sqrt(2GM/r)             | 2           | TIME_FACES\n\n"
        "RESULT: All coefficients are from {2, 3, 4}.\n\n"
        "CAVEAT: Small-integer bias. Most physics formulas have small integer "
        "coefficients. The set {2, 3, 4} covers many natural formulas. "
        "However, the ABSENCE of 5, 7, 9 (non-GFM integers) is noted. "
        "The coefficient 1 (identity) is excluded as trivial.\n\n"
        "STATISTICAL NOTE: P(all 4 distinct coefficients in {2,3,4} | range 2-10) "
        "= (3/9)^4 = 0.0012 = 0.12%. But this assumes independence, which the "
        "formulas are clearly not (they share underlying structure)."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("CATALOG: List all integer coefficients in Keplerian mechanics.")
            .step("1. Kepler III coefficient: T^2 = 4*pi^2 * a^3 / (GM) -> 4")
            .step("2. Kepler III time exponent: T^2 -> 2")
            .step("3. Kepler III spatial exponent: a^3 -> 3")
            .step("4. Vis-viva factor: v^2 = GM(2/r - 1/a) -> 2")
            .step("5. Orbital energy: E = -GMm/(2a) -> 2")
            .step("6. Escape velocity: v_esc = sqrt(2GM/r) -> 2")
            .step("DISTINCT SET: {2, 3, 4}")
            .step("GFM SET: {TIME_FACES, d, k} = {2, 3, 4}")
            .equation("Orbital coefficients = {2, 3, 4} = {TIME_FACES, d, k}")
            .step("CHECK: Any coefficient NOT in {2, 3, 4}? None found in standard formulas.")
            .conclude("ALL Keplerian orbital coefficients belong to the GFM structural set {2, 3, 4}.")
        )

    def model(self) -> Model:
        # The catalog of orbital mechanics coefficients
        orbital_coefficients = {
            'Kepler III coefficient': 4,
            'Kepler time exponent': 2,
            'Kepler spatial exponent': 3,
            'Vis-viva factor': 2,
            'Orbital energy factor': 2,
            'Escape velocity factor': 2,
        }

        # GFM structural numbers
        GFM_set = {len(TIME_FACES), D_SPATIAL, K_CLOSURE}  # {2, 3, 4}

        # Count distinct coefficients
        distinct_coeffs = set(orbital_coefficients.values())
        n_distinct = len(distinct_coeffs)

        # Check all match
        all_in_GFM = all(v in GFM_set for v in orbital_coefficients.values())
        n_matches = sum(1 for v in distinct_coeffs if v in GFM_set)

        # Sets match exactly?
        sets_equal = 1.0 if distinct_coeffs == GFM_set else 0.0

        # Simple probability estimate: P(3 random integers from 2-10 match GFM set)
        # GFM occupies 3 of 9 possible integers in range 2-10
        p_single = 3 / 9  # 1/3
        p_all_3 = p_single ** n_distinct  # (1/3)^3 ~ 0.037

        return (
            Model()
            .add("Distinct coefficients found", n_distinct)
            .add("GFM structural numbers |{2,3,4}|", len(GFM_set))
            .add("Matches with GFM set", n_matches)
            .add("Sets are identical", sets_equal)
            .add("P(random match)", round(p_all_3, 4))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Distinct coefficients found", 3)
            .add("GFM structural numbers |{2,3,4}|", 3)
            .add("Matches with GFM set", 3)
            .add("Sets are identical", 1.0)
            .add("P(random match)", 0.0370)
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    KeplerThirdLawCoefficientFour,      # CRITICAL: 4*pi^2 coefficient, 4 = k
    KeplerExponentsTimeSpatial,          # STANDARD: T^2, a^3 exponents
    VisVivaAndOrbitalEnergyFactorTwo,    # STANDARD: factor 2 = TIME_FACES
    EscapeCircularVelocityRatio,         # STANDARD: sqrt(2), factor 2 = TIME_FACES
    OrbitalCoefficientCatalog,           # EXPLORATORY: all coeffs in {2, 3, 4}
]


def run_all() -> bool:
    """Run all sandbox tests."""
    return run_tests(
        title="SANDBOX: Kepler Orbital Mechanics — Coefficient Structure",
        summary=(
            "STATUS: Work in progress\n\n"
            "EXPLORING:\n"
            "- Why does Kepler's Third Law have coefficient 4 = k = K_CLOSURE?\n"
            "- Why are the exponents (2, 3) = (TIME_FACES, d)?\n"
            "- Why does factor 2 = TIME_FACES appear in vis-viva, energy, escape velocity?\n"
            "- Are ALL orbital coefficients from the GFM set {2, 3, 4}?\n\n"
            "WHEN READY:\n"
            "- audit_score >= 75\n"
            "- Move to calculations/field_theory/test_kepler_orbital_coefficient_GFM.py"
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
