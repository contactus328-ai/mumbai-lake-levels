"""Streamlit dashboard: streamlit run src/lakelevels/dashboard.py"""
import pandas as pd
import streamlit as st

from lakelevels import db, reference

st.set_page_config(page_title="Mumbai Lake Levels", layout="wide")
st.title("Mumbai Water Supply Dashboard")

db.init_db()
with db.get_connection() as conn:
    lake_rows = db.latest_lake_readings(conn)
    rain_rows = db.latest_rainfall_readings(conn, limit=48)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Latest Lake Levels")
    if lake_rows:
        df = pd.DataFrame([dict(r) for r in lake_rows])
        st.bar_chart(df.set_index("lake_name")["level_percent"])
        st.dataframe(df[["lake_name", "level_percent", "content_million_litres", "date", "source"]])
    else:
        st.info("No lake readings yet. Run `python -m lakelevels.cli fetch-manual` after adding rows to data/manual_lake_readings.csv.")

with col2:
    st.subheader("Rainfall (mm)")
    if rain_rows:
        df = pd.DataFrame([dict(r) for r in rain_rows]).sort_values("timestamp")
        st.line_chart(df.set_index("timestamp")["rainfall_mm"])
        st.dataframe(df[["timestamp", "station", "rainfall_mm", "period", "source"]])
    else:
        st.info("No rainfall readings yet. Run `python -m lakelevels.cli fetch-manual` after adding rows to data/manual_rainfall_readings.csv.")

st.divider()
st.subheader("Mumbai Water Supply — Reference Data")

balance = reference.get_water_balance()
usage = reference.get_usage_breakdown()
lakes = reference.get_lakes()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Daily demand", f"{balance['daily_demand_mld']} MLD")
m2.metric("Daily supply", f"{balance['daily_supply_mld']} MLD")
m3.metric("7-lakes daily draw", f"{balance['seven_lakes_daily_draw_mld']} MLD")
m4.metric("Number of lakes", len(lakes))

st.write("**Usage breakdown**")
st.bar_chart(pd.Series(usage).drop("note", errors="ignore"))

st.write("**The 7 lakes supplying Mumbai**")
st.dataframe(pd.DataFrame(lakes))
