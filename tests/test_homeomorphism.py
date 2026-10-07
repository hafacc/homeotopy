"""Tests for the homeomorphism builder."""

import numpy as np

import homeotopy


def test_composition() -> None:
    """Test composing transforms with homeomorphism."""
    rng = np.random.default_rng(0)
    homeo = homeotopy.homeomorphism(homeotopy.simplex(), homeotopy.sphere())

    simplex = rng.dirichlet(np.ones(4), (2, 5))
    sphere = homeo(simplex)
    assert np.allclose(np.linalg.norm(sphere, 2, -1), 1)

    inv = ~homeo
    actual = inv(sphere)
    assert np.allclose(simplex, actual)


def test_integer_input() -> None:
    """Test that integer input is converted to float64."""
    homeo = homeotopy.homeomorphism(homeotopy.simplex(), homeotopy.cube())
    result = homeo(np.array([[1, 0, 0], [0, 1, 0]]))
    assert result.dtype == np.float64


def test_list_input() -> None:
    """Test that nested-list input is converted to float64."""
    homeo = homeotopy.homeomorphism(homeotopy.simplex(), homeotopy.cube())
    result = homeo([[1, 0, 0], [0, 0.5, 0.5]])
    assert result.dtype == np.float64
    assert result.shape == (2, 2)


def test_float32_input() -> None:
    """Test that float32 input stays float32."""
    homeo = homeotopy.homeomorphism(homeotopy.simplex(), homeotopy.cube())
    result = homeo(np.array([[1, 0, 0], [0, 0.5, 0.5]], np.float32))
    assert result.dtype == np.float32
