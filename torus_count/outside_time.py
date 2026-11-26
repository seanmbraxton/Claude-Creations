"""The old view, kept for comparison: everything runs on an outside time tau.

The outside clock may run unevenly. All changes in the system advance at
rates proportional to W'(tau) = 1 + warp*cos(2 pi tau / period), integrated
numerically (cumulative trapezoid), so nothing here uses the closed form of W.

Two kinds of shutter:
  outside: the observer takes a frame every dtau of outside time.
  inside:  the observer's shutter is itself a change in the system. Its phase
           chi advances at nu * W'(tau) and a frame fires when chi crosses an
           integer.
"""
import numpy as np

from .geometry import TAU


def integrated_change(t_max, warp, period, step=2e-4):
    tau = np.arange(0.0, t_max + step, step)
    rate = 1.0 + warp * np.cos(TAU * tau / period)
    I = np.concatenate([[0.0], np.cumsum(0.5 * (rate[1:] + rate[:-1]) * step)])
    return tau, I


def frames_u(omega, dt, n, warp, period, shutter):
    t_max = n * dt
    tau, I = integrated_change(t_max, warp, period)
    if shutter == "outside":
        tau_n = np.arange(n + 1) * dt
        return omega * np.interp(tau_n, tau, I)
    if shutter == "inside":
        chi_targets = np.arange(n + 1) * dt          # nu = 1/dt
        tau_n = np.interp(chi_targets, I, tau)       # when the shutter's own phase ticks
        return omega * np.interp(tau_n, tau, I)
    raise ValueError(shutter)
