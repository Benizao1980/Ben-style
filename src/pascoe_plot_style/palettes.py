"""Colour definitions, palette access and semantic preset helpers."""

from __future__ import annotations

from importlib.resources import files
import json
from collections.abc import Mapping

from matplotlib.colors import LinearSegmentedColormap, to_hex


def _load_json(filename: str) -> dict:
    path = files(__package__).joinpath("data", filename)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


MASTER: dict[str, str] = _load_json("master.json")
PALETTES: dict = _load_json("palettes.json")
PRESETS: dict = _load_json("presets.json")


def _normalise(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace("/", "_").replace(" ", "_")


def _match_key(mapping: Mapping[str, object], key: str) -> str:
    if key in mapping:
        return key
    target = _normalise(key)
    for candidate in mapping:
        if _normalise(candidate) == target:
            return candidate
    raise KeyError(f"Unknown key '{key}'. Available: {sorted(mapping)}")


def master_colour(name: str) -> str:
    """Return a named colour from the master colour library."""
    key = _match_key(MASTER, name)
    return MASTER[key]


def colour(name: str) -> str:
    """Alias for :func:`master_colour`."""
    return master_colour(name)


def _resolve_names(names: list[str]) -> list[str]:
    return [master_colour(name) if not name.startswith("#") else to_hex(name) for name in names]


def list_palettes(kind: str | None = None) -> list[str]:
    """List available palette names, optionally within one palette group."""
    groups = ("film", "qualitative", "sequential", "diverging")
    if kind is not None:
        group = _match_key({g: None for g in groups}, kind)
        return sorted(PALETTES[group])
    return sorted(name for group in groups for name in PALETTES[group])


def _find_palette(name: str) -> tuple[str, list[str]]:
    for group in ("film", "qualitative", "sequential", "diverging"):
        try:
            key = _match_key(PALETTES[group], name)
        except KeyError:
            continue
        return group, list(PALETTES[group][key])
    raise KeyError(f"Unknown palette '{name}'. Available: {list_palettes()}")


def get_palette(name: str = "balanced_8", n: int | None = None, *, repeat: bool = False) -> list[str]:
    """Return a named palette as hexadecimal colours.

    For categorical palettes, ``n`` selects the first ``n`` colours. Continuous
    palettes are sampled evenly when ``n`` is supplied. Repetition is disabled
    unless ``repeat=True`` because duplicated category colours are easy to
    misread in scientific figures.
    """
    group, names = _find_palette(name)
    values = _resolve_names(names)
    if n is None:
        return values
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    if group in {"sequential", "diverging"}:
        cmap = LinearSegmentedColormap.from_list(f"pascoe_{name}", values)
        if n == 1:
            return [to_hex(cmap(0.5))]
        return [to_hex(cmap(i / (n - 1))) for i in range(n)]
    if n <= len(values):
        return values[:n]
    if not repeat:
        raise ValueError(
            f"Palette '{name}' contains {len(values)} colours, but {n} were requested. "
            "Choose a larger palette or pass repeat=True explicitly."
        )
    return [values[i % len(values)] for i in range(n)]


def _traverse_preset(name: str) -> Mapping[str, str]:
    current: object = PRESETS
    for part in name.split("."):
        if not isinstance(current, Mapping):
            raise KeyError(f"Preset path '{name}' does not resolve to a category mapping")
        key = _match_key(current, part)
        current = current[key]
    if not isinstance(current, Mapping) or any(isinstance(v, Mapping) for v in current.values()):
        raise KeyError(
            f"Preset '{name}' is a group. Choose a complete path such as "
            "'acinetobacter.lineage' or 'campylobacter_coli.lineage'."
        )
    return current  # type: ignore[return-value]


def get_preset(name: str) -> dict[str, str]:
    """Return a semantic preset mapping category labels to hexadecimal colours."""
    raw = _traverse_preset(name)
    return {key: master_colour(value) if not value.startswith("#") else to_hex(value) for key, value in raw.items()}


def preset_colour(category: str, preset: str) -> str:
    """Return the colour for one category in a semantic preset."""
    values = get_preset(preset)
    key = _match_key(values, category)
    return values[key]


def categorical_colours(n: int, palette: str = "balanced_8", *, repeat: bool = False) -> list[str]:
    """Return ``n`` colours from a qualitative or named example palette."""
    group, _ = _find_palette(palette)
    if group in {"sequential", "diverging"}:
        raise TypeError(f"Palette '{palette}' is continuous; use get_palette() or make_colormap()")
    return get_palette(palette, n=n, repeat=repeat)


def source_colour(name: str) -> str:
    """Return the stable colour for a host/source category."""
    return preset_colour(name, "source_attribution")


def amr_colour(name: str) -> str:
    """Return the stable colour for an AMR phenotype category."""
    aliases = {"r": "resistant", "i": "intermediate", "s": "susceptible", "na": "unknown"}
    return preset_colour(aliases.get(_normalise(name), name), "amr_phenotype")


def make_colormap(name: str = "warm", *, cmap_name: str | None = None) -> LinearSegmentedColormap:
    """Create a Matplotlib colormap from a sequential or diverging palette."""
    group, _ = _find_palette(name)
    if group not in {"sequential", "diverging"}:
        raise TypeError(f"Palette '{name}' is categorical, not continuous")
    return LinearSegmentedColormap.from_list(cmap_name or f"pascoe_{name}", get_palette(name))
