"""Dual families with as many parents as children (docs/lineage_rules.md, draft 3).

Two sets A and B (the dual tetrahedra, generalised). A torus with k children has k parents;
every tube crosses between A and B; no torus is the child of its own child; positive charges
arrive at one end of the axis and negative at the other, and both departures and arrivals net
zero; tori with identical parents never co-parent.
"""
from itertools import combinations, permutations


def circulant(k):
    """Explicit family on 4k tori: A = B = Z_2k, a -> b iff b - a in {0..k-1}, b -> a iff
    a - b in {1..k}. The 'leading' tubes a -> a and b -> b+1 carry the large charge."""
    m = 2 * k
    A = [("A", i) for i in range(m)]; B = [("B", i) for i in range(m)]
    edges = []
    for a in range(m):
        for d in range(k):
            edges.append((("A", a), ("B", (a + d) % m), d == 0))
    for b in range(m):
        for d in range(1, k + 1):
            edges.append((("B", b), ("A", (b + d) % m), d == 1))
    return A + B, edges


def check_family(nodes, edges, charges):
    """charges(lead) -> charge of a tube; checks every rule."""
    out = {v: [] for v in nodes}; inn = {v: [] for v in nodes}
    for u, v, lead in edges:
        assert u[0] != v[0]                                  # crosses between the dual sets
        out[u].append((v, charges(lead))); inn[v].append((u, charges(lead)))
    pairs = {(u, v) for u, v, _ in edges}
    no_mutual = all((v, u) not in pairs for u, v in pairs)
    balanced = all(sum(c for _, c in out[v]) == 0 and sum(c for _, c in inn[v]) == 0 for v in nodes)
    same_k = all(len(out[v]) == len(inn[v]) for v in nodes)
    par = {v: frozenset(u for u, _ in inn[v]) for v in nodes}
    siblings_ok = all(not (par[a] == par[b] and a != b) for v in nodes for a, b in combinations([u for u, _ in inn[v]], 2))
    touches_all = all(len({w for w, _ in out[v]} | {w for w, _ in inn[v]}) == len(nodes) // 2 for v in nodes)
    return dict(no_mutual=no_mutual, balanced=balanced, parents_equal_children=same_k,
                siblings_ok=siblings_ok, touches_whole_dual_set=touches_all)


def exhaustive_k3_count():
    """All orientations of K_{6,6} where every torus has 3 children and 3 parents, with a
    choice of leading (+2/3) tubes forming a one-in one-out cover; counts labelled families
    satisfying the sibling rule."""
    m = 6
    rows = [frozenset(c) for c in combinations(range(m), 3)]
    total = 0
    def rec(i, chosen, colsum):
        nonlocal total
        if i == m:
            if all(c == 3 for c in colsum):
                total += count_covers(chosen)
            return
        for r in rows:
            if all(colsum[j] + (j in r) <= 3 for j in range(m)):
                for j in r: colsum[j] += 1
                rec(i + 1, chosen + [r], colsum)
                for j in r: colsum[j] -= 1
    rec(0, [], [0] * m)
    return total


def count_covers(ch):
    """Number of ways to pick one leading tube out of and into every torus, times the
    sibling check. ch[a] = children of A-torus a in B; B-torus b's children = A-tori with b not in ch[a]."""
    m = len(ch)
    if not siblings_ok_matrix(ch):
        return 0
    # leading tubes A->B: a permutation with b in ch[a]; B->A: a permutation with b not in ch[a]
    p1 = sum(1 for p in permutations(range(m)) if all(p[a] in ch[a] for a in range(m)))
    p2 = sum(1 for p in permutations(range(m)) if all(b not in ch[p[b]] for b in range(m)))
    return p1 * p2


def siblings_ok_matrix(ch):
    m = len(ch)
    parB = {b: frozenset(a for a in range(m) if b in ch[a]) for b in range(m)}
    parA = {a: frozenset(b for b in range(m) if b not in ch[a]) for a in range(m)}
    for b in range(m):
        ps = sorted(parB[b])
        for x, y in combinations(ps, 2):
            if parA[x] == parA[y]: return False
    for a in range(m):
        ps = sorted(parA[a])
        for x, y in combinations(ps, 2):
            if parB[x] == parB[y]: return False
    return True
