from pieces.Piece import Piece

class Queen(Piece):

    def __init__(self, position, color, symbol='Qu', movementRule = None):
        Piece.__init__(self, position, color, symbol, movementRule)