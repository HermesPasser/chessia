from engine.game import Game
from engine.move_result import MoveResult
from utils import load_board
import unittest

class GameTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_check_move_state_returns_can_be_placed(self):
        self.assertTrue(False)
        
    def test_check_move_state_returns_can_be_placed(self):
        self.assertTrue(False)
     
    def test_check_move_state_returns_can_not_be_placed(self):
        self.assertTrue(False)
   
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

You can't move the 'b' cuzz 'k' will be in check but you can move 'r' since it will make 'k' not in check
'===K====' +
'===P====' +
'========' +
'Q=======' +
'========' +
'r===P===' +
'===b====' +
'====k==='

'===K====' +
'===P====' +
'========' +
'Q=======' +
'========' +
'====b===' +
'========' +
'=====k=='

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