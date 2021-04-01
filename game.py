from utils import make_2d_array
from position import Position
from board import Board
from color import Color
from enum import Enum

class MoveState(Enum):
    # TODO: do i really need an enum for each type of move?
    CAN_BE_PLACED = 0
    CAN_NOT_BE_PLACED = 1
    NO_PIECE_TO_MOVE = 2
    NOT_YOUR_PIECE = 3
    
class Game():
    def __init__(self):
        self.board = Board()
        self._turn = Color.WHITE

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

    def _check_move_state(self, from_pos : Position, to_pos : Position) -> MoveState:
        """Return an enum corresponding to the state of the move."""
        # TODO: make the checks and delegate the important parts to Move and Piece
        # x check if from_pos has a piece
        # x check if from_pos' piece is from the current player
        # check if from_pos' piece is the king and if it is in check
        # check if from_pos' piece can be placed in to_pos
        # check if to_pos has no piece from the current player (if is not a special move)
        # check if to_pos is empty or has a piece from the other player
        # check if from_pos' piece is the king and if putting it in to_pos put it in check
        # check if has a winner (?)

        piece = self.board.get(from_pos.x, from_pos.y)

        # the position has no piece so return w/o switching the turn
        if piece is None:
            return MoveState.NO_PIECE_TO_MOVE

        # the clicked piece is from the other player
        if piece.color != self.get_current_turn():
            return MoveState.NOT_YOUR_PIECE
        
        # check if the piece can be moved on the spot
        if piece.can_move(self.board, from_pos, to_pos):
            return MoveState.CAN_BE_PLACED
        
        return MoveState.CAN_NOT_BE_PLACED 

    def play_turn (self, from_pos : Position, to_pos : Position):      
        rs = self._check_move_state(from_pos, to_pos)

        if rs == MoveState.CAN_BE_PLACED:
            self._move(from_pos, to_pos)
            self.change_turn()
        elif rs == MoveState.CAN_NOT_BE_PLACED:
            raise Exception("The selected piece can't be place on the selected spot")
        else:
            pass # nothing
        
        
