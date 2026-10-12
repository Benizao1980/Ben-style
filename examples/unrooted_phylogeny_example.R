#!/usr/bin/env Rscript
# Small, SYNTHETIC example of an unrooted (not circular) tree using Ben-style.
# Run from repository root: Rscript examples/unrooted_phylogeny_example.R
# Requires ape; no GETcampy datasets or HPC access.

if (!file.exists("R/pascoe_data.R")) {
  stop("Run from the Ben-style repository root.")
}
if (!requireNamespace("ape", quietly=TRUE)) {
  stop("Install R package 'ape' to run this example.")
}
source("R/pascoe_data.R")

# Synthetic taxa and lengths for layout demonstration ONLY.
tree <- ape::read.tree(text=paste0(
  "((GC135_Cinfans:0.10,GTDB_Cinfans_A:0.09,GTDB_Cinfans_B:0.12):0.17,",
  "(GC413_Cjejuni:0.07,GTDB_Cjejuni_A:0.11,GTDB_Cjejuni_B:0.08):0.14,",
  "((GTDB_Ccoli_A:0.10,GTDB_Ccoli_B:0.13):0.11,",
  "(GTDB_Cupsali_A:0.16,GTDB_Cupsali_B:0.12):0.10):0.13,",
  "(GC269_unnamed:0.16,GTDB_unnamed_A:0.18):0.21);"
))

mag_species <- c(
  GC135_Cinfans="Campylobacter infans",
  GC413_Cjejuni="Campylobacter_D jejuni",
  GC269_unnamed="Campylobacter_D sp934718785"
)
colours <- pascoe_presets[["getcampy_species"]]
stopifnot(all(unname(mag_species) %in% names(colours)))
mag_tips <- match(names(mag_species), tree$tip.label)
stopifnot(!anyNA(mag_tips))
mag_colours <- unname(pascoe_master[unname(colours[mag_species])])
ink <- unname(pascoe_master[["ink"]])
grey <- unname(pascoe_master[["light_grey"]])

draw <- function() {
  op <- par(bg="white", fg=ink, mar=c(1,1,3,1), family="sans")
  on.exit(par(op), add=TRUE)
  ape::plot.phylo(
    tree, type="unrooted", use.edge.length=TRUE,
    show.tip.label=TRUE, cex=0.72,
    edge.color=grey, edge.width=0.9, tip.color=ink,
    no.margin=FALSE
  )
  ape::tiplabels(tip=mag_tips, pch=21, bg=mag_colours, col=ink, cex=1.5)
  title(main="Unrooted GETcampy style preview (synthetic)", col.main=ink, cex.main=0.95)
}

dir.create("outputs", showWarnings=FALSE, recursive=TRUE)
stem <- "outputs/unrooted_phylogeny_example"

grDevices::svg(paste0(stem, ".svg"), width=8, height=7.5, bg="white")
draw()
grDevices::dev.off()

grDevices::pdf(paste0(stem, ".pdf"), width=8, height=7.5,
               bg="white", useDingbats=FALSE)
draw()
grDevices::dev.off()

grDevices::png(paste0(stem, ".png"), width=8, height=7.5,
               units="in", res=350, bg="white")
draw()
grDevices::dev.off()

message("Wrote unrooted example SVG, PDF and PNG to outputs/")
