"""Tests for simplex projections."""

import numpy as np
import pytest

import homeotopy


def test_known() -> None:
    """Test projecting known points."""
    simplex = homeotopy.simplex()

    simplex_points = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1 / 2, 1 / 2], [1 / 3, 1 / 3, 1 / 3]],
        "f8",
    )
    inf_ball_points = np.array(
        [[-1, -1 / 3**0.5], [1, -1 / 3**0.5], [0, 1], [1, 1 / 3**0.5], [0, 0]], "f8"
    )
    assert np.allclose(simplex.to_inf_ball(simplex_points), inf_ball_points)
    assert np.allclose(simplex.from_inf_ball(inf_ball_points), simplex_points)


def test_random() -> None:
    """Test projecting random points satisfy invariants."""
    rng = np.random.default_rng(0)
    simplex = homeotopy.simplex()

    inf_ball_points = rng.uniform(-1, 1, (3, 4, 5))
    simplex_points = simplex.from_inf_ball(inf_ball_points)
    assert np.allclose(simplex.to_inf_ball(simplex_points), inf_ball_points)


def test_too_few_dimensions() -> None:
    """Exception thrown when simplex points have fewer than 2 coordinates."""
    simplex = homeotopy.simplex()
    with pytest.raises(ValueError, match="at least 2 coordinates"):
        simplex.to_inf_ball(np.ones((3, 1)))
