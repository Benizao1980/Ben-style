# Styling adapters for BactDating, skygrowth and CaveDive outputs.
# Source R/pascoe_theme.R before this file.

.pascoe_require <- function(packages) {
  missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly=TRUE)]
  if (length(missing)) {
    stop(sprintf("Install the required package(s): %s", paste(missing, collapse=", ")), call.=FALSE)
  }
  invisible(TRUE)
}

pascoe_colour <- function(name) {
  if (!name %in% names(pascoe_master)) stop(sprintf("Unknown master colour: %s", name), call.=FALSE)
  unname(pascoe_master[[name]])
}

theme_pascoe_tree <- function(base_size=9, base_family="Arial") {
  theme_pascoe(base_size=base_size, base_family=base_family, grid="none") +
    ggplot2::theme(
      axis.line.y=ggplot2::element_blank(),
      axis.text.y=ggplot2::element_blank(),
      axis.title.y=ggplot2::element_blank(),
      axis.ticks.y=ggplot2::element_blank(),
      panel.grid=ggplot2::element_blank(),
      legend.key.height=grid::unit(0.35, "cm")
    )
}

.pascoe_highlight_layer <- function(period, root_year=NULL, colour="sand", alpha=0.18) {
  if (is.null(period)) return(NULL)
  if (length(period) != 2 || any(!is.finite(period))) {
    stop("highlight_period must contain two finite values", call.=FALSE)
  }
  x <- sort(as.numeric(period))
  if (!is.null(root_year)) x <- x - root_year
  ggplot2::annotate(
    "rect", xmin=x[1], xmax=x[2], ymin=-Inf, ymax=Inf,
    fill=pascoe_colour(colour), alpha=alpha
  )
}

.pascoe_prepend_layer <- function(plot, layer) {
  if (is.null(layer)) return(plot)
  plot <- plot + layer
  n <- length(plot$layers)
  if (n > 1) plot$layers <- c(plot$layers[n], plot$layers[seq_len(n-1)])
  plot
}

.pascoe_two_limits <- function(values, name="limits") {
  if (is.null(values)) return(NULL)
  values <- as.numeric(values)
  if (length(values) != 2 || any(!is.finite(values))) {
    stop(sprintf("%s must contain two finite values", name), call.=FALSE)
  }
  sort(values)
}

