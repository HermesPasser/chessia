from engine.pieces import Knight, King, Pawn
from engine.color import Color
from tests import valid_moves
from tests.pieces.piece_test_base import PieceTestBase

# TODO: there is lots os replication here, refactor
# TODO: check for invalid moves later
class KnightTest(PieceTestBase):
    def test_can_move_white(self):
        for l in valid_moves.wknight_checks_bking:
            self.assertCanMoveToNonEmptySpot(Knight, Color.WHITE, King, Color.BLACK, l)

    def test_can_move_black(self):
        for l in valid_moves.bknight_checks_wking:
            self.assertCanMoveToNonEmptySpot(Knight, Color.BLACK, King, Color.WHITE, l)
    
    def test_cannot_move_white_your_piece_in_the_way(self):
        moves = [layout
            .replace('y', 'n')
            .replace('x', 'p')
            for layout in valid_moves.knight_valid_moves] 
         
        for l in moves:
            self.assertCanNotMoveToNonEmptySpot(Knight, Color.WHITE, Pawn, Color.WHITE, l)

    def test_cannot_move_black_your_piece_in_the_way(self):
        moves = [layout
            .replace('y', 'N')
            .replace('x', 'P')
            for layout in valid_moves.knight_valid_moves] 
          
        for l in moves:
            self.assertCanNotMoveToNonEmptySpot(Knight, Color.BLACK, Pawn, Color.BLACK, l)
    
    def test_can_move_to_valid_empty_spot_white(self):
        moves = [layout
            .replace('x', 'n')
            .replace('y', '0')
            for layout in valid_moves.knight_valid_moves] 
            
        for l in moves:
            self.assertCanMoveToEmptySpot(Knight, Color.WHITE, l)
  
    def test_can_move_to_valid_empty_spot_black(self):
        moves = [layout
            .replace('x', 'N')
            .replace('y', '0')
            for layout in valid_moves.knight_valid_moves] 
            
        for l in moves:
            self.assertCanMoveToEmptySpot(Knight, Color.BLACK, l)
