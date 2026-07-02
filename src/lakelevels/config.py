import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = PROJECT_ROOT / "lakelevels.db"

REFERENCE_DATA_PATH = DATA_DIR / "reference_data.json"
MANUAL_LAKE_CSV = DATA_DIR / "manual_lake_readings.csv"
MANUAL_RAINFALL_CSV = DATA_DIR / "manual_rainfall_readings.csv"

IMD_API_KEY = os.getenv("IMD_API_KEY", "")
IMD_API_BASE_URL = "https://api.imd.gov.in/public"

BMC_LAKE_DATA_URL = "https://www.mcgm.gov.in/irj/portal/anonymous/qlhydrlc"
