from engine.game import Game, MoveState
from engine.color import Color
from engine.pieces import Bishop, Rook, King
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

    def test_checkmate(self):
        load_board(self.game.board, \
            '===K====' +
            '========' +
            '========' +
            '========' +
            'R=======' +
            '========' +
            '=p======' +
            'k===R===') # mate
        
        self.assertTrue(self.game._checkmated(Color.WHITE))

        load_board(self.game.board, \
            '===K====' +
            '========' +
            '========' +
            '========' +
            'R=======' +
            '========' +
            '========' +
            'k===R===') # not mate
        
        self.assertFalse(self.game._checkmated(Color.WHITE))
        
        load_board(self.game.board, \
            '===K====' +
            '========' +
            '========' +
            '========' +
            'R===q===' +
            '========' +
            '=p======' +
            'kp==R===') # not mate, queen can kil the attacker
        
        self.assertFalse(self.game._checkmated(Color.WHITE))

        load_board(self.game.board, \
            '========' +
            '==r=r===' +
            'q=======' +
            '===K====' +
            'q===b===' +
            '========' +
            '========' +
            '====k===')
        
        self.assertTrue(self.game._checkmated(Color.BLACK))
        
        load_board(self.game.board, \
            'RNB=KBNR' +
            'PPPP=PPP' +
            '====P===' +
            '========' +
            '======pQ' +
            '=====p==' +
            'ppppp==p' +
            'rnbqkbnr') #  fool's mate
        
        self.assertTrue(self.game._checkmated(Color.WHITE))
        
        load_board(self.game.board, \
            'RNBQKBNR' +
            'PPP=PPPP' +
            '===P====' +
            '========' +
            'q=======' +
            '==p=====' +
            'pp=ppppp' +
            'rnb=kbnr') # is not fool's mate since can be blocked
        
        self.assertFalse(self.game._checkmated(Color.WHITE))

        load_board(self.game.board,\
            '=======K' +
            '=====k==' +
            '======q=' +
            '========' +
            '========' +
            '========' +
            '========' +
            '========') # is not mate since the king is not in check
        
        self.assertFalse(self.game._checkmated(Color.BLACK))
          
    def test_stalemate(self):
        load_board(self.game.board,\
            '=======K' +
            '=====k==' +
            '======q=' +
            '========' +
            '========' +
            '========' +
            '========' +
            '========')
        
        self.assertTrue(self.game._stalemated(Color.BLACK))
        # is only stalemate if is the turn of the king w/o moves
        self.assertFalse(self.game._stalemated(Color.WHITE))

        load_board(self.game.board,\
            '=====K==' +
            '=====b==' +
            '=====k==' +
            '========' +
            '========' +
            '========' +
            '========' +
            '========')
        
        self.assertTrue(self.game._stalemated(Color.BLACK))
        self.assertFalse(self.game._stalemated(Color.WHITE))
        
        load_board(self.game.board,\
            'KB=====r' +
            '========' +
            '=k======' +
            '========' +
            '========' +
            '========' +
            '========' +
            '========')
        
        self._turn = Color.BLACK
        self.assertTrue(self.game._stalemated(Color.BLACK))
        self.assertFalse(self.game._stalemated(Color.WHITE))
        
        load_board(self.game.board,\
            '========' +
            '========' +
            '========' +
            '========' +
            '========' +
            '==K=====' +
            '=R======' +
            'k=======')
        
        self.assertTrue(self.game._stalemated(Color.WHITE))
        self.assertFalse(self.game._stalemated(Color.BLACK))
        
        load_board(self.game.board,\
            '========' +
            '========' +
            '=k======' +
            '========' +
            '========' +
            '=q======' +
            'P=======' +
            'K=======')
        
        self.assertTrue(self.game._stalemated(Color.BLACK))
        self.assertFalse(self.game._stalemated(Color.WHITE))

        load_board(self.game.board,\
            'k=======' +
            'P=======' +
            'K=======' +
            '========' +
            '=====B==' +
            '========' +
            '========' +
            '========')
        
        self.assertTrue(self.game._stalemated(Color.WHITE))
        self.assertFalse(self.game._stalemated(Color.BLACK))

    def test_check_move_state_returns_can_be_placed(self):
        load_board(self.game.board, \
            '===K====' +
            '===P====' +
            '===B====' +
            '========' + # in front-right of bishop: 3x4
            '========' +
            '===r====' +
            '===p====' +
            '===k====')

        bishop_pos = self.game.board.get_piece_location(Color.BLACK, Bishop)
        self.assertMoveState(Color.BLACK, bishop_pos, Position(3, 4), MoveState.CAN_BE_PLACED)
    
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
        self.assertMoveState(Color.WHITE, rook_pos, Position(rook_pos.r, rook_pos.c + 1), MoveState.CAN_BE_PLACED)
   
    def test_check_move_state_returns_not_your_piece(self):
        load_board(self.game.board, \
            '===K====' +
            '===P====' +
            '===B====' +
            '========' +
            '========' +
            '===r====' +
            '========' +
            '===k====')
        bishop_pos = self.game.board.get_piece_location(Color.BLACK, Bishop)
        self.assertMoveState(Color.WHITE, bishop_pos, Position(bishop_pos.r, bishop_pos.c + 1), MoveState.NOT_YOUR_PIECE)

    def test_check_move_state_returns_no_piece_to_move(self):
        load_board(self.game.board, \
            '===K====' +
            '===P====' +
            '===B====' +
            '========' +
            '========' +
            '===r====' +
            '===p====' +
            '===k====')

        self.assertMoveState(Color.BLACK, Position(0,0), Position(0, 1), MoveState.NO_PIECE_TO_MOVE)

    def test_check_move_state_returns_king_in_check(self):
        """ we can't eat the white bishop with the black rook since the white rook is attacking the black king """
        load_board(self.game.board, \
            '===K====' +
            '========' +
            '===r====' +
            '========' +
            '===R====' +
            '========' +
            '===b====' +
            '===k====')

        rook_pos = self.game.board.get_piece_location(Color.BLACK, Rook)
        target_pos = self.game.board.get_piece_location(Color.WHITE, Bishop)
        self.assertMoveState(Color.BLACK, rook_pos, target_pos, MoveState.KING_IN_CHECK)

    def test_check_move_state_returns_king_will_be_in_check(self):
        # this layout can test _move_will_leave_in_check_state too
        load_board(self.game.board, \
            '===K====' +
            '===P====' +
            '========' +
            'Q=======' +
            '========' +
            '========' +
            '===r====' +
            '====k===')

        rook_pos = self.game.board.get_piece_location(Color.WHITE, Rook)
        self.assertMoveState(Color.WHITE, rook_pos, Position(rook_pos.r, rook_pos.c - 1), MoveState.KING_WILL_BE_IN_CHECK)
        
        # testing castlling
        load_board(self.game.board, \
            '=K======' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '======R=' +\
            '====k==r' )

        king_pos = self.game.board.get_piece_location(Color.WHITE, King)
        rook_pos = self.game.board.get_piece_location(Color.WHITE, Rook)
        self.assertMoveState(Color.WHITE, king_pos, rook_pos, MoveState.KING_WILL_BE_IN_CHECK)

    def test_check_move_state_returns_king_path_attacked(self):
        load_board(self.game.board, \
            '=K===Q==' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '====k==r' )

        king_pos = self.game.board.get_piece_location(Color.WHITE, King)
        rook_pos = self.game.board.get_piece_location(Color.WHITE, Rook)
        self.assertMoveState(Color.WHITE, king_pos, rook_pos, MoveState.KING_PATH_ATTACKED)
        
        load_board(self.game.board, \
            '=K=Q====' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            '========' +\
            'r===k===' )

        king_pos = self.game.board.get_piece_location(Color.WHITE, King)
        rook_pos = self.game.board.get_piece_location(Color.WHITE, Rook)
        self.assertMoveState(Color.WHITE, king_pos, rook_pos, MoveState.KING_PATH_ATTACKED)
