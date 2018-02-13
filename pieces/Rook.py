import pieces.Piece

class Rook(Piece):
    movementRule

    def __init__(self, position, idNumber, color, symbol='ro', movementRule = None):
        Piece.__init__(self, position, idNumber, color, symbol)
        self.movementRule = movementRule