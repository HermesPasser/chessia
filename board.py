from utils import make_2d_array
from color import Color
from pieces import *
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
        for _, y, p in self._iterate():
            p = '=' if p is None else str(p)
            sio.write(p)
            
            if y == Board.SIZE -1:
                sio.write("\n")
        s = sio.getvalue()
        sio.close()
        return s.strip()

    def get(self, x: int, y: int):
        if x < 0 or x >= Board.SIZE or y < 0 or y >= Board.SIZE:
            raise Exception("Index out of bound")

        return self._board[x][y]

    def set(self, x: int, y: int, piece : Piece):
        if x < 0 or x >= Board.SIZE or y < 0 or y >= Board.SIZE:
            raise Exception("Index out of bound")

        if isinstance(piece, King):
            if piece.color == Color.WHITE:
                self.white_king_loc = Position(x, y)
            else:
                self.black_king_loc = Position(x, y)
        
        self._board[x][y] = piece

    def move(self, from_pos : Position, to_pos : Position): 
        prev = self._board[from_pos.x][from_pos.y]
        
        if isinstance(self._board[to_pos.x][to_pos.y], King):
            raise Exception("Can't override the king")

        self._board[to_pos.x][to_pos.y] = prev
        self._board[from_pos.x][from_pos.y] = None

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
                
        for x, y, p in self._iterate():
            if type(p) is type_piece and p.color == color:
                return Position(x, y)

        raise Exception(f"No {color} {type_piece.__name__} found")

    def in_check(self, color):
        return self.is_square_in_check(color, self.get_king_loc_by_color(color))

    # TODO: do we really need to let it here? Game and King
    # make sense having it but it deals with the internals 
    # of the board.
    def is_square_in_check(self, color, pos_to_check : Position):
        is_empty_spot = self.is_empty_spot(pos_to_check.x, pos_to_check.y)
        other_player_color = color.reverse()
       
        in_check = False
        for piece, pos in self.iterate_material(color):
            if piece is not None and piece.color == other_player_color:                 
                clear_spot = False

                # Remember: the pawn eats diagonally and moves vertically
                if isinstance(piece, Pawn) and is_empty_spot:
                    clear_spot = True
                    self.set(pos_to_check.x, pos_to_check.y, Pawn(color))
                
                if piece.can_move(self, pos, pos_to_check):
                    in_check = True

                if clear_spot:
                    self.set(pos_to_check.x, pos_to_check.y, None)
                
                if in_check:
                    break
        
        return in_check

    def is_empty_spot(self, x, y):
        return self.get(x, y) is None

    # TODO: create wrapper for vertical/horizontal/diagonal where we pass
    # two Positions
    # TODO: merge with vertical
    # TODO: replace position by the x,y used
    def get_pieces_range_horizontal(self, origin : Position, end : Position):
        # TODO: rename variables
        
        move_to_right  = range(origin.y, end.y + 1)
        move_to_left = range(end.y, origin.y + 1)
        current_range = move_to_right if origin.y - end.y < 0 else move_to_left
        
        pieces = []
        for y in current_range:
            piece = self.get(origin.x, y)
            if piece is not None:
                pieces.append((piece, origin.x, y))

        # ensure the list always start from the piece within
        # origin and ends with the piece within the end
        if current_range == move_to_left:
            pieces.reverse()

        return pieces

    def get_pieces_range_vertical(self, origin : Position, end : Position):
        trying_to_move_horizontally = origin.x - end.x < 0 and origin.y - end.y < 0
        if trying_to_move_horizontally:
            return []
        
        descend = range(origin.x, end.x + 1)
        ascend = range(end.x, origin.x + 1)
        current_range = descend if origin.x - end.x < 0 else ascend
        
        pieces = []
        for x in current_range:
            piece = self.get(x, origin.y)
            if piece is not None:
                pieces.append((piece, x, origin.y))
        
        if current_range == ascend:
            pieces.reverse()
        
        return pieces

    def get_pieces_range_diagonal(self, origin_x : int, origin_y : int, end_x : int, end_y : int):
        """ Returns a array of tuples with the coordinates from each piece and the piece itself whitin the (inclusive) range."""
        diff_x = origin_x - end_x 
        diff_y = origin_y - end_y
        abs_x = abs(diff_x) 
        abs_y = abs(diff_y)
        valid_diagonal = abs_x == abs_y

        if not valid_diagonal:
            return []
        
        pieces = []

        #nw(0,0)|ne(0,7)
        #ms(7,0)|se(7,7)
        increment_se = lambda x, y:(x+1, y+1)
        increment_ms = lambda x, y:(x+1, y-1)
        increment_nw = lambda x, y:(x-1, y-1)
        increment_ne = lambda x, y:(x-1, y+1)
        equals = lambda x1, y1, x2, y2: x1 == x2 and y1 == y2

        current = None
        if diff_x == diff_y and diff_x > 0:
            current = increment_nw
        elif diff_x == diff_y and diff_x < 0:
            current = increment_se
        elif diff_x < 0 < diff_y and abs_x == abs_y:
            current = increment_ms
        else: # diff_y < 0 < diff_x and abs_x == abs_y:
            current = increment_ne

        def append(x, y):
            piece = self.get(x, y)
            if piece is not None:
                pieces.append((piece, x, y))
        
        x = origin_x
        y = origin_y
        while not equals(x, y, end_x, end_y):
            append(x, y)
            x , y = current(x, y)
        # since we're inclusive (start..end)
        else: 
            append(end_x, end_y)
     
        return pieces

    def iterate_material(self, color : Color):
        for x, y, p in self._iterate():
            if p and p.color == color:
                yield p, Position(x, y)

    def _iterate(self):
         for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                yield x, y, self.get(x, y)

    def _remove_piece(self, piece):
        pass

    def _make_board(self):
        # FIXME: the acess is [y][x] so i should rename in the other places
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
