from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
)

from models.wireframe import Wireframe
from models.wireframe_3d import Wireframe_3D
from ui.canvas import Canvas
from ui.console import Console


class TransformationWindow(QWidget):
    def __init__(self, canvas: Canvas, console: Console, obj_list):
        super().__init__()
        self.canvas: Canvas = canvas
        self.console: Console = console
        self.obj_list = obj_list
        self.layout = QVBoxLayout()
        self.main_label: QLabel = QLabel("Transformations")
        self.layout.addWidget(self.main_label)
        self.setLayout(self.layout)

        # Controls for 3D translation
        trans_group = QGroupBox("Translation")
        trans_layout = QHBoxLayout()
        self.dx_input = QLineEdit()
        self.dx_input.setPlaceholderText("dx")
        self.dy_input = QLineEdit()
        self.dy_input.setPlaceholderText("dy")
        self.dz_input = QLineEdit()
        self.dz_input.setPlaceholderText("dz")
        self.translate_btn = QPushButton("Apply Translation")
        self.translate_btn.clicked.connect(self.apply_translation)
        trans_layout.addWidget(self.dx_input)
        trans_layout.addWidget(self.dy_input)
        trans_layout.addWidget(self.dz_input)
        trans_layout.addWidget(self.translate_btn)
        trans_group.setLayout(trans_layout)
        self.layout.addWidget(trans_group)

        # Controls for 3D transformation
        trans_group = QGroupBox("Transformation")
        trans_layout = QHBoxLayout()
        self.dx_transform_input = QLineEdit()
        self.dx_transform_input.setPlaceholderText("dx")
        self.dy_transform_input = QLineEdit()
        self.dy_transform_input.setPlaceholderText("dy")
        self.dz_transform_input = QLineEdit()
        self.dz_transform_input.setPlaceholderText("dz")
        self.transform_btn = QPushButton("Apply Transformation")
        self.transform_btn.clicked.connect(self.apply_transformation)
        trans_layout.addWidget(self.dx_transform_input)
        trans_layout.addWidget(self.dy_transform_input)
        trans_layout.addWidget(self.dz_transform_input)
        trans_layout.addWidget(self.transform_btn)
        trans_group.setLayout(trans_layout)
        self.layout.addWidget(trans_group)

        # Controls for Rotation
        rotate_group = QGroupBox("Rotation")  # Changed variable name
        rotate_layout = QHBoxLayout()  # Changed variable name
        self.angle_x_input = QLineEdit()  # Changed variable name
        self.angle_x_input.setPlaceholderText("Angle X")
        self.angle_y_input = QLineEdit()  # Changed variable name
        self.angle_y_input.setPlaceholderText("Angle Y")
        self.angle_z_input = QLineEdit()  # Changed variable name
        self.angle_z_input.setPlaceholderText("Angle Z")
        self.rotate_btn = QPushButton("Apply Rotation")  # Changed variable name
        self.rotate_btn.clicked.connect(self.apply_rotation)
        rotate_layout.addWidget(self.angle_x_input)
        rotate_layout.addWidget(self.angle_y_input)
        rotate_layout.addWidget(self.angle_z_input)
        rotate_layout.addWidget(self.rotate_btn)
        rotate_group.setLayout(rotate_layout)
        self.layout.addWidget(rotate_group)

        # Controls for Rotation (with center)
        rotate_center_group = QGroupBox("Rotation Around Center")
        rotate_center_layout = QHBoxLayout()
        self.center_angle_input = QLineEdit()
        self.center_angle_input.setPlaceholderText("Angle (degrees)")
        self.center_rotate_btn = QPushButton("Rotate Around Center")
        self.center_rotate_btn.clicked.connect(self.apply_rotation_in_center)
        rotate_center_layout.addWidget(self.center_angle_input)
        rotate_center_layout.addWidget(self.center_rotate_btn)
        rotate_center_group.setLayout(rotate_center_layout)
        self.layout.addWidget(rotate_center_group)

        # Controls for Rotation around arbitrary point
        rotate_point_group = QGroupBox("Rotation Around Point")
        rotate_point_layout = QVBoxLayout()

        angle_row = QHBoxLayout()
        angle_row.addWidget(QLabel("Angle:"))
        self.point_angle_input = QLineEdit()
        self.point_angle_input.setPlaceholderText("Degrees")
        angle_row.addWidget(self.point_angle_input)
        rotate_point_layout.addLayout(angle_row)

        point_row = QHBoxLayout()
        point_row.addWidget(QLabel("Center:"))
        self.point_x_input = QLineEdit()
        self.point_x_input.setPlaceholderText("X")
        self.point_y_input = QLineEdit()
        self.point_y_input.setPlaceholderText("Y")
        self.point_z_input = QLineEdit()
        self.point_z_input.setPlaceholderText("Z")
        point_row.addWidget(self.point_x_input)
        point_row.addWidget(self.point_y_input)
        point_row.addWidget(self.point_z_input)
        rotate_point_layout.addLayout(point_row)

        self.rotate_point_btn = QPushButton("Rotate Around Point")
        self.rotate_point_btn.clicked.connect(self.apply_rotation_in_arbitrary_point)
        rotate_point_layout.addWidget(self.rotate_point_btn)

        rotate_point_group.setLayout(rotate_point_layout)
        self.layout.addWidget(rotate_point_group)
        self.disable_3d()

    def apply_translation(self):
        try:
            dx = float(self.dx_input.text())
            dy = float(self.dy_input.text())
            if self.dz_input.isEnabled():
                dz = float(self.dz_input.text())
            else:
                dz = 0
        except ValueError:
            self.console.log("Error: Invalid values for translation.")
            return
        selected_items = self.obj_list.selectedItems()
        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.translate_objects(obj, dx, dy, dz)
                    break

        self.console.log(
            f"Translated {len(selected_items)} object(s) by ({dx}, {dy})."
        )

    def apply_transformation(self):
        try:
            dx = float(self.dx_transform_input.text())
            dy = float(self.dy_transform_input.text())
            if self.dz_transform_input.isEnabled():
                dz = float(self.dz_transform_input.text())
            else:
                dz = 1
        except ValueError:
            self.console.log("Error: Invalid values for transformation.")
            return
        selected_items = self.obj_list.selectedItems()
        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.transform_objects(obj, dx, dy, dz)
                    break

        self.console.log(
            f"Transformed {len(selected_items)} object(s) by ({dx}, {dy})."
        )

    def apply_rotation(self):
        try:
            if self.angle_x_input.isEnabled() and self.angle_y_input.isEnabled():
                angle_x = float(self.angle_x_input.text())
                angle_y = float(self.angle_y_input.text())
            else:
                angle_x = 0
                angle_y = 0
            angle_z = float(self.angle_z_input.text())
        except ValueError:
            self.console.log("Error: Invalid angle for rotation.")
            return
        selected_items = self.obj_list.selectedItems()
        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.rotate_objects(obj, angle_x, angle_y, angle_z)
                    break

        self.console.log(
            f"Rotated {len(selected_items)} object(s) by {angle_z} degrees."
        )

    def apply_rotation_in_center(self):
        try:
            angle = float(self.center_angle_input.text())
        except ValueError:
            self.console.log("Error: Invalid angle for rotation.")
            return

        selected_items = self.obj_list.selectedItems()
        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.rotateWithCenter(obj, angle)
                    break

        self.console.log(
            f"Rotated {len(selected_items)} object(s) by {angle} degrees around center."
        )

    def apply_rotation_in_arbitrary_point(self):
        try:
            angle = float(self.point_angle_input.text())
            px = float(self.point_x_input.text())
            py = float(self.point_y_input.text())
            pz = float(self.point_z_input.text())
        except ValueError:
            self.console.log("Error: Invalid values for rotation around point.")
            return

        selected_items = self.obj_list.selectedItems()
        if not selected_items:
            self.console.log("Error: No object selected.")
            return

        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.rotateInPoint(obj, angle, px, py, pz)
                    break

        self.console.log(
            f"Rotated {len(selected_items)} object(s) by {angle} degrees around point ({px}, {py})."
        )

    def disable_3d(self):
        selected_items = self.obj_list.selectedItems()
        if not selected_items:
            self.dx_input.setEnabled(False)
            self.dy_input.setEnabled(False)
            self.dz_input.setEnabled(False)
            self.dx_transform_input.setEnabled(False)
            self.dy_transform_input.setEnabled(False)
            self.dz_transform_input.setEnabled(False)
            self.center_angle_input.setEnabled(False)
            self.angle_x_input.setEnabled(False)
            self.angle_y_input.setEnabled(False)
            self.angle_z_input.setEnabled(False)
            self.point_angle_input.setEnabled(False)
            self.point_x_input.setEnabled(False)
            self.point_y_input.setEnabled(False)
            self.point_z_input.setEnabled(False)
        else:
            is_3d = False
            for item in selected_items:
                name = item.text()
                for obj in self.canvas.objects:
                    if obj.name == name:
                        if isinstance(obj, Wireframe_3D):
                            is_3d = True
                            break
            if not is_3d:
                self.dz_input.setEnabled(False)
                self.dz_transform_input.setEnabled(False)
                self.angle_x_input.setEnabled(False)
                self.angle_y_input.setEnabled(False)
                self.point_z_input.setEnabled(False)
