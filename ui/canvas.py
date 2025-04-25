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
        self.viewport_xmin = 0
        self.viewport_ymin = 0
        self.viewport_xmax = self.width()
        self.viewport_ymax = self.height()

        self.step = 1.0  # Step size for panning
        self.zoom_factor = 1.2  # Zoom factor

        # Loads the example objects for better utilization of the software
        self.load_example_objects()

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
        self.viewport_xmax = self.width()
        self.viewport_ymax = self.height()
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
        painter.drawRect(20, 20, self.width() - 40, self.height() - 40)  # -2 para compensar a largura da borda

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
                        painter.drawEllipse(int(vx) - 3, int(vy) - 3, 6, 6)

                elif obj.obj_type == ObjectType.LINE:
                    if len(obj.coordinates) >= 2:
                        x1, y1 = obj.coordinates[0]
                        x2, y2 = obj.coordinates[1]
                        vx1, vy1 = self.transform_coords(x1, y1)
                        vx2, vy2 = self.transform_coords(x2, y2)
                        painter.drawLine(int(vx1), int(vy1), int(vx2), int(vy2))


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
