from engine.move_result import MoveResult
from engine.color import Color
import random
import math
# Base: byanofsky.com/2017/07/06/building-a-simple-chess-ai/

random_sort = lambda a: 0.5 - random.random()

def _evaluate_board(board, color):
    value = 0
    for r in range(board.SIZE):
        for c in range(board.SIZE):
            piece = board.get(r, c)
            if piece:
                value += piece.get_value() * (1 if piece.color == color else -1)

    return value


def _evaluate_check(board, color):
    enemy = color.reverse()
    check_bonus = 45
    return check_bonus if board.in_check(enemy) else 0

def _evaluate_threats(game, color, depth):
    global _cached_white_mated, _cached_black_mated
    enemy = color.reverse()
    mate_bonus = 10000
    depth_bonus = 1

    enemy_mated = _cached_white_mated if enemy.is_white() else _cached_black_mated
    return mate_bonus * depth_bonus if enemy_mated else _evaluate_check(game.board, color)


def evaluate(game, color, depth):
    return _evaluate_board(game.board, color) + _evaluate_threats(game, color, depth) -_evaluate_threats(game, color.reverse(), depth)

# since we'll use mate to evaluate the board, why not save the processing
# by storing the value checked to stop the search
_cached_white_mated = None
_cached_black_mated = None

def _game_ended(game):
    global _cached_white_mated, _cached_black_mated
    _cached_white_mated = game._checkmated(Color.WHITE)
    _cached_black_mated = game._checkmated(Color.BLACK)
    return _cached_white_mated or _cached_black_mated


def calc_best_move(depth, game, player_color,alpha=-math.inf, beta=math.inf, is_maximizing_player=True):
    """=> (int, MoveResult)"""
    if depth == 0 or _game_ended(game):
        value = evaluate(game, player_color, depth)
        return [value, None]

    best_move = None # best move not set yet
    possible_moves = game.get_moves(player_color)

    # Set random order for possible moves
    possible_moves.sort(key=random_sort)
    
    # Set a default best move value
    best_move_value = -math.inf if is_maximizing_player else math.inf

    # Search through all possible moves
    for move in possible_moves:
        
        # Make the move, but undo before exiting loop
        game.move(move)
        
        # Recursively get the value from this move
        value = calc_best_move(depth - 1, game, player_color, alpha, beta, not is_maximizing_player)[0]

        if is_maximizing_player:
            # Look for moves that maximize position
            if value > best_move_value:
                best_move_value = value
                best_move = move
            
            alpha = max(alpha, value)
        else:
            # Look for moves that minimize position
            if value < best_move_value:
                best_move_value = value
                best_move = move
            
            beta = min(beta, value)
        
        game.undo()

        if beta <= alpha:
            break

    return [best_move_value, best_move or possible_moves[0]]