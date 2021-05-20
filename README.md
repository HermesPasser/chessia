# Poor Man's Chess (a.k.a chessia)
ai/chess project made for ai class

This is the hacky-est chess implementation you will ever see
=======
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

Make the engine play itself following a moves. Per line must have the zero-based position plus a '-' and the ending position (yes, it doesn't uses the algebraic notation) in the format "rxc-rxc-p" where:  
_r_ is the row  
_c_ is the column  
_p_ is the piece you are promoting the pawn to (no implemented yet so ignore '-p' part)  

By default you can watch a fool's mate.

## License

See _LICENSE_ file
