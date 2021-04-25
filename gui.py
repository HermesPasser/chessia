import sys
from functools import partial
from PyQt5 import Qt, QtCore, QtWidgets
from position import Position
from utils import make_2d_array
from game import Game, ChessException
from board import Board
from pieces import Piece
from color import Color

TITLE = 'ChessIA'

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
        self.setMinimumSize(Qt.QSize(width, height))

    def set_background(self, color):
        self._bg_color = color
        self._update_style()

    def set_foreground(self, color):
        self._fg_color = color
        self._update_style()

    def _update_style(self):
        self.setStyleSheet(f"background-color: {self._bg_color}; color: {self._fg_color}")

        
class ChessBoardGUI(Qt.QMainWindow):
    resized = QtCore.pyqtSignal()
    
    def __init__(self, game):
        super(ChessBoardGUI, self).__init__()
        self.game = game
        self.start_move = False
        self.selected_spot_pos = None
        self._initialize_component()
  
    def resizeEvent(self, event):
        self.resized.emit()
        super().resizeEvent(event)

    def _initialize_component(self):
        self.resized.connect(self._on_resize)

        centralWidget = Qt.QWidget()
        self.setCentralWidget(centralWidget)
        self.layout = Qt.QGridLayout(centralWidget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self._initialize_board_buttons()
        self.update_ui()

    def _initialize_board_buttons(self):
        self.board_buttons = make_2d_array(range(0, 8), None)    
        for r in range(0, 8):
            for c in range(0, 8):
                bg = 'white' if (r + c) % 2 == 0 else 'black'
                btn = Button(f'{r}x{c}', self)
                btn.set_background(bg)
                btn.clicked.connect(partial(self._click, btn, Position(r, c)))

                self.layout.addWidget(btn, r, c)
                self.board_buttons[r][c] = btn
    
    def update_ui(self):
        board = self.game.board

        for r in range(0, 8):
            for c in range(0, 8):
                piece = board.get(r,c)
                btn = self.board_buttons[r][c]
                btn.setText(str(piece) if piece else '')

                fg = '#dbdbdb' if piece and piece.color == Color.WHITE else '#404040'
                btn.set_foreground(fg)

        current_turn = 'white' if self.game.get_current_turn() == Color.WHITE else 'black'
        self.setWindowTitle(f"{TITLE} - {current_turn} turn")

    def _click(self, sender, position):
        if self.start_move:
            self._stop_move_piece(position)
        else:
            self._start_move_piece(sender, position)

    def _stop_move_piece(self, position):
        if self.selected_spot_pos is not None and self.selected_spot_pos is not position:
            try:
                self.game.play_turn(self.selected_spot_pos, position)
            except ChessException as e:
                QtWidgets.QMessageBox.about(self, TITLE, str(e))

        self.update_ui()
        self.selected_spot_pos = None
        self.start_move = False

    def _start_move_piece(self, sender, position):
        # no point on starting the selection if the place has nothing
        if self.game.is_empty_spot(position):
            return
        
        self.start_move = True
        if sender is not None:
            self.selected_spot_pos = position
            self._select_square(sender)

    def _select_square(self, button):
        button.set_foreground('green')
  
    def _on_resize(self):
        for rows in self.board_buttons:
            for b in rows:
                b.set_size(self.width() / 8, self.height() / 8)


def make_window(game):
    app = Qt.QApplication(sys.argv)
    w = ChessBoardGUI(game)
    w.setMinimumSize(600, 600)
    w.show()
    sys.exit(app.exec_())
