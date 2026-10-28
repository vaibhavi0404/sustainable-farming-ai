import streamlit as st
import pandas as pd

from agents import (
    soil_agent,
    weather_agent,
    market_agent,
    decision_agent
)
from database import create_database, save_report, get_reports


# PAGE SETTINGS
st.set_page_config(
    page_title="Sustainable Farming AI",
    page_icon="🌱",
    layout="wide"
)

create_database()

st.title("🌱 Multi-Agent AI System for Sustainable Farming")
st.write(
    "An AI-driven decision support prototype combining "
    "soil, weather, and market information."
)

st.info(
    "Demo notice: The market prices are illustrative sample data. "
    "This prototype does not provide live weather or market feeds."
)


# SIDEBAR INPUTS
st.sidebar.header("Farm Information")

ph = st.sidebar.slider("Soil pH", 3.0, 10.0, 6.5, 0.1)
nitrogen = st.sidebar.number_input(
    "Nitrogen (sample value)", min_value=0, max_value=200, value=50
)
phosphorus = st.sidebar.number_input(
    "Phosphorus (sample value)", min_value=0, max_value=200, value=40
)
potassium = st.sidebar.number_input(
    "Potassium (sample value)", min_value=0, max_value=200, value=45
)

temperature = st.sidebar.slider(
    "Temperature (°C)", -5, 50, 28
)
rainfall = st.sidebar.number_input(
    "Rainfall (mm)", min_value=0, max_value=500, value=80
)

st.sidebar.subheader("Sample Market Prices (₹ per quintal)")

rice_price = st.sidebar.number_input(
    "Rice price", min_value=0, value=2200
)
wheat_price = st.sidebar.number_input(
    "Wheat price", min_value=0, value=2400
)
maize_price = st.sidebar.number_input(
    "Maize price", min_value=0, value=2000
)
cotton_price = st.sidebar.number_input(
    "Cotton price", min_value=0, value=7000
)


# RUN THE MULTI-AGENT ANALYSIS
if st.button("Analyze Farm", type="primary"):

    soil = soil_agent(ph, nitrogen, phosphorus, potassium)

    weather = weather_agent(temperature, rainfall)

    market = market_agent({
        "Rice": rice_price,
        "Wheat": wheat_price,
        "Maize": maize_price,
        "Cotton": cotton_price
    })

    decision = decision_agent(soil, weather, market)

    # DISPLAY AGENT RESULTS
    st.header("Agent Analysis Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🧪 Soil Agent")
        st.write(soil["ph_status"])
        st.write(soil["npk_status"])

    with col2:
        st.subheader("🌦️ Weather Agent")
        st.write(weather["temperature_status"])
        st.write(weather["rainfall_status"])

    with col3:
        st.subheader("📈 Market Agent")
        st.write(market["summary"])

    st.divider()

    st.header("🌱 Final Farming Recommendations")

    for recommendation in decision["recommendations"]:
        st.success(recommendation)

    # SAVE RESULTS TO SQLITE
    save_report(
        soil["summary"],
        weather["summary"],
        market["summary"],
        "; ".join(decision["recommendations"])
    )

    st.success("Analysis saved successfully to the SQLite database.")


# PREVIOUS REPORTS
st.divider()
st.header("📂 Saved Farming Reports")

reports = get_reports()

if reports:
    report_data = []

    for row in reports:
        report_data.append({
            "Report ID": row[0],
            "Soil Analysis": row[1],
            "Weather Analysis": row[2],
            "Market Analysis": row[3],
            "Recommendations": row[4],
            "Created At": row[5]
        })

    st.dataframe(
        pd.DataFrame(report_data),
        use_container_width=True
    )
else:
    st.write("No reports saved yet. Run your first analysis!")