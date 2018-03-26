from pieces.Piece import Piece

class King(Piece):

    def __init__(self, position, color, symbol='Ki'):
        Piece.__init__(self, position, color, symbol)

    def isAttacking(self, square):
        