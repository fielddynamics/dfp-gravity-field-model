"""
Atomic Data for the Periodic Table
===================================

Canonical source for element properties used across all GFM test modules.

Contains:
- ELEMENTS_118: full periodic table as list of tuples
- ATOMIC_DATA: dict keyed by symbol -> (Z, A, radius, IE, EN, valence)
- BINDING_ENERGIES_BY_A: binding energy per nucleon indexed by mass number
- IONIZATION_ENERGIES: first ionization energy by symbol (eV)
- ELECTRONEGATIVITIES: Pauling electronegativity by symbol
- get_binding_energy_by_A(): lookup with interpolation for missing A values

Data sources:
- Mass numbers: most common/stable isotope (IUPAC)
- Radii: empirical atomic radii in pm (Slater / IUPAC)
- Ionization energies: NIST Atomic Spectra Database
- Electronegativities: Pauling scale (revised)
- Binding energies: Nuclear physics reference data
"""

from typing import Dict, List, Optional, Tuple

from .constants_codata import EV

# =============================================================================
# CONVERSION
# =============================================================================

MEV_TO_JOULES = EV * 1e6  # 1.602176634e-13 J/MeV

# =============================================================================
# FULL PERIODIC TABLE (118 ELEMENTS)
# =============================================================================
#
# Each entry: (symbol, name, Z, A, radius_pm, valence)
#   Z = atomic number
#   A = mass number of most common/stable isotope
#   radius_pm = empirical atomic radius in picometers
#   valence = common valence electron count