#' Plot a BactDating result using ggtree and the shared figure style.
#'
#' @param fit A resBactDating object returned by BactDating::bactdate().
#' @param tip_data Optional data.frame containing a label column matching tip labels.
#' @param tip_colour Optional column in tip_data used to colour tip points.
#' @param tip_preset Optional semantic preset, e.g. campylobacter_coli_host.
#' @param tip_palette General categorical palette used when tip_preset is NULL.
#' @param show_hpd Draw BactDating 95% node intervals using its treedata adapter.
#' @param highlight_period Optional calendar-year interval to shade.
#' @param year_limits Optional two-value calendar-year range shared across panels.
#' @return A ggplot/ggtree object.
plot_bactdating_pascoe <- function(
  fit,
  tip_data=NULL,
  tip_colour=NULL,
  tip_preset=NULL,
  tip_palette="balanced_8",
  show_hpd=FALSE,
  highlight_period=NULL,
  year_limits=NULL,
  branch_colour="ink",
  hpd_colour="powder_blue",
  title="Dated phylogeny",
  base_size=9
) {
  .pascoe_require(c("ggplot2", "ggtree"))
  if (is.null(fit$tree) || !inherits(fit$tree, "phylo")) {
    stop("fit must contain a dated phylo object in fit$tree", call.=FALSE)
  }
  if (is.null(fit$tree$root.time)) {
    stop("fit$tree$root.time is required for a calendar-year axis", call.=FALSE)
  }

  tree_object <- fit$tree
  if (isTRUE(show_hpd)) {
    .pascoe_require(c("BactDating", "treeio", "tibble"))
    td <- BactDating::as.treedata.resBactDating(fit)
    tree_object <- methods::new(
      "treedata",
      phylo=td[[1]],
      data=tibble::as_tibble(as.data.frame(td[[2]]))
    )
  }

  p <- ggtree::ggtree(
    tree_object,
    ladderize=TRUE,
    linewidth=0.52,
    colour=pascoe_colour(branch_colour)
  )

  shade <- .pascoe_highlight_layer(
    highlight_period,
    root_year=fit$tree$root.time,
    colour="sand"
  )
  p <- .pascoe_prepend_layer(p, shade)

  if (isTRUE(show_hpd)) {
    p <- p + ggtree::geom_range(
      range="length_0.95_HPD",
      colour=pascoe_colour(hpd_colour),
      alpha=0.55,
      linewidth=1.05
    )
  }

  if (!is.null(tip_data)) {
    if (!"label" %in% names(tip_data)) {
      stop("tip_data must include a 'label' column", call.=FALSE)
    }
    p <- ggtree::`%<+%`(p, tip_data)
    if (!is.null(tip_colour)) {
      if (!tip_colour %in% names(tip_data)) stop("tip_colour is not present in tip_data", call.=FALSE)
      p <- p + ggtree::geom_tippoint(
        ggplot2::aes(colour=.data[[tip_colour]]), size=1.45, alpha=0.95
      )
      if (!is.null(tip_preset)) {
        p <- p + scale_colour_pascoe_preset(tip_preset, drop=FALSE, na.value=pascoe_colour("stone"))
      } else {
        p <- p + scale_colour_pascoe(tip_palette, na.value=pascoe_colour("stone"))
      }
    }
  }

  root_year <- fit$tree$root.time
  x_limits <- if (is.null(year_limits)) NULL else .pascoe_two_limits(year_limits, "year_limits") - root_year
  p +
    ggplot2::scale_x_continuous(
      limits=x_limits,
      labels=function(x) round(root_year + x),
      expand=ggplot2::expansion(mult=c(0.01, 0.025))
    ) +
    ggplot2::labs(x="Calendar year", y=NULL, title=title) +
    theme_pascoe_tree(base_size=base_size)
}

#' Convert a skygrowth fit into a stable tidy data frame.
tidy_skygrowth <- function(fit, max_sample_year=NULL) {
  if (is.null(fit$time) || is.null(fit$ne_ci)) {
    stop("fit must contain time and ne_ci fields", call.=FALSE)
  }
  ci <- as.matrix(fit$ne_ci)
  if (ncol(ci) < 3) stop("fit$ne_ci must contain lower, median and upper columns", call.=FALSE)
  estimate <- if (!is.null(fit$ne)) as.numeric(fit$ne) else as.numeric(ci[,2])
  if (length(estimate) != length(fit$time)) {
    stop("Skygrowth estimate and time vectors have different lengths", call.=FALSE)
  }
  out <- data.frame(
    time_before_present=as.numeric(fit$time),
    lower=as.numeric(ci[,1]),
    estimate=estimate,
    upper=as.numeric(ci[,3])
  )
  if (!is.null(max_sample_year)) {
    out$year <- as.numeric(max_sample_year) - out$time_before_present
    out <- out[order(out$year), , drop=FALSE]
  }
  out
}

