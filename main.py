import sys
from enum import Enum
from typing import List, Tuple

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QDockWidget,
    QTextEdit,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QGroupBox,
    QGridLayout,
)

from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QColor, QPalette, QPainter, QPen


class ObjectType(Enum):
    DOT = 1
    LINE = 2
    POLYGON = 3


# Window class to represent the coordinate system of the world
class Window:
    def __init__(self, xmin=-10, ymin=-10, xmax=10, ymax=10):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def width(self):
        return self.xmax - self.xmin

    def height(self):
        return self.ymax - self.ymin

    # Pan the window
    def pan(self, dx, dy):
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy

    # Zoom the window (centered zoom)
    def zoom(self, factor):
        # Calculate center point
        xcenter = (self.xmin + self.xmax) / 2
        ycenter = (self.ymin + self.ymax) / 2

        # Calculate new width and height
        new_width = self.width() * factor
        new_height = self.height() * factor

        # Set new boundaries
        self.xmin = xcenter - new_width / 2
        self.xmax = xcenter + new_width / 2
        self.ymin = ycenter - new_height / 2
        self.ymax = ycenter + new_height / 2


# Setting the basic class for representing dots, lines and form on the canvas
class Wireframe:
    def __init__(
        self, name: str, obj_type: ObjectType, coordinates: List[Tuple[float, float]]
    ):
        self.name = name
        self.obj_type = obj_type
        self.coordinates = coordinates
        self.color = QColor("black")  # Default color
        self.is_selected = False

    def set_color(self, color: QColor):
        self.color = color

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False


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


class SideBar(QWidget):
    def __init__(self, canvas, console):
        super().__init__()
        self.canvas = canvas
        self.console = console
        self.setAutoFillBackground(True)

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("lightgray"))
        self.setPalette(palette)

        # Add sidebar layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Navigation controls
        nav_group = QGroupBox("Navigation")
        nav_layout = QGridLayout()

        # Panning controls
        self.pan_up_btn = QPushButton("↑")
        self.pan_down_btn = QPushButton("↓")
        self.pan_left_btn = QPushButton("←")
        self.pan_right_btn = QPushButton("→")

        nav_layout.addWidget(self.pan_up_btn, 0, 1)
        nav_layout.addWidget(self.pan_left_btn, 1, 0)
        nav_layout.addWidget(self.pan_right_btn, 1, 2)
        nav_layout.addWidget(self.pan_down_btn, 2, 1)

        # Zoom controls
        self.zoom_in_btn = QPushButton("Zoom In (+)")
        self.zoom_out_btn = QPushButton("Zoom Out (-)")

        nav_layout.addWidget(self.zoom_in_btn, 3, 0, 1, 3)
        nav_layout.addWidget(self.zoom_out_btn, 4, 0, 1, 3)

        nav_group.setLayout(nav_layout)
        layout.addWidget(nav_group)

        # Object creation controls
        creation_group = QGroupBox("Add Object")
        creation_layout = QVBoxLayout()

        # Object type selection
        self.obj_type_combo = QComboBox()
        self.obj_type_combo.addItems(["Dot", "Line", "Polygon"])
        creation_layout.addWidget(QLabel("Object Type:"))
        creation_layout.addWidget(self.obj_type_combo)

        # Object name
        self.obj_name_input = QLineEdit()
        creation_layout.addWidget(QLabel("Object Name:"))
        creation_layout.addWidget(self.obj_name_input)

        # Coordinates input
        self.coords_input = QLineEdit()
        creation_layout.addWidget(QLabel("Coordinates (x1,y1),(x2,y2),...:"))
        creation_layout.addWidget(self.coords_input)

        # Add object button
        self.add_obj_btn = QPushButton("Add Object")
        creation_layout.addWidget(self.add_obj_btn)

        # Clear all button
        self.clear_btn = QPushButton("Clear All")
        creation_layout.addWidget(self.clear_btn)

        creation_group.setLayout(creation_layout)
        layout.addWidget(creation_group)

        # Connect signals to slots
        self.pan_up_btn.clicked.connect(lambda: self.canvas.pan(0, 1))
        self.pan_down_btn.clicked.connect(lambda: self.canvas.pan(0, -1))
        self.pan_left_btn.clicked.connect(lambda: self.canvas.pan(-1, 0))
        self.pan_right_btn.clicked.connect(lambda: self.canvas.pan(1, 0))
        self.zoom_in_btn.clicked.connect(self.canvas.zoom_in)
        self.zoom_out_btn.clicked.connect(self.canvas.zoom_out)
        self.add_obj_btn.clicked.connect(self.add_object)
        self.clear_btn.clicked.connect(self.clear_canvas)

        self.setMinimumSize(200, 300)

    def add_object(self):
        name = self.obj_name_input.text()
        if not name:
            self.console.log("Error: Object name is required.")
            return

        # Parse coordinates
        try:
            coords_str = self.coords_input.text()
            coords = list(eval(coords_str))
        except Exception as e:
            self.console.log(f"Error parsing coordinates: {e}")
            return

        # Get object type
        type_str = self.obj_type_combo.currentText()
        if type_str == "Dot":
            obj_type = ObjectType.DOT
            if len(coords) != 1:
                self.console.log("Error: A dot requires exactly 1 coordinate pair.")
                return
        elif type_str == "Line":
            obj_type = ObjectType.LINE
            if len(coords) != 2:
                self.console.log("Error: A line requires exactly 2 coordinate pairs.")
                return
        elif type_str == "Polygon":
            obj_type = ObjectType.POLYGON
            if len(coords) < 3:
                self.console.log(
                    "Error: A polygon requires at least 3 coordinate pairs."
                )
                return

        # Create and add the object
        new_obj = Wireframe(name, obj_type, coords)
        self.canvas.add_object(new_obj)
        self.console.log(f"Added {type_str.lower()}: {name}")

        # Clear inputs
        self.obj_name_input.clear()
        self.coords_input.clear()

    def clear_canvas(self):
        self.canvas.clear()
        self.console.log("Canvas cleared")


class Console(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumHeight(200)

    def log(self, message: str):
        self.append(message)


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

        # Canvas (Viewport)
        self.canvas = Canvas()
        content_layout.addWidget(self.canvas)

        # Terminal
        self.console = Console()
        content_layout.addWidget(self.console)
        self.console.log("2D Graphics System initialized")

        # Sidebar with access to canvas and console
        self.sidebar = SideBar(self.canvas, self.console)
        self.sidebar.setFixedWidth(250)
        main_layout.addWidget(self.sidebar)

        # setting the basic configuration for the window
        self.setWindowTitle("Sistema básico com Window e Viewport")
        self.setMinimumSize(800, 600)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
