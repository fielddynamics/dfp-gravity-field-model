"""
Electron Shell Structure: A Geometric Interpretation

STATUS: ALTERNATIVE FRAMING (not derivation)

MOTIVATION:
Why do electron shells hold 2, 8, 18, 32 electrons? Quantum mechanics derives
this from the Schrodinger equation: C(n) = 2n^2. But why this formula? GFM
offers a geometric interpretation: the factor of 2 corresponds to the 2 TIME
faces (one per tetrahedron), providing a visual picture for spin degeneracy.

CRITICAL HONESTY NOTE:
GFM does NOT derive shell capacities. Quantum mechanics derives them rigorously:
    1. Schrodinger equation -> n^2 spatial orbitals per shell
    2. Spin-1/2 doubling -> factor of 2
    3. Result: C(n) = 2n^2 = 2, 8, 18, 32

GFM observes that:
    - k = 4 (Field Closure constant)
    - K shell = k/2 = 2
    - L shell = 2k = 8
    - TIME faces = 2 = spin degeneracy factor

This provides a geometric PICTURE that matches the formula, not a replacement
for the quantum mechanical derivation.

audit_score = 84
audit_notes = None
"""

from gravity_field_model.framework import *
from gravity_field_model.common import K_CLOSURE


# =============================================================================
# DERIVED CONSTANTS
# =============================================================================

K = K_CLOSURE  # Field Closure constant (imported from common)
D = K - 1  # d = 3 SPATIAL dimensions
N_TIME_FACES = 2  # One per tetrahedron (textbook Chapter 9)

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


def shell_capacity_GFM(n):
    """
    GFM geometric interpretation: C(n) = n^2 orbital cells x 2 spin states
    
    NOTE: This produces the SAME result as 2n^2 but factored differently.
    This is not a derivation; it's a re-expression with geometric meaning.
    """
    orbital_cells = n * n
    spin_factor = N_TIME_FACES  # 2, from dual tetrahedra
    return orbital_cells * spin_factor


# =============================================================================
# TESTS: SHELL CAPACITIES
# =============================================================================

