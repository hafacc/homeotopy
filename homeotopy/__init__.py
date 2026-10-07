"""A library for creating some standard homeomorphisms.

This library is based around a set of `Topologies`. Calling `homeomorphism` with
two Topologies creates a homeomorphism from one topology to the other.
Topologies should specify their domains, but where unspecified, the topologies
try to conform to a reasonable standard domain. The homeomorphism should work
for closed set elements too, but those elements may not be bijective.

Remarks
-------
It's probably important to note that floating point numbers are not real
numbers, and so none of these are really bijective at all.

Also note that this library does not define homeotopies. It's just named this
to have "py" in the name.
"""

from ._ball import Ball, ball
from ._cube import Cube, cube
from ._homeomorphism import Homeomorphism, Topology, homeomorphism
from ._plane import Plane, plane
from ._simplex import Simplex, simplex
from ._sphere import Sphere, sphere

__all__ = (
    "Ball",
    "Cube",
    "Homeomorphism",
    "Plane",
    "Simplex",
    "Sphere",
    "Topology",
    "ball",
    "cube",
    "homeomorphism",
    "plane",
    "simplex",
    "sphere",
)
