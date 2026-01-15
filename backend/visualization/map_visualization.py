import folium
import geopandas as gpd
import os

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_DIR = os.path.join(BASE_DIR, "backend", "data", "processed")

# -------------------------------
# LOAD DATA
# -------------------------------
population = gpd.read_file(
    os.path.join(DATA_DIR, "accessibility_results.geojson")
)

hospitals = gpd.read_file(
    os.path.join(DATA_DIR, "hospitals.geojson")
)

optimized_path = os.path.join(
    DATA_DIR, "optimized_hospitals.geojson"
)

has_new_hospitals = os.path.exists(optimized_path)

if has_new_hospitals:
    new_hospitals = gpd.read_file(optimized_path)

# -------------------------------
# MAP SETUP
# -------------------------------
center_lat = population.geometry.y.mean()
center_lon = population.geometry.x.mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles="CartoDB positron"
)

# -------------------------------
# POPULATION ZONES
# -------------------------------
for _, row in population.iterrows():
    color = "red" if row["underserved"] else "green"

    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=6,
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=f"""
        <b>Travel time:</b> {row['travel_time_min']:.2f} min<br>
        <b>Underserved:</b> {row['underserved']}
        """
    ).add_to(m)

# -------------------------------
# EXISTING HOSPITALS
# -------------------------------
for _, row in hospitals.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        icon=folium.Icon(color="blue", icon="plus-sign"),
        popup="Existing Hospital"
    ).add_to(m)

# -------------------------------
# NEW HOSPITALS (OPTIONAL)
# -------------------------------
if has_new_hospitals:
    for _, row in new_hospitals.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            icon=folium.Icon(color="purple", icon="star"),
            popup="Recommended New Hospital"
        ).add_to(m)
else:
    folium.map.Marker(
        [center_lat, center_lon],
        icon=folium.DivIcon(
            html="""
            <div style="font-size:14px;color:green;">
            ✅ No new hospitals required (full coverage)
            </div>
            """
        )
    ).add_to(m)

# -------------------------------
# SAVE MAP
# -------------------------------
output_path = os.path.join(
    DATA_DIR, "healthcare_accessibility_map.html"
)

m.save(output_path)

print("✅ Map generated:", output_path)