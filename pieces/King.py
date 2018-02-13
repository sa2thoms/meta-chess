import Piece

class King(Piece):
    def __init__(self, position = None, idNumber, color, symbol='Ki'):
        Piece.__init__(self, position, idNumber, color, symbol)
        