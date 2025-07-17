import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load your combined CSV with State, District, Crop, Latitude, Longitude
df = pd.read_csv(".csv")  # Make sure it has 'State', 'District', 'Crop', 'Latitude', 'Longitude'

# Clean and standardize text
df["State"] = df["State"].str.strip().str.title()
df["District"] = df["District"].str.strip().str.title()
df["Crop"] = df["Crop"].str.strip().str.title()

# Remove rows without coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Combine multiple crops for each district
grouped = df.groupby(["State", "District", "Latitude", "Longitude"])["Crop"].unique().reset_index()
grouped["Crops"] = grouped["Crop"].apply(lambda crops: ", ".join(sorted(set(crops))))

# Create base map
india_map = folium.Map(location=[22.9734, 78.6569], zoom_start=5)
marker_cluster = MarkerCluster().add_to(india_map)

# Add pins for each district
for _, row in grouped.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(
            f"<b>{row['District']}, {row['State']}</b><br><b>Crops:</b> {row['Crops']}",
            max_width=300,
        ),
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(marker_cluster)

# Save map
india_map.save("india_crop_map.html")
print("✅ Map saved as 'india_crop_map.html'")
