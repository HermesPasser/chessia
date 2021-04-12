from color import Color
from copy import copy
import pieces

def make_2d_array(range=range(0, 1), default=0):
    return [[default for _ in range] for _ in range]


# Note to self: if the serialized board has k or K it will
# throw an exception because of the check mate logic, maybe
# we should check it and throw an error somewhere
def load_board(board, text):
    kv = dict()
    kv['♔'] = pieces.King(Color.WHITE)
    kv['k']  = pieces.King(Color.WHITE)
    kv['♕'] = pieces.Queen(Color.WHITE)
    kv['q']  = pieces.Queen(Color.WHITE)
    kv['♖'] = pieces.Rook(Color.WHITE)
    kv['r']  = pieces.Rook(Color.WHITE)
    kv['♗'] = pieces.Bishop(Color.WHITE)
    kv['b']  = pieces.Bishop(Color.WHITE)
    kv['♘'] = pieces.Knight(Color.WHITE)
    kv['n']  = pieces.Knight(Color.WHITE)
    kv['♙'] = pieces.Pawn(Color.WHITE)
    kv['p']  = pieces.Pawn(Color.WHITE)
    kv['♚'] = pieces.King(Color.BLACK)
    kv['K']  = pieces.King(Color.BLACK)
    kv['♛'] = pieces.Queen(Color.BLACK)
    kv['Q']  = pieces.Queen(Color.BLACK)
    kv['♜'] = pieces.Rook(Color.BLACK)
    kv['R']  = pieces.Rook(Color.BLACK)
    kv['♝'] = pieces.Bishop(Color.BLACK)
    kv['B']  = pieces.Bishop(Color.BLACK)
    kv['♞'] = pieces.Knight(Color.BLACK)
    kv['N']  = pieces.Knight(Color.BLACK)
    kv['♟︎'] = pieces.Pawn(Color.BLACK)
    kv['P']  = pieces.Pawn(Color.BLACK)
    
    text = text.strip().replace("\n", '')
    if len(text) != board.SIZE * board.SIZE:
        raise Exception(f"string size ({len(text)}) does not match the board size ({board.SIZE * board.SIZE})")

    i = 0
    for x, y, _ in board._iterate():
        piece = kv.get(text[i], False)

        if piece:
            # [x][y] or [y][x] i don't even know anymore
            board.set(x, y, copy(piece))
        else: # since i may reload the board, is better i clean up the trash
            board.set(x, y, None)
        
        i += 1  

