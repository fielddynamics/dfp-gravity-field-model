"""
Particle Physics: Charge and Spin Correspondences

STATUS: CONSISTENCY CHECKS (not derivations)

These tests verify that GFD's charge quantum (1/d = 1/3) produces consistent
results for composite particle charges, and document the spin/TIME-face
correspondence.

WHAT THESE TESTS DEMONSTRATE:

1. CHARGE CONSISTENCY: Using q = 1/3, all Standard Model particle charges
   are correctly reproduced. This is CONSISTENCY with the Port Ratio, not
   a derivation of why quarks have the charges they do.

2. SPIN CORRESPONDENCE: The 2 TIME faces match the 2 spin states of fermions.
   This is a numerical correspondence, not a derivation of spin-1/2.

3. COLOR STRUCTURE: The 3 vertices per face match the 3 colors of QCD.
   Complete face activation (3 vertices = color neutral) is consistent
   with confinement phenomenology.

WHAT WAS REMOVED (Standard Model documentation without GFD content):
    - QCD confinement scale (pure QCD, no GFD)
    - Neutron beta decay (pure weak interaction, no GFD)
    - Alpha running (pure QED, no GFD)
    - Asymptotic freedom (pure QCD, no GFD)
    - Pion Goldstone boson (pure QCD chiral symmetry, no GFD)
    - Fermi coupling (pure electroweak, no GFD)
    - Quark mass hierarchy (no derivation, just lists masses)
    - Cabibbo angle (admitted numerical fit with fudge factor)
"""

from gfd_model_v2.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

K_CLOSURE = 4                    # Tetrahedral face count
D = K_CLOSURE - 1                # d = 3 SPATIAL dimensions
VERTICES = 2 * K_CLOSURE         # 8 vertices
TIME_FACES = 2                   # One per tetrahedron
SPATIAL_FACES = 6                # Three per tetrahedron

# The fundamental charge quantum from Port Ratio
Q_MIN = 1 / D                    # 1/3


# =============================================================================
# CHARGE CONSISTENCY TESTS
# =============================================================================

class UpQuarkChargeConsistency(Test):
    """
    The up quark has charge +2/3 = 2 x (1/3).
    
    Using the Port Ratio q = 1/3, the up quark charge corresponds to
    2 active vertices on a SPATIAL face of Tetrahedron A.
    
    This is CONSISTENCY, not derivation. The coefficient 2 is assigned
    based on the Standard Model value, not derived from geometry.
    """
    name = "Up Quark Charge Consistency"
    question = "Is the up quark charge +2/3 consistent with 2 activated vertices at q = 1/3 each?"
    reference = "Up quark charge = +2/3 e"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Port Ratio q = 1/d = 1/3 (charge per vertex).")
            .step("STEP 1: Up quark ASSIGNED to activate 2 vertices on Tetrahedron A SPATIAL face.")
            .step("STEP 2: Q_up = (vertices) x (charge/vertex) = 2 x (1/3) = +2/3.")
            .step("STEP 3: Positive sign from Tetrahedron A association.")
            .conclude("OUTPUT: Q_up = +2/3 (consistent with 2 vertices at q = 1/3).")
        )
    
    commentary = (
        "The up quark's charge of +2/3 equals 2 x (1/3), consistent with activating "
        "2 of 3 vertices on a triangular SPATIAL face. NOTE: The assignment '2 vertices' "
        "is made to match the known charge, not derived from geometry. GFD provides "
        "a picture consistent with the value, but does not derive it."
    )
    
    def model(self):
        vertices_active = 2  # Assigned to match Standard Model
        charge = vertices_active * Q_MIN
        return (
            Model()
            .add("Charge quantum", Q_MIN)
            .add("Active vertices (assigned)", vertices_active)
            .add("Up quark charge", charge)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Charge quantum", 1/3)
            .add("Active vertices (assigned)", 2)
            .add("Up quark charge", 2/3)
        )


