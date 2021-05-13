from engine.pieces import Queen, Rook, Bishop, Knight
from PyQt5.QtWidgets import QMessageBox
from ui.button import Button

class PromotionDialog():
    def __init__(self, parent=None):
        self.parent = parent
        self.value = None

    def show(self):
        values = [Queen, Rook, Knight, Bishop]

        msgBox = QMessageBox(self.parent)
        msgBox.setText('Promotion dialog')
        msgBox.setWindowTitle('Which piece do you want the pawn to be promoted to?')

        for piece in values:
            msgBox.addButton(Button(str(piece(0)), self.parent), QMessageBox.YesRole)

        self.value = values[msgBox.exec_()]
        return self.value
