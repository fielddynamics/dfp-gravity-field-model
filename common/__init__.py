"""
GFD Common Constants and Utilities
==================================

Shared physics constants, geometry definitions, and helper functions
used across all GFD test modules.

This module is imported by test files via:
    from common import K, VERTICES, TET_A, ...
    from common.stellar_constants import T_HYDROGEN_FUSION, ...
    from common.constants_codata import M_E, C, HBAR, ...
"""

import math
from typing import Any, Dict, List, Set, Tuple, Optional

# =============================================================================
# PHYSICAL CONSTANTS FROM CODATA 2022
# =============================================================================

from .constants_codata import (
    # Universal constants
    C, SPEED_OF_LIGHT,
    H, H_PLANCK, PLANCK_CONSTANT,
    HBAR, H_BAR, REDUCED_PLANCK_CONSTANT,
    G, GRAVITATIONAL_CONSTANT,
    K_B, BOLTZMANN_CONSTANT,
    # Electromagnetic
    ALPHA, FINE_STRUCTURE_CONSTANT, ALPHA_INVERSE,
    E_CHARGE, ELEMENTARY_CHARGE,
    EPSILON_0, MU_0,
    # Electron properties
    M_E, ELECTRON_MASS, M_E_MEV,
    R_E, CLASSICAL_ELECTRON_RADIUS,
    LAMBDA_COMPTON, LAMBDA_C, ELECTRON_COMPTON_WAVELENGTH, LAMBDA_COMPTON_BAR,
    A_0, BOHR_RADIUS,
    G_ELECTRON,
    # Proton properties
    M_P, PROTON_MASS, M_P_MEV,
    R_PROTON, PROTON_RADIUS,
    LAMBDA_COMPTON_PROTON,
    M_P_OVER_M_E, PROTON_ELECTRON_MASS_RATIO,
    # Neutron properties
    M_N, NEUTRON_MASS, M_N_MEV,
    DELTA_M_NP, DELTA_M_NP_MEV,
    # Planck units
    L_PLANCK, PLANCK_LENGTH,
    T_PLANCK, PLANCK_TIME,
    M_PLANCK, PLANCK_MASS,
    TEMP_PLANCK, PLANCK_TEMPERATURE,
    E_PLANCK, PLANCK_ENERGY,
    # Astronomical
    M_SOLAR, SOLAR_MASS,
    R_SOLAR, SOLAR_RADIUS,
    L_SOLAR, SOLAR_LUMINOSITY,
    AU, ASTRONOMICAL_UNIT,
    PARSEC,
    # Other constants
    R_INFINITY,
    SIGMA_SB, STEFAN_BOLTZMANN,
    N_A, AVOGADRO,
    AMU, ATOMIC_MASS_UNIT,
    # Conversions
    EV, ELECTRON_VOLT,
    EV_TO_KG, J_TO_MEV,
)

# =============================================================================
# GFD MODEL CONSTANTS
# =============================================================================

K = 4                    # Coupling constant (tetrahedral vertices)
K_CLOSURE = 4            # Field closure constant (alias)

# MOND acceleration scale (empirical)
A_MOND = 1.2e-10         # m/s^2 (Milgrom's constant)

# =============================================================================
# STELLATED OCTAHEDRON GEOMETRY
# =============================================================================

# 8 vertices of the stellated octahedron (unit cube corners)
# Each vertex is labeled 0-7, corresponding to binary representations
VERTICES = {0, 1, 2, 3, 4, 5, 6, 7}

# Two interlocking tetrahedra based on vertex parity
# TET_A: odd parity vertices (odd number of 1-bits)
# TET_B: even parity vertices (even number of 1-bits)
TET_A = {1, 2, 4, 7}     # Odd parity
TET_B = {0, 3, 5, 6}     # Even parity

# 8 faces of the stellated octahedron
# Each face is a triangular face from one of the two tetrahedra
FACES = {
    0: (1, 2, 4),  # TET_A face
    1: (1, 2, 7),  # TET_A face
    2: (1, 4, 7),  # TET_A face
    3: (2, 4, 7),  # TET_A face
    4: (0, 3, 5),  # TET_B face
    5: (0, 3, 6),  # TET_B face
    6: (0, 5, 6),  # TET_B face
    7: (3, 5, 6),  # TET_B face
}

