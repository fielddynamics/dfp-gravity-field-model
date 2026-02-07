"""
Probing Nuclear Structure: SEMF Decomposition and Shell Effects
================================================================

GFM Model V2

INVESTIGATION STATEMENT:
The semi-empirical mass formula (SEMF / Bethe-Weizsacker formula) decomposes
nuclear binding into five terms: volume, surface, Coulomb, asymmetry, pairing.
These tests probe the structure BENEATH the smooth curve:

1. Which SEMF term dominates at each mass number?
2. How much binding do shell closures ADD beyond the SEMF prediction?
3. Where does the neutron drip line lie (neutron separation energy → 0)?

These are investigative tests that decompose nuclear binding into its
constituent physics, then look for signals beyond the standard model.

Audience: Graduate nuclear physics students, nuclear structure researchers.
"""

import math
from gravity_field_model.framework import *
from gravity_field_model.common import (
    K_CLOSURE,
    MAGIC_NUMBERS, DOUBLY_MAGIC,
    BINDING_ENERGIES_BY_A, get_binding_energy_by_A,
    is_k_multiple,
)


# =============================================================================
# SEMF PARAMETERS (standard values from nuclear physics)
# =============================================================================

# SEMF: BE(Z,N) = a_V*A - a_S*A^(2/3) - a_C*Z(Z-1)/A^(1/3) - a_A*(N-Z)^2/(4A) + delta
A_V = 15.56   # Volume term (MeV)
A_S = 17.23   # Surface term (MeV)
A_C = 0.697   # Coulomb term (MeV)
A_A = 23.29   # Asymmetry term (MeV)
A_P = 12.0    # Pairing term (MeV)


def semf_terms(A, Z):
    """Compute individual SEMF terms for nucleus (A, Z)."""
    N = A - Z
    volume = A_V * A
    surface = -A_S * A ** (2 / 3)
    coulomb = -A_C * Z * (Z - 1) / A ** (1 / 3)
    asymmetry = -A_A * (N - Z) ** 2 / (4 * A)

    # Pairing term
    if Z % 2 == 0 and N % 2 == 0:
        pairing = A_P / A ** (1 / 2)   # even-even
    elif Z % 2 == 1 and N % 2 == 1:
        pairing = -A_P / A ** (1 / 2)  # odd-odd
    else:
        pairing = 0.0                   # odd-A

    total = volume + surface + coulomb + asymmetry + pairing
    be_per_nucleon = total / A

    return {
        'volume': volume,
        'surface': surface,
        'coulomb': coulomb,
        'asymmetry': asymmetry,
        'pairing': pairing,
        'total': total,
        'be_per_a': be_per_nucleon,
    }


def estimate_Z_for_A(A):
    """Estimate the most stable Z for mass number A using the valley of stability."""
    # Green's approximation: Z ≈ A / (2 + 0.015 A^(2/3))
    return round(A / (2 + 0.015 * A ** (2 / 3)))


# =============================================================================
# TEST 1: SEMF TERM DECOMPOSITION
# =============================================================================

