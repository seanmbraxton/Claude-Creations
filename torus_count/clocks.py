"""Shutters: when the observer takes its frames, expressed as values of u.

relational(du, n)   frames locked to the system's own change: every du of
                    poloidal phase. No outside clock exists.
external(dt, n, omega, warp, period)
                    frames uniform in an outside time tau. The system's
                    change is u = omega * W(tau), where W is a monotone warp:
                    W(tau) = tau + warp * period/(2 pi) * sin(2 pi tau/period).
                    warp = 0 is the original simulation (u = omega * t).
                    |warp| < 1 keeps W strictly increasing, so the warp only
                    changes how the outside clock runs, never the path.
"""
import numpy as np

from .geometry import TAU


def relational(du, n):
    return np.arange(n + 1) * du


def warp_W(tau, warp, period):
    return tau + warp * period / TAU * np.sin(TAU * tau / period)


def external(dt, n, omega, warp=0.0, period=1.0):
    tau = np.arange(n + 1) * dt
    return omega * warp_W(tau, warp, period)
