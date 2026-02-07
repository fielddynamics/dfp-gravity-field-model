# FILENAME: test_edge_count_and_merkaba_structure.py

"""
Edge Count and Merkaba Structure of the Stellated Octahedron
============================================================

The stellated octahedron (Merkaba) consists of two interpenetrating regular
tetrahedra. Each regular tetrahedron has C(4,2) = 6 edges, giving 12 edges
total for the dual structure. This edge count is a theorem of combinatorial
geometry: any complete graph on 4 vertices (K4) has exactly 6 edges, and
two disjoint K4 graphs on 8 vertices produce 12 edges total.

The number 13 = 12 + 1 appears in the GFM formula for G as the denominator:
G = (17/13) * alpha^21 * (hbar*c/m_e^2), where 13 = kd + 1 = 4*3 + 1.
Standard graph theory gives the edge count. GFM notes that adding the
Field Origin (the geometric center where all body diagonals intersect)
to the 12 edges produces the constant 13 that appears in the coupling
denominator.

GFM OBSERVATION: 12 edges + 1 center = 13 = kd + 1 (Merkaba edge structure).

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B,
)


class MerkabaEdgeStructure(Test):
    """
    Validates the edge count of the stellated octahedron and its connection
    to the GFM constant kd + 1 = 13.

    PHYSICAL CONTEXT:
    A regular tetrahedron is the simplest 3D simplex, with 4 vertices and
    C(4,2) = 6 edges. The stellated octahedron comprises two such tetrahedra
    on disjoint vertex sets, giving 6 + 6 = 12 edges total. These edges
    do not intersect at shared vertices (the two tetrahedra share no vertices),
    so no edge is double counted. This is standard combinatorial geometry
    dating to Euler and Coxeter (Regular Polytopes, 1973). Additionally,
    within each tetrahedron all edges must have equal length for regularity,
    which is verified by computing Euclidean distances between vertices
    placed at alternating corners of a cube with coordinates in {-1, +1}^3.
    The edge length is 2*sqrt(2) for a unit cube of half side 1.

    GFM OBSERVATION:
    The total edge count 12 plus the single Field Origin at (0,0,0) gives
    13 = kd + 1, where k = 4 and d = 3. This constant 13 appears as the
    denominator in the G formula: 13 = 12 spatial couplings + 1 structural
    base (the Field Origin). The numerator 17 = k^2 + 1 counts coupling
    channels. The ratio 17/13 encodes the topology of bimetric gravity.

    EPISTEMIC STATUS:
    The edge count (6 per tetrahedron, 12 total) is a mathematical theorem.
    The identification of 12 + 1 = 13 = kd + 1 as physically meaningful is
    an observation noted within the GFM framework.
    """

    name = "Merkaba Edge Structure"

    question = (
        "Why does the stellated octahedron have exactly 12 edges, and why does "
        "adding the Field Origin produce 13 = kd + 1? Each tetrahedron is a "
        "complete graph K4 with C(4,2) = 6 edges. Two disjoint tetrahedra give "
        "12. The question is whether this count has physical significance beyond "
        "combinatorics, given that 13 appears in the denominator of the G formula."
    )

    reference = (
        "Coxeter, Regular Polytopes (1973), Ch. 1: simplex edge counts. "
        "GFM Textbook Ch.9 Sec.9.4: Merkaba edge structure and kd+1 constant. "
        "Paper VII Sec.4.1: G = (17/13) * alpha^21 * (hbar*c/m_e^2)."
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "Standard combinatorial geometry dictates that a tetrahedron (K4 graph) "
        "has exactly 6 edges, so two disjoint tetrahedra have 12. This is a "
        "theorem, not an empirical finding. The regularity of each tetrahedron "
        "is confirmed by verifying all six edge lengths are equal (2*sqrt(2) in "
        "the unit cube embedding). GFM notes as an observation that 12 + 1 = 13 "
        "matches kd + 1, the denominator in the gravitational constant formula. "
        "This is not a derivation of why 13 appears in G; it is a documentation "
        "of the structural correspondence between edge count and coupling constant."
    )

    # Audit scoring
    audit_score = 86
    audit_notes = (
        "Question: 13/15 (asks why and includes specific numbers, but the mystery hook could be sharper; it reads slightly like a statement of facts rather than a tension to resolve. Could frame the surprise more: why should a combinatorial accident match a gravitational coupling constant?). Derivation: 14/15 (excellent intuition before math, the regularity check builds naturally, and the key insight connecting 2*C(k,2) = kd to the simplex condition k = d+1 is genuinely illuminating; minor issue: the 'sqrt(4)*sqrt(2)...' phrasing in the regularity step is slightly clumsy before self correcting). Commentary: 12/15 (clearly states what is a theorem vs an observation, and the epistemic honesty is strong; however it mostly restates the derivation findings rather than delivering a deeper aha moment or analogy; no everyday analogy offered, no implications for what we can now trust or explore next). Model: 9/10 (clean summary with 6 well chosen values; the regularity binary verdict is good practice; edge length is a nice addition beyond just counts). Observations: 8/10 (all values are mathematically exact and therefore perfectly traceable, but the observations section itself does not cite where 13 = kd+1 comes from beyond the module header; Coxeter is cited in reference but not inline with the observed values). Constants: 9/10 (K, TET_A, TET_B, VERTICES all imported from common; d = 3 is used as a literal which is correct per rules; math.sqrt is standard library; minor note: VERTICES is imported but never used in the code). Accessibility: 13/15 (builds well from simple combinatorics to the deeper simplex identity; an undergrad with graph theory background can follow; the Hamming distance argument about same parity vertices differing in exactly 2 bits is elegant but stated without proof, which could lose some readers; no analogy to ground the abstract geometry). Header: 8/10 (module docstring covers domain, key claim, epistemic status, and references; missing explicit target audience level and does not mention scope boundaries or what the test does NOT claim)."
    )

    academic_paper = """\
