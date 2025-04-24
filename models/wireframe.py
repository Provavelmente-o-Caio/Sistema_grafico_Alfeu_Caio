from typing import List, Tuple

import numpy as np
from PyQt6.QtGui import QColor

from utils.types import ObjectType


def create_translation_matrix(dx, dy):
    return np.matrix([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])


def create_scale_matrix(sx, sy):
    return np.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])


def create_rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.matrix(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )


class Wireframe:
    def __init__(
        self, name: str, obj_type: ObjectType, coordinates: List[Tuple[float, float]]
    ):
        self.name = name
        self.obj_type = obj_type
        self.coordinates = coordinates  # wc coordinates
        self.scn_coordinates = []
        self.color = QColor("black")
        self.is_selected = False

    def set_color(self, color: QColor):
        self.color = color

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def translate(self, dx: float, dy: float):
        T = create_translation_matrix(dx, dy)
        new_coords = []
        for x, y in self.coordinates:
            point = np.matrix([x, y, 1])
            transformed_point = point * T
            new_coords.append(
                (float(transformed_point[0, 0]), float(transformed_point[0, 1]))
            )
        self.coordinates = new_coords

    def transform(self, sx: float, sy: float):
        S = create_scale_matrix(sx, sy)
        new_coords = []
        for x, y in self.coordinates:
            point = np.matrix([x, y, 1])
            transformed_point = point * S
            new_coords.append(
                (float(transformed_point[0, 0]), float(transformed_point[0, 1]))
            )
        self.coordinates = new_coords

    def rotate(self, angle: float):
        R = create_rotation_matrix(angle)
        new_coords = []
        for x, y in self.coordinates:
            point = np.matrix([x, y, 1])
            transformed_point = point * R
            new_coords.append(
                (float(transformed_point[0, 0]), float(transformed_point[0, 1]))
            )
        self.coordinates = new_coords

    def getCenterObjectX(self):
        if not self.coordinates:
            return 0

        sum_x = 0
        for x, _ in self.coordinates:
            sum_x += x
        return sum_x / len(self.coordinates)

    def getCenterObjectY(self):
        if not self.coordinates:
            return 0

        sum_y = 0
        for _, y in self.coordinates:
            sum_y += y
        return sum_y / len(self.coordinates)
