# Phylogenetic figure style guide

This guide extends STYLE_GUIDE.md. **Geometry and visual styling are separate decisions.** A Wes Anderson-inspired palette cannot repair an inappropriate tree layout.

## 1. Choose the layout for the biological question

| Purpose | Default layout | Notes |
| --- | --- | --- |
| Broad diversity cloud / starburst sketch | **Unrooted equal-angle**, optionally daylight-optimised | Unequal terminal positions; irregular branching clouds. Do not force tips onto a circle. |
| Genomic relationships within one species | Rectangular phylogram | Branch lengths and scale bar when available. |
| Compact species comparison | Rectangular cladogram only if branch lengths are intentionally suppressed | Topology-only; caption must say so. |
| Dense taxonomy ring | Circular rooted tree **only if explicitly requested** | Terminals on a circumference; not interchangeable with an unrooted cloud. |
| Publication supplement | Appropriate phylogram with support values | Preserve available branch lengths/support; avoid misleading scaling. |

A drawing rendered as 'unrooted' is a **layout**; it does not change the inference or prove the tree is biologically unrooted. Note any rooting or display-root decisions in the caption.

## 2. Unrooted GETcampy GTDB diversity clouds

- Treat the user's hand-drawn starburst design as the **layout reference**: outward, irregular branches forming a diversity cloud, rather than a radial wheel.
- Reuse the complete inferred Newick tree and metadata; do not rerun inference for cosmetic reasons.
- Start with ape::plot.phylo(type="unrooted", use.edge.length=TRUE) or a demonstrably equivalent implementation; use an alternate topology-only version only if needed for comparison.
- **Do not** set every tip radius to one value, arrange tips at uniform angles around a shared rim, or place a large coloured outer ring around a nearly empty disc.
- Prefer pale neutral reference edges, clear darker MAG markers with outlines, and selected species/lineage accents. Keep interior structure visible at final publication dimensions.
- A large tree may need separate nearest-neighbour panels. Select neighbours using explicitly described tree distance or ANI criteria; they are not equivalent.
- Produce a small preview and inspect it **against the requested composition** before spending time on full-resolution exports.

## 3. Colour and taxonomy

Read colours from the canonical preset **getcampy.species** (R: getcampy_species), not hard-coded hex values.

| GTDB / project category | Ben-style master colour |
| --- | --- |
| Campylobacter infans | sage |
| Campylobacter_D jejuni; Campylobacter jejuni alias | powder_blue |
| Campylobacter coli | dusty_pink |
| Campylobacter upsaliensis | lavender |
| Campylobacter fetus | mustard |
| Campylobacter_D sp934718785 | teal |
| Other GTDB taxa | stone |
| Unassigned | warm_grey |

These are **proposed GETcampy manuscript colours**, not universal species identities. Do not silently convert GTDB's Campylobacter_D naming into an unqualified conventional species name. Add verified mappings for additional taxa instead of recycling unrelated colours.

Highlight GETcampy MAGs with a filled point and warm-dark outline, optional connector line, and clear tip/sample label. Show GTDB references with neutral branches; species emphasis should not obscure phylogenetic relationships. Test greyscale legibility.

## 4. Branch lengths, support and labels

- For phylograms, preserve inferred branch lengths and provide a substitutions-per-site scale bar where meaningful.
- For topology-only diagrams, explicitly state that branch lengths are not proportional to evolutionary distance. Never add a scale bar to a cladogram.
- If long branches cause an awkward display, first inspect input tree/root/identifiers. Any transformation (e.g. square-root, capped or logarithmic display scaling) must be disclosed and labelled as visual-only; never imply transformed distances are the underlying estimates.
- FastTree local support is **not** bootstrap percentage. Label support according to the inference software and method.
- Label selected MAGs directly; move crowded labels into callout space rather than inventing tip positions or deleting taxa.
- Report retained tip count, distinct MAG IDs, reference manifest version and taxonomy source in figure documentation.
- Never call a nearest *tree* neighbour the nearest genome by ANI without separate ANI evidence.

## 5. Layout, export and quality gates

Use STYLE_GUIDE.md's white background, Arial/Helvetica/DejaVu Sans font, warm-dark text (#2F2A26), modest panel labels and minimal unboxed legends. Scientific structure should dominate, not decorative bars or rings.

Export editable SVG, vector PDF and at least 300 dpi PNG (600 dpi for dense lines). Inspect the exported SVG/PDF for rasterisation, missing glyphs and clipping.

Before claiming a figure is ready, verify:
1. All intended tips are present exactly once; MAGs match metadata.
2. The selected layout actually matches the user's requested geometry.
3. Reference edges and focal tips remain visible at target print size.
4. Tree support, alignment/ANI values, taxon names and caption are accurate.
5. Preview renders and final exports agree; files are saved to new paths without overwriting original research results.

## 6. Worked example

Run from the repository root (requires R and ape):

~~~bash
Rscript examples/unrooted_phylogeny_example.R
~~~

This example draws a **small synthetic** unrooted tree. It demonstrates layout and preset use only; it does not represent GETcampy biology or automatically render the full 6,445-tip cloud. Review the actual tree before applying the technique to research data.
