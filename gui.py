import tkinter as tk

class ChessBoardGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(expand=True)
        self.initialize_components()

    def initialize_components(self):
        self._initialize_board_buttons()

    def _initialize_board_buttons(self):
        self.board_buttons = []
        for x in range(0, 8):
            self.board_buttons.append([])
            for y in range(0, 8):
                bg = 'white' if (x + y) % 2 == 0 else 'black'
                btn = tk.Button(self, bg=bg)
                btn['text'] = f"{x}x{y}"
                btn.grid(row=x, column=y, sticky='nesw')
                btn.bind("<Button-1>", self.click)
                self.board_buttons[x].append(btn)

    def click(self, event):
        sender = event.widget
        # do something


def make_window():
    root = tk.Tk()
    root.title("ChessIA")
    root.minsize(700, 400)
    app = ChessBoardGUI(root)
    app.mainloop()
