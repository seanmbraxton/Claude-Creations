"""The grandparent rule: every family is a three-generation loop."""
from fractions import Fraction as F
from torus_count.lineage import search, search_grandparent, weakly_connected, generations, charge_matrices


def fams(n):
    return [g for g in search_grandparent(n) if weakly_connected(g)]


def test_fast_search_matches_plain_search():
    for n in range(2, 7):
        assert sorted(fams(n)) == sorted(g for g in search(n, 2) if weakly_connected(g))


def test_smallest_family_has_six_tori():
    for n in range(2, 6):
        assert fams(n) == []
    assert len(fams(6)) == 30


def test_every_family_is_a_three_generation_loop():
    for n in (6, 7):
        for g in fams(n):
            sizes = generations(g, 2)
            assert sizes is not None and min(sizes) >= 2


def test_unit_charges_need_even_generations():
    assert charge_matrices(3, [F(-1), F(1)]) == 0
    assert charge_matrices(2, [F(-1), F(1)]) == 2


def test_thirds_triple_passes_through_generations():
    from itertools import product
    rows = [r for r in product([F(2, 3), F(-1, 3)], repeat=3) if sum(r) == 0]
    balanced = [M for M in product(rows, repeat=3) if all(sum(M[i][j] for i in range(3)) == 0 for j in range(3))]
    assert len(balanced) == 6
    for M in balanced:                      # each child receives exactly one +2/3
        assert all(sum(1 for i in range(3) if M[i][j] == F(2, 3)) == 1 for j in range(3))
