import streamlit as st


def render_demand_chart(demand):
    st.subheader("Hourly Bike Occupancy")

    chart_data = demand.set_index("hour")["avg_occupancy_rate"]

    st.line_chart(chart_data)
