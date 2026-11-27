from fractions import Fraction as F
from math import gcd, log2, sqrt
from torus_count.superposed_pairing import generations_to_neutral as gens, euclid_steps


def test_rational_resolves_irrational_does_not():
    assert gens(F(2, 3), 1) == 3
    assert gens((sqrt(5) - 1) / 2, 1.0, cap=25) is None
    assert gens(1 / sqrt(2), 1.0, cap=25) is None


def test_depends_only_on_reduced_ratio():
    for p, q in [(2, 3), (5, 8), (4, 9)]:
        assert gens(p, q) == gens(3 * p, 3 * q) == gens(F(p, 7), F(q, 7))


def test_lopsided_parents_are_slow():
    for q in range(2, 30):
        assert gens(1, q) == q


def test_every_pairing_beats_the_single_path():
    for q in range(5, 40):
        for p in range(1, q):
            if gcd(p, q) == 1:
                assert gens(p, q) <= euclid_steps(q, p) + 1


def test_comparable_parents_resolve_in_about_log_q():
    for q in [31, 61, 101]:
        mid = [gens(p, q) for p in range(q // 4, 3 * q // 4) if gcd(p, q) == 1]
        assert max(mid) <= 1.5 * log2(q) + 4
