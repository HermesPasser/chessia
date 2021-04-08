from position import Position
from color import Color

# TODO: prevent the move with multiple enemy
# pieces or one of your own in the way (all pieces [pawn first 2-square move included] but king)
# TODO: handle eating a pice on your way
# when you move 2 squares or more (all pieces [pawn first 2-square move included] but king)   

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
        return piece is not None and piece.color == self.color
    
    def has_not_same_color(self, board, position : Position):
        """Checks if the piece on 'position' is not from the same color of this instance"""
        piece = board.get(position.x, position.y)
        return piece is not None and piece.color != self.color
            

class King(Piece):
    def to_unicode(self):
        return '♔' if self.color == Color.WHITE else '♚'

    # TODO: implement castling and prevent the
    # king of moving to a place whre it can
    # be in check
    def can_move(self, board, start, end):
        # target_piece = board.get(end.x, end.y)
        
        if self.has_same_color(board, end):
            # or target_piece is type(Rook): # cause if is a rook, then it should be allowed to select your piece
            return False
        
        # the a enemy piece can reach, the king can't go
        if board.is_square_in_check(self.color, end):
            return False

        # TODO: prevent king to move if it can be in check

        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        can_move_x = abs_x == 1 and abs_y == 0
        can_move_y = abs_x == 0 and abs_y == 1
        can_move_diagonally = abs_x == 1 and abs_y == 1
        
        return can_move_diagonally or can_move_x or can_move_y


class Queen(Piece):
    def to_unicode(self):
        return '♕' if self.color == Color.WHITE else '♛'

    def can_move(self, board, start, end):
        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        can_move_vertical = (abs_x != 0 and abs_y == 0) or (abs_x == 0 and abs_y != 0)
        can_move_diagonal = abs_x != 0 and abs_y != 0 and abs_x == abs_y

        if can_move_diagonal:
            squares = board.get_pieces_range_diagonal(start.x, start.y, end.x, end.y)
        elif abs_x == 0 and abs_y > 0:
            squares = board.get_pieces_range_horizontal(start, end)
        else:
            squares = board.get_pieces_range_vertical(start, end)
   
        if squares:
            squares.pop(0) # pop self

        pieces_in_the_way = len(squares) > 1 or (len(squares) > 0 and squares[0][0].color == self.color)

        return (can_move_vertical or can_move_diagonal) and not pieces_in_the_way


class Rook(Piece):
    def to_unicode(self):
        return '♖' if self.color == Color.WHITE else '♜'

    # TODO: handle castling
    def can_move(self, board, start, end):
        # target_piece = board.get(end.x, end.y)
        if self.has_same_color(board, end):
            # or target_piece is type(Rook): # cause if is a rook, then it should be allowed to select your piece
            return False
        
        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)

        can_move_x = abs_x != 0 and abs_y == 0
        can_move_y = abs_x == 0 and abs_y != 0

        # TODO: create get range origin exlusive
        if not can_move_x and can_move_y:
            squares = board.get_pieces_range_horizontal(start, end)
        else:
            squares = board.get_pieces_range_vertical(start, end)

        squares.pop(0) # remove itself

        # check if there is only one piece (aside from itself) in the way and that the piece is from the other player
        # 2 since one is self
        pieces_in_the_way = len(squares) > 1 or (len(squares) > 0 and squares[0][0].color == self.color)

        return (can_move_x or can_move_y) and not pieces_in_the_way


class Bishop(Piece):        
    def to_unicode(self):
        return '♗' if self.color == Color.WHITE else '♝'

    def can_move(self, board, start, end):
        if self.has_same_color(board, end):
            return False

        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        can_move_diagonal = abs_x != 0 and abs_y != 0 and abs_x == abs_y

        squares = board.get_pieces_range_diagonal(start.x, start.y, end.x, end.y)
        if squares:
            squares.pop(0) # remove itself
        pieces_in_the_way = len(squares) > 1 or (len(squares) > 0 and squares[0][0].color == self.color)

        return can_move_diagonal and not pieces_in_the_way


class Knight(Piece):
    def to_unicode(self):
        return '♘' if self.color == Color.WHITE else '♞'
        
    def can_move(self, board, start, end):
        if self.has_same_color(board, end):
            return False
        
        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        
        return (abs_x == 2 and abs_y == 1) or (abs_x == 1 and abs_y == 2)


class Pawn(Piece):
    def to_unicode(self):
        return '♙' if self.color == Color.WHITE else '♟'

    # TODO: handle pomotion and el passant
    def can_move(self, board, start, end):
        if self.has_same_color(board, end):
            return False
        
        x = start.x - end.x
        y = start.y - end.y
        abs_x = abs(x)

        # it can't land on the diagonals unless there is a enemy piece in there
        has_a_enemy_piece = self.has_not_same_color(board, end)

        can_go_diagonally_left = ((x == -1 and y == 1) or (x == -1 and y == -1)) 
        can_go_diagonally_right = ((x == 1 and y == 1) or (x == 1 and y == -1))
        if  has_a_enemy_piece and (can_go_diagonally_left or can_go_diagonally_right):
            return True

        # since the pawn can't go backwards we should
        # known from where it came (white start on top)
        can_descend = x < 0 and self.is_white()
        can_ascend = x > 0 and not self.is_white()
        is_in_right_direction = can_descend or can_ascend

        # the pawn can only go straight (to y is always zero), 
        # one square at time (two if is its first move) so abs(x) 
        # is one or two 

        # since we can't check from the current pos since it would capture the pawn 
        next_position = Position(start.x + (1 if can_descend else -1), start.y)
 
        enemy_ahead = len(board.get_pieces_range_vertical(next_position, end)) > 0
        can_move_once = abs_x == 1
        can_move_twice = abs_x == 2 and self.is_first_move

        if (
                y == 0 and 
                is_in_right_direction and 
                (can_move_once or can_move_twice) and 
                # the pawn can't land there if there is a enemy 
                # on that square since pawns can only eat diagonally
                not enemy_ahead
            ):
            return True  

        return False