class ShellCapacitiesQM(Test):
    """
    Why do electron shells hold 2, 8, 18, 32 electrons?
    
    Quantum mechanics answers this definitively via C(n) = 2n^2. The Schrodinger
    equation gives n^2 spatial orbitals per shell, and spin-1/2 doubles each
    orbital's capacity. This is the established baseline against which GFM's
    geometric interpretation is compared.
    
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Why does the Schrodinger equation produce n^2 orbitals per shell? "
        "(Answering would improve Derivation by +3 points: connects QM math to geometry) "
        "Q2: Could GFM provide an independent derivation of the 2n^2 formula? "
        "(Answering would improve Question by +2 points: tests predictive vs descriptive) "
        "Q3: How do relativistic corrections modify shell capacities? "
        "(Answering would improve Commentary by +2 points: addresses Dirac vs Schrodinger)"
    )
    """
    name = "Shell Capacities (QM Baseline)"
    question = "Why do electron shells hold 2, 8, 18, 32 electrons?"
    reference = "Quantum mechanics: C(n) = 2n^2"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Each shell has more room as you move outward from the nucleus.")
            .step("ORBITAL COUNT: Schrodinger equation gives n^2 spatial orbitals in shell n.")
            .step("SPIN DOUBLING: Each orbital holds 2 electrons (spin up and spin down).")
            .step("FORMULA: C(n) = 2 x n^2 = 2, 8, 18, 32 for n = 1, 2, 3, 4.")
            .step("VERIFICATION: Noble gases He(2), Ne(10), Ar(18) confirm cumulative shells.")
            .conclude("RESULT: Shell capacity follows from angular momentum quantization + spin.")
        )
    
    commentary = (
        "The factor of 2 in 2n^2 comes from spin degeneracy: each spatial orbital can "
        "host one spin-up and one spin-down electron. GFM interprets this factor as "
        "reflecting the 2 TIME faces of the stellated octahedron, giving a geometric "
        "picture for why spin doubles orbital capacity."
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


class GFMShellReframing(Test):
    """
    GFM reframes 2n^2 as (n^2 orbital cells) x (2 spin states).
    
    The factor of 2 is associated with TIME faces.
    The n^2 factor is associated with orbital geometry.
    
    This produces identical results to 2n^2 because it IS 2n^2,
    just factored differently. It is not a derivation.
    """
    name = "GFM Shell Reframing"
    question = "Does the GFM geometric reframing produce the same shell capacities as 2n^2?"
    reference = "GFM: C(n) = n^2 x TIME_faces"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("ALTERNATIVE FACTORIZATION (not derivation).")
            .step("PREMISE: GFM refactors 2n^2 as: (orbital cells) x (spin factor).")
            .step("STEP 1: Orbital cells = n^2 (spatial configurations).")
            .step("STEP 2: Spin factor = TIME_faces = 2 (dual tetrahedra).")
            .step("STEP 3: C(n) = n^2 x 2 = 2n^2 (same formula, different interpretation).")
            .conclude("OUTPUT: GFM produces 2, 8, 18, 32 (matches QM because it IS 2n^2).")
        )
    
    commentary = (
        "GFM associates the spin factor of 2 with the dual tetrahedra (one TIME face "
        "per tetrahedron). This is a geometric interpretation of spin doubling, not "
        "a derivation. The n^2 factor for orbital cells lacks a clear geometric "
        "origin in GFM. This reframing matches QM because it is algebraically identical."
    )
    
    def model(self):
        return (
            Model()
            .add("K shell (GFM)", shell_capacity_GFM(1))
            .add("L shell (GFM)", shell_capacity_GFM(2))
            .add("M shell (GFM)", shell_capacity_GFM(3))
            .add("N shell (GFM)", shell_capacity_GFM(4))
        )
    
    def observations(self):
        return (
            Observed()
            .add("K shell (GFM)", shell_capacity_qm(1))
            .add("L shell (GFM)", shell_capacity_qm(2))
            .add("M shell (GFM)", shell_capacity_qm(3))
            .add("N shell (GFM)", shell_capacity_qm(4))
        )


