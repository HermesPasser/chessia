from utils import make_2d_array
from color import Color
from pieces import *

class Board():
    def __init__(self):
        self._make_board()

    def get(self, x: int, y: int):
        if x < 0 or x > 7 or y < 0 or y > 7:
            raise Exception("Index out of bound")

        return self._board[x][y]

    def is_empty_spot(self, x, y):
        return self.get(x, y) is None

    def _remove_piece(self, piece):
        pass

    def _set_piece(self, piece):
        pass

    def _make_board(self):
        self._board = make_2d_array(range(0, 8), None)
        
        self._board[0][0] = Rook(Color.WHITE)
        self._board[0][1] = Knight(Color.WHITE)
        self._board[0][2] = Bishop(Color.WHITE)
        self._board[0][3] = Queen(Color.WHITE)
        self._board[0][4] = King(Color.WHITE)
        self._board[0][5] = Bishop(Color.WHITE)
        self._board[0][6] = Knight(Color.WHITE)
        self._board[0][7] = Rook(Color.WHITE)
        self._board[1][0] = Pawn(Color.WHITE)
        self._board[1][1] = Pawn(Color.WHITE)
        self._board[1][2] = Pawn(Color.WHITE)
        self._board[1][3] = Pawn(Color.WHITE)
        self._board[1][4] = Pawn(Color.WHITE)
        self._board[1][5] = Pawn(Color.WHITE)
        self._board[1][6] = Pawn(Color.WHITE)
        self._board[1][7] = Pawn(Color.WHITE)

        self._board[7][0] = Rook(Color.BLACK)
        self._board[7][1] = Knight(Color.BLACK)
        self._board[7][2] = Bishop(Color.BLACK)
        self._board[7][3] = Queen(Color.BLACK)
        self._board[7][4] = King(Color.BLACK)
        self._board[7][5] = Bishop(Color.BLACK)
        self._board[7][6] = Knight(Color.BLACK)
        self._board[7][7] = Rook(Color.BLACK)
        self._board[6][0] = Pawn(Color.BLACK)
        self._board[6][1] = Pawn(Color.BLACK)
        self._board[6][2] = Pawn(Color.BLACK)
        self._board[6][3] = Pawn(Color.BLACK)
        self._board[6][4] = Pawn(Color.BLACK)
        self._board[6][5] = Pawn(Color.BLACK)
        self._board[6][6] = Pawn(Color.BLACK)
        self._board[6][7] = Pawn(Color.BLACK)
