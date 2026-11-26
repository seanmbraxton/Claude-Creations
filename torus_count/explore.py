"""Explore two-parent dual families under rules draft 4 (docs/lineage_rules.md).

A family on 2m tori: sets A and B of size m. Each torus has a + child and a - child in the
other set, and a + parent (mother) and a - parent (father) in the other set. Encoded by four
bijections: plusAB, minusAB (A -> B) and plusBA, minusBA (B -> A).
"""
from itertools import permutations
from fractions import Fraction as F
from math import gcd
import numpy as np

from torus_count.two_parents import canon


def families(m):
    """All families on 2m tori (dual, no torus the child of its own child, sibling rule,
    connected), one per isomorphism class. Tori 0..m-1 are A, m..2m-1 are B."""
    perms = list(permutations(range(m)))
    ident = tuple(range(m))
    found = {}
    for qAB in perms:                                   # plusAB fixed to the identity by relabelling B
        if any(qAB[a] == a for a in range(m)):
            continue
        for pBA in perms:
            for qBA in perms:
                if any(pBA[b] == qBA[b] for b in range(m)):
                    continue
                plus = [m + a for a in range(m)] + [pBA[b] for b in range(m)]
                minus = [m + qAB[a] for a in range(m)] + [qBA[b] for b in range(m)]
                if valid(plus, minus):
                    found.setdefault(canon(plus, minus), (plus, minus))
    return list(found.values())


def valid(plus, minus):
    n = len(plus)
    ip = [0] * n; im = [0] * n
    for v in range(n): ip[plus[v]] = v; im[minus[v]] = v
    for v in range(n):                                   # no torus is the child of its own child
        if {plus[v], minus[v]} & {ip[v], im[v]}:
            return False
    par = [frozenset((ip[v], im[v])) for v in range(n)]
    for c in range(n):                                   # sibling rule
        if par[ip[c]] == par[im[c]]:
            return False
    seen, st = {0}, [0]                                  # connected
    while st:
        x = st.pop()
        for y in (plus[x], minus[x], ip[x], im[x]):
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n


def adjacency(plus, minus):
    n = len(plus); A = np.zeros((n, n), dtype=int)
    for v in range(n):
        A[v, plus[v]] += 1; A[v, minus[v]] += 1
    return A


def simple_cycle_lengths(plus, minus):
    n = len(plus); out = [(plus[v], minus[v]) for v in range(n)]
    lengths = {}
    def dfs(s, v, depth, seen):
        for w in out[v]:
            if w == s:
                lengths[depth] = lengths.get(depth, 0) + 1
            elif w > s and w not in seen:
                seen.add(w); dfs(s, w, depth + 1, seen); seen.discard(w)
    for s in range(n):
        dfs(s, s, 1, {s})
    return dict(sorted(lengths.items()))


def mobius(n):
    res, p, k = 1, 2, n
    while p * p <= k:
        if k % p == 0:
            k //= p
            if k % p == 0: return 0
            res = -res
        p += 1
    return -res if k > 1 else res


def prime_loops(A, upto=12):
    """Number of primitive loops (equivalence classes of primitive closed walks) of each length:
    P(L) = (1/L) * sum_{d | L} mu(L/d) tr(A^d)."""
    tr = {}
    M = np.eye(len(A), dtype=object); Ao = A.astype(object)
    for d in range(1, upto + 1):
        M = M.dot(Ao); tr[d] = int(np.trace(M))
    return {L: sum(mobius(L // d) * tr[d] for d in range(1, L + 1) if L % d == 0) // L for L in range(1, upto + 1)}


def ramanujan(A, k=2):
    """Riemann hypothesis for the family's zeta function 1/det(I - uA): every eigenvalue other
    than the trivial ones (|lambda| = k) has |lambda| <= sqrt(k)."""
    ev = np.linalg.eigvals(A.astype(float))
    nontriv = [x for x in ev if abs(abs(x) - k) > 1e-9]
    worst = max((abs(x) for x in nontriv), default=0.0)
    return worst <= np.sqrt(k) + 1e-9, worst, sorted(ev, key=lambda z: -abs(z))


def fraction_denominators(lengths):
    Ls = list(lengths)
    return sorted({b // gcd(a, b) for a in Ls for b in Ls})
