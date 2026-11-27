from math import radians, log
from torus_count.passage import passage

CH = [1 / 3, -1 / 3, 1 / 3, -1 / 3, 1 / 3, -1 / 3, 1 / 3, -1 / 3]


def test_steep_crosses_instantly():
    steps, depth, t, _ = passage(radians(60), 0.05, CH)
    assert depth == 0 and steps[-1][2] == "cross" and t < 0.06


def test_grazing_climbs_and_deeper_with_flatter_angle():
    depths = [passage(radians(a), 0.05, CH)[1] for a in (2, 0.1, 0.005)]
    assert depths == sorted(depths) and depths[0] >= 1 and depths[-1] > depths[0]


def test_depth_grows_like_log_of_flatness():
    eps = 0.1
    for a in (1e-2, 1e-4, 1e-6):
        d = passage(a, eps, CH)[1]
        assert abs(d - log(a) / log(eps)) <= 1.5


def test_neutral_child_stops_the_climb():
    steps, depth, _, _ = passage(1e-9, 0.1, [2 / 3, -1 / 3, 0.0])
    assert depth == 2 and steps[-1][2] == "neutral"


def test_lived_time_is_an_aeon_when_parent_time_is_an_instant():
    _, depth, t, lived = passage(radians(1), 0.05, CH)
    assert depth >= 1 and abs(lived / t - 0.05 ** -depth) < 1e-6 * 0.05 ** -depth


def test_parent_clock_never_exceeds_one_seam_width_scale():
    for a in (1e-6, 1e-3, 0.05, 0.5, 1.5):
        _, _, t, _ = passage(a, 0.05, CH)
        assert t <= 1.0 + 1e-12