class DownQuarkChargeConsistency(Test):
    """
    The down quark has charge -1/3 = -1 x (1/3).
    
    Using the Port Ratio, this corresponds to 1 active vertex on
    Tetrahedron B (giving negative sign).
    """
    name = "Down Quark Charge Consistency"
    question = "Is the down quark charge -1/3 consistent with 1 activated vertex on Tet B?"
    reference = "Down quark charge = -1/3 e"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Port Ratio q = 1/d = 1/3 (charge per vertex).")
            .step("STEP 1: Down quark ASSIGNED to activate 1 vertex on Tetrahedron B SPATIAL face.")
            .step("STEP 2: Q_down = -(vertices) x (charge/vertex) = -1 x (1/3) = -1/3.")
            .step("STEP 3: Negative sign from Tetrahedron B association.")
            .conclude("OUTPUT: Q_down = -1/3 (consistent with 1 vertex on Tet B).")
        )
    
    commentary = (
        "The down quark's charge of -1/3 equals -1 x (1/3), consistent with activating "
        "1 vertex on Tetrahedron B. The negative sign indicates antimatter-sector "
        "association. This is a consistency check, not a derivation."
    )
    
    def model(self):
        vertices_active = 1  # Assigned
        charge = -vertices_active * Q_MIN  # Negative from Tet B
        return (
            Model()
            .add("Charge quantum", Q_MIN)
            .add("Active vertices (Tet B)", vertices_active)
            .add("Down quark charge", charge)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Charge quantum", 1/3)
            .add("Active vertices (Tet B)", 1)
            .add("Down quark charge", -1/3)
        )


class BaryonNumberConsistency(Test):
    """
    Each quark carries baryon number B = 1/3.
    Three quarks combine to form a baryon with B = 1.
    
    This matches the Port Ratio: each quark occupies 1/d = 1/3 of a
    complete triangular face configuration.
    """
    name = "Baryon Number = 1/d"
    question = "Does quark baryon number B = 1/3 correspond to the Port Ratio 1/d?"
    reference = "Quark baryon number = 1/3"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Port Ratio = 1/d = 1/3 (one vertex out of three on a face).")
            .step("STEP 1: Each quark occupies 1 vertex of a 3-vertex face: B = 1/3.")
            .step("STEP 2: Baryon = 3 quarks = 3 vertices = complete face: B = 3 x (1/3) = 1.")
            .step("STEP 3: Meson = quark + antiquark: B = (1/3) + (-1/3) = 0.")
            .conclude("OUTPUT: Quark B = 1/3, Baryon B = 1, Meson B = 0.")
        )
    
    commentary = (
        "Baryon number 1/3 per quark matches the Port Ratio exactly. A complete face "
        "(3 vertices = baryon) has B = 1. A meson (quark + antiquark) has B = 0 from "
        "cancellation. This is a clean numerical correspondence."
    )
    
    def model(self):
        b_quark = 1 / D  # 1/3
        b_baryon = 3 * b_quark
        b_meson = b_quark + (-b_quark)
        return (
            Model()
            .add("Quark baryon number", b_quark)
            .add("Baryon (3 quarks)", b_baryon)
            .add("Meson (q + qbar)", b_meson)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Quark baryon number", 1/3)
            .add("Baryon (3 quarks)", 1)
            .add("Meson (q + qbar)", 0)
        )


class DeltaPlusPlusConsistency(Test):
    """
    The Delta++ baryon (uuu) has charge +2 = 3 x (+2/3).
    
    Three up quarks, each with +2/3, give the maximum baryon charge.
    This is a consistency check of the charge arithmetic.
    """
    name = "Delta++ Charge = +2"
    question = "Is the Delta++ charge consistent with three up quarks?"
    reference = "Delta++ charge = +2e"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Up quark charge Q_u = +2/3.")
            .step("STEP 1: Delta++ composition: uuu (three up quarks).")
            .step("STEP 2: Q_Delta++ = 3 x Q_u = 3 x (+2/3) = +2.")
            .step("STEP 3: Maximum baryon charge from 3 x maximum quark charge.")
            .conclude("OUTPUT: Delta++ charge = +2 (consistent).")
        )
    
    commentary = (
        "The Delta++ charge of +2 follows from adding three up quark charges. "
        "This represents maximum positive charge for a baryon: 3 x 2 = 6 "
        "activated vertices contributing positive charge."
    )
    
    def model(self):
        q_up = 2 * Q_MIN  # +2/3
        n_quarks = 3
        q_delta = n_quarks * q_up
        return (
            Model()
            .add("Up quark charge", q_up)
            .add("Number of quarks", n_quarks)
            .add("Delta++ charge", q_delta)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Up quark charge", 2/3)
            .add("Number of quarks", 3)
            .add("Delta++ charge", 2.0)
        )


