from pieces.Piece import Piece

class Knight(Piece):
    movementRule = None

    def __init__(self, position, idNumber, color, symbol='kn', movementRule = None):
        Piece.__init__(self, position, idNumber, color, symbol)
        self.movementRule = movementRule