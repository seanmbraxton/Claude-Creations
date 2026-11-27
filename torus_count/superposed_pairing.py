"""Every pairing at once: opposite-sign seams collide, children carry the difference.

Draft 7 rules (only the user's): a mother seam +a and a father seam -b (a, b > 0, continuous).
Each generation, every positive seam present pairs with every negative seam present, and each
pair has a child whose seam is their sum. Parents keep sounding (tones are not used up). The
family is neutral when a child is born at exactly 0, i.e. some seam meets its exact opposite.

Findings (see tests): resolution happens iff a/b is rational; it depends only on the reduced
ratio p/q; with every pairing present it takes about log2(q) generations for comparable parents,
far fewer than the single Euclid path (up to q steps), but a lopsided pair (weak parent 1/m of
the strong one) still needs about m generations; primality of q makes no measurable difference.
"""
from fractions import Fraction


def generations_to_neutral(a, b, cap=60, max_tones=20000):
    """First generation in which a child is born at exactly 0, or None. Use Fractions for exact
    rational input; floats are compared with a small tolerance."""
    exact = isinstance(a, (int, Fraction)) and isinstance(b, (int, Fraction))
    key = (lambda x: x) if exact else (lambda x: round(x, 12))
    S = {key(a): a, key(-b): -b}
    for g in range(1, cap + 1):
        pos = [x for x in S.values() if x > 0]
        neg = [y for y in S.values() if y < 0]
        new = {}
        for x in pos:
            for y in neg:
                s = x + y
                if (s == 0) if exact else abs(s) < 1e-11:
                    return g
                new[key(s)] = s
        S.update(new)
        if len(S) > max_tones:
            return None
    return None


def euclid_steps(p, q):
    """Generations along the single 'subtract the smaller' path (sum of partial quotients)."""
    n = 0
    while q:
        n += p // q
        p, q = q, p % q
    return n
