from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QFileDialog, QRadioButton
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QGroupBox,
    QGridLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
)

from models.wireframe import Wireframe
from ui.canvas import Canvas
from ui.color import Color
from ui.console import Console
from ui.sidebar.transformation_window import TransformationWindow
from utils.types import ObjectType


class SideBar(QWidget):
    def __init__(self, canvas: Canvas, console: Console):
        super().__init__()
        self.canvas = canvas
        self.console = console
        self.tw = None
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

        self.selected_color = QColor("black")  # Default color
        self.color_preview = QWidget()
        self.color_preview.setFixedSize(20, 20)
        self.update_color_preview()

        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        color_layout.addWidget(self.color_preview)

        # Color selection button
        self.select_color_btn = QPushButton("Choose Color")
        self.select_color_btn.clicked.connect(self.choose_color)
        color_layout.addWidget(self.select_color_btn)

        creation_layout.addLayout(color_layout)

        # Add object button
        self.add_obj_btn = QPushButton("Add Object")
        creation_layout.addWidget(self.add_obj_btn)

        creation_group.setLayout(creation_layout)
        layout.addWidget(creation_group)

        # Object list group
        self.obj_list_group = QGroupBox("Object List")
        self.obj_list_layout = QVBoxLayout()

        # Object list
        self.obj_list = QListWidget()
        for obj in self.canvas.objects:
            item = QListWidgetItem(obj.name)
            self.obj_list.addItem(item)
        self.obj_list_layout.addWidget(self.obj_list)

        # Remove object button
        self.rmv_obj_btn = QPushButton("Remove Object")
        self.rmv_obj_btn.clicked.connect(self.remove_object)
        self.obj_list_layout.addWidget(self.rmv_obj_btn)

        # Clear all button
        self.clear_btn = QPushButton("Clear All")
        self.obj_list_layout.addWidget(self.clear_btn)

        # Export objects
        self.export_btn = QPushButton("Export Objects")
        self.export_btn.clicked.connect(self.export_objects)
        self.obj_list_layout.addWidget(self.export_btn)

        # Import objects
        self.import_btn = QPushButton("Import File")
        self.import_btn.clicked.connect(self.import_objects)
        self.obj_list_layout.addWidget(self.import_btn)

        self.obj_list_group.setLayout(self.obj_list_layout)
        layout.addWidget(self.obj_list_group)

        # Transformations
        self.transformation_group = QGroupBox("Transformations")
        self.transformation_layout = QVBoxLayout()

        self.rotation_layout = QHBoxLayout()
        self.rotate_left_window_btn = QPushButton("Rotate <--")
        self.rotate_right_window_btn = QPushButton("Rotate -->")
        self.rotate_left_window_btn.clicked.connect(self.rotate_window_left)
        self.rotate_right_window_btn.clicked.connect(self.rotate_window_right)
        self.rotate_window_input = QLineEdit()

        self.transformation_layout.addWidget(QLabel("Rotation Angle:"))
        self.transformation_layout.addWidget(self.rotate_window_input)
        self.rotation_layout.addWidget(self.rotate_left_window_btn)
        self.rotation_layout.addWidget(self.rotate_right_window_btn)

        self.transformations_btn = QPushButton("Open Transformations")
        self.transformations_btn.clicked.connect(self.show_transformations_window)
        self.transformation_layout.addLayout(self.rotation_layout)
        self.transformation_layout.addWidget(self.transformations_btn)
        self.transformation_group.setLayout(self.transformation_layout)
        layout.addWidget(self.transformation_group)

        # Clipping Algorithm
        self.clipping_group = QGroupBox("Clipping")
        self.clipping_layout = QVBoxLayout()

        self.clipping_label = QLabel("Clipping Algorithm")
        self.line_clipping_algorithm_cs = QRadioButton("Cohen-Sutherland")
        self.line_clipping_algorithm_cs.setChecked(True)
        self.line_clipping_algorithm_lb = QRadioButton("Liang-Barsky")
        self.line_clipping_algorithm_lb.setChecked(False)
        self.line_clipping_algorithm_cs.toggled.connect(self.set_line_clipping_algorithm)
        self.line_clipping_algorithm_lb.toggled.connect(self.set_line_clipping_algorithm)
        self.clipping_layout.addWidget(self.clipping_label)
        self.clipping_layout.addWidget(self.line_clipping_algorithm_cs)
        self.clipping_layout.addWidget(self.line_clipping_algorithm_lb)
        self.clipping_group.setLayout(self.clipping_layout)
        layout.addWidget(self.clipping_group)

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

    def update_color_preview(self):
        self.color_preview.setStyleSheet(
            f"background-color: {self.selected_color.name()}; border: 1px solid #888;"
        )

    def choose_color(self):
        color = Color.get_color(self, self.selected_color)
        if color:
            self.selected_color = color
            self.update_color_preview()

    def add_object(self):
        name = self.obj_name_input.text()
        if not name:
            self.console.log("Error: Object name is required.")
            return

        try:
            coords_str = self.coords_input.text()
            coords = eval(coords_str)
        except Exception as e:
            self.console.log(f"Error parsing coordinates: {e}")
            return

        type_str = self.obj_type_combo.currentText()
        if type_str == "Dot":
            obj_type = ObjectType.DOT
            if all(isinstance(point, float) for point in coords) and len(coords) != 2:
                self.console.log("Error: A dot requires exactly 1 coordinate pair.")
                return
            coords = [coords]
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

        new_obj = Wireframe(name, obj_type, coords)
        new_obj.set_color(self.selected_color)  # Apply selected color
        try:
            if any(new_obj.name == obj.name for obj in self.canvas.objects):
                raise ValueError

            self.canvas.add_object(new_obj)
            self.console.log(f"Added {type_str.lower()}: {name}")
            self.obj_list.addItem(QListWidgetItem(name))
        except ValueError as e:
            self.console.log(f"Error adding object, object {name} already exists")

        # Clear inputs
        self.obj_name_input.clear()
        self.coords_input.clear()

    # Update object list
    def update_object_list(self):
        self.obj_list.clear()
        for obj in self.canvas.objects:
            item = QListWidgetItem(obj.name)
            self.obj_list.addItem(item)

    def remove_object(self):
        selected_items = self.obj_list.selectedItems()
        if not selected_items:
            self.console.log("Error: No object selected.")
            return
        for item in selected_items:
            name = item.text()
            self.canvas.remove_object(name)
            self.obj_list.takeItem(self.obj_list.row(item))
            self.console.log(f"Removed object: {name}")

    def show_transformations_window(self):
        self.tw = TransformationWindow(self.canvas, self.console, self.obj_list)
        self.tw.show()

    def clear_canvas(self):
        self.canvas.clear()
        self.update_object_list()
        self.console.log("Canvas cleared")

    def rotate_window_right(self):
        angle = self.rotate_window_input.text()
        if not angle:
            self.console.log("Error: Rotation angle is required.")
            return
        try:
            angle = float(angle)
            self.canvas.window.rotate(angle)
            self.canvas.update()
            self.console.log(f"Rotating window by {angle} degrees")
        except ValueError:
            self.console.log("Error: Invalid rotation angle.")
            return

    def rotate_window_left(self):
        angle = self.rotate_window_input.text()
        if not angle:
            self.console.log("Error: Rotation angle is required.")
            return
        try:
            angle = -float(angle)
            self.canvas.window.rotate(angle)
            self.canvas.update()
            self.console.log(f"Rotating window by {angle} degrees")
        except ValueError:
            self.console.log("Error: Invalid rotation angle.")
            return

    def export_objects(self):
        if len(self.canvas.objects) > 0:
            self.console.log("Exporting objects")
            self.canvas.export_objects()
        else:
            self.console.log("No objects to be exported.")

    def import_objects(self):

        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Wavefront Files (*.obj);;All Files (*)")

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            if selected_file.endswith(".obj"):
                self.canvas.import_objects(selected_file)
                self.console.log(f"Imported objects from {selected_file}")
                self.update_object_list()
            else:
                self.console.log("Error: Selected file is not a .obj file.")

    def set_line_clipping_algorithm(self, checked):
        line_clipping_algorithm = self.sender()
        if checked:
            self.console.log(f"Setting line clipping algorithm to {line_clipping_algorithm.text()}")
            self.canvas.set_line_clipping_algorithm(line_clipping_algorithm.text())
