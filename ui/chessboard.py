import sys
import time
from functools import partial
from PyQt5 import Qt, QtCore, QtWidgets
from position import Position
from utils import make_2d_array
from game import Game, ChessException
from board import Board
from pieces import Piece
from color import Color
from ui.button import Button
 
TITLE = 'ChessIA'

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

                fg = '#c9c9c9' if piece and piece.color == Color.WHITE else '#404040'
                btn.set_foreground(fg)

        current_turn = 'white' if self.game.get_current_turn() == Color.WHITE else 'black'
        self.setWindowTitle(f"{TITLE} - {current_turn} turn")

    def _click(self, sender, position):
        if self.start_move:
            self._stop_move_piece(position)
        else:
            self._start_move_piece(sender, position)

    def _stop_move_piece(self, position):
        message = False
        if self.selected_spot_pos is not None and self.selected_spot_pos is not position:
            try:
                self.game.play_turn(self.selected_spot_pos, position)
            except ChessException as e:
                message = str(e)

        self.update_ui()
        self.selected_spot_pos = None
        self.start_move = False

        if message:
            QtWidgets.QMessageBox.about(self, TITLE, message)
        else:
            # if no error message is shown then the turn was played sucefully
            self.handle_and_animate_ia_move()

    def handle_and_animate_ia_move(self):
        message = False
        try:
            from_pos, to = self.game.play_turn_ia_start()
        except ChessException as e:
                message = str(e)
        
        button1 = self.board_buttons[from_pos.x][from_pos.y]
        self._select_square(button1)
        
        button2 = self.board_buttons[to.x][to.y]
        self._select_square(button2)

        self.update_ui()
        time.sleep(1)

        self.game.play_turn_ia_end()
        if message:
            QtWidgets.QMessageBox.about(self, TITLE, message)

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