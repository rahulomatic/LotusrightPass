import geopandas as gpd
import networkx as nx
from accessibility import compute_nearest_hospital

# Load processed data
population = gpd.read_file("backend/data/processed/population.geojson")
hospitals = gpd.read_file("backend/data/processed/hospitals.geojson")
graph = nx.read_graphml("backend/data/processed/road_network.graphml")

# Run accessibility analysis
result = compute_nearest_hospital(graph, population, hospitals)

# Save outputs
result.to_file(
    "backend/data/processed/accessibility_results.geojson",
    driver="GeoJSON"
)

print("✅ Accessibility analysis completed")

avg_time = result["travel_time_sec"].mean() / 60
underserved_pct = result["underserved"].mean() * 100

print(f"Average travel time: {avg_time:.2f} minutes")
print(f"Underserved zones: {underserved_pct:.1f}%")