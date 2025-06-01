import numpy as np


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


def create_coord_transform_matrix(cx, cy, angle, sx, sy):
    T = create_translation_matrix(-cx, -cy)
    R = create_rotation_matrix(angle)
    S = create_scale_matrix(sx, sy)
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
