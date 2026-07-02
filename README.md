# Mumbai Lake Levels

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
