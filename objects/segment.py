from PyQt6.QtWidgets import QGraphicsLineItem


class Segment(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, name):
        super().__init__(x1, y1, x2, y2)
        self.name = name