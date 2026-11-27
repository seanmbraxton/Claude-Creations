"""Passing a seam: jump the gap or climb the walls (draft 8).

A seam has width eps. A path meeting it at angle theta (to the seam) spends about eps/sin(theta)
inside. Steep (sin theta >= eps): it crosses, an instant as eps -> 0. Grazing (sin theta < eps):
it runs along the seam and climbs into the child torus behind it. Zooming into a seam of width
eps rescales the across-seam direction by 1/eps, so the angle seen in the child obeys
tan(theta') = tan(theta) / eps. Each climb appends a branch (a hole for the observer).
A neutral child has no seam, so the climb ends there and the path returns.
"""
from math import atan, sin, tan


def passage(theta, eps, charges):
    """charges: the seam charge at each level (0 = neutral). Returns (steps, depth, parent_time,
    lived_time) where steps lists (level, theta, action) with action in cross/climb/neutral."""
    steps, k, th = [], 0, theta
    while True:
        if k >= len(charges) or abs(charges[k]) < 1e-12:
            steps.append((k, th, "neutral"))
            break
        if sin(th) >= eps:
            steps.append((k, th, "cross"))
            break
        steps.append((k, th, "climb"))
        th = atan(tan(th) / eps)
        k += 1
    depth = sum(1 for s in steps if s[2] == "climb")
    # a crossing takes eps/sin(theta); a climber vanishes into the seam, so the parent sees only eps
    parent_time = eps if depth else eps / max(sin(theta), eps)
    return steps, depth, parent_time, parent_time / eps ** depth
