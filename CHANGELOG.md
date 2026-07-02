# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `CHANGELOG.md`.

## [0.1.0] - 2026-07-02

### Added
- Initial project scaffold: package layout, config, data models, SQLite storage, and CLI (`init-db`, `fetch`, `fetch-manual`, `report`).
- BMC lake-level scraper (`sources/bmc_lakes.py`) — best-effort, fails soft since the official portal doesn't render outside a full browser session.
- IMD rainfall API connector (`sources/imd_rainfall.py`) — requires a user-supplied `IMD_API_KEY`, fails soft without one.
- Manual CSV fallback (`sources/manual.py`) for both lake levels and rainfall.
- Static reference data (`data/reference_data.json`): the 7 lakes supplying Mumbai, daily demand/supply figures (MLD), and residential/commercial/industrial usage split.
- Streamlit dashboard (`dashboard.py`) visualizing lake levels, rainfall, and reference data.
- Sample data: 35 lake readings (7 lakes x 5 days) and 144 hourly rainfall readings (2 stations x 3 days), tagged `source=sample_data`.
- Test suite for reference data (`tests/test_reference.py`).
- `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE` (MIT).
