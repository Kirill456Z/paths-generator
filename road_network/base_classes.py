from __future__ import annotations

import latest as latest
import overpy
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Point:
    lat: float = 0.0
    lon: float = 0.0

    def __str__(self):
        return "({},{})".format(self.lat, self.lon)

    def __init__(self, overpy_node: overpy.Node = None, lat=None, lon=None):
        if overpy_node is not None:
            self.lat = float(overpy_node.lat)
            self.lon = float(overpy_node.lon)
        else:
            self.lat = lat
            self.lon = lon

    def to_tuple(self):
        return self.lat, self.lon

    def dist(self, other: Point):
        dx = self.lat - other.lat
        dy = self.lon - other.lon
        return dx * dx + dy * dy


@dataclass
class Path:
    points: list[Point] = field(default_factory=list)

    def __iadd__(self, other: Path) -> Path:
        self.points += other.points
        return self
