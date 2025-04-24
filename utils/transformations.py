import numpy as np

def create_translation_matrix(dx, dy):
    return np.matrix([[1, 0, 0],
                      [0, 1, 0],
                      [dx, dy, 1]])

def create_scale_matrix(sx, sy):
    return np.matrix([[sx, 0, 0],
                      [0, sy, 0],
                      [0, 0, 1]])

def create_rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.matrix([[np.cos(angle), -np.sin(angle), 0],
                      [np.sin(angle),  np.cos(angle), 0],
                      [0,              0,             1]])

def create_coord_transform_matrix(cx, cy, angle, sx, sy):
    T = create_translation_matrix(-cx, -cy)
    R = create_rotation_matrix(angle)
    S = create_scale_matrix(sx, sy)
    M = T @ R @ S # Cria a matriz de transformação de coordenadas
    return M