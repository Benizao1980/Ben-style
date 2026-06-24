"""Pascoe Plot Style: reusable scientific figure styling."""

from .palettes import (
    MASTER,
    PALETTES,
    PRESETS,
    master_colour,
    colour,
    get_palette,
    list_palettes,
    get_preset,
    preset_colour,
    categorical_colours,
    source_colour,
    amr_colour,
    make_colormap,
)
from .style import (
    apply_style,
    style_axes,
    panel_label,
    add_panel_labels,
    figure_size,
    new_figure,
)
from .export import save_figure

__all__ = [
    "MASTER", "PALETTES", "PRESETS", "master_colour", "colour",
    "get_palette", "list_palettes", "get_preset", "preset_colour",
    "categorical_colours", "source_colour", "amr_colour", "make_colormap",
    "apply_style", "style_axes", "panel_label", "add_panel_labels",
    "figure_size", "new_figure", "save_figure",
]

__version__ = "0.3.0"
