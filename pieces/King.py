from pieces.Piece import Piece

class King(Piece):

    def __init__(self, position, color, symbol='Ki'):
        Piece.__init__(self, position, color, symbol, None)

    def isAttacking(self, square, game = None):
        if square == self.position:
            return False
        elif abs(self.position.rank - square.rank) <= 1 and abs(self.position.file - square.file) <= 1:
            return True
        else:
            return False