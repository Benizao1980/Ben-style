#!/usr/bin/env python3
"""Copy this into a project and replace only the example data block."""
from pathlib import Path
import matplotlib.pyplot as plt
from pascoe_plot_style import apply_style, categorical_colours, save_figure, style_axes

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)
apply_style("paper", palette="balanced_8")

# Replace with real data. Never hand-edit plotted values to improve appearance.
x = [1,2,3,4,5]
y = [2.0,3.8,3.1,5.6,6.2]

fig, ax = plt.subplots(figsize=(7.2,4.8))
ax.plot(x, y, marker="o", color=categorical_colours(1)[0])
ax.set(title="Descriptive figure title", xlabel="Clear x-axis label", ylabel="Clear y-axis label")
style_axes(ax, grid="y")
save_figure(fig, OUT / "figure_name", dpi=600)