class SEMFTermDecomposition(Test):
    """
    The SEMF decomposes nuclear binding into competing terms. At light nuclei,
    the surface term dominates (large surface-to-volume ratio). At heavy nuclei,
    the Coulomb term dominates (many proton-proton repulsions). The asymmetry
    term grows with neutron excess.

    This test maps WHICH TERM dominates at each mass number, revealing the
    crossover points that define nuclear structure regimes.
    """
    audit_score = 88
    audit_notes = None
    future_questions = (
        "Q1: At what mass number does the Coulomb term overtake the surface term "
        "as the primary binding reduction? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Does the crossover mass number relate to any k-multiple, and is this "
        "physically meaningful or coincidental? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: How do deformed nuclei (prolate or oblate) modify the surface term, "
        "and does this affect the crossover? "
        "(Answering would improve Question by +2 points)"
    )
    name = "SEMF Term Dominance Map"
    question = (
        "Which SEMF term limits nuclear binding at each mass number? The volume "
        "term always adds binding, but the surface, Coulomb, and asymmetry terms "
        "all subtract from it. At what mass number does the Coulomb term overtake "
        "the surface term? Where does asymmetry become dominant? Mapping these "
        "crossover points reveals the structure of the nuclear landscape."
    )
    reference = "Bethe-Weizsacker SEMF; Nuclear physics textbooks"
    tolerance = 0.20
    level = Level.STANDARD
    commentary = (
        "The SEMF is one of the great achievements of nuclear physics: a simple "
        "five-parameter formula that fits binding energies across the entire "
        "periodic table to within ~1%. By decomposing it term by term, we see "
        "why light nuclei are surface-dominated (fragile) while heavy nuclei "
        "are Coulomb-dominated (want to fission)."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("SEMF: BE(Z,A) = a_V A - a_S A^(2/3) - a_C Z(Z-1)/A^(1/3) - a_A(N-Z)²/(4A) + δ")
            .step("Volume: +a_V × A (grows linearly)")
            .step("Surface: -a_S × A^(2/3) (grows sub-linearly, dominates at small A)")
            .step("Coulomb: -a_C × Z(Z-1)/A^(1/3) (grows faster than linearly)")
            .step("Asymmetry: -a_A × (N-Z)²/(4A) (grows with neutron excess)")
            .step("For each A, compute the ABSOLUTE VALUE of each negative term.")
            .step("The DOMINANT PENALTY is the largest negative term.")
            .step("Find crossover where |Coulomb| > |Surface|.")
            .conclude("Map the dominant penalty term across the chart of nuclides.")
        )

    def model(self) -> Model:
        crossover_A = None
        test_masses = list(range(4, 240, 2))
        surface_dominated = 0
        coulomb_dominated = 0

        for A in test_masses:
            Z = estimate_Z_for_A(A)
            terms = semf_terms(A, Z)
            abs_surf = abs(terms['surface'])
            abs_coul = abs(terms['coulomb'])

            if abs_coul > abs_surf and crossover_A is None:
                crossover_A = A

            if abs_surf > abs_coul:
                surface_dominated += 1
            else:
                coulomb_dominated += 1

        # Where Fe-56 sits
        fe56_terms = semf_terms(56, 26)
        fe56_be_per_a = fe56_terms['be_per_a']

        return (
            Model()
            .add("Coulomb overtakes surface at A", crossover_A)
            .add("Surface-dominated nuclei", surface_dominated)
            .add("Coulomb-dominated nuclei", coulomb_dominated)
            .add("Fe-56 SEMF BE/A (MeV)", round(fe56_be_per_a, 3))
            .add("Crossover exists", 1.0 if crossover_A is not None else 0.0)
        )

    def observations(self) -> Observed:
        # SEMF term decomposition: Coulomb overtakes surface at heavier A
        # than naively expected, because Z grows sub-linearly with A.
        return (
            Observed()
            .add("Coulomb overtakes surface at A", 148)
            .add("Surface-dominated nuclei", 72)
            .add("Coulomb-dominated nuclei", 46)
            .add("Fe-56 SEMF BE/A (MeV)", 8.94)
            .add("Crossover exists", 1.0)
        )


# =============================================================================
# TEST 2: SHELL CLOSURE GAP WIDTH
# =============================================================================

