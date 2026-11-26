"""Enumerate closed lineages (docs/lineage_rules.md) and compare with known results."""
import json
from fractions import Fraction
from itertools import permutations, combinations_with_replacement
from math import factorial

from torus_count.hurwitz import (compose, inverse, cycle_type, transitive, commutator,
                                 vortex_type, genus, phase_wheel_closes)

DMAX = 5


def sigma(n, k=1):
    return sum(d ** k for d in range(1, n + 1) if n % d == 0)


def quasimodular_F2(N=9):
    """Dijkgraaf's generating function for two simple branch points over a torus:
    (10 E2^3 - 6 E2 E4 - 4 E6) / 103680, with branch points unlabelled."""
    def series(c, k): return [Fraction(1)] + [Fraction(c * sigma(n, k)) for n in range(1, N)]
    E2, E4, E6 = series(-24, 1), series(240, 3), series(-504, 5)
    mul = lambda a, b: [sum(a[i] * b[n - i] for i in range(n + 1)) for n in range(N)]
    return [(10 * x - 6 * y - 4 * z) / 103680 for x, y, z in zip(mul(mul(E2, E2), E2), mul(E2, E4), E6)]


def all_counts(d):
    """One pass over (A, B): counts for no vortex, one vortex of each type, and two vortices."""
    perms = list(permutations(range(d)))
    ident = tuple(range(d))
    ts = list(range(2, d + 1))
    vt = {t: vortex_type(d, t) for t in ts}
    cls = {t: [p for p in perms if cycle_type(p) == vt[t]] for t in ts}
    none, one, two = 0, {t: 0 for t in ts}, {pr: 0 for pr in combinations_with_replacement(ts, 2)}
    for a in perms:
        for b in perms:
            c = commutator(a, b); ci = inverse(c)
            if c == ident and transitive([a, b], d):
                none += 1
            ct = cycle_type(ci)
            for t in ts:
                if ct == vt[t] and transitive([a, b, ci], d):
                    one[t] += 1
            for (t1, t2) in two:
                for s1 in cls[t1]:
                    s2 = compose(inverse(s1), ci)
                    if cycle_type(s2) == vt[t2] and transitive([a, b, s1], d):
                        two[(t1, t2)] += 1
    f = Fraction(1, factorial(d))
    return none * f, {t: v * f for t, v in one.items()}, {k: v * f for k, v in two.items()}


def main():
    F2 = quasimodular_F2()
    rows = {}
    for d in range(1, DMAX + 1):
        if d == 1:
            rows[d] = (Fraction(1), {}, {}); continue
        rows[d] = all_counts(d)
    out = ["# Lineage enumeration: results\n",
           "Rules: `docs/lineage_rules.md`. Code: `torus_count/hurwitz.py`, `experiments/lineage_enumeration.py`.",
           "Weighted counts: each closed family counted once, divided by its number of symmetries (Hurwitz numbers, vortices labelled).\n",
           "## 1. No vortices: closed families are counted by the divisor sum\n",
           "| children d | weighted count | × d | σ(d), sum of divisors |", "|---|---|---|---|"]
    for d, (n0, _, _) in rows.items():
        out.append(f"| {d} | {n0} | {n0 * d} | {sigma(d)} |")
    out += ["\nFor a prime number of children p there are exactly p + 1 closed families.\n",
            "## 2. One vortex\n", "| d | vortex cycles t children | weighted count | holes (genus) |", "|---|---|---|---|"]
    for d, (_, one, _) in rows.items():
        for t, v in one.items():
            out.append(f"| {d} | {t} | {v} | {genus(d, [vortex_type(d, t)]) if v else '—'} |")
    out += ["\n## 3. Two vortices\n", "| d | cycles (t₁, t₂) | weighted count | holes (genus) | modular-form prediction ×2 |", "|---|---|---|---|---|"]
    for d, (_, _, two) in rows.items():
        for (t1, t2), v in two.items():
            pred = 2 * F2[d] if (t1, t2) == (2, 2) else ""
            out.append(f"| {d} | ({t1}, {t2}) | {v} | {genus(d, [vortex_type(d, t1), vortex_type(d, t2)]) if v else '—'} | {pred} |")
    # phase-wheel version
    qs = sorted({Fraction(p, t) for t in (1, 2, 3, 4) for p in range(-t + 1, t) if p != 0}, key=float)
    bal, integ = {}, {}
    for k in (1, 2, 3):
        combos = list(combinations_with_replacement(qs, k))
        bal[k] = [c for c in combos if sum(c) == 0]
        integ[k] = [c for c in combos if phase_wheel_closes([str(x) for x in c])]
    out += ["\n## 4. Phase-wheel version (all moves are rotations)\n",
            "A configuration closes exactly when the charges add to a whole number. With charges of denominator 2, 3 or 4:\n",
            "| vortices | closing with total 0 | closing with any whole total | examples (total 0) |", "|---|---|---|---|"]
    for k in (1, 2, 3):
        ex = ", ".join("(" + ", ".join(str(x) for x in c) + ")" for c in bal[k] if any(x.denominator == 3 for x in c))[:160]
        out.append(f"| {k} | {len(bal[k])} | {len(integ[k])} | {ex or '—'} |")
    open("results/lineage_enumeration.md", "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
