import networkx as nx


class NetworkXGraphCreator:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_nodes(self, nodes):
        self.graph.add_nodes_from(nodes)

    def add_edges(self, edges):
        self.graph.add_edges_from(edges)

    def add_edge(self, node, friend):
        self.graph.add_edge(node, friend)

    def get_number_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_number_of_edges(self):
        return self.graph.number_of_edges()
