"""The flow, parametrized by a change inside the system rather than by time.

The reference change is u = (unwrapped poloidal phase) - phi0. Between portal
passes, the toroidal phase advances 1/omega per unit of u: omega is the
winding ratio, poloidal change per toroidal change. A pass happens whenever
the poloidal phase crosses 1/2 (the inner equator, the horn point at eps = 0).

The gate and locking act only on theta, so u is strictly increasing and is
always a valid clock. Whether theta can also serve as a clock is checked by
`theta_is_monotone`.
"""
from dataclasses import dataclass, replace
import numpy as np

from .geometry import TAU

GOLD = (np.sqrt(5) - 1) / 2
SQRT2M1 = np.sqrt(2) - 1


@dataclass(frozen=True)
class Params:
    eps: float = 0.15
    omega: float = GOLD      # poloidal turns per toroidal turn
    k: int = 3               # portal windows per toroidal turn
    cw: float = 0.4          # window width w = cw * |eps|
    lock: bool = True
    cK: float = 1.0          # locking K = cK * |eps|
    flip: str = "off"        # off | kick | reflect  (only when eps < 0)
    th0: float = 0.05
    ph0: float = 0.25

    def with_(self, **kw):
        return replace(self, **kw)


class Flow:
    """Piecewise-linear path theta(u), phi(u) with gate decisions at each pass."""

    def __init__(self, p: Params, u_max: float):
        self.p = p
        eps, k = p.eps, p.k
        self.w = p.cw * abs(eps)
        self.K = p.cK * abs(eps) if p.lock else 0.0
        seg_u, seg_th = [0.0], [p.th0]
        pass_u, pass_th, pass_open = [], [], []
        first = (0.5 - p.ph0) % 1.0
        sign = 1.0
        n = 0
        while True:
            un = first + n
            if un > u_max:
                break
            thB = seg_th[-1] + (un - seg_u[-1]) / p.omega
            off = abs(thB * k - round(thB * k)) / k
            is_open = off <= self.w / 2 + 1e-9
            thA = thB
            if self.K > 0:
                s = sign if (p.flip == "kick" and eps < 0) else 1.0
                thA = thB - s * self.K / (TAU * k) * np.sin(TAU * k * thB)
            if p.flip == "kick" and eps < 0:
                sign = -sign
            if p.flip == "reflect" and eps < 0:
                thA = -thA
            pass_u.append(un); pass_th.append(thB); pass_open.append(is_open)
            seg_u.append(un); seg_th.append(thA)
            n += 1
        self.seg_u = np.array(seg_u)
        self.seg_th = np.array(seg_th)
        self.pass_u = np.array(pass_u)
        self.pass_th = np.array(pass_th)
        self.pass_open = np.array(pass_open, dtype=bool)

    def theta(self, u):
        u = np.asarray(u, dtype=float)
        i = np.searchsorted(self.seg_u, u, side="right") - 1
        return self.seg_th[i] + (u - self.seg_u[i]) / self.p.omega

    def phi(self, u):
        return self.p.ph0 + np.asarray(u, dtype=float)

    def theta_is_monotone(self):
        """Can theta serve as a clock? Only if it never steps backward."""
        jumps = self.seg_th[1:] - (self.seg_th[:-1] + np.diff(self.seg_u) / self.p.omega)
        return bool(np.all(jumps >= -1e-12))


def aligned_start(p: Params):
    """th0 that puts the first pass exactly on window 0."""
    first = (0.5 - p.ph0) % 1.0
    return (-first / p.omega) % 1.0
