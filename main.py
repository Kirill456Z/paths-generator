from road_network.network_db import NetworkDB
from road_network.base_classes import Point, BBox

if __name__ == "__main__":
    '''
    pg = PathGenerator(Point(lat=51.520691, lon=-0.098027))
    pg.generate_path(100)
    print(jsonify(pg.cur_path.points))
    #pg.plot_path()
    '''
    db = NetworkDB()
    # nodes = db.get_tile(Point(lng=37.505283, lat=55.924823))
    # print(nodes)
