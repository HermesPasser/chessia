from move_result import MoveResult
from utils import make_2d_array
from position import Position
from board import Board
from color import Color
from pieces import King
from enum import Enum

class MoveState(Enum):
    CAN_BE_PLACED = 0
    CAN_NOT_BE_PLACED = 1
    NO_PIECE_TO_MOVE = 2
    NOT_YOUR_PIECE = 3
    KING_IN_CHECK = 4
    KING_WILL_BE_IN_CHECK = 5
    CHECK_MATE = 6
    DRAW_BY_STALEMATE = 7

class ChessException(Exception):
    pass

class Game():
    def __init__(self):
        self.board = Board()
        self._turn = Color.WHITE
        self.game_ended = False

    def get_current_turn(self):
        return self._turn

    def change_turn(self):  
       self._turn = Color.WHITE if self._turn == Color.BLACK else Color.BLACK

    def is_empty_spot(self, position : Position) -> bool:
        return self.board.is_empty_spot(position.x, position.y)

    def _move(self, from_pos : Position, to_pos : Position):
        prev = self.board._board[from_pos.x][from_pos.y]
        prev.is_first_move = False
        self.board._board[to_pos.x][to_pos.y] = prev
        self.board._board[from_pos.x][from_pos.y] = None

    def _capture(self, position : Position):
        self.board.set(position.x, position.y, None)

    def _move_will_leave_in_check_state(self, result : MoveResult, from_pos : Position, to_pos : Position) -> bool:
        """ This will do the move, check if it make the king be in check, and then undo the move. """ 
        piece_on_destination = self.board.get(to_pos.x, to_pos.y)
        if piece_on_destination and piece_on_destination.color != self._turn:
            # it throws no (current color) king exception, so let's just prevent it
            # we could just prevent from clicking in the same color in the main method
            # but we __need__ to handle castling in the future. This hack shows how
            # many collateral effects this method (and the ones it calls) have
            return False 

        if result.captured:
            self._capture(result.captured_position)

        piece_is_first_move = self.board.get(from_pos.x, from_pos.y).is_first_move
        self._move(from_pos, to_pos)

        will_be_in_check = self.board.in_check(self.get_current_turn())

        self._move(to_pos, from_pos)
        self.board.get(from_pos.x, from_pos.y).is_first_move = piece_is_first_move

        if result.captured:
            self.board.set(result.captured_position.x, result.captured_position.y, result.captured)

        # since we're currently calling it even when the move isn't successful 
        # then we should keep track of any piece on the destination that may
        # get overwrited (if the piece is the captured then we don't need)
        elif to_pos != result.captured_position:
            self.board.set(to_pos.x, to_pos.y, piece_on_destination)

        return will_be_in_check
        
    def _check_move_state(self, from_pos : Position, to_pos : Position) -> (MoveState, MoveResult):
        """Return an enum corresponding to the state of the move and the move itself if it can be done."""
        # TODO: make the checks and delegate the important parts to Move and Piece

        piece = self.board.get(from_pos.x, from_pos.y)
        selected_piece_is_our_king = type(piece) is King and piece.color == self.get_current_turn()
        is_in_check = self.board.in_check(self.get_current_turn())

        # the position has no piece so return w/o switching the turn
        # or you didn't move
        if piece is None or from_pos == to_pos:
            return MoveState.NO_PIECE_TO_MOVE, None

        # the clicked piece is from the other player
        if piece.color != self.get_current_turn():
            return MoveState.NOT_YOUR_PIECE, None
        
        # check if the piece can be moved on the spot
        result = piece.can_move(self.board, from_pos, to_pos)
        will_be_in_check = self._move_will_leave_in_check_state(result, from_pos, to_pos)
        if result:

            # prevent you from moving any piece that is not the king when it is in check
            # when the king is in check and the if move will not change it 

            if not selected_piece_is_our_king and is_in_check and will_be_in_check:
                return MoveState.KING_IN_CHECK, None 
            
            if will_be_in_check:
                return MoveState.KING_WILL_BE_IN_CHECK, None

            return MoveState.CAN_BE_PLACED, result
        
        # is outside from the if above since this move IS invalid since the king already check
        # if the position is being attacked. Since we want to display a message that is not
        # the default message displayed when the move is invalid piece-wise, then we check 
        # it here too
        if will_be_in_check and selected_piece_is_our_king:
                return MoveState.KING_WILL_BE_IN_CHECK, None
    
        return MoveState.CAN_NOT_BE_PLACED, None

    def verify_for_check_mate(self, color) -> MoveState:
        our_king_pos = self.board.get_piece_location(color, King)
        our_king = self.board.get(our_king_pos.x, our_king_pos.y)

        king_cant_move = False
        pseudo_moves = our_king.get_pseudo_moves(our_king_pos)
        for move in pseudo_moves:
            if our_king.can_move(self.board, our_king_pos, move):
                king_cant_move = True
                break

        if king_cant_move:
            if self.board.in_check(color):
                return MoveState.CHECK_MATE
            
            return MoveState.DRAW_BY_STALEMATE

        return None

    def play_turn (self, from_pos : Position, to_pos : Position):
        if self.game_ended:
            return None
            
        rs, mr = self._check_move_state(from_pos, to_pos)

        if rs == MoveState.CAN_BE_PLACED:
            if mr.captured:
                self._capture(mr.captured_position)

            self._move(from_pos, to_pos)
            self.change_turn()

            color = self._turn
            rs = self.verify_for_check_mate(color)
            if not rs:
                color = color.reverse()
                rs = self.verify_for_check_mate(color)

            if rs == MoveState.CHECK_MATE:
                self.game_ended = True
                raise ChessException(f"CHECK-MATE\n{color} king can't defend himself")
            elif rs == MoveState.DRAW_BY_STALEMATE:
                self.game_ended = True
                raise ChessException(f"Draw by stalemate")

        elif rs == MoveState.CAN_NOT_BE_PLACED:
            raise ChessException("The selected piece can't be place on the selected spot")
        elif rs == MoveState.KING_IN_CHECK:
            raise ChessException(f"You can't move since the king is in check")
        elif rs == MoveState.KING_WILL_BE_IN_CHECK:
            raise ChessException(f"If you move this piece there, the king will be in check")
        else:
            pass # nothing
        
        
