from threading import Lock
from flask import current_app

from .exception import BadGraphDictionaryData, NodeDoesntExist, NoPathExists
from .graph import Graph


class DistanceEngine():
    """`DistanceEngine` is thread-safe class that allows you to do fast shortest path calculations in graph.
        It precomputes all shortest distances after graph is updated and when we call `get_distance` it
        returns result from the cache."""
    __graph: Graph = Graph({}, False, [], [])
    __distances: dict = {}
    __graph_access_lock = Lock()

    def set_graph_from_dict(self, graph_data: dict):
        """
        Takes graph data as a dictionary and updates the cache in a thread-safe way
        """
        current_app.logger.debug("Creating graph from dictionary")
        graph = Graph.create_graph_from_dict(graph_data)
        current_app.logger.debug("Calculating new cache distances between all node pairs")
        distances = graph.calculate_distances()
        with self.__graph_access_lock:
            self.__graph = graph
            self.__distances = distances
            return self.__graph

    def get_distance(self, node_a: str, node_b: str):
        """
        Calculates shortest path distance between two nodes of the graph.
        """
        with self.__graph_access_lock:
            if not self.__graph.does_node_exists(node_a):
                raise NodeDoesntExist(node_a)
            if not self.__graph.does_node_exists(node_b):
                raise NodeDoesntExist(node_b)
            current_app.logger.debug("Fetching distance between '{}' and '{}' from the cache".format(node_a, node_b))
            if node_b not in self.__distances[node_a]:
                raise NoPathExists(node_a, node_b)
            distance = self.__distances[node_a][node_b]
            return distance
