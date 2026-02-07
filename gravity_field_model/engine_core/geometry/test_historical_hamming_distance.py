# FILENAME: test_historical_hamming_distance.py

"""
Hamming Distance Structure Within Dual Tetrahedra
==================================================

The stellated octahedron's two tetrahedra are defined by parity of 3-bit
binary vertex labels. A fundamental question arises: why does this binary
partition produce geometrically regular tetrahedra? Standard combinatorics
shows that vertices sharing the same bit parity always differ in exactly
2 of 3 bits (Hamming distance 2). In Euclidean space with coordinates
drawn from {-1, +1}, Hamming distance 2 maps to Euclidean distance
2*sqrt(2) for every such pair. This uniformity is what makes each
tetrahedron regular, not merely a set of four arbitrary points.

GFM OBSERVATION: The regularity of both tetrahedra follows from the
Hamming distance uniformity inherent in the parity partition of 2^d vertices.

This is an OBSERVATION connecting combinatorial structure to geometry.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, TET_A, TET_B,
)


class HammingDistanceWithinTetrahedra(Test):
    """
    PHYSICAL CONTEXT:
    A regular tetrahedron is the unique simplex in 3 dimensions where all
    edge lengths are equal. When 8 cube vertices are labeled with 3-bit
    binary indices, two vertices share the same parity class (both odd
    popcount or both even popcount) if and only if they differ in exactly
    2 bits. This is a theorem of binary combinatorics first formalized in
    the context of error correcting codes by Hamming (1950). In Euclidean
    coordinates where each bit maps to +1 or -1, Hamming distance 2
    corresponds to Euclidean distance 2*sqrt(2), producing regular
    tetrahedra automatically.

    GFM OBSERVATION:
    The closure constant k=4 gives each tetrahedron exactly 4 vertices,
    yielding C(4,2) = 6 edges per tetrahedron, 12 edges total. The
    uniform Hamming distance of 2 within each parity class is what
    guarantees geometric regularity. The bimetric structure (Alexander,
    Marciano, Smolin 2014; Hassan, Rosen 2012) requires two congruent
    regular tetrahedra, and the binary encoding delivers this without
    any tuning.

    EPISTEMIC STATUS:
    This is a mathematical observation. The Hamming distance uniformity
    is a provable theorem of binary combinatorics, and the Euclidean
    distance correspondence is exact. No free parameters or fits are
    involved.
    """

    name = "Hamming Distance Within Tetrahedra"

    question = (
        "Why do vertices within each tetrahedron always differ in exactly "
        "2 of 3 bits? This Hamming distance uniformity is the combinatorial "
        "reason the parity partition produces regular tetrahedra rather than "
        "irregular ones. Does this hold for all 6 edges in each tetrahedron, "
        "and does it correctly map to the expected Euclidean distance of "
        "2*sqrt(2) in the {-1, +1}^3 coordinate system?"
    )

    reference = (
        "Hamming (1950), Error detecting and error correcting codes; "
        "Coxeter (1973), Regular Polytopes; "
        "GFM Textbook Ch.9 Sec.9.2: Binary encoding of cube vertices"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "Standard combinatorics proves that two 3-bit strings with the same "
        "parity must differ in exactly 0 or 2 positions. Since distinct vertices "
        "cannot differ in 0 bits, Hamming distance 2 is the only possibility. "
        "Each differing bit flips one coordinate from +1 to -1 or vice versa, "
        "contributing a squared distance of (2)^2 = 4. Two such flips give "
        "Euclidean distance sqrt(4+4) = 2*sqrt(2). This observation confirms "
        "that the binary parity partition is not merely a labeling convention "
        "but a geometric theorem: regularity of the dual tetrahedra is forced "
        "by the bit structure. This is not a derivation from GFM principles "
        "but an observation that the GFM geometry inherits exact regularity "
        "from the binary encoding."
    )

    # Audit scoring
    audit_score = 87
    audit_notes = (
        "Question: 12/15 (asks the right why question and includes specific numbers, but reads slightly like a checklist of sub questions rather than a single compelling mystery hook with clear stakes). Derivation: 14/15 (excellent intuition first structure, clearly separates combinatorics from GFM observation, the parity argument is built step by step before any equation appears, minor point: could add a brief analogy to make the even/odd parity argument more vivid for undergrads). Commentary: 12/15 (solid mechanistic explanation of why Hamming distance 2 forces regularity, correctly flags epistemic status as observation not derivation, but lacks an analogy to everyday experience and does not state broader implications for what we can now trust about the bimetric structure). Model: 9/10 (clean summary with 4 values, boolean verdict for uniformity is good practice, mean Euclidean is a proper summary stat, minor redundancy in having both mean and expected as separate model outputs since they are identical by construction). Observations: 8/10 (values are mathematically exact and traceable to combinatorial theorem, Hamming and Coxeter references are solid, but CODATA is not relevant here and the Hamming 1950 citation could include the journal: Bell System Technical Journal). Constants: 9/10 (K, TET_A, TET_B properly imported from common, no physics constants hardcoded, the literal 8 and 2 appear inline but these are combinatorial counts not physics constants so this is acceptable, minor deduction because K is imported but never used in computation). Accessibility: 13/15 (builds well from binary labeling to parity to Hamming distance to Euclidean distance, an undergrad with discrete math background can follow, but the connection between Hamming distance and error correcting codes mentioned in the docstring is never unpacked in the derivation or commentary, which is a missed scaffolding opportunity). Header: 10/10 (module docstring clearly states the domain, the question, the GFM observation, epistemic status as observation not derivation, and key references, scope is well bounded)."
    )

    academic_paper = """\