# Complementary pairs: each vertex pairs with its XOR complement (vertex ^ 7)
# These pairs cross tetrahedra: one from TET_A, one from TET_B
COMPLEMENTARY_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]

# TIME faces (2 of 8) - faces at the "poles" of the structure
TIME_FACES = {3, 7}  # (2, 4, 7) and (3, 5, 6)

# SPATIAL faces (6 of 8) - faces forming the "equator"
SPATIAL_FACES = {0, 1, 2, 4, 5, 6}

# =============================================================================
# VERTEX HELPER FUNCTIONS
# =============================================================================

def get_vertex_binary(vertex: int) -> str:
    """Get the 3-bit binary representation of a vertex (0-7)."""
    if not 0 <= vertex <= 7:
        raise ValueError(f"Vertex must be 0-7, got {vertex}")
    return format(vertex, '03b')


def get_vertex_parity(vertex: int) -> int:
    """Get the parity (0 or 1) of a vertex based on its 1-bit count."""
    return bin(vertex).count('1') % 2


def get_tetrahedron(vertex: int) -> str:
    """Determine which tetrahedron a vertex belongs to: 'A' or 'B'."""
    if vertex in TET_A:
        return 'A'
    elif vertex in TET_B:
        return 'B'
    else:
        raise ValueError(f"Vertex {vertex} not in TET_A or TET_B")


def get_complement(vertex: int) -> int:
    """Get the complementary vertex (XOR with 7)."""
    return vertex ^ 7


# =============================================================================
# PI BASE-8 AND BBP ALGORITHM
# =============================================================================
# 
# IMPORTANT: Pi digits are imported from the verified pi_data module which
# contains 10,000 fractional digits computed via mpmath at 12,000 decimal
# digits of precision using two independent methods.
#
# Do NOT use hardcoded pi digits elsewhere - they are likely incorrect.
# Always import from this module or directly from pi_data.
# =============================================================================

# Import verified pi data from authoritative source
try:
    from gfd_model_v2.engine.engine_crosschecks.pi_data import (
        PI_BASE8_FRACTIONAL as _PI_BASE8_FRACTIONAL,
        PI_INTEGER_PART as _PI_INTEGER_PART,
        get_pi_base8 as _get_pi_base8_verified,
    )
    _PI_DATA_AVAILABLE = True
except ImportError:
    # Fallback for when running outside the package structure
    _PI_DATA_AVAILABLE = False
    _PI_BASE8_FRACTIONAL = None
    _PI_INTEGER_PART = 3

# Pi base-16 digits (verified)
# Pi (base 16) = 3.243F6A8885A308D313198A2E03707344A4093822299F31D...
PI_BASE16_DIGITS = "3243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89"


def get_pi_base8(n_digits: int, include_integer: bool = True) -> List[int]:
    """
    Get pi base-8 digits as a list of integers.
    
    Uses verified data from pi_data module (10,000 fractional digits available).
    
    Args:
        n_digits: Number of fractional digits to include (max 10,000)
        include_integer: If True, include the integer part (3) at the start
        
    Returns:
        List of digits (each 0-7)
        
    Raises:
        ValueError: If n_digits exceeds available verified digits
    """
    if _PI_DATA_AVAILABLE:
        return _get_pi_base8_verified(n_digits, include_integer)
    else:
        raise ImportError(
            "Verified pi_data module not available. "
            "Cannot provide guaranteed-correct pi digits."
        )


def pi_base_8(n: int = 100) -> List[int]:
    """
    Return first n digits of pi in base 8 as a list of integers.
    
    Includes the integer part (3) as the first digit.
    Total length will be n, so fractional digits = n - 1.
    """
    if n <= 0:
        return []
    # n includes the integer part, so we want n-1 fractional digits
    return get_pi_base8(n - 1, include_integer=True)


def pi_base_16(n: int = 100) -> List[int]:
    """
    Return first n digits of pi in base 16 as a list of integers.
    
    Includes the integer part (3) as the first digit.
    Each digit is 0-15 (hex values).
    """
    hex_map = {c: i for i, c in enumerate('0123456789ABCDEF')}
    return [hex_map[c] for c in PI_BASE16_DIGITS[:n]]


