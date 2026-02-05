"""
CODATA 2022 Fundamental Physical Constants
==========================================

This module contains fundamental physical constants from the 2022 CODATA
(Committee on Data for Science and Technology) recommended values.

Source: NIST Reference on Constants, Units, and Uncertainty
        https://physics.nist.gov/cuu/Constants/

Last updated: CODATA 2022 (published 2024)

All values include standard uncertainty in comments where applicable.
"""

import math

# =============================================================================
# UNIVERSAL CONSTANTS
# =============================================================================

# Speed of light in vacuum (exact, defined value)
C = 299792458  # m/s (exact)
SPEED_OF_LIGHT = C

# Planck constant (exact, defined value)
H = 6.62607015e-34  # J*s (exact)
H_PLANCK = H
PLANCK_CONSTANT = H

# Reduced Planck constant (h-bar = h / 2*pi)
HBAR = H / (2 * math.pi)  # 1.054571817...e-34 J*s
H_BAR = HBAR
REDUCED_PLANCK_CONSTANT = HBAR

# Newtonian constant of gravitation
G = 6.67430e-11  # m^3 kg^-1 s^-2, uncertainty: 0.00015e-11
GRAVITATIONAL_CONSTANT = G

# Boltzmann constant (exact, defined value)
K_B = 1.380649e-23  # J/K (exact)
BOLTZMANN_CONSTANT = K_B

# =============================================================================
# ELECTROMAGNETIC CONSTANTS
# =============================================================================

# Elementary charge (exact, defined value)
E_CHARGE = 1.602176634e-19  # C (exact)
ELEMENTARY_CHARGE = E_CHARGE

# Vacuum electric permittivity
EPSILON_0 = 8.8541878188e-12  # F/m, uncertainty: 0.0000000014e-12

# Vacuum magnetic permeability
MU_0 = 1.25663706127e-6  # N/A^2, uncertainty: 0.00000000020e-6

# Fine-structure constant
ALPHA = 7.2973525643e-3  # dimensionless, uncertainty: 0.0000000011e-3
FINE_STRUCTURE_CONSTANT = ALPHA
ALPHA_INVERSE = 1 / ALPHA  # ~137.035999177

# =============================================================================
# ELECTRON PROPERTIES
# =============================================================================

# Electron mass
M_E = 9.1093837139e-31  # kg, uncertainty: 0.0000000028e-31
ELECTRON_MASS = M_E

# Electron mass energy equivalent (in MeV)
M_E_MEV = 0.51099895069  # MeV, uncertainty: 0.00000000016

# Classical electron radius (r_e = alpha^2 * a_0)
R_E = 2.8179403205e-15  # m, uncertainty: 0.0000000013e-15
CLASSICAL_ELECTRON_RADIUS = R_E

# Compton wavelength of electron
LAMBDA_COMPTON = 2.42631023538e-12  # m, uncertainty: 0.00000000076e-12
LAMBDA_C = LAMBDA_COMPTON  # Alias
ELECTRON_COMPTON_WAVELENGTH = LAMBDA_COMPTON

# Reduced Compton wavelength (lambda_C / 2*pi)
LAMBDA_COMPTON_BAR = LAMBDA_COMPTON / (2 * math.pi)  # ~3.8616e-13 m

# Bohr radius
A_0 = 5.29177210544e-11  # m, uncertainty: 0.00000000082e-11
BOHR_RADIUS = A_0

# Electron g-factor
G_ELECTRON = -2.00231930436092  # uncertainty: 0.00000000000036

# =============================================================================
# PROTON PROPERTIES
# =============================================================================

# Proton mass
M_P = 1.67262192595e-27  # kg, uncertainty: 0.00000000052e-27
PROTON_MASS = M_P

# Proton mass energy equivalent (in MeV)
M_P_MEV = 938.27208943  # MeV, uncertainty: 0.00000029

# Proton charge radius
R_PROTON = 8.4075e-16  # m, uncertainty: 0.0064e-16 (muonic hydrogen value)
PROTON_RADIUS = R_PROTON

# Proton Compton wavelength
LAMBDA_COMPTON_PROTON = 1.32140985360e-15  # m, uncertainty: 0.00000000041e-15

# Proton-electron mass ratio
M_P_OVER_M_E = 1836.152673426  # dimensionless, uncertainty: 0.000000032
PROTON_ELECTRON_MASS_RATIO = M_P_OVER_M_E

# =============================================================================
# NEUTRON PROPERTIES
# =============================================================================

# Neutron mass
M_N = 1.67492750056e-27  # kg, uncertainty: 0.00000000085e-27
NEUTRON_MASS = M_N

# Neutron mass energy equivalent (in MeV)
M_N_MEV = 939.56542194  # MeV, uncertainty: 0.00000048

# Neutron-proton mass difference
DELTA_M_NP = M_N - M_P  # ~2.3e-30 kg
DELTA_M_NP_MEV = M_N_MEV - M_P_MEV  # ~1.293 MeV

# =============================================================================
# PLANCK UNITS
# =============================================================================

