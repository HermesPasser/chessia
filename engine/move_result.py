from io import StringIO
from engine.position import Position

class MoveResultBase:
    
    def set_succeed(self, succeed):
        self.succeed = succeed
        return self

    def __bool__(self):
        return self.succeed
    
    __nonzero__ = __bool__

    def __eq__(self, other):
        return bool(self) == other


class MoveResult(MoveResultBase):
    def __init__(self, piece, from_pos, to_pos, was_first_move):
        self.piece = piece
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.was_first_move = was_first_move
        self.succeed = False
        self.captured = None
        self.captured_position = None
        self.should_promote = False
        self.promoted_to = None
    
    def capture(self, piece, position):
        self.captured = piece
        self.captured_position = position
        return self

    def __repr__(self):
        captured = f", capured: {self.captured}" if self.captured is not None else ''
        return f"MoveResult({self.succeed}{captured})"

    def __str__(self):
        io = StringIO()
        io.write(f"[{type(self).__name__}:")
        io.write(f"{self.piece} ")
        io.write('moved' if self.succeed else 'failed to move from')
        io.write(f" {self.from_pos} -> {self.to_pos}")
        if self.captured:
            io.write(f", and capured {self.captured} on {self.captured_position}")
        io.write(f"]")
        val = io.getvalue()
        io.close()
        return val

class CastlingMoveResult(MoveResultBase):
    def __init__(self):
        self.succeed = True
        self.king_final_pos = None
        self.king_pos = None
    
    @staticmethod
    def from_move_result(result):
        castling = CastlingMoveResult()
        castling.succeed = result.succeed
        castling.set_moved_piece(result.from_pos, result.to_pos)
        return castling

    def set_moved_piece(self, from_pos, to_pos):
        self.king_pos = from_pos
        self.rook_pos = to_pos

        if self.king_pos.c - self.rook_pos.c == 4: # long castling
            self.king_final_pos = Position(self.king_pos.r, self.king_pos.c - 2)
            self.rook_final_pos = Position(self.king_pos.r, self.king_pos.c - 1)
        else:
            self.king_final_pos = Position(self.king_pos.r, self.king_pos.c + 2)
            self.rook_final_pos = Position(self.king_pos.r, self.king_pos.c + 1)
