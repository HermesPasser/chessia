from position import Position
from color import Color

class Piece():
    def __init__(self, color : Color):
        self.color = color
        self.is_first_move = True

    def __repr__(self):
        return self.to_unicode()

    def can_move(self, board, start : Position, end : Position) -> bool:
        raise NotImplementedError(f"Not implemented for '{type(self)}'")

    def to_unicode(self):
        raise NotImplementedError(f"Not implemented for '{type(self)}'")

    def is_white(self) -> bool:
        return self.color == Color.WHITE

    def has_same_color(self, board, position : Position):
        """Checks if the piece on 'position' is from the same color of this instance"""
        piece = board.get(position.x, position.y)
        return piece is not None and piece.is_white() == self.is_white()
            

class King(Piece):
    def to_unicode(self):
        return '♔' if self.color == Color.WHITE else '♚'


class Queen(Piece):
    def to_unicode(self):
        return '♕' if self.color == Color.WHITE else '♛'


class Rook(Piece):
    def to_unicode(self):
        return '♖' if self.color == Color.WHITE else '♜'


class Bishop(Piece):        
    def to_unicode(self):
        return '♗' if self.color == Color.WHITE else '♝'


class Knight(Piece):
    def to_unicode(self):
        return '♘' if self.color == Color.WHITE else '♞'


class Pawn(Piece):
    def to_unicode(self):
        return '♙' if self.color == Color.WHITE else '♟'

    # TODO: handle pomotion and el passant   
    def can_move(self, board, start, end):   
        x = start.x - end.x
        y = start.y - end.y
        abs_x = abs(x)

        # since the pawn can't go backwards we should
        # known from where it came (white start on top)
        can_descend = x < 0 and self.is_white()
        can_ascend = x > 0 and not self.is_white()
        is_in_right_direction = can_descend or can_ascend

        # the pawn can only go straight (to y is always zero), 
        # one spot at time (two if is its first move) so abs(x) 
        # is one or two 
        can_move_once = abs_x == 1
        can_move_twice = abs_x == 2 and self.is_first_move

        if y == 0 and is_in_right_direction and (can_move_once or can_move_twice):
            return True  

        return False