#' Plot a skygrowth effective-population-size trajectory.
#'
#' @param max_sample_year Calendar year of the most recent sample; converts time-before-present to years.
#' @param sampling_years Optional sampling years drawn as a restrained rug.
#' @param year_limits Optional two-value x-axis range, normally calendar years.
plot_skygrowth_pascoe <- function(
  fit,
  max_sample_year=NULL,
  sampling_years=NULL,
  highlight_period=NULL,
  year_limits=NULL,
  log_y=TRUE,
  estimate_colour="teal",
  interval_colour="seafoam",
  title="Effective population size",
  base_size=9
) {
  .pascoe_require("ggplot2")
  dat <- tidy_skygrowth(fit, max_sample_year=max_sample_year)
  xvar <- if (is.null(max_sample_year)) "time_before_present" else "year"

  p <- ggplot2::ggplot(dat, ggplot2::aes(x=.data[[xvar]], y=.data$estimate))
  shade <- .pascoe_highlight_layer(highlight_period, colour="sand")
  if (!is.null(shade)) p <- p + shade

  finite_ci <- dat[is.finite(dat$lower) & is.finite(dat$upper) & dat$lower > 0, , drop=FALSE]
  if (nrow(finite_ci)) {
    p <- p + ggplot2::geom_ribbon(
      data=finite_ci,
      ggplot2::aes(x=.data[[xvar]], ymin=.data$lower, ymax=.data$upper),
      inherit.aes=FALSE,
      fill=pascoe_colour(interval_colour),
      alpha=0.30
    )
  }
  p <- p + ggplot2::geom_line(
    colour=pascoe_colour(estimate_colour), linewidth=0.9, lineend="round"
  )

  if (!is.null(sampling_years)) {
    rug <- data.frame(x=as.numeric(sampling_years))
    if (is.null(max_sample_year)) rug$x <- max(rug$x, na.rm=TRUE) - rug$x
    p <- p + ggplot2::geom_rug(
      data=rug, ggplot2::aes(x=.data$x), inherit.aes=FALSE,
      sides="b", colour=pascoe_colour("warm_grey"), alpha=0.45, linewidth=0.32
    )
  }

  if (is.null(max_sample_year)) {
    p <- p + ggplot2::scale_x_reverse()
    xlab <- "Time before most recent sample"
  } else {
    xlab <- "Calendar year"
  }
  if (isTRUE(log_y)) p <- p + ggplot2::scale_y_log10()
  if (!is.null(year_limits)) {
    limits <- .pascoe_two_limits(year_limits, "year_limits")
    p <- p + ggplot2::coord_cartesian(xlim=limits)
  }

  p +
    ggplot2::labs(x=xlab, y=expression(N[e]), title=title) +
    theme_pascoe(base_size=base_size, grid="y") +
    ggplot2::theme(panel.grid.minor=ggplot2::element_blank())
}

#' Summarise CaveDive posterior expansion support for each incoming branch.
tidy_cavedive_branches <- function(fit) {
  if (is.null(fit$phylo_preprocessed) || is.null(fit$model_data) || is.null(fit$expansion_data)) {
    stop("fit must be an expansionsMCMC-like object", call.=FALSE)
  }
  pre <- fit$phylo_preprocessed
  n_nodes <- pre$n_tips + pre$phy$Nnode
  node <- seq_len(n_nodes)
  edge_id <- vapply(node, function(i) {
    value <- pre$incoming[[i]]
    if (is.null(value) || !length(value) || is.na(value[1])) NA_integer_ else as.integer(value[1])
  }, integer(1))

  sampled_iterations <- unique(as.numeric(fit$model_data$it))
  sampled_iterations <- sampled_iterations[is.finite(sampled_iterations)]
  iterations <- length(sampled_iterations)
  if (!is.finite(iterations) || iterations <= 0) {
    stop("Could not determine the number of sampled CaveDive iterations", call.=FALSE)
  }

  support <- rep(0, n_nodes)
  events <- fit$expansion_data
  if (nrow(events) > 0) {
    events <- events[is.finite(events$it) & is.finite(events$br), c("it", "br"), drop=FALSE]
    events <- events[events$it %in% sampled_iterations, , drop=FALSE]
    # Count a branch at most once in each MCMC iteration.
    events <- unique(events)
    counts <- table(events$br)
    hit <- match(as.character(edge_id), names(counts))
    support[!is.na(hit)] <- as.numeric(counts[hit[!is.na(hit)]]) / iterations
  }
  data.frame(node=node, edge_id=edge_id, expansion_support=pmin(support, 1))
}

