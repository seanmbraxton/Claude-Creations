"""Checks on the lineage enumeration against known mathematics."""
from fractions import Fraction
import pytest

from torus_count.hurwitz import hurwitz, vortex_type, genus, phase_wheel_closes


def sigma(n):
    return sum(k for k in range(1, n + 1) if n % k == 0)


@pytest.mark.parametrize("d", [1, 2, 3, 4, 5])
def test_unbranched_lineages_count_divisor_sums(d):
    """Closed families with d children and no vortices are the d-sheeted covers of a
    torus; there are sigma(d) of them, i.e. the weighted count is sigma(d)/d."""
    w, _ = hurwitz(d, [])
    assert w == Fraction(sigma(d), d)


def test_single_simple_vortex_never_closes():
    """A lone vortex that swaps two children is an odd shuffle; the rim is even."""
    for d in range(2, 6):
        assert hurwitz(d, [vortex_type(d, 2)])[1] == 0


def test_phase_wheel_confinement():
    assert phase_wheel_closes(["2/3", "-1/3", "-1/3"])
    assert not phase_wheel_closes(["1/3"])
    assert not phase_wheel_closes(["1/3", "1/3"])
    assert phase_wheel_closes(["1/3", "1/3", "1/3"])      # total 1: needs a twist of 1


def test_genus_is_whole():
    for d in range(2, 6):
        for t1 in range(2, d + 1):
            for t2 in range(2, d + 1):
                if hurwitz(d, [vortex_type(d, t1), vortex_type(d, t2)])[1]:
                    assert genus(d, [vortex_type(d, t1), vortex_type(d, t2)]).denominator == 1


def test_two_simple_vortices_match_quasimodular_formula():
    """Dijkgraaf: two simple branch points over a torus are counted by
    (10 E2^3 - 6 E2 E4 - 4 E6)/103680 with unlabelled branch points; labelled = 2x."""
    expected = {2: 1, 3: 8, 4: 30, 5: 80}
    for d, e in expected.items():
        assert hurwitz(d, [vortex_type(d, 2), vortex_type(d, 2)])[0] == 2 * e
