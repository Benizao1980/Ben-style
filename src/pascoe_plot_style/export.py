"""Consistent vector-first figure export."""

from __future__ import annotations

from pathlib import Path
from collections.abc import Iterable
from matplotlib.figure import Figure


def save_figure(
    fig: Figure,
    path: str | Path,
    *,
    formats: Iterable[str] = ("svg", "pdf", "png"),
    dpi: int = 300,
    transparent: bool = False,
    close: bool = False,
) -> list[Path]:
    """Save one figure in several formats using a shared basename."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    stem = target.with_suffix("")
    written: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        outfile = stem.with_suffix(f".{fmt}")
        kwargs = {
            "bbox_inches": "tight", "pad_inches": 0.06,
            "transparent": transparent,
            "facecolor": "none" if transparent else "white",
        }
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = dpi
        fig.savefig(outfile, **kwargs)
        written.append(outfile)
    if close:
        import matplotlib.pyplot as plt
        plt.close(fig)
    return written
