"""
The BBP integrand's roots read as stellated-octahedron geometry
===============================================================

Role:     Supporting finding for Theorem 4: the integrand's numbers as octahedron ratios, with a square as control.
Expected: Passes. Note the control: a square has the same numbers.

Hypothesis (geometric reading): the two numbers that make the BBP integral
work are lengths and angles of the stellated octahedron.

- The real roots +-sqrt(2) equal tetrahedron edge / cube edge (each
  tetrahedron edge is a face diagonal of the cube).
- The complex roots 1 +- i point along a tetrahedron edge drawn in the cube
  face that contains it, at 45 degrees to the cube edges.
- The BBP integration limit 1/sqrt(2) = 16^(-1/8) equals cube edge /
  tetrahedron edge.

All lengths and angles are computed from the eight cube coordinates
(+-1, +-1, +-1) via ``geometry_derivation``.

A control asks whether a single square has the same numbers. If it does, the
reading is a property of a square face and does not by itself single out the
stellated octahedron.
"""

import math
from itertools import combinations

from mpmath import mp, mpf, sqrt as msqrt, polyroots, arg, pi as mpi

from gravity_field_model.framework import *
from gravity_field_model.engine_core.field_closure import geometry_derivation as geo
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import PRECISION


def _dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


class FaceDiagonalReading(Test):
    name = "BBP Roots as Stellated-Octahedron Ratios"
    question = (
        "Are the numbers that make the BBP integral produce pi (the roots sqrt(2) and 1+i, "
        "and the limit 1/sqrt(2)) the edge ratio and edge angle of the stellated octahedron, "
        "and are they specific to it?"
    )
    reference = "Cube coordinates (+-1,+-1,+-1); BBP integrand from Bailey, Borwein, Plouffe (1997)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Cube edge = shortest vertex distance; tetrahedron edge = side of the inscribed regular tetrahedra.")
            .step("Check that every tetrahedron edge lies in a cube face (its endpoints share one coordinate).")
            .step("Ratio tetrahedron edge / cube edge vs the positive real root of y^4-2y^3+4y-4.")
            .step("Angle between a tetrahedron edge and the cube edges of its face vs arg(1+i).")
            .step("Control: the same ratio and angle in a unit square (diagonal vs side).")
            .conclude("The ratios agree exactly; the control shows whether they need more than a square.")
        )

    commentary = (
        "The stellated octahedron's tetrahedra have the cube's face diagonals as edges, so "
        "tetrahedron edge / cube edge = sqrt(2) and a tetrahedron edge runs at 45 degrees "
        "across its face. These are exactly the BBP integrand's real root sqrt(2), the "
        "argument of its complex root 1+i, and (inverted) the integration limit 1/sqrt(2). "
        "The control is the important qualification: a single square has the same diagonal "
        "ratio and the same angle. This reading therefore uses one square face of the cube. "
        "What is particular to the stellated octahedron (two tetrahedra, the TIME axis, the "
        "chamber split) does not enter here; the selection tests in this package examine that."
    )

    def model(self):
        verts = geo.cube_vertices()
        cube_edge = min(_dist(verts[a], verts[b]) for a, b in combinations(verts, 2))
        tets = geo.regular_tetrahedra()
        tet_edges = [(a, b) for t in tets for a, b in combinations(sorted(t), 2)]
        tet_edge = _dist(verts[tet_edges[0][0]], verts[tet_edges[0][1]])
        in_face = sum(
            1 for a, b in tet_edges
            if sum(1 for x, y in zip(verts[a], verts[b]) if x == y) == 1
        )
        # Angle between a tetrahedron edge and a cube edge in the same face.
        # The edge vector has one zero coordinate (the face it lies in); a cube
        # edge of that face runs along either of the other two axes.
        a, b = tet_edges[0]
        e = [y - x for x, y in zip(verts[a], verts[b])]
        other = [0.0] * 3
        other[next(i for i, c in enumerate(e) if c != 0)] = 1.0
        cosang = abs(sum(x * y for x, y in zip(e, other))) / math.sqrt(sum(x * x for x in e))
        angle_deg = math.degrees(math.acos(cosang))

        with mp.workdps(PRECISION):
            roots = polyroots([1, -2, 0, 4, -4], maxsteps=200, extraprec=200)
            real_root = max(r.real for r in roots if abs(r.imag) < mpf(10) ** -50)
            complex_root = [r for r in roots if r.imag > mpf(10) ** -50][0]
            root_angle = float(arg(complex_root) * 180 / mpi)
            bbp_limit = float(mpf(16) ** (-mpf(1) / 8))

        # Control: a unit square.
        sq = [(0, 0), (1, 0), (0, 1), (1, 1)]
        sq_side = min(_dist(p, q) for p, q in combinations(sq, 2))
        sq_diag = max(_dist(p, q) for p, q in combinations(sq, 2))
        sq_angle = math.degrees(math.atan2(1, 1))
        square_has_same = (abs(sq_diag / sq_side - float(real_root)) < 1e-12
                           and abs(sq_angle - root_angle) < 1e-12)

        return (
            Model()
            .add("Tetrahedron edges lying in a cube face (of 12)", in_face)
            .add("Tet edge / cube edge minus real root sqrt(2)", tet_edge / cube_edge - float(real_root))
            .add("Cube edge / tet edge minus BBP limit 16^(-1/8)", cube_edge / tet_edge - bbp_limit)
            .add("Tet edge angle in face minus arg(1+i) (deg)", angle_deg - root_angle)
            .add("Same ratio and angle in a single square (1=yes)", 1 if square_has_same else 0)
        )

    def observations(self):
        return (
            Observed()
            .add("Tetrahedron edges lying in a cube face (of 12)", 12)
            .add("Tet edge / cube edge minus real root sqrt(2)", 0.0, abs_tol=1e-12)
            .add("Cube edge / tet edge minus BBP limit 16^(-1/8)", 0.0, abs_tol=1e-12)
            .add("Tet edge angle in face minus arg(1+i) (deg)", 0.0, abs_tol=1e-9)
            # A square's diagonal is sqrt(2) times its side and runs at 45 degrees.
            .add("Same ratio and angle in a single square (1=yes)", 1)
        )


ALL_TESTS = [FaceDiagonalReading]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("BBP face-diagonal reading", "BBP integrand roots vs stellated-octahedron ratios.", ALL_TESTS) else 1)
