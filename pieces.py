from position import Position
from color import Color

class Piece():
    def __init__(self, color : Color):
        self.color = color

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
