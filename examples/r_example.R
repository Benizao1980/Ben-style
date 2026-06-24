source("R/pascoe_theme.R")
library(ggplot2)

df <- data.frame(
  lineage=factor(c("ST-828 complex", "ST-1150 complex", "other"), levels=c("ST-828 complex", "ST-1150 complex", "other")),
  percent=c(78,22,4)
)

p <- ggplot(df, aes(lineage, percent, fill=lineage)) +
  geom_col(width=0.68) +
  geom_text(aes(label=paste0(percent,"%")), vjust=-0.45, colour=pascoe_master[["ink"]]) +
  scale_fill_pascoe_preset("campylobacter_coli_lineage", guide="none") +
  scale_y_continuous(expand=expansion(mult=c(0,0.1))) +
  labs(title="Campylobacter coli lineage preset", x=NULL, y="Isolates (%)") +
  theme_pascoe(grid="y")

save_pascoe_plot(p, "outputs/r_campylobacter_coli_example")
