from pieces.Piece import Piece

from Square import Square
from Move import Move

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

    def allAttackingMoves(self, game):
        startFile = max([0, self.position.file - 1])
        endFile = min([7, self.position.file + 1])
        startRank = max([0, self.position.rank - 1])
        endRank = min([7, self.position.rank + 1])

        moves = []

        for f in range(startFile, endFile + 1):
            for r in range(startRank, endRank + 1):
                square = Square(f, r)
                if square != self.position:
                    moves.append(Move(self.position, square))
        
        return moves

    def pointValue(self):
        return 65536.0