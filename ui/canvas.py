import numpy as np
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette
from PyQt6.QtWidgets import QWidget
import math

from models.window import Window
from models.wireframe import Wireframe
from models.wireframe_3d import Wireframe_3D
from models.point_3d import Point3D
from utils.descritorOBJ import DescritorOBJ
from utils.transformations import (
    create_bezier_matrix,
    forward_differences_matrix,
    create_b_spline_matrix,
)
from utils.types import ObjectType


class Canvas(QWidget):
    def __init__(self, console):
        super().__init__()
        self.console = console
        self.descritor = DescritorOBJ()
        self.setAutoFillBackground(True)

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        self.setPalette(palette)

        self.setMinimumSize(400, 300)

        # List to store all wireframe objects (display file)
        self.objects: List[Wireframe | Wireframe_3D] = []

        # Window and viewport setup
        self.window: Window = Window()
        self.border_width: int = 50
        self.viewport_xmin: int = self.border_width
        self.viewport_ymin: int = self.border_width
        self.viewport_xmax: int = self.width() - self.border_width
        self.viewport_ymax: int = self.height() - self.border_width

        self.step = 1.0  # Step size for panning
        self.zoom_factor = 1.2  # Zoom factor

        # Loads the example objects for better utilization of the software
        self.load_example_objects()

        # Setting the line clipping Algorithm
        self.line_clipping_algorithm = "Cohen-Sutherland"

        # Setting the movement mode
        self.movement_mode = "Move"

        # setting the projection view
        self.projection = "Parallel Projection"

        # Show the curves control points
        self.show_control_points = False

    def add_object(self, wireframe: Wireframe):
        """
        Add a new object to the canvas
        """

        try:
            if any(wireframe.name == obj.name for obj in self.objects):
                raise ValueError

            self.objects.append(wireframe)
            self.update()
        except ValueError:
            self.console.log(f"Object {wireframe.name} already exists")

    def load_example_objects(self):
        """
        Preset objects to show this project funcionalities
        """

        dot = Wireframe("Dot Example", ObjectType.DOT, [(0, 0)])
        dot.set_color(QColor("red"))
        self.add_object(dot)

        line = Wireframe("Line Example", ObjectType.LINE, [(-5, -5), (5, 5)])
        line.set_color(QColor("green"))
        self.add_object(line)

        triangle = Wireframe(
            "Triangle Example",
            ObjectType.POLYGON,
            [(0, 0), (5, 8), (-5, 8)],
            fill=True,
        )
        triangle.set_color(QColor("blue"))
        self.add_object(triangle)

        cube = Wireframe_3D(
            "Square Example",
            ObjectType.POLYGON_3D,
            [
                Point3D((-5, -5, 0)),
                Point3D((5, -5, 0)),
                Point3D((5, 5, 0)),
                Point3D((-5, 5, 0)),
                Point3D((-5, -5, 5)),
                Point3D((5, -5, 5)),
                Point3D((5, 5, 5)),
                Point3D((-5, 5, 5)),
            ],
            [
                (0, 1),
                (0, 3),
                (0, 4),
                (1, 2),
                (1, 5),
                (2, 3),
                (2, 6),
                (3, 7),
                (4, 5),
                (4, 7),
                (5, 6),
                (6, 7),
            ],
        )
        cube.set_color(QColor("cyan"))
        self.add_object(cube)

        curve = Wireframe(
            "Continuous Curve",
            ObjectType.CURVE,
            [
                (0, 0),
                (2, 2),
                (4, -2),
                (6, 0),  # First Bézier segment: P0, P1, P2, P3
                (6, 0),
                (8, 2),
                (10, -2),
                (12, 0),  # Second Bézier segment: P3 == P4 ensures G0 continuity
                (12, 0),
                (14, 2),
                (16, -2),
                (18, 0),  # Third Bézier segment: P7 == P8 ensures G0 continuity
            ],
        )

        curve.set_color(QColor("orange"))
        self.add_object(curve)

        bspline = Wireframe(
            "B-Spline Example",
            ObjectType.CURVE_BSPLINE,
            [
                (-10, 0),
                (-5, 10),
                (0, -10),
                (5, 10),
                (10, 0),
            ],
        )
        bspline.set_color(QColor("purple"))
        self.add_object(bspline)

        center = (0, 0)
        radius = 4
        height = 4

        # uso de IA:
        # pode desenhar um wireframe_3d no load_example_objects no formato de um hexágono?
        points = []
        for z in [-height / 2, height / 2]:
            for i in range(6):
                angle = 2 * math.pi * i / 6
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                points.append(Point3D((x, y, z)))

        edges = []
        for i in range(6):
            # Superior
            edges.append((i, (i + 1) % 6))
            # Inferior
            edges.append((i + 6, ((i + 1) % 6) + 6))
            # Ligações verticais
            edges.append((i, i + 6))

        hexagon3d = Wireframe_3D(
            "Hexagonal Prism", ObjectType.POLYGON_3D, points, edges
        )
        hexagon3d.set_color(QColor("red"))
        self.add_object(hexagon3d)

    def remove_object(self, name: str):
        """
        Removes the selected objects from the canvas
        """

        self.objects = [obj for obj in self.objects if obj.name != name]
        self.update()

    def clear(self):
        """
        Removes all objects from the canvas
        """

        self.objects.clear()
        self.update()

    def translate_objects(
        self, object: Wireframe | Wireframe_3D, dx: float, dy: float, dz: float = 0
    ):
        """
        This method is responsible for 2D translation.
        It basically is adding and/or subtracting coordinates to all objects
        """

        if isinstance(object, Wireframe):
            object.translate(dx, dy)
        elif isinstance(object, Wireframe_3D):
            object.translate(dx, dy, dz)
        self.update()

    def transform_objects(
        self, object: Wireframe | Wireframe_3D, dx: float, dy: float, dz: float = 0
    ):
        """
        This method is responsible for 2D transformation.
        It basically is mutltiplication coordinates to an objects
        """

        if isinstance(object, Wireframe):
            object.transform(dx, dy)
        elif isinstance(object, Wireframe_3D):
            object.transform(dx, dy, dz)
        self.update()

    def rotate_objects(
        self,
        object: Wireframe | Wireframe_3D,
        angle_x: float,
        angle_y: float,
        angle_z: float,
    ):
        """
        This method is responsible for 3D rotation
        It basically is multiplying the objects for sin and cos
        """

        if isinstance(object, Wireframe):
            object.rotate(angle_z)
        elif isinstance(object, Wireframe_3D):
            object.rotate(angle_x, angle_y, angle_z)
        self.update()

    def rotateWithCenter(self, object: Wireframe | Wireframe_3D, angle: float):
        """
        This method is responsible for rotating a single object
        """

        if isinstance(object, Wireframe):
            cx = object.get_center_object_x()
            cy = object.get_center_object_y()

            self.translate_objects(object, -cx, -cy)
            object.rotate(angle)
            self.translate_objects(object, cx, cy)
        elif isinstance(object, Wireframe_3D):
            cx = object.get_center_object_x()
            cy = object.get_center_object_y()
            cz = object.get_center_object_x()

            self.translate_objects(object, -cx, -cy, -cz)
            object.rotate_z(angle)
            self.translate_objects(object, cx, cy, cz)

        self.update()

    def rotateInPoint(
        self,
        object: Wireframe | Wireframe_3D,
        angle: float,
        px: float,
        py: float,
        pz: float = 0,
    ):
        """
        This method rotates an object around a specific point
        """

        if isinstance(object, Wireframe):
            object.translate(-px, -py)
            object.rotate(angle)
            object.translate(px, py)
        elif isinstance(object, Wireframe_3D):
            object.translate(-px, -py, -pz)
            object.rotate_z(angle)
            object.translate(px, py, pz)
        self.update()

    def transform_coords(self, xw=0, yw=0, zw=1):
        """
        Window to Viewport transformation
        """
        if self.projection == "Parallel Projection":
            projection_matrix = self.window.parallel_orthogonal_projection()
        elif self.projection == "Perspective Projection":
            projection_matrix = self.window.perspective_projection()
        coord_array = np.matrix([[xw, yw, zw, 1]])
        v_proj = coord_array @ projection_matrix

        w = v_proj[0, 3] if v_proj[0, 3] != 0 else 1
        x_proj = v_proj[0, 0] / w
        y_proj = v_proj[0, 1] / w
        z_proj = v_proj[0, 2] / w

        if z_proj == 0 or w <= 0:
            return None, None

        xn, yn, zn = self.window.world_to_normalized(x_proj, y_proj, z_proj)

        M = self.window.get_transformation_matrix()
        point = np.matrix([xn, yn, zn, 1])
        transformed = point * M
        xt, yt, _ = (
            float(transformed[0, 0]),
            float(transformed[0, 1]),
            float(transformed[0, 2]),
        )

        xvp = self.viewport_xmin + (self.viewport_xmax - self.viewport_xmin) * (
            (xt + 1) / 2
        )
        yvp = self.viewport_ymin + (self.viewport_ymax - self.viewport_ymin) * (
            1 - ((yt + 1) / 2)
        )

        return xvp, yvp

    def resizeEvent(self, event):
        self.viewport_xmax = self.width() - self.border_width
        self.viewport_ymax = self.height() - self.border_width
        self.update()

    def move(self, dx, dy, dz):
        if self.movement_mode == "Move":
            self.pan(dx, dy, dz)
        elif self.movement_mode == "Rotate":
            self.rotate_camera(dx * 10, dy * 10, dz * 10)

    def pan(self, dx, dy, dz):
        """
        Pan the window by dx and dy.
        """

        self.window.pan(dx * self.step, dy * self.step, dz * self.step)
        self.update()

    def rotate_camera(self, dx, dy, dz):
        self.window.rotate_x(dx * self.step)
        self.window.rotate_y(dy * self.step)
        self.window.rotate_z(dz * self.step)
        self.update()

    # Zoom the window
    def zoom_in(self):
        self.window.zoom(1 / self.zoom_factor)
        self.update()

    def zoom_out(self):
        self.window.zoom(self.zoom_factor)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Desenha a borda vermelha
        border_pen = QPen(QColor("red"))
        border_pen.setWidth(2)  # border width
        painter.setPen(border_pen)
        painter.drawRect(
            self.viewport_xmin,
            self.viewport_ymin,
            self.viewport_xmax - self.border_width,
            self.viewport_ymax - self.border_width,
        )

        for obj in self.objects:
            try:
                pen = QPen(obj.color)
                if obj.is_selected:
                    pen.setWidth(2)
                painter.setPen(pen)

                if obj.obj_type == ObjectType.DOT:
                    (x, y) = obj.coordinates[0]
                    vx, vy = self.transform_coords(x, y)
                    if vx and vy:
                        self.point_clipping(painter, vx, vy)
                elif obj.obj_type == ObjectType.LINE:
                    if len(obj.coordinates) == 2:
                        x1, y1 = obj.coordinates[0]
                        x2, y2 = obj.coordinates[1]
                        vx1, vy1 = self.transform_coords(x1, y1)
                        vx2, vy2 = self.transform_coords(x2, y2)
                        if (vx1 and vy1) and (vx2 and vy2):
                            clipped_line = self.line_clipping(vx1, vy1, vx2, vy2)
                            if clipped_line:
                                vx1, vy1, vx2, vy2 = clipped_line
                                painter.drawLine(int(vx1), int(vy1), int(vx2), int(vy2))

                elif obj.obj_type == ObjectType.POLYGON:
                    if len(obj.coordinates) >= 3:
                        if obj.fill:
                            painter.setBrush(obj.color)
                        else:
                            painter.setBrush(Qt.BrushStyle.NoBrush)
                        painter.setPen(pen)
                        self.polygon_clipping(painter, obj)
                elif obj.obj_type == ObjectType.CURVE:
                    if len(obj.coordinates) >= 4:
                        self.check_bezier_continuity(obj.coordinates)

                        for i in range(0, len(obj.coordinates) - 3, 4):
                            x1, y1 = obj.coordinates[i]
                            x2, y2 = obj.coordinates[i + 1]
                            x3, y3 = obj.coordinates[i + 2]
                            x4, y4 = obj.coordinates[i + 3]
                            segment = self.bezier(x1, y1, x2, y2, x3, y3, x4, y4)
                            if len(segment) >= 2:
                                for j in range(len(segment) - 1):
                                    vx1, vy1 = self.transform_coords(
                                        segment[j][0], segment[j][1]
                                    )
                                    vx2, vy2 = self.transform_coords(
                                        segment[j + 1][0], segment[j + 1][1]
                                    )
                                    if (vx1 and vy1) and (vx2 and vy2):
                                        clipped_line = self.line_clipping(
                                            vx1, vy1, vx2, vy2
                                        )
                                        if clipped_line:
                                            vx1, vy1, vx2, vy2 = clipped_line
                                            painter.drawLine(
                                                int(vx1), int(vy1), int(vx2), int(vy2)
                                            )
                        if self.show_control_points:
                            for x, y in obj.coordinates:
                                vx, vy = self.transform_coords(x, y)
                                if vx and vy:
                                    painter.setBrush(QColor("Magenta"))
                                    self.point_clipping(painter, vx, vy)
                elif obj.obj_type == ObjectType.CURVE_BSPLINE:
                    if len(obj.coordinates) >= 4:
                        num_segments = len(obj.coordinates) - 3
                        for i in range(num_segments):
                            x1, y1 = obj.coordinates[i]
                            x2, y2 = obj.coordinates[i + 1]
                            x3, y3 = obj.coordinates[i + 2]
                            x4, y4 = obj.coordinates[i + 3]
                            segment = self.b_spline(x1, y1, x2, y2, x3, y3, x4, y4)
                            for j in range(len(segment) - 1):
                                vx1, vy1 = self.transform_coords(
                                    segment[j][0], segment[j][1]
                                )
                                vx2, vy2 = self.transform_coords(
                                    segment[j + 1][0], segment[j + 1][1]
                                )
                                if (vx1 and vy1) and (vx2 and vy2):
                                    clipped_line = self.line_clipping(
                                        vx1, vy1, vx2, vy2
                                    )
                                    if clipped_line:
                                        vx1, vy1, vx2, vy2 = clipped_line
                                        painter.drawLine(
                                            int(vx1), int(vy1), int(vx2), int(vy2)
                                        )
                        if self.show_control_points:
                            for x, y in obj.coordinates:
                                vx, vy = self.transform_coords(x, y)
                                if vx and vy:
                                    painter.setBrush(QColor("Magenta"))
                                    self.point_clipping(painter, vx, vy)
                elif obj.obj_type == ObjectType.POLYGON_3D:
                    for edge in obj.edges:
                        if len(obj.points[int(edge[0])].get_coordinates()) == 1:
                            x1, y1, z1 = obj.points[int(edge[0])].get_coordinates()[0]
                            x2, y2, z2 = obj.points[int(edge[1])].get_coordinates()[0]
                        else:
                            x1, y1, z1 = obj.points[int(edge[0])].get_coordinates()
                            x2, y2, z2 = obj.points[int(edge[1])].get_coordinates()
                        vx1, vy1 = self.transform_coords(x1, y1, z1)
                        vx2, vy2 = self.transform_coords(x2, y2, z2)
                        if (vx1 and vy1) and (vx2 and vy2):
                            clipped_line = self.line_clipping(vx1, vy1, vx2, vy2)
                            if clipped_line:
                                vx1, vy1, vx2, vy2 = clipped_line
                                painter.drawLine(int(vx1), int(vy1), int(vx2), int(vy2))

            except OverflowError:
                self.console.log(f"{obj.name} was not added due to an overflow error.")

    def export_objects(self):
        self.descritor.objs = self.objects.copy()
        self.descritor.export_file()

    def import_objects(self, path, fill: bool = False):
        new_objects = self.descritor.import_file(path, fill)
        for new_object in new_objects:
            self.add_object(new_object)

    def point_clipping(self, painter: QPainter, vx: float, vy: float):
        """
        Draws a point if it is within the viewport.
        """
        if (
            self.viewport_xmin <= vx <= self.viewport_xmax
            and self.viewport_ymin <= vy <= self.viewport_ymax
        ):
            painter.drawEllipse(int(vx) - 3, int(vy) - 3, 6, 6)

    def line_clipping(self, vx1: float, vy1: float, vx2: float, vy2: float):
        """
        Applies the selected line clipping algorithm to the line defined by (vx1, vy1) and (vx2, vy2).
        """
        if self.line_clipping_algorithm == "Cohen-Sutherland":
            return self.cohen_sutherland(vx1, vy1, vx2, vy2)
        elif self.line_clipping_algorithm == "Liang-Barsky":
            return self.liang_barsky(vx1, vy1, vx2, vy2)
        return None

    def set_line_clipping_algorithm(self, line_clipping_algorithm: str):
        """
        Set the line clipping algorithm to be used.
        """
        self.line_clipping_algorithm = line_clipping_algorithm
        self.update()

    def set_movement_mode(self, movement_mode: str) -> None:
        self.movement_mode = movement_mode

    def set_projection_mode(self, projection_mode: str) -> None:
        self.projection = projection_mode
        self.update()

    @property
    def get_movement_mode(self):
        return self.movement_mode

    def cohen_sutherland(self, vx1: float, vy1: float, vx2: float, vy2: float):
        """
        Cohen-Sutherland line clipping algorithm.
        """
        cs_value_p1 = self.cohen_sutherland_point(vx1, vy1)
        cs_value_p2 = self.cohen_sutherland_point(vx2, vy2)
        x1, y1 = vx1, vy1
        x2, y2 = vx2, vy2
        while True:
            if cs_value_p1 & cs_value_p2:
                return None
            elif not (cs_value_p1 | cs_value_p2):
                return x1, y1, x2, y2
            else:
                m = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else None
                if cs_value_p1 != 0:
                    x1, y1 = self.cohen_sutherland_redraw(cs_value_p1, x1, y1, m)
                    cs_value_p1 = self.cohen_sutherland_point(x1, y1)
                else:
                    x2, y2 = self.cohen_sutherland_redraw(cs_value_p2, x2, y2, m)
                    cs_value_p2 = self.cohen_sutherland_point(x2, y2)

    def cohen_sutherland_point(self, vx: float, vy: float) -> int:
        """
        Applies the classification of the point in the viewport acording to the Cohen-Sutherland algorithm.
        """
        cs_value = 0

        if vx < self.viewport_xmin:
            cs_value |= 1  # 0001/left
        elif vx > self.viewport_xmax:
            cs_value |= 2  # 0010/right

        if vy > self.viewport_ymax:
            cs_value |= 4  # 0100/bottom
        elif vy < self.viewport_ymin:
            cs_value |= 8  # 1000/top

        return cs_value

    def cohen_sutherland_redraw(
        self, cs_value: int, vx: float, vy: float, m: float | None
    ):
        """
        Redraws the point according to the Cohen-Sutherland algorithm.
        """
        x, y = vx, vy
        if cs_value & 1:  # 0001/left
            y = m * (self.viewport_xmin - vx) + vy if m else vy
            x = self.viewport_xmin
        if cs_value & 2:  # 0010/right
            y = m * (self.viewport_xmax - vx) + vy if m else vy
            x = self.viewport_xmax
        if cs_value & 4:  # 0100/bottom
            x = vx + (1 / m) * (self.viewport_ymax - vy) if m else vx
            y = self.viewport_ymax
        if cs_value & 8:  # 1000/top
            x = vx + (1 / m) * (self.viewport_ymin - vy) if m else vx
            y = self.viewport_ymin

        return x, y

    def liang_barsky(self, vx1: float, vy1: float, vx2: float, vy2: float):
        """
        Liang-Barsky line clipping algorithm.
        """
        delta_x = vx2 - vx1
        delta_y = vy2 - vy1

        p = [-delta_x, delta_x, -delta_y, delta_y]

        q = [
            vx1 - self.viewport_xmin,
            self.viewport_xmax - vx1,
            vy1 - self.viewport_ymin,
            self.viewport_ymax - vy1,
        ]

        zeta1 = 0
        zeta2 = 1
        for i in range(4):
            if p[i] == 0:  # parallel to a limit
                if q[i] < 0:  # outside the limits
                    return None
            else:
                r = q[i] / p[i]
                if p[i] < 0:  # outside --> in
                    zeta1 = max(zeta1, r)
                else:  # inside --> out
                    zeta2 = min(zeta2, r)

        x1, y1 = vx1, vy1
        x2, y2 = vx2, vy2

        if zeta1 > zeta2:
            return None
        if zeta1 != 0:
            x1 = vx1 + zeta1 * delta_x
            y1 = vy1 + zeta1 * delta_y
        if zeta2 != 1:
            x2 = vx1 + zeta2 * delta_x
            y2 = vy1 + zeta2 * delta_y

        return x1, y1, x2, y2

    def polygon_clipping(self, painter: QPainter, obj: Wireframe):
        """
        Currently only Sutherland-Hodgman algorithm is implemented, however, the algoritm is open to expansion using other clipping algorithms.
        """
        self.sutherland_hodgman(painter, obj)

    def sutherland_hodgman(self, painter: QPainter, obj: Wireframe):
        """
        Sutherland-Hodgman polygon clipping algorithm.
        """
        points = [self.transform_coords(x, y) for x, y in obj.coordinates]
        if all(point != (None, None) for point in points):
            edges = ["LEFT", "RIGHT", "BOTTOM", "TOP"]

            clipped_points = points

            for edge in edges:
                input_list = clipped_points
                clipped_points = []
                for i in range(len(input_list)):
                    current_point = input_list[i]
                    next_point = input_list[(i + 1) % len(input_list)]

                    x1, y1 = current_point
                    x2, y2 = next_point
                    if self.sutherland_hogdman_inside(x1, y1, edge):
                        clipped_points.append((x1, y1))
                        if not self.sutherland_hogdman_inside(x2, y2, edge):
                            clipped_points.append(
                                self.sutherland_hodgman_redraw(x1, y1, x2, y2, edge)
                            )
                    elif self.sutherland_hogdman_inside(x2, y2, edge):
                        clipped_points.append(
                            self.sutherland_hodgman_redraw(x1, y1, x2, y2, edge)
                        )

            if len(clipped_points) >= 3:
                qpoints = [QPointF(x, y) for x, y in clipped_points]
                painter.drawPolygon(*qpoints)

    def sutherland_hogdman_inside(self, x: float, y: float, edge: str) -> bool:
        """
        Check if the point is inside the edge.
        """
        if edge == "LEFT":
            return x >= self.viewport_xmin
        elif edge == "RIGHT":
            return x <= self.viewport_xmax
        elif edge == "BOTTOM":
            return y <= self.viewport_ymax
        elif edge == "TOP":
            return y >= self.viewport_ymin
        else:
            return False

    def sutherland_hodgman_redraw(
        self, x1: float, y1: float, x2: float, y2: float, edge: str
    ):
        """
        Redraw the point according to the Sutherland-Hodgman algorithm.
        """
        vx = x2 - x1
        vy = y2 - y1
        x, y = 0, 0
        if edge == "LEFT":
            x = self.viewport_xmin
            y = y1 + vy * (self.viewport_xmin - x1) / vx if vx != 0 else y1
        elif edge == "RIGHT":
            x = self.viewport_xmax
            y = y1 + vy * (self.viewport_xmax - x1) / vx if vx != 0 else y1
        elif edge == "BOTTOM":
            y = self.viewport_ymax
            x = x1 + vx * (self.viewport_ymax - y1) / vy if vy != 0 else x1
        elif edge == "TOP":
            y = self.viewport_ymin
            x = x1 + vx * (self.viewport_ymin - y1) / vy if vy != 0 else x1
        return x, y

    def bezier(self, x1, y1, x2, y2, x3, y3, x4, y4, precision=100):
        """
        Creates the points for the bezier curve method
        """

        cx, cy = create_bezier_matrix([x1, y1], [x2, y2], [x3, y3], [x4, y4])

        points = []
        for i in range(precision + 1):
            t = i / precision

            t_matrix = np.matrix([[t**3, t**2, t, 1]])

            x = float(t_matrix @ cx)
            y = float(t_matrix @ cy)

            points.append((x, y))

        return points

    def check_bezier_continuity(self, points: list) -> bool:
        """
        Checks if there is G(0) continuity in the curves
        """
        if len(points) < 7:  # At least two segments
            return True

        for i in range(0, len(points) - 3, 4):
            if i + 4 >= len(points):
                break

            end_point = points[i + 3]
            next_start = points[i + 4]

            if end_point != next_start:
                self.console.log(
                    f"Found discontinuous points: {end_point}, {next_start}"
                )
                return False

        return True

    def b_spline(
        self, x1, y1, x2, y2, x3, y3, x4, y4, precision=100
    ) -> list[tuple[float, float]]:
        """
        Creates the points for the B-spline curve method using foward differences
        """

        cx, cy = create_b_spline_matrix([x1, y1], [x2, y2], [x3, y3], [x4, y4])
        delta = 1 / precision
        fd = forward_differences_matrix(delta)

        dx = fd @ cx
        dy = fd @ cy

        x: float = dx[0, 0]
        dx1: float = dx[1, 0]
        dx2: float = dx[2, 0]
        dx3: float = dx[3, 0]

        y: float = dy[0, 0]
        dy1: float = dy[1, 0]
        dy2: float = dy[2, 0]
        dy3: float = dy[3, 0]

        points: list[tuple[float, float]] = []
        for _ in range(precision + 1):
            points.append((x, y))
            x += dx1
            dx1 += dx2
            dx2 += dx3

            y += dy1
            dy1 += dy2
            dy2 += dy3

        return points
