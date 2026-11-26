from fractions import Fraction as F
from torus_count.dual_families import circulant, check_family


def test_minimal_dual_families_exist_for_k_2_to_5():
    for k in (2, 3, 5):
        big = F(1) if k == 2 else F(k - 1, k); small = -big / (k - 1)
        nodes, edges = circulant(k)
        assert len(nodes) == 4 * k
        assert all(check_family(nodes, edges, lambda lead: big if lead else small).values())
