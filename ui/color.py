from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QColorDialog,
    QGridLayout,
    QWidget
)
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtCore import pyqtSignal, Qt

# This class is responsible for displaying a color preview system
class ColorPreview(QWidget):
    def __init__(self, color=QColor("black"), size=30):
        super().__init__()
        self.color = color
        self.size = size
        self.setFixedSize(size, size)
        self.update_color(color)
    
    def update_color(self, color):
        self.color = color
        self.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #888;")
        self.update()

# This is the dialog with a color picker with a manual RGB and Hex input 
class ColorPicker(QDialog):
    colorSelected = pyqtSignal(QColor)
    
    def __init__(self, initial_color=QColor("black"), parent=None):
        super().__init__(parent)
        self.setWindowTitle("Color Selector")
        self.current_color = initial_color
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Color preview
        preview_layout = QHBoxLayout()
        preview_label = QLabel("Current Color:")
        self.color_preview = ColorPreview(self.current_color)
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.color_preview)
        preview_layout.addStretch()
        main_layout.addLayout(preview_layout)
        
        # RGB input
        rgb_layout = QGridLayout()
        
        # Red
        rgb_layout.addWidget(QLabel("R:"), 0, 0)
        self.red_input = QLineEdit(str(self.current_color.red()))
        self.red_input.setMaxLength(3)
        self.red_input.textChanged.connect(self.update_from_rgb)
        rgb_layout.addWidget(self.red_input, 0, 1)
        
        # Green
        rgb_layout.addWidget(QLabel("G:"), 1, 0)
        self.green_input = QLineEdit(str(self.current_color.green()))
        self.green_input.setMaxLength(3)
        self.green_input.textChanged.connect(self.update_from_rgb)
        rgb_layout.addWidget(self.green_input, 1, 1)
        
        # Blue
        rgb_layout.addWidget(QLabel("B:"), 2, 0)
        self.blue_input = QLineEdit(str(self.current_color.blue()))
        self.blue_input.setMaxLength(3)
        self.blue_input.textChanged.connect(self.update_from_rgb)
        rgb_layout.addWidget(self.blue_input, 2, 1)
        
        main_layout.addLayout(rgb_layout)
        
        # Hex input
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("Hex:"))
        self.hex_input = QLineEdit(self.current_color.name())
        self.hex_input.setMaxLength(7)  # #RRGGBB format
        self.hex_input.textChanged.connect(self.update_from_hex)
        hex_layout.addWidget(self.hex_input)
        main_layout.addLayout(hex_layout)
        
        # Button to open color dialog
        color_dialog_btn = QPushButton("Open Color Picker")
        color_dialog_btn.clicked.connect(self.open_color_dialog)
        main_layout.addWidget(color_dialog_btn)
        
        # Common colors palette
        colors_layout = QGridLayout()
        common_colors = [
            QColor("red"), QColor("green"), QColor("blue"),
            QColor("cyan"), QColor("darkorange"), QColor("yellow"),
            QColor("black"), QColor("orchid"), QColor("gray")
        ]
        
        row, col = 0, 0
        for color in common_colors:
            color_btn = QPushButton()
            color_btn.setFixedSize(30, 30)
            color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #888;")
            color_btn.clicked.connect(lambda checked, c=color: self.set_color(c))
            colors_layout.addWidget(color_btn, row, col)
            col += 1
            if col > 2:  # 3 colors per row
                col = 0
                row += 1
                
        main_layout.addLayout(colors_layout)
        
        # Accept/Cancel buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)
        
        self.setMinimumWidth(300)
        
    def open_color_dialog(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.set_color(color)
    
    def update_from_rgb(self):
        try:
            r = min(max(int(self.red_input.text() or 0), 0), 255)
            g = min(max(int(self.green_input.text() or 0), 0), 255)
            b = min(max(int(self.blue_input.text() or 0), 0), 255)
            
            self.set_color(QColor(r, g, b), update_rgb=False)
        except ValueError:
            pass  # Ignore invalid input
    
    def update_from_hex(self):
        hex_code = self.hex_input.text()
        if hex_code.startswith('#') and len(hex_code) == 7:  # Valid hex format
            color = QColor(hex_code)
            if color.isValid():
                self.set_color(color, update_hex=False)
    
    def set_color(self, color, update_rgb=True, update_hex=True):
        if not color.isValid():
            return
            
        self.current_color = color
        self.color_preview.update_color(color)
        
        # Update RGB inputs if needed
        if update_rgb:
            self.red_input.setText(str(color.red()))
            self.green_input.setText(str(color.green()))
            self.blue_input.setText(str(color.blue()))
        
        # Update hex input if needed
        if update_hex:
            self.hex_input.setText(color.name())
    
    def get_color(self):
        return self.current_color
    
    def accept(self):
        self.colorSelected.emit(self.current_color)
        super().accept()


class Color:
    @staticmethod
    def get_color(parent=None, initial_color=QColor("black")):
        dialog = ColorPicker(initial_color, parent)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_color()
            
        return None