# Planck length
L_PLANCK = 1.616255e-35  # m, uncertainty: 0.000018e-35
PLANCK_LENGTH = L_PLANCK

# Planck time
T_PLANCK = 5.391247e-44  # s, uncertainty: 0.000060e-44
PLANCK_TIME = T_PLANCK

# Planck mass
M_PLANCK = 2.176434e-8  # kg, uncertainty: 0.000024e-8
PLANCK_MASS = M_PLANCK

# Planck temperature
TEMP_PLANCK = 1.416784e32  # K, uncertainty: 0.000016e32
PLANCK_TEMPERATURE = TEMP_PLANCK

# Planck energy
E_PLANCK = M_PLANCK * C**2  # ~1.956e9 J
PLANCK_ENERGY = E_PLANCK

# =============================================================================
# ASTRONOMICAL CONSTANTS
# =============================================================================

# Solar mass (IAU 2015 nominal value)
M_SOLAR = 1.98841e30  # kg, uncertainty: ~0.00004e30
SOLAR_MASS = M_SOLAR

# Solar radius (IAU 2015 nominal value)
R_SOLAR = 6.957e8  # m
SOLAR_RADIUS = R_SOLAR

# Solar luminosity (IAU 2015 nominal value)
L_SOLAR = 3.828e26  # W
SOLAR_LUMINOSITY = L_SOLAR

# Astronomical unit (exact, defined value)
AU = 149597870700  # m (exact)
ASTRONOMICAL_UNIT = AU

# Parsec
PARSEC = 3.0856775814913673e16  # m

# =============================================================================
# OTHER USEFUL CONSTANTS
# =============================================================================

# Rydberg constant
R_INFINITY = 10973731.568157  # m^-1, uncertainty: 0.000012

# Stefan-Boltzmann constant
SIGMA_SB = 5.670374419e-8  # W m^-2 K^-4 (exact, derived)
STEFAN_BOLTZMANN = SIGMA_SB

# Avogadro constant (exact, defined value)
N_A = 6.02214076e23  # mol^-1 (exact)
AVOGADRO = N_A

# Atomic mass unit
AMU = 1.66053906892e-27  # kg, uncertainty: 0.00000000052e-27
ATOMIC_MASS_UNIT = AMU

# =============================================================================
# CONVERSION FACTORS
# =============================================================================

# Electron volt
EV = 1.602176634e-19  # J (exact, from e definition)
ELECTRON_VOLT = EV

# eV to kg conversion
EV_TO_KG = EV / C**2  # ~1.783e-36 kg/eV

# Joules to MeV
J_TO_MEV = 1 / (EV * 1e6)  # ~6.242e12 MeV/J

# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Universal
    "C", "SPEED_OF_LIGHT",
    "H", "H_PLANCK", "PLANCK_CONSTANT",
    "HBAR", "H_BAR", "REDUCED_PLANCK_CONSTANT",
    "G", "GRAVITATIONAL_CONSTANT",
    "K_B", "BOLTZMANN_CONSTANT",
    # Electromagnetic
    "E_CHARGE", "ELEMENTARY_CHARGE",
    "EPSILON_0", "MU_0",
    "ALPHA", "FINE_STRUCTURE_CONSTANT", "ALPHA_INVERSE",
    # Electron
    "M_E", "ELECTRON_MASS", "M_E_MEV",
    "R_E", "CLASSICAL_ELECTRON_RADIUS",
    "LAMBDA_COMPTON", "LAMBDA_C", "ELECTRON_COMPTON_WAVELENGTH", "LAMBDA_COMPTON_BAR",
    "A_0", "BOHR_RADIUS",
    "G_ELECTRON",
    # Proton
    "M_P", "PROTON_MASS", "M_P_MEV",
    "R_PROTON", "PROTON_RADIUS",
    "LAMBDA_COMPTON_PROTON",
    "M_P_OVER_M_E", "PROTON_ELECTRON_MASS_RATIO",
    # Neutron
    "M_N", "NEUTRON_MASS", "M_N_MEV",
    "DELTA_M_NP", "DELTA_M_NP_MEV",
    # Planck units
    "L_PLANCK", "PLANCK_LENGTH",
    "T_PLANCK", "PLANCK_TIME",
    "M_PLANCK", "PLANCK_MASS",
    "TEMP_PLANCK", "PLANCK_TEMPERATURE",
    "E_PLANCK", "PLANCK_ENERGY",
    # Astronomical
    "M_SOLAR", "SOLAR_MASS",
    "R_SOLAR", "SOLAR_RADIUS",
    "L_SOLAR", "SOLAR_LUMINOSITY",
    "AU", "ASTRONOMICAL_UNIT",
    "PARSEC",
    # Other
    "R_INFINITY",
    "SIGMA_SB", "STEFAN_BOLTZMANN",
    "N_A", "AVOGADRO",
    "AMU", "ATOMIC_MASS_UNIT",
    # Conversions
    "EV", "ELECTRON_VOLT",
    "EV_TO_KG", "J_TO_MEV",
]
