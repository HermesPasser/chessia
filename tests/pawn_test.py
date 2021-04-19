from pieces import *
from color import Color
from board import Board
from utils import load_board, make_spots, piece_from_char
from tests import valid_moves
import unittest

# TODO: test invalid move when pawn try to go backwards
# TODO: test the same stuff for black Pawn
# TODO: figure out a way to get rid of the duplicate code
# TODO: test pawn try to move where there is a piece
# TODO: eu inverti qual cor fica em cima, e por isso tenho
# que inverter qual peça que deve descer
class PawnTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(False)

    def test_can_move_black_diagonal_left(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '==q=====' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.WHITE, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_move_white_diagonal_left(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '==Q=====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_not_move_black_diagonal_left_backwards(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '==q=====' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.WHITE, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_not_move_white_diagonal_left_backwards(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '==Q=====' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    # TODO: this is passing but should't
    def test_can_not_move_black_diagonal_right_backwards(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '====q===' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
          
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.WHITE, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    # TODO: this is passing but should't
    def test_can_not_move_white_diagonal_right_backwards(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '====Q===' +\
            '========' +\
            '========' +\
            '========')
          
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_not_move_black_diagonal_left(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '==q=====' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.WHITE, Queen)

        self.board.set(target_pos.x, target_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        
        self.assertFalse(rs)

    def test_can_not_move_white_diagonal_left(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '==Q=====' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Queen)

        self.board.set(target_pos.x, target_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        
        self.assertFalse(rs)

    def test_can_move_black_diagonal_right(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '====q===' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.WHITE, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_move_white_diagonal_right(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '====Q===' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Queen)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_not_move_black_diagonal_right(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '====q===' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.WHITE, Queen)

        self.board.set(target_pos.x, target_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_not_move_white_diagonal_right(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '====Q===' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Queen)

        self.board.set(target_pos.x, target_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_move_black_once(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_move_white_once(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '===0====' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_not_move_black_once_backwards(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '===0====' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        
        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_not_move_white_once_backwards(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '===0====' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        
        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_not_move_black_twice_backwards(self):
        load_board(self.board, \
            '========' +\
            '===0====' +\
            '========' +\
            '===P====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        
        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_not_move_white_twice_backwards(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===p====' +\
            '========' +\
            '===0====' +\
            '========' +\
            '========')
        
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        
        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_move_black_twice(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '========' +\
            '===0====' +\
            '========' +\
            '========')
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_move_white_twice(self):
        load_board(self.board, \
            '========' +\
            '===0====' +\
            '========' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertTrue(rs)

    def test_can_not_move_black_twice_because_is_2nd_move(self):
        load_board(self.board, \
            '========' +\
            '========' +\
            '========' +\
            '===P====' +\
            '========' +\
            '===0====' +\
            '========' +\
            '========')
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        pawn.is_first_move = False
        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)

    def test_can_not_move_white_twice_because_is_2nd_move(self):
        load_board(self.board, \
            '========' +\
            '===0====' +\
            '========' +\
            '===p====' +\
            '========' +\
            '========' +\
            '========' +\
            '========')
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)

        target_pos = self.board.get_piece_location(Color.BLACK, Piece)
        self.board.set(target_pos.x, target_pos.y, None)

        pawn.is_first_move = False
        rs = pawn.can_move(self.board, pawn_pos, target_pos)
        self.assertFalse(rs)
