"""Load hand-entered readings from the CSV files in data/.

This is the most reliable data path: BMC's lake data lives behind a legacy
portal that can't be scraped without a full browser session, and IMD's hourly
rainfall API requires a registered key. Until those are wired up (or when
they fail), append rows to the CSVs in data/ and run `lakelevels fetch-manual`.
"""
import csv

from lakelevels.config import MANUAL_LAKE_CSV, MANUAL_RAINFALL_CSV
from lakelevels.models import LakeReading, RainfallReading


def read_manual_lake_readings() -> list[LakeReading]:
    readings = []
    with open(MANUAL_LAKE_CSV, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not row.get("date"):
                continue
            readings.append(LakeReading(
                date=row["date"],
                lake_name=row["lake_name"],
                level_percent=float(row["level_percent"]) if row.get("level_percent") else None,
                content_million_litres=float(row["content_million_litres"]) if row.get("content_million_litres") else None,
                source=row.get("source") or "manual",
            ))
    return readings


def read_manual_rainfall_readings() -> list[RainfallReading]:
    readings = []
    with open(MANUAL_RAINFALL_CSV, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not row.get("timestamp"):
                continue
            readings.append(RainfallReading(
                timestamp=row["timestamp"],
                station=row["station"],
                rainfall_mm=float(row["rainfall_mm"]),
                period=row.get("period") or "hourly",
                source=row.get("source") or "manual",
            ))
    return readings
