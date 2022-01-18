from road_network.base_classes import Point, Node, Edge, Path
from road_network.earth_subdivision import point_to_tile, tile_to_bbox
from pymongo import MongoClient, GEO2D
from pymongo.errors import ConnectionFailure
from road_network.overpass_query import make_query
import datetime
import os

USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")


class NetworkDB:

    def __init__(self):
        self.client = MongoClient("mongodb+srv://path-gen-cluster0.nvadu.mongodb.net/path-gen", username=USER,
                                  password=PASSWORD)
        try:
            self.client.admin.command('ping')
            self.db = self.client.path_gen
            print("Connected to database server")
        except ConnectionFailure:
            print("Server not available")
        pass

    def get_tile(self, point: Point):
        """ Returns nodes that are inside the tile containing given point """
        tile = point_to_tile(point)
        tiles_collection = self.db.stored_tiles
        doc = tiles_collection.find_one({'xcoord': tile.x_coord, 'ycoord': tile.y_coord})
        bbox = tile_to_bbox(tile)
        if doc is None:
            print("Tile containing given point is not stored in memory")
            nodes = make_query(bbox)
            new_tile = {'xcoord': tile.x_coord, 'ycoord': tile.y_coord, 'insertion_time': datetime.datetime.utcnow()}
            tiles_collection.insert_one(new_tile)
            data = []
            for node in nodes.values():
                neighbors = [{"to_node": neighbor.to_node_id, "path": [[p.lng, p.lat] for p in neighbor.path.points]}
                             for neighbor in node.neighbors]
                data.append({"_id": node.id, "loc": [node.lng, node.lat], "neighbors": neighbors})
            nodes_collection = self.db.nodes
            nodes_collection.create_index([("loc", GEO2D)])
            nodes_collection.insert_many(data)
            return nodes
        else:
            print("Data stored, trying to access")
            nodes_collection = self.db.nodes
            res = nodes_collection.find(
                {"loc": {"$geoWithin": {"$box": [[bbox.min_lng, bbox.min_lat], [bbox.max_lng, bbox.max_lat]]}}})
            # res = nodes_collection.find(query)
            nodes: dict[int, Node] = {}
            for node in res:
                new_node = Node(point=Point(node["loc"][0], node["loc"][1]), id=node["_id"])
                nodes[new_node.id] = new_node
                for neighbor_edge in node["neighbors"]:
                    path = Path([Point(loc[0], loc[1]) for loc in neighbor_edge["path"]])
                    new_node.neighbors.append(Edge(neighbor_edge["to_node"], path))
            return nodes
