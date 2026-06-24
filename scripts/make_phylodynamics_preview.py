#!/usr/bin/env python3
"""Generate the documentation preview for the R phylodynamics worked example."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pascoe_plot_style import (  # noqa: E402
    apply_style,
    get_preset,
    make_colormap,
    master_colour,
    panel_label,
    save_figure,
    style_axes,
)


@dataclass
class Node:
    node_id: int
    year: float
    children: tuple[int, int] | None
    y: float = 0.0
    support: float = 0.0


def simulate_tree(n_tips: int = 42, seed: int = 1150) -> tuple[dict[int, Node], int, list[int]]:
    rng = np.random.default_rng(seed)
    sample_years = np.sort(rng.integers(1994, 2019, size=n_tips))
    nodes: dict[int, Node] = {
        i: Node(i, float(sample_years[i]), None, y=float(i)) for i in range(n_tips)
    }
    active = list(range(n_tips))
    next_id = n_tips
    current_year = float(sample_years.min() - 1)

    while len(active) > 1:
        a, b = rng.choice(active, size=2, replace=False)
        active.remove(int(a))
        active.remove(int(b))
        child_min = min(nodes[int(a)].year, nodes[int(b)].year)
        current_year = min(current_year - rng.uniform(0.7, 3.8), child_min - rng.uniform(0.4, 2.2))
        y = (nodes[int(a)].y + nodes[int(b)].y) / 2
        nodes[next_id] = Node(next_id, current_year, (int(a), int(b)), y=y)
        active.append(next_id)
        next_id += 1

    root = active[0]
    shift = 1906.0 - nodes[root].year
    for node in nodes.values():
        node.year += shift

    internal = [i for i, node in nodes.items() if node.children is not None]
    candidate = sorted(internal, key=lambda i: abs(nodes[i].year - 1989))[:6]
    rng.shuffle(candidate)
    for rank, node_id in enumerate(candidate[:4]):
        nodes[node_id].support = [0.82, 0.61, 0.37, 0.18][rank]

    # Give descendants of supported nodes a soft trace of the same event.
    def propagate(node_id: int, value: float) -> None:
        node = nodes[node_id]
        if node.children is None:
            return
        for child in node.children:
            nodes[child].support = max(nodes[child].support, value)
            propagate(child, value * 0.88)

    for node_id in candidate[:4]:
        propagate(node_id, nodes[node_id].support)

    return nodes, root, list(range(n_tips))


def draw_tree(ax, nodes: dict[int, Node], root: int, tip_ids: list[int], *, support: bool = False) -> None:
    cmap = make_colormap("expansion_support")
    norm = Normalize(0, 1)
    ink = master_colour("ink")
    light = master_colour("light_grey")

    def branch_colour(child_id: int) -> str:
        if not support:
            return ink
        value = nodes[child_id].support
        return cmap(norm(value)) if value > 0 else light

    def walk(node_id: int) -> None:
        node = nodes[node_id]
        if node.children is None:
            return
        c1, c2 = node.children
        children = (nodes[c1], nodes[c2])
        ax.plot(
            [node.year, node.year],
            [children[0].y, children[1].y],
            color=branch_colour(node_id),
            linewidth=1.0 if support else 0.75,
            solid_capstyle="round",
            zorder=2,
        )
        for child_id in (c1, c2):
            child = nodes[child_id]
            value = child.support
            ax.plot(
                [node.year, child.year],
                [child.y, child.y],
                color=branch_colour(child_id),
                linewidth=(0.65 + 1.7 * value) if support else 0.75,
                solid_capstyle="round",
                zorder=2,
            )
            walk(child_id)

    walk(root)

    host_palette = get_preset("campylobacter_coli.host")
    hosts = np.array(["human", "poultry", "pig", "cattle"])
    rng = np.random.default_rng(828)
    host = rng.choice(hosts, size=len(tip_ids), p=[0.48, 0.34, 0.10, 0.08])
    for tip_id, category in zip(tip_ids, host):
        tip = nodes[tip_id]
        ax.scatter(
            tip.year,
            tip.y,
            s=12,
            color=host_palette[category],
            edgecolor="white",
            linewidth=0.25,
            zorder=4,
        )

    ax.axvspan(1980, 2000, color=master_colour("sand"), alpha=0.18, zorder=0)
    ax.set_xlim(1902, 2021)
    ax.set_ylim(-1.5, len(tip_ids) + 0.5)
    ax.set_yticks([])
    ax.set_xlabel("Calendar year")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    style_axes(ax, grid=None)


def draw_skygrowth(ax) -> None:
    years = np.linspace(1906, 2018, 180)
    baseline = 150 * np.exp((years - 1906) / 55)
    expansion = 1 + 11 / (1 + np.exp(-(years - 1988) / 4.0))
    ne = baseline * expansion
    lower = ne / 1.75
    upper = ne * 1.75

    ax.axvspan(1980, 2000, color=master_colour("sand"), alpha=0.18, zorder=0)
    ax.fill_between(years, lower, upper, color=master_colour("seafoam"), alpha=0.32, linewidth=0)
    ax.plot(years, ne, color=master_colour("teal"), linewidth=2.0)

    rng = np.random.default_rng(17)
    sampling = np.concatenate([
        rng.integers(1995, 2005, 20),
        rng.integers(2006, 2019, 54),
    ])
    ymin = 58
    for year in sampling:
        ax.plot([year, year], [ymin, ymin * 1.13], color=master_colour("warm_grey"), alpha=0.32, linewidth=0.45)

    ax.set_yscale("log")
    ax.set_xlim(1902, 2021)
    ax.set_ylim(50, upper.max() * 1.15)
    ax.set_xlabel("Calendar year")
    ax.set_ylabel(r"Effective population size ($N_e$)")
    style_axes(ax, grid="y")


def main() -> None:
    apply_style("paper", palette="balanced_8")
    nodes, root, tips = simulate_tree()

    fig = plt.figure(figsize=(7.2, 9.8))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.28, 0.78, 1.28], hspace=0.35)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[2, 0])

    draw_tree(ax_a, nodes, root, tips, support=False)
    ax_a.set_title("Dated phylogeny")
    draw_skygrowth(ax_b)
    ax_b.set_title("Effective population size")
    draw_tree(ax_c, nodes, root, tips, support=True)
    ax_c.set_title("Clonal expansion support")

    for ax, label in zip((ax_a, ax_b, ax_c), "ABC"):
        panel_label(ax, label, x=-0.075, y=1.025)

    cmap = make_colormap("expansion_support")
    sm = ScalarMappable(norm=Normalize(0, 1), cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax_c, orientation="vertical", fraction=0.025, pad=0.015)
    cbar.set_label("Posterior branch support")
    cbar.outline.set_visible(False)

    fig.text(
        0.995,
        0.006,
        "Illustrative data",
        ha="right",
        va="bottom",
        fontsize=7,
        color=master_colour("warm_grey"),
    )

    out = ROOT / "docs" / "phylodynamics_worked_example"
    save_figure(fig, out, formats=("svg", "png"), dpi=300, close=True)
    print(f"wrote {out}.svg and {out}.png")


if __name__ == "__main__":
    main()
