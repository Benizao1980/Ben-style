"""Illustrative Campylobacter coli project preset. Values are synthetic."""
from pathlib import Path
import matplotlib.pyplot as plt
from pascoe_plot_style import apply_style, get_preset, save_figure, style_axes

OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)
apply_style("paper")

labels = ["ST-828 complex", "ST-1150 complex", "Other"]
values = [74, 22, 4]
palette = get_preset("campylobacter_coli.lineage")
fig, ax = plt.subplots(figsize=(7.2, 4.6))
bars = ax.bar(labels, values, color=[palette[x if x != "Other" else "other"] for x in labels], width=0.68)
ax.bar_label(bars, labels=[f"{x}%" for x in values], padding=3)
ax.set(title="Campylobacter coli lineage preset", xlabel=None, ylabel="Isolates (%)", ylim=(0, 88))
style_axes(ax, grid="y")
save_figure(fig, OUT / "campylobacter_coli_lineage_example", close=True)
