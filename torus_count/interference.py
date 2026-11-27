"""Splits in superposition: a twisted torus splits its imbalance among its children every way
at once, each way with a phase, and the ways interfere.

Model (draft 6 of the lineage rules):
  * the parent's imbalance is M units of charge;
  * a split gives k children positive whole numbers of units m_0..m_{k-1} summing to M
    (every way of doing this is present at once);
  * child j sits at angle theta_j on the parent's surface, where its vortex is;
  * a child carrying m units at angle theta contributes the phase e^{i m theta}
    (charge times angle, like the phase of a charge-m vortex turned to angle theta);
  * the amplitude for k children is the sum of e^{i sum_j m_j theta_j} over all splits.

With equally spaced children (theta_j = 2 pi j / k) this sum is exactly 1 in size when k
divides M and exactly 0 otherwise, because prod_j (1 - w^j t) = 1 - t^k for w = e^{2 pi i/k}.
"""
import cmath
from math import pi


def compositions(M, k):
    """All ordered ways to write M as k positive whole numbers."""
    if k == 1:
        yield (M,)
        return
    for first in range(1, M - k + 2):
        for rest in compositions(M - first, k - 1):
            yield (first,) + rest


def angles(split, placement):
    k, M = len(split), sum(split)
    if placement == "equal":
        return [2 * pi * j / k for j in range(k)]
    if placement == "by_charge":       # each child's arc is proportional to its charge
        out, acc = [], 0
        for m in split:
            out.append(2 * pi * (acc + m / 2) / M)
            acc += m
        return out
    raise ValueError(placement)


def amplitude(M, k, placement="equal"):
    total = 0j
    for s in compositions(M, k):
        th = angles(s, placement)
        total += cmath.exp(1j * sum(m * t for m, t in zip(s, th)))
    return total


def survivors(M, placement="equal", tol=1e-9):
    """Numbers of children whose splits survive the interference (amplitude not zero)."""
    return [k for k in range(1, M + 1) if abs(amplitude(M, k, placement)) > tol]
