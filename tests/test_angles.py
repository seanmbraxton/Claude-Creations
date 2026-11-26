import numpy as np
from torus_count.angles import rotation_families, rotation_family, realign
from torus_count.explore import adjacency, ramanujan


def test_rotation_families_worst_eigenvalue_is_2cos_pi_over_L():
    for N in range(6, 32, 2):
        for a, b in rotation_families(N):
            ok, worst, _ = ramanujan(adjacency(*rotation_family(N, a, b)))
            L = realign(N, a, b)
            assert abs(worst - 2 * np.cos(np.pi / L)) < 1e-9
            assert ok == (L <= 4)
