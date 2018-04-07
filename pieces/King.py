from pieces.Piece import Piece

class King(Piece):

    def __init__(self, position, color, symbol='Ki'):
        Piece.__init__(self, position, color, symbol)

    def isAttacking(self, square, game = None):
        if abs(self.position.rank - square.rank) == 1 or abs(self.position.file - square.file) == 1:
            return True
        else:
            return False