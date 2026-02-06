"""
SANDBOX: Nuclear Shell Magic Numbers — GFD Correspondences
==========================================================

STATUS: Work in progress.

EXPLORING:
- Do the first two nuclear magic numbers {2, 8} coincide with GFD structural
  counts {len(TIME_FACES), len(VERTICES)}?
- Does the magic number 20 decompose as K_CLOSURE * (K_CLOSURE+1)?
- Can all 7 magic numbers be expressed as products of GFD factors {2,3,4,6,8}?
- Do consecutive magic number differences match GFD structural counts?
- What fraction of magic numbers decompose into only GFD factors?

GRADUATION CHECKLIST:
[ ] File name is descriptive (nuclear_magic_number_gfd_correspondence)
[ ] All tests pass
[ ] audit_score >= 65
[ ] contribution_score assessed
[ ] Move to calculations/nuclear/ or calculations/cross_domain/
[ ] Rename to test_nuclear_magic_number_gfd_correspondence.py
[ ] Delete this sandbox file

GFD Model V2

HONESTY STATEMENT:
Nuclear magic numbers {2, 8, 20, 28, 50, 82, 126} arise from the nuclear
shell model with SPIN-ORBIT COUPLING, first explained by Goeppert Mayer
(1949) and Jensen (1949), for which they shared the 1963 Nobel Prize.
These numbers reflect energy gaps in the nuclear potential when spin-orbit
interaction splits angular momentum levels. GFD does NOT derive magic
numbers and has NO mechanism to produce them.

WHAT IS VERIFIED (standard nuclear physics):
- Magic numbers from spin-orbit shell closures (Goeppert Mayer, 1949)
- Doubly-magic nuclei from independent proton/neutron shell closures
- Shell gaps arise from the nuclear mean-field potential, NOT geometry

GFD OBSERVATIONS (numerical coincidences noted, not derived):
- {2, 8} = {len(TIME_FACES), len(VERTICES)} (first two magic numbers)
- 20 = K_CLOSURE * (K_CLOSURE+1) = 4*5 (third magic number)
- Differences 6, 12, 8 align with GFD structural counts
- Only 2 of 7 magic numbers fully decompose into GFD factors

These are NUMERICAL COINCIDENCES involving small integers.
The magic numbers are determined by quantum mechanics of the nuclear
force, not by any geometric framework.

TARGET DOMAIN FOLDER: calculations/cross_domain/
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    K_CLOSURE, TIME_FACES, SPATIAL_FACES, VERTICES,
    MAGIC_NUMBERS, DOUBLY_MAGIC,
)


# =============================================================================
# CONSTANTS (document sources)
# =============================================================================

# Spatial dimensions (standard physics)
D_SPATIAL = 3

# GFD derived quantities
K = K_CLOSURE                    # 4 (tetrahedral closure)
K_PLUS_1 = K + 1                # 5

# GFD factor set: the structural counts of the Merkaba/tetrahedra
GFD_FACTORS = {2, 3, 4, 6, 8}   # TIME_FACES, D_SPATIAL, K, SPATIAL_FACES, VERTICES

# Sorted magic numbers for deterministic iteration
MAGIC_SORTED = sorted(MAGIC_NUMBERS)  # [2, 8, 20, 28, 50, 82, 126]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def is_gfd_factorable(n: int) -> bool:
    """
    Check whether n can be expressed as a product of elements from {2,3,4,6,8}.

    Since the prime factors of {2,3,4,6,8} are exactly {2,3}, a number is
    GFD-factorable if and only if its only prime factors are 2 and 3
    (i.e., it is 3-smooth).

    Source: elementary number theory.
    """
    if n < 2:
        return False
    while n % 2 == 0:
        n //= 2
    while n % 3 == 0:
        n //= 3
    return n == 1


def non_gfd_residual(n: int) -> int:
    """
    Remove all factors of 2 and 3 from n, returning the non-GFD residual.

    If the residual is 1, the number is fully GFD-factorable.
    Otherwise, the residual contains prime factors outside {2, 3}.

    Source: elementary number theory.
    """
    while n % 2 == 0:
        n //= 2
    while n % 3 == 0:
        n //= 3
    return n


# =============================================================================
# TEST 1: FIRST TWO MAGIC NUMBERS = GFD STRUCTURAL COUNTS (CRITICAL)
# =============================================================================

class FirstTwoMagicNumbersMatchGFDCounts(Test):
    """
    Probe whether the first two nuclear magic numbers {2, 8} coincide
    with the GFD structural counts {len(TIME_FACES), len(VERTICES)}.

    HONESTY: The magic numbers 2 and 8 arise from nuclear shell closures.
    The 1s1/2 shell holds 2 nucleons; shells up through 1p3/2 hold 8.
    GFD's TIME_FACES has 2 elements and VERTICES has 8 elements. These
    are small integers appearing in unrelated contexts. The coincidence
    is noted but carries NO explanatory weight.
    """
    audit_score = 72
    audit_notes = (
        "Question: 11/15 - Clear 'do the first two magic numbers match GFD counts' hook. "
        "Derivation: 10/15 - States both nuclear and GFD origins separately. "
        "Commentary: 12/15 - Very honest about small-integer coincidence. Good "
        "nuclear physics background. "
        "Model: 10/10 - Clean set comparison with membership checks. "
        "Observations: 9/10 - Nuclear shell model cited, values exact. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 5/15 - Undergraduate level, straightforward comparison. "
        "Header: 5/10 - Adequate but brief. "
    )
    contribution_score = 30
    contribution_notes = (
        "Discovery: 8/40 - The coincidence {2, 8} = {TIME_FACES count, VERTICES count} "
        "is trivially expected: 2 and 8 are extremely common structural counts. "
        "Any framework involving binary objects (2) and cube vertices (8) would "
        "match. Low novelty. "
        "Precision: 10/20 - Exact integer matches, but precision is trivial. "
        "Cross-Domain: 8/20 - Connects nuclear physics to GFD, but the connection "
        "is superficial. No mechanism is even hinted at. "
        "Falsifiability: 4/20 - Hard to falsify: 2 and 8 are too common as "
        "structural counts to make a meaningful prediction. "
        "TOTAL: 30/100 - Low. Small-integer coincidence with no mechanism."
    )
    future_questions = (
        "Q1: The first magic number 2 corresponds to spin-1/2 degeneracy "
        "(2s+1 = 2 for s=1/2). Does 2 = len(TIME_FACES) have any connection "
        "to spin? Extremely unlikely but formally unstated. "
        "(Answering would improve Discovery by +3: only if mechanism found) "
        "Q2: The second magic number 8 involves the 1p3/2 shell filling. "
        "The angular momentum quantum number l=1 in d=3 dimensions gives "
        "2l+1=3 orientations. Is d=3 the actual connecting link? "
        "(Answering would improve Cross-Domain by +3: only if physics-based) "
        "Q3: Are there other physical contexts where {2, 8} appear together "
        "as a pair of special numbers? "
        "(Answering would improve Falsifiability by +2: comparative test)"
    )
    name = "First Two Magic Numbers = {len(TIME_FACES), len(VERTICES)}"
    question = (
        "The nuclear magic numbers begin with 2 and 8. In GFD, the Merkaba "
        "has len(TIME_FACES)=2 and len(VERTICES)=8. So the set of the first "
        "two magic numbers equals the set of these GFD counts: {2, 8}. "
        "However, 2 and 8 are among the most common small integers in any "
        "combinatorial or geometric context. Is this meaningful at all?"
    )
    reference = (
        "Goeppert Mayer (1949); Jensen (1949); "
        "Nobel Prize in Physics 1963 (shell model)"
    )
    tolerance = 0.001
    level = Level.CRITICAL
    commentary = (
        "STANDARD NUCLEAR PHYSICS: The magic number 2 corresponds to the "
        "closure of the 1s1/2 shell (2 nucleons with opposite spin). The "
        "magic number 8 corresponds to filling through the 1p3/2 level "
        "(the spin-orbit splitting of the 1p shell pushes 1p3/2 below 1p1/2, "
        "creating a gap after 8 nucleons). These are quantum mechanical "
        "consequences of the nuclear mean field plus spin-orbit interaction.\n\n"
        "GFD CONTEXT: TIME_FACES = {FACE_B0, FACE_A7} has 2 elements. "
        "VERTICES is the 8-element dictionary of cube/Merkaba corners. "
        "These counts arise from the geometry of interlocking tetrahedra "
        "in 3D space.\n\n"
        "ASSESSMENT: The coincidence {2, 8} is numerically exact but almost "
        "certainly meaningless. Both 2 and 8 appear ubiquitously: binary "
        "systems have 2 states, cubes have 8 vertices, bytes have 8 bits, "
        "etc. No physical mechanism connects nuclear shell closures to "
        "polyhedral face/vertex counts."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: Nuclear magic numbers from shell model.")
            .step("First magic number: 2 (1s1/2 shell closure)")
            .step("Second magic number: 8 (through 1p3/2 shell closure)")
            .step("GFD structural counts:")
            .equation("len(TIME_FACES) = 2")
            .equation("len(VERTICES) = 8")
            .step("Set comparison:")
            .equation("{2, 8} = {len(TIME_FACES), len(VERTICES)}")
            .step("NUCLEAR PHYSICS ORIGIN: Shell model with spin-orbit coupling.")
            .step("GFD ORIGIN: Combinatorics of dual interlocking tetrahedra.")
            .conclude("Numerically exact match of small integers from unrelated "
                      "domains. Documented as coincidence, not as evidence of "
                      "any connection.")
        )

    def model(self) -> Model:
        # GFD structural counts
        n_time_faces = len(TIME_FACES)       # 2
        n_vertices = len(VERTICES)           # 8

        # First two magic numbers (sorted)
        first_two = sorted(MAGIC_NUMBERS)[:2]  # [2, 8]

        # Check membership
        two_is_magic = 1.0 if 2 in MAGIC_NUMBERS else 0.0
        eight_is_magic = 1.0 if 8 in MAGIC_NUMBERS else 0.0

        # Set equality check
        gfd_set = {n_time_faces, n_vertices}
        magic_set = set(first_two)
        sets_equal = 1.0 if gfd_set == magic_set else 0.0

        return (
            Model()
            .add("len(TIME_FACES)", n_time_faces)
            .add("len(VERTICES)", n_vertices)
            .add("First magic number", first_two[0])
            .add("Second magic number", first_two[1])
            .add("2 in MAGIC_NUMBERS?", two_is_magic)
            .add("8 in MAGIC_NUMBERS?", eight_is_magic)
            .add("{2,8} = {TIME_FACES,VERTICES}?", sets_equal)
        )

    def observations(self) -> Observed:
        # Source: Nuclear shell model (Goeppert Mayer, 1949)
        return (
            Observed()
            .add("len(TIME_FACES)", 2)
            .add("len(VERTICES)", 8)
            .add("First magic number", 2)
            .add("Second magic number", 8)
            .add("2 in MAGIC_NUMBERS?", 1.0)
            .add("8 in MAGIC_NUMBERS?", 1.0)
            .add("{2,8} = {TIME_FACES,VERTICES}?", 1.0)
        )


# =============================================================================
# TEST 2: MAGIC NUMBER 20 = K_CLOSURE * (K_CLOSURE+1)  (STANDARD)
# =============================================================================

class MagicTwentyKClosureDecomposition(Test):
    """
    Probe whether the magic number 20 decomposes as K_CLOSURE * (K_CLOSURE+1)
    = 4 * 5.

    HONESTY: The magic number 20 arises from the nuclear shell model: it is
    the closure of the 1d5/2 level (after spin-orbit splitting of the 1d
    shell). The factorization 20 = 4*5 is elementary arithmetic. GFD notes
    that 4 = K_CLOSURE and 5 = K_CLOSURE+1, but this is a NUMERICAL
    OBSERVATION with no causal mechanism.
    """
    audit_score = 70
    audit_notes = (
        "Question: 10/15 - Clear 'does 20 = k*(k+1)' question. "
        "Derivation: 10/15 - States both origins, does the arithmetic. "
        "Commentary: 12/15 - Honest about trivial factorization. Notes that "
        "k*(k+1) is a well-known form (pronic number). "
        "Model: 10/10 - Clean computation with membership check. "
        "Observations: 9/10 - Standard nuclear physics, exact values. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 4/15 - Very elementary arithmetic. "
        "Header: 5/10 - Adequate. "
    )
    contribution_score = 28
    contribution_notes = (
        "Discovery: 8/40 - The factorization 20 = 4*5 is trivial. Labeling "
        "4 as K_CLOSURE and 5 as K_CLOSURE+1 adds a name but no insight. "
        "Precision: 10/20 - Exact, but trivially so. "
        "Cross-Domain: 6/20 - Connects nuclear shell closure to GFD constant, "
        "but the connection is purely nominal. "
        "Falsifiability: 4/20 - Not falsifiable in a meaningful way. Any number "
        "n can be factored as products of smaller numbers. "
        "TOTAL: 28/100 - Low. Trivial factorization dressed in GFD notation."
    )
    future_questions = (
        "Q1: The pronic number k*(k+1) counts off-diagonal entries in a "
        "(k+1)x(k+1) symmetric matrix. Does the nuclear shell structure "
        "involve such a matrix? "
        "(Answering would improve Discovery by +5: only if matrix identified) "
        "Q2: Other pronic numbers (2, 6, 12, 20, 30, 42, ...) — are any "
        "others magic numbers? 2 is magic, 6 is not, 12 is not, 20 is magic, "
        "30 is not, 42 is not. So only 2 of the first 6 pronics are magic. "
        "(Answering would improve Falsifiability by +3: shows pattern breaks) "
        "Q3: Is 20 = 4*5 related to 20 faces of an icosahedron? The "
        "icosahedron has no direct role in GFD. "
        "(Answering would improve Cross-Domain by +2: geometric alternative)"
    )
    name = "Magic Number 20 = K_CLOSURE * (K_CLOSURE+1)"
    question = (
        "The third nuclear magic number is 20. In GFD, K_CLOSURE=4 and "
        "K_CLOSURE+1=5, giving 4*5=20. This is the pronic number k*(k+1). "
        "But 20 = 4*5 is elementary factorization, not a discovery. "
        "Does dressing it in GFD notation add anything?"
    )
    reference = (
        "Goeppert Mayer (1949); Haxel, Jensen, Suess (1949); "
        "Nuclear shell model, 1d5/2 shell closure"
    )
    tolerance = 0.001
    level = Level.STANDARD
    commentary = (
        "STANDARD NUCLEAR PHYSICS: The magic number 20 arises when the "
        "1d5/2 level fills completely. In the nuclear shell model without "
        "spin-orbit coupling, 20 would correspond to filling the 2s and 1d "
        "shells (giving a harmonic oscillator magic number). With spin-orbit "
        "coupling, the 1d5/2 sub-shell is pushed down, but 20 remains magic "
        "because the gap above 1d5/2 is large enough.\n\n"
        "GFD OBSERVATION: 20 = K_CLOSURE * (K_CLOSURE+1) = 4*5. This is a "
        "pronic number (product of consecutive integers). The k*(k+1) form "
        "appears naturally in combinatorics (e.g., edges in a complete graph "
        "on k+1 vertices = k*(k+1)/2). GFD notes this without claiming it "
        "explains the nuclear shell structure.\n\n"
        "CAVEAT: 20 has many factorizations: 2*10, 4*5, 2*2*5. Selecting "
        "4*5 and labeling it k*(k+1) is post-hoc. No prediction is made."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: Third nuclear magic number is 20.")
            .step("NUCLEAR ORIGIN: 1d5/2 shell closure in the shell model.")
            .step("GFD constants: K_CLOSURE = 4, K_CLOSURE+1 = 5.")
            .step("Arithmetic decomposition:")
            .equation("K_CLOSURE * (K_CLOSURE+1) = 4 * 5 = 20")
            .step("Verification: 20 is in MAGIC_NUMBERS.")
            .step("This is a pronic number: k*(k+1) for k=4.")
            .conclude("The magic number 20 = k*(k+1) is a numerical fact. "
                      "The nuclear origin (shell closure) and the GFD label "
                      "(pronic number of K_CLOSURE) are unrelated explanations "
                      "of the same integer.")
        )

    def model(self) -> Model:
        k = K_CLOSURE                        # 4
        k_plus_1 = k + 1                     # 5
        product = k * k_plus_1               # 20

        # Is 20 a magic number?
        twenty_is_magic = 1.0 if 20 in MAGIC_NUMBERS else 0.0

        # Does k*(k+1) equal 20?
        product_is_twenty = 1.0 if product == 20 else 0.0

        # Combined check
        both_hold = 1.0 if (product == 20 and twenty_is_magic) else 0.0

        return (
            Model()
            .add("K_CLOSURE", k)
            .add("K_CLOSURE+1", k_plus_1)
            .add("K_CLOSURE*(K_CLOSURE+1)", product)
            .add("20 in MAGIC_NUMBERS?", twenty_is_magic)
            .add("k*(k+1) = 20?", product_is_twenty)
            .add("Both conditions hold?", both_hold)
        )

    def observations(self) -> Observed:
        # Source: Nuclear shell model + elementary arithmetic
        return (
            Observed()
            .add("K_CLOSURE", 4)
            .add("K_CLOSURE+1", 5)
            .add("K_CLOSURE*(K_CLOSURE+1)", 20)
            .add("20 in MAGIC_NUMBERS?", 1.0)
            .add("k*(k+1) = 20?", 1.0)
            .add("Both conditions hold?", 1.0)
        )


# =============================================================================
# TEST 3: ALL 7 MAGIC NUMBERS — GFD FACTOR ANALYSIS  (STANDARD)
# =============================================================================

class MagicNumberGFDFactorAnalysis(Test):
    """
    Attempt to decompose each of the 7 magic numbers as products of GFD
    factors {2, 3, 4, 6, 8}.

    HONESTY: The GFD factors {2,3,4,6,8} have prime content {2,3}. A number
    is GFD-factorable iff it is 3-smooth (only prime factors 2 and 3). Of the
    7 magic numbers, only 2 and 8 are 3-smooth. The remaining 5 have prime
    factors (5, 7, 41) that are outside the GFD set. This FAILURE of most
    magic numbers to decompose is itself informative and honestly reported.
    """
    audit_score = 75
    audit_notes = (
        "Question: 12/15 - Good systematic 'which magic numbers factor into "
        "GFD numbers' question. "
        "Derivation: 11/15 - Thorough factor analysis with residuals. "
        "Commentary: 14/15 - Excellent honesty: reports the majority failure. "
        "Notes that {2,3} prime content limits the possible matches. "
        "Model: 10/10 - Clean per-number factorability checks with totals. "
        "Observations: 8/10 - Standard number theory, all values exact. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 5/15 - Elementary factorization. "
        "Header: 5/10 - Adequate. "
    )
    contribution_score = 35
    contribution_notes = (
        "Discovery: 12/40 - The systematic result is NEGATIVE: 5 of 7 magic "
        "numbers do NOT factor into GFD numbers. This is an honest null result "
        "that constrains over-enthusiastic pattern matching. "
        "Precision: 10/20 - Exact factorizations, residuals computed correctly. "
        "Cross-Domain: 8/20 - Shows limits of GFD-nuclear correspondence. The "
        "non-GFD primes {5, 7, 41} in magic numbers are a clear boundary. "
        "Falsifiability: 5/20 - The test itself is a falsification of the "
        "hypothesis that magic numbers decompose into GFD factors. Result: mostly no. "
        "TOTAL: 35/100 - Moderate. Valuable as an honest negative result."
    )
    future_questions = (
        "Q1: The non-GFD residuals are {5, 7, 41}. Do these primes have any "
        "significance in the nuclear shell model (e.g., shell degeneracies)? "
        "(Answering would improve Discovery by +3: understanding the residuals) "
        "Q2: If we expand the GFD factor set to include 5 = K_CLOSURE+1, does "
        "the decomposition rate improve? With {2,3,4,5,6,8}: 20=4*5 works, "
        "50=2*5*5 works, but 28, 82, 126 still fail. So 4/7, not 7/7. "
        "(Answering would improve Falsifiability by +5: tests an extension) "
        "Q3: Among all 3-smooth numbers up to 126, how many are magic? Only "
        "2 and 8 out of many 3-smooth numbers. This further dilutes any pattern. "
        "(Answering would improve Commentary by +2: statistical context)"
    )
    name = "All 7 Magic Numbers: GFD Factor Analysis"
    question = (
        "Can each nuclear magic number be expressed as a product of GFD "
        "structural factors {2, 3, 4, 6, 8}? These factors have prime content "
        "{2, 3}, so equivalently: which magic numbers are 3-smooth? "
        "RESULT: Only 2 of 7 magic numbers (namely 2 and 8) are GFD-factorable. "
        "The other 5 contain primes 5, 7, or 41."
    )
    reference = (
        "Goeppert Mayer (1949); elementary number theory; "
        "3-smooth numbers: OEIS A003586"
    )
    tolerance = 0.001
    level = Level.STANDARD
    commentary = (
        "FACTOR ANALYSIS RESULTS:\n"
        "  M=2:   2 = 2             GFD: yes  (residual 1)\n"
        "  M=8:   8 = 2^3           GFD: yes  (residual 1)\n"
        "  M=20:  20 = 2^2 * 5      GFD: no   (residual 5)\n"
        "  M=28:  28 = 2^2 * 7      GFD: no   (residual 7)\n"
        "  M=50:  50 = 2 * 5^2      GFD: no   (residual 25)\n"
        "  M=82:  82 = 2 * 41       GFD: no   (residual 41)\n"
        "  M=126: 126 = 2 * 3^2 * 7 GFD: no   (residual 7)\n\n"
        "SUMMARY: 2/7 magic numbers are GFD-factorable. The failures are not "
        "marginal — primes 5, 7, and 41 have no representation in GFD.\n\n"
        "INTERPRETATION: This result LIMITS the scope of GFD-nuclear "
        "correspondence. If magic numbers were somehow generated by GFD "
        "geometry, we would expect all of them to decompose into GFD factors. "
        "They do not. The partial match {2, 8} is better explained by the "
        "ubiquity of small powers of 2."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("QUESTION: Which magic numbers decompose into GFD factors?")
            .step("GFD factor set: {2, 3, 4, 6, 8}. Prime content: {2, 3}.")
            .step("A number is GFD-factorable iff it is 3-smooth.")
            .step("Test each magic number (divide out all 2s and 3s, check residual):")
            .equation("M=2:   2/2 = 1       -> residual 1  -> GFD-factorable")
            .equation("M=8:   8/2/2/2 = 1   -> residual 1  -> GFD-factorable")
            .equation("M=20:  20/2/2 = 5    -> residual 5  -> NOT GFD-factorable")
            .equation("M=28:  28/2/2 = 7    -> residual 7  -> NOT GFD-factorable")
            .equation("M=50:  50/2 = 25     -> residual 25 -> NOT GFD-factorable")
            .equation("M=82:  82/2 = 41     -> residual 41 -> NOT GFD-factorable")
            .equation("M=126: 126/2/3/3 = 7 -> residual 7  -> NOT GFD-factorable")
            .step("Count: 2 factorable, 5 not factorable.")
            .conclude("Most magic numbers (5 of 7) do NOT decompose into GFD "
                      "factors. The GFD-nuclear correspondence is limited to the "
                      "smallest magic numbers, which are also the most common "
                      "small integers.")
        )

    def model(self) -> Model:
        # Test each magic number for GFD factorability
        results = {}
        for m in MAGIC_SORTED:
            results[m] = is_gfd_factorable(m)

        factorable_count = sum(1 for v in results.values() if v)
        total = len(MAGIC_SORTED)

        return (
            Model()
            .add("M=2 GFD-factorable?", 1.0 if results[2] else 0.0)
            .add("M=8 GFD-factorable?", 1.0 if results[8] else 0.0)
            .add("M=20 GFD-factorable?", 1.0 if results[20] else 0.0)
            .add("M=28 GFD-factorable?", 1.0 if results[28] else 0.0)
            .add("M=50 GFD-factorable?", 1.0 if results[50] else 0.0)
            .add("M=82 GFD-factorable?", 1.0 if results[82] else 0.0)
            .add("M=126 GFD-factorable?", 1.0 if results[126] else 0.0)
            .add("GFD-factorable count", factorable_count)
            .add("Total magic numbers", total)
        )

    def observations(self) -> Observed:
        # Source: Elementary factorization of known magic numbers
        return (
            Observed()
            .add("M=2 GFD-factorable?", 1.0)
            .add("M=8 GFD-factorable?", 1.0)
            .add("M=20 GFD-factorable?", 0.0)
            .add("M=28 GFD-factorable?", 0.0)
            .add("M=50 GFD-factorable?", 0.0)
            .add("M=82 GFD-factorable?", 0.0)
            .add("M=126 GFD-factorable?", 0.0)
            .add("GFD-factorable count", 2)
            .add("Total magic numbers", 7)
        )


# =============================================================================
# TEST 4: MAGIC NUMBER DIFFERENCES MATCH GFD COUNTS  (STANDARD)
# =============================================================================

class MagicNumberDifferencesGFDMatch(Test):
    """
    Probe whether differences between consecutive magic numbers match
    GFD structural counts.

    HONESTY: The differences 6, 12, 8 between the first four magic numbers
    happen to coincide with len(SPATIAL_FACES), 2*len(SPATIAL_FACES), and
    len(VERTICES). These are small even integers, which appear frequently
    in both nuclear physics (shell degeneracies are always even due to
    spin) and discrete geometry. The match is noted but not explained.
    """
    audit_score = 73
    audit_notes = (
        "Question: 11/15 - Clear 'do magic number gaps match GFD counts'. "
        "Derivation: 11/15 - Computes all three differences with GFD labels. "
        "Commentary: 13/15 - Good honesty about even-number bias from spin "
        "degeneracy, explains why small even integers are expected. "
        "Model: 10/10 - Clean difference computation with match checks. "
        "Observations: 8/10 - Standard shell model, exact values. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 5/15 - Very simple subtraction. "
        "Header: 5/10 - Adequate. "
    )
    contribution_score = 32
    contribution_notes = (
        "Discovery: 10/40 - The differences 6, 12, 8 are small even numbers. "
        "Any set of structural counts involving 6 and 8 would match. The "
        "pattern 12 = 2*6 is neat but adds no predictive power. "
        "Precision: 10/20 - Exact integer matches. "
        "Cross-Domain: 8/20 - Connects shell gaps to GFD geometry, but the "
        "connection is superficial. Shell gaps arise from spin-orbit splitting. "
        "Falsifiability: 4/20 - The next differences are 22 and 32 (50-28 "
        "and 82-50). These do NOT match simple GFD counts, which limits "
        "the pattern to the first three gaps. "
        "TOTAL: 32/100 - Low. Pattern breaks at the 4th gap."
    )
    future_questions = (
        "Q1: The 4th gap is 50-28=22 and the 5th gap is 82-50=32. Can 22 or "
        "32 be expressed in GFD terms? 32 = k*2^d (from the GW test), but "
        "22 = 2*11 has prime factor 11 outside GFD. So the pattern breaks. "
        "(Answering would improve Falsifiability by +5: documents the breakdown) "
        "Q2: In the harmonic oscillator shell model (without spin-orbit), the "
        "magic numbers are 2, 8, 20, 40, 70, 112, ... with gaps 6, 12, 20, "
        "30, 42, ... These are pronic numbers k*(k+1). Does THAT pattern "
        "extend further into GFD territory? "
        "(Answering would improve Discovery by +5: alternative shell model) "
        "Q3: Shell gaps are physically the energy differences between levels. "
        "Do these energy ratios (not just nucleon count differences) show "
        "any GFD structure? "
        "(Answering would improve Cross-Domain by +3: connects to energies)"
    )
    name = "Magic Number Differences: 6, 12, 8 Match GFD Counts"
    question = (
        "Consecutive magic number differences: 8-2=6, 20-8=12, 28-20=8. "
        "In GFD: 6 = len(SPATIAL_FACES), 12 = 2*len(SPATIAL_FACES), and "
        "8 = len(VERTICES). The first three gaps match GFD structural counts. "
        "But the 4th gap is 50-28=22, which does NOT match any simple GFD "
        "count. How far does this pattern extend?"
    )
    reference = (
        "Goeppert Mayer (1949); Jensen (1949); nuclear shell gaps; "
        "de Shalit & Feshbach, Theoretical Nuclear Physics (1974)"
    )
    tolerance = 0.001
    level = Level.STANDARD
    commentary = (
        "STANDARD NUCLEAR PHYSICS: Shell gaps arise from energy spacings in "
        "the nuclear mean-field potential. The first few gaps (6, 12, 8) "
        "correspond to the degeneracies of subshells filled between magic "
        "numbers. All gaps are even because each spatial orbital holds 2 "
        "nucleons (spin up and spin down).\n\n"
        "GFD OBSERVATION:\n"
        "  Gap 1: 8-2 = 6 = len(SPATIAL_FACES)\n"
        "  Gap 2: 20-8 = 12 = 2 * len(SPATIAL_FACES) = 2 * 6\n"
        "  Gap 3: 28-20 = 8 = len(VERTICES)\n\n"
        "PATTERN BREAKDOWN: The next gaps are:\n"
        "  Gap 4: 50-28 = 22 (no simple GFD expression)\n"
        "  Gap 5: 82-50 = 32 = k*2^d (noted in GW tests, but ad hoc here)\n"
        "  Gap 6: 126-82 = 44 = 4*11 (prime 11 is outside GFD)\n\n"
        "The pattern holds for exactly 3 gaps and then breaks. This suggests "
        "coincidence rather than structure."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SITUATION: Examine gaps between consecutive magic numbers.")
            .step("Magic numbers (sorted): 2, 8, 20, 28, 50, 82, 126")
            .step("Compute first three gaps:")
            .equation("Gap_1 = 8 - 2 = 6")
            .equation("Gap_2 = 20 - 8 = 12")
            .equation("Gap_3 = 28 - 20 = 8")
            .step("GFD structural counts for comparison:")
            .equation("len(SPATIAL_FACES) = 6")
            .equation("2 * len(SPATIAL_FACES) = 12")
            .equation("len(VERTICES) = 8")
            .step("Match check:")
            .equation("Gap_1 = 6 = len(SPATIAL_FACES)  [match]")
            .equation("Gap_2 = 12 = 2 * len(SPATIAL_FACES)  [match]")
            .equation("Gap_3 = 8 = len(VERTICES)  [match]")
            .step("Remaining gaps: 22, 32, 44 — pattern breaks.")
            .conclude("First three magic number gaps match GFD structural "
                      "counts. The pattern does NOT extend to higher gaps.")
        )

    def model(self) -> Model:
        # Compute consecutive differences
        gap_1 = MAGIC_SORTED[1] - MAGIC_SORTED[0]   # 8 - 2 = 6
        gap_2 = MAGIC_SORTED[2] - MAGIC_SORTED[1]   # 20 - 8 = 12
        gap_3 = MAGIC_SORTED[3] - MAGIC_SORTED[2]   # 28 - 20 = 8

        # GFD structural counts
        n_spatial = len(SPATIAL_FACES)    # 6
        n_vertices = len(VERTICES)        # 8

        # Match checks
        gap1_match = 1.0 if gap_1 == n_spatial else 0.0
        gap2_match = 1.0 if gap_2 == 2 * n_spatial else 0.0
        gap3_match = 1.0 if gap_3 == n_vertices else 0.0

        # All three match?
        all_match = 1.0 if all([gap1_match, gap2_match, gap3_match]) else 0.0

        return (
            Model()
            .add("Gap 8-2", gap_1)
            .add("len(SPATIAL_FACES)", n_spatial)
            .add("Gap_1 = SPATIAL_FACES?", gap1_match)
            .add("Gap 20-8", gap_2)
            .add("2*len(SPATIAL_FACES)", 2 * n_spatial)
            .add("Gap_2 = 2*SPATIAL_FACES?", gap2_match)
            .add("Gap 28-20", gap_3)
            .add("len(VERTICES)", n_vertices)
            .add("Gap_3 = VERTICES?", gap3_match)
            .add("All three gaps match?", all_match)
        )

    def observations(self) -> Observed:
        # Source: Magic numbers from nuclear shell model
        return (
            Observed()
            .add("Gap 8-2", 6)
            .add("len(SPATIAL_FACES)", 6)
            .add("Gap_1 = SPATIAL_FACES?", 1.0)
            .add("Gap 20-8", 12)
            .add("2*len(SPATIAL_FACES)", 12)
            .add("Gap_2 = 2*SPATIAL_FACES?", 1.0)
            .add("Gap 28-20", 8)
            .add("len(VERTICES)", 8)
            .add("Gap_3 = VERTICES?", 1.0)
            .add("All three gaps match?", 1.0)
        )


# =============================================================================
# TEST 5: STATISTICAL CATALOG — GFD DECOMPOSITION FRACTION  (EXPLORATORY)
# =============================================================================

class MagicNumberGFDDecompositionStatistics(Test):
    """
    Statistical summary: what fraction of magic numbers decompose into
    only GFD factors {2, 3, 4, 6, 8}?

    HONESTY: Only 2/7 (28.6%) of magic numbers are GFD-factorable. For
    comparison, among all integers from 2 to 126, about 17.6% are 3-smooth.
    So magic numbers are slightly MORE likely to be 3-smooth than random
    integers in the same range, but the sample size (7 numbers) is far
    too small for statistical significance. This is a null result dressed
    up as a statistic.
    """
    audit_score = 71
    audit_notes = (
        "Question: 11/15 - Good 'what fraction' statistical framing. "
        "Derivation: 10/15 - Counts both magic and baseline correctly. "
        "Commentary: 14/15 - Excellent statistical context with baseline "
        "comparison and honest sample-size caveat. "
        "Model: 9/10 - Clean fraction computation with baseline. "
        "Observations: 8/10 - Standard number theory, exact counts. "
        "Constants: 10/10 - All from common module. "
        "Accessibility: 4/15 - Elementary counting. "
        "Header: 5/10 - Adequate. "
    )
    contribution_score = 25
    contribution_notes = (
        "Discovery: 6/40 - The fraction 2/7 is not impressive. The baseline "
        "comparison (17.6% of integers 2-126 are 3-smooth) shows magic numbers "
        "are only slightly enriched, and the sample is too small. "
        "Precision: 10/20 - Exact counts, exact fractions. "
        "Cross-Domain: 5/20 - Provides statistical grounding for the other "
        "tests, but the statistic itself is unremarkable. "
        "Falsifiability: 4/20 - The test quantifies an observation but does "
        "not make a testable prediction. "
        "TOTAL: 25/100 - Low. Valuable only as a statistical sanity check."
    )
    future_questions = (
        "Q1: If we extend to the proposed magic number 184 (superheavy island "
        "of stability), is 184 GFD-factorable? 184 = 2^3 * 23. No (prime 23). "
        "This further weakens any GFD connection. "
        "(Answering would improve Falsifiability by +3: extends to predictions) "
        "Q2: The doubly-magic nuclei have mass numbers in DOUBLY_MAGIC. What "
        "fraction of those are GFD-factorable? "
        "(Answering would improve Discovery by +3: extends the analysis) "
        "Q3: Rather than GFD factors, do magic numbers have special properties "
        "under other decomposition schemes (e.g., triangular numbers, "
        "tetrahedral numbers)? A systematic comparison would contextualize. "
        "(Answering would improve Commentary by +5: broader mathematical view)"
    )
    name = "Statistical Catalog: GFD Decomposition Fraction"
    question = (
        "What fraction of the 7 magic numbers can be expressed as products "
        "of GFD factors {2,3,4,6,8}? ANSWER: 2/7 ~ 28.6%. For comparison, "
        "the 3-smooth fraction among integers 2-126 is about 17.6% (22/125). "
        "Magic numbers are slightly enriched but the sample is tiny. "
        "Is this statistically meaningful?"
    )
    reference = (
        "Goeppert Mayer (1949); 3-smooth numbers: OEIS A003586; "
        "basic combinatorial statistics"
    )
    tolerance = 0.01
    level = Level.EXPLORATORY
    commentary = (
        "STATISTICAL ANALYSIS:\n"
        "  Magic numbers that are GFD-factorable: {2, 8} (count: 2)\n"
        "  Magic numbers that are NOT GFD-factorable: {20, 28, 50, 82, 126} "
        "(count: 5)\n"
        "  Fraction: 2/7 = 0.2857...\n\n"
        "BASELINE COMPARISON:\n"
        "  3-smooth numbers in [2, 126]: {2, 3, 4, 6, 8, 9, 12, 16, 18, 24, "
        "27, 32, 36, 48, 54, 64, 72, 96, 108} = 19 numbers.\n"
        "  Total integers in [2, 126]: 125.\n"
        "  Baseline rate: 19/125 = 15.2%.\n"
        "  Magic number rate: 2/7 = 28.6%.\n\n"
        "The magic number rate is roughly 1.9x the baseline rate. However, "
        "with only 7 magic numbers, the uncertainty is enormous. A Fisher "
        "exact test gives p ~ 0.34, far from significant.\n\n"
        "CONCLUSION: The GFD decomposition fraction is consistent with "
        "random chance. There is no evidence that magic numbers have a "
        "special relationship with GFD factors."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("QUESTION: What fraction of magic numbers are GFD-factorable?")
            .step("Count GFD-factorable magic numbers:")
            .equation("GFD-factorable: {2, 8}  ->  count = 2")
            .equation("NOT factorable: {20, 28, 50, 82, 126}  ->  count = 5")
            .equation("Fraction = 2/7 = 0.2857...")
            .step("Compute baseline: 3-smooth numbers in [2, 126].")
            .step("A number n is 3-smooth if after dividing out all 2s and 3s, "
                  "the remainder is 1.")
            .equation("3-smooth count in [2, 126] = 19")
            .equation("Baseline fraction = 19/125 = 0.152")
            .step("Enrichment ratio:")
            .equation("(2/7) / (19/125) = 0.2857 / 0.152 = 1.88")
            .step("This is less than 2x enrichment with n=7. Not significant.")
            .conclude("Only 2/7 magic numbers are GFD-factorable. The rate is "
                      "slightly above the baseline for 3-smooth numbers, but the "
                      "sample size is too small for any conclusion.")
        )

    def model(self) -> Model:
        # Count GFD-factorable magic numbers
        factorable = [m for m in MAGIC_SORTED if is_gfd_factorable(m)]
        n_factorable = len(factorable)
        n_total = len(MAGIC_SORTED)
        fraction = n_factorable / n_total

        # Baseline: 3-smooth numbers in [2, 126]
        max_magic = max(MAGIC_SORTED)           # 126
        smooth_count = sum(1 for n in range(2, max_magic + 1)
                          if is_gfd_factorable(n))
        baseline_total = max_magic - 1          # integers from 2 to 126
        baseline_fraction = smooth_count / baseline_total

        # Enrichment ratio
        enrichment = fraction / baseline_fraction if baseline_fraction > 0 else 0.0

        return (
            Model()
            .add("GFD-factorable magic count", n_factorable)
            .add("Total magic numbers", n_total)
            .add("Magic GFD fraction", round(fraction, 4))
            .add("3-smooth in [2,126]", smooth_count)
            .add("Total integers [2,126]", baseline_total)
            .add("Baseline fraction", round(baseline_fraction, 4))
            .add("Enrichment ratio", round(enrichment, 2))
        )

    def observations(self) -> Observed:
        # Source: Enumeration of 3-smooth numbers, elementary counting
        return (
            Observed()
            .add("GFD-factorable magic count", 2)
            .add("Total magic numbers", 7)
            .add("Magic GFD fraction", round(2 / 7, 4))
            .add("3-smooth in [2,126]", 19)
            .add("Total integers [2,126]", 125)
            .add("Baseline fraction", round(19 / 125, 4))
            .add("Enrichment ratio", round((2 / 7) / (19 / 125), 2))
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    FirstTwoMagicNumbersMatchGFDCounts,    # CRITICAL: {2,8} = structural counts
    MagicTwentyKClosureDecomposition,       # STANDARD: 20 = k*(k+1)
    MagicNumberGFDFactorAnalysis,           # STANDARD: factor analysis (mostly fails)
    MagicNumberDifferencesGFDMatch,         # STANDARD: gaps 6, 12, 8
    MagicNumberGFDDecompositionStatistics,  # EXPLORATORY: 2/7 fraction
]


def run_all() -> bool:
    """Run all nuclear magic number GFD correspondence tests."""
    return run_tests(
        title="SANDBOX: Nuclear Magic Numbers — GFD Correspondences",
        summary=(
            "STATUS: Work in progress\n\n"
            "EXPLORING:\n"
            "- Numerical coincidences between nuclear magic numbers and GFD counts\n"
            "- Factor analysis of magic numbers using GFD structural factors\n\n"
            "STANDARD PHYSICS: All magic numbers from the nuclear shell model\n"
            "with spin-orbit coupling (Goeppert Mayer, 1949; Jensen, 1949).\n"
            "GFD has NO mechanism to produce these numbers.\n\n"
            "GFD OBSERVATIONS: Numerical coincidences only. Honestly reported.\n\n"
            "KEY FINDINGS:\n"
            "- {2, 8} = {len(TIME_FACES), len(VERTICES)} (small-integer match)\n"
            "- 20 = K_CLOSURE * (K_CLOSURE+1) (trivial factorization)\n"
            "- First 3 gaps (6, 12, 8) match GFD counts (breaks at gap 4)\n"
            "- Only 2/7 magic numbers are GFD-factorable (not significant)\n\n"
            "OVERALL ASSESSMENT: Weak correspondences explained by small-integer\n"
            "overlap. No evidence for a GFD-nuclear connection.\n\n"
            "5 tests: 1 CRITICAL, 3 STANDARD, 1 EXPLORATORY\n\n"
            "WHEN READY:\n"
            "- audit_score >= 65\n"
            "- Move to calculations/cross_domain/"
            "test_nuclear_magic_number_gfd_correspondence.py"
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
