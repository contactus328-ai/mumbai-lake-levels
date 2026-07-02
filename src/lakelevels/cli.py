"""CLI entrypoint: python -m lakelevels.cli <command>

Commands:
    init-db         create the SQLite database and tables
    fetch           try live sources (BMC scrape, IMD API), fall back to manual CSVs
    fetch-manual    load only the manual CSV files in data/
    report          print latest lake levels, rainfall, and reference stats
"""
import argparse
import sys
from datetime import date

from lakelevels import db, reference
from lakelevels.sources import bmc_lakes, imd_rainfall, manual


def cmd_init_db(_args) -> None:
    db.init_db()
    print("Database initialized.")


def cmd_fetch(_args) -> None:
    db.init_db()
    today = date.today().isoformat()

    lake_readings = bmc_lakes.fetch_bmc_lake_readings(today)
    if not lake_readings:
        lake_readings = manual.read_manual_lake_readings()

    rain_readings = imd_rainfall.fetch_hourly_rainfall()
    if not rain_readings:
        rain_readings = manual.read_manual_rainfall_readings()

    with db.get_connection() as conn:
        for r in lake_readings:
            db.insert_lake_reading(conn, r)
        for r in rain_readings:
            db.insert_rainfall_reading(conn, r)

    print(f"Stored {len(lake_readings)} lake readings, {len(rain_readings)} rainfall readings.")


def cmd_fetch_manual(_args) -> None:
    db.init_db()
    with db.get_connection() as conn:
        lake_readings = manual.read_manual_lake_readings()
        rain_readings = manual.read_manual_rainfall_readings()
        for r in lake_readings:
            db.insert_lake_reading(conn, r)
        for r in rain_readings:
            db.insert_rainfall_reading(conn, r)
    print(f"Stored {len(lake_readings)} lake readings, {len(rain_readings)} rainfall readings from CSVs.")


def cmd_report(_args) -> None:
    db.init_db()
    with db.get_connection() as conn:
        lakes = db.latest_lake_readings(conn)
        rain = db.latest_rainfall_readings(conn)

    print("=== Latest Lake Levels ===")
    if lakes:
        for row in lakes:
            print(f"  {row['lake_name']:<20} {row['level_percent']}%  ({row['content_million_litres']} ML)  [{row['date']}, {row['source']}]")
    else:
        print("  No readings stored yet. Run `fetch` or `fetch-manual` first.")

    print("\n=== Recent Rainfall ===")
    if rain:
        for row in rain:
            print(f"  {row['timestamp']}  {row['station']:<12} {row['rainfall_mm']} mm  [{row['source']}]")
    else:
        print("  No readings stored yet.")

    print("\n=== Mumbai Water Reference Data ===")
    balance = reference.get_water_balance()
    print(f"  Daily demand:            {balance['daily_demand_mld']} MLD")
    print(f"  Daily supply:            {balance['daily_supply_mld']} MLD")
    print(f"  Seven lakes daily draw:  {balance['seven_lakes_daily_draw_mld']} MLD")
    print(f"  Number of lakes:         {len(reference.get_lakes())}")
    usage = reference.get_usage_breakdown()
    print(f"  Usage split:             residential {usage['residential']}% / "
          f"commercial {usage['commercial']}% / industrial {usage['industrial']}% / "
          f"other {usage['other_public_use']}%")


def main() -> None:
    parser = argparse.ArgumentParser(prog="lakelevels")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db").set_defaults(func=cmd_init_db)
    sub.add_parser("fetch").set_defaults(func=cmd_fetch)
    sub.add_parser("fetch-manual").set_defaults(func=cmd_fetch_manual)
    sub.add_parser("report").set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
