from pieces import Rook, Pawn, Bishop
from color import Color
from tests.piece_test_base import PieceTestBase

class BishopTest(PieceTestBase):
    def test_can_move(self):
        self.assertCanMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '=====0==' +\
            '========' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '========' +\
            '========' +\
            '0=======' +\
            '========')

        self.assertCanMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '========' +\
            '==0=====' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '========' +\
            '=====0==' +\
            '========' +\
            '========')

    def test_can_not_move_piece_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '=====0==' +\
            '====p===' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_piece_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '=====0==' +\
            '====P===' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '========' +\
            '=P======' +\
            '0=======' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '========' +\
            '=p======' +\
            '0=======' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '=0======' +\
            '==P=====' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '=0======' +\
            '==p=====' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '====p===' +\
            '=====0==' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '====P===' +\
            '=====0==' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '======0=' +\
            '=====P==' +\
            '====P===' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '==p=====' +\
            '=p======' +\
            '0=======' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '0=======' +\
            '=P======' +\
            '==P=====' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '====p===' +\
            '=====p==' +\
            '======0=' +\
            '========')

    def test_can_capture_piece_on_land_spot(self):
        self.assertCanMoveToNonEmptySpot(Bishop, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '=====P==' +\
            '========' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Bishop, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '==p=====' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Bishop, Color.WHITE, Pawn, Color.BLACK, \
            'P=======' +\
            '========' +\
            '========' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Bishop, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '========' +\
            '=====p==' +\
            '========' +\
            '========')

    def test_can_not_capture_piece_on_land_spot_piece_in_the_way(self):
        self.assertCanNotMoveToNonEmptySpot(Bishop, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '=====P==' +\
            '====R===' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Bishop, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '==r=====' +\
            '=p======' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Bishop, Color.WHITE, Pawn, Color.BLACK, \
            'P=======' +\
            '=R======' +\
            '========' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Bishop, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===B====' +\
            '====R===' +\
            '=====p==' +\
            '========' +\
            '========')
            
    def test_can_not_move_non_diagonally(self):
        self.assertCanNotMoveToEmptySpot(Bishop, Color.BLACK, \
            '========' +\
            '========' +\
            '===0====' +\
            '===B====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===b====' +\
            '========' +\
            '========' +\
            '===0====' +\
            '========')
          
    def test_can_not_move_wrong_diagonals(self):
        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '========' +\
            '===b====' +\
            '========' +\
            '========' +\
            '=====0==' +\
            '========' +\
            '========')
        
        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '=0======' +\
            '===b====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '========' +\
            '===b====' +\
            '========' +\
            '========' +\
            '=0======' +\
            '========' +\
            '========')
        
        self.assertCanNotMoveToEmptySpot(Bishop, Color.WHITE, \
            '========' +\
            '========' +\
            '===b====' +\
            '=====0==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
