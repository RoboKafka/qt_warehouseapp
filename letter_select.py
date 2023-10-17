from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal
class LetterButton(QPushButton):
    letterSelected = Signal(str)  # Custom signal to emit the selected letter

    def __init__(self, letter, parent=None):
        super(LetterButton, self).__init__(letter, parent)
        self.letter = letter
        self.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        # Emit the custom signal with the selected letter
        self.letterSelected.emit(self.letter)