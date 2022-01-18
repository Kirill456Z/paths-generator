from __future__ import annotations
from matplotlib import collections
from road_network.base_classes import Point, Node, Tile
from road_network.earth_subdivision import point_to_tile
from road_network.network_db import NetworkDB


class RoadNetwork:
    nodes: dict[int, Node]
    loaded_tiles: set[Tile]
    network_db: NetworkDB = NetworkDB()

    def __init__(self):
        self.loaded_tiles = set()
        self.nodes = {}

    def get(self, node_id: int, loc: Point):
        if node_id not in self.nodes:
            self.nodes.update(self.network_db.get_tile(loc))
        return self.nodes[node_id]

    def get_nearest_node(self, target: Point) -> tuple[float, Node]:
        tile = point_to_tile(target)
        if tile not in self.loaded_tiles:
            self.nodes.update(self.network_db.get_tile(target))
        self.loaded_tiles.add(tile)
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
            nodes_x.append(node.lng)
            nodes_y.append(node.lat)
            for edge in node.neighbors:
                for (from_p, to_p) in zip(edge.path.points, edge.path.points[1:]):
                    segments.append([(from_p.lng, from_p.lat), (to_p.lng, to_p.lat)])
        lc = collections.LineCollection(segments, linewidths=2, colors='#5490E3')
        ax.add_collection(lc)
        # ax.autoscale()
        ax.scatter(nodes_x, nodes_y, c='#265BA6', s=6)
        # plt.savefig("network_plot.png", format="png")
        return ax
