from Square import Square

class Move:
    def __init__(self, startSquare, endSquare):
        assert isinstance(startSquare, Square)
        assert isinstance(endSquare, Square)
        assert not endSquare == startSquare

        self.start = startSquare
        self.end = endSquare

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
