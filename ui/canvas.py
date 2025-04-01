from typing import List
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette
from PyQt6.QtCore import Qt

from models.wireframe import Wireframe
from models.window import Window
from utils.types import ObjectType

class Canvas(QWidget):
    def __init__(self, console):
        super().__init__()
        self.console = console
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
        
        self.load_example_objects()

    def add_object(self, wireframe: Wireframe):
        self.objects.append(wireframe)
        self.update()  # Redraw canvas
        
    def load_example_objects(self):
        # Exemplo: Ponto (Dot)
        dot = Wireframe("Dot Example", ObjectType.DOT, [(0, 0)])
        dot.set_color(QColor("red"))
        self.add_object(dot)

        # Exemplo: Linha (Line)
        line = Wireframe("Line Example", ObjectType.LINE, [(-5, -5), (5, 5)])
        line.set_color(QColor("green"))
        self.add_object(line)

        # Exemplo: Polígono (Polygon)
        triangle = Wireframe("Polygon Example", ObjectType.POLYGON, [(0, 0), (5, 8), (-5, 8)])
        triangle.set_color(QColor("blue"))
        self.add_object(triangle)
        
        # Exemplo: Polígono (Polygon)
        square = Wireframe("Polygon Example", ObjectType.POLYGON, [(-5, -5), (5, -5), (5, 5), (-5, 5)])
        square.set_color(QColor("blue"))
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

    # Window to Viewport transformation
    def transform_coords(self, xw, yw):
        xvp = (self.viewport_xmax - self.viewport_xmin) * (
            (xw - self.window.xmin) / (self.window.xmax - self.window.xmin)
        )
        yvp = (self.viewport_ymax - self.viewport_ymin) * (
            1 - ((yw - self.window.ymin) / (self.window.ymax - self.window.ymin))
        )
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


        # Draw all wireframe objects
        for obj in self.objects:
            try:
                # Set color for drawing
                pen = QPen(obj.color)
                if obj.is_selected:
                    pen.setWidth(2)  # Make selected objects more visible
                painter.setPen(pen)

                if obj.obj_type == ObjectType.DOT:
                    # Draw a point (small circle)
                    if len(obj.coordinates) > 0:
                        x, y = obj.coordinates[0]
                        vx, vy = self.transform_coords(x, y)
                        painter.drawEllipse(int(vx) - 3, int(vy) - 3, 6, 6)

                elif obj.obj_type == ObjectType.LINE:
                    # Draw a line
                    if len(obj.coordinates) >= 2:
                        x1, y1 = obj.coordinates[0]
                        x2, y2 = obj.coordinates[1]
                        vx1, vy1 = self.transform_coords(x1, y1)
                        vx2, vy2 = self.transform_coords(x2, y2)
                        painter.drawLine(int(vx1), int(vy1), int(vx2), int(vy2))


                elif obj.obj_type == ObjectType.POLYGON:
                    # Draw a polygon as a series of connected lines
                    if len(obj.coordinates) >= 3:
                        # Draw edges instead of using drawPolygon
                        for i in range(len(obj.coordinates)):
                            x1, y1 = obj.coordinates[i]
                            x2, y2 = obj.coordinates[(i + 1) % len(obj.coordinates)]
                            vx1, vy1 = self.transform_coords(x1, y1)
                            vx2, vy2 = self.transform_coords(x2, y2)
                            painter.drawLine(int(vx1), int(vy1), int(vx2), int(vy2))
            except OverflowError as e:
                self.console.log(f"{obj.name} não desenhado no viewport, ocorreu overflow")