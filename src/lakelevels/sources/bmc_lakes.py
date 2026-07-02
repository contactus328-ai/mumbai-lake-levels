"""Best-effort scraper for BMC's daily lake stock report.

The official page (BMC_LAKE_DATA_URL) is served from a legacy SAP NetWeaver
"iView" portal that returns an error outside a full browser session, so plain
HTTP requests will not get real data most of the time. This scraper is kept
as a best-effort attempt (in case BMC changes the page, or you swap in a
Selenium/Playwright-driven fetch later) and always fails soft: on any error
it returns an empty list so callers can fall back to
`lakelevels.sources.manual`.
"""
import logging

import requests
from bs4 import BeautifulSoup

from lakelevels.config import BMC_LAKE_DATA_URL
from lakelevels.models import LakeReading

logger = logging.getLogger(__name__)


def fetch_bmc_lake_readings(date: str) -> list[LakeReading]:
    try:
        response = requests.get(BMC_LAKE_DATA_URL, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("BMC lake data fetch failed (%s); use manual CSV fallback instead.", exc)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table is None:
        logger.warning("BMC lake data page returned no table; use manual CSV fallback instead.")
        return []

    readings = []
    for row in table.find_all("tr")[1:]:
        cells = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cells) < 3:
            continue
        lake_name, level_percent, content_ml = cells[0], cells[1], cells[2]
        try:
            readings.append(LakeReading(
                date=date,
                lake_name=lake_name,
                level_percent=float(level_percent.replace("%", "")),
                content_million_litres=float(content_ml.replace(",", "")),
                source="bmc_portal_scrape",
            ))
        except ValueError:
            continue
    return readings
