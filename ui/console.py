from PyQt6.QtWidgets import QTextEdit

class Console(QTextEdit):
    """
    Console widget that inherits from QTextEdit.
    """
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumHeight(200)

    def log(self, message: str):
        """
        Writes a message on the console.
        """
        self.append(message)