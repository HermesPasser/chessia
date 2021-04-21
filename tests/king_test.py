from pieces import Bishop, King, Knight, Pawn, Queen, Rook
from color import Color
from tests.piece_test_base import PieceTestBase

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
            '========')
            
        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '==0=====' +\
            '===k====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
            
        self.assertCanMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '====0===' +\
            '===K====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
            
        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '==0k====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
            
        self.assertCanMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K0===' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
            
        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '====0===' +\
            '========' +\
            '========' +\
            '========')
            
        self.assertCanMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '==0=====' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_twice(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '===0====' +\
            '========' +\
            '===K====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_rook_attaking_square(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===0==r=' +\
            '===K====')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
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
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '====0===' +\
            '========' +\
            '==B=====' +\
            '========')

    def test_can_not_move_knight_attaking_square(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '====0===' +\
            '==n=====' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===k====' +\
            '====0===' +\
            '==N=====' +\
            '========' +\
            '========')

    def test_can_not_move_pawn_attaking_square(self):
        self.assertCanNotMoveToEmptySpot(King, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===K====' +\
            '===0====' +\
            '====p===' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(King, Color.WHITE, \
            '========' +\
            '==P=====' +\
            '===0====' +\
            '===k====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
