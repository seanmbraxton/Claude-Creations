"""Closed lineages under the grandparent rule (docs/lineage_rules.md).

A family is a directed graph on n tori: an edge u -> v means a vortex on u spawned
v (v's toroidal axis receives the tube). Rules:
  * no torus is its own child, at most one tube from u to v;
  * every torus has at least 2 vortices (charges must sum to zero) and is someone's child;
  * closure rule C_L: whenever v0 -> v1 -> ... -> vL, then vL -> v0.
    L = 2 is "every child reconnects to its grandparent through its own offspring".
"""
from itertools import combinations, permutations, product
from fractions import Fraction


def search(n, L=2, min_out=2):
    """All families on n tori satisfying C_L, as tuples of out-sets (labelled)."""
    others = [[v for v in range(n) if v != u] for u in range(n)]
    options = [[frozenset(c) for k in range(min_out, n) for c in combinations(others[u], k)] for u in range(n)]
    sols = []
    out = [None] * n

    def walks_ok():
        # every complete walk of length L among assigned tori must close
        def rec(path):
            u = path[-1]
            if out[u] is None:
                return True
            if len(path) == L + 1:
                return True
            for v in out[u]:
                p = path + [v]
                if len(p) == L + 1:
                    end = p[-1]
                    if end == p[0]:
                        return False                      # would need a self-loop
                    if out[end] is not None and p[0] not in out[end]:
                        return False
                elif not rec(p):
                    return False
            return True
        return all(rec([s]) for s in range(n) if out[s] is not None)

    def bt(i):
        if i == n:
            indeg = [0] * n
            for u in range(n):
                for v in out[u]:
                    indeg[v] += 1
            if min(indeg) >= 1:
                sols.append(tuple(out))
            return
        for o in options[i]:
            out[i] = o
            if walks_ok():
                bt(i + 1)
        out[i] = None

    bt(0)
    return sols


def canonical(g):
    n = len(g)
    best = None
    for p in permutations(range(n)):
        key = tuple(sorted((p[u], p[v]) for u in range(n) for v in g[u]))
        if best is None or key < best:
            best = key
    return best


def weakly_connected(g):
    n = len(g); adj = [set() for _ in range(n)]
    for u in range(n):
        for v in g[u]:
            adj[u].add(v); adj[v].add(u)
    seen, st = {0}, [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y); st.append(y)
    return len(seen) == n


def generations(g, L):
    """If g is a blow-up of a directed (L+1)-cycle, return the generation classes."""
    n = len(g)
    level = {0: 0}; st = [0]
    while st:
        u = st.pop()
        for v in g[u]:
            want = (level[u] + 1) % (L + 1)
            if v in level and level[v] != want:
                return None
            if v not in level:
                level[v] = want; st.append(v)
        for w in range(n):
            if u in g[w]:
                want = (level[u] - 1) % (L + 1)
                if w in level and level[w] != want:
                    return None
                if w not in level:
                    level[w] = want; st.append(w)
    if len(level) < n:
        return None
    parts = [[v for v in range(n) if level[v] == k] for k in range(L + 1)]
    for u in range(n):                                  # every torus feeds the whole next generation
        if set(g[u]) != set(parts[(level[u] + 1) % (L + 1)]):
            return None
    return [len(p) for p in parts]


def closed_families(n, L=2):
    seen = {}
    for g in search(n, L):
        if not weakly_connected(g):
            continue
        c = canonical(g)
        if c not in seen:
            seen[c] = g
    return list(seen.values())


def charge_matrices(m, alphabet, arrivals_balanced=True):
    """Ways to put charges on the m x m tubes between two consecutive generations:
    every torus's departing charges sum to 0 (rows), and optionally every torus's
    arriving charges sum to 0 (columns)."""
    rows = [r for r in product(alphabet, repeat=m) if sum(r) == 0]
    count = 0
    for M in product(rows, repeat=m):
        if not arrivals_balanced or all(sum(M[i][j] for i in range(m)) == 0 for j in range(m)):
            count += 1
    return count


def classify(n, L=2):
    """Exhaustive search on n tori. Returns (number of labelled connected families,
    set of generation-size patterns up to rotation, list of families that are NOT
    blow-ups of an (L+1)-cycle)."""
    labelled, patterns, odd = 0, set(), []
    for g in search(n, L):
        if not weakly_connected(g):
            continue
        labelled += 1
        sizes = generations(g, L)
        if sizes is None:
            odd.append(g)
        else:
            rots = [tuple(sizes[i:] + sizes[:i]) for i in range(len(sizes))]
            patterns.add(min(rots))
    return labelled, patterns, odd


def search_grandparent(n, min_out=2):
    """Fast exhaustive search for the grandparent rule (L = 2) with propagation:
    G -> P -> X forces X -> G (and X != G)."""
    others = [[v for v in range(n) if v != u] for u in range(n)]
    out = [None] * n
    req = [set() for _ in range(n)]
    parents = [set() for _ in range(n)]        # assigned parents of each torus
    sols = []

    def bt(u):
        if u == n:
            indeg = [len(parents[v]) for v in range(n)]
            if min(indeg) >= 1:
                sols.append(tuple(out))
            return
        need = req[u]
        free = [v for v in others[u] if v not in need]
        for k in range(max(0, min_out - len(need)), len(free) + 1):
            for extra in combinations(free, k):
                S = frozenset(need) | frozenset(extra)
                if not S:
                    continue
                undo, ok = [], True
                # u as middle: G -> u -> Y forces Y -> G
                for G in parents[u]:
                    for Y in S:
                        if Y == G: ok = False; break
                        if out[Y] is not None:
                            if G not in out[Y]: ok = False; break
                        elif G not in req[Y]:
                            req[Y].add(G); undo.append((Y, G))
                    if not ok: break
                # u as grandparent: u -> P -> X forces X -> u
                if ok:
                    for P in S:
                        if out[P] is None: continue
                        for X in out[P]:
                            if X == u: ok = False; break
                            if out[X] is not None:
                                if u not in out[X]: ok = False; break
                            elif u not in req[X]:
                                req[X].add(u); undo.append((X, u))
                        if not ok: break
                if ok:
                    out[u] = S
                    for v in S: parents[v].add(u)
                    # tori assigned later that already list u as child are handled when assigned
                    # but children of u assigned earlier: u -> P (assigned) -> X done above;
                    # earlier tori G with u in out[G]: G -> u -> Y done via parents[u]
                    bt(u + 1)
                    for v in S: parents[v].discard(u)
                    out[u] = None
                for (Y, G) in undo: req[Y].discard(G)

    # parents[u] must include earlier tori that list u as a child: maintained when they were assigned
    bt(0)
    return sols
