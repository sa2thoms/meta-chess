from pieces.Piece import Piece

class Queen(Piece):
    movementRule = None

    def __init__(self, position, idNumber, color, symbol='Qu', movementRule = None):
        Piece.__init__(self, position, idNumber, color, symbol)
        self.movementRule = movementRule