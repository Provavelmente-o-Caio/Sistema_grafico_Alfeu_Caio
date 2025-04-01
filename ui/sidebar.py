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
from PyQt6.QtGui import QColor, QPalette

from utils.types import ObjectType
from models.wireframe import Wireframe
from ui.canvas import Canvas
from ui.console import Console
from ui.color import Color


class SideBar(QWidget):
    def __init__(self, canvas: Canvas, console: Console):
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

        # Clear all button
        self.clear_btn = QPushButton("Clear All")
        creation_layout.addWidget(self.clear_btn)

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

        self.obj_list_group.setLayout(self.obj_list_layout)
        layout.addWidget(self.obj_list_group)

        # Controls for 2D translation
        trans_group = QGroupBox("Translação")
        trans_layout = QHBoxLayout()
        self.dx_input = QLineEdit()
        self.dx_input.setPlaceholderText("dx")
        self.dy_input = QLineEdit()
        self.dy_input.setPlaceholderText("dy")
        self.translate_btn = QPushButton("Aplicar Translação")
        self.translate_btn.clicked.connect(self.apply_translation)
        trans_layout.addWidget(self.dx_input)
        trans_layout.addWidget(self.dy_input)
        trans_layout.addWidget(self.translate_btn)
        trans_group.setLayout(trans_layout)
        layout.addWidget(trans_group)

        # Controles para Transformação 2D
        trans_group = QGroupBox("Transformação")
        trans_layout = QHBoxLayout()
        self.dx_transform_input = QLineEdit()
        self.dx_transform_input.setPlaceholderText("dx")
        self.dy_transform_input = QLineEdit()
        self.dy_transform_input.setPlaceholderText("dy")
        self.transform_btn = QPushButton("Aplicar Transformação")
        self.transform_btn.clicked.connect(self.apply_transformation)
        trans_layout.addWidget(self.dx_transform_input)
        trans_layout.addWidget(self.dy_transform_input)
        trans_layout.addWidget(self.transform_btn)
        trans_group.setLayout(trans_layout)
        layout.addWidget(trans_group)

        # Controls for Rotation
        rotate_group = QGroupBox("Rotação")
        rotate_layout = QHBoxLayout()
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Angle")
        self.rotate_btn = QPushButton("Aplicar Rotação")
        self.rotate_btn.clicked.connect(self.apply_rotation)
        rotate_layout.addWidget(self.angle_input)
        rotate_layout.addWidget(self.rotate_btn)
        rotate_group.setLayout(rotate_layout)
        layout.addWidget(rotate_group)

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

        # Parse coordinates
        try:
            coords_str = self.coords_input.text()
            coords = eval(coords_str)
        except Exception as e:
            self.console.log(f"Error parsing coordinates: {e}")
            return

        # Get object type
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
        self.canvas.add_object(new_obj)
        self.console.log(f"Added {type_str.lower()}: {name}")

        # Clear inputs
        self.obj_name_input.clear()
        self.coords_input.clear()

        # Update object list
        self.obj_list.addItem(QListWidgetItem(name))

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

    def apply_translation(self):
        try:
            dx = float(self.dx_input.text())
            dy = float(self.dy_input.text())
        except ValueError:
            self.console.log("Error: Valores inválidos para translação.")
            return
        self.canvas.translate_objects(dx, dy)
        self.console.log(f"Transladou os objetos por ({dx}, {dy}).")

    def apply_transformation(self):
        try:
            dx = float(self.dx_transform_input.text())
            dy = float(self.dy_transform_input.text())
        except ValueError:
            self.console.log("Error: Valores inválidos para transformação.")
            return
        self.canvas.transform_objects(dx, dy)
        self.console.log(f"Transformou os objetos por ({dx}, {dy}).")

    def apply_rotation(self):
        try:
            angle = float(self.angle_input.text())
        except ValueError:
            self.console.log("Error: Invalid angle for rotation.")
            return
        self.canvas.rotate_objects(angle)
        self.console.log(f"Rotacionou os objetos em {angle} graus.")

    def clear_canvas(self):
        self.canvas.clear()
        self.update_object_list()
        self.console.log("Canvas cleared")
