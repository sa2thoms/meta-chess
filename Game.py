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

    def __init__(self, ruleSet = None):
        self.ruleSet = ruleSet

    def loadPieces(self):
        if (self.ruleSet == None):
            raise NoRuleException('There is no rule set from which to load the game')

        self.whitePieces = []
        self.blackPieces = []

        for i in range(0, 8):
            whitePieces.append(Pawn(position=[i, 1], idNumber=i))

        whitePieces.append(Rook(position=[0, 0], idNumber=8, movementRule=self.ruleSet.rookMovement))
        whitePieces.append(Knight(position=[1, 0], idNumber=9, movementRule=self.ruleSet.knightMovement))
        whitePieces.append(Bishop(position=[2, 0], idNumber=10, movementRule=self.ruleSet.bishopMovement))
        