from ui import make_window
from engine.game import Game

try:
    game = Game()
    make_window(game)
except Exception as e:
    print(game.get_current_turn())
    print(game.board)
    raise e
