# FILENAME: test_hamming_distance_tetrahedra.py

"""
Hamming Distance Structure of Dual Tetrahedra
==============================================

The stellated octahedron's two tetrahedra are defined by parity partition
of the cube's 8 vertices. But a partition into two groups of 4 is not
automatically two regular tetrahedra. The geometric claim requires that
all edges within each tetrahedron have equal length, which in the binary
encoding translates to a uniform Hamming distance between vertex labels.

Standard combinatorics tells us that 3 bit binary strings of the same
parity class always differ in exactly 2 bit positions (Hamming distance 2).
This is because flipping a single bit changes parity, so same parity
vertices must differ by an even number of bits: either 0 (same vertex)
or 2 (the only remaining option in 3 bits). This uniform Hamming distance
of 2 maps to a uniform Euclidean edge length of 2*sqrt(2) in the (+/- 1)
coordinate system, confirming geometric regularity.

GFM OBSERVATION: Hamming distance 2 within each chamber means single bit
errors always cross between Tet A and Tet B, linking geometry to error detection.

This is an OBSERVATION connecting combinatorial structure to geometric regularity.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, TET_A, TET_B,
)


class HammingDistanceWithinTetrahedra(Test):
    """
    PHYSICAL CONTEXT:
    A regular tetrahedron is defined by the property that all six edges
    have equal length. When four vertices of a cube are selected to form
    an inscribed tetrahedron, this regularity is guaranteed if and only
    if every pair of selected vertices lies on a face diagonal (not an
    edge and not a space diagonal) of the cube. In the binary labeling
    of cube vertices with 3 bit strings, face diagonals connect vertices
    that differ in exactly 2 bit positions, i.e., Hamming distance 2.
    This is a standard result in combinatorial geometry (Coxeter 1973).

    GFM OBSERVATION:
    The Hamming distance structure has a direct information theoretic
    interpretation. Within each tetrahedron (same parity chamber), all
    pairs are at Hamming distance 2. Between tetrahedra (opposite parity),
    pairs are at Hamming distance 1 or 3 (odd distances only). This means
    any single bit flip on a vertex label necessarily crosses chambers,
    mirroring how the implicit channel (complement 7 minus V) always
    references the opposite tetrahedron.

    EPISTEMIC STATUS:
    This is a mathematical verification of combinatorial geometry, not a
    GFM derivation. The observation that Hamming structure enforces chamber
    crossing under single bit errors is noted but not claimed as derived.
    """

    name = "Hamming Distance Within Tetrahedra"

    question = (
        "Why do all vertex pairs within each tetrahedron have Hamming distance "
        "exactly 2? In 3 bit binary strings, same parity vertices cannot differ "
        "by 1 or 3 bits (both odd), leaving Hamming distance 2 as the only "
        "possibility. Does this combinatorial constraint fully explain the "
        "geometric regularity of the inscribed tetrahedra?"
    )

    reference = (
        "Coxeter (1973), Regular Polytopes; "
        "GFM Textbook Ch.9 Sec.9.2: Binary encoding of cube vertices"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "Standard combinatorics proves that within a parity class of 3 bit "
        "strings, every pair differs in exactly 2 positions. This maps to "
        "Euclidean distance 2*sqrt(2) in the (+/- 1) cube, confirming all "
        "six edges of each inscribed tetrahedron are equal. The observation "
        "that single bit errors always cross chambers is noted as a structural "
        "property, not a derivation. This extends the existing binary encoding "
        "tests by proving the partition produces genuine regular tetrahedra, "
        "not merely arbitrary groups of 4 vertices."
    )

    # Audit scoring
    audit_score = 88
    audit_notes = (
        "Question: 12/15 (asks a clear why question with specific numbers, but partially answers itself in the framing, reducing mystery tension; the second sentence gives away the punchline before the reader can wonder). Derivation: 14/15 (excellent intuition first structure, the parity constraint insight is the right scaffolding before math, the equation step flows naturally; minor note that the inter tetrahedral observation at the end slightly dilutes the main thread). Commentary: 12/15 (delivers the key insight that partition produces genuine regular tetrahedra, correctly labels the observation, but lacks an analogy for accessibility and does not state broader implications for the GFM program beyond extending existing tests). Model: 9/10 (clean summary with 4 well chosen quantities, the variance metric is a smart way to encode regularity as a single number; edge length and pair counts are interpretable at a glance). Observations: 8/10 (values are mathematically exact and traceable to combinatorial counting and coordinate geometry, Coxeter citation is appropriate, but the 12 and 16 counts could benefit from a brief note showing C(4,2)*2 and 4*4 derivations in the reference field). Constants: 8/10 (K, TET_A, TET_B properly imported from common; however K is imported but never used in the computation, and the literal 3 for spatial dimensions appears without comment, though this is acceptable per project convention). Accessibility: 14/15 (builds from binary labels to Hamming distance to Euclidean distance in a clear progression, explains Hamming distance when first introduced, an undergraduate with basic combinatorics can follow; the only gap is that face diagonal versus edge versus space diagonal distinction could use one more clarifying sentence). Header: 9/10 (comprehensive module docstring covering what is tested, why it matters, the GFM observation, and epistemic status; includes the key physical claim and references; could add an explicit target audience line and a note on relationship to the existing binary encoding test file)."
    )

    academic_paper = """\
