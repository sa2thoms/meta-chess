from pieces.Piece import Piece

class Knight(Piece):

    def __init__(self, position, color, symbol='kn', movementRule = None):
        Piece.__init__(self, position, color, symbol, movementRule)