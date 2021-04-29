from io import StringIO

class MoveResult:
    def __init__(self, succeed : bool, captured=None):
        """captured: (Piece, Position), optional"""
        self.succeed = succeed
        self.captured, self.captured_position = captured or (None, None)
    
    def set_moved_piece(self, piece, from_pos, to_pos, was_first_move):
        self.piece = piece
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.was_first_move = was_first_move

    def __bool__(self):
        return self.succeed
    
    __nonzero__ = __bool__

    def __eq__(self, other):
        return bool(self) == other

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
            io.write(f", and {self.captured} capured on {self.captured_position}")
        io.write(f"]")
        val = io.getvalue()
        io.close()
        return val

                