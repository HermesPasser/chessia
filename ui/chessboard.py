from functools import partial
from PyQt5 import Qt, QtCore, QtWidgets
from utils import make_2d_array
from engine.position import Position
from engine.game import ChessException, PromotionException
from ui.promotion_dialog import PromotionDialog
from ui.button import Button
from ui.worker import Worker

TITLE = 'ChessIA'

class ChessBoardGUI(Qt.QMainWindow):
    resized = QtCore.pyqtSignal()
    finished = Qt.pyqtSignal()

    def __init__(self, parent, game):
        super(ChessBoardGUI, self).__init__()
        self.parent = parent
        self.game = game
        self.move_started = False
        self.selected_spot_pos = None
        self.ai_playing = False 
        self.no_ai = False
        self._initialize_component()
  
    def resizeEvent(self, event):
        self.resized.emit()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
 
        if key == QtCore.Qt.Key_Q and not self.ai_playing:
            self.game.game_ended = False
            self.game.undo()
            self.game.undo()
            self.update_ui()
        elif key == QtCore.Qt.Key_W:
            print(self.game.board)
        elif key == QtCore.Qt.Key_R:
            self.no_ai = not self.no_ai # turn a.i off
            print('a.i off:', self.no_ai)
        elif key == QtCore.Qt.Key_D:
            self.game.change_turn()
            self.update_ui()
            print('turn changed to', self.game.get_current_turn())
        elif key == QtCore.Qt.Key_Escape:
            self._show_parent()
    
    def _show_parent(self):
        self.hide()
        self.parent.show()

    def replay(self, coordinates):
        self.ai_playing = True
        self._call_replay_worker(coordinates)

    def _initialize_component(self):
        self.promo_dialog = PromotionDialog()
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
        if self.ai_playing or self.game.game_ended:
            return

        if self.move_started:
            self._stop_move_piece(position)
        else:
            self._start_move_piece(sender, position)

    def _stop_move_piece(self, position):
        message = False
        if self.selected_spot_pos is not None and self.selected_spot_pos is not position:
            try:
                self.game.play_turn(self.selected_spot_pos, position)
            except PromotionException:
                self.game.promote(self.promo_dialog.show())
                # need to finish manually since we didn't change since a exception was raised
                self.game.change_turn()
            except ChessException as e:
                message = str(e)

        self.update_ui()
        self.selected_spot_pos = None
        self.move_started = False

        if message:
            QtWidgets.QMessageBox.about(self, TITLE, message)
            if 'CHECKMATE' in message or 'STALEMATE' in message:
                self._show_parent()
            return
        
        # since we can't say the turn ended just because not exception was thrown
        if not self.no_ai and self.game.get_current_turn().is_black():
            self.ai_playing = True
            self._call_ai_worker()

    def _start_move_piece(self, sender, position):
        # no point on starting the selection if the place has nothing
        if self.game.is_empty_spot(position):
            return
        
        self.move_started = True
        if sender is not None:
            self.selected_spot_pos = position
            self._select_square(sender)

    def _call_ai_worker(self):
        self.worker = Worker.make_ai_worker(self.game)
        self.worker.progress.connect(self._ai_worker_progressed)
        self.worker.finished.connect(lambda: self._ai_worker_finished())
        self.worker.start()

    def _ai_worker_progressed(self, from_pos, to_pos, message):
        if not message:
            btn = self.board_buttons[from_pos.r][from_pos.c]
            btn2 = self.board_buttons[to_pos.r][to_pos.c]
            self._select_square(btn)
            self._select_square(btn2)
        
        self.update_ui()
        if message:
            QtWidgets.QMessageBox.about(self, TITLE, message)
            if 'CHECKMATE' in message or 'STALEMATE' in message:
                self._call_ai_worker()

    def _ai_worker_finished(self):
        self.game.play_turn_ia_end()
        self.ai_playing = False
        self.update_ui()

    def _call_replay_worker(self, coordinates):
        self.worker = Worker.make_replay_worker(self.game, coordinates)
        self.worker.progress.connect(self._replay_worker_progressed)
        self.worker.finished.connect(lambda: self._replay_worker_finished())  
        self.worker.start()

    def _replay_worker_progressed(self):
        self.update_ui()

    def _replay_worker_finished(self):
        self.update_ui()
        self.ai_playing = False

    def _select_square(self, button):
        button.set_foreground('green')

    def _on_resize(self):
        for rows in self.board_buttons:
            for b in rows:
                b.set_size(self.width() / 8, self.height() / 8)
