# Worked example: styling BactDating, skygrowth and CaveDive outputs.
#
# The script runs with synthetic objects by default. To use real analyses,
# replace the three demo objects with readRDS() calls as shown below.

source("R/pascoe_theme.R")
source("R/pascoe_phylodynamics.R")

required <- c("ape", "ggplot2", "ggtree", "patchwork")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly=TRUE)]
if (length(missing)) stop("Install: ", paste(missing, collapse=", "))

USE_DEMO_DATA <- TRUE

if (!USE_DEMO_DATA) {
  # Expected native objects:
  bactdating_fit <- readRDS("results/bactdating_fit.rds")
  skygrowth_fit  <- readRDS("results/skygrowth_fit.rds")
  cavedive_fit   <- readRDS("results/cavedive_fit.rds")
  tip_metadata   <- read.csv("results/tip_metadata.csv", stringsAsFactors=FALSE)
} else {
  set.seed(1150)
  tree <- ape::rcoal(72)
  tree$tip.label <- sprintf("isolate_%03d", seq_len(ape::Ntip(tree)))
  depth <- max(ape::node.depth.edgelength(tree)[seq_len(ape::Ntip(tree))])
  tree$edge.length <- tree$edge.length / depth * 112
  tree$root.time <- 1906

  bactdating_fit <- structure(
    list(tree=tree, rootdate=1906, CI=matrix(NA_real_, ape::Ntip(tree)+ape::Nnode(tree), 2)),
    class="resBactDating"
  )

  time <- seq(0, 112, length.out=130)
  year <- 2018 - time
  log_ne <- 2.0 + 0.018*(year-1906) + 2.4/(1+exp(-(year-1988)/4.5))
  median_ne <- exp(log_ne)
  skygrowth_fit <- structure(
    list(
      time=time,
      ne_ci=cbind(median_ne/1.8, median_ne, median_ne*1.8)
    ),
    class="skygrowth.mcmc"
  )

  n_tips <- ape::Ntip(tree)
  n_nodes <- n_tips + ape::Nnode(tree)
  incoming <- vector("list", n_nodes)
  for (i in seq_len(nrow(tree$edge))) incoming[[tree$edge[i,2]]] <- i
  node_depth <- ape::node.depth.edgelength(tree)
  nodes_df <- data.frame(
    is_tip=seq_len(n_nodes) <= n_tips,
    times=node_depth-max(node_depth[seq_len(n_tips)])
  )
  pre <- structure(
    list(phy=tree, n_tips=n_tips, incoming=incoming, nodes.df=nodes_df),
    class="preprocessedPhy"
  )

  internal_edges <- which(tree$edge[,2] > n_tips)
  target_edges <- sample(internal_edges, 3)
  iterations <- 4000
  event_rows <- lapply(seq_len(iterations), function(it) {
    picked <- target_edges[runif(length(target_edges)) < c(0.62, 0.33, 0.14)]
    if (!length(picked)) return(NULL)
    data.frame(
      it=it,
      t_mid=runif(length(picked), 4, 12),
      K=runif(length(picked), 400, 1800),
      time=runif(length(picked), -45, -18),
      br=picked,
      pr=runif(length(picked), 0.25, 0.9)
    )
  })
  expansion_data <- do.call(rbind, event_rows)
  model_data <- data.frame(
    it=seq_len(iterations),
    dim=sample(0:3, iterations, replace=TRUE),
    N=rgamma(iterations, 8, 0.02),
    pr=runif(iterations), lh=rnorm(iterations), prior=rnorm(iterations)
  )
  cavedive_fit <- structure(
    list(
      phylo_preprocessed=pre,
      model_data=model_data,
      expansion_data=expansion_data,
      metadata=list(effective_it=iterations)
    ),
    class="expansionsMCMC"
  )

  tip_metadata <- data.frame(
    label=tree$tip.label,
    host=sample(c("human", "poultry", "pig", "cattle"), n_tips, replace=TRUE,
                prob=c(0.52,0.30,0.10,0.08)),
    year=sample(1996:2018, n_tips, replace=TRUE)
  )
}

max_year <- max(tip_metadata$year, na.rm=TRUE)
root_year <- bactdating_fit$tree$root.time
year_limits <- c(floor(root_year), ceiling(max_year))
focus_period <- c(1980, 2000)  # Replace with a justified interval, or set NULL

p_tree <- plot_bactdating_pascoe(
  bactdating_fit,
  tip_data=tip_metadata,
  tip_colour="host",
  tip_preset="campylobacter_coli_host",
  show_hpd=FALSE,
  highlight_period=focus_period,
  year_limits=year_limits,
  title="Dated phylogeny"
)

p_ne <- plot_skygrowth_pascoe(
  skygrowth_fit,
  max_sample_year=max_year,
  sampling_years=tip_metadata$year,
  highlight_period=focus_period,
  year_limits=year_limits,
  title="Effective population size"
)

p_expansion <- plot_cavedive_pascoe(
  cavedive_fit,
  max_sample_year=max_year,
  calendar_root_year=root_year,
  tip_data=tip_metadata,
  tip_fill="host",
  tip_preset="campylobacter_coli_host",
  highlight_period=focus_period,
  year_limits=year_limits,
  title="CaveDive branch support"
)
# The host legend is already supplied by panel A; retain only the CaveDive support guide here.
p_expansion <- p_expansion + ggplot2::guides(fill="none")

figure <- assemble_phylodynamics_pascoe(
  p_tree, p_ne, p_expansion,
  layout="vertical",
  heights=c(1.30, 0.82, 1.30)
)

save_pascoe_plot(
  figure,
  "outputs/phylodynamics_worked_example",
  width=7.2,
  height=10.2
)
