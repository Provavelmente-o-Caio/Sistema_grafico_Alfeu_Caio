import numpy as np

from utils.transformations import create_coord_transform_matrix_3d, create_translation_matrix_3d, create_rotation_matrix_3dx, create_rotation_matrix_3dy, create_perspective_matrix

class Window:
    def __init__(
        self,
        xmin: int = -10,
        ymin: int = -10,
        xmax: int = 10,
        ymax: int = 10,
        zmax: int = 10,
        zmin: int = -10,
    ):
        self.__xmin: int = xmin
        self.__ymin: int = ymin
        self.__xmax: int = xmax
        self.__ymax: int = ymax
        self.__zmax: int = zmax
        self.__zmin: int = zmin
        self.__x_rotation_angle: float = 0
        self.__y_rotation_angle: float = 0
        self.__z_rotation_angle: float = 0

    def width(self) -> int:
        """
        Returns the width of the window
        """

        return self.__xmax - self.__xmin

    def height(self) -> int:
        """
        Returns the height of the window
        """

        return self.__ymax - self.__ymin

    def depth(self) -> int:
        """
        Returns the depth of the window
        """

        return self.__zmax - self.__zmin

    def center(self) -> tuple[float, float, float]:
        """
        Returns the center point of the window
        """

        return (self.__xmin + self.__xmax) / 2, (self.__ymin + self.__ymax) / 2, (self.__zmin + self.__zmax) / 2

    def get_transformation_matrix(self):
        """
        Returns the transformation matrix for the window
        """

        return create_coord_transform_matrix_3d(0, 0, 0, 0, 0, self.__z_rotation_angle, 1.0, 1.0, 1.0)

    def pan(self, dx, dy, dz) -> None:
        """
        Pan the window
        """

        dx_norm = dx / (self.__xmax - self.__xmin)
        dy_norm = dy / (self.__ymax - self.__ymin)
        dz_norm = dz / (self.__zmax - self.__zmin)

        angle_rad = np.deg2rad(self.__z_rotation_angle)
        adjusted_dx = dx_norm * np.cos(angle_rad) - dy_norm * np.sin(angle_rad)
        adjusted_dy = dx_norm * np.sin(angle_rad) + dy_norm * np.cos(angle_rad)
        adjusted_dz = dz_norm

        dx_world = adjusted_dx * (self.__xmax - self.__xmin)
        dy_world = adjusted_dy * (self.__ymax - self.__ymin)
        dz_world = adjusted_dz * (self.__zmax - self.__zmin)

        self.__xmin += dx_world
        self.__xmax += dx_world
        self.__ymin += dy_world
        self.__ymax += dy_world
        self.__zmin += dz_world
        self.__zmax += dz_world

    def zoom(self, factor) -> None:
        """
        Zoom the window (centered zoom)
        """

        # Calculate center point
        xcenter, ycenter, zcenter = self.center()

        # Calculate new width and height
        new_width = self.width() * factor
        new_height = self.height() * factor
        new_depth = self.depth() * factor

        # Set new boundaries
        self.__xmin = xcenter - new_width / 2
        self.__xmax = xcenter + new_width / 2
        self.__ymin = ycenter - new_height / 2
        self.__ymax = ycenter + new_height / 2
        self.__zmin = zcenter - new_depth / 2
        self.__zmax = zcenter + new_depth / 2

    def rotate_x(self, angle: float) -> None:
        """
        Rotates the window x angle by the specified angle in degrees
        """

        self.__x_rotation_angle = (self.__x_rotation_angle + angle) % 360

    def rotate_y(self, angle: float) -> None:
        """
        Rotates the window y angle by the specified angle in degrees
        """

        self.__y_rotation_angle = (self.__y_rotation_angle + angle) % 360

    def rotate_z(self, angle: float) -> None:
        """
        Rotates the window by the specified angle in degrees
        """

        self.__z_rotation_angle = (self.__z_rotation_angle + angle) % 360

    def world_to_normalized(self, xw: float, yw: float, zw: float) -> tuple[float, float, float]:
        """
        Converts from World Coordinates to Normalized Device Coordinates
        """

        xn = (2.0 * (xw - self.__xmin) / (self.__xmax - self.__xmin)) - 1.0
        yn = (2.0 * (yw - self.__ymin) / (self.__ymax - self.__ymin)) - 1.0
        zn = (2.0 * (zw - self.__zmin) / (self.__zmax - self.__zmin)) - 1.0

        return xn, yn, zn

    def normalized_to_world(self, xn: float, yn: float, zn: float) -> tuple[float, float, float]:
        """
        Converts from Normalized Device Coordinates to World Coordinates
        """

        xw = self.__xmin + ((xn + 1.0) * (self.__xmax - self.__xmin)) / 2.0
        yw = self.__ymin + ((yn + 1.0) * (self.__ymax - self.__ymin)) / 2.0
        zw = self.__zmin + ((zn + 1.0) * (self.__zmax - self.__zmin)) / 2.0

        return xw, yw, zw

    def parallel_orthogonal_projection(self):
        vrp_x, vrp_y, vrp_z = self.center()
        vrp = create_translation_matrix_3d(-vrp_x, -vrp_y, -vrp_z)
        vpn_x = create_rotation_matrix_3dx(-self.__x_rotation_angle)
        vpn_y = create_rotation_matrix_3dy(-self.__y_rotation_angle)

        return vrp @ vpn_x @ vpn_y

    def perspective_projection(self):
        vrp_x, vrp_y, vrp_z = self.center()
        vrp = create_translation_matrix_3d(-vrp_x, -vrp_y, -vrp_z)
        vpn_x = create_rotation_matrix_3dx(-self.__x_rotation_angle)
        vpn_y = create_rotation_matrix_3dy(-self.__y_rotation_angle)
        d = 40
        cop = create_perspective_matrix(d)

        return vrp @ vpn_x @ vpn_y @ cop

    def get_angles(self) -> tuple[float, float, float]:
        """
        Returns the current rotation angles of the window
        """

        return self.__x_rotation_angle, self.__y_rotation_angle, self.__z_rotation_angle
