import itertools
from math import radians, cos, sin, acos

from links import Graph
from nodes_fetcher import Node, NodeHandler


class LinkCreator:

    @staticmethod
    def great_distance_calc(node_one: Node, node_two: Node):
        slon = radians(node_one.latitude)
        slat = radians(node_one.longitude)
        elon = radians(node_two.latitude)
        elat = radians(node_two.longitude)

        dist = 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))

        return dist

    def __init__(self):
        self.node_handler = NodeHandler()
        honest_miners, dishonest_miners, relays = self.node_handler.get_selected_nodes()

        self.all_nodes = honest_miners + dishonest_miners + relays
        self.miners = honest_miners + dishonest_miners
        self.total_links = 0
        self.graph = None

    def create_links(self):
        combinations = list(itertools.combinations(self.all_nodes, 2))

        d = 1500
        graph = Graph()

        len_graph = 0
        while (not graph.is_connected() or d < 4000 or len_graph < 10):
            graph = Graph()
            graph.add_extra_relays(self.node_handler.get_extra_relays())
            for node1, node2 in combinations:
                distance_calc = self.great_distance_calc(node1, node2)
                if distance_calc <= d:
                    graph.add_edge(node1, node2, distance_calc)
            d *= 1.2
            len_graph = len(graph.graph)
            self.caculate_total_links(graph)

        self.graph = graph
        return graph

    def caculate_total_links(self, graph):
        total_links = 0
        for _, values in graph.graph.items():
            total_links += len(values)
        self.total_links = total_links

    def create_routes(self):
        graph = self.create_links()
        distances = dict(dict())
        for start in self.miners:
            # for start in self.all_nodes:
            dist = {}
            for end in self.all_nodes:
                dist = {**dist, **graph.dijkstra(start, end)}
            distances[start] = dist
        return distances
        # graph.printSolution(start, dist)

    def print_total_links(self):
        print("Links:", self.total_links)


if __name__ == '__main__':
    creator = LinkCreator()
    # creator.create_links()

    # iter = graph.__iter__()
    # start = next(iter)
    # end = next(iter)
    # nodes_distance, _ = graph.Dijkstra(graph, start, end)
    # for node, x in nodes_distance.items():
    #     print(str(node) + " " + str(x))

    routes = creator.create_routes()
    graph = creator.graph

    for start, dist in routes.items():
        graph.printSolution(start, dist)
    creator.print_total_links()
