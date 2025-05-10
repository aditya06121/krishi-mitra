import streamlit as st
import pandas as pd
import plotly.express as px


# Load data
df = pd.read_csv("data_season.csv")
df.columns = df.columns.str.strip().str.capitalize()  # Normalize columns

st.set_page_config(layout="wide")
st.title("🌾 Crop Production & Suggestion Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_season = st.sidebar.multiselect("Select Season", df["Season"].unique(), default=df["Season"].unique())
selected_crops = st.sidebar.multiselect("Select Crops", df["Crops"].unique(), default=df["Crops"].unique())
selected_location = st.sidebar.multiselect("Select Location", df["Location"].unique(), default=df["Location"].unique())

filtered = df[
    df["Season"].isin(selected_season) &
    df["Crops"].isin(selected_crops) &
    df["Location"].isin(selected_location)
]

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", 
    "🌱 Crop Suggestions", 
    "📈 Trends", 
    "🚨 Detect Wrong Practices", 
    "🔄 Suggest Crop Rotation", 
    "💬 Ask CropBot"
])

with tab1:
    st.subheader("Top 10 Crops by Average Yield")
    crop_yield_avg = filtered.groupby("Crops")["Yeilds"].mean().sort_values(ascending=False).reset_index()
    fig1 = px.bar(crop_yield_avg.head(10), x="Crops", y="Yeilds", color="Crops")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Distribution of Irrigation Types")
    irrigation_dist = filtered["Irrigation"].value_counts().reset_index()
    irrigation_dist.columns = ["Irrigation", "Count"]
    fig2 = px.pie(irrigation_dist, names="Irrigation", values="Count")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top 10 Locations by Total Yield")
    location_yield = filtered.groupby("Location")["Yeilds"].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(location_yield.head(10), x="Location", y="Yeilds", color="Location")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Download Filtered Data")
    st.download_button("⬇️ Download CSV", filtered.to_csv(index=False), file_name="filtered_crop_data.csv")

with tab2:
    st.subheader("Get Crop Suggestions Based on Environment")
    temp = st.slider("Temperature (°C)", 10.0, 40.0, 25.0)
    rain = st.slider("Rainfall (mm)", 0.0, 5000.0, 1500.0)
    humidity = st.slider("Humidity (%)", 10.0, 100.0, 60.0)

    suggested = df[
        (df['Temperature'].between(temp - 2, temp + 2)) &
        (df['Rainfall'].between(rain - 500, rain + 500)) &
        (df['Humidity'].between(humidity - 10, humidity + 10))
    ]

    if not suggested.empty:
        best = suggested.groupby("Crops")["Yeilds"].mean().sort_values(ascending=False).head(5)
        st.success("Top 5 crops to grow in this environment:")
        st.table(best)
    else:
        st.warning("No suggestions found for selected environmental conditions.")

