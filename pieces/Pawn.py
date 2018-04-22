from pieces.Piece import Piece

from Square import Square
from Move import Move

from color import WHITE, BLACK

class Pawn(Piece):

    def __init__(self, position, color, symbol='pa'):
        Piece.__init__(self, position, color, symbol, None)

    def isAttacking(self, square, game):
        if self.taken:
            return False

        forward = 1
        startRank = 1
        if self.color == BLACK:
            forward = -1
            startRank = 6
        
        if game.getPiece(square) == None:
            if square.rank == self.position.rank + forward and square.file == self.position.file:
                return True
            elif square.rank == self.position.rank + (forward * 2) and square.file == self.position.file and self.position.rank == startRank:
                return True
            else:
                return False
        elif game.getPiece(square).color != self.color:
            if square.rank == self.position.rank + forward and abs(square.file - self.position.file) == 1:
                return True
            else:
                return False
        else:
            return False

    def allAttackingMoves(self, game):
        if self.taken:
            return []
        elif self.color == WHITE:
            moves = []
            startFile = max([0, self.position.file - 1])
            endFile = min([7, self.position.file + 1])
            if self.position.rank < 8:
                for f in range(startFile, endFile + 1):
                    moves.append(Move(self.position, Square(f, self.position.rank + 1)))
                if self.position.rank == 1:
                    moves.append(Move(self.position, Square(self.position.file, self.position.rank + 2)))
            return filter((lambda m: self.isAttacking(m.end, game)), moves)
        elif self.color == BLACK:
            moves = []
            startFile = max([0, self.position.file - 1])
            endFile = min([7, self.position.file + 1])
            if self.position.rank > 0:
                for f in range(startFile, endFile + 1):
                    moves.append(Move(self.position, Square(f, self.position.rank - 1)))
                if self.position.rank == 6:
                    moves.append(Move(self.position, Square(self.position.file, self.position.rank - 2)))
            return filter((lambda m: self.isAttacking(m.end, game)), moves)

    def pointValue(self):
        if self.color == WHITE:
            return 0.8 + 0.2 * self.position.rank
        else:
            return 0.8 + 0.2 * (7 - self.position.rank)
    