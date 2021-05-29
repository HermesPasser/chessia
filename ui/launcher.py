from ui.chessboard import ChessBoardGUI, TITLE
from PyQt5 import QtWidgets, uic
from utils import make_position_array

class LauncherUI(QtWidgets.QDialog):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.board = ChessBoardGUI(self, game)
        self.editbox = QtWidgets.QPlainTextEdit()
        self._initialize_component()

    def _initialize_component(self):
        uic.loadUi("ui/launcher.ui", self)
        self.setWindowTitle(TITLE)
        self.board.setMinimumSize(600, 600)
        self.playButton.clicked.connect(self.open_board)
        self.replayButton.clicked.connect(self.open_replay_editbox)
        self.difficulty_1.toggled.connect(lambda: self.set_difficulty(2))
        self.difficulty_2.toggled.connect(lambda: self.set_difficulty(3))
        self.difficulty_3.toggled.connect(lambda: self.set_difficulty(4))
        self.difficulty_4.toggled.connect(lambda: self.set_difficulty(5))
        self.editbox.setWindowTitle('Replay')
        self.editbox.setPlainText("6x5-5x5\n1x4-3x4\n6x6-4x6\n0x3-4x7")
        self.editbox.closeEvent = self.start_replay

    def set_difficulty(self, level):
        self.game.ai_difficulty = level

    def open_board(self):
        if self.game.game_ended:
            self.game.restart()
        
        self.board.show()
        self.hide()

    def open_replay_editbox(self):
        self.editbox.show()

    def start_replay(self, e):
        self.game.restart()
        try:
            ar = make_position_array(self.editbox.toPlainText().strip())
            self.open_board()
            self.board.replay(ar)
        except Exception as e:
            print(e)