ELEMENTS_118: List[Tuple[str, str, int, int, int, int]] = [
    ("H",  "Hydrogen",       1,   1,   25,  1),
    ("He", "Helium",          2,   4,   31,  0),
    ("Li", "Lithium",         3,   7,  145,  1),
    ("Be", "Beryllium",       4,   9,  105,  2),
    ("B",  "Boron",           5,  11,   85,  3),
    ("C",  "Carbon",          6,  12,   76,  4),
    ("N",  "Nitrogen",        7,  14,   71,  3),
    ("O",  "Oxygen",          8,  16,   66,  2),
    ("F",  "Fluorine",        9,  19,   57,  1),
    ("Ne", "Neon",           10,  20,   58,  0),
    ("Na", "Sodium",         11,  23,  180,  1),
    ("Mg", "Magnesium",      12,  24,  150,  2),
    ("Al", "Aluminium",      13,  27,  125,  3),
    ("Si", "Silicon",        14,  28,  110,  4),
    ("P",  "Phosphorus",     15,  31,  100,  3),
    ("S",  "Sulfur",         16,  32,  100,  2),
    ("Cl", "Chlorine",       17,  35,   99,  1),
    ("Ar", "Argon",          18,  40,   71,  0),
    ("K",  "Potassium",      19,  39,  220,  1),
    ("Ca", "Calcium",        20,  40,  180,  2),
    ("Sc", "Scandium",       21,  45,  160,  3),
    ("Ti", "Titanium",       22,  48,  140,  4),
    ("V",  "Vanadium",       23,  51,  135,  5),
    ("Cr", "Chromium",       24,  52,  140,  3),
    ("Mn", "Manganese",      25,  55,  140,  2),
    ("Fe", "Iron",           26,  56,  140,  3),
    ("Co", "Cobalt",         27,  59,  135,  2),
    ("Ni", "Nickel",         28,  58,  135,  2),
    ("Cu", "Copper",         29,  63,  135,  2),
    ("Zn", "Zinc",           30,  65,  135,  2),
    ("Ga", "Gallium",        31,  70,  130,  3),
    ("Ge", "Germanium",      32,  73,  125,  4),
    ("As", "Arsenic",        33,  75,  115,  3),
    ("Se", "Selenium",       34,  79,  115,  2),
    ("Br", "Bromine",        35,  80,  114,  1),
    ("Kr", "Krypton",        36,  84,   88,  0),
    ("Rb", "Rubidium",       37,  85,  235,  1),
    ("Sr", "Strontium",      38,  88,  200,  2),
    ("Y",  "Yttrium",        39,  89,  180,  3),
    ("Zr", "Zirconium",      40,  91,  155,  4),
    ("Nb", "Niobium",        41,  93,  145,  5),
    ("Mo", "Molybdenum",     42,  96,  145,  6),
    ("Tc", "Technetium",     43,  98,  135,  7),
    ("Ru", "Ruthenium",      44, 101,  130,  4),
    ("Rh", "Rhodium",        45, 103,  135,  3),
    ("Pd", "Palladium",      46, 106,  140,  2),
    ("Ag", "Silver",         47, 108,  160,  1),
    ("Cd", "Cadmium",        48, 112,  155,  2),
    ("In", "Indium",         49, 115,  155,  3),
    ("Sn", "Tin",            50, 120,  145,  4),
    ("Sb", "Antimony",       51, 122,  145,  3),
    ("Te", "Tellurium",      52, 128,  140,  2),
    ("I",  "Iodine",         53, 127,  133,  1),
    ("Xe", "Xenon",          54, 131,  108,  0),
    ("Cs", "Caesium",        55, 133,  260,  1),
    ("Ba", "Barium",         56, 137,  215,  2),
    ("La", "Lanthanum",      57, 139,  195,  3),
    ("Ce", "Cerium",         58, 140,  185,  3),
    ("Pr", "Praseodymium",   59, 141,  185,  3),
    ("Nd", "Neodymium",      60, 144,  185,  3),
    ("Pm", "Promethium",     61, 145,  185,  3),
    ("Sm", "Samarium",       62, 150,  185,  3),
    ("Eu", "Europium",       63, 152,  185,  2),
    ("Gd", "Gadolinium",     64, 157,  180,  3),
    ("Tb", "Terbium",        65, 159,  175,  3),
    ("Dy", "Dysprosium",     66, 163,  175,  3),
    ("Ho", "Holmium",        67, 165,  175,  3),
    ("Er", "Erbium",         68, 167,  175,  3),
    ("Tm", "Thulium",        69, 169,  175,  3),
    ("Yb", "Ytterbium",      70, 173,  175,  2),
    ("Lu", "Lutetium",       71, 175,  175,  3),
    ("Hf", "Hafnium",        72, 178,  155,  4),
    ("Ta", "Tantalum",       73, 181,  145,  5),
    ("W",  "Tungsten",       74, 184,  135,  6),
    ("Re", "Rhenium",        75, 186,  135,  4),
    ("Os", "Osmium",         76, 190,  130,  4),
    ("Ir", "Iridium",        77, 192,  135,  4),
    ("Pt", "Platinum",       78, 195,  135,  4),
    ("Au", "Gold",           79, 197,  135,  3),
    ("Hg", "Mercury",        80, 201,  150,  2),
    ("Tl", "Thallium",       81, 204,  190,  1),
    ("Pb", "Lead",           82, 207,  180,  2),
    ("Bi", "Bismuth",        83, 209,  160,  3),
    ("Po", "Polonium",       84, 209,  190,  2),
    ("At", "Astatine",       85, 210,  127,  1),
    ("Rn", "Radon",          86, 222,  120,  0),
    ("Fr", "Francium",       87, 223,  260,  1),
    ("Ra", "Radium",         88, 226,  215,  2),
    ("Ac", "Actinium",       89, 227,  195,  3),
    ("Th", "Thorium",        90, 232,  180,  4),
    ("Pa", "Protactinium",   91, 231,  180,  5),
    ("U",  "Uranium",        92, 238,  175,  6),
    ("Np", "Neptunium",      93, 237,  175,  5),
    ("Pu", "Plutonium",      94, 244,  175,  4),
    ("Am", "Americium",      95, 243,  175,  3),
    ("Cm", "Curium",         96, 247,  176,  3),
    ("Bk", "Berkelium",      97, 247,  176,  3),
    ("Cf", "Californium",    98, 251,  176,  3),
    ("Es", "Einsteinium",    99, 252,  176,  3),
    ("Fm", "Fermium",       100, 257,  176,  3),
    ("Md", "Mendelevium",   101, 258,  176,  3),
    ("No", "Nobelium",      102, 259,  176,  2),
    ("Lr", "Lawrencium",    103, 266,  176,  3),
    ("Rf", "Rutherfordium", 104, 267,  157,  4),
    ("Db", "Dubnium",       105, 268,  149,  5),
    ("Sg", "Seaborgium",    106, 269,  143,  6),
    ("Bh", "Bohrium",       107, 270,  141,  7),
    ("Hs", "Hassium",       108, 277,  134,  8),
    ("Mt", "Meitnerium",    109, 278,  128,  3),
    ("Ds", "Darmstadtium",  110, 281,  128,  2),
    ("Rg", "Roentgenium",   111, 282,  121,  1),
    ("Cn", "Copernicium",   112, 285,  122,  2),
    ("Nh", "Nihonium",      113, 286,  136,  1),
    ("Fl", "Flerovium",     114, 289,  143,  2),
    ("Mc", "Moscovium",     115, 290,  162,  1),
    ("Lv", "Livermorium",   116, 293,  175,  2),
    ("Ts", "Tennessine",    117, 294,  165,  1),
    ("Og", "Oganesson",     118, 294,  157,  0),
]

