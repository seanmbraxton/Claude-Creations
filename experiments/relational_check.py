"""Does anything in the model depend on an absolute time?

For each cell (eps, delta, omega) the observer is run four ways:
  original   frames uniform in t, with u = omega * t         (the old simulation)
  relational frames locked to the system's own change u      (no time anywhere)
  inside     an uneven outside clock drives everything, the shutter included
  outside    an uneven outside clock drives only the shutter's ticks
Truth, portal passes and coherence are computed from the path in u.
"""
import json
import math
import numpy as np

from torus_count.dynamics import Params, Flow, GOLD, SQRT2M1
from torus_count.observer import observe, truth_visits, match
from torus_count import clocks, outside_time

T = 40.0                      # toroidal turns of path
PERIOD = 2.5                  # outside clock's unevenness period (T is a multiple)
EPS = np.round(np.linspace(-0.4, 0.4, 9), 3)
DELTAS = [0.01, 0.02, 0.03, 0.05, 0.1]
OMEGAS = {"golden": GOLD, "sqrt2-1": SQRT2M1, "1/3": 1 / 3}
WARPS = [0.3, 0.6, 0.9]


def cell(p, delta):
    v = math.hypot(1.0, p.omega)
    dt = delta / v
    n = int(T / dt)
    u_max = p.omega * n * dt
    flow = Flow(p, u_max + 1)
    visits = truth_visits(flow, delta, u_max, p.omega * dt / 16)
    tol = p.omega * dt / 16
    run = lambda fu: match(observe(flow, fu, delta), visits, tol)
    out = {"original": run(clocks.external(dt, n, p.omega)),
           "relational": run(clocks.relational(p.omega * dt, n))}
    for w in WARPS:
        out[f"inside {w}"] = run(outside_time.frames_u(p.omega, dt, n, w, PERIOD, "inside"))
        out[f"outside {w}"] = run(outside_time.frames_u(p.omega, dt, n, w, PERIOD, "outside"))
    out["passes"] = int(flow.pass_open.sum()), len(flow.pass_open)
    return out


def main():
    rows = []
    for name, om in OMEGAS.items():
        for e in EPS:
            for d in DELTAS:
                p = Params(eps=float(e), omega=om)
                rows.append((name, float(e), d, cell(p, d)))
    same = lambda a, b: a["observed"] == b["observed"] and a["false"] == b["false"]
    ok = lambda r: r["observed"] == r["true"] and r["false"] == 0
    summary = {"cells": len(rows),
               "relational == original": sum(same(r["relational"], r["original"]) for *_, r in rows)}
    for w in WARPS:
        summary[f"inside {w}: counts unchanged"] = sum(same(r[f"inside {w}"], r["original"]) for *_, r in rows)
        summary[f"outside {w}: counts unchanged"] = sum(same(r[f"outside {w}"], r["original"]) for *_, r in rows)
        summary[f"outside {w}: verdict unchanged"] = sum(ok(r[f"outside {w}"]) == ok(r["original"]) for *_, r in rows)
        summary[f"outside {w}: mean |obs-true|"] = float(np.mean([abs(r[f"outside {w}"]["observed"] - r[f"outside {w}"]["true"]) for *_, r in rows]))
    summary["original: mean |obs-true|"] = float(np.mean([abs(r["original"]["observed"] - r["original"]["true"]) for *_, r in rows]))
    summary["original: cells where observer agrees with truth"] = sum(ok(r["original"]) for *_, r in rows)

    # Can the toroidal phase serve as a clock?
    mono = {}
    for flip in ["off", "kick", "reflect"]:
        for lock in [False, True]:
            vals = [Flow(Params(eps=float(e), lock=lock, flip=flip), 60).theta_is_monotone() for e in EPS]
            mono[f"lock={lock}, flip={flip}"] = f"{sum(vals)}/{len(vals)} eps values"
    summary["theta usable as a clock"] = mono
    print(json.dumps(summary, indent=2))
    json.dump(summary, open("results/relational_check.json", "w"), indent=2)


if __name__ == "__main__":
    main()
