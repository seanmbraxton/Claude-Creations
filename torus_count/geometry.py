"""Torus geometry and the observer's possible projections (metrics)."""
import numpy as np

TAU = 2 * np.pi


def cd(a):
    """Circular difference in turns, in (-1/2, 1/2]."""
    return a - np.round(a)


def radii(eps):
    """R = 1, r = 1 - eps: eps is the hole radius (ring > 0, horn = 0, spindle < 0)."""
    return 1.0, 1.0 - eps


def embed(theta, phi, eps):
    R, r = radii(eps)
    a, b = TAU * np.asarray(theta), TAU * np.asarray(phi)
    rho = R + r * np.cos(b)
    return rho * np.cos(a), rho * np.sin(a), r * np.sin(b)


def metric(kind, eps=0.0):
    """Distance between two states (theta, phi), in turns."""
    if kind == "flat":
        return lambda t1, p1, t2, p2: np.hypot(cd(t1 - t2), cd(p1 - p2))
    if kind == "theta":
        return lambda t1, p1, t2, p2: np.abs(cd(t1 - t2))
    if kind == "emb":
        _, r = radii(eps)
        sc = 1.0 / (TAU * r)

        def d(t1, p1, t2, p2):
            x1, y1, z1 = embed(t1, p1, eps)
            x2, y2, z2 = embed(t2, p2, eps)
            return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) * sc
        return d
    raise ValueError(kind)
