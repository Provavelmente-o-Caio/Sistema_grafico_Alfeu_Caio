import numpy as np
from PyQt6.QtGui import QColor
from models.point_3d import Point3D
from utils.types import ObjectType
from utils.transformations import forward_differences_bicubic_setup, forward_differences_bicubic_evaluate


class SurfaceBSplineFD:
    def __init__(
        self,
        name: str,
        control_points_matrix: list[list[Point3D]],
        resolution: int = 20,
        fill: bool = False,
    ):
        self.name: str = name
        self.obj_type: ObjectType = ObjectType.SURFACE_BSPLINE_FD
        self.control_points_matrix: list[list[Point3D]] = control_points_matrix
        self.color: QColor = QColor("black")
        self.is_selected: bool = False
        self.fill: bool = fill
        self.resolution: int = resolution
        
        self.rows = len(control_points_matrix)
        self.cols = len(control_points_matrix[0]) if self.rows > 0 else 0
        
        if self.rows < 4 or self.cols < 4:
            raise ValueError("Control points matrix must be at least 4x4")
        if self.rows > 20 or self.cols > 20:
            raise ValueError("Control points matrix cannot exceed 20x20")
        
        self.surface_patches = []
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
        for row in self.control_points_matrix:
            for point in row:
                point.translate(dx, dy, dz)
        self.generate_surface()

    def transform(self, sx: float, sy: float, sz: float) -> None:
        for row in self.control_points_matrix:
            for point in row:
                point.transform(sx, sy, sz)
        self.generate_surface()

    def rotate(self, angle_x: float, angle_y: float, angle_z: float):
        for row in self.control_points_matrix:
            for point in row:
                point.rotate(angle_x, angle_y, angle_z)
        self.generate_surface()

    def generate_surface(self):
        """Generate surface patches using forward differences"""
        self.surface_patches = []
        
        patches_u = max(1, self.rows - 3)
        patches_v = max(1, self.cols - 3)
        
        for i in range(patches_u):
            for j in range(patches_v):
                patch_control_points = []
                for u in range(4):
                    row = []
                    for v in range(4):
                        row.append(self.control_points_matrix[min(i + u, self.rows - 1)][min(j + v, self.cols - 1)])
                    patch_control_points.append(row)
                
                try:
                    Cx, Cy, Cz, delta_u, delta_v = forward_differences_bicubic_setup(
                        patch_control_points, self.resolution
                    )
                    patch_points = forward_differences_bicubic_evaluate(
                        Cx, Cy, Cz, delta_u, delta_v, self.resolution
                    )
                    self.surface_patches.append(patch_points)
                except Exception as e:
                    print(f"Error generating patch [{i}][{j}]: {e}")

    def get_wireframe_edges(self) -> list[tuple[Point3D, Point3D]]:
        """Get edges for wireframe rendering of all patches"""
        edges = []
        
        for patch in self.surface_patches:
            if not patch:
                continue
                
            for i in range(len(patch)):
                for j in range(len(patch[i]) - 1):
                    p1 = patch[i][j]
                    p2 = patch[i][j + 1]
                    edges.append((p1, p2))
            
            for i in range(len(patch) - 1):
                for j in range(len(patch[i])):
                    p1 = patch[i][j]
                    p2 = patch[i + 1][j]
                    edges.append((p1, p2))
        
        return edges

    def get_control_points_flat(self) -> list[Point3D]:
        """Get all control points as a flat list"""
        points = []
        for row in self.control_points_matrix:
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

    def get_dimensions(self) -> tuple[int, int]:
        return self.rows, self.cols