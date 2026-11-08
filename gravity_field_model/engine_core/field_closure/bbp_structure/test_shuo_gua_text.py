"""
The Shuo Gua text itself: ranks, families and opposites
========================================================

Role:     PROOF.md Theorem 1 (c) and (e): checks the encoding against the classical Chinese text, not a translation.
Expected: Passes. A failure means the text and the trigram figures disagree about a child's rank or an opposite pair.

Theorem 1(e) uses the Shuo Gua's ranking of the six children. This test reads
that ranking directly from the received Chinese text (Shuo Gua, sections 10
and 3, as given by the Chinese Text Project, ctext.org/book-of-changes/shuo-gua)
and checks it against the trigram figures.

Section 10 names each child with an ordinal of "seeking" (索):
    震一索而得男 ... 巽一索而得女 ... 坎再索而得男 ... 離再索而得女 ...
    艮三索而得男 ... 兌三索而得女
(Zhen: first seeking, a son; Xun: first seeking, a daughter; Kan and Li:
second; Gen and Dui: third.)

The test checks, for all six children:
- a son (男) has one yang line, a daughter (女) one yin line;
- the ordinal of the seeking (一 1, 再 2, 三 3) is the position of that
  distinctive line counted from the bottom.

Section 3 pairs the trigrams: 天地 (heaven, earth), 山澤 (mountain, lake),
雷風 (thunder, wind), 水火 (water, fire). The test checks that each pair is
line-for-line opposite.

The trigram figures (lines bottom to top, 1 = yang) are the standard ones.
"""

from gravity_field_model.framework import *

SECTION_10 = (
    "乾，天也，故稱乎父。坤，地也，故稱乎母。"
    "震一索而得男，故謂之長男。巽一索而得女，故謂之長女。"
    "坎再索而得男，故謂之中男。離再索而得女，故謂之中女。"
    "艮三索而得男，故謂之少男。兌三索而得女，故謂之少女。"
)
SECTION_3 = "天地定位，山澤通氣，雷風相薄，水火不相射，八卦相錯。"

# Trigram figures, bottom line first (1 = yang), and their images.
FIGURE = {
    "乾": (1, 1, 1), "坤": (0, 0, 0), "震": (1, 0, 0), "巽": (0, 1, 1),
    "坎": (0, 1, 0), "離": (1, 0, 1), "艮": (0, 0, 1), "兌": (1, 1, 0),
}
IMAGE = {"天": "乾", "地": "坤", "山": "艮", "澤": "兌", "雷": "震", "風": "巽", "水": "坎", "火": "離"}
ORDINAL = {"一": 1, "再": 2, "三": 3}


def parse_children(text):
    """[(trigram, ordinal, 'son'|'daughter')] from section 10."""
    out = []
    for clause in text.split("。"):
        if "索而得" in clause:
            tri, rest = clause[0], clause[1:]
            ordinal = ORDINAL[rest[0]]
            sex = "son" if "得男" in clause else "daughter"
            out.append((tri, ordinal, sex))
    return out


def parse_pairs(text):
    """The four image pairs of section 3 (天地, 山澤, 雷風, 水火)."""
    pairs = []
    for clause in text.split("，"):
        a, b = clause[0], clause[1]
        if a in IMAGE and b in IMAGE:
            pairs.append((IMAGE[a], IMAGE[b]))
    return pairs


class ShuoGuaText(Test):
    name = "The Shuo Gua Text: Ranks of the Children and the Opposites"
    question = (
        "Does the classical text of the Shuo Gua itself rank each child by the position of "
        "its distinctive line, bottom to top, and pair the trigrams as exact opposites?"
    )
    reference = "Shuo Gua sections 3 and 10, Chinese text (Chinese Text Project, ctext.org)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Parse section 10: six clauses 'X n-th seeking obtains a son/daughter'.")
            .step("For each child, find its distinctive line: the single yang line of a son, the single yin line of a daughter.")
            .step("Compare the ordinal of the seeking with that line's position from the bottom.")
            .step("Parse section 3 into four image pairs and check that each pair is line-for-line opposite.")
            .conclude("If all agree, the text fixes bottom = first, so the encoding of Theorem 1(e) is the text's own.")
        )

    commentary = (
        "The text and the figures agree in every case. Each son has exactly one yang line and "
        "each daughter one yin line, and the ordinal of the seeking (first, second, third) is "
        "the position of that line counted from the bottom. So the ranking used in Theorem "
        "1(e) is stated in the classical text itself: the first seeking is the bottom line. "
        "The four pairs of section 3 are exact opposites, the four body diagonals of the cube."
    )

    def model(self):
        kids = parse_children(SECTION_10)
        n_sex_ok = n_rank_ok = 0
        for tri, ordinal, sex in kids:
            lines = FIGURE[tri]
            distinctive = 1 if sex == "son" else 0
            positions = [i + 1 for i, l in enumerate(lines) if l == distinctive]
            n_sex_ok += int(len(positions) == 1)
            n_rank_ok += int(positions == [ordinal])
        pairs = parse_pairs(SECTION_3)
        opp = sum(1 for a, b in pairs if all(x + y == 1 for x, y in zip(FIGURE[a], FIGURE[b])))
        return (
            Model()
            .add("Children named in section 10", len(kids))
            .add("Children with one distinctive line matching their sex", n_sex_ok)
            .add("Children whose seeking ordinal = position of that line from the bottom", n_rank_ok)
            .add("Image pairs in section 3", len(pairs))
            .add("Pairs that are line-for-line opposites", opp)
        )

    def observations(self):
        return (
            Observed()
            # Three sons and three daughters.
            .add("Children named in section 10", 6)
            .add("Children with one distinctive line matching their sex", 6)
            .add("Children whose seeking ordinal = position of that line from the bottom", 6)
            # Heaven-earth, mountain-lake, thunder-wind, water-fire.
            .add("Image pairs in section 3", 4)
            .add("Pairs that are line-for-line opposites", 4)
        )


ALL_TESTS = [ShuoGuaText]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Shuo Gua text", "Ranks and opposites from the Chinese text.", ALL_TESTS) else 1)
