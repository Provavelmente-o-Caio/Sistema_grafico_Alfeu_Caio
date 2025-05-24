from locale import normalize
from utils.transformations import create_coord_transform_matrix
import numpy as np


class Window:
    def __init__(
        self, xmin: int = -10, ymin: int = -10, xmax: int = 10, ymax: int = 10
    ):
        self.xmin: int = xmin
        self.ymin: int = ymin
        self.xmax: int = xmax
        self.ymax: int = ymax
        self.rotation_angle: float = 0

    def width(self) -> int:
        return self.xmax - self.xmin

    def height(self) -> int:
        return self.ymax - self.ymin

    def center(self) -> tuple[float, float]:
        return (self.xmin + self.xmax) / 2, (self.ymin + self.ymax) / 2

    def get_transformation_matrix(self):
        return create_coord_transform_matrix(0, 0, self.rotation_angle, 1.0, 1.0)

    def pan(self, dx, dy) -> None:
        """
        Pan the window
        """

        dx_norm = dx / (self.xmax - self.xmin)
        dy_norm = dy / (self.ymax - self.ymin)

        angle_rad = np.deg2rad(self.rotation_angle)
        adjusted_dx = dx_norm * np.cos(angle_rad) - dy_norm * np.sin(angle_rad)
        adjusted_dy = dx_norm * np.sin(angle_rad) + dy_norm * np.cos(angle_rad)

        dx_world = adjusted_dx * (self.xmax - self.xmin)
        dy_world = adjusted_dy * (self.ymax - self.ymin)

        self.xmin += dx_world
        self.xmax += dx_world
        self.ymin += dy_world
        self.ymax += dy_world

    def zoom(self, factor):
        """
        Zoom the window (centered zoom)
        """

        # Calculate center point
        xcenter, ycenter = self.center()

        # Calculate new width and height
        new_width = self.width() * factor
        new_height = self.height() * factor

        # Set new boundaries
        self.xmin = xcenter - new_width / 2
        self.xmax = xcenter + new_width / 2
        self.ymin = ycenter - new_height / 2
        self.ymax = ycenter + new_height / 2

    def rotate(self, angle: float):
        self.rotation_angle = (self.rotation_angle + angle) % 360

    def world_to_normalized(self, xw: float, yw: float) -> tuple[float, float]:
        """
        Converts from World Coordinates to Normalized Device Coordinates
        """

        xn = (2.0 * (xw - self.xmin) / (self.xmax - self.xmin)) - 1.0
        yn = (2.0 * (yw - self.ymin) / (self.ymax - self.ymin)) - 1.0
        return xn, yn

    def normalized_to_world(self, xn: float, yn: float)-> tuple[float, float]:
        """
        Converts from Normalized Device Coordinates to World Coordinates
        """

        xw = self.xmin + ((xn + 1.0) * (self.xmax - self.xmin)) / 2.0
        yw = self.ymin + ((yn + 1.0) * (self.ymax - self.ymin)) / 2.0
        return xw, yw
