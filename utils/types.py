from enum import Enum


class ObjectType(Enum):
    DOT = 1
    LINE = 2
    POLYGON = 3
    CURVE = 4
    CURVE_BSPLINE = 5
    POLYGON_3D = 6
    SURFACE_BEZIER = 7
    SURFACE_BSPLINE = 8
    SURFACE_BSPLINE_FD = 9