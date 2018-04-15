from Square import Square
from Move import Move

class MovementRule:

    def __init__(self, vert = False, horiz = False, diag = False, jumps = []):
        self.allowsVerticalCartesian = vert
        self.allowsHorizontalCartesian = horiz
        self.allowsDiagonal = diag
        self.jumpRules = jumps

    def _moveConformsToJumpRules(self, move):
        for jumpRule in self.jumpRules:
            if (jumpRule[0] == abs(move.end.file - move.start.file) and jumpRule[1] == abs(move.end.rank - move.start.rank)):
                return True
            if (jumpRule[1] == abs(move.end.file - move.start.file) and jumpRule[0] == abs(move.end.rank - move.start.rank)):
                return True
        return False

    def _signOf(self, a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return None

    def isAttacking(self, move, game):
        if self._moveConformsToJumpRules(move):
            return True
        elif move.end.file == move.start.file and self.allowsVerticalCartesian:
            dist = move.end.rank - move.start.rank
            step = self._signOf(dist)
            for r in range(move.start.rank + step, move.end.rank, step):
                if (game.getPiece(Square(move.start.file, r))):
                    return False
            return True
        elif move.end.rank == move.start.rank and self.allowsHorizontalCartesian:
            dist = move.end.file - move.start.file
            step = self._signOf(dist)
            for f in range(move.start.file + step, move.end.file, step):
                if (game.getPiece(Square(f, move.start.rank))):
                    return False
            return True
        elif abs(move.end.file - move.start.file) == abs(move.end.rank - move.start.rank) and self.allowsDiagonal:
            fdist = move.end.file - move.start.file
            fstep = self._signOf(fdist)
            fcount = move.start.file + fstep

            rdist = move.end.rank - move.start.rank
            rstep = self._signOf(rdist)
            rcount = move.start.rank + rstep

            for i in range(1, abs(fdist)):
                if game.getPiece(Square(fcount, rcount)):
                    return False
                fcount += fstep
                rcount += rstep
            return True
        else:
            return False