from torus_count.two_parents import families_ext


def test_dual_tetrahedron_smallest_family_is_eight():
    for n in range(3, 8):
        assert families_ext(n, dual=True, no_mutual=True) == []
    assert len(families_ext(8, dual=True, no_mutual=True)) == 4
    assert len(families_ext(8, dual=True, no_mutual=True, siblings=True)) == 2
