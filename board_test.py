from pieces import *
from color import Color
from board import Board
from utils import load_board, make_spots
import unittest

class BoardTest(unittest.TestCase):
    def setUp(self):
        board_layout = """
rnbqkbnr
pppppppp
==k===R=
===Q====
==p=p===
==PB=r==
PP=PPP=P
RNBQKBNR
"""
        self.board = Board(False)
        load_board(self.board, board_layout)

    def actual_diagonal_test(self, position_start, position_end, expected):     
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
