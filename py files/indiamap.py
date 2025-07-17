import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load datasets
df = pd.read_csv("crop_data.csv")
city_coords = pd.read_csv("in.csv")

# Standardize strings
df["District"] = df["District"].str.lower().str.strip()
df["State"] = df["State"].str.lower().str.strip()
city_coords["city"] = city_coords["city"].str.lower().str.strip()
city_coords["admin_name"] = city_coords["admin_name"].str.lower().str.strip()

# Get most common crop per district
top_crops = df.dropna(subset=["Crop"]).groupby(["State", "District"])["Crop"].agg(lambda x: x.value_counts().index[0]).reset_index()
top_crops.columns = ["state", "district", "most_common_crop"]

# Merge with coordinates
merged = pd.merge(top_crops, city_coords, how="inner", left_on="district", right_on="city")

# Create map
india_map = folium.Map(location=[22.9734, 78.6569], zoom_start=5)
marker_cluster = MarkerCluster().add_to(india_map)

for _, row in merged.iterrows():
    popup = f"<b>District:</b> {row['district'].title()}<br><b>State:</b> {row['state'].title()}<br><b>Crop:</b> {row['most_common_crop']}"
    folium.Marker(location=[row['lat'], row['lng']], popup=popup).add_to(marker_cluster)

# Save to HTML
india_map.save("Crop_Map_India.html")
