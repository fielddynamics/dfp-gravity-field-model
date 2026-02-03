"""
Stellar Constants and Functions
===============================

Constants and helper functions for stellar physics calculations in the GFD framework.

Includes:
- Stellar temperature thresholds for fusion stages
- Density constants (white dwarf, nuclear, etc.)
- Mass ratios and astronomical constants
- Nuclear magic numbers
- Atomic mass data
"""

import math
from typing import Dict, List, Set

# =============================================================================
# FUNDAMENTAL CONSTANTS FROM CODATA 2022
# =============================================================================

from .constants_codata import (
    C, HBAR, G, ALPHA,
    M_E, R_E, M_P, M_N,
    M_SOLAR, R_SOLAR, L_SOLAR,
    A_0,
    M_E_MEV, M_P_MEV, M_N_MEV,
    M_P_OVER_M_E,
)

# GFD model constants
K = 4                    # Coupling constant
K_CLOSURE = 4            # Field closure constant

# =============================================================================
# STELLAR TEMPERATURE THRESHOLDS
# =============================================================================

# Fusion temperature thresholds (K)
T_HYDROGEN_FUSION = 1.5e7    # pp-chain ignition (~15 million K)
T_HELIUM_FUSION = 1.0e8      # Triple-alpha process (~100 million K)
T_CARBON_FUSION = 5.0e8      # Carbon burning (~500 million K)
T_OXYGEN_FUSION = 1.0e9      # Oxygen burning (~1 billion K)
T_SILICON_FUSION = 2.7e9     # Silicon burning (~2.7 billion K)
T_IRON_PHOTODISINTEGRATION = 5.0e9  # Iron photodisintegration (~5 billion K)

# =============================================================================
# STELLAR DENSITY CONSTANTS
# =============================================================================

# Key density values (kg/m^3)
RHO_WHITE_DWARF = 1e9        # Typical white dwarf density
RHO_NEUTRON_STAR = 4e17      # Typical neutron star density
RHO_NUCLEAR = 2.3e17         # Nuclear density (nucleon packing)
RHO_FIELD_BINDING = 1e14     # Approximate density for field binding effects
RHO_SOLAR_CORE = 1.5e5       # Solar core density
RHO_SOLAR_SURFACE = 2e-4     # Solar photosphere density

# =============================================================================
# MASS RATIOS AND ASTRONOMICAL CONSTANTS
# =============================================================================

# Mass ratios (from CODATA 2022)
MASS_RATIO_PROTON_ELECTRON = M_P_OVER_M_E  # ~1836.15 (CODATA 2022)
MASS_RATIO_NEUTRON_PROTON = M_N / M_P      # ~1.00138 (derived from CODATA)

# Solar parameters (R_SOLAR, L_SOLAR from CODATA, others are observational)
T_SOLAR_CORE = 1.57e7        # Solar core temperature (K) - Standard Solar Model
T_SOLAR_SURFACE = 5772       # Solar effective surface temperature (K) - IAU
P_SOLAR_CORE = 2.5e16        # Solar core pressure (Pa) - Standard Solar Model
SOLAR_MASS_LOSS_RATE = 4.26e9  # Solar mass loss rate from fusion (kg/s)

# Stellar limits
CHANDRASEKHAR_LIMIT = 1.4    # White dwarf mass limit (solar masses)
TOV_LIMIT = 2.2              # Tolman-Oppenheimer-Volkoff limit (solar masses)

# =============================================================================
# NUCLEAR PHYSICS CONSTANTS
# =============================================================================

# Magic numbers - nucleon numbers with exceptional nuclear stability
MAGIC_NUMBERS = {2, 8, 20, 28, 50, 82, 126}

# Doubly magic nuclei (both proton and neutron numbers are magic)
DOUBLY_MAGIC = {
    4: (2, 2),     # He-4
    16: (8, 8),    # O-16
    40: (20, 20),  # Ca-40
    48: (20, 28),  # Ca-48
    56: (28, 28),  # Ni-56
    132: (50, 82), # Sn-132
    208: (82, 126),# Pb-208
}

# Stable k-multiples (A values that are k-multiples with enhanced stability)
STABLE_K_MULTIPLES = {4, 8, 12, 16, 20, 24, 28, 32, 40, 56}

# Nuclear binding energy peak
FE_56_BINDING_ENERGY_PER_NUCLEON = 8.79  # MeV/nucleon (most stable)

# Particle masses (MeV/c^2) - from CODATA 2022
MASS_ELECTRON_MEV = M_E_MEV  # ~0.511 MeV
MASS_PROTON_MEV = M_P_MEV    # ~938.272 MeV
MASS_NEUTRON_MEV = M_N_MEV   # ~939.565 MeV
MASS_DIFF_NEUTRON_PROTON_MEV = M_N_MEV - M_P_MEV  # ~1.293 MeV

# =============================================================================
# ATOMIC DATA
# =============================================================================

# Atomic mass numbers (most common isotope)
ATOM_MASS_NUMBERS: Dict[str, int] = {
    'H': 1, 'He': 4, 'Li': 7, 'Be': 9, 'B': 11, 'C': 12, 'N': 14, 'O': 16,
    'F': 19, 'Ne': 20, 'Na': 23, 'Mg': 24, 'Al': 27, 'Si': 28, 'P': 31,
    'S': 32, 'Cl': 35, 'Ar': 40, 'K': 39, 'Ca': 40,
    'Fe': 56, 'Co': 59, 'Ni': 58, 'Cu': 63, 'Zn': 65,
    'U': 238, 'Pu': 244,
}

