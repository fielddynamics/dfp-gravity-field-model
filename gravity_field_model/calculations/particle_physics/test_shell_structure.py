"""
Electron Shell Structure: A Geometric Interpretation

STATUS: ALTERNATIVE FRAMING (not derivation)

These tests examine electron shell capacities (2, 8, 18, 32) through the lens
of GFD geometry. The capacities follow the well-established 2n^2 formula from
quantum mechanics.

CRITICAL HONESTY NOTE:

The shell capacities 2, 8, 18, 32 are DERIVED in standard quantum mechanics from:
    1. Schrodinger equation solution for hydrogen-like atoms
    2. Angular momentum quantization giving (2l+1) m_l states per subshell
    3. Spin-1/2 doubling from Dirac equation

GFD does NOT derive these capacities. Instead, GFD observes that:
    - k = 4 (Field Closure constant)
    - The capacities can be written as: k/2, 2k, 2*9, 2k^2
    - This provides a geometric PICTURE but not a DERIVATION

The question is whether this geometric reframing is:
    (a) A genuine insight into underlying structure, or
    (b) Retrofitting k=4 to match known values

This file documents the correspondences honestly without claiming derivation.
"""

from gravity_field_model.framework import *


# =============================================================================
# CONSTANTS
# =============================================================================

K = 4  # Field Closure constant
D = K - 1  # d = 3 SPATIAL dimensions
TIME_FACES = 2  # One per tetrahedron

# Shell capacities from quantum mechanics
SHELL_CAPACITIES = {
    1: 2,   # K shell: 2 = 2(1)^2
    2: 8,   # L shell: 8 = 2(2)^2
    3: 18,  # M shell: 18 = 2(3)^2
    4: 32,  # N shell: 32 = 2(4)^2
}

# Noble gas electron counts
NOBLE_GASES = {
    'He': 2,
    'Ne': 10,
    'Ar': 18,
    'Kr': 36,
    'Xe': 54,
    'Rn': 86,
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def shell_capacity_qm(n):
    """
    Standard quantum mechanics formula: C(n) = 2n^2
    
    Derivation (QM):
        - n^2 spatial states from angular momentum: sum of (2l+1) for l=0 to n-1
        - Factor of 2 from spin-1/2 (two m_s values per spatial state)
    """
    return 2 * n * n


def shell_capacity_gfd(n):
    """
    GFD geometric interpretation: C(n) = n^2 orbital cells x 2 spin states
    
    NOTE: This produces the SAME result as 2n^2 but factored differently.
    This is not a derivation; it's a re-expression.
    """
    orbital_cells = n * n
    spin_factor = TIME_FACES  # 2, from dual tetrahedra
    return orbital_cells * spin_factor


# =============================================================================
# TESTS: SHELL CAPACITIES
# =============================================================================

class ShellCapacitiesQM(Test):
    """
    BASELINE: Standard quantum mechanics gives shell capacities 2, 8, 18, 32
    via the 2n^2 formula.
    
    This is well-established physics, not GFD content. It provides the
    reference values that GFD attempts to reframe geometrically.
    """
    name = "Shell Capacities (QM Baseline)"
    question = "What are the electron shell capacities from the standard 2n^2 formula?"
    reference = "Quantum mechanics: C(n) = 2n^2"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("STANDARD QUANTUM MECHANICS (not GFD derivation).")
            .step("PREMISE: Schrodinger equation yields n^2 spatial orbitals per shell.")
            .step("STEP 1: For shell n: Sum of (2l+1) for l = 0 to n-1 = n^2 spatial states.")
            .step("STEP 2: Spin-1/2 gives 2 spin states per spatial state.")
            .step("STEP 3: Total capacity: C(n) = 2n^2 = 2, 8, 18, 32 for n = 1, 2, 3, 4.")
            .conclude("OUTPUT: K=2, L=8, M=18, N=32 (from QM, not GFD).")
        )
    
    commentary = (
        "The 2n^2 shell capacity formula is a result of standard quantum mechanics. "
        "It comes from solving the Schrodinger equation for the hydrogen atom and "
        "applying Pauli exclusion. GFD does not derive this formula; it provides "
        "an alternative geometric picture that happens to match."
    )
    
    def model(self):
        return (
            Model()
            .add("K shell (n=1)", shell_capacity_qm(1))
            .add("L shell (n=2)", shell_capacity_qm(2))
            .add("M shell (n=3)", shell_capacity_qm(3))
            .add("N shell (n=4)", shell_capacity_qm(4))
        )
    
    def observations(self):
        return (
            Observed()
            .add("K shell (n=1)", 2)
            .add("L shell (n=2)", 8)
            .add("M shell (n=3)", 18)
            .add("N shell (n=4)", 32)
        )


