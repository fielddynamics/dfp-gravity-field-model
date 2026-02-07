"""
MOND Acceleration Scale from GFM Geometry
=========================================

This module examines GFM's derivation of the MOND acceleration scale a_0
from electron properties and the Field Closure constant k=4.

THE DERIVATION CHAIN:
1. a_0 = k^2 * G * m_e / r_e^2  (MOND scale from electron + k=4)
2. H_flat = 2*pi*a_0 / c        (Hubble from horizon thermodynamics)
3. H = H_flat / sqrt(k/pi)      (geometry correction)

THE CLAIM:
Starting from k=4 (tetrahedral), G, and electron properties (m_e, r_e),
the derivation produces:
- a_0 ~ 1.22e-10 m/s^2 (MOND acceleration scale)
- H ~ 70 km/s/Mpc (Hubble constant)

CRITICAL ASSESSMENT:
The formula a_0 = k^2 * G * m_e / r_e^2 uses:
- k^2 = 16 (from k=4, the tetrahedral closure)
- G (known gravitational constant)
- m_e, r_e (electron mass and classical radius)

The question: Is the factor k^2 = 16 DERIVED from geometry,
or is it FITTED to produce the known a_0?

References:
- GFM Textbook Chapter 6
- Milgrom (1983) MOND
- GW170817 Hubble measurement
"""

import sys
import math

from gravity_field_model.framework import *
from gravity_field_model.common import (
    C, G, M_E as ELECTRON_MASS, R_E, K, A_MOND,
)

# =============================================================================
# CONSTANTS
# =============================================================================

PI = math.pi

# Hubble constant observations (km/s/Mpc)
# These are observational reference values, not model parameters
H_GW170817 = 70.0   # Gravitational wave measurement (GW170817)
H_PLANCK = 67.4     # CMB measurement (Planck 2018)
H_SHOES = 73.0      # Distance ladder (SH0ES collaboration)

# Conversion factor: 1 km/s/Mpc to s^-1
KM_S_MPC_TO_SI = 1000 / (3.086e22)  # ~3.24e-20 s^-1

# MOND phenomenological value from common
A_MOND_OBSERVED = A_MOND  # m/s^2


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_geometry_bridge():
    """Geometry bridge sqrt(k/pi) = 1.128."""
    return math.sqrt(K / PI)


def get_a0_from_geometry():
    """MOND acceleration from GFM: a_0 = k^2 * G * m_e / r_e^2."""
    return (K**2) * G * ELECTRON_MASS / (R_E**2)


def get_hubble_flat():
    """H_flat from a_0 via horizon thermodynamics: H = 2*pi*a_0/c."""
    a_0 = get_a0_from_geometry()
    H_SI = 2 * PI * a_0 / C
    return H_SI / KM_S_MPC_TO_SI  # Convert to km/s/Mpc


def get_hubble_corrected():
    """H with geometry correction: H = H_flat / sqrt(k/pi)."""
    H_flat = get_hubble_flat()
    return H_flat / get_geometry_bridge()


# =============================================================================
# TESTS
# =============================================================================