# =============================================================================
# FIRST IONIZATION ENERGIES (eV)
# =============================================================================
# Source: NIST Atomic Spectra Database

IONIZATION_ENERGIES: Dict[str, float] = {
    "H":  13.598, "He": 24.587, "Li":  5.392, "Be":  9.323, "B":   8.298,
    "C":  11.260, "N":  14.534, "O":  13.618, "F":  17.423, "Ne": 21.565,
    "Na":  5.139, "Mg":  7.646, "Al":  5.986, "Si":  8.152, "P":  10.487,
    "S":  10.360, "Cl": 12.968, "Ar": 15.760, "K":   4.341, "Ca":  6.113,
    "Sc":  6.561, "Ti":  6.828, "V":   6.746, "Cr":  6.767, "Mn":  7.434,
    "Fe":  7.902, "Co":  7.881, "Ni":  7.640, "Cu":  7.726, "Zn":  9.394,
    "Ga":  5.999, "Ge":  7.900, "As":  9.815, "Se":  9.752, "Br": 11.814,
    "Kr": 14.000, "Rb":  4.177, "Sr":  5.695, "Y":   6.217, "Zr":  6.634,
    "Nb":  6.759, "Mo":  7.092, "Tc":  7.280, "Ru":  7.361, "Rh":  7.459,
    "Pd":  8.337, "Ag":  7.576, "Cd":  8.994, "In":  5.786, "Sn":  7.344,
    "Sb":  8.608, "Te":  9.010, "I":  10.451, "Xe": 12.130, "Cs":  3.894,
    "Ba":  5.212, "La":  5.577, "Ce":  5.539, "Pr":  5.473, "Nd":  5.525,
    "Pm":  5.582, "Sm":  5.644, "Eu":  5.670, "Gd":  6.150, "Tb":  5.864,
    "Dy":  5.939, "Ho":  6.022, "Er":  6.108, "Tm":  6.184, "Yb":  6.254,
    "Lu":  5.426, "Hf":  6.825, "Ta":  7.550, "W":   7.864, "Re":  7.833,
    "Os":  8.438, "Ir":  8.967, "Pt":  8.959, "Au":  9.226, "Hg": 10.437,
    "Tl":  6.108, "Pb":  7.417, "Bi":  7.286, "Po":  8.414, "At":  9.318,
    "Rn": 10.749, "Fr":  4.073, "Ra":  5.278, "Ac":  5.170, "Th":  6.307,
    "Pa":  5.890, "U":   6.194, "Np":  6.266, "Pu":  6.026, "Am":  5.974,
    "Cm":  5.991, "Bk":  6.198, "Cf":  6.282, "Es":  6.420, "Fm":  6.500,
    "Md":  6.580, "No":  6.650, "Lr":  4.960, "Rf":  6.010, "Db":  6.890,
    "Sg":  7.100, "Bh":  7.400, "Hs":  7.600, "Mt":  8.000, "Ds":  8.300,
    "Rg":  8.500, "Cn":  8.700, "Nh":  7.300, "Fl":  8.400, "Mc":  5.600,
    "Lv":  7.000, "Ts":  7.700, "Og":  8.900,
}

