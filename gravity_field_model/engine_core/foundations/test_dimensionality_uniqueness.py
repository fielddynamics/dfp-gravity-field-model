"""
Dimensionality Uniqueness: 2(d+1) = 2^d Only for d = 3
========================================================

The number of spatial dimensions in our universe is three. This is one of
the most basic facts of physics, yet standard physics treats it as a given
rather than deriving it. String theory requires 9 or 10 spatial dimensions
and must compactify the extras. Loop quantum gravity typically assumes d = 3
from the start. Neither framework explains WHY three dimensions are selected.

In the GFM stellated octahedron geometry, two independent counting rules
apply to the structure: 2(d+1) counts the vertices as two simplices in d
dimensions (each simplex has d+1 vertices), while 2^d counts the vertices
as corners of a d dimensional hypercube. These two expressions are equal
if and only if d = 3, yielding 2(3+1) = 2^3 = 8 vertices. This identity
uniquely selects three spatial dimensions and produces K = d+1 = 4, the
closure constant that underpins the entire GFM framework.

GFM OBSERVATION: The equation 2(d+1) = 2^d has a unique positive integer
solution at d = 3, which gives K = 4 and 8 vertices.

This is a DERIVATION from the requirement that simplex and hypercube
vertex counts must agree, not a fitted or adjusted result.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K,
)


TOTAL_VERTICES = 8


def simplex_count(d):
    """Vertex count from two simplices in d dimensions: 2(d+1)."""
    return 2 * (d + 1)


def hypercube_count(d):
    """Vertex count from d dimensional hypercube: 2^d."""
    return 2 ** d


def find_unique_solution(d_max=20):
    """
    Scan positive integers d = 1 to d_max for solutions of 2(d+1) = 2^d.
    Returns the list of solutions found.
    """
    solutions = []
    for d in range(1, d_max + 1):
        if simplex_count(d) == hypercube_count(d):
            solutions.append(d)
    return solutions


class DimensionalityUniqueness(Test):
    """
    PHYSICAL CONTEXT:
    The dimensionality of space is a foundational parameter in all of physics.
    Ehrenfest (1917) showed that stable planetary orbits require d = 3, and
    Tangherlini (1963) demonstrated that the hydrogen atom has no stable bound
    states for d >= 4. These are consequences of d = 3 but do not derive it
    from a single unifying principle. The question of why space has exactly
    three dimensions remains open in standard physics.

    GFM OBSERVATION:
    The GFM stellated octahedron requires that two independent vertex counting
    methods agree: 2(d+1) from two d simplices (tetrahedra for d = 3) and 2^d
    from the embedding hypercube (cube for d = 3). The equation 2(d+1) = 2^d
    has exactly one positive integer solution: d = 3. This yields K = d+1 = 4,
    the closure constant, and 2^d = 8 = 2K total vertices. Every GFM structure
    constant (K = 4, vertices = 8, faces = 8, K^2+1 = 17, Kd+1 = 13) follows
    from this single identity.

    EPISTEMIC STATUS:
    This is a mathematical derivation. The identity 2(d+1) = 2^d having a
    unique solution at d = 3 is provable by elementary algebra and exhaustive
    search over positive integers. Its physical interpretation as selecting
    spatial dimensionality is a GFM framework claim.
    """

    name = "Dimensionality Uniqueness d = 3"

    question = (
        "Why does the universe have exactly three spatial dimensions? "
        "The GFM stellated octahedron requires two vertex counting methods "
        "to agree: 2(d+1) from paired simplices and 2^d from the embedding "
        "hypercube. For which values of d do these counts match, and is the "
        "solution unique? If d = 3 is the only solution, does it also produce "
        "the correct closure constant K = 4?"
    )

    reference = (
        "Ehrenfest (1917) Proc. Amsterdam Acad. 20 200; "
        "Tangherlini (1963) Nuovo Cimento 27 636; "
        "Coxeter (1973) Regular Polytopes; "
        "GFM Paper VII Section 2.2"
    )

    tolerance = 0.001

    level = Level.CRITICAL

    commentary = (
        "The equation 2(d+1) = 2^d is satisfied only at d = 3 among positive "
        "integers. This is verifiable by direct computation: for d = 1, "
        "2(2) = 4 vs 2^1 = 2; for d = 2, 2(3) = 6 vs 2^2 = 4; for d = 3, "
        "2(4) = 8 = 2^3 = 8; for d = 4, 2(5) = 10 vs 2^4 = 16, and the "
        "exponential 2^d grows strictly faster than the linear 2(d+1) for all "
        "d > 3. The result is a derivation from the requirement that simplex "
        "and hypercube descriptions of the same structure must be compatible. "
        "From d = 3 alone, K = 4, vertices = 8, the bimetric channel count "
        "K^2+1 = 17, the edge structure Kd+1 = 13, and the coupling hierarchy "
        "depth 1+K+K^2 = 21 all follow. This single identity anchors every "
        "structural constant in the GFM framework."
    )

    # Audit scoring
    audit_score = 85
    audit_notes = (
        "Question: 13/15 (opens with the deep WHY of dimensionality, includes specific numbers and stakes, but the second half listing sub questions slightly dilutes the mystery hook). Derivation: 14/15 (excellent scaffolding from polytope facts to GFM requirement to exhaustive check to formal proof to consequences; intuition is strong throughout; minor note: no everyday analogy to ground the abstract math). Commentary: 11/15 (thorough walkthrough of the d=1 through d=4 cases which is valuable, but reads more like a derivation recap than an insight delivery; missing an analogy, missing implications beyond GFM, no aha moment about what it means physically that only d=3 works). Model: 9/10 (clean set of 9 summary values covering the identity, uniqueness, and all derived constants; easy to interpret; could arguably drop one or two redundant items but well within range). Observations: 8/10 (values are mathematically exact and traceable to GFM definitions and Coxeter; K imported from common; TOTAL_VERTICES hardcoded as 8 rather than imported, minor gap). Constants: 8/10 (K properly imported from common; TOTAL_VERTICES defined as module level constant with value 8 rather than imported from geometry_constants; math imported but unused; no physics constants needed so scope is inherently limited). Accessibility: 13/15 (an undergraduate with linear algebra can follow the simplex and hypercube counting; the exhaustive check is pedagogically strong; the formal proof step with derivatives assumes calculus comfort; no everyday analogy like why you can tie knots only in 3D to anchor intuition for non specialists). Header: 9/10 (comprehensive module docstring covering the physical context, the GFM observation, epistemic status as derivation, and the specific identity being tested; clearly states what is and is not claimed; could add a brief target audience line and coverage assessment)."
    )

    academic_paper = """\
