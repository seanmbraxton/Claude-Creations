"""Why the golden ratio: families whose mother and father maps commute.

P = mother map (v -> its + child), M = father map (v -> its - child). If P and M commute, the
family is a rotation family on a cycle of N tori: P = shift by a, M = shift by b. Its
eigenvalues are e^{2 pi i k a/N} + e^{2 pi i k b/N}, of size 2|cos(pi k (a - b)/N)|.
"""
from math import gcd
import numpy as np
from torus_count.explore import valid, adjacency, ramanujan


def commute(plus, minus):
    return all(plus[minus[v]] == minus[plus[v]] for v in range(len(plus)))


def realign(N, a, b):
    """L = N / gcd(a - b, N): how many steps before the mother and father lines realign."""
    return N // gcd((a - b) % N, N)


def rotation_family(N, a, b):
    plus = [(v + a) % N for v in range(N)]
    minus = [(v + b) % N for v in range(N)]
    return plus, minus


def rotation_families(N):
    """Rotation families on N tori (N even, a and b odd so generations alternate between the
    two dual sets) that satisfy all the lineage rules."""
    out = []
    for a in range(1, N, 2):
        for b in range(1, N, 2):
            if a == b:
                continue
            plus, minus = rotation_family(N, a, b)
            if valid(plus, minus):
                out.append((a, b))
    return out
