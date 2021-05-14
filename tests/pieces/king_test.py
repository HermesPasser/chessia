from engine.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from engine.color import Color
from tests.pieces.piece_test_base import PieceTestBase

class KingTest(PieceTestBase):
    def test_can_move(self):
        self.assertCanMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '===0====' +\
            '===K====' +\
            '========' +\
            '========' +\
            '========' +\
            '=====k==')
            
        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '==0=====' +\
            '===k====' +\
            '========' +\
            '========' +\
            '========' +\
            '======K=')
            
        self.assertCanMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '====0===' +\
            '===K====' +\
            '========' +\
            '========' +\
            '========' +\
            '=====k==')
            
        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '==0k====' +\
            '========' +\
            '========' +\
            '========' +\
            '=======K')
            
        self.assertCanMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K0===' +\
            '========' +\
            '========' +\
            '========' +\
            '====k===')
            
        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '====0===' +\
            '========' +\
            '========' +\
            '=====K==')
            
        self.assertCanMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '===k====')

        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '==0=====' +\
            '========' +\
            '========' +\
            '===K====')

    def test_can_not_twice(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '===0====' +\
            '========' +\
            '===K====' +\
            '========' +\
            '========' +\
            '========' +\
            '====k===')

    def test_can_not_move_rook_attaking_square(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '====k===' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===0==r=' +\
            '===K====')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '===K====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===0==R=' +\
            '===k====')

    def test_can_not_move_bishop_attaking_square(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '====0===' +\
            '========' +\
            '==b=====' +\
            '=======k')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '====0===' +\
            '========' +\
            '==B=====' +\
            '======K=')

    def test_can_not_move_knight_attaking_square(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '====0===' +\
            '==n=====' +\
            '========' +\
            '======k=')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '====0===' +\
            '==N=====' +\
            '========' +\
            '======K=')

    def test_can_not_move_pawn_attaking_square(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '===0====' +\
            '====p===' +\
            '========' +\
            '=k======')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '==P=====' +\
            '===0====' +\
            '===k====' +\
            '========' +\
            '========' +\
            '========' +\
            '==K=====')

    def test_can_black_castling_queen_side(self):
        self.assertCanMoveToNonEmptySpot(King, Color.BLACK, Rook, Color.BLACK, \
            'R===K===' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=k======')
    
    def test_can_black_castling_king_side(self):
        self.assertCanMoveToNonEmptySpot(King, Color.BLACK, Rook, Color.BLACK, \
            '====K==R' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=k======')

    def test_can_white_castling_queen_side(self):
        self.assertCanMoveToNonEmptySpot(King, Color.WHITE, Rook, Color.WHITE, \
            '=K======' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            'r===k===' )

    def test_can_white_castling_king_side(self):
        self.assertCanMoveToNonEmptySpot(King, Color.WHITE, Rook, Color.WHITE, \
            '=K======' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '====k==r' )
    
    def test_can_not_castling_not_rook_first_move(self):
        self.assertCanNotMoveToNonEmptySpot(King, Color.BLACK, Rook, Color.BLACK, \
            'R===K===' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=k======', False, True)
    
    def test_can_not_castling_not_king_first_move(self):
        self.assertCanNotMoveToNonEmptySpot(King, Color.BLACK, Rook, Color.BLACK, \
            'R===K===' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=k======', True, False)
    
    def test_can_castling_path_under_attack_queen_side(self):
        self.assertCanNotMoveToNonEmptySpot(King, Color.WHITE, Rook, Color.WHITE, \
            '=K=Q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            'r===k===' )
  
    def test_can_castling_path_under_attack_king_side(self):
        self.assertCanNotMoveToNonEmptySpot(King, Color.WHITE, Rook, Color.WHITE, \
            '=K======' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '======P=' +\
            '====k==r' )

    def test_opposition(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '===0====' +\
            '===k====' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '===0====' +\
            '===K====' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '==0=====' +\
            '===k====' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '====0===' +\
            '===k====' +\
            '========' +\
            '========')
       
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K0k==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
       
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '====0===' +\
            '===K=k==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '====0===' +\
            '===K=k==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K=k==' +\
            '====0===' +\
            '========' +\
            '========' +\
            '========')
            
        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '====0===' +\
            '===K=k==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===K=k==' +\
            '====0===' +\
            '========' +\
            '========' +\
            '========')