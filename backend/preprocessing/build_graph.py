import osmnx as ox
import networkx as nx

def build_road_graph(place_name):
    """
    Downloads road network and converts to NetworkX graph
    """
    graph = ox.graph_from_place(place_name, network_type="drive")
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)
    return graph

def save_graph(graph, path):
    nx.write_graphml(graph, path)