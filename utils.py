from importlib import import_module
from engine.color import Color
from copy import copy
import engine.pieces as pieces
import pickle
import io

def make_2d_array(range=range(0, 1), default=0):
    return [[default for _ in range] for _ in range]


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

# we will use the super class to represent a 
# spot from where we want to recover the
# position
kv['0']  = pieces.Piece(Color.BLACK)


def piece_from_char(char):
    return copy(kv.get(char, None))


# Note to self: if the serialized board has k or K it will
# throw an exception because of the check mate logic, maybe
# we should check it and throw an error somewhere
def load_board(board, text):
    text = text.strip().replace("\n", '')
    if len(text) != board.SIZE * board.SIZE:
        raise Exception(f"string size ({len(text)}) does not match the board size ({board.SIZE * board.SIZE})")

    i = 0
    for row, col, _ in board._iterate():
        piece = piece_from_char(text[i])

        if piece:
            board.set(row, col, piece)
        else: # since i may reload the board, is better i clean up the trash
            board.set(row, col, None)
        
        i += 1  


def make_spot(text):
    """Given a string p<r,c> where:

    p is a char representation of a piece
    r and c are a digit 
    
    returns a tuple reprsenting a spot/square:
    (pieces.Piece, int, int)
    """
    p, _, r, _, c, _ = list(text)
    return (piece_from_char(p), int(r), int(c))


def make_spots(*args):
    return [make_spot(text) for text in args]


class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        safe_modules = { 'engine.position', 'engine.move_result', 'engine.pieces', 'engine.color' }
        safe_types = {
            'CastlingMoveResult',
            'MoveResult',
            'Position',
            'Color',
            'King',
            'Queen',
            'Rook',
            'Bishop',
            'Knight',
            'Pawn',
        }

        if module in safe_modules and name in safe_types:
            return getattr(import_module(module), name)

        raise pickle.UnpicklingError("global '%s.%s' is forbidden" % (module, name))

def serialize(binary_data, filename : str):
    file = io.open(filename, 'ab+')
    pickle.dump(binary_data, file)
    file.close()

def deserialize(filename):
    bytes = io.open(filename, 'rb')
    obj = RestrictedUnpickler(bytes).load()
    bytes.close()
    return obj
