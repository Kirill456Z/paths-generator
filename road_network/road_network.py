from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib import collections
from road_network.base_classes import Point, Path
from dataclasses import dataclass, field
import overpy


class RoadNetwork:
    @dataclass
    class Edge:
        to_node: RoadNetwork.Node
        path: Path

    @dataclass
    class Node(Point):
        neighbors: list[RoadNetwork.Edge] = field(default_factory=list)

        def __init__(self, overpy_node: overpy.Node):
            super().__init__(overpy_node)
            self.neighbors = []

    nodes: dict[int, Node]

    def __init__(self, query_res: overpy.Result):
        self.nodes = {}
        node_to_way = {}
        for way in query_res.get_ways():
            for node in way.get_nodes():
                node_to_way.setdefault(node.id, list())
                node_to_way[node.id].append(way.id)
        for way in query_res.get_ways():
            cur_path = Path()
            last_node = None
            for i, node in enumerate(way.get_nodes()):
                cur_path.points.append(Point(node))
                if len(node_to_way[node.id]) > 1 or i == 0 or i == len(way.get_nodes()) - 1:
                    cur_node = self.nodes.setdefault(node.id, self.Node(node))
                    if last_node is not None:
                        last_node.neighbors.append(self.Edge(cur_node, cur_path))
                        cur_node.neighbors.append(self.Edge(last_node, Path(cur_path.points[::-1])))
                        cur_path = Path([cur_node])
                    last_node = cur_node

    def get_nearest_node(self, target: Point) -> tuple[float, Node]:
        min_dist = float("+inf")
        nearest_node = None
        for node in self.nodes.values():
            cur_dist = target.dist(node)
            if cur_dist < min_dist:
                min_dist = cur_dist
                nearest_node = node
        return min_dist, nearest_node

    def plot_network(self, ax):
        # fig, ax = plt.subplots()
        nodes_x = []
        nodes_y = []
        segments = []
        for node in self.nodes.values():
            nodes_x.append(node.lon)
            nodes_y.append(node.lat)
            for edge in node.neighbors:
                for (from_p, to_p) in zip(edge.path.points, edge.path.points[1:]):
                    segments.append([(from_p.lon, from_p.lat), (to_p.lon, to_p.lat)])
        lc = collections.LineCollection(segments, linewidths=2, colors='#5490E3')
        ax.add_collection(lc)
        # ax.autoscale()
        ax.scatter(nodes_x, nodes_y, c='#265BA6', s=6)
        # plt.savefig("network_plot.png", format="png")
        return ax
