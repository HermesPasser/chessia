from utils import make_2d_array
from position import Position
from board import Board
from color import Color

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

    def move(self, from_pos : Position, to_pos : Position):
        """Return None if the move could be done or a string with the explanaition if not"""
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
        message = ''

        # the position has no piece
        if piece is None:
            return 'there is nothing on selected spot'

        # FIXME: selecting your own piece returns message instead of None, redo this
        # the clicked piece is from the other player
        # if piece.is_white() != self.get_current_turn():
            # return 'the selected piece is not yours'
        
        if piece.can_move(self.board, from_pos, to_pos):
            prev = self.board._board[from_pos.x][from_pos.y]
            self.board._board[to_pos.x][to_pos.y] = prev
            self.board._board[from_pos.x][from_pos.y] = None
        else:
            message = "the selected piece can't be place on the selected spot"

        # TODO: check if the move was valid and computed it to change turn...
        self.change_turn()
        return message if message == '' else None
