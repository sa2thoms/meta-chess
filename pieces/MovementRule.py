from Square import Square
from Move import Move

class MovementRule:

    def __init__(self, vert = False, horiz = False, diag = False, jumps = []):
        self.allowsVerticalCartesian = vert
        self.allowsHorizontalCartesian = horiz
        self.allowsDiagonal = diag
        self.jumpRules = jumps

        self._pointValue = self._calculatePointValue()

    def fullCopy(self):
        return MovementRule(self.allowsVerticalCartesian, self.allowsHorizontalCartesian, self.allowsDiagonal, self.jumpRules)

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

    def allAttackingMoves(self, startSquare, game):
        allMoves = []
        for f in range(0, 8):
            for r in range(0, 8):
                endSquare = Square(f, r)
                if startSquare != endSquare:
                    move = Move(startSquare, endSquare)
                    if self.isAttacking(move, game):
                        allMoves.append(move)
        return allMoves

    def _calculatePointValue(self):
        total = 0.0

        if self.allowsVerticalCartesian or self.allowsHorizontalCartesian:
            total += 2.0
            if self.allowsVerticalCartesian and self.allowsHorizontalCartesian:
                total += 3.0
        
        if self.allowsDiagonal:
            total += 3.0 + (total / 5.0)

        for jumpRule in self.jumpRules:
            if jumpRule[0] == 0 or jumpRule[1] == 0:
                total += 1.0 + (total / 10.0)
            elif jumpRule[0] == jumpRule[1]:
                total += 1.0 + (total / 10.0)
            elif jumpRule[0] <= 3 and jumpRule[1] <= 3:
                total += 3.0 + (total / 5.0)
            else:
                total += 1.5 + (total / 10.0)
        
        return total

    def pointValue(self, square):
        total = self._pointValue
        if abs(3.5 - square.file) < 2.0 and abs(3.5 - square.rank) < 2.0:
            total += 0.3 + (total * 0.05)
        
        return total