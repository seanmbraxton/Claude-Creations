from math import comb
from torus_count.interference import amplitude, survivors


def test_equal_spacing_survivors_are_divisors():
    for M in range(1, 13):
        assert survivors(M) == [k for k in range(1, M + 1) if M % k == 0]


def test_survivors_have_unit_size():
    for M in range(1, 11):
        for k in survivors(M):
            assert abs(abs(amplitude(M, k)) - 1) < 1e-9


def test_prime_charges_only_survive_whole_or_all_ones():
    for p in [2, 3, 5, 7, 11]:
        assert survivors(p) == [1, p]


def test_arcs_by_charge_never_cancel():
    # with arcs proportional to charge every split carries the same phase, pi * M
    for M in range(1, 10):
        for k in range(1, M + 1):
            assert abs(abs(amplitude(M, k, "by_charge")) - comb(M - 1, k - 1)) < 1e-6
