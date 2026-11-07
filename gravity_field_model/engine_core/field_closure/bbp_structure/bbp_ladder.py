"""
The BBP ladder: digits of pi at any position, without the earlier digits
=======================================================================

The BBP formula, pi = sum_k 16^-k [4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)],
lets one compute the hexadecimal digits of pi starting at any position n
directly (Bailey, Borwein, Plouffe 1997). Multiply by 16^n and keep only the
fractional part: for each slot j,

    frac(16^n S_j) = frac( sum_{k<=n} (16^(n-k) mod (8k+j)) / (8k+j)
                           + sum_{k>n} 16^(n-k) / (8k+j) ),

and frac(16^n pi) = frac(4 F_1 - 2 F_4 - F_5 - F_6). The modular powers keep
every number small, so rung n costs about n operations and needs nothing
from rungs 1..n-1.

Because 8 = 2^3 and 16 = 2^4 are both powers of two, the base-16 and base-8
expansions of pi are the same binary stream cut into groups of 4 and 3 bits.
Base-8 digit m (1-based) is bits 3m-2 .. 3m of that stream, so it can be read
from the hexadecimal rung that contains those bits. The two groupings
realign every 12 bits: 3 hex digits = 4 octal digits.

Implementation: integer modular powers and float64 fractional parts, as in
Bailey's reference program; the first ~8 hexadecimal digits of each rung are
reliable. ``EXTRACT_HEX`` digits are used per rung.
"""

from typing import List

SLOTS_BBP = ((1, 4.0), (4, -2.0), (5, -1.0), (6, -1.0))
EXTRACT_HEX = 6          # hex digits taken from each rung (float64 gives ~8)


def _frac_16n_slot(n: int, j: int) -> float:
    """frac(16^n * sum_k 1/(16^k (8k+j)))."""
    s = 0.0
    for k in range(n + 1):
        den = 8 * k + j
        s = (s + pow(16, n - k, den) / den) % 1.0
    k = n + 1
    term = 1.0
    while True:
        term = 16.0 ** (n - k) / (8 * k + j)
        if term < 1e-17:
            break
        s += term
        k += 1
    return s % 1.0


def frac_16n_pi(n: int) -> float:
    """frac(16^n pi): the fractional part seen from rung n of the ladder."""
    return sum(w * _frac_16n_slot(n, j) for j, w in SLOTS_BBP) % 1.0


def hex_digits_at(n: int, count: int = EXTRACT_HEX) -> List[int]:
    """Hexadecimal digits n+1 .. n+count of pi (1-based after the point)."""
    x = frac_16n_pi(n)
    out = []
    for _ in range(count):
        x *= 16
        d = int(x)
        out.append(d)
        x -= d
    return out


def octal_digit_at(m: int) -> int:
    """
    Base-8 fractional digit m of pi (1-based), read from the ladder alone.

    The digit is bits 3m-2 .. 3m (1-based) of pi's binary expansion. The rung
    n = (3m-3) // 4 gives hex digits n+1 .., i.e. bits 4n+1 ..; the three
    wanted bits lie within the first two hex digits of that rung.
    """
    first_bit = 3 * m - 2               # 1-based
    n = (first_bit - 1) // 4            # rung
    hexd = hex_digits_at(n, 2)
    bits = "".join(format(h, "04b") for h in hexd)
    offset = first_bit - (4 * n + 1)    # 0..3
    return int(bits[offset:offset + 3], 2)


def octal_digits_from_ladder(count: int) -> List[int]:
    """The first `count` base-8 fractional digits of pi, each from its own rung."""
    return [octal_digit_at(m) for m in range(1, count + 1)]


def base_2k_digit_at(m: int, k: int) -> int:
    """Fractional digit m (1-based) of pi in base 2^k, from the ladder (k <= 8)."""
    first_bit = k * (m - 1) + 1
    n = (first_bit - 1) // 4
    need = (first_bit - (4 * n + 1) + k + 3) // 4
    hexd = hex_digits_at(n, max(need, 1))
    bits = "".join(format(h, "04b") for h in hexd)
    offset = first_bit - (4 * n + 1)
    return int(bits[offset:offset + k], 2)