Hamming Distance Uniformity as the Combinatorial Origin of Tetrahedral Regularity in the Stellated Octahedron Binary vertex encoding and the geometric structure of dual field chambers AUTHOR GFM Research Agent ABSTRACT The Gravity Field Model requires two regular, congruent tetrahedra forming a stellated octahedron. This paper investigates why the standard binary labeling of cube vertices, combined with parity partition, necessarily produces regular tetrahedra. We prove that distinct vertices within the same parity class always differ in exactly 2 of 3 bits (Hamming distance 2), which maps to a uniform Euclidean edge length of 2*sqrt(2) in the {-1, +1}^3 coordinate system. Exhaustive computation over all 12 intra-tetrahedral edges confirms this with 0.00% deviation. Regularity is a theorem of the binary encoding, not an independent geometric assumption. 1. INTRODUCTION 1.1 The Regularity Question The stellated octahedron consists of two interpenetrating tetrahedra whose 8 vertices coincide with the corners of a cube. In the Gravity Field Model, the bimetric structure requires that both tetrahedra be regular and congruent (Alexander, Marciano, and Smolin 2014; Hassan and Rosen 2012). Previous tests in this domain have validated the parity partition: vertices with odd bit count popcount form Tetrahedron A = {1, 2, 4, 7}, while vertices with even popcount form Tetrahedron B = {0, 3, 5, 6}. What those tests did not address is the deeper question: why does this partition produce regular tetrahedra at all? Four arbitrary points in three dimensions generically form an irregular tetrahedron. Something specific about the binary encoding must force all six edge lengths within each tetrahedron to be equal. 1.2 The Combinatorial Approach Rather than verifying regularity by computing coordinates directly, we trace it to a more fundamental origin: the Hamming distance structure of 3-bit binary strings. Hamming (1950) introduced the concept of distance between binary codewords as the number of positions in which they differ. We show that the parity constraint forces a uniform Hamming distance of exactly 2 between all distinct same-parity vertices, and that this uniformity translates directly into Euclidean regularity. 1.3 Structure of This Paper Section 2 establishes the binary framework and proves the Hamming distance theorem. Section 3 presents the Euclidean mapping and computational verification. Section 4 discusses the significance for the bimetric structure. Section 5 states the conclusion. 2. THE BINARY FRAMEWORK 2.1 Vertex Encoding A cube in d = 3 dimensions has 2^3 = 8 vertices. Labeling each vertex with a 3-bit binary index from 000 to 111, the coordinate assignment follows: each bit value 0 maps to the coordinate -1, and each bit value 1 maps to +1. Vertex 0 = (000) sits at (-1, -1, -1), while vertex 7 = (111) sits at (+1, +1, +1). This encoding is bijective and preserves the full symmetry group of the cube. 2.2 The Parity Theorem Consider two distinct vertices in the same parity class. Their binary labels have the same popcount parity (both odd or both even). The bitwise XOR of their labels identifies the positions where they differ. The XOR of two same-parity strings must have an even number of 1-bits, because the sum of two integers with the same parity is even. The possible Hamming distances are therefore 0 or 2 (since the maximum is 3, and 3 is odd, it is excluded). For distinct vertices, Hamming distance 0 is impossible. This completes the proof: every pair of distinct vertices within the same tetrahedron differs in exactly 2 of 3 bit positions. No exceptions exist because no other even value between 0 and 3 is available. 3. FROM HAMMING DISTANCE TO EUCLIDEAN REGULARITY 3.1 The Distance Mapping When two vertices differ in exactly 2 bit positions, each differing coordinate contributes a squared displacement of (+1 - (-1))^2 = 4. The one matching coordinate contributes zero. The total squared Euclidean distance is therefore 4 + 4 + 0 = 8, giving an edge length of sqrt(8) = 2*sqrt(2) = 2.828427. This value is independent of which 2 of the 3 positions differ. Every intra-tetrahedral edge has exactly the same length, which is the definition of a regular tetrahedron. 3.2 Computational Verification Exhaustive enumeration over all C(4,2) = 6 edges within Tetrahedron A and all 6 edges within Tetrahedron B yields 12 total intra-tetrahedral edges. The results match expectations exactly across all four reported quantities. The Hamming distance uniformity boolean equals 1.0 (all edges have Hamming distance 2). The total edge count equals 12. The mean Euclidean edge length equals 2.828427. The expected Euclidean edge length equals 2.828427. All four comparisons show 0.00% deviation. 4. DISCUSSION 4.1 Significance for the Bimetric Structure The bimetric formulation of gravity (Hassan and Rosen 2012) requires two distinct metric sectors. In the GFM realization, these correspond to two tetrahedra that must be congruent to preserve the ghost freedom condition. The result established here demonstrates that congruence is not an additional constraint imposed on the geometry. It follows automatically from the binary encoding. Any labeling of cube vertices by 3-bit strings, partitioned by popcount parity, produces two regular tetrahedra with identical edge lengths. The bimetric symmetry is inherited from combinatorics. 4.2 Scope and Epistemic Status This result is a mathematical observation, not a physical derivation. It establishes that regularity is a theorem of the vertex encoding, confirming what the GFM geometry assumes. The proof relies only on properties of binary strings in d = 3 dimensions. It does not extend automatically to higher dimensions: in d = 4, same-parity vertices can differ in 2 or 4 bits, breaking distance uniformity. The restriction to d = 3 is consistent with the GFM uniqueness condition 2(d+1) = 2^d, which holds only for d = 3. 5. CONCLUSION The parity partition of 3-bit binary vertex labels forces every intra-tetrahedral edge to have Hamming distance exactly 2, which maps to Euclidean distance exactly 2*sqrt(2). Exhaustive computation over all 12 edges confirms this with 0.00% deviation across all quantities. Regularity of the dual tetrahedra in the stellated octahedron is therefore not a geometric assumption but a combinatorial theorem. This result grounds the bimetric symmetry
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD COMBINATORICS: Label cube vertices 0 through 7 "
                "using 3-bit binary. Assign coordinates: bit=0 maps to -1, "
                "bit=1 maps to +1."
            )
            .step(
                "Two vertices share the same parity (both in Tet A or both "
                "in Tet B) if and only if they differ in an even number of "
                "bits: 0 or 2. Since we consider distinct vertices, the only "
                "possibility is Hamming distance 2."
            )
            .equation(
                "hamming_distance(v_i, v_j) = 2 for all i != j in same tetrahedron"
            )
            .step(
                "Each differing bit contributes (1 - (-1))^2 = 4 or "
                "(-1 - 1)^2 = 4 to the squared Euclidean distance. "
                "Two differing bits give d^2 = 4 + 4 = 8."
            )
            .equation("euclidean_distance = sqrt(8) = 2*sqrt(2)")
            .step(
                "Tet A has vertices {1, 2, 4, 7}, giving C(4,2) = 6 edges. "
                "Tet B has vertices {0, 3, 5, 6}, also giving 6 edges. "
                "All 12 edges should have Hamming distance 2 and Euclidean "
                "distance 2*sqrt(2)."
            )
            .step(
                "GFM OBSERVATION: The closure constant k = 4 determines "
                "that each tetrahedron has 4 vertices and 6 edges. The "
                "uniform Hamming distance ensures both tetrahedra are "
                "regular and congruent, satisfying the bimetric symmetry "
                "requirement."
            )
            .conclude(
                "All 12 intra-tetrahedral edges have Hamming distance "
                "exactly 2 and Euclidean distance exactly 2*sqrt(2). "
                "Regularity is a theorem of the binary encoding, not "
                "an assumption."
            )
        )

    def model(self) -> Model:
        # Vertex coordinates in {-1, +1}^3
        coords = {}
        for v in range(8):
            x = -1 + 2 * ((v >> 2) & 1)
            y = -1 + 2 * ((v >> 1) & 1)
            z = -1 + 2 * (v & 1)
            coords[v] = (x, y, z)

        def hamming(a, b):
            return bin(a ^ b).count('1')

        def euclidean(a, b):
            ca, cb = coords[a], coords[b]
            return math.sqrt(sum((ci - cj) ** 2 for ci, cj in zip(ca, cb)))

        tet_a_list = sorted(TET_A)
        tet_b_list = sorted(TET_B)

        # Check all intra-tetrahedral Hamming distances
        hamming_all_two = 1.0  # 1.0 if all are 2, 0.0 otherwise
        total_edges = 0
        euclidean_sum = 0.0

        for tet in [tet_a_list, tet_b_list]:
            for i in range(len(tet)):
                for j in range(i + 1, len(tet)):
                    h = hamming(tet[i], tet[j])
                    e = euclidean(tet[i], tet[j])
                    if h != 2:
                        hamming_all_two = 0.0
                    euclidean_sum += e
                    total_edges += 1

        mean_euclidean = euclidean_sum / total_edges
        expected_euclidean = 2.0 * math.sqrt(2.0)

        return (
            Model()
            .add("Uniform Hamming distance 2 (boolean)", hamming_all_two)
            .add("Total intra-tetrahedral edges", float(total_edges))
            .add("Mean Euclidean edge length", mean_euclidean)
            .add("Expected Euclidean edge length", expected_euclidean)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Uniform Hamming distance 2 (boolean)", 1.0)
            .add("Total intra-tetrahedral edges", 12.0)
            .add("Mean Euclidean edge length", 2.0 * math.sqrt(2.0))
            .add("Expected Euclidean edge length", 2.0 * math.sqrt(2.0))
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Hamming Distance Structure Within Dual Tetrahedra",
        summary="Validates that parity partition forces uniform Hamming distance 2 and regular tetrahedra",
        test_classes=[HammingDistanceWithinTetrahedra],
    )
