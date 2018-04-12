from Square import Square

class Move:
    def __init__(self, startSquare, endSquare):
        assert isinstance(startSquare, Square)
        assert isinstance(endSquare, Square)

        self.start = startSquare
        self.end = endSquare

    def __eql__(self, other):
        return self.start == other.start and self.end == other.end
