"""
Stellated Octahedron Geometry Constants
=======================================

This module defines the geometric constants for the GFM field closure model:
- 8 vertices at unit cube corners
- 2 interlocking tetrahedra (Chamber A and Chamber B)
- 8 triangular faces (4 per chamber)
- Complementary pairs linking opposite chambers

These constants are the foundation of the pi base-8 traversal algorithm
used for field closure calculations.
"""

from typing import Dict, List, Set, Tuple

# =============================================================================
# STELLATED OCTAHEDRON GEOMETRY
# =============================================================================
#
# The stellated octahedron consists of 8 vertices at the corners of a unit cube,
# forming two interlocking tetrahedra (Chamber A and Chamber B).
#
# CUBE STRUCTURE (view from front-right-above):
#
#               V6 ----------- V7              y (up)
#               /|            /|               |
#              / |           / |               |   z (front)
#             /  |          /  |               |  /
#           V2 ----------- V3  |               | /
#            |   |         |   |               |/
#            |  V4 --------|-- V5              +-------> x (right)
#            |  /          |  /
#            | /           | /
#            |/            |/
#           V0 ----------- V1
#
# COORDINATE SYSTEM:
#   - x axis: left (-1) to right (+1)
#   - y axis: bottom (-1) to top (+1)
#   - z axis: back (-1) to front (+1)
#
# 3-BIT BINARY ENCODING:
#   Vertex number V = (bit2)(bit1)(bit0) in binary, where:
#     - bit2 (MSB) encodes x: 0 -> x=-1 (left),  1 -> x=+1 (right)
#     - bit1       encodes y: 0 -> y=-1 (bottom), 1 -> y=+1 (top)
#     - bit0 (LSB) encodes z: 0 -> z=-1 (back),  1 -> z=+1 (front)
#
#   Example: V5 = 101 binary -> bit2=1 (x=+1), bit1=0 (y=-1), bit0=1 (z=+1)
#            Position: right-bottom-front = (+1, -1, +1)
#
# PARITY AND CHAMBER ASSIGNMENT:
#   - Popcount = number of 1-bits in the binary representation
#   - Even parity (popcount 0 or 2) -> Chamber B (TET_B)
#   - Odd parity (popcount 1 or 3)  -> Chamber A (TET_A)
#
# =============================================================================

# 8 vertices of the stellated octahedron (unit cube corners)
VERTICES: Dict[int, Dict] = {
    # Vertex: binary, coordinates (x, y, z), popcount, parity, chamber
    0: {'binary': '000', 'coords': (-1, -1, -1)},  # popcount=0, Even -> Chamber B, left-bottom-back
    1: {'binary': '001', 'coords': (-1, -1, +1)},  # popcount=1, Odd  -> Chamber A, left-bottom-front
    2: {'binary': '010', 'coords': (-1, +1, -1)},  # popcount=1, Odd  -> Chamber A, left-top-back
    3: {'binary': '011', 'coords': (-1, +1, +1)},  # popcount=2, Even -> Chamber B, left-top-front
    4: {'binary': '100', 'coords': (+1, -1, -1)},  # popcount=1, Odd  -> Chamber A, right-bottom-back
    5: {'binary': '101', 'coords': (+1, -1, +1)},  # popcount=2, Even -> Chamber B, right-bottom-front
    6: {'binary': '110', 'coords': (+1, +1, -1)},  # popcount=2, Even -> Chamber B, right-top-back
    7: {'binary': '111', 'coords': (+1, +1, +1)},  # popcount=3, Odd  -> Chamber A, right-top-front
}

# =============================================================================
# TWO INTERLOCKING TETRAHEDRA (DUAL FIELD CHAMBERS)
# =============================================================================
#
# The 8 vertices partition into two tetrahedra based on parity:
#
#   CHAMBER A (TET_A)              CHAMBER B (TET_B)
#   Odd parity vertices            Even parity vertices
#   {V1, V2, V4, V7}               {V0, V3, V5, V6}
#
#            V7                            V6
#           /|\                           /|\
#          / | \                         / | \
#         /  |  \                       /  |  \
#        V1--+--V2                     V0--+--V3
#            |                             |
#            V4                            V5
#
# These form a stellated octahedron when combined, satisfying:
#   - Bimetric gravity requirements (two coupled geometric structures)
#   - Spinor compatibility (720 degree rotation returns to initial state)
#   - Chirality balance (both self-dual and anti-self-dual sectors)
#
# =============================================================================

TET_A: Set[int] = {1, 2, 4, 7}  # Chamber A: odd parity vertices (popcount = 1 or 3)
TET_B: Set[int] = {0, 3, 5, 6}  # Chamber B: even parity vertices (popcount = 0 or 2)

