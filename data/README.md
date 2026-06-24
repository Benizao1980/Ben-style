# Palette data

These JSON files are the canonical colour definitions for the repository.

- `master.json` defines the named colour vocabulary.
- `palettes.json` defines named, qualitative, sequential and diverging palettes by referring to master colour names.
- `presets.json` defines scientific category mappings by referring to master colour names.

After editing any of these files, run:

```bash
python scripts/sync_palette_data.py
```

This copies the JSON files into the installable Python package and regenerates `R/pascoe_data.R`. Do not edit the generated R data file directly.
