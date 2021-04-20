from pieces import *
from color import Color
from board import Board
from utils import load_board, make_spots, piece_from_char
from tests import valid_moves
import unittest

class BoardTests(unittest.TestCase):
    # yes, the board is upside down so the pawns can't do much. I'm not fixing it
    board_layout = \
        'rnbq=bnr\n' +\
        'pppppppp\n' +\
        '==k===R=\n' +\
        '===Q====\n' +\
        '==p=p===\n' +\
        '==PB=r==\n' +\
        'PP=PPP=P\n' +\
        'RNBQKBNR\n'

    def setUp(self):
        self.board = Board(False)   

    def test_is_square_in_check_returns_true(self):
        for l in valid_moves.checked_positions:
            load_board(self.board, l)

            # the only purpose of the 'piece' piece here is to get its position
            target_pos = self.board.get_piece_location(Color.BLACK, Piece)
            self.board.set(target_pos.x, target_pos.y, None)
            
            self.assertTrue(self.board.is_square_in_check(Color.WHITE, target_pos))

    def actual_is_in_check_returns_true(self, color, layout):
        load_board(self.board, layout)
        self.assertTrue(self.board.in_check(color))

    def test_is_in_check_white_returns_true(self):
        layouts = []
        layouts += valid_moves.bknight_checks_wking
       
        layouts.append(\
          '===R====' +\
          '========' +\
          '===k====' +\
          '========' +\
          '========' +\
          '========' +\
          '========' +\
          '===K====')
        
        layouts.append(\
          '========' +\
          '========' +\
          '===k====' +\
          '========' +\
          '========' +\
          '========' +\
          '===Q====' +\
          '===K====')
        
        layouts.append(\
          '========' +\
          '========' +\
          '===k====' +\
          '==B=====' +\
          '========' +\
          '========' +\
          '========' +\
          '===K====')

        layouts.append(\
          '========' +\
          '========' +\
          '===k====' +\
          '====Q===' +\
          '========' +\
          '========' +\
          '========' +\
          '===K====')

        layouts.append(\
          '========' +\
          '==P=====' +\
          '===k====' +\
          '========' +\
          '========' +\
          '========' +\
          '========' +\
          '===K====')

        for l in layouts:
            self.actual_is_in_check_returns_true(Color.WHITE, l)

    def test_is_in_check_black_returns_true(self):
        layouts = []
        layouts += valid_moves.wknight_checks_bking
       
        layouts.append(\
          '===r====' +\
          '========' +\
          '===K====' +\
          '========' +\
          '========' +\
          '========' +\
          '========' +\
          '===k====')
        
        layouts.append(\
          '========' +\
          '========' +\
          '===K====' +\
          '========' +\
          '========' +\
          '========' +\
          '===q====' +\
          '===k====')
        
        layouts.append(\
          '========' +\
          '========' +\
          '===K====' +\
          '==b=====' +\
          '========' +\
          '========' +\
          '========' +\
          '===k====')

        layouts.append(\
          '========' +\
          '========' +\
          '===K====' +\
          '====q===' +\
          '========' +\
          '========' +\
          '========' +\
          '===k====')

        layouts.append(\
          '========' +\
          '========' +\
          '===K====' +\
          '====p===' +\
          '========' +\
          '========' +\
          '========' +\
          '===k====')

        for l in layouts:
            self.actual_is_in_check_returns_true(Color.BLACK, l)

    def actual_get_test(self, x, y, piece_char):
        load_board(self.board, BoardTests.board_layout)
        rs = self.board.get(x, y)
        self.assertEqual(rs, piece_from_char(piece_char))

    def test_get(self):
        self.actual_get_test(0, 0, 'r')
        self.actual_get_test(3, 3, 'Q')
        self.actual_get_test(3, 6, None)
        self.actual_get_test(7, 7, 'R')
        self.actual_get_test(3, 0, None)

    def test_is_empty_spot_returns_true(self):
        load_board(self.board, BoardTests.board_layout)
        self.assertTrue(self.board.is_empty_spot(2, 0))
        self.assertTrue(self.board.is_empty_spot(3, 1))
        self.assertTrue(self.board.is_empty_spot(4, 6))
        self.assertTrue(self.board.is_empty_spot(6, 2))
        self.assertTrue(self.board.is_empty_spot(6, 6))

    def test_is_empty_spot_returns_false(self):
        load_board(self.board, BoardTests.board_layout)
        self.assertFalse(self.board.is_empty_spot(0, 1))
        self.assertFalse(self.board.is_empty_spot(5, 3))
        self.assertFalse(self.board.is_empty_spot(5, 5))
        self.assertFalse(self.board.is_empty_spot(6, 7))
        self.assertFalse(self.board.is_empty_spot(0, 7))
        self.assertFalse(self.board.is_empty_spot(7, 7))

    def actual_vertical_test(self, start : Position, end : Position, expected):
        load_board(self.board, BoardTests.board_layout)
        rs = self.board.get_pieces_range_vertical(start, end)
        self.assertSequenceEqual(rs, expected)

    def test_get_pieces_range_vertical_top_bottom(self):
        self.actual_vertical_test(Position(1, 5), Position(6, 5), make_spots('p<1,5>', 'r<5,5>', 'P<6,5>'))

    def test_get_pieces_range_vertical_top_bottom_empty(self):
        self.actual_vertical_test(Position(2, 1), Position(3, 1), [])

    def test_get_pieces_range_vertical_bottom_top(self):
        self.actual_vertical_test(Position(7, 1), Position(6, 1), make_spots('N<7,1>', 'P<6,1>'))

    def test_get_pieces_range_vertical_bottom_top_empty(self):
        self.actual_vertical_test(Position(5, 0), Position(2, 0), [])

    def actual_horizontal_test(self, start : Position, end : Position, expected):
        load_board(self.board, BoardTests.board_layout)
        rs = self.board.get_pieces_range_horizontal(start, end)
        self.assertSequenceEqual(rs, expected)

    def test_get_pieces_range_horizontal_left_right(self):
        self.actual_horizontal_test(Position(5, 1), Position(5, 5), make_spots('P<5,2>', 'B<5,3>', 'r<5,5>'))

    def test_get_pieces_range_horizontal_left_right_empty(self):
        self.actual_horizontal_test(Position(3, 0), Position(3, 2), [])

    def test_get_pieces_range_horizontal_right_left(self):
        self.actual_horizontal_test(Position(2, 6), Position(2, 2), make_spots('R<2,6>', 'k<2,2>'))

    def test_get_pieces_range_horizontal_right_empty(self):
        self.actual_horizontal_test(Position(4, 1), Position(4, 0), [])

    def actual_diagonal_test(self, position_start, position_end, expected):     
        load_board(self.board, BoardTests.board_layout)
        rs = self.board.get_pieces_range_diagonal(position_start.x, position_start.y, position_end.x, position_end.y)
        self.assertSequenceEqual(rs, expected)

    def test_get_pieces_range_diagonal_nw_se_1(self):
        self.actual_diagonal_test(Position(2, 2), Position(5, 5), make_spots('k<2,2>', 'Q<3,3>', 'p<4,4>', 'r<5,5>'))

    def test_get_pieces_range_diagonal_nw_se_2(self):
        self.actual_diagonal_test(Position(6, 6), Position(3, 3), make_spots('r<5,5>', 'p<4,4>', 'Q<3,3>'))

    def test_get_pieces_range_diagonal_nw_se_empty(self):
        self.actual_diagonal_test(Position(2, 1), Position(4, 3), [])

    def test_get_pieces_range_diagonal_se_nw(self):
        self.actual_diagonal_test(Position(6, 4), Position(5, 3), make_spots('P<6,4>', 'B<5,3>'))

    def test_get_pieces_range_diagonal_se_nw_empty(self):
        self.actual_diagonal_test(Position(5, 4), Position(3, 2), [])

    def test_get_pieces_range_diagonal_ms_ne(self):
        self.actual_diagonal_test(Position(5, 1), Position(1, 5), make_spots('p<4,2>', 'Q<3,3>', 'p<1,5>'))

    def test_get_pieces_range_diagonal_ms_ne_empty(self):
        self.actual_diagonal_test(Position(5, 0), Position(2, 3), [])

    def test_get_pieces_range_diagonal_me_ms(self):
        self.actual_diagonal_test(Position(4, 5), Position(0, 1), make_spots('p<1,2>', 'n<0,1>'))

    def test_get_pieces_range_diagonal_me_ms_empty(self):
        self.actual_diagonal_test(Position(4, 5), Position(2, 3), [])
