"""Matplotlib styling and layout helpers."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

from .palettes import PALETTES, get_palette, master_colour

_CONTEXTS = {
    "paper": {
        "font.size": 9.0, "axes.titlesize": 10.5, "axes.labelsize": 9.5,
        "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
        "legend.fontsize": 8.2, "lines.linewidth": 2.1, "lines.markersize": 5.3,
    },
    "presentation": {
        "font.size": 14.0, "axes.titlesize": 18.0, "axes.labelsize": 15.0,
        "xtick.labelsize": 12.5, "ytick.labelsize": 12.5,
        "legend.fontsize": 12.0, "lines.linewidth": 2.8, "lines.markersize": 7.0,
    },
    "poster": {
        "font.size": 18.0, "axes.titlesize": 24.0, "axes.labelsize": 20.0,
        "xtick.labelsize": 16.0, "ytick.labelsize": 16.0,
        "legend.fontsize": 16.0, "lines.linewidth": 3.4, "lines.markersize": 9.0,
    },
}


def _ui(name: str) -> str:
    return master_colour(PALETTES["ui"][name])


def apply_style(context: str = "paper", palette: str = "balanced_8") -> None:
    """Apply the global Pascoe style to Matplotlib."""
    if context not in _CONTEXTS:
        raise KeyError(f"Unknown context '{context}'. Choose from {sorted(_CONTEXTS)}")
    cycle = get_palette(palette)
    base = {
        "figure.facecolor": _ui("background"),
        "figure.edgecolor": _ui("background"),
        "axes.facecolor": _ui("background"),
        "axes.edgecolor": _ui("axis"),
        "axes.labelcolor": _ui("text"),
        "axes.titlecolor": _ui("text"),
        "axes.titlelocation": "left",
        "axes.titleweight": "semibold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.9,
        "axes.grid": False,
        "axes.axisbelow": True,
        "axes.prop_cycle": cycler(color=cycle),
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
        "font.weight": "normal",
        "text.color": _ui("text"),
        "xtick.color": _ui("text"),
        "ytick.color": _ui("text"),
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "grid.color": _ui("grid"),
        "grid.linewidth": 0.75,
        "grid.alpha": 0.85,
        "legend.frameon": False,
        "legend.borderaxespad": 0.3,
        "legend.handlelength": 1.7,
        "legend.handletextpad": 0.5,
        "savefig.facecolor": _ui("background"),
        "savefig.edgecolor": _ui("background"),
        "savefig.transparent": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.06,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
    base.update(_CONTEXTS[context])
    mpl.rcParams.update(base)


def style_axes(
    ax: mpl.axes.Axes,
    *,
    grid: Literal["x", "y", "both"] | None = None,
    despine: bool = True,
    title_left: bool = True,
    zero_line: bool = False,
) -> mpl.axes.Axes:
    """Apply finishing rules to one axis and return it."""
    ax.set_facecolor(_ui("background"))
    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(_ui("axis"))
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(colors=_ui("text"))
    ax.xaxis.label.set_color(_ui("text"))
    ax.yaxis.label.set_color(_ui("text"))
    if title_left:
        ax.title.set_ha("left")
        ax.title.set_position((0, 1.0))
    ax.grid(False)
    if grid:
        axis = "both" if grid == "both" else grid
        ax.grid(True, axis=axis, color=_ui("grid"), linewidth=0.75, alpha=0.85)
        ax.set_axisbelow(True)
    if zero_line:
        ax.axhline(0, color=_ui("light_border"), linewidth=0.9, zorder=0)
    return ax


def panel_label(
    ax: mpl.axes.Axes,
    label: str,
    *,
    x: float = -0.11,
    y: float = 1.04,
    size: float | None = None,
) -> mpl.text.Text:
    """Add a simple bold panel label in axes coordinates."""
    return ax.text(
        x, y, label, transform=ax.transAxes, ha="left", va="bottom",
        fontsize=size or mpl.rcParams["axes.titlesize"], fontweight="bold",
        color=_ui("text"), clip_on=False,
    )


def add_panel_labels(axes: Iterable[mpl.axes.Axes], labels: Iterable[str] | None = None) -> None:
    """Add sequential A, B, C... labels to an iterable of axes."""
    axes = list(axes)
    if labels is None:
        labels = [chr(65 + i) for i in range(len(axes))]
    for ax, label in zip(axes, labels):
        panel_label(ax, str(label))


def figure_size(
    width: Literal["single", "double", "poster"] | float = "double",
    *,
    aspect: float = 0.68,
    height: float | None = None,
) -> tuple[float, float]:
    """Return a practical figure size in inches."""
    widths = {"single": 3.5, "double": 7.2, "poster": 10.0}
    width_in = widths[width] if isinstance(width, str) else float(width)
    return width_in, float(height) if height is not None else width_in * aspect


def new_figure(
    width: Literal["single", "double", "poster"] | float = "double",
    *,
    aspect: float = 0.68,
    height: float | None = None,
    **kwargs,
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """Create a single-axis figure using the standard size presets."""
    return plt.subplots(figsize=figure_size(width, aspect=aspect, height=height), **kwargs)
