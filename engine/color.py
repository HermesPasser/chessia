from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 2

    def reverse(self):
        """Return the other color."""
        return Color.BLACK if self == Color.WHITE else Color.WHITE 
