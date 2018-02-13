import Piece

class Knight(Piece):
    movementRule

    def __init__(self, position = None, idNumber, color, symbol='kn', movementRule = None):
        Piece.__init__(self, position, idNumber, color, symbol)
        self.movementRule = movementRule