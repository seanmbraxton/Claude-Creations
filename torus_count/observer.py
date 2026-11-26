"""The internal observer and the ground truth.

The observer remembers its first frame and counts a return each time a frame
re-enters the delta-neighborhood of that memory (re-entry only).

The ground truth counts entries of the exact path into the flat delta-disk
around the true start. It is computed from the path itself (fine steps in u),
so it cannot depend on how any clock runs.
"""
from dataclasses import dataclass
import numpy as np

from .geometry import metric, cd


@dataclass
class Observation:
    frames_u: np.ndarray
    entries: np.ndarray      # frame indices where a count fired
    inside: np.ndarray       # bool per frame
    mem: np.ndarray          # (n_frames, 2) remembered state per frame


def observe(flow, frames_u, delta, kind="flat", drift=0.0):
    p = flow.p
    th, ph = flow.theta(frames_u), flow.phi(frames_u)
    d = metric(kind, p.eps)
    if drift == 0:
        inside = d(th, ph, p.th0, p.ph0) < delta
        prev = np.concatenate([[True], inside[:-1]])
        entries = np.nonzero(inside & ~prev)[0]
        mem = np.tile([p.th0, p.ph0], (len(th), 1))
        return Observation(np.asarray(frames_u), entries, inside, mem)
    mt, mp = p.th0, p.ph0
    was_in = True
    entries, inside, mem = [], np.zeros(len(th), bool), np.zeros((len(th), 2))
    for i in range(len(th)):
        is_in = d(th[i], ph[i], mt, mp) < delta
        if i > 0 and is_in and not was_in:
            entries.append(i)
            if drift > 0:
                mt += drift * cd(th[i] - mt)
                mp += drift * cd(ph[i] - mp)
        was_in = is_in
        inside[i] = is_in
        mem[i] = (mt, mp)
    return Observation(np.asarray(frames_u), np.array(entries, int), inside, mem)


def truth_visits(flow, delta, u_max, du_fine):
    """Return list of (u_in, u_out) visits of the exact path to the flat delta-disk."""
    p = flow.p
    u = np.arange(0.0, u_max + du_fine / 2, du_fine)
    d = metric("flat")(flow.theta(u), flow.phi(u), p.th0, p.ph0)
    inn = d < delta
    visits, start = [], None
    for j in range(1, len(u)):
        if inn[j] and not inn[j - 1]:
            start = u[j]
        if not inn[j] and inn[j - 1] and start is not None:
            visits.append((start, u[j])); start = None
    if start is not None:
        visits.append((start, u[-1]))
    return visits


def match(obs, visits, tol):
    """Split observer counts into confirmed / false, and true visits into caught / missed."""
    caught = np.zeros(len(visits), bool)
    false = 0
    for i in obs.entries:
        uu = obs.frames_u[i]
        hit = [k for k, (a, b) in enumerate(visits) if a - tol <= uu <= b + tol]
        if hit:
            caught[hit[0]] = True
        else:
            false += 1
    return dict(observed=len(obs.entries), true=len(visits),
                missed=int((~caught).sum()), false=false)
