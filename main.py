import sys

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QDockWidget,
    QTextEdit,
)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Content layout
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # Sidebar
        self.sidebar = foo("blue")
        self.sidebar.setFixedWidth(250)
        main_layout.addWidget(self.sidebar)

        # Viewport
        self.viewport = foo("green")
        content_layout.addWidget(self.viewport)

        # Terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumHeight(200)
        content_layout.addWidget(self.terminal)

        # teste terminal
        self.terminal.append("oi :)")

        # setting the basic configuration for the window
        self.setWindowTitle("Sistema básico com Window e Viewport")
        self.setMinimumSize(500, 500)
        self.show()


# I guess this will be the layout
class foo(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        self.setMinimumSize(50, 50)


class SideBar:
    pass


class Console:
    pass


class Canvas:
    pass


# Setting the basic class for representing dots, lines and form on the canvas
class Wireframe:
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
