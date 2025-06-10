from models.point_3d import Point3D
from utils.types import ObjectType


class Wireframe_3D:
    def __init__(
        self,
        name: str,
        obj_type: ObjectType,
        points: list[Point3D],
        edges: list[tuple[int, int]],
        fill: bool = False,
    ):
        self.name: str = name
        self.obj_type: ObjectType = obj_type
        self.points: list[Point3D] = points
        self.color: str = "black"
        self.is_selected: bool = False
        self.fill: bool = fill
        self.edges: list[tuple[int, int]] = edges

    def set_fill(self, fill: bool) -> None:
        self.fill = fill

    def set_color(self, color: str) -> None:
        self.color = color

    def select(self) -> None:
        self.is_selected = True

    def deselect(self) -> None:
        self.is_selected = False

    def translate(self, dx: float, dy: float, dz: float) -> None:
        for point in self.points:
            point.translate(dx, dy, dz)

    def transform(self, sx: float, sy: float, sz: float) -> None:
        for point in self.points:
            point.transform(sx, sy, sz)

    def rotate_x(self, angle: float) -> None:
        for point in self.points:
            point.rotate_x(angle)

    def rotate_y(self, angle: float) -> None:
        for point in self.points:
            point.rotate_y(angle)

    def rotate_z(self, angle: float) -> None:
        for point in self.points:
            point.rotate_z(angle)

    def get_center_object_x(self) -> float:
        if not self.points:
            return 0
        sum_x = 0
        for point in self.points:
            sum_x += point.coordinates[0][0]
        return sum_x / len(self.points)

    def get_center_object_y(self) -> float:
        if not self.points:
            return 0
        sum_y = 0
        for point in self.points:
            sum_y += point.coordinates[0][1]
        return sum_y / len(self.points)

    def get_center_object_z(self) -> float:
        if not self.points:
            return 0
        sum_z = 0
        for point in self.points:
            sum_z += point.coordinates[0][2]
        return sum_z / len(self.points)

    def export_coordinates(self) -> list[tuple[int, int, int]]:
        return [point.coordinates[0] for point in self.points]

    def get_name(self) -> str:
        return self.name

    def get_color(self) -> str:
        return self.color

    def get_obj_type(self) -> ObjectType:
        return self.obj_type

    def get_edges(self) -> list[tuple[int, int]]:
        return self.edges
