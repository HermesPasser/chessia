from pieces import *
from color import Color
from board import Board
from utils import load_board, make_spots, piece_from_char
from tests import valid_moves
import unittest

# TODO: there is lots os replication here, refactor
# TODO: check for invalid moves later
class KnightTests(unittest.TestCase):
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

# TODO: test invalid move when pawn try to go backwards
# TODO: test the same stuff for black Pawn
# TODO: figure out a way to get rid of the duplicate code
# TODO: test pawn try to move where there is a piece
class PawnTests(unittest.TestCase):
    def setUp(self):
        self.board = Board(False) 
        self.board_layout_white = \
            '===z====' +\
            '===p====' +\
            '==PyP===' +\
            '===x====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' # z: 0x3 | P: 2x2 | x1: 2x3 | P: 2x4 | x2: 3x3 
        
        self.board_layout_black = \
            '========' +\
            '========' +\
            '========' +\
            '===x====' +\
            '===y====' +\
            '==pxp===' +\
            '===P====' +\
            '===z====' 

    def test_can_move_white_diagonal_left(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 2)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    def test_can_not_move_white_diagonal_left(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 2)

        self.board.set(destination_pos.x, destination_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)

    def test_can_move_white_diagonal_right(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 4)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    def test_can_not_move_white_diagonal_right(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 4)

        self.board.set(destination_pos.x, destination_pos.y, None) # remove pawn from position
        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)

    def test_can_move_white_once(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(2, 3)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    # TODO: test backwards twice
    def test_can_not_move_white_once_backwards(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(0, 3)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)

    def test_can_move_white_twice(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(3, 3)

        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertTrue(rs)

    def test_can_not_move_white_twice_because_is_2nd_move(self):
        load_board(self.board, self.board_layout_white)
        pawn_pos = self.board.get_piece_location(Color.WHITE, Pawn)
        pawn = self.board.get(pawn_pos.x, pawn_pos.y)
        destination_pos = Position(3, 3)

        pawn.is_first_move = False
        rs = pawn.can_move(self.board, pawn_pos, destination_pos)
        self.assertFalse(rs)
