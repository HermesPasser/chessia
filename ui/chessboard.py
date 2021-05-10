import sys
import time
from functools import partial
from PyQt5 import Qt, QtCore, QtWidgets
from utils import make_2d_array
from engine.position import Position
from engine.game import Game, ChessException
from ui.button import Button
from ui.worker import Worker

TITLE = 'Poor man\'s chessAI'

class ChessBoardGUI(Qt.QMainWindow):
    resized = QtCore.pyqtSignal()
    finished = Qt.pyqtSignal()

    def __init__(self, game):
        super(ChessBoardGUI, self).__init__()
        self.game = game
        self.start_move = False
        self.selected_spot_pos = None
        self.ai_turn = False
        self.no_ai = False
        self._initialize_component()
  
    def resizeEvent(self, event):
        self.resized.emit()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
 
        if key == QtCore.Qt.Key_Q and self.game.get_current_turn().is_black():
            self.game.game_ended = False
            self.game.undo()
            self.game.undo()
            self.update_ui()
        elif key == QtCore.Qt.Key_W:
            print(self.game.board)
        elif key == QtCore.Qt.Key_R:
            self.no_ai = not self.no_ai # turn a.i off
            print('a.i on:', self.no_ai)
        elif key == QtCore.Qt.Key_D:
            self.game.change_turn()
            self.update_ui()
            print('turn changed to', self.game.get_current_turn())
    
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

                fg = '#c9c9c9' if piece and piece.color.is_white() else '#404040'
                btn.set_foreground(fg)

        current_turn =  str(self.game.get_current_turn())
        self.setWindowTitle(f"{TITLE} - {current_turn} turn")

    def _click(self, sender, position):
        if self.ai_turn or self.game.game_ended:
            return

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
            return
        
        # since we can't say the turn ended just because not exception was thrown
        if not self.no_ai and self.game.get_current_turn().is_black():
            self._call_worker()

    def _start_move_piece(self, sender, position):
        # no point on starting the selection if the place has nothing
        if self.game.is_empty_spot(position):
            return
        
        self.start_move = True
        if sender is not None:
            self.selected_spot_pos = position
            self._select_square(sender)

    def _call_worker(self):
        self.ai_turn = True

        self.thread = Qt.QThread()
        self.worker = Worker(self.game)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self._worker_progressed)
        self.worker.finished.connect(lambda: self._worker_finished())
        self.thread.start()

    def _worker_progressed(self, from_pos, to_pos, message):
        if not message:
            btn = self.board_buttons[from_pos.x][from_pos.y]
            btn2 = self.board_buttons[to_pos.x][to_pos.y]
            self._select_square(btn)
            self._select_square(btn2)
        
        self.update_ui()
        if message:
            QtWidgets.QMessageBox.about(self, TITLE, message)

    def _worker_finished(self):
        self.game.play_turn_ia_end()
        self.ai_turn = False
        self.update_ui()

    def _select_square(self, button):
        button.set_foreground('green')
  
    def _on_resize(self):
        for rows in self.board_buttons:
            for b in rows:
                b.set_size(self.width() / 8, self.height() / 8)
