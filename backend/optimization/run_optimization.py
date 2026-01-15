import geopandas as gpd
import osmnx as ox
import json
import sys


from p_median import p_median_heuristic, evaluate_facility_set

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
# LOAD DATA
# -------------------------------
population = gpd.read_file(
    "backend/data/processed/accessibility_results.geojson"
)

hospitals = gpd.read_file(
    "backend/data/processed/hospitals.geojson"
)

# -------------------------------
# IDENTIFY UNDERSERVED ZONES
# -------------------------------
underserved = population[population["underserved"] == True]

if underserved.empty:
    print("ℹ️ No underserved zones found.")
    print("ℹ️ Existing hospitals provide adequate coverage.")

    # Save empty optimization results
    with open(
        "backend/data/processed/optimization_summary.json", "w"
    ) as f:
        f.write(
            '{ "message": "No underserved zones found. No new hospitals required." }'
        )

    # Exit gracefully
    sys.exit(0)


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

# -------------------------------
# BEFORE OPTIMIZATION
# -------------------------------
before_avg_time = evaluate_facility_set(
    graph,
    demand_nodes,
    existing_hospital_nodes
)

# -------------------------------
# RUN P-MEDIAN OPTIMIZATION
# -------------------------------
P_NEW_HOSPITALS = 2

new_facilities, after_avg_time = p_median_heuristic(
    graph,
    demand_nodes,
    candidate_nodes,
    p=P_NEW_HOSPITALS
)

# -------------------------------
# SAVE RESULTS
# -------------------------------
improvement = {
    "avg_travel_time_before_min": round(before_avg_time / 60, 2),
    "avg_travel_time_after_min": round(after_avg_time / 60, 2),
    "improvement_minutes": round((before_avg_time - after_avg_time) / 60, 2),
    "new_facilities_count": P_NEW_HOSPITALS
}

features = []
for i, node in enumerate(new_facilities):
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                graph.nodes[node]["x"],
                graph.nodes[node]["y"]
            ]
        },
        "properties": {"id": i}
    })

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open(
    "backend/data/processed/optimized_hospitals.geojson", "w"
) as f:
    json.dump(geojson, f, indent=4)

with open(
    "backend/data/processed/optimization_summary.json", "w"
) as f:
    json.dump(improvement, f, indent=4)

print("✅ Milestone 3 optimization completed")
print(improvement)