# =============================================================================
# 8 TRIANGULAR FACES
# =============================================================================
#
# Each tetrahedron has 4 triangular faces. Total: 8 faces.
#
# FACE NAMING CONVENTION:
#   FACE_[Chamber][OppositeVertex]
#   - Chamber: A or B (which tetrahedron the face belongs to)
#   - OppositeVertex: the vertex NOT in this face
#
# Example: FACE_A7 is the Chamber A face that does NOT contain V7
#          Its vertices are {V1, V2, V4} (all Chamber A vertices except V7)
#
# FACE TYPES:
#   - TIME faces (2): FACE_A7 and FACE_B0 (opposite the apex vertices V7 and V0)
#   - SPATIAL faces (6): All other faces (contain an apex vertex)
#
# This gives the (3+1) spacetime decomposition: 3 spatial + 1 time per chamber.
#
# =============================================================================

FACES: Dict[str, Set[int]] = {
    # CHAMBER A FACES (vertices from TET_A = {1, 2, 4, 7})
    'FACE_A1': {2, 4, 7},  # Face opposite V1, contains {V2, V4, V7} - SPATIAL
    'FACE_A2': {1, 4, 7},  # Face opposite V2, contains {V1, V4, V7} - SPATIAL
    'FACE_A4': {1, 2, 7},  # Face opposite V4, contains {V1, V2, V7} - SPATIAL
    'FACE_A7': {1, 2, 4},  # Face opposite V7, contains {V1, V2, V4} - TIME face

    # CHAMBER B FACES (vertices from TET_B = {0, 3, 5, 6})
    'FACE_B0': {3, 5, 6},  # Face opposite V0, contains {V3, V5, V6} - TIME face
    'FACE_B3': {0, 5, 6},  # Face opposite V3, contains {V0, V5, V6} - SPATIAL
    'FACE_B5': {0, 3, 6},  # Face opposite V5, contains {V0, V3, V6} - SPATIAL
    'FACE_B6': {0, 3, 5},  # Face opposite V6, contains {V0, V3, V5} - SPATIAL
}

# =============================================================================
# COMPLEMENTARY PAIRS
# =============================================================================
#
# Each vertex has a complementary partner at the opposite corner of the cube.
# Complementary vertices have:
#   - Binary representations that are bitwise complements (XOR with 111)
#   - Sum equal to 7 (e.g., V3 + V4 = 3 + 4 = 7)
#   - Opposite chambers (one in TET_A, one in TET_B)
#
#   Pair      Binary XOR     Sum    Chambers
#   (V0, V7)  000 ^ 111 = 7   7     B <-> A
#   (V1, V6)  001 ^ 110 = 7   7     A <-> B
#   (V2, V5)  010 ^ 101 = 7   7     A <-> B
#   (V3, V4)  011 ^ 100 = 7   7     B <-> A
#
# SIGNIFICANCE: The first two pi base-8 digits (3, 1) produce vertices V3 and V4,
# which form a complementary pair. This immediately activates both chambers
# and establishes bimetric coupling at traversal initialization.
#
# =============================================================================

COMPLEMENTARY_PAIRS: List[Tuple[int, int]] = [
    (0, 7),  # V0 (Chamber B) <-> V7 (Chamber A), opposite cube corners
    (1, 6),  # V1 (Chamber A) <-> V6 (Chamber B), opposite cube corners
    (2, 5),  # V2 (Chamber A) <-> V5 (Chamber B), opposite cube corners
    (3, 4),  # V3 (Chamber B) <-> V4 (Chamber A), first pi traversal pair
]

# =============================================================================
# TIME AND SPATIAL FACE CLASSIFICATION
# =============================================================================
#
# The 8 faces divide into TIME (2) and SPATIAL (6) categories:
#
#   TIME FACES: Opposite the apex vertices (V0 and V7)
#     - FACE_A7: opposite V7 (the all-positive vertex)
#     - FACE_B0: opposite V0 (the all-negative vertex)
#     These are the "polar" faces at opposite ends of the structure.
#
#   SPATIAL FACES: All other faces (6 total)
#     - Chamber A: FACE_A1, FACE_A2, FACE_A4 (each contains apex V7)
#     - Chamber B: FACE_B3, FACE_B5, FACE_B6 (each contains apex V0)
#
# This gives each chamber a (3+1) structure: 3 spatial faces + 1 time face,
# mirroring the (3+1) spacetime decomposition in General Relativity.
#
# =============================================================================

TIME_FACES: Set[str] = {'FACE_A7', 'FACE_B0'}  # 2 faces opposite apex vertices

SPATIAL_FACES: Set[str] = {  # 6 faces that include an apex vertex
    'FACE_A1', 'FACE_A2', 'FACE_A4',  # Chamber A spatial (contain V7)
    'FACE_B3', 'FACE_B5', 'FACE_B6',  # Chamber B spatial (contain V0)
}


