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

def calculate_best_move_one(game, player_color):
    # List all possible moves
    possible_moves = game.get_moves(player_color) # criar

    # Sort moves randomly, so the same move isn't always picked on ties
    possible_moves.sort(random_sort)

    # Exit if the game is over
    if game.game_ended or len(possible_moves) == 0:
        return

    # Search for move with highest value
    best_moveSoFar = None
    best_move_value = -math.inf
    for move in possible_moves:
        game.move(move)
        moveValue = evaluate_board(game.board, player_color)
        if moveValue > best_move_value:
            best_moveSoFar = move
            best_move_value = moveValue
        
        game.undo()

    return best_moveSoFar

def calc_best_move(depth, game, player_color,alpha=-math.inf, beta=math.inf, is_maximizing_player=True):
    # Base case: evaluate board
    # print('.', end='')
    if depth == 0:
        value = evaluate_board(game.board, player_color)
        return [value, None]

    # Recursive case: search possible moves
    best_move = None # best move not set yet
    possible_moves = game.get_moves(player_color)
    # possible_moves = ["Nc6", "Na6", "Nh6", "Nf6", "a6", "a5", "b6", "b5", "c6", "c5", "d6"]

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

        # Log the value of this move
        # print('Max: ' if is_maximizing_player else 'Min: ', depth, move, value, best_move, best_move_value)

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
        
        # Undo previous move
        game.undo()
        # Check for alpha beta pruning
        if beta <= alpha:
            # print('p')
            # print('Prune', alpha, beta)
            break
    return best_move or possible_moves[0]