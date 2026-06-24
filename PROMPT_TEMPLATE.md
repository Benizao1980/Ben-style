# Reusable figure-styling prompt

```text
Restyle this scientific figure using the Pascoe scientific figure system.

Core rules:
- white background;
- warm near-black text and axes (#2F2A26), not pure black;
- clean sans-serif font (Arial, Helvetica or DejaVu Sans);
- thicker data lines and lighter structural lines;
- remove top and right spines from ordinary Cartesian plots;
- no grid unless it materially improves interpretation; then use a faint grid only on the value axis;
- left-aligned titles, frameless legends and simple bold A–D panel labels;
- no decorative boxes, title bands, cartoons or infographic styling;
- preserve balanced spacing and let the data occupy most of each panel;
- use identical scales for directly compared panels;
- export true-vector SVG and PDF plus 300–600 dpi PNG.

Choose colours from the Pascoe master library or a defined palette. For general categories, default to balanced_8. Use a sequential palette for ordered magnitude and a diverging palette only where a meaningful centre exists.

Where a semantic project preset exists, retain its mapping across all panels. Do not change biological category colours merely to improve one panel.

For a phylodynamic composite:
- put dated-tree, demographic-history and branch-expansion panels on the same calendar-year range;
- use the exact dated-tree root year as the calendar origin for related tree analyses;
- show demographic uncertainty as a ribbon and sampling years as a restrained rug;
- map branch-level posterior support continuously from neutral grey to burgundy;
- keep host or lineage colours identical across tree panels;
- shade a date interval only when its meaning is stated explicitly.

Do not invent, smooth, omit or alter data. Keep all values, labels, uncertainty intervals, statistical tests and category definitions faithful to the supplied input.
```
