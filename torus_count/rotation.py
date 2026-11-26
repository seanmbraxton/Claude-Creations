"""Pure rotation by alpha per step: the pass map with no gate and no locking."""
import numpy as np

from .geometry import cd


def first_return(alpha, delta, qmax=10**7):
    """Smallest q >= 1 with the orbit back within delta of its start."""
    q = np.arange(1, qmax + 1)
    hit = np.nonzero(np.abs(cd(q * alpha)) < delta)[0]
    return int(q[hit[0]]) if len(hit) else None


def return_times(alpha, length, x0=0.0, n=200_000):
    """Gaps between successive visits of the orbit to [0, length)."""
    x = (x0 + np.arange(n) * alpha) % 1.0
    idx = np.nonzero(x < length)[0]
    return np.diff(idx)


def convergent_denominators(alpha, qmax):
    out, (k0, k1), y = [], (0, 1), alpha   # (q_{-1}, q_{-2})
    for _ in range(60):
        a = int(np.floor(y))
        k0, k1 = a * k0 + k1, k0
        if k0 > qmax:
            break
        if k0 >= 1:
            out.append(k0)
        f = y - a
        if f < 1e-15:
            break
        y = 1 / f
    return out
