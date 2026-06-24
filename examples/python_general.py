"""General palettes and core style example."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from pascoe_plot_style import apply_style, get_palette, make_colormap, save_figure, style_axes

OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)
apply_style("paper", palette="balanced_8")

x = np.arange(1, 7)
fig, ax = plt.subplots(figsize=(7.2, 4.6))
for i, name in enumerate(("moonrise", "asteroid_city", "darjeeling")):
    y = np.array([1.0, 1.8, 1.5, 2.6, 2.9, 3.5]) + i * 0.65
    ax.plot(x, y, marker="o", color=get_palette(name, 1)[0], label=name.replace("_", " ").title())
ax.set(title="Named palette examples", xlabel="Sampling point", ylabel="Illustrative value")
ax.legend(loc="upper left")
style_axes(ax, grid="y")
save_figure(fig, OUT / "general_named_palettes", close=True)

matrix = np.outer(np.linspace(0.1, 1, 14), np.linspace(0, 1, 20))
fig, ax = plt.subplots(figsize=(7.2, 4.4))
image = ax.imshow(matrix, cmap=make_colormap("warm"), aspect="auto")
ax.set(title="Warm sequential palette", xlabel="Time", ylabel="Location")
fig.colorbar(image, ax=ax, label="Relative burden", fraction=0.035, pad=0.025)
style_axes(ax)
save_figure(fig, OUT / "general_sequential", close=True)
