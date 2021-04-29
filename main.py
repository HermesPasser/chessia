from ui import make_window
from game import Game

game = Game()
# from utils import load_board
# load_board(game.board, \
    # '========' +\
    # '=p=P=P==' +\
    # '========' +\
    # '=p=q==P=' +\
    # '========' +\
    # '==p=pPP=' +\
    # '========' +\
    # '====k=K=')
    # 'RNB=KB=R' +\
    # 'PPPP=PPP' +\
    # '====P==N' +\
    # '========' +\
    # '===pp===' +\
    # '==n===Qp' +\
    # 'ppp===pp' +\
    # 'r=bqkbnr')
make_window(game)
