import folium
import geopandas as gpd

# Load data
population = gpd.read_file(
    "backend/data/processed/accessibility_results.geojson"
)
hospitals = gpd.read_file(
    "backend/data/processed/hospitals.geojson"
)
new_hospitals = gpd.read_file(
    "backend/data/processed/optimized_hospitals.geojson"
)

# Map center (mean of population points)
center_lat = population.geometry.y.mean()
center_lon = population.geometry.x.mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles="CartoDB positron"
)

# ------------------------
# Population Zones
# ------------------------
for _, row in population.iterrows():
    color = "red" if row["underserved"] else "green"

    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=f"""
        <b>Zone:</b> {row.get('zone_id', 'N/A')}<br>
        <b>Travel time:</b> {row['travel_time_min']:.2f} min<br>
        <b>Underserved:</b> {row['underserved']}
        """
    ).add_to(m)

# ------------------------
# Existing Hospitals
# ------------------------
for _, row in hospitals.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        icon=folium.Icon(color="blue", icon="plus-sign"),
        popup=f"<b>Hospital:</b> {row.get('name', 'Existing Hospital')}"
    ).add_to(m)

# ------------------------
# Suggested New Hospitals
# ------------------------
for _, row in new_hospitals.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        icon=folium.Icon(color="purple", icon="star"),
        popup="<b>Recommended New Hospital</b>"
    ).add_to(m)

# Save map
m.save("backend/data/processed/healthcare_accessibility_map.html")

print("✅ Interactive map generated")