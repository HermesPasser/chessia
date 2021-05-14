class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x}x{self.y}"

    def __eq__(self, o):
        if type(o) is not Position:
            return False
        return self.x == o.x and self.y == o.y
