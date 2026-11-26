"""Time as the relations of change: what must and must not depend on a clock."""
import math
import numpy as np
import pytest

from torus_count.dynamics import Params, Flow, GOLD, SQRT2M1
from torus_count.observer import observe, truth_visits, match
from torus_count import clocks, outside_time

CASES = [(e, d, om) for e in (-0.3, 0.0, 0.25) for d in (0.01, 0.03, 0.1) for om in (GOLD, SQRT2M1, 1 / 3)]


def setup(eps, delta, omega, T=30.0):
    p = Params(eps=eps, omega=omega)
    dt = delta / math.hypot(1, omega)
    n = int(T / dt)
    flow = Flow(p, omega * n * dt + 1)
    visits = truth_visits(flow, delta, omega * n * dt, omega * dt / 16)
    run = lambda fu: match(observe(flow, fu, delta), visits, omega * dt / 16)
    return p, dt, n, run


@pytest.mark.parametrize("eps,delta,omega", CASES)
def test_relational_rewrite_reproduces_original(eps, delta, omega):
    p, dt, n, run = setup(eps, delta, omega)
    assert np.allclose(clocks.relational(omega * dt, n), clocks.external(dt, n, omega))
    assert run(clocks.relational(omega * dt, n)) == run(clocks.external(dt, n, omega))


@pytest.mark.parametrize("eps,delta,omega", CASES)
@pytest.mark.parametrize("warp", [0.3, 0.9])
def test_global_retiming_changes_nothing(eps, delta, omega, warp):
    """An uneven outside clock that drives every change, the shutter included."""
    p, dt, n, run = setup(eps, delta, omega)
    fu = outside_time.frames_u(omega, dt, n, warp, 2.5, "inside")
    assert run(fu) == run(clocks.external(dt, n, omega))


def test_changing_the_shutter_relation_changes_counts():
    """Only the shutter runs on the uneven clock: a different relation, so counts may differ."""
    changed = 0
    for eps, delta, omega in CASES:
        p, dt, n, run = setup(eps, delta, omega)
        fu = outside_time.frames_u(omega, dt, n, 0.9, 2.5, "outside")
        changed += run(fu) != run(clocks.external(dt, n, omega))
    assert changed > 0


def test_which_changes_can_be_clocks():
    for e in (-0.3, 0.0, 0.3):
        assert Flow(Params(eps=e, lock=False), 50).theta_is_monotone()
    assert not Flow(Params(eps=0.3, lock=True), 50).theta_is_monotone()
    assert not Flow(Params(eps=-0.3, lock=False, flip="reflect"), 50).theta_is_monotone()
