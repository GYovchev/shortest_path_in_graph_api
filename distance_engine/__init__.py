from threading import Lock
import logging
from flask import current_app

from .exception import BadGraphDictionaryData, NodeDoesntExist
from .graph import Graph


class DistanceEngine():
    """`DistanceEngine` is thread-safe class that allows you to do fast shortest path calculations in graph.
        It precomputes all shortest distances after graph is updated and when we call `get_distance` it
        returns result from the cache."""
    __graph: Graph = Graph({}, False, [], [])
    __distances: dict = {}
    __graph_access_lock = Lock()

    def set_graph(self, graph: Graph):
        distances = graph.calculate_distances()
        self.__graph_access_lock.acquire()
        try:
            self.__graph = graph
            self.__distances = distances
            return self.__graph
        finally:
            self.__graph_access_lock.release()

    def set_graph_from_dict(self, graph_data: dict):
        """
        Takes graph data as dictionary and updates `DistanceEngine`'s `__graph` and `__distances` fields in a thread-safe way
        """
        graph = Graph.create_graph_from_dict(graph_data)
        distances = graph.calculate_distances()
        self.__graph_access_lock.acquire()
        try:
            self.__graph = graph
            self.__distances = distances
            return self.__graph
        finally:
            self.__graph_access_lock.release()
            current_app.logger.info("asdasdsa")

    def get_distance(self, node_a: str, node_b: str):
        self.__graph_access_lock.acquire()
        try:
            if not self.__graph.does_node_exists(node_a):
                raise NodeDoesntExist(node_a)
            if not self.__graph.does_node_exists(node_b):
                raise NodeDoesntExist(node_b)
            result = self.__distances[node_a][node_b]
            return result
        finally:
            self.__graph_access_lock.release()
