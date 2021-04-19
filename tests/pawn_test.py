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
        self.board_layout_black = \
            '===Z====' +\
            '===P====' +\
            '==pYp===' +\
            '===X====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' # z: 0x3 | P: 2x2 | x1: 2x3 | P: 2x4 | x2: 3x3 

    def test_can_move_black_diagonal_left(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 2)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    def test_can_not_move_black_diagonal_left(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 2)

        self.board.set(destination_pos.x, destination_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)

    def test_can_move_black_diagonal_right(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 4)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    def test_can_not_move_black_diagonal_right(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 4)

        self.board.set(destination_pos.x, destination_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)

    def test_can_move_black_once(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 3)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    # TODO: test backwards twice
    def test_can_not_move_black_once_backwards(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(0, 3)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)

    def test_can_move_black_twice(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(3, 3)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    def test_can_not_move_black_twice_because_is_2nd_move(self):
        load_board(self.board, self.board_layout_black)
        pawn_pos = self.board.get_piece_location(Color.BLACK, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(3, 3)

        pawn.is_first_move = False
        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)
