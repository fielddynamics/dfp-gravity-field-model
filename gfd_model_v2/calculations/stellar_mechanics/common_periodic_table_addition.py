
# =============================================================================
# PERIODIC TABLE DATA
# =============================================================================
# Moved from test_valence_predictions.py and test_power_output.py so that all
# test modules share a single source of element data.
#
# USAGE: Append this entire block to the end of common.py
# =============================================================================

# Format: (symbol, name, Z, A, measured_radius_pm, valence)
# A = mass number = gravity field count in Tet B
# Radius = empirical atomic radius in picometers
# Valence = common oxidation state / valence electron count

ELEMENTS_118 = [
    # Period 1
    ("H",  "Hydrogen",      1,   1,   31, 1),
    ("He", "Helium",        2,   4,   28, 0),
    # Period 2
    ("Li", "Lithium",       3,   7,  152, 1),
    ("Be", "Beryllium",     4,   9,  112, 2),
    ("B",  "Boron",         5,  11,   87, 3),
    ("C",  "Carbon",        6,  12,   76, 4),
    ("N",  "Nitrogen",      7,  14,   71, 5),
    ("O",  "Oxygen",        8,  16,   66, 6),
    ("F",  "Fluorine",      9,  19,   57, 7),
    ("Ne", "Neon",         10,  20,   58, 0),
    # Period 3
    ("Na", "Sodium",       11,  23,  186, 1),
    ("Mg", "Magnesium",    12,  24,  160, 2),
    ("Al", "Aluminum",     13,  27,  143, 3),
    ("Si", "Silicon",      14,  28,  111, 4),
    ("P",  "Phosphorus",   15,  31,  107, 5),
    ("S",  "Sulfur",       16,  32,  105, 6),
    ("Cl", "Chlorine",     17,  35,  102, 7),
    ("Ar", "Argon",        18,  40,  106, 0),
    # Period 4
    ("K",  "Potassium",    19,  39,  227, 1),
    ("Ca", "Calcium",      20,  40,  197, 2),
    ("Sc", "Scandium",     21,  45,  162, 3),
    ("Ti", "Titanium",     22,  48,  147, 4),
    ("V",  "Vanadium",     23,  51,  134, 5),
    ("Cr", "Chromium",     24,  52,  128, 6),
    ("Mn", "Manganese",    25,  55,  127, 7),
    ("Fe", "Iron",         26,  56,  126, 2),
    ("Co", "Cobalt",       27,  59,  125, 3),
    ("Ni", "Nickel",       28,  58,  124, 2),
    ("Cu", "Copper",       29,  63,  128, 1),
    ("Zn", "Zinc",         30,  64,  134, 2),
    ("Ga", "Gallium",      31,  69,  135, 3),
    ("Ga", "Gallium",      31,  69,  135, 3),
    ("Ge", "Germanium",    32,  74,  122, 4),
    ("As", "Arsenic",      33,  75,  119, 5),
    ("Se", "Selenium",     34,  80,  120, 6),
    ("Br", "Bromine",      35,  79,  120, 7),
    ("Kr", "Krypton",      36,  84,  116, 0),
    # Period 5
    ("Rb", "Rubidium",     37,  85,  248, 1),
    ("Sr", "Strontium",    38,  88,  215, 2),
    ("Y",  "Yttrium",      39,  89,  180, 3),
    ("Zr", "Zirconium",    40,  90,  160, 4),
    ("Nb", "Niobium",      41,  93,  146, 5),
    ("Mo", "Molybdenum",   42,  98,  139, 6),
    ("Tc", "Technetium",   43,  98,  136, 7),
    ("Ru", "Ruthenium",    44, 102,  134, 8),
    ("Rh", "Rhodium",      45, 103,  134, 3),
    ("Pd", "Palladium",    46, 106,  137, 2),
    ("Ag", "Silver",       47, 107,  145, 1),
    ("Cd", "Cadmium",      48, 114,  152, 2),
    ("In", "Indium",       49, 115,  167, 3),
    ("Sn", "Tin",          50, 120,  140, 4),
    ("Sb", "Antimony",     51, 121,  139, 5),
    ("Te", "Tellurium",    52, 130,  138, 6),
    ("I",  "Iodine",       53, 127,  139, 7),
    ("Xe", "Xenon",        54, 132,  140, 0),
    # Period 6
    ("Cs", "Cesium",       55, 133,  265, 1),
    ("Ba", "Barium",       56, 138,  222, 2),
    ("La", "Lanthanum",    57, 139,  187, 3),
    ("Ce", "Cerium",       58, 140,  182, 4),
    ("Pr", "Praseodymium", 59, 141,  182, 3),
    ("Nd", "Neodymium",    60, 144,  181, 3),
    ("Pm", "Promethium",   61, 145,  183, 3),
    ("Sm", "Samarium",     62, 152,  180, 3),
    ("Eu", "Europium",     63, 153,  180, 3),
    ("Gd", "Gadolinium",   64, 158,  180, 3),
    ("Tb", "Terbium",      65, 159,  177, 3),
    ("Dy", "Dysprosium",   66, 164,  178, 3),
    ("Ho", "Holmium",      67, 165,  176, 3),
    ("Er", "Erbium",       68, 166,  176, 3),
    ("Tm", "Thulium",      69, 169,  176, 3),
    ("Yb", "Ytterbium",    70, 174,  176, 3),
    ("Lu", "Lutetium",     71, 175,  174, 3),
    ("Hf", "Hafnium",      72, 180,  159, 4),
    ("Ta", "Tantalum",     73, 181,  146, 5),
    ("W",  "Tungsten",     74, 184,  139, 6),
    ("Re", "Rhenium",      75, 187,  137, 7),
    ("Os", "Osmium",       76, 192,  135, 8),
    ("Ir", "Iridium",      77, 193,  136, 4),
    ("Pt", "Platinum",     78, 195,  139, 4),
    ("Au", "Gold",         79, 197,  136, 1),
    ("Hg", "Mercury",      80, 202,  151, 2),
    ("Tl", "Thallium",     81, 205,  170, 3),
    ("Pb", "Lead",         82, 208,  146, 4),
    ("Bi", "Bismuth",      83, 209,  148, 5),
    ("Po", "Polonium",     84, 209,  140, 6),
    ("At", "Astatine",     85, 210,  150, 7),
    ("Rn", "Radon",        86, 222,  150, 0),
    # Period 7
    ("Fr", "Francium",     87, 223,  260, 1),
    ("Ra", "Radium",       88, 226,  221, 2),
    ("Ac", "Actinium",     89, 227,  215, 3),
    ("Th", "Thorium",      90, 232,  206, 4),
    ("Pa", "Protactinium", 91, 231,  200, 5),
    ("U",  "Uranium",      92, 238,  196, 6),
    ("Np", "Neptunium",    93, 237,  190, 5),
    ("Pu", "Plutonium",    94, 244,  187, 4),
    ("Am", "Americium",    95, 243,  180, 3),
    ("Cm", "Curium",       96, 247,  169, 3),
    ("Bk", "Berkelium",    97, 247,  170, 3),
    ("Cf", "Californium",  98, 251,  170, 3),
    ("Es", "Einsteinium",  99, 252,  170, 3),
    ("Fm", "Fermium",     100, 257,  170, 3),
    ("Md", "Mendelevium", 101, 258,  170, 3),
    ("No", "Nobelium",    102, 259,  170, 2),
    ("Lr", "Lawrencium",  103, 262,  170, 3),
    ("Rf", "Rutherfordium",104, 267, 157, 4),
    ("Db", "Dubnium",     105, 268,  149, 5),
    ("Sg", "Seaborgium",  106, 269,  143, 6),
    ("Bh", "Bohrium",     107, 270,  141, 7),
    ("Hs", "Hassium",     108, 277,  134, 8),
    ("Mt", "Meitnerium",  109, 278,  129, 3),
    ("Ds", "Darmstadtium",110, 281,  128, 2),
    ("Rg", "Roentgenium", 111, 282,  121, 1),
    ("Cn", "Copernicium", 112, 285,  122, 2),
    ("Nh", "Nihonium",    113, 286,  136, 3),
    ("Fl", "Flerovium",   114, 289,  143, 4),
    ("Mc", "Moscovium",   115, 290,  162, 3),
    ("Lv", "Livermorium", 116, 293,  175, 2),
    ("Ts", "Tennessine",  117, 294,  165, 1),
    ("Og", "Oganesson",   118, 294,  157, 0),
]


