from engine.position import Position
from engine.color import Color
from engine.move_result import MoveResult, CastlingMoveResult
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
    def can_move(self, board, start : Position, end : Position, land_under_attack=False) -> bool:
        """Returns true if the piece can move from 'start' to 'end'\n
        
        land_under_attack: if true, the position were the piece is tryingto move is under attack"""
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

    def handle_jump_over_pieces(self, board, end : Position, squares : list) -> MoveResult:
        """Given a list of spots/squares (Piece, Position) it returns a result move if is no piece was jumped over
        It assumes if is not empty, then the first the piece who called the method.
        """
        if squares:
            squares.pop(0) # pop self

        jumped_over_pieces = len(squares) > 1
        if jumped_over_pieces:
            return MoveResult(False)  
        
        captured_piece = None
        if len(squares) == 1:
            landed_spot = Position(squares[0][1], squares[0][2]) 
            landed_piece = squares[0][0]
            
            jumped_over_a_piece = landed_spot != end
            if jumped_over_a_piece:
                return MoveResult(False)
            
            landed_on_friend = landed_piece.color == self.color
            if landed_on_friend:
                return MoveResult(False)
            
            captured_piece = (landed_piece, landed_spot)
             
        return MoveResult(True, captured_piece)  
            

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

        # castling
        moves.append(Position(current_pos.x, current_pos.y - 2))
        moves.append(Position(current_pos.x, current_pos.y + 2))
        return [move for move in moves if in_range(move.x) and in_range(move.y)]

    # TODO: implement castling and prevent the
    def can_move(self, board, start, end, land_under_attack=False):
        # where a enemy piece can reach, the king don't
        if land_under_attack:
            return MoveResult(False)
        
        piece = board.get(end.x, end.y)

        if self.has_same_color(board, end):
            # no need to check distance/position since there's no way this can be performed
            # wrongly given only those conditions (unless we're testing on non default layout)
            no_pieces_in_the_way = len(board.get_pieces_range_horizontal(start, end)) == 2
            is_valid_castling = isinstance(piece, Rook) and self.is_first_move and piece.is_first_move and no_pieces_in_the_way
            
            result = CastlingMoveResult()
            result.set_moved_piece(None, start, end, None)
            
            if is_valid_castling:
                safe_path = not board.is_square_in_check(self.color, result.rook_final_pos)
                safe_landing = not board.is_square_in_check(self.color, result.king_final_pos)
                result.succeed = safe_path and safe_landing
                return result

            return MoveResult(False)
        
        king_on_target = isinstance(piece, King) and piece.color != self.color

        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        can_move_x = abs_x == 1 and abs_y == 0
        can_move_y = abs_x == 0 and abs_y == 1
        can_move_diagonally = abs_x == 1 and abs_y == 1

        distance = lambda p1, p2: abs(math.sqrt((p2.y - p1.y) * (p2.y - p1.y) + (p2.x - p1.x) * (p2.x - p1.x)))

        # it must have at least, one square of distance between each king
        other_color = self.color.reverse()
        other_king_pos = board.get_king_loc_by_color(other_color)
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

    def can_move(self, board, start, end, land_under_attack=False):
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

        valid_move = (can_move_vertical or can_move_diagonal)
        if not valid_move:
            return MoveResult(False)

        return self.handle_jump_over_pieces(board, end, squares)


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

    def can_move(self, board, start, end, land_under_attack=False):
        if self.has_same_color(board, end):
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

        valid_move = (can_move_x or can_move_y)
        if not valid_move:
            return MoveResult(False)

        return self.handle_jump_over_pieces(board, end, squares)  


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

    def can_move(self, board, start, end, land_under_attack=False):
        if self.has_same_color(board, end):
            return MoveResult(False)

        abs_x = abs(start.x - end.x)
        abs_y = abs(start.y - end.y)
        can_move_diagonal = abs_x != 0 and abs_y != 0 and abs_x == abs_y

        squares = board.get_pieces_range_diagonal(start.x, start.y, end.x, end.y)

        valid_move = can_move_diagonal
        if not valid_move:
            return MoveResult(False)

        return self.handle_jump_over_pieces(board, end, squares)


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

    def can_move(self, board, start, end, land_under_attack=False):
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
    MIDDLE_ROWS = (3, 4)

    def __init__(self, color : Color):
        self.color = color
        self.is_first_move = True
        self.did_moved_twice = False

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

    def handle_el_passant(self, board, start, y):       
        captured_piece = None
        going_left = y == 1
        going_right = y == -1

        if going_left: 
            pos = Position(start.x, start.y - 1)
            captured_piece = board.get(start.x , start.y - 1)
        elif going_right:
            pos = Position(start.x, start.y + 1)
            captured_piece = board.get(start.x , start.y + 1)

        can_en_passant = isinstance(captured_piece, Pawn) and pos.x in Pawn.MIDDLE_ROWS and captured_piece.did_moved_twice
        if can_en_passant:
            return MoveResult(True, captured=(captured_piece, pos))
        
        return MoveResult(False)
        
    # TODO: handle pomotion
    def can_move(self, board, start, end, land_under_attack=False):
        if self.has_same_color(board, end):
            return MoveResult(False)
        
        diff_x = start.x - end.x
        diff_y = start.y - end.y
        abs_x = abs(diff_x)
        
        # it can't land on the diagonals unless there is a enemy piece in there
        has_a_enemy_piece = self.has_not_same_color(board, end)

        # since the pawn can't go backwards we should
        # know from where it came from
        can_descend = diff_x < 0 and self.direction_is_down()
        can_ascend = diff_x > 0 and not self.direction_is_down()
        is_in_right_direction = can_descend or can_ascend

        # since we can't check from the current pos since it would capture the pawn 
        next_position = Position(start.x + (1 if can_descend else -1), start.y)
        enemy_ahead = len(board.get_pieces_range_vertical(next_position, end)) > 0

        can_diagonally_descend = ((diff_x == -1 and diff_y == 1) or (diff_x == -1 and diff_y == -1)) and can_descend
        can_diagonally_ascend = ((diff_x == 1 and diff_y == 1) or (diff_x == 1 and diff_y == -1)) and can_ascend
        if has_a_enemy_piece and (can_diagonally_descend or can_diagonally_ascend):
            captured_piece = board.get(end.x, end.y)
            return MoveResult(True, captured=(captured_piece, end))
        
        if not enemy_ahead and can_diagonally_descend or can_diagonally_ascend:
            el_passant_result = self.handle_el_passant(board, start, diff_y)
            if el_passant_result:
                return el_passant_result
        
        # the pawn can only go straight (y is always zero), 
        # one square at time (two if is its first move) so abs(x) 
        # is one or two 
        can_move_once = abs_x == 1
        can_move_twice = abs_x == 2 and self.is_first_move

        valid_move = (
            diff_y == 0 and 
            is_in_right_direction and 
            (can_move_once or can_move_twice) and 
            # the pawn can't land there if there is a enemy 
            # on that square since pawns can only eat diagonally
            not enemy_ahead
        )

        # FIXME: setting the status here is dangerous since we test a lot with the pieces, and undo()
        # didn't reset this variable.As the game is played, it seems that this isn't breaking to break 
        # anything so we can worry about it another time. *shurgs* 
        if valid_move and can_move_twice:
            self.did_moved_twice = True
        
        return MoveResult(valid_move)