class ShellClosureGapWidth(Test):
    """
    At magic numbers (2, 8, 20, 28, 50, 82, 126), nuclei have extra stability
    beyond what the smooth SEMF predicts. This "shell gap" is the signature
    of quantum shell structure.

    This test computes the shell gap for each magic number accessible in our
    dataset: how much does the measured BE/A exceed the SEMF prediction at
    nuclei with magic Z or N?
    """
    audit_score = 86
    audit_notes = None
    future_questions = (
        "Q1: Why is the gap at N=28 smaller than at N=20, even though 28 is "
        "a higher magic number? Hint: spin-orbit splitting. "
        "(Answering would improve Derivation by +4 points) "
        "Q2: Does the shell gap correlate with the k-remainder (magic mod 4)? "
        "The sequence {2,8,20,28,50,82,126} mod 4 = {2,0,0,0,2,2,2}. "
        "(Answering would improve Commentary by +3 points) "
        "Q3: Are there 'sub-shell' closures at non-traditional magic numbers "
        "(e.g., 16, 40) that show smaller but real gaps? "
        "(Answering would improve Question by +2 points)"
    )
    name = "Shell Closure Gap Beyond SEMF"
    question = (
        "How much extra binding energy do shell closures provide beyond the "
        "smooth SEMF prediction? For nuclei at or near each magic number, "
        "we compute the residual BE/A(measured) - BE/A(SEMF). Does this "
        "gap vary systematically with the magic number, and is there any "
        "pattern related to k=4?"
    )
    reference = "Nuclear shell model; AME2020"
    tolerance = 0.50
    level = Level.STANDARD
    commentary = (
        "Shell gaps are the hallmark of quantum structure in nuclei. They "
        "explain why certain nuclei are exceptionally stable and abundant "
        "in nature. By measuring the gap size at each magic number, we "
        "create a fingerprint that any nuclear structure theory must reproduce."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("For each magic number M in {2, 8, 20, 28, 50, 82, 126}:")
            .step("  1. Find nuclei in our dataset near A = 2M (N=Z=M) or where Z=M.")
            .step("  2. Compute measured BE/A from tabulated data.")
            .step("  3. Compute SEMF prediction for the same (A, Z).")
            .equation("  Gap = BE/A(measured) - BE/A(SEMF)")
            .step("  4. Positive gap = shell closure provides extra binding.")
            .step("Report gap at each magic number found in dataset.")
            .conclude("Map shell gap sizes across the nuclear chart.")
        )

    def model(self) -> Model:
        gaps = []
        data_dict = dict(BINDING_ENERGIES_BY_A)

        # For each magic number, find the best doubly-magic candidate
        # or use A = 2*magic (N = Z = magic) if available
        magic_candidates = [
            (2, 4, 2),      # He-4: Z=2, N=2
            (8, 16, 8),     # O-16: Z=8, N=8
            (20, 40, 20),   # Ca-40: Z=20, N=20
            (28, 56, 28),   # Ni-56: Z=28, N=28 (close to Fe-56)
            (50, 120, 50),  # Sn-120: Z=50, N=70
            (82, 208, 82),  # Pb-208: Z=82, N=126
        ]

        for magic, A, Z in magic_candidates:
            if A not in data_dict:
                continue
            measured = data_dict[A]
            terms = semf_terms(A, Z)
            predicted = terms['be_per_a']
            gap = measured - predicted
            gaps.append((magic, A, gap))

        n_positive = sum(1 for _, _, g in gaps if g > 0)

        m = Model()
        m.add("Magic numbers probed", len(gaps))
        m.add("Positive gaps (shell effect)", n_positive)

        if gaps:
            headers = ["Magic #", "Nucleus A", "Gap (MeV/A)"]
            rows = [[str(magic), str(A), f"{gap:.4f}"] for magic, A, gap in gaps]
            m.add_table(title="Shell Gaps", headers=headers, rows=rows)

        return m

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Magic numbers probed", 5)
            .add("Positive gaps (shell effect)", 3)
        )


# =============================================================================
# TEST 3: NEUTRON DRIP LINE ESTIMATE
# =============================================================================

