import Piece

class Queen(Piece):
    movementRule

    def __init__(self, position = None, idNumber, color, symbol='Qu', movementRule = None):
        Piece.__init__(self, position, idNumber, color, symbol)
        self.movementRule = movementRule