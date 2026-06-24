# Pascoe figure style guide

## 1. Purpose

The style should make complex scientific figures feel ordered, warm and coherent without competing with the data. The visual identity comes from consistent typography, spacing, line weights and restraint—not from forcing every figure into the same colours.

## 2. Core visual rules

1. Use a white background.
2. Use warm near-black (`ink`, `#2F2A26`) for text and axes rather than pure black.
3. Remove top and right spines from ordinary Cartesian plots.
4. Use moderately thick data lines and lighter structural lines.
5. Use no grid by default; where useful, add only a faint grid on the value axis.
6. Left-align plot titles.
7. Use a clean sans-serif typeface that survives journal production: Arial, Helvetica or DejaVu Sans.
8. Keep legends frameless and close to the data.
9. Use bold uppercase panel labels at the upper-left of each panel.
10. Avoid decorative title bands, shaded boxes, ornamental gradients and infographic clutter.

## 3. Colour architecture

### Master library

`data/master.json` is the single vocabulary of named colours. New palettes and scientific presets should reference these names rather than repeating hex codes.

### Named example palettes

The named palettes are reusable categorical colour families:

- `grand_budapest`
- `moonrise`
- `asteroid_city`
- `darjeeling`
- `royal_tenenbaums`
- `fantastic_mr_fox`
- `life_aquatic`
- `french_dispatch`

They are options, not semantic mappings. Choosing one does not imply biological meaning.

### Functional palettes

Use `balanced_4`, `balanced_6`, `balanced_8` or `balanced_12` for general categorical plots. Use `muted_8` when colour should recede and `accessible_8` when distinguishability is the priority. The latter is an accessibility-oriented starting point, not a substitute for checking the final figure and adding redundant labels or shapes.

Use sequential palettes for ordered magnitude and diverging palettes only where a meaningful centre exists.

## 4. Semantic project presets

A preset assigns stable colours to scientific categories. Keep these mappings stable across a manuscript or project.

Examples include:

- source attribution;
- AMR phenotype;
- *Acinetobacter* lineages, carbapenems and resistance architectures;
- *Campylobacter coli* lineages, clinical status and host source.

Project presets should be treated as editable examples. A new project can add its own mapping in `data/presets.json` without modifying the general palettes.

## 5. Choosing categorical colours

- Aim for no more than 6–8 simultaneous categories in a standard panel.
- Group minor categories into `Other` only where scientifically defensible.
- Use the same colour for the same biological category throughout a manuscript.
- Do not recycle one colour for two different categories in adjacent panels.
- Do not depend on colour alone: use labels, ordering, shapes or line styles where needed.
- The helper will not silently repeat categorical colours unless explicitly asked.

## 6. Continuous data

- Use `warm`, `cool`, `green`, `purple` or `neutral` for ordered values.
- Use `cool_warm`, `teal_coral` or `purple_green` for centred effects or differences.
- State the centre and transformation in the caption where it affects interpretation.
- Avoid rainbow colour maps.

## 7. Statistical graphics

- Show raw observations where feasible.
- Put summaries behind rather than over the data.
- Show uncertainty intervals, not only point estimates.
- Use common axis limits for direct panel comparisons.
- For predicted-versus-observed plots, include the identity line.
- For MIC plots, label breakpoints and relevant dilution-error regions.
- Avoid encoding the same statistic simultaneously by colour, size and annotation.

## 8. Trees and genomic figures

- Use thin warm-dark branches on white.
- Keep metadata strips close to the tips.
- Avoid oversized tip markers.
- Use the same host, lineage and AMR colours as the rest of the manuscript.
- Use neutral greys for background metadata unless colour carries biological meaning.
- Let the tree occupy most of the available plotting area.

## 9. Composition

- Maintain consistent outer margins and inter-panel spacing.
- Let the primary data object dominate each panel.
- Keep explanatory prose outside the plot area where possible.
- Use portrait layouts only when the scientific structure benefits from them.
- Do not stretch figures merely to fill a page.

## 10. Export

For manuscript figures, produce:

- SVG as the editable vector master;
- PDF as the publication/vector fallback;
- PNG at 300 dpi minimum, or 600 dpi for line-heavy figures.

Use a white, non-transparent background unless another application explicitly requires transparency. Inspect the exported SVG for clipping, font substitution and unintended rasterisation.
