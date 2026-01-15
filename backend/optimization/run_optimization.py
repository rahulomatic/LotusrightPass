import geopandas as gpd
import networkx as nx
import json
import osmnx as ox

from p_median import p_median_heuristic, evaluate_facility_set

TRAVEL_TIME_THRESHOLD = 30 * 60  # 30 minutes
P_NEW_HOSPITALS = 2


# Load data
graph = nx.read_graphml("backend/data/processed/road_network.graphml")
population = gpd.read_file("backend/data/processed/accessibility_results.geojson")
hospitals = gpd.read_file("backend/data/processed/hospitals.geojson")

# Identify underserved zones
underserved = population[population["underserved"] == True]

# Map to graph nodes
demand_nodes = ox.nearest_nodes(
    graph,
    underserved.geometry.x,
    underserved.geometry.y
)

candidate_nodes = ox.nearest_nodes(
    graph,
    population.geometry.x,
    population.geometry.y
)

existing_hospital_nodes = ox.nearest_nodes(
    graph,
    hospitals.geometry.x,
    hospitals.geometry.y
)

# BEFORE optimization
before_avg_time = evaluate_facility_set(
    graph,
    demand_nodes,
    existing_hospital_nodes
)

# Run p-median optimization
new_facilities, after_avg_time = p_median_heuristic(
    graph,
    demand_nodes,
    candidate_nodes,
    p=P_NEW_HOSPITALS
)

# Improvement metrics
improvement = {
    "avg_travel_time_before_min": round(before_avg_time / 60, 2),
    "avg_travel_time_after_min": round(after_avg_time / 60, 2),
    "improvement_minutes": round((before_avg_time - after_avg_time) / 60, 2),
    "new_facilities_count": P_NEW_HOSPITALS
}

# Convert new facility nodes to GeoJSON
new_points = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": (
                graph.nodes[n]["x"],
                graph.nodes[n]["y"]
            )
        },
        "properties": {"id": i}
    }
    for i, n in enumerate(new_facilities)
]

geojson = {
    "type": "FeatureCollection",
    "features": new_points
}

# Save outputs
with open("backend/data/processed/optimized_hospitals.geojson", "w") as f:
    json.dump(geojson, f, indent=4)

with open("backend/data/processed/optimization_summary.json", "w") as f:
    json.dump(improvement, f, indent=4)

print("✅ Milestone 3 completed")
print(improvement)