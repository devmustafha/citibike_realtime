import streamlit as st


def render_station_explorer(occupancy, utilization):
    st.header("Station Explorer")

    stations = occupancy["station_id"].sort_values().tolist()

    selected_station = st.selectbox(
        "Select a station",
        stations,
    )

    current = occupancy[occupancy["station_id"] == selected_station].iloc[0]

    history = utilization[utilization["station_id"] == selected_station].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚲 Bikes Available",
            f"{current['bikes_available']:.0f}",
        )

    with col2:
        st.metric(
            "🅿️ Docks Available",
            f"{current['docks_available']:.0f}",
        )

    with col3:
        st.metric(
            "📊 Occupancy",
            f"{current['bike_occupancy_rate']:.2f}%",
        )

    st.caption(f"Snapshot: {current['snapshot_time']}")

    st.subheader("Station Utilization")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Avg Bikes",
            f"{history['avg_bikes_available']:.2f}",
        )

    with col2:
        st.metric(
            "Avg Docks",
            f"{history['avg_docks_available']:.2f}",
        )

    with col3:
        st.metric(
            "Avg Occupancy",
            f"{history['avg_occupancy_rate']:.2f}%",
        )

    with col4:
        st.metric(
            "Observation Days",
            f"{history['observation_days']}",
        )