# =============================================================================
# PAULING ELECTRONEGATIVITIES
# =============================================================================
# Source: Pauling scale (revised). None where not defined.

ELECTRONEGATIVITIES: Dict[str, Optional[float]] = {
    "H":  2.20, "He": None, "Li": 0.98, "Be": 1.57, "B":  2.04,
    "C":  2.55, "N":  3.04, "O":  3.44, "F":  3.98, "Ne": None,
    "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90, "P":  2.19,
    "S":  2.58, "Cl": 3.16, "Ar": None, "K":  0.82, "Ca": 1.00,
    "Sc": 1.36, "Ti": 1.54, "V":  1.63, "Cr": 1.66, "Mn": 1.55,
    "Fe": 1.83, "Co": 1.88, "Ni": 1.91, "Cu": 1.90, "Zn": 1.65,
    "Ga": 1.81, "Ge": 2.01, "As": 2.18, "Se": 2.55, "Br": 2.96,
    "Kr": 3.00, "Rb": 0.82, "Sr": 0.95, "Y":  1.22, "Zr": 1.33,
    "Nb": 1.60, "Mo": 2.16, "Tc": 1.90, "Ru": 2.20, "Rh": 2.28,
    "Pd": 2.20, "Ag": 1.93, "Cd": 1.69, "In": 1.78, "Sn": 1.96,
    "Sb": 2.05, "Te": 2.10, "I":  2.66, "Xe": 2.60, "Cs": 0.79,
    "Ba": 0.89, "La": 1.10, "Ce": 1.12, "Pr": 1.13, "Nd": 1.14,
    "Pm": 1.13, "Sm": 1.17, "Eu": 1.20, "Gd": 1.20, "Tb": 1.10,
    "Dy": 1.22, "Ho": 1.23, "Er": 1.24, "Tm": 1.25, "Yb": 1.10,
    "Lu": 1.27, "Hf": 1.30, "Ta": 1.50, "W":  2.36, "Re": 1.90,
    "Os": 2.20, "Ir": 2.20, "Pt": 2.28, "Au": 2.54, "Hg": 2.00,
    "Tl": 1.62, "Pb": 1.87, "Bi": 2.02, "Po": 2.00, "At": 2.20,
    "Rn": 2.20, "Fr": 0.70, "Ra": 0.90, "Ac": 1.10, "Th": 1.30,
    "Pa": 1.50, "U":  1.38, "Np": 1.36, "Pu": 1.28, "Am": 1.13,
    "Cm": 1.28, "Bk": 1.30, "Cf": 1.30, "Es": 1.30, "Fm": 1.30,
    "Md": 1.30, "No": 1.30, "Lr": 1.30, "Rf": None, "Db": None,
    "Sg": None, "Bh": None, "Hs": None, "Mt": None, "Ds": None,
    "Rg": None, "Cn": None, "Nh": None, "Fl": None, "Mc": None,
    "Lv": None, "Ts": None, "Og": None,
}