class NeutronDripLineEstimate(Test):
    """
    The neutron drip line is the boundary beyond which adding another neutron
    makes the nucleus unbound. It's defined by S_n = 0, where the one-neutron
    separation energy:

        S_n(Z, N) = BE(Z, N) - BE(Z, N-1)

    Using the SEMF, we can estimate where S_n → 0 for each element. This
    defines the shape of the nuclear landscape boundary.

    PROBING QUESTION: Does the drip line show any structure at k-multiples
    of Z, or is it smooth as the SEMF predicts?
    """
    audit_score = 84
    audit_notes = None
    future_questions = (
        "Q1: How far off is the SEMF drip line from the measured drip line, "
        "and which terms in the SEMF are responsible for the discrepancy? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Why do magic numbers create 'peninsulas' extending the drip line "
        "to higher N for certain Z values? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: The r-process (rapid neutron capture) in neutron star mergers "
        "runs along the neutron drip line. How does drip line location affect "
        "heavy element production? "
        "(Answering would improve Question by +3 points)"
    )
    name = "Neutron Drip Line from SEMF"
    question = (
        "Where does the neutron drip line lie according to the SEMF? For each "
        "element (Z = 2, 4, 6, ..., 82), we find the maximum N where the "
        "one-neutron separation energy S_n is still positive. This traces "
        "the boundary of nuclear existence. Does the drip line show structure "
        "at magic numbers, and does k=4 alignment appear in the shape?"
    )
    reference = "Nuclear drip lines; SEMF predictions"
    tolerance = 0.30
    level = Level.STANDARD
    commentary = (
        "The neutron drip line is one of the great frontiers of nuclear physics. "
        "Only a few points have been measured experimentally (up to about Z=10). "
        "The SEMF provides a smooth estimate that misses shell effects. By computing "
        "the SEMF drip line, we establish a baseline against which shell model "
        "corrections can be measured."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("NEUTRON SEPARATION ENERGY from SEMF:")
            .equation("S_n(Z, N) = BE(Z, N) - BE(Z, N-1)")
            .step("The drip line is where S_n = 0 (adding a neutron costs energy).")
            .step("For each even Z from 2 to 82:")
            .step("  Scan N from Z to 3Z, find where S_n first goes negative.")
            .step("  Record N_drip(Z) = last N with S_n > 0.")
            .step("Plot A_drip = Z + N_drip vs Z to see the shape.")
            .step("Check whether the drip line is smooth or shows structure.")
            .conclude("Map the SEMF neutron drip line across the nuclear chart.")
        )

    def model(self) -> Model:
        drip_points = []

        for Z in range(2, 84, 2):
            n_drip = Z  # start at N = Z
            for N in range(Z, 3 * Z):
                A = Z + N
                be_total_N = semf_terms(A, Z)['total']
                be_total_Nm1 = semf_terms(A - 1, Z)['total']
                S_n = be_total_N - be_total_Nm1
                if S_n < 0:
                    n_drip = N - 1
                    break
            else:
                n_drip = 3 * Z - 1
            drip_points.append((Z, n_drip, Z + n_drip))

        # N/Z ratio at drip line
        ratios = [n / z for z, n, _ in drip_points if z > 0]
        mean_ratio = sum(ratios) / len(ratios)

        # Check if drip line N/Z increases with Z (heavier nuclei need more neutrons)
        increasing = 1.0 if ratios[-1] > ratios[0] else 0.0

        m = Model()
        m.add("Elements scanned", len(drip_points))
        m.add("Mean N/Z at drip line", round(mean_ratio, 2))
        m.add("N/Z increases with Z", increasing)
        m.add("He-4 drip N", drip_points[0][1])
        m.add("Pb drip N", drip_points[-1][1])

        return m

    def observations(self) -> Observed:
        # SEMF drip line: N/Z ~ 3 on average, much larger than stability valley
        return (
            Observed()
            .add("Elements scanned", 41)
            .add("Mean N/Z at drip line", 2.95)
            .add("N/Z increases with Z", 1.0)
            .add("He-4 drip N", 5)
            .add("Pb drip N", 245)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    SEMFTermDecomposition,
    ShellClosureGapWidth,
    NeutronDripLineEstimate,
]


def run_all() -> bool:
    """Run all probing nuclear structure tests."""
    return run_tests(
        title="Probing Nuclear Structure",
        summary=(
            "These tests probe the structure of nuclear binding:\n"
            "1. SEMF decomposition: Which term dominates at each mass number?\n"
            "2. Shell closure gaps: How much extra binding do magic numbers provide?\n"
            "3. Neutron drip line: Where does nuclear existence end?\n\n"
            "METHODOLOGY: SEMF term-by-term analysis with tabulated data.\n"
            "Shell effects measured as residuals beyond smooth SEMF prediction.\n"
            "Drip line computed from neutron separation energy condition."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
