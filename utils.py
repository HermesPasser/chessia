from color import Color
from copy import copy
import pieces

def make_2d_array(range=range(0, 1), default=0):
    return [[default for _ in range] for _ in range]


def load_board(board, text):
    type = dict()
    type['♔'] = pieces.King(Color.WHITE)
    type['k'] = pieces.King(Color.WHITE)
    type['♕'] = pieces.Queen(Color.WHITE)
    type['q'] = pieces.Queen(Color.WHITE)
    type['♖'] = pieces.Rook(Color.WHITE)
    type['r'] = pieces.Rook(Color.WHITE)
    type['♗'] = pieces.Bishop(Color.WHITE)
    type['b'] = pieces.Bishop(Color.WHITE)
    type['♘'] = pieces.Knight(Color.WHITE)
    type['k'] = pieces.Knight(Color.WHITE)
    type['♙'] = pieces.Pawn(Color.WHITE)
    type['p'] = pieces.Pawn(Color.WHITE)
    type['♚'] = pieces.King(Color.BLACK)
    type['K'] = pieces.King(Color.BLACK)
    type['♛'] = pieces.Queen(Color.BLACK)
    type['Q'] = pieces.Queen(Color.BLACK)
    type['♜'] = pieces.Rook(Color.BLACK)
    type['R'] = pieces.Rook(Color.BLACK)
    type['♝'] = pieces.Bishop(Color.BLACK)
    type['B'] = pieces.Bishop(Color.BLACK)
    type['♞'] = pieces.Knight(Color.BLACK)
    type['K'] = pieces.Knight(Color.BLACK)
    type['♟︎'] = pieces.Pawn(Color.BLACK)
    type['P'] = pieces.Pawn(Color.BLACK)
    
    text = text.strip().replace("\n", '')
    if len(text) != board.SIZE * board.SIZE -1:
      raise Exception(f"string size ({len(text)}) does not match the board size ({board.SIZE * board.SIZE})")
    
    x = 0
    y = 0
    for c in text:
      piece = type.get(c, False)
      if not piece:
        continue
      
      # [x][y] or [y][x] i don't even know anymore
      board.set(x, y, copy(piece))
      x += 1
      if x == board.SIZE:
        x = 0
        y += 1