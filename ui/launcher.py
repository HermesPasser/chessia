from ui.chessboard import ChessBoardGUI, TITLE
from PyQt5 import Qt, uic
from utils import deserialize

class LauncherUI(Qt.QMainWindow):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.board = ChessBoardGUI(self, game)
        self._initialize_component()

    def _initialize_component(self):
        uic.loadUi("ui/launcher.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(TITLE)
        self.board.setMinimumSize(600, 600)
        self.playButton.clicked.connect(self.open_board)
        self.replayButton.clicked.connect(self.load_match)
        self.difficulty_1.toggled.connect(lambda: self.set_difficulty(2))
        self.difficulty_2.toggled.connect(lambda: self.set_difficulty(3))
        self.difficulty_3.toggled.connect(lambda: self.set_difficulty(4))
        self.difficulty_4.toggled.connect(lambda: self.set_difficulty(5))

    def set_difficulty(self, level):
        self.game.ai_difficulty = level

    def open_board(self):
        if self.game.game_ended:
            self.game.restart()
        
        self.board.show()
        self.hide()

    def load_match(self):
        self.game.restart()
        result = Qt.QFileDialog.getOpenFileName(self, 'Open match to replay', None, "Chessia (*.chessia)")
        if not result[0]:
            return
        
        try:
            moves = deserialize(result[0])
            print(moves)
            self.open_board()
            self.board.replay(moves)
        except Exception as e:
            print(e)

