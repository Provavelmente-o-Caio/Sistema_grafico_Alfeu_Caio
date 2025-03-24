from PyQt6.QtWidgets import QGraphicsEllipseItem


class Point(QGraphicsEllipseItem):
    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name