class GFDShellReframing(Test):
    """
    GFD reframes 2n^2 as (n^2 orbital cells) x (2 spin states).
    
    The factor of 2 is associated with TIME faces.
    The n^2 factor is associated with orbital geometry.
    
    This produces identical results to 2n^2 because it IS 2n^2,
    just factored differently. It is not a derivation.
    """
    name = "GFD Shell Reframing"
    question = "Does the GFD geometric reframing produce the same shell capacities as 2n^2?"
    reference = "GFD: C(n) = n^2 x TIME_faces"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("ALTERNATIVE FACTORIZATION (not derivation).")
            .step("PREMISE: GFD refactors 2n^2 as: (orbital cells) x (spin factor).")
            .step("STEP 1: Orbital cells = n^2 (spatial configurations).")
            .step("STEP 2: Spin factor = TIME_faces = 2 (dual tetrahedra).")
            .step("STEP 3: C(n) = n^2 x 2 = 2n^2 (same formula, different interpretation).")
            .conclude("OUTPUT: GFD produces 2, 8, 18, 32 (matches QM because it IS 2n^2).")
        )
    
    commentary = (
        "GFD associates the spin factor of 2 with the dual tetrahedra (one TIME face "
        "per tetrahedron). This is a geometric interpretation of spin doubling, not "
        "a derivation. The n^2 factor for orbital cells lacks a clear geometric "
        "origin in GFD. This reframing matches QM because it is algebraically identical."
    )
    
    def model(self):
        return (
            Model()
            .add("K shell (GFD)", shell_capacity_gfd(1))
            .add("L shell (GFD)", shell_capacity_gfd(2))
            .add("M shell (GFD)", shell_capacity_gfd(3))
            .add("N shell (GFD)", shell_capacity_gfd(4))
        )
    
    def observations(self):
        return (
            Observed()
            .add("K shell (GFD)", shell_capacity_qm(1))
            .add("L shell (GFD)", shell_capacity_qm(2))
            .add("M shell (GFD)", shell_capacity_qm(3))
            .add("N shell (GFD)", shell_capacity_qm(4))
        )


class SpinFactorFromTimeFaces(Test):
    """
    The factor of 2 in shell capacities comes from electron spin.
    GFD interprets this as the 2 TIME faces of the stellated octahedron.
    
    This is the same correspondence documented in other particle physics tests.
    """
    name = "Spin Factor = TIME Faces"
    question = "Does the spin degeneracy factor of 2 correspond to the TIME face count?"
    reference = "Spin-1/2 gives 2 spin states"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("CORRESPONDENCE (documented elsewhere).")
            .step("PREMISE: Electrons have spin-1/2, giving 2s+1 = 2 spin states.")
            .step("STEP 1: Field Chamber has 2 TIME faces (one per tetrahedron).")
            .step("STEP 2: GFD correspondence: spin states = TIME faces = 2.")
            .step("STEP 3: Each orbital can hold 2 electrons (one per TIME face).")
            .conclude("OUTPUT: Spin factor = 2 = TIME faces (correspondence).")
        )
    
    commentary = (
        "The factor of 2 in 2n^2 arises from spin degeneracy in standard physics. "
        "GFD interprets this as reflecting the two TIME faces of the stellated "
        "octahedron. This is a consistent interpretation across GFD's particle "
        "physics framework."
    )
    
    def model(self):
        return (
            Model()
            .add("TIME faces", TIME_FACES)
            .add("Spin states (2s+1)", 2)
            .add("Electrons per orbital", 2)
        )
    
    def observations(self):
        return (
            Observed()
            .add("TIME faces", 2)
            .add("Spin states (2s+1)", 2)
            .add("Electrons per orbital", 2)
        )


