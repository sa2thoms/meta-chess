import RuleSet
import Piece
import Pawn
import King
import Queen
import Rook
import Knight
import Bishop
import NoRuleException

class Game:
    ruleSet
    whitePieces
    blackPieces

    COLOR_WHITE = 0
    COLOR_BLACK = 1

    def __init__(self, ruleSet = None):
        self.ruleSet = ruleSet

    def loadPieces(self):
        if (self.ruleSet == None):
            raise NoRuleException('There is no rule set from which to load the game')

        if (self.whitePieces.count() == 0 and self.blackPieces.count() == 0):
            raise Exception('Game is already loaded')

        self.whitePieces = []
        self.blackPieces = []

        for i in range(0, 8):
            whitePieces.append(Pawn(position=[i, 1], idNumber=i, COLOR_WHITE))
            blackPieces.append(Pawn(position=[i, 6], idNumber=i, COLOR_BLACK))

        self._loadPowerPieces(self.COLOR_WHITE)
        self._loadPowerPieces(self.COLOR_BLACK)

    def _loadPowerPieces(self, color):
        row = color * 7
        teamList = self.whitePieces
        if color == self.COLOR_BLACK:
            teamList = self.blackPieces

        teamList.append(Rook(position=[0, row], idNumber=8, color=color, movementRule=self.ruleSet.rookMovement))
        teamList.append(Knight(position=[1, row], idNumber=9, color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Bishop(position=[2, row], idNumber=10, color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Queen(position=[3, row], idNumber=11, color=color, movementRule=self.ruleSet.queenMovement))
        teamList.append(King(position=[4, row], idNumber=12, color=color))
        teamList.append(Bishop(position=[5, row], idNumber=13, color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Knight(position=[6, row], idNumber=14, color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Rook(position=[7, row], idNumber=15, color=color, movementRule=self.ruleSet.rookMovement))