# =============================================================================
# VERTEX HELPER FUNCTIONS
# =============================================================================

def get_vertex_binary(vertex: int) -> str:
    """
    Get the 3-bit binary representation of a vertex (0-7).
    
    The binary encodes the cube corner position:
        bit2 (MSB) = x: 0 -> left (-1),  1 -> right (+1)
        bit1       = y: 0 -> bottom (-1), 1 -> top (+1)
        bit0 (LSB) = z: 0 -> back (-1),  1 -> front (+1)
    
    Examples:
        get_vertex_binary(0) -> '000' -> (-1,-1,-1) left-bottom-back
        get_vertex_binary(5) -> '101' -> (+1,-1,+1) right-bottom-front
        get_vertex_binary(7) -> '111' -> (+1,+1,+1) right-top-front
    """
    if not 0 <= vertex <= 7:
        raise ValueError(f"Vertex must be 0-7, got {vertex}")
    return format(vertex, '03b')


def get_vertex_parity(vertex: int) -> int:
    """
    Get the parity (0 or 1) of a vertex based on its popcount (number of 1-bits).
    
    Parity determines chamber assignment:
        - Even parity (popcount 0 or 2) -> 0 -> Chamber B (TET_B)
        - Odd parity (popcount 1 or 3)  -> 1 -> Chamber A (TET_A)
    
    Examples:
        get_vertex_parity(0) -> 0 (000 has 0 ones, even -> Chamber B)
        get_vertex_parity(3) -> 0 (011 has 2 ones, even -> Chamber B)
        get_vertex_parity(1) -> 1 (001 has 1 one, odd -> Chamber A)
        get_vertex_parity(7) -> 1 (111 has 3 ones, odd -> Chamber A)
    """
    return bin(vertex).count('1') % 2


def get_tetrahedron(vertex: int) -> str:
    """
    Determine which tetrahedron (Field Chamber) a vertex belongs to.
    
    Returns:
        'A' for Chamber A (TET_A) - odd parity vertices {1, 2, 4, 7}
        'B' for Chamber B (TET_B) - even parity vertices {0, 3, 5, 6}
    
    The two chambers form the dual structure required for bimetric gravity.
    """
    if vertex in TET_A:
        return 'A'
    elif vertex in TET_B:
        return 'B'
    else:
        raise ValueError(f"Vertex {vertex} not in TET_A or TET_B")


def get_complement(vertex: int) -> int:
    """
    Get the complementary vertex (XOR with 7, or equivalently 7 - vertex).
    
    Complementary vertices are at opposite corners of the cube and always
    belong to opposite chambers. Their binary representations are bitwise
    complements of each other.
    
    Examples:
        get_complement(0) -> 7  (000 ^ 111 = 111, Chamber B -> A)
        get_complement(3) -> 4  (011 ^ 111 = 100, Chamber B -> A)
        get_complement(5) -> 2  (101 ^ 111 = 010, Chamber B -> A)
    
    The first pi traversal step activates V3, and the second activates V4.
    Since get_complement(3) == 4, this immediately establishes bimetric coupling.
    """
    return vertex ^ 7


def get_vertex_coords(vertex: int) -> Tuple[int, int, int]:
    """
    Get the (x, y, z) coordinates of a vertex.
    
    Each coordinate is either -1 or +1, derived from the binary encoding:
        x = -1 if bit2 == 0 else +1
        y = -1 if bit1 == 0 else +1
        z = -1 if bit0 == 0 else +1
    
    Examples:
        get_vertex_coords(0) -> (-1, -1, -1)  # origin corner
        get_vertex_coords(7) -> (+1, +1, +1)  # opposite corner
        get_vertex_coords(5) -> (+1, -1, +1)  # right-bottom-front
    """
    if not 0 <= vertex <= 7:
        raise ValueError(f"Vertex must be 0-7, got {vertex}")
    return VERTICES[vertex]['coords']


def get_faces_for_vertex(vertex: int) -> List[str]:
    """
    Get the list of faces that contain this vertex.
    
    Each vertex belongs to exactly 3 faces (all faces of its chamber
    except the one opposite to it).
    
    Examples:
        get_faces_for_vertex(0) -> ['FACE_B3', 'FACE_B5', 'FACE_B6']
        get_faces_for_vertex(7) -> ['FACE_A1', 'FACE_A2', 'FACE_A4']
    """
    return [name for name, vertices in FACES.items() if vertex in vertices]


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Constants
    'VERTICES',
    'TET_A',
    'TET_B',
    'FACES',
    'COMPLEMENTARY_PAIRS',
    'TIME_FACES',
    'SPATIAL_FACES',
    # Functions
    'get_vertex_binary',
    'get_vertex_parity',
    'get_tetrahedron',
    'get_complement',
    'get_vertex_coords',
    'get_faces_for_vertex',
]