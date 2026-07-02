# Mumbai Lake Levels

[![Tests](https://github.com/contactus328-ai/mumbai-lake-levels/actions/workflows/tests.yml/badge.svg)](https://github.com/contactus328-ai/mumbai-lake-levels/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/contactus328-ai/mumbai-lake-levels)](https://github.com/contactus328-ai/mumbai-lake-levels/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/contactus328-ai/mumbai-lake-levels)](https://github.com/contactus328-ai/mumbai-lake-levels/pulls)

**[Live demo](https://contactus328-aii-3bqsuqesy8agfxnu7nuvua.streamlit.app/)** — hosted on Streamlit Community Cloud.

Tracks Mumbai's water supply system: the 7 lakes that supply the city, daily/hourly rainfall, and how demand compares to supply across residential, commercial, and industrial use.

## What this covers

- **Lake levels** for the 7 reservoirs that supply Mumbai (Upper Vaitarna, Modak Sagar, Middle Vaitarna, Tansa, Bhatsa, Vihar, Tulsi)
- **Rainfall**, ideally at hourly resolution, from IMD (India Meteorological Department)
- **Water demand vs. supply** (in MLD — million litres per day) and the residential/commercial/industrial usage split, sourced from BMC (Brihanmumbai Municipal Corporation) reporting

## A note on data sources (read this first)

Mumbai doesn't have a single clean public API for this data, so the project is built around graceful fallbacks:

| Data | Live source | Reality | Fallback |
|---|---|---|---|
| Lake levels | BMC hydraulic dept. portal (`mcgm.gov.in`) | Legacy SAP portal; doesn't render outside a full browser session, so plain HTTP scraping usually returns nothing | Manual entry via `data/manual_lake_readings.csv` |
| Rainfall | IMD API (`api.imd.gov.in`) | Requires a free API key you register for yourself — this project can't do that on your behalf | Manual entry via `data/manual_rainfall_readings.csv` |
| Demand/supply/usage split | BMC public reporting | Doesn't change often; kept as static reference data | `data/reference_data.json` — edit directly when BMC publishes new figures |

The scraper and API client are both implemented and will be used automatically when they work — they just fail soft (log a warning, return no rows) so the pipeline always has the CSV fallback to lean on.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e .              # or: pip install -r requirements.txt
cp .env.example .env          # add IMD_API_KEY if you have one

# verify core deps actually installed before relying on them
python -c "import requests, bs4, dotenv; print('core deps OK')"
```

## Usage

```bash
# create the local database
python -m lakelevels.cli init-db

# try live sources, fall back to CSVs automatically
python -m lakelevels.cli fetch

# or load only what's in the manual CSVs
python -m lakelevels.cli fetch-manual

# print a text report
python -m lakelevels.cli report

# launch the visual dashboard
pip install -e ".[dashboard]"

# verify the dashboard extras actually installed before relying on them
python -c "import streamlit, pandas, altair; print('dashboard deps OK')"

streamlit run src/lakelevels/dashboard.py
```

## Deploying the dashboard

Already deployed at **https://contactus328-aii-3bqsuqesy8agfxnu7nuvua.streamlit.app/**.

GitHub Pages only serves static files, so it can't host the Streamlit app
directly (it needs a running Python process). This project uses
[Streamlit Community Cloud](https://share.streamlit.io) instead — it's free
and deploys straight from this repo. To redeploy or set up your own instance:

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=contactus328-ai/mumbai-lake-levels&branch=main&mainModule=src/lakelevels/dashboard.py)

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub.
2. Click "New app", select this repo and the `main` branch.
3. Set the main file path to `src/lakelevels/dashboard.py`.
4. (Optional) In the app's "Secrets", add `IMD_API_KEY` if you have one.
5. Deploy. `requirements.txt` installs the app itself (`-e .`) plus its
   dependencies, so no extra config is needed.

The cloud instance starts with an empty database (`lakelevels.db` is
gitignored) — `dashboard.py` seeds it from `data/manual_lake_readings.csv`
and `data/manual_rainfall_readings.csv` automatically on first load.

## Adding manual readings

Append rows to the CSVs in `data/`:

- `manual_lake_readings.csv`: `date,lake_name,level_percent,content_million_litres,source`
- `manual_rainfall_readings.csv`: `timestamp,station,rainfall_mm,period,source`

Then run `python -m lakelevels.cli fetch-manual`.

## Project layout

```
src/lakelevels/
  config.py         paths, env vars, source URLs
  models.py         LakeReading / RainfallReading dataclasses
  db.py             SQLite storage
  reference.py      loads data/reference_data.json
  cli.py            fetch / report commands
  dashboard.py       Streamlit visualization
  sources/
    bmc_lakes.py     best-effort BMC portal scraper
    imd_rainfall.py  IMD API client (needs IMD_API_KEY)
    manual.py        CSV fallback loader
data/
  reference_data.json          static demand/supply/usage figures
  manual_lake_readings.csv     hand-entered lake levels
  manual_rainfall_readings.csv hand-entered rainfall
tests/
```

## Data provenance for reference figures

See `data/reference_data.json` → `_meta.sources`. Figures (demand ~4200 MLD, supply ~3850-4100 MLD, usage split) are drawn from BMC hydraulic department reporting as covered in local press; update the JSON file as BMC publishes newer numbers.
