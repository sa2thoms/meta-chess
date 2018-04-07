from pieces.Piece import Piece

class Pawn(Piece):

    def __init__(self, position, color, symbol='pa'):
        Piece.__init__(self, position, color, symbol)

    def isAttacking(self, square, game):
        if self.color == game.COLOR_WHITE:
            if game.getPiece(square).color != self.color:
                if square.rank == self.position.rank + 1 and abs(square.file - self.position.file) == 1:
                    return True
                else:
                    return False
            elif game.getPiece(square) == None:
                if square.rank == self.position.rank + 1 and square.file == self.position.file:
                    return True
                elif square.rank == self.position.rank + 2 and square.file == self.position.file and self.position.rank == 1:
                    return True
                else:
                    return False
            else:
                return False
        elif self.color == game.COLOR_BLACK:
            if game.getPiece(square).color != self.color:
                if square.rank == self.position.rank - 1 and abs(square.file - self.position.file) == 1:
                    return True
                else:
                    return False
            elif game.getPiece(square) == None:
                if square.rank == self.position.rank - 1 and square.file == self.position.file:
                    return True
                elif square.rank == self.position.rank - 2 and square.file == self.position.file and self.position.rank == 6:
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise Exception('The piece has no valid color. It is impossible to check the validity of an attack')