import os
import osmnx as ox
import networkx as nx

# Change this to your city/region
PLACE_NAME = "Kochi, Kerala, India"

# Resolve project paths safely
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

PROCESSED_DIR = os.path.join(BASE_DIR, "backend", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("⏳ Downloading road network from OpenStreetMap...")

# Download road network
G = ox.graph_from_place(
    PLACE_NAME,
    network_type="drive"
)

# Add speed & travel time
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# Save graph
output_path = os.path.join(PROCESSED_DIR, "road_network.graphml")
nx.write_graphml(G, output_path)

print("✅ Road network saved to:", output_path)