"""IMD (India Meteorological Department) rainfall connector.

Requires an API key from https://api.imd.gov.in/public/index.php, set as
IMD_API_KEY in .env. Without a key, fetch_hourly_rainfall() returns an empty
list so callers fall back to lakelevels.sources.manual.

NOTE: IMD's public API surface changes; verify the endpoint path and response
shape against current API docs before relying on this in production, and
adjust ENDPOINT / the parsing below to match.
"""
import logging

import requests

from lakelevels.config import IMD_API_BASE_URL, IMD_API_KEY
from lakelevels.models import RainfallReading

logger = logging.getLogger(__name__)

ENDPOINT = f"{IMD_API_BASE_URL}/rainfall"
MUMBAI_STATIONS = ["Colaba", "Santacruz"]


def fetch_hourly_rainfall() -> list[RainfallReading]:
    if not IMD_API_KEY:
        logger.warning("IMD_API_KEY not set; use manual CSV fallback instead.")
        return []

    readings = []
    for station in MUMBAI_STATIONS:
        try:
            response = requests.get(
                ENDPOINT,
                params={"station": station, "period": "hourly"},
                headers={"Authorization": f"Bearer {IMD_API_KEY}"},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            logger.warning("IMD rainfall fetch failed for %s (%s).", station, exc)
            continue

        for entry in payload.get("data", []):
            try:
                readings.append(RainfallReading(
                    timestamp=entry["timestamp"],
                    station=station,
                    rainfall_mm=float(entry["rainfall_mm"]),
                    period="hourly",
                    source="imd_api",
                ))
            except (KeyError, ValueError):
                continue
    return readings
