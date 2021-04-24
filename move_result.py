
class MoveResult:
    def __init__(self, succeed : bool, captured=None):
        """captured: (Piece, Position), optional"""
        self.succeed = succeed
        self.captured, self.captured_position = captured or (None, None)
    
    def __bool__(self):
        return self.succeed
    
    __nonzero__ = __bool__

    def __eq__(self, other):
        return bool(self) == other

    def __repr__(self):
        captured = f", capured: {self.captured}" if self.captured is not None else ''
        return f"MoveResult({self.succeed}{captured})"
                