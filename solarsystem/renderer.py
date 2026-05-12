"""Plotly 3D figure builder for the solar system orrery."""

import math
import numpy as np
import plotly.graph_objects as go
from solarsystem.config import (
    PLANETS, SUN_COLOR, SUN_RENDER_SIZE,
    BACKGROUND_COLOR, SATURN_RING_COLOR, SATURN_RING_SCALE,
)

_NO_PROJECTION = dict(
    x=dict(show=False),
    y=dict(show=False),
    z=dict(show=False),
)


def _add_stars(fig: go.Figure) -> None:
    """Scatter 2000 random points on a sphere to simulate a starfield."""
    rng = np.random.default_rng(seed=42)  # fixed seed for reproducibility across renders
    xyz = rng.standard_normal((3, 2000))
    xyz /= np.linalg.norm(xyz, axis=0)  # normalize to unit sphere
    xyz *= 50  # scale to 50 AU radius
    star_x, star_y, star_z = xyz[0], xyz[1], xyz[2]
    fig.add_trace(go.Scatter3d(
        x=star_x.tolist(), y=star_y.tolist(), z=star_z.tolist(),
        mode="markers",
        marker=dict(size=0.8, color="#ffffff", opacity=0.6),
        hoverinfo="skip",
        showlegend=False,
    ))


def _add_sun(fig: go.Figure) -> None:
    """Add the Sun as a marker at the origin."""
    fig.add_trace(go.Scatter3d(
        x=[0.0], y=[0.0], z=[0.0],
        mode="markers",
        marker=dict(size=SUN_RENDER_SIZE, color=SUN_COLOR, symbol="circle"),
        name="Sun",
        hovertext="Sun",
        hoverinfo="text",
        projection=_NO_PROJECTION,
    ))
    fig.add_trace(go.Scatter3d(
        x=[0.0], y=[0.0], z=[0.0],
        mode="markers",
        marker=dict(size=22, color=SUN_COLOR, opacity=0.15, symbol="circle"),
        hoverinfo="skip",
        showlegend=False,
        name="Sun glow",
        projection=_NO_PROJECTION,
    ))


def _add_orbit(
    fig: go.Figure,
    planet: dict,
    path: list[tuple[float, float, float]],
) -> None:
    """Add a planet's orbital path as a faint line."""
    xs, ys, zs = zip(*path)
    fig.add_trace(go.Scatter3d(
        x=list(xs), y=list(ys), z=list(zs),
        mode="lines",
        line=dict(color=planet["color"], width=1),
        opacity=0.5,
        name=f"{planet['name']} orbit",
        hoverinfo="skip",
        showlegend=False,
    ))


def _add_planet(
    fig: go.Figure,
    planet: dict,
    position: tuple[float, float, float],
    date: str,
) -> None:
    """Add a planet as a marker with tooltip and optional label."""
    x, y, z = position
    if planet["name"] == "Moon":
        x = x + 0.05  # cosmetic offset only — Moon otherwise overlaps Earth in the scene
    distance = math.sqrt(x**2 + y**2 + z**2)

    unlabelled = {"Moon", "Pluto"}  # too small/distant; labels cause clutter
    if planet["name"] in unlabelled:
        mode = "markers"
        text = None
        textposition = None
        textfont = None
    else:
        mode = "markers+text"
        text = planet["name"]
        textposition = "top center"
        textfont = dict(color="#ffffff", size=10)

    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode=mode,
        marker=dict(size=planet["render_size"], color=planet["color"], symbol="circle"),
        name=planet["name"],
        hovertext=f"{planet['name']}<br>{distance:.2f} AU<br>{date}",
        hoverinfo="text",
        projection=_NO_PROJECTION,
        text=text,
        textposition=textposition,
        textfont=textfont,
    ))


def _add_saturn_rings(
    fig: go.Figure,
    position: tuple[float, float, float],
) -> None:
    """Add a flat elliptical ring around Saturn."""
    x, y, z = position
    # Fixed 1.5 AU radius — large enough to always be visible at any zoom level
    ring_radius = 1.5
    angles = np.linspace(0, 2 * math.pi, 200)
    ring_x = [x + ring_radius * math.cos(a) for a in angles]
    ring_y = [y + ring_radius * math.sin(a) for a in angles]
    ring_z = [z] * 200
    fig.add_trace(go.Scatter3d(
        x=ring_x, y=ring_y, z=ring_z,
        mode="lines",
        line=dict(color=SATURN_RING_COLOR, width=3),
        opacity=0.6,
        name="Saturn rings",
        hoverinfo="skip",
        showlegend=False,
    ))


def _apply_layout(fig: go.Figure, date: str) -> None:
    """Apply dark theme, camera, and axis settings to the figure."""
    # showbackground=False removes the white box that Plotly draws around the 3D scene
    axis = dict(
        showbackground=False,
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showspikes=False,
        title="",
        range=[-50, 50],  # ±50 AU covers Neptune (30 AU) and Uranus (19 AU) without clipping
    )
    fig.update_layout(
        title=f"Solar System — {date}",
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font=dict(color="#ffffff"),
        showlegend=True,
        legend=dict(bgcolor="#111111", font=dict(color="#ffffff")),
        scene=dict(
            bgcolor=BACKGROUND_COLOR,
            xaxis=axis,
            yaxis=axis,
            zaxis=axis,
            camera=dict(eye=dict(x=0.8, y=0.6, z=0.5)),
            aspectmode="cube",  # uniform cube prevents AU scaling from making planets microscopic
        ),
    )


def build_figure(
    positions: dict[str, tuple[float, float, float]],
    orbits: dict[str, list[tuple[float, float, float]]],
    date: str,
) -> go.Figure:
    """Build a Plotly 3D figure of the solar system with Sun at origin."""
    fig = go.Figure()

    _add_stars(fig)
    _add_sun(fig)

    for planet in PLANETS:
        _add_orbit(fig, planet, orbits[planet["name"]])

    for planet in PLANETS:
        _add_planet(fig, planet, positions[planet["name"]], date)

    _add_saturn_rings(fig, positions["Saturn"])

    _apply_layout(fig, date)

    return fig
