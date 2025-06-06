import streamlit as st

import numpy as np
import pandas as pd

from datetime import datetime, date, time
import requests

st.markdown("""# 🚖 Taxi Fare Prediction
## Please select the ride parameters:
This is text""")

# 1. Date and Time
pickup_date = st.date_input("📅 Pickup Date", value=date.today())
pickup_time = st.time_input("⏰ Pickup Time", value=datetime.now().time())
pickup_datetime = datetime.combine(pickup_date, pickup_time)

# 2. Pickup Coordinates
pickup_longitude = st.number_input("📍 Pickup Longitude", value=-73.985428, format="%.6f")
pickup_latitude = st.number_input("📍 Pickup Latitude", value=40.748817, format="%.6f")

# 3. Dropoff Coordinates
dropoff_longitude = st.number_input("🏁 Dropoff Longitude", value=-73.985428, format="%.6f")
dropoff_latitude = st.number_input("🏁 Dropoff Latitude", value=40.748817, format="%.6f")

# 4. Passenger Count
passenger_count = st.number_input("👥 Passenger Count", min_value=1, max_value=8, value=1)


params = {
    "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": int(passenger_count)
}

if st.button("🚕 Predict Fare"):
    url = 'https://taxifare.lewagon.ai/predict'
    response = requests.get(url, params=params)

    if response.status_code == 200:
        result = response.json()
        fare = result.get("fare")  # assuming response is {'fare': float}

        if fare is not None:
            st.success(f"💰 Estimated Fare: ${fare:.2f}")
        else:
            st.error("⚠️ 'fare' not found in API response.")
    else:
        st.error(f"❌ API request failed with status code {response.status_code}")


st.markdown("### 🗺 Pickup & Dropoff Locations")

map_df = pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude]
}, index=["Pickup", "Dropoff"])

st.map(map_df)

st.balloons()
