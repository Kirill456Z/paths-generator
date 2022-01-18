from road_network.base_classes import Point, Tile, BBox

MIN_LAT, MAX_LAT = -90.0, 90.0
MIN_LNG, MAX_LNG = -180.0, 180.0
LAT_SUBDIV, LNG_SUBDIV = 18000, 36000
LAT_TSIZE = (MAX_LAT - MIN_LAT) / LAT_SUBDIV
LNG_TSIZE = (MAX_LNG - MIN_LNG) / LNG_SUBDIV


def point_to_tile(point: Point) -> Tile:
    return Tile(int((point.lng - MIN_LNG) // LNG_TSIZE),
                int((point.lat - MIN_LAT) // LAT_TSIZE))


def tile_to_bbox(tile: Tile) -> BBox:
    return BBox(tile.y_coord * LAT_TSIZE + MIN_LAT, tile.x_coord * LNG_TSIZE + MIN_LNG,
                (tile.y_coord + 1) * LAT_TSIZE + MIN_LAT, (tile.x_coord + 1) * LNG_TSIZE + MIN_LNG)
