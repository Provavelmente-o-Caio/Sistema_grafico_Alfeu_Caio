from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

from objects.point import Point
from objects.segment import Segment


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(self.renderHints())

        self.window_xmin = -100
        self.window_ymin = -100
        self.window_xmax = 100
        self.window_ymax = 100

        self.viewport_xmin = 0
        self.viewport_ymin = 0
        self.viewport_xmax = 500
        self.viewport_ymax = 500

        self.scale_factor = 1.0
        self.update_view()

    def update_view(self):
        self.setSceneRect(
            self.viewport_xmin,
            self.viewport_ymin,
            self.viewport_xmax,
            self.viewport_ymax,
        )

    def add_segment(self, x1, y1, x2, y2, name):
        segment = Segment(x1, y1, x2, y2, name)
        segment.setPen(QPen(Qt.GlobalColor.black))
        self.scene.addItem(segment)

    def add_point(self, x, y, name):
        point = Point(x, y, name)
        point.setPen(QPen(Qt.GlobalColor.red))
        self.scene.addItem(point)

    def transform_to_viewport(self, xw, yw):
        xvp = (self.viewport_xmax - self.viewport_xmin) * (
            (xw - self.window_xmin) / (self.window_xmax - self.window_xmin)
        )
        yvp = (self.viewport_ymax - self.viewport_ymin) * (
            1 - ((yw - self.window_ymin) / (self.window_ymax - self.window_ymin))
        )
        return xvp, yvp
