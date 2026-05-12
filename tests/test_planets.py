"""Integration tests for solarsystem.planets — real DE440 ephemeris."""

import math
import pytest
from astropy.time import Time
from solarsystem.planets import get_positions
from solarsystem.config import PLANETS


# Verifies the result contains Sun and all configured planets
def test_returns_all_bodies():
    positions = get_positions(Time("2026-05-12", scale="utc"))
    expected = {"Sun"} | {p["name"] for p in PLANETS}
    assert set(positions.keys()) == expected
    assert len(positions) == len(PLANETS) + 1


# Verifies the Sun is always placed at the heliocentric origin
def test_sun_at_origin():
    positions = get_positions(Time("2026-05-12", scale="utc"))
    assert positions["Sun"] == (0.0, 0.0, 0.0)


# Verifies Earth's distance from the Sun is within its known orbital range (~1 AU)
def test_earth_distance():
    positions = get_positions(Time("2026-05-12", scale="utc"))
    x, y, z = positions["Earth"]
    distance = math.sqrt(x**2 + y**2 + z**2)
    assert 0.98 < distance < 1.02, f"Earth distance {distance:.4f} AU outside expected range"


# Verifies all coordinate values are plain Python floats, not numpy scalars
def test_all_values_are_plain_floats():
    positions = get_positions(Time("2026-05-12", scale="utc"))
    for name, (x, y, z) in positions.items():
        assert isinstance(x, float), f"{name}: x is {type(x)}, expected float"
        assert isinstance(y, float), f"{name}: y is {type(y)}, expected float"
        assert isinstance(z, float), f"{name}: z is {type(z)}, expected float"


# Verifies a raw string input raises TypeError instead of silently failing
def test_invalid_input_raises_typeerror():
    with pytest.raises(TypeError):
        get_positions("2026-05-12")


# Verifies Earth moves between two dates 6 months apart
def test_different_dates_give_different_positions():
    pos_jan = get_positions(Time("2026-01-01", scale="utc"))
    pos_jul = get_positions(Time("2026-07-01", scale="utc"))
    assert pos_jan["Earth"] != pos_jul["Earth"]
