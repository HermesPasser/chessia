from position import Position
from color import Color
from move_result import MoveResult
import math

in_range = lambda x: x > -1 and x < 8

# TODO: handle eating a pice on your way
# when you move 2 squares or more (all pieces [pawn first 2-square move included] but king)   

class Piece():
    def __init__(self, color : Color):
        self.color = color
        self.is_first_move = True

    def __eq__(self, other):
        return (
          isinstance(other, type(self)) 
          and other.color == self.color
          and other.is_first_move == self.is_first_move
        )

    def __repr__(self):
        return self.to_unicode()

    def get_value(self) -> int:
        """Returns how valuable the piece is"""
        raise NotImplementedError(f"Not implemented for '{type(self)}'")

    def get_pseudo_moves(self, current_pos) -> list:
        """Returns all possible spots where you can place it without any validation"""
        raise NotImplementedError(f"Not implemented for '{type(self)}'")

    # TODO: this is dump, why it need to receive a start to
    # know if it can move? it make more sense to store its 
    # location
    def can_move(self, board, start : Position, end : Position, no_checks=False) -> bool:
        """Returns true if the piece can move from 'start' to 'end'\n
        
        no_checks: exclusive for the king, if true it would not check if the 'end'
        position is being attacked, since the attacked logic can call this method
        from the king, this flag prevents it from going to a infinete loop."""
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

    def get_value(self):
        return 10000

    def get_pseudo_moves(self, current_pos) -> list:
        moves = []
        moves.append(Position(current_pos.x, current_pos.y - 1))
        moves.append(Position(current_pos.x, current_pos.y + 1))
        moves.append(Position(current_pos.x + 1, current_pos.y))
        moves.append(Position(current_pos.x + 1, current_pos.y - 1))
        moves.append(Position(current_pos.x + 1, current_pos.y + 1))
        moves.append(Position(current_pos.x - 1, current_pos.y))
        moves.append(Position(current_pos.x - 1, current_pos.y - 1))
        moves.append(Position(current_pos.x - 1, current_pos.y + 1))
        return [move for move in moves if in_range(move.x) and in_range(move.y)]

    # TODO: implement castling and prevent the
    def can_move(self, board, start, end, no_checks=False):
        # target_piece = board.get(end.x, end.y)
        
        if self.has_same_color(board, end):
            # or target_piece is type(Rook): # cause if is a rook, then it should be allowed to select your piece
            return MoveResult(False)
        
        # the a enemy piece can reach, the king can't go
        if not no_checks and board.is_square_in_check(self.color, end):
            return MoveResult(False)

        piece = board.get(end.x, end.y)
        king_on_target = isinstance(piece, King) and piece.color != self.color

        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        can_move_x = abs_x == 1 and abs_y == 0
        can_move_y = abs_x == 0 and abs_y == 1
        can_move_diagonally = abs_x == 1 and abs_y == 1

        distance = lambda p1, p2: abs(math.sqrt((p2.y - p1.y) * (p2.y - p1.y) + (p2.x - p1.x) * (p2.x - p1.x)))

        # it must have at least, one square of distance between each king
        other_color = Color.WHITE if self.color == Color.BLACK else Color.BLACK
        other_king_pos = board.get_piece_location(other_color, King)
        other_king_too_close = distance(end, other_king_pos) < 2
        
        captured_piece = None
        if piece and not king_on_target:
            captured_piece = (piece, end)

        valid_move = (
            not king_on_target and
            not other_king_too_close and
            (can_move_diagonally or can_move_x or can_move_y)
        )
        return MoveResult(valid_move, captured_piece)


class Queen(Piece):
    def to_unicode(self):
        return '♕' if self.color == Color.WHITE else '♛'
    
    def get_value(self):
        return 1000

    def get_pseudo_moves(self, current_pos) -> list:
        return Rook(self.color).get_pseudo_moves(current_pos) + Bishop(self.color).get_pseudo_moves(current_pos)

    def can_move(self, board, start, end, no_checks=False):
        if self.has_same_color(board, end):
            return MoveResult(False)
        
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
        valid_move = (can_move_vertical or can_move_diagonal) and not pieces_in_the_way
        
        captured_piece = None
        if valid_move and len(squares) == 1:
            captured_piece = (squares[0][0], Position(squares[0][1], squares[0][2]))
        
        return MoveResult(valid_move, captured_piece)


