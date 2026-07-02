import sqlite3
from contextlib import contextmanager

from lakelevels.config import DB_PATH
from lakelevels.models import LakeReading, RainfallReading

SCHEMA = """
CREATE TABLE IF NOT EXISTS lake_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    lake_name TEXT NOT NULL,
    level_percent REAL,
    content_million_litres REAL,
    source TEXT NOT NULL,
    UNIQUE(date, lake_name, source)
);

CREATE TABLE IF NOT EXISTS rainfall_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    station TEXT NOT NULL,
    rainfall_mm REAL NOT NULL,
    period TEXT NOT NULL,
    source TEXT NOT NULL,
    UNIQUE(timestamp, station, period, source)
);
"""


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def insert_lake_reading(conn: sqlite3.Connection, reading: LakeReading) -> None:
    conn.execute(
        """INSERT OR IGNORE INTO lake_readings
           (date, lake_name, level_percent, content_million_litres, source)
           VALUES (?, ?, ?, ?, ?)""",
        (reading.date, reading.lake_name, reading.level_percent,
         reading.content_million_litres, reading.source),
    )


def insert_rainfall_reading(conn: sqlite3.Connection, reading: RainfallReading) -> None:
    conn.execute(
        """INSERT OR IGNORE INTO rainfall_readings
           (timestamp, station, rainfall_mm, period, source)
           VALUES (?, ?, ?, ?, ?)""",
        (reading.timestamp, reading.station, reading.rainfall_mm,
         reading.period, reading.source),
    )


def latest_lake_readings(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """SELECT * FROM lake_readings l
           WHERE date = (SELECT MAX(date) FROM lake_readings)
           ORDER BY lake_name"""
    ).fetchall()


def latest_rainfall_readings(conn: sqlite3.Connection, limit: int = 24) -> list[sqlite3.Row]:
    return conn.execute(
        """SELECT * FROM rainfall_readings
           ORDER BY timestamp DESC LIMIT ?""",
        (limit,),
    ).fetchall()
