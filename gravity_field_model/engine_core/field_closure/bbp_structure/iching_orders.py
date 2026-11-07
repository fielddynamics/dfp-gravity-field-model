"""
Documented orders of the eight trigrams
=======================================

Sources: R. Wilhelm, The I Ching or Book of Changes, trans. C. F. Baynes
(Princeton, 1950), Shuo Kua (Discussion of the Trigrams):
- ch. 10, the family: Qian father, Kun mother; Zhen, Kan, Gen the eldest,
  middle and youngest sons; Xun, Li, Dui the eldest, middle and youngest
  daughters. The text derives each child's rank from the position of its
  single distinctive line: first (bottom), second (middle), third (top).
- ch. 3, the Earlier Heaven (Fu Xi) arrangement: Qian S, Kun N, Li E,
  Kan W, Zhen NE, Xun SW, Dui SE, Gen NW. Shao Yong's numbering of it
  (11th century): Qian 1, Dui 2, Li 3, Zhen 4, Xun 5, Kan 6, Gen 7, Kun 8.
- ch. 5, the Later Heaven (King Wen) arrangement, in the order of the text,
  starting in the east and going round: Zhen E, Xun SE, Li S, Kun SW,
  Dui W, Qian NW, Kan N, Gen NE. Its Lo Shu numbering: Kan 1, Kun 2,
  Zhen 3, Xun 4, Qian 6, Dui 7, Gen 8, Li 9.

Vertex labels are those of the model (bottom line = most significant bit):
Kun 0, Gen 1, Kan 2, Xun 3, Zhen 4, Li 5, Dui 6, Qian 7.
"""

VERTEX = {"Kun": 0, "Gen": 1, "Kan": 2, "Xun": 3, "Zhen": 4, "Li": 5, "Dui": 6, "Qian": 7}

# Lines bottom, middle, top (1 = yang), from the trigram figures.
LINES = {
    "Qian": (1, 1, 1), "Kun": (0, 0, 0),
    "Zhen": (1, 0, 0), "Kan": (0, 1, 0), "Gen": (0, 0, 1),
    "Xun": (0, 1, 1), "Li": (1, 0, 1), "Dui": (1, 1, 0),
}

# Shuo Kua ch. 10 in the order of the text: father, mother, then each son
# followed by the daughter of the same rank ("seeks for the first time ...
# a second time ... a third time").
SHUO_GUA_SEQUENCE = ["Qian", "Kun", "Zhen", "Xun", "Kan", "Li", "Gen", "Dui"]

ARRANGEMENTS = {
    "Shuo Gua ch. 10 sequence": SHUO_GUA_SEQUENCE,
    "Fu Xi numbering 1-8 (Shao Yong)": ["Qian", "Dui", "Li", "Zhen", "Xun", "Kan", "Gen", "Kun"],
    "Fu Xi circle, S-SE-E-NE-N-NW-W-SW": ["Qian", "Dui", "Li", "Zhen", "Kun", "Gen", "Kan", "Xun"],
    "Fu Xi circle, S-SW-W-NW-N-NE-E-SE": ["Qian", "Xun", "Kan", "Gen", "Kun", "Zhen", "Li", "Dui"],
    "King Wen circle, order of ch. 5": ["Zhen", "Xun", "Li", "Kun", "Dui", "Qian", "Kan", "Gen"],
    "King Wen circle, reverse": ["Gen", "Kan", "Qian", "Dui", "Kun", "Li", "Xun", "Zhen"],
    "King Wen Lo Shu numbering": ["Kan", "Kun", "Zhen", "Xun", "Qian", "Dui", "Gen", "Li"],
}


def chamber_order(arrangement, apex):
    """
    The vertices of the chamber containing `apex` (Qian for TetA, Kun for
    TetB) in the order the arrangement lists them, rotated so the apex (the
    temporal face) is read first.
    """
    teta = apex == "Qian"
    names = [n for n in arrangement if (sum(LINES[n]) % 2 == 1) == teta]
    i = names.index(apex)
    names = names[i:] + names[:i]
    return [VERTEX[n] for n in names]
