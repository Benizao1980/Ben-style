# Changelog

## Unreleased — Codex and phylogeny style

- Added AGENTS.md and TREE_STYLE_GUIDE.md to distinguish unrooted starburst trees from circular cladograms and add figure QC gates.
- Added a GETcampy species colour preset using existing master colours, synchronised for Python and R.
- Added a synthetic R/ape unrooted tree example and Python regression tests.
- Linked phylogenetic plotting conventions from the README, style guide and prompt template.


## 0.3.0 — 2026-06-24

- Added R adapters for native BactDating, skygrowth and CaveDive result objects.
- Added calendar-year tree axes, optional BactDating node-date intervals and metadata-aware tip styling.
- Added a skygrowth trajectory helper with uncertainty ribbon, log scale and sampling-date rug.
- Added CaveDive branch-level posterior support summarisation and continuous branch styling.
- Added a coordinated three-panel phylodynamics assembler and vector-first export example.
- Added a generic phylodynamics semantic preset and `expansion_support` continuous palette.
- Added a synthetic, runnable worked example and generated visual preview.

## 0.2.0 — 2026-06-24

- Reframed the package as an organism-agnostic scientific styling system.
- Added a 32-colour master library.
- Added eight named example palettes and neutral functional palettes.
- Added sequential and diverging palettes.
- Reworked scientific colours as semantic presets referencing the master library.
- Added *Acinetobacter* and *Campylobacter coli* worked presets and examples.
- Renamed public Python, R and Matplotlib interfaces to remove style-specific wording.
- Added canonical JSON files plus a package-data synchronisation script.
- Expanded validation tests and generated visual references.

## 0.1.0 — 2026-06-24

- Initial GitHub-ready release.