class MONDScaleFromGeometry(Test):
    """
    THE a_0 DERIVATION: a_0 = k^2 * G * m_e / r_e^2
    
    This is the key formula that connects GFM geometry to MOND.
    
    WHY k^2 = 16?
    k = 4 is the tetrahedral closure constant (minimum faces to enclose 3D).
    k^2 = 16 represents coupling between two field envelopes, each with k faces.
    
    RESULT: a_0 = 16 * G * m_e / r_e^2 = 1.22e-10 m/s^2
    This matches the MOND phenomenological value to ~2%.
    """
    name = "MOND Acceleration a_0 = k^2 * G * m_e / r_e^2"
    question = (
        "Why does the MOND transition occur at a_0 ~ 1.2e-10 m/s^2? Field envelope coupling "
        "with k^2 = 16 channels gives a_0 = k^2 * G * m_e / r_e^2, matching observations."
    )
    reference = "GFM Framework, Milgrom (1983)"
    tolerance = 0.05
    level = Level.CRITICAL
    audit_score = 91
    audit_notes = None
    future_questions = (
        "Q1: Why specifically k^2 = 16 coupling channels rather than k or 2k? "
        "(Answering would improve Derivation by +3 points: justifying the face-to-face counting) "
        "Q2: How do field envelope interactions at r_e scale produce effects at galactic scales? "
        "(Answering would improve Commentary by +2 points: bridging micro-macro connection) "
        "Q3: What distinguishes GFM's a_0 derivation from dark matter explanations? "
        "(Answering would improve Audience Accessibility by +3 points: contrasting paradigms)"
    )
    
    commentary = (
        "THE DERIVATION:\n"
        "GFM claims the MOND acceleration scale emerges from Field Envelope\n"
        "geometry. The electron's classical radius r_e defines the fundamental\n"
        "tile size, and the electron mass m_e defines the tile's inertia.\n\n"
        "Step 1: Two Field Envelopes couple through their k=4 faces.\n"
        "Step 2: The coupling involves k^2 = 16 face-to-face channels.\n"
        "Step 3: The gravitational acceleration from one tile on another is:\n"
        "        a = G * m_e / r_e^2 (standard Newtonian)\n"
        "Step 4: With k^2 coupling channels: a_0 = k^2 * G * m_e / r_e^2\n\n"
        "CALCULATION:\n"
        "a_0 = 16 * (6.674e-11) * (9.109e-31) / (2.818e-15)^2\n"
        "a_0 = 16 * 7.64e-11 m/s^2 = 1.22e-10 m/s^2\n\n"
        "CRITICAL ASSESSMENT:\n"
        "The formula works, but why k^2 specifically? The textbook argues\n"
        "this comes from face-to-face coupling between tetrahedra, but\n"
        "the factor could be post-hoc. The test documents the result."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("MOND SCALE FROM GFM GEOMETRY:")
            .step("k = 4 (tetrahedral closure constant)")
            .step("k^2 = 16 (face-to-face coupling channels)")
            .step("G = 6.674e-11 m^3/(kg*s^2)")
            .step("m_e = 9.109e-31 kg")
            .step("r_e = 2.818e-15 m")
            .equation("a_0 = k^2 * G * m_e / r_e^2")
            .step("a_0 = 16 * 6.674e-11 * 9.109e-31 / (2.818e-15)^2")
            .step("a_0 = 16 * 7.64e-11 = 1.22e-10 m/s^2")
            .step("MOND observed: a_0 ~ 1.2e-10 m/s^2")
            .conclude("GFM predicts a_0 to within ~2% of MOND value.")
        )
    
    def model(self) -> Model:
        a_0 = get_a0_from_geometry()
        error_pct = abs(a_0 - A_MOND_OBSERVED) / A_MOND_OBSERVED * 100
        match = 1.0 if error_pct < 5 else 0.0
        
        return (
            Model()
            .add("k", K)
            .add("k^2", K**2)
            .add("a_0 predicted (m/s^2)", a_0)
            .add("a_0 MOND (m/s^2)", A_MOND_OBSERVED)
            .add("Error (%)", round(error_pct, 1))
            .add("Match (< 5%)", match)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("k", 4)
            .add("k^2", 16)
            .add("a_0 predicted (m/s^2)", 1.22e-10)
            .add("a_0 MOND (m/s^2)", 1.2e-10)
            .add("Error (%)", 1.7)
            .add("Match (< 5%)", 1.0)
        )


class GeometryBridge(Test):
    """
    The geometry bridge sqrt(k/pi) = 1.128.
    
    This factor converts between:
    - Spherical geometry (continuous, characterized by pi)
    - Tetrahedral geometry (discrete, characterized by k=4)
    
    WHY sqrt(k/pi)?
    Area scales as square of length. The bridge converts 2D areas
    (like solid angle) between discrete and continuous frames.
    """
    name = "Geometry Bridge sqrt(k/pi) = 1.128"
    question = (
        "Why does sqrt(k/pi) bridge continuous and discrete geometry? Spherical geometry "
        "uses pi (4*pi steradians), while tetrahedral uses k=4 discrete ports. The ratio bridges them."
    )
    reference = "GFM Framework"
    tolerance = 0.001
    level = Level.STANDARD
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Why does the bridge involve sqrt(k/pi) rather than just k/pi? "
        "(Answering would improve Derivation by +2 points: explaining area vs length scaling) "
        "Q2: Where else in physics do spherical-to-discrete geometry conversions appear? "
        "(Answering would improve Audience Accessibility by +3 points: providing familiar analogies) "
        "Q3: Does the bridge factor appear in other GFM derivations beyond Hubble? "
        "(Answering would improve Commentary by +2 points: showing framework consistency)"
    )
    
    commentary = (
        "THE GEOMETRY BRIDGE:\n\n"
        "Spherical geometry uses pi for solid angles (4*pi steradians).\n"
        "Tetrahedral geometry uses k=4 for discrete coupling ports.\n"
        "The ratio k/pi = 4/3.14159 = 1.273 relates these frames.\n"
        "For length (not area), take sqrt: sqrt(k/pi) = 1.128.\n\n"
        "PHYSICAL MEANING:\n"
        "sqrt(k/pi) > 1 means discrete coupling is less efficient than\n"
        "spherical. When converting from spherical to tetrahedral,\n"
        "divide by sqrt(k/pi) to reduce the effective coupling."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("GEOMETRY BRIDGE:")
            .step("Spherical: characterized by pi (from 4*pi steradians)")
            .step("Tetrahedral: characterized by k=4 (discrete ports)")
            .step("Area ratio: k/pi = 4/pi = 1.273")
            .step("Length ratio (sqrt): sqrt(k/pi) = sqrt(1.273) = 1.128")
            .step("Since k > pi, the bridge > 1")
            .conclude("sqrt(k/pi) = 1.128 bridges discrete and continuous geometry.")
        )
    
    def model(self) -> Model:
        k_over_pi = K / PI
        bridge = math.sqrt(k_over_pi)
        k_greater_pi = 1 if K > PI else 0
        
        return (
            Model()
            .add("k", K)
            .add("pi", round(PI, 4))
            .add("k/pi", round(k_over_pi, 4))
            .add("sqrt(k/pi)", round(bridge, 4))
            .add("k > pi", k_greater_pi)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("k", 4)
            .add("pi", 3.1416)
            .add("k/pi", 1.2732)
            .add("sqrt(k/pi)", 1.1284)
            .add("k > pi", 1)
        )


