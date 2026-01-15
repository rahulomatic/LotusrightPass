import geopandas as gpd
import networkx as nx
import osmnx as ox
import numpy as np
import heapq

TRAVEL_TIME_THRESHOLD = 10 * 60  # 30 minutes


def map_points_to_nodes(graph, gdf):
    """Map GeoDataFrame points to nearest graph nodes"""
    return ox.nearest_nodes(
        graph,
        X=gdf.geometry.x,
        Y=gdf.geometry.y
    )


def multi_source_dijkstra_fallback(graph, sources, weight="travel_time", cutoff=None):
    """Multi-source Dijkstra (safe for all NetworkX versions)"""
    dist = {}
    pq = []

    for s in sources:
        dist[s] = 0
        heapq.heappush(pq, (0, s))

    while pq:
        cur_dist, u = heapq.heappop(pq)

        if cutoff and cur_dist > cutoff:
            continue
        if cur_dist > dist.get(u, float("inf")):
            continue

        for v, edge_data in graph[u].items():
            for _, attr in edge_data.items():
                w = attr.get(weight, 1)
                new_dist = cur_dist + w

                if new_dist < dist.get(v, float("inf")):
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))

    return dist


def compute_accessibility_optimized(graph, population_gdf, hospital_gdf):
    """Optimized accessibility analysis"""

    hospital_nodes = set(map_points_to_nodes(graph, hospital_gdf))
    pop_nodes = map_points_to_nodes(graph, population_gdf)

    shortest_times = multi_source_dijkstra_fallback(
        graph,
        hospital_nodes,
        cutoff=TRAVEL_TIME_THRESHOLD
    )

    population_gdf["travel_time_sec"] = [
        shortest_times.get(node, np.inf) for node in pop_nodes
    ]
    population_gdf["travel_time_min"] = population_gdf["travel_time_sec"] / 60
    population_gdf["underserved"] = (
        population_gdf["travel_time_sec"] > TRAVEL_TIME_THRESHOLD
    )

    return population_gdf