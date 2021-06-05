# ChessIA

The hacky-est chess engine you will ever see, made for an ai class

## How to play

Well, like any other chess

**Options & debug options**

_q_: undo the last two moves  
_w_: dumps the chessboard into the terminal (will break if unicode characters aren't supported)  
_r_: turn the a.i off  
_d_: change the turn  
_esc_: open the main window (the game will be paused). Good if you want to change the difficulty  

## Difficulty

This engine uses a poor man's version from the minimax with alpha-delta pruning, therefore greater the difficulty, the longer you will have to wait until the movement is made.  

The implementation is based on Brandon Yanofsky's [chess a.i](https://github.com/byanofsky/chess-ai-2) and uses Larry Kaufman’s suggested values to evaluete the pieces.  

**The difficulties**  
depth set to 2: _Too Young to Lose_  
depth set to 3: _Checkmate Me Plenty_  
depth set to 4: _Ultra Inteligence_  
depth set to 5: _Chessmaster Incarnate_  

## Replay

When the game ends you can save de match to be watched later.   

The source comes with the foolsmate.chessia file, which shows a fool's mate.

## License

See _LICENSE_ file