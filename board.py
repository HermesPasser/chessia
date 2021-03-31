from utils import make_2d_array
from color import Color

class Board():
    def __init__(self):
        self._make_board()

    def get(self, x: int, y: int):
        if x < 0 or x > 7 or y < 0 or y > 7:
            raise Error("Index out of bound")

        return self._board[x][y]

    def is_empty_spot(self, x, y):
        return self.get(x, y) is None

    def _remove_piece(self, piece):
        pass

    def _set_piece(self, piece):
        pass

    def _make_board(self):
        self._board = make_2d_array(range(0, 8), None)
        
