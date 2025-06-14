import numpy as np

from utils.transformations import (
    create_rotation_matrix_2d,
    create_translation_matrix_3d,
    create_scale_matrix_3d,
    create_rotation_matrix_3dx,
    create_rotation_matrix_3dy,
    create_rotation_matrix_3dz,
    create_rotation_matrix_3d
)


class Point3D:
    def __init__(self, coordinates: list[tuple[int, int, int]]):
        self.coordinates: list[tuple[int, int, int]] = coordinates

    def get_coordinates(self) -> list[tuple[int, int, int]]:
        return self.coordinates

    def translate(self, dx: float, dy: float, dz: float) -> None:
        T = create_translation_matrix_3d(dx, dy, dz)
        self.transformation(op=T)

    def transform(self, sx: float, sy: float, sz: float) -> None:
        S = create_scale_matrix_3d(sx, sy, sz)
        self.transformation(op=S)

    def rotate_x(self, angle: float) -> None:
        Rx = create_rotation_matrix_3dx(angle)
        self.transformation(op=Rx)

    def rotate_y(self, angle: float) -> None:
        Ry = create_rotation_matrix_3dy(angle)
        self.transformation(op=Ry)

    def rotate_z(self, angle: float) -> None:
        Rz = create_rotation_matrix_3dz(angle)
        self.transformation(op=Rz)

    def rotate(self, angle_x: float, angle_y: float, angle_z: float):
        R = create_rotation_matrix_3d(angle_x, angle_y, angle_z)
        self.transformation(op=R)

    def transformation(self, obj=None, op=None) -> None:
        new_coords = []
        x, y, z = self.coordinates
        point = np.matrix([x, y, z, 1])
        transformed_point = point * op
        new_coords.append(
            (
                float(transformed_point[0, 0]),
                float(transformed_point[0, 1]),
                float(transformed_point[0, 2]),
            )
        )
        if len(new_coords) == 1:
            new_coords = new_coords[0]
        self.coordinates = new_coords
