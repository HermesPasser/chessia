import random
import math
# Base: byanofsky.com/2017/07/06/building-a-simple-chess-ai/

random_sort = lambda a: 0.5 - random.random()

def evaluate_board(board, color):
    value = 0
    for r in range(board.SIZE):
        for c in range(board.SIZE):
            piece = board.get(r, c)
            if piece:
                value += piece.get_value() * (1 if piece.color == color else -1)

    return value

def calc_best_move(depth, game, player_color,alpha=-math.inf, beta=math.inf, is_maximizing_player=True):
    if depth == 0:
        value = evaluate_board(game.board, player_color)
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