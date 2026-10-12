"""Regression checks for the GETcampy phylogeny style additions."""

from pathlib import Path
import json

from pascoe_plot_style import MASTER, get_preset


ROOT = Path(__file__).resolve().parents[1]


def test_getcampy_species_preset():
    colours = get_preset("getcampy.species")
    assert colours["Campylobacter infans"] == MASTER["sage"]
    assert colours["Campylobacter_D jejuni"] == MASTER["powder_blue"]
    assert colours["Campylobacter jejuni"] == colours["Campylobacter_D jejuni"]
    assert colours["Campylobacter_D sp934718785"] == MASTER["teal"]
    assert colours["Other GTDB taxa"] == MASTER["stone"]


def test_getcampy_canonical_packaged_mapping():
    canonical = json.loads((ROOT / "data/presets.json").read_text())
    packaged = json.loads((ROOT / "src/pascoe_plot_style/data/presets.json").read_text())
    assert canonical == packaged
    assert all(colour in MASTER for colour in canonical["getcampy"]["species"].values())


def test_tree_guidance_and_synthetic_example_exist():
    guide = (ROOT / "TREE_STYLE_GUIDE.md").read_text()
    example = (ROOT / "examples/unrooted_phylogeny_example.R").read_text()
    r_data = (ROOT / "R/pascoe_data.R").read_text()
    assert "Unrooted equal-angle" in guide
    assert 'type="unrooted"' in example
    assert 'use.edge.length=TRUE' in example
    assert "getcampy_species" in r_data
    assert "getcampy_species" in example
