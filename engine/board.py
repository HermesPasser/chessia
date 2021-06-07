from utils import make_2d_array
from engine.color import Color
from engine.pieces import *
from io import StringIO

class Board():
    SIZE = 8

    def __init__(self, pre_populate=True):
        self._board = make_2d_array(range(Board.SIZE), None)
        self.white_king_loc = None
        self.black_king_loc = None
        if pre_populate:
            self._make_board()
            self.white_king_loc = self.get_piece_location(Color.WHITE, King)
            self.black_king_loc = self.get_piece_location(Color.BLACK, King)

    def get_king_loc_by_color(self, color : Color) -> Piece:
        return self.black_king_loc if color == Color.BLACK else self.white_king_loc

    def __repr__(self):
        # FIXME: i think is omitting something
        sio = StringIO()
        for _, c, p in self._iterate():
            p = '=' if p is None else str(p)
            sio.write(p)
            
            if c == Board.SIZE -1:
                sio.write("\n")
        s = sio.getvalue()
        sio.close()
        return s.strip()

    def get(self, r: int, c: int):
        if r < 0 or r >= Board.SIZE or c < 0 or c >= Board.SIZE:
            raise Exception("Index out of bound")

        return self._board[r][c]

    def set(self, r: int, c: int, piece : Piece):
        if r < 0 or r >= Board.SIZE or c < 0 or c >= Board.SIZE:
            raise Exception("Index out of bound")

        if isinstance(piece, King):
            if piece.color == Color.WHITE:
                self.white_king_loc = Position(r, c)
            else:
                self.black_king_loc = Position(r, c)
        
        self._board[r][c] = piece

    def move(self, from_pos : Position, to_pos : Position): 
        prev = self._board[from_pos.r][from_pos.c]
        
        if isinstance(self._board[to_pos.r][to_pos.c], King):
            raise Exception("Can't override the king")

        self._board[to_pos.r][to_pos.c] = prev
        self._board[from_pos.r][from_pos.c] = None

        if isinstance(prev, King):
            if prev.color == Color.WHITE:
                self.white_king_loc = to_pos
            else:
                self.black_king_loc = to_pos

    def get_piece_location(self, color : Color, type_piece : type) -> Position:
        if type(type_piece) is King:
            if self.white_king_loc and color == Color.WHITE:
                return self.white_king_loc
            elif self.black_king_loc:
                return self.black_king_loc
                
        for row, col, p in self._iterate():
            if type(p) is type_piece and p.color == color:
                return Position(row, col)

        raise Exception(f"No {color} {type_piece.__name__} found")

    def in_check(self, color):
        return self.is_square_in_check(color, self.get_king_loc_by_color(color))

    # TODO: do we really need to let it here? Game and King
    # make sense having it but it deals with the internals 
    # of the board.
    def is_square_in_check(self, color, pos_to_check : Position):
        is_empty_spot = self.is_empty_spot(pos_to_check.r, pos_to_check.c)
        other_player_color = color.reverse()
       
        in_check = False
        for piece, pos in self.iterate_material(other_player_color):
            if piece is not None:
                clear_spot = False

                # Remember: the pawn eats diagonally and moves vertically
                if isinstance(piece, Pawn) and is_empty_spot:
                    clear_spot = True
                    self.set(pos_to_check.r, pos_to_check.c, Pawn(color))
                
                if piece.can_move(self, pos, pos_to_check):
                    in_check = True

                if clear_spot:
                    self.set(pos_to_check.r, pos_to_check.c, None)
                
                if in_check:
                    break
        
        return in_check

    def is_empty_spot(self, row, col):
        return self.get(row, col) is None

    # TODO: create wrapper for vertical/horizontal/diagonal where we pass
    # two Positions
    # TODO: merge with vertical
    # TODO: replace position by the r,c used
    def get_pieces_range_horizontal(self, origin : Position, end : Position):
        # TODO: rename variables
        
        move_to_right  = range(origin.c, end.c + 1)
        move_to_left = range(end.c, origin.c + 1)
        current_range = move_to_right if origin.c - end.c < 0 else move_to_left
        
        pieces = []
        for col in current_range:
            piece = self.get(origin.r, col)
            if piece is not None:
                pieces.append((piece, origin.r, col))

        # ensure the list always start from the piece within
        # origin and ends with the piece within the end
        if current_range == move_to_left:
            pieces.reverse()

        return pieces

    def get_pieces_range_vertical(self, origin : Position, end : Position):
        trying_to_move_horizontally = origin.r - end.r < 0 and origin.c - end.c < 0
        if trying_to_move_horizontally:
            return []
        
        descend = range(origin.r, end.r + 1)
        ascend = range(end.r, origin.r + 1)
        current_range = descend if origin.r - end.r < 0 else ascend
        
        pieces = []
        for row in current_range:
            piece = self.get(row, origin.c)
            if piece is not None:
                pieces.append((piece, row, origin.c))
        
        if current_range == ascend:
            pieces.reverse()
        
        return pieces

    def get_pieces_range_diagonal(self, origin_r : int, origin_c : int, end_r : int, end_c : int):
        """ Returns a array of tuples with the coordinates from each piece and the piece itself whitin the (inclusive) range."""
        diff_r = origin_r - end_r 
        diff_c = origin_c - end_c
        abs_r = abs(diff_r) 
        abs_c = abs(diff_c)
        valid_diagonal = abs_r == abs_c

        if not valid_diagonal:
            return []
        
        pieces = []

        #nw(0,0)|ne(0,7)
        #ms(7,0)|se(7,7)
        increment_se = lambda row, col:(row+1, col+1)
        increment_ms = lambda row, col:(row+1, col-1)
        increment_nw = lambda row, col:(row-1, col-1)
        increment_ne = lambda row, col:(row-1, col+1)
        equals = lambda x1, y1, x2, y2: x1 == x2 and y1 == y2

        current = None
        if diff_r == diff_c and diff_r > 0:
            current = increment_nw
        elif diff_r == diff_c and diff_r < 0:
            current = increment_se
        elif diff_r < 0 < diff_c and abs_r == abs_c:
            current = increment_ms
        else: # diff_c < 0 < diff_r and abs_r == abs_c:
            current = increment_ne

        def append(r, c):
            piece = self.get(r, c)
            if piece is not None:
                pieces.append((piece, r, c))
        
        r = origin_r
        c = origin_c
        while not equals(r, c, end_r, end_c):
            append(r, c)
            r , c = current(r, c)
        # since we're inclusive (start..end)
        else: 
            append(end_r, end_c)
     
        return pieces

    def iterate_material(self, color : Color):
        for row, col, p in self._iterate():
            if p and p.color == color:
                yield p, Position(row, col)

    def _iterate(self):
         for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                yield row, col, self.get(row, col)

    def _remove_piece(self, piece):
        pass

    def _make_board(self):
        self._board[0][0] = Rook(Color.BLACK)
        self._board[0][1] = Knight(Color.BLACK)
        self._board[0][2] = Bishop(Color.BLACK)
        self._board[0][3] = Queen(Color.BLACK)
        self._board[0][4] = King(Color.BLACK)
        self._board[0][5] = Bishop(Color.BLACK)
        self._board[0][6] = Knight(Color.BLACK)
        self._board[0][7] = Rook(Color.BLACK)
        self._board[1][0] = Pawn(Color.BLACK)
        self._board[1][1] = Pawn(Color.BLACK)
        self._board[1][2] = Pawn(Color.BLACK)
        self._board[1][3] = Pawn(Color.BLACK)
        self._board[1][4] = Pawn(Color.BLACK)
        self._board[1][5] = Pawn(Color.BLACK)
        self._board[1][6] = Pawn(Color.BLACK)
        self._board[1][7] = Pawn(Color.BLACK)

        self._board[7][0] = Rook(Color.WHITE)
        self._board[7][1] = Knight(Color.WHITE)
        self._board[7][2] = Bishop(Color.WHITE)
        self._board[7][3] = Queen(Color.WHITE)
        self._board[7][4] = King(Color.WHITE)
        self._board[7][5] = Bishop(Color.WHITE)
        self._board[7][6] = Knight(Color.WHITE)
        self._board[7][7] = Rook(Color.WHITE)
        self._board[6][0] = Pawn(Color.WHITE)
        self._board[6][1] = Pawn(Color.WHITE)
        self._board[6][2] = Pawn(Color.WHITE)
        self._board[6][3] = Pawn(Color.WHITE)
        self._board[6][4] = Pawn(Color.WHITE)
        self._board[6][5] = Pawn(Color.WHITE)
        self._board[6][6] = Pawn(Color.WHITE)
        self._board[6][7] = Pawn(Color.WHITE)
