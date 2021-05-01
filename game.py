from move_result import MoveResult
from utils import make_2d_array
from position import Position
from board import Board
from color import Color
from pieces import King
from enum import Enum
import ai

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
        self.ai_difficulty = 3
        self.moves = []

    def get_current_turn(self):
        return self._turn

    def change_turn(self):  
       self._turn = Color.WHITE if self._turn == Color.BLACK else Color.BLACK

    def is_empty_spot(self, position : Position) -> bool:
        return self.board.is_empty_spot(position.x, position.y)

    def _capture(self, position : Position):
        self.board.set(position.x, position.y, None)

    def move(self, move : MoveResult):
        if move.captured:
            self._capture(move.captured_position)

        self.board.move(move.from_pos, move.to_pos)
        move.piece.is_first_move = False

        self.moves.append(move)

    def get_moves(self, color) -> MoveResult:
        # loop tru all pieces from a color
        moves = []
        for p, pos in self.board.iterate_material(color):
            pseudo_moves = p.get_pseudo_moves(pos)

            # from the pseudo moves, get the ones that can be made
            for pseudo in pseudo_moves:
                rs, result = self._check_move_state(pos, pseudo)
                if rs == MoveState.CAN_BE_PLACED and result:
                    moves.append(result)
        
        return moves

    def undo(self):
        # undo a move
        if len(self.moves) == 0:
            return
        
        move = self.moves.pop()

        self.board.move(move.to_pos, move.from_pos)
        
        self.board.get(move.from_pos.x, move.from_pos.y).is_first_move = move.was_first_move
        if move.captured:
            self.board.set(move.captured_position.x, move.captured_position.y, move.captured)
        
    def _move_will_leave_in_check_state(self, result : MoveResult, from_pos : Position, to_pos : Position) -> bool:
        """ This will do the move, check if it make the king be in check, and then undo the move. """
        piece_on_destination = self.board.get(to_pos.x, to_pos.y)

        if piece_on_destination:
            if piece_on_destination.color == self._turn or isinstance(piece_on_destination, King):
                return False 
        
        self.move(result)
        will_be_in_check = self.board.in_check(self.get_current_turn())
        self.undo()

        # since the operation is not atomic if resultmove is false
        # and this is going to be called even then is false because
        # of the flawed way i handle the current/next turn check
        # verifying code
        if not result and piece_on_destination:
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
        
        
        land_under_attack = False
        if isinstance(piece, King):
            land_under_attack = self.board.is_square_in_check(self._turn, to_pos)
        
        result = piece.can_move(self.board, from_pos, to_pos, land_under_attack)
        result.set_moved_piece(piece, from_pos, to_pos, piece.is_first_move)
        will_be_in_check = self._move_will_leave_in_check_state(result, from_pos, to_pos)
        # check if the piece can be moved on the spot
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

    def _captured_king(self, mr : MoveResult):
        """Throws the message of end game if a king was captured"""
        if not mr.captured or not isinstance(mr.captured, King):
            return

        self.game_ended = True
        player_message = "You captured the A.I's king , you have won!"
        ai_message = "A.I have won!"
        raise ChessException(player_message if self._turn == Color.WHITE else ai_message)

    def play_turn (self, from_pos : Position, to_pos : Position):
        if self.game_ended:
            return None

        rs, mr = self._check_move_state(from_pos, to_pos)

        if rs == MoveState.CAN_BE_PLACED:
            self._captured_king(mr)

            self.move(mr)
            self.change_turn()
           
        elif rs == MoveState.CAN_NOT_BE_PLACED:
            raise ChessException("The selected piece can't be place on the selected spot")
        elif rs == MoveState.KING_IN_CHECK:
            raise ChessException(f"You can't move since the king is in check")
        elif rs == MoveState.KING_WILL_BE_IN_CHECK:
            raise ChessException(f"If you move this piece there, the king will be in check")
        else:
            pass # nothing
        
    def play_turn_ia_start(self):
        if self.game_ended:
            return None
        # since is confusing to de i.a do make
        # the move w/o the board being updated
        # the UI will call it instead of it
        # being call on the play_turn()
        
        # TODO: we don't handle when the a.i don't have valid moves

        _, ai_move = ai.calc_best_move(self.ai_difficulty, self, Color.BLACK)
        if ai_move:
            self.move(ai_move)
            self._captured_king(ai_move)
        
            print("ai::", ai_move)
            return (ai_move.from_pos, ai_move.to_pos)

        print("ai:: no more moves to do")
        self.game_ended = True
        raise ChessException("A.I's king was stalemated, tecnically is a draw but since the\nis the Poor Man's ChessAI then you have won!")

    def play_turn_ia_end(self):
        self.change_turn()
