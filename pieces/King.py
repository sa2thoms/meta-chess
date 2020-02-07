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
        elif self.position == Square(7 * self.color, 4) and square.rank == self.position.rank and abs(square.file - self.position.file) == 2:
            return True
        else:
            return False
        
    def fullCopy(self):
        position_copy = None if self.position == None else self.position.fullCopy()
        return King(position_copy, self.color, self.symbol)

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

        if self.position == Square(4, 7 * self.color):
            moves.append(Move(self.position, Square(self.position.file - 2, self.position.rank)))
            moves.append(Move(self.position, Square(self.position.file + 2, self.position.rank)))
        
        return moves

    def pointValue(self):
        return 65536.0