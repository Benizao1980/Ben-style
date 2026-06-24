# BactDating + skygrowth + CaveDive worked example

This example applies one coherent visual system to three related but structurally different R outputs:

- **BactDating**: a dated `phylo` tree, a calendar root time and optional node-date intervals;
- **skygrowth**: a time vector and lower/median/upper effective-population-size estimates;
- **CaveDive**: posterior expansion events assigned to branches across MCMC iterations.

Run from the repository root:

```r
source("examples/phylodynamics_worked_example.R")
```

The script uses synthetic objects by default. Set `USE_DEMO_DATA <- FALSE` and replace the three `readRDS()` paths with real outputs. For future analyses, save the native fitted objects with `saveRDS()` rather than retaining only rendered plots or summary tables; this preserves node intervals, posterior trajectories and branch-level MCMC events.

## R dependencies

```r
install.packages(c("ape", "ggplot2", "patchwork"))
# ggtree and treeio are Bioconductor packages:
BiocManager::install(c("ggtree", "treeio"))
```

`BactDating`, `skygrowth` and `CaveDive` are only required to generate or inspect their native fitted objects; the plotting adapter additionally needs `BactDating`, `treeio` and `tibble` when `show_hpd=TRUE`.

## Recommended figure logic

1. Use the exact BactDating root year as the CaveDive calendar origin and the same calendar-year range across all panels.
2. Use a single shaded interval only when it has an explicit biological interpretation.
3. Keep host or lineage colours stable at the tips.
4. Use a continuous scale for CaveDive posterior branch support, rather than assigning arbitrary categorical colours.
5. Show sampling dates as a restrained rug beneath the skygrowth trajectory to reveal changes in sampling intensity.
6. Export SVG and PDF as the primary publication files; retain PNG only for previews.

## Minimal real-data pattern

```r
source("R/pascoe_theme.R")
source("R/pascoe_phylodynamics.R")

bd <- readRDS("bactdating_fit.rds")
sg <- readRDS("skygrowth_fit.rds")
cd <- readRDS("cavedive_fit.rds")
meta <- read.csv("tip_metadata.csv")

max_year <- max(meta$year, na.rm=TRUE)
root_year <- bd$tree$root.time
year_limits <- c(floor(root_year), ceiling(max_year))

pA <- plot_bactdating_pascoe(
  bd,
  tip_data=meta,
  tip_colour="host",
  tip_preset="campylobacter_coli_host",
  year_limits=year_limits
)

pB <- plot_skygrowth_pascoe(
  sg,
  max_sample_year=max_year,
  sampling_years=meta$year,
  year_limits=year_limits
)

pC <- plot_cavedive_pascoe(
  cd,
  max_sample_year=max_year,
  calendar_root_year=root_year,
  tip_data=meta,
  tip_fill="host",
  tip_preset="campylobacter_coli_host",
  year_limits=year_limits
)

pC <- pC + ggplot2::guides(fill="none")  # host legend already shown in panel A
figure <- assemble_phylodynamics_pascoe(pA, pB, pC)
save_pascoe_plot(figure, "outputs/phylodynamics", width=7.2, height=10.2)
```

BactDating 95% node intervals can be added with `show_hpd=TRUE`. For large trees, use them selectively or reserve the full interval plot for supplementary material because drawing every interval can obscure the topology.
