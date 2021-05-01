from game import ChessException
from PyQt5 import Qt

class Worker(Qt.QObject):
    start = Qt.pyqtSignal()
    progress = Qt.pyqtSignal(object, object, str)
    finished = Qt.pyqtSignal()

    def __init__(self, game):
        Qt.QObject.__init__(self)
        self.game = game
        self.start.connect(self.run)

    def run(self):
        message = None
        try:
            from_pos, to = self.game.play_turn_ia_start()
        except ChessException as e:
            message = str(e)
        
        self.progress.emit(from_pos, to, message)
        self.finished.emit()
