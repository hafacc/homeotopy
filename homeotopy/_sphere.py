from dataclasses import dataclass
from functools import cache

import numpy as np
from numpy.typing import NDArray

from ._homeomorphism import Topology


@dataclass(frozen=True, slots=True)
class Sphere(Topology):
    """The topology of the unit sphere.

    This represents all points in R^n s.t. ||x||_2 = 1, except for the point
    (1, 0, ..., 0). That point is considered the boundary of the space, and will
    be mapped to the largest closed point in some other topologies.

    Remarks
    -------
    If you had points on the surface of another p-ball, you could use the ball
    homeomorphism to first map them onto the surface of the 2-ball, and then
    apply this homeomorphism.
    """

    # NOTE for both of these we need to special case (1, 0, ..., 0) to (1, 1, ..., 1) and vice versa
    def to_inf_ball(self, points: NDArray[np.floating]) -> NDArray[np.floating]:
        dim = points.shape[-1]
        if dim < 2:  # noqa: PLR2004
            raise ValueError(f"sphere points must have at least 2 coordinates: {dim}")

        tiny = np.finfo(points.dtype).smallest_normal
        scale = 1 - points[..., :1]

        normal = np.tanh(points[..., 1:] / np.maximum(scale, tiny))
        return np.where(scale <= 0, 1, normal)

    def from_inf_ball(self, points: NDArray[np.floating]) -> NDArray[np.floating]:
        big = np.finfo(points.dtype).max
        with np.errstate(divide="ignore"):
            plane = np.arctanh(points)

        s2 = (plane[..., None, :] @ plane[..., None])[..., 0]
        s2p = np.minimum(s2 + 1, big)

        x0 = np.where(s2 == np.inf, 1, (s2 - 1) / s2p)
        xns = np.where(s2 == np.inf, 0, 2 * plane / s2p)
        return np.concatenate([x0, xns], -1)


@cache
def sphere() -> Sphere:
    """Create a topology for the unit sphere."""
    return Sphere()
