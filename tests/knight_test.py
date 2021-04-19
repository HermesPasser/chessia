from pieces import *
from color import Color
from board import Board
from utils import load_board, make_spots, piece_from_char
from tests import valid_moves
import unittest

# TODO: there is lots os replication here, refactor
# TODO: check for invalid moves later
class KnightTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(False)   

    def test_can_move_white(self):
        for l in valid_moves.wknight_checks_bking:
            load_board(self.board, l)

            knight_pos = self.board.get_piece_location(Color.WHITE, Knight)
            knight = self.board.get(knight_pos.x, knight_pos.y)

            # white_knight_valid_moves is a list with layouts where the Knight
            # can capture the king, therefore the king's loc 
            destination_pos = self.board.get_piece_location(Color.BLACK, King)

            rs = knight.can_move(self.board, knight_pos, destination_pos)
            self.assertTrue(rs)

    def test_can_move_black(self):
        for l in valid_moves.bknight_checks_wking:
            load_board(self.board, l)

            knight_pos = self.board.get_piece_location(Color.BLACK, Knight)
            knight = self.board.get(knight_pos.x, knight_pos.y)

            # white_knight_valid_moves is a list with layouts where the Knight
            # can capture the king, therefore the king's loc 
            destination_pos = self.board.get_piece_location(Color.WHITE, King)

            rs = knight.can_move(self.board, knight_pos, destination_pos)
            self.assertTrue(rs)
    
    def test_cannot_move_white_your_piece_in_the_way(self):
        for l in valid_moves.knight_valid_moves:
            load_board(self.board, l.replace('y', 'n').replace('x', 'p'))

            knight_pos = self.board.get_piece_location(Color.WHITE, Knight)
            knight = self.board.get(knight_pos.x, knight_pos.y)

            destination_pos = self.board.get_piece_location(Color.WHITE, Pawn)

            rs = knight.can_move(self.board, knight_pos, destination_pos)
            self.assertFalse(rs)
    
    def test_cannot_move_black_your_piece_in_the_way(self):
        for l in valid_moves.knight_valid_moves:
            load_board(self.board, l.replace('y', 'N').replace('x', 'P'))

            knight_pos = self.board.get_piece_location(Color.BLACK, Knight)
            knight = self.board.get(knight_pos.x, knight_pos.y)

            destination_pos = self.board.get_piece_location(Color.BLACK, Pawn)

            rs = knight.can_move(self.board, knight_pos, destination_pos)
            self.assertFalse(rs)
    
    def test_can_move_to_valid_empty_spot_white(self):
        moves = [layout
            .replace('x', 'n')
            .replace('y', 'p') # add a pawn to be able to get its position
            for layout in valid_moves.knight_valid_moves] 
            
        for l in moves:
            load_board(self.board, l)
            knight_pos = self.board.get_piece_location(Color.WHITE, Knight)
            knight = self.board.get(knight_pos.x, knight_pos.y)

            destination_pos = self.board.get_piece_location(Color.WHITE, Pawn)
            # we just need the postion, so we delete the pawn
            self.board.set(destination_pos.x, destination_pos.y, None)

            rs = knight.can_move(self.board, knight_pos, destination_pos)
            self.assertTrue(rs)
  
    def test_can_move_to_valid_empty_spot_black(self):
        moves = [layout
            .replace('x', 'N')
            .replace('y', 'p') # add a pawn to be able to get its position
            for layout in valid_moves.knight_valid_moves] 
            
        for l in moves:
            load_board(self.board, l)
            knight_pos = self.board.get_piece_location(Color.BLACK, Knight)
            knight = self.board.get(knight_pos.x, knight_pos.y)

            destination_pos = self.board.get_piece_location(Color.WHITE, Pawn)
            # we just need the postion, so we delete the pawn
            self.board.set(destination_pos.x, destination_pos.y, None)

            rs = knight.can_move(self.board, knight_pos, destination_pos)
            self.assertTrue(rs)