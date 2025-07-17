import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load Models
with open("crop_recommendation_model.pkl", "rb") as f:
    model1 = pickle.load(f)

with open("crop_encoder.pkl", "rb") as f:
    model2 = pickle.load(f)

with open("crop_rotation_model.pkl", "rb") as f:
    model3 = pickle.load(f)

st.set_page_config(page_title="Crop Advisor", layout="wide")
st.title("🌾 Intelligent Crop Advisor")

# Tabs for each model
tab1, tab2, tab3 = st.tabs([
    "Model 1 - Based on Soil & Climate",
    "Model 2 - Based on Location & Season",
    "Model 3 - Crop Rotation Suggestion"
])

# ------------------- TAB 1: CROP RECOMMENDATION MODEL -------------------
with tab1:
    st.subheader("🔬 Predict Crop (pH, N, P, K, Rainfall, Humidity, Temperature)")
    col1, col2, col3 = st.columns(3)
    with col1:
        N = st.number_input("Nitrogen (N)", min_value=0.0, max_value=140.0, value=50.0)
        P = st.number_input("Phosphorous (P)", min_value=0.0, max_value=150.0, value=50.0)
        K = st.number_input("Potassium (K)", min_value=0.0, max_value=200.0, value=50.0)
    with col2:
        temp = st.slider("Temperature (°C)", 0.0, 50.0, 25.0)
        humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0)
    with col3:
        ph = st.slider("pH value", 0.0, 14.0, 6.5)
        rainfall = st.slider("Rainfall (mm)", 0.0, 400.0, 100.0)

    if st.button("🔍 Predict Best Crop", key="model1"):
        features = np.array([[N, P, K, temp, humidity, ph, rainfall]])
        prediction = model1.predict(features)[0]
        st.success(f"🌱 Recommended Crop: **{prediction.capitalize()}**")

# ------------------- TAB 2: ENCODED LOCATION-BASED CROP MODEL -------------------
with tab2:
    st.subheader("🗺️ Predict Crop (State, District, Season)")

    # Modify based on your encoder data
    states = ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Uttar Pradesh']
    districts = ['Bangalore', 'Pune', 'Chennai', 'Lucknow']
    seasons = ['Kharif', 'Rabi', 'Whole Year']

    selected_state = st.selectbox("State", states)
    selected_district = st.selectbox("District", districts)
    selected_season = st.selectbox("Season", seasons)

    if st.button("🔍 Predict Crop", key="model2"):
        try:
            # Encode inputs numerically if model2 is trained on label-encoded values
            input_data = pd.DataFrame([[selected_state, selected_district, selected_season]],
                                      columns=['State', 'District', 'Season'])

            # If model2 expects encoded input, encode using saved encoder if available
            prediction = model2.predict(input_data)[0]
            st.success(f"🌾 Suitable Crop: **{prediction.capitalize()}**")
        except Exception as e:
            st.error(f"⚠️ Could not make prediction. Error: {e}")

# ------------------- TAB 3: CROP ROTATION MODEL -------------------
with tab3:
    st.subheader("🔄 Predict Crop to Rotate")

    prev_crop = st.selectbox("Select Your Previous Crop", [
        "rice", "wheat", "maize", "cotton", "barley", "bajra", "jowar"
    ])

    if st.button("🔁 Suggest Next Crop", key="model3"):
        try:
            prediction = model3.predict([[prev_crop]])[0]
            st.success(f"🔄 You should rotate to: **{prediction.capitalize()}**")
        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")
