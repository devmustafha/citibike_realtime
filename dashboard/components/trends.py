import streamlit as st


def render_trends(hourly, daily):
    st.header("Historical Trends")

    hourly_tab, daily_tab = st.tabs(["Hourly", "Daily"])

    with hourly_tab:
        if hourly.empty:
            st.info("No hourly trend data available.")
        else:
            st.subheader("Hourly Occupancy")

            st.line_chart(hourly.set_index("hour")[["avg_occupancy_rate"]])

            st.subheader("Hourly Availability")

            st.line_chart(
                hourly.set_index("hour")[
                    [
                        "avg_bikes_available",
                        "avg_docks_available",
                    ]
                ]
            )

    with daily_tab:
        if daily.empty:
            st.info("No daily trend data available.")
        else:
            st.subheader("Daily Occupancy")

            st.line_chart(
                daily.set_index("date")[
                    [
                        "avg_occupancy_rate",
                        "peak_occupancy_rate",
                        "lowest_occupancy_rate",
                    ]
                ]
            )

            st.subheader("Daily Availability")

            st.line_chart(
                daily.set_index("date")[
                    [
                        "avg_bikes_available",
                        "avg_docks_available",
                    ]
                ]
            )
