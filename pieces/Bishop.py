from pieces.Piece import Piece

class Bishop(Piece):

    def __init__(self, position, color, symbol='bi', movementRule = None):
        Piece.__init__(self, position, color, symbol)
        self.movementRule = movementRule