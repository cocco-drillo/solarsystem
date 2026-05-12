"""Integration tests for solarsystem.orbits — real DE440 ephemeris."""

import math
import pytest
from astropy.time import Time
from solarsystem.orbits import get_orbit_paths
from solarsystem.config import PLANETS


# Verifies the result contains exactly all configured planet bodies
def test_returns_all_bodies():
    paths = get_orbit_paths(n_points=10)
    assert set(paths.keys()) == {p["name"] for p in PLANETS}
    assert len(paths) == len(PLANETS)


# Verifies every orbit path has exactly the requested number of sample points
def test_correct_number_of_points():
    paths = get_orbit_paths(n_points=10)
    for planet in PLANETS:
        assert len(paths[planet["name"]]) == 10, (
            f"{planet['name']}: expected 10 points, got {len(paths[planet['name']])}"
        )


# Verifies every sample point is a tuple of three plain Python floats
def test_all_tuples_of_three_floats():
    paths = get_orbit_paths(n_points=5)
    for planet in PLANETS:
        for i, point in enumerate(paths[planet["name"]]):
            assert isinstance(point, tuple), f"{planet['name']}[{i}]: expected tuple"
            assert len(point) == 3, f"{planet['name']}[{i}]: expected length 3"
            for j, val in enumerate(point):
                assert isinstance(val, float), (
                    f"{planet['name']}[{i}][{j}]: expected float, got {type(val)}"
                )


# Verifies Mercury's sampled positions stay within its known perihelion/aphelion range
def test_mercury_orbit_radius():
    paths = get_orbit_paths(n_points=20)
    for i, (x, y, z) in enumerate(paths["Mercury"]):
        dist = math.sqrt(x**2 + y**2 + z**2)
        assert 0.28 < dist < 0.48, (
            f"Mercury point {i}: distance {dist:.4f} AU outside [0.28, 0.48]"
        )


# Verifies Earth's sampled positions stay within its nearly circular orbit (~1 AU)
def test_earth_orbit_radius():
    paths = get_orbit_paths(n_points=20)
    for i, (x, y, z) in enumerate(paths["Earth"]):
        dist = math.sqrt(x**2 + y**2 + z**2)
        assert 0.98 < dist < 1.02, (
            f"Earth point {i}: distance {dist:.4f} AU outside [0.98, 1.02]"
        )


# Verifies the optional reference_time parameter is accepted and returns correct structure
def test_reference_time_parameter():
    paths = get_orbit_paths(n_points=5, reference_time=Time("2026-01-01", scale="utc"))
    assert len(paths) == len(PLANETS)
    assert set(paths.keys()) == {p["name"] for p in PLANETS}
