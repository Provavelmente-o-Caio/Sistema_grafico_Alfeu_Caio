import numpy as np


def create_translation_matrix_2d(dx: float, dy: float) -> np.matrix:
    return np.matrix([
        [1, 0, 0],
        [0, 1, 0],
        [dx, dy, 1]
    ])

def create_translation_matrix_3d(dx: float, dy: float, dz: float) -> np.matrix:
    return np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])

def create_scale_matrix_2d(sx: float, sy: float) -> np.matrix:
    return np.matrix([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def create_scale_matrix_3d(sx: float, sy: float, sz: float) -> np.matrix:
    return np.matrix([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_2d(angle: float) -> np.matrix:
    angle = np.deg2rad(angle)
    return np.matrix(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )

def create_rotation_matrix_3dx(angle: float) -> np.matrix:
    angle = np.deg2rad(angle)
    return np.matrix([
        [1, 0, 0, 0],
        [0, np.cos(angle), np.sin(angle), 0],
        [0, -np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_3dy(angle: float) -> np.matrix:
    angle = np.deg2rad(angle)
    return np.matrix([
        [np.cos(angle), 0, -np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_3dz(angle: float) -> np.matrix:
    angle = np.deg2rad(angle)
    return np.matrix([
        [np.cos(angle), np.sin(angle), 0, 0],
        [-np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_3d(x_angle: float, y_angle: float, z_angle: float) -> np.matrix:
    x_angle = np.deg2rad(x_angle)
    y_angle = np.deg2rad(y_angle)
    z_angle = np.deg2rad(z_angle)

    Rx = create_rotation_matrix_3dx(x_angle)
    Ry = create_rotation_matrix_3dz(y_angle)
    Rz = create_rotation_matrix_3dy(z_angle)

    R = Rx @ Ry @ Rz
    return R

def create_coord_transform_matrix(cx, cy, angle, sx, sy):
    T = create_translation_matrix_2d(-cx, -cy)
    R = create_rotation_matrix_2d(angle)
    S = create_scale_matrix_2d(sx, sy)
    M = T @ R @ S
    return M

def create_coord_transform_matrix_3d(cx, cy, cz, x_angle, y_angle, z_angle):
    T = create_translation_matrix_3d(cx, cy, cz)
    R = create_rotation_matrix_3d(x_angle, y_angle, z_angle)
    S = create_scale_matrix_3d(cx, cy, cz)
    M = T @ R @ S
    return M


def create_bezier_matrix(p1, p2, p3, p4):
    bezier = np.matrix([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])

    px_matrix = np.matrix([[p1[0], p2[0], p3[0], p4[0]]])
    py_matrix = np.matrix([[p1[1], p2[1], p3[1], p4[1]]])

    px = bezier @ px_matrix.T
    py = bezier @ py_matrix.T

    return px, py


def create_b_spline_matrix(p1, p2, p3, p4):
    b_spline = (
        np.matrix([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) / 6
    )

    px_matrix = np.matrix([[p1[0], p2[0], p3[0], p4[0]]])
    py_matrix = np.matrix([[p1[1], p2[1], p3[1], p4[1]]])

    px = b_spline @ px_matrix.T
    py = b_spline @ py_matrix.T

    return px, py


def forward_differences_matrix(delta: float = 0.1):
    forward_differences = np.matrix(
        [
            [0, 0, 0, 1],
            [pow(delta, 3), pow(delta, 2), delta, 0],
            [6 * pow(delta, 3), 2 * pow(delta, 2), 0, 0],
            [6 * pow(delta, 3), 0, 0, 0],
        ]
    )

    return forward_differences
