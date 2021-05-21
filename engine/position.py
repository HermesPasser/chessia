class Position():
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __repr__(self):
        return f"{self.r}x{self.c}"

    def __eq__(self, o):
        if type(o) is not Position:
            return False
        return self.r == o.r and self.c == o.c