TITLE Uniqueness of Three Spatial Dimensions from Simplex Hypercube Vertex Agreement ABSTRACT We investigate whether the equation 2(d+1) = 2^d, requiring simplex and hypercube vertex counts to agree, has a unique positive integer solution. Exhaustive search and analytic proof confirm d = 3 is the sole solution. This is a mathematical DERIVATION that anchors the GFM closure constant K = 4. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The dimensionality of space is among the most fundamental parameters in physics, yet no consensus exists on why d = 3. Ehrenfest (1917) demonstrated that stable planetary orbits require three spatial dimensions. Tangherlini (1963) showed the hydrogen atom has no bound states for d greater than or equal to 4. These results confirm that d = 3 is necessary for the physics we observe, but they are consequences of dimensionality rather than explanations of it. String theory requires 9 or 10 spatial dimensions and must compactify the extras by hand. Loop quantum gravity typically assumes d = 3 as an input. The GFM stellated octahedron is constructed from two interpenetrating tetrahedra embedded in a cube. This structure imposes two independent vertex counting constraints. Each tetrahedron is a d dimensional simplex with d+1 vertices, giving 2(d+1) total. The embedding hypercube contributes 2^d vertex positions. For the structure to close, meaning every hypercube corner is occupied by exactly one simplex vertex, these counts must match: 2(d+1) = 2^d. This test investigates whether that equation has a unique solution among positive integers, and whether that solution produces the GFM closure constant K = 4. 2. METHODOLOGY We evaluate both sides of 2(d+1) = 2^d for every positive integer d from 1 to 20, recording all values where equality holds. We then prove analytically that no solutions exist beyond this range: the exponential 2^d grows strictly faster than the linear 2(d+1) for all d greater than 3, since the derivative of 2^d (which is 2^d times ln 2) exceeds the derivative of 2(d+1) (which is 2) for all d greater than or equal to 2. The search range of d = 1 through 20 is therefore exhaustive. Agreement criterion: exact integer equality. From the solution d, we derive K = d+1 and verify all downstream GFM structural constants. 3. RESULTS Exhaustive search results for 2(d+1) versus 2^d: d = 1: 4 versus 2 (no match). d = 2: 6 versus 4 (no match). d = 3: 8 versus 8 (match). d = 4: 10 versus 16 (no match). d = 5 through 20: exponential dominates, no further matches. Number of solutions found: exactly 1. Unique solution: d = 3. Derived structural constants from d = 3: K = d+1 = 4 (closure constant, matches GFM definition). Total vertices = 2K = 8 (matches stellated octahedron). Coupling channels = K^2+1 = 17 (16 face pairings plus Field Origin). Edge structure = Kd+1 = 13 (12 edges plus center). Hierarchy depth = 1+K+K^2 = 21 (coupling exponent in G derivation). All nine model outputs match their expected values exactly. 4. DISCUSSION The identity 2(d+1) = 2^d having a unique solution at d = 3 is a theorem of elementary number theory, not an approximation or a fit. Its physical significance within GFM is that it provides a single principle from which every structural constant in the framework derives. The closure constant K = 4 is not assumed; it follows from d = 3. The numbers 8, 17, 13, and 21 that appear throughout the GFM derivations of G, electron spin, and the coupling hierarchy all trace back to this one equation. EPISTEMIC STATUS: DERIVATION. The mathematical uniqueness is proven. The interpretive claim that this equation selects the dimensionality of physical space is a GFM framework assertion, not a theorem of standard physics. This test connects to every other GFM result: the G derivation uses 17, 13, and 21; the spin derivation uses the 8 vertex structure; the bimetric architecture requires two tetrahedra with 2K = 8 vertices. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove that 2(d+1) = 2^d is the reason our universe has three dimensions. The requirement that simplex and hypercube vertex counts must agree is a GFM postulate, not an established physical law. Other frameworks
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD PHYSICS: In d spatial dimensions, a simplex has d+1 "
                "vertices. A hypercube has 2^d vertices. These are independent "
                "geometric facts from polytope theory (Coxeter 1973)."
            )
            .step(
                "GFM STRUCTURE: The stellated octahedron consists of two "
                "interpenetrating tetrahedra (simplices) embedded in a cube "
                "(hypercube). The vertex count must be consistent: the two "
                "simplices contribute 2(d+1) vertices, and the hypercube "
                "provides 2^d vertex positions."
            )
            .step(
                "REQUIREMENT: For the structure to close, every hypercube "
                "vertex must be occupied by exactly one simplex vertex and "
                "vice versa. This demands 2(d+1) = 2^d."
            )
            .equation("2(d+1) = 2^d")
            .step(
                "EXHAUSTIVE CHECK: d=1: 4 vs 2 (no). d=2: 6 vs 4 (no). "
                "d=3: 8 vs 8 (YES). d=4: 10 vs 16 (no). For d > 3, "
                "2^d grows exponentially while 2(d+1) grows linearly, so "
                "no further solutions exist."
            )
            .step(
                "FORMAL PROOF: For d >= 4, we show 2^d > 2(d+1). At d=4, "
                "16 > 10. The derivative of 2^d is 2^d * ln(2), which exceeds "
                "the derivative of 2(d+1), which is 2, for all d >= 2. Since "
                "2^d overtakes 2(d+1) between d=2 and d=3 and the exponential "
                "grows strictly faster thereafter, d=3 is the unique solution."
            )
            .step(
                "CONSEQUENCES: d = 3 gives K = d+1 = 4 (closure constant), "
                "2K = 8 vertices, K^2+1 = 17 coupling channels, Kd+1 = 13 "
                "edge structure, and 1+K+K^2 = 21 coupling hierarchy depth."
            )
            .conclude(
                "Three spatial dimensions are uniquely selected by the "
                "requirement that simplex and hypercube vertex counts agree. "
                "This is the foundational identity of the GFM framework, from "
                "which all structural constants derive."
            )
        )

    def model(self) -> Model:
        d = 3
        simplex_vertices = simplex_count(d)
        hypercube_vertices = hypercube_count(d)
        k_derived = d + 1
        solutions = find_unique_solution(20)
        num_solutions = len(solutions)
        unique_d = solutions[0] if num_solutions == 1 else 0

        return (
            Model()
            .add("2(d+1) for d=3", float(simplex_vertices))
            .add("2^d for d=3", float(hypercube_vertices))
            .add("Number of solutions (d=1 to 20)", float(num_solutions))
            .add("Unique solution d", float(unique_d))
            .add("K = d+1", float(k_derived))
            .add("Total vertices 2K", float(2 * k_derived))
            .add("Coupling channels K^2+1", float(k_derived**2 + 1))
            .add("Edge structure Kd+1", float(k_derived * d + 1))
            .add("Hierarchy depth 1+K+K^2", float(1 + k_derived + k_derived**2))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("2(d+1) for d=3", 8.0)
            .add("2^d for d=3", 8.0)
            .add("Number of solutions (d=1 to 20)", 1.0)
            .add("Unique solution d", 3.0)
            .add("K = d+1", float(K))
            .add("Total vertices 2K", float(TOTAL_VERTICES))
            .add("Coupling channels K^2+1", 17.0)
            .add("Edge structure Kd+1", 13.0)
            .add("Hierarchy depth 1+K+K^2", 21.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Dimensionality Uniqueness: 2(d+1) = 2^d Only for d = 3",
        summary="Tests that three spatial dimensions are uniquely selected by simplex hypercube vertex agreement",
        test_classes=[DimensionalityUniqueness],
    )
