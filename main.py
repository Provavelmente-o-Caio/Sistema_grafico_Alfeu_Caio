import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout

from ui.canvas import Canvas
from ui.console import Console
from ui.sidebar.sidebar import SideBar


# from PyQt6.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Content layout
        content_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)

        # Terminal
        self.console = Console()

        # Canvas (Viewport)
        self.canvas = Canvas(self.console)
        content_layout.addWidget(self.canvas)

        content_layout.addWidget(self.console)
        self.console.log("2D Graphics System initialized")

        # Sidebar with access to canvas and console
        self.sidebar = SideBar(self.canvas, self.console)
        self.sidebar.setFixedWidth(250)
        main_layout.addWidget(self.sidebar)

        # setting the basic configuration for the window
        self.setWindowTitle("Sistema básico com Window e Viewport")
        self.showFullScreen()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
