import numpy as np

from utils.transformations import (
    create_translation_matrix_3d,
    create_scale_matrix_3d,
    create_rotation_matrix_3dx,
    create_rotation_matrix_3dy,
    create_rotation_matrix_3dz,
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

    def transformation(self, obj=None, op=None) -> None:
        new_coords = []
        for x, y, z in self.coordinates:
            point = np.matrix([x, y, z, 1])
            transformed_point = point * op
            new_coords.append(
                (
                    float(transformed_point[0, 0]),
                    float(transformed_point[0, 1]),
                    float(transformed_point[0, 2]),
                )
            )
        self.coordinates = new_coords