class HubbleFromMOND(Test):
    """
    Hubble constant from a_0: H = 2*pi*a_0/c / sqrt(k/pi) ~ 70 km/s/Mpc.
    
    THE DERIVATION CHAIN:
    1. a_0 = k^2 * G * m_e / r_e^2 = 1.22e-10 m/s^2 (from geometry)
    2. H_flat = 2*pi*a_0/c = 79 km/s/Mpc (horizon thermodynamics)
    3. H = H_flat / sqrt(k/pi) = 70 km/s/Mpc (geometry correction)
    
    RESULT: H = 70 km/s/Mpc, matching GW170817 to <1%.
    """
    name = "Hubble Constant H ~ 70 km/s/Mpc from Geometry"
    question = (
        "Why does the Hubble constant emerge from electron geometry? From a_0 via horizon "
        "thermodynamics, H = (2*pi*a_0/c) / sqrt(k/pi) = 70 km/s/Mpc, matching GW170817."
    )
    reference = "GW170817: 70.0 +/- 12 km/s/Mpc"
    tolerance = 0.02
    level = Level.CRITICAL
    audit_score = 93
    audit_notes = None
    future_questions = (
        "Q1: Why does GFM predict 70 km/s/Mpc while Planck and SH0ES disagree with each other? "
        "(Answering would improve Commentary by +3 points: addressing the Hubble tension directly) "
        "Q2: How does the horizon thermodynamics step connect to the Gibbons-Hawking temperature? "
        "(Answering would improve Derivation by +2 points: making the physics chain explicit) "
        "Q3: What future observations could definitively test the GFM Hubble prediction? "
        "(Answering would improve Observation Quality by +3 points: identifying discriminating tests)"
    )
    
    commentary = (
        "THE DERIVATION:\n\n"
        "Step 1: a_0 = k^2 * G * m_e / r_e^2 = 1.22e-10 m/s^2\n"
        "Step 2: H_flat = 2*pi*a_0/c (horizon thermodynamics)\n"
        "        H_flat = 2*pi * 1.22e-10 / 3e8 = 2.56e-18 s^-1\n"
        "        H_flat = 79 km/s/Mpc\n"
        "Step 3: Apply geometry correction: H = H_flat / sqrt(k/pi)\n"
        "        H = 79 / 1.128 = 70 km/s/Mpc\n\n"
        "COMPARISON TO OBSERVATIONS:\n"
        "- GW170817 (direct): 70.0 +/- 12 km/s/Mpc [BEST MATCH]\n"
        "- Planck CMB: 67.4 +/- 0.5 km/s/Mpc\n"
        "- SH0ES distance ladder: 73.0 +/- 1.0 km/s/Mpc\n\n"
        "The GFM prediction sits exactly at the GW170817 value,\n"
        "between Planck and SH0ES (the 'Hubble tension')."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("HUBBLE FROM GFM:")
            .step("a_0 = k^2 * G * m_e / r_e^2 = 1.22e-10 m/s^2")
            .step("H_flat = 2*pi*a_0/c = 2*pi * 1.22e-10 / 3e8")
            .step("H_flat = 2.56e-18 s^-1 = 79 km/s/Mpc")
            .step("Geometry correction: divide by sqrt(k/pi) = 1.128")
            .step("H = 79 / 1.128 = 70.0 km/s/Mpc")
            .conclude("GFM predicts H = 70 km/s/Mpc, matching GW170817.")
        )
    
    def model(self) -> Model:
        H_flat = get_hubble_flat()
        H = get_hubble_corrected()
        bridge = get_geometry_bridge()
        
        error_gw = abs(H - H_GW170817)
        error_planck = abs(H - H_PLANCK)
        error_shoes = abs(H - H_SHOES)
        
        closest_gw = 1 if (error_gw < error_planck and error_gw < error_shoes) else 0
        
        return (
            Model()
            .add("H_flat (km/s/Mpc)", round(H_flat, 1))
            .add("sqrt(k/pi)", round(bridge, 4))
            .add("H predicted", round(H, 1))
            .add("GW170817", H_GW170817)
            .add("Planck", H_PLANCK)
            .add("SH0ES", H_SHOES)
            .add("Closest to GW170817", closest_gw)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("H_flat (km/s/Mpc)", 79.0)
            .add("sqrt(k/pi)", 1.1284)
            .add("H predicted", 70.0)
            .add("GW170817", 70.0)
            .add("Planck", 67.4)
            .add("SH0ES", 73.0)
            .add("Closest to GW170817", 1)
        )


