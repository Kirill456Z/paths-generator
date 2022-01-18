from road_network.road_network import RoadNetwork
from road_network.base_classes import Point, Path, Node
from random import choice
from matplotlib import collections
import matplotlib.pyplot as plt

QUERY_FSTR = """  way{}["highway"];
            (._;>;);
            out body; """


class PathGenerator:
    road_net: RoadNetwork
    cur_node: Node
    cur_path: Path
    turns_counter: int = 0

    def __init__(self):
        self.cur_path = Path()
        self.road_net = RoadNetwork()

    def generate_path(self, nodes_count: int, start: Point):
        self.cur_path = Path()
        self.cur_node = self.road_net.get_nearest_node(start)[1]
        visited_points = set()
        for i in range(nodes_count):
            not_visited_neighbors = [n for n in self.cur_node.neighbors if
                                     n.to_node_id not in visited_points]
            if len(not_visited_neighbors) == 0:
                not_visited_neighbors = self.cur_node.neighbors
            edge = choice(not_visited_neighbors)
            self.cur_node = self.road_net.get(edge.to_node_id, edge.path.points[-1])
            visited_points.add(edge.to_node_id)
            # self.plot_animated(edge.path)
            self.cur_path += edge.path

    def plot_animated(self, added_path):
        if self.turns_counter == 0:
            self.fig, self.ax = plt.subplots(figsize=(6, 6))
            self.road_net.plot_network(self.ax)
            self.cur_p = plt.scatter(self.cur_node.lng, self.cur_node.lat, color='red', s=4, zorder=100)
        segments = []
        for from_p, to_p in zip(added_path.points, added_path.points[1:]):
            segments.append([(from_p.lng, from_p.lat), (to_p.lng, to_p.lat)])
        lc = collections.LineCollection(segments, colors='#BD7B20', linewidths=1, linestyles='dashed')
        self.cur_p.remove()
        self.cur_p = plt.scatter(self.cur_node.lng, self.cur_node.lat, color='red', s=2, zorder=100)
        self.ax.add_collection(lc)
        plt.savefig("plot/network_plot{}.png".format(self.turns_counter), format="png")
        self.turns_counter += 1

    def plot_path(self):
        fig, ax = plt.subplots(figsize=(15, 15))
        self.road_net.plot_network(ax)
        segments = []
        for from_p, to_p in zip(self.cur_path.points, self.cur_path.points[1:]):
            segments.append([(from_p.lng, from_p.lat), (to_p.lng, to_p.lat)])
        lc = collections.LineCollection(segments, colors='#BD7B20', linewidths=1, linestyles='dashed')
        ax.add_collection(lc)
        plt.scatter(self.cur_node.lng, self.cur_node.lat, color='red', s=10, zorder=100)
        plt.xlim(self.bounding_box[1], self.bounding_box[3])
        plt.ylim(self.bounding_box[0], self.bounding_box[2])
        plt.savefig("network_plot.png", format="png")
