"""Enumerate closed lineages: shuffles of d children that close on a torus.

See docs/lineage_rules.md. A configuration is a tuple of permutations
(A, B, S_1, ..., S_k) of the d children with A B A^-1 B^-1 S_1 ... S_k = id.
"""
from fractions import Fraction
from itertools import permutations
from math import factorial


def compose(p, q):
    """(p * q)(x) = p(q(x)): first q, then p."""
    return tuple(p[i] for i in q)


def inverse(p):
    inv = [0] * len(p)
    for i, j in enumerate(p):
        inv[j] = i
    return tuple(inv)


def cycle_type(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen:
            continue
        n, j = 0, i
        while j not in seen:
            seen.add(j); j = p[j]; n += 1
        out.append(n)
    return tuple(sorted(out, reverse=True))


def transitive(gens, d):
    seen, stack = {0}, [0]
    while stack:
        x = stack.pop()
        for g in gens:
            y = g[x]
            if y not in seen:
                seen.add(y); stack.append(y)
    return len(seen) == d


def commutator(a, b):
    return compose(compose(a, b), compose(inverse(a), inverse(b)))


def vortex_type(d, t):
    """One child of winding t over a vortex: a t-cycle, the rest untouched."""
    return tuple(sorted([t] + [1] * (d - t), reverse=True))


def hurwitz(d, types):
    """Weighted count of closed, connected lineages with d children and vortices of
    the given cycle types (0, 1 or 2 vortices). Returns (Fraction, raw count)."""
    perms = list(permutations(range(d)))
    ident = tuple(range(d))
    classes = {}
    for p in perms:
        classes.setdefault(cycle_type(p), []).append(p)
    count = 0
    for a in perms:
        for b in perms:
            c = commutator(a, b)
            if len(types) == 0:
                if c == ident and transitive([a, b], d):
                    count += 1
            elif len(types) == 1:
                s1 = inverse(c)                       # c * s1 = id
                if cycle_type(s1) == types[0] and transitive([a, b, s1], d):
                    count += 1
            else:
                ci = inverse(c)
                for s1 in classes.get(types[0], []):
                    s2 = compose(inverse(s1), ci)     # c * s1 * s2 = id
                    if cycle_type(s2) == types[1] and transitive([a, b, s1], d):
                        count += 1
    return Fraction(count, factorial(d)), count


def genus(d, types):
    """Riemann–Hurwitz over a torus: 2g - 2 = sum (d - number of cycles)."""
    tot = sum(d - len(t) for t in types)
    return Fraction(tot, 2) + 1


def phase_wheel_closes(charges):
    """Phase-wheel version: all moves are rotations, so closure means the charges'
    rotations add to a whole number of turns."""
    return sum(Fraction(c) for c in charges).denominator == 1
