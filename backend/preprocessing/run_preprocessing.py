from load_data import load_population, load_hospitals
from clean_coordinates import project_to_meters
from build_graph import build_road_graph, save_graph

# Load data
population = load_population("data/raw/population.csv")
hospitals = load_hospitals("data/raw/hospitals.csv")

# Project for distance calculations
population_proj = project_to_meters(population)
hospitals_proj = project_to_meters(hospitals)

# Save processed data
population_proj.to_file("data/processed/population.geojson", driver="GeoJSON")
hospitals_proj.to_file("data/processed/hospitals.geojson", driver="GeoJSON")

# Build road network
graph = build_road_graph("Kozhikode, Kerala, India")
save_graph(graph, "data/processed/road_network.graphml")

print("✅ Preprocessing complete")