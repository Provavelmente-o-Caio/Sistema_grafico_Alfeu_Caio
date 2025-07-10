import numpy as np
from PyQt6.QtGui import QColor
from models.point_3d import Point3D
from utils.types import ObjectType


class Surface3D:
    def __init__(
        self,
        name: str,
        obj_type: ObjectType,
        control_points: list[list[Point3D]],
        resolution: int = 20,
        fill: bool = False,
    ):
        self.name: str = name
        self.obj_type: ObjectType = obj_type
        self.control_points: list[list[Point3D]] = control_points  
        self.color: QColor = QColor("black")
        self.is_selected: bool = False
        self.fill: bool = fill
        self.resolution: int = resolution
        self.surface_points: list[list[Point3D]] = []
        self.triangles: list[tuple[int, int, int]] = []
        self.generate_surface()

    def set_fill(self, fill: bool) -> None:
        self.fill = fill

    def set_color(self, color: QColor) -> None:
        self.color = color

    def select(self) -> None:
        self.is_selected = True

    def deselect(self) -> None:
        self.is_selected = False

    def translate(self, dx: float, dy: float, dz: float) -> None:
        for row in self.control_points:
            for point in row:
                point.translate(dx, dy, dz)
        self.generate_surface()

    def transform(self, sx: float, sy: float, sz: float) -> None:
        for row in self.control_points:
            for point in row:
                point.transform(sx, sy, sz)
        self.generate_surface()

    def rotate(self, angle_x: float, angle_y: float, angle_z: float):
        for row in self.control_points:
            for point in row:
                point.rotate(angle_x, angle_y, angle_z)
        self.generate_surface()

    def generate_surface(self):
        """Generate the surface mesh from control points"""
        if self.obj_type == ObjectType.SURFACE_BEZIER:
            self._generate_bezier_surface()
        elif self.obj_type == ObjectType.SURFACE_BSPLINE:
            self._generate_bspline_surface()

    def _generate_bezier_surface(self):
        """Generate Bézier bicubic surface"""
        # Bézier basis matrix
        M_bezier = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])

        self.surface_points = []
        
        for i in range(self.resolution + 1):
            u = i / self.resolution
            row_points = []
            
            for j in range(self.resolution + 1):
                v = j / self.resolution
                
                point = self._evaluate_bezier_point(u, v, M_bezier)
                row_points.append(point)
            
            self.surface_points.append(row_points)
        
        self._generate_triangles()

    def _generate_bspline_surface(self):
        """Generate B-Spline surface"""
        M_bspline = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 0, 3, 0],
            [1, 4, 1, 0]
        ]) / 6

        self.surface_points = []
        
        for i in range(self.resolution + 1):
            u = i / self.resolution
            row_points = []
            
            for j in range(self.resolution + 1):
                v = j / self.resolution
                
                point = self._evaluate_bezier_point(u, v, M_bspline)
                row_points.append(point)
            
            self.surface_points.append(row_points)
        
        self._generate_triangles()

    def _evaluate_bezier_point(self, u: float, v: float, basis_matrix: np.ndarray) -> Point3D:
        """Evaluate a point on the surface at parameters u, v"""
        U = np.array([u**3, u**2, u, 1])
        V = np.array([v**3, v**2, v, 1])
        
        x_points = np.zeros((4, 4))
        y_points = np.zeros((4, 4))
        z_points = np.zeros((4, 4))
        
        for i in range(4):
            for j in range(4):
                coords = self.control_points[i][j].get_coordinates()
                if isinstance(coords, list) and len(coords) > 0:
                    x, y, z = coords[0]
                else:
                    x, y, z = coords
                x_points[i][j] = x
                y_points[i][j] = y
                z_points[i][j] = z
        
        x = U @ basis_matrix @ x_points @ basis_matrix.T @ V
        y = U @ basis_matrix @ y_points @ basis_matrix.T @ V
        z = U @ basis_matrix @ z_points @ basis_matrix.T @ V
        
        return Point3D([(float(x), float(y), float(z))])

    def _generate_triangles(self):
        """Generate triangles for wireframe rendering"""
        self.triangles = []
        
        for i in range(self.resolution):
            for j in range(self.resolution):
                v1 = i * (self.resolution + 1) + j
                v2 = v1 + 1
                v3 = (i + 1) * (self.resolution + 1) + j
                v4 = v3 + 1
                
                self.triangles.append((v1, v2, v3))
                self.triangles.append((v2, v4, v3))

    def get_wireframe_edges(self) -> list[tuple[Point3D, Point3D]]:
        """Get edges for wireframe rendering"""
        edges = []
        
        # Horizontal edges
        for i in range(len(self.surface_points)):
            for j in range(len(self.surface_points[i]) - 1):
                p1 = self.surface_points[i][j]
                p2 = self.surface_points[i][j + 1]
                edges.append((p1, p2))
        
        # Vertical edges
        for i in range(len(self.surface_points) - 1):
            for j in range(len(self.surface_points[i])):
                p1 = self.surface_points[i][j]
                p2 = self.surface_points[i + 1][j]
                edges.append((p1, p2))
        
        return edges

    def get_control_points_flat(self) -> list[Point3D]:
        """Get all control points as a flat list"""
        points = []
        for row in self.control_points:
            points.extend(row)
        return points

    def get_center_object_x(self) -> float:
        points = self.get_control_points_flat()
        if not points:
            return 0
        sum_x = sum(p.get_coordinates()[0] if isinstance(p.get_coordinates(), tuple) 
                   else p.get_coordinates()[0][0] for p in points)
        return sum_x / len(points)

    def get_center_object_y(self) -> float:
        points = self.get_control_points_flat()
        if not points:
            return 0
        sum_y = sum(p.get_coordinates()[1] if isinstance(p.get_coordinates(), tuple) 
                   else p.get_coordinates()[0][1] for p in points)
        return sum_y / len(points)

    def get_center_object_z(self) -> float:
        points = self.get_control_points_flat()
        if not points:
            return 0
        sum_z = sum(p.get_coordinates()[2] if isinstance(p.get_coordinates(), tuple) 
                   else p.get_coordinates()[0][2] for p in points)
        return sum_z / len(points)

    def export_coordinates(self) -> list[Point3D]:
        return self.get_control_points_flat()

    def get_name(self) -> str:
        return self.name

    def get_color(self) -> str:
        return self.color.name()

    def get_obj_type(self) -> ObjectType:
        return self.obj_type