class PauliExclusionInterpretation(Test):
    """
    Pauli exclusion limits each orbital to 2 electrons.
    GFD interprets this as: 1 electron per tetrahedron x 2 tetrahedra = 2.
    
    This is a geometric PICTURE, not a derivation of Pauli exclusion.
    """
    name = "Pauli Exclusion Interpretation"
    question = "Can Pauli exclusion be pictured as one electron per tetrahedron?"
    reference = "Pauli exclusion: max 2 electrons per orbital"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("GEOMETRIC INTERPRETATION (not derivation of Pauli).")
            .step("PREMISE: Pauli exclusion: no two identical fermions in same quantum state.")
            .step("STEP 1: Each orbital defines a spatial state.")
            .step("STEP 2: GFD: one electron on Tet A TIME face, one on Tet B TIME face.")
            .step("STEP 3: Maximum 2 electrons per orbital (different TIME faces).")
            .conclude("OUTPUT: Pauli limit = 2 = tetrahedra count (geometric picture).")
        )
    
    commentary = (
        "Pauli exclusion is derived in QM from the antisymmetry requirement for "
        "fermion wavefunctions. GFD provides a geometric PICTURE: each tetrahedron "
        "can host one electron in a given orbital, so the dual structure limits "
        "occupancy to 2. This does not derive Pauli exclusion from geometry."
    )
    
    def model(self):
        return (
            Model()
            .add("Tetrahedra", 2)
            .add("Electrons per tetrahedron per orbital", 1)
            .add("Max electrons per orbital", 2)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tetrahedra", 2)
            .add("Electrons per tetrahedron per orbital", 1)
            .add("Max electrons per orbital", 2)
        )


# =============================================================================
# TESTS: NUMERICAL OBSERVATIONS (honesty about retrofitting)
# =============================================================================