TITLE Edge Count and Regularity of the Stellated Octahedron: Validating the kd+1 = 13 Structural Constant ABSTRACT This investigation validates the edge count of the stellated octahedron (Merkaba) and examines its connection to the GFM constant 13 = kd + 1. The model computes 6 edges per tetrahedron, 12 total, all of equal length, confirming regularity. The correspondence 12 + 1 = 13 is documented as an OBSERVATION. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The gravitational constant G in the GFM framework is expressed as G = (17/13) * alpha^21 * (hbar*c/m_e^2). The denominator 13 is identified with kd + 1, where k = 4 is the closure constant and d = 3 is the number of spatial dimensions. But where does the number 12 come from geometrically, and why does adding 1 produce a physically meaningful constant? Standard combinatorial geometry provides a clear answer for the edge count. A tetrahedron is the complete graph K4 on 4 vertices. The number of edges in any complete graph K_n is C(n,2) = n(n-1)/2. For n = 4 this gives 6. The stellated octahedron consists of two tetrahedra on disjoint vertex sets, so the total edge count is 12. This is a theorem, not an empirical observation. GFM notes that 12 edges plus 1 Field Origin (the geometric center at coordinates (0,0,0)) yields 13, matching the denominator of the G formula. This test investigates whether the edge count, the regularity of both tetrahedra, and the algebraic identity connecting edge count to kd are all exactly satisfied. A deeper question emerges from the algebra. The identity 2 * C(k,2) = k(k-1) equals kd only when k-1 = d, which is precisely the simplex condition: a simplex in d dimensions has d+1 vertices. This test verifies that the stellated octahedron satisfies this condition exactly. 2. METHODOLOGY The model assigns coordinates from {-1, +1}^3 to 8 cube vertices using the standard binary encoding (vertex index bits map to coordinate signs). Tet A = {1,2,4,7} and Tet B = {0,3,5,6} are imported from the geometry constants module. For each tetrahedron, all C(4,2) = 6 vertex pairs are enumerated. Euclidean distances are computed between each pair. Edge counts, mean edge length, and maximum deviation from mean length are recorded. Regularity is assessed as a binary verdict: 1.0 if all edges are equal within floating point tolerance (less than 1e-10), 0.0 otherwise. The Merkaba constant is computed as total edges plus 1. The algebraic product K * d is computed independently. Agreement criterion: exact match (tolerance 1%) for all six output quantities. 3. RESULTS Model output: Edges per tetrahedron: 6.0 (observed: 6.0, exact match) Total Merkaba edges: 12.0 (observed: 12.0, exact match) Edge length regularity: 1.0 (observed: 1.0, all edges equal) Edge length: 2.828427 (observed: 2*sqrt(2) = 2.828427, exact match) Merkaba constant kd+1: 13.0 (observed: 13.0, exact match) kd from algebra: 12.0 (observed: 12.0, exact match) All six quantities match exactly. Both tetrahedra are perfectly regular, with uniform edge length 2*sqrt(2). The identity 2*C(k,2) = kd = 12 is confirmed, and it holds because k = d+1 = 4 satisfies the simplex condition. 4. DISCUSSION The edge count is a mathematical certainty, not an empirical finding. What merits attention is the chain of identities: total edges = k(k-1) = kd, which requires k = d+1. This is the simplex condition, the defining property of a tetrahedron in 3 dimensions. The "+1" in kd+1 = 13 corresponds to the Field Origin, the unique center point equidistant from all 8 vertices at distance sqrt(3). EPISTEMIC STATUS: The edge count and regularity are DERIVATIONS from standard geometry. The identification of 12+1 = 13 as the denominator of the G formula is an OBSERVATION within the GFM framework. We do not derive G from edge counting. We observe that the structural constants of the stellated octahedron reproduce the numerical factors that appear in the coupling formula. 5. LIMITATIONS AND HONESTY STATEMENT This test does not derive the gravitational constant. The correspondence between edge count and coupling denominator could be coincidental. The "+1" identification with the Field Origin is an interpretive choice, not a mathematical necessity. Further work should investigate whether the numerator 17 admits a similarly clean geometric decomposition within the same structure.
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: A tetrahedron has 4 vertices. The number "
                "of edges in a complete graph on n vertices is C(n,2) = n(n-1)/2."
            )
            .equation("edges_per_tet = C(4,2) = 4*3/2 = 6")
            .step(
                "The stellated octahedron has two tetrahedra on disjoint vertex "
                "sets (Tet A = {1,2,4,7}, Tet B = {0,3,5,6}). No vertex is shared, "
                "so edges do not overlap."
            )
            .equation("total_edges = 6 + 6 = 12")
            .step(
                "REGULARITY CHECK: Each vertex has coordinates in {-1,+1}^3. "
                "Within Tet A, any two vertices differ in exactly 2 of 3 coordinates "
                "(since they have the same parity, they cannot differ in 1 or 3 bits). "
                "The Euclidean distance is sqrt(4) * sqrt(2) ... more precisely, "
                "each differing coordinate contributes (1 - (-1))^2 = 4 or "
                "(-1 - 1)^2 = 4. Two coordinates differ, so d^2 = 4 + 4 = 8, "
                "d = 2*sqrt(2)."
            )
            .equation("edge_length = 2*sqrt(2) for all edges in both tetrahedra")
            .step(
                "GFM OBSERVATION: The Field Origin at (0,0,0) is equidistant "
                "from all 8 vertices at distance sqrt(3). Adding this single "
                "center point to the 12 edges gives the structural count "
                "12 + 1 = 13."
            )
            .equation("kd + 1 = 4*3 + 1 = 13")
            .step(
                "The algebraic identity kd = k * d = (vertices per tet) * "
                "(spatial dimensions) = 4 * 3 = 12 equals the edge count. "
                "This holds because C(k,2) = k(k-1)/2 edges per tetrahedron, "
                "times 2 tetrahedra, gives k(k-1) = 12 when k = 4. "
                "Equivalently, k(k-1) = kd requires k-1 = d, which is exactly "
                "the simplex condition: a tetrahedron in d dimensions has d+1 = k "
                "vertices."
            )
            .conclude(
                "Each tetrahedron contributes 6 edges (all equal length 2*sqrt(2)), "
                "totaling 12 for the Merkaba. The identity 2*C(k,2) = k(k-1) = kd "
                "holds precisely because k = d+1 (the simplex condition). Adding "
                "the Field Origin gives 13 = kd + 1."
            )
        )

    def model(self) -> Model:
        d = 3

        # Vertex coordinates: V_i has coordinates (-1)^bit for each bit
        def coords(v):
            x = -1.0 + 2.0 * ((v >> 2) & 1)
            y = -1.0 + 2.0 * ((v >> 1) & 1)
            z = -1.0 + 2.0 * (v & 1)
            return (x, y, z)

        def distance(v1, v2):
            c1, c2 = coords(v1), coords(v2)
            return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

        # Count edges and check regularity for Tet A
        tet_a_list = sorted(TET_A)
        edges_a = 0
        lengths_a = []
        for i in range(len(tet_a_list)):
            for j in range(i + 1, len(tet_a_list)):
                edges_a += 1
                lengths_a.append(distance(tet_a_list[i], tet_a_list[j]))

        # Count edges and check regularity for Tet B
        tet_b_list = sorted(TET_B)
        edges_b = 0
        lengths_b = []
        for i in range(len(tet_b_list)):
            for j in range(i + 1, len(tet_b_list)):
                edges_b += 1
                lengths_b.append(distance(tet_b_list[i], tet_b_list[j]))

        total_edges = edges_a + edges_b

        # Check all edges have equal length (regularity)
        all_lengths = lengths_a + lengths_b
        mean_length = sum(all_lengths) / len(all_lengths)
        max_deviation = max(abs(el - mean_length) for el in all_lengths)

        # Regularity: 1.0 if all edges equal, 0.0 otherwise
        regular = 1.0 if max_deviation < 1e-10 else 0.0

        # Merkaba constant: edges + Field Origin
        merkaba_constant = total_edges + 1

        # Algebraic identity: kd = k*(k-1) for k = d+1
        kd_value = K * d

        # Expected edge length
        edge_length = 2.0 * math.sqrt(2.0)

        return (
            Model()
            .add("Edges per tetrahedron", float(edges_a))
            .add("Total Merkaba edges", float(total_edges))
            .add("Edge length regularity", regular)
            .add("Edge length", mean_length)
            .add("Merkaba constant kd+1", float(merkaba_constant))
            .add("kd from algebra", float(kd_value))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Edges per tetrahedron", 6.0)
            .add("Total Merkaba edges", 12.0)
            .add("Edge length regularity", 1.0)
            .add("Edge length", 2.0 * math.sqrt(2.0))
            .add("Merkaba constant kd+1", 13.0)
            .add("kd from algebra", 12.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Merkaba Edge Structure and the kd+1 Constant",
        summary="Validates edge count, regularity, and 12+1=13 structure of the stellated octahedron",
        test_classes=[MerkabaEdgeStructure],
    )
