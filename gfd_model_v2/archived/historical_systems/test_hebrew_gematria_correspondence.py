"""
DFP Framework | Gravity Field Dynamics (GFD) Model
--------------------------------------------------
HISTORICAL SYSTEMS: Hebrew Gematria Correspondence Documentation

PURPOSE: Document the mathematical correspondence between Hebrew Gematria
values and the stellated octahedron (Merkabah) geometry. This follows the
scientific practice of recording all potentially relevant historical
correspondences for completeness.

GEMATRIA SYSTEM:
Hebrew Gematria (Mispar Hechrachi) assigns numerical values to each letter
of the 22-letter Hebrew alphabet:
    Units (1-9):    Aleph=1, Bet=2, Gimel=3, Dalet=4, Heh=5, Vav=6, Zayin=7, Chet=8, Tet=9
    Tens (10-90):   Yod=10, Kaf=20, Lamed=30, Mem=40, Nun=50, Samech=60, Ayin=70, Peh=80, Tsade=90
    Hundreds:       Qof=100, Resh=200, Shin=300, Tav=400

MERKABAH CALCULATION:
מרכבה (Mem-Resh-Kaf-Bet-Heh) = 40 + 200 + 20 + 2 + 5 = 267

CORRESPONDENCES AT 267:
Several Hebrew words share the gematria value 267:
    - מרכבה (Merkabah): "chariot, war chariot" - the divine vehicle in Ezekiel
    - נזיר (Nazir): "consecrated one, Nazarite, prince"
    - אסור (Asur): "bond, fetter"

HISTORICAL CONTEXT:
The Merkabah (מרכבה) appears in Ezekiel 1:1-28 as the divine throne-chariot,
featuring four living creatures with four faces each, intersecting wheels
with eyes, and a sapphire throne. This vision became central to Jewish
mysticism (Ma'aseh Merkabah, "Works of the Chariot").

SCIENTIFIC NOTE:
This correspondence is documented following the practice of recording
historical mathematical relationships. The GFD model's stellated octahedron
structure is derived from physical principles (topology, k=4 closure) and
does not depend on this gematria correspondence.

REFERENCES:
- Strong's Hebrew 4818: מֶרְכָּבָה (merkabah)
- Bill Heidrick, Hebrew Gematria Dictionary
- Ezekiel 1:1-28, 10:1-22 (Biblical source)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# =============================================================================
# LOCAL HELPER FUNCTIONS (for standalone execution)
# =============================================================================

def print_test_header(title: str):
    """Print a formatted test header."""
    print()
    print("=" * 70)
    print(f"TEST: {title}")
    print("=" * 70)

def print_test_result(passed: bool, message: str):
    """Print a formatted test result."""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status}: {message}")

def print_test_summary(passed: int, failed: int):
    """Print test summary."""
    total = passed + failed
    print()
    print(f"Result: {passed}/{total} tests passed")
    print()

# =============================================================================
# HEBREW ALPHABET WITH GEMATRIA VALUES
# =============================================================================

# Standard Hebrew Gematria (Mispar Hechrachi)
HEBREW_LETTERS = {
    # Units (1-9)
    'aleph':   {'hebrew': 'א', 'value': 1,   'name': 'Aleph',   'meaning': 'ox, strength'},
    'bet':     {'hebrew': 'ב', 'value': 2,   'name': 'Bet',     'meaning': 'house'},
    'gimel':   {'hebrew': 'ג', 'value': 3,   'name': 'Gimel',   'meaning': 'camel'},
    'dalet':   {'hebrew': 'ד', 'value': 4,   'name': 'Dalet',   'meaning': 'door'},
    'heh':     {'hebrew': 'ה', 'value': 5,   'name': 'Heh',     'meaning': 'window, breath'},
    'vav':     {'hebrew': 'ו', 'value': 6,   'name': 'Vav',     'meaning': 'hook, nail'},
    'zayin':   {'hebrew': 'ז', 'value': 7,   'name': 'Zayin',   'meaning': 'weapon, sword'},
    'chet':    {'hebrew': 'ח', 'value': 8,   'name': 'Chet',    'meaning': 'fence, enclosure'},
    'tet':     {'hebrew': 'ט', 'value': 9,   'name': 'Tet',     'meaning': 'serpent, surround'},
    # Tens (10-90)
    'yod':     {'hebrew': 'י', 'value': 10,  'name': 'Yod',     'meaning': 'hand, work'},
    'kaf':     {'hebrew': 'כ', 'value': 20,  'name': 'Kaf',     'meaning': 'palm, open hand'},
    'lamed':   {'hebrew': 'ל', 'value': 30,  'name': 'Lamed',   'meaning': 'staff, goad'},
    'mem':     {'hebrew': 'מ', 'value': 40,  'name': 'Mem',     'meaning': 'water'},
    'nun':     {'hebrew': 'נ', 'value': 50,  'name': 'Nun',     'meaning': 'fish, life'},
    'samech':  {'hebrew': 'ס', 'value': 60,  'name': 'Samech',  'meaning': 'support, prop'},
    'ayin':    {'hebrew': 'ע', 'value': 70,  'name': 'Ayin',    'meaning': 'eye, see'},
    'peh':     {'hebrew': 'פ', 'value': 80,  'name': 'Peh',     'meaning': 'mouth, speak'},
    'tsade':   {'hebrew': 'צ', 'value': 90,  'name': 'Tsade',   'meaning': 'fish hook, desire'},
    # Hundreds (100-400)
    'qof':     {'hebrew': 'ק', 'value': 100, 'name': 'Qof',     'meaning': 'back of head, cycle'},
    'resh':    {'hebrew': 'ר', 'value': 200, 'name': 'Resh',    'meaning': 'head, beginning'},
    'shin':    {'hebrew': 'ש', 'value': 300, 'name': 'Shin',    'meaning': 'tooth, consume'},
    'tav':     {'hebrew': 'ת', 'value': 400, 'name': 'Tav',     'meaning': 'mark, covenant'},
}

# Final letter forms (sofit) - higher values
FINAL_LETTERS = {
    'kaf_sofit':   {'hebrew': 'ך', 'value': 500, 'name': 'Final Kaf'},
    'mem_sofit':   {'hebrew': 'ם', 'value': 600, 'name': 'Final Mem'},
    'nun_sofit':   {'hebrew': 'ן', 'value': 700, 'name': 'Final Nun'},
    'peh_sofit':   {'hebrew': 'ף', 'value': 800, 'name': 'Final Peh'},
    'tsade_sofit': {'hebrew': 'ץ', 'value': 900, 'name': 'Final Tsade'},
}

# =============================================================================
# WORDS FOR ANALYSIS
# =============================================================================

# Hebrew words with their letter breakdowns
HEBREW_WORDS = {
    'merkabah': {
        'hebrew': 'מרכבה',
        'transliteration': 'Merkabah',
        'meaning': 'chariot, war chariot, divine vehicle',
        'letters': ['mem', 'resh', 'kaf', 'bet', 'heh'],
        'source': "Strong's Hebrew 4818; Ezekiel 1, 10",
        'context': 'The divine throne-chariot in Ezekiel\'s vision'
    },
    'nazir': {
        'hebrew': 'נזיר',
        'transliteration': 'Nazir',
        'meaning': 'consecrated one, Nazarite, prince',
        'letters': ['nun', 'zayin', 'yod', 'resh'],
        'source': "Strong's Hebrew 5139; Numbers 6",
        'context': 'One who takes a vow of consecration'
    },
    'asur': {
        'hebrew': 'אסור',
        'transliteration': 'Asur',
        'meaning': 'bond, fetter, binding',
        'letters': ['aleph', 'samech', 'vav', 'resh'],
        'source': "Bill Heidrick Gematria Dictionary",
        'context': 'That which binds or constrains'
    },
    'chamorei': {
        'hebrew': 'חמורי',
        'transliteration': 'Chamorei',
        'meaning': 'ass driver, donkey handler',
        'letters': ['chet', 'mem', 'vav', 'resh', 'yod'],
        'source': "Bill Heidrick Gematria Dictionary",
        'context': 'One who drives beasts of burden'
    },
}

# Words at other significant values
OTHER_SIGNIFICANT_WORDS = {
    # Value 8 (number of vertices)
    'chad': {'hebrew': 'חד', 'value': 12, 'meaning': 'one, sharp'},
    # Value 26 (Tetragrammaton YHVH)
    'yhvh': {'hebrew': 'יהוה', 'value': 26, 'meaning': 'The Name (YHVH)'},
    # Value 32 (total triads: 8 faces x 4)
    'lev': {'hebrew': 'לב', 'value': 32, 'meaning': 'heart'},
    # Value 72 (Shem HaMephorash - 72 names)
    'chesed': {'hebrew': 'חסד', 'value': 72, 'meaning': 'loving-kindness'},
}


def calculate_gematria(letters: list) -> int:
    """Calculate gematria value from list of letter names."""
    total = 0
    for letter in letters:
        if letter in HEBREW_LETTERS:
            total += HEBREW_LETTERS[letter]['value']
        elif letter in FINAL_LETTERS:
            total += FINAL_LETTERS[letter]['value']
    return total


def get_letter_breakdown(letters: list) -> str:
    """Get formatted breakdown of letter values."""
    parts = []
    for letter in letters:
        if letter in HEBREW_LETTERS:
            info = HEBREW_LETTERS[letter]
            parts.append(f"{info['hebrew']}({info['value']})")
    return " + ".join(parts)


# =============================================================================
# TESTS
# =============================================================================

def test_alphabet_completeness():
    """
    Verify the Hebrew alphabet has 22 letters with correct value structure.
    
    STRUCTURE:
    - 9 units (1-9): Aleph through Tet
    - 9 tens (10-90): Yod through Tsade
    - 4 hundreds (100-400): Qof through Tav
    - Total: 22 letters (like 22 paths on Tree of Life)
    
    The 22 letters encode 22 = 2 * 11, where 11 = number of sephiroth
    on the Tree of Life minus 1 (Daath).
    """
    letter_count = len(HEBREW_LETTERS)
    
    # Check structure
    units = [l for l, d in HEBREW_LETTERS.items() if d['value'] < 10]
    tens = [l for l, d in HEBREW_LETTERS.items() if 10 <= d['value'] < 100]
    hundreds = [l for l, d in HEBREW_LETTERS.items() if d['value'] >= 100]
    
    structure_correct = len(units) == 9 and len(tens) == 9 and len(hundreds) == 4
    
    passed = letter_count == 22 and structure_correct
    print_test_result(passed, f"Hebrew alphabet: {letter_count} letters (9 units + 9 tens + 4 hundreds)")
    
    return passed


def test_merkabah_gematria():
    """
    Calculate and verify the gematria value of Merkabah (מרכבה).
    
    CALCULATION:
    מ (Mem)   = 40
    ר (Resh)  = 200
    כ (Kaf)   = 20
    ב (Bet)   = 2
    ה (Heh)   = 5
    ─────────────
    Total     = 267
    
    SIGNIFICANCE:
    Merkabah is the Hebrew word for "chariot" and specifically refers
    to the divine throne-chariot in Ezekiel's vision. It is also the
    name for the stellated octahedron (star tetrahedron) in sacred
    geometry traditions.
    """
    word = HEBREW_WORDS['merkabah']
    calculated = calculate_gematria(word['letters'])
    breakdown = get_letter_breakdown(word['letters'])
    
    expected = 267
    
    passed = calculated == expected
    print_test_result(passed, f"Merkabah (מרכבה) gematria: {calculated}")
    print(f"    Calculation: {breakdown} = {calculated}")
    print(f"    Meaning: {word['meaning']}")
    print(f"    Source: {word['source']}")
    
    return passed


def test_nazir_gematria():
    """
    Calculate the gematria value of Nazir (נזיר) - "consecrated one".
    
    CALCULATION:
    נ (Nun)   = 50
    ז (Zayin) = 7
    י (Yod)   = 10
    ר (Resh)  = 200
    ─────────────
    Total     = 267
    
    CORRESPONDENCE:
    Both Merkabah (chariot) and Nazir (consecrated one) share the
    value 267. In mystical interpretation, this suggests a connection
    between the divine vehicle and consecrated individuals.
    
    BIBLICAL CONTEXT:
    The Nazarite vow (Numbers 6) involves:
    - Abstaining from wine and grapes
    - Not cutting hair
    - Avoiding contact with the dead
    Famous Nazarites: Samson, Samuel, John the Baptist
    """
    word = HEBREW_WORDS['nazir']
    calculated = calculate_gematria(word['letters'])
    breakdown = get_letter_breakdown(word['letters'])
    
    expected = 267
    
    passed = calculated == expected
    print_test_result(passed, f"Nazir (נזיר) gematria: {calculated}")
    print(f"    Calculation: {breakdown} = {calculated}")
    print(f"    Meaning: {word['meaning']}")
    print(f"    Context: {word['context']}")
    
    return passed


def test_asur_gematria():
    """
    Calculate the gematria value of Asur (אסור) - "bond, fetter".
    
    CALCULATION:
    א (Aleph)  = 1
    ס (Samech) = 60
    ו (Vav)    = 6
    ר (Resh)   = 200
    ─────────────
    Total      = 267
    
    CORRESPONDENCE:
    The word for "binding/constraint" shares gematria 267 with
    Merkabah. This could suggest the chariot as a structure that
    "binds" or contains the divine presence.
    """
    word = HEBREW_WORDS['asur']
    calculated = calculate_gematria(word['letters'])
    breakdown = get_letter_breakdown(word['letters'])
    
    expected = 267
    
    passed = calculated == expected
    print_test_result(passed, f"Asur (אסור) gematria: {calculated}")
    print(f"    Calculation: {breakdown} = {calculated}")
    print(f"    Meaning: {word['meaning']}")
    
    return passed


def test_267_correspondences():
    """
    Verify all words with gematria value 267 and document correspondences.
    
    INTERPRETATION:
    The shared gematria value 267 connects:
    - Merkabah (chariot): The divine vehicle/structure
    - Nazir (consecrated one): The purified individual
    - Asur (bond): The binding/containing principle
    
    Traditional gematria interpretation would see these as
    conceptually linked: the consecrated one (Nazir) is bound
    (Asur) to the divine chariot (Merkabah).
    
    SCIENTIFIC NOTE:
    This is documented as a mathematical curiosity. The GFD model
    derives the stellated octahedron from topology (k=4 closure),
    not from gematria. The correspondence is noted for completeness.
    """
    words_267 = []
    
    for name, word in HEBREW_WORDS.items():
        value = calculate_gematria(word['letters'])
        if value == 267:
            words_267.append((name, word))
    
    passed = len(words_267) >= 3
    print_test_result(passed, f"Words with gematria 267: {len(words_267)} found")
    
    print("\n    GEMATRIA 267 CORRESPONDENCES:")
    print("    " + "=" * 60)
    for name, word in words_267:
        print(f"    {word['hebrew']:>8} ({word['transliteration']:<12}) = {word['meaning']}")
    print("    " + "=" * 60)
    
    return passed


def test_geometric_number_correspondences():
    """
    Check if key geometric numbers have significant gematria correspondences.
    
    GFD MODEL NUMBERS:
    - 4: k=4 closure constant
    - 8: number of vertices (2k)
    - 32: total triads (8 faces x 4 regions)
    - 267: Merkabah value
    
    This tests whether these numbers have significance in Hebrew numerology.
    """
    print("\n    GEOMETRIC-GEMATRIA NUMBER ANALYSIS:")
    print("    " + "-" * 60)
    
    # 32 = Lev (heart)
    lev_value = HEBREW_LETTERS['lamed']['value'] + HEBREW_LETTERS['bet']['value']
    print(f"    32 = לב (Lev, 'heart') = {lev_value}")
    print(f"       GFD: 32 = 8 faces x 4 triads = total sampling regions")
    
    # 26 = YHVH
    yhvh_value = (HEBREW_LETTERS['yod']['value'] + HEBREW_LETTERS['heh']['value'] + 
                  HEBREW_LETTERS['vav']['value'] + HEBREW_LETTERS['heh']['value'])
    print(f"    26 = יהוה (YHVH, 'The Name') = {yhvh_value}")
    print(f"       Note: 26 = 2 x 13 (love, echad)")
    
    # 8 = Chet
    chet_value = HEBREW_LETTERS['chet']['value']
    print(f"     8 = ח (Chet, 'fence/enclosure') = {chet_value}")
    print(f"       GFD: 8 = number of vertices in stellated octahedron")
    
    # 4 = Dalet
    dalet_value = HEBREW_LETTERS['dalet']['value']
    print(f"     4 = ד (Dalet, 'door') = {dalet_value}")
    print(f"       GFD: k=4 = topological closure constant")
    
    print("    " + "-" * 60)
    
    passed = lev_value == 32 and yhvh_value == 26 and chet_value == 8 and dalet_value == 4
    print_test_result(passed, "Geometric numbers have Hebrew letter correspondences")
    
    return passed


def test_267_prime_factorization():
    """
    Analyze the prime factorization of 267.
    
    CALCULATION:
    267 = 3 x 89
    
    WHERE:
    - 3 = number of spatial dimensions
    - 89 = 24th prime number
    - 24 = number of edges in stellated octahedron (12 per tetrahedron x 2)
    
    DIGITAL ROOT:
    267 -> 2+6+7 = 15 -> 1+5 = 6
    6 = number of edges per tetrahedron
    """
    n = 267
    
    # Prime factorization
    factors = []
    temp = n
    divisor = 2
    while divisor * divisor <= temp:
        while temp % divisor == 0:
            factors.append(divisor)
            temp //= divisor
        divisor += 1
    if temp > 1:
        factors.append(temp)
    
    # Digital root
    digital_sum = sum(int(d) for d in str(n))
    digital_root = digital_sum
    while digital_root >= 10:
        digital_root = sum(int(d) for d in str(digital_root))
    
    # Check 89 is 24th prime
    def nth_prime(n):
        primes = []
        candidate = 2
        while len(primes) < n:
            is_prime = all(candidate % p != 0 for p in primes)
            if is_prime:
                primes.append(candidate)
            candidate += 1
        return primes[-1]
    
    prime_24 = nth_prime(24)
    
    passed = factors == [3, 89] and prime_24 == 89 and digital_root == 6
    print_test_result(passed, f"267 = {' x '.join(map(str, factors))}")
    print(f"    3 = spatial dimensions")
    print(f"    89 = 24th prime (24 = edges in stellated octahedron)")
    print(f"    Digital root: 2+6+7 = 15 -> 1+5 = 6 (edges per tetrahedron)")
    
    return passed


def test_print_full_analysis():
    """
    Print comprehensive gematria analysis for documentation.
    """
    print("\n  COMPREHENSIVE HEBREW GEMATRIA ANALYSIS")
    print("  " + "=" * 70)
    
    print("\n  MERKABAH (מרכבה) - THE DIVINE CHARIOT")
    print("  " + "-" * 70)
    print("  Biblical Source: Ezekiel 1:1-28, 10:1-22")
    print("  Description: Throne-chariot with four living creatures,")
    print("               intersecting wheels with eyes, sapphire throne")
    print("  Geometric Form: Stellated octahedron (star tetrahedron)")
    print("  Gematria Value: 267")
    
    print("\n  WORDS SHARING GEMATRIA VALUE 267:")
    print("  " + "-" * 70)
    print(f"  {'Hebrew':>10} | {'Name':>12} | {'Value':>6} | {'Meaning':<30}")
    print("  " + "-" * 70)
    
    for name, word in HEBREW_WORDS.items():
        value = calculate_gematria(word['letters'])
        if value == 267:
            print(f"  {word['hebrew']:>10} | {word['transliteration']:>12} | {value:>6} | {word['meaning']:<30}")
    
    print("  " + "-" * 70)
    
    print("\n  INTERPRETIVE CONNECTIONS:")
    print("  - Merkabah (chariot) + Nazir (consecrated) = the purified one rides")
    print("  - Merkabah (structure) + Asur (bond) = the binding structure")
    print("  - All three share 267 = 3 x 89 (3D structure, 24th prime)")
    
    print("\n  SCIENTIFIC DISCLAIMER:")
    print("  This gematria correspondence is documented for completeness.")
    print("  The GFD model derives the stellated octahedron from:")
    print("    - Topological closure (k=4)")
    print("    - Bimetric gravity (dual tetrahedra)")
    print("    - Field dynamics (NOT from Hebrew numerology)")
    print("  " + "=" * 70)
    
    return True


def run_all_tests():
    """Run all Hebrew gematria correspondence tests."""
    print_test_header("Hebrew Gematria Correspondence (Merkabah Analysis)")
    print("  Context: Documentation of Hebrew numerical correspondences")
    
    tests = [
        test_alphabet_completeness,
        test_merkabah_gematria,
        test_nazir_gematria,
        test_asur_gematria,
        test_267_correspondences,
        test_geometric_number_correspondences,
        test_267_prime_factorization,
        test_print_full_analysis,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_test_result(False, f"{test.__name__} raised exception: {e}")
            failed += 1
    
    print_test_summary(passed, failed)
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
