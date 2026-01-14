import geopandas as gpd
import networkx as nx
import osmnx as ox
import numpy as np

TRAVEL_TIME_THRESHOLD = 30 * 60  # 30 minutes in seconds


def map_points_to_nodes(graph, gdf):
    """
    Map GeoDataFrame points to nearest graph nodes
    """
    return ox.nearest_nodes(
        graph,
        X=gdf.geometry.x,
        Y=gdf.geometry.y
    )


def multi_source_dijkstra(graph, hospital_nodes):
    """
    Computes shortest travel time from ANY hospital
    to all reachable nodes (with cutoff for scale)
    """
    lengths = nx.multi_source_dijkstra_path_length(
        graph,
        hospital_nodes,
        cutoff=TRAVEL_TIME_THRESHOLD,
        weight="travel_time"
    )
    return lengths


def compute_accessibility_optimized(graph, population_gdf, hospital_gdf):
    """
    Main optimized accessibility pipeline
    """

    # 1. Map hospitals to graph nodes
    hospital_nodes = set(map_points_to_nodes(graph, hospital_gdf))

    # 2. Map population zones to graph nodes
    pop_nodes = map_points_to_nodes(graph, population_gdf)

    # 3. Run ONE multi-source Dijkstra
    shortest_times = multi_source_dijkstra(graph, hospital_nodes)

    # 4. Assign travel times to population zones
    travel_times = []
    underserved = []

    for node in pop_nodes:
        time = shortest_times.get(node, np.inf)
        travel_times.append(time)
        underserved.append(time > TRAVEL_TIME_THRESHOLD)

    population_gdf["travel_time_sec"] = travel_times
    population_gdf["underserved"] = underserved

    return population_gdf

print(nx.__version__)

nx.multi_source_dijkstra_path_length(
    graph,
    hospital_nodes,
    cutoff=TRAVEL_TIME_THRESHOLD,
    weight="travel_time"
)