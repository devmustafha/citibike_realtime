import streamlit as st
from components.charts import render_demand_chart
from components.metrics import render_system_metrics
from components.station import render_station_explorer
from components.trends import render_trends

from analytics.duckdb.service import run_query

st.set_page_config(
    page_title="Citi Bike Analytics",
    page_icon="🚲",
    layout="wide",
)


@st.cache_data(ttl=300)
def load_system_metrics():
    return {
        "availability": run_query("systems/availability.sql"),
        "health": run_query("systems/health.sql"),
    }


@st.cache_data(ttl=300)
def load_demand():
    return run_query("systems/demand.sql")


@st.cache_data(ttl=300)
def load_station_data():
    return {
        "occupancy": run_query("stations/occupancy.sql"),
        "utilization": run_query("stations/utilization.sql"),
    }


@st.cache_data(ttl=300)
def load_trends():
    return {
        "hourly": run_query("trends/hourly.sql"),
        "daily": run_query("trends/daily.sql"),
    }


st.title("🚲 Citi Bike Analytics")

system_metrics = load_system_metrics()
demand = load_demand()
station_data = load_station_data()
trends = load_trends()


metrics_tab, stations_tab, trends_tab = st.tabs(["Overview", "Stations", "Trends"])


with metrics_tab:
    render_system_metrics(
        availability=system_metrics["availability"],
        health=system_metrics["health"],
    )

    render_demand_chart(demand)


with stations_tab:
    render_station_explorer(
        occupancy=station_data["occupancy"],
        utilization=station_data["utilization"],
    )


with trends_tab:
    render_trends(
        hourly=trends["hourly"],
        daily=trends["daily"],
    )
