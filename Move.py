from Square import Square

class Move:
    def __init__(self, startSquare, endSquare):
        assert not endSquare == startSquare

        self.start = startSquare
        self.end = endSquare

    def fullCopy(self):
        return Move(self.start, self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __str__(self):
        return str(self.start) + " to " + str(self.end)

    def __repr__(self):
        return str(self)
