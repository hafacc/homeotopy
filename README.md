# Homeotopy

[![build](https://github.com/hafacc/homeotopy/actions/workflows/build.yml/badge.svg)](https://github.com/hafacc/homeotopy/actions/workflows/build.yml)
[![pypi](https://img.shields.io/pypi/v/homeotopy)](https://pypi.org/project/homeotopy/)
[![docs](https://img.shields.io/badge/api-docs-blue)](https://hafa.cc/homeotopy)

A python library for computing homeomorphisms between some common continuous
spaces.

## Installation

```sh
pip install homeotopy
```

## Usage

```py
import numpy as np

import homeotopy

rng = np.random.default_rng(0)
points = rng.dirichlet(np.ones(4), 10)  # 10 points on the simplex in R^4
# create a mapping from the simplex to the surface of the sphere
mapping = homeotopy.homeomorphism(homeotopy.simplex(), homeotopy.sphere())
sphere_points = mapping(points)

rev_mapping = ~mapping
duplicate_points = rev_mapping(sphere_points)
```

## Development

### Checks

```sh
uv run ruff format --check
uv run ruff check
uv run pyright
uv run pytest
```

### Publishing

Releases are cut manually: run the [`release` workflow](https://github.com/hafacc/homeotopy/actions/workflows/release.yml)
from the Actions tab and pick a version bump (patch/minor/major). It runs the checks,
bumps the version, builds and publishes to PyPI via
[trusted publishing](https://docs.pypi.org/trusted-publishers/) (no API token), tags the
release, and deploys the docs.
