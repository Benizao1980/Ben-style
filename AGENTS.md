# Ben-style — Codex/agent instructions

This repository is the canonical **Pascoe scientific figure styling** package. Consult README.md, STYLE_GUIDE.md, TREE_STYLE_GUIDE.md, and PROMPT_TEMPLATE.md before generating or modifying figures.

## General workflow
- Reuse the existing palettes, semantic presets, R functions and Python helpers; do not invent ad hoc colour codes or overwrite existing mappings.
- Edit master colours or film palettes only with explicit approval. Add new biological categories to data/presets.json using names from data/master.json.
- After changing data/*.json, run python scripts/sync_palette_data.py and python -m pytest. Commit the synchronised packaged JSON and generated R/pascoe_data.R along with the canonical change.
- Use the same category-to-colour mapping across all figures in a study. Use symbol shape/outlines and labels so colour is not the only encoding.
- Preserve data values, uncertainties, labels, inferred topology and tip membership. Never silently discard tips, collapse clades or recalculate phylogenies to solve a visual-layout issue.
- Use white background, warm near-black (#2F2A26) text, restrained axes, thin structural marks, and vector-first output (SVG, PDF, high-resolution PNG).

## Phylogenies
- Choose geometry by scientific objective, not by aesthetic shorthand. **Unrooted equal-angle/starburst** is not a circular rooted cladogram; see TREE_STYLE_GUIDE.md.
- When an unrooted cloud is requested, do not force all tips onto a shared perimeter, draw a dominating annotation ring, or rescale branch lengths without disclosure.
- For dense GTDB contexts, grey reference branches, distinguish selected MAG tips with species colours and dark outlines, and make a small preview for user sign-off before final exports.
- Use GETcampy species preset getcampy.species for GETcampy figures, retaining actual GTDB nomenclature for labels.
- Confirm tip counts/IDs, metadata joins, annotations and legibility before reporting completion. If visual inspection is unavailable, say so.
- Use examples/unrooted_phylogeny_example.R for the supported ape-based starting point.

## Safety and scope
- Figure styling instructions do **not** authorise access to remote systems, samples, restricted metadata or credentials.
- Do not modify HPC results or submit jobs unless separately authorised in the project's operating instructions.
- Work in a dedicated branch for repository changes and request review before merging to main.
