from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
)

from ui.canvas import Canvas
from ui.console import Console


class TransformationWindow(QWidget):
    def __init__(self, canvas: Canvas, console: Console, obj_list):
        super().__init__()
        self.canvas = canvas
        self.console = console
        self.obj_list = obj_list
        self.layout = QVBoxLayout()
        self.main_label = QLabel("Transformations")
        self.layout.addWidget(self.main_label)
        self.setLayout(self.layout)

        # Controls for 2D translation
        trans_group = QGroupBox("Translation")
        trans_layout = QHBoxLayout()
        self.dx_input = QLineEdit()
        self.dx_input.setPlaceholderText("dx")
        self.dy_input = QLineEdit()
        self.dy_input.setPlaceholderText("dy")
        self.translate_btn = QPushButton("Apply Translation")
        self.translate_btn.clicked.connect(self.apply_translation)
        trans_layout.addWidget(self.dx_input)
        trans_layout.addWidget(self.dy_input)
        trans_layout.addWidget(self.translate_btn)
        trans_group.setLayout(trans_layout)
        self.layout.addWidget(trans_group)

        # Controls for 2D transformation
        trans_group = QGroupBox("Transformation")
        trans_layout = QHBoxLayout()
        self.dx_transform_input = QLineEdit()
        self.dx_transform_input.setPlaceholderText("dx")
        self.dy_transform_input = QLineEdit()
        self.dy_transform_input.setPlaceholderText("dy")
        self.transform_btn = QPushButton("Apply Transformation")
        self.transform_btn.clicked.connect(self.apply_transformation)
        trans_layout.addWidget(self.dx_transform_input)
        trans_layout.addWidget(self.dy_transform_input)
        trans_layout.addWidget(self.transform_btn)
        trans_group.setLayout(trans_layout)
        self.layout.addWidget(trans_group)

        # Controls for Rotation
        rotate_group = QGroupBox("Rotation")  # Changed variable name
        rotate_layout = QHBoxLayout()  # Changed variable name
        self.angle_input = QLineEdit()  # Changed variable name
        self.angle_input.setPlaceholderText("Angle")
        self.rotate_btn = QPushButton("Apply Rotation")  # Changed variable name
        self.rotate_btn.clicked.connect(self.apply_rotation)
        rotate_layout.addWidget(self.angle_input)
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
        point_row.addWidget(self.point_x_input)
        point_row.addWidget(self.point_y_input)
        rotate_point_layout.addLayout(point_row)

        self.rotate_point_btn = QPushButton("Rotate Around Point")
        self.rotate_point_btn.clicked.connect(self.apply_rotation_in_arbitrary_point)
        rotate_point_layout.addWidget(self.rotate_point_btn)

        rotate_point_group.setLayout(rotate_point_layout)
        self.layout.addWidget(rotate_point_group)

    def apply_translation(self):
        try:
            dx = float(self.dx_input.text())
            dy = float(self.dy_input.text())
        except ValueError:
            self.console.log("Error: Invalid values for translation.")
            return
        selected_items = self.obj_list.selectedItems()
        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.translate_objects(obj, dx, dy)
                    break

        self.console.log(
            f"Translated {len(selected_items)} object(s) by ({dx}, {dy})."
        )

    def apply_transformation(self):
        try:
            dx = float(self.dx_transform_input.text())
            dy = float(self.dy_transform_input.text())
        except ValueError:
            self.console.log("Error: Invalid values for transformation.")
            return
        selected_items = self.obj_list.selectedItems()
        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.transform_objects(obj, dx, dy)
                    break

        self.console.log(
            f"Transformed {len(selected_items)} object(s) by ({dx}, {dy})."
        )

    def apply_rotation(self):
        try:
            angle = float(self.angle_input.text())
        except ValueError:
            self.console.log("Error: Invalid angle for rotation.")
            return
        selected_items = self.obj_list.selectedItems()
        for item in selected_items:
            name = item.text()
            for obj in self.canvas.objects:
                if obj.name == name:
                    self.canvas.rotate_objects(obj, angle)
                    break

        self.console.log(
            f"Rotated {len(selected_items)} object(s) by {angle} degrees."
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
                    self.canvas.rotateInPoint(obj, angle, px, py)
                    break

        self.console.log(
            f"Rotated {len(selected_items)} object(s) by {angle} degrees around point ({px}, {py})."
        )