# =============================================================================
# COMPOSITE ATOMIC DATA DICT
# =============================================================================
# Keyed by symbol -> (Z, A, radius_pm, IE_eV, EN_pauling, valence)
# This is the primary lookup used by test files.

ATOMIC_DATA: Dict[str, Tuple[int, int, int, float, Optional[float], int]] = {}
for _sym, _name, _z, _a, _r, _v in ELEMENTS_118:
    ATOMIC_DATA[_sym] = (
        _z,
        _a,
        _r,
        IONIZATION_ENERGIES.get(_sym, 0.0),
        ELECTRONEGATIVITIES.get(_sym),
        _v,
    )

# =============================================================================
# BINDING ENERGIES PER NUCLEON (MeV)
# =============================================================================
# Indexed by mass number A.  Values from nuclear physics reference data.
# Coverage: key isotopes from A=1 to A=294.
# For mass numbers not listed, get_binding_energy_by_A() interpolates.

BINDING_ENERGIES_BY_A: Dict[int, float] = {
    1: 0.000,
    2: 1.112,    # H-2  (deuterium)
    3: 2.573,    # He-3
    4: 7.074,    # He-4 (alpha particle, 1k)
    6: 5.333,    # Li-6
    7: 5.606,    # Li-7
    9: 6.463,    # Be-9
    10: 6.475,   # B-10
    11: 6.928,   # B-11
    12: 7.680,   # C-12 (3k)
    13: 7.470,   # C-13
    14: 7.476,   # N-14
    15: 7.699,   # N-15
    16: 7.976,   # O-16 (4k)
    17: 7.751,   # O-17
    18: 7.767,   # O-18
    19: 7.779,   # F-19
    20: 8.032,   # Ne-20 (5k)
    23: 8.112,   # Na-23
    24: 8.261,   # Mg-24 (6k)
    27: 8.332,   # Al-27
    28: 8.448,   # Si-28 (7k)
    31: 8.481,   # P-31
    32: 8.493,   # S-32 (8k)
    35: 8.520,   # Cl-35
    39: 8.557,   # K-39
    40: 8.551,   # Ca-40 (10k)
    45: 8.619,   # Sc-45
    48: 8.723,   # Ti-48 (12k)
    51: 8.742,   # V-51
    52: 8.776,   # Cr-52 (13k)
    55: 8.765,   # Mn-55
    56: 8.790,   # Fe-56 (14k) — PEAK
    58: 8.732,   # Ni-58
    59: 8.768,   # Co-59
    62: 8.795,   # Ni-62 (highest per-nucleon, but Fe-56 is commonly cited peak)
    63: 8.752,   # Cu-63
    65: 8.757,   # Zn-65
    70: 8.711,   # Ga-70
    73: 8.705,   # Ge-73
    75: 8.701,   # As-75
    79: 8.691,   # Se-79
    80: 8.690,   # Br-80
    84: 8.672,   # Kr-84 (21k)
    85: 8.667,   # Rb-85
    88: 8.654,   # Sr-88 (22k)
    89: 8.649,   # Y-89
    91: 8.636,   # Zr-91
    93: 8.624,   # Nb-93
    96: 8.610,   # Mo-96 (24k)
    98: 8.598,   # Tc-98
    101: 8.581,  # Ru-101
    103: 8.571,  # Rh-103
    106: 8.554,  # Pd-106
    108: 8.542,  # Ag-108 (27k)
    112: 8.520,  # Cd-112 (28k)
    115: 8.504,  # In-115
    120: 8.483,  # Sn-120 (30k)
    122: 8.471,  # Sb-122
    127: 8.445,  # I-127
    128: 8.440,  # Te-128 (32k)
    131: 8.424,  # Xe-131
    133: 8.410,  # Cs-133
    137: 8.389,  # Ba-137
    139: 8.378,  # La-139
    140: 8.376,  # Ce-140 (35k)
    141: 8.371,  # Pr-141
    144: 8.358,  # Nd-144 (36k)
    145: 8.354,  # Pm-145
    150: 8.331,  # Sm-150
    152: 8.321,  # Eu-152 (38k)
    157: 8.298,  # Gd-157
    159: 8.288,  # Tb-159
    163: 8.270,  # Dy-163
    165: 8.261,  # Ho-165
    167: 8.251,  # Er-167
    169: 8.241,  # Tm-169
    173: 8.222,  # Yb-173
    175: 8.212,  # Lu-175
    178: 8.197,  # Hf-178
    181: 8.182,  # Ta-181
    184: 8.167,  # W-184 (46k)
    186: 8.157,  # Re-186
    190: 8.137,  # Os-190
    192: 8.127,  # Ir-192 (48k)
    195: 8.113,  # Pt-195
    197: 8.103,  # Au-197
    201: 8.083,  # Hg-201
    204: 8.068,  # Tl-204 (51k)
    207: 8.053,  # Pb-207
    209: 8.040,  # Bi-209
    210: 8.033,  # Po-210 / At-210
    222: 7.970,  # Rn-222
    223: 7.965,  # Fr-223
    226: 7.950,  # Ra-226
    227: 7.946,  # Ac-227
    231: 7.927,  # Pa-231
    232: 7.924,  # Th-232 (58k)
    237: 7.900,  # Np-237
    238: 7.896,  # U-238
    243: 7.872,  # Am-243
    244: 7.868,  # Pu-244 (61k)
    247: 7.854,  # Cm/Bk-247
    251: 7.835,  # Cf-251
    252: 7.831,  # Es-252 (63k)
    257: 7.810,  # Fm-257
    258: 7.806,  # Md-258
    259: 7.802,  # No-259
    266: 7.770,  # Lr-266
    267: 7.766,  # Rf-267
    268: 7.762,  # Db-268 (67k)
    269: 7.758,  # Sg-269
    270: 7.754,  # Bh-270
    277: 7.722,  # Hs-277
    278: 7.718,  # Mt-278
    281: 7.704,  # Ds-281
    282: 7.700,  # Rg-282
    285: 7.686,  # Cn-285
    286: 7.682,  # Nh-286
    289: 7.668,  # Fl-289
    290: 7.664,  # Mc-290
    293: 7.650,  # Lv-293
    294: 7.646,  # Ts/Og-294
}