class Rook(Piece):
    def to_unicode(self):
        return '♖' if self.color == Color.WHITE else '♜'

    def get_value(self):
        return 525

    def get_pseudo_moves(self, current_pos) -> list:       
        move_to_right = range(current_pos.y, 8)
        move_to_left = range(0, current_pos.y + 1)
        descend = range(current_pos.x, 8)
        ascend = range(0, current_pos.x + 1)
        
        moves = []
        def populate_vertical(increment_lambda):
            for y in increment_lambda:
                if not (y == current_pos.x and y == current_pos.y):
                    moves.append(Position(current_pos.x, y))

        def populate_horizontal(increment_lambda):
            for x in increment_lambda:
                if x != current_pos.x:
                    moves.append(Position(x, current_pos.y))

        populate_vertical(move_to_right)
        populate_vertical(move_to_left)
        populate_horizontal(ascend)
        populate_horizontal(descend)

        return moves

    # TODO: handle castling
    def can_move(self, board, start, end, no_checks=False):
        # target_piece = board.get(end.x, end.y)
        if self.has_same_color(board, end):
            # or target_piece is type(Rook): # cause if is a rook, then it should be allowed to select your piece
            return MoveResult(False)
        
        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)

        can_move_x = abs_x != 0 and abs_y == 0
        can_move_y = abs_x == 0 and abs_y != 0

        # TODO: create get range origin exlusive
        if not can_move_x and can_move_y:
            squares = board.get_pieces_range_horizontal(start, end)
        else:
            squares = board.get_pieces_range_vertical(start, end)

        if squares:
            squares.pop(0) # remove itself

        # check if there is only one piece (aside from itself) in the way and that the piece is from the other player
        # 2 since one is self
        pieces_in_the_way = len(squares) > 1 or (len(squares) > 0 and squares[0][0].color == self.color)
        valid_move = (can_move_x or can_move_y) and not pieces_in_the_way

        captured_piece = None
        if valid_move and len(squares) == 1:
            captured_piece = (squares[0][0], Position(squares[0][1], squares[0][2]))

        return MoveResult(valid_move, captured_piece)


class Bishop(Piece):  
    def to_unicode(self):
        return '♗' if self.color == Color.WHITE else '♝'

    def get_value(self):
        return 350

    def get_pseudo_moves(self, current_pos) -> list:
        moves = []

        increment_se = lambda x, y:(x+1, y+1)
        increment_ms = lambda x, y:(x+1, y-1)
        increment_nw = lambda x, y:(x-1, y-1)
        increment_ne = lambda x, y:(x-1, y+1)

        def populate(increment_lambda):
            x = current_pos.x
            y = current_pos.y

            while x > -1 and x < 8 and y > -1 and y < 8:
                if not (x == current_pos.x and y == current_pos.y):
                    moves.append(Position(x, y))
                x , y = increment_lambda(x, y)

        populate(increment_se)
        populate(increment_ms)
        populate(increment_nw)
        populate(increment_ne)

        return moves

    def can_move(self, board, start, end, no_checks=False):
        if self.has_same_color(board, end):
            return MoveResult(False)

        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        can_move_diagonal = abs_x != 0 and abs_y != 0 and abs_x == abs_y

        squares = board.get_pieces_range_diagonal(start.x, start.y, end.x, end.y)
        if squares:
            squares.pop(0) # remove itself
        pieces_in_the_way = len(squares) > 1 or (len(squares) > 0 and squares[0][0].color == self.color)
        valid_move = can_move_diagonal and not pieces_in_the_way

        captured_piece = None
        if valid_move and len(squares) == 1:
            captured_piece = (squares[0][0], Position(squares[0][1], squares[0][2]))

        return MoveResult(valid_move, captured_piece)


