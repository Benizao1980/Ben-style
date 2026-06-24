#!/usr/bin/env python3
"""Generate palette and semantic-preset references for the documentation."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pascoe_plot_style import MASTER, apply_style, get_palette, get_preset, master_colour, save_figure

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
apply_style("paper")

# Master library
items = list(MASTER.items())
cols = 8
rows = (len(items) + cols - 1) // cols
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.set_xlim(0, cols)
ax.set_ylim(0, rows + 1.15)
ax.axis("off")
ax.text(0, rows + 0.9, "Pascoe Plot Style", fontsize=19, fontweight="bold", ha="left")
ax.text(0, rows + 0.48, "Master colour library", fontsize=10.5, color=master_colour("warm_grey"), ha="left")
for i, (name, value) in enumerate(items):
    r, c = divmod(i, cols)
    y = rows - 1 - r
    ax.add_patch(Rectangle((c + 0.04, y + 0.36), 0.84, 0.48, facecolor=value, edgecolor="white", linewidth=0.8))
    ax.text(c + 0.46, y + 0.25, name.replace("_", " "), fontsize=7.7, ha="center", va="top")
save_figure(fig, DOCS / "master_colour_reference", formats=("svg","png"), dpi=300, close=True)

# Named and functional palettes
names = ["grand_budapest","moonrise","asteroid_city","darjeeling","royal_tenenbaums","fantastic_mr_fox","life_aquatic","french_dispatch","balanced_4","balanced_6","balanced_8","balanced_12","muted_8","accessible_8","warm","cool","green","purple","cool_warm","teal_coral"]
fig, ax = plt.subplots(figsize=(12, 11.5))
ax.set_xlim(0, 12)
ax.set_ylim(-0.2, len(names) + 1.35)
ax.axis("off")
ax.text(0, len(names) + 1.02, "Named and functional palettes", fontsize=19, fontweight="bold", ha="left")
ax.text(0, len(names) + 0.58, "Categorical, sequential and diverging colour families", fontsize=10.5, color=master_colour("warm_grey"), ha="left")
for idx, name in enumerate(names):
    y = len(names) - 1 - idx
    values = get_palette(name)
    ax.text(0, y + 0.48, name.replace("_", " "), fontsize=9.2, fontweight="bold", ha="left", va="center")
    box_w = 8.8 / len(values)
    for j, value in enumerate(values):
        ax.add_patch(Rectangle((2.7 + j * box_w, y + 0.17), box_w * 0.92, 0.62, facecolor=value, edgecolor="white", linewidth=0.8))
save_figure(fig, DOCS / "palette_reference", formats=("svg","png"), dpi=300, close=True)

# Semantic presets
preset_paths = [
    ("Source attribution", "source_attribution", ["poultry", "ruminant", "pig", "wild_bird", "environment", "other", "human"]),
    ("AMR phenotype", "amr_phenotype", None),
    ("Acinetobacter lineages", "acinetobacter.lineage", None),
    ("Acinetobacter architecture", "acinetobacter.architecture", None),
    ("C. coli lineages", "campylobacter_coli.lineage", None),
    ("C. coli clinical status", "campylobacter_coli.clinical_status", None),
]
fig, ax = plt.subplots(figsize=(12, 6.8))
ax.set_xlim(0, 12)
ax.set_ylim(-0.1, len(preset_paths) + 1.3)
ax.axis("off")
ax.text(0, len(preset_paths) + 0.95, "Scientific presets", fontsize=19, fontweight="bold", ha="left")
ax.text(0, len(preset_paths) + 0.52, "Project mappings built from the master library", fontsize=10.5, color=master_colour("warm_grey"), ha="left")
for idx, (title, path, display_keys) in enumerate(preset_paths):
    y = len(preset_paths) - 1 - idx
    values = get_preset(path)
    if display_keys is not None:
        values = {key: values[key] for key in display_keys}
    ax.text(0, y + 0.55, title, fontsize=9.5, fontweight="bold", ha="left", va="center")
    box_w = 8.8 / len(values)
    for j, (label, value) in enumerate(values.items()):
        x = 2.7 + j * box_w
        ax.add_patch(Rectangle((x, y + 0.31), box_w * 0.88, 0.55, facecolor=value, edgecolor="white", linewidth=0.8))
        ax.text(x + box_w * 0.44, y + 0.20, label.replace("_", " "), fontsize=7.1, ha="center", va="top")
save_figure(fig, DOCS / "preset_reference", formats=("svg","png"), dpi=300, close=True)
