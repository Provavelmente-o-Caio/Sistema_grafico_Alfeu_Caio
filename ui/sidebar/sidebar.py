from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QCheckBox, QFileDialog, QRadioButton, QAbstractItemView
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
from models.wireframe_3d import Wireframe_3D
from models.point_3d import Point3D
from models.surface_3d import Surface3D
from models.surface_BSpline import SurfaceBSplineFD
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
        self.add_obj_w = None
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
        self.up_btn = QPushButton("↑")
        self.down_btn = QPushButton("↓")
        self.left_btn = QPushButton("←")
        self.right_btn = QPushButton("→")
        self.foward_btn = QPushButton("↥")
        self.back_btn = QPushButton("↧")

        nav_layout.addWidget(self.up_btn, 0, 1)
        nav_layout.addWidget(self.left_btn, 1, 0)
        nav_layout.addWidget(self.right_btn, 1, 2)
        nav_layout.addWidget(self.down_btn, 2, 1)
        nav_layout.addWidget(self.foward_btn, 2, 0)
        nav_layout.addWidget(self.back_btn, 2, 2)

        # Zoom controls
        self.zoom_in_btn = QPushButton("Zoom (+)")
        self.zoom_out_btn = QPushButton("Zoom (-)")

        nav_layout.addWidget(self.zoom_in_btn, 3, 0)
        nav_layout.addWidget(self.zoom_out_btn, 3, 2)

        # Mode selection button
        self.movement_mode = QRadioButton("Move")
        self.movement_mode.setChecked(True)
        self.rotation_mode = QRadioButton("Rotate")
        self.rotation_mode.setChecked(False)
        self.movement_mode.toggled.connect(self.set_movement_mode)
        self.rotation_mode.toggled.connect(self.set_movement_mode)
        nav_layout.addWidget(self.movement_mode, 4, 0)
        nav_layout.addWidget(self.rotation_mode, 4, 2)

        nav_group.setLayout(nav_layout)
        layout.addWidget(nav_group)

        # Object creation controls
        creation_group = QGroupBox("Add Object")
        creation_layout = QVBoxLayout()

        # Object type selection
        self.obj_type_combo = QComboBox()
        self.obj_type_combo.addItems(
           ["Dot | 2D", "Line | 2D", "Polygon | 2D", "Curve (Bezier) | 2D", "Curve (B-Spline) | 2D", "Polygon | 3D", "Surface (Bezier) | 3D", "Surface (B-Spline) | 3D", "Surface (B-Spline FD) | 3D"]
        )
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

        # Edges input
        self.edges_input = QLineEdit()
        creation_layout.addWidget(QLabel("Edges (0, 1),(0,2),...:"))
        creation_layout.addWidget(self.edges_input)

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

        # Fill checkbox
        self.fill_checkbox = QCheckBox()
        self.fill_checkbox.toggled.connect(self.fill_checkbox_toggled)
        color_layout.addWidget(self.fill_checkbox)

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
        self.obj_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
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

        # Options
        self.options_group = QGroupBox("Options")
        self.options_layout = QVBoxLayout()

        # Clipping algorithm selection
        self.clipping_layout = QVBoxLayout()
        self.clipping_label = QLabel("Clipping Algorithm")
        self.line_clipping_algorithm_cs = QRadioButton("Cohen-Sutherland")
        self.line_clipping_algorithm_cs.setChecked(True)
        self.line_clipping_algorithm_lb = QRadioButton("Liang-Barsky")
        self.line_clipping_algorithm_lb.setChecked(False)
        self.line_clipping_algorithm_cs.toggled.connect(
            self.set_line_clipping_algorithm
        )
        self.line_clipping_algorithm_lb.toggled.connect(
            self.set_line_clipping_algorithm
        )
        self.options_layout.addWidget(self.clipping_label)
        self.options_layout.addWidget(self.line_clipping_algorithm_cs)
        self.options_layout.addWidget(self.line_clipping_algorithm_lb)

        # See curve points
        self.see_curve_points_label = QLabel("Curve Points")
        self.see_curve_points_checkbox = QCheckBox("See Curve Points")
        self.see_curve_points_checkbox.toggled.connect(self.see_curve_points_toggled)
        self.options_layout.addWidget(self.see_curve_points_label)
        self.options_layout.addWidget(self.see_curve_points_checkbox)

        self.options_group.setLayout(self.options_layout)
        layout.addWidget(self.options_group)

        # Projection selection
        self.projection_group = QGroupBox("Projection")
        self.projection_layout = QVBoxLayout()
        self.parallel_orthogonal_projection = QRadioButton("Parallel Projection")
        self.parallel_orthogonal_projection.setChecked(True)
        self.perspective_projection = QRadioButton("Perspective Projection")
        self.perspective_projection.setChecked(False)
        self.parallel_orthogonal_projection.toggled.connect(self.set_projection_mode)
        self.perspective_projection.toggled.connect(self.set_projection_mode)
        self.projection_layout.addWidget(self.parallel_orthogonal_projection)
        self.projection_layout.addWidget(self.perspective_projection)
        self.projection_group.setLayout(self.projection_layout)
        layout.addWidget(self.projection_group)

        # Connect signals to slots
        ## This first part allows repetition
        self.up_btn.setAutoRepeat(True)
        self.down_btn.setAutoRepeat(True)
        self.left_btn.setAutoRepeat(True)
        self.right_btn.setAutoRepeat(True)
        self.foward_btn.setAutoRepeat(True)
        self.back_btn.setAutoRepeat(True)
        self.zoom_in_btn.setAutoRepeat(True)
        self.zoom_out_btn.setAutoRepeat(True)
        ## setting movement
        self.up_btn.clicked.connect(lambda: self.canvas.move(0, 1, 0))
        self.down_btn.clicked.connect(lambda: self.canvas.move(0, -1, 0))
        self.left_btn.clicked.connect(lambda: self.canvas.move(-1, 0, 0))
        self.right_btn.clicked.connect(lambda: self.canvas.move(1, 0, 0))
        self.foward_btn.clicked.connect(lambda: self.canvas.move(0, 0, 1))
        self.back_btn.clicked.connect(lambda: self.canvas.move(0, 0, -1))
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
        coords = []
        edges = []
        if not name:
            self.console.log("Error: Object name is required.").strip()
            return

        # uso de IA:
        # Pode adaptar essa passagem de código para aceitar as entradas anteriores mas também interpretar essa nova? (0,0,0),(1,0,1),(2,0,1),(3,0,0);(0,1,1),(1,1,2),(2,1,2),(3,1,1);(0,2,1),(1,2,2),(2,2,2),(3,2,1);(0,3,0),(1,3,1),(2,3,1),(3,3,0)
        try:
            coords_str = self.coords_input.text().strip()
            if ";" in coords_str:
                coords = []
                rows = coords_str.split(";")
                for row in rows:
                    line = []
                    row = row.strip()
                    if not row:
                        continue
                    points = row.split("),")
                    for i in range(len(points)):
                        pt = points[i].strip()
                        if not pt.endswith(")"):
                            pt += ")"
                        pt = pt.replace("(", "").replace(")", "")
                        x, y, z = map(float, pt.split(","))
                        line.append((x, y, z))
                    coords.append(line)
            else:
                coords = eval(coords_str)
        except Exception as e:
            self.console.log(f"Error parsing coordinates: {e}")
            return
        if self.edges_input.text() != "":
            try:
                edges_str = self.edges_input.text()
                edges = eval(edges_str)
            except Exception as e:
                self.console.log(f"Error parsing edges: {e}")

        type_str = self.obj_type_combo.currentText()
        obj_type = None
        
        if type_str == "Dot | 2D":
            obj_type = ObjectType.DOT
            if (
                len(coords) != 2
                or not isinstance(coords[0], int)
                or not isinstance(coords[1], int)
            ):
                self.console.log("Error: A dot requires exactly 1 coordinate pair.")
                return
            if len(edges) != 0:
                self.console.log("Error: A dot cannot have edges.")
                return
        if type_str == "Line | 2D":
            obj_type = ObjectType.LINE
            if len(coords) != 2 or any(
                not isinstance(point, tuple) or len(point) != 2 for point in coords
            ):
                self.console.log("Error: A line requires exactly 2 coordinate pairs.")
                return
            if len(edges) != 0:
                self.console.log("Error: A line cannot have edges.")
                return
        if type_str == "Polygon | 2D":
            obj_type = ObjectType.POLYGON
            if len(coords) < 3 or any(
                not isinstance(point, tuple) or len(point) != 2 for point in coords
            ):
                self.console.log(
                    "Error: A polygon requires at least 3 coordinate pairs."
                )
                return
            if len(edges) != 0:
                self.console.log("Error: A polygon cannot have edges.")
                return
        if type_str == "Curve (Bezier) | 2D":
            obj_type = ObjectType.CURVE
            if len(coords) % 4 != 0:
                self.console.log("Error: A curve requires 4 coordinate pairs.")
                return
        if type_str == "Curve (B-Spline) | 2D":
            obj_type = ObjectType.CURVE_BSPLINE
            if len(coords) < 4:
                self.console.log(
                    "Error: A B-Spline curve requires at least 4 coordinate pairs."
                )
                return
        if type_str == "Polygon | 3D":
            obj_type = ObjectType.POLYGON_3D
            if len(coords) < 2:
                self.console.log(
                    "Error: A 3D polygon requires at least 2 coordinate groups."
                )
                return
            if len(edges) < 1:
                self.console.log(
                    "Error: A 3D polygon requires at least 1 edge."
                )
                return
        if type_str == "Surface (Bezier) | 3D":
            obj_type = ObjectType.SURFACE_BEZIER
            if len(coords) != 16:
                self.console.log("Error: A Bézier surface requires exactly 16 control points (4x4 grid).")
                return
            control_points = []
            for i in range(4):
                row = []
                for j in range(4):
                    idx = i * 4 + j
                    row.append(Point3D([coords[idx]]))
                control_points.append(row)
            
            new_obj = Surface3D(name, obj_type, control_points)    
        if type_str == "Surface (B-Spline) | 3D":
            obj_type = ObjectType.SURFACE_BSPLINE
            if len(coords) != 16:
                self.console.log("Error: A B-Spline surface requires exactly 16 control points (4x4 grid).")
                return
            control_points = []
            for i in range(4):
                row = []
                for j in range(4):
                    idx = i * 4 + j
                    row.append(Point3D([coords[idx]]))
                control_points.append(row)
            
            new_obj = Surface3D(name, obj_type, control_points)
        if type_str == "Surface (B-Spline FD) | 3D":
            obj_type = ObjectType.SURFACE_BSPLINE_FD
            
            if isinstance(coords, str):
                rows = coords.strip().split(';')
                control_points_matrix = []
                    
                for row_str in rows:
                    if not row_str.strip():
                        continue
                    row_coords = eval(row_str.strip())
                    row_points = []
                    for coord in row_coords:
                        row_points.append(Point3D([coord]))
                    control_points_matrix.append(row_points)
            else:
                control_points_matrix = []
                rows = len(coords)
                cols = len(coords[0]) if rows > 0 else 0
                
                for i in range(rows):
                    row_points = []
                    for j in range(cols):
                        row_points.append(Point3D([coords[i][j]]))
                    control_points_matrix.append(row_points)
                
            rows = len(control_points_matrix)
            cols = len(control_points_matrix[0]) if rows > 0 else 0
                
            if rows < 4 or cols < 4:
                self.console.log("Error: B-Spline FD surface requires at least 4x4 control points.")
                return
            if rows > 20 or cols > 20:
                self.console.log("Error: B-Spline FD surface cannot exceed 20x20 control points.")
                return
                
            
            new_obj = SurfaceBSplineFD(name, control_points_matrix)
            self.console.log(f"Created B-Spline FD surface with {rows}x{cols} control points")

        if obj_type:
            if obj_type == ObjectType.DOT:
                coords = [coords]
            if len(edges) == 0:
                new_obj = Wireframe(name, obj_type, coords)
            else:
                points = []
                for coord in coords:
                    points.append(Point3D(coord))
                if len(edges) == 2 and type(edges[0]) != tuple:
                    edges = [edges]
                new_obj = Wireframe_3D(name, obj_type, points, edges)
            new_obj.set_color(self.selected_color)  # Apply selected color
            new_obj.set_fill(self.fill_checkbox.isChecked())  # Apply fill option
            try:
                if any(new_obj.name == obj.name for obj in self.canvas.objects):
                    raise ValueError

                self.canvas.add_object(new_obj)
                self.console.log(f"Added {type_str.lower()}: {name}")
                self.obj_list.addItem(QListWidgetItem(name))
            except ValueError:
                self.console.log(f"Error adding object, object {name} already exists")

            # Clear inputs
            self.obj_name_input.clear()
            self.coords_input.clear()
            self.edges_input.clear()
        else:
            self.console.log("Error: failed to give an object type to the object")

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
            self.canvas.window.rotate_z(angle)
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
            self.canvas.window.rotate_z(angle)
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
                self.canvas.import_objects(
                    selected_file, self.fill_checkbox.isChecked()
                )
                self.console.log(f"Imported objects from {selected_file}")
                self.update_object_list()
            else:
                self.console.log("Error: Selected file is not a .obj file.")

    def set_line_clipping_algorithm(self, checked):
        line_clipping_algorithm = self.sender()
        if checked:
            self.console.log(
                f"Setting line clipping algorithm to {line_clipping_algorithm.text()}"
            )
            self.canvas.set_line_clipping_algorithm(line_clipping_algorithm.text())

    def set_movement_mode(self, checked):
        movement_mode = self.sender()
        if checked:
            self.console.log(f"Setting movement mode to {movement_mode.text()}")
            self.canvas.set_movement_mode(movement_mode.text())

    def fill_checkbox_toggled(self, checked):
        if checked:
            self.console.log("Fill color option enabled")
        else:
            self.console.log("Fill color option disabled")

    def see_curve_points_toggled(self, checked):
        self.canvas.show_control_points = checked
        self.canvas.update()
        if checked:
            self.console.log("Showing curve control points")
        else:
            self.console.log("Hiding curve control points")
        self.canvas.update()

    def set_projection_mode(self, checked):
        projection = self.sender()
        if checked:
            self.console.log(f"Setting projection algorithm to {projection.text()}")
            self.canvas.set_projection_mode(projection.text())
