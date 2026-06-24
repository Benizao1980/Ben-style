from pathlib import Path
import json
import matplotlib
import matplotlib.pyplot as plt
import pytest

from pascoe_plot_style import (
    MASTER, PALETTES, PRESETS, apply_style, categorical_colours, get_palette,
    get_preset, make_colormap, master_colour, preset_colour, save_figure,
)


def _all_palette_refs():
    for group in ("film", "qualitative", "sequential", "diverging"):
        for values in PALETTES[group].values():
            yield from values
    yield from PALETTES["ui"].values()


def _walk_preset_refs(node):
    for value in node.values():
        if isinstance(value, dict):
            yield from _walk_preset_refs(value)
        else:
            yield value


def test_all_references_resolve():
    assert all(ref in MASTER or str(ref).startswith("#") for ref in _all_palette_refs())
    assert all(ref in MASTER or str(ref).startswith("#") for ref in _walk_preset_refs(PRESETS))


def test_master_and_palette_access():
    assert master_colour("dusty pink") == "#D899A5"
    assert len(get_palette("moonrise")) == 8
    assert len(get_palette("warm", n=11)) == 11
    assert categorical_colours(6, "balanced_6") == get_palette("balanced_6")
    with pytest.raises(ValueError):
        categorical_colours(9, "balanced_8")


def test_semantic_presets():
    source = get_preset("source_attribution")
    assert source["poultry"] == MASTER["sunflower"]
    assert preset_colour("ST-1150 complex", "campylobacter_coli.lineage") == MASTER["teal"]
    assert preset_colour("IC2", "acinetobacter.lineage") == MASTER["navy"]


def test_style_and_colormap():
    apply_style("paper", "balanced_8")
    assert matplotlib.rcParams["axes.spines.top"] is False
    assert matplotlib.rcParams["text.color"].lower() == MASTER["ink"].lower()
    assert make_colormap("cool_warm").N > 0


def test_export(tmp_path: Path):
    apply_style("paper")
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    files = save_figure(fig, tmp_path / "test", formats=("svg", "png"), close=True)
    assert all(path.exists() for path in files)


def test_packaged_mplstyle_loads():
    from importlib.resources import files
    style_file = files("pascoe_plot_style.mplstyles").joinpath("pascoe.mplstyle")
    plt.style.use(style_file)
    assert matplotlib.rcParams["text.color"].lower() == MASTER["ink"].lower()


def test_canonical_and_packaged_json_are_synced():
    root = Path(__file__).resolve().parents[1]
    for name in ("master.json", "palettes.json", "presets.json"):
        canonical = json.loads((root / "data" / name).read_text())
        packaged = json.loads((root / "src" / "pascoe_plot_style" / "data" / name).read_text())
        assert canonical == packaged
