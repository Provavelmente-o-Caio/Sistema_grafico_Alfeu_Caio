import sys

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit,
    QLabel,
)

from canvas import Canvas
from sidebar import Sidebar


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

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(250)
        main_layout.addWidget(self.sidebar)

        # Viewport
        self.viewport = Canvas()
        content_layout.addWidget(QLabel("Viewport"))
        content_layout.addWidget(self.viewport)

        # Terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumHeight(200)
        content_layout.addWidget(QLabel("Terminal"))
        content_layout.addWidget(self.terminal)

        # setting the basic configuration for the window
        self.setWindowTitle("Sistema básico com Window e Viewport")
        self.setMinimumSize(800, 500)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
