from dataclasses import dataclass


@dataclass
class LakeReading:
    date: str  # YYYY-MM-DD
    lake_name: str
    level_percent: float | None
    content_million_litres: float | None
    source: str


@dataclass
class RainfallReading:
    timestamp: str  # ISO 8601
    station: str
    rainfall_mm: float
    period: str  # e.g. "hourly", "daily"
    source: str
