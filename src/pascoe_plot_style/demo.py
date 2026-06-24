"""Command-line demonstration figures."""

from pathlib import Path
import matplotlib.pyplot as plt

from . import apply_style, get_palette, get_preset, make_colormap, save_figure, style_axes


def main() -> None:
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    apply_style("paper")

    labels = ["Poultry", "Ruminant", "Pig", "Wild bird"]
    values = [68, 28, 1, 3]
    source = get_preset("source_attribution")
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    bars = ax.bar(labels, values, color=[source[x.lower().replace(" ", "_")] for x in labels], width=0.68)
    ax.bar_label(bars, fmt="%.0f%%", padding=3)
    ax.set_ylim(0, 76)
    ax.set_ylabel("Attributed infections (%)")
    ax.set_title("Source attribution")
    style_axes(ax, grid="y")
    save_figure(fig, out / "demo_source_attribution", close=True)

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    for i, palette_name in enumerate(("moonrise", "asteroid_city", "darjeeling")):
        values = [1 + i, 2.4 + i, 2.0 + i, 3.2 + i, 3.7 + i]
        ax.plot(range(5), values, marker="o", color=get_palette(palette_name, 1)[0], label=palette_name.replace("_", " ").title())
    ax.set(title="Named palette examples", xlabel="Time", ylabel="Illustrative value")
    ax.legend()
    style_axes(ax, grid="y")
    save_figure(fig, out / "demo_named_palettes", close=True)

    matrix = [[(i + 1) * (j + 1) for j in range(18)] for i in range(10)]
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    image = ax.imshow(matrix, cmap=make_colormap("warm"), aspect="auto")
    ax.set(title="Sequential palette", xlabel="Time", ylabel="Location")
    fig.colorbar(image, ax=ax, label="Relative burden", fraction=0.035, pad=0.025)
    style_axes(ax)
    save_figure(fig, out / "demo_sequential", close=True)
    print(f"Wrote demonstration figures to {out.resolve()}")


if __name__ == "__main__":
    main()