class SpinFactorFromTimeFaces(Test):
    """
    Why does spin contribute a factor of exactly 2 to shell capacity?
    
    Spin-1/2 gives 2s+1 = 2 states (up and down), doubling each orbital's
    electron capacity. GFM interprets this factor as the 2 TIME faces of the
    stellated octahedron: one electron per TIME face per orbital.
    
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Does the TIME face interpretation predict anything about spin-orbit coupling? "
        "(Answering would improve Derivation by +3 points: connects to fine structure) "
        "Q2: Why do only two electrons fit per orbital, not three or four? "
        "(Answering would improve Question by +2 points: justifies factor from geometry) "
        "Q3: How does the TIME face picture relate to Hund's rules for orbital filling? "
        "(Answering would improve Commentary by +2 points: connects to chemistry rules)"
    )
    """
    name = "Spin Factor = TIME Faces"
    question = "Why does spin contribute a factor of exactly 2 to orbital capacity?"
    reference = "Dirac equation: spin-1/2 gives 2 projections"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: The dual tetrahedra have 2 TIME faces at opposite poles.")
            .step("SPIN PHYSICS: Spin-1/2 gives 2s+1 = 2 states per spatial orbital.")
            .step("ORBITAL CAPACITY: Each orbital holds 2 electrons (one up, one down).")
            .step("GEOMETRIC MATCH: 2 TIME faces = 2 spin states.")
            .step("INTERPRETATION: Spin-up -> Tet A TIME face; Spin-down -> Tet B TIME face.")
            .conclude("RESULT: The factor 2 in 2n^2 reflects the dual tetrahedron structure.")
        )
    
    commentary = (
        "The ubiquitous factor of 2 in atomic physics (2n^2 shell capacity, 2 electrons "
        "per orbital, 2 spin states) finds a unified geometric origin in the 2 TIME faces "
        "of the stellated octahedron. This suggests spin is not just an abstract quantum "
        "number but reflects the polar structure of the Field Chamber."
    )
    
    def model(self):
        return (
            Model()
            .add("TIME faces", N_TIME_FACES)
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
    Why can at most 2 electrons occupy the same orbital?
    
    Pauli exclusion forbids identical fermions in the same quantum state. With
    2 spin states per orbital, the maximum is 2 electrons. GFM visualizes this
    geometrically: one electron per tetrahedron, and there are exactly 2 tetrahedra.
    
    This is a PICTURE, not a derivation. Pauli exclusion comes from wavefunction
    antisymmetry, not from geometry.
    
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Why do bosons not obey Pauli exclusion while fermions do? "
        "(Answering would improve Question by +3 points: connects spin-statistics to geometry) "
        "Q2: Does wavefunction antisymmetry have a geometric interpretation in GFM? "
        "(Answering would improve Derivation by +2 points: bridges QM formalism to geometry) "
        "Q3: How does Pauli exclusion lead to electron degeneracy pressure in stars? "
        "(Answering would improve Audience Accessibility by +2 points: astrophysical application)"
    )
    """
    name = "Pauli Exclusion Interpretation"
    question = "Why is orbital occupancy limited to exactly 2 electrons?"
    reference = "Pauli exclusion principle: identical fermions cannot share quantum states"
    level = Level.STANDARD
    tolerance = 0.01
    
    def derivation(self):
        return (
            Derivation()
            .step("INTUITION: Two tetrahedra, two 'slots' per orbital.")
            .step("PAULI PRINCIPLE: No two identical fermions in the same quantum state.")
            .step("SPIN STATES: Each orbital has 2 spin states (up, down).")
            .step("GEOMETRIC PICTURE: One electron on Tet A TIME face, one on Tet B.")
            .step("LIMIT: 2 electrons per orbital = 2 tetrahedra per Field Chamber.")
            .conclude("RESULT: The dual structure provides a visual for Pauli's factor of 2.")
        )
    
    commentary = (
        "Pauli exclusion limits orbital occupancy, but QM does not explain why the limit "
        "is specifically 2. GFM offers a visual answer: the stellated octahedron has 2 "
        "tetrahedra, and each can host one electron per orbital. This makes the factor 2 "
        "feel natural rather than arbitrary, even though the underlying physics is wavefunction "
        "antisymmetry."
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
    Why does the innermost shell hold exactly 2 electrons?
    
    The K shell (n=1) has capacity C(1) = 2(1)^2 = 2. This equals k/2 = 4/2 = 2,
    where k = 4 is the Field Closure constant. It also equals the TIME face count.
    
    HONESTY: This is retrofitting k=4 to the known value. We observe the pattern
    but do not claim to derive it.
    
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Is k/2 = 2 a fundamental relationship or numerical coincidence? "
        "(Answering would improve Derivation by +3 points: tests if pattern is predictive) "
        "Q2: Why is helium so chemically inert with just 2 electrons? "
        "(Answering would improve Commentary by +2 points: connects to noble gas stability) "
        "Q3: Does the K shell capacity relate to the 2 tetrahedra apex vertices? "
        "(Answering would improve Question by +2 points: geometric K shell interpretation)"
    )
    """
    name = "K Shell = k/2 (Observation)"
    question = "Why does the K shell hold exactly 2 electrons?"
    reference = "Helium: 2 electrons fill the K shell"
    level = Level.EXPLORATORY
    
    def derivation(self):
        return (
            Derivation()
            .step("OBSERVATION: K shell capacity = 2 (from QM formula 2n^2 with n=1).")
            .step("FIELD CLOSURE: k = 4 faces for tetrahedral closure.")
            .step("PATTERN: 2 = k/2 = 4/2.")
            .step("ALSO: 2 = TIME faces = spin states.")
            .step("HONESTY: We observe this pattern; we do not derive it.")
            .conclude("RESULT: K shell = 2 = k/2 = TIME faces (numerical correspondence).")
        )
    
    commentary = (
        "The K shell's capacity of 2 has multiple geometric interpretations: k/2, the "
        "TIME face count, and the spin degeneracy. Whether these are coincidences or "
        "reflect deeper structure is an open question. The correspondence is exact, "
        "not approximate."
    )
    
    def model(self):
        return Model().add("K shell", K // 2)
    
    def observations(self):
        return Observed().add("K shell", 2)


class LShellNumerology(Test):
    """
    Why does the L shell hold exactly 8 electrons?
    
    The L shell (n=2) has capacity C(2) = 2(2)^2 = 8. This equals 2k = 2 x 4 = 8,
    and also equals the vertex count of the stellated octahedron. Completing the
    L shell     'fills' all 8 vertex positions.
    
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: Does vertex filling order predict chemical properties (electronegativity)? "
        "(Answering would improve Model Output by +3 points: testable chemical predictions) "
        "Q2: Why is neon so stable when all 8 vertices are filled? "
        "(Answering would improve Question by +2 points: connects to octet rule) "
        "Q3: How do the 8 L shell electrons map to specific stellated octahedron vertices? "
        "(Answering would improve Derivation by +2 points: concrete vertex assignment)"
    )
    """
    name = "L Shell = 2k (Observation)"
    question = "Why does the L shell hold exactly 8 electrons?"
    reference = "Neon: 8 electrons fill the L shell (total 10 with K shell)"
    level = Level.EXPLORATORY
    
    def derivation(self):
        return (
            Derivation()
            .step("OBSERVATION: L shell capacity = 8 (from 2n^2 with n=2).")
            .step("FIELD CLOSURE: k = 4; stellated octahedron has 2k = 8 vertices.")
            .step("PATTERN: L shell = 8 = 2k = vertex count.")
            .step("INTERPRETATION: Completing L shell fills all vertex positions.")
            .step("NOBLE GAS: Ne with 10 electrons (2 + 8) is extremely stable.")
            .conclude("RESULT: L shell = 8 = 2k = vertices (geometric correspondence).")
        )
    
    commentary = (
        "The L shell's capacity of 8 matches the stellated octahedron's vertex count "
        "exactly. If each L shell electron corresponds to one vertex position, then "
        "noble gas stability (filled shells) reflects geometric completion: all 8 "
        "vertices occupied. This is speculation, but the numerical match is exact."
    )
    
    def model(self):
        return Model().add("L shell", 2 * K)
    
    def observations(self):
        return Observed().add("L shell", 8)


class NobleGasSequencePattern(Test):
    """
    Noble gas differences: 8, 8, 18, 18, 32.
    
    The pattern shows each capacity appearing twice (Aufbau filling order).
    This is standard chemistry, not GFM content.
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
            .conclude("OUTPUT: Differences 8, 8, 18, 18, 32 (from Aufbau, not GFM).")
        )
    
    commentary = (
        "The noble gas sequence reflects orbital filling order (Aufbau principle). "
        "Each shell capacity appears twice because of how s, p, d, f subshells fill "
        "across periods. This is standard chemistry. GFM can note that 8 = 2k, but "
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
    GFMShellReframing,
    
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
            "These tests examine electron shell capacities through GFM geometry.\n\n"
            "IMPORTANT: Shell capacities (2, 8, 18, 32) are DERIVED by quantum mechanics "
            "from the Schrodinger equation and Pauli exclusion. GFM does NOT derive these "
            "values; it provides an alternative GEOMETRIC PICTURE that produces the same "
            "numbers.\n\n"
            "The spin factor of 2 is associated with TIME faces (one per tetrahedron). "
            "The n^2 orbital factor lacks clear geometric origin in GFM.\n\n"
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