with tab3:
    st.subheader("Average Yield per Season")
    season_yield = filtered.groupby("Season")["Yeilds"].mean().reset_index()
    fig4 = px.line(season_yield, x="Season", y="Yeilds", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Crop Distribution by Season")
    season_crop_dist = filtered.groupby(["Season", "Crops"]).size().reset_index(name='Count')
    fig5 = px.bar(season_crop_dist, x="Season", y="Count", color="Crops", barmode="stack")
    st.plotly_chart(fig5, use_container_width=True)

with tab4:
    st.subheader("🚨 Detect Wrong Farming Practices")
    check_crop = st.selectbox("Select Crop", df["Crops"].unique())
    input_temp = st.slider("Your Temperature (°C)", 10.0, 60.0, 25.0)
    input_rain = st.slider("Your Rainfall (mm)", 0.0, 5000.0, 1500.0)

    ref = df[df["Crops"] == check_crop]
    if not ref.empty:
        ideal_temp = ref["Temperature"].mean()
        ideal_rain = ref["Rainfall"].mean()

        issues = []
        if abs(input_temp - ideal_temp) > 3:
            issues.append(f"⚠️ Temperature is off. Ideal: {ideal_temp:.1f}°C")
        if abs(input_rain - ideal_rain) > 400:
            issues.append(f"⚠️ Rainfall is off. Ideal: {ideal_rain:.1f} mm")

        if issues:
            for i in issues:
                st.warning(i)
        else:
            st.success("✅ Your environmental practice looks good for this crop.")
    else:
        st.warning("No reference data found for this crop.")


with tab5:
    st.subheader("🔄 Crop Rotation Suggestions")

    st.markdown("Crop rotation helps improve soil fertility, manage pests, and maintain crop yields. Select your current crop:")

    crop_selected = st.selectbox("🌾 Current Crop", sorted(df["Crops"].unique()))

    # Rotation logic for common crops with reasons
    rotation_reasons = {
        ("Paddy", "Wheat"): "Breaks pest cycles and reduces water demand.",
        ("Wheat", "Pulses"): "Pulses fix nitrogen and enrich soil.",
        ("Pulses", "Maize"): "Maize benefits from improved nitrogen availability.",
        ("Maize", "Groundnut"): "Reduces soil compaction and adds organic matter.",
        ("Groundnut", "Cotton"): "Minimizes pest carryover and uses deep-rooted structure.",
        ("Cotton", "Millets"): "Restores micro-nutrient balance and resists drought.",
        ("Millets", "Vegetables"): "Takes advantage of residual fertility.",
        ("Vegetables", "Paddy"): "Balances soil moisture and nutrients.",
        ("Paddy", "Mustard"): "Controls weeds and diversifies root depth.",
        ("Mustard", "Sugarcane"): "Sugarcane benefits from pre-conditioned soil."
    }

    # Crops not requiring rotation and reasons
    non_rotation_crops = {
        "Coconut": ("Perennial", "Lives 60–80 years, rotation not needed."),
        "Ginger": ("Rhizome", "Often intercropped or left fallow, not rotated annually."),
        "Coffee": ("Perennial", "Remains for decades; rarely replaced."),
        "Cardamom": ("Perennial", "Under shade trees, not rotated."),
        "Arecanut": ("Perennial", "Plantation crop with long lifespan."),
        "Tea": ("Perennial", "Lasts decades, only pruned—not rotated.")
    }

    if crop_selected in [key[0] for key in rotation_reasons]:
        st.markdown(f"### 🔁 Suggested Rotation(s) for **{crop_selected}**:")
        for (curr, next_crop), reason in rotation_reasons.items():
            if curr == crop_selected:
                st.success(f"➡️ **{next_crop}**\n\n📝 _Reason: {reason}_")
    elif crop_selected in non_rotation_crops:
        crop_type, reason = non_rotation_crops[crop_selected]
        st.info(f"ℹ️ **{crop_selected}** is a **{crop_type}** crop.\n\n🔁 _Rotation not needed:_ {reason}")
    else:
        st.warning("⚠️ No specific rotation data found for this crop. Try another.")

    # Top 10 crop suggestions
    st.markdown("---")
    st.markdown("### 🌾 Top 10 Crops & Their Recommended Rotations:")

    top_crops = df["Crops"].value_counts().head(10).index.tolist()
    for crop in top_crops:
        if crop in non_rotation_crops:
            crop_type, reason = non_rotation_crops[crop]
            st.markdown(f"**❌ {crop}** (Type: _{crop_type}_) — {reason}")
        else:
            rotations = [pair for pair in rotation_reasons if pair[0] == crop]
            if rotations:
                st.markdown(f"**🔄 {crop}:**")
                for (cur, nxt) in rotations:
                    st.markdown(f"- ➡️ **{nxt}** (_{rotation_reasons[(cur, nxt)]}_)")
            else:
                st.markdown(f"**{crop}** ➡️ _(No rotation data available)_")


with tab6:
    st.subheader("💬 Ask CropBot (Interactive Assistant)")

    st.markdown("### 📌 Select a query type or ask a custom question:")

    query_type = st.selectbox("What do you want to ask about?", [
        "— Select —",
        "Best Crop for My Conditions",
        "Sowing Time of a Crop",
        "Ideal Conditions for a Crop",
        "Crops Suitable for a Season",
        "Custom Question"
    ])

    if query_type == "Best Crop for My Conditions":
        temp = st.slider("🌡️ Temperature (°C)", 10.0, 40.0, 25.0)
        rain = st.slider("🌧️ Rainfall (mm)", 0.0, 5000.0, 1500.0)
        humidity = st.slider("💧 Humidity (%)", 10.0, 100.0, 60.0)

        suggested = df[
            (df['Temperature'].between(temp - 2, temp + 2)) &
            (df['Rainfall'].between(rain - 500, rain + 500)) &
            (df['Humidity'].between(humidity - 10, humidity + 10))
        ]
        if not suggested.empty:
            top = suggested.groupby("Crops")["Yeilds"].mean().sort_values(ascending=False).head(5)
            st.success("Top 5 crops for your conditions:")
            st.table(top)
        else:
            st.warning("No crops found for selected conditions.")

    elif query_type == "Sowing Time of a Crop":
        selected_crop = st.selectbox("🌱 Select a crop", sorted(df["Crops"].unique()))
        if selected_crop:
            seasons = df[df["Crops"] == selected_crop]["Season"].mode()
            if not seasons.empty:
                st.success(f"🗓️ Sow **{selected_crop}** during the **{seasons[0]}** season.")
            else:
                st.warning("No sowing time data found.")

    elif query_type == "Ideal Conditions for a Crop":
        selected_crop = st.selectbox("🔍 Select crop", sorted(df["Crops"].unique()))
        if selected_crop:
            crop_df = df[df["Crops"] == selected_crop]
            if not crop_df.empty:
                temp = crop_df["Temperature"].mean()
                rain = crop_df["Rainfall"].mean()
                humidity = crop_df["Humidity"].mean()
                st.success(
                    f"🌡️ Temperature: {temp:.1f}°C\n"
                    f"🌧️ Rainfall: {rain:.1f} mm\n"
                    f"💧 Humidity: {humidity:.1f}%"
                )
            else:
                st.warning("No environment data for selected crop.")

    elif query_type == "Crops Suitable for a Season":
        selected_season = st.selectbox("🗓️ Select Season", sorted(df["Season"].unique()))
        crops_in_season = df[df["Season"] == selected_season]["Crops"].value_counts().head(10)
        if not crops_in_season.empty:
            st.success(f"🌱 Common crops in **{selected_season}** season:")
            st.table(crops_in_season)
        else:
            st.warning("No crops found for this season.")

    elif query_type == "Custom Question":
        user_input = st.text_input("💬 Type your question:")
        if user_input:
            user_input = user_input.lower()

            if "best crop" in user_input or "what crop" in user_input:
                st.info("Try using the 'Best Crop for My Conditions' section above.")
            elif "sow" in user_input or "plant" in user_input:
                for crop in df["Crops"].unique():
                    if crop.lower() in user_input:
                        season = df[df["Crops"] == crop]["Season"].mode().values[0]
                        st.success(f"🗓️ Sow **{crop}** during the **{season}** season.")
                        break
                else:
                    st.warning("🤷 Sorry, couldn't find sowing info for that crop.")
            elif "condition" in user_input or "grow" in user_input:
                for crop in df["Crops"].unique():
                    if crop.lower() in user_input:
                        row = df[df["Crops"] == crop]
                        st.success(
                            f"🌡️ Ideal Temp: {row['Temperature'].mean():.1f}°C\n"
                            f"🌧️ Rainfall: {row['Rainfall'].mean():.1f} mm\n"
                            f"💧 Humidity: {row['Humidity'].mean():.1f}%"
                        )
                        break
                else:
                    st.warning("No ideal conditions found for that crop.")
            else:
                st.info("Try asking about sowing time, best crops, or crop conditions.")
