from PyQt5 import Qt

class Button(Qt.QPushButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(text, parent)
        self._bg_color = 'white'
        self._fg_color = 'black'

        font = Qt.QFont("Times", 25, Qt.QFont.Bold)
        self.setFont(font)
        self.setText(text)
        self.set_size(75, 75)

    def set_size(self, width, height):
        self.setMinimumSize(Qt.QSize(int(width), int(height)))

    def set_background(self, color):
        self._bg_color = color
        self._update_style()

    def set_foreground(self, color):
        self._fg_color = color
        self._update_style()

    def _update_style(self):
        self.setStyleSheet(f"background-color: {self._bg_color}; color: {self._fg_color}")