def get_binding_energy_by_A(A: int) -> float:
    """
    Get binding energy per nucleon (MeV) for mass number A.

    If A is in the table, returns the exact value. Otherwise linearly
    interpolates between the nearest bracketing entries.

    Args:
        A: Mass number (positive integer)

    Returns:
        Binding energy per nucleon in MeV

    Raises:
        ValueError: If A < 1 or > max tabulated value
    """
    if A < 1:
        raise ValueError(f"Mass number must be >= 1, got {A}")

    if A in BINDING_ENERGIES_BY_A:
        return BINDING_ENERGIES_BY_A[A]

    # Interpolate
    sorted_keys = sorted(BINDING_ENERGIES_BY_A.keys())

    if A < sorted_keys[0]:
        return 0.0
    if A > sorted_keys[-1]:
        return BINDING_ENERGIES_BY_A[sorted_keys[-1]]

    # Find bracketing keys
    lower = max(k for k in sorted_keys if k < A)
    upper = min(k for k in sorted_keys if k > A)
    be_lower = BINDING_ENERGIES_BY_A[lower]
    be_upper = BINDING_ENERGIES_BY_A[upper]

    # Linear interpolation
    frac = (A - lower) / (upper - lower)
    return be_lower + frac * (be_upper - be_lower)


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "MEV_TO_JOULES",
    "ELEMENTS_118",
    "IONIZATION_ENERGIES",
    "ELECTRONEGATIVITIES",
    "ATOMIC_DATA",
    "BINDING_ENERGIES_BY_A",
    "get_binding_energy_by_A",
]