class DerivationConsistency(Test):
    """
    Round-trip consistency check: m_e -> a_0 -> H -> m_e.
    
    The derivation should close: starting from electron mass,
    deriving H, then inverting should recover m_e.
    
    This tests mathematical consistency, not physical truth.
    """
    name = "Round-Trip Consistency Check"
    question = (
        "Why must the derivation chain m_e -> a_0 -> H -> m_e close exactly? Algebraic "
        "consistency requires sub-percent round-trip error, validating internal logic."
    )
    reference = "Self-consistency requirement"
    tolerance = 0.01
    level = Level.STANDARD
    audit_score = 80
    audit_notes = None
    future_questions = (
        "Q1: What does perfect round-trip closure tell us about the derivation's validity? "
        "(Answering would improve Commentary by +3 points: interpreting consistency properly) "
        "Q2: Could numerical precision limitations mask a small algebraic inconsistency? "
        "(Answering would improve Observation Quality by +2 points: addressing computation limits) "
        "Q3: Are there other closed loops in GFM that could serve as consistency tests? "
        "(Answering would improve Derivation by +2 points: suggesting additional verification paths)"
    )
    
    commentary = (
        "This test checks INTERNAL CONSISTENCY, not physical correctness.\n\n"
        "If the algebra is correct, starting from m_e, deriving H,\n"
        "then inverting should recover m_e exactly.\n\n"
        "The round-trip error measures only numerical precision,\n"
        "not whether the underlying physics is correct."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ROUND-TRIP CONSISTENCY:")
            .step("Forward: m_e -> a_0 = k^2*G*m_e/r_e^2 -> H = 2*pi*a_0/(c*sqrt(k/pi))")
            .step("Reverse: H -> a_0 = H*c*sqrt(k/pi)/(2*pi) -> m_e = a_0*r_e^2/(k^2*G)")
            .step("The forward and reverse should be exact inverses.")
            .conclude("Round-trip tests algebraic consistency only.")
        )
    
    def model(self) -> Model:
        # Forward
        H_predicted = get_hubble_corrected()
        
        # Reverse: from H, recover m_e
        H_SI = H_predicted * KM_S_MPC_TO_SI
        a_0_recovered = H_SI * C * get_geometry_bridge() / (2 * PI)
        m_e_recovered = a_0_recovered * R_E**2 / (K**2 * G)
        
        error_pct = abs(m_e_recovered - ELECTRON_MASS) / ELECTRON_MASS * 100
        
        return (
            Model()
            .add("m_e original (kg)", ELECTRON_MASS)
            .add("H derived (km/s/Mpc)", round(H_predicted, 2))
            .add("m_e recovered (kg)", m_e_recovered)
            .add("Round-trip error (%)", round(error_pct, 4))
        )
    
    def observations(self) -> Observed:
        return None


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    MONDScaleFromGeometry,
    GeometryBridge,
    HubbleFromMOND,
    DerivationConsistency,
]


def run_all() -> bool:
    """Run all Hubble-Electron-MOND tests."""
    return run_tests(
        title="MOND Acceleration Scale from GFM Geometry",
        summary=(
            "This module tests GFM's derivation of the MOND acceleration scale.\n\n"
            "THE DERIVATION CHAIN:\n"
            "1. a_0 = k^2 * G * m_e / r_e^2 = 1.22e-10 m/s^2 (geometry)\n"
            "2. H_flat = 2*pi*a_0/c = 79 km/s/Mpc (horizon thermodynamics)\n"
            "3. H = H_flat / sqrt(k/pi) = 70 km/s/Mpc (geometry correction)\n\n"
            "RESULTS:\n"
            "- a_0 predicted: 1.22e-10 m/s^2 (vs MOND 1.2e-10, error 2%)\n"
            "- H predicted: 70 km/s/Mpc (vs GW170817 70.0, error <1%)\n\n"
            "CRITICAL QUESTION:\n"
            "Is the factor k^2 = 16 derived from geometry, or fitted to data?"
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
