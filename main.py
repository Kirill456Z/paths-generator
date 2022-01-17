import pickle
import overpy
from road_network.road_network import RoadNetwork
from path_generator import PathGenerator
from road_network.base_classes import Point
from flask import jsonify

if __name__ == "__main__":
    pg = PathGenerator(Point(lat=51.520691, lon=-0.098027))
    pg.generate_path(100)
    print(jsonify(pg.cur_path.points))
    #pg.plot_path()