class Knight(Piece):
    def to_unicode(self):
        return '♘' if self.color == Color.WHITE else '♞'

    def get_value(self):
        return 350

    def get_pseudo_moves(self, current_pos) -> list:
        moves = []
        moves.append(Position(current_pos.x - 1, current_pos.y + 2))
        moves.append(Position(current_pos.x - 1, current_pos.y - 2))
        moves.append(Position(current_pos.x + 1, current_pos.y + 2))
        moves.append(Position(current_pos.x + 1, current_pos.y - 2))
        moves.append(Position(current_pos.x - 2, current_pos.y + 1))
        moves.append(Position(current_pos.x - 2, current_pos.y - 1))
        moves.append(Position(current_pos.x + 2, current_pos.y + 1))
        moves.append(Position(current_pos.x + 2, current_pos.y - 1))
        return [move for move in moves if in_range(move.x) and in_range(move.y)]

    def can_move(self, board, start, end, no_checks=False):
        if self.has_same_color(board, end):
            return MoveResult(False)

        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        valid_move = (abs_x == 2 and abs_y == 1) or (abs_x == 1 and abs_y == 2)

        captured_piece = None
        if valid_move:
            captured_piece = (board.get(end.x, end.y), end)

        return MoveResult(valid_move, captured_piece)


class Pawn(Piece):
    color_that_descends = Color.BLACK

    def get_value(self):
        return 100

    def to_unicode(self):
        return '♙' if self.color == Color.WHITE else '♟'

    def direction_is_down(self):
        """Returns true if the piece starts at 2nd row and have to descend"""
        return self.color == Pawn.color_that_descends

    def get_pseudo_moves(self, current_pos) -> list:
        descend = self.direction_is_down()
        moves = []

        if descend:
            # diagonal
            moves.append(Position(current_pos.x + 1, current_pos.y - 1))
            moves.append(Position(current_pos.x + 1, current_pos.y + 1))
            
            moves.append(Position(current_pos.x + 1, current_pos.y))
            if self.is_first_move:
                moves.append(Position(current_pos.x + 2, current_pos.y))
        else:
            moves.append(Position(current_pos.x - 1, current_pos.y - 1))
            moves.append(Position(current_pos.x - 1, current_pos.y + 1))

            moves.append(Position(current_pos.x - 1, current_pos.y))
            if self.is_first_move:
                moves.append(Position(current_pos.x - 2, current_pos.y))

        return [move for move in moves if in_range(move.x) and in_range(move.y)]

    # TODO: handle pomotion and el passant
    def can_move(self, board, start, end, no_checks=False):
        if self.has_same_color(board, end):
            return MoveResult(False)
        
        x = start.x - end.x
        y = start.y - end.y
        abs_x = abs(x)

        # it can't land on the diagonals unless there is a enemy piece in there
        has_a_enemy_piece = self.has_not_same_color(board, end)

        # since the pawn can't go backwards we should
        # know from where it came from
        can_descend = x < 0 and self.direction_is_down()
        can_ascend = x > 0 and not self.direction_is_down()
        is_in_right_direction = can_descend or can_ascend

        can_go_diagonally_left = ((x == -1 and y == 1) or (x == -1 and y == -1)) and can_descend
        can_go_diagonally_right = ((x == 1 and y == 1) or (x == 1 and y == -1)) and can_ascend
        if has_a_enemy_piece and (can_go_diagonally_left or can_go_diagonally_right):
            captured_piece = board.get(end.x, end.y)
            return MoveResult(True, captured=(captured_piece, end))

        # the pawn can only go straight (y is always zero), 
        # one square at time (two if is its first move) so abs(x) 
        # is one or two 

        # since we can't check from the current pos since it would capture the pawn 
        next_position = Position(start.x + (1 if can_descend else -1), start.y)
 
        enemy_ahead = len(board.get_pieces_range_vertical(next_position, end)) > 0
        can_move_once = abs_x == 1
        can_move_twice = abs_x == 2 and self.is_first_move

        valid_move = (
            y == 0 and 
            is_in_right_direction and 
            (can_move_once or can_move_twice) and 
            # the pawn can't land there if there is a enemy 
            # on that square since pawns can only eat diagonally
            not enemy_ahead
        )
        return MoveResult(valid_move)