# Atomic valences (common valence states)
ATOM_VALENCES: Dict[str, int] = {
    'H': 1, 'He': 0, 'Li': 1, 'Be': 2, 'B': 3, 'C': 4, 'N': 3, 'O': 2,
    'F': 1, 'Ne': 0, 'Na': 1, 'Mg': 2, 'Al': 3, 'Si': 4, 'P': 3,
    'S': 2, 'Cl': 1, 'Ar': 0, 'K': 1, 'Ca': 2,
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def is_k_multiple(n: int, k: int = K_CLOSURE) -> bool:
    """
    Check if a number is a k-multiple.
    
    Args:
        n: Number to check
        k: The k-value (default: K_CLOSURE = 4)
        
    Returns:
        True if n is evenly divisible by k
    """
    return n % k == 0


def get_k_factor(n: int, k: int = K_CLOSURE) -> float:
    """
    Calculate the k-factor of a number.
    
    Args:
        n: Number to calculate k-factor for
        k: The k-value (default: K_CLOSURE = 4)
        
    Returns:
        n / k as a float
    """
    return n / k


# Alias for backward compatibility
k_factor = get_k_factor


def k_remainder(n: int, k: int = K_CLOSURE) -> int:
    """
    Calculate the remainder when dividing by k.
    
    Args:
        n: Number to check
        k: The k-value (default: K_CLOSURE = 4)
        
    Returns:
        n mod k
    """
    return n % k


def is_magic_number(n: int) -> bool:
    """Check if a number is a nuclear magic number."""
    return n in MAGIC_NUMBERS


def fusion_threshold_ratio(element: str) -> float:
    """
    Get the fusion threshold temperature ratio relative to hydrogen fusion.
    
    Args:
        element: Element symbol ('H', 'He', 'C', 'O', 'Si')
        
    Returns:
        Ratio of element's fusion temperature to hydrogen fusion temperature
    """
    thresholds = {
        'H': T_HYDROGEN_FUSION,
        'He': T_HELIUM_FUSION,
        'C': T_CARBON_FUSION,
        'O': T_OXYGEN_FUSION,
        'Si': T_SILICON_FUSION,
    }
    if element not in thresholds:
        raise ValueError(f"Unknown element: {element}")
    return thresholds[element] / T_HYDROGEN_FUSION


def compression_ratio_equilibrium_to_tile() -> float:
    """
    Calculate the compression ratio from equilibrium density to tile density.
    
    This represents the density increase needed to reach nuclear scales
    from typical stellar equilibrium conditions.
    
    Returns:
        Ratio of nuclear density to white dwarf density
    """
    return RHO_NUCLEAR / RHO_WHITE_DWARF


def calculate_chandrasekhar_fields() -> float:
    """
    Calculate the number of gravity fields (nucleons) at the Chandrasekhar limit.
    
    Returns:
        Approximate number of protons in 1.4 solar masses
    """
    M_ch = CHANDRASEKHAR_LIMIT * M_SOLAR
    return M_ch / M_P


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Temperature thresholds
    "T_HYDROGEN_FUSION", "T_HELIUM_FUSION", "T_CARBON_FUSION", 
    "T_OXYGEN_FUSION", "T_SILICON_FUSION", "T_IRON_PHOTODISINTEGRATION",
    # Density constants
    "RHO_WHITE_DWARF", "RHO_NEUTRON_STAR", "RHO_NUCLEAR", "RHO_FIELD_BINDING",
    "RHO_SOLAR_CORE", "RHO_SOLAR_SURFACE",
    # Mass ratios
    "MASS_RATIO_PROTON_ELECTRON", "MASS_RATIO_NEUTRON_PROTON",
    # Solar parameters
    "R_SOLAR", "L_SOLAR", "T_SOLAR_CORE", "T_SOLAR_SURFACE", "P_SOLAR_CORE",
    "SOLAR_MASS_LOSS_RATE",
    # Stellar limits
    "CHANDRASEKHAR_LIMIT", "TOV_LIMIT",
    # Nuclear physics
    "MAGIC_NUMBERS", "DOUBLY_MAGIC", "STABLE_K_MULTIPLES",
    "FE_56_BINDING_ENERGY_PER_NUCLEON",
    "MASS_ELECTRON_MEV", "MASS_PROTON_MEV", "MASS_NEUTRON_MEV", 
    "MASS_DIFF_NEUTRON_PROTON_MEV",
    # Atomic data
    "ATOM_MASS_NUMBERS", "ATOM_VALENCES",
    # Helper functions
    "is_k_multiple", "get_k_factor", "k_factor", "k_remainder", "is_magic_number",
    "fusion_threshold_ratio", "compression_ratio_equilibrium_to_tile",
    "calculate_chandrasekhar_fields",
    # Re-exported from CODATA
    "R_E", "A_0", "K_CLOSURE", "M_E", "C", "HBAR", "G", "M_SOLAR", "M_P",
]
