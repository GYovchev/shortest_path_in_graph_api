from typing import List

import networkx as nx

from .edge import Edge, EdgeAttributes
from .exception import NodeDoesntExist, BadGraphDictionaryData
from .node import Node


class Graph:
    metadata: dict = {}
    directed: bool = False
    nodes: List[Node] = []
    edges: List[Edge] = []
    nx_graph: nx.Graph = nx.Graph()

    def __init__(self, metadata: dict, directed: bool, nodes: List[Node], edges: List[Edge]):
        self.metadata = metadata
        self.directed = directed
        self.nodes = nodes
        self.edges = edges
        self.nx_graph = nx.DiGraph() if directed else nx.Graph()

        node_ids = [node.id for node in nodes]
        self.nx_graph.add_nodes_from(node_ids)

        for edge in edges:
            if edge.source not in self.nx_graph.nodes:
                raise NodeDoesntExist(edge.source)
            if edge.target not in self.nx_graph.nodes:
                raise NodeDoesntExist(edge.target)

        nx_edges_list = list(map(lambda e: (e.source, e.target, e.attributes.weight), edges))
        self.nx_graph.add_weighted_edges_from(nx_edges_list)

    def calculate_distances(self):
        return dict(nx.all_pairs_dijkstra_path_length(self.nx_graph))

    def does_node_exists(self, node: str):
        return self.nx_graph.has_node(node)

    def to_dictionary(self):
        return {
            "directed": self.directed,
            "graph": self.metadata,
            "links": [edge.to_dictionary() for edge in self.edges],
            "nodes": [node.to_dictionary() for node in self.nodes],
        }

    @staticmethod
    def create_graph_from_dict(graph_data: dict):
        """Creates graph object from a valid dictionary"""
        Graph.run_validation_checks_on_graph_data(graph_data)

        metadata = {}
        directed = False
        nodes = []
        edges = []

        if "directed" in graph_data and graph_data["directed"] is True:
            directed = True
        if "graph" in graph_data:
            metadata = graph_data["graph"]
        for node in graph_data["nodes"]:
            nodes.append(Node(node["id"]))
        if "links" in graph_data:
            edges = list(map(lambda l: Edge(l["source"], l["target"], EdgeAttributes(l["attributes"]["weight"])), graph_data["links"]))
        graph = Graph(metadata, directed, nodes, edges)
        return graph

    @staticmethod
    def run_validation_checks_on_graph_data(graph_data: dict):
        if "graph" not in graph_data:
            raise BadGraphDictionaryData("'graph' property is missing.")
        if "name" not in graph_data["graph"]:
            raise BadGraphDictionaryData("'nodes[graph]' should have a property 'name' of type string.")
        if "version" not in graph_data["graph"]:
            raise BadGraphDictionaryData("'nodes[graph]' should have a property 'version' of type number.")

        if not "nodes" in graph_data:
            raise BadGraphDictionaryData("'nodes' property is missing.")
        if not isinstance(graph_data["nodes"], list):
            raise BadGraphDictionaryData("'nodes' property should be an array.")
        for i, node in enumerate(graph_data["nodes"]):
            if "id" not in node or not isinstance(node["id"], str):
                raise BadGraphDictionaryData("'nodes[{}]' should have a property 'id' of type string.".format(i))

        if "links" in graph_data:
            if not isinstance(graph_data["links"], list):
                raise BadGraphDictionaryData("'links' property should be an array.")
            for i, link in enumerate(graph_data["links"]):
                if "source" not in link or not isinstance(link["source"], str):
                    raise BadGraphDictionaryData(
                        "'links[{}]' should have a property 'source' of type string.".format(i))
                if "target" not in link or not isinstance(link["target"], str):
                    raise BadGraphDictionaryData(
                        "'links[{}]' should have a property 'target' of type string.".format(i))
                if "attributes" not in link or not isinstance(link["attributes"], dict):
                    raise BadGraphDictionaryData(
                        "'links[{}]' should have an object property 'attributes'.".format(i))
                if "weight" not in link["attributes"] or not isinstance(link["attributes"]["weight"], (int, float)):
                    raise BadGraphDictionaryData(
                        "'links[{}][attributes]' should have a property 'weight' of type float.".format(i))
