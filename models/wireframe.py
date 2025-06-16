import numpy as np
from PyQt6.QtGui import QColor

from utils.transformations import (
    create_translation_matrix_2d,
    create_scale_matrix_2d,
    create_rotation_matrix_2d,
)
from utils.types import ObjectType


class Wireframe:
    def __init__(
        self,
        name: str,
        obj_type: ObjectType,
        coordinates: list[tuple[int, int]],
        fill: bool = False,
    ):
        self.name: str = name
        self.obj_type: ObjectType = obj_type
        self.coordinates: list[tuple[int, int]] = coordinates
        self.color: QColor = QColor("black")
        self.is_selected: bool = False
        self.fill: bool = fill

    def set_fill(self, fill: bool) -> None:
        self.fill = fill

    def set_color(self, color: QColor) -> None:
        self.color = color

    def select(self) -> None:
        self.is_selected = True

    def deselect(self) -> None:
        self.is_selected = False

    def translate(self, dx: float, dy: float) -> None:
        T = create_translation_matrix_2d(dx, dy)
        self.transformation(op=T)

    def transform(self, sx: float, sy: float) -> None:
        S = create_scale_matrix_2d(sx, sy)
        self.transformation(op=S)

    def rotate(self, angle: float) -> None:
        R = create_rotation_matrix_2d(angle)
        self.transformation(op=R)

    def transformation(self, obj=None, op=None) -> None:
        new_coords = []
        for x, y in self.coordinates:
            point = np.matrix([x, y, 1])
            transformed_point = point @ op
            new_coords.append(
                (float(transformed_point[0, 0]), float(transformed_point[0, 1]))
            )
        self.coordinates = new_coords

    def get_center_object_x(self) -> float:
        if not self.coordinates:
            return 0

        sum_x = 0
        for x, _ in self.coordinates:
            sum_x += x
        return sum_x / len(self.coordinates)

    def get_center_object_y(self) -> float:
        if not self.coordinates:
            return 0

        sum_y = 0
        for _, y in self.coordinates:
            sum_y += y
        return sum_y / len(self.coordinates)

    def export_coordinates(self) -> list[tuple[int, int]]:
        return self.coordinates

    def get_name(self) -> str:
        return self.name

    def get_color(self) -> str:
        return self.color.name()

    def get_obj_type(self) -> ObjectType:
        return self.obj_type