#' Plot CaveDive branch-level posterior expansion support.
#'
#' @param calendar_root_year Preferred exact calendar root year, usually from BactDating.
#' @param max_sample_year Used to infer the root year only when calendar_root_year is absent.
#' @param year_limits Optional two-value calendar-year range shared across panels.
plot_cavedive_pascoe <- function(
  fit,
  max_sample_year=NULL,
  calendar_root_year=NULL,
  tip_data=NULL,
  tip_fill=NULL,
  tip_preset=NULL,
  tip_palette="balanced_8",
  highlight_period=NULL,
  year_limits=NULL,
  support_palette="expansion_support",
  title="Clonal expansion support",
  base_size=9
) {
  .pascoe_require(c("ggplot2", "ggtree", "ape"))
  pre <- fit$phylo_preprocessed
  if (is.null(pre$phy) || !inherits(pre$phy, "phylo")) {
    stop("fit$phylo_preprocessed$phy must be a phylo object", call.=FALSE)
  }
  support <- tidy_cavedive_branches(fit)

  p <- ggtree::ggtree(
    pre$phy,
    ladderize=TRUE,
    linewidth=0.50,
    colour=pascoe_colour("light_grey")
  )
  p <- ggtree::`%<+%`(p, support)
  p <- p + ggtree::geom_tree(
    ggplot2::aes(colour=.data$expansion_support), linewidth=0.72, lineend="round"
  )

  depth <- max(ape::node.depth.edgelength(pre$phy)[seq_len(pre$n_tips)], na.rm=TRUE)
  root_year <- if (!is.null(calendar_root_year)) {
    as.numeric(calendar_root_year)
  } else if (!is.null(max_sample_year)) {
    as.numeric(max_sample_year) - depth
  } else {
    NULL
  }
  shade <- .pascoe_highlight_layer(highlight_period, root_year=root_year, colour="sand")
  p <- .pascoe_prepend_layer(p, shade)

  if (!is.null(tip_data)) {
    if (!"label" %in% names(tip_data)) stop("tip_data must include a 'label' column", call.=FALSE)
    p <- ggtree::`%<+%`(p, tip_data)
    if (!is.null(tip_fill)) {
      if (!tip_fill %in% names(tip_data)) stop("tip_fill is not present in tip_data", call.=FALSE)
      p <- p + ggtree::geom_tippoint(
        ggplot2::aes(fill=.data[[tip_fill]]), shape=21, size=1.45,
        colour=pascoe_colour("ink"), stroke=0.18
      )
      if (!is.null(tip_preset)) {
        p <- p + scale_fill_pascoe_preset(tip_preset, drop=FALSE, na.value=pascoe_colour("stone"))
      } else {
        p <- p + scale_fill_pascoe(tip_palette, na.value=pascoe_colour("stone"))
      }
    }
  }

  p <- p + scale_colour_pascoe_continuous(
    support_palette,
    limits=c(0,1),
    name="Expansion\nsupport",
    na.value=pascoe_colour("light_grey")
  )

  if (is.null(root_year)) {
    x_limits <- if (is.null(year_limits)) NULL else .pascoe_two_limits(year_limits, "year_limits")
    xscale <- ggplot2::scale_x_continuous(
      limits=x_limits,
      expand=ggplot2::expansion(mult=c(0.01,0.025))
    )
    xlab <- "Time since root"
  } else {
    x_limits <- if (is.null(year_limits)) NULL else .pascoe_two_limits(year_limits, "year_limits") - root_year
    xscale <- ggplot2::scale_x_continuous(
      limits=x_limits,
      labels=function(x) round(root_year + x),
      expand=ggplot2::expansion(mult=c(0.01,0.025))
    )
    xlab <- "Calendar year"
  }

  p + xscale +
    ggplot2::labs(x=xlab, y=NULL, title=title) +
    theme_pascoe_tree(base_size=base_size)
}

#' Assemble aligned BactDating, skygrowth and CaveDive panels.
assemble_phylodynamics_pascoe <- function(
  dated_tree,
  skygrowth,
  cavedive,
  layout=c("vertical", "tree_ne_over_cavedive"),
  tags="A",
  heights=c(1.25, 0.82, 1.25),
  legend_position="bottom"
) {
  .pascoe_require(c("patchwork", "ggplot2"))
  layout <- match.arg(layout)
  if (layout == "vertical") {
    out <- patchwork::wrap_plots(
      list(dated_tree, skygrowth, cavedive), ncol=1, heights=heights, guides="collect"
    )
  } else {
    top <- patchwork::wrap_plots(list(dated_tree, skygrowth), ncol=2, widths=c(1.35,1))
    out <- patchwork::wrap_plots(list(top, cavedive), ncol=1, heights=c(1,1.05), guides="collect")
  }
  out <- out + patchwork::plot_annotation(tag_levels=tags)
  if (!is.null(legend_position)) {
    out <- out & ggplot2::theme(legend.position=legend_position)
  }
  out
}