# Binding energies per nucleon (MeV) — keyed by mass number A
# Source: Nuclear physics data (CODATA/AME2020)
BINDING_ENERGIES_BY_A = {
    # Period 1
    1: 0.000,    # H-1 (reference, no binding)
    4: 7.074,    # He-4 (alpha particle) - 1k
    # Period 2
    7: 5.606, 9: 6.463, 11: 6.928,
    12: 7.680, 14: 7.476, 16: 7.976, 19: 7.779, 20: 8.032,
    # Period 3
    23: 8.111, 24: 8.261, 27: 8.331, 28: 8.448, 31: 8.448,
    32: 8.493, 35: 8.520, 40: 8.551,
    # Period 4
    39: 8.557, 45: 8.619, 48: 8.643, 51: 8.656, 52: 8.664,
    55: 8.765, 56: 8.790,   # Fe-56 - 14k (MAXIMUM!)
    59: 8.768, 58: 8.732, 63: 8.752, 64: 8.736, 69: 8.705,
    74: 8.697, 75: 8.702, 80: 8.697, 79: 8.696, 84: 8.700,
    # Period 5
    85: 8.697, 88: 8.686, 89: 8.680, 90: 8.671, 93: 8.662,
    98: 8.636, 102: 8.613, 103: 8.605, 106: 8.586, 107: 8.579,
    114: 8.544, 115: 8.538, 120: 8.505, 121: 8.497, 130: 8.431,
    127: 8.452, 132: 8.410,
    # Period 6
    133: 8.402, 138: 8.362, 139: 8.354, 140: 8.346, 141: 8.340,
    144: 8.320, 145: 8.314, 152: 8.263, 153: 8.257, 158: 8.222,
    159: 8.216, 164: 8.182, 165: 8.176, 166: 8.170, 169: 8.152,
    174: 8.120, 175: 8.114, 180: 8.082, 181: 8.077, 184: 8.059,
    187: 8.041, 192: 8.011, 193: 8.006, 195: 7.996, 197: 7.986,
    202: 7.961, 205: 7.945, 208: 7.867, 209: 7.848, 210: 7.834,
    222: 7.742,
    # Period 7
    223: 7.735, 226: 7.716, 227: 7.710, 232: 7.615, 231: 7.620,
    238: 7.570, 237: 7.575, 244: 7.540, 243: 7.545, 247: 7.520,
    251: 7.495, 252: 7.490, 257: 7.465, 258: 7.460, 259: 7.455,
    262: 7.440, 267: 7.415, 268: 7.410, 269: 7.405, 270: 7.400,
    277: 7.365, 278: 7.360, 281: 7.345, 282: 7.340, 285: 7.325,
    286: 7.320, 289: 7.305, 290: 7.300, 293: 7.285, 294: 7.280,
}


