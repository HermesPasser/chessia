from engine.move_result import MoveResult, CastlingMoveResult
from engine.position import Position
from engine.board import Board
from engine.color import Color
from engine.pieces import Piece, King, Queen, Pawn
from enum import Enum
import engine.ai as ai

class MoveState(Enum):
    CAN_BE_PLACED = 0
    CAN_NOT_BE_PLACED = 1
    NO_PIECE_TO_MOVE = 2
    NOT_YOUR_PIECE = 3
    KING_IN_CHECK = 4
    KING_WILL_BE_IN_CHECK = 5
    DRAW_BY_STALEMATE = 6
    KING_PATH_ATTACKED = 7

class ChessException(Exception):
    pass

# I would fown uppon seeing something like
# this somewhere else but this is python
class PromotionException(ChessException):
    pass

class Game():
    def __init__(self):
        self.restart()
    
    def restart(self):
        self.board = Board()
        self._turn = Color.WHITE
        self.game_ended = False
        self.ai_difficulty = 3
        self.move_result_waiting_promotion = None
        self.moves = []

    def get_current_turn(self):
        return self._turn

    def change_turn(self):  
       self._turn = self._turn.reverse()

    def is_empty_spot(self, position : Position) -> bool:
        return self.board.is_empty_spot(position.r, position.c)

    def _capture(self, position : Position):
        self.board.set(position.r, position.c, None)

    def move(self, move : MoveResult):
        if isinstance(move, CastlingMoveResult):
            self.board.get(move.king_pos.r, move.king_pos.c).is_first_move = False
            self.board.get(move.rook_pos.r, move.rook_pos.c).is_first_move = False

            self.board.move(move.king_pos, move.king_final_pos)
            self.board.move(move.rook_pos, move.rook_final_pos)
        else:
            if move.captured:
                self._capture(move.captured_position)

            self.board.move(move.from_pos, move.to_pos)
            if move.should_promote:
                # since the a.i will simulate by moving the player's piece and therefore
                # with promoted_to not selected
                if not move.promoted_to:
                    move.promoted_to = Queen(move.piece.color)
                
                self.board.set(move.to_pos.r, move.to_pos.c, move.promoted_to)
                
            move.piece.is_first_move = False

        self.moves.append(move)

    def get_valid_moves_raw(self, piece, pos) -> list:
        """Returns all the spots thar a spefic 'piece' can be placed given its position 'pos'."""
        legal_moves = []
        pseudo_moves = piece.get_pseudo_moves(pos)

        for pseudo in pseudo_moves:
            rs, result = self._check_move_state(pos, pseudo, piece.color)
            if rs == MoveState.CAN_BE_PLACED and result:
                legal_moves.append(pseudo)
    
        return legal_moves

    def get_moves(self, color) -> MoveResult:
        """Returns a list of all possible valid MoveResults that a given rank can do."""
        # loop tru all pieces from a color
        moves = []
        for p, pos in self.board.iterate_material(color):
            pseudo_moves = p.get_pseudo_moves(pos)

            # from the pseudo moves, get the ones that can be made
            for pseudo in pseudo_moves:
                rs, result = self._check_move_state(pos, pseudo, color)
                if rs == MoveState.CAN_BE_PLACED and result:
                    moves.append(result)
        
        return moves

    def undo(self):
        # undo a move
        if len(self.moves) == 0:
            return
        
        move = self.moves.pop()
        if isinstance(move, CastlingMoveResult):
            self.board.move(move.king_final_pos, move.king_pos)
            self.board.move(move.rook_final_pos, move.rook_pos)
            
            self.board.get(move.king_pos.r, move.king_pos.c).is_first_move = True
            self.board.get(move.rook_pos.r, move.rook_pos.c).is_first_move = True

            return
        
        self.board.move(move.to_pos, move.from_pos)
       
        if move.should_promote:
            self.board.set(move.from_pos.r, move.from_pos.c, move.piece)
        self.board.get(move.from_pos.r, move.from_pos.c).is_first_move = move.was_first_move
        
        if move.captured:
            self.board.set(move.captured_position.r, move.captured_position.c, move.captured)
        
    def _move_will_leave_in_check_state(self, result : MoveResult, from_pos : Position, to_pos : Position, turn) -> bool:
        """ This will do the move, check if it make the king be in check, and then undo the move. """
        piece_on_destination = self.board.get(to_pos.r, to_pos.c)

        if piece_on_destination:
            if piece_on_destination.color == turn or isinstance(piece_on_destination, King):
                return False 
        
        self.move(result)
        will_be_in_check = self.board.in_check(turn)
        self.undo()

        # since the operation is not atomic if resultmove is false
        # and this is going to be called even then is false because
        # of the flawed way i handle the current/next turn check
        # verifying code
        if not result and piece_on_destination:
            self.board.set(to_pos.r, to_pos.c, piece_on_destination)

        return will_be_in_check

    def _checkmated(self, turn):
        checkmate = self.board.in_check(turn)
        legal_moves = self.get_moves(turn)

        for move in legal_moves:
            self.move(move)

            if not self.board.in_check(turn):
                checkmate = False
            
            self.undo()

            if not checkmate:
                break
        
        return checkmate

    def _stalemated(self, turn):
        if len(self.get_moves(turn)) == 0 and not self.board.in_check(turn):
            return True
        return False

    def _check_move_state(self, from_pos : Position, to_pos : Position, turn=None) -> (MoveState, MoveResult):
        """Return an enum corresponding to the state of the move and the move itself if it can be done."""
        # TODO: make the checks and delegate the important parts to Move and Piece
        if not turn:
            turn = self._turn
        
        # HACK to reset the state since we can't leave it True
        for piece, _ in self.board.iterate_material(turn):
            if isinstance(piece, Pawn):
                piece.did_moved_twice = False

        piece = self.board.get(from_pos.r, from_pos.c)
        selected_piece_is_our_king = type(piece) is King and piece.color == turn
        is_in_check = self.board.in_check(turn)
        
        # the position has no piece so return w/o switching the turn
        # or you didn't move
        if piece is None or from_pos == to_pos:
            return MoveState.NO_PIECE_TO_MOVE, None

        # the clicked piece is from the other player
        if piece.color != turn:
            return MoveState.NOT_YOUR_PIECE, None
      
        land_under_attack = False
        if isinstance(piece, King):
            land_under_attack = self.board.is_square_in_check(turn, to_pos)
        
        result = piece.can_move(self.board, from_pos, to_pos, land_under_attack)
        will_be_in_check = self._move_will_leave_in_check_state(result, from_pos, to_pos, turn)
          
        # TODO: this check is in king.can_move too since i can't figure the best way to
        # place it. Since we dealing with messaging, i put the copy below but since is
        # defined that is not a valid move from king if it will be in check so i put
        # the same logic there. Maybe i can put MoveState as a MoveResult property
        # and remove it from here.
        # HACK: since the final position is a lie (end != rook pos but rook.r,rook.c-1)
        # and we have to check if the ACTUAL position where the king is going is in check
        if isinstance(result, CastlingMoveResult):
            if self.board.is_square_in_check(turn, result.king_final_pos):
                return MoveState.KING_WILL_BE_IN_CHECK, None 
            
            if self.board.is_square_in_check(self._turn, result.rook_final_pos):
                return MoveState.KING_PATH_ATTACKED, None 
        
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

    def _check_end_game(self):
        # we check for the other player since he's the one who suffered by the last turn
        the_other_player = self._turn.reverse()
        if self._checkmated(the_other_player):
            self.game_ended = True
            raise ChessException(f"CHECKMATE\n{the_other_player} have won!")
        elif self._stalemated(the_other_player):
            self.game_ended = True
            raise ChessException(f"Draw by STALEMATE")

    def promote(self, piece : Piece):
        self.move_result_waiting_promotion.promoted_to = piece(self._turn)
        # since move is not called in play_turn if needs to promote
        self.move(self.move_result_waiting_promotion)
        self.move_result_waiting_promotion = None

    def replay(self, moves):
        for rs in moves:
            self.move(rs)
            self._check_end_game()
            yield rs
            self.change_turn()
        
    def play_turn (self, from_pos : Position, to_pos : Position):
        if self.game_ended or self.move_result_waiting_promotion:
            return None

        rs, mr = self._check_move_state(from_pos, to_pos)

        if rs == MoveState.CAN_BE_PLACED:

            self._check_end_game()
            if isinstance(mr, MoveResult) and mr.should_promote:
                self.move_result_waiting_promotion = mr
                raise PromotionException()
            
            self.move(mr)
            self.change_turn()

        elif rs == MoveState.CAN_NOT_BE_PLACED:
            raise ChessException("The selected piece can't be place on the selected spot")
        elif rs == MoveState.KING_IN_CHECK:
            raise ChessException(f"You can't move since the king is in check")
        elif rs == MoveState.KING_WILL_BE_IN_CHECK:
            raise ChessException(f"If you move this piece there, the king will be in check")
        elif rs == MoveState.KING_PATH_ATTACKED:
            raise ChessException(f"Your can castle to this side since the king's patch is being attacked")
        else:
            pass # nothing
        
    def play_turn_ia_start(self):
        if self.game_ended or self.move_result_waiting_promotion:
            return None
        # since is confusing to de i.a do make
        # the move w/o the board being updated
        # the UI will call it instead of it
        # being call on the play_turn()
        
        # TODO: we don't handle when the a.i don't have valid moves

        _, ai_move = ai.calc_best_move(self.ai_difficulty, self, Color.BLACK)
        if ai_move:

            self._check_end_game()
            if ai_move.should_promote:
                ai_move.promoted_to = Queen(Color.BLACK)
            
            self.move(ai_move)
        
            print("ai::", ai_move)
            return (ai_move.from_pos, ai_move.to_pos)

    def play_turn_ia_end(self):
        self.change_turn()


