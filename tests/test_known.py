"""Known results the model must reproduce before anything new is trusted."""
import math
import numpy as np
import pytest

from torus_count.rotation import first_return, return_times, convergent_denominators
from torus_count.dynamics import Params, Flow, aligned_start, GOLD, SQRT2M1


def test_three_gap():
    rng = np.random.default_rng(1)
    for _ in range(200):
        alpha, length, x0 = rng.random(), rng.uniform(0.005, 0.3), rng.random()
        gaps = np.unique(return_times(alpha, length, x0, n=60_000))
        assert len(gaps) <= 3
        if len(gaps) == 3:
            assert gaps[2] == gaps[0] + gaps[1]


@pytest.mark.parametrize("alpha", [GOLD, SQRT2M1, math.pi - 3, math.e - 2])
def test_first_returns_are_convergent_denominators(alpha):
    dens = set(convergent_denominators(alpha, 10**7))
    for delta in np.logspace(-1, -6, 60):
        assert first_return(alpha, delta) in dens


def test_golden_returns_are_fibonacci():
    fib = [1, 2]
    while fib[-1] < 10**7:
        fib.append(fib[-1] + fib[-2])
    seen = {first_return(GOLD, d) for d in np.logspace(-1, -5.5, 80)}
    assert seen <= set(fib) and len(seen) >= 10


@pytest.mark.parametrize("length", [0.1, 0.03, 0.01])
def test_kac_mean_return(length):
    gaps = return_times(GOLD, length, 0.0, n=2_000_000)
    assert abs(gaps.mean() - 1 / length) / (1 / length) < 0.01


@pytest.mark.parametrize("frames_per_cycle,ok", [(8, True), (4, True), (2.5, True), (1.8, False), (1.3, False)])
def test_nyquist(frames_per_cycle, ok):
    du = 1 / frames_per_cycle                  # poloidal phase per frame
    n = 4096
    signal = np.cos(2 * np.pi * np.arange(n) * du)
    est = np.argmax(np.abs(np.fft.rfft(signal))[1:]) + 1
    assert (abs(est / n - du) < 2 / n) == ok


def test_eps0_selection_rule():
    for pp in range(1, 7):
        for tt in range(1, 7):
            if math.gcd(pp, tt) != 1:
                continue
            for k in range(1, 9):
                p = Params(eps=0.0, omega=pp / tt, k=k, lock=False)
                p = p.with_(th0=aligned_start(p))
                f = Flow(p, u_max=40 * pp + 1)
                assert f.pass_open.all() == (k % pp == 0), (pp, tt, k)
