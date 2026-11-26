"""Two-parent families: every torus has a +1 child and a -1 child, and receives one +1
(from one parent) and one -1 (from the other). A family is a pair of permutations
(plus, minus) of the tori: plus[v] receives v's +1 tube, minus[v] its -1 tube.

Basic rules: nobody is their own child, a torus's two children differ, its two parents
differ, and the family is connected. Optional rules:
  no_mutual  - no torus is the child of its own child (no 2-step loops)
  siblings   - two tori with the same pair of parents may not co-parent a child
"""
from itertools import permutations


def derangements(n):
    return [p for p in permutations(range(n)) if all(p[i] != i for i in range(n))]


def inverse(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return q


def connected(plus, minus):
    n = len(plus); seen = {0}; st = [0]
    adj = [set() for _ in range(n)]
    for v in range(n):
        for w in (plus[v], minus[v]):
            adj[v].add(w); adj[w].add(v)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n


def ok(plus, minus, no_mutual=False, siblings=False):
    n = len(plus)
    if any(plus[v] == minus[v] for v in range(n)):
        return False
    ip, im = inverse(plus), inverse(minus)
    if any(ip[v] == im[v] for v in range(n)):
        return False
    if no_mutual:
        for v in range(n):
            for c in (plus[v], minus[v]):
                if v in (plus[c], minus[c]):
                    return False
    if siblings:
        par = [frozenset((ip[v], im[v])) for v in range(n)]
        for c in range(n):
            a, b = ip[c], im[c]
            if par[a] == par[b]:
                return False
    return connected(plus, minus)


def canon(plus, minus):
    """Canonical form under relabelling (edges keep their +/- colour)."""
    n = len(plus); best = None
    for r in range(n):
        lab = {r: 0}; order = [r]; i = 0
        while i < len(order):
            v = order[i]; i += 1
            for w in (plus[v], minus[v]):
                if w not in lab:
                    lab[w] = len(order); order.append(w)
        if len(order) < n:
            continue
        key = tuple((lab[plus[v]], lab[minus[v]]) for v in order)
        if best is None or key < best:
            best = key
    return best


def families(n, **rules):
    if n < 3:
        return []
    ds = derangements(n)
    # fix the + pairing up to relabelling: one representative per cycle type
    reps, seen = [], set()
    for p in ds:
        ct = tuple(sorted(cycle_lengths(p)))
        if ct not in seen:
            seen.add(ct); reps.append(p)
    found = {}
    for plus in reps:
        for minus in ds:
            if ok(plus, minus, **rules):
                c = canon(plus, minus)
                found.setdefault(c, (plus, minus))
    return list(found.values())


def cycle_lengths(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen: continue
        j, k = i, 0
        while j not in seen:
            seen.add(j); j = p[j]; k += 1
        out.append(k)
    return out


def describe(plus, minus):
    """Shape facts: cycle lengths of the + and - pairings, and the girth."""
    n = len(plus)
    from collections import deque
    g = 10**9
    for s in range(n):
        dist = {s: 0}; q = deque([s])
        while q:
            v = q.popleft()
            for w in (plus[v], minus[v]):
                if w == s: g = min(g, dist[v] + 1)
                if w not in dist: dist[w] = dist[v] + 1; q.append(w)
    return sorted(cycle_lengths(plus)), sorted(cycle_lengths(minus)), g


def ok_ext(plus, minus, no_mutual=False, siblings=False, half_siblings=False, dual=False):
    """Extra variants. dual: tori form two equal halves and every tube crosses between
    them (parents always come from the other half). half_siblings: two tori sharing any
    parent may not co-parent a child."""
    if not ok(plus, minus, no_mutual, siblings):
        return False
    n = len(plus)
    if dual:
        side = {0: 0}; st = [0]
        nbr = [set() for _ in range(n)]
        for v in range(n):
            for w in (plus[v], minus[v]):
                nbr[v].add(w); nbr[w].add(v)
        while st:
            v = st.pop()
            for w in nbr[v]:
                if w in side:
                    if side[w] == side[v]: return False
                else:
                    side[w] = 1 - side[v]; st.append(w)
        if sum(side.values()) * 2 != n:
            return False
    if half_siblings:
        ip, im = inverse(plus), inverse(minus)
        par = [{ip[v], im[v]} for v in range(n)]
        for c in range(n):
            if par[ip[c]] & par[im[c]]:
                return False
    return True


def families_ext(n, **rules):
    if n < 3:
        return []
    ds = derangements(n)
    reps, seen = [], set()
    for p in ds:
        ct = tuple(sorted(cycle_lengths(p)))
        if ct not in seen:
            seen.add(ct); reps.append(p)
    found = {}
    for plus in reps:
        for minus in ds:
            if ok_ext(plus, minus, **rules):
                found.setdefault(canon(plus, minus), (plus, minus))
    return list(found.values())
