import streamlit as st


def render_system_metrics(availability, health):
    availability_row = availability.iloc[0]
    health_row = health.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🚲 Bikes Available",
            value=f"{availability_row['total_bikes_available']:,}",
        )

    with col2:
        st.metric(
            label="🅿️ Docks Available",
            value=f"{availability_row['total_docks_available']:,}",
        )

    with col3:
        st.metric(
            label="📊 Bike Occupancy",
            value=f"{availability_row['bike_occupancy_rate']:.0%}",
        )

    with col4:
        st.metric(
            label="📍 Active Stations",
            value=f"{health_row['active_station_count']:,}",
            delta=f"{health_row['disabled_station_count']:,} disabled",
            delta_color="inverse",
        )