TITLE Hamming Distance Uniformity as Proof of Geometric Regularity in the Dual Tetrahedral Partition ABSTRACT We investigate whether the parity partition of a cube's 8 vertices into two groups of 4 produces geometrically regular tetrahedra. By computing all pairwise Hamming distances within and between parity classes, the model confirms uniform intra class distance of 2 and uniform Euclidean edge length of 2.828427, with zero variance. This is a mathematical verification, not a GFM derivation. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The Gravity Field Model posits that gravity's internal structure is a stellated octahedron: two interpenetrating tetrahedra whose 8 vertices coincide with the corners of a cube. Previous tests in the binary encoding suite established that popcount parity partitions these 8 vertices into two groups of 4, and that complementary pairs (connected by XOR with 7) always cross between groups. However, a crucial gap remained. Partitioning 8 vertices into two sets of 4 does not automatically produce two regular tetrahedra. There are 35 ways to choose 4 vertices from 8, and most selections yield irregular shapes. The geometric claim requires that all six edges within each group have equal length. Standard combinatorial geometry (Coxeter 1973) establishes that a cube admits exactly two inscribed regular tetrahedra, and these correspond to the two parity classes. The mechanism is Hamming distance: within a parity class of 3 bit binary strings, every distinct pair must differ in exactly 2 bit positions, because single bit flips change parity. This test verifies that claim exhaustively and computes the resulting Euclidean edge lengths. 2. METHODOLOGY The model enumerates all C(4,2) = 6 vertex pairs within Tet A = {1, 2, 4, 7} and all 6 pairs within Tet B = {0, 3, 5, 6}, computing the Hamming distance H(a, b) = popcount(a XOR b) for each. It counts how many pairs achieve H = 2. Separately, it enumerates all 4 times 4 = 16 inter tetrahedral pairs and counts those with odd Hamming distance. For geometric confirmation, it converts each vertex index to (+/- 1, +/- 1, +/- 1) coordinates and computes Euclidean distances, reporting the mean edge length and the population variance. Agreement criterion: exact match (0.00% error) against combinatorial predictions. 3. RESULTS The model calculates 12 intra tetrahedral pairs at Hamming distance 2, matching the expected value of 12.0 exactly (0.00% error). This accounts for all 6 pairs in Tet A plus all 6 pairs in Tet B, with no exceptions. The model calculates 16 inter tetrahedral pairs with odd Hamming distance, matching the expected 16.0 exactly (0.00% error). This covers all possible cross chamber pairs. The mean Euclidean edge length within each tetrahedron is 2.828427, matching the theoretical value 2*sqrt(2) = 2.828427 exactly (0.00% error). The edge length variance is 0, matching the expected 0.0 exactly. Zero variance is the definitive signature of geometric regularity: every edge in both tetrahedra has identical length. 4. DISCUSSION The results establish, through exhaustive enumeration rather than sampling, that the parity partition produces two geometrically regular tetrahedra. The underlying reason is a theorem of binary arithmetic: in d = 3 bit strings, same parity implies even Hamming distance, and the only nonzero even distance available is 2. This forces uniform edge length. EPISTEMIC STATUS: MATHEMATICAL VERIFICATION. The regularity of inscribed tetrahedra is a known result in combinatorial geometry. We verify it computationally within the GFM vertex labeling scheme. We observe that the inter tetrahedral structure is equally constrained: all 16 cross chamber pairs have odd Hamming distance (1 or 3), meaning any single bit perturbation to a vertex label necessarily crosses chambers. This mirrors the implicit channel property of the GFM traversal, where complement 7 minus V always references the opposite tetrahedron. This correspondence is noted as an OBSERVATION. 5. LIMITATIONS AND HONESTY STATEMENT This test does not derive any physical law. It verifies a combinatorial property that was already known (Coxeter 1973). The connection between Hamming distance structure and error detection in field closure is an observation, not a proven causal link. The result is specific to d = 3 dimensions and does not generalize automatically to higher dimensional analogs. 6. CONCLUSION We confirm that the parity partition of the cube produces two regular tetrahedra with zero edge length
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD COMBINATORICS: Label cube vertices 0 through 7 "
                "using 3 bit binary strings. Tet A = {1, 2, 4, 7} (odd "
                "popcount), Tet B = {0, 3, 5, 6} (even popcount)."
            )
            .step(
                "Hamming distance H(a, b) counts the number of bit positions "
                "where a and b differ. For 3 bit strings, H ranges from 0 to 3."
            )
            .step(
                "KEY CONSTRAINT: Flipping one bit changes popcount parity. "
                "Therefore two vertices of the same parity must differ by an "
                "even number of bits: H = 0 (same vertex) or H = 2."
            )
            .step(
                "For distinct vertices in the same tetrahedron, H = 2 is "
                "the only option. Each pair differs in exactly 2 of 3 bit "
                "positions."
            )
            .equation(
                "Euclidean distance = sqrt(sum of (2)^2 per differing bit) "
                "= sqrt(4 + 4) = sqrt(8) = 2*sqrt(2)"
            )
            .step(
                "Verify: C(4, 2) = 6 pairs per tetrahedron. All 6 must "
                "have Hamming distance 2. Total across both tetrahedra: 12 "
                "pairs, all at Hamming distance 2."
            )
            .step(
                "GFM OBSERVATION: Between tetrahedra (opposite parity), "
                "Hamming distances are 1 or 3 (always odd). A single bit "
                "error on any vertex label necessarily crosses chambers. "
                "This mirrors the implicit channel property where complement "
                "7 XOR V always lands in the opposite tetrahedron."
            )
            .conclude(
                "All 12 intra tetrahedral pairs have Hamming distance exactly "
                "2, proving both inscribed tetrahedra are geometrically regular. "
                "All 16 inter tetrahedral pairs have odd Hamming distance (1 or 3), "
                "confirming chamber crossing under any single bit perturbation."
            )
        )

    def model(self) -> Model:
        def hamming(a, b):
            return bin(a ^ b).count('1')

        # Count intra-tetrahedral pairs at Hamming distance 2
        intra_hd2 = 0
        for i, va in enumerate(TET_A):
            for vb in list(TET_A)[i + 1:]:
                if hamming(va, vb) == 2:
                    intra_hd2 += 1
        for i, va in enumerate(TET_B):
            for vb in list(TET_B)[i + 1:]:
                if hamming(va, vb) == 2:
                    intra_hd2 += 1

        # Count inter-tetrahedral pairs with odd Hamming distance
        inter_odd = 0
        for va in TET_A:
            for vb in TET_B:
                h = hamming(va, vb)
                if h % 2 == 1:
                    inter_odd += 1

        # Compute uniform edge length within each tetrahedron
        # Vertices in +/-1 coordinates: bit k -> +1 if set, -1 if not
        def coords(v):
            return [1.0 if (v >> bit) & 1 else -1.0 for bit in range(3)]

        edge_lengths = []
        for tet in [TET_A, TET_B]:
            tet_list = list(tet)
            for i in range(len(tet_list)):
                for j in range(i + 1, len(tet_list)):
                    c1 = coords(tet_list[i])
                    c2 = coords(tet_list[j])
                    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
                    edge_lengths.append(dist)

        # Edge length variance (0 means perfectly regular)
        mean_len = sum(edge_lengths) / len(edge_lengths)
        variance = sum((el - mean_len) ** 2 for el in edge_lengths) / len(edge_lengths)

        return (
            Model()
            .add("Intra tetrahedral pairs at Hamming distance 2", float(intra_hd2))
            .add("Inter tetrahedral pairs with odd Hamming distance", float(inter_odd))
            .add("Edge length within tetrahedron", mean_len)
            .add("Edge length variance", variance)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Intra tetrahedral pairs at Hamming distance 2", 12.0)
            .add("Inter tetrahedral pairs with odd Hamming distance", 16.0)
            .add("Edge length within tetrahedron", 2.0 * math.sqrt(2.0))
            .add("Edge length variance", 0.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Hamming Distance Structure of Dual Tetrahedra",
        summary="Validates that uniform Hamming distance 2 within each parity class produces geometrically regular tetrahedra",
        test_classes=[HammingDistanceWithinTetrahedra],
    )
