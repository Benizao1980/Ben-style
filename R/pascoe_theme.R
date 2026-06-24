# Pascoe scientific ggplot2 theme, palettes and semantic presets

.pascoe_theme_file <- tryCatch(normalizePath(sys.frame(1)$ofile), error=function(e) NA_character_)
if (!exists("pascoe_master", inherits=FALSE)) {
  if (is.na(.pascoe_theme_file)) stop("Could not locate R/pascoe_data.R")
  source(file.path(dirname(.pascoe_theme_file), "pascoe_data.R"), local=FALSE)
}
rm(.pascoe_theme_file)

pascoe_palette <- function(name="balanced_8", n=NULL) {
  if (!name %in% names(pascoe_palettes)) stop(sprintf("Unknown palette: %s", name))
  values <- unname(pascoe_master[pascoe_palettes[[name]]])
  if (is.null(n)) return(values)
  if (n < 0) stop("n must be non-negative")
  if (n > length(values)) stop("Requested more colours than the palette contains")
  values[seq_len(n)]
}

pascoe_preset <- function(name) {
  if (!name %in% names(pascoe_presets)) stop(sprintf("Unknown preset: %s", name))
  refs <- pascoe_presets[[name]]
  values <- pascoe_master[unname(refs)]
  names(values) <- names(refs)
  values
}

theme_pascoe <- function(base_size=9, base_family="Arial", grid="none") {
  stopifnot(grid %in% c("none", "x", "y", "both"))
  theme <- ggplot2::theme_classic(base_size=base_size, base_family=base_family) +
    ggplot2::theme(
      plot.background=ggplot2::element_rect(fill="white", colour=NA),
      panel.background=ggplot2::element_rect(fill="white", colour=NA),
      text=ggplot2::element_text(colour=pascoe_master[["ink"]]),
      axis.text=ggplot2::element_text(colour=pascoe_master[["ink"]]),
      axis.title=ggplot2::element_text(colour=pascoe_master[["ink"]]),
      axis.line=ggplot2::element_line(colour=pascoe_master[["ink"]], linewidth=0.45),
      axis.ticks=ggplot2::element_line(colour=pascoe_master[["ink"]], linewidth=0.4),
      plot.title=ggplot2::element_text(face="bold", hjust=0, size=base_size*1.17),
      plot.subtitle=ggplot2::element_text(hjust=0, colour=pascoe_master[["warm_grey"]]),
      plot.tag=ggplot2::element_text(face="bold", size=base_size*1.17),
      plot.tag.position=c(0,1),
      legend.background=ggplot2::element_blank(), legend.key=ggplot2::element_blank(),
      legend.title=ggplot2::element_text(face="bold"),
      panel.grid=ggplot2::element_blank(), plot.margin=ggplot2::margin(7,8,7,8)
    )
  if (grid %in% c("x","both")) theme <- theme + ggplot2::theme(panel.grid.major.x=ggplot2::element_line(colour=pascoe_master[["light_grey"]], linewidth=0.35))
  if (grid %in% c("y","both")) theme <- theme + ggplot2::theme(panel.grid.major.y=ggplot2::element_line(colour=pascoe_master[["light_grey"]], linewidth=0.35))
  theme
}

scale_colour_pascoe <- function(palette="balanced_8", ...) ggplot2::scale_colour_manual(values=pascoe_palette(palette), ...)
scale_fill_pascoe <- function(palette="balanced_8", ...) ggplot2::scale_fill_manual(values=pascoe_palette(palette), ...)
scale_colour_pascoe_preset <- function(preset, ...) ggplot2::scale_colour_manual(values=pascoe_preset(preset), ...)
scale_fill_pascoe_preset <- function(preset, ...) ggplot2::scale_fill_manual(values=pascoe_preset(preset), ...)
scale_fill_pascoe_continuous <- function(palette="warm", ...) ggplot2::scale_fill_gradientn(colours=pascoe_palette(palette), ...)
scale_colour_pascoe_continuous <- function(palette="warm", ...) ggplot2::scale_colour_gradientn(colours=pascoe_palette(palette), ...)

save_pascoe_plot <- function(plot, path, width=7.2, height=4.8, dpi=300, bg="white") {
  dir.create(dirname(path), recursive=TRUE, showWarnings=FALSE)
  stem <- sub("\\.[^.]+$", "", path)
  ggplot2::ggsave(paste0(stem,".svg"), plot=plot, width=width, height=height, units="in", bg=bg)
  ggplot2::ggsave(paste0(stem,".pdf"), plot=plot, width=width, height=height, units="in", bg=bg)
  ggplot2::ggsave(paste0(stem,".png"), plot=plot, width=width, height=height, units="in", dpi=dpi, bg=bg)
  invisible(c(paste0(stem,".svg"), paste0(stem,".pdf"), paste0(stem,".png")))
}
