from typing import List
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette
from PyQt6.QtCore import Qt

from models.wireframe import Wireframe
from models.window import Window
from utils.types import ObjectType

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
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

    def add_object(self, wireframe: Wireframe):
        self.objects.append(wireframe)
        self.update()  # Redraw canvas

    def remove_object(self, name: str):
        self.objects = [obj for obj in self.objects if obj.name != name]
        self.update()

    def clear(self):
        self.objects.clear()
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