from math import radians, cos, sin, acos

from nodes_fetcher import Node


class DistanceCalculator:

    @staticmethod
    def great_distance_calc(node_one: Node, node_two: Node):
        slon = radians(node_one.latitude)
        slat = radians(node_one.longitude)
        elon = radians(node_two.latitude)
        elat = radians(node_two.longitude)

        dist = 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))

        return dist
