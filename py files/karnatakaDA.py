import streamlit as st
import pandas as pd
import plotly.express as px
from chatbot import answer_question
from rules_engine import detect_wrong_practices
from crop_models import recommend_crop_env, recommend_crop_location, recommend_crop_rotation

# Load data
df = pd.read_csv("data_season.csv")

st.set_page_config(page_title="Smart Crop Advisory Dashboard", layout="wide")
st.title("\ud83c\udf3e Smart Crop Advisory System")

# Sidebar options
option = st.sidebar.selectbox("Choose Feature", [
    "Home Dashboard",
    "Crop Comparison",
    "Recommend Crop (Env Params)",
    "Recommend Crop (Location/Season)",
    "Suggest Crop Rotation",
    "Check Farming Practices",
    "Chat with CropBot"
])

# Home Dashboard
if option == "Home Dashboard":
    st.header("Overview of Crop Data")
    st.dataframe(df.head(50))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Average Yield per Crop")
        fig = px.bar(df.groupby("Crops")["yeilds"].mean().sort_values().reset_index(), x="yeilds", y="Crops", orientation='h')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Crop Distribution by Season")
        fig = px.pie(df, names="Season", title="Seasonal Crop Share")
        st.plotly_chart(fig, use_container_width=True)

# Crop Comparison
elif option == "Crop Comparison":
    crops = df["Crops"].unique()
    selected = st.multiselect("Select up to 3 crops to compare", crops)
    if selected:
        filtered = df[df["Crops"].isin(selected)]
        st.subheader("Yield Comparison")
        fig = px.line(filtered, x="Year", y="yeilds", color="Crops", markers=True)
        st.plotly_chart(fig)

        st.subheader("Price Trend")
        fig = px.line(filtered, x="Year", y="price", color="Crops", markers=True)
        st.plotly_chart(fig)

# Recommend by Env Params
elif option == "Recommend Crop (Env Params)":
    st.subheader("Enter Environmental Parameters")
    ph = st.number_input("Soil pH", 4.0, 9.0, step=0.1)
    N = st.number_input("Nitrogen (N)", 0, 500)
    P = st.number_input("Phosphorous (P)", 0, 500)
    K = st.number_input("Potassium (K)", 0, 500)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 3000.0)
    temp = st.number_input("Temperature (°C)", 10.0, 45.0)
    humidity = st.number_input("Humidity (%)", 20.0, 100.0)

    if st.button("Suggest Crop"):
        result = recommend_crop_env(ph, N, P, K, rainfall, temp, humidity)
        st.success(f"Recommended Crop: {result}")

# Recommend by Location & Season
elif option == "Recommend Crop (Location/Season)":
    st.subheader("Select Location & Season")
    states = df["Location"].unique()
    loc = st.selectbox("Location", sorted(states))
    season = st.selectbox("Season", ["Kharif", "Rabi", "Whole Year"])
    if st.button("Get Recommendation"):
        crop = recommend_crop_location(loc, season)
        st.success(f"Best suited crop: {crop}")

# Crop Rotation Suggestion
elif option == "Suggest Crop Rotation":
    st.subheader("Enter Previous Crop for Rotation Suggestion")
    previous = st.selectbox("Previous Crop", df["Crops"].unique())
    if st.button("Suggest Rotation Crop"):
        rotation = recommend_crop_rotation(previous)
        st.success(f"Suggested Crop for Rotation: {rotation}")

# Check for Wrong Practices
elif option == "Check Farming Practices":
    st.subheader("Enter Your Farming Practices")
    crop = st.selectbox("Crop", df["Crops"].unique())
    season = st.selectbox("Season", ["Kharif", "Rabi", "Whole Year"])
    irrigation = st.selectbox("Irrigation Type", df["Irrigation"].unique())
    humidity = st.number_input("Humidity", 20.0, 100.0)
    rainfall = st.number_input("Rainfall", 0.0, 3000.0)
    temp = st.number_input("Temperature", 10.0, 45.0)

    if st.button("Check My Practice"):
        problems = detect_wrong_practices(crop, season, irrigation, rainfall, temp, humidity)
        if problems:
            for issue in problems:
                st.error(issue)
        else:
            st.success("Your farming practice seems good!")

# Chatbot Interface
elif option == "Chat with CropBot":
    st.subheader("Ask me anything about crops ✨")
    user_input = st.text_input("Ask your question:")
    if user_input:
        response = answer_question(user_input)
        st.info(response)