class KShellNumerology(Test):
    """
    K shell capacity = 2 = k/2 where k=4.
    
    HONESTY: This is retrofitting k=4 to match the known value 2.
    There is no derivation; 2 = k/2 is observed, not predicted.
    """
    name = "K Shell = k/2 (Observation)"
    question = "Can the K shell capacity be written as k/2?"
    reference = "K shell = 2, k = 4"
    level = Level.EXPLORATORY
    
    def derivation(self):
        return (
            Derivation()
            .step("NUMERICAL OBSERVATION (not derivation).")
            .step("PREMISE: K shell capacity = 2 (from QM). k = 4 (Field Closure).")
            .step("STEP 1: Observe that 2 = k/2 = 4/2.")
            .step("STEP 2: k/2 = TIME face count = spin states (consistent).")
            .step("STEP 3: This is an observation, not a prediction or derivation.")
            .conclude("OUTPUT: K shell = 2 = k/2 (observed correspondence).")
        )
    
    commentary = (
        "The K shell capacity of 2 equals k/2 where k=4. This is noted as a "
        "correspondence: the first shell capacity equals half the Field Closure "
        "constant, which also equals the TIME face count. Whether this is "
        "meaningful or coincidental is left as an open question."
    )
    
    def model(self):
        return Model().add("K shell", K // 2)
    
    def observations(self):
        return Observed().add("K shell", 2)


class LShellNumerology(Test):
    """
    L shell capacity = 8 = 2k where k=4.
    
    This also equals the stellated octahedron vertex count.
    """
    name = "L Shell = 2k (Observation)"
    question = "Can the L shell capacity be written as 2k?"
    reference = "L shell = 8, 2k = 8"
    level = Level.EXPLORATORY
    
    def derivation(self):
        return (
            Derivation()
            .step("NUMERICAL OBSERVATION (not derivation).")
            .step("PREMISE: L shell capacity = 8 (from QM). k = 4 (Field Closure).")
            .step("STEP 1: Observe that 8 = 2k = 2 x 4.")
            .step("STEP 2: 2k = stellated octahedron vertex count (consistent).")
            .step("STEP 3: This is an observation, not a prediction or derivation.")
            .conclude("OUTPUT: L shell = 8 = 2k = vertices (observed correspondence).")
        )
    
    commentary = (
        "The L shell capacity of 8 equals 2k, the stellated octahedron vertex count. "
        "This suggests a correspondence between second-shell electrons and Field "
        "Chamber vertices. The interpretation is that completing the L shell fills "
        "all geometric vertex positions."
    )
    
    def model(self):
        return Model().add("L shell", 2 * K)
    
    def observations(self):
        return Observed().add("L shell", 8)


class NobleGasSequencePattern(Test):
    """
    Noble gas differences: 8, 8, 18, 18, 32.
    
    The pattern shows each capacity appearing twice (Aufbau filling order).
    This is standard chemistry, not GFD content.
    """
    name = "Noble Gas Differences"
    question = "What pattern do noble gas electron count differences follow?"
    reference = "Periodic table: He=2, Ne=10, Ar=18, Kr=36, Xe=54, Rn=86"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("STANDARD CHEMISTRY (Aufbau principle).")
            .step("PREMISE: Noble gases occur at filled-shell electron configurations.")
            .step("STEP 1: He(2), Ne(10), Ar(18), Kr(36), Xe(54), Rn(86).")
            .step("STEP 2: Differences: 8, 8, 18, 18, 32 (each capacity appears twice).")
            .step("STEP 3: Pattern from orbital filling order (s, p, d, f subshells).")
            .conclude("OUTPUT: Differences 8, 8, 18, 18, 32 (from Aufbau, not GFD).")
        )
    
    commentary = (
        "The noble gas sequence reflects orbital filling order (Aufbau principle). "
        "Each shell capacity appears twice because of how s, p, d, f subshells fill "
        "across periods. This is standard chemistry. GFD can note that 8 = 2k, but "
        "the doubling pattern comes from Aufbau, not geometry."
    )
    
    def model(self):
        nobles = [NOBLE_GASES[g] for g in ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']]
        diffs = [nobles[i+1] - nobles[i] for i in range(len(nobles)-1)]
        return (
            Model()
            .add("Diff He->Ne", diffs[0])
            .add("Diff Ne->Ar", diffs[1])
            .add("Diff Ar->Kr", diffs[2])
            .add("Diff Kr->Xe", diffs[3])
            .add("Diff Xe->Rn", diffs[4])
        )
    
    def observations(self):
        return (
            Observed()
            .add("Diff He->Ne", 8)
            .add("Diff Ne->Ar", 8)
            .add("Diff Ar->Kr", 18)
            .add("Diff Kr->Xe", 18)
            .add("Diff Xe->Rn", 32)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    # Baseline and reframing
    ShellCapacitiesQM,
    GFDShellReframing,
    
    # Spin interpretation
    SpinFactorFromTimeFaces,
    PauliExclusionInterpretation,
    
    # Numerical observations
    KShellNumerology,
    LShellNumerology,
    NobleGasSequencePattern,
]


def run_all():
    """Run all shell structure tests."""
    return run_tests(
        title="Electron Shell Structure: A Geometric Interpretation",
        summary=(
            "These tests examine electron shell capacities through GFD geometry.\n\n"
            "IMPORTANT: Shell capacities (2, 8, 18, 32) are DERIVED by quantum mechanics "
            "from the Schrodinger equation and Pauli exclusion. GFD does NOT derive these "
            "values; it provides an alternative GEOMETRIC PICTURE that produces the same "
            "numbers.\n\n"
            "The spin factor of 2 is associated with TIME faces (one per tetrahedron). "
            "The n^2 orbital factor lacks clear geometric origin in GFD.\n\n"
            "Numerical observations (k/2=2, 2k=8) are noted as correspondences, not "
            "predictions. The reader should evaluate whether this geometric reframing "
            "provides insight or merely retrofits k=4 to known values."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
