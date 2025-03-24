from PyQt6.QtWidgets import QTextEdit

class Console(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumHeight(200)

    def log(self, message: str):
        self.append(message)