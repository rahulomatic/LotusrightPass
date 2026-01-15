import geopandas as gpd
import osmnx as ox

from accessibility_optimized import compute_accessibility_optimized

# -------------------------------
# LOAD ROAD NETWORK (IN-MEMORY)
# -------------------------------
print("⏳ Loading road network in memory...")

graph = ox.graph_from_place(
    "Kozhikode, Kerala, India",
    network_type="drive"
)

graph = ox.add_edge_speeds(graph)
graph = ox.add_edge_travel_times(graph)

print("✅ Road network ready")

# -------------------------------
# LOAD PREPROCESSED DATA
# -------------------------------
population = gpd.read_file(
    "backend/data/processed/population.geojson"
)

hospitals = gpd.read_file(
    "backend/data/processed/hospitals.geojson"
)

# -------------------------------
# RUN ACCESSIBILITY ANALYSIS
# -------------------------------
result = compute_accessibility_optimized(
    graph,
    population,
    hospitals
)

# -------------------------------
# SAVE OUTPUT
# -------------------------------
result.to_file(
    "backend/data/processed/accessibility_results.geojson",
    driver="GeoJSON"
)

print("✅ Milestone 2 accessibility analysis completed")