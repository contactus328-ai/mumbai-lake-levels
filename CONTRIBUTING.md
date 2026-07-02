# Contributing

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev,dashboard]"
python -m pytest tests/
```

## Adding or correcting data

- **Lake levels / rainfall**: append rows to `data/manual_lake_readings.csv` or
  `data/manual_rainfall_readings.csv`, then run
  `python -m lakelevels.cli fetch-manual` to load them into the database. Use a
  `source` value that identifies where the reading came from (e.g. `bmc_report`,
  `imd_report`) rather than reusing `sample_data`, which is reserved for the
  placeholder rows already in the repo.
- **Reference figures** (demand/supply/usage split, lake list): edit
  `data/reference_data.json` directly and update `_meta.sources` /
  `_meta.last_updated` to cite where the new figure came from.

## Working on the scraper / API connectors

`src/lakelevels/sources/bmc_lakes.py` and `imd_rainfall.py` are best-effort and
expected to fail soft — if you change them, keep the behavior of returning an
empty list (with a logged warning) on any failure, so `lakelevels.cli fetch`
can still fall back to the manual CSVs.

## Before submitting a change

```bash
python -m pytest tests/
python -m lakelevels.cli fetch-manual
python -m lakelevels.cli report
```

If you touched `src/lakelevels/dashboard.py`, also run it manually
(`streamlit run src/lakelevels/dashboard.py`) and check the page renders with
no errors.

## Pull requests

Keep PRs focused on one change. Describe *why* the change is needed, not just
what changed — especially for data corrections, since it helps future
contributors judge whether a figure is still current.
