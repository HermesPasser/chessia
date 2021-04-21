from pieces import Queen, Pawn, Bishop
from color import Color
from tests.piece_test_base import PieceTestBase

class QueenTest(PieceTestBase):
    def test_can_move_diagonally(self):
        self.assertCanMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '=====0==' +\
            '========' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '========' +\
            '========' +\
            '0=======' +\
            '========')

        self.assertCanMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '==0=====' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '========' +\
            '=====0==' +\
            '========' +\
            '========')

    def test_can_not_move_diagonally_ally_piece_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '=====0==' +\
            '====p===' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '========' +\
            '=P======' +\
            '0=======' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '=0======' +\
            '==p=====' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '====P===' +\
            '=====0==' +\
            '========' +\
            '========')

    def test_can_not_move_diagonally_too_many_enemy_pieces_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '======0=' +\
            '=====P==' +\
            '====P===' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '==p=====' +\
            '=p======' +\
            '0=======' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '0=======' +\
            '=P======' +\
            '==P=====' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '====p===' +\
            '=====p==' +\
            '======0=' +\
            '========')

    def test_can_capture_diagonally_piece_on_land_spot(self):
        self.assertCanMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '=====P==' +\
            '========' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '==p=====' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            'P=======' +\
            '========' +\
            '========' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '========' +\
            '=====p==' +\
            '========' +\
            '========')

    def test_can_not_capture_diagonally_piece_on_land_spot_piece_in_the_way(self):
        self.assertCanNotMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '=====P==' +\
            '====R===' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '==r=====' +\
            '=p======' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            'P=======' +\
            '=R======' +\
            '========' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '====R===' +\
            '=====p==' +\
            '========' +\
            '========')
          
    def test_can_not_move_wrong_diagonals(self):
        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '===q====' +\
            '========' +\
            '========' +\
            '=====0==' +\
            '========' +\
            '========')
        
        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '=0======' +\
            '===q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '===q====' +\
            '========' +\
            '========' +\
            '=0======' +\
            '========' +\
            '========')
        
        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '===q====' +\
            '=====0==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_move_vertically(self):
        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '===Q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===0====')

        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '===Q====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '===0====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '========')

        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===0====' +\
            '===Q====' +\
            '========')

    def test_can_move_hozitontally(self):
        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '0==Q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Q===0' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_vertically_ally_piece_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===q====' +\
            '========' +\
            '===p====' +\
            '===0====' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '===0====' +\
            '===P====' +\
            '===Q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_horizontally_ally_piece_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '==Q=P0==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '0p=q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_vertically_too_many_enemy_pieces_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '===Q====' +\
            '========' +\
            '===p====' +\
            '===p====' +\
            '===0====' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '======0=' +\
            '========' +\
            '======P=' +\
            '========' +\
            '======P=' +\
            '========' +\
            '=====q==' +\
            '========')

    def test_can_not_move_horizontally_too_many_enemy_pieces_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '==Q=pp=0' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=0=PP=q=' +\
            '========')

    def test_can_capture_piece_on_land_spot_vertically(self):
        self.assertCanMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '===p====' +\
            '========' +\
            '========' +\
            '===Q====' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '==q=====' +\
            '========' +\
            '========' +\
            '========' +\
            '==P=====' +\
            '========' +\
            '========')

    def test_can_capture_piece_on_land_spot_horizontally(self):
        self.assertCanMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=p==Q===' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '==q===P=' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_capture_piece_on_land_spot_vertically_piece_in_the_way(self):
        self.assertCanNotMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '====p===' +\
            '====b===' +\
            '========' +\
            '====Q===' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '==q=====' +\
            '========' +\
            '========' +\
            '==B=====' +\
            '==P=====' +\
            '========' +\
            '========')

    def test_can_not_capture_piece_on_land_spot_horizontally_piece_in_the_way(self):
        self.assertCanNotMoveToNonEmptySpot(Queen, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=pb=Q===' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Queen, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===q=BP=' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
