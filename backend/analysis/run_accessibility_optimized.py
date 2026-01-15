import geopandas as gpd
import networkx as nx
from accessibility_optimized import compute_accessibility_optimized

# Load data
population = gpd.read_file("backend/data/processed/population.geojson")
hospitals = gpd.read_file("backend/data/processed/hospitals.geojson")
graph = nx.read_graphml("backend/data/processed/road_network.graphml")

# Run optimized analysis
result = compute_accessibility_optimized(graph, population, hospitals)

# Save output
result.to_file(
    "backend/data/processed/accessibility_results_optimized.geojson",
    driver="GeoJSON"
)

# Stats
avg_time = result["travel_time_sec"].mean() / 60
underserved_pct = result["underserved"].mean() * 100

print("✅ Optimized accessibility analysis completed")
print(f"Average travel time: {avg_time:.2f} minutes")
print(f"Underserved zones: {underserved_pct:.1f}%")