class OmegaMinusConsistency(Test):
    """
    The Omega- baryon (sss) has charge -1 = 3 x (-1/3).
    
    Three strange quarks (same charge as down) give unit negative charge.
    """
    name = "Omega- Charge = -1"
    question = "Is the Omega- charge consistent with three strange quarks?"
    reference = "Omega- charge = -1e"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Strange quark charge Q_s = -1/3 (same as down quark).")
            .step("STEP 1: Omega- composition: sss (three strange quarks).")
            .step("STEP 2: Q_Omega- = 3 x Q_s = 3 x (-1/3) = -1.")
            .step("STEP 3: This confirmed quark model prediction in 1964.")
            .conclude("OUTPUT: Omega- charge = -1 (consistent).")
        )
    
    commentary = (
        "The Omega- charge of -1 confirmed the quark model in 1964 before its discovery. "
        "Three strange quarks, each with -1/3, sum to -1. This represents complete "
        "face activation on Tetrahedron B (antimatter sector)."
    )
    
    def model(self):
        q_strange = -1 * Q_MIN  # -1/3
        n_quarks = 3
        q_omega = n_quarks * q_strange
        return (
            Model()
            .add("Strange quark charge", q_strange)
            .add("Number of quarks", n_quarks)
            .add("Omega- charge", q_omega)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Strange quark charge", -1/3)
            .add("Number of quarks", 3)
            .add("Omega- charge", -1.0)
        )


class PositronChargeConsistency(Test):
    """
    The positron has charge +1, opposite to the electron's -1.
    
    In GFD, the positron occupies Tetrahedron A (opposite to electron's Tet B),
    demonstrating matter-antimatter charge conjugation.
    """
    name = "Positron Charge = +1"
    question = "Is positron charge consistent with the dual tetrahedron matter/antimatter structure?"
    reference = "Positron charge = +1e"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Dual tetrahedra provide matter (Tet A) and antimatter (Tet B) sectors.")
            .step("STEP 1: Electron: complete face on Tet B -> Q_e = -3 x (1/3) = -1.")
            .step("STEP 2: Positron: complete face on Tet A -> Q_pos = +3 x (1/3) = +1.")
            .step("STEP 3: Annihilation: Q_e + Q_pos = -1 + 1 = 0 (charge conserved).")
            .conclude("OUTPUT: Positron charge = +1 (opposite tetrahedron gives opposite sign).")
        )
    
    commentary = (
        "The positron's +1 charge arises from complete face activation on Tetrahedron A "
        "(matter sector), while the electron activates the complementary face on "
        "Tetrahedron B (antimatter sector). This demonstrates how the dual structure "
        "provides a geometric basis for charge conjugation."
    )
    
    def model(self):
        q_electron = -D * Q_MIN  # -1 (Tet B)
        q_positron = D * Q_MIN   # +1 (Tet A)
        sum_charge = q_electron + q_positron
        return (
            Model()
            .add("Electron charge", q_electron)
            .add("Positron charge", q_positron)
            .add("Sum (annihilation)", sum_charge)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Electron charge", -1.0)
            .add("Positron charge", 1.0)
            .add("Sum (annihilation)", 0.0)
        )


# =============================================================================
# SPIN AND STRUCTURE CORRESPONDENCES
# =============================================================================

class FermionSpinCorrespondence(Test):
    """
    All fermions have spin-1/2, giving 2 spin states.
    GFD proposes: spin = 1 / (TIME faces) = 1/2.
    
    This is a CORRESPONDENCE, not a derivation. Spin-1/2 comes from
    Dirac equation and Lorentz group representation theory.
    """
    name = "Fermion Spin = 1/2"
    question = "Does fermion spin-1/2 correspond to the 2 TIME faces of the Field Chamber?"
    reference = "Fermion spin = 1/2"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Field Chamber has 2 TIME faces (one per tetrahedron).")
            .step("STEP 1: GFD correspondence: spin quantum = 1 / (TIME faces) = 1/2.")
            .step("STEP 2: Spin states = 2s + 1 = 2 (up and down).")
            .step("STEP 3: Each spin state corresponds to one TIME face activation.")
            .conclude("OUTPUT: Spin = 1/2, Spin states = 2 = TIME faces.")
        )
    
    commentary = (
        "Fermion spin-1/2 corresponds numerically to 1/(TIME faces) = 1/2. The two "
        "spin projections (up/down) may represent activation of Tetrahedron A versus "
        "Tetrahedron B TIME faces. This is a GFD interpretation, not a replacement "
        "for the Dirac equation derivation of spin-1/2."
    )
    
    def model(self):
        spin_states = TIME_FACES  # 2
        spin_value = 1 / TIME_FACES  # 1/2
        return (
            Model()
            .add("TIME faces", TIME_FACES)
            .add("Spin quantum number", spin_value)
            .add("Spin states", spin_states)
        )
    
    def observations(self):
        return (
            Observed()
            .add("TIME faces", 2)
            .add("Spin quantum number", 0.5)
            .add("Spin states", 2)
        )


