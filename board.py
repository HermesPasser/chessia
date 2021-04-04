from utils import make_2d_array
from color import Color
from pieces import *
from io import StringIO

class Board():
    SIZE = 8

    def __init__(self):
        self._make_board()

    def __repr__(self):
        sio = StringIO()
        for _, y, p in self._iterate():
            if y == Board.SIZE -1:
                sio.write("\n")
                continue
            
            p = '□' if p is None else str(p)
            sio.write(p)
        s = sio.getvalue()
        sio.close()
        return s

    def get(self, x: int, y: int):
        # TODO: assert is y = 7 works and y = SIZE not
        if x < 0 or x >= Board.SIZE or y < 0 or y >= Board.SIZE:
            raise Exception("Index out of bound")

        return self._board[x][y]

    def get_piece_location(self, color : Color, type_piece : type) -> Position:
        for x, y, p in self._iterate():
            if type(p) is type_piece and p.color == color:
                return Position(x, y)

        raise Exception(f"No {color} {type} found")

    def in_check(self, color):
        # TODO: too much computation, this and get_piece_location loops tru
        # the board, and since this is going to be called by the king,
        # will have more loops since the king has to check the position
        # where it will be in the future
        # i can just reuse a version of this with a can_move for each piece
        # in the places where the king will be since there is pieces (pawn)
        # that can only move to a place where there is a piece

        other_player_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        king_loc = self.get_piece_location(color, King)
        
        # since the game ends before the king is eaten the board not locating it
        # doesn't make any sense
        assert(king_loc != None)

        # FIXME: loops thru like for piece in self._board: seems to be faster but
        # i dont store the position anywhere yet so i had to do the 
        # old way. Maybe create a spot/square wrapper or add a position
        # to the piece class
        for x, y, piece in self._iterate():
            if piece is not None and piece.color == other_player_color: 
                if piece.can_move(self, Position(x, y), king_loc):
                    return True
        
        return False

    # TODO: do we really need to let it here? Game and King
    # make sense having it but it deals with the internals 
    # of the board.
    def is_square_in_check(self, color, pos_to_check : Position):
        p = self.get(pos_to_check.x, pos_to_check.y)
        is_empty_spot = p is None
        is_our_king = not is_empty_spot and p.color == color and type(p) != King
        
        if is_our_king:
            return self.in_check(color)

        # FIXME: do we need to check if the sport as a
        # enemy piece? it really should return false 
        # if there is
        if not is_empty_spot:
            return False

        # TODO: create a method to get the piece directly
        king_loc = self.get_piece_location(color, King)
        our_king = self.get(king_loc.x, king_loc.y)

        # move the king to the given position
        self._board[pos_to_check.x][pos_to_check.y] = our_king
        self._board[king_loc.x][king_loc.y] = None

        # check if the king would be in check there
        is_place_in_check = self.in_check(color)

        # move the king back to its original position
        self._board[pos_to_check.x][pos_to_check.y] = None
        self._board[king_loc.x][king_loc.y] = our_king

        return is_place_in_check

    def is_empty_spot(self, x, y):
        return self.get(x, y) is None

    def _iterate(self):
         for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                yield x, y, self.get(x, y)

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
