from pieces.Piece import Piece

class Rook(Piece):

    def __init__(self, position, color, symbol='ro', movementRule = None):
        Piece.__init__(self, position, color, symbol)
        self.movementRule = movementRule