from pieces import Piece
from color import Color
from board import Board
from utils import load_board
import unittest

class PieceTestBase(unittest.TestCase):
    def setUp(self):
        self.board = Board(False)

    def get_targed_and_clean_spot(self):
        pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(pos.x, pos.y, None)
        return pos

    def assertCanMoveToEmptySpot(self, piece_kind : Piece, color : Color, layout : str, first_move=True):
        """Given a layout, it checks if the piece can move to the position specified by '0'
        \npiece_kind: the piece that will be searched, not the instance
        """
        rs = self._canPieceMoveToEmptySpot(piece_kind, color, layout, first_move)
        self.assertTrue(rs)
        
    def assertCanNotMoveToEmptySpot(self, piece_kind : Piece, color : Color, layout : str, first_move=True):
        """Given a layout, it checks if the piece can't move to the position specified by '0'
        \npiece_kind: the piece that will be searched, not the instance
        """
        rs = self._canPieceMoveToEmptySpot(piece_kind, color, layout, first_move)
        self.assertFalse(rs)

    def _canPieceMoveToEmptySpot(self, piece_kind : Piece, color : Color, layout : str, first_move=True) -> bool:
        load_board(self.board, layout)
        target_pos = self.get_targed_and_clean_spot()
        
        piece_pos = self.board.get_piece_location(color, piece_kind)
        piece = self.board.get(piece_pos.x, piece_pos.y)
        piece.is_first_move = first_move
        return piece.can_move(self.board, piece_pos, target_pos)
 
    def assertCanMoveToNonEmptySpot(self, our_piece_kind : Piece, our_color : Color, other_piece_kind : Piece, other_color : Color, layout : str):
        """ """
        rs = self._canPieceMoveToNonEmptySpot(our_piece_kind, other_piece_kind, our_color, other_color, layout)
        self.assertTrue(rs)
 
    def assertCanNotMoveToNonEmptySpot(self, our_piece_kind : Piece, our_color : Color, other_piece_kind : Piece, other_color : Color, layout : str):
        """ """
        rs = self._canPieceMoveToNonEmptySpot(our_piece_kind, other_piece_kind, our_color, other_color, layout)
        self.assertFalse(rs)

    def _canPieceMoveToNonEmptySpot(self, our_piece_kind : Piece, other_piece_kind : Piece, our_color : Color, other_color : Color, layout : str) -> bool:
        load_board(self.board, layout)
        
        our_piece_pos = self.board.get_piece_location(our_color, our_piece_kind)
        our_piece = self.board.get(our_piece_pos.x, our_piece_pos.y)
        
        other_piece_pos = self.board.get_piece_location(other_color, other_piece_kind)
        return our_piece.can_move(self.board, our_piece_pos, other_piece_pos)

