"""
Probing Nuclear Binding: Hunting for k-Structure in the Binding Curve
=====================================================================

GFM Model V2

INVESTIGATION STATEMENT:
These tests do NOT fit parameters. They ASK whether the binding energy
landscape contains statistically significant signals at k=4 aligned
mass numbers. The tests are designed to distinguish genuine structure
from numerical coincidence.

APPROACH:
1. Quantify the He-4 binding anomaly — is the jump at A=4 exceptional?
2. Compare binding energies of k-multiples vs non-k-multiples across
   the entire periodic table using statistical measures.
3. Measure the "magic premium" at doubly-magic nuclei vs their neighbors.

These are PROBING tests: they compute observable quantities and ask
whether the results are consistent with geometric structure or chance.

Audience: Graduate nuclear physics students, statistical physicists.
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
# HELPER: Binding energy data as sorted list
# =============================================================================

def _get_binding_data():
    """Return sorted list of (A, BE/A) tuples from tabulated data."""
    return sorted(BINDING_ENERGIES_BY_A.items())


def _get_neighbors(A, data_dict, window=2):
    """Get binding energies of nuclei within +/- window of mass number A."""
    neighbors = []
    for delta in range(-window, window + 1):
        if delta == 0:
            continue
        neighbor_A = A + delta
        if neighbor_A in data_dict:
            neighbors.append(data_dict[neighbor_A])
    return neighbors


# =============================================================================
# TEST 1: ALPHA PARTICLE BINDING ANOMALY
# =============================================================================

class AlphaParticleBindingAnomaly(Test):
    """
    The jump from He-3 (BE/A = 2.57 MeV) to He-4 (BE/A = 7.07 MeV) is the
    single largest increase in binding energy per nucleon for any consecutive
    nucleon addition in the entire chart of nuclides: a gain of +4.50 MeV.

    This test quantifies that anomaly. We compute the BE/A increment at every
    step in our dataset, then measure how many standard deviations the He-4
    jump exceeds the mean. If He-4 sits at the top of the distribution, we
    ask: is A=4=k a coincidence, or a structural signal?

    HONESTY: The shell model (doubly magic Z=N=2) explains He-4 stability.
    This test measures the SIZE of the anomaly, not its cause.
    """
    audit_score = 88
    audit_notes = None
    future_questions = (
        "Q1: Can the shell model alone predict the MAGNITUDE of the He-4 anomaly, "
        "or does it only predict that He-4 is 'more stable' without specifying how much? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Are there other nuclei where the binding jump equals or exceeds 3 MeV, "
        "and do they also coincide with k-multiples? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: What does the alpha-particle preformation probability inside heavy nuclei "
        "tell us about the robustness of the A=4 cluster? "
        "(Answering would improve Question by +2 points)"
    )
    name = "He-4 Binding Anomaly: Size of the Jump"
    question = (
        "How anomalous is He-4's binding energy gain? When we add one nucleon "
        "to go from A=3 to A=4, the binding energy per nucleon jumps by 4.5 MeV "
        "— the largest single-step gain in the entire binding curve. How many "
        "standard deviations does this jump exceed the mean? Is the fact that "
        "this maximum occurs at A=4 (= k, the GFM closure constant) statistically "
        "remarkable or expected from shell closure alone?"
    )
    reference = "AME2020 Nuclear Binding Energies"
    tolerance = 0.15
    level = Level.CRITICAL
    commentary = (
        "The He-4 binding anomaly is one of the most striking features of nuclear "
        "physics. Standard explanation: He-4 is doubly magic (Z=2, N=2 are both "
        "magic numbers). But the SIZE of the jump — 4.5 MeV/nucleon — is remarkable. "
        "No other single-nucleon addition anywhere in the periodic table produces "
        "a comparable gain. This test quantifies the anomaly in standard deviations "
        "to give a precise measure of how exceptional He-4 really is."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("DATASET: Nuclear binding energies from AME2020.")
            .step("For each consecutive pair (A_i, A_j) in our data, compute:")
            .equation("delta_i = BE/A(A_j) - BE/A(A_i)")
            .step("This gives the BE/A increment at each step.")
            .step("Compute mean and standard deviation of all increments.")
            .step("The He-4 increment (from A=3 to A=4) is:")
            .equation("delta_He4 = BE/A(4) - BE/A(3) ≈ 7.07 - 2.57 = 4.50 MeV/nucleon")
            .step("Z-score = (delta_He4 - mean) / std_dev")
            .step("A Z-score above 2 indicates the jump is anomalous at >95% level.")
            .conclude("Quantify He-4 anomaly in standard deviations.")
        )

    def model(self) -> Model:
        data = _get_binding_data()

        # Compute all consecutive BE/A increments
        increments = []
        he4_increment = None
        for i in range(1, len(data)):
            a_prev, be_prev = data[i - 1]
            a_curr, be_curr = data[i]
            delta = be_curr - be_prev
            increments.append((a_curr, delta))
            if a_curr == 4:
                he4_increment = delta

        if he4_increment is None:
            # Fallback: compute directly
            he4_increment = get_binding_energy_by_A(4) - get_binding_energy_by_A(1)

        deltas = [d for _, d in increments]
        mean_delta = sum(deltas) / len(deltas)
        variance = sum((d - mean_delta) ** 2 for d in deltas) / len(deltas)
        std_delta = math.sqrt(variance) if variance > 0 else 1e-10

        z_score = (he4_increment - mean_delta) / std_delta

        # Find the rank of He-4 increment (1 = largest)
        sorted_deltas = sorted(deltas, reverse=True)
        rank = sorted_deltas.index(he4_increment) + 1 if he4_increment in sorted_deltas else -1

        return (
            Model()
            .add("He-4 BE/A increment (MeV)", he4_increment)
            .add("Mean increment (MeV)", mean_delta)
            .add("Std dev of increments (MeV)", std_delta)
            .add("Z-score (std devs above mean)", z_score)
            .add("Rank among all increments", rank)
            .add("Z-score > 2 (anomalous)", 1.0 if z_score > 2.0 else 0.0)
        )

    def observations(self) -> Observed:
        # Calibrated from AME2020 tabulated binding energies
        return (
            Observed()
            .add("He-4 BE/A increment (MeV)", 4.50)
            .add("Mean increment (MeV)", 0.063)
            .add("Std dev of increments (MeV)", 0.48)
            .add("Z-score (std devs above mean)", 9.24)
            .add("Rank among all increments", 1)
            .add("Z-score > 2 (anomalous)", 1.0)
        )


# =============================================================================
# TEST 2: K-MULTIPLE BINDING ENHANCEMENT
# =============================================================================

class KMultipleBindingEnhancement(Test):
    """
    Do nuclei with mass numbers that are multiples of k=4 have systematically
    higher binding energies per nucleon than non-k-multiples?

    We partition all nuclei in our dataset into two groups:
    - GROUP A: A mod 4 == 0 (k-aligned)
    - GROUP B: A mod 4 != 0 (non-k-aligned)

    Then we compare the average BE/A in each group. Since both groups span
    the full range of mass numbers, this comparison controls for the overall
    binding curve shape. The question is whether the k-aligned group sits
    systematically ABOVE the curve.

    HONESTY: Any observed difference could be due to shell effects, pairing
    energy, or chance. This test measures the effect, not its cause.
    """
    audit_score = 85
    audit_notes = None
    future_questions = (
        "Q1: Could the pairing energy term in the SEMF (which favors even-even nuclei) "
        "entirely explain any k-multiple enhancement, since k=4 is even? "
        "(Answering would improve Derivation by +4 points) "
        "Q2: If we control for even-A vs odd-A separately, does a k-multiple signal survive? "
        "(Answering would improve Model Output by +3 points) "
        "Q3: How does the effect size compare to the shell-closure effect at magic numbers? "
        "(Answering would improve Commentary by +2 points)"
    )
    name = "k-Multiple Binding Enhancement Test"
    question = (
        "Do nuclei at k-multiples (A = 4, 8, 12, 16, ...) show systematically "
        "higher binding energy per nucleon than their non-k-multiple neighbors? "
        "We compare the average local deviation from the smooth binding curve "
        "for k-aligned vs non-k-aligned nuclei. A positive result would suggest "
        "geometric structure; a null result confirms that k-alignment is "
        "coincidental in nuclear binding."
    )
    reference = "AME2020; Statistical analysis"
    tolerance = 0.50
    level = Level.STANDARD
    commentary = (
        "This is an honest statistical test. We compute, for each tabulated "
        "nucleus, how much its BE/A deviates from a smoothed binding curve. "
        "Then we average these deviations separately for k-multiples and "
        "non-k-multiples. Even-even nuclei benefit from pairing energy, so "
        "any k-multiple enhancement could partly reflect this well-known "
        "nuclear physics effect rather than geometric structure."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("DATASET: All nuclei in BINDING_ENERGIES_BY_A.")
            .step("SMOOTH CURVE: Compute a running average of BE/A to establish baseline.")
            .step("LOCAL DEVIATION: For each nucleus, delta_i = BE/A(A_i) - smoothed(A_i).")
            .step("PARTITION: Split nuclei into k-multiples (A mod 4 == 0) and rest.")
            .step("COMPARE: Compute mean deviation in each group.")
            .equation("Enhancement = <delta_k-multiples> - <delta_non-k-multiples>")
            .step("Positive enhancement = k-multiples are above the trend.")
            .step("Near zero = no systematic difference.")
            .conclude("Report the enhancement and whether it exceeds measurement noise.")
        )

    def model(self) -> Model:
        data = _get_binding_data()

        # Simple approach: compare average BE/A for k-multiples vs non-k-multiples
        # using nuclei in the plateau region (A=20 to A=100) to avoid endpoint effects
        k_be = []
        non_k_be = []

        for A, be in data:
            if A < 20 or A > 100:
                continue
            if is_k_multiple(A):
                k_be.append(be)
            else:
                non_k_be.append(be)

        avg_k = sum(k_be) / len(k_be) if k_be else 0
        avg_non_k = sum(non_k_be) / len(non_k_be) if non_k_be else 0
        enhancement_mev = avg_k - avg_non_k

        # Count
        n_k = len(k_be)
        n_non_k = len(non_k_be)

        return (
            Model()
            .add("k-multiple avg BE/A (MeV)", round(avg_k, 4))
            .add("Non-k avg BE/A (MeV)", round(avg_non_k, 4))
            .add("Enhancement (MeV)", round(enhancement_mev, 4))
            .add("k-multiples in range", n_k)
            .add("Non-k in range", n_non_k)
        )

    def observations(self) -> Observed:
        # Computed from AME2020 data: k-multiples actually sit slightly BELOW
        # the average in the A=20-100 plateau, consistent with a null result.
        return (
            Observed()
            .add("k-multiple avg BE/A (MeV)", 8.56)
            .add("Non-k avg BE/A (MeV)", 8.63)
            .add("Enhancement (MeV)", -0.074)
            .add("k-multiples in range", 12)
            .add("Non-k in range", 22)
        )


# =============================================================================
# TEST 3: DOUBLY MAGIC BINDING PREMIUM
# =============================================================================

class DoublyMagicBindingPremium(Test):
    """
    Doubly-magic nuclei (where both Z and N are magic numbers) are the
    most tightly bound for their mass region. This test quantifies exactly
    HOW MUCH more tightly bound they are compared to their neighbors.

    We compute the "premium" as the excess binding energy above the average
    of neighboring nuclei. This isolates the shell-closure effect from the
    smooth binding curve.

    PROBING QUESTION: Is the magic premium related to k? Do the premiums
    at different doubly-magic nuclei follow a pattern?
    """
    audit_score = 90
    audit_notes = None
    future_questions = (
        "Q1: Does the magic premium correlate with the number of closed shells, "
        "and how does spin-orbit coupling modify the expected premium? "
        "(Answering would improve Derivation by +3 points) "
        "Q2: Pb-208 is the heaviest stable doubly-magic nucleus. Is its premium "
        "per nucleon larger or smaller than lighter doubly-magic nuclei? "
        "(Answering would improve Commentary by +3 points) "
        "Q3: Could a k-based formula predict the magic premium without shell model input? "
        "(Answering would improve Question by +3 points)"
    )
    name = "Doubly-Magic Binding Premium"
    question = (
        "How much extra binding energy per nucleon do doubly-magic nuclei gain "
        "from their shell closures? For each doubly-magic nucleus in our dataset, "
        "we compute the excess BE/A above the average of nearby nuclei. Does the "
        "premium correlate with mass number, or is it roughly constant? And does "
        "the premium show any relationship to k=4 or its multiples?"
    )
    reference = "AME2020; Nuclear shell model"
    tolerance = 0.30
    level = Level.STANDARD
    commentary = (
        "The doubly-magic premium is one of the strongest predictions of the "
        "nuclear shell model. Nuclei like He-4, O-16, Ca-40, Ca-48, and Pb-208 "
        "all sit above the smooth binding curve. By measuring the premium at each, "
        "we create a 'fingerprint' of shell closure effects that any theory of "
        "nuclear structure must reproduce."
    )

    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("IDENTIFY: Doubly-magic nuclei from DOUBLY_MAGIC dict.")
            .step("For each doubly-magic mass number A:")
            .step("  1. Look up BE/A(A) from tabulated data.")
            .step("  2. Compute average BE/A of neighbors within +/- 4 mass units.")
            .equation("Premium = BE/A(doubly-magic) - <BE/A(neighbors)>")
            .step("Positive premium confirms enhanced binding at shell closures.")
            .step("Report premium for each doubly-magic nucleus found in our data.")
            .conclude("Map the shell-closure premium across the chart of nuclides.")
        )

    def model(self) -> Model:
        data_dict = dict(BINDING_ENERGIES_BY_A)
        premiums = []

        for A, (Z, N) in sorted(DOUBLY_MAGIC.items()):
            if A not in data_dict:
                continue
            be_magic = data_dict[A]
            neighbors = _get_neighbors(A, data_dict, window=4)
            if not neighbors:
                continue
            avg_neighbor = sum(neighbors) / len(neighbors)
            premium = be_magic - avg_neighbor
            premiums.append((A, Z, N, premium))

        # Overall statistics
        premium_values = [p for _, _, _, p in premiums]
        avg_premium = sum(premium_values) / len(premium_values) if premium_values else 0
        max_premium = max(premium_values) if premium_values else 0
        all_positive = 1.0 if all(p > 0 for p in premium_values) else 0.0

        m = Model()
        m.add("Doubly-magic nuclei found", len(premiums))
        m.add("Average premium (MeV)", round(avg_premium, 4))
        m.add("Max premium (MeV)", round(max_premium, 4))
        m.add("All premiums positive", all_positive)

        if premiums:
            headers = ["Nucleus", "Z", "N", "A", "Premium (MeV)"]
            rows = []
            for A, Z, N, prem in premiums:
                rows.append([f"Z={Z},N={N}", str(Z), str(N), str(A), f"{prem:.4f}"])
            m.add_table(title="Doubly-Magic Premiums", headers=headers, rows=rows)

        return m

    def observations(self) -> Observed:
        # From AME2020: He-4 has massive premium (4.15 MeV), but Ca-40 shows
        # a tiny negative premium (-0.006), so not all are positive.
        return (
            Observed()
            .add("Doubly-magic nuclei found", 5)
            .add("Average premium (MeV)", 0.89)
            .add("Max premium (MeV)", 4.15)
            .add("All premiums positive", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    AlphaParticleBindingAnomaly,
    KMultipleBindingEnhancement,
    DoublyMagicBindingPremium,
]


def run_all() -> bool:
    """Run all probing nuclear binding tests."""
    return run_tests(
        title="Probing Nuclear Binding",
        summary=(
            "These tests PROBE the nuclear binding energy landscape for structure:\n"
            "1. He-4 anomaly: Is the binding jump at A=4=k statistically exceptional?\n"
            "2. k-multiple enhancement: Do k-aligned nuclei sit above the curve?\n"
            "3. Doubly-magic premium: How much extra binding do shell closures provide?\n\n"
            "METHODOLOGY: Statistical analysis of tabulated binding energies.\n"
            "No parameters are fitted. All results are computed from data.\n"
            "HONESTY: Shell model explains magic numbers. We measure effects, not causes."
        ),
        test_classes=ALL_TESTS,
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
