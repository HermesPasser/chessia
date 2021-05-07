from engine.game import Game, MoveState
from engine.color import Color
from engine.pieces import Bishop, Rook
from engine.position import Position
from engine.move_result import MoveResult
from utils import load_board
import unittest

class GameTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def assertMoveState(self, turn, start, end, state):
        self.game._turn = turn       
        result, _ = self.game._check_move_state(start, end)
        self.assertEqual(result, state, f"Expecting {state}, given {result}")
    
    def test_check_move_state_returns_can_be_placed(self):
        self.assertTrue(False)
    
    def test_check_move_state_returns_can_not_be_placed_if_leave_king_unprotected(self):
        # TODO: should this kind of move really lead to a CAN_NOT_BE_PLACED?
        """ You can't move since the bishop will left the king unprotected, if it is the rook being moved it would be fine. """
        load_board(self.game.board, \
            '===K====' +
            '===P====' +
            '========' +
            'Q=======' +
            '========' +
            'r===P===' +
            '===b====' + # right-side of bishop: 6x4
            '====k===')
        bishop_pos = self.game.board.get_piece_location(Color.WHITE, Bishop)
        self.assertMoveState(Color.WHITE, bishop_pos, Position(6, 4), MoveState.CAN_NOT_BE_PLACED)

        rook_pos = self.game.board.get_piece_location(Color.WHITE, Rook)
        self.assertMoveState(Color.WHITE, rook_pos, Position(rook_pos.x, rook_pos.y + 1), MoveState.CAN_BE_PLACED)
   
    def test_check_move_state_returns_not_your_piece(self):
        self.assertTrue(False)

    def test_check_move_state_returns_no_piece_to_move(self):
        self.assertTrue(False)

    def test_check_move_state_returns_king_in_check(self):
        self.assertTrue(False)

    def test_check_move_state_returns_king_will_be_in_check(self):
        self.assertTrue(False)

"""
test the _check_move_state and _move_will_leave_in_check_state in the case
'===K====' +
'===P====' +
'========' +
'Q=======' +
'========' +
'========' +
'===b====' +
'====k==='

i think it should say the king is in check
'===K====' +
'===P====' +
'===R====' +
'Q=======' +
'========' +
'========' +
'========' +
'==b=k=p='

stalemate (draw)
'========' +
'==r=r===' +
'q=======' +
'===K====' +
'q=======' +
'========' +
'========' +
'====k==='

checkmate
'========' +
'==r=r===' +
'q=======' +
'===K====' +
'q===b===' +
'========' +
'========' +
'====k==='
"""