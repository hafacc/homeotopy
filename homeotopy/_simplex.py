from dataclasses import dataclass
from functools import cache

import numpy as np
from numpy.typing import NDArray

from ._homeomorphism import Topology


@cache
def basis(dim: int) -> NDArray[np.float64]:
    """Create a basis for rotating the simplex onto the origin of dim - 1.

    The result has shape (dim - 1, dim) and is read-only.
    """
    nums = np.arange(1, dim)
    frac = 1 / (nums + 1)
    res = np.tril(np.ones((dim - 1, dim))) * (-((frac / nums) ** 0.5))[:, None]
    res[np.arange(dim - 1), nums] = (1 - frac) ** 0.5
    res.flags.writeable = False
    return res


@dataclass(frozen=True, slots=True)
class Simplex(Topology):
    """The topology of the simplex.

    This represents all points in R^n s.t. 0 < x_i and Σx_i = 1.
    """

    def to_inf_ball(self, points: NDArray[np.floating]) -> NDArray[np.floating]:
        dim = points.shape[-1]
        if dim < 2:  # noqa: PLR2004
            raise ValueError(f"simplex points must have at least 2 coordinates: {dim}")

        tiny = np.finfo(points.dtype).smallest_normal

        simp_direc = points - np.full(dim, 1 / dim, points.dtype)
        isimp_a = dim * np.maximum(-simp_direc, simp_direc / (dim - 1)).max(-1)

        cube_direc = simp_direc @ basis(dim).astype(points.dtype, copy=False).T
        icube_a = np.max(np.abs(cube_direc), -1) + tiny

        return np.clip(cube_direc * (isimp_a / icube_a)[..., None], -1, 1)

    def from_inf_ball(self, points: NDArray[np.floating]) -> NDArray[np.floating]:
        tiny = np.finfo(points.dtype).smallest_normal
        dim = points.shape[-1]

        icube_a = np.max(np.abs(points), -1)

        simp_direc = points @ basis(dim + 1).astype(points.dtype, copy=False)
        isimp_a = (dim + 1) * np.maximum(-simp_direc, simp_direc / dim).max(-1) + tiny

        raw = simp_direc * (icube_a / isimp_a)[..., None] + np.full(
            dim + 1, 1 / (dim + 1), points.dtype
        )
        return np.clip(raw, 0, 1)


@cache
def simplex() -> Simplex:
    """Create the topology of the simplex."""
    return Simplex()
