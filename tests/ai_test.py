from engine.game import Game
from engine.color import Color
from engine.move_result import MoveResult
from engine.ai import calc_best_move
from utils import load_board
import unittest

class AiTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_if_ai_goes_for_the_simple_checkmate(self):
        # Since the a.i could perform a fools mate in one
        # move, any other move should be ignored since
        # instante checkmate is the best.
        load_board(self.game.board, \
                'RNBQKBNR' +
                'PPPP=PPP' +
                '====P===' +
                '========' +
                '======p=' +
                '=====p==' +
                'ppppp==p' +
                'rnbqkbnr')

        _, move_result = calc_best_move(2, self.game, Color.BLACK)
        self.game.move(move_result) 
        self.assertTrue(self.game._checkmated(Color.WHITE))
