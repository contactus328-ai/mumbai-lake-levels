"""Static reference data: Mumbai's lakes, water demand/supply, and sector usage."""
import json
from functools import lru_cache

from lakelevels.config import REFERENCE_DATA_PATH


@lru_cache
def load_reference_data() -> dict:
    with open(REFERENCE_DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_lakes() -> list[dict]:
    return load_reference_data()["lakes"]


def get_water_balance() -> dict:
    return load_reference_data()["water_balance_mld"]


def get_usage_breakdown() -> dict:
    return load_reference_data()["usage_breakdown_percent"]
