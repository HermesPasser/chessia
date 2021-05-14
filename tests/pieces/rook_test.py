from engine.pieces import Rook, Pawn, Bishop
from engine.color import Color
from tests.pieces.piece_test_base import PieceTestBase

class RookTest(PieceTestBase):
    def test_can_move_vertically(self):
        self.assertCanMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '===R====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===0====')

        self.assertCanMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '===R====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Rook, Color.BLACK, \
            '===0====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===R====' +\
            '========')

        self.assertCanMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===0====' +\
            '===R====' +\
            '========')

    def test_can_move_hozitontally(self):
        self.assertCanMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '0==R====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===R===0' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_vertically_piece_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Rook, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===r====' +\
            '========' +\
            '===p====' +\
            '===0====' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===r====' +\
            '========' +\
            '===P====' +\
            '===0====' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '===0====' +\
            '===P====' +\
            '===R====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '===0====' +\
            '===p====' +\
            '===R====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_horizontally_piece_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===Rp0==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===RP0==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '0p=r====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '0P=r====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_vertically_too_many_enemy_pieces_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '===R====' +\
            '========' +\
            '===p====' +\
            '===p====' +\
            '===0====' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.WHITE, \
            '======0=' +\
            '========' +\
            '======P=' +\
            '========' +\
            '======P=' +\
            '========' +\
            '======r=' +\
            '========')

    def test_can_not_move_horizontally_too_many_enemy_pieces_in_the_way(self):
        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '===Rpp=0' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=0=PP=r=' +\
            '========')

    def test_can_capture_piece_on_land_spot_vertically(self):
        self.assertCanMoveToNonEmptySpot(Rook, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '====p===' +\
            '========' +\
            '========' +\
            '====R===' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Rook, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '==r=====' +\
            '========' +\
            '========' +\
            '========' +\
            '==P=====' +\
            '========' +\
            '========')

    def test_can_capture_piece_on_land_spot_horizontally(self):
        self.assertCanMoveToNonEmptySpot(Rook, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=p==R===' +\
            '========' +\
            '========')

        self.assertCanMoveToNonEmptySpot(Rook, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '==r===P=' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_capture_piece_on_land_spot_vertically_piece_in_the_way(self):
        self.assertCanNotMoveToNonEmptySpot(Rook, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '====p===' +\
            '====b===' +\
            '========' +\
            '====R===' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Rook, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '==r=====' +\
            '========' +\
            '========' +\
            '==B=====' +\
            '==P=====' +\
            '========' +\
            '========')

    def test_can_not_capture_piece_on_land_spot_horizontally_piece_in_the_way(self):
        self.assertCanNotMoveToNonEmptySpot(Rook, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '=pb=R===' +\
            '========' +\
            '========')

        self.assertCanNotMoveToNonEmptySpot(Rook, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===rBP==' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_non_vertically_and_hozontally(self):
        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '====R===' +\
            '=====0==' +\
            '========' +\
            '========' +\
            '========')
        
        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '===0====' +\
            '====R===' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '====R===' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '=====0==' +\
            '====R===' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

        self.assertCanNotMoveToEmptySpot(Rook, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '====R===' +\
            '========' +\
            '======0=' +\
            '========' +\
            '========')

