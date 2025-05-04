from typing import List

import numpy as np
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette
from PyQt6.QtWidgets import QWidget

from models.window import Window
from models.wireframe import Wireframe
from utils.descritorOBJ import DescritorOBJ
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
        self.objects: List[Wireframe] = []

        # Window and viewport setup
        self.window = Window()
        self.border_width = 200
        self.viewport_xmin = self.border_width
        self.viewport_ymin = self.border_width
        self.viewport_xmax = self.width() - self.border_width
        self.viewport_ymax = self.height() - self.border_width

        self.step = 1.0  # Step size for panning
        self.zoom_factor = 1.2  # Zoom factor

        # Loads the example objects for better utilization of the software
        self.load_example_objects()

        # Setting the line clipping Algorithm
        self.line_clipping_algorithm = "Cohen-Sutherland"

    # Adds a new object in the canvas
    def add_object(self, wireframe: Wireframe):
        try:
            if any(wireframe.name == obj.name for obj in self.objects):
                raise ValueError

            self.objects.append(wireframe)
            self.update()
        except ValueError:
            self.console.log(f"Object {wireframe.name} already exists")

    # Loads the preset objects
    def load_example_objects(self):
        dot = Wireframe("Dot Example", ObjectType.DOT, [(0, 0)])
        dot.set_color(QColor("red"))
        self.add_object(dot)

        line = Wireframe("Line Example", ObjectType.LINE, [(-5, -5), (5, 5)])
        line.set_color(QColor("green"))
        self.add_object(line)

        triangle = Wireframe("Triangle Example", ObjectType.POLYGON, [(0, 0), (5, 8), (-5, 8)])
        triangle.set_color(QColor("blue"))
        self.add_object(triangle)

        square = Wireframe("Square Example", ObjectType.POLYGON, [(-5, -5), (5, -5), (5, 5), (-5, 5)])
        square.set_color(QColor("yellow"))
        self.add_object(square)

    def remove_object(self, name: str):
        self.objects = [obj for obj in self.objects if obj.name != name]
        self.update()

    def clear(self):
        self.objects.clear()
        self.update()

    # This method is responsible for 2D translation.
    # It basically is adding and/or subtracting coordinates to all objects
    def translate_objects(self, dx: float, dy: float):
        for obj in self.objects:
            obj.translate(dx, dy)
        self.update()

    # This method is responsible for 2D transformation.
    # It basically is mutltiplication coordinates to all objects
    def transform_objects(self, dx: float, dy: float):
        for obj in self.objects:
            obj.transform(dx, dy)
        self.update()

    # This method is responsible for 2D rotation
    # It basically is multiplying the objects for sin and cos
    def rotate_objects(self, angle: float):
        for obj in self.objects:
            obj.rotate(angle)
        self.update()

    # This method is responsible for rotating a single object
    def rotateWithCenter(self, object: Wireframe, angle: float):
        cx = object.getCenterObjectX()
        cy = object.getCenterObjectY()

        self.translate_objects(-cx, -cy)
        object.rotate(angle)

        self.translate_objects(cx, cy)

        self.update()

    # This method rotates an object around a specific point
    def rotateInPoint(self, object: Wireframe, angle: float, px: float, py: float):
        object.translate(-px, -py)

        object.rotate(angle)
        object.translate(px, py)

        self.update()

    # Window to Viewport transformation
    def transform_coords(self, xw, yw):
        xn, yn = self.window.world_to_normalized(xw, yw)

        M = self.window.get_transformation_matrix()
        point = np.matrix([xn, yn, 1])
        transformed = point * M
        xt, yt = float(transformed[0, 0]), float(transformed[0, 1])

        xvp = self.viewport_xmin + (self.viewport_xmax - self.viewport_xmin) * ((xt + 1) / 2)
        yvp = self.viewport_ymin + (self.viewport_ymax - self.viewport_ymin) * (1 - ((yt + 1) / 2))

        return xvp, yvp

    def resizeEvent(self, event):
        self.viewport_xmax = self.width() - self.border_width
        self.viewport_ymax = self.height() - self.border_width
        self.update()

    # Pan the window
    def pan(self, dx, dy):
        self.window.pan(dx * self.step, dy * self.step)
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
        border_pen.setWidth(2)  # Largura da borda
        painter.setPen(border_pen)
        painter.drawRect(self.viewport_xmin, self.viewport_ymin, self.viewport_xmax - self.border_width,
                         self.viewport_ymax - self.border_width)

        for obj in self.objects:
            try:
                pen = QPen(obj.color)
                if obj.is_selected:
                    pen.setWidth(2)
                painter.setPen(pen)

                if obj.obj_type == ObjectType.DOT:
                    if len(obj.coordinates) > 0:
                        x, y = obj.coordinates[0]
                        vx, vy = self.transform_coords(x, y)
                        self.point_clipping(painter, vx, vy)

                elif obj.obj_type == ObjectType.LINE:
                    if len(obj.coordinates) >= 2:
                        x1, y1 = obj.coordinates[0]
                        x2, y2 = obj.coordinates[1]
                        vx1, vy1 = self.transform_coords(x1, y1)
                        vx2, vy2 = self.transform_coords(x2, y2)
                        self.line_clipping(painter, vx1, vy1, vx2, vy2)

                elif obj.obj_type == ObjectType.POLYGON:
                    if len(obj.coordinates) >= 3:
                        for i in range(len(obj.coordinates)):
                            x1, y1 = obj.coordinates[i]
                            x2, y2 = obj.coordinates[(i + 1) % len(obj.coordinates)]
                            vx1, vy1 = self.transform_coords(x1, y1)
                            vx2, vy2 = self.transform_coords(x2, y2)
                            painter.drawLine(int(vx1), int(vy1), int(vx2), int(vy2))
            except OverflowError as e:
                self.console.log(f"{obj.name} was not added, OverflowError occurred.")

    def export_objects(self):
        self.descritor.objs = self.objects.copy()
        self.descritor.export_file()

    def import_objects(self, path):
        new_objects = self.descritor.import_file(path)
        for new_object in new_objects:
            self.add_object(new_object)

    def point_clipping(self, painter, vx, vy):
        if self.viewport_xmin <= vx <= self.viewport_xmax and self.viewport_ymin <= vy <= self.viewport_ymax:
            painter.drawEllipse(int(vx) - 3, int(vy) - 3, 6, 6)

    def line_clipping(self, painter, vx1, vy1, vx2, vy2):
        if self.line_clipping_algorithm == "Cohen-Sutherland":
            self.cohen_sutherland(painter, vx1, vy1, vx2, vy2)
        elif self.line_clipping_algorithm == "Liang-Barsky":
            self.liang_barsky(painter, vx1, vy1, vx2, vy2)

    def set_line_clipping_algorithm(self, line_clipping_algorithm):
        self.line_clipping_algorithm = line_clipping_algorithm
        self.update()

    def cohen_sutherland(self, painter, vx1, vy1, vx2, vy2):
        cs_value_p1 = self.cohen_sutherland_point(vx1, vy1)
        cs_value_p2 = self.cohen_sutherland_point(vx2, vy2)
        x1, y1 = vx1, vy1
        x2, y2 = vx2, vy2
        while True:
            if cs_value_p1 & cs_value_p2:
                return
            elif not (cs_value_p1 | cs_value_p2):
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
                return
            else:
                m = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else None
                if cs_value_p1 != 0:
                    x1, y1 = self.cohen_sutherland_redraw(cs_value_p1, x1, y1, m)
                    cs_value_p1 = self.cohen_sutherland_point(x1, y1)
                else:
                    x2, y2 = self.cohen_sutherland_redraw(cs_value_p2, x2, y2, m)
                    cs_value_p2 = self.cohen_sutherland_point(x2, y2)

    def cohen_sutherland_point(self, vx, vy):
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

    def cohen_sutherland_redraw(self, cs_value, vx, vy, m):
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

    def liang_barsky(self, painter, vx1, vy1, vx2, vy2):
        delta_x = vx2 - vx1
        delta_y = vy2 - vy1

        p = [-delta_x, delta_x, -delta_y, delta_y]

        q = [vx1 - self.viewport_xmin, self.viewport_xmax - vx1, vy1 - self.viewport_ymin, self.viewport_ymax - vy1]

        zeta1 = 0
        zeta2 = 1
        for i in range(4):
            if p[i] == 0:  # paralela a um dos limites
                if q[i] < 0:  # fora dos limites
                    return
            else:
                r = q[i] / p[i]
                if p[i] < 0:  # outside --> in
                    zeta1 = max(zeta1, r)
                else:  # inside --> out
                    zeta2 = min(zeta2, r)

        x1, y1 = vx1, vy1
        x2, y2 = vx2, vy2

        if zeta1 > zeta2:
            return
        if zeta1 != 0:
            x1 = vx1 + zeta1 * delta_x
            y1 = vy1 + zeta1 * delta_y
        if zeta2 != 1:
            x2 = vx1 + zeta2 * delta_x
            y2 = vy1 + zeta2 * delta_y

        painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def poligon_clipping(self, painter, obj):  # weiler-atherton
        pass
