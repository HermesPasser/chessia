from engine.pieces import Piece
from engine.color import Color
from engine.board import Board
from utils import load_board
import unittest

class PieceTestBase(unittest.TestCase):
    def setUp(self):
        self.board = Board(False)

    def get_targed_and_clean_spot(self):
        pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(pos.x, pos.y, None)
        return pos

    def assertCanMoveToEmptySpotEnPassant(self, piece_kind : Piece, color : Color, enemy_kind : Piece, enemy_color : Color, layout : str, enemy_did_moved_twice=True):
        """Test the en passant move by checking if a piece was captured on the sides of the pawn and by allowing to set if the piece moved twice
        """
        rs = self._canPieceMoveToEmptySpotEnPassant(piece_kind, color, enemy_kind, enemy_color, layout, enemy_did_moved_twice)
        self.assertTrue(rs)
    
    def assertCanNotMoveToEmptySpotEnPassant(self, piece_kind : Piece, color : Color, enemy_kind : Piece, enemy_color : Color, layout : str, enemy_did_moved_twice=True):
        """Test the en passant move by checking if a piece was captured on the sides of the pawn and by allowing to set if the piece moved twice
        """
        rs = self._canPieceMoveToEmptySpotEnPassant(piece_kind, color, enemy_kind, enemy_color, layout, enemy_did_moved_twice)
        self.assertFalse(rs)
     
    def _canPieceMoveToEmptySpotEnPassant(self, piece_kind : Piece, color : Color, enemy_kind : Piece, enemy_color : Color, layout : str, enemy_did_moved_twice) -> bool:
        load_board(self.board, layout)
        target_pos = self.get_targed_and_clean_spot()
        
        piece_pos = self.board.get_piece_location(color, piece_kind)
        piece = self.board.get(piece_pos.x, piece_pos.y)

        captured_pos = self.board.get_piece_location(enemy_color, enemy_kind)
        captured = self.board.get(captured_pos.x, captured_pos.y)
        captured.did_moved_twice = enemy_did_moved_twice

        land_under_attack = self.board.is_square_in_check(color, target_pos)
        rs = piece.can_move(self.board, piece_pos, target_pos, land_under_attack)
        return rs and rs.captured_position == captured_pos
    
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
        land_under_attack = self.board.is_square_in_check(color, target_pos)
        return piece.can_move(self.board, piece_pos, target_pos, land_under_attack)
 
    def assertCanMoveToNonEmptySpot(self, our_piece_kind : Piece, our_color : Color, other_piece_kind : Piece, other_color : Color, layout : str, our_first_move=True, other_first_move=True):
        """ """
        rs = self._canPieceMoveToNonEmptySpot(our_piece_kind, other_piece_kind, our_color, other_color, layout, our_first_move, other_first_move)
        self.assertTrue(rs)
 
    def assertCanNotMoveToNonEmptySpot(self, our_piece_kind : Piece, our_color : Color, other_piece_kind : Piece, other_color : Color, layout : str, our_first_move=True, other_first_move=True):
        """ """
        rs = self._canPieceMoveToNonEmptySpot(our_piece_kind, other_piece_kind, our_color, other_color, layout, our_first_move, other_first_move)
        self.assertFalse(rs)

    def _canPieceMoveToNonEmptySpot(self, our_piece_kind : Piece, other_piece_kind : Piece, our_color : Color, other_color : Color, layout : str, our_first_move=True, other_first_move=True) -> bool:
        load_board(self.board, layout)
        
        our_piece_pos = self.board.get_piece_location(our_color, our_piece_kind)
        our_piece = self.board.get(our_piece_pos.x, our_piece_pos.y)
        our_piece.is_first_move = our_first_move

        other_piece_pos = self.board.get_piece_location(other_color, other_piece_kind)
        other_piece = self.board.get(other_piece_pos.x, other_piece_pos.y)
        other_piece.is_first_move = other_first_move
        land_under_attack = self.board.is_square_in_check(our_color, other_piece_pos)
        
        return our_piece.can_move(self.board, our_piece_pos, other_piece_pos, land_under_attack)

