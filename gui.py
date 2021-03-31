import tkinter as tk
from tkinter.font import Font
from tkinter.messagebox import showinfo
from position import Position
from utils import make_2d_array
from game import Game
from board import Board
from pieces import Piece
from color import Color

TITLE = 'ChessIA'

class ChessBoardGUI(tk.Frame):
    def __init__(self, master, game):
        super().__init__(master)
        self.game = game
        self.master = master
        self.start_move = False
        self.selected_spot_pos = None

        self.pack(expand=True)
        self.initialize_components()
        self.update_board_buttons()

    def initialize_components(self):
        self._initialize_board_buttons()

    def update_board_buttons(self):
        board = self.game.board

        for x in range(0, 8):
            for y in range(0, 8):
                piece = board.get(x,y)
                btn = self.board_buttons[x][y]
                btn['text'] = piece or ''

                if piece is not None:
                    btn['fg'] = '#0b2a2e' if piece.is_white() else '#2e0e0b'

        current_turn = 'white' if self.game.get_current_turn() == Color.WHITE else 'black'
        self.master.title(f"{TITLE} - {current_turn} turn")

    def _initialize_board_buttons(self):
        self.board_buttons = make_2d_array(range(0, 8), None)
        for x in range(0, 8):
            for y in range(0, 8):
                bg = 'white' if (x + y) % 2 == 0 else 'black'
                font = Font(size=25, weight='bold')

                btn = tk.Button(self, bg=bg)
                btn.grid(row=x, column=y, sticky='nesw')
                btn['font'] = font
                btn.bind("<Button-1>", self._click)
                
                # create the property on the fly
                btn.position = Position(x, y)

                self.board_buttons[x][y] = btn

    def _click(self, event):
        sender = event.widget
        position = sender.position

        if self.start_move:
            self._stop_move_piece(position)
        else:
            self._start_move_piece(sender, position)

    def _stop_move_piece(self, position):
        if self.selected_spot_pos is not None and self.selected_spot_pos is not position:
            result = self.game.move(self.selected_spot_pos, position)
            if result is not None:
                showinfo(title=TITLE, message=result)

        self.update_board_buttons()
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
        button['fg'] = 'green'


def make_window(game):
    root = tk.Tk()
    root.title(TITLE)
    root.minsize(700, 400)
    app = ChessBoardGUI(root, game)
    app.mainloop()
