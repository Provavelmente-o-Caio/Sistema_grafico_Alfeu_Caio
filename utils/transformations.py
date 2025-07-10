import numpy as np


def create_translation_matrix_2d(dx: float, dy: float) -> np.array:
    return np.array([
        [1, 0, 0],
        [0, 1, 0],
        [dx, dy, 1]
    ])

def create_translation_matrix_3d(dx: float, dy: float, dz: float) -> np.array:
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])

def create_scale_matrix_2d(sx: float, sy: float) -> np.array:
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def create_scale_matrix_3d(sx: float, sy: float, sz: float) -> np.array:
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_2d(angle: float) -> np.array:
    angle = np.deg2rad(angle)
    return np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )

def create_rotation_matrix_3dx(angle: float) -> np.array:
    angle = np.deg2rad(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), np.sin(angle), 0],
        [0, -np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_3dy(angle: float) -> np.array:
    angle = np.deg2rad(angle)
    return np.array([
        [np.cos(angle), 0, -np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_3dz(angle: float) -> np.array:
    angle = np.deg2rad(angle)
    return np.array([
        [np.cos(angle), np.sin(angle), 0, 0],
        [-np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix_3d(x_angle: float, y_angle: float, z_angle: float) -> np.array:
    Rx = create_rotation_matrix_3dx(x_angle)
    Ry = create_rotation_matrix_3dy(y_angle)
    Rz = create_rotation_matrix_3dz(z_angle)

    R = Rx @ Ry @ Rz
    return R

def create_coord_transform_matrix(cx, cy, angle, sx, sy):
    T = create_translation_matrix_2d(-cx, -cy)
    R = create_rotation_matrix_2d(angle)
    S = create_scale_matrix_2d(sx, sy)
    M = T @ R @ S
    return M

def create_coord_transform_matrix_3d(cx, cy, cz, x_angle, y_angle, z_angle, sx, sy, sz):
    T = create_translation_matrix_3d(cx, cy, cz)
    R = create_rotation_matrix_3d(x_angle, y_angle, z_angle)
    S = create_scale_matrix_3d(sx, sy, sz)
    M = T @ R @ S
    return M

def create_perspective_matrix(d: int) -> np.array:
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1/d, 0]
    ]).T

def create_bezier_matrix(p1, p2, p3, p4):
    bezier = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])

    px_matrix = np.array([[p1[0], p2[0], p3[0], p4[0]]])
    py_matrix = np.array([[p1[1], p2[1], p3[1], p4[1]]])

    px = bezier @ px_matrix.T
    py = bezier @ py_matrix.T

    return px, py


def create_b_spline_matrix(p1, p2, p3, p4):
    b_spline = (
        np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) / 6
    )

    px_matrix = np.array([[p1[0], p2[0], p3[0], p4[0]]])
    py_matrix = np.array([[p1[1], p2[1], p3[1], p4[1]]])

    px = b_spline @ px_matrix.T
    py = b_spline @ py_matrix.T

    return px, py


def forward_differences_matrix(delta: float = 0.1):
    forward_differences = np.array(
        [
            [0, 0, 0, 1],
            [pow(delta, 3), pow(delta, 2), delta, 0],
            [6 * pow(delta, 3), 2 * pow(delta, 2), 0, 0],
            [6 * pow(delta, 3), 0, 0, 0],
        ]
    )

    return forward_differences

def create_bspline_bicubic_matrix():
    """Creates the B-spline bicubic basis matrix"""
    return np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 0, 3, 0],
        [1, 4, 1, 0]
    ]) / 6

def forward_differences_bicubic_setup(control_points_4x4, n_steps=20):
    """
    Setup forward differences for bicubic B-spline surface
    control_points_4x4: 4x4 matrix of Point3D objects
    n_steps: number of steps for parametrization (default 20)
    """
    M = create_bspline_bicubic_matrix()
    delta_u = 1.0 / n_steps
    delta_v = 1.0 / n_steps
    
    Gx = np.zeros((4, 4))
    Gy = np.zeros((4, 4))
    Gz = np.zeros((4, 4))
    
    for i in range(4):
        for j in range(4):
            coords = control_points_4x4[i][j].get_coordinates()
            if isinstance(coords, list):
                x, y, z = coords[0]
            else:
                x, y, z = coords
            Gx[i][j] = x
            Gy[i][j] = y
            Gz[i][j] = z
    
    Cx = M @ Gx @ M.T
    Cy = M @ Gy @ M.T
    Cz = M @ Gz @ M.T
    
    return Cx, Cy, Cz, delta_u, delta_v

def forward_differences_bicubic_evaluate(Cx, Cy, Cz, delta_u, delta_v, n_steps=20):
    """
    Evaluate bicubic surface using forward differences
    Returns list of surface points
    """
    points = []
    
    for i in range(n_steps + 1):
        u = i * delta_u
        row_points = []
        
        u_powers = np.array([u**3, u**2, u, 1])
        
        ax = u_powers @ Cx
        ay = u_powers @ Cy
        az = u_powers @ Cz
        
        v = 0.0
        x = ax[3]  # a0
        y = ay[3]  # a0
        z = az[3]  # a0
        
        dx = ax[2] * delta_v 
        dy = ay[2] * delta_v
        dz = az[2] * delta_v
        
        d2x = ax[1] * delta_v * delta_v  
        d2y = ay[1] * delta_v * delta_v
        d2z = az[1] * delta_v * delta_v
        
        d3x = ax[0] * delta_v * delta_v * delta_v  
        d3y = ay[0] * delta_v * delta_v * delta_v
        d3z = az[0] * delta_v * delta_v * delta_v
        
        for j in range(n_steps + 1):
            from models.point_3d import Point3D
            row_points.append(Point3D([(float(x), float(y), float(z))]))
            
            x += dx
            y += dy
            z += dz
            
            dx += d2x
            dy += d2y
            dz += d2z
            
            d2x += d3x
            d2y += d3y
            d2z += d3z
        
        points.append(row_points)
    
    return points