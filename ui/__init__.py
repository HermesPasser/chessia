from ui.chessboard import ChessBoardGUI
from PyQt5.Qt import QApplication
import sys

def make_window(game):
    app = QApplication(sys.argv)
    w = ChessBoardGUI(game)
    w.setMinimumSize(600, 600)
    w.show()
    sys.exit(app.exec_())

modules = [make_window]