# 🪐 solarsystem

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)
![Tests passing](https://img.shields.io/badge/tests-12%20passing-brightgreen)

An interactive 3D orrery of the solar system with real planetary positions from NASA JPL ephemerides, rendered as a standalone HTML file.

---

## Demo

The output is a fully interactive HTML file — rotate the scene, zoom in and out, and hover over any planet to see its name, distance from the Sun, and the current date. No server or install required for the viewer.

> 📸 Screenshot / GIF coming soon

---

## ✨ Features

- Real planetary positions via NASA JPL DE440 ephemerides (Astropy)
- All 8 planets + Moon + Pluto
- Interactive 3D scene: rotate, zoom, hover tooltips
- Saturn's rings rendered
- Starfield background (2000 stars)
- Standalone HTML output — no server, no install for the viewer
- Rich CLI with progress bars and colored output
- Snapshot mode (single date) and animate mode (date range with slider)
- 12 passing integration tests

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/alessandrooliverio/solarsystem.git
cd solarsystem

# 2. Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python3 main.py now
```

---

## Usage

```bash
# Snapshot of today
python3 main.py now

# Snapshot of a specific date
python3 main.py --date 2030-06-21

# Animate one year, one frame per day
python3 main.py animate --days 365

# Animate one year, one frame per week (faster)
python3 main.py animate --days 365 --step 7

# Custom output path
python3 main.py now --output my_orrery.html
```

All commands write a self-contained `orrery.html` (or the path you specify) that opens directly in any browser.

---

## Project structure

```
solarsystem/
├── solarsystem/
│   ├── __init__.py
│   ├── config.py        planet metadata (name, color, radius, period, body_name)
│   ├── planets.py       get_positions(time) → dict[str, tuple[float,float,float]]
│   ├── orbits.py        get_orbit_paths(n_points) → dict[str, list[tuple]]
│   ├── renderer.py      build_figure(positions, orbits, date) → go.Figure
│   └── exporter.py      save_html(fig, path) → None
├── tests/
│   ├── __init__.py
│   ├── test_planets.py
│   └── test_orbits.py
├── main.py              CLI entry point
├── requirements.txt
├── CONTEXT.md
├── DECISIONS.md
├── README.md
└── LICENSE
```

---

## Stack

| Layer | Technology |
|---|---|
| Computation | Astropy + NumPy |
| Visualization | Plotly (`go.Figure`) |
| CLI | argparse + Rich |
| Output | Standalone HTML via CDN |

---

## How it works

Planetary positions are computed using NASA JPL's DE440 ephemeris via Astropy's `get_body_barycentric`. Each planet is queried in the barycentric ICRS frame, then converted to heliocentric coordinates by subtracting the Sun's barycentric position. All coordinates are returned in Astronomical Units (AU), with the Sun fixed at the origin.

The rendering pipeline builds a Plotly `go.Figure` composed entirely of `go.Scatter3d` traces: a starfield sphere, the Sun with a glow effect, faint orbital path lines sampled at evenly spaced intervals over each body's sidereal period, planet markers with hover tooltips, and Saturn's rings as a flat ellipse. The figure is exported to a self-contained HTML file using Plotly's CDN mode, keeping the output under 200 KB.

The CLI is built with `argparse` and dispatches to one of two pipelines: `snapshot` calls `get_positions` once and renders a single frame; `animate` pre-samples all orbit paths once, then builds a `go.Frame` per time step and attaches a date slider and play/pause controls to the figure. All terminal output — progress bars, export confirmations, and error messages — goes through Rich.

---

## Tests

There are 12 integration tests spread across two files, all running against the real DE440 ephemeris with no mocking. They verify body count, coordinate types, Sun placement at the origin, Earth's distance from the Sun, Mercury's perihelion/aphelion range, and correct orbit path structure.

```bash
python3 -m pytest tests/ -v
```

---

## License

MIT — see [LICENSE](LICENSE).

---

## Author

Alessandro Oliverio — [github.com/alessandrooliverio](https://github.com/alessandrooliverio)
