import tkinter as tk
from utils import make_2d_array

TITLE = 'ChessIA'

class ChessBoardGUI(tk.Frame):
    def __init__(self, master, game):
        super().__init__(master)
        self.game = game
        self.master = master
        self.pack(expand=True)
        self.initialize_components()

    def initialize_components(self):
        self._initialize_board_buttons()

    def _initialize_board_buttons(self):
        self.board_buttons = make_2d_array(range(0, 8), None)
        for x in range(0, 8):
            for y in range(0, 8):
                bg = 'white' if (x + y) % 2 == 0 else 'black'
                btn = tk.Button(self, bg=bg)
                btn['text'] = f"{x}x{y}"
                btn.grid(row=x, column=y, sticky='nesw')
                btn.bind("<Button-1>", self._click)
                self.board_buttons[x][y] = btn

    def _click(self, event):
        sender = event.widget
        # do something


def make_window(game):
    root = tk.Tk()
    root.title(TITLE)
    root.minsize(700, 400)
    app = ChessBoardGUI(root, game)
    app.mainloop()
