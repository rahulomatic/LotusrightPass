import numpy as np
import networkx as nx
import osmnx as ox
import heapq


def multi_source_dijkstra(graph, sources, weight="travel_time", cutoff=None):
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


def evaluate_facility_set(graph, demand_nodes, facility_nodes):
    """
    Computes average travel time from demand nodes
    to nearest facility
    """
    distances = multi_source_dijkstra(
        graph,
        facility_nodes,
        cutoff=None
    )

    times = [
        distances.get(node, float("inf"))
        for node in demand_nodes
    ]

    return np.mean(times)


def p_median_heuristic(
    graph,
    demand_nodes,
    candidate_nodes,
    p=2
):
    """
    Greedy p-median heuristic:
    Iteratively pick facility that gives best improvement
    """

    selected = []

    for _ in range(p):
        best_node = None
        best_score = float("inf")

        for candidate in candidate_nodes:
            if candidate in selected:
                continue

            score = evaluate_facility_set(
                graph,
                demand_nodes,
                selected + [candidate]
            )

            if score < best_score:
                best_score = score
                best_node = candidate

        selected.append(best_node)

    return selected, best_score