from pieces import *
from color import Color
from board import Board
from utils import load_board, make_spots
import unittest

class BoardTest(unittest.TestCase):
    board_layout = """
rnbq=bnr
pppppppp
==k===R=
===Q====
==p=p===
==PB=r==
PP=PPP=P
RNBQKBNR
"""  
    def setUp(self):
        self.board = Board(False)   

    def actual_vertical_test(self, start : Position, end : Position, expected):
        load_board(self.board, BoardTest.board_layout)
        rs = self.board.get_pieces_range_vertical(start, end)
        self.assertSequenceEqual(rs, expected)

    def test_get_pieces_range_vertical_top_bottom(self):
        self.actual_vertical_test(Position(1, 5), Position(6, 5), make_spots('p<1,5>', 'r<5,5>', 'P<6,5>'))

    def test_get_pieces_range_vertical_bottom_top(self):
        self.actual_vertical_test(Position(7, 1), Position(6, 1), make_spots('N<7,1>', 'P<6,1>'))

    def actual_horizontal_test(self, start : Position, end : Position, expected):
        load_board(self.board, BoardTest.board_layout)
        rs = self.board.get_pieces_range_horizontal(start, end)
        self.assertSequenceEqual(rs, expected)

    def test_get_pieces_range_horizontal_left_right(self):
        self.actual_horizontal_test(Position(5, 1), Position(5, 5), make_spots('P<5,2>', 'B<5,3>', 'r<5,5>'))

    def test_get_pieces_range_horizontal_right_left(self):
        self.actual_horizontal_test(Position(2, 6), Position(2, 2), make_spots('R<2,6>', 'k<2,2>'))

    def actual_diagonal_test(self, position_start, position_end, expected):     
        load_board(self.board, BoardTest.board_layout)
        rs = self.board.get_pieces_range_diagonal(position_start.x, position_start.y, position_end.x, position_end.y)
        self.assertSequenceEqual(rs, expected)

    def test_get_pieces_range_diagonal_nw_se_1(self):
        self.actual_diagonal_test(Position(2, 2), Position(5, 5), make_spots('k<2,2>', 'Q<3,3>', 'p<4,4>', 'r<5,5>'))

    def test_get_pieces_range_diagonal_se_nw(self):
        self.actual_diagonal_test(Position(6, 4), Position(5, 3), make_spots('P<6,4>', 'B<5,3>'))

    def test_get_pieces_range_diagonal_nw_se_2(self):
        self.actual_diagonal_test(Position(6, 6), Position(3, 3), make_spots('r<5,5>', 'p<4,4>', 'Q<3,3>'))

    def test_get_pieces_range_diagonal_ms_ne(self):
        self.actual_diagonal_test(Position(5, 1), Position(1, 5), make_spots('p<4,2>', 'Q<3,3>', 'p<1,5>'))

    def test_get_pieces_range_diagonal_me_ms(self):
        self.actual_diagonal_test(Position(4, 5), Position(0, 1), make_spots('p<1,2>', 'n<0,1>'))


if __name__ == '__main__':
   unittest.main()