def get_pi_digit_base8(position: int) -> int:
    """
    Get a single digit of pi in base 8 at the given position.
    
    Position 0 is the integer part (3).
    Position 1+ are fractional digits.
    """
    digits = get_pi_base8(position + 1, include_integer=True)
    if position < 0 or position >= len(digits):
        raise ValueError(f"Position {position} out of range")
    return digits[position]


# =============================================================================
# TRAVERSAL FUNCTIONS
# =============================================================================

def traverse_pi_base8(n_digits: int = 100, include_integer: bool = True) -> List[Dict]:
    """
    Traverse the stellated octahedron using pi base-8 digits.
    
    The traversal algorithm:
    1. Each pi digit (0-7) is added to the cumulative sum
    2. The current vertex is cumsum mod 8
    3. An orbit completes when cumsum crosses a multiple of 8
    
    Args:
        n_digits: Number of fractional digits to traverse
        include_integer: If True, include pi's integer part (3) as first step
        
    Returns:
        List of step dictionaries, each containing:
        - step: Step number (0-indexed)
        - digit: The pi digit at this step (0-7)
        - cumsum: Cumulative sum of all digits so far
        - vertex: Current vertex position (cumsum mod 8)
        - tetrahedron: 'A' for odd-parity vertices, 'B' for even-parity
        - orbit: Orbit number (cumsum // 8)
        - orbit_complete: True if this step completed an orbit (cumsum % 8 == 0)
    """
    digits = get_pi_base8(n_digits, include_integer)
    results = []
    cumsum = 0
    
    for step, digit in enumerate(digits):
        cumsum += digit
        vertex = cumsum % 8
        tet = 'A' if vertex in TET_A else 'B'
        orbit = cumsum // 8
        orbit_complete = cumsum > 0 and cumsum % 8 == 0
        
        results.append({
            'step': step,
            'digit': digit,
            'cumsum': cumsum,
            'vertex': vertex,
            'tetrahedron': tet,
            'orbit': orbit,
            'orbit_complete': orbit_complete,
        })
    
    return results


def calculate_settlement_frequency() -> float:
    """
    Calculate the settlement (closure) frequency from model parameters.
    
    f = c / (k * r_e) where:
    - c = speed of light
    - k = coupling constant (4)
    - r_e = classical electron radius
    
    Returns approximately 2.66e22 Hz
    """
    return C / (K * R_E)


# =============================================================================
# STELLAR CONSTANTS (re-exported from stellar_constants for convenience)
# =============================================================================

# Import stellar constants for backward compatibility
# Tests that do `from common import T_HYDROGEN_FUSION` will still work
try:
    from .stellar_constants import (
        # Temperature thresholds
        T_HYDROGEN_FUSION, T_HELIUM_FUSION, T_CARBON_FUSION, 
        T_OXYGEN_FUSION, T_SILICON_FUSION, T_IRON_PHOTODISINTEGRATION,
        # Density constants
        RHO_WHITE_DWARF, RHO_NEUTRON_STAR, RHO_NUCLEAR, RHO_FIELD_BINDING,
        RHO_SOLAR_CORE, RHO_SOLAR_SURFACE,
        # Mass ratios
        MASS_RATIO_PROTON_ELECTRON, MASS_RATIO_NEUTRON_PROTON,
        # Solar parameters
        T_SOLAR_CORE, T_SOLAR_SURFACE, P_SOLAR_CORE,
        SOLAR_MASS_LOSS_RATE,
        # Stellar limits
        CHANDRASEKHAR_LIMIT, TOV_LIMIT,
        # Nuclear physics
        MAGIC_NUMBERS, FE_56_BINDING_ENERGY_PER_NUCLEON,
        MASS_ELECTRON_MEV, MASS_PROTON_MEV, MASS_NEUTRON_MEV,
        MASS_DIFF_NEUTRON_PROTON_MEV,
        # Atomic data
        ATOM_MASS_NUMBERS, ATOM_VALENCES,
        # Helper functions
        is_k_multiple, get_k_factor, is_magic_number,
        fusion_threshold_ratio, compression_ratio_equilibrium_to_tile,
        calculate_chandrasekhar_fields,
    )
    _STELLAR_AVAILABLE = True
