import neighbors as neighbors

from road_network.road_network import RoadNetwork
from road_network.base_classes import Point, Path
from api_buffer import ApiBuffer
from random import choice
from matplotlib import collections
import matplotlib.pyplot as plt

QUERY_FSTR = """  way{}["highway"];
            (._;>;);
            out body; """


class PathGenerator:
    bb_size: float = 0.01
    road_net: RoadNetwork
    cur_node: RoadNetwork.Node
    cur_path: Path
    turns_counter: int = 0

    def __init__(self, point: Point):
        self.cur_path = Path()
        self.bounding_box = (point.lat - self.bb_size, point.lon - self.bb_size,
                             point.lat + self.bb_size, point.lon + self.bb_size)
        query = QUERY_FSTR.format(self.bounding_box)
        api_buf = ApiBuffer()
        api_buf.make_query(query)
        res = api_buf.get_last_query()
        self.road_net = RoadNetwork(res)
        # self.road_net.plot_network()
        self.cur_node = self.road_net.get_nearest_node(point)[1]

    def generate_path(self, nodes_count):
        visited_points = set()
        for i in range(nodes_count):
            not_visited_neighbors = [n for n in self.cur_node.neighbors if
                                     Point(n.to_node).to_tuple() not in visited_points]
            if len(not_visited_neighbors) == 0:
                return
            edge = choice(not_visited_neighbors)
            self.cur_node = edge.to_node
            visited_points.add(Point(self.cur_node).to_tuple())
            # self.plot_animated(edge.path)
            self.cur_path += edge.path

    def plot_animated(self, added_path):
        if self.turns_counter == 0:
            self.fig, self.ax = plt.subplots(figsize=(6, 6))
            self.road_net.plot_network(self.ax)
            self.cur_p = plt.scatter(self.cur_node.lon, self.cur_node.lat, color='red', s=4, zorder=100)
        segments = []
        for from_p, to_p in zip(added_path.points, added_path.points[1:]):
            segments.append([(from_p.lon, from_p.lat), (to_p.lon, to_p.lat)])
        lc = collections.LineCollection(segments, colors='#BD7B20', linewidths=1, linestyles='dashed')
        self.cur_p.remove()
        self.cur_p = plt.scatter(self.cur_node.lon, self.cur_node.lat, color='red', s=2, zorder=100)
        self.ax.add_collection(lc)
        plt.savefig("plot/network_plot{}.png".format(self.turns_counter), format="png")
        self.turns_counter += 1

    def plot_path(self):
        fig, ax = plt.subplots(figsize=(15, 15))
        self.road_net.plot_network(ax)
        segments = []
        for from_p, to_p in zip(self.cur_path.points, self.cur_path.points[1:]):
            segments.append([(from_p.lon, from_p.lat), (to_p.lon, to_p.lat)])
        lc = collections.LineCollection(segments, colors='#BD7B20', linewidths=1, linestyles='dashed')
        ax.add_collection(lc)
        plt.scatter(self.cur_node.lon, self.cur_node.lat, color='red', s=10, zorder=100)
        plt.xlim(self.bounding_box[1], self.bounding_box[3])
        plt.ylim(self.bounding_box[0], self.bounding_box[2])
        plt.savefig("network_plot.png", format="png")
