from typing import List, Tuple
from PyQt6.QtGui import QColor
from utils.types import ObjectType

class Wireframe:
    def __init__(
        self, name: str, obj_type: ObjectType, coordinates: List[Tuple[float, float]]
    ):
        self.name = name
        self.obj_type = obj_type
        self.coordinates = coordinates
        self.color = QColor("black")  # Default color
        self.is_selected = False

    def set_color(self, color: QColor):
        self.color = color

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False