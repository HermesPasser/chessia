from engine.game import ChessException
from PyQt5 import Qt

class Worker(Qt.QObject):
    start = Qt.pyqtSignal()
    progress = Qt.pyqtSignal(object, object, str)
    finished = Qt.pyqtSignal()

    @staticmethod
    def make_ai_worker(game):
        w = Worker(game)
        w.thread.started.connect(w.run_ai)
        return w

    def __init__(self, game):
        Qt.QObject.__init__(self)
        self.game = game

        self.thread = Qt.QThread()
        self.moveToThread(self.thread)
        self.finished.connect(self.thread.quit)
        self.finished.connect(self.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def start(self):
        self.thread.start()

    def run_ai(self):
        message = None
        try:
            from_pos, to = self.game.play_turn_ia_start()
        except ChessException as e:
            message = str(e)
        
        if from_pos and to:
            self.progress.emit(from_pos, to, message)
        self.finished.emit()
