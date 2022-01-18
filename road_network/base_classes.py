from __future__ import annotations
import overpy
from dataclasses import dataclass, field, astuple


@dataclass
class Point:
    lng: float
    lat: float

    def __str__(self):
        return str(astuple(self))

    def __init__(self, lng=None, lat=None):
        self.lng = lng
        self.lat = lat

    def dist(self, other: Point):
        dx = self.lat - other.lat
        dy = self.lng - other.lng
        return dx * dx + dy * dy


@dataclass
class Path:
    points: list[Point] = field(default_factory=list)

    def __iadd__(self, other: Path) -> Path:
        self.points += other.points
        return self


@dataclass(frozen=True)
class Tile:
    x_coord: int
    y_coord: int


@dataclass
class BBox:
    min_lat: float
    min_lng: float
    max_lat: float
    max_lng: float

    def __str__(self):
        return str(astuple(self))

    def is_inside(self, point: Point):
        return self.min_lng <= point.lng < self.max_lng and self.min_lat <= point.lat < self.max_lat


@dataclass
class Edge:
    to_node_id: int
    path: Path


@dataclass
class Node(Point):
    id: int
    neighbors: list[Edge] = field(default_factory=list)

    def __init__(self, overpy_node: overpy.Node = None, point: Point = None, id: int = None):
        if overpy_node is not None:
            super().__init__(float(overpy_node.lon), float(overpy_node.lat))
            self.id = overpy_node.id
            self.neighbors = []
        else:
            super().__init__(point.lng, point.lat)
            self.id = id
            self.neighbors = []
