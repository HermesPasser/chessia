from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 2

    def __str__(self):
        return 'white' if self == Color.WHITE else 'black'

    def reverse(self):
        """Return the other color."""
        return Color.BLACK if self == Color.WHITE else Color.WHITE

    def is_white(self):
        return self == Color.WHITE

    def is_black(self):
        return not self.is_white()
