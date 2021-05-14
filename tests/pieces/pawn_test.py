from engine.pieces import Pawn, Queen
from engine.color import Color
from tests.pieces.piece_test_base import PieceTestBase

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

    def test_can_not_move_black_diagonal_no_pice_on_landing_spot(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '==0=====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')

    def test_can_not_move_white_diagonal_no_pice_on_landing_spot(self):
        self.assertCanNotMoveToEmptySpot(Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '====0===' +\
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

    def test_can_move_white_en_passant_right(self):
        self.assertCanMoveToEmptySpotEnPassant(Pawn, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '====0===' +\
            '===pP===' +\
            '========' +\
            '========' +\
            '========', True)

        self.assertCanMoveToEmptySpotEnPassant(Pawn, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '====0===' +\
            '===pP===' +\
            '========' +\
            '========' +\
            '========' +\
            '========', True)

    def test_can_move_white_en_passant_right(self):
        self.assertCanMoveToEmptySpotEnPassant(Pawn, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '==0=====' +\
            '==Pp====' +\
            '========' +\
            '========' +\
            '========', True)

    def test_can_move_black_en_passant_left(self):
        self.assertCanMoveToEmptySpotEnPassant(Pawn, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===pP===' +\
            '===0====' +\
            '========' +\
            '========', True)

    def test_can_move_black_en_passant_right(self):
        self.assertCanMoveToEmptySpotEnPassant(Pawn, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '==Pp====' +\
            '===0====' +\
            '========' +\
            '========', True)
    
    def test_can_not_move_white_en_passant_not_on_the_mid_spots(self):
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '====0===' +\
            '===pP===' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========', True)

    def test_can_not_move_black_en_passant_not_on_the_mid_spots(self):
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '==Pp====' +\
            '===0====', True)
        
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '===pP===' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========' +\
            '========', True) 

    def test_can_not_move_white_en_passant_enemy_did_not_moved_twice(self):
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '====0===' +\
            '===pP===' +\
            '========' +\
            '========' +\
            '========', False)
        
    def test_can_not_move_black_en_passant_enemy_did_not_moved_twice(self):
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '===pP===' +\
            '===0====' +\
            '========' +\
            '========', False)

    def test_can_not_move_white_en_passant_right_enemy_is_not_a_pawn(self):
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===0====' +\
            '===Qp===' +\
            '========' +\
            '========' +\
            '========', True)
        
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.WHITE, Queen, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '====0===' +\
            '===pQ===' +\
            '========' +\
            '========' +\
            '========', True)

    def test_can_not_move_black_en_passant_right_enemy_is_not_a_pawn(self):
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '==Pq====' +\
            '===0====' +\
            '========' +\
            '========', True)
        
        self.assertCanNotMoveToEmptySpotEnPassant(Pawn, Color.BLACK, Queen, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '====qP==' +\
            '====0===' +\
            '========' +\
            '========', True)

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

    def test_can_move_black_once_piece_on_spot(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.BLACK, Pawn, Color.WHITE, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========')

    def test_can_move_white_once_piece_on_spot(self):
        self.assertCanNotMoveToNonEmptySpot(Pawn, Color.WHITE, Pawn, Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '===p====' +\
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

    def test_can_promote_white(self):
        self.assertPawnCanPromote(Color.WHITE, \
            '===0====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
    
    def test_can_promote_black(self):
        self.assertPawnCanPromote(Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '====P===' +\
            '====0===')
            
    def test_can_not_promote_white(self):
        self.assertPawnCanNotPromote(Color.WHITE, \
            '========' +\
            '===0====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
  
    def test_can_not_promote_black(self):
        self.assertPawnCanNotPromote(Color.BLACK, \
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '====P===' +\
            '====0===' +\
            '========')