except ImportError:
    # Stellar constants not yet available (e.g., during initial import)
    _STELLAR_AVAILABLE = False


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # CODATA Physical constants
    "C", "SPEED_OF_LIGHT",
    "H", "H_PLANCK", "PLANCK_CONSTANT",
    "HBAR", "H_BAR", "REDUCED_PLANCK_CONSTANT",
    "G", "GRAVITATIONAL_CONSTANT",
    "K_B", "BOLTZMANN_CONSTANT",
    "ALPHA", "FINE_STRUCTURE_CONSTANT", "ALPHA_INVERSE",
    "E_CHARGE", "ELEMENTARY_CHARGE",
    "EPSILON_0", "MU_0",
    "M_E", "ELECTRON_MASS", "M_E_MEV",
    "R_E", "CLASSICAL_ELECTRON_RADIUS",
    "LAMBDA_COMPTON", "LAMBDA_C", "ELECTRON_COMPTON_WAVELENGTH", "LAMBDA_COMPTON_BAR",
    "A_0", "BOHR_RADIUS",
    "G_ELECTRON",
    "M_P", "PROTON_MASS", "M_P_MEV",
    "R_PROTON", "PROTON_RADIUS",
    "LAMBDA_COMPTON_PROTON",
    "M_P_OVER_M_E", "PROTON_ELECTRON_MASS_RATIO",
    "M_N", "NEUTRON_MASS", "M_N_MEV",
    "DELTA_M_NP", "DELTA_M_NP_MEV",
    "L_PLANCK", "PLANCK_LENGTH",
    "T_PLANCK", "PLANCK_TIME",
    "M_PLANCK", "PLANCK_MASS",
    "TEMP_PLANCK", "PLANCK_TEMPERATURE",
    "E_PLANCK", "PLANCK_ENERGY",
    "M_SOLAR", "SOLAR_MASS",
    "R_SOLAR", "SOLAR_RADIUS",
    "L_SOLAR", "SOLAR_LUMINOSITY",
    "AU", "ASTRONOMICAL_UNIT",
    "PARSEC",
    "R_INFINITY",
    "SIGMA_SB", "STEFAN_BOLTZMANN",
    "N_A", "AVOGADRO",
    "AMU", "ATOMIC_MASS_UNIT",
    "EV", "ELECTRON_VOLT",
    "EV_TO_KG", "J_TO_MEV",
    # GFD constants
    "K", "K_CLOSURE",
    "A_MOND",
    # Geometry
    "VERTICES", "TET_A", "TET_B", "FACES", "TIME_FACES", "SPATIAL_FACES", 
    "COMPLEMENTARY_PAIRS",
    # Vertex functions
    "get_vertex_binary", "get_vertex_parity", "get_tetrahedron", "get_complement",
    # Pi digits
    "PI_BASE16_DIGITS",
    "pi_base_8", "pi_base_16", "get_pi_base8", "get_pi_digit_base8",
    # Traversal
    "traverse_pi_base8", "calculate_settlement_frequency",
    # Stellar constants (when available)
    "T_HYDROGEN_FUSION", "T_HELIUM_FUSION", "T_CARBON_FUSION",
    "T_OXYGEN_FUSION", "T_SILICON_FUSION", "T_IRON_PHOTODISINTEGRATION",
    "RHO_WHITE_DWARF", "RHO_NEUTRON_STAR", "RHO_NUCLEAR", "RHO_FIELD_BINDING",
    "RHO_SOLAR_CORE", "RHO_SOLAR_SURFACE",
    "MASS_RATIO_PROTON_ELECTRON", "MASS_RATIO_NEUTRON_PROTON",
    "T_SOLAR_CORE", "T_SOLAR_SURFACE", "P_SOLAR_CORE",
    "SOLAR_MASS_LOSS_RATE",
    "CHANDRASEKHAR_LIMIT", "TOV_LIMIT",
    "MAGIC_NUMBERS", "FE_56_BINDING_ENERGY_PER_NUCLEON",
    "MASS_ELECTRON_MEV", "MASS_PROTON_MEV", "MASS_NEUTRON_MEV",
    "MASS_DIFF_NEUTRON_PROTON_MEV",
    "ATOM_MASS_NUMBERS", "ATOM_VALENCES",
    "is_k_multiple", "get_k_factor", "is_magic_number",
    "fusion_threshold_ratio", "compression_ratio_equilibrium_to_tile",
    "calculate_chandrasekhar_fields",
]
