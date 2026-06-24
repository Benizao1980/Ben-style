"""Illustrative Acinetobacter project preset. Values are synthetic."""
from pathlib import Path
import matplotlib.pyplot as plt
from pascoe_plot_style import apply_style, get_preset, save_figure, style_axes

OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)
apply_style("paper")

labels = ["IC1", "IC2", "IC7", "Unassigned"]
values = [32, 35, 14, 19]
palette = get_preset("acinetobacter.lineage")
fig, ax = plt.subplots(figsize=(7.2, 4.6))
bars = ax.bar(labels, values, color=[palette[x if x != "Unassigned" else "unassigned"] for x in labels], width=0.68)
ax.bar_label(bars, labels=[f"{x}%" for x in values], padding=3)
ax.set(title="Acinetobacter lineage preset", xlabel=None, ylabel="Isolates (%)", ylim=(0, 42))
style_axes(ax, grid="y")
save_figure(fig, OUT / "acinetobacter_lineage_example", close=True)
