from engine.pieces import Pawn, Queen
from engine.color import Color
from tests.piece_test_base import PieceTestBase

# TODO: test invalid move when pawn try to go backwards
# TODO: test the same stuff for black Pawn
# TODO: figure out a way to get rid of the duplicate code
# TODO: test pawn try to move where there is a piece
class PawnTest(PieceTestBase):
    def test_can_move_black_diagonal_left(self):
        self.assertCanMoveToNonEmptySpot(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '==q=====' +\
            '========' +\
            '========' +\
            '========')

    def test_can_move_white_diagonal_left(self):
        self.assertCanMoveToNonEmptySpot(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '==Q=====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_black_diagonal_left_backwards(self):
            self.assertCanNotMoveToNonEmptySpot(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '==q=====' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_white_diagonal_left_backwards(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '==Q=====' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_black_diagonal_right_backwards(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '====q===' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_white_diagonal_right_backwards(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '====Q===' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_black_diagonal_left(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '==q=====' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_white_diagonal_left(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '==Q=====' +\
            '========' +\
            '========' +\
            '========')

    def test_can_move_black_diagonal_right(self):
        self.assertCanMoveToNonEmptySpot(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '====q===' +\
            '========' +\
            '========' +\
            '========')

    def test_can_move_white_diagonal_right(self):
        self.assertCanMoveToNonEmptySpot(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '====Q===' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_black_diagonal_right(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '====q===' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_white_diagonal_right(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '====Q===' +\
            '========' +\
            '========' +\
            '========')

    def test_can_move_black_once(self):
        self.assertCanMoveToEmptySpot(Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========')

    def test_can_move_white_once(self):
        self.assertCanMoveToEmptySpot(Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '===0====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_black_once_backwards(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '===0====' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_white_once_backwards(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_black_twice_backwards(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.BLACK, \
            '========' +\
            '===0====' +\
            '========' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_white_twice_backwards(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '========' +\
            '===0====' +\
            '========' +\
            '========')

    def test_can_move_black_twice(self):
        self.assertCanMoveToEmptySpot(Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '========' +\
            '===0====' +\
            '========' +\
            '========')

    def test_can_move_white_twice(self):
        self.assertCanMoveToEmptySpot(Pawn, Color.WHITE, \
            '========' +\
            '===0====' +\
            '========' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_black_twice_because_is_2nd_move(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '========' +\
            '===0====' +\
            '========' +\
            '========', first_move=False)

    def test_can_not_move_white_twice_because_is_2nd_move(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.WHITE, \
            '========' +\
            '===0====' +\
            '========' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========', first_move=False)
