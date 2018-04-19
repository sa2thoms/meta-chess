from pieces.Piece import Piece

class Pawn(Piece):

    def __init__(self, position, color, symbol='pa'):
        Piece.__init__(self, position, color, symbol, None)

    def isAttacking(self, square, game):
        if self.taken:
            return False
        if self.color == game.COLOR_WHITE:
            if game.getPiece(square) == None:
                if square.rank == self.position.rank + 1 and square.file == self.position.file:
                    return True
                elif square.rank == self.position.rank + 2 and square.file == self.position.file and self.position.rank == 1:
                    return True
                else:
                    return False
            elif game.getPiece(square).color != self.color:
                if square.rank == self.position.rank + 1 and abs(square.file - self.position.file) == 1:
                    return True
                else:
                    return False
            else:
                return False
        elif self.color == game.COLOR_BLACK:
            if game.getPiece(square) == None:
                if square.rank == self.position.rank - 1 and square.file == self.position.file:
                    return True
                elif square.rank == self.position.rank - 2 and square.file == self.position.file and self.position.rank == 6:
                    return True
                else:
                    return False
            elif game.getPiece(square).color != self.color:
                if square.rank == self.position.rank - 1 and abs(square.file - self.position.file) == 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise Exception('The piece has no valid color. It is impossible to check the validity of an attack')

    def allAttackingMoves(self, game):
        if self.taken:
            return []
        elif self.color == Game.COLOR_WHITE:
            moves = []
            startFile = max([0, self.position.file - 1])
            endFile = min([7, self.position.file + 1])
            if self.position.rank < 8:
                for f in range(startFile, endFile + 1):
                    moves.append(Move(self.position, Square(f, self.position.rank + 1)))
                if self.position.rank == 1:
                    moves.append(Move(self.position, Square(self.position.file, self.position.rank + 2)))
            return filter((lambda m: self.isAttacking(m.end, game)), moves)
        elif self.color == Game.COLOR_BLACK:
            moves = []
            startFile = max([0, self.position.file - 1])
            endFile = min([7, self.position.file + 1])
            if self.position.rank > 0:
                for f in range(startFile, endFile - 1):
                    moves.append(Move(self.position, Square(f, self.position.rank - 1)))
                if self.position.rank == 6:
                    moves.append(Move(self.position, Square(self.position.file, self.position.rank - 2)))
            return filter((lambda m: self.isAttacking(m.end, game)), moves)

    def pointValue(self):
        if self.color == Game.COLOR_WHITE:
            return 0.8 + 0.2 * self.position.rank
        else:
            return 0.8 + 0.2 * (7 - self.position.rank)
    