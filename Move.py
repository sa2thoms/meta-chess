from Square import Square

class Move:
    def __init__(self, startSquare, endSquare):
        assert isinstance(startSquare, Square)
        assert isinstance(endSquare, Square)

        self.start = startSquare
        self.end = endSquare