class NeutrinoFlavorCorrespondence(Test):
    """
    There are exactly 3 light neutrino flavors (e, mu, tau).
    This was measured from Z boson decay width at LEP.
    
    GFD has d = 3 SPATIAL dimensions. The correspondence is noted.
    """
    name = "3 Neutrino Flavors = d"
    question = "Does the neutrino flavor count match the SPATIAL dimension count d = 3?"
    reference = "LEP measurement: N_nu = 2.984 +/- 0.008"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: From Field Closure, d = k - 1 = 3 SPATIAL dimensions.")
            .step("STEP 1: Each tetrahedron has d = 3 SPATIAL faces.")
            .step("STEP 2: LEP measured N_nu = 2.984 (consistent with exactly 3).")
            .step("STEP 3: Numerical correspondence: d = 3 = neutrino flavors.")
            .conclude("OUTPUT: SPATIAL faces = 3, Neutrino flavors = 3 (correspondence).")
        )
    
    commentary = (
        "The 3 light neutrino flavors match d = 3 SPATIAL dimensions exactly. Each "
        "flavor may correspond to one SPATIAL face. However, the LEP measurement "
        "determined N_nu from physics (Z decay width), not from geometry. This is "
        "a numerical correspondence, not an explanation of why 3 generations exist."
    )
    
    def model(self):
        d_spatial = D  # 3
        n_measured = 2.984  # LEP result
        return (
            Model()
            .add("SPATIAL dimensions (d)", d_spatial)
            .add("Measured N_nu (LEP)", n_measured)
        )
    
    def observations(self):
        return (
            Observed()
            .add("SPATIAL dimensions (d)", 3)
            .add("Measured N_nu (LEP)", 2.984)
        )


class ColorNeutralityCorrespondence(Test):
    """
    All observable hadrons are color-neutral (color singlets).
    Baryons combine RGB; mesons combine color + anticolor.
    
    GFD: Complete face (3 vertices) = color neutral.
    Partial face (1-2 vertices) = colored (confined).
    """
    name = "Color Neutrality = Complete Face"
    question = "Does color neutrality correspond to complete triangular face activation?"
    reference = "QCD confinement: only color singlets propagate"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Triangular faces have d = 3 vertices, matching 3 color charges.")
            .step("STEP 1: Baryon (qqq): 3 quarks activate all 3 vertices (R+G+B = white).")
            .step("STEP 2: Meson (q-qbar): color + anticolor cancels to colorless.")
            .step("STEP 3: Partial activation (1-2 vertices) carries net color, cannot propagate.")
            .conclude("OUTPUT: Complete face = color neutral, Partial = confined.")
        )
    
    commentary = (
        "Color confinement requires observable particles to be color singlets. In the "
        "GFD picture, this corresponds to complete triangular face activation (baryons) "
        "or color-anticolor cancellation (mesons). Partial face states are confined, "
        "consistent with isolated quarks never being observed. This is a structural "
        "analogy, not a derivation of QCD dynamics."
    )
    
    def model(self):
        colors = D  # 3 colors (R, G, B)
        vertices_per_face = D  # 3 vertices
        baryon_quarks = D  # 3 quarks for RGB
        meson_constituents = 2  # color + anticolor
        return (
            Model()
            .add("QCD colors", colors)
            .add("Vertices per face", vertices_per_face)
            .add("Baryon quark count", baryon_quarks)
            .add("Meson constituents", meson_constituents)
        )
    
    def observations(self):
        return (
            Observed()
            .add("QCD colors", 3)
            .add("Vertices per face", 3)
            .add("Baryon quark count", 3)
            .add("Meson constituents", 2)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    # Charge consistency
    UpQuarkChargeConsistency,
    DownQuarkChargeConsistency,
    BaryonNumberConsistency,
    DeltaPlusPlusConsistency,
    OmegaMinusConsistency,
    PositronChargeConsistency,
    
    # Spin and structure
    FermionSpinCorrespondence,
    NeutrinoFlavorCorrespondence,
    ColorNeutralityCorrespondence,
]


def run_all():
    """Run all advanced particle physics tests."""
    return run_tests(
        title="Charge and Spin Correspondences",
        summary=(
            "These tests verify CONSISTENCY of GFD's charge quantum (1/d = 1/3) with "
            "Standard Model particle charges, and document spin/structure correspondences.\n\n"
            "CHARGE TESTS: Verify that using q = 1/3, all particle charges are correctly "
            "reproduced. This is consistency, not derivation; the vertex counts are "
            "assigned to match known charges.\n\n"
            "STRUCTURE TESTS: Document correspondences between geometric counts (TIME faces, "
            "SPATIAL faces, vertices) and particle physics multiplicities (spin states, "
            "generations, colors).\n\n"
            "REMOVED: Tests that merely documented Standard Model physics without GFD content "
            "(QCD running, electroweak physics, quark mass hierarchies)."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
