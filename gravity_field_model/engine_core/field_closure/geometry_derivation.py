"""
Geometry derived from vertex coordinates alone
==============================================

Several field-closure tests compare a structural count (vertices per
tetrahedron, faces, TIME faces) with an expected value. Reading those counts
from the hand-written tables in ``common.geometry_constants`` and comparing
them with the same numbers cannot fail. The functions here recompute the
structure from the eight cube coordinates (+-1, +-1, +-1) only, so the tests
check the tables against the geometry.

Nothing here reads TET_A, TET_B, FACES or TIME_FACES.
"""

from itertools import combinations, product
from math import isclose, sqrt
from typing import Dict, FrozenSet, List, Tuple

Coords = Tuple[int, int, int]


def cube_vertices() -> Dict[int, Coords]:
    """Vertex index -> coordinates, with index bits (x, y, z) mapped to -1/+1."""
    return {
        (bx << 2) | (by << 1) | bz: (2 * bx - 1, 2 * by - 1, 2 * bz - 1)
        for bx, by, bz in product((0, 1), repeat=3)
    }


def _dist(a: Coords, b: Coords) -> float:
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def regular_tetrahedra() -> List[FrozenSet[int]]:
    """
    All sets of four cube vertices that are mutually at the face-diagonal
    distance 2*sqrt(2), i.e. the regular tetrahedra inscribed in the cube.
    The stellated octahedron is the union of the two that exist.
    """
    verts = cube_vertices()
    d = 2 * sqrt(2)
    tets = []
    for quad in combinations(verts, 4):
        if all(isclose(_dist(verts[a], verts[b]), d) for a, b in combinations(quad, 2)):
            tets.append(frozenset(quad))
    return tets


def tetrahedron_faces() -> Dict[int, FrozenSet[int]]:
    """
    Faces of the two inscribed tetrahedra, keyed by the vertex each face is
    opposite to (the convention of the FACE_An / FACE_Bn names).
    """
    faces = {}
    for tet in regular_tetrahedra():
        for v in tet:
            faces[v] = frozenset(tet - {v})
    return faces


def face_normal(face: FrozenSet[int]) -> Tuple[float, float, float]:
    """Outward unit normal of a face (pointing away from the cube centre)."""
    verts = cube_vertices()
    p0, p1, p2 = (verts[v] for v in sorted(face))
    u = [p1[i] - p0[i] for i in range(3)]
    w = [p2[i] - p0[i] for i in range(3)]
    n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
    centroid = [sum(verts[v][i] for v in face) / 3 for i in range(3)]
    if sum(n[i] * centroid[i] for i in range(3)) < 0:
        n = [-x for x in n]
    norm = sqrt(sum(x * x for x in n))
    return tuple(x / norm for x in n)


def time_faces() -> Dict[int, FrozenSet[int]]:
    """
    Faces perpendicular to the body diagonal through vertices 0 = (-1,-1,-1)
    and 7 = (+1,+1,+1): the axis the model identifies with time.
    """
    axis = (1 / sqrt(3),) * 3
    out = {}
    for v, face in tetrahedron_faces().items():
        n = face_normal(face)
        if isclose(abs(sum(a * b for a, b in zip(n, axis))), 1.0):
            out[v] = face
    return out


def tetrahedron_of(vertex: int) -> int:
    """Index (0 or 1) of the inscribed tetrahedron containing a vertex, ordered by smallest vertex."""
    tets = sorted(regular_tetrahedra(), key=min)
    return 0 if vertex in tets[0] else 1