# Ionization energies (eV) for key elements
IONIZATION_ENERGIES = {
    'H': 13.60, 'He': 24.59, 'Li': 5.39, 'Be': 9.32, 'B': 8.30, 'C': 11.26,
    'N': 14.53, 'O': 13.62, 'F': 17.42, 'Ne': 21.56, 'Na': 5.14, 'Mg': 7.65,
    'Al': 5.99, 'Si': 8.15, 'P': 10.49, 'S': 10.36, 'Cl': 12.97, 'Ar': 15.76,
    'K': 4.34, 'Ca': 6.11, 'Fe': 7.90, 'Kr': 14.00, 'Ag': 7.58, 'Au': 9.23,
    'Pb': 7.42, 'U': 6.19,
}


# Pauling electronegativities for key elements
ELECTRONEGATIVITIES = {
    'H': 2.20, 'Li': 0.98, 'Be': 1.57, 'B': 2.04, 'C': 2.55, 'N': 3.04,
    'O': 3.44, 'F': 3.98, 'Na': 0.93, 'Mg': 1.31, 'Al': 1.61, 'Si': 1.90,
    'P': 2.19, 'S': 2.58, 'Cl': 3.16, 'K': 0.82, 'Ca': 1.00, 'Fe': 1.83,
    'Kr': 3.00, 'Ag': 1.93, 'Au': 2.54, 'Pb': 2.33, 'U': 1.38,
}


# Derived: ATOMIC_DATA dict keyed by symbol for quick lookups
# Format: symbol -> (Z, A, radius_pm, ionization_eV, electronegativity, valence)
ATOMIC_DATA = {}
for _sym, _name, _z, _a, _r, _val in ELEMENTS_118:
    _ie = IONIZATION_ENERGIES.get(_sym)
    _en = ELECTRONEGATIVITIES.get(_sym)
    ATOMIC_DATA[_sym] = (_z, _a, _r, _ie, _en, _val)


def get_binding_energy_by_A(A):
    """Get binding energy per nucleon (MeV) for mass number A.

    Exact lookup when A is in BINDING_ENERGIES_BY_A, otherwise a smooth
    interpolation that follows the nuclear binding energy curve.
    """
    if A in BINDING_ENERGIES_BY_A:
        return BINDING_ENERGIES_BY_A[A]
    # Interpolation fallback
    if A <= 2:   return 1.1
    if A <= 30:  return 7.5 + (A - 10) * 0.05
    if A <= 62:  return 8.5 + (62 - abs(A - 56)) * 0.01
    if A <= 150: return 8.0 - (A - 62) * 0.003
    return 7.8 - (A - 150) * 0.003
