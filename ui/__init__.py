from PyQt5.Qt import QApplication
from ui.launcher import LauncherUI
import sys

def make_window(game):
    app = QApplication(sys.argv)
    l = LauncherUI(game)
    l.show()
    sys.exit(app.exec_())

modules = [make_window]